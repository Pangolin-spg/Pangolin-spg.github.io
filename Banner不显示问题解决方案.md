# 🔧 Banner在Astra自定义器中不显示的解决方案

## ❓ 问题描述

在 **外观 → 自定义 → 页眉** 中添加HTML小部件并粘贴Banner代码后,Banner不显示。

---

## 🔍 **根本原因**

### **您的functions.php中的冲突代码**:

```php
.ast-primary-header-bar {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    z-index: 9999;  ← 这里!
}
```

### **Banner代码中的z-index**:

```css
.pangolin-top-banner {
    z-index: 9999;  ← 和Header一样!
}
```

### **冲突结果**:
- 两个元素都是 `z-index: 9999`
- Header的 `position: fixed` 会覆盖Banner
- Banner被遮挡,看不见

---

## ✅ **解决方案**

### **方案1: 提高Banner的z-index** ⭐⭐⭐⭐⭐ (已完成)

我已经为您更新了Banner代码:

```css
.pangolin-top-banner {
    z-index: 99999; /* 从9999提高到99999 */
}
```

**现在请重新粘贴更新后的Banner代码!**

---

### **方案2: 调整Header的top值**

如果方案1不行,可以修改`functions.php`:

```php
/* 在 functions.php 中找到这段代码 */
.ast-primary-header-bar {
    position: fixed !important;
    top: 0 !important;  /* 改为 top: 50px !important; */
    ...
}
```

**修改为**:

```php
.ast-primary-header-bar {
    position: fixed !important;
    top: 50px !important;  /* 为Banner留出空间 */
    ...
}
```

**注意**: 这会让Header下移50px,为Banner腾出空间。

---

### **方案3: 使用wp_body_open钩子** ⭐⭐⭐⭐⭐ (最推荐)

**不在自定义器中添加**,而是在`functions.php`中添加:

#### **步骤**:

1. **打开functions.php**
   ```
   外观 → 主题文件编辑器 → functions.php
   ```

2. **在文件末尾(?>之前)添加**:

