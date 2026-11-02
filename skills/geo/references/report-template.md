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

1. **01**:站点定性(业务/架构判定依据)、检测方法、8 类覆盖矩阵表、免责 notice
2. **02**:第一句 = 四层定位;3 卡必须有一张 P1(若有)
3. **03**:7 维度条 + 权重 + 加权总分 + 等级;若剔除维度注明重归一化
4. **04**:4–8 卡;每卡 tag + 标题 + 证据 + 影响
5. **05**:三张表全要;抽样表每页一行
6. **06**:四层 ×(实测/判定/缺口/动作);含分平台可见性表(发现层)
7. **07**:EV-01 起连续编号;结果列判定词
8. **08**:每条 P1/P2/P3 + 实施难度(小时/天/周)+ 负责角色(前端/SEO/内容/运营)
9. **09**:防误伤——整改时别把这些改坏了
10. **10**:四层 ×(已具备资产清单/缺失资产按价值排序)
11. **11**:3 阶段(解除阻断→内容分层→引用资产);每阶段量化 KPI(公开 URL 数/Schema 部署率/复测目标分)
12. **12**:一句话定性 + 预期提升区间(如 53 → 78–85)
