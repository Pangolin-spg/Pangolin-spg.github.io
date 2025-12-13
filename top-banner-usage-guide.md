# 顶部促销横幅 - 使用说明

## 🎯 功能概述

在英文首页顶部显示促销横幅，点击后打开 Elementor 访谈表单弹窗。

### 显示效果
```
┌────────────────────────────────────────────────────────────┐
│ Discover the New Pangolin Version — Join a 30-min         │
│ interview & get 50% OFF for life.                      [×] │
└────────────────────────────────────────────────────────────┘
```

---

## ✅ 已实现的功能

### 1. 显示条件
- ✅ **仅英文首页显示**
- ✅ 中文首页不显示
- ✅ 其他页面不显示

### 2. 交互功能
- ✅ **点击横幅** → 打开访谈表单弹窗（ID: 12817）
- ✅ **点击关闭按钮** → 关闭横幅
- ✅ **关闭后 24 小时内不再显示**（使用 localStorage）

### 3. 样式特性
- ✅ 高度：40px（桌面端）
- ✅ 背景色：#F8F8F8（浅灰）
- ✅ 文字颜色：#333333
- ✅ 强调色：#0066FF（蓝色）
- ✅ 通栏水平铺满
- ✅ 内容居中显示
- ✅ 悬停效果
- ✅ 响应式设计

### 4. 页面适配
- ✅ 自动为页面主体添加 `padding-top: 40px`
- ✅ 避免横幅遮挡页面内容
- ✅ 关闭后自动移除间距

---

## 📐 样式规格

### 桌面端（>768px）
```css
高度: 40px
字体大小: 14px
背景色: #F8F8F8
文字颜色: #333333
强调色: #0066FF
```

### 平板端（≤768px）
```css
高度: 自适应（最小 40px）
字体大小: 12px
内边距: 8px 0
```

### 手机端（≤480px）
```css
字体大小: 11px
行高: 1.4
```

---

## 🔧 配置说明

### 修改弹窗 ID

如果需要更换弹窗，修改 `functions.php` 中的第 1449 行：

```javascript
elementorProFrontend.modules.popup.showPopup({ id: 12817 });
//                                                  ^^^^^ 修改这里
```

### 修改显示时长

默认关闭后 24 小时内不再显示，如需修改：

在 `functions.php` 的第 1465 行：

```javascript
var expireTime = new Date().getTime() + (24 * 60 * 60 * 1000);
//                                       ^^ 修改小时数
```

示例：
- 12 小时：`12 * 60 * 60 * 1000`
- 7 天：`7 * 24 * 60 * 60 * 1000`
- 永久关闭：删除整个 localStorage 逻辑

### 修改文案

在 `functions.php` 的第 1297-1299 行：

```html
<span class="banner-text">
    Discover the New Pangolin Version — Join a 30-min interview & get 
    <strong class="highlight">50% OFF for life</strong>.
</span>
```

### 修改颜色

在 `functions.php` 的 CSS 部分：

```css
/* 背景色 */
background-color: #F8F8F8;  /* 第 1313 行 */

/* 文字颜色 */
color: #333333;  /* 第 1336 行 */

/* 强调色 */
color: #0066FF;  /* 第 1341 行 */
```

---

## 🧪 测试步骤

### 步骤 1：访问英文首页
```
1. 清除浏览器缓存（Ctrl+F5）
2. 访问网站英文首页
3. ✅ 应该看到顶部横幅
4. ✅ 页面内容应该在横幅下方，不被遮挡
```

### 步骤 2：测试点击打开弹窗
```
1. 点击横幅任意位置（除了关闭按钮）
2. ✅ 应该打开访谈表单弹窗
3. ✅ 弹窗 ID 应该是 12817
```

### 步骤 3：测试关闭功能
```
1. 点击横幅右侧的 × 按钮
2. ✅ 横幅应该消失
3. ✅ 页面顶部间距应该移除
4. 刷新页面
5. ✅ 横幅不应该再次出现（24小时内）
```

### 步骤 4：测试其他页面
```
1. 访问中文首页
2. ✅ 不应该显示横幅

3. 访问其他页面（关于我们、产品页等）
4. ✅ 不应该显示横幅
```

### 步骤 5：测试响应式
```
1. 按 F12 打开开发者工具
2. 切换到移动设备视图
3. ✅ 横幅应该自适应宽度
4. ✅ 字体大小应该变小
5. ✅ 关闭按钮应该正常显示
```

---

## 🔍 调试方法

### 查看控制台日志

按 F12 打开浏览器控制台，您会看到：

**横幅初始化：**
```
[Banner] 初始化顶部横幅
```

**点击横幅：**
```
[Banner] 横幅被点击，尝试打开弹窗 ID: 12817
[Banner] 弹窗已打开
```

**点击关闭：**
```
[Banner] 关闭按钮被点击
[Banner] 横幅已关闭，24小时内不再显示
```

