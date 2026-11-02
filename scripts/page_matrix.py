#!/usr/bin/env python3
"""page_matrix.py — 8 类页面覆盖矩阵探测.

用法:
  claude-geo run page_matrix.py <url> [--industry saas|ecommerce|education|local|b2b|media] [--out file.json]

每类页面探测一组候选路径 + 从 sitemap 里按关键词匹配,输出「独立URL/锚点/未发现」矩阵。
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"

PAGE_TYPES = ["home", "about", "product_service", "faq_help", "case_testimonial",
              "news_blog", "contact", "privacy_legal"]

COMMON_PATHS = {
    "about": ["/about", "/about-us", "/company", "/gioi-thieu", "/legal/about"],
    "product_service": ["/pricing", "/products", "/services", "/features", "/apis", "/explore"],
    "faq_help": ["/faq", "/faqs", "/help", "/support", "/docs", "/cau-hoi-thuong-gap"],
    "case_testimonial": ["/cases", "/case-studies", "/customers", "/testimonials", "/use-cases"],
    "news_blog": ["/blog", "/news", "/articles", "/updates", "/changelog", "/tin-tuc", "/wiki"],
    "contact": ["/contact", "/contact-us", "/lien-he"],
    "privacy_legal": ["/privacy", "/privacy-policy", "/terms", "/terms-of-service", "/legal",
                      "/chinh-sach-bao-mat", "/chinh-sach", "/bao-mat", "/dieu-khoan-su-dung",
                      "/dieu-khoan", "/chinh-sach-thanh-toan-hoan-phi"],
}

SITEMAP_KEYWORDS = {
    "about": ["about", "company", "gioi-thieu"],
    "product_service": ["pricing", "product", "service", "feature"],
    "faq_help": ["faq", "help", "support", "question"],
    "case_testimonial": ["case", "customer", "testimonial", "use-case"],
    "news_blog": ["blog", "news", "article", "update", "changelog"],
    "contact": ["contact", "lien-he"],
    "privacy_legal": ["privacy", "terms", "legal", "policy", "dieu-khoan"],
}


def fetch_status(url: str) -> dict:
    try:
        r = requests.get(url, timeout=15, allow_redirects=True, headers={"User-Agent": UA})
        ct = r.headers.get("content-type", "")
        return {"url": url, "status": r.status_code, "final_url": r.url,
                "is_html": "html" in ct, "bytes": len(r.text)}
    except requests.RequestException as e:
        return {"url": url, "error": str(e)[:100]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--industry", default="generic")
    ap.add_argument("--out")
    args = ap.parse_args()
    url = args.url if re.match(r"^https?://", args.url) else "https://" + args.url
    url = url.rstrip("/")
    host = urlparse(url).netloc

    # sitemap URLs
    sm_urls = []
    try:
        r = requests.get(url + "/sitemap.xml", timeout=15, headers={"User-Agent": UA})
        if r.status_code == 200:
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
            if locs and "<sitemapindex" in r.text:
                for sub in locs[:5]:
                    try:
                        r2 = requests.get(sub, timeout=15, headers={"User-Agent": UA})
                        sm_urls.extend(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r2.text)[:5000])
                    except requests.RequestException:
                        pass
            else:
                sm_urls = locs[:5000]
    except requests.RequestException:
        pass

    matrix = {}
    matrix["home"] = {"probes": [fetch_status(url + "/")], "sitemap_hits": [url + "/"]}
    for ptype in PAGE_TYPES[1:]:
        probes = [fetch_status(url + p) for p in COMMON_PATHS.get(ptype, [])]
        # sitemap keyword match (host-only)
        kw = SITEMAP_KEYWORDS.get(ptype, [])
        hits = [u for u in sm_urls if any(k in u.lower() for k in kw)][:10]
        ok_200_html = [p for p in probes if p.get("status") == 200 and p.get("is_html")]
        if ok_200_html or hits:
            status = "independent-url"
            evidence = (ok_200_html[0]["url"] if ok_200_html else None, hits[:3])
        else:
            any_200 = [p for p in probes if p.get("status") == 200]
            status = "anchor-or-none"
            evidence = (any_200[0]["url"] if any_200 else None, [])
        matrix[ptype] = {"status": status,
                         "probed": [p for p in probes if p.get("status") or p.get("error")],
                         "sitemap_hits": hits,
                         "evidence": {"path": evidence[0], "sitemap": evidence[1]}}

    result = {
        "target": url, "industry_hint": args.industry,
        "sitemap_url_count": len(sm_urls),
        "matrix": matrix,
        "coverage": {t: (m["status"] if t != "home" else "independent-url") for t, m in matrix.items()},
    }
    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"saved -> {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
