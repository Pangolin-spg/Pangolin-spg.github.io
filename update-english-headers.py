#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有英文文章页面的导航栏
添加语言切换按钮，统一风格
"""

import re
import os

articles = [
    'getting-started-amazon-scraping-api.html',
    'advanced-amazon-data-extraction-best-practices.html',
    'amazon-product-selection-api-data.html',
    'amazon-sponsored-products-ad-monitoring.html',
    'amazon-price-monitoring-system.html',
    'amazon-business-case-studies.html'
]

print("🚀 更新英文文章页面导航栏...")
print("=" * 60)

# 标准英文导航栏模板
standard_nav_template = '''    <!-- Navigation -->
    <nav class="fixed w-full z-50 transition-all duration-300 backdrop-blur-md bg-black/20" id="navbar">
        <div class="glass-card rounded-full mt-4 mx-auto max-w-7xl px-6 py-3 flex justify-between items-center">
            <a href="/index.html" class="flex items-center gap-3">
                <img src="https://www.pangolinfo.com/wp-content/uploads/2025/06/Pangolin-LOGO-Scrape-API-.webp"
                    alt="Pangolin Amazon Scraping API Logo"
                    class="w-8 h-8 rounded-lg shadow-lg shadow-accent-cyan/30" />
                <span class="text-xl font-bold tracking-tight">PANGOLIN</span>
            </a>
            <div class="hidden md:flex gap-8 text-sm font-medium text-gray-300">
                <a href="/index.html#home" class="nav-link hover:text-white transition">Home</a>
                <a href="/index.html#solutions" class="nav-link hover:text-white transition">Solutions</a>
                <a href="/index.html#use-cases" class="nav-link hover:text-white transition">Use Cases</a>
                <a href="/blog.html" class="nav-link hover:text-white transition">Blog</a>
                <a href="https://docs.pangolinfo.com/en-index" class="nav-link hover:text-white transition">Docs</a>
                <a href="https://www.pangolinfo.com/scrape-api-pricing-2/"
                    class="nav-link hover:text-white transition">Pricing</a>
            </div>
            <div class="flex items-center gap-4">
                <!-- Language Switcher -->
                <div class="language-switcher">
                    <a href="/zh/articles/FILENAME" class="language-btn">
                        <span>🇨🇳</span>
                        <span>中文</span>
                    </a>
                </div>
                <!-- Get API Key Button -->
                <a href="https://tool.pangolinfo.com/"
                    class="bg-white/10 hover:bg-white/20 border border-white/10 backdrop-blur-sm px-5 py-2 rounded-full text-sm font-semibold transition hover:shadow-lg hover:shadow-accent-cyan/20">
                    Get API Key
                </a>
            </div>
        </div>
    </nav>
'''

# 语言切换器样式
style_code = '''
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
    </style>'''

success_count = 0

for filename in articles:
    filepath = f'articles/{filename}'
    print(f"\n📝 处理: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. 替换导航栏
        # 构造当篇特定的导航栏
        nav_html = standard_nav_template.replace('FILENAME', filename)
        
        # 使用正则替换原有 nav
        nav_pattern = r'<nav class="fixed[^>]*>.*?</nav>'
        if re.search(nav_pattern, content, re.DOTALL):
            content = re.sub(nav_pattern, nav_html.strip(), content, flags=re.DOTALL)
            print("  ✅ 已更新导航栏")
        else:
            print("  ⚠️  未找到导航栏，跳过")

        # 2. 添加 CSS 样式 (如果还没有)
        if '.language-btn {' not in content:
            content = content.replace('</style>', style_code)
            print("  ✅ 已添加 CSS 样式")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        success_count += 1
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")

print("\n" + "=" * 60)
print(f"✅ 完成！更新了 {success_count}/{len(articles)} 篇英文文章")
