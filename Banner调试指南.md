# 🔍 Banner问题诊断和调试指南

## 🐛 当前问题

1. ❌ 点击"Apply Now"无法打开Popup
2. ❌ 关闭Banner后Header不上移

---

## 📋 **第一步: 浏览器Console诊断**

### **打开开发者工具**:
1. 访问您的网站
2. 按 `F12` 打开开发者工具
3. 切换到 `Console` 标签
4. 粘贴以下代码并回车:

```javascript
console.log('=== Pangolin Banner 诊断 ===');
console.log('1. Banner元素:', !!document.getElementById('pangolinTopBanner'));
console.log('2. Apply按钮:', !!document.querySelector('.pangolin-cta-btn'));
console.log('3. Header元素:', !!document.querySelector('.ast-primary-header-bar'));
console.log('4. Elementor Pro:', typeof elementorProFrontend);
console.log('5. jQuery:', typeof jQuery);
console.log('6. Header top值:', window.getComputedStyle(document.querySelector('.ast-primary-header-bar')).top);
console.log('================');
```

**请将Console中显示的结果告诉我!**

---

## 🔧 **可能的原因**

### **原因1: Elementor Pro未加载**

如果Console显示 `Elementor Pro: undefined`,说明:
- Elementor Pro未激活
- 或脚本加载顺序问题

**解决方案**: 使用Popup的显示条件功能

1. 进入 `模板` → `弹出式窗口`
2. 编辑您的访谈Popup (ID: 12817)
3. 点击左下角的 ⚙️ **设置**
4. 找到 **显示条件** (Display Conditions)
5. 添加条件: **On Click** → CSS选择器: `.pangolin-cta-btn`
6. 保存并更新

这样Elementor会自动处理Popup触发,不需要JavaScript!

---

### **原因2: CSS优先级冲突**

Header的top值可能被其他CSS覆盖。

**测试**: 在Console中运行:

```javascript
const header = document.querySelector('.ast-primary-header-bar');
header.style.setProperty('top', '0px', 'important');
console.log('测试完成,Header应该已上移');
```

如果Header上移了,说明是CSS优先级问题。

**解决方案**: 使用body类控制

---

## 🚀 **快速修复代码**

请用这个增强版代码替换functions.php中Banner的JavaScript部分:

找到第299行左右的 `<script>` 标签,替换整个script内容为:

```php
    <script>
    // 添加body类标记Banner状态
    document.body.classList.add('pangolin-banner-visible');
    
    (function() {
        // 倒计时功能
        function updateCountdown() {
            const deadline = new Date('2025-12-31T23:59:59');
            const now = new Date();
            const diff = deadline - now;
            
            if (diff > 0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                
                const daysEl = document.getElementById('pangolinDays');
                const hoursEl = document.getElementById('pangolinHours');
                const minutesEl = document.getElementById('pangolinMinutes');
                
                if (daysEl) daysEl.textContent = String(days).padStart(2, '0');
                if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');
                if (minutesEl) minutesEl.textContent = String(minutes).padStart(2, '0');
            }
        }
        
        updateCountdown();
        setInterval(updateCountdown, 60000);
        
        // 检查是否已关闭Banner
        if (localStorage.getItem('pangolinBannerClosed') === 'true') {
            const banner = document.getElementById('pangolinTopBanner');
            if (banner) {
                banner.style.display = 'none';
                document.body.classList.remove('pangolin-banner-visible');
            }
        }
    })();
    
    // 关闭Banner函数
    function closeBanner() {
        const banner = document.getElementById('pangolinTopBanner');
        if (banner) {
            banner.style.display = 'none';
        }
        document.body.classList.remove('pangolin-banner-visible');
        localStorage.setItem('pangolinBannerClosed', 'true');
    }
    </script>
```

---

然后在CSS部分(第38行左右的`<style>`标签内)添加这些样式:

```css
/* 使用body类控制Header位置 - 更可靠 */
body.pangolin-banner-visible .ast-primary-header-bar {
    top: 50px !important;
}

body:not(.pangolin-banner-visible) .ast-primary-header-bar {
    top: 0px !important;
}

/* Admin Bar适配 */
body.admin-bar.pangolin-banner-visible .ast-primary-header-bar {
    top: 82px !important;
}

body.admin-bar:not(.pangolin-banner-visible) .ast-primary-header-bar {
    top: 32px !important;
}

@media screen and (max-width: 782px) {
    body.admin-bar.pangolin-banner-visible .ast-primary-header-bar {
        top: 96px !important;
    }
    body.admin-bar:not(.pangolin-banner-visible) .ast-primary-header-bar {
        top: 46px !important;
    }
}
```

---

## ✅ **Popup触发的最佳方案**

**不使用JavaScript,使用Elementor的内置功能**:

1. 编辑Popup (ID: 12817)
2. ⚙️ 设置 → 高级 → 打开方式
3. 选择 **On Click**
4. CSS选择器输入: `.pangolin-cta-btn`
5. 保存

这样点击Banner的按钮就会自动触发Popup!

---

## 📞 **需要我的帮助**

请告诉我:

1. **Console诊断结果** (运行上面的诊断代码)
2. **Popup ID是否确实是12817**
3. **是否使用了CDN或缓存插件**

我会根据您的反馈提供精准的解决方案!
