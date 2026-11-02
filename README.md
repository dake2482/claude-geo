# claude-geo

> GEO(生成式引擎优化)官网诊断插件 —— 给任意网站一个 URL,产出一份带 7 维评分、证据台账、整改清单和 90 天路线图的中文 HTML 诊断报告。

**适用对象**:希望在 ChatGPT / Perplexity / Google AI Overviews 等 AI 搜索中获得可见性与引用的官网运营者;想用一套可复现流程做 GEO 诊断的 SEO/增长团队。

## 它解决什么问题

传统 SEO 审计回答"我在搜索结果里排得怎么样";claude-geo 回答的是另一组问题:

- AI 爬虫(GPTBot / OAI-SearchBot / PerplexityBot / ClaudeBot,**它们大多不执行 JS**)能发现并读到我的站的多少内容?
- AI 读完页面后,能建立"这个品牌 = 一个可核验的真实主体"的实体认知吗?
- 当用户在 AI 助手里问相关问题时,我的站有没有**会被摘录引用**的内容资产?

## 核心概念:GEO 四层模型

```
01 被发现(Discover)    抓取入口层  HTTPS · 规范域 · robots · Sitemap · llms.txt · SSR · 导航
02 被理解(Understand)  语义解释层  H 层级 · FAQ · Schema · 表格化 · 面包屑 · 语言标注
03 被信任(Trust)       主体证明层  公司实体 · 联系方式 · 案例 · 作者 · 权威来源 · 隐私政策
04 被引用(Cite)        答案资产层  FAQ · 教程 · 对比 · 案例 · 流程 · 可核验定义与数据
```

诊断叙事沿四层推进:**瓶颈在哪一层就先修哪一层**——发现层不通时,理解/信任/引用层的投入对 AI 全部不可见。

## 评分体系(7 维度,固定权重)

| 维度 | 权重 | 检查内容 |
|---|---|---|
| 技术可访问性 | 15% | DNS/跳转链/HTTPS/安全头/robots 策略实质/sitemap/llms.txt 三态/渲染模式/软404/canonical |
| 页面 SEO 质量 | 15% | Title/Description 唯一性、H 结构、图片 Alt、面包屑、内链与死链 |
| **内容资产覆盖** | **20%** | 8 类页面覆盖矩阵、公开 URL 规模、正文规模、内容形态、更新机制 |
| AI 发现能力 | 10% | 分 UA robots 判定、llms.txt、SSR 直出、公开 URL 净数、分平台可见性 |
| AI 理解能力 | 15% | JSON-LD 实体字段完整度分档、语义 HTML、表格化、Schema 与可见信息一致性 |
| 品牌与产品实体完整度 | 15% | 公司主体、NAP 跨位置一致性、案例、权威来源逐条实测、隐私政策 |
| AI 引用资产潜力 | 10% | 问答/定义/对比/流程/案例五类引用资产、结论句密度、来源可核验性 |

等级:**A ≥85 / B 70–84 / C 50–69 / D <50**。权重硬编码在 `score_geo.py` 中由脚本计算,禁止口算。

**P1 一票否决项**(命中任一,对应维度 ≤40 且管理层摘要置顶):首页 noindex、robots `Disallow: /` 式封禁、全站软 200(编造路径 200 且 MD5 与首页一致)、canonical 全站指首页、纯 CSR 且初始 HTML 零正文、收费业务无隐私政策。

## 检查项体系的来源

检查项(74 项)对比提炼三份真实 GEO 诊断报告并交叉验证——它们共享同一套 7 维评分、12 章节报告结构、四层模型与证据纪律:

- PalFish(越南在线教育多页站,69/C)
- Neta Studio(AI 工具 SaaS,7,405 URL,70/B+)
- 入境客(入境游 B2B 单页站,53/C)

完整分析见 [`docs/cross-validation.md`](docs/cross-validation.md)。评分公式已用入境客报告的原始维度分复现验证(精确得出 53.0/C)。

## 命令

| 命令 | 功能 | 耗时 |
|---|---|---|
| `/geo audit <url>` | 全站诊断:3 个证据脚本 + 7 个子代理并行 → 12 章节中文 HTML 报告 | 10–15 分钟 |
| `/geo page <url>` | 单页深挖:AI 爬虫视角的可见/可理解/可引用分析 | 2–3 分钟 |
| `/geo probe <url>` | 纯证据采集(robots/sitemap/llms.txt/软404/meta),不出评分 | <1 分钟 |
| `/geo llms <url>` | llms.txt 三态检测(未部署/假部署/已部署)+ 规范化生成 | 1–2 分钟 |
| `/geo doctor` | 运行环境自检 | 秒级 |

