#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整翻译文章 - 包括添加语言切换按钮和翻译正文内容
先处理第一篇文章作为示例
"""

import re

filename = 'getting-started-amazon-scraping-api.html'

print(f"📝 正在完整翻译: {filename}")
print("=" * 60)

# 读取中文版本（已有基础翻译）
with open(f'zh/articles/{filename}', 'r', encoding='utf-8') as f:
    content = f.read()

print("步骤 1: 添加语言切换按钮样式...")

# 添加语言切换器样式（如果还没有）
if 'language-switcher' not in content:
    language_styles = '''
        /* Language Switcher */
        .language-switcher {
            display: inline-block;
        }

        .language-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            color: #fff;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .language-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(56, 189, 248, 0.5);
            transform: translateY(-1px);
        }
'''
    content = content.replace('</style>', language_styles + '    </style>')
    print("  ✅ 已添加语言切换器样式")

print("步骤 2: 在导航栏添加语言切换按钮...")

# 在导航栏中添加语言切换按钮
# 找到 "Get API Key" 按钮之前的位置
nav_button_pattern = r'(<a href="https://tool\.pangolinfo\.com/"[^>]*>\s*获取 API Key\s*</a>)'

language_switcher_html = '''            <div class="flex items-center gap-4">
                <!-- Language Switcher -->
                <div class="language-switcher">
                    <a href="/articles/''' + filename + '''" class="language-btn">
                        <span>🇺🇸</span>
                        <span>English</span>
                    </a>
                </div>
                <!-- Get API Key Button -->
                \\1
            </div>'''

# 替换导航栏按钮部分
content = re.sub(
    nav_button_pattern,
    language_switcher_html,
    content
)
print("  ✅ 已添加语言切换按钮到导航栏")

print("步骤 3: 翻译文章标题和元数据...")

# SEO 标题
content = content.replace(
    '<title>Getting Started with Amazon Scraping API for Product Data Extraction | Pangolin Blog</title>',
    '<title>Amazon 数据抓取 API 产品数据提取入门指南 | Pangolin 博客</title>'
)

# Meta 描述
content = re.sub(
    r'<meta name="description"\s+content="[^"]*"',
    '<meta name="description" content="学习如何使用 Pangol Info 的 Amazon 数据抓取 API 提取产品数据、价格和评论。完整的入门指南，包含代码示例和最佳实践。"',
    content
)

# Meta 关键词
content = re.sub(
    r'<meta name="keywords"\s+content="[^"]*"',
    '<meta name="keywords" content="Amazon API, 数据抓取, 产品数据提取, Amazon 爬虫, 电商数据, API 教程"',
    content
)

print("  ✅ 已翻译 SEO 元数据")

print("步骤 4: 翻译文章主标题...")

# H1 标题
content = re.sub(
    r'<h1[^>]*>Getting Started with Amazon Scraping API for Product Data Extraction</h1>',
    '<h1 class="text-4xl md:text-5xl font-black mb-6 leading-tight">Amazon 数据抓取 API 产品数据提取入门指南</h1>',
    content
)

print("  ✅ 已翻译主标题")

print("步骤 5: 翻译文章摘要...")

# 文章摘要/描述
content = re.sub(
    r'<p class="text-xl text-gray-400 mb-8 leading-relaxed">.*?</p>',
    '<p class="text-xl text-gray-400 mb-8 leading-relaxed">学习如何使用 Pangol Info 的 Amazon 数据抓取 API 从 Amazon 市场提取全面的产品数据、价格和评论信息。本指南将带您了解从身份验证到高级数据提取的完整流程。</p>',
    content,
    count=1,
    flags=re.DOTALL
)

print("  ✅ 已翻译文章摘要")

print("步骤 6: 翻译侧边栏目录...")

# 侧边栏标题
content = content.replace('Table of Contents', '目录')
content = content.replace('On This Page', '本页内容')

# 目录项（示例 - 需要根据实际内容调整）
toc_translations = {
    'Why Amazon Data Extraction Matters': '为什么 Amazon 数据提取很重要',
    'Understanding Pangol Info\'s API': '了解 Pangol Info 的 API',
    'Getting Started: Prerequisites': '入门准备：前置条件',
    'Authentication and API Basics': '身份验证和 API 基础',
    'Step-by-Step Guide': '分步指南',
    'Basic Product Extraction': '基础产品数据提取',
    'Advanced Features': '高级功能',
    'Best Practices': '最佳实践',
    'Error Handling': '错误处理',
    'Rate Limiting': '速率限制',
    'Next Steps': '下一步',
}

for en, zh in toc_translations.items():
    content = content.replace(f'>{en}<', f'>{zh}<')

print("  ✅ 已翻译侧边栏目录")

# 保存
with open(f'zh/articles/{filename}', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 60)
print(f"✅ 完成！已保存到: zh/articles/{filename}")
print("\n⚠️  注意:")
print("  - 已添加语言切换按钮")
print("  - 已翻译 SEO 元数据")
print("  - 已翻译标题和摘要")
print("  - 已翻译侧边栏目录")
print("\n📝 正文段落需要逐段翻译，建议使用专业翻译工具")
print("   或者告诉我需要翻译哪些具体部分")
