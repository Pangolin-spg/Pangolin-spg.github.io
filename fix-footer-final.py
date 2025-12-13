#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有中文文章中遗漏的页脚文本（处理跨行情况）
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

print("🔍 开始精确检查并修复页脚...")

footer_desc_pattern = r'Professional Amazon scraping API and e-commerce data extraction\s+solutions for businesses worldwide\.'
footer_desc_trans = '为全球企业提供专业的 Amazon 数据抓取 API 和电商数据提取解决方案。'

footer_sub_pattern = r'Amazon Scraping API & E-commerce Data Intelligence'
footer_sub_trans = 'Amazon 数据抓取 API 与电商数据智能'

for filename in articles:
    filepath = f'zh/articles/{filename}'
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    
    # 修复描述
    if re.search(footer_desc_pattern, content, re.DOTALL):
        content = re.sub(footer_desc_pattern, footer_desc_trans, content, flags=re.DOTALL)
        modified = True
        print(f"  ✅ [页脚描述] {filename} 已修复")
    else:
        # 检查是否已经是中文
        if "为全球企业提供专业的" in content:
            print(f"  ✓ [页脚描述] {filename} 已是中文")
        else:
            print(f"  ⚠️ [页脚描述] {filename} 未找到匹配文本")

    # 修复底部版权行的副标题
    if re.search(footer_sub_pattern, content):
        content = re.sub(footer_sub_pattern, footer_sub_trans, content)
        modified = True
        print(f"  ✅ [页脚副标] {filename} 已修复")
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("\n✅ 完成")
