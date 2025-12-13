#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量翻译所有文章的正文内容
包括章节标题、关键短语等
"""

import re

# 每篇文章的章节标题配置
articles_sections = {
    'advanced-amazon-data-extraction-best-practices.html': {
        'h2_h3': {
            'Introduction to Advanced Amazon Data Extraction': 'Amazon 数据提取高级技术简介',
            'Understanding Amazon API Architecture': '理解 Amazon API 架构',
            'Advanced Extraction Techniques': '高级提取技术',
            'Batch Processing': '批量处理',
            'Parallel Requests': '并行请求',
            'Data Validation': '数据验证',
            'Error Handling Strategies': '错误处理策略',
            'Rate Limiting Best Practices': '速率限制最佳实践',
            'Performance Optimization': '性能优化',
            'Caching Strategies': '缓存策略',
            'Data Storage': '数据存储',
            'Monitoring and Logging': '监控和日志',
            'Security Best Practices': '安全最佳实践',
            'Conclusion': '总结',
        }
    },
    'amazon-product-selection-api-data.html': {
        'h2_h3': {
            'Why Data-Driven Product Selection Matters': '为什么数据驱动的产品选择很重要',
            'Understanding Market Dynamics': '理解市场动态',
            'Key Metrics for Product Selection': '产品选择的关键指标',
            'Sales Velocity': '销售速度',
            'Competition Analysis': '竞争分析',
            'Profit Margins': '利润率',
            'Market Trends': '市场趋势',
            'Using Amazon API for Product Research': '使用 Amazon API 进行产品研究',
            'Category Analysis': '类别分析',
            'Competitor Tracking': '竞争对手跟踪',
            'Review Analysis': '评论分析',
            'Building a Product Selection System': '构建产品选择系统',
            'Data Collection': '数据收集',
            'Analysis Framework': '分析框架',
            'Decision Making': '决策制定',
            'Case Studies': '案例研究',
            'Conclusion': '总结',
        }
    },
    'amazon-sponsored-products-ad-monitoring.html': {
        'h2_h3': {
            'Understanding Amazon Sponsored Products': '了解 Amazon 赞助产品',
            'Why Monitor Competitor Ads': '为什么要监控竞争对手广告',
            'Amazon SERP API Overview': 'Amazon SERP API 概述',
            'Setting Up Ad Monitoring': '设置广告监控',
            'Tracking Sponsored Placements': '跟踪赞助投放',
            'Keyword Analysis': '关键词分析',
            'Ad Position Tracking': '广告位置跟踪',
            'Competitor Strategy Analysis': '竞争对手策略分析',
            'Bid Estimation': '出价估算',
            'Ad Copy Analysis': '广告文案分析',
            'Optimizing Your PPC Campaigns': '优化您的 PPC 广告活动',
            'Budget Allocation': '预算分配',
            'Keyword Strategy': '关键词策略',
            'Performance Metrics': '性能指标',
            'Automation and Alerts': '自动化和提醒',
            'Conclusion': '总结',
        }
    },
    'amazon-price-monitoring-system.html': {
        'h2_h3': {
            'Why Price Monitoring Matters': '为什么价格监控很重要',
            'System Architecture': '系统架构',
            'Components Overview': '组件概述',
            'Data Flow': '数据流',
            'Setting Up the Environment': '设置环境',
            'Prerequisites': '前置条件',
            'Installation': '安装',
            'Building the Price Tracker': '构建价格跟踪器',
            'Data Collection': '数据收集',
            'Price Comparison': '价格比较',
            'Alert System': '提醒系统',
            'Database Design': '数据库设计',
            'Schema Design': '架构设计',
            'Optimization': '优化',
            'Advanced Features': '高级功能',
            'Historical Analysis': '历史分析',
            'Competitor Tracking': '竞争对手跟踪',
            'Deployment and Scaling': '部署和扩展',
            'Conclusion': '总结',
        }
    },
    'amazon-business-case-studies.html': {
        'h2_h3': {
            'Introduction': '简介',
            'Case Study 1: E-commerce Startup': '案例研究 1：电商创业公司',
            'The Challenge': '挑战',
            'The Solution': '解决方案',
            'Results': '结果',
            'Case Study 2: Established Seller': '案例研究 2：成熟卖家',
            'Case Study 3: Market Expansion': '案例研究 3：市场扩张',
            'Case Study 4: Price Optimization': '案例研究 4：价格优化',
            'Key Takeaways': '关键要点',
            'Common Success Factors': '共同成功因素',
            'Lessons Learned': '经验教训',
            'Implementation Guide': '实施指南',
            'Getting Started': '开始使用',
            'Best Practices': '最佳实践',
            'Conclusion': '总结',
        }
    },
}

# 通用翻译（适用于所有文章）
common_translations = {
    'Copy Code': '复制代码',
    'Copied!': '已复制！',
    'Try It Now': '立即试用',
    'Learn More': '了解更多',
    'View Full Documentation': '查看完整文档',
    'View Documentation': '查看文档',
    'Get Started': '开始使用',
    'Read More': '阅读更多',
    'Next Steps': '下一步',
    'Prerequisites': '前置条件',
    'Example': '示例',
    'Note': '注意',
    'Warning': '警告',
    'Tip': '提示',
    'Important': '重要',
}

print("🚀 批量翻译所有文章正文...")
print("=" * 60)

success_count = 0

for filename, config in articles_sections.items():
    print(f"\n📝 翻译: {filename}")
    
    try:
        # 读取文件
        with open(f'zh/articles/{filename}', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 翻译章节标题
        for en, zh in config['h2_h3'].items():
            section_id = en.lower().replace(" ", "-").replace(":", "").replace("'", "")
            
            # H2 标题
            content = re.sub(
                f'<h2[^>]*>{re.escape(en)}</h2>',
                f'<h2 id="{section_id}">{zh}</h2>',
                content
            )
            # H3 标题
            content = re.sub(
                f'<h3[^>]*>{re.escape(en)}</h3>',
                f'<h3 id="{section_id}">{zh}</h3>',
                content
            )
            # 链接文本
            content = re.sub(
                f'>{re.escape(en)}<',
                f'>{zh}<',
                content
            )
        
        print("  ✅ 章节标题")
        
        # 通用翻译
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
print(f"✅ 批量翻译完成！成功处理 {success_count}/{len(articles_sections)} 篇文章")
print("\n已翻译:")
print("  ✅ 所有章节标题 (H2, H3)")
print("  ✅ 侧边栏目录")
print("  ✅ 通用UI元素")
print("  ✅ 按钮和链接")
