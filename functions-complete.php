<?php
/**
 * ===================================================================
 * Astra Child Theme functions.php - 最终整合版 (v18 - 集成访谈Banner)
 * 新增：Pangolin 访谈优惠 Banner (固定顶部,带倒计时)
 * 新增：Polylang 语言条件支持，可在 Elementor 主题生成器中按语言显示不同模板
 * 修改1：适配 WordPress Admin Bar，登录状态下自动下移页眉防止被遮挡
 * 修改2：提高液态玻璃的透明度 (0.85 -> 0.6)，视觉更通透
 * 保留：沉浸式页眉、在线客服、视频埋点等所有功能
 * ===================================================================
 */

// 加载父主题样式
function astra_child_enqueue_styles() {
    wp_enqueue_style('astra-child-theme-css', 
        get_stylesheet_directory_uri() . '/style.css',
        array('astra-theme-css'),
        wp_get_theme()->get('Version')
    );
}
add_action('wp_enqueue_scripts', 'astra_child_enqueue_styles', 15);

/**
 * ===================================================================
 * 【新增】Pangolin 访谈优惠 Banner
 * ===================================================================
 * 功能：
 * - 固定在页面顶部的蓝紫渐变Banner
 * - 实时倒计时(天:时:分)
 * - 点击"Apply Now"触发Elementor Popup (ID: 12817)
 * - 关闭后使用localStorage记忆,不再显示
 * - 自动适配固定Header和WordPress Admin Bar
 */
