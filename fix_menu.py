import os
import re

template_dir = 'templates'
for filename in os.listdir(template_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find the mobile menu block and the closing header tag
    # It assumes mobile menu is right inside the header at the end
    pattern = r'(\s*<!-- Mobile menu -->\s*<div class="mobile-menu".*?</div>)\s*</header>'
    
    def replacer(match):
        mobile_menu = match.group(1)
        return '\n  </header>\n' + mobile_menu + '\n'
        
    new_content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filename}")
    else:
        print(f"No match in {filename}")

