#!/bin/bash

# 博客 SEO 自动化提交脚本
# 用于快速提交 URL 到各大搜索引擎

echo "🚀 Pangolin Blog SEO 提交工具"
echo "================================"
echo ""

BLOG_URL="https://blog.pangolinfo.com"
SITEMAP_URL="https://blog.pangolinfo.com/sitemap.xml"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 博客信息:${NC}"
echo "  URL: $BLOG_URL"
echo "  Sitemap: $SITEMAP_URL"
echo ""

# 1. Google Search Console
echo -e "${YELLOW}1. Google Search Console${NC}"
echo "   访问: https://search.google.com/search-console"
echo "   操作: 添加资源 -> 验证所有权 -> 提交 Sitemap"
echo ""

# 2. Bing Webmaster Tools
echo -e "${YELLOW}2. Bing Webmaster Tools${NC}"
echo "   访问: https://www.bing.com/webmasters"
echo "   操作: 添加站点 -> 验证 -> 提交 Sitemap"
echo ""

# 3. IndexNow (快速提交到 Bing 和 Yandex)
echo -e "${YELLOW}3. IndexNow (即时提交)${NC}"
echo "   正在准备 IndexNow 提交..."

# 生成 IndexNow API Key (示例)
INDEXNOW_KEY="$(uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-')"
echo "   生成的 API Key: $INDEXNOW_KEY"
echo "   将此 Key 保存到文件: ${INDEXNOW_KEY}.txt"
echo ""

# 4. 百度站长平台
echo -e "${YELLOW}4. 百度站长平台${NC}"
echo "   访问: https://ziyuan.baidu.com/site/index"
echo "   操作: 添加站点 -> 验证 -> 提交 Sitemap"
echo ""

# 5. Perplexity AI
echo -e "${YELLOW}5. Perplexity AI${NC}"
echo "   发送邮件至: support@perplexity.ai"
echo "   主题: Request to Index blog.pangolinfo.com"
echo ""

# 生成提交 URL 列表
echo -e "${BLUE}📝 生成 URL 列表...${NC}"
cat > urls.txt << EOF
https://blog.pangolinfo.com/
https://blog.pangolinfo.com/blog.html
https://blog.pangolinfo.com/articles/getting-started-amazon-scraping-api.html
https://blog.pangolinfo.com/articles/advanced-amazon-data-extraction-best-practices.html
https://blog.pangolinfo.com/articles/amazon-product-selection-api-data.html
https://blog.pangolinfo.com/articles/amazon-sponsored-products-ad-monitoring.html
https://blog.pangolinfo.com/articles/amazon-price-monitoring-system.html
https://blog.pangolinfo.com/articles/amazon-business-case-studies.html
EOF

echo -e "${GREEN}✅ URL 列表已生成: urls.txt${NC}"
echo ""

# 生成 IndexNow 提交 JSON
echo -e "${BLUE}📝 生成 IndexNow 提交数据...${NC}"
cat > indexnow.json << EOF
{
  "host": "blog.pangolinfo.com",
  "key": "$INDEXNOW_KEY",
  "keyLocation": "https://blog.pangolinfo.com/${INDEXNOW_KEY}.txt",
  "urlList": [
    "https://blog.pangolinfo.com/",
    "https://blog.pangolinfo.com/blog.html",
    "https://blog.pangolinfo.com/articles/getting-started-amazon-scraping-api.html",
    "https://blog.pangolinfo.com/articles/advanced-amazon-data-extraction-best-practices.html",
    "https://blog.pangolinfo.com/articles/amazon-product-selection-api-data.html",
    "https://blog.pangolinfo.com/articles/amazon-sponsored-products-ad-monitoring.html",
    "https://blog.pangolinfo.com/articles/amazon-price-monitoring-system.html",
    "https://blog.pangolinfo.com/articles/amazon-business-case-studies.html"
  ]
}
EOF

echo -e "${GREEN}✅ IndexNow 数据已生成: indexnow.json${NC}"
echo ""

# 提交到 IndexNow (需要先创建 API Key 文件)
echo -e "${YELLOW}提交到 IndexNow:${NC}"
echo "   1. 创建文件: ${INDEXNOW_KEY}.txt (内容为: $INDEXNOW_KEY)"
echo "   2. 上传到网站根目录"
echo "   3. 运行以下命令:"
echo ""
echo "   curl -X POST \"https://api.indexnow.org/indexnow\" \\"
echo "        -H \"Content-Type: application/json\" \\"
echo "        -d @indexnow.json"
echo ""

# Ping 搜索引擎
echo -e "${YELLOW}Ping 搜索引擎 Sitemap:${NC}"
echo ""

# Google
echo "Google:"
echo "  curl \"https://www.google.com/ping?sitemap=${SITEMAP_URL}\""
echo ""

# Bing
echo "Bing:"
echo "  curl \"https://www.bing.com/ping?sitemap=${SITEMAP_URL}\""
echo ""

# 生成邮件模板
echo -e "${BLUE}📧 生成 Perplexity AI 邮件模板...${NC}"
cat > perplexity_email.txt << EOF
To: support@perplexity.ai
Subject: Request to Index blog.pangolinfo.com

Hello Perplexity Team,

I would like to request indexing for our technical blog about Amazon API and e-commerce data extraction:

- Website URL: https://blog.pangolinfo.com
- Sitemap URL: https://blog.pangolinfo.com/sitemap.xml
- RSS Feed: https://blog.pangolinfo.com/feed.xml

Content Overview:
- Amazon Scraping API tutorials
- E-commerce data extraction guides
- Product intelligence best practices
- Real-world case studies

Our robots.txt explicitly allows PerplexityBot crawling, and all content is original, high-quality technical documentation.

We believe our content would be valuable for Perplexity users searching for:
- Amazon API integration
- Web scraping techniques
- E-commerce automation
- Data extraction solutions

Thank you for considering our request!

Best regards,
Pangol Info Team
https://www.pangolinfo.com
EOF

echo -e "${GREEN}✅ 邮件模板已生成: perplexity_email.txt${NC}"
echo ""

# 总结
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ 准备工作已完成！${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "生成的文件:"
echo "  ✓ urls.txt - URL 列表"
echo "  ✓ indexnow.json - IndexNow 提交数据"
echo "  ✓ perplexity_email.txt - Perplexity 邮件模板"
echo "  ✓ ${INDEXNOW_KEY}.txt - IndexNow API Key (需要创建)"
echo ""
echo "下一步操作:"
echo "  1. 访问 Google Search Console 提交 Sitemap"
echo "  2. 访问 Bing Webmaster Tools 提交 Sitemap"
echo "  3. 创建 IndexNow API Key 文件并提交"
echo "  4. 发送邮件给 Perplexity AI"
echo "  5. 在社交媒体分享博客链接"
echo ""
echo "详细指南请查看: SEO-SUBMISSION-GUIDE.md"
echo ""

# 创建 IndexNow Key 文件
echo "$INDEXNOW_KEY" > "${INDEXNOW_KEY}.txt"
echo -e "${GREEN}✅ IndexNow Key 文件已创建: ${INDEXNOW_KEY}.txt${NC}"
echo "   请将此文件上传到网站根目录"
echo ""