add_action('wp_body_open', 'pangolin_add_interview_banner', 1);
function pangolin_add_interview_banner() {
    ?>
    <!-- Pangolin Interview Banner -->
    <style>
        .pangolin-top-banner {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #7c3aed 100%);
            color: white;
            padding: 12px 20px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            overflow: hidden;
            z-index: 99999; /* 高于Header的9999 */
        }

        .pangolin-top-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            right: 10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(124, 58, 237, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            animation: pangolinPulse 6s ease-in-out infinite;
        }

        @keyframes pangolinPulse {
            0%, 100% {
                transform: scale(1);
                opacity: 0.4;
            }
            50% {
                transform: scale(1.2);
                opacity: 0.6;
            }
        }

        .pangolin-banner-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            position: relative;
            z-index: 2;
        }

        .pangolin-banner-left {
            display: flex;
            align-items: center;
            gap: 16px;
            flex: 1;
        }

        .pangolin-banner-icon {
            font-size: 20px;
            color: #fbbf24;
            animation: pangolinBounce 2s infinite;
        }

        @keyframes pangolinBounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-4px);
            }
        }

        .pangolin-banner-text {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .pangolin-banner-message {
            font-size: 15px;
            font-weight: 600;
            line-height: 1.4;
        }

        .pangolin-highlight {
            color: #fbbf24;
            font-weight: 900;
        }

        .pangolin-badge {
            background: rgba(251, 191, 36, 0.2);
            border: 1px solid rgba(251, 191, 36, 0.4);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            color: #fbbf24;
            white-space: nowrap;
        }

        .pangolin-countdown {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 0, 0, 0.2);
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .pangolin-countdown-label {
            font-size: 12px;
            font-weight: 600;
            opacity: 0.9;
        }

        .pangolin-countdown-time {
            display: flex;
            gap: 6px;
            font-family: 'Courier New', monospace;
            font-weight: 900;
        }

        .pangolin-countdown-value {
            font-size: 16px;
            color: #fbbf24;
            min-width: 20px;
            text-align: center;
        }

        .pangolin-countdown-sep {
            color: #fbbf24;
            opacity: 0.6;
        }

        .pangolin-countdown-unit {
            font-size: 10px;
            opacity: 0.8;
        }

        .pangolin-banner-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .pangolin-cta-btn {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: #1e3a8a;
            font-size: 14px;
            font-weight: 900;
            padding: 10px 24px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .pangolin-cta-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(251, 191, 36, 0.6);
        }

        .pangolin-close-btn {
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.7);
            font-size: 20px;
            cursor: pointer;
            padding: 4px 8px;
            transition: all 0.3s ease;
        }

        .pangolin-close-btn:hover {
            color: white;
            transform: scale(1.1);
        }

        /* 适配固定Header - 为Banner留出50px空间 */
        body .ast-primary-header-bar {
            top: 50px !important;
        }

        /* 登录状态适配 - WordPress Admin Bar */
        body.admin-bar .pangolin-top-banner {
            top: 32px;
        }

        body.admin-bar .ast-primary-header-bar {
            top: 82px !important; /* 32px(admin bar) + 50px(banner) */
        }

        @media screen and (max-width: 782px) {
            body.admin-bar .pangolin-top-banner {
                top: 46px;
            }
            body.admin-bar .ast-primary-header-bar {
                top: 96px !important; /* 46px + 50px */
            }
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            .pangolin-banner-content {
                flex-direction: column;
                gap: 12px;
                text-align: center;
            }
            .pangolin-banner-left {
                flex-direction: column;
                gap: 8px;
            }
            .pangolin-banner-right {
                width: 100%;
                justify-content: center;
                flex-wrap: wrap;
            }
            .pangolin-countdown {
                order: -1;
                width: 100%;
                justify-content: center;
            }
        }
    </style>

    <div class="pangolin-top-banner" id="pangolinTopBanner">
        <div class="pangolin-banner-content">
            <div class="pangolin-banner-left">
                <i class="fas fa-sparkles pangolin-banner-icon"></i>
                <div class="pangolin-banner-text">
                    <span class="pangolin-banner-message">
                        🎉 <strong>New Version Launch:</strong> Join our interview & get <span class="pangolin-highlight">50% OFF Forever</span>
                    </span>
                    <span class="pangolin-badge">Limited to 50 Users</span>
                </div>
            </div>
            <div class="pangolin-banner-right">
                <div class="pangolin-countdown">
                    <span class="pangolin-countdown-label">Ends in:</span>
                    <div class="pangolin-countdown-time">
                        <span><span class="pangolin-countdown-value" id="pangolinDays">--</span><span class="pangolin-countdown-unit">d</span></span>
                        <span class="pangolin-countdown-sep">:</span>
                        <span><span class="pangolin-countdown-value" id="pangolinHours">--</span><span class="pangolin-countdown-unit">h</span></span>
                        <span class="pangolin-countdown-sep">:</span>
                        <span><span class="pangolin-countdown-value" id="pangolinMinutes">--</span><span class="pangolin-countdown-unit">m</span></span>
                    </div>
                </div>
                <a href="#elementor-popup-12817" class="pangolin-cta-btn">
                    Apply Now
                    <i class="fas fa-arrow-right"></i>
                </a>
                <button class="pangolin-close-btn" onclick="closeBanner()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    </div>

    <script>
    (function() {
        // 倒计时功能
        function updateCountdown() {
            const deadline = new Date('2025-12-31T23:59:59');
            const now = new Date();
            const diff = deadline - now;
            
            if (diff > 0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                
                document.getElementById('pangolinDays').textContent = String(days).padStart(2, '0');
                document.getElementById('pangolinHours').textContent = String(hours).padStart(2, '0');
                document.getElementById('pangolinMinutes').textContent = String(minutes).padStart(2, '0');
            }
        }
        
        updateCountdown();
        setInterval(updateCountdown, 60000); // 每分钟更新一次
        
        // 检查是否已关闭Banner
        if (localStorage.getItem('pangolinBannerClosed') === 'true') {
            document.getElementById('pangolinTopBanner').style.display = 'none';
            adjustHeaderPosition(true); // Banner已关闭,Header上移
        }
        
        // Elementor Popup触发功能
        document.addEventListener('DOMContentLoaded', function() {
            const applyBtn = document.querySelector('.pangolin-cta-btn');
            if (applyBtn && typeof elementorProFrontend !== 'undefined') {
                applyBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    elementorProFrontend.modules.popup.showPopup({ id: 12817 });
                });
            }
        });
    })();
    
    // 关闭Banner函数
    function closeBanner() {
        document.getElementById('pangolinTopBanner').style.display = 'none';
        localStorage.setItem('pangolinBannerClosed', 'true');
        adjustHeaderPosition(true); // 调整Header位置
    }
    
    // 动态调整Header位置
    function adjustHeaderPosition(bannerClosed) {
        const header = document.querySelector('.ast-primary-header-bar');
        const isAdminBar = document.body.classList.contains('admin-bar');
        const isMobile = window.innerWidth <= 782;
        
        if (header) {
            if (bannerClosed) {
                // Banner关闭,Header上移到顶部
                if (isAdminBar) {
                    header.style.top = (isMobile ? '46px' : '32px') + ' !important';
                } else {
                    header.style.top = '0px !important';
                }
            } else {
                // Banner显示,Header下移
                if (isAdminBar) {
                    header.style.top = (isMobile ? '96px' : '82px') + ' !important';
                } else {
                    header.style.top = '50px !important';
                }
            }
        }
    }
    </script>
    <?php
}

