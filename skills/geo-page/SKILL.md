---
name: geo-page
description: "Deep GEO analysis of a single page: AI crawler visibility, initial-HTML content, schema on this page, citability of passages, entity signals. Use when the user gives one URL and wants page-level GEO, not a site-wide audit."
user-invocable: true
argument-hint: "[url]"
license: MIT
metadata:
  version: "0.1.0"
  category: geo
---

# GEO 单页深度分析

单页视角回答一个问题:**一个不执行 JS 的 AI 抓取器拿到这个 URL 时,能看到什么、能理解什么、会引用什么**。

## 流程

1. 证据:
```
"${GEO_SKILL_ROOT}/scripts/claude-geo" run probe_site.py <url> --out /tmp/geo-page/probe.json
"${GEO_SKILL_ROOT}/scripts/claude-geo" run check_schema.py <url> --out /tmp/geo-page/schema.json
```
2. 手工补充(curl/无头浏览器按需):
   - **无 JS 视角正文**:curl 原始 HTML 去标签后的可见文字(这是 GPTBot/PerplexityBot 看到的全部)
   - **段落可引用性**:抽 3 个关键段落,判断是否自包含(脱离上下文可被摘录)、是否有定义句式("X 是…"、直接结论句)、量化主张是否带来源
   - **单页四层小结**:发现(canonical/robots/meta robots)→ 理解(H 结构/Schema)→ 信任(NAP/作者/日期)→ 引用(FAQ/表格/清单/对比)

## 输出格式

- 实测表:指标 → 值 → 判定
- 发现清单(P1/P2/P3 + 证据)
- 单页 GEO 得分(四层各 0–100,不套全站 7 维权重)
- 一段"AI 抓取器视角"的直白描述(它实际读到了什么)
