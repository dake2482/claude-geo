---
name: geo-llms
description: "llms.txt 三态检测(未部署/假部署/已部署)、规范化校验(llmstxt.org 格式)与生成。Use when the user mentions llms.txt, llms-full.txt, AI 内容协议, or wants to generate/fix one."
user-invocable: true
argument-hint: "[url|generate <url>]"
license: MIT
metadata:
  version: "0.1.0"
  category: geo
---

# llms.txt 检测与生成

## 三态检测(必验 content-type,不能只看状态码)

| 状态 | 判定 | 证据 |
|---|---|---|
| 404 / 4xx | **未部署** | 状态码 |
| 200 但 `content-type: text/html` 且正文与首页 HTML 一致 | **假部署**(SPA 通配回退) | MD5 比对 |
| 200 且 `text/plain` | **已部署**,再走规范校验 | 头 + 内容 |

同时探测 `/llms-full.txt`(常见同病:被 SPA 回退成 HTML)。

## 规范校验(llmstxt.org 社区规范)

- H1 站点名称;blockquote 一句话摘要
- `## 分节`(Docs / FAQ / Legal / API 等)
- 每条:`- [标题](URL): 一句话描述` —— **必须是真 Markdown 链接**,纯文本 `Docs: URL` 行不合格(Lighthouse llms-txt 检查会 fail)
- 链接目标必须匿名可达(实测状态码,登录墙后的 URL 不许进)
- 高价值机器可读资产(如公开 API catalog JSON)应单列并置前

## 生成

从 sitemap + 站内抽样生成,模板:

```
# <品牌名>

> <一句话品牌定义,含业务关键词>

## Docs
- [标题](https://...): 描述

## FAQ
...

## Legal
...

## Machine-readable
- [public-api-catalog.json](https://...): 130+ endpoints, model catalog
```

事实底线:**llms.txt 被 Google Search 忽略**;其价值面向 Perplexity/第三方 agent 的发现入口,报告措辞不得宣称 Google 排名收益。