/**
 * ===================================================================
 * 【新增】Polylang 多语言页脚支持
 * ===================================================================
 * 使用方法：
 * 1. 在 Elementor 主题生成器中创建两个页脚模板
 * 2. 第一个页脚设置显示条件为"整个网站"（这是中文页脚）
 * 3. 第二个页脚也设置显示条件为"整个网站"（这是英文页脚）
 * 4. 在 Polylang 设置中，将这两个页脚模板关联为翻译关系
 * 5. 系统会自动根据当前页面语言显示对应的页脚
 */

// 让 Polylang 支持 Elementor 模板
function enable_polylang_for_elementor_templates($post_types, $is_settings) {
    // 添加 Elementor 的模板文章类型
    $post_types['elementor_library'] = 'elementor_library';
    return $post_types;
}
add_filter('pll_get_post_types', 'enable_polylang_for_elementor_templates', 10, 2);

// 确保 Polylang 在后台管理界面显示语言选择
function add_polylang_language_column_to_elementor($columns) {
    if (function_exists('pll_current_language')) {
        // 这将触发 Polylang 添加语言列
        return $columns;
    }
    return $columns;
}
add_filter('manage_elementor_library_posts_columns', 'add_polylang_language_column_to_elementor');

function filter_elementor_template_by_language($template_id) {
    // 检查是否为页脚模板且 Polylang 已激活
    if (!function_exists('pll_current_language') || empty($template_id)) {
        return $template_id;
    }
    
    $current_lang = pll_current_language();
    
    // 获取当前模板的语言版本（如果设置了翻译）
    if (function_exists('pll_get_post')) {
        $translated_template = pll_get_post($template_id, $current_lang);
        if ($translated_template) {
            return $translated_template;
        }
    }
    
    return $template_id;
}
add_filter('elementor/theme/get_location_templates/template_id', 'filter_elementor_template_by_language');

/**
 * 【核心修改】添加页眉滚动效果的 JS 和 CSS
 */
