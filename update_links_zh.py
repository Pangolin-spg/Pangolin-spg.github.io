
import os
import glob

# 映射列表 (按长度从长到短排序，防止前缀替换错误)
# Key: 原英文/旧链接
# Value: 新中文链接
replacements = [
    # --- 特定 API 文档 (最长，最具体) ---
    ("https://docs.pangolinfo.com/en-api-reference/amazonApi/amazonScrapeAPI", "https://docs.pangolinfo.com/cn-api-reference/amazonApi/amazonScrapeAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/amazonApi/amazonAsyncAPI", "https://docs.pangolinfo.com/cn-api-reference/amazonApi/amazonAsyncAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/universalApi/universalApi", "https://docs.pangolinfo.com/cn-api-reference/universalApi/universalApi"),
    ("https://docs.pangolinfo.com/en-api-reference/serpApi/serpAPI", "https://docs.pangolinfo.com/cn-api-reference/serpApi/serpAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/serpApi/serpAsyncAPI", "https://docs.pangolinfo.com/cn-api-reference/serpApi/serpAsyncAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/serpApi/serpBatchAsyncAPI", "https://docs.pangolinfo.com/cn-api-reference/serpApi/serpBatchAsyncAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/aiModeSerpApi/aiModeSerpAPI", "https://docs.pangolinfo.com/cn-api-reference/aiModeSerpApi/aiModeSerpAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/trendsApi/keywordTrendsAPI", "https://docs.pangolinfo.com/cn-api-reference/trendsApi/keywordTrendsAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/mapDataApi/mapDataAPI", "https://docs.pangolinfo.com/cn-api-reference/mapDataApi/mapDataAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/mapDataApi/mapDataBatchAPI", "https://docs.pangolinfo.com/cn-api-reference/mapDataApi/mapDataBatchAPI"),
    ("https://docs.pangolinfo.com/en-api-reference/wipoApi/wipoAPI", "https://docs.pangolinfo.com/cn-api-reference/wipoApi/wipoAPI"),
    
    # --- 落地页与产品页 ---
    ("https://www.pangolinfo.com/pangolin-scrape-api-professional-web-data-crawling-service/", "https://www.pangolinfo.com/zh/anonymous-data-scraping-service/"),
    ("https://www.pangolinfo.com/pangolin-scrapeapi-empower-your-ai-with-the-amazon-data-scraping-api/", "https://www.pangolinfo.com/zh/amazon-api-cn/"),
    ("https://www.pangolinfo.com/amz-data-tracker/", "https://www.pangolinfo.com/zh/amz-data-tracker-2/"),
    
    # --- 定价 ---
    ("https://www.pangolinfo.com/scrape-api-pricing-2/", "https://www.pangolinfo.com/zh/scrape-api-pricing/"),
    
    # --- 案例研究 (需要在导航和页脚中检查) ---
    # 有时可能是 /index.html#use-cases 或 /case-studies/
    # 这里我们添加一个通用的替换，如果找不到特定的英文URL可能需要根据上下文人工检查
    # 如果原始文件中有指向案例的英文落地页链接，应该在这里添加
    
    # --- 通用文档首页 ---
    ("https://docs.pangolinfo.com/en-index", "https://docs.pangolinfo.com/cn-index"),
    ("https://docs.pangolinfo.com/index.html", "https://docs.pangolinfo.com/cn-index"),

    # --- 官网首页 (最短，放在最后) ---
    # 注意: 这里的替换要非常小心，避免替换掉上面长链接的前缀
    # 因为我们是按顺序执行 replace，所以执行到这里时，上面的长链接已经被替换为中文链接了。
    # 中文链接也包含 pangolinfo.com，所以我们只替换完全匹配英文首页的引用
    # 策略：如果是 href="https://www.pangolinfo.com/" 这种形式
    ('href="https://www.pangolinfo.com/"', 'href="https://www.pangolinfo.com/zh/home/"'),
    ('href="https://www.pangolinfo.com"', 'href="https://www.pangolinfo.com/zh/home/"'),
]

# 所有的中文 HTML 页面
files = glob.glob('zh/**/*.html', recursive=True)

for filepath in files:
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for en_link, zh_link in replacements:
        if en_link in content:
            print(f"  Replacing {en_link} -> {zh_link}")
            content = content.replace(en_link, zh_link)
            
    # 特别处理：案例研究链接
    # 用户给的是: https://www.pangolinfo.com/zh/scrape-api-case-studies/
    # 我们之前的导航栏可能用的是 /zh/index.html#use-cases 或类似的锚点
    # 用户请求中提到"用户案例中文页面"，我们应该尝试替换导航栏中的"应用场景"链接
    if '/zh/index.html#use-cases' in content:
        print("  Replacing nav link #use-cases -> scrape-api-case-studies")
        # 这里决定是否替换导航栏锚点为外部链接。通常落地页链接更好。
        content = content.replace('/zh/index.html#use-cases', 'https://www.pangolinfo.com/zh/scrape-api-case-studies/')
        
    # 如果内容有变化则写入
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ Updated.")
    else:
        print("  No changes needed.")
