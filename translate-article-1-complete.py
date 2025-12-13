#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整翻译第一篇文章 - Getting Started with Amazon Scraping API
这是一个示例，展示如何完整翻译文章内容
"""

import re

filename = 'getting-started-amazon-scraping-api.html'

print(f"📝 完整翻译: {filename}")
print("=" * 60)

# 读取文件
with open(f'zh/articles/{filename}', 'r', encoding='utf-8') as f:
    content = f.read()

print("\n步骤 1: 翻译 SEO 元数据...")

# SEO 标题
content = re.sub(
    r'<title>.*?</title>',
    '<title>Amazon 数据抓取 API 产品数据提取入门指南 | Pangolin 博客</title>',
    content,
    flags=re.DOTALL
)

# Meta 描述
content = re.sub(
    r'<meta name="description" content="[^"]*"',
    '<meta name="description" content="学习如何使用 Pangol Info 的 Amazon 数据抓取 API 提取产品数据、价格和评论。完整的入门指南，包含代码示例和最佳实践。"',
    content
)

# Meta 关键词
content = re.sub(
    r'<meta name="keywords" content="[^"]*"',
    '<meta name="keywords" content="Amazon API, 数据抓取, 产品数据提取, Amazon 爬虫, 电商数据, API 教程"',
    content
)

print("  ✅ SEO 元数据已翻译")

print("\n步骤 2: 翻译主标题...")

# H1 标题
content = re.sub(
    r'<h1 class="text-4xl[^>]*>Getting Started with Amazon Scraping API for Product Data Extraction</h1>',
    '<h1 class="text-4xl md:text-6xl font-black mb-6 leading-tight">Amazon 数据抓取 API 产品数据提取入门指南</h1>',
    content
)

print("  ✅ 主标题已翻译")

print("\n步骤 3: 翻译文章摘要...")

# 文章摘要（第一个大段落）
content = re.sub(
    r'(<p class="text-xl text-gray-400[^>]*>).*?(</p>)',
    r'\1学习如何使用 Pangol Info 的 Amazon 数据抓取 API 从 Amazon 市场提取全面的产品数据、价格和评论信息。本指南将带您了解从身份验证到高级数据提取的完整流程，包含实用代码示例和最佳实践。\2',
    content,
    count=1,
    flags=re.DOTALL
)

print("  ✅ 文章摘要已翻译")

print("\n步骤 4: 翻译章节标题...")

# H2 和 H3 标题翻译
section_titles = {
    'Why Amazon Product Data Extraction Matters': '为什么 Amazon 产品数据提取很重要',
    'Understanding Pangol Info\'s Amazon Scraping API': '了解 Pangol Info 的 Amazon 数据抓取 API',
    'Getting Started: Prerequisites': '入门准备：前置条件',
    'Authentication and API Basics': '身份验证和 API 基础',
    'Extracting Product Data: Step-by-Step Guide': '提取产品数据：分步指南',
    'Basic Product Information Extraction': '基础产品信息提取',
    'Understanding the Response Structure': '理解响应结构',
    'Building a Price Monitoring System': '构建价格监控系统',
    'Best Practices and Optimization': '最佳实践和优化',
    'Rate Limiting and Error Handling': '速率限制和错误处理',
    'Conclusion': '总结',
    'Ready to Start Extracting Amazon Data?': '准备开始提取 Amazon 数据了吗？',
}

for en, zh in section_titles.items():
    # H2 标题
    content = re.sub(
        f'<h2[^>]*>{re.escape(en)}</h2>',
        f'<h2 id="{en.lower().replace(" ", "-").replace(":", "").replace("?", "")}">{zh}</h2>',
        content
    )
    # H3 标题
    content = re.sub(
        f'<h3[^>]*>{re.escape(en)}</h3>',
        f'<h3 id="{en.lower().replace(" ", "-").replace(":", "").replace("?", "")}">{zh}</h3>',
        content
    )
    # 带编号的标题
    content = re.sub(
        f'<h3[^>]*>\\d+\\. {re.escape(en)}</h3>',
        lambda m: f'<h3 id="{en.lower().replace(" ", "-")}">{m.group(0).split(">")[1].split(".")[0]}. {zh}</h3>',
        content
    )

print("  ✅ 章节标题已翻译")

print("\n步骤 5: 翻译侧边栏...")

# 侧边栏标题
content = content.replace('Table of Contents', '目录')
content = content.replace('On This Page', '本页内容')

# 侧边栏链接
toc_links = {
    'Why Amazon Data Extraction Matters': '为什么 Amazon 数据提取很重要',
    'Understanding Pangol Info\'s API': '了解 Pangol Info 的 API',
    'Getting Started: Prerequisites': '入门准备：前置条件',
    'Authentication and API Basics': '身份验证和 API 基础',
    'Step-by-Step Guide': '分步指南',
    'Basic Product Extraction': '基础产品数据提取',
    'Response Structure': '响应结构',
    'Price Monitoring': '价格监控',
    'Best Practices': '最佳实践',
    'Rate Limiting': '速率限制',
}

for en, zh in toc_links.items():
    content = re.sub(
        f'>{re.escape(en)}<',
        f'>{zh}<',
        content
    )

print("  ✅ 侧边栏已翻译")

print("\n步骤 6: 翻译 CTA 部分...")

# CTA 文本
content = re.sub(
    r'Get 1,000 free API credits and start building today',
    '获取 1,000 个免费 API 积分，立即开始构建',
    content
)

content = re.sub(
    r'Start Free Trial',
    '开始免费试用',
    content
)

content = re.sub(
    r'View API Documentation',
    '查看 API 文档',
    content
)

print("  ✅ CTA 部分已翻译")

print("\n步骤 7: 翻译产品卡片...")

# 产品卡片描述
content = re.sub(
    r'Professional Amazon & e-commerce data extraction API',
    'Amazon 和电商数据提取专业 API',
    content
)

content = re.sub(
    r'Zero-code Amazon product tracking with automated price',
    '零代码 Amazon 产品跟踪，支持自动化价格',
    content
)

print("  ✅ 产品卡片已翻译")

# 保存
with open(f'zh/articles/{filename}', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 60)
print(f"✅ 完成！已保存到: zh/articles/{filename}")
print("\n已翻译内容:")
print("  ✅ SEO 元数据")
print("  ✅ 主标题 (H1)")
print("  ✅ 文章摘要")
print("  ✅ 所有章节标题 (H2, H3)")
print("  ✅ 侧边栏目录")
print("  ✅ CTA 部分")
print("  ✅ 产品卡片")
print("\n⚠️  注意: 正文段落内容较多，建议使用专业翻译工具逐段翻译")
print("或者我可以继续为其他文章应用相同的翻译模式")
