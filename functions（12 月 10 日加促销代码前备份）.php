<?php
/**
 * ===================================================================
 * Astra Child Theme functions.php - 最终整合版 (v17 - 支持Polylang多语言页脚)
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
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        z-index: 9998;
        
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
    /* 当登录且显示管理条时，页眉下移 32px */
    body.admin-bar .ast-primary-header-bar {
        top: 32px !important;
    }
    /* 移动端 WordPress 管理条通常较高 (46px)，需单独适配 */
    @media screen and (max-width: 782px) {
        body.admin-bar .ast-primary-header-bar {
            top: 46px !important;
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
 * ===================================================================
 * Polylang 语言切换器自定义样式
 * ===================================================================
 * 将语言切换器显示为紧凑的按钮样式,与其他菜单项区分
 */
function add_polylang_language_switcher_styles() {
    ?>
    <style>
    /* Polylang 语言切换器按钮样式 */
    .main-header-menu .lang-item > a,
    .main-header-menu .menu-item[class*="language"] > a,
    .main-header-menu .menu-item[class*="lang"] > a {
        /* 按钮样式 */
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        
        /* 文字样式 */
        padding: 4px 16px !important;
        margin: 0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #ffffff !important;
        text-transform: none !important;
        letter-spacing: 0.3px !important;
        line-height: 1.1 !important;
        white-space: nowrap !important;
        text-decoration: none !important;
        display: inline-block !important;
        vertical-align: middle !important;
        
        /* 强制限制高度 */
        min-height: 0 !important;
        height: auto !important;
        max-height: 28px !important;
        
        /* 动画效果 */
        transition: all 0.3s ease !important;
    }

    /* 悬停效果 */
    .main-header-menu .lang-item > a:hover,
    .main-header-menu .menu-item[class*="language"] > a:hover,
    .main-header-menu .menu-item[class*="lang"] > a:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    /* 点击效果 */
    .main-header-menu .lang-item > a:active,
    .main-header-menu .menu-item[class*="language"] > a:active,
    .main-header-menu .menu-item[class*="lang"] > a:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
    }

    /* 调整父元素 - 重置 Astra 主题的默认高度 */
    .main-header-menu .lang-item,
    .main-header-menu .menu-item[class*="language"],
    .main-header-menu .menu-item[class*="lang"] {
        padding: 0 !important;
        margin: 0 10px !important;
        min-height: 0 !important;
        height: auto !important;
        line-height: normal !important;
    }

    /* 更强制的高度重置 - 针对 Astra 主题 */
    .main-header-bar .main-header-menu .lang-item,
    .main-header-bar .main-header-menu .menu-item[class*="language"],
    .main-header-bar .main-header-menu .menu-item[class*="lang"] {
        min-height: 0 !important;
        height: auto !important;
        align-items: center !important;
    }

    .main-header-bar .main-header-menu .lang-item > a,
    .main-header-bar .main-header-menu .menu-item[class*="language"] > a,
    .main-header-bar .main-header-menu .menu-item[class*="lang"] > a {
        min-height: 0 !important;
        height: auto !important;
    }

    /* 移除 Astra 主题的默认悬停背景 */
    .main-header-menu .lang-item > a:hover,
    .main-header-menu .menu-item[class*="language"] > a:hover,
    .main-header-menu .menu-item[class*="lang"] > a:hover {
        background-color: transparent;
    }

    /* 移除可能的下划线 */
    .main-header-menu .lang-item a,
    .main-header-menu .menu-item[class*="language"] a,
    .main-header-menu .menu-item[class*="lang"] a {
        text-decoration: none !important;
        border-bottom: none !important;
    }

    /* 确保链接文字颜色正确 */
    .main-header-menu .lang-item a span,
    .main-header-menu .menu-item[class*="language"] a span,
    .main-header-menu .menu-item[class*="lang"] a span {
        color: inherit !important;
    }

    /* 响应式设计 - 平板设备 */
    @media (max-width: 992px) {
        .main-header-menu .lang-item > a,
        .main-header-menu .menu-item[class*="language"] > a,
        .main-header-menu .menu-item[class*="lang"] > a {
            padding: 4px 12px !important;
            font-size: 13px !important;
            line-height: 1.1 !important;
            max-height: 26px !important;
        }
        
        .main-header-menu .lang-item,
        .main-header-menu .menu-item[class*="language"],
        .main-header-menu .menu-item[class*="lang"] {
            margin: 0 8px !important;
        }
    }

    /* 响应式设计 - 移动设备 */
    @media (max-width: 768px) {
        .main-header-menu .lang-item > a,
        .main-header-menu .menu-item[class*="language"] > a,
        .main-header-menu .menu-item[class*="lang"] > a {
            padding: 5px 14px !important;
            font-size: 14px !important;
            line-height: 1.1 !important;
            max-height: 28px !important;
        }
        
        .main-header-menu .lang-item,
        .main-header-menu .menu-item[class*="language"],
        .main-header-menu .menu-item[class*="lang"] {
            margin: 10px auto !important;
            display: block !important;
            text-align: center !important;
            max-width: 150px !important;
        }
    }
    </style>
    <?php
}
add_action('wp_head', 'add_polylang_language_switcher_styles');

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
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GET1NHBL0N"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-GET1NHBL0N');
        
        document.addEventListener('visibilitychange', function () {
            if (document.hidden) {
                console.log('==========isHidden:隐藏 ');
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
    // 在 Elementor 编辑器中不加载，避免冲突
    if ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) {
        return;
    }
    
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
                // 计算弹窗应该显示的位置
                // 垂直居中:客服图标的中心点 - 弹窗高度的一半
                const popupTop = top + (height / 2) - (codeWrapper.offsetHeight / 2);
                // 水平位置:客服图标左侧,留出 10px 间距
                const popupLeft = left - codeWrapper.offsetWidth - 10;
                
                Object.assign(codeWrapper.style, {
                    opacity: 1,
                    visibility: 'visible',
                    top: `${popupTop}px`,
                    left: `${popupLeft}px`,
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
    // 在 Elementor 编辑器中不加载，避免冲突
    if ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) {
        return;
    }
    
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

/**
 * =================================================================
 * Cloudflare Turnstile 验证码集成 - 防止机器人表单提交
 * =================================================================
 * 配置时间：2025-12-10
 * 服务：Cloudflare Turnstile
 * 站点：Pangolin 官网
 */

// 配置密钥
define('TURNSTILE_SITE_KEY', '0x4AAAAAACFub-s1vgpEKek0');
define('TURNSTILE_SECRET_KEY', '0x4AAAAAACFub5brTezVyhvwZ0-qBqkTxyw');

/**
 * 1. 加载 Turnstile 脚本和自定义 JS
 */
add_action('wp_footer', 'load_turnstile_captcha_assets');
function load_turnstile_captcha_assets() {
    // 在 Elementor 编辑器中不加载，避免冲突
    if ( \Elementor\Plugin::$instance->editor->is_edit_mode() || \Elementor\Plugin::$instance->preview->is_preview_mode() ) {
        return;
    }
    
    ?>
    <!-- Cloudflare Turnstile Script -->
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>
    
    <script>
    // 全局变量存储已渲染的验证码
    window.turnstileWidgets = window.turnstileWidgets || [];
    
    // 添加验证码到表单
    function addTurnstileToForms() {
        console.log('[Turnstile] 开始查找 Elementor 表单...');
        
        var forms = [];
        
        // 方法 1: 标准 Elementor 表单（最精确）
        var elementorForms = document.querySelectorAll('.elementor-form');
        console.log('[Turnstile] 方法1 - 找到', elementorForms.length, '个 .elementor-form');
        
        if (elementorForms.length > 0) {
            forms = Array.from(elementorForms);
        } else {
            // 方法 2: 查找所有表单，然后严格过滤
            var allForms = document.querySelectorAll('form');
            console.log('[Turnstile] 方法2 - 页面上共有', allForms.length, '个表单');
            
            allForms.forEach(function(form) {
                // 排除搜索表单
                if (form.role === 'search' || 
                    form.className.indexOf('search') !== -1 ||
                    form.id.indexOf('search') !== -1 ||
                    form.querySelector('input[type="search"]')) {
                    console.log('[Turnstile] ⊗ 跳过搜索表单:', form.className || form.id);
                    return;
                }
                
                // 排除评论表单
                if (form.id === 'commentform' || 
                    form.className.indexOf('comment') !== -1) {
                    console.log('[Turnstile] ⊗ 跳过评论表单:', form.className || form.id);
                    return;
                }
                
                // 排除登录/注册表单
                if (form.className.indexOf('login') !== -1 || 
                    form.className.indexOf('register') !== -1 ||
                    form.id.indexOf('login') !== -1) {
                    console.log('[Turnstile] ⊗ 跳过登录/注册表单:', form.className || form.id);
                    return;
                }
                
                // 只保留 Elementor 表单
                if (form.className.indexOf('elementor') !== -1 || 
                    form.closest('.elementor-element') ||
                    form.querySelector('.elementor-field-group')) {
                    console.log('[Turnstile] ✓ 找到 Elementor 表单:', form.className);
                    forms.push(form);
                }
            });
            
            console.log('[Turnstile] 方法2 - 过滤后找到', forms.length, '个 Elementor 表单');
        }
        
        if (forms.length === 0) {
            console.log('[Turnstile] ❌ 未找到任何 Elementor 表单');
            return false;
        }
        
        var added = false;
        
        forms.forEach(function(form, index) {
            console.log('[Turnstile] 处理表单', index, '- Class:', form.className);
            
            // 检查是否已经添加过验证码
            if (form.querySelector('.cf-turnstile-wrapper')) {
                console.log('[Turnstile] 表单', index, '已有验证码，跳过');
                return;
            }
            
            // 查找提交按钮 - 使用多种选择器
            var submitButton = form.querySelector('.elementor-field-type-submit') ||
                              form.querySelector('.elementor-button') ||
                              form.querySelector('button[type="submit"]') ||
                              form.querySelector('input[type="submit"]');
            
            console.log('[Turnstile] 提交按钮:', submitButton ? '找到' : '未找到');
            
            if (submitButton) {
                // 创建验证码容器
                var captchaWrapper = document.createElement('div');
                captchaWrapper.className = 'elementor-field-group elementor-column elementor-col-100 cf-turnstile-wrapper';
                captchaWrapper.style.cssText = 'margin: 20px 0; text-align: center; width: 100%; clear: both;';
                
                // 创建 Turnstile 容器
                var captchaDiv = document.createElement('div');
                captchaDiv.className = 'cf-turnstile';
                captchaDiv.id = 'turnstile-' + Math.random().toString(36).substr(2, 9);
                
                captchaWrapper.appendChild(captchaDiv);
                
                // 在提交按钮前插入验证码
                submitButton.parentNode.insertBefore(captchaWrapper, submitButton);
                
                // 渲染 Turnstile
                renderTurnstile(captchaDiv);
                
                console.log('[Turnstile] ✅ 验证码已添加到表单', index);
                added = true;
            } else {
                console.log('[Turnstile] ❌ 表单', index, '未找到提交按钮');
            }
        });
        
        return added;
    }
    
    // 渲染 Turnstile 验证码
    function renderTurnstile(element) {
        // 等待 Turnstile API 加载
        if (typeof turnstile === 'undefined') {
            setTimeout(function() {
                renderTurnstile(element);
            }, 100);
            return;
        }
        
        try {
            // 获取语言设置
            var htmlLang = document.documentElement.lang || 'zh-CN';
            console.log('[Turnstile] 检测到的语言:', htmlLang);
            
            // 改进语言判断逻辑
            var lang = 'zh-CN'; // 默认中文
            if (htmlLang) {
                var langLower = htmlLang.toLowerCase();
                // 检查是否包含 'en'（支持 en、en-US、en-GB 等）
                if (langLower.indexOf('en') === 0 || langLower === 'en') {
                    lang = 'en';
                }
            }
            
            console.log('[Turnstile] 使用的语言:', lang);
            
            // 渲染验证码
            var widgetId = turnstile.render(element, {
                sitekey: '<?php echo esc_js(TURNSTILE_SITE_KEY); ?>',
                theme: 'light',
                size: 'normal',
                language: lang,
                callback: function(token) {
                    console.log('[Turnstile] 验证成功');
                },
                'error-callback': function() {
                    console.log('[Turnstile] 验证失败');
                }
            });
            
            window.turnstileWidgets.push(widgetId);
            console.log('[Turnstile] 验证码已渲染, Widget ID:', widgetId);
        } catch (error) {
            console.error('[Turnstile] 渲染失败:', error);
        }
    }
    
    // 页面加载完成后执行
    function initTurnstile() {
        console.log('[Turnstile] 初始化开始，等待表单加载...');
        
        // 第一次尝试：等待 2 秒（给表单更多加载时间）
        setTimeout(function() {
            console.log('[Turnstile] 第1次尝试添加验证码');
            var success = addTurnstileToForms();
            
            if (!success) {
                // 第二次尝试：再等 2 秒
                console.log('[Turnstile] 第1次失败，2秒后第2次尝试...');
                setTimeout(function() {
                    console.log('[Turnstile] 第2次尝试添加验证码');
                    var success2 = addTurnstileToForms();
                    
                    if (!success2) {
                        // 第三次尝试：再等 3 秒
                        console.log('[Turnstile] 第2次失败，3秒后第3次尝试...');
                        setTimeout(function() {
                            console.log('[Turnstile] 第3次尝试添加验证码');
                            addTurnstileToForms();
                        }, 3000);
                    }
                }, 2000);
            }
        }, 2000);
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTurnstile);
    } else {
        initTurnstile();
    }
    
    // 监听 Elementor 弹窗打开事件
    jQuery(document).ready(function($) {
        console.log('[Turnstile] 开始监听弹窗事件');
        
        // 方法 1: 监听 Elementor 弹窗显示事件
        $(document).on('elementor/popup/show', function(event, id, instance) {
            console.log('[Turnstile] 检测到 Elementor 弹窗打开 (方法1), ID:', id);
            setTimeout(function() {
                addTurnstileToForms();
            }, 500);
        });
        
        // 方法 2: 监听所有弹窗相关的点击事件
        $(document).on('click', '[data-elementor-open-lightbox], .elementor-popup-trigger, [href*="#elementor-action"]', function() {
            console.log('[Turnstile] 检测到弹窗触发按钮被点击 (方法2)');
            setTimeout(function() {
                addTurnstileToForms();
            }, 800);
        });
        
        // 方法 3: 监听 DOM 变化（弹窗出现）
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) {
                            // 检测弹窗容器
                            if (node.classList && (
                                node.classList.contains('elementor-popup-modal') ||
                                node.classList.contains('dialog-widget-content') ||
                                node.classList.contains('elementor-location-popup')
                            )) {
                                console.log('[Turnstile] 检测到弹窗容器出现 (方法3)');
                                setTimeout(function() {
                                    addTurnstileToForms();
                                }, 500);
                            }
                            
                            // 检测表单出现
                            if (node.classList && node.classList.contains('elementor-form')) {
                                console.log('[Turnstile] 检测到新表单出现 (方法3)');
                                setTimeout(function() {
                                    addTurnstileToForms();
                                }, 500);
                            }
                            
                            // 检测弹窗内的表单
                            if (node.querySelector && node.querySelector('.elementor-form')) {
                                console.log('[Turnstile] 检测到弹窗内有表单 (方法3)');
                                setTimeout(function() {
                                    addTurnstileToForms();
                                }, 500);
                            }
                        }
                    });
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        console.log('[Turnstile] 弹窗监听器已启动');
    });
    </script>
    
    <style>
    /* Cloudflare Turnstile 验证码样式 */
    .cf-turnstile-wrapper {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 15px 0 !important;
        background: #f9f9f9;
        border-radius: 8px;
        margin: 20px auto !important;
        min-height: 65px;
        text-align: center !important;
    }
    
    .cf-turnstile {
        margin: 0 auto !important;
        display: inline-block !important;
    }
    
    /* 确保在弹窗中也居中 */
    .elementor-popup-modal .cf-turnstile-wrapper,
    .dialog-widget-content .cf-turnstile-wrapper {
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .cf-turnstile-wrapper {
            padding: 10px 0 !important;
        }
        
        .cf-turnstile {
            transform: scale(0.95);
            transform-origin: center;
        }
    }
    
    @media (max-width: 480px) {
        .cf-turnstile {
            transform: scale(0.85);
        }
    }
    </style>
    <?php
}

