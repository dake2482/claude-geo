# 三份 GEO 诊断报告交叉验证

> 分析对象:同一模板体系下的三份「SEO × GEO 官网增长诊断报告」
> - **PalFish**(palfish.vn,越南在线英语教育,WordPress 多页站)— 综合 **69/100**
> - **Neta Studio**(neta.art,AI 世界构建工具 SaaS,Next.js SSR + 7,405 URL)— 综合 **70/100 (B+)**
> - **入境客**(rujingke.com,入境游 B2B 单页站 + 登录业务系统)— 综合 **53/100 (C)**
>
> 结论:三份报告共享**同一套固定评分体系**(7 维度、同权重)、**同一份 12 章节报告结构**、
> **同一个 GEO 四层模型**(被发现 → 被理解 → 被信任 → 被引用)、以及**同一条证据纪律**
> (每项结论必须挂 HTTP/源码实测证据)。差异只在行业适配与站点架构判断。
> 本项目(claude-geo)的检查项体系即从这三份报告对比提炼并归一化。

## 1. 统一的 7 维度评分体系(权重完全一致)

| 维度 | 权重 | PalFish | Neta | 入境客 | 说明 |
|---|---|---|---|---|---|
| 技术可访问性 | 15% | 62 | 88 | 82 | DNS/HTTPS/robots/sitemap/渲染模式/404/canonical |
| 页面 SEO 质量 | 15% | 61 | 75 | 66 | Title/Description/H 结构/图片 Alt/内链/面包屑 |
| 内容资产覆盖 | 20% | 76 | 72 | 36 | 8 类页面覆盖矩阵/正文规模/内容形态/更新机制 |
| AI 发现能力 | 10% | 58 | 78 | 45 | robots AI 规则/llms.txt/sitemap/SSR/noindex 阻断 |
| AI 理解能力 | 15% | 82 | 55 | 54 | JSON-LD 完整度/语义 HTML/层级/表格化/定义句 |
| 品牌与产品实体完整度 | 15% | 65 | 68* | 40 | 公司主体/NAP 一致性/案例/作者/E-E-A-T |
| AI 引用资产潜力 | 10% | 71 | 58 | 50 | 问答/定义/对比/流程/案例五类引用资产 |

*Neta 报告仪表盘标 78、GEO 详情章节标 68(信任能力),取 GEO 章节口径。

入境客报告直接给出了加权算式:`82×15% + 66×15% + 36×20% + 45×10% + 54×15% + 40×15% + 50×10% = 53.0`,
证明权重是硬编码的评分规则,非临时拼凑。

**等级带**(由 Neta 70=B+、入境客 53=C 反推):A ≥85 / B 70–84 / C 50–69 / D <50。

## 2. 统一的 12 章节报告结构

三份报告章节编号与内容完全同构:

| # | 章节 | 内容 |
|---|---|---|
| 01 | 检测范围声明 | 站点定性(业务/架构)、检测方法、**8 类页面覆盖矩阵**、评分免责声明 |
| 02 | 管理层摘要 | 一段总评 + 三张卡(立即处理/信任合规/可放大资产 或 优势/风险/机会) |
| 03 | 综合评分仪表盘 | 7 维度条形图 + 加权总分 + 权重声明 |
| 04 | 关键发现 | 4–8 张 P1/P2/P3/优势 卡片 |
| 05 | SEO 详情 | 5.1 技术 SEO 检测表(检测项/结果/判定/详情)、5.2 页面 SEO 抽样表、5.3 内链面包屑 / 结构化数据表 |
| 06 | GEO 详情 | **四层能力**各一节:AI 发现 / AI 理解 / AI 信任 / AI 引用,每层 实测→判定→缺口→动作 |
| 07 | 证据台账 | EV-01…EV-N:检测项 / URL / 结果 / 证据摘要(HTTP 状态、MD5、字节数、源码片段) |
| 08 | 整改清单 | P1/P2/P3 × 问题/建议动作/预期影响/实施难度/负责团队 |
| 09 | 现存优势 | 4–8 条"需保留的资产",防止整改时误伤 |
| 10 | 数字资产地图 | 四层模型 × (已具备资产 / 缺失资产按 GEO 价值排序) |
| 11 | 90 天路线图 | 3–4 阶段,每阶段带可量化 KPI(公开 URL 数、Schema 部署率、综合分目标) |
| 12 | 最终结论 | 一句话定性 + 预期提升幅度 |

