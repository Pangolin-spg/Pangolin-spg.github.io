#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有中文文章中侧边栏 (Sidebar) 产品卡片的英文内容
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

print("🔍 开始修复侧边栏卡片内容...")

replacements = [
    # Scrape API Card
    (r'Professional Amazon scraping API with 99\.9% uptime and automatic captcha handling\.', 
     '具有 99.9% 正常运行时间和自动验证码处理功能的专业 Amazon 抓取 API。'),
    (r'<span class="text-xs text-accent-cyan bg-accent-cyan/10 px-2 py-0.5 rounded">Best\s+Seller</span>',
     '<span class="text-xs text-accent-cyan bg-accent-cyan/10 px-2 py-0.5 rounded">畅销</span>'),
     
    # AMZ Tracker Card
    (r'Visual dashboard for tracking ASIN performance, keywords, and BSR history\.', 
     '用于跟踪 ASIN 表现、关键词和 BSR 历史的可视化仪表板。'),
    (r'<span\s+class="text-xs text-accent-purple bg-accent-purple/10 px-2 py-0.5 rounded">New</span>',
     '<span class="text-xs text-accent-purple bg-accent-purple/10 px-2 py-0.5 rounded">新</span>'),
    (r'View Demo', '查看演示'),
     
    # Extension Card
    (r'Free Chrome extension for quick data extraction directly from your browser\.', 
     '免费 Chrome 扩展，直接从浏览器快速提取数据。'),
    (r'<span class="text-xs text-gray-400 bg-gray-800 px-2 py-0.5 rounded">Free</span>',
     '<span class="text-xs text-gray-400 bg-gray-800 px-2 py-0.5 rounded">免费</span>'),
    (r'Install Now', '立即安装'),
    
    # 额外检查
    (r'Install Extension', '安装扩展'),
    (r'Browser Extension', '浏览器扩展'),
    (r'AMZ Data Tracker Chrome extension for instant Amazon\s+product analysis', 
     'AMZ Data Tracker Chrome 扩展用于即时 Amazon 产品分析')
]

for filename in articles:
    filepath = f'zh/articles/{filename}'
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    modified = False
    for pat, rep in replacements:
        if re.search(pat, content, re.IGNORECASE | re.DOTALL):
            content = re.sub(pat, rep, content, flags=re.IGNORECASE | re.DOTALL)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ [侧边栏] {filename} 已修复")
    else:
        print(f"  ✓ [侧边栏] {filename} 未发现需修复内容")

print("\n✅ 完成")
