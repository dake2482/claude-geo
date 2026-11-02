---
name: geo-audit
description: "Run a full-site GEO diagnostic and produce the 12-section Chinese HTML report. Use when the user wants the complete audit (评分仪表盘/证据台账/整改清单/90天路线图), not a single page or a quick check."
user-invocable: true
argument-hint: "[url]"
license: MIT
metadata:
  version: "0.1.0"
  category: geo
---

# GEO 全站诊断流程

前置:主 hub(`geo`)负责编排,本技能定义报告怎么写、分怎么合。

## 流程

### 1. 证据采集(主线程)

```
"${GEO_SKILL_ROOT}/scripts/claude-geo" run probe_site.py <url> --out /tmp/geo-<host>/probe.json
"${GEO_SKILL_ROOT}/scripts/claude-geo" run check_schema.py <url> --out /tmp/geo-<host>/schema.json
"${GEO_SKILL_ROOT}/scripts/claude-geo" run page_matrix.py <url> --out /tmp/geo-<host>/matrix.json
```

从 probe.json 判定:**业务类型**(SaaS/电商/教育/本地/B2B/媒体)与**架构**(多页/单页/SPA+登录系统/纯 CSR)。此判定写进报告 01 章节。

### 2. 并行子代理

一次消息派发 7 个代理(见 hub)。每个代理的返回必须包含:
- findings:[P1/P2/P3/优势] + 标题 + 证据(引用 EV 编号或自行抓取的实测) + 建议
- score:维度分 0–100 + 一段得分理由
- gaps:数据缺口(无法验证的项)

### 3. 合分

```
"${GEO_SKILL_ROOT}/scripts/claude-geo" run score_geo.py --scores '{"technical":82,"onpage":66,"content":36,"discover":45,"understand":54,"entity":40,"citation":50}'
```

输出加权总分与等级。**维度分由代理判,总分由脚本算**——禁止口算加权。

### 4. 报告

加载 `../geo/references/report-template.md`,写单文件 HTML(内嵌 CSS,无外部资源),保存为
`<工作区>/geo-report-<host>-<yyyymmdd>.html`。12 章节结构固定,缺数据的章节写"数据缺口"而不是删章节。

## 评分要点(摘自 scoring-rubric,细则见该文件)

- 内容资产 20% 最重:8 类页面矩阵 + 正文规模 + 五类内容形态是主战场
- P1 一票否决项:发现层阻断(noindex/robots 封禁/软 200/canonical 指首页/纯 CSR)→ 对应维度 ≤40 并置顶
- Schema 按**字段完整度**分档:零 → 骨架(仅 name/url) → 核心字段(logo/sameAs/address) → 全套(含 SearchAction/Offer/Breadcrumb)
- 三态 llms.txt:404=未部署 / 200+html=假部署 / 200+text/plain=已部署(再看链接规范)

## 报告叙事原则

管理层摘要第一句 = 四层模型定位("瓶颈在发现层"或"发现通、信任断")。
关键发现 4–8 张卡,每张有证据。整改清单每条带:优先级/动作/预期影响/实施难度/负责角色。
90 天路线图 3 阶段,每阶段带量化 KPI(公开 URL 数、Schema 部署率、复测目标分)。
