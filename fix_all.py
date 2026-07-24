import os
import re

mobile_menu_html = """
  <!-- Mobile menu -->
  <div class="mobile-menu" id="mobile-menu" aria-hidden="true">
    <ul class="mobile-nav-list" role="list">
      <li><a href="/" class="mobile-nav-link">Bosh sahifa</a></li>
      <li><a href="/biz-haqimizda/" class="mobile-nav-link">Biz haqimizda</a></li>
      <li><a href="/yetakchilar/" class="mobile-nav-link">Yetakchilar</a></li>
      <li><a href="/jurnal/" class="mobile-nav-link">Yetakchilar online jurnali</a></li>
      <li><a href="/iqtiboslar/" class="mobile-nav-link">Yetakchilardan iqtiboslar</a></li>
      <li><a href="/ariza/" class="mobile-nav-link mobile-nav-cta">Ariza qoldirish</a></li>
    </ul>
  </div>
"""

template_dir = 'templates'
for filename in os.listdir(template_dir):
    if not filename.endswith('.html'):
        continue
    if filename == "index.html":
        continue # Already fixed
        
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'class="mobile-menu"' not in content:
        # replace </header> with </header> \n {mobile_menu_html}
        new_content = content.replace('</header>', '</header>\n' + mobile_menu_html)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added mobile menu to {filename}")
