# Amazon URL Parameter Construction: Complete Guide for Data Scraping

> Master the 14 core parameters and boost your scraping efficiency by 100x

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Table of Contents

- [What is URL Parameter Construction?](#what-is-url-parameter-construction)
- [Why Master URL Parameters?](#why-master-url-parameters)
- [Complete Parameter Reference](#complete-parameter-reference)
- [Practical Use Cases](#practical-use-cases)
- [Python Implementation](#python-implementation)
- [Common Pitfalls](#common-pitfalls)
- [Integration with Pangolin API](#integration-with-pangolin-api)
- [Advanced Techniques](#advanced-techniques)
- [Contributing](#contributing)
- [License](#license)

## What is URL Parameter Construction?

Amazon URL parameter construction is the process of programmatically building complete page access links according to Amazon's official URL structure rules. This technique is fundamental to e-commerce data scraping, allowing developers to generate precise URLs for target pages without manual navigation.

**A standard Amazon URL consists of three components:**

```
https://www.amazon.com/s?k=laptop&i=computers&low-price=5000&high-price=20000&page=1
│      │              │ │ │      │          │         │           │        │
│      │              │ │ └──────┴─────────┴─────────┴───────────┴────────┘
│      │              │ │                  Query Parameters
│      │              │ └─ Path
│      │              └─── Domain
│      └──────────────────── Protocol
```

## Why Master URL Parameters?

### 🚀 100x Efficiency Boost

Transform 1,000 manual operations into a single automated loop:

| Scenario | Manual | Automated | Improvement |
|----------|--------|-----------|-------------|
| Single keyword search | 1 operation | 1 line of code | Equal |
| 100 keywords × 10 price ranges | 1,000 operations | 1 loop | **1000x** |
| Multi-page scraping | Click through pages | Batch URL generation | **100x** |

### 💰 Cost Reduction

- **Precise requests**: Correct URL parameters ensure accurate data in one request
- **Reduced API calls**: Avoid repeated requests due to parameter errors
- **Lower operational costs**: Automate what would require manual labor

### 🎯 Precise Data Control

- Specify zip code for regional pricing
- Filter by exact price ranges
- Sort by sales, rating, or price
- Combine complex conditions (4+ stars + Prime + price range)

## Complete Parameter Reference

Here are the **14 core parameters** every developer should know:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `k` | Search Control | Search keyword, supports multi-word | `wireless+headphones` |
| `i` | Search Control | Category ID, limits search scope | `electronics`, `aps` (all) |
| `rh` | Filter Conditions | Composite filter (brand, rating, Prime) | `p_72:1249150011` (4+ stars) |
| `low-price` | Filter Conditions | Minimum price (cents in most categories) | `5000` (=$50.00) |
| `high-price` | Filter Conditions | Maximum price (cents in most categories) | `20000` (=$200.00) |
| `s` | Sorting Method | Result sorting rules | `price-asc-rank` (price ↑) |
| `page` | Pagination Control | Page number (usually max 20 pages) | `1`, `2`, `3`...`20` |
| `ref` | Tracking Identifier | Source tracking, simulates real user | `sr_pg_1`, `nb_sb_noss` |
| `qid` | Tracking Identifier | Query timestamp | `1702284567` |
| `node` | Category Navigation | Category node ID for bestsellers | `172282` (Electronics) |
| `field-keywords` | Search Control | Keyword (legacy parameter) | `laptop` |
| `bbn` | Category Navigation | Browse Bin Number | `172282` |
| `ie` | Encoding Setting | Character encoding | `UTF8` |
| `tag` | Affiliate Identifier | Amazon Associates ID | `youraffid-20` |

### ⚠️ Critical Notes

- 💰 **Price parameters use cents**: `$50` = `5000`, `$200` = `20000`
- 🔤 **Encode spaces**: Use `+` or `%20`
- 📄 **20-page limit**: Use price segmentation to bypass
- 🌍 **Different sites**: `.com`, `.co.uk`, `.co.jp` may have different category IDs

## Practical Use Cases

### Case 1: Basic Search

**Requirement**: Scrape "wireless headphones" in Electronics category

```python
# URL Construction
url = "https://www.amazon.com/s?k=wireless+headphones&i=electronics&ref=nb_sb_noss"
```

**Using Pangolin Scrape API**:

```python
import requests

response = requests.post('https://api.pangolinfo.com/scrape', json={
    'url': url,
    'type': 'search',
    'format': 'json'
})
data = response.json()
print(f"Found {len(data.get('products', []))} products")
```

### Case 2: Price Filtering

**Requirement**: Scrape Bluetooth speakers priced $50-$200, sorted by price ascending

```python
from urllib.parse import urlencode

params = {
    'k': 'bluetooth speaker',
    'i': 'electronics',
    'low-price': 5000,    # $50 in cents
    'high-price': 20000,  # $200 in cents
    's': 'price-asc-rank'
}

url = f"https://www.amazon.com/s?{urlencode(params)}"
# Result: https://www.amazon.com/s?k=bluetooth+speaker&i=electronics&low-price=5000&high-price=20000&s=price-asc-rank
```

### Case 3: Bestseller List

**Requirement**: Get Electronics category Best Sellers

```python
# Bestseller URL structure differs from search pages
url = "https://www.amazon.com/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0"
```

### Case 4: Multi-Page Scraping

**Requirement**: Scrape first 5 pages of "laptop" results

```python
base_url = "https://www.amazon.com/s"
keyword = "laptop"

for page in range(1, 6):
    url = f"{base_url}?k={keyword}&page={page}&ref=sr_pg_{page}"
    print(f"Page {page}: {url}")
    # Send to API for scraping
```

### Case 5: Complex Filtering

**Requirement**: Laptops with 4+ stars, Prime badge, priced $100-$500

```python
params = {
    'k': 'laptop',
    'i': 'computers',
    'rh': 'p_72:1249150011,p_85:2470955011',  # 4+ stars + Prime
    'low-price': 10000,
    'high-price': 50000
}

url = f"https://www.amazon.com/s?{urlencode(params)}"
```

**rh Parameter Breakdown**:
- `p_72:1249150011` = 4+ stars rating
- `p_85:2470955011` = Prime products
- Multiple conditions connected by commas

## Python Implementation

### Basic URL Builder Class

```python
from urllib.parse import urlencode, quote_plus
from typing import Optional

class AmazonURLBuilder:
    """Amazon URL Builder for automated scraping"""
    
    BASE_URLS = {
        'us': 'https://www.amazon.com',
        'uk': 'https://www.amazon.co.uk',
        'jp': 'https://www.amazon.co.jp',
        'de': 'https://www.amazon.de',
        'ca': 'https://www.amazon.ca'
    }
    
    SORT_OPTIONS = {
        'relevance': 'relevanceblender',
        'price_asc': 'price-asc-rank',
        'price_desc': 'price-desc-rank',
        'review': 'review-rank',
        'newest': 'date-desc-rank'
    }
    
    def __init__(self, marketplace: str = 'us'):
        """
        Initialize URL builder
        
        Args:
            marketplace: Marketplace code (us, uk, jp, de, ca)
        """
        self.base_url = self.BASE_URLS.get(marketplace, self.BASE_URLS['us'])
        self.marketplace = marketplace
    
    def build_search_url(
        self,
        keyword: str,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = 'relevance',
        page: int = 1,
        prime_only: bool = False,
        min_rating: Optional[int] = None
    ) -> str:
        """
        Build search URL with parameters
        
        Args:
            keyword: Search keyword
            category: Category ID (e.g., 'electronics', 'books')
            min_price: Minimum price in dollars
            max_price: Maximum price in dollars
            sort_by: Sorting method
            page: Page number
            prime_only: Filter Prime products only
            min_rating: Minimum rating (4 or 5)
        
        Returns:
            Complete search URL
        """
        params = {
            'k': keyword,
            's': self.SORT_OPTIONS.get(sort_by, sort_by),
            'page': page,
            'ref': f'sr_pg_{page}'
        }
        
        if category:
            params['i'] = category
        
        # Convert price to cents
        if min_price is not None:
            params['low-price'] = int(min_price * 100)
        if max_price is not None:
            params['high-price'] = int(max_price * 100)
        
        # Composite filter conditions
        rh_parts = []
        if prime_only:
            rh_parts.append('p_85:2470955011')
        if min_rating == 4:
            rh_parts.append('p_72:1249150011')
        elif min_rating == 5:
            rh_parts.append('p_72:1249137011')
        
        if rh_parts:
            params['rh'] = ','.join(rh_parts)
        
        query_string = urlencode(params, quote_via=quote_plus)
        return f"{self.base_url}/s?{query_string}"
    
    def build_bestseller_url(self, category: str, page: int = 1) -> str:
        """
        Build Best Sellers list URL
        
        Args:
            category: Category name (e.g., 'electronics', 'books')
            page: Page number
        
        Returns:
            Bestseller URL
        """
        if page == 1:
            return f"{self.base_url}/gp/bestsellers/{category}"
        else:
            return f"{self.base_url}/gp/bestsellers/{category}/ref=zg_bs_pg_{page}?ie=UTF8&pg={page}"
    
    def build_product_url(self, asin: str) -> str:
        """
        Build product detail page URL
        
        Args:
            asin: Product ASIN code
        
        Returns:
            Product detail page URL
        """
        return f"{self.base_url}/dp/{asin}"
```

### Usage Examples

```python
# Initialize builder
builder = AmazonURLBuilder(marketplace='us')

# Example 1: Basic search
url1 = builder.build_search_url(
    keyword='wireless headphones',
    category='electronics'
)
print("Basic search:", url1)

# Example 2: With price filtering and sorting
url2 = builder.build_search_url(
    keyword='laptop',
    category='computers',
    min_price=500,
    max_price=1500,
    sort_by='price_asc',
    page=1
)
print("Price filtering:", url2)

# Example 3: Prime products with high rating
url3 = builder.build_search_url(
    keyword='bluetooth speaker',
    prime_only=True,
    min_rating=4,
    sort_by='review'
)
print("Prime + high rating:", url3)

# Example 4: Bestseller URL
url4 = builder.build_bestseller_url(category='electronics', page=2)
print("Bestseller page:", url4)
```

## Common Pitfalls

### ❌ Mistake 1: Wrong Price Unit

```python
# ❌ Wrong - will be interpreted as $0.50-$2.00
params = {'low-price': 50, 'high-price': 200}

# ✅ Correct - $50-$200
params = {'low-price': 5000, 'high-price': 20000}
```

### ❌ Mistake 2: Unencoded Spaces

```python
# ❌ Wrong - will cause errors
url = "https://www.amazon.com/s?k=wireless headphones"

# ✅ Correct
url = "https://www.amazon.com/s?k=wireless+headphones"

# Or use proper encoding
from urllib.parse import quote_plus
url = f"https://www.amazon.com/s?k={quote_plus('wireless headphones')}"
```

### ❌ Mistake 3: Ignoring 20-Page Limit

**Problem**: Amazon search shows max 20 pages

**Solution**: Price segmentation strategy

```python
price_ranges = [(0, 50), (50, 100), (100, 200), (200, 500)]

for min_p, max_p in price_ranges:
    for page in range(1, 21):  # 20 pages per price segment
        url = builder.build_search_url(
            'laptop',
            min_price=min_p,
            max_price=max_p,
            page=page
        )
        # Scrape data
```

## Integration with Pangolin API

### Complete Integration Example

```python
import requests
from typing import Dict, List

class PangolinScraper:
    """Pangolin API Integration Class"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = 'https://api.pangolinfo.com/scrape'
        self.url_builder = AmazonURLBuilder()
    
    def scrape_search(self, keyword: str, **kwargs) -> Dict:
        """
        Scrape search results
        
        Args:
            keyword: Search keyword
            **kwargs: Other URL parameters
        
        Returns:
            Parsed JSON data
        """
        url = self.url_builder.build_search_url(keyword, **kwargs)
        
        payload = {
            'api_key': self.api_key,
            'url': url,
            'type': 'search',
            'format': 'json'
        }
        
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def scrape_with_price_segmentation(
        self,
        keyword: str,
        category: str,
        price_ranges: List[tuple]
    ) -> List[Dict]:
        """
        Scrape using price segmentation strategy
        
        Args:
            keyword: Search keyword
            category: Category
            price_ranges: List of (min_price, max_price) tuples
        
        Returns:
            All product data
        """
        all_products = []
        
        for min_price, max_price in price_ranges:
            print(f"Scraping price range: ${min_price}-${max_price}")
            
            for page in range(1, 11):  # 10 pages per price segment
                try:
                    data = self.scrape_search(
                        keyword=keyword,
                        category=category,
                        min_price=min_price,
                        max_price=max_price,
                        page=page
                    )
                    
                    if data.get('products'):
                        all_products.extend(data['products'])
                    else:
                        break
                        
                except Exception as e:
                    print(f"Scraping failed: {e}")
                    break
        
        return all_products

# Usage
scraper = PangolinScraper(api_key='your_api_key_here')

# Price segmentation scraping
price_ranges = [(0, 50), (50, 100), (100, 200)]
products = scraper.scrape_with_price_segmentation(
    keyword='laptop',
    category='computers',
    price_ranges=price_ranges
)
print(f"Total products scraped: {len(products)}")
```

### Pangolin API Advantages

- ✅ **98% sponsored ad capture rate**
- ✅ Automatic URL parameter handling
- ✅ Supports zip code specification
- ✅ Returns structured JSON data
- ✅ Handles anti-scraping automatically

## Advanced Techniques

### 1. Batch URL Generation

```python
def generate_batch_urls(
    keywords: List[str],
    categories: List[str],
    price_ranges: List[tuple]
) -> List[Dict]:
    """Generate URLs for batch scraping"""
    builder = AmazonURLBuilder()
    urls = []
    
    for keyword in keywords:
        for category in categories:
            for min_price, max_price in price_ranges:
                for page in range(1, 21):
                    url = builder.build_search_url(
                        keyword=keyword,
                        category=category,
                        min_price=min_price,
                        max_price=max_price,
                        page=page
                    )
                    urls.append({
                        'url': url,
                        'keyword': keyword,
                        'category': category,
                        'price_range': f'${min_price}-${max_price}',
                        'page': page
                    })
    
    return urls
```

### 2. Multi-Sort Strategy

```python
def scrape_with_multiple_sorts(keyword: str, sort_methods: List[str]):
    """Scrape using multiple sorting methods"""
    builder = AmazonURLBuilder()
    
    for sort_method in sort_methods:
        for page in range(1, 11):
            url = builder.build_search_url(
                keyword=keyword,
                sort_by=sort_method,
                page=page
            )
            # Scrape data
            print(f"Scraping {sort_method}, page {page}")

# Usage
sort_methods = ['relevance', 'price_asc', 'review', 'newest']
scrape_with_multiple_sorts('bluetooth speaker', sort_methods)
```

### 3. Error Handling and Retry

```python
import time
from requests.exceptions import RequestException

def robust_scrape(url: str, max_retries: int = 3):
    """Scraping with retry mechanism"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

## Summary

Master these 3 core points:

1. **Prices use cents**: `$50` = `5000`
2. **Encode spaces**: Use `+` or `%20`
3. **Bypass limits**: Price segmentation solves 20-page limit

URL parameter construction is the foundation of efficient data scraping. Whether you build your own tools or use professional APIs like Pangolin, understanding these fundamentals is essential.

## Tools & Resources

### Professional Solutions

**For Technical Teams**: [Pangolin Scrape API](https://www.pangolinfo.com)
- Automatic URL parameter handling
- 98% sponsored ad capture rate
- Structured JSON data output

**For Non-Technical Users**: AMZ Data Tracker
- Zero-code configuration
- Visual interface
- Scheduled scraping

### Related Projects

- [Amazon Product Scraper](https://github.com/example/amazon-scraper)
- [E-commerce Data Tools](https://github.com/example/ecommerce-tools)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors
- Inspired by the e-commerce data community
- Special thanks to Pangolin API team

---

**Found this helpful? ⭐ Star this repo and share with your network!**

**Questions or suggestions?** Open an issue or reach out on [Twitter](https://twitter.com/yourhandle)

#Amazon #DataScraping #Python #EcommerceData #WebScraping #API
