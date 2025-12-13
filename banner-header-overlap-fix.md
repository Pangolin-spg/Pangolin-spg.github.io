# 横幅遮挡导航栏问题修复

## 🎯 问题根源

### 问题现象
横幅广告遮挡了导航栏的一部分菜单。

### 根本原因
导航栏使用了 `position: fixed; top: 0`，这意味着：
- 导航栏固定在视口顶部（top: 0）
- **不受 body padding 影响**
- 横幅也是 `position: fixed; top: 0`
- 结果：两者重叠，横幅遮挡导航栏

```css
/* 导航栏的 CSS（在 functions.php 第 79-81 行） */
.ast-primary-header-bar {
    position: fixed !important;
    top: 0 !important;  /* ← 问题所在：固定在顶部 */
}
```

---

## ✅ 解决方案

### 核心思路

**当有横幅时，修改导航栏的 top 值为 40px**

```css
/* 有横幅时，导航栏下移 40px */
body.has-top-banner .ast-primary-header-bar {
    top: 40px !important;
}
```

---

## 📋 完整的修复 CSS

### 基础设置
```css
/* 导航栏默认在顶部 */
.ast-primary-header-bar {
    position: fixed !important;
    top: 0 !important;
    z-index: 9998;
}
```

### 横幅相关设置
```css
/* 横幅 */
.pangolin-promo-banner {
    position: fixed;
    top: 0;
    z-index: 999999 !important;  /* 高于导航栏 */
    height: 40px;
}

/* body 向下移动（为页面内容留出空间） */
body.has-top-banner {
    padding-top: 40px !important;
}

/* 导航栏下移 40px，在横幅下方 */
body.has-top-banner .ast-primary-header-bar {
    top: 40px !important;
}
```

### WordPress 管理条兼容
```css
/* 只有管理条时 */
body.admin-bar .ast-primary-header-bar {
    top: 32px !important;
}

/* 同时有管理条和横幅时 */
body.admin-bar.has-top-banner .ast-primary-header-bar {
    top: 72px !important;  /* 32px + 40px */
}
```

### 手机端
```css
@media (max-width: 768px) {
    /* 横幅高度 */
    .pangolin-promo-banner {
        height: 56px;
    }
    
    /* body padding */
    body.has-top-banner {
        padding-top: 56px !important;
    }
    
    /* 导航栏位置（在横幅下方） */
    body.has-top-banner .ast-primary-header-bar {
        top: 56px !important;
    }
}
```

---

## 🎨 布局效果

### 桌面端
```
┌─────────────────────────────────────────────────┐
│ 横幅 (40px, fixed, top: 0, z-index: 999999)     │
├─────────────────────────────────────────────────┤ ← 横幅底部 (40px)
│ 导航栏 (fixed, top: 40px, z-index: 9998)        │ ← 不被遮挡 ✅
│ [Logo]  Product | Pricing | Solution  [Reg/Log]│
├─────────────────────────────────────────────────┤
│ body (padding-top: 40px)                        │
│ ┌─────────────────────────────────────────────┐ │
│ │ 页面内容                                     │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### 关闭横幅后
```
┌─────────────────────────────────────────────────┐
│ 导航栏 (fixed, top: 0)                          │ ← 回到顶部 ✅
│ [Logo]  Product | Pricing | Solution  [Reg/Log]│
├─────────────────────────────────────────────────┤
│ body (padding-top: 0)                           │
│ ┌─────────────────────────────────────────────┐ │
│ │ 页面内容                                     │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 🧪 测试步骤

### 步骤 1：强制刷新
```
Ctrl+Shift+R (Windows) 或 Cmd+Shift+R (Mac)
或者
Ctrl+F5 (Windows)
```

**重要：** 必须强制刷新，清除浏览器缓存！

### 步骤 2：访问英文首页

**检查点：**
```
✅ 横幅在最顶部
✅ 导航栏在横幅下方（不被遮挡）
✅ 所有菜单项清晰可见
✅ Logo 清晰可见
✅ 注册/登录按钮清晰可见
```

### 步骤 3：滚动页面
```
✅ 导航栏保持在横幅下方
✅ 导航栏显示毛玻璃效果
```

### 步骤 4：关闭横幅
```
✅ 横幅消失
✅ 导航栏回到顶部（top: 0）
✅ 页面布局正常
```

---

## 🔍 调试命令

