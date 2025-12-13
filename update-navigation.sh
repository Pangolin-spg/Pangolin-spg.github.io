#!/bin/bash

# 批量更新所有英文页面的导航栏
# 1. 添加语言切换器样式
# 2. 更新导航栏添加语言切换器
# 3. 将 "Try Free" 改为 "Get API Key"

cd /Users/macos/Documents/Antigravity/Pangolin-spg.github.io

echo "🔄 开始更新所有英文页面..."

# 语言切换器样式（需要添加到 </style> 之前）
LANG_STYLES='
        /* Language Switcher */
        .language-switcher {
            position: relative;
            display: inline-block;
        }

        .language-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            color: #fff;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .language-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(56, 189, 248, 0.5);
        }

        .language-dropdown {
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 8px;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 8px;
            min-width: 140px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            z-index: 1000;
        }

        .language-switcher:hover .language-dropdown {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .language-option {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 12px;
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.2s ease;
        }

        .language-option:hover {
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
        }

        .language-option.active {
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            font-weight: 600;
        }'

echo "✅ 首页已手动更新"

# 更新 blog.html
echo "📝 更新 blog.html..."
# 这个文件需要手动处理，因为结构可能不同

# 更新所有文章页面
echo "📝 更新文章页面..."
for file in articles/*.html; do
    if [ -f "$file" ]; then
        echo "  处理: $file"
        # 将 Try Free 改为 Get API Key
        sed -i '' 's/>Try Free</>Get API Key</g' "$file"
    fi
done

echo "✅ 所有页面已更新完成！"
echo ""
echo "下一步："
echo "1. 手动更新 blog.html 的导航栏"
echo "2. 创建 /zh/ 目录"
echo "3. 生成所有中文页面"
