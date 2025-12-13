# Google Analytics 代码检查指南

## 📋 操作步骤

### 第一步:禁用插件
1. 登录 WordPress 后台
2. 进入 **插件 → 已安装的插件**
3. 找到植入 Google Analytics 的插件
4. 点击 **停用**
5. **不要删除插件**,先测试确认无误后再删除

---

## 🔍 方法一:浏览器开发者工具检查(推荐)

### Chrome/Edge 浏览器:

1. **打开网站首页**
   - 访问: `https://www.pangolinfo.com`

2. **打开开发者工具**
   - 按 `F12` 或 `右键 → 检查`

3. **查看网络请求**
   - 切换到 **Network(网络)** 标签
   - 刷新页面 (`F5`)
   - 在过滤框中输入: `gtag` 或 `googletagmanager`

4. **验证加载成功**
   - 应该看到以下请求:
     ```
     ✅ gtag/js?id=G-GET1NHBL0N (状态码: 200)
     ✅ collect?v=2&... (GA 数据发送请求)
     ```

5. **查看源代码**
   - 切换到 **Elements(元素)** 标签
   - 按 `Ctrl+F` (Mac: `Cmd+F`) 搜索: `G-GET1NHBL0N`
   - 应该在 `<head>` 部分找到以下代码:
     ```html
     <!-- Google tag (gtag.js) -->
     <script async src="https://www.googletagmanager.com/gtag/js?id=G-GET1NHBL0N"></script>
     <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());
       gtag('config', 'G-GET1NHBL0N');
       ...
     </script>
     ```

---

## 🔍 方法二:查看页面源代码

1. **访问网站首页**
   - `https://www.pangolinfo.com`

2. **查看源代码**
   - 按 `Ctrl+U` (Mac: `Cmd+Option+U`)
   - 或 `右键 → 查看网页源代码`

3. **搜索关键代码**
   - 按 `Ctrl+F` (Mac: `Cmd+F`)
   - 搜索: `G-GET1NHBL0N`
   - 应该在 `<head>` 部分找到完整的 GA 代码

4. **确认代码位置**
   - 代码应该在 `</head>` 标签之前
   - 包含完整的 gtag.js 引用和配置

---

## 🔍 方法三:浏览器控制台检查

1. **打开开发者工具**
   - 按 `F12`

2. **切换到 Console(控制台)** 标签

3. **输入以下命令**:
   ```javascript
   typeof gtag
   ```

4. **验证结果**:
   - ✅ 如果返回 `"function"` → GA 加载成功
   - ❌ 如果返回 `"undefined"` → GA 未加载

5. **进一步检查 dataLayer**:
   ```javascript
   window.dataLayer
   ```
   - 应该返回一个数组,包含 GA 事件数据

---

## 🔍 方法四:Google Analytics 实时报告

1. **登录 Google Analytics**
   - 访问: `https://analytics.google.com`

2. **进入实时报告**
   - 左侧菜单 → **报告 → 实时**

3. **访问您的网站**
   - 在新标签页打开网站首页
   - 浏览几个页面

4. **查看实时数据**
   - 应该在 GA 实时报告中看到:
     - ✅ 当前活跃用户数 ≥ 1
     - ✅ 页面浏览记录
     - ✅ 事件记录(如果触发了视频播放等)

---

## 🔍 方法五:使用 Google Tag Assistant

1. **安装浏览器扩展**
   - Chrome: [Google Tag Assistant Legacy](https://chrome.google.com/webstore/detail/tag-assistant-legacy-by-g/kejbdjndbnbjgmefkgdddjlbokphdefk)

2. **访问网站**
   - 打开您的网站首页

3. **启用 Tag Assistant**
   - 点击浏览器工具栏中的扩展图标
   - 点击 **Enable** 启用
   - 刷新页面

4. **查看检测结果**
   - 应该显示:
     - ✅ Google Analytics (GA4) - G-GET1NHBL0N
     - 状态: 绿色(正常工作)

---

## ✅ 验证自定义事件

### 测试页面离开事件:

1. **打开开发者工具 Console**
2. **访问网站任意页面**
3. **切换到其他标签页** (不要关闭)
4. **查看控制台输出**:
   - 应该看到: `==========isHidden:隐藏`
5. **检查 Network 标签**:
   - 应该看到发送到 GA 的 `collect` 请求
   - 包含事件名: `marketing_pangolin_page_leave`

### 测试视频埋点事件:

1. **访问包含视频的页面** (视频 ID: `pangolin-intro-video`)
2. **打开开发者工具 Network 标签**
3. **过滤**: `collect`
4. **播放视频**,应该看到以下事件:
   - ✅ `video_loaded` - 视频加载完成
   - ✅ `video_start` - 开始播放
   - ✅ `video_progress` - 播放进度 (25%, 50%, 75%)
   - ✅ `video_pause` - 暂停
   - ✅ `video_complete` - 播放完成

---

## ⚠️ 常见问题排查

### 问题1: 找不到 GA 代码

**可能原因**:
- 缓存插件(如 WP Rocket)缓存了旧版本
- CDN 缓存未更新

**解决方法**:
1. 清除 WordPress 缓存
2. 清除 CDN 缓存
3. 清除浏览器缓存 (`Ctrl+Shift+Delete`)
4. 使用隐身模式测试

### 问题2: GA 代码存在但不发送数据

**检查步骤**:
1. 打开 Console,查看是否有 JavaScript 错误
2. 检查是否有广告拦截器阻止了 GA
3. 确认 GA 属性 ID `G-GET1NHBL0N` 正确

### 问题3: 代码加载了两次

**可能原因**:
- 插件和 functions.php 同时加载了代码

**解决方法**:
- 确认插件已完全禁用
- 检查主题设置中是否有其他 GA 配置

---

## 📊 最终确认清单

- [ ] 浏览器 Network 中能看到 `gtag/js?id=G-GET1NHBL0N` 请求
- [ ] 页面源代码中存在完整的 GA 代码
- [ ] Console 中 `typeof gtag` 返回 `"function"`
- [ ] GA 实时报告中能看到访问数据
- [ ] 页面离开事件正常触发(Console 有日志)
- [ ] 视频埋点事件正常发送(如适用)
- [ ] 没有 JavaScript 错误
- [ ] 代码只加载一次(没有重复)

---

## 🎯 推荐检查顺序

1. **方法一**(开发者工具) - 最快速、最直观
2. **方法四**(GA 实时报告) - 验证数据收集
3. **方法五**(Tag Assistant) - 深度诊断

如果以上三个方法都通过,说明 GA 代码已经**完全正常工作**! ✅
