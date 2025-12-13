# 验证码快速入门指南 - 5 分钟搞定

## 🎯 推荐方案：Cloudflare Turnstile

**为什么选择 Turnstile？**
- ✅ 完全免费，无限制
- ✅ 用户体验好，大多数情况下无感
- ✅ 隐私友好，不追踪用户
- ✅ 中国大陆可用
- ✅ 配置简单

---

## 📝 5 步完成配置

### 第 1 步：注册 Cloudflare Turnstile（2 分钟）

1. 访问：https://dash.cloudflare.com/
2. 注册或登录 Cloudflare 账号
3. 左侧菜单找到 **Turnstile**
4. 点击 **"Add Site"**
5. 填写信息：
   ```
   Site name: Pangolin 官网
   Domain: pangolinfo.com
   Widget Mode: Managed（推荐）
   ```
6. 点击 **"Create"**

### 第 2 步：获取密钥（30 秒）

创建成功后，您会看到：
```
Site Key: 0x4AAAAAAA...（复制这个）
Secret Key: 0x4AAAAAAA...（复制这个）
```

⚠️ **请妥善保存这两个密钥！**

### 第 3 步：修改配置代码（1 分钟）

1. 打开文件：`captcha-integration-code.php`
2. 找到配置区域（第 18-20 行）
3. 替换密钥：
   ```php
   define('TURNSTILE_SITE_KEY', '粘贴您的 Site Key');
   define('TURNSTILE_SECRET_KEY', '粘贴您的 Secret Key');
   define('USE_TURNSTILE', true); // 确保是 true
   ```
4. 确保其他验证码服务是关闭的：
   ```php
   define('USE_RECAPTCHA', false);
   define('USE_HCAPTCHA', false);
   ```

### 第 4 步：添加到 functions.php（1 分钟）

1. 打开 `functions.php`
2. 滚动到文件底部（在 `?>` 之前）
3. 复制 `captcha-integration-code.php` 的全部内容
4. 粘贴到 `functions.php` 底部
5. 保存文件

### 第 5 步：测试（30 秒）

1. 访问您的网站表单页面
2. 刷新页面
3. 您应该会看到验证码出现在表单底部
4. 填写表单并提交
5. 检查是否成功提交

---

## ✅ 验证是否生效

### 方法 1：查看页面源代码
```
1. 打开表单页面
2. 右键 → 查看网页源代码
3. 搜索 "turnstile"
4. 如果找到相关代码，说明已加载
```

### 方法 2：浏览器控制台
```
1. 打开表单页面
2. 按 F12 打开开发者工具
3. 切换到 "Console" 标签
4. 刷新页面
5. 不应该有错误信息
```

### 方法 3：实际测试
```
1. 正常填写表单并提交 → 应该成功
2. 快速连续提交多次 → 应该被拦截
3. 使用自动化工具提交 → 应该被拦截
```

---

## 🎨 自定义样式（可选）

如果您想调整验证码的外观：

### 修改主题
在代码中找到：
```php
data-theme="light"
```
可以改为：
- `light` - 浅色主题
- `dark` - 深色主题
- `auto` - 自动适应

### 修改大小
在代码中找到：
```php
data-size="normal"
```
可以改为：
- `normal` - 正常大小（推荐）
- `compact` - 紧凑模式

### 修改位置
在代码中找到：
```css
.elementor-field-type-captcha {
    justify-content: center; /* 居中 */
}
```
可以改为：
- `flex-start` - 左对齐
- `center` - 居中
- `flex-end` - 右对齐

---

## 🔧 常见问题

### ❓ 验证码不显示？

**检查清单：**
- [ ] Site Key 是否正确填写？
- [ ] 域名是否添加到 Turnstile？
- [ ] `USE_TURNSTILE` 是否设置为 `true`？
- [ ] 代码是否正确添加到 `functions.php`？
- [ ] 是否清除了缓存？

**解决方法：**
```
1. 清除浏览器缓存
2. 清除 WordPress 缓存（如果使用了缓存插件）
3. 检查浏览器控制台是否有错误
4. 确认域名拼写正确（不要加 http:// 或 https://）
```

### ❓ 验证总是失败？

**检查清单：**
- [ ] Secret Key 是否正确？
- [ ] 服务器能否访问 Cloudflare API？
- [ ] 是否有防火墙拦截？

**解决方法：**
```
1. 重新生成密钥
2. 检查服务器网络连接
3. 查看 WordPress 错误日志
```

### ❓ 如何查看错误日志？