### 检查导航栏位置
```javascript
// 在浏览器控制台（F12）运行
var header = document.querySelector('.ast-primary-header-bar');
var body = document.body;

console.log('body 是否有 has-top-banner class:', body.classList.contains('has-top-banner'));
console.log('header top:', window.getComputedStyle(header).top);
console.log('header position:', window.getComputedStyle(header).position);

// 应该显示：
// body 是否有 has-top-banner class: true
// header top: 40px
// header position: fixed
```

### 检查是否被遮挡
```javascript
var banner = document.getElementById('pangolin-top-banner');
var header = document.querySelector('.ast-primary-header-bar');

var bannerBottom = banner.getBoundingClientRect().bottom;
var headerTop = header.getBoundingClientRect().top;

console.log('横幅底部:', bannerBottom);
console.log('导航栏顶部:', headerTop);
console.log('是否紧贴:', Math.abs(headerTop - bannerBottom) < 2);

if (headerTop >= bannerBottom) {
    console.log('✅ 导航栏在横幅下方，不被遮挡');
} else {
    console.log('❌ 导航栏被横幅遮挡了', bannerBottom - headerTop, 'px');
}
```

### 检查 Z-Index
```javascript
var banner = document.getElementById('pangolin-top-banner');
var header = document.querySelector('.ast-primary-header-bar');

console.log('横幅 z-index:', window.getComputedStyle(banner).zIndex);
console.log('导航栏 z-index:', window.getComputedStyle(header).zIndex);

// 应该显示：
// 横幅 z-index: 999999
// 导航栏 z-index: 9998
```

---

## ⚠️ 故障排查

### 问题 1：还是被遮挡

**可能原因：** 浏览器缓存

**解决方法：**
1. 强制刷新：Ctrl+Shift+R 或 Cmd+Shift+R
2. 清除浏览器缓存
3. 使用隐私模式测试

### 问题 2：导航栏 top 不是 40px

**检查 CSS 优先级：**
```javascript
var header = document.querySelector('.ast-primary-header-bar');
console.log('header top:', window.getComputedStyle(header).top);
```

**如果不是 40px，增加优先级：**
```css
body.has-top-banner .ast-primary-header-bar {
    top: 40px !important;
}
```

### 问题 3：关闭横幅后导航栏不回到顶部

**检查 JavaScript：**
```javascript
// 确保关闭横幅时移除了 has-top-banner class
document.body.classList.remove('has-top-banner');
```

---

## 📊 Z-Index 层级

```
层级（从高到低）：
999999: 横幅 (.pangolin-promo-banner)
9998:   导航栏 (.ast-primary-header-bar)
99:     Sticky 导航栏（滚动后）
auto:   页面内容
```

---

## 🎯 关键点总结

### 为什么导航栏会被遮挡？
```
1. 导航栏是 position: fixed; top: 0
2. 横幅也是 position: fixed; top: 0
3. 横幅的 z-index (999999) 高于导航栏 (9998)
4. 结果：横幅在导航栏上方，遮挡了导航栏
```

### 解决方案
```
1. 保持横幅在 top: 0
2. 修改导航栏的 top 为 40px（当有横幅时）
3. 结果：导航栏在横幅下方，不被遮挡
```

### CSS 设置
```css
/* 桌面端 */
body.has-top-banner .ast-primary-header-bar {
    top: 40px !important;
}

/* 手机端 */
@media (max-width: 768px) {
    body.has-top-banner .ast-primary-header-bar {
        top: 56px !important;
    }
}
```

---

## 📋 修改记录

### 文件：functions.php

#### 添加（第 111-125 行）
```css
/* --- 修复：横幅广告遮挡问题 --- */
/* 当有横幅时，页眉下移 40px */
body.has-top-banner .ast-primary-header-bar {
    top: 40px !important;
}

/* 同时有管理条和横幅时 */
body.admin-bar.has-top-banner .ast-primary-header-bar {
    top: 72px !important;  /* 32px + 40px */
}

@media screen and (max-width: 782px) {
    body.admin-bar.has-top-banner .ast-primary-header-bar {
        top: 86px !important;  /* 46px + 40px */
    }
}
```

---

**修复时间**: 2025-12-10  
**状态**: ✅ 已完成  
**关键修改**: 添加 `body.has-top-banner .ast-primary-header-bar { top: 40px; }`

---

**请立即测试：**
1. ✅ **强制刷新**（Ctrl+Shift+R）← 重要！
2. ✅ 访问英文首页
3. ✅ 检查导航栏是否在横幅下方
4. ✅ 检查所有菜单项是否清晰可见
5. ✅ 点击关闭按钮测试

**现在导航栏应该不会被横幅遮挡了！** 😊
