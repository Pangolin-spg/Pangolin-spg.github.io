#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整重新生成中文博客汇总页
读取英文blog.html，翻译所有可见文本，保留品牌/产品名称
"""

import re

# 读取英文blog.html作为基础
with open('blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("📖 正在读取英文博客汇总页...")
print(f"文件大小: {len(content)} 字符")

# ============ 第一步：基础设置 ============
# 修改 lang 属性
content = content.replace('<html lang="en">', '<html lang="zh-CN">')

# ============ 第二步：SEO Meta Tags ============
content = content.replace(
    '<title>Amazon API Blog Archive | E-commerce Data Extraction Articles</title>',
    '<title>Amazon API 博客归档 | 电商数据提取文章</title>'
)

content = content.replace(
    'Browse expert articles on Amazon scraping API, e-commerce data extraction, product intelligence, and API integration. Real-world case studies and technical tutorials.',
    '浏览关于 Amazon 数据抓取 API、电商数据提取、产品智能和 API 集成的专家文章。真实案例研究和技术教程。'
)

content = content.replace(
    'Amazon API Blog, E-commerce Data Extraction, Amazon API Tutorials, Product Intelligence, Web Scraping Guide',
    'Amazon API 博客, 电商数据提取, Amazon API 教程, 产品智能, 网页抓取指南'
)

# Open Graph
content = content.replace(
    'Amazon API Blog Archive | Expert Tutorials & Case Studies',
    'Amazon API 博客归档 | 专家教程与案例研究'
)

content = content.replace(
    'Comprehensive Amazon API tutorials, e-commerce data extraction guides, and real-world case studies.',
    '全面的 Amazon API 教程、电商数据提取指南和真实案例研究。'
)

# Schema.org
content = content.replace(
    '"name": "Pangol Info Scrape API Blog Archive"',
    '"name": "Pangol Info 数据抓取 API 博客归档"'
)

content = content.replace(
    '"description": "Expert Amazon API tutorials and e-commerce data extraction guides"',
    '"description": "专业的 Amazon API 教程和电商数据提取指南"'
)

# ============ 第三步：添加 Hreflang ============
if 'Hreflang Tags' not in content:
    hreflang = '''    <!-- Hreflang Tags -->
    <link rel="alternate" hreflang="en" href="https://blog.pangolinfo.com/blog.html">
    <link rel="alternate" hreflang="zh-CN" href="https://blog.pangolinfo.com/zh/blog.html">
    <link rel="alternate" hreflang="x-default" href="https://blog.pangolinfo.com/blog.html">

'''
    content = content.replace('</head>', hreflang + '</head>')

# ============ 第四步：导航栏 ============
# 更新导航链接指向中文版本
content = content.replace('href="index.html#home"', 'href="/zh/index.html#home"')
content = content.replace('href="index.html#solutions"', 'href="/zh/index.html#solutions"')
content = content.replace('href="index.html#use-cases"', 'href="/zh/index.html#use-cases"')
content = content.replace('href="blog.html"', 'href="/zh/blog.html"')

# 导航文本
content = content.replace('>Home<', '>首页<')
content = content.replace('>Solutions<', '>解决方案<')
content = content.replace('>Use Cases<', '>应用场景<')
content = content.replace('>Blog<', '>博客<')
content = content.replace('>Docs<', '>文档<')
content = content.replace('>Pricing<', '>定价<')
content = content.replace('>Get API Key<', '>获取 API Key<')

# 语言切换器 - 中文页面显示 English
content = re.sub(
    r'<a href="/zh/blog\.html" class="language-btn">\s*<span>🇨🇳</span>\s*<span>中文</span>',
    '<a href="/blog.html" class="language-btn">\n                        <span>🇺🇸</span>\n                        <span>English</span>',
    content
)

# ============ 第五步：Hero Section ============
content = content.replace('Amazon API', 'Amazon API')
content = content.replace('Blog Archive', '博客归档')

content = content.replace(
    'Expert insights, tutorials, and case studies on Amazon data extraction and e-commerce intelligence',
    '关于 Amazon 数据提取和电商智能的专家洞察、教程和案例研究'
)

# ============ 第六步：Search and Filter ============
content = content.replace('Search articles...', '搜索文章...')
content = content.replace('All Articles', '全部文章')
content = content.replace('Tutorials', '教程')
content = content.replace('Case Studies', '案例研究')

# ============ 第七步：Stats Section ============
content = content.replace('Published Articles', '已发布文章')
content = content.replace('Categories', '分类')
content = content.replace('Monthly Readers', '月度读者')
content = content.replace('New Content', '新内容')
content = content.replace('Weekly', '每周')

# ============ 第八步：No Results Message ============
content = content.replace('No articles found', '未找到文章')
content = content.replace(
    'Try adjusting your search or filter to find what you\'re looking for.',
    '尝试调整您的搜索或筛选条件以找到您要查找的内容。'
)

# ============ 第九步：Newsletter Section ============
content = content.replace('Stay Updated with Latest Insights', '获取最新洞察')
content = content.replace(
    'Subscribe to our newsletter for expert tips, tutorials, and Amazon API updates',
    '订阅我们的新闻通讯，获取专家提示、教程和 Amazon API 更新'
)
content = content.replace('Enter your email', '输入您的邮箱')
content = content.replace('Subscribe', '订阅')

# ============ 第十步：CTA Section ============
content = content.replace('Ready to Get Started?', '准备开始了吗？')
content = content.replace(
    'Join thousands of businesses using Pangol Info API for Amazon data extraction',
    '加入数千家使用 Pangol Info API 进行 Amazon 数据提取的企业'
)
content = content.replace('Start Free Trial', '开始免费试用')
content = content.replace('View Documentation', '查看文档')

# ============ 第十一步：Footer ============
content = content.replace('Quick Links', '快速链接')
content = content.replace('Products', '产品')
content = content.replace('Resources', '资源')
content = content.replace('Company', '公司')
content = content.replace('Documentation', '文档')
content = content.replace('API Reference', 'API 参考')
content = content.replace('Legal', '法律')
content = content.replace('Privacy Policy', '隐私政策')
content = content.replace('Terms of Service', '服务条款')
content = content.replace('Official Website', '官方网站')
content = content.replace('Console', '控制台')
content = content.replace('Amazon Solutions', 'Amazon 解决方案')
content = content.replace('Blog Articles', '博客文章')

content = content.replace(
    'Professional Amazon scraping API and e-commerce data extraction solutions for businesses worldwide.',
    '为全球企业提供专业的 Amazon 数据抓取 API 和电商数据提取解决方案。'
)

content = content.replace(
    '© 2025 Pangol Info Scrape API. All rights reserved.',
    '© 2025 Pangol Info Scrape API. 保留所有权利。'
)

# ============ 第十二步：文章数据翻译 ============
# 文章标题和摘要
article_translations = {
    '"Getting Started with Amazon Scraping API"': '"Amazon 数据抓取 API 入门指南"',
    '"Learn how to leverage Pangol Info\'s Amazon scraping API to extract comprehensive product data, pricing, and reviews from Amazon marketplace."':
    '"学习如何利用 Pangol Info 的 Amazon 数据抓取 API 从 Amazon 市场提取全面的产品数据、价格和评论信息。"',
    
    '"Advanced Amazon Data Extraction Best Practices"': '"Amazon 数据提取高级最佳实践"',
    '"Master advanced techniques for efficient data extraction, rate limiting, and error handling when working with Amazon APIs."':
    '"掌握使用 Amazon API 时的高效数据提取、速率限制和错误处理的高级技术。"',
    
    '"Amazon Product Selection: Using API Data to Find Winning Products"': '"使用 API 数据选择优质 Amazon 产品"',
    '"Discover how to use API data to identify profitable products, analyze market trends, and make data-driven product selection decisions."':
    '"了解如何使用 API 数据识别盈利产品、分析市场趋势并做出数据驱动的产品选择决策。"',
    
    '"Amazon Sponsored Products: Monitor Competitor Ad Campaigns"': '"监控 Amazon 竞争对手广告活动"',
    '"Track competitor advertising strategies, sponsored product placements, and optimize your own PPC campaigns with real-time data."':
    '"跟踪竞争对手的广告策略、赞助产品投放，并使用实时数据优化您自己的 PPC 广告活动。"',
    
    '"Building Real-Time Amazon Price Monitoring System"': '"构建实时 Amazon 价格监控系统"',
    '"Step-by-step guide to creating an automated Amazon price tracking system using Pangol Info\'s e-commerce API."':
    '"使用 Pangol Info 的电商 API 创建自动化 Amazon 价格跟踪系统的分步指南。"',
    
    '"Scale Your Amazon Business with Data-Driven Product Intelligence"': '"通过数据驱动的产品智能扩展 Amazon 业务"',
    '"Real-world case studies showing how businesses achieve 10x growth using data-driven strategies and Amazon API integration."':
    '"真实案例研究展示企业如何使用数据驱动策略和 Amazon API 集成实现 10 倍增长。"',
    
    # 分类
    '"API Tutorial"': '"API 教程"',
    '"Best Practices"': '"最佳实践"',
    '"Product Selection"': '"产品选择"',
    '"Amazon Ads"': '"Amazon 广告"',
    '"Price Tracking"': '"价格跟踪"',
    '"Case Study"': '"案例研究"',
}

for en, zh in article_translations.items():
    content = content.replace(en, zh)

# ============ 第十三步：其他常见词汇 ============
content = content.replace(' min read', ' 分钟阅读')
content = content.replace('Read Article', '阅读文章')
content = content.replace('Read More', '阅读更多')

# 保存
with open('zh/blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 完整的中文博客汇总页生成完成！")
print(f"📄 输出文件: zh/blog.html")
print(f"文件大小: {len(content)} 字符")
print("\n🎯 翻译完成的部分:")
print("  ✅ SEO Meta Tags")
print("  ✅ 导航栏（链接已更新指向中文版）")
print("  ✅ Hero Section")
print("  ✅ 搜索和筛选")
print("  ✅ 统计数据")
print("  ✅ 文章数据（6篇）")
print("  ✅ Newsletter")
print("  ✅ CTA")
print("  ✅ Footer")
print("  ✅ 语言切换按钮（显示 English）")
