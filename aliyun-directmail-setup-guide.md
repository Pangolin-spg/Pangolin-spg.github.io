# 阿里云邮件推送服务完整配置指南

## 📋 目录
1. [服务介绍与选择](#服务介绍与选择)
2. [开通阿里云邮件推送服务](#开通阿里云邮件推送服务)
3. [配置发信域名](#配置发信域名)
4. [创建发信地址](#创建发信地址)
5. [获取 SMTP 凭证](#获取-smtp-凭证)
6. [WordPress 配置](#wordpress-配置)
7. [测试与验证](#测试与验证)
8. [常见问题排查](#常见问题排查)

---

## 一、服务介绍与选择

### 阿里云提供两种邮件服务：

#### 1️⃣ **阿里云邮件推送（DirectMail）** ⭐ 推荐
- **适用场景**：网站表单通知、系统邮件、营销邮件
- **价格**：
  - 免费额度：每日 200 封（每月 6,000 封）
  - 付费：0.00035 元/封起
- **优势**：
  - ✅ 与阿里云服务器完美兼容
  - ✅ 高送达率（95%+）
  - ✅ 支持 SMTP 和 API 两种方式
  - ✅ 详细的发送统计和日志
- **访问地址**：https://www.aliyun.com/product/directmail

#### 2️⃣ **阿里云企业邮箱**
- **适用场景**：企业日常邮件通信
- **价格**：免费版 5 个账号，付费版 ¥600/年起
- **优势**：专业企业邮箱，品牌形象好
- **访问地址**：https://www.aliyun.com/product/alimail

**本指南重点介绍邮件推送服务（DirectMail）**

---

## 二、开通阿里云邮件推送服务

### 步骤 1：登录阿里云控制台

1. 访问：https://www.aliyun.com/
2. 登录您的阿里云账号
3. 如果是国际版，访问：https://www.alibabacloud.com/

### 步骤 2：开通邮件推送服务

#### 方法 A：通过产品页面开通
```
1. 访问：https://www.aliyun.com/product/directmail
2. 点击"立即开通"
3. 选择地域（建议选择与您服务器相同的地域）
   - 华东1（杭州）
   - 华北2（北京）
   - 华南1（深圳）
   - 新加坡（国际版推荐）
4. 确认开通
```

#### 方法 B：通过控制台搜索
```
1. 登录阿里云控制台
2. 在顶部搜索框输入"邮件推送"
3. 点击"邮件推送 DirectMail"
4. 点击"立即开通"
```

### 步骤 3：实名认证（必需）

如果您的账号未完成实名认证，需要先完成：
```
控制台 → 账号管理 → 实名认证
```

---

## 三、配置发信域名

### 为什么需要配置域名？
- 提高邮件送达率
- 避免被标记为垃圾邮件
- 建立品牌信任度

### 步骤 1：添加发信域名

1. 进入邮件推送控制台
2. 左侧菜单：**发信域名** → **新建域名**
3. 输入您的域名（例如：`pangolinfo.com`）
4. 点击"确定"

### 步骤 2：验证域名所有权

阿里云会要求您添加 DNS 记录来验证域名所有权。

#### 获取验证记录
```
控制台会显示类似以下信息：
记录类型：TXT
主机记录：_dmarc
记录值：v=DMARC1; p=none; rua=mailto:dmarc@example.com
```

#### 添加 DNS 记录

**如果您的域名在阿里云：**
```
1. 进入"云解析 DNS"控制台
2. 找到您的域名 → 点击"解析设置"
3. 点击"添加记录"
4. 按照阿里云提供的信息填写：
   - 记录类型：TXT
   - 主机记录：（阿里云提供的值）
   - 记录值：（阿里云提供的值）
   - TTL：默认 10 分钟
5. 点击"确认"
```

**如果您的域名在其他服务商（如 Cloudflare、GoDaddy）：**
```
1. 登录您的域名服务商控制台
2. 找到 DNS 管理
3. 添加 TXT 记录
4. 填写阿里云提供的主机记录和记录值
5. 保存
```

#### 验证 DNS 记录

```bash
# 在终端运行以下命令检查 DNS 是否生效
dig TXT _dmarc.pangolinfo.com

# 或使用
nslookup -type=TXT _dmarc.pangolinfo.com
```

### 步骤 3：配置 SPF 记录（提高送达率）

SPF 记录用于防止邮件被伪造。

**添加 SPF 记录：**
```
记录类型：TXT
主机记录：@
记录值：v=spf1 include:spf.aliyundm.com -all
TTL：10 分钟
```

### 步骤 4：配置 DKIM 记录（可选但推荐）

DKIM 用于邮件签名验证。

**在邮件推送控制台获取 DKIM 记录：**
```
发信域名 → 选择您的域名 → 查看 DKIM 配置
```

**添加 DKIM 记录：**
```
记录类型：TXT
主机记录：（阿里云提供，通常是 default._domainkey）
记录值：（阿里云提供的公钥）
TTL：10 分钟
```

### 步骤 5：等待验证通过

```
1. 返回邮件推送控制台
2. 点击"验证"按钮
3. 等待 DNS 生效（通常 10 分钟 - 24 小时）
4. 验证通过后，状态会变为"验证通过"
```

---

## 四、创建发信地址

### 步骤 1：新建发信地址

```
1. 邮件推送控制台 → 发信地址 → 新建发信地址
2. 填写信息：
   - 发信地址：noreply@pangolinfo.com
     （可以是 noreply、info、contact 等）
   - 发件人名称：Pangolin 官网
     （这是收件人看到的发件人名称）
   - 选择域名：pangolinfo.com
   - 回信地址：（可选）如果需要接收回复，填写真实邮箱
3. 点击"确定"
```

### 步骤 2：记录发信地址

创建成功后，记录以下信息（后续配置需要）：
```
发信地址：noreply@pangolinfo.com
发件人名称：Pangolin 官网
```

---

## 五、获取 SMTP 凭证

### 步骤 1：创建 SMTP 密码

```
1. 邮件推送控制台 → SMTP 服务 → SMTP 密码
2. 点击"新建 SMTP 密码"
3. 选择发信地址：noreply@pangolinfo.com
4. 点击"确定"
5. ⚠️ 重要：立即复制并保存密码（只显示一次！）
```

### 步骤 2：记录 SMTP 配置信息

根据您选择的地域，SMTP 服务器地址不同：

| 地域 | SMTP 服务器地址 | 端口 |
|------|----------------|------|
| 华东1（杭州） | smtpdm.aliyun.com | 25, 80, 465 |
| 华北2（北京） | smtpdm.aliyun.com | 25, 80, 465 |
| 华南1（深圳） | smtpdm.aliyun.com | 25, 80, 465 |
| 新加坡 | smtpdm-ap-southeast-1.aliyun.com | 25, 80, 465 |
| 悉尼 | smtpdm-ap-southeast-2.aliyun.com | 25, 80, 465 |

**完整配置信息：**
```
SMTP 服务器：smtpdm.aliyun.com
SMTP 端口：
  - 25（无加密，可能被阿里云封禁）
  - 80（无加密）
  - 465（SSL 加密，推荐）
加密方式：SSL/TLS
SMTP 用户名：noreply@pangolinfo.com
SMTP 密码：[您刚才创建的密码]
```

---

## 六、WordPress 配置

### 方案 A：使用 WP Mail SMTP 插件（推荐）

#### 1. 安装插件

```
WordPress 后台 → 插件 → 安装插件
搜索："WP Mail SMTP"
安装并启用
```

#### 2. 配置插件

```
WordPress 后台 → WP Mail SMTP → Settings

【General 标签】
From Email: noreply@pangolinfo.com
From Name: Pangolin 官网
Force From Email: 勾选
Force From Name: 勾选

【Mailer 标签】
选择：Other SMTP

【Other SMTP 配置】
SMTP Host: smtpdm.aliyun.com
Encryption: SSL
SMTP Port: 465
Auto TLS: 关闭
Authentication: 开启
SMTP Username: noreply@pangolinfo.com
SMTP Password: [您的 SMTP 密码]

点击 "Save Settings"
```

#### 3. 发送测试邮件

```
WP Mail SMTP → Email Test
输入您的邮箱地址
点击 "Send Email"
检查是否收到测试邮件
```

### 方案 B：使用 Post SMTP 插件（备选）

#### 1. 安装插件

```
WordPress 后台 → 插件 → 安装插件
搜索："Post SMTP Mailer"
安装并启用
```

#### 2. 配置向导

```
1. 启用后会自动启动配置向导
2. 选择 "I'll configure it myself"
3. 填写信息：
   - Sender Email: noreply@pangolinfo.com
   - Sender Name: Pangolin 官网
4. 选择 Transport: SMTP
5. 填写 SMTP 信息：
   - Outgoing Mail Server: smtpdm.aliyun.com
   - Port: 465
   - Security: SSL
   - Authentication: Plain
   - Username: noreply@pangolinfo.com
   - Password: [您的 SMTP 密码]
6. 完成配置
```

### 方案 C：直接在 functions.php 中配置（高级）

如果您不想使用插件，可以直接在 `functions.php` 中添加代码：

```php
/**
 * 配置 WordPress 使用阿里云邮件推送 SMTP
 */
add_action('phpmailer_init', 'configure_aliyun_smtp');
function configure_aliyun_smtp($phpmailer) {
    $phpmailer->isSMTP();
    $phpmailer->Host       = 'smtpdm.aliyun.com';
    $phpmailer->SMTPAuth   = true;
    $phpmailer->Port       = 465;
    $phpmailer->Username   = 'noreply@pangolinfo.com'; // 替换为您的发信地址
    $phpmailer->Password   = 'YOUR_SMTP_PASSWORD';      // 替换为您的 SMTP 密码
    $phpmailer->SMTPSecure = 'ssl';
    $phpmailer->From       = 'noreply@pangolinfo.com'; // 替换为您的发信地址
    $phpmailer->FromName   = 'Pangolin 官网';          // 替换为您的发件人名称
    
    // 调试模式（可选，生产环境请删除）
    // $phpmailer->SMTPDebug = 2;
}

/**
 * 设置默认发件人邮箱
 */
add_filter('wp_mail_from', 'custom_wp_mail_from');
function custom_wp_mail_from($original_email_address) {
    return 'noreply@pangolinfo.com'; // 替换为您的发信地址
}

/**
 * 设置默认发件人名称
 */
add_filter('wp_mail_from_name', 'custom_wp_mail_from_name');
function custom_wp_mail_from_name($original_email_from) {
    return 'Pangolin 官网'; // 替换为您的发件人名称
}
```

---

## 七、测试与验证

### 1. WordPress 测试邮件

使用 WP Mail SMTP 的测试功能：
```
WP Mail SMTP → Email Test
输入您的邮箱
发送测试邮件
```

### 2. Elementor 表单测试

```
1. 编辑您的 Elementor 表单
2. 进入 "Actions After Submit"
3. 确保 "Email" 动作已启用
4. 配置邮件接收地址
5. 保存并在前台测试提交表单
6. 检查是否收到邮件
```

### 3. 检查发送日志

#### WP Mail SMTP 日志
```
安装 "WP Mail Logging" 插件
WordPress 后台 → WP Mail Log
查看所有邮件发送记录
```

#### 阿里云控制台日志
```
邮件推送控制台 → 发送统计
查看发送成功率、失败原因等
```

### 4. 检查垃圾邮件箱

如果没收到邮件，检查：
- ✅ 垃圾邮件箱
- ✅ 促销邮件标签（Gmail）
- ✅ 所有邮件

---

## 八、常见问题排查

### ❌ 问题 1：无法连接到 SMTP 服务器

**可能原因：**
- 阿里云服务器封禁了 25 端口
- 防火墙拦截

**解决方案：**
```bash
# 1. 测试端口连通性
telnet smtpdm.aliyun.com 465

# 2. 如果 465 端口无法连接，尝试 80 端口
# 在 WP Mail SMTP 中修改：
Port: 80
Encryption: None 或 TLS
```

### ❌ 问题 2：SMTP 认证失败

**可能原因：**
- SMTP 密码错误
- 用户名格式错误

**解决方案：**
```
1. 重新生成 SMTP 密码
   邮件推送控制台 → SMTP 服务 → SMTP 密码 → 重置密码
2. 确认用户名是完整的邮箱地址（如 noreply@pangolinfo.com）
3. 确认没有多余的空格
```

### ❌ 问题 3：邮件发送成功但未收到

**可能原因：**
- 被标记为垃圾邮件
- SPF/DKIM 配置不正确

**解决方案：**
```
1. 检查 SPF 记录是否正确
   dig TXT pangolinfo.com
   应该看到：v=spf1 include:spf.aliyundm.com -all

2. 检查 DKIM 记录
   dig TXT default._domainkey.pangolinfo.com

3. 在阿里云控制台查看发送日志
   邮件推送 → 发送统计 → 查看详情

4. 使用邮件测试工具
   访问：https://www.mail-tester.com/
   发送邮件到提供的地址
   查看评分和建议
```

### ❌ 问题 4：发送频率受限

**可能原因：**
- 超过免费额度（200 封/天）
- 触发反垃圾邮件机制

**解决方案：**
```
1. 检查当日发送量
   邮件推送控制台 → 发送统计

2. 升级到付费版本
   邮件推送控制台 → 资源包管理 → 购买资源包

3. 优化发送频率
   - 避免短时间内大量发送
   - 使用队列机制
```

### ❌ 问题 5：Elementor 表单不发送邮件

**可能原因：**
- Elementor 表单配置错误
- WordPress 邮件功能被禁用

**解决方案：**
```
1. 检查 Elementor 表单设置
   编辑表单 → Actions After Submit → Email
   确保：
   - "Email" 动作已启用
   - "To" 字段填写了正确的邮箱
   - "From Email" 使用 [email] 或留空

2. 启用 WP Mail Logging 插件
   查看是否有邮件发送记录

3. 检查 functions.php 是否有冲突代码
   临时禁用自定义邮件配置测试

4. 使用 Elementor 的调试模式
   wp-config.php 中添加：
   define('ELEMENTOR_DEBUG', true);
```

---

## 九、进阶优化

### 1. 启用邮件日志

安装 **WP Mail Logging** 插件：
```
WordPress 后台 → 插件 → 安装插件
搜索："WP Mail Logging"
安装并启用
```

### 2. 配置邮件队列（高流量网站）

安装 **WP Mail Queue** 插件：
```
WordPress 后台 → 插件 → 安装插件
搜索："WP Mail Queue"
安装并启用
配置：每分钟发送 10 封邮件
```

### 3. 设置邮件模板

美化 Elementor 表单邮件：
```php
// 在 functions.php 中添加
add_filter('wp_mail_content_type', 'set_html_content_type');
function set_html_content_type() {
    return 'text/html';
}

// 自定义邮件模板
add_filter('wp_mail', 'custom_email_template');
function custom_email_template($args) {
    if (strpos($args['subject'], 'Elementor') !== false) {
        $args['message'] = '
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #f9f9f9; padding: 30px; border-radius: 10px;">
                <h2 style="color: #0c254b;">新的表单提交</h2>
                <div style="background: white; padding: 20px; border-radius: 5px;">
                    ' . $args['message'] . '
                </div>
                <p style="color: #999; font-size: 12px; margin-top: 20px;">
                    此邮件由 Pangolin 官网自动发送
                </p>
            </div>
        </body>
        </html>';
    }
    return $args;
}
```

### 4. 监控发送状态

在 `functions.php` 中添加错误日志：
```php
// 记录邮件发送失败
add_action('wp_mail_failed', 'log_mail_errors');
function log_mail_errors($wp_error) {
    error_log('邮件发送失败: ' . $wp_error->get_error_message());
}
```

---

## 十、完整配置检查清单

### ✅ 阿里云控制台
- [ ] 邮件推送服务已开通
- [ ] 发信域名已添加并验证通过
- [ ] SPF 记录已配置
- [ ] DKIM 记录已配置（可选）
- [ ] 发信地址已创建
- [ ] SMTP 密码已生成并保存

### ✅ DNS 配置
- [ ] TXT 记录（域名验证）已添加
- [ ] SPF 记录已添加
- [ ] DKIM 记录已添加
- [ ] DNS 已生效（可通过 dig 命令验证）

### ✅ WordPress 配置
- [ ] WP Mail SMTP 插件已安装并配置
- [ ] SMTP 设置正确（服务器、端口、加密方式）
- [ ] 发件人信息已设置
- [ ] 测试邮件发送成功

### ✅ Elementor 表单
- [ ] Email 动作已启用
- [ ] 接收邮箱地址正确
- [ ] 表单提交测试成功
- [ ] 邮件接收成功

---

## 十一、需要帮助？

如果您在配置过程中遇到问题，我可以：

1. **帮您修改 functions.php**
   - 添加 SMTP 配置代码
   - 优化邮件发送逻辑

2. **提供自定义代码**
   - 邮件模板美化
   - 发送日志记录
   - 错误处理

3. **排查具体问题**
   - 查看错误日志
   - 测试 SMTP 连接
   - 检查 DNS 配置

请告诉我您需要哪方面的帮助！

---

## 附录：快速参考

### 阿里云 SMTP 服务器地址

| 地域 | SMTP 地址 |
|------|-----------|
| 中国大陆 | smtpdm.aliyun.com |
| 新加坡 | smtpdm-ap-southeast-1.aliyun.com |
| 悉尼 | smtpdm-ap-southeast-2.aliyun.com |
| 法兰克福 | smtpdm-eu-central-1.aliyun.com |

### 推荐端口

| 端口 | 加密方式 | 推荐度 |
|------|---------|--------|
| 465 | SSL | ⭐⭐⭐⭐⭐ |
| 587 | TLS | ⭐⭐⭐⭐ |
| 80 | 无/TLS | ⭐⭐⭐ |
| 25 | 无 | ❌ 不推荐 |

### 有用的命令

```bash
# 测试 SMTP 端口
telnet smtpdm.aliyun.com 465

# 检查 SPF 记录
dig TXT pangolinfo.com

# 检查 DKIM 记录
dig TXT default._domainkey.pangolinfo.com

# 查看 WordPress 错误日志
tail -f wp-content/debug.log
```
