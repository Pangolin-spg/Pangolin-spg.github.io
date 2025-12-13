#!/bin/bash

# 批量为所有文章页面添加语言切换器
# 此脚本会：
# 1. 在每个文章的 </style> 前添加语言切换器样式
# 2. 更新导航栏添加语言切换器和 "Get API Key" 按钮

cd /Users/macos/Documents/Antigravity/Pangolin-spg.github.io/articles

echo "🔄 开始更新所有文章页面..."

# 语言切换器样式
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

# 处理每个文章文件
for file in *.html; do
    if [ -f "$file" ]; then
        echo "📝 处理: $file"
        
        # 提取文件名（不含扩展名）用于中文链接
        filename="${file%.html}"
        
        # 备份原文件
        cp "$file" "$file.bak"
        
        # 使用 Python 进行更精确的替换
        python3 << EOF
import re

filename = "$file"
article_name = "$filename"

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在 </style> 前添加语言切换器样式（如果还没有）
if 'Language Switcher' not in content:
    content = content.replace('    </style>', '''$LANG_STYLES
    </style>''')

# 2. 替换 "Try Free" 为 "Get API Key"
content = content.replace('>Try Free<', '>Get API Key<')

# 3. 更新导航栏（查找并替换 Try Free 按钮部分）
# 查找导航栏中的按钮部分
nav_pattern = r'(<a href="https://tool\.pangolinfo\.com/"[^>]*>)\s*Get API Key\s*(</a>)'

if re.search(nav_pattern, content):
    # 构建新的导航栏结尾部分（包含语言切换器）
    new_nav_end = '''<div class="flex items-center gap-4">
                <!-- Language Switcher -->
                <div class="language-switcher">
                    <button class="language-btn">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
                        </svg>
                        <span>EN</span>
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    <div class="language-dropdown">
                        <a href="/articles/''' + article_name + '''.html" class="language-option active">
                            <span>🇺🇸</span>
                            <span>English</span>
                        </a>
                        <a href="/zh/articles/''' + article_name + '''.html" class="language-option">
                            <span>🇨🇳</span>
                            <span>中文</span>
                        </a>
                    </div>
                </div>
                <!-- Get API Key Button -->
                <a href="https://tool.pangolinfo.com/"
                    class="bg-white/10 hover:bg-white/20 border border-white/10 backdrop-blur-sm px-5 py-2 rounded-full text-sm font-semibold transition hover:shadow-lg hover:shadow-accent-cyan/20">
                    Get API Key
                </a>
            </div>'''
    
    # 替换按钮为新的导航栏结尾
    content = re.sub(
        r'<a href="https://tool\.pangolinfo\.com/"[^>]*>\s*Get API Key\s*</a>',
        new_nav_end,
        content,
        count=1
    )

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 已更新: {filename}")
EOF
        
    fi
done

echo ""
echo "✅ 所有文章页面更新完成！"
echo ""
echo "已更新的文件："
ls -1 *.html | grep -v ".bak"

echo ""
echo "备份文件已保存为 .bak，如需回滚可以使用这些备份"
