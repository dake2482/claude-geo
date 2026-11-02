# claude-geo 评分细则(7 维度 × 检查项全集)

> 来源:三份真实 GEO 诊断报告交叉验证(docs/cross-validation.md)。
> 权重固定;等级 A≥85 / B 70–84 / C 50–69 / D<50。

## 维度 1:技术可访问性(15%)

| # | 检查项 | 判定要点 | 级别参考 |
|---|---|---|---|
| 1 | DNS 可解析 | A 记录存在 / NXDOMAIN | P1 若不可解析 |
| 2 | www↔裸域规范化 | 有解析、301/308 到唯一规范域;www NXDOMAIN 记 P3 | P3 |
| 3 | HTTP→HTTPS | 跳转链 ≤2 跳、参数保留 | P2 若多跳/丢参数 |
| 4 | HTTPS 证书 | 签发方/CN/有效期 | P1 若无效/过期 |
| 5 | HTTP/2、h3(alt-svc) | 支持即加分项 | — |
| 6 | 安全响应头 | HSTS/CSP/XFO/XCTO/Referrer-Policy 齐全度 | P3 每缺一项 |
| 7 | 首页状态/耗时/字节 | 200、单次样本(注明非基准) | — |
| 8 | robots.txt 策略实质 | `Disallow: /` + Allow 例外 = 变相全站封禁 → P1 | **P1** |
| 9 | robots AI 爬虫规则 | GPTBot/OAI-SearchBot/ClaudeBot/PerplexityBot 显式规则;缺失≠扣分(默认放行) | — |
| 10 | Content Signals | Search/AI-Input/AI-Train 声明;缺失记"未声明" | — |
| 11 | sitemap | URL 数/lastmod 真实性(全为构建日=不可信)/内容页覆盖 | P2 仅首页 |
| 12 | llms.txt 三态 | 404=未部署;200+html=假部署(MD5 比对);200+text/plain=已部署再验链接 | P2 未部署 |
| 13 | 渲染模式 | SSR(初始 HTML 含正文)/CSR;去标签字数 | **P1** 纯 CSR |
| 14 | 软 404 | 编造路径 200 + 与首页 MD5 一致 | **P1** |
| 15 | Meta Robots | 首页 noindex/nofollow = 最硬 P1 | **P1** |
| 16 | Canonical | 每页自指唯一;全站指首页 = P1;首页缺失 = P2 | P1/P2 |
| 17 | html lang / hreflang | 与内容语言一致;国际化站看 x-default | P3 |
| 18 | OG/Twitter 卡 | og:image 1200×630、twitter:card | P3 缺 og:image |
| 19 | 移动端基础 | viewport、断点 | P3 |

## 维度 2:页面 SEO 质量(15%)

| # | 检查项 | 判定要点 |
|---|---|---|
| 20 | Title | 唯一、50–60 字内、含关键词、品牌后缀 |
| 21 | Description | 唯一、信息密度;**同页多份(模板+插件双写)**点名为 P2;旧信息残留 P2 |
| 22 | H1 唯一性 | 每页 1 个、主题明确 |
| 23 | Heading 层级 | 无跳级(H1→H3)、分区清晰 |
| 24 | 图片 Alt | 覆盖率(非空/总数);装饰图空 alt 合法;内容图必须描述 |
| 25 | 面包屑 | 可视化 + BreadcrumbList 双轨;按页面类型列缺口 |
| 26 | 内链 | 锚文本语义、导航/页脚完整、内容页↔列表闭环 |
| 27 | 死链 | 抽样站内 URL 逐个验证,404 点名路径 |
| 28 | 内容形态统计 | table/ol/ul/details 计数(img=0 的 SVG 站也要记录) |

## 维度 3:内容资产覆盖(20%,最高权重)

| # | 检查项 | 判定要点 | 级别参考 |
|---|---|---|---|
| 29 | **8 类页面矩阵** | 首页/关于/产品服务/FAQ帮助/案例/资讯/联系/隐私协议;每类:独立URL/锚点/未发现 | 缺法律页(收费业务)P1 |
| 30 | 公开 URL 净数 | sitemap 实数 × 可索引比例 | 仅 1 URL → 维度 ≤40 |
| 31 | 正文规模 | 去标签字符数 vs 页面类型下限 | — |
| 32 | 内容形态 | FAQ 条数+答案长度/流程/清单/对比表/量化案例 | — |
| 33 | FAQ 形态 | 独立 URL > 页内锚点 > 缺失 | P2 全缺 |
| 34 | 作者/更新时间 | 署名机制、datePublished 可见性 | P3 |
| 35 | UGC 模板重复度 | 大规模同构路径抽样去重 | P3 |
| 36 | 帮助中心/知识库 | 存在性与深度 | P3 |