## 3. 统一的 GEO 四层模型

```
01 被发现(Discover)   → 抓取入口层:HTTPS、规范域、robots、Sitemap、llms.txt、SSR、导航
02 被理解(Understand) → 语义解释层:H 层级、FAQ、Schema、表格化、面包屑、语言标注
03 被信任(Trust)      → 主体证明层:公司实体、联系方式、案例、作者、权威来源、隐私政策
04 被引用(Cite)       → 答案资产层:FAQ、教程、对比、案例、流程、可核验定义与数据
```

仪表盘 7 维 = 3 个 SEO 维度(技术/页面/内容)+ 4 个 GEO 维度(发现/理解/实体=信任/引用)。

## 4. 检查项全集(对比提炼,claude-geo 的 scoring-rubric 来源)

### 4.1 技术 SEO(技术可访问性)
1. DNS 可解析(A 记录 / NXDOMAIN);www 解析与否、www↔裸域 301/308 规范化
2. HTTP→HTTPS 跳转链与跳数;查询参数保留
3. HTTPS 证书(签发方 / CN / 有效期)
4. HTTP/2、HTTP/3(alt-svc)
5. 安全响应头:HSTS、CSP、X-Frame-Options、X-Content-Type-Options、Referrer-Policy
6. 首页状态码 / 响应时间 / HTML 字节数(单次样本,注明非性能基准)
7. robots.txt:状态、语法合法性、Allow/Disallow 策略实质(是否存在 `Disallow: /` + 例外放行式封禁)、**AI 爬虫显式规则(GPTBot / OAI-SearchBot / ClaudeBot / PerplexityBot / ChatGPT-User 等)**、**Content Signals 协议(Search / AI-Input / AI-Train)**、Sitemap 声明
8. sitemap.xml:状态、URL 数、子地图索引结构、lastmod 真实性(是否全为构建日)、priority/changefreq、是否覆盖内容页
9. llms.txt:状态、内容类型(**200 但 text/html = SPA 回退,实为未部署**)、Markdown 链接与分节规范
10. 渲染模式:SSR / CSR 判定;核心正文是否在初始 HTML;去标签可见正文字数
11. 404 处理:真实 404 vs **软 200**(任意编造路径返回 200 + 同一 HTML,MD5 逐字节比对)
12. Meta Robots:noindex / nofollow(含首页误封)
13. Canonical:存在性、自指、每页唯一、重复输出、全站统一指首页类错误
14. URL 结构:语义化路由、登录后业务路由与公开内容路由区分
15. 移动端基础信号:viewport、响应式断点数量
16. 页面语言:`html lang`、多语言切换、hreflang / x-default、国际化(英文版)
17. OG / Twitter 卡:og:type/locale/site_name/title/description/url/**og:image(1200×630)**、twitter:card
18. 内链结构:导航 / 页脚 / 锚文本语义(非"点击这里")/ 内链闭环(内容页回上级列表)
19. 外链可达性:出站链接抽测(权威来源是否 200)

### 4.2 页面 SEO(页面 SEO 质量)
20. Title:长度(约 50–60 上限)、唯一性、含核心关键词、品牌后缀
21. Description:长度、信息密度、**同页重复输出检测(模板 + SEO 插件双写)**、旧信息残留
22. H1 唯一性与主题明确度
23. Heading 层级:无跳级(如 H1→H3)、H2/H3 数量与分区
24. 图片 Alt 覆盖率(非空 Alt / 总 img 数);**装饰图(空 Alt 合法)与内容图区分**;图片 width/height
25. 面包屑:可视化 + BreadcrumbList,覆盖哪些页面类型、缺哪些
26. 主题集中度:页面主题聚焦度
27. 内链锚文本质量;死链(抽样站内 URL 逐个状态码)
28. `<img>` 为 0(纯 SVG 图标站)与表格数为 0 等内容形态统计

### 4.3 内容资产(内容资产覆盖,权重最高 20%)
29. **8 类页面覆盖矩阵**:首页 / 品牌·关于 / 核心服务·产品详情 / FAQ·帮助中心 / 客户案例·评价 / 新闻资讯·科普知识 / 联系我们·门店 / 隐私政策·法律协议 —— 每类记录"独立 URL / 页面锚点 / 未发现"三种状态
30. sitemap URL 规模(1 vs 182 vs 7,405)与内容页占比
31. 可见正文规模(字符/字数)与页面类型下限对照
32. 内容形态:FAQ 条数与答案长度、流程步骤、清单、对比表、量化案例
33. UGC / 模板页重复度(大流量路径)
34. 帮助中心 / 知识库是否存在
35. 作者署名与更新时间标注机制
36. FAQ 独立页 vs 页面内嵌(锚点)

### 4.4 GEO 四层
**L1 发现能力**:robots AI 爬虫规则、Content Signals、sitemap 分层、llms.txt、SSR 直出、内链网络、noindex/robots 层封禁、公开可索引 URL 数
**L2 理解能力**:JSON-LD 全套(Organization / WebSite+SearchAction / Service / Product / Course+Offer / FAQPage / BreadcrumbList / Article / BlogPosting / Person / ItemList / CreativeWork)、JSON 语法解析、**实体字段完整度**(Organization: name/url/logo/sameAs/address/contactPoint/foundingDate)、语义化 HTML(main/nav/section/article、aria-labelledby)、页面可见信息与 Schema 一致性、定义句 / 术语块、表格化内容、FAQ 结构(H3 问句)
**L3 信任能力**:公司法律名称、地址、电话 / 邮箱、资质牌照 / ICP 备案、关于页深度(团队 / 历程 / 使命)、客户案例(量化)、作者与更新时间、权威来源引用(gov.cn 等实测 200)、品牌命名统一度、NAP 跨 Meta/正文/Schema/页脚一致性、隐私政策 / 服务协议、免责与核对日期标注
**L4 引用潜力**:五类引用资产(问答 / 定义 / 对比 / 流程 / 案例)、直接结论句、量化主张 + 就近来源、可核验边界声明、独立可引用 URL、外链提及与 sameAs 社媒矩阵

### 4.5 证据纪律(三报告共性,最重要)
- 每项结论挂实测证据:HTTP 状态码、响应头、字节数、**MD5 逐字节比对**(软 200 判定)、源码片段、链接实测状态
- 证据台账编号(EV-01…)与正文发现互相引用
- 明确声明"基于公开页面实测,不代表搜索引擎或 AI 平台官方评价"
- 无法抓取 / 鉴权拦截的项目如实标注,不做经验推测
- 抽样方法透明:基于 sitemap 抽样、8 类覆盖矩阵、站内链接核验条数

## 5. 三站对照观察(交叉验证发现)

- **软 200 是通病**:入境客(25 个路径 200、5 份 MD5 一致)与 Neta(FAQ 路径 404 正确)对照,说明该项被当作 P1 级硬伤;apihop.ai 审计(本机另测)同样命中。
- **首页索引信号是最常见的"一票否决"**:PalFish 首页 noindex,nofollow + 无 canonical;入境客 robots `Disallow: /` 仅放行首页;Neta 首页缺 canonical——三种不同形态,同一层(被发现)故障。
- **Schema"有骨架、缺血肉"分级**:入境客(Organization 仅 name/url/description)vs PalFish(Course+CourseInstance+Offer 全套)vs Neta(全站为零)——评分不只看"有没有",看**字段完整度**。
- **llms.txt 三态**:未部署(Neta 404)/ 假部署(入境客 200 但回退首页 HTML)/ 已部署(PalFish 200 text/plain)——必须验 content-type 与内容,不能只看状态码。
- **权重设计意图**:内容资产 20% 最重,信任实体 15% 次之——该体系认定"GEO 的瓶颈通常在内容与信任,而非技术"。
