#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制翻译 getting-started-amazon-scraping-api.html 的正文
采用基于 HTML 结构的精确定位替换
"""

import re

filepath = 'zh/articles/getting-started-amazon-scraping-api.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"📝 正在强制翻译: {filepath}")

# 1. 替换引言 (Intro Paragraph)
# 定位: <p class="text-xl text-gray-300 font-medium mb-8">
# 内容: "Amazon product data extraction has become essential..."
intro_pattern = r'(<p class="text-xl text-gray-300 font-medium mb-8">\s*)([\s\S]*?)(\s*</p>)'
intro_translation = """
    Amazon 产品数据提取已成为电商企业、市场研究人员和数据分析师的必备能力。无论您是监控竞争对手价格、进行产品研究，还是构建价格比对工具，可靠地访问 Amazon 庞大的产品目录都至关重要。本综合指南将带您了解使用 Pangol Info 的 Amazon 数据抓取 API 高效、大规模提取产品数据所需的一切知识。
"""
if re.search(intro_pattern, content):
    content = re.sub(intro_pattern, lambda m: f"{m.group(1)}{intro_translation.strip()}{m.group(3)}", content)
    print("  ✅ 引言已翻译")
else:
    print("  ⚠️ 未找到引言段落")


# 2. 替换 "为什么 Amazon 产品数据提取很重要" 下面的段落
# 定位: <h2 id="why-amazon-product-data-extraction-matters">...</h2> 紧接着的 <p>
# 原文: "Amazon hosts over 350 million products..."
why_matters_h2 = r'(<h2 id="why-amazon-product-data-extraction-matters">.*?</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
why_matters_trans = """
    Amazon 在全球多个市场拥有超过 3.5 亿种产品。对于在电商领域运营的企业而言，访问这些数据可提供无价的洞察：
"""
if re.search(why_matters_h2, content):
    content = re.sub(why_matters_h2, lambda m: f"{m.group(1)}{why_matters_trans.strip()}{m.group(3)}", content)
    print("  ✅ '为什么重要' 段落已翻译")

# 3. 替换下面的列表 (Competitive Intelligence, etc.)
# 我们直接替换整个列表项
list_translations = [
    (r'<strong>Competitive Intelligence</strong>: Track competitor pricing strategies, product\s+launches, and inventory levels in real-time',
     '<strong>竞争情报</strong>：实时跟踪竞争对手的定价策略、产品发布和库存水平'),
    (r'<strong>Market Research</strong>: Identify trending products, analyze customer sentiment\s+through reviews, and discover market gaps',
     '<strong>市场研究</strong>：识别热门产品，通过评论分析客户情绪，并发现市场空白'),
    (r'<strong>Dynamic Pricing</strong>: Adjust your pricing strategy based on real-time market\s+data to maximize profitability',
     '<strong>动态定价</strong>：根据实时市场数据调整您的定价策略，以实现利润最大化'),
    (r'<strong>Product Selection</strong>: Make data-driven decisions about which products to\s+sell based on demand, competition, and profitability metrics',
     '<strong>选品决策</strong>：根据需求、竞争和盈利指标，做出数据驱动的产品销售决策'),
    (r'<strong>Inventory Management</strong>: Monitor stock levels and availability patterns to\s+optimize your own inventory',
     '<strong>库存管理</strong>：监控库存水平和供货模式，以优化您自己的库存'),
]

for pattern, trans in list_translations:
    # 使用正则替换，允许空白字符
    content = re.sub(pattern, trans, content, flags=re.DOTALL)
print("  ✅ 列表项已翻译")

# 4. 替换 "However, extracting this data manually..."
# 定位: 上一个列表结束后的 <p>
however_pattern = r'(</ul>\s*<p>\s*)(However, extracting this data manually is impractical[\s\S]*?)(\s*</p>)'
however_trans = """
    然而，大规模手动提取数据是不切实际的。Amazon 的网站结构复杂，频繁变化，并实施了复杂的反爬虫措施。这正是 Pangol Info 的 Amazon 数据抓取 API 发挥价值的地方。
