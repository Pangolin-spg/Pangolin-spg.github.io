/**
 * =================================================================
 * 阿里云邮件推送 SMTP 配置
 * =================================================================
 * 使用说明：
 * 1. 将此代码添加到 functions.php 的底部（在 ?> 之前）
 * 2. 替换下方的配置信息为您的实际信息
 * 3. 保存文件
 * 4. 测试邮件发送功能
 * 
 * 注意：如果您使用了 WP Mail SMTP 插件，请不要同时使用此代码
 */

/**
 * 配置 WordPress 使用阿里云邮件推送 SMTP
 */
add_action('phpmailer_init', 'configure_aliyun_directmail_smtp');
function configure_aliyun_directmail_smtp($phpmailer) {
    // ============ 配置区域 - 请修改以下信息 ============
    
    // SMTP 服务器地址（根据您的地域选择）
    // 中国大陆：smtpdm.aliyun.com
    // 新加坡：smtpdm-ap-southeast-1.aliyun.com
    // 悉尼：smtpdm-ap-southeast-2.aliyun.com
    $smtp_host = 'smtpdm.aliyun.com';
    
    // SMTP 端口（推荐 465）
    // 465 = SSL 加密（推荐）
    // 587 = TLS 加密
    // 80 = 无加密或 TLS
    $smtp_port = 465;
    
    // 加密方式（与端口对应）
    // 'ssl' = 使用 465 端口
    // 'tls' = 使用 587 端口
    // '' = 使用 80 端口（无加密）
    $smtp_secure = 'ssl';
    
    // SMTP 用户名（您在阿里云创建的发信地址）
    $smtp_username = 'noreply@pangolinfo.com';
    
    // SMTP 密码（在阿里云邮件推送控制台生成的 SMTP 密码）
    $smtp_password = 'YOUR_SMTP_PASSWORD_HERE';
    
    // 发件人邮箱（通常与 SMTP 用户名相同）
    $from_email = 'noreply@pangolinfo.com';
    
    // 发件人名称（收件人看到的发件人名称）
    $from_name = 'Pangolin 官网';
    
    // ============ 配置区域结束 ============
    
    // 应用配置
    $phpmailer->isSMTP();
    $phpmailer->Host       = $smtp_host;
    $phpmailer->SMTPAuth   = true;
    $phpmailer->Port       = $smtp_port;
    $phpmailer->Username   = $smtp_username;
    $phpmailer->Password   = $smtp_password;
    $phpmailer->SMTPSecure = $smtp_secure;
    $phpmailer->From       = $from_email;
    $phpmailer->FromName   = $from_name;
    $phpmailer->CharSet    = 'UTF-8';
    
    // 调试模式（可选）
    // 如果遇到问题，取消下面两行的注释以启用调试
    // $phpmailer->SMTPDebug = 2; // 1 = 错误和消息, 2 = 消息, 3 = 详细信息
    // $phpmailer->Debugoutput = 'error_log'; // 输出到 PHP 错误日志
}

/**
 * 设置默认发件人邮箱
 * 防止 WordPress 使用 wordpress@yourdomain.com
 */
add_filter('wp_mail_from', 'aliyun_mail_from');
function aliyun_mail_from($original_email_address) {
    // 替换为您的发信地址
    return 'noreply@pangolinfo.com';
}

/**
 * 设置默认发件人名称
 */
add_filter('wp_mail_from_name', 'aliyun_mail_from_name');
function aliyun_mail_from_name($original_email_from) {
    // 替换为您的发件人名称
    return 'Pangolin 官网';
}

/**
 * 记录邮件发送失败的错误（可选）
 * 错误日志位置：wp-content/debug.log
 * 需要在 wp-config.php 中启用调试模式
 */
add_action('wp_mail_failed', 'log_aliyun_mail_errors');
function log_aliyun_mail_errors($wp_error) {
    $error_message = $wp_error->get_error_message();
    error_log('[阿里云邮件推送] 邮件发送失败: ' . $error_message);
    
    // 如果需要，也可以记录更详细的信息
    error_log('[阿里云邮件推送] 错误详情: ' . print_r($wp_error, true));
}

/**
 * 设置邮件内容类型为 HTML（可选）
 * 如果您想发送 HTML 格式的邮件，取消下面的注释
 */
// add_filter('wp_mail_content_type', 'aliyun_mail_content_type');
// function aliyun_mail_content_type() {
//     return 'text/html';
// }

/**
 * 自定义 Elementor 表单邮件模板（可选）
 * 美化从 Elementor 表单发送的邮件
 */
/*
add_filter('wp_mail', 'customize_elementor_email_template');
function customize_elementor_email_template($args) {
    // 只处理包含 "Elementor" 或特定关键词的邮件
    if (strpos($args['subject'], 'Elementor') !== false || 
        strpos($args['subject'], '表单') !== false) {
        
        // 获取原始邮件内容
        $original_message = $args['message'];
        
        // 包装为 HTML 模板
        $args['message'] = '
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, sans-serif; background-color: #f5f5f5;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <!-- 头部 -->
                            <tr>
                                <td style="padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px 10px 0 0;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">
                                        📬 新的表单提交
                                    </h1>
                                </td>
                            </tr>
                            
                            <!-- 内容 -->
                            <tr>
                                <td style="padding: 40px 30px;">
                                    <div style="background-color: #f9fafb; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                                        ' . nl2br($original_message) . '
                                    </div>
                                </td>
                            </tr>
                            
                            <!-- 页脚 -->
                            <tr>
                                <td style="padding: 20px 30px; background-color: #f9fafb; border-radius: 0 0 10px 10px; text-align: center;">
                                    <p style="margin: 0; color: #6b7280; font-size: 12px;">
                                        此邮件由 <strong>Pangolin 官网</strong> 自动发送<br>
                                        发送时间：' . date('Y-m-d H:i:s') . '
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>';
        
        // 确保使用 HTML 内容类型
        add_filter('wp_mail_content_type', function() {
            return 'text/html';
        });
    }
    
    return $args;
}
*/

/**
 * 测试邮件发送功能（仅用于调试）
 * 访问：yoursite.com/?test_aliyun_email=1
 * 测试完成后请删除此代码
 */
/*
add_action('init', 'test_aliyun_email_sending');
function test_aliyun_email_sending() {
    if (isset($_GET['test_aliyun_email']) && current_user_can('administrator')) {
        $to = 'your-test-email@example.com'; // 替换为您的测试邮箱
        $subject = '阿里云邮件推送测试 - ' . date('Y-m-d H:i:s');
        $message = '
            <h2>测试邮件</h2>
            <p>如果您收到这封邮件，说明阿里云邮件推送配置成功！</p>
            <ul>
                <li>发送时间：' . date('Y-m-d H:i:s') . '</li>
                <li>网站：' . get_bloginfo('name') . '</li>
                <li>URL：' . home_url() . '</li>
            </ul>
        ';
        
        $headers = array('Content-Type: text/html; charset=UTF-8');
        
        $result = wp_mail($to, $subject, $message, $headers);
        
        if ($result) {
            wp_die('✅ 测试邮件发送成功！请检查您的邮箱（包括垃圾邮件箱）。<br><a href="' . home_url() . '">返回首页</a>');
        } else {
            wp_die('❌ 测试邮件发送失败！请检查配置和错误日志。<br><a href="' . home_url() . '">返回首页</a>');
        }
    }
}
*/
