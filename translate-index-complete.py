#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整的中文首页翻译脚本 - 修复版
确保所有英文文本都被翻译
"""

import re

# 读取文件
with open('zh/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 基础设置
content = content.replace('<html lang="en">', '<html lang="zh-CN">')

# 2. SEO Meta Tags
content = content.replace(
    '<title>Amazon Scraping API Blog | E-commerce Data Extraction Tutorials</title>',
    '<title>Amazon 数据抓取 API 博客 | 电商数据提取教程</title>'
)

content = content.replace(
    'Expert Amazon scraping API tutorials and e-commerce data extraction guides. Learn product data intelligence, price monitoring, and competitive analysis with Pangol Info API.',
    '专业的 Amazon 数据抓取 API 教程和电商数据提取指南。学习产品数据智能分析、价格监控和竞争分析。'
)

content = content.replace(
    'Amazon Scraping API, E-commerce Data Extraction, Amazon Product Data, Price Monitoring API, Amazon SERP API',
    'Amazon 数据抓取 API, 电商数据提取, Amazon 产品数据, 价格监控 API, Amazon SERP API'
)

# 3. Open Graph
content = content.replace(
    'Amazon Scraping API & E-commerce Data Extraction | Pangolin Blog',
    'Amazon 数据抓取 API 与电商数据提取 | Pangolin 博客'
)

content = content.replace(
    'Expert insights on Amazon scraping API, e-commerce data extraction, and product intelligence. Real-time pricing, inventory tracking, and competitive analysis.',
    '专业的 Amazon 数据抓取 API 洞察、电商数据提取和产品智能分析。实时价格监控、库存追踪和竞争分析。'
)

content = content.replace(
    'Expert insights on Amazon scraping API, e-commerce data extraction, and product intelligence.',
    '专业的 Amazon 数据抓取 API 洞察、电商数据提取和产品智能分析。'
)

# 4. Schema.org
content = content.replace(
    '"name": "Pangol Info Scrape API Blog"',
    '"name": "Pangol Info 数据抓取 API 博客"'
)

content = content.replace(
    '"description": "Expert insights on Amazon scraping API and e-commerce data extraction"',
    '"description": "专业的 Amazon 数据抓取 API 和电商数据提取洞察"'
)

# 5. 添加 Hreflang
if 'Hreflang Tags' not in content:
    hreflang = '''    <!-- Hreflang Tags -->
    <link rel="alternate" hreflang="en" href="https://blog.pangolinfo.com/index.html">
    <link rel="alternate" hreflang="zh-CN" href="https://blog.pangolinfo.com/zh/index.html">
    <link rel="alternate" hreflang="x-default" href="https://blog.pangolinfo.com/index.html">

'''
    content = content.replace('</head>', hreflang + '</head>')

# 6. 导航栏
content = content.replace('>Home<', '>首页<')
content = content.replace('>Solutions<', '>解决方案<')
content = content.replace('>Use Cases<', '>应用场景<')
content = content.replace('>Blog<', '>博客<')
content = content.replace('>Docs<', '>文档<')
content = content.replace('>Pricing<', '>定价<')
content = content.replace('>Get API Key<', '>获取 API Key<')

# 7. 语言切换器
content = content.replace(
    '<a href="/zh/index.html" class="language-btn">',
    '<a href="/index.html" class="language-btn">'
)
content = re.sub(
    r'<span>🇨🇳</span>\s*<span>中文</span>',
    '<span>🇺🇸</span>\n                        <span>English</span>',
    content
)

# 8. Hero Section - 完整翻译
content = content.replace(
    'AMAZON SCRAPING API & E-COMMERCE DATA INTELLIGENCE',
    'AMAZON 数据抓取 API 与电商数据智能'
)

content = content.replace(
    'Amazon Product Data API',
    'Amazon 产品数据 API'
)

content = content.replace(
    'for E-commerce Intelligence',
    '助力电商智能决策'
)

# 修复 Hero 描述
content = re.sub(
    r'专业的 Amazon API 洞察。电商数据提取和产品智能分析。\s*Discover how\s*Pangol Info\'s Amazon API empowers businesses with real-time pricing,\s*inventory tracking, and',
    '了解 Pangol Info 的 Amazon API 如何通过实时定价、库存跟踪和',
    content
)

content = content.replace(
    'competitive intelligence for data-driven decision making.',
    '竞争情报为企业提供数据驱动的决策支持。'
)

# 按钮文本
content = content.replace('Start Free Trial', '开始免费试用')
content = content.replace('View Documentation', '查看文档')
content = content.replace('API Playground', 'API 演示')

# 9. Solutions Section - 完整翻译
content = content.replace('Pangolin Solutions Section', 'Pangolin 解决方案')
content = content.replace('Powerful Solutions for', '强大的解决方案')
content = content.replace('E-commerce Success', '助力电商成功')
content = content.replace(
    'Comprehensive tools and APIs designed to give you a competitive edge in the Amazon marketplace',
    '全面的工具和 API，助您在 Amazon 市场获得竞争优势'
)

# Solutions 卡片
content = content.replace('Product Data Extraction', '产品数据提取')
content = content.replace(
    'Extract comprehensive product information including titles, prices, ratings, reviews, and specifications',
    '提取全面的产品信息，包括标题、价格、评分、评论和规格参数'
)

content = content.replace('Price Monitoring', '价格监控')
content = content.replace(
    'Track competitor pricing in real-time and optimize your pricing strategy for maximum profitability',
    '实时跟踪竞争对手定价，优化您的定价策略以实现最大盈利'
)

content = content.replace('SERP Analysis', '搜索结果分析')
content = content.replace(
    'Analyze search rankings, sponsored products, and keyword performance to improve visibility',
    '分析搜索排名、赞助产品和关键词表现，提升产品可见度'
)

content = content.replace('Inventory Tracking', '库存追踪')
content = content.replace(
    'Monitor stock levels and availability across multiple sellers to prevent stockouts',
    '监控多个卖家的库存水平和可用性，防止缺货情况'
)

content = content.replace('Review Analytics', '评论分析')
content = content.replace(
    'Gain insights from customer reviews and ratings to improve product quality and customer satisfaction',
    '从客户评论和评分中获取洞察，提升产品质量和客户满意度'
)

content = content.replace('Competitor Intelligence', '竞争情报')
content = content.replace(
    'Stay ahead with detailed competitor analysis including pricing, inventory, and market positioning',
    '通过详细的竞争对手分析保持领先，包括定价、库存和市场定位'
)

# 10. Use Cases Section
content = content.replace('Use Cases', '应用场景')
content = content.replace('Real-World Applications', '实际应用案例')
content = content.replace(
    'See how businesses leverage Pangol Info\'s Amazon API for data-driven growth',
    '了解企业如何利用 Pangol Info 的 Amazon API 实现数据驱动的增长'
)

content = content.replace('Price Optimization', '价格优化')
content = content.replace(
    'Dynamic pricing strategies based on real-time market data',
    '基于实时市场数据的动态定价策略'
)

content = content.replace('Product Research', '产品研究')
content = content.replace(
    'Identify trending products and market opportunities',
    '识别趋势产品和市场机会'
)

content = content.replace('Market Analysis', '市场分析')
content = content.replace(
    'Comprehensive market insights and competitive intelligence',
    '全面的市场洞察和竞争情报'
)

# 11. Latest Articles Section
content = content.replace('Latest Articles', '最新文章')
content = content.replace('Expert Insights & Tutorials', '专家洞察与教程')
content = content.replace(
    'Learn from our comprehensive guides on Amazon API integration and data extraction',
    '从我们关于 Amazon API 集成和数据提取的综合指南中学习'
)

content = content.replace('View All Articles', '查看所有文章')

# 文章标题翻译
articles = {
    'Getting Started with Amazon Scraping API': 'Amazon 数据抓取 API 入门指南',
    'Learn how to leverage Pangol Info\'s Amazon scraping API to extract comprehensive product data, pricing, and reviews from Amazon marketplace.':
    '学习如何利用 Pangol Info 的 Amazon 数据抓取 API 从 Amazon 市场提取全面的产品数据、价格和评论信息。',
    
    'Advanced Amazon Data Extraction Best Practices': 'Amazon 数据提取高级最佳实践',
    'Master advanced techniques for efficient data extraction, rate limiting, and error handling when working with Amazon APIs.':
    '掌握使用 Amazon API 时的高效数据提取、速率限制和错误处理的高级技术。',
    
    'Amazon Product Selection: Using API Data to Find Winning Products': '使用 API 数据选择优质 Amazon 产品',
    'Discover how to use API data to identify profitable products, analyze market trends, and make data-driven product selection decisions.':
    '了解如何使用 API 数据识别盈利产品、分析市场趋势并做出数据驱动的产品选择决策。',
    
    'Amazon Sponsored Products: Monitor Competitor Ad Campaigns': '监控 Amazon 竞争对手广告活动',
    'Track competitor advertising strategies, sponsored product placements, and optimize your own PPC campaigns with real-time data.':
    '跟踪竞争对手的广告策略、赞助产品投放，并使用实时数据优化您自己的 PPC 广告活动。',
    
    'Building Real-Time Amazon Price Monitoring System': '构建实时 Amazon 价格监控系统',
    'Step-by-step guide to creating an automated Amazon price tracking system using Pangol Info\'s e-commerce API.':
    '使用 Pangol Info 的电商 API 创建自动化 Amazon 价格跟踪系统的分步指南。',
    
    'Scale Your Amazon Business with Data-Driven Product Intelligence': '通过数据驱动的产品智能扩展 Amazon 业务',
    'How businesses leverage Pangol Info\'s Amazon API for data-driven growth':
    '企业如何利用 Pangol Info 的 Amazon API 实现数据驱动的增长',
    
    'Real-world case studies showing how businesses achieve 10x growth using data-driven strategies and Amazon API integration.':
    '真实案例研究展示企业如何使用数据驱动策略和 Amazon API 集成实现 10 倍增长。'
}

for en, zh in articles.items():
    content = content.replace(en, zh)

# 12. Newsletter Section
content = content.replace('Stay Updated', '保持更新')
content = content.replace(
    'Subscribe to our newsletter for the latest Amazon API insights and tutorials',
    '订阅我们的新闻通讯，获取最新的 Amazon API 洞察和教程'
)
content = content.replace('Enter your email', '输入您的邮箱')
content = content.replace('Subscribe', '订阅')

# 13. Footer
content = content.replace('Quick Links', '快速链接')
content = content.replace('Resources', '资源')
content = content.replace('Documentation', '文档')
content = content.replace('API Reference', 'API 参考')
content = content.replace('Tutorials', '教程')
content = content.replace('Case Studies', '案例研究')
content = content.replace('Legal', '法律')
content = content.replace('Privacy Policy', '隐私政策')
content = content.replace('Terms of Service', '服务条款')
content = content.replace(
    '© 2025 Pangol Info Scrape API. All rights reserved.',
    '© 2025 Pangol Info Scrape API. 保留所有权利。'
)

# 14. 其他常见词汇
content = content.replace(' min read', ' 分钟阅读')
content = content.replace('Read More', '阅读更多')

# 保存
with open('zh/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 中文首页完整翻译完成！")