/**
 * 2. 验证 Turnstile 响应
 */
add_action('elementor_pro/forms/validation', 'validate_turnstile_captcha', 10, 2);
function validate_turnstile_captcha($record, $ajax_handler) {
    // 获取 Turnstile 响应
    $turnstile_response = isset($_POST['cf-turnstile-response']) ? sanitize_text_field($_POST['cf-turnstile-response']) : '';
    
    // 检查是否有响应
    if (empty($turnstile_response)) {
        // 根据语言返回错误信息
        $current_lang = function_exists('pll_current_language') ? pll_current_language() : 'zh';
        $error_message = ($current_lang === 'en') 
            ? 'Please complete the verification.' 
            : '请完成人机验证。';
        
        $ajax_handler->add_error_message($error_message);
        error_log('[Turnstile] 验证失败 - 未收到响应 - IP: ' . $_SERVER['REMOTE_ADDR']);
        return;
    }
    
    // 验证 token
    $verify_result = verify_turnstile_token($turnstile_response);
    
    if (!$verify_result['success']) {
        $ajax_handler->add_error_message($verify_result['message']);
        return;
    }
    
    // 验证成功，记录日志
    error_log('[Turnstile] 验证成功 - IP: ' . $_SERVER['REMOTE_ADDR']);
}