```php
/**
 * 添加Pangolin访谈Banner到页面顶部
 */
add_action('wp_body_open', 'pangolin_add_interview_banner', 1);
function pangolin_add_interview_banner() {
    ?>
    <!-- Pangolin Interview Banner -->
    <style>
        .pangolin-top-banner {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #7c3aed 100%);
            color: white;
            padding: 12px 20px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            overflow: hidden;
            z-index: 99999; /* 高于Header的9999 */
        }

        .pangolin-top-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            right: 10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(124, 58, 237, 0.3) 0%, transparent 70%);
            border-radius: 50%;
            animation: pangolinPulse 6s ease-in-out infinite;
        }

        @keyframes pangolinPulse {
            0%, 100% {
                transform: scale(1);
                opacity: 0.4;
            }
            50% {
                transform: scale(1.2);
                opacity: 0.6;
            }
        }

        .pangolin-banner-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            position: relative;
            z-index: 2;
        }

        .pangolin-banner-left {
            display: flex;
            align-items: center;
            gap: 16px;
            flex: 1;
        }

        .pangolin-banner-icon {
            font-size: 20px;
            color: #fbbf24;
            animation: pangolinBounce 2s infinite;
        }

        @keyframes pangolinBounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-4px);
            }
        }

        .pangolin-banner-text {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .pangolin-banner-message {
            font-size: 15px;
            font-weight: 600;
            line-height: 1.4;
        }

        .pangolin-highlight {
            color: #fbbf24;
            font-weight: 900;
        }

        .pangolin-badge {
            background: rgba(251, 191, 36, 0.2);
            border: 1px solid rgba(251, 191, 36, 0.4);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            color: #fbbf24;
            white-space: nowrap;
        }

        .pangolin-countdown {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 0, 0, 0.2);
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .pangolin-countdown-label {
            font-size: 12px;
            font-weight: 600;
            opacity: 0.9;
        }

        .pangolin-countdown-time {
            display: flex;
            gap: 6px;
            font-family: 'Courier New', monospace;
            font-weight: 900;
        }

        .pangolin-countdown-value {
            font-size: 16px;
            color: #fbbf24;
            min-width: 20px;
            text-align: center;
        }

        .pangolin-countdown-sep {
            color: #fbbf24;
            opacity: 0.6;
        }

        .pangolin-countdown-unit {
            font-size: 10px;
            opacity: 0.8;
        }

        .pangolin-banner-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .pangolin-cta-btn {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: #1e3a8a;
            font-size: 14px;
            font-weight: 900;
            padding: 10px 24px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(251, 191, 36, 0.4);
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .pangolin-cta-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(251, 191, 36, 0.6);
        }

        .pangolin-close-btn {
            background: transparent;
            border: none;
            color: rgba(255, 255, 255, 0.7);
            font-size: 20px;
            cursor: pointer;
            padding: 4px 8px;
            transition: all 0.3s ease;
        }

        .pangolin-close-btn:hover {
            color: white;
            transform: scale(1.1);
        }

        /* 适配您的固定Header */
        body .ast-primary-header-bar {
            top: 50px !important; /* 为Banner留出空间 */
        }

        /* 登录状态下的适配 */
        body.admin-bar .pangolin-top-banner {
            top: 32px;
        }

        body.admin-bar .ast-primary-header-bar {
            top: 82px !important; /* 32px(admin bar) + 50px(banner) */
        }

        @media screen and (max-width: 782px) {
            body.admin-bar .pangolin-top-banner {
                top: 46px;
            }
            body.admin-bar .ast-primary-header-bar {
                top: 96px !important; /* 46px + 50px */
            }
        }

        /* 响应式 */
        @media (max-width: 768px) {
            .pangolin-banner-content {
                flex-direction: column;
                gap: 12px;
                text-align: center;
            }
            .pangolin-banner-left {
                flex-direction: column;
                gap: 8px;
            }
            .pangolin-banner-right {
                width: 100%;
                justify-content: center;
                flex-wrap: wrap;
            }
            .pangolin-countdown {
                order: -1;
                width: 100%;
                justify-content: center;
            }
        }
    </style>

    <div class="pangolin-top-banner" id="pangolinTopBanner">
        <div class="pangolin-banner-content">
            <div class="pangolin-banner-left">
                <i class="fas fa-sparkles pangolin-banner-icon"></i>
                <div class="pangolin-banner-text">
                    <span class="pangolin-banner-message">
                        🎉 <strong>New Version Launch:</strong> Join our interview & get <span class="pangolin-highlight">50% OFF Forever</span>
                    </span>
                    <span class="pangolin-badge">Limited to 50 Users</span>
                </div>
            </div>
            <div class="pangolin-banner-right">
                <div class="pangolin-countdown">
                    <span class="pangolin-countdown-label">Ends in:</span>
                    <div class="pangolin-countdown-time">
                        <span><span class="pangolin-countdown-value" id="pangolinDays">--</span><span class="pangolin-countdown-unit">d</span></span>
                        <span class="pangolin-countdown-sep">:</span>
                        <span><span class="pangolin-countdown-value" id="pangolinHours">--</span><span class="pangolin-countdown-unit">h</span></span>
                        <span class="pangolin-countdown-sep">:</span>
                        <span><span class="pangolin-countdown-value" id="pangolinMinutes">--</span><span class="pangolin-countdown-unit">m</span></span>
                    </div>
                </div>
                <a href="#elementor-popup-12817" class="pangolin-cta-btn">
                    Apply Now
                    <i class="fas fa-arrow-right"></i>
                </a>
                <button class="pangolin-close-btn" onclick="document.getElementById('pangolinTopBanner').style.display='none'; localStorage.setItem('pangolinBannerClosed', 'true');">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    </div>

    <script>
    (function() {
        function updateCountdown() {
            const deadline = new Date('2025-12-31T23:59:59');
            const now = new Date();
            const diff = deadline - now;
            
            if (diff > 0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                
                document.getElementById('pangolinDays').textContent = String(days).padStart(2, '0');
                document.getElementById('pangolinHours').textContent = String(hours).padStart(2, '0');
                document.getElementById('pangolinMinutes').textContent = String(minutes).padStart(2, '0');
            }
        }
        
        updateCountdown();
        setInterval(updateCountdown, 60000);
        
        if (localStorage.getItem('pangolinBannerClosed') === 'true') {
            document.getElementById('pangolinTopBanner').style.display = 'none';
        }
    })();
    </script>
    <?php
}
```

