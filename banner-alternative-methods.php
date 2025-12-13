/**
 * 顶部促销横幅 - 备用方案
 * 如果 wp_body_open 不工作，使用这个版本
 */

// 方案 1: 使用 wp_head（在 </head> 前加载）
add_action('wp_head', 'add_top_promo_banner_head');
function add_top_promo_banner_head() {
    // 只在英文首页显示
    if (!is_front_page()) {
        return;
    }
    
    // 检查是否是英文页面
    $current_lang = 'en';
    if (function_exists('pll_current_language')) {
        $current_lang = pll_current_language();
    }
    
    if ($current_lang !== 'en') {
        return;
    }
    
    ?>
    <script>
    // 在页面加载完成后立即添加横幅
    document.addEventListener('DOMContentLoaded', function() {
        var banner = document.createElement('div');
        banner.id = 'pangolin-top-banner';
        banner.className = 'pangolin-promo-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <span class="banner-text">
                    Discover the New Pangolin Version — Join a 30-min interview & get 
                    <strong class="highlight">50% OFF for life</strong>.
                </span>
                <button class="banner-close" aria-label="Close banner">×</button>
            </div>
        `;
        
        // 插入到 body 最前面
        if (document.body.firstChild) {
            document.body.insertBefore(banner, document.body.firstChild);
        } else {
            document.body.appendChild(banner);
        }
        
        console.log('[Banner] 横幅已通过 JavaScript 添加');
    });
    </script>
    <?php
}

// 方案 2: 使用 wp_footer（在页面底部加载，然后用 JS 移到顶部）
add_action('wp_footer', 'add_top_promo_banner_footer', 1);
function add_top_promo_banner_footer() {
    // 只在英文首页显示
    if (!is_front_page()) {
        return;
    }
    
    // 检查是否是英文页面
    $current_lang = 'en';
    if (function_exists('pll_current_language')) {
        $current_lang = pll_current_language();
    }
    
    if ($current_lang !== 'en') {
        return;
    }
    
    ?>
    <script>
    (function() {
        // 创建横幅
        var banner = document.createElement('div');
        banner.id = 'pangolin-top-banner';
        banner.className = 'pangolin-promo-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <span class="banner-text">
                    Discover the New Pangolin Version — Join a 30-min interview & get 
                    <strong class="highlight">50% OFF for life</strong>.
                </span>
                <button class="banner-close" aria-label="Close banner">×</button>
            </div>
        `;
        
        // 移到 body 最前面
        if (document.body.firstChild) {
            document.body.insertBefore(banner, document.body.firstChild);
        } else {
            document.body.appendChild(banner);
        }
        
        console.log('[Banner] 横幅已添加到页面顶部');
    })();
    </script>
    <?php
}
