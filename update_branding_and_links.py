import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Update Logo Text (Header)
    # Pattern: <span class="text-xl font-bold tracking-tight">PANGOLIN</span>
    # Replacement: <span class="text-xl font-bold tracking-tight">PANGOL<span style="color:#FF9900">INFO</span></span>
    # Using simple replace for exact matches is safer than regex for this specific string
    content = content.replace(
        '<span class="text-xl font-bold tracking-tight">PANGOLIN</span>',
        '<span class="text-xl font-bold tracking-tight">PANGOL<span style="color:#FF9900">INFO</span></span>'
    )
    
    # 2. Update Logo Text (Footer)
    # Pattern: <span class="font-bold text-lg text-white">PANGOLIN</span>
    content = content.replace(
        '<span class="font-bold text-lg text-white">PANGOLIN</span>',
        '<span class="font-bold text-lg text-white">PANGOL<span style="color:#FF9900">INFO</span></span>'
    )
    
    # 3. Update www.pangolinfo.com links to open in new tab
    # Regex to find <a> tags containing href="https://www.pangolinfo.com..."
    # We want to maintain robust parsing.
    
    def link_replacer(match):
        tag = match.group(0)
        
        # Double check it is a pangolinfo.com link
        if 'www.pangolinfo.com' not in tag:
            return tag
            
        # If target is already present
        if 'target=' in tag:
            # If it's not _blank, we might want to change it, but play safe:
            # if target="_blank" is not there, we assume it's custom, but user said "ALL ... changed to new window"
            # So let's enforce target="_blank" if it's www.pangolinfo.com
            
            # Replace existing target value with _blank
            tag = re.sub(r'target=["\'][^"\']*["\']', 'target="_blank"', tag)
            return tag
        else:
            # Insert target="_blank" before the closing >
            # Check for self-closing />
            if tag.endswith('/>'):
                return tag[:-2] + ' target="_blank"/>'
            else:
                return tag[:-1] + ' target="_blank">'

    # Regex matches opening <a ... > tag
    # Explaining the regex:
    # <a          : Match literal <a
    # \s+         : Must have space after a
    # [^>]*       : Match anything that is not a closing bracket (attributes)
    # href=["\']  : Match href attribute start
    # https?://www\.pangolinfo\.com : Match the domain
    # [^>]*       : Match remaining attributes
    # >           : Match closing bracket
    
    # Actually, the href can be anywhere in the tag.
    # Pattern: <a [^>]*href=["']https?://www\.pangolinfo\.com[^>]*>
    
    link_pattern = r'<a\s+[^>]*href=["\']https?://www\.pangolinfo\.com[^"\']*["\'][^>]*>'
    
    content = re.sub(link_pattern, link_replacer, content, flags=re.IGNORECASE)

    if content != original_content:
        print(f"Updating {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root_dir = '/Users/macos/Documents/Antigravity/Pangolin-spg.github.io'
    updated_files = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Exclude hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    updated_files += 1
    
    print(f"Total files updated: {updated_files}")

if __name__ == "__main__":
    main()
