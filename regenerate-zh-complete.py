#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整重新生成中文HTML
读取英文HTML，翻译所有可见文本，保留品牌/产品名称
"""

import re

# 读取英文HTML作为基础
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("📖 正在读取英文HTML...")
print(f"文件大小: {len(content)} 字符")

# ============ 第一步：基础设置 ============
# 修改 lang 属性
content = content.replace('<html lang="en">', '<html lang="zh-CN">')

# ============ 第二步：SEO Meta Tags ============
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

# Open Graph
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

# Schema.org
content = content.replace(
    '"name": "Pangol Info Scrape API Blog"',
    '"name": "Pangol Info 数据抓取 API 博客"'
)

content = content.replace(
    '"description": "Expert insights on Amazon scraping API and e-commerce data extraction"',
    '"description": "专业的 Amazon 数据抓取 API 和电商数据提取洞察"'
)

# ============ 第三步：添加 Hreflang ============
if 'Hreflang Tags' not in content:
    hreflang = '''    <!-- Hreflang Tags -->
    <link rel="alternate" hreflang="en" href="https://blog.pangolinfo.com/index.html">
    <link rel="alternate" hreflang="zh-CN" href="https://blog.pangolinfo.com/zh/index.html">
    <link rel="alternate" hreflang="x-default" href="https://blog.pangolinfo.com/index.html">

'''
    content = content.replace('</head>', hreflang + '</head>')

# ============ 第四步：导航栏 ============
content = content.replace('>Home<', '>首页<')
content = content.replace('>Solutions<', '>解决方案<')
content = content.replace('>Use Cases<', '>应用场景<')
content = content.replace('>Blog<', '>博客<')
content = content.replace('>Docs<', '>文档<')
content = content.replace('>Pricing<', '>定价<')
content = content.replace('>Get API Key<', '>获取 API Key<')

# 语言切换器 - 中文页面显示 English
content = re.sub(
    r'<a href="/zh/index\.html" class="language-btn">\s*<span>🇨🇳</span>\s*<span>中文</span>',
    '<a href="/index.html" class="language-btn">\n                        <span>🇺🇸</span>\n                        <span>English</span>',
    content
)

# ============ 第五步：Hero Section ============
content = re.sub(
    r'Amazon Scraping API & E-commerce Data Intelligence',
    'AMAZON 数据抓取 API 与电商数据智能',
    content
)

content = content.replace('Amazon Product Data API', 'Amazon 产品数据 API')
content = content.replace('for E-commerce Intelligence', '助力电商智能决策')

# Hero 描述 - 使用正则处理跨行
content = re.sub(
    r'Expert insights on Amazon scraping API, e-commerce data extraction, and product intelligence\.\s*Discover\s*how Pangol Info\'s Amazon API empowers businesses with real-time pricing, inventory tracking, and\s*competitive analysis\.',
    '从 Amazon 市场获取实时产品数据、价格智能和竞争洞察。了解 Pangol Info 的 Amazon API 如何通过实时定价、库存跟踪和竞争情报为企业提供数据驱动的决策支持。',
    content,
    flags=re.DOTALL
)

content = content.replace('Start Free Trial', '开始免费试用')
content = content.replace('API Playground', 'API 演示')

# ============ 第六步：Stats Section ============
content = content.replace('API Uptime', 'API 正常运行时间')
content = content.replace('Daily Amazon API Calls', '每日 API 调用次数')
content = content.replace('E-commerce Businesses', '电商企业客户')
content = content.replace('Amazon Ad Coverage', '广告数据覆盖率')

# ============ 第七步：Solutions Section ============
content = content.replace('Amazon & E-commerce Data Solutions', 'Amazon 与电商数据解决方案')
content = re.sub(
    r'Professional APIs for Amazon product data, pricing intelligence, and e-commerce\s*analytics',
    '专业的 Amazon 产品数据、价格智能和电商分析 API 服务',
    content
)

content = content.replace('Amazon Scraping API', 'Amazon 数据抓取 API')
content = re.sub(
    r'Complete Amazon product data extraction and e-commerce\s*intelligence',
    '完整的 Amazon 产品数据提取和电商智能分析服务',
    content
)

content = content.replace('API\n                            Docs', 'API\n                            文档')
content = content.replace('Learn\n                            More', '了解\n                            更多')

# 产品卡片
content = content.replace('Amazon Product Data', 'Amazon 产品数据')
content = re.sub(
    r'Extract product details, prices, variants, images,\s*reviews, and ratings from Amazon marketplace',
    '从 Amazon 市场提取产品详情、价格、变体、图片、评论和评分',
    content
)

content = content.replace('Amazon Search Results', 'Amazon 搜索结果')
content = re.sub(
    r'Collect organic rankings, sponsored ads, and Amazon\s*SERP metadata',
    '收集自然排名、赞助广告和 Amazon SERP 元数据',
    content
)

content = content.replace('Amazon Review Data', 'Amazon 评论数据')
content = re.sub(
    r'Gather customer reviews, ratings, sentiment\s*analysis, and product feedback',
    '收集客户评论、评分、情感分析和产品反馈',
    content
)

# AMZ Data Tracker
content = re.sub(
    r'Real-time Amazon product tracking, price monitoring, and\s*sales analytics with automated reporting\.',
    '实时 Amazon 产品跟踪、价格监控和销售分析，支持自动化报告。',
    content
)
content = content.replace('Zero-code Amazon\n                            tracking', '零代码 Amazon\n                            跟踪')
content = content.replace('Automated price\n                            alerts', '自动价格\n                            提醒')
content = content.replace('Excel export\n                            ready', 'Excel 导出\n                            就绪')

# Amazon SERP API
content = re.sub(
    r'Amazon search results, keyword rankings, and sponsored\s*product placement data\.',
    'Amazon 搜索结果、关键词排名和赞助产品投放数据。',
    content
)
content = content.replace('Amazon organic\n                            rankings', 'Amazon 自然\n                            排名')
content = content.replace('Sponsored ads\n                            tracking', '赞助广告\n                            跟踪')
content = content.replace('Multi-marketplace\n                            support', '多市场\n                            支持')

# Amazon Data Solutions
content = content.replace('Amazon Data Solutions', 'Amazon 数据解决方案')
content = re.sub(
    r'AI-powered Amazon data intelligence for product selection\s*and market analysis\.',
    'AI 驱动的 Amazon 数据智能，用于产品选择和市场分析。',
    content
)
content = content.replace('AI-driven\n                            insights', 'AI 驱动\n                            洞察')
content = content.replace('Competitive\n                            analysis', '竞争\n                            分析')
content = content.replace('Market trends', '市场趋势')

# ============ 第八步：Use Cases ============
content = content.replace('Use Cases', '应用场景')
content = content.replace('Real-World Applications', '实际应用案例')
content = re.sub(
    r'See how businesses leverage Pangol Info\'s Amazon API for data-driven growth',
    '了解企业如何利用 Pangol Info 的 Amazon API 实现数据驱动的增长',
    content
)

content = re.sub(
    r'From Amazon product selection to competitive pricing, our APIs cover the entire\s*e-commerce lifecycle',
    '从 Amazon 产品选择到竞争定价，我们的 API 覆盖整个电商生命周期',
    content
)

# Use Case 卡片
content = content.replace('Amazon Product Selection', 'Amazon 产品选择')
content = content.replace('Comprehensive Amazon product data for informed selection decisions', 
                         '全面的 Amazon 产品数据，助力明智的选择决策')
content = content.replace('Full Amazon\n                            catalog', '完整 Amazon\n                            目录')
content = content.replace('Category\n                            deep-dive', '类别\n                            深度分析')
content = content.replace('Real-time product\n                            data', '实时产品\n                            数据')

content = content.replace('Amazon Ad Monitoring', 'Amazon 广告监控')
content = content.replace('Track Amazon sponsored products and advertising strategies',
                         '跟踪 Amazon 赞助产品和广告策略')
content = content.replace('Keyword ad\n                            tracking', '关键词广告\n                            跟踪')
content = content.replace('Sponsored\n                            placement', '赞助\n                            投放')
content = content.replace('Competitor ads', '竞争对手广告')

content = content.replace('Price Optimization', '价格优化')
content = content.replace('Track Amazon and e-commerce pricing for competitive advantage',
                         '跟踪 Amazon 和电商定价，获得竞争优势')
content = content.replace('Real-time price\n                            tracking', '实时价格\n                            跟踪')
content = content.replace('Price change\n                            alerts', '价格变动\n                            提醒')
content = content.replace('Historical\n                            pricing', '历史\n                            定价')

content = content.replace('Amazon Bestseller Tracking', 'Amazon 畅销榜跟踪')
content = content.replace('Monitor Amazon bestseller lists and category rankings',
                         '监控 Amazon 畅销榜和类别排名')
content = content.replace('Bestseller\n                            rankings', '畅销榜\n                            排名')
content = content.replace('Category trends', '类别趋势')
content = content.replace('New release\n                            tracking', '新品\n                            跟踪')

# ============ 第九步：Success Stories ============
content = content.replace('E-commerce Success', '电商成功案例')
content = content.replace('How businesses leverage Pangol Info\'s Amazon API for data-driven growth',
                         '企业如何利用 Pangol Info 的 Amazon API 实现数据驱动的增长')

content = content.replace('Amazon Product Intelligence', 'Amazon 产品智能')
content = re.sub(
    r'Powered 30K SKU Amazon product selection\s*with 99%\+ API success rate',
    '支持 30K SKU Amazon 产品选择，API 成功率超过 99%',
    content
)
content = content.replace('99%+ Amazon API Success', 'Amazon API 成功率超过 99%')

content = content.replace('Multi-Category E-commerce', '多类别电商')
content = re.sub(
    r'Enabled multi-category expansion with Amazon\s*data extraction',
    '通过 Amazon 数据提取实现多类别扩展',
    content
)
content = content.replace('Multi-Category Coverage', '多类别覆盖')

content = content.replace('Amazon Ad Intelligence', 'Amazon 广告智能')
content = re.sub(
    r'Built hourly Amazon sponsored product\s*monitoring system',
    '构建每小时 Amazon 赞助产品监控系统',
    content
)
content = content.replace('Hourly Amazon Tracking', '每小时 Amazon 跟踪')

content = content.replace('Amazon Keyword Platform', 'Amazon 关键词平台')
content = re.sub(
    r'High-precision Amazon SERP API supporting\s*million-scale traffic analysis',
    '高精度 Amazon SERP API，支持百万级流量分析',
    content
)
content = content.replace('Million-Scale Amazon Data', '百万级 Amazon 数据')

# ============ 第十步：APIs Section ============
content = content.replace('API Documentation', 'API 文档')
content = content.replace('Comprehensive guides for Amazon scraping API and e-commerce data extraction',
                         'Amazon 数据抓取 API 和电商数据提取的综合指南')

content = content.replace('Complete Amazon product data extraction', '完整的 Amazon 产品数据提取')
content = content.replace('Multi-platform e-commerce data', '多平台电商数据')
content = content.replace('Amazon search results data', 'Amazon 搜索结果数据')
content = content.replace('Amazon search trends analysis', 'Amazon 搜索趋势分析')
content = content.replace('Geo-targeted e-commerce data', '地理定向电商数据')
content = content.replace('Intellectual property data', '知识产权数据')

# ============ 第十一步：Latest Articles ============
content = content.replace('Latest Articles', '最新文章')
content = content.replace('Expert Insights & Tutorials', '专家洞察与教程')
content = content.replace('Learn from our comprehensive guides on Amazon API integration and data extraction',
                         '从我们关于 Amazon API 集成和数据提取的综合指南中学习')
content = content.replace('View All Articles', '查看所有文章')

# 文章数据
content = content.replace('"Getting Started with Amazon Scraping API"', '"Amazon 数据抓取 API 入门指南"')
content = content.replace('"Learn how to leverage Pangol Info\'s Amazon scraping API to extract comprehensive product data, pricing, and reviews from Amazon marketplace."',
                         '"学习如何利用 Pangol Info 的 Amazon 数据抓取 API 从 Amazon 市场提取全面的产品数据、价格和评论信息。"')

content = content.replace('"Advanced Amazon Data Extraction Best Practices"', '"Amazon 数据提取高级最佳实践"')
content = content.replace('"Master advanced techniques for efficient data extraction, rate limiting, and error handling when working with Amazon APIs."',
                         '"掌握使用 Amazon API 时的高效数据提取、速率限制和错误处理的高级技术。"')

content = content.replace('"Amazon Product Selection: Using API Data to Find Winning Products"', '"使用 API 数据选择优质 Amazon 产品"')
content = content.replace('"Discover how to use API data to identify profitable products, analyze market trends, and make data-driven product selection decisions."',
                         '"了解如何使用 API 数据识别盈利产品、分析市场趋势并做出数据驱动的产品选择决策。"')

content = content.replace('"Amazon Sponsored Products: Monitor Competitor Ad Campaigns"', '"监控 Amazon 竞争对手广告活动"')
content = content.replace('"Track competitor advertising strategies, sponsored product placements, and optimize your own PPC campaigns with real-time data."',
                         '"跟踪竞争对手的广告策略、赞助产品投放，并使用实时数据优化您自己的 PPC 广告活动。"')

content = content.replace('"Building Real-Time Amazon Price Monitoring System"', '"构建实时 Amazon 价格监控系统"')
content = content.replace('"Step-by-step guide to creating an automated Amazon price tracking system using Pangol Info\'s e-commerce API."',
                         '"使用 Pangol Info 的电商 API 创建自动化 Amazon 价格跟踪系统的分步指南。"')

content = content.replace('"Scale Your Amazon Business with Data-Driven Product Intelligence"', '"通过数据驱动的产品智能扩展 Amazon 业务"')
content = content.replace('"How businesses leverage Pangol Info\'s Amazon API for data-driven growth"',
                         '"企业如何利用 Pangol Info 的 Amazon API 实现数据驱动的增长"')

# ============ 第十二步：CTA ============
content = content.replace('Ready to Get Started?', '准备开始了吗？')
content = content.replace('Ready to Scale Your Amazon Data Extraction?', '准备扩展您的 Amazon 数据提取了吗？')
content = re.sub(
    r'Get started with 1,000 free Amazon API credits\. No credit\s*card required\. Start extracting Amazon product data in minutes\.',
    '获取 1,000 个免费 Amazon API 积分。无需信用卡。几分钟内开始提取 Amazon 产品数据。',
    content
)
content = content.replace('View Documentation', '查看文档')
content = content.replace('View API Docs', '查看 API 文档')

# ============ 第十三步：Newsletter ============
content = content.replace('Stay Updated', '保持更新')
content = content.replace('Subscribe to our newsletter for the latest Amazon API insights and tutorials',
                         '订阅我们的新闻通讯，获取最新的 Amazon API 洞察和教程')
content = content.replace('Enter your email', '输入您的邮箱')
content = content.replace('Subscribe', '订阅')

# ============ 第十四步：Footer ============
content = content.replace('Quick Links', '快速链接')
content = content.replace('Products', '产品')
content = content.replace('Resources', '资源')
content = content.replace('Company', '公司')
content = content.replace('Documentation', '文档')
content = content.replace('API Reference', 'API 参考')
content = content.replace('Tutorials', '教程')
content = content.replace('Case Studies', '案例研究')
content = content.replace('Legal', '法律')
content = content.replace('Privacy Policy', '隐私政策')
content = content.replace('Terms of Service', '服务条款')
content = content.replace('Official Website', '官方网站')
content = content.replace('Console', '控制台')
content = content.replace('Amazon Solutions', 'Amazon 解决方案')
content = content.replace('Blog Articles', '博客文章')

content = re.sub(
    r'Professional Amazon scraping API and e-commerce data extraction\s*solutions for businesses worldwide\.',
    '为全球企业提供专业的 Amazon 数据抓取 API 和电商数据提取解决方案。',
    content
)

content = content.replace('© 2025 Pangol Info Scrape API. All rights reserved.',
                         '© 2025 Pangol Info Scrape API. 保留所有权利。')

# ============ 第十五步：其他常见词汇 ============
content = content.replace(' min read', ' 分钟阅读')
content = content.replace('Read More', '阅读更多')
content = content.replace('Read Article', '阅读文章')

# 保存
with open('zh/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 完整的中文HTML生成完成！")
print(f"📄 输出文件: zh/index.html")
print(f"文件大小: {len(content)} 字符")
print("\n🎯 翻译完成的部分:")
print("  ✅ SEO Meta Tags")
print("  ✅ 导航栏")
print("  ✅ Hero Section")
print("  ✅ Stats")
print("  ✅ Solutions")
print("  ✅ Use Cases")
print("  ✅ Success Stories")
print("  ✅ APIs Section")
print("  ✅ Latest Articles")
print("  ✅ CTA")
print("  ✅ Newsletter")
print("  ✅ Footer")
print("  ✅ 语言切换按钮（已修复）")
