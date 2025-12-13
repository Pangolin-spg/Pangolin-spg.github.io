#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一所有文章页面的导航栏
使用与首页和博客汇总页相同的导航栏结构
"""

import re

articles = [
    'getting-started-amazon-scraping-api.html',
    'advanced-amazon-data-extraction-best-practices.html',
    'amazon-product-selection-api-data.html',
    'amazon-sponsored-products-ad-monitoring.html',
    'amazon-price-monitoring-system.html',
    'amazon-business-case-studies.html'
]

print("🚀 统一所有文章页面的导航栏...")
print("=" * 60)

# 标准导航栏HTML（中文版）
standard_nav = '''    <!-- Navigation -->
    <nav class="fixed w-full z-50 transition-all duration-300" id="navbar">
        <div class="glass-card rounded-full mt-4 mx-auto max-w-6xl px-6 py-3 flex justify-between items-center">
            <a href="https://www.pangolinfo.com/" class="flex items-center gap-3">
                <img src="https://www.pangolinfo.com/wp-content/uploads/2025/06/Pangolin-LOGO-Scrape-API-.webp"
                    alt="Pangolin Amazon 数据抓取 API Logo"
                    class="w-8 h-8 rounded-lg shadow-lg shadow-accent-cyan/30" />
                <span class="text-xl font-bold tracking-tight">PANGOLIN</span>
            </a>
            <div class="hidden md:flex gap-8 text-sm font-medium text-gray-300">
                <a href="/zh/index.html#home" class="nav-link hover:text-white transition">首页</a>
                <a href="/zh/index.html#solutions" class="nav-link hover:text-white transition">解决方案</a>
                <a href="/zh/index.html#use-cases" class="nav-link hover:text-white transition">应用场景</a>
                <a href="/zh/blog.html" class="nav-link hover:text-white transition">博客</a>
                <a href="https://docs.pangolinfo.com/en-index" class="nav-link hover:text-white transition">文档</a>
                <a href="https://www.pangolinfo.com/scrape-api-pricing-2/"
                    class="nav-link hover:text-white transition">定价</a>
            </div>
            <div class="flex items-center gap-4">
                <!-- Language Switcher -->
                <div class="language-switcher">
                    <a href="/articles/FILENAME" class="language-btn">
                        <span>🇺🇸</span>
                        <span>English</span>
                    </a>
                </div>
                <!-- Get API Key Button -->
                <a href="https://tool.pangolinfo.com/"
                    class="bg-white/10 hover:bg-white/20 border border-white/10 backdrop-blur-sm px-5 py-2 rounded-full text-sm font-semibold transition hover:shadow-lg hover:shadow-accent-cyan/20">
                    获取 API Key
                </a>
            </div>
        </div>
    </nav>
'''

success_count = 0

for filename in articles:
    print(f"\n📝 处理: {filename}")
    
    try:
        # 读取文件
        with open(f'zh/articles/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换文件名占位符
        nav_html = standard_nav.replace('FILENAME', filename)
        
        # 找到并替换整个导航栏
        # 匹配从 <nav 到 </nav> 的整个导航栏
        nav_pattern = r'<nav class="fixed[^>]*>.*?</nav>'
        
        if re.search(nav_pattern, content, re.DOTALL):
            content = re.sub(nav_pattern, nav_html.strip(), content, flags=re.DOTALL)
            print("  ✅ 已替换为标准导航栏")
        else:
            print("  ⚠️  未找到导航栏，跳过")
        
        # 保存
        with open(f'zh/articles/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        
        success_count += 1
        print(f"  ✅ 完成")
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")

print("\n" + "=" * 60)
print(f"✅ 完成！成功处理 {success_count}/{len(articles)} 篇文章")
print("\n所有文章现在都使用统一的导航栏了！")
print("包含: LOGO + 导航菜单 + 语言切换按钮 + 获取 API Key 按钮")
