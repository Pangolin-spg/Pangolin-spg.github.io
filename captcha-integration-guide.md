# Elementor 表单验证码集成完整指南

## 📋 目录
1. [验证码服务对比](#验证码服务对比)
2. [Google reCAPTCHA v3（最推荐）](#google-recaptcha-v3)
3. [Cloudflare Turnstile（隐私友好）](#cloudflare-turnstile)
4. [hCaptcha（开源替代）](#hcaptcha)
5. [WordPress 插件方案](#wordpress-插件方案)
6. [Elementor Pro 内置方案](#elementor-pro-内置方案)
7. [自定义代码方案](#自定义代码方案)
8. [效果对比与选择建议](#效果对比与选择建议)

---

## 一、验证码服务对比

| 服务 | 免费额度 | 用户体验 | 隐私性 | 推荐度 | 适用场景 |
|------|---------|---------|--------|--------|---------|
| **Google reCAPTCHA v3** | 100万次/月 | ⭐⭐⭐⭐⭐ 无感 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 全球网站 |
| **Cloudflare Turnstile** | 无限制 | ⭐⭐⭐⭐⭐ 无感 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 隐私优先 |
| **hCaptcha** | 无限制 | ⭐⭐⭐⭐ 偶尔需点击 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 开源项目 |
| **Google reCAPTCHA v2** | 100万次/月 | ⭐⭐⭐ 需点击 | ⭐⭐⭐ | ⭐⭐⭐ | 传统网站 |

### 🏆 我的推荐排序：

1. **Cloudflare Turnstile** - 最佳选择（免费无限、隐私友好、用户体验好）
2. **Google reCAPTCHA v3** - 次佳选择（无感验证、但需要 Google 服务）
3. **hCaptcha** - 备选方案（开源、隐私好、但偶尔需要用户交互）

---

## 二、Google reCAPTCHA v3（最推荐）

### ✨ 特点
- ✅ **完全无感**：用户无需任何操作
- ✅ **智能评分**：基于用户行为给出 0-1 分数
- ✅ **免费额度大**：100万次/月
- ✅ **准确率高**：Google AI 驱动
- ❌ **需要 Google 服务**：中国大陆可能受影响

### 📝 接入步骤

#### 步骤 1：注册 reCAPTCHA

1. 访问：https://www.google.com/recaptcha/admin/create
2. 登录 Google 账号
3. 填写信息：
   ```
   标签：Pangolin 官网表单
   reCAPTCHA 类型：reCAPTCHA v3
   域名：pangolinfo.com
         www.pangolinfo.com
   接受服务条款：勾选
   ```
4. 点击"提交"

#### 步骤 2：获取密钥

注册成功后会得到：
```
网站密钥（Site Key）：6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
密钥（Secret Key）：6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
⚠️ **请妥善保存这两个密钥！**

#### 步骤 3：WordPress 集成（三种方案）

##### 方案 A：使用插件（最简单）⭐⭐⭐⭐⭐

**推荐插件：reCAPTCHA for Elementor Forms**

```
1. WordPress 后台 → 插件 → 安装插件
2. 搜索："reCaptcha for Elementor Forms"
3. 安装并启用
4. 设置 → reCAPTCHA
5. 填写：
   - Site Key: [您的网站密钥]
   - Secret Key: [您的密钥]
   - reCAPTCHA Version: v3
6. 保存设置
7. 编辑 Elementor 表单 → Form Fields → 添加 "reCAPTCHA" 字段
8. 保存
```

##### 方案 B：Elementor Pro 内置功能（如果您有 Pro 版）

```
1. 编辑 Elementor 表单
2. 左侧面板 → Form Fields
3. 点击 "+" 添加字段
4. 选择 "reCAPTCHA v3"
5. 在 "Actions After Submit" 中确保启用了 reCAPTCHA 验证
6. Elementor → 设置 → Integrations → reCAPTCHA
7. 填写 Site Key 和 Secret Key
8. 保存
```

##### 方案 C：手动代码集成（高级）

在 `functions.php` 中添加：

```php
/**
 * Google reCAPTCHA v3 集成
 */

// 1. 配置密钥
define('RECAPTCHA_SITE_KEY', '6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
define('RECAPTCHA_SECRET_KEY', '6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');

// 2. 在前台加载 reCAPTCHA 脚本
add_action('wp_enqueue_scripts', 'load_recaptcha_script');
function load_recaptcha_script() {
    // 只在有表单的页面加载
    if (is_page() || is_single()) {
        wp_enqueue_script(
            'google-recaptcha',
            'https://www.google.com/recaptcha/api.js?render=' . RECAPTCHA_SITE_KEY,
            array(),
            null,
            true
        );
    }
}

// 3. 添加 reCAPTCHA 到 Elementor 表单
add_action('elementor_pro/forms/render_field/recaptcha_v3', 'add_recaptcha_v3_field', 10, 3);
function add_recaptcha_v3_field($item, $item_index, $form) {
    ?>
    <input type="hidden" name="g-recaptcha-response" id="g-recaptcha-response">
    <script>
        grecaptcha.ready(function() {
            grecaptcha.execute('<?php echo RECAPTCHA_SITE_KEY; ?>', {action: 'submit'})
            .then(function(token) {
                document.getElementById('g-recaptcha-response').value = token;
            });
        });
    </script>
    <?php
}

// 4. 验证 reCAPTCHA
add_filter('elementor_pro/forms/validation', 'validate_recaptcha_v3', 10, 2);
function validate_recaptcha_v3($record, $ajax_handler) {
    $fields = $record->get('fields');
    
    // 获取 reCAPTCHA token
    $recaptcha_response = isset($_POST['g-recaptcha-response']) ? $_POST['g-recaptcha-response'] : '';
    
    if (empty($recaptcha_response)) {
        $ajax_handler->add_error_message('验证码验证失败，请刷新页面重试。');
        return;
    }
    
    // 验证 token
    $verify_url = 'https://www.google.com/recaptcha/api/siteverify';
    $response = wp_remote_post($verify_url, array(
        'body' => array(
            'secret' => RECAPTCHA_SECRET_KEY,
            'response' => $recaptcha_response,
            'remoteip' => $_SERVER['REMOTE_ADDR']
        )
    ));
    
    if (is_wp_error($response)) {
        $ajax_handler->add_error_message('验证码服务暂时不可用，请稍后重试。');
        return;
    }
    
    $response_body = json_decode(wp_remote_retrieve_body($response), true);
    
    // 检查验证结果
    if (!$response_body['success']) {
        $ajax_handler->add_error_message('验证码验证失败，请重试。');
        return;
    }
    
    // 检查分数（0.5 以上认为是人类）
    if ($response_body['score'] < 0.5) {
        $ajax_handler->add_error_message('您的操作疑似机器人行为，请稍后重试。');
        error_log('reCAPTCHA 低分: ' . $response_body['score'] . ' - IP: ' . $_SERVER['REMOTE_ADDR']);
        return;
    }
}
```

---

## 三、Cloudflare Turnstile（强烈推荐）

### ✨ 特点
- ✅ **完全免费**：无限制使用
- ✅ **隐私友好**：不追踪用户
- ✅ **无感验证**：大多数情况下无需用户操作
- ✅ **速度快**：Cloudflare CDN 加速
- ✅ **中国可用**：不依赖 Google 服务

### 📝 接入步骤

#### 步骤 1：注册 Cloudflare Turnstile

1. 访问：https://dash.cloudflare.com/
2. 登录或注册 Cloudflare 账号
3. 左侧菜单 → Turnstile
4. 点击 "Add Site"
5. 填写信息：
   ```
   Site name: Pangolin 官网
   Domain: pangolinfo.com
   Widget Mode: Managed（推荐）
   ```
6. 点击 "Create"

#### 步骤 2：获取密钥

```
Site Key: 0x4XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Secret Key: 0x4XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### 步骤 3：WordPress 集成

##### 方案 A：使用插件

**推荐插件：Turnstile for Elementor**

```
1. 下载插件（需要手动安装）
   或搜索 "Cloudflare Turnstile" 相关插件
2. 上传并启用
3. 配置 Site Key 和 Secret Key
4. 在 Elementor 表单中添加 Turnstile 字段
```

##### 方案 B：手动代码集成（推荐）

在 `functions.php` 中添加：

```php
/**
 * Cloudflare Turnstile 集成
 */

// 1. 配置密钥
define('TURNSTILE_SITE_KEY', '0x4XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');
define('TURNSTILE_SECRET_KEY', '0x4XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX');

// 2. 加载 Turnstile 脚本
add_action('wp_enqueue_scripts', 'load_turnstile_script');
function load_turnstile_script() {
    if (is_page() || is_single()) {
        wp_enqueue_script(
            'cloudflare-turnstile',
            'https://challenges.cloudflare.com/turnstile/v0/api.js',
            array(),
            null,
            true
        );
    }
}

// 3. 在表单中添加 Turnstile widget
add_action('elementor_pro/forms/render_field/turnstile', 'add_turnstile_field', 10, 3);
function add_turnstile_field($item, $item_index, $form) {
    ?>
    <div class="cf-turnstile" 
         data-sitekey="<?php echo TURNSTILE_SITE_KEY; ?>"
         data-theme="light"
         data-size="normal">
    </div>
    <?php
}

// 4. 验证 Turnstile
add_filter('elementor_pro/forms/validation', 'validate_turnstile', 10, 2);
function validate_turnstile($record, $ajax_handler) {
    $turnstile_response = isset($_POST['cf-turnstile-response']) ? $_POST['cf-turnstile-response'] : '';
    
    if (empty($turnstile_response)) {
        $ajax_handler->add_error_message('请完成人机验证。');
        return;
    }
    
    // 验证 token
    $verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
    $response = wp_remote_post($verify_url, array(
        'body' => array(
            'secret' => TURNSTILE_SECRET_KEY,
            'response' => $turnstile_response,
            'remoteip' => $_SERVER['REMOTE_ADDR']
        )
    ));
    
    if (is_wp_error($response)) {
        $ajax_handler->add_error_message('验证服务暂时不可用，请稍后重试。');
        return;
    }
    
    $response_body = json_decode(wp_remote_retrieve_body($response), true);
    
    if (!$response_body['success']) {
        $ajax_handler->add_error_message('人机验证失败，请重试。');
        error_log('Turnstile 验证失败: ' . print_r($response_body, true));
        return;
    }
}
```

---

## 四、hCaptcha（开源替代）

### ✨ 特点
- ✅ **完全免费**：无限制
- ✅ **隐私友好**：GDPR 合规
- ✅ **开源**：透明可信
- ⚠️ **偶尔需要点击**：用户体验稍差

### 📝 接入步骤

#### 步骤 1：注册 hCaptcha

1. 访问：https://www.hcaptcha.com/
2. 注册账号
3. Dashboard → New Site
4. 填写域名：`pangolinfo.com`
5. 获取 Site Key 和 Secret Key

#### 步骤 2：WordPress 集成

**推荐插件：hCaptcha for WordPress**

```
1. WordPress 后台 → 插件 → 安装插件
2. 搜索："hCaptcha for WordPress"
3. 安装并启用
4. 设置 → hCaptcha
5. 填写 Site Key 和 Secret Key
6. 在 "Integrations" 中勾选 "Elementor Forms"
7. 保存
```

---

## 五、WordPress 插件方案（最简单）

### 🔌 推荐插件组合

#### 方案 1：Advanced Google reCAPTCHA

```
插件名称：Advanced Google reCAPTCHA
功能：支持 v2、v3，自动集成 Elementor
安装：WordPress 后台 → 插件 → 搜索安装

配置步骤：
1. 安装并启用插件
2. 设置 → Advanced reCAPTCHA
3. 选择 reCAPTCHA v3
4. 填写 Site Key 和 Secret Key
5. 在 "Forms" 选项中勾选 "Elementor Forms"
6. 设置阈值分数（推荐 0.5）
7. 保存
```

#### 方案 2：Really Simple CAPTCHA（轻量级）

```
插件名称：Really Simple CAPTCHA
功能：简单的图片验证码，无需第三方服务
适用：不想依赖外部服务的场景

缺点：
- 用户体验较差（需要输入验证码）
- 对机器人防护能力一般
```

---

## 六、Elementor Pro 内置方案

如果您使用 **Elementor Pro**，可以直接使用内置的 reCAPTCHA 功能：

### 配置步骤

```
1. WordPress 后台 → Elementor → 设置 → Integrations
2. 找到 "reCAPTCHA" 部分
3. 选择版本：reCAPTCHA v3（推荐）
4. 填写：
   - Site Key: [您的网站密钥]
   - Secret Key: [您的密钥]
5. 保存

6. 编辑表单：
   - 打开 Elementor 编辑器
   - 选择表单小部件
   - 左侧面板 → Form Fields
   - 点击 "+" 添加字段
   - 选择 "reCAPTCHA v3"
   - 保存

7. 配置验证：
   - 表单设置 → Actions After Submit
   - 确保 "reCAPTCHA" 动作已启用
   - 设置分数阈值（0.5 推荐）
```

---

## 七、自定义代码方案（完整版）

我为您准备了一个完整的、即用的代码方案，支持多种验证码服务。

### 特点
- ✅ 支持 reCAPTCHA v3、Turnstile、hCaptcha
- ✅ 自动检测并加载对应脚本
- ✅ 统一的验证接口
- ✅ 详细的错误日志
- ✅ 支持多语言

**代码文件：** `captcha-integration-code.php`（见下一个文件）

---

## 八、效果对比与选择建议

### 🎯 根据您的需求选择

#### 场景 1：国际网站，追求最佳用户体验
**推荐：Google reCAPTCHA v3**
- 完全无感
- 准确率最高
- 免费额度充足

#### 场景 2：重视隐私，或中国大陆用户较多
**推荐：Cloudflare Turnstile**
- 完全免费无限制
- 不依赖 Google
- 隐私友好
- 速度快

#### 场景 3：开源项目，需要透明度
**推荐：hCaptcha**
- 开源
- 隐私合规
- 免费无限制

#### 场景 4：快速部署，不想写代码
**推荐：WordPress 插件**
- 安装即用
- 可视化配置
- 自动更新

### 📊 防护效果对比

| 验证方式 | 机器人拦截率 | 误杀率 | 用户体验 |
|---------|------------|--------|---------|
| reCAPTCHA v3 | 95%+ | <1% | ⭐⭐⭐⭐⭐ |
| Turnstile | 93%+ | <2% | ⭐⭐⭐⭐⭐ |
| hCaptcha | 90%+ | 3-5% | ⭐⭐⭐⭐ |
| reCAPTCHA v2 | 85%+ | <1% | ⭐⭐⭐ |

---

## 九、我的最终推荐

### 🏆 最佳方案（按优先级）

#### 1️⃣ Cloudflare Turnstile + 插件
```
优势：
✅ 完全免费无限制
✅ 隐私友好
✅ 中国可用
✅ 配置简单

适合：所有网站
```

#### 2️⃣ Google reCAPTCHA v3 + Elementor Pro 内置
```
优势：
✅ 无感验证
✅ 准确率高
✅ 集成简单（如果有 Pro 版）

适合：国际网站，已购买 Elementor Pro
```

#### 3️⃣ Google reCAPTCHA v3 + 插件
```
优势：
✅ 无感验证
✅ 配置简单
✅ 免费额度大

适合：国际网站，没有 Elementor Pro
```

---

## 十、快速开始清单

### ✅ 准备工作
- [ ] 确定使用哪个验证码服务
- [ ] 注册账号并获取密钥
- [ ] 确认是否有 Elementor Pro

### ✅ 实施步骤
- [ ] 安装对应插件或添加代码
- [ ] 配置 Site Key 和 Secret Key
- [ ] 在表单中添加验证码字段
- [ ] 测试表单提交
- [ ] 检查验证是否生效

### ✅ 验证效果
- [ ] 正常提交表单（应该成功）
- [ ] 快速连续提交（应该被拦截）
- [ ] 查看后台日志
- [ ] 监控垃圾表单数量

---

## 十一、常见问题

### ❓ Q1：验证码不显示？
**A：** 检查：
1. Site Key 是否正确
2. 域名是否已添加到验证码服务
3. 浏览器控制台是否有错误
4. 是否被广告拦截器屏蔽

### ❓ Q2：验证总是失败？
**A：** 检查：
1. Secret Key 是否正确
2. 服务器能否访问验证 API
3. 时间是否同步（reCAPTCHA 对时间敏感）

### ❓ Q3：中国大陆用户无法使用 reCAPTCHA？
**A：** 
- 使用 Cloudflare Turnstile 替代
- 或使用 hCaptcha
- 或使用国内验证码服务（如腾讯云、阿里云）

### ❓ Q4：如何调整验证严格程度？
**A：** 
- reCAPTCHA v3：调整分数阈值（0.5 = 中等，0.7 = 严格）
- Turnstile：选择 Managed 或 Non-Interactive 模式
- hCaptcha：在后台调整难度

---

## 需要帮助？

我可以帮您：
1. 选择最适合的验证码方案
2. 直接修改 functions.php 添加验证码
3. 配置和测试验证码功能
4. 排查验证码相关问题
5. 优化验证码的用户体验

请告诉我您想使用哪个方案，我可以提供具体的实施步骤！
