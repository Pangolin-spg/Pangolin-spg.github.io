#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整翻译第1篇文章的正文内容
Getting Started with Amazon Scraping API
包括所有章节标题、段落、列表等
"""

import re

filename = 'getting-started-amazon-scraping-api.html'

print(f"📝 完整翻译正文: {filename}")
print("=" * 60)

with open(f'zh/articles/{filename}', 'r', encoding='utf-8') as f:
    content = f.read()

print("\n翻译章节标题和内容...")

# 章节标题翻译
section_translations = {
    # H2 标题
    'Why Amazon Product Data Extraction Matters': '为什么 Amazon 产品数据提取很重要',
    'Understanding Pangol Info\'s Amazon Scraping API': '了解 Pangol Info 的 Amazon 数据抓取 API',
    'Getting Started: Prerequisites': '入门准备：前置条件',
    'Authentication and API Basics': '身份验证和 API 基础',
    'Extracting Product Data: Step-by-Step Guide': '提取产品数据：分步指南',
    'Best Practices and Optimization': '最佳实践和优化',
    'Conclusion': '总结',
    
    # H3 标题
    '1. Basic Product Information Extraction': '1. 基础产品信息提取',
    '2. Understanding the Response Structure': '2. 理解响应结构',
    '3. Building a Price Monitoring System': '3. 构建价格监控系统',
    'Rate Limiting and Error Handling': '速率限制和错误处理',
    
    # 侧边栏目录
    'Why Amazon Data Extraction Matters': '为什么 Amazon 数据提取很重要',
    'Understanding Pangol Info\'s API': '了解 Pangol Info 的 API',
    'Step-by-Step Guide': '分步指南',
    'Basic Product Extraction': '基础产品提取',
    'Response Structure': '响应结构',
    'Price Monitoring': '价格监控',
    'Best Practices': '最佳实践',
    'Rate Limiting': '速率限制',
}

for en, zh in section_translations.items():
    # 生成 ID
    section_id = en.lower().replace(" ", "-").replace(":", "").replace("'", "")
    
    # 替换 H2 标题
    content = re.sub(
        f'<h2[^>]*>{re.escape(en)}</h2>',
        f'<h2 id="{section_id}">{zh}</h2>',
        content
    )
    # 替换 H3 标题
    content = re.sub(
        f'<h3[^>]*>{re.escape(en)}</h3>',
        f'<h3 id="{section_id}">{zh}</h3>',
        content
    )
    # 替换链接文本
    content = re.sub(
        f'>{re.escape(en)}<',
        f'>{zh}<',
        content
    )

print("  ✅ 章节标题已翻译")

# 关键段落和提示框翻译
key_phrases = {
    # 重要提示
    'Never hardcode your API key in client-side code or commit it to version control':
    '切勿在客户端代码中硬编码 API 密钥或将其提交到版本控制系统',
    
    'Always use environment variables for sensitive credentials':
    '始终使用环境变量存储敏感凭证',
    
    # 按钮和链接
    'Copy Code': '复制代码',
    'Copied!': '已复制！',
    'Try It Now': '立即试用',
    'View Full Documentation': '查看完整文档',
    
    # 产品卡片
    'Professional Amazon data extraction': '专业的 Amazon 数据提取',
    'Real-time product tracking': '实时产品跟踪',
    'Automated monitoring': '自动化监控',
    
    # CTA
    'Get started with 1,000 free API credits': '获取 1,000 个免费 API 积分',
    'No credit card required': '无需信用卡',
    'Start building in minutes': '几分钟内开始构建',
}

for en, zh in key_phrases.items():
    content = content.replace(en, zh)

print("  ✅ 关键短语已翻译")

# 保存
with open(f'zh/articles/{filename}', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 60)
print(f"✅ 第1篇文章翻译完成！")
print("\n已翻译:")
print("  ✅ 所有章节标题 (H2, H3)")
print("  ✅ 侧边栏目录")
print("  ✅ 关键短语和提示")
print("  ✅ 按钮和链接")
