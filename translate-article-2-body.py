#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译第二篇文章的正文段落
Advanced Amazon Data Extraction Best Practices
"""

import re

filename = 'zh/articles/advanced-amazon-data-extraction-best-practices.html'
print(f"📝 正在翻译正文段落: {filename}")

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

translations = [
    # Intro
    (
        r'While basic product scraping is straightforward, extracting data at an enterprise scale introduces a new set of complexities\. Rate limits, IP blocks, data validation, and concurrent request management become critical factors in your success\.',
        '虽然基础的产品抓取很简单，但在企业级规模上提取数据会引入一系列新的复杂性。速率限制、IP 封禁、数据验证和并发请求管理成为成功的关键因素。'
    ),
    (
        r'In this advanced guide, we\'ll explore the best practices and optimization strategies used by top e-commerce data teams to build robust, scalable Amazon scraping pipelines using Pangol Info\'s API\.',
        '在这份高级指南中，我们将探讨顶级电商数据团队使用的最佳实践和优化策略，利用 Pangol Info 的 API 构建稳健、可扩展的 Amazon 抓取管道。'
    ),
    # Understanding Architecture
    (
        r'Before optimizing, it\'s crucial to understand how modern Amazon APIs handle requests\. A robust architecture typically consists of:',
        '在优化之前，了解现代 Amazon API 如何处理请求至关重要。一个稳健的架构通常包括：'
    ),
    (
        r'<strong>Request Scheduler:</strong> Manages the queue and timing of outgoing API calls',
        '<strong>请求调度器：</strong> 管理传出 API 调用的队列和时间'
    ),
    (
        r'<strong>Proxy & Rotation Layer:</strong> Handled automatically by Pangol Info, but meaningful to understand',
        '<strong>代理和轮换层：</strong> 由 Pangol Info 自动处理，但理解其原理很有意义'
    ),
    (
        r'<strong>Parser & Validator:</strong> Checks response integrity before storage',
        '<strong>解析器和验证器：</strong> 在存储之前检查响应的完整性'
    ),
    (
        r'<strong>Storage Layer:</strong> Efficiently saves structured data',
        '<strong>存储层：</strong> 高效保存结构化数据'
    ),
    # Advanced Extraction Techniques
    (
        r'When dealing with thousands of ASINs, sequential processing is too slow\. Implementing parallel processing with proper concurrency control is essential\.',
        '在处理数千个 ASIN 时，顺序处理太慢了。实施具有适当并发控制的并行处理至关重要。'
    ),
    (
        r'Here is an example using Python\'s <code[^>]*>concurrent\.futures</code>:',
        '这是一个使用 Python <code class="text-accent-cyan">concurrent.futures</code> 的示例：'
    ),
    # Batch Processing
    (
        r'Instead of processing items one by one, group them into batches\. This reduces overhead and makes error recovery easier\. If a batch fails, you only need to retry that specific subset of ASINs\.',
        '不要逐个处理项目，而是将它们分组为批次。这减少了开销并使错误恢复更容易。如果一个批次失败，您只需要重试该特定的 ASIN 子集。'
    ),
    # Data Validation
    (
        r'Never trust the incoming data blindly\. Amazon\'s HTML structure changes frequently, which can lead to parsing errors\. Implement a validation layer to ensure data quality\.',
        '永远不要盲目信任传入的数据。Amazon 的 HTML 结构频繁变化，可能导致解析错误。实施验证层以确保数据质量。'
    ),
    (
        r'Key checks to implement:',
        '需要实施的关键检查：'
    ),
    (
        r'<strong>Required Fields:</strong> Ensure critical fields like price and title are present',
        '<strong>必填字段：</strong> 确保存在价格和标题等关键字段'
    ),
    (
        r'<strong>Data Types:</strong> Verify price is a number, date is valid, etc\.',
        '<strong>数据类型：</strong> 验证价格是数字，日期有效等。'
    ),
    (
        r'<strong>Logic Checks:</strong> Price shouldn\'t be zero unless free',
        '<strong>逻辑检查：</strong> 除非免费，否则价格不应为零'
    ),
    # Error Handling
    (
        r'Robust error handling sets professional scrapers apart from hobbyist scripts\. You need a strategy for different types of errors:',
        '稳健的错误处理将专业抓取工具与业余脚本区分开来。您需要制定应对不同类型错误的策略：'
    ),
    (
        r'<strong>404 Not Found:</strong> The product might be delisted\. Log it and remove from queue\.',
        '<strong>404 未找到：</strong> 产品可能已下架。记录它并从队列中移除。'
    ),
    (
        r'<strong>429 Too Many Requests:</strong> You are hitting limits\. Implement exponential backoff\.',
        '<strong>429 请求过多：</strong> 您已达到限制。实施指数退避算法。'
    ),
    (
        r'<strong>5xx Server Errors:</strong> Amazon or API issue\. Retry after a delay\.',
        '<strong>5xx 服务器错误：</strong> Amazon 或 API 问题。延迟后重试。'
    ),
    # Rate Limiting
    (
        r'Even with an enterprise API, respecting limits is good citizenship and ensures stability\. Use the <code[^>]*>bucket token</code> algorithm or simple fixed-window counters to manage your request rate locally\.',
        '即使使用企业级 API，遵守限制也是良好的公民行为并能确保稳定性。使用<code class="text-accent-cyan">令牌桶</code>算法或简单的固定窗口计数器在本地管理您的请求速率。'
    ),
    # Performance Optimization
    (
        r'To get maximum throughput:',
        '为了获得最大吞吐量：'
    ),
    (
        r'<strong>Keep Connections Alive:</strong> Use sessions to reuse TCP connections',
        '<strong>保持连接存活：</strong> 使用会话以重用 TCP 连接'
    ),
    (
        r'<strong>Async I/O:</strong> Use asynchronous libraries like <code[^>]*>aiohttp</code> for non-blocking operations',
        '<strong>异步 I/O：</strong> 对于非阻塞操作，使用像 <code class="text-accent-cyan">aiohttp</code> 这样的异步库'
    ),
    (
        r'<strong>Minimal Headers:</strong> Send only necessary headers to reduce bandwidth',
        '<strong>最小标头：</strong> 仅发送必要的标头以减少带宽'
    ),
    # Conclusion
    (
        r'Building a high-performance Amazon scraper requires more than just code; it requires architectural thinking\. By implementing these best practices—validation, error handling, and concurrency—you can build a system that is reliable and scalable\.',
        '构建高性能 Amazon 抓取工具不仅仅需要代码；它需要架构思维。通过实施这些最佳实践——验证、错误处理和并发——您可以构建一个可靠且可扩展的系统。'
    ),
]

for pattern, replacement in translations:
    if '\\' not in pattern:
        content = content.replace(pattern.replace('\\', ''), replacement)
    else:
        content = re.sub(pattern, replacement, content)

print("✅ 翻译完成")

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)