function add_header_scroll_script() {
    ?>
    <style>
    /* --- 基础状态：始终固定，无背景 --- */
    .ast-primary-header-bar {
        position: fixed !important; /* 强制固定在顶部 */
        top: 50px !important; /* 为Banner留出50px空间 */
        left: 0 !important;
        width: 100% !important;
        z-index: 9999;
        
        /* 初始状态：完全透明 */
        background-color: transparent !important;
        background-image: none !important;
        box-shadow: none !important;
        border: none !important;
        border-radius: 0 !important;
        
        /* 关键：只对背景属性做平滑过渡动画 (淡入淡出) */
        transition: background-color 0.5s ease, backdrop-filter 0.5s ease, box-shadow 0.5s ease, top 0.3s ease !important;
    }

    /* --- 修复：WordPress 后台管理条遮挡问题 --- */
    /* 当登录且显示管理条时，页眉下移 82px (32px admin bar + 50px banner) */
    body.admin-bar .ast-primary-header-bar {
        top: 82px !important;
    }
    /* 移动端 WordPress 管理条通常较高 (46px)，需单独适配 */
    @media screen and (max-width: 782px) {
        body.admin-bar .ast-primary-header-bar {
            top: 96px !important; /* 46px + 50px */
        }
    }

    /* --- 滚动触发状态：液态玻璃遮罩显现 --- */
    .ast-primary-header-bar.ast-header-sticked {
        /* 位置、大小完全不变，因此LOGO和菜单不会跳动 */
        
        /* 液态玻璃视觉效果：提高透明度 (0.6) + 高斯模糊 */
        background-color: rgba(255, 255, 255, 0.6) !important; 
        backdrop-filter: blur(15px); /* 保持模糊度以确保文字可读 */
        -webkit-backdrop-filter: blur(15px); /* Safari 兼容 */
        
        /* 底部增加一条极细微的玻璃边缘线 */
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
        
        /* 柔和的投影 */
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03) !important;
    }
    </style>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var header = document.querySelector('.ast-primary-header-bar');
        
        // 兼容性检查
        if (!header) {
             header = document.querySelector('.site-header');
        }

        var scrollTrigger = 10; // 滚动触发阈值

        if (header) {
            // 初始化检查
            checkScroll();

            window.addEventListener('scroll', function() {
                checkScroll();
            });

            function checkScroll() {
                var scrollY = window.scrollY || window.pageYOffset;

                if (scrollY > scrollTrigger) {
                    // 滚动中：添加淡入效果
                    header.classList.add('ast-header-sticked');
                } else {
                    // 回到顶部：恢复透明
                    header.classList.remove('ast-header-sticked');
                }
            }
        }
    });
    </script>
    <?php
}
// 添加到页面头部
add_action('wp_head', 'add_header_scroll_script');

/**
 * 加载代码块相关的脚本和样式
 */
function astra_child_enqueue_code_block_assets() {
    // 加载自定义JavaScript
    wp_enqueue_script(
        'code-block-copy',
        get_stylesheet_directory_uri() . '/js/code-block-copy.js',
        array('jquery'),
        '1.0.0',
        true
    );
}
add_action('wp_enqueue_scripts', 'astra_child_enqueue_code_block_assets');

/**
 * 处理Gutenberg编辑器的代码块（统一处理，避免重复）- 仅作用于前台
 */
function handle_gutenberg_code_blocks($block_content, $block) {
    if ( ! is_admin() && $block['blockName'] === 'core/code') { 
        if (strpos($block_content, 'copy-button') !== false) {
            return $block_content;
        }
        $code_text = strip_tags($block_content);
        $code_text = html_entity_decode($code_text);
        return '<div class="code-block-container">' . 
               '<button class="copy-button" data-clipboard-text="' . esc_attr($code_text) . '">Copy</button>' .
               $block_content . 
               '</div>';
    }
    return $block_content;
}
add_filter('render_block', 'handle_gutenberg_code_blocks', 10, 2);

/**
 * 【新增】为后台编辑器加载代码块的专属美化样式
 */
add_action( 'admin_enqueue_scripts', 'admin_code_block_styles' );
function admin_code_block_styles() {
    $css = "
        .editor-styles-wrapper .wp-block-code pre {
            background-color: #1a202c !important;
            color: #e2e8f0 !important;
            border: 1px solid #2d3748 !important;
            padding: 20px !important;
            border-radius: 8px !important;
            font-family: 'Fira Code', 'Menlo', 'Monaco', 'Courier New', monospace !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
        }
        .editor-styles-wrapper .wp-block-code pre code {
            background: none !important;
            padding: 0 !important;
            color: inherit !important;
            font-size: inherit !important;
        }
    ";
    wp_add_inline_style( 'wp-edit-blocks', $css );
}

/**
 * 防止WP Rocket合并关键的CSS和JS文件
 */
