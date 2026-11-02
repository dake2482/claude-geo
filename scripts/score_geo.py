#!/usr/bin/env python3
"""score_geo.py — 7 维度加权总分计算(权重硬编码,禁止口算).

用法:
  claude-geo run score_geo.py --scores '{"technical":82,"onpage":66,"content":36,"discover":45,"understand":54,"entity":40,"citation":50}'
可选: --missing discover  (某维度缺数据,剔除后权重重归一化并披露)
"""
import argparse
import json
import sys

WEIGHTS = {
    "technical": ("技术可访问性", 0.15),
    "onpage": ("页面SEO质量", 0.15),
    "content": ("内容资产覆盖", 0.20),
    "discover": ("AI发现能力", 0.10),
    "understand": ("AI理解能力", 0.15),
    "entity": ("品牌与产品实体完整度", 0.15),
    "citation": ("AI引用资产潜力", 0.10),
}


def grade(total: float) -> str:
    if total >= 85:
        return "A"
    if total >= 70:
        return "B"
    if total >= 50:
        return "C"
    return "D"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", required=True, help="JSON: {dim: 0-100}")
    ap.add_argument("--missing", nargs="*", default=[], help="剔除缺数据的维度(权重重归一化)")
    args = ap.parse_args()

    scores = json.loads(args.scores)
    unknown = [k for k in scores if k not in WEIGHTS]
    if unknown:
        print(json.dumps({"error": f"unknown dims: {unknown}; valid: {list(WEIGHTS)}"}, ensure_ascii=False))
        return 2

    active = {k: v for k, v in WEIGHTS.items() if k not in args.missing}
    missing_weight = sum(WEIGHTS[k][1] for k in args.missing)
    norm = 1.0 - missing_weight
    total = 0.0
    detail = {}
    for k, (label, w) in active.items():
        s = scores.get(k)
        if s is None:
            print(json.dumps({"error": f"missing score for '{k}' (or pass --missing {k})"}, ensure_ascii=False))
            return 2
        s = max(0.0, min(100.0, float(s)))
        eff_w = w / norm if norm > 0 else 0
        total += s * eff_w
        detail[k] = {"label": label, "score": s, "weight": round(eff_w, 4)}

    total = round(total, 1)
    result = {
        "weighted_total": total,
        "grade": grade(total),
        "dimensions": detail,
        "excluded": {k: WEIGHTS[k][0] for k in args.missing} or None,
        "weight_renormalized": bool(args.missing),
        "formula": " + ".join(
            f"{detail[k]['score']}×{round(detail[k]['weight']*100)}%" for k in active
        ) + f" = {total}",
        "grade_bands": "A≥85 / B 70–84 / C 50–69 / D<50",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
