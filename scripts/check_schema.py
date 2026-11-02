#!/usr/bin/env python3
"""check_schema.py — JSON-LD 实体清单与字段完整度分级.

用法:
  claude-geo run check_schema.py <url> [--out file.json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"

# 每类实体的关键字段与分档
ENTITY_FIELDS = {
    "Organization": {
        "skeleton": ["name", "url"],
        "core": ["logo", "sameAs", "address", "contactPoint"],
        "full": ["foundingDate", "description", "email", "telephone"],
    },
    "WebSite": {
        "skeleton": ["name", "url"],
        "core": ["inLanguage", "publisher"],
        "full": ["potentialAction"],  # SearchAction lives here
    },
    "Service": {"skeleton": ["name"], "core": ["provider", "offers"], "full": ["areaServed", "description"]},
    "Product": {"skeleton": ["name"], "core": ["offers", "image"], "full": ["brand", "description"]},
    "Course": {"skeleton": ["name", "description"], "core": ["provider", "hasCourseInstance"], "full": ["offers"]},
    "FAQPage": {"skeleton": ["mainEntity"], "core": ["mainEntity"], "full": []},
    "BreadcrumbList": {"skeleton": ["itemListElement"], "core": ["itemListElement"], "full": []},
    "Article": {"skeleton": ["headline"], "core": ["author", "datePublished", "publisher"], "full": ["dateModified", "image"]},
    "BlogPosting": {"skeleton": ["headline"], "core": ["author", "datePublished", "publisher"], "full": ["dateModified", "image"]},
    "Person": {"skeleton": ["name"], "core": ["url"], "full": ["affiliation", "sameAs"]},
}


def flatten_nodes(data):
    """展开 @graph / list / 单对象为节点列表。"""
    nodes = []
    if isinstance(data, dict):
        if "@graph" in data and isinstance(data["@graph"], list):
            nodes.extend(data["@graph"])
        else:
            nodes.append(data)
    elif isinstance(data, list):
        nodes.extend(data)
    return nodes


def node_types(node) -> list:
    t = node.get("@type", "")
    if isinstance(t, list):
        return [str(x) for x in t]
    return [str(t)] if t else []


def grade_entity(node_type: str, node: dict) -> dict:
    spec = ENTITY_FIELDS.get(node_type)
    if not spec:
        return {"type": node_type, "present_fields": sorted(k for k in node if not k.startswith("@"))[:15],
                "grade": "unknown-type"}
    def hit(fields):
        return [f for f in fields if f in node and node[f] not in (None, "", [], {})]
    sk, core, full = hit(spec["skeleton"]), hit(spec["core"]), hit(spec["full"])
    if full:
        grade = "full"
    elif core:
        grade = "core"
    elif sk:
        grade = "skeleton"
    else:
        grade = "empty"
    return {"type": node_type, "grade": grade,
            "fields_present": sk + core + full,
            "fields_missing_core": [f for f in spec["core"] if f not in sk + core + full],
            "fields_missing_full": [f for f in spec["full"] if f not in sk + core + full]}


def analyze_page(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    blocks = soup.find_all("script", type="application/ld+json")
    microdata = bool(soup.find(attrs={"itemscope": True}))
    page = {"jsonld_blocks": len(blocks), "microdata": microdata, "entities": [], "errors": []}
    faq_questions = 0
    for b in blocks:
        raw = b.string or b.get_text()
        try:
            data = json.loads(raw)
        except Exception as e:
            page["errors"].append(str(e)[:120])
            continue
        for node in flatten_nodes(data):
            types = node_types(node)
            for t in types:
                g = grade_entity(t, node)
                if t == "FAQPage":
                    me = node.get("mainEntity") or []
                    faq_questions += len(me)
                    g["faq_question_count"] = len(me)
                    answers = [q.get("acceptedAnswer", {}).get("text", "") for q in me if isinstance(q, dict)]
                    if answers:
                        g["faq_answer_chars"] = {"min": min(len(a) for a in answers),
                                                 "max": max(len(a) for a in answers)}
                page["entities"].append(g)
    page["faq_questions_total"] = faq_questions
    return page


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out")
    args = ap.parse_args()
    url = args.url if re.match(r"^https?://", args.url) else "https://" + args.url

    r = requests.get(url, timeout=20, headers={"User-Agent": UA})
    result = {"url": url, "http_status": r.status_code, **analyze_page(r.text)}

    summary = {}
    for e in result["entities"]:
        t = e["type"]
        rank = {"full": 3, "core": 2, "skeleton": 1, "empty": 0, "unknown-type": 1}
        if t not in summary or rank.get(e["grade"], 0) > rank.get(summary[t], 0):
            summary[t] = e["grade"]
    result["type_summary"] = summary
    result["schema_score_hint"] = {
        "zero": len(result["entities"]) == 0,
        "has_org": "Organization" in summary,
        "has_faqpage": "FAQPage" in summary,
        "has_breadcrumb": "BreadcrumbList" in summary,
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