"""
if re.search(however_pattern, content):
    content = re.sub(however_pattern, lambda m: f"{m.group(1)}{however_trans.strip()}{m.group(3)}", content)
    print("  ✅ However 段落已翻译")

# 5. 替换 "了解 Pangol Info 的 Amazon 数据抓取 API" 下面的段落
# 定位: <h2 id="understanding-pangol-info's-amazon-scraping-api">...</h2> 紧接着的 <p>
understanding_h2 = r'(<h2 id="understanding-pangol-infos-amazon-scraping-api">.*?</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
# 注意: id 可能已经被之前的脚本修改过，可能是 id="understanding-pangol-infos-amazon-scraping-api"
# 让我检查之前的文件的 id
# 之前的脚本产生的 id 可能是: understanding-pangol-infos-amazon-scraping-api (把 ' 去掉了)
# 原文 id 是: understanding-pangol-info's-amazon-scraping-api
# 但现在的 content 里已经是中文标题了吗？是的。
# 让我宽容一些匹配
understanding_h2_loose = r'(<h2[^>]*>了解 Pangol Info.*?</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
understanding_trans = """
    Pangol Info 的 Amazon 数据抓取 API 是专为 Amazon 数据提取设计的企业级解决方案。与普通的网络爬虫不同，它处理了 Amazon 基础设施的所有复杂性：
"""
if re.search(understanding_h2_loose, content):
    content = re.sub(understanding_h2_loose, lambda m: f"{m.group(1)}{understanding_trans.strip()}{m.group(3)}", content)
    print("  ✅ '了解 API' 段落已翻译")

# 6. Key Features 列表
key_features_trans = [
    (r'<strong>99.9% Success Rate</strong>: Advanced anti-detection technology ensures\s+reliable data extraction', '<strong>99.9% 成功率</strong>：先进的反检测技术确保可靠的数据提取'),
    (r'<strong>Multi-Marketplace Support</strong>: Extract data from Amazon.com,\s+Amazon.co.uk, Amazon.de, and 15\+ other marketplaces', '<strong>多市场支持</strong>：从 Amazon.com、Amazon.co.uk、Amazon.de 和其他 15+ 个市场提取数据'),
    (r'<strong>Comprehensive Data Fields</strong>: Access product details, pricing,\s+reviews, ratings, images, variants, and more', '<strong>全面的数据字段</strong>：访问产品详情、定价、评论、评分、图片、变体等'),
    (r'<strong>Real-time Data</strong>: Get fresh, up-to-date information with sub-second\s+response times', '<strong>实时数据</strong>：以亚秒级响应时间获取最新的实时信息'),
    (r'<strong>Scalable Infrastructure</strong>: Handle millions of requests with\s+enterprise-grade reliability', '<strong>可扩展架构</strong>：以企业级可靠性处理数百万请求')
]
for pattern, trans in key_features_trans:
    content = re.sub(pattern, trans, content, flags=re.DOTALL)
print("  ✅ Key Features 已翻译")

# 7. Prerequisites
# <p>Before diving into code, you'll need:</p>
prereq_pattern = r'(<p>Before diving into code, you\'ll need:</p>)'
prereq_trans = '<p>在深入代码之前，您需要准备：</p>'
content = re.sub(prereq_pattern, prereq_trans, content)

prereq_list = [
    (r'<strong>Pangol Info API Account</strong>: Sign up at', '<strong>Pangol Info API 账户</strong>：注册于'),
    (r'to get your API\s+credentials', '以获取您的 API 凭证'),
    (r'<strong>API Key</strong>: Obtain your authentication key from the dashboard \(you\'ll get\s+1,000 free credits to start\)', '<strong>API Key</strong>：从控制台获取您的认证密钥（您将获得 1,000 个免费积分作为开始）'),
    (r'<strong>Development Environment</strong>: Python 3.7\+, Node.js 14\+, or any language that\s+can make HTTP requests', '<strong>开发环境</strong>：Python 3.7+、Node.js 14+ 或任何可以发送 HTTP 请求的语言'),
    (r'<strong>Basic Programming Knowledge</strong>: Familiarity with REST APIs and JSON data\s+structures', '<strong>基础编程知识</strong>：熟悉 REST API 和 JSON 数据结构')
]
for pattern, trans in prereq_list:
    content = re.sub(pattern, trans, content, flags=re.DOTALL)
print("  ✅ Prerequisites 已翻译")

# 8. Authentication
auth_p = r'(<h2[^>]*>身份验证和 API 基础</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
auth_trans = """
    Pangol Info 的 API 使用 Bearer 令牌认证。每个请求都必须在 Authorization 标头中包含您的 API 密钥。基本结构如下：
