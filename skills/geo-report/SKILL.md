---
name: geo-report
description: "Generate the 12-section Chinese HTML diagnostic report (single file, embedded CSS) from collected agent results. Use after a geo audit's agents return, or when the user asks to re-render/save the report."
user-invocable: true
argument-hint: "[from <json-or-context>]"
license: MIT
metadata:
  version: "0.1.0"
  category: geo
---

# GEO 诊断报告生成

报告 = 单文件 HTML,内嵌 CSS,**零外部资源**(无 CDN 字体/JS/图),可直接离线打开与转发。视觉规格:

- 宽 1300px 居中;色系:主蓝 `#175cd3`、深蓝 `#0b2f6b`、警示红 `#b42318`、琥珀 `#b96308`、绿 `#18794e`,浅底软色块
- 评分仪表盘:左深蓝渐变总分卡 + 右 7 行维度条形(分数条 + 权重标注)
- 发现卡:顶部 4px 色条按级别(P1 红/P2 琥珀/P3 青/优势 绿)
- 表格:细边框 `#dfe7f1`,表头浅蓝底
- 打印友好(@media print)

## 12 章节结构(编号固定,缺数据写"数据缺口",不删章节)

1. **检测范围声明**:站点定性(业务/架构)、检测方法、8 类页面覆盖矩阵表、免责声明
2. **管理层摘要**:一段总评(四层定位句开头)+ 3 张卡(立即处理/主要风险/可放大资产)
3. **综合评分仪表盘**:7 维度 + 权重 + 加权总分 + 等级
4. **关键发现**:4–8 张卡
5. **SEO 详情**:5.1 技术 SEO 检测表(检测项/结果/判定/详情);5.2 页面 SEO 抽样表;5.3 结构化数据表(类型/状态/字段完整度/说明)
6. **GEO 详情**:四层各一节,每层 实测→判定→缺口→动作
7. **证据台账**:EV-01…N:检测项/URL/结果/证据摘要
8. **整改清单**:优先级/问题/建议动作/预期影响/实施难度/负责角色
9. **现存优势**:4–8 条"需保留资产"
10. **数字资产地图**:四层 ×(已具备/缺失,缺失按 GEO 价值排序)
11. **90 天路线图**:3 阶段,每阶段量化 KPI
12. **最终结论**:一句话定性 + 预期提升(如"53 → 78–85")

## 措辞纪律

- 每个结论都可溯源到 EV 编号;无证据的判断不出现
- 脚注固定两条:"本评分基于公开页面实测生成,不代表搜索引擎或 AI 平台官方评价" + "报告由 claude-geo 生成,复测: /geo audit <url>"
- 数字带单位与口径(字数=去标签可见正文;响应时间=单次公开网络样本)
