#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译剩余 4 篇文章的正文段落
"""

import re
import os

files_to_translate = {
    'zh/articles/amazon-product-selection-api-data.html': [
        (r'In the vast Amazon marketplace, selecting the right product to sell is often the difference between success and failure.', '在广阔的 Amazon 市场中，选择合适的产品进行销售往往决定了成败。'),
        (r'Making decisions based on gut feeling or limited data is risky.', '凭直觉或有限数据做决定是有风险的。'),
        (r'In this guide, we\'ll show you how to leverage', '在本指南中，我们将向您展示如何利用'),
        (r'This approach minimizes risk', '这种方法将风险降至最低'),
        (r'Understanding Market Dynamics', '了解市场动态'),
        (r'Key Metrics for Product Selection', '产品选择的关键指标'),
        (r'Sales Velocity', '销售速度'),
        (r'Competition Analysis', '竞争分析'),
        (r'Profit Margins', '利润率'),
        (r'Market Trends', '市场趋势'),
        (r'Using Amazon API for Product Research', '使用 Amazon API 进行产品研究'),
        (r'Category Analysis', '类别分析'),
        (r'Competitor Tracking', '竞争对手跟踪'),
        (r'Review Analysis', '评论分析'),
        (r'Building a Product Selection System', '构建产品选择系统'),
        (r'Data Collection', '数据收集'),
        (r'Analysis Framework', '分析框架'),
        (r'Decision Making', '决策制定'),
        (r'Case Studies', '案例研究'),
        (r'Conclusion', '总结'),
        # 正文补充
        (r'Successful sellers use data to identify high-demand, low-competition niches.', '成功的卖家使用数据来识别高需求、低竞争的利基市场。'),
        (r'By analyzing sales rank (BSR), price history, and review growth', '通过分析销售排名 (BSR)、价格历史和评论增长'),
        (r'Estimating monthly sales is crucial.', '估算月销售额至关重要。'),
        (r'Identify how many other sellers are on the listing.', '识别 listing 上有多少其他卖家。'),
        (r'Calculate potential fees and costs.', '计算潜在的费用和成本。'),
        (r'Spot seasonal trends and long-term demand.', '发现季节性趋势和长期需求。'),
    ],
    'zh/articles/amazon-sponsored-products-ad-monitoring.html': [
        (r'Amazon Sponsored Products are a primary driver of visibility and sales.', 'Amazon 赞助产品是知名度和销量的主要驱动力。'),
        (r'However, without visibility into your competitors\' strategies', '然而，如果不了解竞争对手的策略'),
        (r'In this article, we\'ll explore how to use the Amazon SERP API', '在本文中，我们将探讨如何使用 Amazon SERP API'),
        (r'optimizing your own campaigns for maximum ROI', '优化您自己的广告活动以获得最大投资回报率'),
        (r'Understanding Amazon Sponsored Products', '了解 Amazon 赞助产品'),
        (r'Why Monitor Competitor Ads', '为什么要监控竞争对手广告'),
        (r'Amazon SERP API Overview', 'Amazon SERP API 概述'),
        (r'Setting Up Ad Monitoring', '设置广告监控'),
        (r'Tracking Sponsored Placements', '跟踪赞助投放'),
        (r'Keyword Analysis', '关键词分析'),
        (r'Ad Position Tracking', '广告位置跟踪'),
        (r'Competitor Strategy Analysis', '竞争对手策略分析'),
        (r'Bid Estimation', '出价估算'),
        (r'Ad Copy Analysis', '广告文案分析'),
        (r'Optimizing Your PPC Campaigns', '优化您的 PPC 广告活动'),
    ],
    'zh/articles/amazon-price-monitoring-system.html': [
        (r'Price is one of the most significant factors influencing buying decisions on Amazon.', '价格是影响 Amazon 购买决策的最重要因素之一。'),
        (r'In this technical guide, we will build a robust price monitoring system', '在这份技术指南中，我们将构建一个稳健的价格监控系统'),
        (r'using Python and Pangol Info\'s API', '使用 Python 和 Pangol Info 的 API'),
        (r'Why Price Monitoring Matters', '为什么价格监控很重要'),
        (r'System Architecture', '系统架构'),
        (r'Components Overview', '组件概述'),
        (r'Data Flow', '数据流'),
        (r'Setting Up the Environment', '设置环境'),
        (r'Prerequisites', '前置条件'),
        (r'Installation', '安装'),
        (r'Building the Price Tracker', '构建价格跟踪器'),
        (r'Data Collection', '数据收集'),
        (r'Price Comparison', '价格比较'),
        (r'Alert System', '提醒系统'),
        (r'Database Design', '数据库设计'),
    ],
    'zh/articles/amazon-business-case-studies.html': [
        (r'Theory is good, but real-world results are better.', '理论虽好，但现实世界的结果更佳。'),
        (r'In this collection of case studies', '在这个案例研究集中'),
        (r'we showcase how diverse businesses', '我们展示了各种企业如何'),
        (r'Introduction', '简介'),
        (r'Case Study 1: E-commerce Startup', '案例研究 1：电商创业公司'),
        (r'The Challenge', '挑战'),
        (r'The Solution', '解决方案'),
        (r'Results', '结果'),
        (r'Case Study 2: Established Seller', '案例研究 2：成熟卖家'),
        (r'Case Study 3: Market Expansion', '案例研究 3：市场扩张'),
        (r'Case Study 4: Price Optimization', '案例研究 4：价格优化'),
        (r'Key Takeaways', '关键要点'),
    ]
}

print("🚀 正在翻译剩余文章的正文...")

for filepath, replacements in files_to_translate.items():
    if not os.path.exists(filepath):
        print(f"❌ 文件未找到: {filepath}")
        continue
        
    print(f"📝 处理: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for eng, ch in replacements:
        # 允许空格差异
        pattern = re.escape(eng).replace(r'\ ', r'\s+')
        content = re.sub(pattern, ch, content, flags=re.IGNORECASE | re.DOTALL)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("\n✅ 完成")
