#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制翻译剩余 5 篇文章的正文
采用基于 HTML 结构和唯一ID的精确定位替换
"""

import re
import os

# ================= 通用辅助函数 =================
def translate_file(filepath, replacements):
    print(f"\n📝 处理: {filepath}")
    if not os.path.exists(filepath):
        print(f"  ❌ 文件未找到: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_count = 0
    for pattern, substitution in replacements:
        if re.search(pattern, content):
            # 如果 substitution 是函数（lambda），直接传递
            if callable(substitution):
                content = re.sub(pattern, substitution, content)
            else:
                # 否则直接替换
                content = re.sub(pattern, substitution, content, flags=re.DOTALL)
            modified_count += 1
        else:
            # 调试用：打印未找到的模式的前60个字符
            # print(f"  ⚠️ 未找到模式: {pattern[:60]}...")
            pass
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 更新了 {modified_count} 处内容")

# ================= 翻译配置 =================

# 1. Advanced Best Practices
advanced_replacements = [
    # Intro
    (r'(<p class="text-xl text-gray-300 font-medium mb-8">\s*)([\s\S]*?)(\s*</p>)', 
     lambda m: f"{m.group(1)}虽然基础的产品抓取很简单，但在企业级规模上提取数据会引入一系列新的复杂性。速率限制、IP 封禁、数据验证和并发请求管理成为成功的关键因素。在这个高级指南中，我们将探讨顶级电商数据团队使用的最佳实践和优化策略，利用 Pangol Info 的 API 构建稳健、可扩展的 Amazon 抓取管道。{m.group(3)}"),
    
    # Understanding Architecture H2 -> P
    (r'(<h2[^>]*>.*?</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)', 
     lambda m: f"{m.group(1)}在优化之前，了解现代 Amazon API 如何处理请求至关重要。一个稳健的架构通常包括：{m.group(3)}"),
    
    # Architecture List
    (r'<strong>Request Scheduler</strong>: Manages the queue and timing of outgoing API calls', 
     '<strong>请求调度器</strong>：管理传出 API 调用的队列和时间'),
    (r'<strong>Proxy & Rotation Layer</strong>: Handled automatically by Pangol Info, but meaningful to understand', 
     '<strong>代理与轮换层</strong>：由 Pangol Info 自动处理，但理解其原理很有意义'),
    (r'<strong>Parser & Validator</strong>: Checks response integrity before storage', 
     '<strong>解析器与验证器</strong>：在存储之前检查响应的完整性'),
    (r'<strong>Storage Layer</strong>: Efficiently saves structured data', 
     '<strong>存储层</strong>：高效保存结构化数据'),
     
    # Advanced Extraction Techniques
    (r'(<h2[^>]*>高级提取技术</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}在处理数千个 ASIN 时，顺序处理太慢了。实施具有适当并发控制的并行处理至关重要。{m.group(3)}"),
     
    # Batch Processing
    (r'(<h3[^>]*>批量处理</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}不要逐个处理项目，而是将它们分组为批次。这减少了开销并使错误恢复更容易。如果一个批次失败，您只需要重试该特定的 ASIN 子集。{m.group(3)}"),
     
    # Data Validation
    (r'(<h3[^>]*>数据验证</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}永远不要盲目信任传入的数据。Amazon 的 HTML 结构频繁变化，可能导致解析错误。实施验证层以确保数据质量。需要实施的关键检查：{m.group(3)}"),
    
    # Validation List
    (r'<strong>Required Fields</strong>: Ensure critical fields like price and title are present', 
     '<strong>必填字段</strong>：确保存在价格和标题等关键字段'),
    (r'<strong>Data Types</strong>: Verify price is a number, date is valid, etc\.', 
     '<strong>数据类型</strong>：验证价格是数字，日期有效等'),
    (r'<strong>Logic Checks</strong>: Price shouldn\'t be zero unless free', 
     '<strong>逻辑检查</strong>：除非免费，否则价格不应为零'),
     
    # Error Handling Strategy H3 -> P
    (r'(<h3[^>]*>错误处理策略</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}稳健的错误处理将专业抓取工具与业余脚本区分开来。您需要制定应对不同类型错误的策略：{m.group(3)}"),
     
    # Error List
    (r'<strong>404 Not Found</strong>: The product might be delisted\. Log it and remove from queue', 
     '<strong>404 未找到</strong>：产品可能已下架。记录它并从队列中移除'),
    (r'<strong>429 Too Many Requests</strong>: You are hitting limits\. Implement exponential backoff', 
     '<strong>429 请求过多</strong>：您已达到限制。实施指数退避算法'),
    (r'<strong>5xx Server Errors</strong>: Amazon or API issue\. Retry after a delay', 
     '<strong>5xx 服务器错误</strong>：Amazon 或 API 问题。延迟后重试'),
     
    # Rate Limiting
    (r'(<h3[^>]*>速率限制最佳实践</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}即使使用企业级 API，遵守限制也是良好的公民行为并能确保稳定性。使用<code>令牌桶</code>算法或简单的固定窗口计数器在本地管理您的请求速率。{m.group(3)}"),
     
    # Conclusion
    (r'(<h2[^>]*>总结</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}构建高性能 Amazon 抓取工具不仅仅需要代码；它需要架构思维。通过实施这些最佳实践——验证、错误处理和并发——您可以构建一个可靠且可扩展的系统。{m.group(3)}")
]

# 2. Product Selection
selection_replacements = [
    (r'(<p class="text-xl text-gray-300 font-medium mb-8">\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}在广阔的 Amazon 市场中，选择合适的产品进行销售往往决定了成败。凭直觉或有限数据做决定是有风险的。在本指南中，我们将向您展示如何利用 Pangol Info 的 API 数据来识别高潜力的利基市场、分析竞争对手并以最小风险验证产品创意。{m.group(3)}"),
    
    (r'(<h2[^>]*>.*?</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}成功的卖家使用数据来识别高需求、低竞争的利基市场。与其猜测什么好卖，不如分析市场信号：{m.group(3)}"),
     
    (r'(<h3[^>]*>.*?</h3>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}通过分析销售排名 (BSR)、价格历史和评论增长，您可以准确估算需求的稳定性。{m.group(3)}"), # 第一个 H3
]

# 3. Ad Monitoring
ad_replacements = [
    (r'(<p class="text-xl text-gray-300 font-medium mb-8">\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}Amazon 赞助产品是知名度和销量的主要驱动力。然而，如果不了解竞争对手的策略，您实际上是在盲目出价。在本文中，我们将探讨如何使用 Amazon SERP API 来监控竞争对手的广告，揭示他们的关键词策略，并优化您自己的广告活动以获得最大投资回报率。{m.group(3)}"),
    
    (r'(<h2[^>]*>.*?</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}Amazon 的广告生态系统竞争激烈。监控您的竞争对手可以让您：发现新的高转化关键词、了解他们的出价策略，并识别您可以超越他们的机会。{m.group(3)}")
]

# 4. Price Monitoring
price_replacements = [
    (r'(<p class="text-xl text-gray-300 font-medium mb-8">\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}价格是影响 Amazon 购买决策的最重要因素之一。在这份技术指南中，我们将构建一个稳健的价格监控系统，使用 Python 和 Pangol Info 的 API 来跟踪价格变化、检测折扣并触发自动警报。{m.group(3)}"),
    
    (r'(<h2[^>]*>.*?</h2>\s*<p>\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}在电商领域，价格波动频繁。自动化监控系统让您保持领先，而无需全天候手动检查页面。{m.group(3)}")
]

# 5. Case Studies
case_replacements = [
    (r'(<p class="text-xl text-gray-300 font-medium mb-8">\s*)([\s\S]*?)(\s*</p>)',
     lambda m: f"{m.group(1)}理论虽好，但现实世界的结果更佳。在这个案例研究集中，我们展示了各种企业——从初创公司到大型企业——如何利用 Amazon 数据提取来实现显著增长、优化运营并获得竞争优势。{m.group(3)}"),
]

# 执行列表
tasks = [
    ("zh/articles/advanced-amazon-data-extraction-best-practices.html", advanced_replacements),
    ("zh/articles/amazon-product-selection-api-data.html", selection_replacements),
    ("zh/articles/amazon-sponsored-products-ad-monitoring.html", ad_replacements),
    ("zh/articles/amazon-price-monitoring-system.html", price_replacements),
    ("zh/articles/amazon-business-case-studies.html", case_replacements),
]

print("🚀 开始强制翻译剩余文章正文...")
for filepath, replacements in tasks:
    translate_file(filepath, replacements)

print("\n✅ 完成")
