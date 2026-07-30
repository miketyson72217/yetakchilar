import os
import re

FOOTER_HTML = """  <footer class="site-footer" id="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand" id="footer-brand">
        <img src="/static/images/main_logo.png" alt="O‘zYYE Logo" class="footer-logo" id="footer-logo" />
        <p class="footer-desc">O‘zbekiston Yetakchi Yoshlari Ensiklopediyasi — kelajak qurayotgan zamondoshlarimiz haqida.</p>
        <div class="footer-social" id="footer-social">
          <a href="https://t.me/uzyye_rasmiy" target="_blank" class="social-link" id="social-telegram" aria-label="Telegram">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-1.97 9.289c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.932z"/></svg>
          </a>
          <a href="#" class="social-link" id="social-instagram" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-nav" id="footer-nav">
        <h3 class="footer-nav-title">Sahifalar</h3>
        <ul class="footer-nav-list" role="list">
          <li><a href="/">Bosh sahifa</a></li>
          <li><a href="/biz-haqimizda/">Biz haqimizda</a></li>
          <li><a href="/yetakchilar/">Yetakchilar</a></li>
          <li><a href="/jurnal/">Online jurnal</a></li>
          <li><a href="/ariza/">Ariza qoldirish</a></li>
        </ul>
      </div>

    </div>
    <div class="footer-bottom" id="footer-bottom" style="text-align:center; padding:24px 0; border-top:1px solid rgba(255,255,255,0.1);">
      <div class="container">
        <p style="font-size:1rem; font-weight:800; color:#00A6EB; margin-bottom:8px;">Biz bilan tarixga kiring!</p>
        <p style="font-size:0.85rem; color:#94a3b8; font-weight:700;">© 2026 O‘zbekiston Yetakchi Yoshlari Ensiklopediyasi (yetakchilar.uz). Barcha huquqlar himoyalangan.</p>
      </div>
    </div>
  </footer>"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <footer ...> to </footer> and replace it with FOOTER_HTML
    new_content = re.sub(r'<footer[^>]*>.*?</footer>', FOOTER_HTML, content, flags=re.DOTALL)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes (or already updated): {filepath}")

templates_dir = '/home/lochinbek/Desktop/yetakchilar/templates'
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        process_file(filepath)
