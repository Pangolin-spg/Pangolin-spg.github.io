#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有中文文章中遗漏的 '下一步' (Next Steps) 列表及其他提示框内容
"""

import re
import os

# 定义所有文章路径
articles = [
    'getting-started-amazon-scraping-api.html',
    'advanced-amazon-data-extraction-best-practices.html',
    'amazon-product-selection-api-data.html',
    'amazon-sponsored-products-ad-monitoring.html',
    'amazon-price-monitoring-system.html',
    'amazon-business-case-studies.html'
]

# 定义替换规则列表 (Regex Pattern -> Replacement String)
# 使用 re.DOTALL 确保匹配跨行
replacements = [
    # 1. Sign up for Pangolin
    (r'<li><strong>Sign up for Pangolin</strong>: Get your free API key at', 
     '<li><strong>注册 Pangolin</strong>：免费获取您的 API Key 于'),
     
    # 2. Explore the Docs
    # 注意：用户反馈中已经是 "Explore the 文档"，说明之前有部分脚本把 "Documentation" 替换成了 "文档"
    (r'<li><strong>Explore the (Documentation|文档)</strong>: Visit', 
     '<li><strong>探索文档</strong>：访问'),
     
    (r'for complete\s+API reference', '获取完整的 API 参考'),
     
    # 3. Test in the Playground
    (r'<li><strong>Test in the Playground</strong>: Try the interactive API Playground', 
     '<li><strong>在 Playground 中测试</strong>：尝试交互式 API Playground'),
     
    # 4. Join the Community
    (r'<li><strong>Join the Community</strong>: Connect with other developers and share your\s+use cases', 
     '<li><strong>加入社区</strong>：与其他开发者联系并分享您的用例'),

    # 5. 为了保险，处理 href 链接后的文字 (如 tool.pangolinfo.com 链接后的文字虽然一般不翻译，但上下文可能需要)
    # 这里主要处理列表项文本，上面已经覆盖。
    
    # 6. 处理其他可能的 Box 内容 (Info/Warning/Success)
    
    # "Security Best Practice" Warning Box
    (r'<h4[^>]*><i[^>]*></i>Security Best Practice</h4>', 
     '<h4 class="font-bold text-lg mb-2 text-yellow-500"><i class="fas fa-exclamation-triangle mr-2"></i>安全最佳实践</h4>'),
     
    (r'Never hardcode your API key in client-side code or commit it to version\s+control', 
     '切勿在客户端代码中硬编码您的 API Key 或将其提交到版本控制系统'),
     
    (r'Use environment variables or secure key management systems\.', 
     '使用环境变量或安全密钥管理系统。'),

    # Key Features Box (如果之前漏了)
    (r'<h4[^>]*>Key Features</h4>', 
     '<h4 class="font-bold text-lg mb-2 text-accent-cyan">主要功能</h4>'),
]

print("🚀 开始修复遗漏的列表和提示框...")

for filename in articles:
    filepath = f'zh/articles/{filename}'
    if not os.path.exists(filepath):
        continue
        
    print(f"📝 检查: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for pattern, substitution in replacements:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, substitution, content, flags=re.IGNORECASE | re.DOTALL)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ 已修复遗漏内容")
    else:
        print("  ✓ 未发现遗漏或已修复")

print("\n✅ 完成")
