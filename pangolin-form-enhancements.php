<?php
/**
 * Pangolin Interview Form - 增强功能
 * 
 * 将此代码添加到子主题的 functions.php 或使用 Code Snippets 插件
 */

// ============================================
// 1. 自定义 Elementor Form 邮件模板(HTML格式)
// ============================================

add_filter('elementor_pro/forms/email_content', 'pangolin_custom_email_template', 10, 2);

function pangolin_custom_email_template($email_content, $record) {
    // 获取表单字段
    $fields = $record->get('fields');
    
    // 检查是否是访谈申请表单(通过表单ID或字段名称判断)
    if (!isset($fields['company_name'])) {
        return $email_content; // 不是我们的表单,返回原内容
    }
    
    // 提取字段值
    $company_name = isset($fields['company_name']) ? $fields['company_name']['value'] : 'N/A';
    $work_email = isset($fields['work_email']) ? $fields['work_email']['value'] : 'N/A';
    $position = isset($fields['position']) ? $fields['position']['value'] : 'N/A';
    $current_needs = isset($fields['current_needs']) ? $fields['current_needs']['value'] : 'N/A';
    $pain_points = isset($fields['pain_points']) ? $fields['pain_points']['value'] : 'N/A';
    
    // 获取提交信息
    $submission_date = current_time('Y-m-d H:i:s');
    $user_ip = $_SERVER['REMOTE_ADDR'];
    $user_agent = $_SERVER['HTTP_USER_AGENT'];
    
    // HTML 邮件模板
    $html_email = '
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #7c3aed 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .header h1 { margin: 0; font-size: 24px; }
            .content { background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; }
            .section { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; border-left: 4px solid #2563eb; }
            .section h2 { color: #1e3a8a; font-size: 18px; margin-top: 0; }
            .field { margin-bottom: 15px; }
            .field-label { font-weight: 600; color: #4b5563; margin-bottom: 5px; }
            .field-value { color: #1f2937; background: #f3f4f6; padding: 10px; border-radius: 5px; }
            .footer { background: #1f2937; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; }
            .cta-button { display: inline-block; background: #fbbf24; color: #1e3a8a; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 10px; }
            .meta { font-size: 12px; color: #6b7280; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 New Interview Application</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">50% OFF Forever Program</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📋 Company Information</h2>
                    <div class="field">
                        <div class="field-label">Company Name:</div>
                        <div class="field-value">' . esc_html($company_name) . '</div>
                    </div>
                    <div class="field">
                        <div class="field-label">Contact Email:</div>
                        <div class="field-value">' . esc_html($work_email) . '</div>
                    </div>
                    <div class="field">
                        <div class="field-label">Position:</div>
                        <div class="field-value">' . esc_html($position) . '</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>💼 Business Details</h2>
                    <div class="field">
                        <div class="field-label">Current Data Needs:</div>
                        <div class="field-value">' . nl2br(esc_html($current_needs)) . '</div>
                    </div>
                    <div class="field">
                        <div class="field-label">Current Pain Points:</div>
                        <div class="field-value">' . nl2br(esc_html($pain_points)) . '</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📅 Next Steps</h2>
                    <ol style="margin: 10px 0; padding-left: 20px;">
                        <li>Review the application details above</li>
                        <li>Schedule an interview with the applicant</li>
                        <li>Confirm the 50% lifetime discount eligibility</li>
                    </ol>
                    <a href="https://calendly.com/tammy-pangolinfo/customer-interview" class="cta-button">
                        📅 Schedule Interview on Calendly
                    </a>
                </div>
                
                <div class="meta">
                    <strong>Submission Details:</strong><br>
                    📅 Date: ' . esc_html($submission_date) . '<br>
                    🌐 IP Address: ' . esc_html($user_ip) . '<br>
                    💻 User Agent: ' . esc_html($user_agent) . '
                </div>
            </div>
            
            <div class="footer">
                <p style="margin: 0;">Pangolin Interview Application System</p>
                <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.8;">Powered by Elementor Forms + WP Mail SMTP</p>
            </div>
        </div>
    </body>
    </html>
    ';
    
    return $html_email;
}


// ============================================
// 2. 发送确认邮件给申请人
// ============================================

add_action('elementor_pro/forms/new_record', 'pangolin_send_confirmation_email', 10, 2);

function pangolin_send_confirmation_email($record, $handler) {
    // 获取表单字段
    $fields = $record->get('fields');
    
    // 检查是否是访谈申请表单
    if (!isset($fields['company_name'])) {
        return;
    }
    
    $work_email = isset($fields['work_email']) ? $fields['work_email']['value'] : '';
    $company_name = isset($fields['company_name']) ? $fields['company_name']['value'] : '';
    
    if (empty($work_email)) {
        return;
    }
    
    // 邮件主题
    $subject = 'Thank you for your interview application - Pangolin';
    
    // 邮件内容(HTML)
    $message = '
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #7c3aed 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; }
            .cta-button { display: inline-block; background: #fbbf24; color: #1e3a8a; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }
            .footer { background: #1f2937; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Application Received!</h1>
            </div>
            
            <div class="content">
                <p>Dear ' . esc_html($company_name) . ' Team,</p>
                
                <p>Thank you for applying to our <strong>50% OFF Forever</strong> program! We\'re excited to learn more about your data collection needs.</p>
                
                <p><strong>What\'s Next?</strong></p>
                <ol>
                    <li>Our team will review your application within 24 hours</li>
                    <li>We\'ll reach out to schedule a 30-minute interview</li>
                    <li>After the interview, you\'ll receive your lifetime 50% discount code</li>
                </ol>
                
                <p>Want to schedule your interview right away? Click the button below:</p>
                
                <div style="text-align: center;">
                    <a href="https://calendly.com/tammy-pangolinfo/customer-interview" class="cta-button">
                        📅 Schedule Interview Now
                    </a>
                </div>
                
                <p>If you have any questions, feel free to reply to this email.</p>
                
                <p>Best regards,<br>
                <strong>The Pangolin Team</strong></p>
            </div>
            
            <div class="footer">
                <p>© 2025 Pangolin. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    ';
    
    // 邮件头
    $headers = array(
        'Content-Type: text/html; charset=UTF-8',
        'From: Pangolin <noreply@yoursite.com>', // 替换为您的发件邮箱
    );
    
    // 发送邮件(会自动使用 WP Mail SMTP)
    wp_mail($work_email, $subject, $message, $headers);
}


// ============================================
// 3. 保存表单数据到数据库(可选)
// ============================================

add_action('elementor_pro/forms/new_record', 'pangolin_save_form_to_database', 10, 2);

function pangolin_save_form_to_database($record, $handler) {
    global $wpdb;
    
    // 获取表单字段
    $fields = $record->get('fields');
    
    // 检查是否是访谈申请表单
    if (!isset($fields['company_name'])) {
        return;
    }
    
    // 准备数据
    $data = array(
        'company_name' => isset($fields['company_name']) ? $fields['company_name']['value'] : '',
        'work_email' => isset($fields['work_email']) ? $fields['work_email']['value'] : '',
        'position' => isset($fields['position']) ? $fields['position']['value'] : '',
        'current_needs' => isset($fields['current_needs']) ? $fields['current_needs']['value'] : '',
        'pain_points' => isset($fields['pain_points']) ? $fields['pain_points']['value'] : '',
        'submission_date' => current_time('mysql'),
        'ip_address' => $_SERVER['REMOTE_ADDR'],
    );
    
    // 保存到自定义表或使用 WordPress 的 options/postmeta
    // 这里使用 options 作为简单示例
    $submissions = get_option('pangolin_interview_submissions', array());
    $submissions[] = $data;
    update_option('pangolin_interview_submissions', $submissions);
    
    // 或者创建自定义数据库表(需要先创建表结构)
    // $table_name = $wpdb->prefix . 'pangolin_interviews';
    // $wpdb->insert($table_name, $data);
}


// ============================================
// 4. 自定义表单验证消息(英文)
// ============================================

add_filter('elementor_pro/forms/validation/text', 'pangolin_custom_validation_messages', 10, 3);
add_filter('elementor_pro/forms/validation/email', 'pangolin_custom_validation_messages', 10, 3);
add_filter('elementor_pro/forms/validation/textarea', 'pangolin_custom_validation_messages', 10, 3);

function pangolin_custom_validation_messages($validation, $field, $record) {
    // 自定义必填字段提示
    if ($field['required'] && empty($field['value'])) {
        $field_labels = array(
            'company_name' => 'Please enter your company name',
            'work_email' => 'Please enter a valid work email address',
            'position' => 'Please enter your role or position',
            'current_needs' => 'Please describe your current data needs',
            'pain_points' => 'Please describe your current pain points',
        );
        
        $field_id = $field['id'];
        if (isset($field_labels[$field_id])) {
            $validation['error'] = $field_labels[$field_id];
        }
    }
    
    return $validation;
}


// ============================================
// 5. 添加管理后台查看提交记录页面(可选)
// ============================================

add_action('admin_menu', 'pangolin_add_admin_menu');

function pangolin_add_admin_menu() {
    add_menu_page(
        'Interview Applications',
        'Interview Apps',
        'manage_options',
        'pangolin-interviews',
        'pangolin_display_submissions',
        'dashicons-email-alt',
        30
    );
}

function pangolin_display_submissions() {
    $submissions = get_option('pangolin_interview_submissions', array());
    
    echo '<div class="wrap">';
    echo '<h1>Interview Applications</h1>';
    
    if (empty($submissions)) {
        echo '<p>No submissions yet.</p>';
    } else {
        echo '<table class="wp-list-table widefat fixed striped">';
        echo '<thead><tr>';
        echo '<th>Date</th>';
        echo '<th>Company</th>';
        echo '<th>Email</th>';
        echo '<th>Position</th>';
        echo '<th>Actions</th>';
        echo '</tr></thead>';
        echo '<tbody>';
        
        foreach (array_reverse($submissions) as $index => $submission) {
            echo '<tr>';
            echo '<td>' . esc_html($submission['submission_date']) . '</td>';
            echo '<td>' . esc_html($submission['company_name']) . '</td>';
            echo '<td><a href="mailto:' . esc_attr($submission['work_email']) . '">' . esc_html($submission['work_email']) . '</a></td>';
            echo '<td>' . esc_html($submission['position']) . '</td>';
            echo '<td><a href="https://calendly.com/tammy-pangolinfo/customer-interview" target="_blank" class="button">Schedule Interview</a></td>';
            echo '</tr>';
        }
        
        echo '</tbody></table>';
    }
    
    echo '</div>';
}
