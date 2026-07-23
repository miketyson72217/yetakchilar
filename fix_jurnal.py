import re

with open('templates/jurnal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We replace the main journal rendering part
# The block starts at `<div class="journal-master-container">` and ends right before `</main>`
start_marker = '<div class="journal-master-container">'
end_marker = '</main>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

coming_soon_html = """
        <!-- Coming Soon Card -->
        <div style="background: var(--bg-surface); border: 1px solid rgba(0, 166, 235, 0.35); border-radius: var(--radius-xl); padding: 70px 40px; text-align: center; backdrop-filter: blur(24px); box-shadow: 0 35px 100px rgba(0,0,0,0.7); max-width: 840px; margin: 40px auto 80px; position: relative; overflow: hidden;" class="reveal">
          <div style="position: absolute; top: -60px; left: 50%; transform: translateX(-50%); width: 300px; height: 300px; background: radial-gradient(circle, rgba(0,166,235,0.25) 0%, rgba(0,0,0,0) 70%); pointer-events: none; border-radius: 50%;"></div>
          <span style="display: inline-flex; align-items: center; background: linear-gradient(135deg, #00A6EB 0%, #0066FF 100%); color: #ffffff; font-weight: 900; font-size: 0.85rem; padding: 7px 22px; border-radius: 100px; letter-spacing: 0.15em; text-transform: uppercase; box-shadow: 0 4px 20px rgba(0,166,235,0.4); margin-bottom: 24px;">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" style="margin-right:8px;"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path></svg>
            TEZ KUNDA / COMING SOON
          </span>
          <h2 style="font-size: clamp(2rem, 4vw, 3rem); font-weight: 900; color: var(--text-primary); margin-bottom: 20px; line-height: 1.2;">Yangi Nashr Tez Kunda!</h2>
          <p style="font-size: 1.15rem; color: var(--text-secondary); line-height: 1.7; max-width: 650px; margin: 0 auto 36px;">Oʻzbekiston Yetakchi Yoshlari jurnalining navbatdagi maxsus soni tayyorlanmoqda. Tez kunda yangi va ilhomlantiruvchi hikoyalar bilan qaytamiz!</p>
          <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
            <a href="/" class="btn btn-primary" style="padding: 14px 28px;">Bosh sahifaga qaytish &rarr;</a>
            <a href="/ariza/" class="btn btn-outline" style="padding: 14px 28px;">Ariza qoldirish</a>
          </div>
        </div>
"""

new_body = """<div class="journal-master-container">
      <div class="container">

        {% if journal %}
        <!-- Magazine Overview Hero -->
        <div class="magazine-hero-card reveal">
          <div class="mag-cover-standalone" id="open-flipbook-trigger">
            <span class="cover-tag-pill">3D FLIPBOOK</span>
            <img src="{% if journal and journal.front_cover %}{{ journal.front_cover.url }}{% else %}/static/images/journal_front_cover.png{% endif %}" onerror="this.src='/static/images/journal_front_cover.png'" alt="Jurnal muqovasi" class="mag-cover-img-flat" />
          </div>

          <div class="mag-info-block">
            <div class="mag-meta-row">
              <span class="mag-meta-item">{{ journal.issue_number }}-SON</span>
              <span class="mag-meta-item" style="color:#22c55e; background:rgba(34,197,94,0.1); border-color:rgba(34,197,94,0.25);">BEPUL MUTOLAA</span>
            </div>
            <h1>{{ journal.title }}</h1>
            <p class="mag-desc-para">{{ journal.description }}</p>

            <div class="mag-specs-grid">
              <div class="spec-box">
                <strong>Muallif</strong>
                <span>{% if journal.author and journal.author != "Oʻzbekiston Yetakchi Yoshlari" %}{{ journal.author }}{% else %}Oʻzbekiston Yetakchi Yoshlari{% endif %}</span>
              </div>
              <div class="spec-box">
                <strong>Chop etilgan sana</strong>
                <span>{{ journal.release_date }}</span>
              </div>
              <div class="spec-box">
                <strong>Sahifalar soni</strong>
                <span>{{ journal.pages_count }} Sahifa</span>
              </div>
              <div class="spec-box">
                <strong>Fayl hajmi</strong>
                <span>{{ journal.file_size }}</span>
              </div>
              <div class="spec-box">
                <strong>ISSN Indeksi</strong>
                <span>{{ journal.issn }}</span>
              </div>
            </div>

            <div class="mag-actions-flex">
              <a href="#flipbook-stage" class="btn btn-primary">
                3D Virtual Kitobni Ochish &rarr;
              </a>
              {% if journal.pdf_file %}
              <a href="{{ journal.pdf_file.url }}" download class="btn btn-outline" id="btn-download-pdf">
                Yuklab olish (PDF)
              </a>
              {% endif %}
              <button class="btn btn-outline" id="btn-share-journal">
                Ulashish
              </button>
            </div>
          </div>
        </div>

        <!-- Cover Stories -->
        <div class="cover-stories-section reveal">
          <span class="section-label">EKSKLYUZIV JURNAL MAQOLALARI</span>
          <h2 class="section-title">Ushbu sonda nimalar bor?</h2>
          <p class="section-desc">Chuqurlashtirilgan jurnalistika, tahliliy suhbatlar va mualliflik darslari</p>

          <div class="stories-grid">
            {% for article in journal.articles.all %}
            <div class="story-card">
              <div>
                <div class="story-badge">{{ article.category }}</div>
                <h3 class="story-title">{{ article.title }}</h3>
                <p class="story-desc">{{ article.short_description }}</p>
              </div>
              <div class="story-meta"><span>{{ article.author_name }}</span><span>SAHIFA {% if article.page_number < 10 %}0{% endif %}{{ article.page_number }}</span></div>
            </div>
            {% empty %}
            <div style="grid-column: 1 / -1; padding: 20px; text-align: center; color: var(--text-tertiary);">
                Hozircha maqolalar mavjud emas.
            </div>
            {% endfor %}
          </div>
        </div>

        <!-- 3D Flipbook Reader Stage -->
        <div class="flipbook-stage-wrapper reveal" id="flipbook-stage">

          <!-- Toolbar -->
          <div class="flipbook-toolbar">
            <div class="toolbar-group">
              <button class="tool-btn" id="tb-prev">&larr; Oldingi</button>
              <div class="page-input-wrap">
                <input type="number" class="page-num-input" id="tb-page-num" value="1" min="1" />
                <span>/ <span id="tb-total-pages">{{ journal.pages_count|default:"10" }}</span></span>
              </div>
              <button class="tool-btn" id="tb-next">Keyingi &rarr;</button>
            </div>

            <div class="toolbar-group">
              <button class="tool-btn" id="tb-zoom-out">Kichik &minus;</button>
              <button class="tool-btn" id="tb-zoom-reset">100%</button>
              <button class="tool-btn" id="tb-zoom-in">Katta +</button>
              <button class="tool-btn" id="tb-thumbs">Miniatyura</button>
              <button class="tool-btn" id="tb-fullscreen">Toʻliq ekran</button>
            </div>
          </div>

          <!-- Flipbook viewport -->
          <div class="flipbook-viewport" id="flipbook-viewport">
            <div id="flipbook-instance">

              <!-- Sahifa 1: Old muqova (HARD COVER) -->
              <div class="fpage fpage-cover" data-density="hard">
                <img src="{% if journal and journal.front_cover %}{{ journal.front_cover.url }}{% else %}/static/images/journal_front_cover.png{% endif %}" onerror="this.src='/static/images/journal_front_cover.png'" alt="Old muqova" />
              </div>

              <!-- Sahifa 2: Jurnal haqida (SOFT PAGE) -->
              <div class="fpage fpage-inner" data-density="soft">
                <div class="fpage-content">
                  <div class="mag-page-header">
                    <span>OʻzYYE JURNALI — {{ journal.issue_number }}-SON</span>
                    <span>YETAKCHI YOSHLAR</span>
                  </div>
                  <div class="page-section-title">02 | JURNAL HAQIDA</div>
                  <div class="page-author">Oʻzbekiston Yetakchi Yoshlari</div>
                  <div class="page-body">
                    <p>Ushbu elektron jurnal Oʻzbekistonning turli sohalarida yutuqlarga erishayotgan faol yoshlarning tajribasi, maslahatlari hamda ilhomlantiruvchi hikoyalarini jamlagan loyihadir.</p>
                    <div class="page-pull-quote">"Kelajakni bugungi mehnat va intizom belgilaydi."</div>
                    <p>Ushbu sonda biznes, IT, sport va ilm-fan sohalarida faoliyat yuritayotgan yoshlarimiz tajribasi bilan tanishishingiz mumkin.</p>
                  </div>
                  <div class="mag-page-footer">
                    <span>Oʻzbekiston Yetakchi Yoshlari</span>
                    <span class="page-num-tag">SAHIFA 02</span>
                  </div>
                </div>
              </div>

              <!-- Sahifa 3: Mundarija (SOFT PAGE) -->
              <div class="fpage fpage-inner" data-density="soft">
                <div class="fpage-content">
                  <div class="mag-page-header">
                    <span>OʻzYYE JURNALI</span>
                    <span>MUNDARIJA</span>
                  </div>
                  <div class="page-section-title">03 | MUNDARIJA</div>
                  <div style="flex:1; overflow:hidden; overflow-y:auto;">
                    {% for article in journal.articles.all %}
                    <div class="toc-item">
                      <div><div class="toc-item-title">{{ article.title }}</div><div class="toc-item-sub">{{ article.author_name }} — {{ article.category }}</div></div>
                      <div class="toc-item-page">{% if article.page_number < 10 %}0{% endif %}{{ article.page_number }}</div>
                    </div>
                    {% endfor %}
                  </div>
                  <div class="mag-page-footer">
                    <span>Oʻzbekiston Yetakchi Yoshlari</span>
                    <span class="page-num-tag">SAHIFA 03</span>
                  </div>
                </div>
              </div>

              {% for article in journal.articles.all %}
              <!-- Sahifa: Maqola (SOFT PAGE) -->
              <div class="fpage fpage-inner" data-density="soft">
                <div class="fpage-content">
                  <div class="mag-page-header">
                    <span>{{ article.category }}</span>
                    <span>MAQOLA</span>
                  </div>
                  <div class="page-section-title">{% if article.page_number < 10 %}0{% endif %}{{ article.page_number }} | {{ article.title }}</div>
                  <div class="page-author">Muallif: {{ article.author_name }}</div>
                  <div class="page-body">
                    {% if article.pull_quote %}
                    <div class="page-pull-quote">"{{ article.pull_quote }}"</div>
                    {% endif %}
                    <p>{{ article.content|linebreaksbr }}</p>
                  </div>
                  <div class="mag-page-footer">
                    <span>Maqola</span>
                    <span class="page-num-tag">SAHIFA {% if article.page_number < 10 %}0{% endif %}{{ article.page_number }}</span>
                  </div>
                </div>
              </div>
              {% endfor %}

              <!-- Oxirgi Sahifa: Orqa muqova (HARD COVER) -->
              <div class="fpage fpage-cover" data-density="hard">
                <img src="{% if journal and journal.back_cover %}{{ journal.back_cover.url }}{% else %}/static/images/journal_back_cover.png{% endif %}" onerror="this.src='/static/images/journal_back_cover.png'" alt="Orqa muqova" />
              </div>

            </div>
          </div>
        </div>

        {% else %}
""" + coming_soon_html + """
        {% endif %}

      </div>
    </div>
"""

new_content = content[:start_idx] + new_body + content[end_idx:]

# 2. Now letʼs fix the thumbs-grid
thumbs_grid_start = new_content.find('<div class="thumbs-grid" id="thumbs-grid">')
thumbs_grid_end = new_content.find('</div>\n    </div>\n  </div>\nʼn  <footer')

if thumbs_grid_start != -1 and thumbs_grid_end != -1:
    thumbs_grid_html = """<div class="thumbs-grid" id="thumbs-grid">
        <div class="thumb-card active" onclick="goToPageNum(0)">
          <img src="{% if journal and journal.front_cover %}{{ journal.front_cover.url }}{% else %}/static/images/journal_front_cover.png{% endif %}" onerror="this.src='/static/images/journal_front_cover.png'" />
          <div class="thumb-label">1 — Old Muqova</div>
        </div>
        <div class="thumb-card" onclick="goToPageNum(1)"><div class="thumb-card-inner">02 — Jurnal Haqida</div><div class="thumb-label">2</div></div>
        <div class="thumb-card" onclick="goToPageNum(2)"><div class="thumb-card-inner">03 — Mundarija</div><div class="thumb-label">3</div></div>
        
        {% for article in journal.articles.all %}
        <div class="thumb-card" onclick="goToPageNum({{ forloop.counter|add:2 }})"><div class="thumb-card-inner">{% if article.page_number < 10 %}0{% endif %}{{ article.page_number }} — {{ article.title|truncatechars:20 }}</div><div class="thumb-label">{{ forloop.counter|add:3 }}</div></div>
        {% endfor %}

        <div class="thumb-card" onclick="goToPageNum({{ journal.articles.count|add:3 }})">
          <img src="{% if journal and journal.back_cover %}{{ journal.back_cover.url }}{% else %}/static/images/journal_back_cover.png{% endif %}" onerror="this.src='/static/images/journal_back_cover.png'" />
          <div class="thumb-label">{{ journal.articles.count|add:4 }} — Orqa Muqova</div>
        </div>
      </div>"""
    
    new_content = new_content[:thumbs_grid_start] + thumbs_grid_html + new_content[thumbs_grid_end:]

with open('templates/jurnal.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Template updated.")
