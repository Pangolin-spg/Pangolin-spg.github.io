# 修复 WordPress "nonce_failure" 错误

## 🎯 问题说明

当您在 WordPress 后台编辑 `functions.php` 时，保存时出现 "nonce_failure" 错误。

### 什么是 Nonce？
Nonce（Number used ONCE）是 WordPress 的安全机制，用于验证请求的有效性。默认情况下，nonce 的有效期是 12 小时。

### 为什么会出现这个错误？
1. **编辑时间过长** - 超过了 nonce 的有效期
2. **浏览器缓存** - 浏览器缓存了旧的 nonce
3. **会话过期** - WordPress 会话已过期
4. **文件太大** - `functions.php` 文件过大，保存超时

---

## ✅ 解决方案

### 方案 1：通过 FTP/文件管理器上传（推荐）

这是最安全、最可靠的方法。

#### 步骤 1：准备文件
1. 在本地保存好修改后的 `functions.php`
2. 备份原文件（重要！）

#### 步骤 2：连接服务器
使用 FTP 客户端（如 FileZilla）或主机提供的文件管理器

#### 步骤 3：找到文件
```
/wp-content/themes/您的主题名称/functions.php
```

如果是子主题：
```
/wp-content/themes/您的子主题名称/functions.php
```

#### 步骤 4：上传文件
1. 下载原文件作为备份
2. 上传修改后的文件
3. 覆盖原文件

#### 步骤 5：验证
1. 访问网站
2. 检查是否正常工作
3. 查看横幅是否显示

---

### 方案 2：使用 Code Snippets 插件（最佳实践）

不直接编辑 `functions.php`，而是使用插件管理代码。

#### 步骤 1：安装插件
1. 在 WordPress 后台
2. **插件 → 安装插件**
3. 搜索 **Code Snippets** 或 **WPCode**
4. 安装并激活

#### 步骤 2：创建代码片段
1. **Snippets → Add New**
2. 输入标题：`Pangolin Top Banner`
3. 粘贴横幅代码
4. 设置运行位置：**Run everywhere**
5. 激活代码片段

#### 步骤 3：从 functions.php 中移除代码
1. 编辑 `functions.php`
2. 删除横幅相关代码
3. 保存

**优点：**
- ✅ 不会因为 nonce 失败
- ✅ 更安全（不直接编辑主题文件）
- ✅ 更新主题时不会丢失代码
- ✅ 可以轻松启用/禁用代码

---

### 方案 3：增加 Nonce 有效期

如果您坚持在 WordPress 后台编辑。

#### 步骤 1：编辑 wp-config.php
通过 FTP 或文件管理器打开 `wp-config.php`

#### 步骤 2：添加代码
在 `/* That's all, stop editing! Happy publishing. */` 之前添加：

```php
// 增加 nonce 有效期为 24 小时
define('NONCE_LIFE', 86400);
```

#### 步骤 3：清除缓存
1. 清除浏览器缓存
2. 清除 WordPress 缓存（如果有缓存插件）

#### 步骤 4：重新登录
1. 退出 WordPress
2. 重新登录
3. 再次编辑 `functions.php`

---

### 方案 4：分段保存

如果文件很大，可以分段编辑。

#### 步骤 1：先保存一部分
1. 只添加一部分代码
2. 保存
3. 立即再次编辑

#### 步骤 2：继续添加
1. 添加剩余代码
2. 保存

---

## 🔧 快速修复步骤

### 如果您现在遇到 nonce_failure

**立即执行：**

1. **复制您的代码**
   - 复制您在编辑器中的所有修改
   - 保存到本地文件

2. **通过 FTP 上传**
   - 连接 FTP
   - 找到 `functions.php`
   - 下载备份
   - 上传修改后的文件

**或者：**

1. **安装 Code Snippets 插件**
2. **创建新代码片段**
3. **粘贴横幅代码**
4. **激活**

---

## 📋 推荐的工作流程

### 最佳实践

1. **使用 Code Snippets 插件** - 管理所有自定义代码
2. **使用子主题** - 避免主题更新时丢失修改
3. **使用 FTP** - 编辑重要文件
4. **定期备份** - 使用备份插件

### 编辑 functions.php 的正确方式

```
1. 备份原文件
   ↓
2. 在本地编辑器中修改（如 VS Code）
   ↓
3. 通过 FTP 上传
   ↓
4. 测试网站
   ↓
5. 如果有问题，恢复备份
```

---

## ⚠️ 重要提示

### 编辑 functions.php 的风险

1. **语法错误会导致网站崩溃**
   - 一个小错误就可能导致白屏
   - 始终保留备份

2. **主题更新会覆盖修改**
   - 使用子主题
   - 或使用 Code Snippets 插件

3. **nonce 失败会丢失修改**
   - 在本地编辑器中编辑
   - 通过 FTP 上传

---

## 🎯 针对您的情况

### 当前状态
- ✅ 代码已在本地编辑完成
- ❌ WordPress 后台保存失败（nonce_failure）

### 推荐操作

**选项 1：FTP 上传（最快）**
```
1. 通过 FTP 连接服务器
2. 找到 functions.php
3. 下载备份
4. 上传修改后的文件
5. 测试网站
```

**选项 2：Code Snippets（最安全）**
```
1. 安装 Code Snippets 插件
2. 创建新代码片段
3. 粘贴横幅代码（从 add_top_promo_banner 函数开始）
4. 激活代码片段
5. 测试网站
```

---

## 📝 Code Snippets 示例

### 如果使用 Code Snippets 插件

**代码片段设置：**
- **标题**: Pangolin Top Banner
- **代码类型**: PHP Snippet
- **运行位置**: Run everywhere
- **代码**:

```php
<?php
// 顶部促销横幅
add_action('wp_body_open', 'add_top_promo_banner');
function add_top_promo_banner() {
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
    
    // ... 其余代码 ...
}
```

---

## 🔍 验证代码是否生效

### 方法 1：查看页面源代码
1. 访问英文首页
2. 右键 → 查看页面源代码
3. 搜索 `pangolin-top-banner`
4. 如果找到，说明代码已生效

### 方法 2：查看控制台
1. 打开控制台（F12）
2. 刷新页面
3. 查看是否有 `[Banner] 初始化顶部横幅` 的日志

---

**创建时间**: 2025-12-11  
**问题**: nonce_failure 错误  
**推荐方案**: FTP 上传或 Code Snippets 插件

---

**立即行动：**
1. ✅ 选择一个方案（FTP 或 Code Snippets）
2. ✅ 备份原文件
3. ✅ 上传/创建代码片段
4. ✅ 测试网站

**如有问题，请告诉我！** 😊
