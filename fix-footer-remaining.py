#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余文章的页脚 (处理第二种页脚样式)
"""

import re
import os

articles = [
    'amazon-price-monitoring-system.html',
    'amazon-business-case-studies.html'
]

print("🔍 开始修复剩余文章的页脚...")

replacements = [
    (r'Empowering Amazon sellers with enterprise-grade data infrastructure\.', 
     '利用企业级数据基础设施为 Amazon 卖家赋能。'),
    (r'All rights reserved\.', '保留所有权利。')
]

for filename in articles:
    filepath = f'zh/articles/{filename}'
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for eng, ch in replacements:
        if re.search(eng, content):
            content = re.sub(eng, ch, content)
            modified = True
            print(f"  ✅ [页脚] {filename}: 已翻译 '{eng[:20]}...'")
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("\n✅ 完成")