/**
 * 3. Turnstile 验证函数
 */
function verify_turnstile_token($response) {
    $verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
    
    // 发送验证请求
    $response_data = wp_remote_post($verify_url, array(
        'body' => array(
            'secret' => TURNSTILE_SECRET_KEY,
            'response' => $response,
            'remoteip' => $_SERVER['REMOTE_ADDR']
        ),
        'timeout' => 10
    ));
    
    // 检查请求是否成功
    if (is_wp_error($response_data)) {
        error_log('[Turnstile] API 请求失败: ' . $response_data->get_error_message());
        
        $current_lang = function_exists('pll_current_language') ? pll_current_language() : 'zh';
        $error_message = ($current_lang === 'en')
            ? 'Verification service is temporarily unavailable. Please try again later.'
            : '验证服务暂时不可用，请稍后重试。';
        
        return array(
            'success' => false,
            'message' => $error_message
        );
    }
    
    // 解析响应
    $response_body = json_decode(wp_remote_retrieve_body($response_data), true);
    
    // 检查验证结果
    if (!isset($response_body['success']) || !$response_body['success']) {
        $error_codes = isset($response_body['error-codes']) ? implode(', ', $response_body['error-codes']) : 'unknown';
        error_log('[Turnstile] 验证失败 - IP: ' . $_SERVER['REMOTE_ADDR'] . ' - 错误代码: ' . $error_codes);
        
        $current_lang = function_exists('pll_current_language') ? pll_current_language() : 'zh';
        $error_message = ($current_lang === 'en')
            ? 'Verification failed. Please try again.'
            : '人机验证失败，请重试。';
        
        return array(
            'success' => false,
            'message' => $error_message
        );
    }
    
    // 验证成功
    return array(
        'success' => true,
        'message' => 'Verification passed'
    );
}