"""
if re.search(auth_p, content):
    content = re.sub(auth_p, lambda m: f"{m.group(1)}{auth_trans.strip()}{m.group(3)}", content)
    print("  ✅ Authentication 段落已翻译")

# 9. Step-by-Step Guide Intro (Basic Product Info)
step_basic_p = r'(<h3[^>]*>1. 基础产品信息提取</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
step_basic_trans = """
    让我们从提取基础产品信息开始。最常见的用例是使用 ASIN（Amazon 标准识别码）从产品详情页获取数据。
"""
if re.search(step_basic_p, content):
    content = re.sub(step_basic_p, lambda m: f"{m.group(1)}{step_basic_trans.strip()}{m.group(3)}", content)
    print("  ✅ Step 1 段落已翻译")
    
# 10. Code explanation "Python Example:"
content = content.replace('<p><strong>Python Example:</strong></p>', '<p><strong>Python 示例：</strong></p>')

# 11. Understanding Response
resp_p = r'(<h3[^>]*>2. 理解响应结构</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
resp_trans = """
    当您设置 <code>format: "json"</code> 时，Pangolin 会返回如下结构的 JSON 数据：
"""
if re.search(resp_p, content):
    content = re.sub(resp_p, lambda m: f"{m.group(1)}{resp_trans.strip()}{m.group(3)}", content)
    print("  ✅ Step 2 段落已翻译")

# 12. Price Monitoring
price_p = r'(<h3[^>]*>3. 构建价格监控系统</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
price_trans = """
    价格监控是 Amazon 数据提取最有价值的应用之一。这是一个完整的示例：
"""
if re.search(price_p, content):
    content = re.sub(price_p, lambda m: f"{m.group(1)}{price_trans.strip()}{m.group(3)}", content)
    print("  ✅ Step 3 段落已翻译")

# 13. Best Practices
best_p = r'(<h3[^>]*>速率限制和错误处理</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
best_trans = """
    实施适当的速率限制和错误处理可确保可靠的长期运行：
"""
if re.search(best_p, content):
    content = re.sub(best_p, lambda m: f"{m.group(1)}{best_trans.strip()}{m.group(3)}", content)
    print("  ✅ Best Practices 段落已翻译")
    
# 14. Conclusion
concl_p = r'(<h2[^>]*>总结</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)'
concl_trans = """
    Amazon 产品数据提取是一项强大的能力，可以改变您的电商业务战略。借助 Pangol Info 的 Amazon 数据抓取 API，您可以访问企业级基础设施，处理所有数据提取的复杂性，从而专注于获取洞察和做出数据驱动的决策。
"""
if re.search(concl_p, content):
    content = re.sub(concl_p, lambda m: f"{m.group(1)}{concl_trans.strip()}{m.group(3)}", content)
    print("  ✅ Conclusion 段落已翻译")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ {filepath} 强制翻译完成")