function exclude_files_from_wp_rocket($excluded_files) {
    if (!is_array($excluded_files)) {
        $excluded_files = array();
    }
    
    $excluded_files[] = get_stylesheet_directory_uri() . '/style.css';
    $excluded_files[] = get_stylesheet_directory_uri() . '/js/code-block-copy.js';
    
    return $excluded_files;
}
add_filter('rocket_exclude_css', 'exclude_files_from_wp_rocket');
add_filter('rocket_exclude_js', 'exclude_files_from_wp_rocket');

// 添加 Referrer Meta 标签
add_action('wp_head', function() {
    echo '<meta name="referrer" content="no-referrer-when-downgrade">' . "\n";
});

function add_category_to_pages() {
    register_taxonomy_for_object_type( 'category', 'page' );
}
add_action( 'init', 'add_category_to_pages' );

/**
 * =================================================================
 * Google Analytics & 视频埋点
 * =================================================================
 */
add_action( 'wp_head', 'pangolin_add_gtag_script' );
function pangolin_add_gtag_script() {
    ?>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GET1NHBL0N"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-GET1NHBL0N');
        
        document.addEventListener('visibilitychange', function () {
            if (document.hidden) {
                gtag('event', 'marketing_pangolin_page_leave', {
                    page_location: window.location.href,
                    page_origin: window.location.origin,
                    page_path: window.location.pathname,
                    event_category: 'engagement',
                });
            }
        });

        document.addEventListener('DOMContentLoaded', function() {
            var video = document.getElementById('pangolin-intro-video');
            
            if (video) {
                var progressMarkers = {};
                
                video.addEventListener('play', function() {
                    gtag('event', 'video_start', {
                        'event_category': 'video_engagement',
                        'event_label': 'pangolin-intro-video',
                        'video_title': 'Pangolin Intro Video',
                        'video_url': video.currentSrc || video.src,
                        'video_duration': Math.round(video.duration) || 0,
                        'page_location': window.location.href,
                        'custom_parameter_1': 'elementor_video'
                    });
                });
                
                video.addEventListener('pause', function() {
                    if (!video.ended) {
                        gtag('event', 'video_pause', {
                            'event_category': 'video_engagement',
                            'event_label': 'pangolin-intro-video',
                            'video_title': 'Pangolin Intro Video',
                            'video_current_time': Math.round(video.currentTime),
                            'video_percent': Math.round((video.currentTime / video.duration) * 100),
                            'page_location': window.location.href
                        });
                    }
                });
                
                video.addEventListener('ended', function() {
                    gtag('event', 'video_complete', {
                        'event_category': 'video_engagement',
                        'event_label': 'pangolin-intro-video',
                        'video_title': 'Pangolin Intro Video',
                        'video_duration': Math.round(video.duration),
                        'page_location': window.location.href,
                        'video_completion_rate': '100'
                    });
                });
                
                video.addEventListener('timeupdate', function() {
                    if (video.duration > 0) {
                        var progress = Math.round((video.currentTime / video.duration) * 100);
                        
                        if ((progress >= 25 && !progressMarkers['25']) ||
                            (progress >= 50 && !progressMarkers['50']) ||
                            (progress >= 75 && !progressMarkers['75'])) {
                            
                            var milestone = '';
                            if (progress >= 75 && !progressMarkers['75']) {
                                milestone = '75';
                                progressMarkers['75'] = true;
                            } else if (progress >= 50 && !progressMarkers['50']) {
                                milestone = '50';
                                progressMarkers['50'] = true;
                            } else if (progress >= 25 && !progressMarkers['25']) {
                                milestone = '25';
                                progressMarkers['25'] = true;
                            }
                            
                            if (milestone) {
                                gtag('event', 'video_progress', {
                                    'event_category': 'video_engagement',
                                    'event_label': 'pangolin-intro-video',
                                    'video_title': 'Pangolin Intro Video',
                                    'video_progress': milestone + '%',
                                    'video_current_time': Math.round(video.currentTime),
                                    'page_location': window.location.href
                                });
                            }
                        }
                    }
                });
                
                video.addEventListener('loadedmetadata', function() {
                    gtag('event', 'video_loaded', {
                        'event_category': 'video_engagement',
                        'event_label': 'pangolin-intro-video',
                        'video_title': 'Pangolin Intro Video',
                        'video_duration': Math.round(video.duration),
                        'page_location': window.location.href
                    });
                });
                
                video.addEventListener('waiting', function() {
                    gtag('event', 'video_buffering', {
                        'event_category': 'video_engagement',
                        'event_label': 'pangolin-intro-video',
                        'video_current_time': Math.round(video.currentTime),
                        'page_location': window.location.href
                    });
                });
                
                video.addEventListener('volumechange', function() {
                    gtag('event', 'video_volume_change', {
                        'event_category': 'video_engagement',
                        'event_label': 'pangolin-intro-video',
                        'video_volume': Math.round(video.volume * 100),
                        'video_muted': video.muted,
                        'page_location': window.location.href
                    });
                });
            }
        });
    </script>
    <?php
}

