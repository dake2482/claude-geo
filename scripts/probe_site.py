#!/usr/bin/env python3
"""probe_site.py — claude-geo 证据采集主脚本.

用法:
  claude-geo run probe_site.py <url> [--out file.json] [--ua UA] [--timeout 20]

输出单份 JSON 证据包(键名即 EV 台账科目),覆盖:
  redirects / homepage(headers, meta, content stats) / robots / sitemap /
  llms_txt / soft404 / security_headers
"""
import argparse
import hashlib
import json
import random
import re
import string
import sys
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
AI_UAS = [
    "GPTBot/1.0 (+https://openai.com/gptbot)",
    "OAI-SearchBot/1.0; +https://openai.com/searchbot",
    "ClaudeBot/1.0 (+claudebot@anthropic.com)",
    "PerplexityBot/1.0 (+https://perplexity.ai/perplexitybot)",
]


def norm_url(u: str) -> str:
    if not re.match(r"^https?://", u):
        u = "https://" + u
    return u.rstrip("/")


def fetch(url: str, ua: str, timeout: int, allow_redirects=True):
    try:
        t0 = time.time()
        r = requests.get(
            url, timeout=timeout, allow_redirects=allow_redirects,
            headers={"User-Agent": ua, "Accept-Language": "en,zh;q=0.8"},
        )
        elapsed = round(time.time() - t0, 2)
        return {"ok": True, "status": r.status_code, "elapsed_s": elapsed,
                "final_url": r.url, "headers": dict(r.headers), "body": r.text,
                "content_type": r.headers.get("content-type", ""), "resp": r}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}


def md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8", "replace")).hexdigest()


def redirect_chain(scheme_host: str, timeout: int) -> dict:
    """http://host 与 www 变体的跳转链(不跟随,逐跳记录)。"""
    out = {}
    host = scheme_host
    for label, url in {
        "http_apex": "http://" + host,
        "https_www": "https://www." + host,
        "http_www": "http://www." + host,
    }.items():
        hops = []
        current = url
        for _ in range(5):
            try:
                r = requests.get(current, timeout=timeout, allow_redirects=False,
                                 headers={"User-Agent": UA})
                hops.append({"url": current, "status": r.status_code,
                             "location": r.headers.get("location")})
                if r.status_code in (301, 302, 303, 307, 308) and r.headers.get("location"):
                    current = urljoin(current, r.headers["location"])
                else:
                    break
            except requests.RequestException as e:
                hops.append({"url": current, "error": str(e)})
                break
        out[label] = hops
    return out


def parse_homepage(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    titles = [t.get_text(strip=True) for t in soup.find_all("title")]
    descs = [m.get("content", "").strip() for m in soup.find_all("meta", attrs={"name": "description"})]
    canonicals = [l["href"] for l in soup.find_all("link", rel="canonical") if l.get("href")]
    meta_robots = [m.get("content", "").strip() for m in soup.find_all("meta", attrs={"name": "robots"})]
    og = {m.get("property"): m.get("content") for m in soup.find_all("meta") if (m.get("property") or "").startswith("og:")}
    twitter = {m.get("name"): m.get("content") for m in soup.find_all("meta") if (m.get("name") or "").startswith("twitter:")}
    viewport = [m.get("content") for m in soup.find_all("meta", attrs={"name": "viewport"})]
    html_tag = soup.find("html")
    lang = html_tag.get("lang") if html_tag else None
    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    headings = {f"h{i}": len(soup.find_all(f"h{i}")) for i in range(1, 7)}
    imgs = soup.find_all("img")
    alt_nonempty = sum(1 for i in imgs if (i.get("alt") or "").strip())
    for a in soup.find_all("a", href=True):
        pass
    links = {"internal": set(), "external": set()}
    apex = urlparse(base_url).netloc
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        p = urlparse(href)
        if p.scheme not in ("http", "https"):
            continue
        if p.netloc == apex:
            links["internal"].add(href.split("#")[0])
        else:
            links["external"].add(href)
    text = soup.get_text(" ", strip=True)
    return {
        "titles": titles,
        "descriptions": descs,
        "canonicals": canonicals,
        "meta_robots": meta_robots,
        "html_lang": lang,
        "viewport": viewport,
        "og": og,
        "twitter": twitter,
        "h1": h1s,
        "heading_counts": headings,
        "img_total": len(imgs), "img_alt_nonempty": alt_nonempty,
        "img_alt_coverage": round(alt_nonempty / len(imgs), 3) if imgs else None,
        "tables": len(soup.find_all("table")),
        "ol": len(soup.find_all("ol")), "ul": len(soup.find_all("ul")),
        "details": len(soup.find_all("details")),
        "scripts_external": len(soup.find_all("script", src=True)),
        "jsonld_blocks": len(soup.find_all("script", type="application/ld+json")),
        "internal_links": sorted(links["internal"]),
        "external_links": sorted(links["external"]),
        "visible_text_chars": len(text),
        "visible_text_sample": text[:600],
    }


def parse_robots(text: str) -> dict:
    groups = {}
    current = "*"
    sitemap = None
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower()
        val = val.strip()
        if key == "user-agent":
            current = val
            groups.setdefault(current, {"allow": [], "disallow": [], "other": {}})
        elif key in ("allow", "disallow") and current in groups:
            groups[current][key].append(val)
        elif key == "sitemap":
            sitemap = val
        elif current in groups:
            groups[current]["other"][key] = val
    ai_rules = {ua: groups.get(ua) for ua in
                ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
                 "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "CCBot", "Bytespider")
                if ua in groups}
    content_signal_keys = [k for g in groups.values() for k in g["other"] if "content-signal" in k]
    star = groups.get("*", {"allow": [], "disallow": [], "other": {}})
    has_root_disallow = "/" in star["disallow"] or "" in star["disallow"]
    return {"groups": groups, "disallow_root": has_root_disallow,
            "disallow_root_allow_exceptions": star["allow"] if has_root_disallow else [],
            "sitemap": sitemap,
            "ai_ua_rules": ai_rules, "content_signals": content_signal_keys}


def parse_sitemap(text: str) -> dict:
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text)
    lastmods = re.findall(r"<lastmod>\s*([^<\s]+)\s*</lastmod>", text)
    is_index = "<sitemapindex" in text
    return {"url_count": len(locs), "is_index": is_index,
            "lastmod": {"count": len(lastmods),
                        "uniform": len(set(lastmods)) <= 1 if lastmods else None,
                        "values_sample": sorted(set(lastmods))[:3]},
            "locs_sample": locs[:20]}