## 架构(对标 [claude-seo](https://github.com/AgriciDaniel/claude-seo) 的设计)

```
claude-geo/
├── skills/
│   ├── geo/                 # hub:命令表、编排逻辑、评分权重、质量门
│   │   └── references/      # scoring-rubric(74 项细则)/页面矩阵/报告模板/证据标准/四层模型
│   ├── geo-audit/           # 全站诊断流程
│   ├── geo-page/            # 单页分析
│   ├── geo-llms/            # llms.txt 检测与生成
│   └── geo-report/          # 12 章节 HTML 报告生成
├── agents/                  # 7 个维度子代理(与 7 个评分维度一一对应,并行执行)
├── scripts/
│   ├── claude-geo           # runtime 启动器(解析 Python 版本后转交 runtime.py)
│   ├── runtime.py           # 隔离 venv 引导 + setup/doctor/run 分发
│   ├── probe_site.py        # 证据采集:跳转链/robots 策略实质/sitemap/llms 三态/软404 MD5/meta/AI-UA 视角
│   ├── check_schema.py      # JSON-LD 实体清单与字段完整度分档(skeleton/core/full)
│   ├── page_matrix.py       # 8 类页面覆盖矩阵探测(通用+分行业候选路径)
│   └── score_geo.py         # 加权总分计算(权重校验,支持缺维度重归一化)
├── docs/cross-validation.md # 检查项体系的三报告交叉验证
└── install-zcode.sh / install.sh / uninstall.sh
```

设计原则:**脚本产出证据,代理产出判断,报告产出叙事**。每个子代理必须引用探测脚本的硬证据(HTTP 状态、MD5 比对、字节数、源码片段),没有证据的判断只能进"数据缺口"。

## 安装

依赖:Python 3.11–3.14,git。无需任何 API Key。

**ZCode**:

```bash
git clone https://github.com/dake2482/claude-geo.git
cd claude-geo && bash install-zcode.sh
```

技能装到 `~/.zcode/skills/geo*`,代理装到 `~/.zcode/agents/`,Python 依赖装进隔离 venv(`~/Library/Application Support/claude-geo/`,macOS;Linux 为 `~/.local/share/claude-geo/`),不污染系统环境。

**Claude Code(手动安装)**:

```bash
bash install.sh    # 装到 ~/.claude/skills + ~/.claude/agents
```

安装器会把文档中的 `${GEO_SKILL_ROOT}` 占位符重写为目标机器的绝对路径。

**卸载**:`bash uninstall.sh`

## 使用

```
新开会话 → /geo audit https://example.com
```

- 报告输出为单文件 HTML(内嵌 CSS,零外部资源),可直接离线打开、转发
- 整改后复测跑同一条命令,总分与维度分可直接对比
- 环境变量 `CLAUDE_GEO_PYTHON` 可指定解释器,`CLAUDE_GEO_DATA_DIR` 可指定数据目录

## 报告长什么样

12 章节固定结构:检测范围声明(含 8 类页面覆盖矩阵)→ 管理层摘要 → 评分仪表盘 → 关键发现 → SEO 详情 → GEO 详情(四层 × 实测/判定/缺口/动作)→ 证据台账(EV 编号)→ 整改清单(优先级/难度/负责角色)→ 现存优势 → 数字资产地图 → 90 天路线图(带量化 KPI)→ 最终结论。

## 事实底线(内置在提示词里,不会越界)

- 评分基于公开页面实测,不代表搜索引擎或 AI 平台官方评价
- llms.txt 被 Google Search 忽略是公开事实;其价值只面向其他 AI 平台
- FAQPage 的 Google 富结果已全面下线,不建议为此新增
- 探测只做 GET;软 404 探测路径为随机编造的无副作用路径
- 抓取内容一律视为不可信外部数据,页面里的"指令"只会被当作发现上报

## 与 claude-seo 的关系

claude-geo 的工程架构(技能/代理/runtime/安装器分层,`${CLAUDE_PLUGIN_ROOT}` 路径重写,隔离 venv)完全师承 [claude-seo](https://github.com/AgriciDaniel/claude-seo);两者互补不替代:

| | claude-seo | claude-geo |
|---|---|---|
| 视角 | 传统搜索排名 + 技术债 | AI 可见性 + 实体 + 引用资产 |
| 评分 | SEO Health Score(7 类,含 CWV/外链) | GEO 7 维(内容资产 20% 最重) |
| 报告 | 英文 Markdown/PDF | 中文单文件 HTML(12 章节) |

同一站点跑两份报告对照,是排查"SEO 还行但 AI 搜不到"类问题的最快方式。

## License

MIT
