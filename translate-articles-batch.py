#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成6篇文章的中文版本
读取英文文章HTML，翻译所有可见文本，保留品牌/产品名称
"""

import os
import re

# 文章列表
articles = [
    'getting-started-amazon-scraping-api.html',
    'advanced-amazon-data-extraction-best-practices.html',
    'amazon-product-selection-api-data.html',
    'amazon-sponsored-products-ad-monitoring.html',
    'amazon-price-monitoring-system.html',
    'amazon-business-case-studies.html'
]

# 确保中文文章目录存在
os.makedirs('zh/articles', exist_ok=True)

print("🚀 开始批量翻译文章...")
print(f"总共 {len(articles)} 篇文章\n")

# 通用翻译映射（适用于所有文章）
common_translations = {
    # 基础设置
    '<html lang="en">': '<html lang="zh-CN">',
    
    # 导航栏
    '>Home<': '>首页<',
    '>Solutions<': '>解决方案<',
    '>Use Cases<': '>应用场景<',
    '>Blog<': '>博客<',
    '>Docs<': '>文档<',
    '>Pricing<': '>定价<',
    '>Get API Key<': '>获取 API Key<',
    
    # 语言切换器 - 文章页面应该显示 English
    'href="/zh/': 'href="/',  # 先改回英文链接
    
    # 侧边栏
    'Table of Contents': '目录',
    'Related Articles': '相关文章',
    'Quick Navigation': '快速导航',
    'On This Page': '本页内容',
    
    # 阅读时间
    ' min read': ' 分钟阅读',
    'minute read': '分钟阅读',
    
    # 按钮和链接
    'Read More': '阅读更多',
    'Read Article': '阅读文章',
    'View Documentation': '查看文档',
    'Start Free Trial': '开始免费试用',
    'Try It Now': '立即试用',
    'Learn More': '了解更多',
    'Get Started': '开始使用',
    
    # CTA
    'Ready to Get Started?': '准备开始了吗？',
    'Ready to Start Building?': '准备开始构建了吗？',
    'Start Building Today': '今天就开始构建',
    
    # Newsletter
    'Subscribe to our newsletter': '订阅我们的新闻通讯',
    'Enter your email': '输入您的邮箱',
    'Subscribe': '订阅',
    
    # Footer
    'Quick Links': '快速链接',
    'Products': '产品',
    'Resources': '资源',
    'Company': '公司',
    'Documentation': '文档',
    'API Reference': 'API 参考',
    'Tutorials': '教程',
    'Case Studies': '案例研究',
    'Legal': '法律',
    'Privacy Policy': '隐私政策',
    'Terms of Service': '服务条款',
    'Official Website': '官方网站',
    'Console': '控制台',
    'Amazon Solutions': 'Amazon 解决方案',
    'Blog Articles': '博客文章',
    
    '© 2025 Pangol Info Scrape API. All rights reserved.': 
    '© 2025 Pangol Info Scrape API. 保留所有权利。',
    
    'Professional Amazon scraping API and e-commerce data extraction solutions for businesses worldwide.':
    '为全球企业提供专业的 Amazon 数据抓取 API 和电商数据提取解决方案。',
}

def translate_article(filename):
    """翻译单篇文章"""
    print(f"📝 正在翻译: {filename}")
    
    # 读取英文文章
    with open(f'articles/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content)
    
    # 应用通用翻译
    for en, zh in common_translations.items():
        content = content.replace(en, zh)
    
    # 添加 Hreflang 标签
    if 'Hreflang Tags' not in content:
        hreflang = f'''    <!-- Hreflang Tags -->
    <link rel="alternate" hreflang="en" href="https://blog.pangolinfo.com/articles/{filename}">
    <link rel="alternate" hreflang="zh-CN" href="https://blog.pangolinfo.com/zh/articles/{filename}">
    <link rel="alternate" hreflang="x-default" href="https://blog.pangolinfo.com/articles/{filename}">

'''
        content = content.replace('</head>', hreflang + '</head>')
    
    # 修复导航链接 - 指向中文版本
    content = content.replace('href="index.html', 'href="/zh/index.html')
    content = content.replace('href="blog.html', 'href="/zh/blog.html')
    content = content.replace('href="../index.html', 'href="/zh/index.html')
    content = content.replace('href="../blog.html', 'href="/zh/blog.html')
    
    # 语言切换器 - 中文页面显示 English
    content = re.sub(
        r'<a href="/zh/articles/[^"]*" class="language-btn">\s*<span>🇨🇳</span>\s*<span>中文</span>',
        f'<a href="/articles/{filename}" class="language-btn">\n                        <span>🇺🇸</span>\n                        <span>English</span>',
        content
    )
    
    # 如果没有语言切换器，添加一个
    if 'language-btn' not in content:
        # 这里可以添加语言切换器的代码
        pass
    
    # 保存中文版本
    with open(f'zh/articles/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)
    
    translated_size = len(content)
    print(f"  ✅ 完成: {original_size} → {translated_size} 字符")
    
    return True

# 翻译所有文章
success_count = 0
for article in articles:
    try:
        if translate_article(article):
            success_count += 1
        print()
    except Exception as e:
        print(f"  ❌ 错误: {e}\n")

print("=" * 60)
print(f"✅ 翻译完成！")
print(f"📊 成功: {success_count}/{len(articles)} 篇文章")
print(f"📁 输出目录: zh/articles/")
print("\n⚠️  注意: 这是基础翻译，每篇文章可能还需要针对性的内容翻译")
print("建议逐篇检查并补充翻译文章标题、描述等核心内容")
