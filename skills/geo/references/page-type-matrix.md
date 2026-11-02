# 8 类页面覆盖矩阵 + 分行业候选路径

固定 8 类(三报告共识):

| 类型 | 通用候选路径 | 判定三态 |
|---|---|---|
| 首页 | `/` | 独立 URL |
| 品牌·关于 | /about /about-us /company /gioi-thieu(越) | 独立 URL / 锚点 / 未发现 |
| 核心服务·产品 | /pricing /products /services /features /apis | 同上 |
| FAQ·帮助中心 | /faq /faqs /help /support /docs | 同上 |
| 客户案例·评价 | /cases /case-studies /customers /testimonials /use-cases | 同上 |
| 新闻资讯·科普 | /blog /news /articles /updates /changelog /wiki | 同上 |
| 联系我们·门店 | /contact /contact-us | 同上 |
| 隐私政策·法律 | /privacy /privacy-policy /terms /legal | 同上 |

行业适配(追加候选,page_matrix.py `--industry`):

- **saas**:产品页加 /integrations /docs /status /changelog;案例加 /customers
- **ecommerce**:产品=/collections /products;加 /cart /reviews
- **education**:FAQ=/help;资讯=/blog /knowledge;加 /courses /teachers /pricing
- **local**:联系=门店页(地图/NAP);加 /locations /reviews
- **b2b**:加 /partners /qualifications(资质);案例=合作案例
- **media**:资讯=主体;/topics /authors

SPA 站注意:锚点形态(`/#faq`、`#inbound-faq`)算"锚点",不算独立 URL——对 AI 可引用性是两种价值。
单页站(仅首页可索引)在矩阵里 7 类为"未发现/锚点",内容资产维度按 ≤40 起评。