/**
 * =================================================================
 * 在线客服系统
 * =================================================================
 */
add_action( 'wp_footer', 'pangolin_add_online_chat_system' );
function pangolin_add_online_chat_system() {
    ?>
    <script>
    const locales = {
        "zh": ['zh-CN'],
        "en": ['en-US']
    }
    
    const langInfo = {
        'zh': {
            langAlias: ['zh-CN'],
            title: '点击在线客服<br>或扫码加微信',
            qrCode: 'https://www.pangolinfo.com/wp-content/uploads/2025/03/WX20250526-134449@2x-e1748497234391.png',
            chatUrl: 'https://chat.quickcep.com/initQuickChat.js?platform=others&accessId=83fb47fa-68bc-4d37-8d61-2d381b922816&lang=zh'
        },
        'en': {
            langAlias: ['en-US'],
            title: 'Chat online or scan<br>to chat on WhatsApp',
            qrCode: 'https://www.pangolinfo.com/wp-content/uploads/2025/08/en-help-qrcode.webp',
            chatUrl: 'https://chat.quickcep.com/initQuickChat.js?platform=others&accessId=83fb47fa-68bc-4d37-8d61-2d381b922816&lang=en'
        }
    }[Object.entries(locales).find(([key, arr]) => arr.includes(document.documentElement.lang))?.[0] || 'zh']
    
    injectChat()
    
    function injectChat() {
        const script = document.createElement('script');
        script.async = true;
        script.src = langInfo.chatUrl;
        document.body.appendChild(script);
    }
    
    waitForElement('#quick-chat-iframe', (target) => {
        const codeWrapper = createElementTools()
        
        const resizeObserver = new ResizeObserver(entries => {
            for (let entry of entries) {
                const { width, height } = entry.contentRect;
                width > 100 && Object.assign(codeWrapper.style, { opacity: 0, visibility: 'hidden' })
            }
        });
        resizeObserver.observe(target);
        
        target.addEventListener("mouseenter", (e) => {
            const styles = getComputedStyle(e.target);
            const { bottom, height, left, right, top, width, x, y } = e.target.getBoundingClientRect();
            if (width < 100) {
                Object.assign(codeWrapper.style, {
                    opacity: 1,
                    visibility: 'visible',
                    top: `${top - (codeWrapper.offsetHeight / 2) - (height / 2)}px`,
                    left: `${left - (codeWrapper.offsetWidth / 2) - (width / 2)}px`,
                })
            }
        })
        
        target.addEventListener("mouseleave", () => {
            Object.assign(codeWrapper.style, { opacity: 0, visibility: 'hidden' })
        })
    });
    
    function waitForElement(selector, callback) {
        const timer = setInterval(() => {
            const el = document.querySelector(selector);
            if (el) {
                callback(el);
                clearInterval(timer);
            }
        }, 200);
    }
    
    function createElementTools() {
        const wrapper = document.createElement("div");
        Object.assign(wrapper.style, {
            position: 'fixed', 
            padding: '20px',
            textAlign: 'center', 
            color: '#0c254b',
            visibility: 'hidden', 
            transition: 'opacity .3s ease',
            opacity: 0, 
            borderRadius: '15px', 
            background: '#FFFFFF', 
            boxShadow: '0 4px 20px rgba(0, 0, 0, .15)',
            zIndex: 9999
        })
        
        const text = document.createElement("p");
        text.innerHTML = langInfo?.title || '-';
        Object.assign(text.style, { 
            margin: '0 0 10px', 
            fontSize: '12px', 
            fontWeight: '400', 
            color: '#0c254b' 
        })
        wrapper.appendChild(text);
        
        const img = document.createElement("img");
        img.src = langInfo?.qrCode || '-';
        img.alt = "QR Code";
        Object.assign(img.style, { 
            margin: '0 auto', 
            width: '120px', 
            height: 'auto', 
            display: 'block', 
            borderRadius: '5px' 
        })
        
        wrapper.appendChild(img);
        document.body.appendChild(wrapper);
        
        return wrapper
    }
    </script>
    <?php
}

