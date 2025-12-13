#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量翻译所有6篇文章的关键内容
包括 SEO、标题、摘要、章节标题、侧边栏等
"""

import re

# 定义所有文章及其翻译内容
articles_config = {
    'getting-started-amazon-scraping-api.html': {
        'title': 'Amazon 数据抓取 API 产品数据提取入门指南 | Pangolin 博客',
        'description': '学习如何使用 Pangol Info 的 Amazon 数据抓取 API 提取产品数据、价格和评论。完整的入门指南，包含代码示例和最佳实践。',
        'keywords': 'Amazon API, 数据抓取, 产品数据提取, Amazon 爬虫, 电商数据, API 教程',
        'h1': 'Amazon 数据抓取 API 产品数据提取入门指南',
        'intro': '学习如何使用 Pangol Info 的 Amazon 数据抓取 API 从 Amazon 市场提取全面的产品数据、价格和评论信息。本指南将带您了解从身份验证到高级数据提取的完整流程，包含实用代码示例和最佳实践。',
    },
    'advanced-amazon-data-extraction-best-practices.html': {
        'title': 'Amazon 数据提取高级最佳实践：电商智能优化指南 | Pangolin 博客',
        'description': '掌握 Amazon 数据提取的高级技术、速率限制、错误处理和性能优化。专业的最佳实践指南，助您构建高效稳定的数据抓取系统。',
        'keywords': 'Amazon 数据提取, 最佳实践, API 优化, 速率限制, 错误处理, 电商数据',
        'h1': 'Amazon 数据提取高级最佳实践：电商智能优化指南',
        'intro': '探索经过验证的 Amazon 产品数据提取、价格智能和大规模客户评论分析技术。本指南涵盖高级优化策略、错误处理机制和性能调优方法，帮助您构建企业级数据抓取解决方案。',
    },
    'amazon-product-selection-api-data.html': {
        'title': '使用 API 数据选择优质 Amazon 产品：数据驱动选品指南 | Pangolin 博客',
        'description': '通过 Amazon API 数据分析市场趋势、竞争对手和客户行为，做出明智的产品选择决策。完整的数据驱动选品策略和实战案例。',
        'keywords': 'Amazon 产品选择, 选品策略, 市场分析, 数据驱动, 竞品分析, 电商选品',
        'h1': '使用 API 数据选择优质 Amazon 产品：数据驱动选品指南',
        'intro': '通过自动化 API 提取分析市场趋势、竞争对手数据和客户行为，掌握 Amazon 产品选择技巧。学习如何利用数据洞察识别高潜力产品、评估市场机会并做出明智的选品决策。',
    },
    'amazon-sponsored-products-ad-monitoring.html': {
        'title': '使用 API 监控 Amazon 竞争对手广告活动：广告智能分析 | Pangolin 博客',
        'description': '使用 Amazon SERP API 跟踪竞争对手的赞助产品投放、广告策略和促销活动。优化您的 PPC 广告投放，提升广告 ROI。',
        'keywords': 'Amazon 广告监控, 竞品广告分析, PPC 优化, 赞助产品, 广告策略, SERP API',
        'h1': '使用 API 监控 Amazon 竞争对手广告活动：广告智能分析',
        'intro': '使用 Amazon SERP API 跟踪赞助产品投放、广告策略和促销活动。学习如何监控竞争对手的广告表现、关键词策略和出价模式，优化您自己的 PPC 广告活动以获得更高的投资回报率。',
    },
    'amazon-price-monitoring-system.html': {
        'title': '使用 API 构建实时 Amazon 价格监控系统：完整开发指南 | Pangolin 博客',
        'description': '使用 Pangol Info 的电商 API 创建自动化 Amazon 价格跟踪系统的分步指南。包含代码示例、架构设计和最佳实践。',
        'keywords': 'Amazon 价格监控, 价格跟踪系统, 自动化监控, 价格变动提醒, 电商 API',
        'h1': '使用 API 构建实时 Amazon 价格监控系统：完整开发指南',
        'intro': '使用 Pangol Info 的电商 API 创建自动化 Amazon 价格跟踪系统的分步指南。学习如何设计系统架构、实现实时价格监控、配置价格变动提醒，并优化系统性能以处理大规模产品监控。',
    },
    'amazon-business-case-studies.html': {
        'title': '通过数据驱动的产品智能扩展 Amazon 业务：成功案例研究 | Pangolin 博客',
        'description': '真实案例研究展示卖家如何利用 Amazon 数据抓取 API 实现 10 倍增长和竞争优势。学习成功企业的数据策略和实施方法。',
        'keywords': 'Amazon 案例研究, 业务增长, 数据驱动, 成功案例, 电商策略, API 应用',
        'h1': '通过数据驱动的产品智能扩展 Amazon 业务：成功案例研究',
        'intro': '真实案例研究展示卖家如何利用 Amazon 数据抓取 API 实现 10 倍增长和竞争优势。探索成功企业如何运用数据智能优化产品选择、定价策略和市场拓展，获得可持续的业务增长。',
    },
}

# 通用翻译内容
common_translations = {
    'Table of Contents': '目录',
    'On This Page': '本页内容',
    'Related Articles': '相关文章',
    'Quick Navigation': '快速导航',
    'Start Free Trial': '开始免费试用',
    'View API Documentation': '查看 API 文档',
    'View Documentation': '查看文档',
    'Get Started': '开始使用',
    'Learn More': '了解更多',
    'Read More': '阅读更多',
    'Try It Now': '立即试用',
    'Get 1,000 free API credits and start building today': '获取 1,000 个免费 API 积分，立即开始构建',
    'Ready to Start Extracting Amazon Data?': '准备开始提取 Amazon 数据了吗？',
    'Ready to Get Started?': '准备开始了吗？',
    'Professional Amazon & e-commerce data extraction API': 'Amazon 和电商数据提取专业 API',
    'Zero-code Amazon product tracking with automated price': '零代码 Amazon 产品跟踪，支持自动化价格',
}

print("🚀 批量翻译所有文章...")
print("=" * 60)

success_count = 0

for filename, config in articles_config.items():
    print(f"\n📝 翻译: {filename}")
    
    try:
        # 读取文件
        with open(f'zh/articles/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. SEO 元数据
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{config["title"]}</title>',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'<meta name="description" content="[^"]*"',
            f'<meta name="description" content="{config["description"]}"',
            content
        )
        
        content = re.sub(
            r'<meta name="keywords" content="[^"]*"',
            f'<meta name="keywords" content="{config["keywords"]}"',
            content
        )
        
        print("  ✅ SEO 元数据")
        
        # 2. H1 标题
        content = re.sub(
            r'<h1 class="text-4xl[^>]*>.*?</h1>',
            f'<h1 class="text-4xl md:text-6xl font-black mb-6 leading-tight">{config["h1"]}</h1>',
            content,
            flags=re.DOTALL
        )
        
        print("  ✅ 主标题")
        
        # 3. 文章摘要
        content = re.sub(
            r'(<p class="text-xl text-gray-400[^>]*>).*?(</p>)',
            f'\\1{config["intro"]}\\2',
            content,
            count=1,
            flags=re.DOTALL
        )
        
        print("  ✅ 文章摘要")
        
        # 4. 通用翻译
        for en, zh in common_translations.items():
            content = content.replace(en, zh)
        
        print("  ✅ 通用内容")
        
        # 保存
        with open(f'zh/articles/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        
        success_count += 1
        print(f"  ✅ 完成")
        
    except Exception as e:
        print(f"  ❌ 错误: {e}")

print("\n" + "=" * 60)
print(f"✅ 批量翻译完成！成功处理 {success_count}/{len(articles_config)} 篇文章")
print("\n已翻译内容:")
print("  ✅ SEO 元数据（标题、描述、关键词）")
print("  ✅ 文章主标题 (H1)")
print("  ✅ 文章摘要")
print("  ✅ 通用 UI 元素（按钮、链接等）")
print("\n⚠️  注意: 章节标题和正文段落需要针对每篇文章单独翻译")
