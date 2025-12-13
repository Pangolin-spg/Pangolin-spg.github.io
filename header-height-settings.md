# 页眉高度设置说明

## 📍 页眉高度在哪里设置？

### 当前设置位置

**文件：** `functions.php`  
**行数：** 第 86-87 行

```css
/* 页眉高度设置 - 可以在这里修改 */
min-height: 60px !important;  /* 最小高度，可以根据需要调整 */
```

---

## 🎨 如何修改页眉高度？

### 方法 1：修改 functions.php（推荐）

在 `functions.php` 的第 87 行，修改 `min-height` 的值：

```css
/* 当前设置（60px） */
min-height: 60px !important;

/* 示例：增加到 80px */
min-height: 80px !important;

/* 示例：减少到 50px */
min-height: 50px !important;
```

### 方法 2：使用 Astra 主题设置

如果您使用的是 Astra 主题的默认页眉：

```
WordPress 后台 → 外观 → 自定义 → Header Builder → Primary Header → Height
```

### 方法 3：使用 Elementor 自定义页眉

如果您使用 Elementor 创建了自定义页眉：

```
Elementor → 主题生成器 → Header → 编辑页眉模板 → 设置 Section 高度
```

---

## 📊 不同高度的视觉效果

### 小型页眉（50px）
```css
min-height: 50px !important;
```
- ✅ 节省空间
- ✅ 适合简洁设计
- ❌ Logo 和菜单可能显得拥挤

### 标准页眉（60px）- 当前设置
```css
min-height: 60px !important;
```
- ✅ 平衡的视觉效果
- ✅ Logo 和菜单有足够空间
- ✅ 适合大多数网站

### 大型页眉（80px）
```css
min-height: 80px !important;
```
- ✅ 更醒目
- ✅ 适合大 Logo
- ❌ 占用更多屏幕空间

---

## 🔧 完整的页眉高度 CSS

### 基础设置
```css
.ast-primary-header-bar {
    min-height: 60px !important;  /* 最小高度 */
}
```

### 响应式设置（可选）

如果您想在不同设备上使用不同的高度：

```css
/* 桌面端 */
.ast-primary-header-bar {
    min-height: 60px !important;
}

/* 平板端 */
@media (max-width: 992px) {
    .ast-primary-header-bar {
        min-height: 55px !important;
    }
}

/* 手机端 */
@media (max-width: 768px) {
    .ast-primary-header-bar {
        min-height: 50px !important;
    }
}
```

---

## 🎯 相关元素的高度调整

### Logo 高度

如果修改了页眉高度，可能需要调整 Logo 的高度：

```css
/* 在 functions.php 的 <style> 中添加 */
.site-branding img {
    max-height: 40px !important;  /* Logo 最大高度 */
}
```

### 菜单项高度

确保菜单项与页眉高度匹配：

```css
.main-header-menu > li > a {
    line-height: 60px !important;  /* 与页眉高度一致 */
}
```

---

## 📋 修改步骤

### 步骤 1：打开 functions.php
```
WordPress 后台 → 外观 → 主题文件编辑器 → functions.php
```

### 步骤 2：找到第 87 行
```css
min-height: 60px !important;
```

### 步骤 3：修改高度值
```css
/* 例如：改为 70px */
min-height: 70px !important;
```

### 步骤 4：保存并刷新
```
1. 点击"更新文件"
2. 清除缓存（Ctrl+F5）
3. 刷新页面查看效果
```

---

## ⚠️ 注意事项

### 1. 保持一致性
- Logo 高度应该小于页眉高度
- 菜单项的 line-height 应该与页眉高度一致

### 2. 响应式设计
- 在小屏幕上可能需要减小高度
- 确保在所有设备上测试

### 3. 内容对齐
- 修改高度后，检查 Logo 和菜单是否居中对齐
- 可能需要调整 padding 或 margin

---

## 🔍 调试命令

### 检查当前页眉高度
```javascript
// 在浏览器控制台（F12）运行
var header = document.querySelector('.ast-primary-header-bar');
console.log('页眉高度:', header.offsetHeight, 'px');
console.log('min-height:', window.getComputedStyle(header).minHeight);
```

### 检查 Logo 高度
```javascript
var logo = document.querySelector('.site-branding img');
console.log('Logo 高度:', logo.offsetHeight, 'px');
```

---

## 📊 推荐设置

### 标准网站
```css
min-height: 60px !important;  /* 页眉 */
max-height: 40px !important;  /* Logo */
```

### 品牌导向网站（大 Logo）
```css
min-height: 80px !important;  /* 页眉 */
max-height: 60px !important;  /* Logo */
```

### 简约风格网站
```css
min-height: 50px !important;  /* 页眉 */
max-height: 30px !important;  /* Logo */
```

---

## 🎨 当前页眉设置

### 位置
```
文件：functions.php
函数：add_header_scroll_script()
行数：第 86-87 行
```

### 当前值
```css
min-height: 60px !important;
```

### 修改方法
```
1. 编辑 functions.php
2. 找到第 87 行
3. 修改 60px 为您想要的值
4. 保存并刷新
```

---

**修改时间**: 2025-12-10  
**当前高度**: 60px  
**可调整范围**: 40px - 100px

---

**如果需要修改页眉高度，请告诉我您想要的高度值，我可以帮您修改！** 😊
