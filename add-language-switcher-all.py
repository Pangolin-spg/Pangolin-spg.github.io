#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有6篇文章添加语言切换按钮
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

print("🚀 为所有文章添加语言切换按钮...")
print("=" * 60)

# 语言切换器样式
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

success_count = 0

for filename in articles:
    print(f"\n📝 处理: {filename}")
    
    try:
        # 读取文件
        with open(f'zh/articles/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 添加样式（如果还没有）
        if 'language-switcher' not in content:
            content = content.replace('</style>', language_styles + '    </style>')
            print("  ✅ 已添加语言切换器样式")
        
        # 2. 在导航栏添加语言切换按钮
        # 找到 "获取 API Key" 按钮
        nav_button_pattern = r'(<a href="https://tool\.pangolinfo\.com/"[^>]*>\s*获取 API Key\s*</a>)'
        
        language_switcher_html = f'''            <div class="flex items-center gap-4">
                <!-- Language Switcher -->
                <div class="language-switcher">
                    <a href="/articles/{filename}" class="language-btn">
                        <span>🇺🇸</span>
                        <span>English</span>
                    </a>
                </div>
                <!-- Get API Key Button -->
                \\1
            </div>'''
        
        # 检查是否已经有语言切换按钮
        if 'language-switcher' in content and 'language-btn' in content:
            # 已经有按钮，只需要确保链接正确
            content = re.sub(
                r'<a href="[^"]*" class="language-btn">',
                f'<a href="/articles/{filename}" class="language-btn">',
                content
            )
            print("  ✅ 已更新语言切换按钮链接")
        else:
            # 添加语言切换按钮
            content = re.sub(
                nav_button_pattern,
                language_switcher_html,
                content
            )
            print("  ✅ 已添加语言切换按钮到导航栏")
        
        # 保存
        with open(f'zh/articles/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        
        success_count += 1
        print(f"  ✅ 完成")
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")

print("\n" + "=" * 60)
print(f"✅ 完成！成功处理 {success_count}/{len(articles)} 篇文章")
print("\n所有文章现在都有语言切换按钮了！")