3. **保存文件**

4. **清除缓存**

5. **访问网站查看**

---

## 📋 **推荐实施步骤**

### **最简单的方法** (方案3):

1. ✅ **复制上面的完整PHP代码**
2. ✅ **粘贴到functions.php末尾**
3. ✅ **保存**
4. ✅ **清除缓存**
5. ✅ **访问网站**

**优点**:
- ✅ 不需要在自定义器中操作
- ✅ 自动适配您的固定Header
- ✅ 自动处理WordPress Admin Bar
- ✅ 代码统一管理
- ✅ 不会有z-index冲突

---

## 🎯 **关键调整说明**

### **为什么要调整Header的top值**:

```css
/* Banner高度约50px */
.pangolin-top-banner {
    position: fixed;
    top: 0;
    height: ~50px;
}

/* Header需要下移,为Banner腾出空间 */
.ast-primary-header-bar {
    top: 50px !important; /* 原来是0 */
}
```

### **登录状态的适配**:

```css
/* 未登录 */
Banner: top: 0
Header: top: 50px

/* 登录(桌面) */
Admin Bar: top: 0 (32px高)
Banner: top: 32px
Header: top: 82px (32+50)

/* 登录(移动) */
Admin Bar: top: 0 (46px高)
Banner: top: 46px
Header: top: 96px (46+50)
```

---

## ✅ **检查清单**

实施后请检查:

- [ ] Banner显示在页面最顶部
- [ ] Header显示在Banner下方
- [ ] 倒计时正常运行
- [ ] 点击"Apply Now"打开Popup
- [ ] 移动端显示正常
- [ ] 登录状态下位置正确
- [ ] 关闭Banner后不再显示

---

## 🐛 **故障排除**

### **问题1: Banner仍然不显示**

**检查**:
- 浏览器控制台是否有错误 (F12)
- Font Awesome是否加载
- CSS是否被其他样式覆盖

**解决**:
```
清除所有缓存
硬刷新: Ctrl+Shift+R
检查CSS优先级
```

### **问题2: Banner和Header重叠**

**原因**: top值设置不正确

**解决**:
```css
/* 调整Header的top值 */
.ast-primary-header-bar {
    top: 60px !important; /* 增加到60px */
}
```

### **问题3: 移动端显示异常**

**检查**: 响应式CSS是否生效

**解决**: 在移动设备上测试,调整断点

---

## 💡 **最终建议**

### **推荐方案**: 使用方案3 (functions.php)

**原因**:
1. ✅ 最可靠 - 不受自定义器限制
2. ✅ 自动适配 - 处理所有边缘情况
3. ✅ 易于维护 - 代码集中管理
4. ✅ 性能更好 - 直接输出HTML

### **不推荐**: 在自定义器中添加

**原因**:
1. ❌ z-index冲突
2. ❌ 位置难以控制
3. ❌ 可能被其他元素覆盖
4. ❌ 调试困难

---

## 📞 **需要帮助?**

如果仍然有问题:

1. **截图发送**:
   - 浏览器控制台 (F12)
   - 页面显示效果
   - 元素检查器

2. **提供信息**:
   - 使用的方案
   - 错误信息
   - 浏览器版本

---

**更新日期**: 2025-12-05  
**状态**: ✅ 已提供3种解决方案  
**推荐**: 方案3 (functions.php)