/**
 * =================================================================
 * Elementor 弹窗关闭按钮修复
 * =================================================================
 * 修复关闭按钮不显示的问题
 */
add_action('wp_head', 'fix_elementor_popup_close_button');
function fix_elementor_popup_close_button() {
    ?>
    <style>
    /* Elementor 弹窗关闭按钮修复 */
    .elementor-popup-modal .dialog-close-button,
    .elementor-popup-modal .eicon-close {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* 关闭按钮基础样式 */
    .elementor-popup-modal .dialog-close-button {
        position: absolute;
        top: 20px;
        right: 20px;
        width: 40px;
        height: 40px;
        cursor: pointer;
        z-index: 999999 !important;
        background: transparent;
        border: none;
        padding: 0;
    }
    
    /* 关闭图标样式 */
    .elementor-popup-modal .dialog-close-button i {
        font-size: 24px;
        color: #333;
        line-height: 40px;
    }
    
    .elementor-popup-modal .dialog-close-button:hover i {
        color: #000;
    }
    
    /* 如果使用 SVG 图标 */
    .elementor-popup-modal .dialog-close-button svg {
        width: 24px;
        height: 24px;
        fill: #333;
    }
    
    .elementor-popup-modal .dialog-close-button:hover svg {
        fill: #000;
    }
    
    /* 确保图标库加载 */
    .elementor-popup-modal .eicon {
        font-family: 'eicons' !important;
        speak: none;
        font-style: normal;
        font-weight: normal;
        font-variant: normal;
        text-transform: none;
        line-height: 1;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* 备用方案：使用 × 符号 */
    .elementor-popup-modal .dialog-close-button:not(:has(i)):not(:has(svg))::before {
        content: '×';
        font-size: 32px;
        line-height: 40px;
        color: #333;
        font-weight: 300;
        display: block;
        text-align: center;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .elementor-popup-modal .dialog-close-button {
            top: 10px;
            right: 10px;
            width: 36px;
            height: 36px;
        }
        
        .elementor-popup-modal .dialog-close-button i {
            font-size: 20px;
            line-height: 36px;
        }
    }
    </style>
    <?php
}
?>