def probe_soft404(home: str, timeout: int) -> dict:
    rnd = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    paths = [f"/this-page-does-not-exist-{rnd}",
             f"/nonexistent-{rnd}-xyz123",
             f"/zz-{rnd}-probe/tail"]
    results = []
    home_md5 = None
    base = fetch(home, UA, timeout)
    if base["ok"]:
        home_md5 = md5(base["body"])
    for p in paths:
        r = fetch(home.rstrip("/") + p, UA, timeout)
        if r["ok"]:
            results.append({"path": p, "status": r["status"], "content_type": r["content_type"],
                            "md5": md5(r["body"]), "same_as_home": md5(r["body"]) == home_md5 if home_md5 else None,
                            "is_html": "html" in r["content_type"]})
        else:
            results.append({"path": p, "error": r["error"]})
    soft = all(x.get("status") == 200 and x.get("is_html") for x in results if "status" in x)
    return {"home_md5": home_md5, "probes": results,
            "soft200": bool(soft and all(x.get("same_as_home") for x in results if "same_as_home" in x))}


SECURITY_HEADERS = ["strict-transport-security", "content-security-policy",
                    "x-frame-options", "x-content-type-options", "referrer-policy"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    url = norm_url(args.url)
    host = urlparse(url).netloc
    ev = {"target": url, "host": host, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}

    # 站点级文件(robots/sitemap/llms)一律挂在站点根,与输入路径无关
    origin = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    ev["redirects"] = redirect_chain(host, args.timeout)

    home = fetch(url, UA, args.timeout)
    if not home["ok"]:
        print(json.dumps({"target": url, "error": home["error"], "fatal": True}, ensure_ascii=False, indent=2))
        return 1
    home_md5 = md5(home["body"])
    ev["homepage"] = {
        "status": home["status"], "final_url": home["final_url"],
        "elapsed_s": home["elapsed_s"], "html_bytes": len(home["body"]),
        "content_type": home["content_type"],
        "server": home["headers"].get("server"),
        "alt_svc": home["headers"].get("alt-svc"),
        "security_headers": {h: home["headers"].get(h) for h in SECURITY_HEADERS},
        "cache_control": home["headers"].get("cache-control"),
        "md5": home_md5,
    }
    ev["homepage_meta"] = parse_homepage(home["body"], home["final_url"])

    robots = fetch(origin + "/robots.txt", UA, args.timeout)
    if robots["ok"]:
        ev["robots"] = {"status": robots["status"], "content_type": robots["content_type"],
                        "body": robots["body"][:4000], **parse_robots(robots["body"])}
    else:
        ev["robots"] = {"status": None, "error": robots["error"]}

    sm_url = (ev.get("robots", {}) or {}).get("sitemap") or (origin + "/sitemap.xml")
    sm = fetch(sm_url, UA, args.timeout)
    if sm["ok"] and "xml" in (sm["content_type"] or "") or (sm["ok"] and "<loc>" in sm["body"]):
        ev["sitemap"] = {"url": sm_url, "status": sm["status"], **parse_sitemap(sm["body"])}
    else:
        ev["sitemap"] = {"url": sm_url, "status": sm.get("status"), "error": sm.get("error"),
                         "note": "no sitemap or non-XML response"}

    llms = fetch(origin + "/llms.txt", UA, args.timeout)
    llms_full = fetch(origin + "/llms-full.txt", UA, args.timeout)
    def llms_state(r):
        if not r["ok"]:
            return {"state": "error", "error": r["error"]}
        if r["status"] == 404:
            return {"state": "not-deployed"}
        ct = r["content_type"] or ""
        if "html" in ct:
            same = md5(r["body"]) == home_md5
            return {"state": "fake-deployed" if same else "html-response",
                    "note": "200 but HTML (SPA fallback?) — treated as not deployed"}
        md_links = len(re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", r["body"]))
        return {"state": "deployed", "content_type": ct, "bytes": len(r["body"]),
                "markdown_links": md_links, "body_sample": r["body"][:800]}
    ev["llms_txt"] = {"status": llms.get("status"), **llms_state(llms)}
    ev["llms_full_txt"] = {"status": llms_full.get("status"), **llms_state(llms_full)}

    ev["soft404"] = probe_soft404(home["final_url"], args.timeout)

    ai_view = fetch(home["final_url"], AI_UAS[1], args.timeout)
    ev["ai_bot_view"] = {
        "ua": AI_UAS[1], "status": ai_view.get("status"),
        "same_md5_as_browser": md5(ai_view.get("body", "")) == home_md5 if ai_view.get("ok") else None,
    }

    out = json.dumps(ev, ensure_ascii=False, indent=2)
    if args.out:
        Path = __import__("pathlib").Path
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"saved -> {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