**启用 WordPress 调试：**

在 `wp-config.php` 中添加：
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

然后查看：`wp-content/debug.log`

### ❓ 中国大陆用户能用吗？

**可以！** Cloudflare Turnstile 在中国大陆可以正常使用，不像 Google reCAPTCHA 需要翻墙。

---

## 🚀 进阶配置

### 1. 只在特定表单启用验证码

修改代码中的 `add_captcha_to_elementor_form` 函数：

```php
add_action('elementor_pro/forms/render/item', 'add_captcha_to_elementor_form', 10, 3);
function add_captcha_to_elementor_form($item, $item_index, $form) {
    // 只在特定表单 ID 启用（例如：表单 ID 为 12345）
    $form_id = $form->get_id();
    $enabled_forms = array('12345', '67890'); // 添加您的表单 ID
    
    if (!in_array($form_id, $enabled_forms)) {
        return;
    }
    
    // ... 其余代码保持不变
}
```

### 2. 调整验证严格程度

Turnstile 有三种模式：

**在 Cloudflare 后台调整：**
```
Dashboard → Turnstile → 选择您的站点 → Settings
Widget Mode:
- Managed（推荐）：自动调整难度
- Non-Interactive：完全无感，但可能误放
- Invisible：隐藏式，需要代码调整
```

### 3. 添加多语言支持

修改代码中的语言设置：

```php
data-language="<?php echo function_exists('pll_current_language') ? pll_current_language() : 'zh'; ?>"
```

支持的语言代码：
- `zh` - 中文
- `en` - 英文
- `ja` - 日语
- `ko` - 韩语
- 等等...

---

## 📊 监控效果

### 查看拦截统计

代码中已包含统计功能：

```
WordPress 后台 → Elementor → 验证码统计
```

您可以看到：
- 总提交次数
- 拦截次数
- 拦截率
- 最后提交时间

### 查看详细日志

在 `wp-content/debug.log` 中搜索：
```
[Turnstile]
```

您会看到类似：
```
[Turnstile] 验证成功 - IP: 123.456.789.0
[Turnstile] 验证失败 - IP: 111.222.333.444 - 错误: timeout-or-duplicate
```

---

## 🎁 额外福利：备用方案

如果 Turnstile 不适合您，这里有备用方案：

### 方案 B：Google reCAPTCHA v3

**优势：** 完全无感，准确率高
**劣势：** 中国大陆可能无法访问

**快速切换：**
```php
// 在配置区域修改：
define('USE_TURNSTILE', false);  // 关闭 Turnstile
define('USE_RECAPTCHA', true);   // 启用 reCAPTCHA
```

**注册地址：** https://www.google.com/recaptcha/admin/create

### 方案 C：hCaptcha

**优势：** 开源，隐私友好
**劣势：** 偶尔需要用户点击

**快速切换：**
```php
// 在配置区域修改：
define('USE_TURNSTILE', false);  // 关闭 Turnstile
define('USE_HCAPTCHA', true);    // 启用 hCaptcha
```

**注册地址：** https://www.hcaptcha.com/

---

## 💡 最佳实践

### 1. 定期检查统计数据
```
每周查看一次验证码统计
关注拦截率是否正常（通常 5-20%）
如果拦截率过高，可能需要调整设置
```

### 2. 监控用户反馈
```
如果用户反馈验证码太难
可以在 Cloudflare 后台调整为更宽松的模式
```

### 3. 保持密钥安全
```
不要将密钥提交到公开的代码仓库
定期更换密钥（建议每 6 个月）
如果怀疑密钥泄露，立即重新生成
```

### 4. 备份配置
```
保存一份密钥的备份
记录配置的日期和版本
```

---

## 🆘 需要帮助？

如果您在配置过程中遇到任何问题：

1. **检查文档**：先查看 `captcha-integration-guide.md`
2. **查看日志**：启用调试模式查看错误信息
3. **测试连接**：确认服务器能访问 Cloudflare API
4. **联系我**：提供具体的错误信息，我可以帮您排查

---

## ✨ 总结

您现在应该已经成功配置了验证码！

**配置完成后，您的表单将：**
- ✅ 自动拦截机器人提交
- ✅ 保持良好的用户体验
- ✅ 减少垃圾邮件
- ✅ 节省处理时间

**下一步建议：**
1. 监控几天，查看拦截效果
2. 根据统计数据调整设置
3. 配置邮件推送服务（如果还没配置）

祝您使用愉快！🎉
