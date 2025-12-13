/**
 * =================================================================
 * 验证码集成代码 - 支持多种验证码服务
 * =================================================================
 * 支持的服务：
 * 1. Cloudflare Turnstile（推荐）
 * 2. Google reCAPTCHA v3
 * 3. hCaptcha
 * 
 * 使用方法：
 * 1. 选择一个验证码服务并注册获取密钥
 * 2. 在下方配置区域填写您的密钥
 * 3. 取消对应服务的注释
 * 4. 将代码添加到 functions.php
 * 5. 在 Elementor 表单中测试
 */

// ============================================================
// 配置区域 - 请根据您选择的服务填写对应的密钥
// ============================================================

// 方案 1：Cloudflare Turnstile（推荐）
// 注册地址：https://dash.cloudflare.com/
define('TURNSTILE_SITE_KEY', '0x4XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
define('TURNSTILE_SECRET_KEY', '0x4XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
define('USE_TURNSTILE', true); // 设置为 true 启用

// 方案 2：Google reCAPTCHA v3
// 注册地址：https://www.google.com/recaptcha/admin/create
define('RECAPTCHA_SITE_KEY', '6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
define('RECAPTCHA_SECRET_KEY', '6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
define('USE_RECAPTCHA', false); // 设置为 true 启用

// 方案 3：hCaptcha
// 注册地址：https://www.hcaptcha.com/
define('HCAPTCHA_SITE_KEY', 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX');
define('HCAPTCHA_SECRET_KEY', '0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
define('USE_HCAPTCHA', false); // 设置为 true 启用

// 验证分数阈值（仅 reCAPTCHA v3 使用）
// 0.0 = 最宽松，1.0 = 最严格，推荐 0.5
define('RECAPTCHA_SCORE_THRESHOLD', 0.5);

// ============================================================
// 1. 加载验证码脚本
// ============================================================

add_action('wp_enqueue_scripts', 'load_captcha_scripts');
function load_captcha_scripts() {
    // 只在有表单的页面加载
    if (!is_page() && !is_single()) {
        return;
    }
    
    // Cloudflare Turnstile
    if (defined('USE_TURNSTILE') && USE_TURNSTILE) {
        wp_enqueue_script(
            'cloudflare-turnstile',
            'https://challenges.cloudflare.com/turnstile/v0/api.js',
            array(),
            null,
            true
        );
    }
    
    // Google reCAPTCHA v3
    if (defined('USE_RECAPTCHA') && USE_RECAPTCHA) {
        wp_enqueue_script(
            'google-recaptcha',
            'https://www.google.com/recaptcha/api.js?render=' . RECAPTCHA_SITE_KEY,
            array(),
            null,
            true
        );
    }
    
    // hCaptcha
    if (defined('USE_HCAPTCHA') && USE_HCAPTCHA) {
        wp_enqueue_script(
            'hcaptcha',
            'https://js.hcaptcha.com/1/api.js',
            array(),
            null,
            true
        );
    }
}

// ============================================================
// 2. 在 Elementor 表单底部自动添加验证码
// ============================================================

add_action('elementor_pro/forms/render/item', 'add_captcha_to_elementor_form', 10, 3);
function add_captcha_to_elementor_form($item, $item_index, $form) {
    // 只在最后一个字段后添加
    $fields = $form->get_settings('form_fields');
    $last_field_index = count($fields) - 1;
    
    if ($item_index !== $last_field_index) {
        return;
    }
    
    echo '<div class="elementor-field-type-captcha elementor-field-group" style="margin-top: 20px;">';
    
    // Cloudflare Turnstile
    if (defined('USE_TURNSTILE') && USE_TURNSTILE) {
        ?>
        <div class="cf-turnstile" 
             data-sitekey="<?php echo esc_attr(TURNSTILE_SITE_KEY); ?>"
             data-theme="light"
             data-size="normal"
             data-language="<?php echo function_exists('pll_current_language') ? pll_current_language() : 'zh'; ?>">
        </div>
        <?php
    }
    
    // Google reCAPTCHA v3（隐藏式）
    if (defined('USE_RECAPTCHA') && USE_RECAPTCHA) {
        ?>
        <input type="hidden" name="g-recaptcha-response" id="g-recaptcha-response-<?php echo $form->get_id(); ?>">
        <script>
            grecaptcha.ready(function() {
                grecaptcha.execute('<?php echo esc_js(RECAPTCHA_SITE_KEY); ?>', {action: 'submit'})
                .then(function(token) {
                    document.getElementById('g-recaptcha-response-<?php echo $form->get_id(); ?>').value = token;
                });
            });
        </script>
        <div style="font-size: 12px; color: #666; margin-top: 10px;">
            此站点受 reCAPTCHA 保护，适用 Google 
            <a href="https://policies.google.com/privacy" target="_blank">隐私政策</a>和
            <a href="https://policies.google.com/terms" target="_blank">服务条款</a>。
        </div>
        <?php
    }
    
    // hCaptcha
    if (defined('USE_HCAPTCHA') && USE_HCAPTCHA) {
        ?>
        <div class="h-captcha" 
             data-sitekey="<?php echo esc_attr(HCAPTCHA_SITE_KEY); ?>"
             data-theme="light"
             data-size="normal">
        </div>
        <?php
    }
    
    echo '</div>';
}

// ============================================================
// 3. 验证码验证逻辑
// ============================================================

add_action('elementor_pro/forms/validation', 'validate_captcha_submission', 10, 2);
function validate_captcha_submission($record, $ajax_handler) {
    
    // Cloudflare Turnstile 验证
    if (defined('USE_TURNSTILE') && USE_TURNSTILE) {
        $turnstile_response = isset($_POST['cf-turnstile-response']) ? sanitize_text_field($_POST['cf-turnstile-response']) : '';
        
        if (empty($turnstile_response)) {
            $ajax_handler->add_error_message('请完成人机验证。');
            return;
        }
        
        $verify_result = verify_turnstile($turnstile_response);
        
        if (!$verify_result['success']) {
            $ajax_handler->add_error_message($verify_result['message']);
            return;
        }
    }
    
    // Google reCAPTCHA v3 验证
    if (defined('USE_RECAPTCHA') && USE_RECAPTCHA) {
        $recaptcha_response = isset($_POST['g-recaptcha-response']) ? sanitize_text_field($_POST['g-recaptcha-response']) : '';
        
        if (empty($recaptcha_response)) {
            $ajax_handler->add_error_message('验证码验证失败，请刷新页面重试。');
            return;
        }
        
        $verify_result = verify_recaptcha($recaptcha_response);
        
        if (!$verify_result['success']) {
            $ajax_handler->add_error_message($verify_result['message']);
            return;
        }
    }
    
    // hCaptcha 验证
    if (defined('USE_HCAPTCHA') && USE_HCAPTCHA) {
        $hcaptcha_response = isset($_POST['h-captcha-response']) ? sanitize_text_field($_POST['h-captcha-response']) : '';
        
        if (empty($hcaptcha_response)) {
            $ajax_handler->add_error_message('请完成人机验证。');
            return;
        }
        
        $verify_result = verify_hcaptcha($hcaptcha_response);
        
        if (!$verify_result['success']) {
            $ajax_handler->add_error_message($verify_result['message']);
            return;
        }
    }
}

// ============================================================
// 4. Cloudflare Turnstile 验证函数
// ============================================================

function verify_turnstile($response) {
    $verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
    
    $response_data = wp_remote_post($verify_url, array(
        'body' => array(
            'secret' => TURNSTILE_SECRET_KEY,
            'response' => $response,
            'remoteip' => $_SERVER['REMOTE_ADDR']
        ),
        'timeout' => 10
    ));
    
    if (is_wp_error($response_data)) {
        error_log('[Turnstile] 验证请求失败: ' . $response_data->get_error_message());
        return array(
            'success' => false,
            'message' => '验证服务暂时不可用，请稍后重试。'
        );
    }
    
    $response_body = json_decode(wp_remote_retrieve_body($response_data), true);
    
    if (!isset($response_body['success']) || !$response_body['success']) {
        $error_codes = isset($response_body['error-codes']) ? implode(', ', $response_body['error-codes']) : 'unknown';
        error_log('[Turnstile] 验证失败 - IP: ' . $_SERVER['REMOTE_ADDR'] . ' - 错误: ' . $error_codes);
        
        return array(
            'success' => false,
            'message' => '人机验证失败，请重试。'
        );
    }
    
    // 记录成功的验证
    error_log('[Turnstile] 验证成功 - IP: ' . $_SERVER['REMOTE_ADDR']);
    
    return array(
        'success' => true,
        'message' => '验证通过'
    );
}

// ============================================================
// 5. Google reCAPTCHA v3 验证函数
// ============================================================

function verify_recaptcha($response) {
    $verify_url = 'https://www.google.com/recaptcha/api/siteverify';
    
    $response_data = wp_remote_post($verify_url, array(
        'body' => array(
            'secret' => RECAPTCHA_SECRET_KEY,
            'response' => $response,
            'remoteip' => $_SERVER['REMOTE_ADDR']
        ),
        'timeout' => 10
    ));
    
    if (is_wp_error($response_data)) {
        error_log('[reCAPTCHA] 验证请求失败: ' . $response_data->get_error_message());
        return array(
            'success' => false,
            'message' => '验证服务暂时不可用，请稍后重试。'
        );
    }
    
    $response_body = json_decode(wp_remote_retrieve_body($response_data), true);
    
    if (!isset($response_body['success']) || !$response_body['success']) {
        $error_codes = isset($response_body['error-codes']) ? implode(', ', $response_body['error-codes']) : 'unknown';
        error_log('[reCAPTCHA] 验证失败 - IP: ' . $_SERVER['REMOTE_ADDR'] . ' - 错误: ' . $error_codes);
        
        return array(
            'success' => false,
            'message' => '验证码验证失败，请重试。'
        );
    }
    
    // 检查分数
    $score = isset($response_body['score']) ? floatval($response_body['score']) : 0;
    
    if ($score < RECAPTCHA_SCORE_THRESHOLD) {
        error_log('[reCAPTCHA] 分数过低 - IP: ' . $_SERVER['REMOTE_ADDR'] . ' - 分数: ' . $score);
        
        return array(
            'success' => false,
            'message' => '您的操作疑似机器人行为，请稍后重试。'
        );
    }
    
    // 记录成功的验证
    error_log('[reCAPTCHA] 验证成功 - IP: ' . $_SERVER['REMOTE_ADDR'] . ' - 分数: ' . $score);
    
    return array(
        'success' => true,
        'message' => '验证通过',
        'score' => $score
    );
}

// ============================================================
// 6. hCaptcha 验证函数
// ============================================================

function verify_hcaptcha($response) {
    $verify_url = 'https://hcaptcha.com/siteverify';
    
    $response_data = wp_remote_post($verify_url, array(
        'body' => array(
            'secret' => HCAPTCHA_SECRET_KEY,
            'response' => $response,
            'remoteip' => $_SERVER['REMOTE_ADDR']
        ),
        'timeout' => 10
    ));
    
    if (is_wp_error($response_data)) {
        error_log('[hCaptcha] 验证请求失败: ' . $response_data->get_error_message());
        return array(
            'success' => false,
            'message' => '验证服务暂时不可用，请稍后重试。'
        );
    }
    
    $response_body = json_decode(wp_remote_retrieve_body($response_data), true);
    
    if (!isset($response_body['success']) || !$response_body['success']) {
        $error_codes = isset($response_body['error-codes']) ? implode(', ', $response_body['error-codes']) : 'unknown';
        error_log('[hCaptcha] 验证失败 - IP: ' . $_SERVER['REMOTE_ADDR'] . ' - 错误: ' . $error_codes);
        
        return array(
            'success' => false,
            'message' => '人机验证失败，请重试。'
        );
    }
    
    // 记录成功的验证
    error_log('[hCaptcha] 验证成功 - IP: ' . $_SERVER['REMOTE_ADDR']);
    
    return array(
        'success' => true,
        'message' => '验证通过'
    );
}

// ============================================================
// 7. 添加验证码样式（可选）
// ============================================================

add_action('wp_head', 'add_captcha_custom_styles');
function add_captcha_custom_styles() {
    ?>
    <style>
    /* 验证码容器样式 */
    .elementor-field-type-captcha {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px 0;
    }
    
    /* Cloudflare Turnstile 样式 */
    .cf-turnstile {
        margin: 0 auto;
    }
    
    /* hCaptcha 样式 */
    .h-captcha {
        margin: 0 auto;
    }
    
    /* reCAPTCHA 提示文字 */
    .elementor-field-type-captcha a {
        color: #667eea;
        text-decoration: none;
    }
    
    .elementor-field-type-captcha a:hover {
        text-decoration: underline;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .elementor-field-type-captcha {
            padding: 10px 0;
        }
        
        .cf-turnstile,
        .h-captcha {
            transform: scale(0.9);
            transform-origin: center;
        }
    }
    </style>
    <?php
}

// ============================================================
// 8. 统计和监控（可选）
// ============================================================

/**
 * 记录验证码验证统计
 */
add_action('elementor_pro/forms/new_record', 'log_captcha_stats', 10, 2);
function log_captcha_stats($record, $ajax_handler) {
    // 获取表单 ID
    $form_id = $record->get_form_settings('id');
    
    // 记录统计信息
    $stats = get_option('captcha_stats', array());
    
    if (!isset($stats[$form_id])) {
        $stats[$form_id] = array(
            'total_submissions' => 0,
            'blocked_submissions' => 0,
            'last_submission' => ''
        );
    }
    
    $stats[$form_id]['total_submissions']++;
    $stats[$form_id]['last_submission'] = current_time('mysql');
    
    update_option('captcha_stats', $stats);
}

/**
 * 在后台显示验证码统计（可选）
 */
add_action('admin_menu', 'add_captcha_stats_page');
function add_captcha_stats_page() {
    add_submenu_page(
        'elementor',
        '验证码统计',
        '验证码统计',
        'manage_options',
        'captcha-stats',
        'display_captcha_stats_page'
    );
}

function display_captcha_stats_page() {
    $stats = get_option('captcha_stats', array());
    ?>
    <div class="wrap">
        <h1>验证码统计</h1>
        <table class="wp-list-table widefat fixed striped">
            <thead>
                <tr>
                    <th>表单 ID</th>
                    <th>总提交次数</th>
                    <th>拦截次数</th>
                    <th>拦截率</th>
                    <th>最后提交时间</th>
                </tr>
            </thead>
            <tbody>
                <?php if (empty($stats)): ?>
                    <tr>
                        <td colspan="5">暂无数据</td>
                    </tr>
                <?php else: ?>
                    <?php foreach ($stats as $form_id => $data): ?>
                        <tr>
                            <td><?php echo esc_html($form_id); ?></td>
                            <td><?php echo esc_html($data['total_submissions']); ?></td>
                            <td><?php echo esc_html($data['blocked_submissions']); ?></td>
                            <td>
                                <?php 
                                $rate = $data['total_submissions'] > 0 
                                    ? round(($data['blocked_submissions'] / $data['total_submissions']) * 100, 2) 
                                    : 0;
                                echo esc_html($rate) . '%';
                                ?>
                            </td>
                            <td><?php echo esc_html($data['last_submission']); ?></td>
                        </tr>
                    <?php endforeach; ?>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
    <?php
}

// ============================================================
// 9. 调试和测试功能（生产环境请删除）
// ============================================================

/**
 * 测试验证码功能
 * 访问：yoursite.com/?test_captcha=1
 */
/*
add_action('init', 'test_captcha_functionality');
function test_captcha_functionality() {
    if (isset($_GET['test_captcha']) && current_user_can('administrator')) {
        echo '<h1>验证码配置测试</h1>';
        
        echo '<h2>当前配置：</h2>';
        echo '<ul>';
        echo '<li>Turnstile: ' . (defined('USE_TURNSTILE') && USE_TURNSTILE ? '✅ 已启用' : '❌ 未启用') . '</li>';
        echo '<li>reCAPTCHA: ' . (defined('USE_RECAPTCHA') && USE_RECAPTCHA ? '✅ 已启用' : '❌ 未启用') . '</li>';
        echo '<li>hCaptcha: ' . (defined('USE_HCAPTCHA') && USE_HCAPTCHA ? '✅ 已启用' : '❌ 未启用') . '</li>';
        echo '</ul>';
        
        echo '<h2>密钥配置：</h2>';
        echo '<ul>';
        if (defined('USE_TURNSTILE') && USE_TURNSTILE) {
            echo '<li>Turnstile Site Key: ' . (strlen(TURNSTILE_SITE_KEY) > 10 ? '✅ 已配置' : '❌ 未配置') . '</li>';
        }
        if (defined('USE_RECAPTCHA') && USE_RECAPTCHA) {
            echo '<li>reCAPTCHA Site Key: ' . (strlen(RECAPTCHA_SITE_KEY) > 10 ? '✅ 已配置' : '❌ 未配置') . '</li>';
        }
        if (defined('USE_HCAPTCHA') && USE_HCAPTCHA) {
            echo '<li>hCaptcha Site Key: ' . (strlen(HCAPTCHA_SITE_KEY) > 10 ? '✅ 已配置' : '❌ 未配置') . '</li>';
        }
        echo '</ul>';
        
        wp_die();
    }
}
*/