/**
 * =================================================================
 * Cookie 同意弹窗
 * =================================================================
 */
add_action( 'wp_footer', 'pangolin_add_cookie_consent_banner' );
function pangolin_add_cookie_consent_banner() {
    if ( function_exists( 'pll_current_language' ) ) {
        $current_lang = pll_current_language();
    } else {
        $current_lang = 'en';
    }

    if ( $current_lang === 'zh' ) {
        $privacy_policy_url = 'https://www.pangolinfo.com/zh/privacy-policy-cn/';
        $banner_text = '我们使用必要的 Cookie 以确保我们网站的正常运行。在征得您的同意后，我们可能还会使用非必要的 Cookie 来改善用户体验并分析网站流量。点击"接受"，即表示您同意我们按照《<a href="%s">隐私政策</a>》中的描述使用 Cookie。';
        $decline_btn_text = '拒绝';
        $accept_btn_text = '接受';
    } else {
        $privacy_policy_url = 'https://www.pangolinfo.com/pangolin-scrape-api-privacy-policy/';
        $banner_text = 'We use essential cookies to make our site work. With your consent, we may also use non-essential cookies to improve user experience and analyze website traffic. By clicking "Accept," you agree to our website\'s cookie use as described in our <a href="%s">Cookie Policy</a>.';
        $decline_btn_text = 'Decline';
        $accept_btn_text = 'Accept';
    }
    ?>
    <div id="cookie-consent-banner">
        <p><?php printf($banner_text, esc_url($privacy_policy_url)); ?></p>
        <div class="ccb-buttons">
            <button class="ccb-button ccb-decline" id="cookie-decline"><?php echo esc_html($decline_btn_text); ?></button>
            <button class="ccb-button ccb-accept" id="cookie-accept"><?php echo esc_html($accept_btn_text); ?></button>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var banner = document.getElementById('cookie-consent-banner');
        if (!banner) return;

        var acceptBtn = document.getElementById('cookie-accept');
        var declineBtn = document.getElementById('cookie-decline');

        function getCookie(name) {
            var value = '; ' + document.cookie;
            var parts = value.split('; ' + name + '=');
            if (parts.length === 2) return parts.pop().split(';').shift();
        }

        if (!getCookie('cookie_consent_status')) {
            banner.style.display = 'block';
        }

        function setConsentCookie(status) {
            var date = new Date();
            date.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000));
            var expires = "expires=" + date.toUTCString();
            document.cookie = 'cookie_consent_status=' + status + ';' + expires + ';path=/;SameSite=Lax';
            banner.style.display = 'none';
        }

        acceptBtn.addEventListener('click', function() { setConsentCookie('accepted'); });
        declineBtn.addEventListener('click', function() { setConsentCookie('declined'); });
    });
    </script>
    <?php
}
?>
