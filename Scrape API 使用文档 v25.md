# Scrape API 使用文档 (v25.09)

## 目录
1. [API 产品概览](#api-产品概览)
2. [基础信息](#基础信息)
   - [Base URL](#base-url)
   - [认证接口](#认证接口)
3. [Amazon Scrape API](#amazon-scrape-api)
   - [同步接口](#同步接口)
   - [异步接口](#异步接口)
4. [通用采集 API](#通用采集-api)
5. [SERP API](#serp-api)
   - [SERP API](#serp-api-1)
   - [SERP API Plus](#serp-api-plus)
6. [AI Mode SERP API](#ai-mode-serp-api)
7. [Keyword Trends API](#keyword-trends-api)

---

## API 产品概览

| 产品名称 | 通用采集 API | AI Mode SERP API |
|---------|-------------|----------------|
| **Amazon Scrape API** | 通用型站点 API：通过同步接口获取**各类通用网站**的公开数据，返回原始 HTML（已压缩）或免费转换后的 Markdown 格式 | 对于部分搜索结果中包含的 AI 概述模块，AI Mode SERP API 能够抓取、提取并解析这些信息，助力卖家理解用户真实意图，把握前沿消费趋势 |
| 可动态兼容 Amazon 页面结构变化，返回结构化页面数据或页面原始 HTML（已压缩）或免费转换后的 Markdown 格式 | 通用采集 API 一般网页抓取成功率可达 90% 以上 | |
| [同步接口](#同步接口)（适合需要即时响应的电商数据需求） | | |
| [异步接口](#异步接口)（适合处理大批量、非即时性的电商数据采集任务） | | |
| **SERP API** | **Keyword Trends API** | |
| SERP API 接口提供根据关键词返回从搜索引擎中返回搜索结果，帮助卖家快速洞察市场趋势与热门品类，辅助精准选品。通过设置参数，可以返回 10 个结果（SERP API）或最多 100 个结果（SERP API Plus）。 | 获取关键词在不同时间段、地区的热度变化趋势。支持跨区域对比、历史波动分析，帮助电商卖家洞察市场趋势、把握关键词热度变化。 | |

---

## 基础信息

### Base URL

```shell
https://scrapeapi.pangolinfo.com
```

### 认证接口

**接口说明**：获取长期有效的访问凭证 Token

- **请求 URL**：`https://scrapeapi.pangolinfo.com/api/v1/auth`
- **请求方法**：`POST`
- **请求头**：

| 参数名 | 参数值 | 类型 | 说明 |
|--------|--------|------|------|
| Content-Type | application/json | string | |

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| email | Y | string | 注册邮箱 |
| password | Y | string | 密码 |

- **请求示例**：
```shell
curl -X POST https://scrapeapi.pangolinfo.com/api/v1/auth \
-H 'Content-Type: application/json' \
-d '{"email": "xxxx@gmail.com", "password": "xxxx"}'
```

- **返回示例**：
```json
{
  "code": 0,
  "message": "ok",
  "data": "xxxx"
}
```

- **返回值说明**：

| 返回值 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 信息 |
| data | string | 认证返回 token |

- **状态码说明**：

| 状态码 | 描述 |
|--------|------|
| 0 | 成功 |
| 1004 | 无效 token |
| 2001 | 积点余额不足 |
| 2007 | 账户已过期 |
| 10000 / 10001 | 爬取失败 |
| 404 | URL 地址错误 |

---

## Amazon Scrape API

### 接口介绍

可动态兼容 Amazon 等各类电商页面结构变化。该接口通过智能识别算法自动识别并提取相关产品数据，如标题、折扣、价格、可用性和描述等。开发者无需关注目标页面 DOM 结构变更，系统将持续维护数据解析逻辑。

**支持国家**：美国、英国、法国、德国（更多国家持续支持中）

**平均响应时间**：10 秒

**积点消耗说明**：

| format 参数 | 扣除积点数 |
|-------------|-----------|
| json（获取解析后的字段） | 1 个/次 |
| rawHtml、markdown（获取源文件） | 0.75 个/次 |

### 同步接口

#### 提交任务

- **请求 URL**：`https://scrapeapi.pangolinfo.com/api/v1/scrape`
- **请求方法**：`POST`
- **请求头**：

| 参数名 | 参数值 | 类型 | 说明 |
|--------|--------|------|------|
| Content-Type | application/json | string | |
| Authorization | Bearer xxxx | string | 认证 Token |

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| url | Y | string | 目标网页 URL |
| parserName | Y | string | 解析器名称（json 格式时必须填写） |
| format | Y | string | 数据返回格式（json/rawHtml/markdown） |
| bizContext | N | Object | 业务上下文（如邮编地址） |

#### format 参数说明

| 可选项 | 对应产品 | 扣除积点数 |
|--------|----------|-----------|
| markdown | Scrape API(RAW) | 0.75 个/次 |
| rawHtml | Scrape API(RAW) | 0.75 个/次 |
| json | Scrape API | 1 个/次 |

> **注**：format 选择 "json"，则必须填写 "parserName" 参数，否则不用填写

#### parserName 解析器参数说明

| 解析器名称 | 解析模板 |
|------------|----------|
| amzProductDetail | 商品详情 |
| amzKeyword | 关键词 |
| amzProductOfCategory | 商品分类列表 |
| amzProductOfSeller | 卖家商品列表 |
| amzBestSellers | 热销榜 |
| amzNewReleases | 新品榜 |

#### bizContext 业务上下文参数说明

| 参数名 | 描述 | 备注 |
|--------|------|------|
| zipcode | 邮编 | Amazon 站点必须填写邮编参数 |

**支持邮编**：

| 国家 | 支持邮编 |
|------|----------|
| 美国 | "10041", "90001", "60601", "84104" |
| 英国 | "W1S3AS", "EH151LR", "M139PL", "M25BQ" |
| 法国 | "75000", "69001", "06000", "13000" |
| 德国 | "80331", "10115", "20095", "60306" |

#### 请求示例

```shell
curl -X POST https://scrapeapi.pangolinfo.com/api/v1/scrape \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer xxxx' \
-d '{
  "url": "https://www.amazon.com/dp/B0DYTF8L2W",
  "parserName": "amzProductDetail",
  "format": "json",
  "bizContext": {
    "zipcode": "10041"
  }
}'
```

#### 返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "json": [
      {
        "code": 0,
        "data": {
          "results": [
            {
              "asin": "B0DYTF8L2W",
              "title": "Sweetcrispy Convertible Sectional Sofa Couch...",
              "price": "$...",
              "star": "4.4",
              "rating": "22",
              "image": "https://...",
              "images": ["https://...", "..."],
              "brand": "Sweetcrispy",
              "description": "...",
              "sales": "...",
              "seller": "...",
              "shipper": "...",
              "merchant_id": "null",
              "color": "Beige",
              "size": "...",
              "has_cart": false,
              "otherAsins": ["..."],
              "coupon": "null",
              "category_id": "3733551",
              "category_name": "Sofas & Couches",
              "product_dims": "20.07\"D x 126.77\"W x 24.01\"H",
              "pkg_dims": "20.07\"D x 126.77\"W x 24.01\"H",
              "product_weight": "47.4 Pounds",
              "reviews": {...},
              "customerReviews": "...",
              "first_date": "...",
              "deliveryTime": "...",
              "additional_details": false
            }
          ]
        },
        "message": "ok"
      }
    ],
    "url": "https://www.amazon.com/dp/B0DYTF8L2W",
    "taskId": "45403c7fd7c148f280d0f4f7284bc9e9"
  }
}
```

#### 返回值说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 信息 |
| data | object | 返回数据 |

#### 返回参数 'data' 说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| json | []string | 返回 JSON 数据 |
| url | string | 任务 URL |
| taskId | string | 任务 ID |

#### 各解析器返回数据说明

##### amzProductDetail（商品详情）

| 参数 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 码 |
| title | string | 商品标题 |
| price | string | 商品价格 |
| star | string | 商品评分 |
| rating | string | 商品评分数 |
| image | string | 图片链接 |
| images | []string | 图片集 |
| sales | string | 商品销量 |
| seller | string | 卖家 |
| shipper | string | 发货人 |
| merchant_id | string | 卖家 ID |
| color | string | 颜色 |
| size | string | 尺寸 |
| brand | string | 品牌 |
| has_cart | bool | 是否有购物车 |
| otherAsins | []string | 关联 ASIN |
| description | string | 商品描述 |
| deliveryTime | string | 发货时间 |
| coupon | string | 优惠券 |
| customerReviews | []string | 客户评论 |
| category_id | string | 类目 ID |
| pkg_dims | string | 包裹尺寸 |
| pkg_weight | string | 包裹重量 |
| product_dims | string | 商品尺寸 |
| product_weight | string | 商品重量 |
| first_date | string | 上市时间 |

##### amzKeyword（关键词）

| 参数 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 码 |
| title | string | 商品标题 |
| price | string | 商品价格 |
| star | string | 商品评分 |
| rating | string | 商品评分数 |
| image | string | 图片链接 |
| sales | string | 商品销量 |
| nature_rank | int | 自然排名 |
| sponsored | string | 是否 SP 广告 |

##### amzProductOfCategory（商品分类列表）

| 参数 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 码 |
| title | string | 商品标题 |
| price | string | 商品价格 |
| star | string | 商品评分 |
| rating | string | 商品评分数 |
| image | string | 图片链接 |

##### amzProductOfSeller（卖家商品列表）

| 参数 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 码 |
| title | string | 商品标题 |
| price | string | 商品价格 |
| star | string | 商品评分 |
| rating | string | 商品评分数 |
| image | string | 图片链接 |

##### amzBestSellers（热销榜）

| 参数 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 码 |
| rank | string | 榜单排名 |
| title | string | 商品标题 |
| price | string | 商品价格 |
| star | string | 商品评分 |
| rating | string | 商品评分数 |
| image | string | 图片链接 |

##### amzNewReleases（新品榜）

| 参数 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN 码 |
| rank | string | 榜单排名 |
| title | string | 商品标题 |
| price | string | 商品价格 |
| star | string | 商品评分 |
| rating | string | 商品评分数 |
| image | string | 图片链接 |

---

### 异步接口

#### 简要描述

异步接口，需要额外部署接收程序。提供 Java、Go、Python 三种语言的示例代码。

- **Java 接收程序**：[Java-data-receive.zip](https://www.pangolinfo.com/wp-content/uploads/2024/08/data-receiver.zip) (92.3KB)
- **Go 接收程序**：[Go-data-receiver.zip](https://www.pangolinfo.com/wp-content/uploads/2024/10/go-data-receiver.zip) (7KB)
- **Python 接收程序**：[Py-data-receiver.zip](https://www.pangolinfo.com/wp-content/uploads/2024/10/py-data-receiver.zip) (1KB)

#### 提交任务

- **请求 URL**：`https://extapi.pangolinfo.com/api/v1/scrape/async`
- **请求方法**：`POST`
- **请求头**：

| 参数名 | 参数值 | 类型 | 说明 |
|--------|--------|------|------|
| Content-Type | application/json | string | |
| Authorization | Bearer xxxx | string | 认证 Token |

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| url | Y | string | 目标网页 URL |
| callbackUrl | Y | string | 接收数据的服务地址 |
| bizKey | Y | string | 业务类型（见下表） |
| zipcode | Y | string | 亚马逊邮编信息 |

#### bizKey 业务类型说明

| bizKey | 描述 |
|--------|------|
| amzProductDetail | 获取商品详情 |
| amzKeyword | 根据关键字获取商品列表 |
| amzProductOfCategory | 根据商品类别获取商品列表 |
| amzProductOfSeller | 根据卖家获取商品列表 |
| amzBestSellers | 热卖榜 |
| amzNewReleases | 新品榜 |

#### 请求示例

```shell
curl -X POST https://extapi.pangolinfo.com/api/v1/scrape/async \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer xxxx' \
-d '{
  "url": "https://www.amazon.com/dp/B0DYTF8L2W",
  "callbackUrl": "https://your-server.com/receive",
  "bizKey": "amzProductDetail",
  "zipcode": "10041"
}'
```

#### 返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "data": "e7da6144bed54df7a2891e98fdc8d517",
    "bizMsg": "ok",
    "bizCode": 0
  }
}
```

#### 返回值说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 信息 |
| data | object | 返回数据 |

#### 返回参数 'data' 说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| data | string | 任务 ID |
| bizMsg | string | Amazon 返回的业务信息 |
| bizCode | int | Amazon 返回的业务状态码 |

#### 积点消耗说明

| 操作 | 消耗积点数 |
|------|-----------|
| 获取解析后的字段 | 1 个/次 |

---

## 通用采集 API

### 接口介绍

作为数据解决方案中的全能型产品，通用采集 API 不局限于电商数据，提供覆盖新闻、社交媒体、论坛、企业官网等多样化网站的公开数据采集能力。通过稳定的同步 API 接口，可实时获取舆情动态、行业趋势、竞品信息等关键商业情报。

**平均响应时间**：40 秒

**抓取成功率**：90% 以上

**积点消耗说明**：

| format 参数 | 消耗积点数 |
|-------------|-----------|
| rawHtml、markdown（获取源文件） | 1 个/次 |

### 批量提交任务接口（同步）

- **请求 URL**：`https://scrapeapi.pangolinfo.com/api/v1/scrape/batch`
- **请求方法**：`POST`
- **请求头**：

| 参数名 | 参数值 | 类型 | 说明 |
|--------|--------|------|------|
| Content-Type | application/json | string | |
| Authorization | Bearer xxxx | string | 认证 Token |

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| urls | Y | []string | 目标网页 URLs |
| format | Y | string | rawHtml 或 markdown |
| timeout | N | int | 超时时间（单位：毫秒） |

#### 请求示例

```shell
curl -X POST https://scrapeapi.pangolinfo.com/api/v1/scrape/batch \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer xxxx' \
-d '{
  "urls": [
    "https://www.amazon.com/dp/B0B41YH9B6"
  ],
  "format": "rawHtml"
}'
```

#### 返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": [
    {
      "rawHtml": ["{\"code\":0,\"data\":{\"results\":[...]}"],
      "url": "https://www.amazon.com/dp/B0B41YH9B6",
      "taskId": "89b47267873c4fda99b21aeabd2fe851"
    }
  ]
}
```

#### 返回值说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 信息 |
| data | object | 返回数据 |

#### 返回参数 'data' 说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| json | []string | 返回 JSON 数据 |
| url | string | 任务 URL |
| taskId | string | 任务 ID |

---

## SERP API

### 接口介绍

SERP API 接口提供根据关键词返回从搜索引擎中返回搜索结果，帮助卖家快速洞察市场趋势与热门品类，辅助精准选品。通过设置参数，可以返回 10 个结果（SERP API）或最多 100 个结果（SERP API Plus）。

**平均响应时间**：10 秒

**积点消耗说明**：

| 接口类型 | resultNum 参数 | 扣除积点数 |
|----------|----------------|-----------|
| SERP API（每个请求返回 10 个结果） | 10 (Default) | 0.5 个/次 |
| SERP API Plus（每个请求返回最多 100 个结果） | 100 | 1 个/次 |

### SERP API

#### 创建任务

- **请求 URL**：`https://scrapeapi.pangolinfo.com/api/v1/scrape`
- **请求方法**：`POST`
- **请求头**：

| 参数名 | 参数值 | 类型 | 说明 |
|--------|--------|------|------|
| Content-Type | application/json | string | |
| Authorization | Bearer xxxx | string | 认证 Token |

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| url | Y | string | 目标网页 URL（Google 搜索结果页） |
| parserName | Y | string | 解析器名称（如 "googleSearch"） |
| format | Y | string | 数据返回格式（json） |
| scrapeContext | N | Object | 配置参数，如 `{"resultNum": 10, "region": "us"}` |

#### 请求示例

```shell
curl -X POST https://scrapeapi.pangolinfo.com/api/v1/scrape \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer xxxx' \
-d '{
  "url": "https://www.google.com/search?q=how+java+work",
  "scrapeContext": {
    "resultNum": 10,
    "region": "us"
  },
  "format": "json",
  "parserName": "googleSearch"
}'
```

#### 返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "json": [
      {
        "code": 0,
        "data": {
          "items": [
            {
              "type": "organic",
              "items": [
                {
                  "text": "Medium · Fasrin Aleem...",
                  "type": "organic",
                  "title": "Let's Understand Java. How Java Works? | by Fasrin Aleem",
                  "url": "https://medium.com/nerd-for-tech/lets-understand-java-261b2e6bcf2e"
                },
                {
                  "text": "Microsoft Azure...",
                  "type": "organic",
                  "title": "What is Java?---Beginner's Guide to Java",
                  "url": "https://azure.microsoft.com/..."
                }
              ]
            },
            {
              "type": "related_searches",
              "items": [
                "How java work step by step",
                "How java work for beginners",
                "Features of Java",
                "What is Java programming used for",
                "Java tutorial",
                "Java compiler",
                "History of Java",
                "What is Java language"
              ]
            }
          ]
        },
        "message": "ok"
      }
    ],
    "url": "https://www.google.com/search?q=how+java+work&gl=us&lr=lang_en",
    "taskId": "b6d9022f693b44f6bd7a87b31112df00"
  }
}
```

#### 返回值说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 信息 |
| data | object | 返回数据 |

#### 返回参数 'data' 说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| json | []string | 返回 JSON 数据 |
| url | string | 任务 URL |
| taskId | string | 任务 ID |

#### 返回 JSON 数据说明

| 参数 | 类型 | 说明 |
|------|------|------|
| type | string | 搜索结果类型（organic/related_searches） |
| url | string | 搜索结果链接 |
| title | string | 搜索结果标题 |
| text | string | 搜索结果内容 |

---

### SERP API Plus

#### 创建任务

- **请求 URL**：`https://scrapeapi.pangolinfo.com/api/v1/scrape`
- **请求方法**：`POST`
- **请求头**：同 SERP API

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| url | Y | string | 目标网页 URL |
| parserName | Y | string | 解析器名称（"googleSearch"） |
| format | Y | string | 数据返回格式（json） |
| scrapeContext | N | Object | 配置参数，如 `{"resultNum": 100, "region": "us"}` |

#### 请求示例

```shell
curl -X POST https://scrapeapi.pangolinfo.com/api/v1/scrape \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer xxxx' \
-d '{
  "url": "https://www.google.com/search?q=how+java+work",
  "scrapeContext": {
    "resultNum": 100,
    "region": "us"
  },
  "format": "json",
  "parserName": "googleSearch"
}'
```

#### 返回示例

结构同 SERP API，但会返回最多 100 条结果。

---

## AI Mode SERP API

### 接口介绍

对于部分搜索结果中包含的 AI 概述模块，AI Mode SERP API 能够抓取、提取并解析这些信息，助力卖家理解用户真实意图，把握前沿消费趋势。

**平均响应时间**：10 秒

**积点消耗说明**：2 个/次（获取完整的 AI Overview 信息）

### 创建任务

- **请求 URL**：`https://scrapeapi.pangolinfo.com/api/v1/scrape`
- **请求方法**：`POST`
- **请求头**：

| 参数名 | 参数值 | 类型 | 说明 |
|--------|--------|------|------|
| Content-Type | application/json | string | |
| Authorization | Bearer xxxx | string | 认证 Token |

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| url | Y | string | 目标网页 URL |
| parserName | Y | string | 解析器名称（"googleAiSearch"） |
| format | Y | string | 数据返回格式（json） |
| scrapeContext | Y | Object | 配置参数，必须包含 `{"aiOverview": true, "region": "us"}` |

### 请求示例

```shell
curl -X POST https://scrapeapi.pangolinfo.com/api/v1/scrape \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer xxxx' \
-d '{
  "url": "https://www.google.com/search?q=how+does+java+work",
  "scrapeContext": {
    "aiOverview": true,
    "region": "us"
  },
  "format": "json",
  "parserName": "googleAiSearch"
}'
```

### 返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "json": [
      {
        "code": 0,
        "data": {
          "type": "organic",
          "items": [
            {
              "references": [],
              "type": "ai_overview",
              "items": [
                {
                  "type": "ai_overview_elem",
                  "content": [
                    "Java's functionality revolves around the principle of \"write once, run anywhere\" (WORA)..."
                  ]
                },
                {
                  "type": "ai_overview_elem",
                  "content": [
                    "Writing Source Code:",
                    "Compilation:",
                    "Writing Source Code: Developers write Java programs using the Java programming language...",
                    "Compilation: The Java Compiler, part of the JDK, translates the .java source files into bytecode..."
                  ]
                }
              ]
            },
            {
              "type": "organic",
              "items": [
                {
                  "text": "Medium · Fasrin Aleem...",
                  "type": "organic",
                  "title": "Let's Understand Java. How Java Works? | by Fasrin Aleem",
                  "url": "https://medium.com/nerd-for-tech/lets-understand-java-261b2e6bcf2e"
                }
              ]
            }
          ]
        },
        "message": "ok"
      }
    ],
    "url": "https://www.google.com/search?q=how+does+java+work&gl=us&lr=lang_en",
    "taskId": "a8393aa101154c559a75ab998fb52714"
  }
}
```

### 返回值说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 信息 |
| data | object | 返回数据 |

### 返回参数 'data' 说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| json | []string | 返回 JSON 数据 |
| url | string | 任务 URL |
| taskId | string | 任务 ID |

### 返回参数 'json' 说明

| 参数 | 类型 | 说明 |
|------|------|------|
| type | string | 搜索结果类型 |
| url | string | 搜索结果链接 |
| title | string | 搜索结果标题 |
| text | string | 搜索结果内容 |

### 返回参数 'ai overview' 说明

| 参数 | 类型 | 说明 |
|------|------|------|
| title | string | 标题 |
| content | string | 内容 |

### 返回参数 'references' 说明

| 参数 | 类型 | 说明 |
|------|------|------|
| title | string | 标题 |
| url | string | 链接 |
| snippet | string | 内容 |
| sourceName | string | 数据来源 |

---

## Keyword Trends API

### 接口介绍

获取关键词在不同时间段、地区的热度变化趋势。支持跨区域对比、历史波动分析，帮助电商卖家洞察市场趋势、把握关键词热度变化。

**平均响应时间**：10 秒

**积点消耗说明**：1.5 个/次

### 创建任务

- **请求 URL**：`https://scrapeapi.pangolinfo.com/api/v1/scrape`
- **请求方法**：`POST`
- **请求头**：

| 参数名 | 参数值 | 类型 | 说明 |
|--------|--------|------|------|
| Content-Type | application/json | string | |
| Authorization | Bearer xxxx | string | 认证 Token |

- **请求参数（Body）**：

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| url | Y | string | 目标网页 URL（Google Trends） |
| parserName | Y | string | 解析器名称（"googleTrends"） |
| format | Y | string | 数据返回格式（json） |
| scrapeContext | Y | Object | 配置参数，包含 keywords 和 time 范围 |

#### scrapeContext 示例

```json
{
  "keywords": ["men's running shoes", "women's running shoes"],
  "time": "2025-02-28 2025-07-28"
}
```

### 请求示例

```shell
curl -X POST https://scrapeapi.pangolinfo.com/api/v1/scrape \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer xxxx' \
-d '{
  "url": "https://trends.google.com",
  "scrapeContext": {
    "keywords": ["men'\''s running shoes"],
    "time": "2025-02-28 2025-03-01"
  },
  "format": "json",
  "parserName": "googleTrends"
}'
```

### 返回示例

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "json": [
      {
        "code": 0,
        "data": {
          "keywords": ["men's running shoes"],
          "items": {
            "data": [
              {
                "formattedAxisTime": "Feb 28",
                "hasData": [true],
                "formattedValue": ["83"],
                "formattedTime": "Feb 28, 2025",
                "time": "1740700800",
                "value": [83]
              },
              {
                "formattedAxisTime": "Mar 1",
                "hasData": [true],
                "formattedValue": ["100"],
                "formattedTime": "Mar 1, 2025",
                "time": "1740787200",
                "value": [100]
              }
            ],
            "queries_list": [
              {
                "rising": [],
                "top": [
                  {
                    "query": "mens running shoes",
                    "hasData": true,
                    "link": "/trends/explore?q=mens+running+shoes&date=2025-02-28+2025-03-01",
                    "formattedValue": "100",
                    "value": 100
                  }
                ],
                "keyword": "men's running shoes"
              }
            ]
          }
        },
        "message": "ok"
      }
    ],
    "url": "https://trends.google.com",
    "taskId": "266040d9b68944d8af075a11075279f8"
  }
}
```

### 返回值说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 信息 |
| data | object | 返回数据 |

### 返回参数 'data' 说明

| 返回值 | 类型 | 说明 |
|--------|------|------|
| json | []string | 返回 JSON 数据 |
| url | string | 任务 URL |
| taskId | string | 任务 ID |

### 返回参数 'json' 说明

| 参数 | 类型 | 说明 |
|------|------|------|
| type | string | 搜索结果类型 |
| data | string | 搜索结果 |
| queries_list | string | 搜索结果列表 |

### 返回参数 'queries_list' 说明

| 参数 | 类型 | 说明 |
|------|------|------|
| keyword | string | 关键词 |
| top | string | 排名 |
| rising | string | 上升趋势 |

---

## 使用提示

1. **认证 Token**：获取后长期有效，请妥善保管
2. **邮编设置**：Amazon 请求必须填写对应国家的邮编
3. **format 参数**：选择 json 时必须指定 parserName
4. **异步接口**：需要部署接收服务并配置 callbackUrl
5. **积点消耗**：不同接口和返回格式消耗不同，请根据需求选择
6. **重试机制**：建议对 10000/10001（爬取失败）错误码实现重试逻辑

---

**文档版本**：v25.09
**更新日期**：2025-12-12
**技术支持**：如有问题请联系技术支持团队