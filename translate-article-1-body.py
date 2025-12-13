#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译第一篇文章的正文段落
Getting Started with Amazon Scraping API
"""

import re

filename = 'zh/articles/getting-started-amazon-scraping-api.html'
print(f"📝 正在翻译正文段落: {filename}")

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义要翻译的段落映射 (原文特征片段 -> 完整中文翻译)
# 注意：这里我们使用 re.sub 来进行替换，尽量匹配完整的 p 标签内容
translations = [
    (
        r'In the competitive world of e-commerce, data is power\. Whether you\'re building a price monitoring tool, analyzing competitor strategies, or conducting market research, access to accurate and real-time Amazon product data is essential\.',
        '在竞争激烈的电商世界中，数据就是力量。无论您是构建价格监控工具、分析竞争对手策略，还是进行市场研究，获取准确且实时的 Amazon 产品数据至关重要。'
    ),
    (
        r'However, scraping Amazon data at scale comes with significant challenges: CAPTCHAs, IP bans, changing HTML structures, and complex anti-bot measures\. That\'s where <span class="text-accent-cyan font-semibold">Pangol Info\'s Amazon Scraping API</span> comes in\.',
        '然而，大规模抓取 Amazon 数据面临着巨大挑战：验证码、IP 封禁、不断变化的 HTML 结构以及复杂的反爬虫措施。这正是 <span class="text-accent-cyan font-semibold">Pangol Info Amazon 数据抓取 API</span> 发挥作用的地方。'
    ),
    (
        r'In this comprehensive guide, we\'ll walk you through everything you need to know to get started with our API, from obtaining your API key to making your first request and handling complex data extraction scenarios\.',
        '在这份综合指南中，我们将带您了解开始使用我们需要知道的一切，从获取 API 密钥到发送第一个请求以及处理复杂的数据提取场景。'
    ),
    # Why Amazon Product Data Extraction Matters
    (
        r'Amazon is the world\'s largest e-commerce marketplace, making it a goldmine of data for businesses and developers\. Extracting this data allows you to:',
        'Amazon 是全球最大的电商市场，对于企业和开发者来说是一个巨大的数据金矿。提取这些数据可以帮助您：'
    ),
    (
        r'Monitor price changes in real-time across millions of products',
        '实时监控数百万种产品的价格变化'
    ),
    (
        r'Track competitor inventory levels and stock availability',
        '跟踪竞争对手的库存水平和供货情况'
    ),
    (
        r'Analyze product reviews and sentiment to improve your own offerings',
        '分析产品评论和情感，以改进您自己的产品'
    ),
    (
        r'Discover trending products and profitable niches',
        '发现热门产品和有利可图的利基市场'
    ),
    (
        r'Optimize your advertising campaigns based on competitor keywords',
        '根据竞争对手的关键词优化您的广告活动'
    ),
    # Understanding Pangol Info's API
    (
        r'Our API handles all the heavy lifting of web scraping, including proxy rotation, CAPTCHA solving, and browser rendering\. You simply send a request to our endpoint, and we return structured JSON data containing all the product details you need\.',
        '我们的 API 处理所有繁重的网页抓取工作，包括代理轮换、验证码解析和浏览器渲染。您只需向我们的端点发送请求，我们就会返回包含您所需的所有产品详情的结构化 JSON 数据。'
    ),
    (
        r'Key features include:',
        '主要功能包括：'
    ),
    (
        r'<strong>High Success Rate:</strong> 99\.9% success rate with automated retries',
        '<strong>高成功率：</strong> 99.9% 的成功率，支持自动重试'
    ),
    (
        r'<strong>Real-Time Data:</strong> Get fresh data directly from Amazon live pages',
        '<strong>实时数据：</strong> 直接从 Amazon 实时页面获取最新数据'
    ),
    (
        r'<strong>Geo-Targeting:</strong> Scrape data from any Amazon marketplace region \(US, UK, DE, JP, etc\.\)',
        '<strong>地理定位：</strong> 从任何 Amazon 市场区域（美国、英国、德国、日本等）抓取数据'
    ),
    (
        r'<strong>Scalable Infrastructure:</strong> Handle millions of requests per day without blocking',
        '<strong>可扩展架构：</strong> 每天处理数百万个请求而不会被阻止'
    ),
    # Getting Started: Prerequisites
    (
        r'Before we dive into the code, make sure you have the following:',
        '在深入代码之前，请确保您具备以下条件：'
    ),
    (
        r'A <strong>Pangol Info account</strong> \(Sign up for free to get 1,000 credits\)',
        '一个 <strong>Pangol Info 账户</strong>（免费注册可获得 1,000 积分）'
    ),
    (
        r'Your unique <strong>API Key</strong> from the dashboard',
        '控制台中您唯一的 <strong>API Key</strong>'
    ),
    (
        r'Python installed on your machine \(or any HTTP client like Postman or cURL\)',
        '您的机器上已安装 Python（或任何 HTTP 客户端，如 Postman 或 cURL）'
    ),
    # Authentication and API Basics
    (
        r'All requests to the Pangol Info API must be authenticated using your API token\. You can pass the token either as a query parameter or in the authorization header\.',
        '所有对 Pangol Info API 的请求都必须使用您的 API 令牌进行身份验证。您可以将令牌作为查询参数传递，也可以在授权标头中传递。'
    ),
    (
        r'The base endpoint for scraping is:',
        '抓取的基础端点是：'
    ),
    (
        r'For security reasons, we recommend setting your API token as an environment variable rather than hardcoding it in your scripts\.',
        '出于安全原因，建议将您的 API 令牌设置为环境变量，而不是将其硬编码在脚本中。'
    ),
    # Extracting Product Data
    (
        r'Now let\'s look at how to extract various types of data from Amazon\.',
        '现在让我们看看如何从 Amazon 提取各种类型的数据。'
    ),
    (
        r'To scrape a product detail page, you need the product\'s ASIN \(Amazon Standard Identification Number\) or the full product URL\.',
        '要抓取产品详情页，您需要产品的 ASIN（Amazon 标准识别码）或完整的产品 URL。'
    ),
    (
        r'Here\'s a simple Python script to get product title, price, and rating:',
        '这是一个简单的 Python 脚本，用于获取产品标题、价格和评分：'
    ),
    # Understanding Response
    (
        r'The API returns a JSON object with a <code[^>]*>scraped_content</code> field containing the parsed data\. Here\'s what the structure looks like:',
        'API 返回一个包含 <code class="text-accent-cyan">scraped_content</code> 字段的 JSON 对象，其中包含解析后的数据。结构如下所示：'
    ),
    # Price Monitoring
    (
        r'One of the most common use cases is tracking price history\. You can set up a scheduled job \(cron job\) to run this script periodically and save the data to a database\.',
        '最常见的用例之一是跟踪价格历史。您可以设置定时任务（cron job）定期运行此脚本并将数据保存到数据库。'
    ),
    # Best Practices
    (
        r'To ensure optimal performance and minimize errors, follow these best practices:',
        '为确保最佳性能并最大限度地减少错误，请遵循以下最佳实践：'
    ),
    (
        r'<strong>Respect Rate Limits:</strong> While our API handles rotation, sending too many concurrent requests might trigger account-level limits\. Start with 5-10 concurrent threads\.',
        '<strong>遵守速率限制：</strong> 虽然我们的 API 处理轮换，但发送过多并发请求可能会触发账户级限制。建议从 5-10 个并发线程开始。'
    ),
    (
        r'<strong>Error Handling:</strong> Always wrap your API calls in try-except blocks to handle network timeouts or parsing errors gracefully\.',
        '<strong>错误处理：</strong> 始终将 API 调用包装在 try-except 块中，以优雅地处理网络超时或解析错误。'
    ),
    (
        r'<strong>Use Webhooks:</strong> For large-scale scraping, use our async webhooks processing to receive results without keeping connections open\.',
        '<strong>使用 Webhooks：</strong> 对于大规模抓取，请使用我们的异步 Webhooks 处理来接收结果，而无需保持连接打开。'
    ),
    # Conclusion
    (
        r'Getting started with Amazon data extraction doesn\'t have to be complicated\. with Pangol Info\'s API, you can focus on analyzing the data rather than fighting anti-bot measures\.',
        '开始 Amazon 数据提取并不一定很复杂。使用 Pangol Info 的 API，您可以专注于分析数据，而不是与反爬虫措施作斗争。'
    ),
]

for pattern, replacement in translations:
    # 尝试直接替换文本内容
    # 使用 re.sub 进行替换，忽略大小写以防万一
    # 我们匹配原始文本，不做复杂的正则，除非必要
    
    # 简单的文本替换
    if '\\' not in pattern:
        content = content.replace(pattern.replace('\\', ''), replacement)
    else:
        # 正则替换
        content = re.sub(pattern, replacement, content)

print("✅ 翻译完成")

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)