## 维度 4:AI 发现能力(10%)

| # | 检查项 |
|---|---|
| 37 | 分 UA robots 判定(GPTBot/OAI-SearchBot/ChatGPT-User/ClaudeBot/Claude-SearchBot/PerplexityBot/Perplexity-User/Google-Extended/CCBot/Bytespider) |
| 38 | sitemap 对 AI 的入口价值 |
| 39 | llms.txt 状态 + 逐链接匿名可达 |
| 40 | SSR 判定(初始 HTML 字数) |
| 41 | noindex/robots 层封禁导致的公开 URL 净数 |
| 42 | 首页无 JS 出链深度(能爬多深) |
| 43 | well-known 发现文件(ai-catalog.json/security.txt;存在记,缺失不扣) |
| 44 | 分平台可见性判定表:ChatGPT Search / Perplexity / Google AI Overviews / Claude |

## 维度 5:AI 理解能力(15%)

| # | 检查项 | 分档 |
|---|---|---|
| 45 | JSON-LD 语法有效性 | 解析失败点名 |
| 46 | Organization | 零/骨架(name+url)/核心(+logo+sameAs+address)/全套(+foundingDate) |
| 47 | WebSite | +SearchAction +inLanguage |
| 48 | Service/Product(+Offer) | 产品语义承载 |
| 49 | Course(+CourseInstance+Offer) | 教育类 |
| 50 | FAQPage | 问题数、答案 30–150 字、与可见问答一致 |
| 51 | BreadcrumbList | 覆盖页面类型 |
| 52 | Article/BlogPosting | author/datePublished/dateModified/publisher/image |
| 53 | 语义 HTML | main/nav/section/article、aria-labelledby |
| 54 | H 结构与主题分区 | — |
| 55 | 表格化内容 | 对比/价格/参数表加分 |
| 56 | 定义句/术语块 | 自包含可摘录 |
| 57 | Schema 与可见信息一致性 | 地址/电话对不上比缺失更糟 |

## 维度 6:品牌与产品实体完整度(15%)

| # | 检查项 | 级别参考 |
|---|---|---|
| 58 | 公司法律主体(4 处找:正文/页脚/About/Schema) | P1 收费业务无主体 |
| 59 | NAP 一致性矩阵(Meta vs 正文 vs Schema vs 页脚) | P2 旧信息/占位符 |
| 60 | 资质/备案(ICP 等) | — |
| 61 | 关于页深度(团队/历程/使命) | P2 一段话 |
| 62 | 联系方式真实性(非仅表单) | — |
| 63 | 客户案例(量化、授权) | P3 |
| 64 | 作者署名/更新时间 | P3 |
| 65 | 权威来源引用逐条实测 | 亮点项 |
| 66 | 隐私政策/服务协议 | **P1** 收费业务缺失 |
| 67 | 品牌命名统一度 | P2 混名 |
| 68 | 免责声明/核对日期 | 加分项 |

## 维度 7:AI 引用资产潜力(10%)

| # | 检查项 |
|---|---|
| 69 | 五类引用资产:问答/定义/对比/流程/案例 逐类盘点 |
| 70 | 直接结论句密度(抽 3 页计数) |
| 71 | 量化主张 + 就近来源 |
| 72 | 可独立引用 URL(非锚点) |
| 73 | 措辞克制度与免责边界(可摘录性) |
| 74 | 按业务定制的"最该先写的 N 篇可引用内容"清单 |

## P1 清单与处理规则

命中任一下列项 = P1:置顶强调(管理层摘要第一卡/关键发现第一位/整改第一行),并在**归属维度**内重扣(-20~-30),**不强制维度 ≤40**:

1. 首页 noindex/nofollow → 归属:发现维重扣,技术维轻扣
2. robots `Disallow: /` 式封禁(仅放行首页/静态资源)→ 归属:发现维重扣,技术维轻扣(robots 语法本身合法)
3. 全站软 200(编造路径 200 + MD5 一致)→ 归属:技术维重扣(404 语义是管道职责)
4. canonical 全站指首页 → 归属:发现维重扣
5. 纯 CSR 且初始 HTML 零正文 → 归属:发现维重扣,技术维按管道(可达/HTTPS)正常评
6. 收费业务无隐私政策 → 归属:实体信任维重扣
7. sitemap 仅 1 条 URL 且无任何内容页 → 归属:内容资产维重扣

**与原体系对齐依据**:原报告在 robots 全禁 + 软 200 并存时,技术可访问性给 82(管道健康:DNS/HTTPS/头/SSR 全优),发现维给 45(策略封禁)——P1 决定"叙事优先级",不决定"维度天花板"。
