# 12 章节报告模板(单文件 HTML)

保存名:`geo-report-<host>-<yyyymmdd>.html`。零外部资源(内嵌 CSS,无 CDN/JS/字体/图)。

## HTML 骨架(直接复用)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1300, initial-scale=1">
  <title>「品牌」GEO 官网增长诊断报告</title>
  <style>
    :root { --ink:#132238; --muted:#5d6b7e; --line:#dfe7f1; --blue:#175cd3;
      --blue-dark:#0b2f6b; --blue-soft:#eaf2ff; --teal:#087b74; --teal-soft:#e7f7f4;
      --amber:#b96308; --amber-soft:#fff4df; --red:#b42318; --red-soft:#fff0ee;
      --green:#18794e; --green-soft:#eaf7f0; }
    body { margin:0; background:#fff; color:var(--ink); font:15px/1.68 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
    .report { width:1300px; max-width:1300px; margin:0 auto; padding:0 34px 48px; }
    .cover { padding:48px 54px; display:grid; grid-template-columns:1.4fr .6fr; gap:42px; align-items:center;
      border:1px solid #d8e4f3; border-top:6px solid var(--blue); background:linear-gradient(135deg,#f8fbff,#edf5ff 58%,#f4fbfa); }
    .cover h1 { margin:18px 0 0; font-size:42px; line-height:1.14; color:var(--blue-dark); }
    .cover-score { padding:28px; text-align:center; border:1px solid #cadcf4; border-radius:22px; background:#fff; }
    .cover-score strong { font-size:32px; color:var(--blue); }
    section { margin-top:28px; }
    .section-head { display:flex; gap:14px; padding-bottom:12px; border-bottom:2px solid var(--line); }
    .section-no { color:var(--blue); font-weight:800; letter-spacing:.12em; }
    .section-head h2 { margin:0; font-size:26px; color:var(--blue-dark); }
    .grid-2,.grid-3,.grid-4 { display:grid; gap:16px; margin-top:16px; }
    .grid-2{grid-template-columns:repeat(2,1fr)} .grid-3{grid-template-columns:repeat(3,1fr)} .grid-4{grid-template-columns:repeat(4,1fr)}
    .card { padding:18px; border:1px solid var(--line); border-radius:14px; background:#fff; }
    .card h3 { margin:0; font-size:18px; color:var(--blue-dark); }
    .card p { margin:10px 0 0; color:var(--muted); }
    .tag { display:inline-block; padding:4px 9px; border-radius:999px; font-size:14px; font-weight:800; }
    .tag-p1{color:var(--red);background:var(--red-soft)} .tag-p2{color:var(--amber);background:var(--amber-soft)}
    .tag-p3{color:var(--teal);background:var(--teal-soft)} .tag-good{color:var(--green);background:var(--green-soft)}
    .dashboard { display:grid; grid-template-columns:410px 1fr; gap:18px; margin-top:18px; }
    .score-panel { padding:24px; border-radius:18px; background:linear-gradient(150deg,#0b2f6b,#175cd3); color:#fff; }
    .score-value { font-size:32px; font-weight:900; }
    .bar { height:9px; margin-top:7px; border-radius:99px; background:#e8eef6; }
    .bar i { display:block; height:9px; border-radius:99px; background:linear-gradient(90deg,#175cd3,#3ca9d6); }
    table { width:100%; margin-top:16px; border-collapse:collapse; font-size:14px; }
    th,td { padding:11px 12px; border:1px solid var(--line); text-align:left; vertical-align:top; overflow-wrap:anywhere; }
    th { background:#edf3fb; color:var(--blue-dark); font-weight:800; }
    tr:nth-child(even) td { background:#fbfcfe; }
    .notice { padding:15px 18px; border-left:4px solid var(--blue); background:var(--blue-soft); font-weight:700; }
    .finding { border-top:4px solid var(--blue); } .finding.p1{border-top-color:var(--red)}
    .finding.p2{border-top-color:var(--amber)} .finding.good{border-top-color:var(--green)}
    .footnote { margin-top:22px; padding-top:14px; border-top:1px solid var(--line); color:var(--muted); font-size:14px; }
    @media print { .report{box-shadow:none} }
  </style>
</head>
<body><main class="report">
  <!-- 封面:kicker/h1(结论式标题)/副标题/URL + 右侧总分卡 -->
  <!-- 01 检测范围声明:notice 免责 + grid-3(页面类型覆盖/源码样本/链接核验) -->
  <!-- 02 管理层摘要:summary 一段 + 3 张卡(P1 立即处理/信任合规/可放大资产) -->
  <!-- 03 评分仪表盘:dashboard(score-panel + 7 行 dimension bar) -->
  <!-- 04 关键发现:grid,finding.p1/.p2/.good 卡 -->
  <!-- 05 SEO 详情:detail-card × 3(技术表/页面抽样表/Schema 表) -->
  <!-- 06 GEO 详情:grid-2 × 4 层(实测/判定/缺口/动作) -->
  <!-- 07 证据台账:table(EV 编号/检测项/URL/结果/证据摘要) -->
  <!-- 08 整改清单:table(优先级/问题/建议/预期影响/难度/角色) -->
  <!-- 09 现存优势:grid-4 tag-good 卡 -->
  <!-- 10 数字资产地图:grid-4(四层)已具备/缺失 -->
  <!-- 11 90 天路线图:grid-3 阶段卡 + 阶段 KPI -->
  <!-- 12 最终结论:conclusion 卡 -->
  <!-- footnote:免责声明 + 复测指令 -->
</main></body></html>
```

## 各章节必含要素

1. **01 检测范围声明**(英文小标题 SCOPE & METHODOLOGY):
   - **站点定性表**(封面下或 01 首):目标站点 | 业务类型(如"入境游 B2B 客源对接平台(单页站+登录业务系统)")| 综合评级 | 检测方式
   - 检测方法(逐条列出:源码级抓取/robots·sitemap·llms.txt 实测/候选路径探测/跳转链与证书验证/前端 JS 路由盘点(SPA 站必做))
   - **8 类页面覆盖矩阵表**(完整表格,不许只用一句话带过):每类一行,列 = 页面类型 | 实测结果(独立 URL 200 / 锚点(#faq) / 未发现)
   - 免责 notice
2. **02 管理层摘要**(EXECUTIVE SUMMARY):第一句 = 四层定位;3 卡必须有一张 P1(若有);增长判断句(修复后预期分区间)
3. **03 综合评分仪表盘**(SCORE DASHBOARD):7 维度条 + 权重 + 加权总分 + 等级 + 加权算式;若剔除维度注明重归一化;复测版附各维度与上次对比
4. **04 关键发现**(KEY FINDINGS):4–8 卡;每卡 tag + 标题 + 证据 + 影响;P1 居首
5. **05 SEO 详情**(SEO DETAILS):三张表全要:
   - 5.1 技术 SEO 检测表:列 = 检测项 | 结果 | 判定词 | 证据说明
   - 5.2 页面 SEO 表:多页站用"每页一行"抽样表;单页/少页站改用"每检测项一行"(Title/Description/H1/Heading/主题集中度/Alt/内链/面包屑/OG/外链,每项配判定词)
   - 5.3 结构化数据表:类型 | 分档 | 字段明细 | 说明
6. **06 GEO 详情**(GEO DETAILS · FOUR LAYERS):四层各一节,**四段式固定:实测 → 判定(一句话评级,如"中等偏好""有潜力""已通")→ 缺口 → 动作**;发现层含分平台可见性表
7. **07 证据台账**(EVIDENCE LEDGER):EV-01 起连续编号;列 = 编号 | 检测项 | 实测证据(HTTP/源码直取) | 结果;SPA+登录站必含"前端 JS 路由盘点"条目
8. **08 整改清单**(ACTION LIST):每条 优先级/问题/建议动作/预期影响/实施难度/负责角色
9. **09 现存优势**(STRENGTHS TO PRESERVE):4–8 条"需保留资产",防误伤
10. **10 数字资产地图**(DIGITAL ASSET MAP):四层 ×(已具备/缺失,按 GEO 价值排序);**已具备资产逐项命名**(如"6 大信任卖点卡片""4 步合作流程""FAQ ×10""gov.cn 资料引用 ×5"),不用概述式
11. **11 90 天路线图**(90-DAY ROADMAP):3 阶段(解除阻断→内容分层→引用资产);每阶段末尾独立 KPI 块(量化:公开 URL 数/Schema 部署率/复测目标分)
12. **12 最终结论**(CONCLUSION):一句话定性 + 预期提升区间(如 53 → 78–85)

## 判定词标准表(表格"判定"列统一使用)

优秀 / 良好 / 正常 / 基本健康 / 部分完整 / 不适用(纯 SVG 站的 Alt 等) / 薄弱 / 异常 / 未部署 / 假部署 / 未发现
避免自造判定词;需要说明时放"说明"列。