**已关闭状态：**
```
[Banner] 横幅在24小时内已被关闭，不显示
```

### 清除关闭状态

如果想重新显示横幅（用于测试），在浏览器控制台运行：

```javascript
localStorage.removeItem('pangolin_banner_closed');
location.reload();
```

---

## ⚠️ 注意事项

### 1. Elementor Pro 依赖

横幅需要 Elementor Pro 才能打开弹窗。如果没有安装 Elementor Pro，控制台会显示：

```
[Banner] Elementor Pro 未加载，无法打开弹窗
```

### 2. 弹窗 ID 必须正确

确保弹窗 ID `12817` 存在且已发布。检查方法：

```
WordPress 后台 → 模板 → 弹窗
查找 ID 为 12817 的弹窗
确保状态为"已发布"
```

### 3. 语言检测

横幅使用 Polylang 检测语言。如果没有安装 Polylang，默认显示在所有首页。

### 4. Z-index 层级

横幅的 `z-index: 9999`，确保它在最上层。如果有其他元素遮挡，可能需要调整 z-index。

### 5. 缓存问题

修改代码后记得清除：
- 浏览器缓存
- WordPress 缓存
- CDN 缓存（如果使用）

---

## 🎨 自定义示例

### 示例 1：更改为红色强调

```css
.pangolin-promo-banner .banner-text .highlight {
    color: #FF0000;  /* 红色 */
    font-weight: 700;
}
```

### 示例 2：增加高度

```css
.pangolin-promo-banner {
    height: 50px;  /* 从 40px 改为 50px */
}

body.has-top-banner {
    padding-top: 50px !important;  /* 同步修改 */
}
```

### 示例 3：添加动画效果

```css
.pangolin-promo-banner {
    animation: slideDown 0.5s ease;
}

@keyframes slideDown {
    from {
        transform: translateY(-100%);
    }
    to {
        transform: translateY(0);
    }
}
```

### 示例 4：更改文案

```html
<span class="banner-text">
    🎉 Limited Time Offer — Get 
    <strong class="highlight">50% OFF</strong> 
    on Annual Plans!
</span>
```

---

## 📊 技术细节

### 文件位置
- **文件**: `functions.php`
- **行数**: 第 1267-1489 行
- **函数**: `add_top_promo_banner()`

### 显示逻辑
```php
1. 检查是否是首页 (is_front_page())
2. 检查是否是英文页面 (pll_current_language() === 'en')
3. 检查是否已关闭 (localStorage)
4. 如果都通过，显示横幅
```

### 弹窗触发
```javascript
elementorProFrontend.modules.popup.showPopup({ id: 12817 });
```

### 关闭逻辑
```javascript
1. 添加 .banner-closed class
2. 移除 .has-top-banner class
3. 保存到 localStorage
4. 设置 24 小时过期时间
```

---

## 🆘 常见问题

### Q1: 横幅不显示

**检查清单：**
- [ ] 是否在英文首页？
- [ ] 是否清除了缓存？
- [ ] 是否在 24 小时内关闭过？
- [ ] 浏览器控制台是否有错误？

**解决方法：**
```javascript
// 清除关闭状态
localStorage.removeItem('pangolin_banner_closed');
location.reload();
```

### Q2: 点击横幅没有反应

**检查清单：**
- [ ] Elementor Pro 是否已安装？
- [ ] 弹窗 ID 12817 是否存在？
- [ ] 弹窗是否已发布？
- [ ] 浏览器控制台是否有错误？

**解决方法：**
查看控制台日志，确认错误信息。

### Q3: 横幅遮挡了页面内容

**检查清单：**
- [ ] `body.has-top-banner` class 是否添加成功？
- [ ] CSS 是否被其他样式覆盖？

**解决方法：**
```css
/* 增加 CSS 优先级 */
body.has-top-banner {
    padding-top: 40px !important;
    margin-top: 0 !important;
}
```

### Q4: 在中文首页也显示了

**原因：** Polylang 未正确配置或未安装

**解决方法：**
检查 Polylang 设置，确保语言检测正常工作。

---

## 📚 相关文件

- `functions.php` - 主要代码文件
- `top-banner-promo.html` - 独立 HTML 版本（供参考）

---

## 🎊 总结

### 功能特性
- ✅ 只在英文首页显示
- ✅ 点击打开 Elementor 弹窗
- ✅ 可关闭，24 小时内不再显示
- ✅ 响应式设计
- ✅ 符合设计规范

### 技术亮点
- ✅ 使用 WordPress 条件标签
- ✅ Polylang 语言检测
- ✅ localStorage 状态管理
- ✅ Elementor Pro API 集成
- ✅ 完善的调试日志

---

**实现时间**: 2025-12-10  
**状态**: ✅ 已完成  
**测试**: 待用户验证

---

**请访问英文首页测试横幅功能！** 😊
