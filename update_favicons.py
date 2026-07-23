import os
import re

templates_dir = '/home/lochinbek/Desktop/yetakchilar/templates'
new_favicon_html = '  <link rel="icon" type="image/png" href="/static/images/main_logo2.png" />'

favicon_pattern = re.compile(r'^\s*<link rel=".*?(?:shortcut icon|icon|apple-touch-icon)".*?href=".*?favicon.*?".*?>\s*\n', re.MULTILINE)

for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check if it has favicons
        if 'favicon.ico' in content:
            # Replace the block of favicons with the new single favicon
            # First, just find the first occurrence to replace, and remove the rest
            matches = list(favicon_pattern.finditer(content))
            if matches:
                # Replace first match with new_favicon_html
                first_match = matches[0]
                new_content = content[:first_match.start()] + new_favicon_html + '\n' + content[first_match.end():]
                
                # Remove remaining matches
                # We need to re-find them because string indices changed
                while True:
                    m = favicon_pattern.search(new_content)
                    if not m:
                        break
                    new_content = new_content[:m.start()] + new_content[m.end():]
                
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated {filename}")
