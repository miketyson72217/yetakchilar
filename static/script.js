/* =============================================
   script.js — O‘zYYE Website JS
   ============================================= */

// ===== HEADER SCROLL EFFECT =====
const header = document.getElementById('main-header');
if (header) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }, { passive: true });
}

// ===== MOBILE BURGER MENU =====
const burgerBtn = document.getElementById('burger-btn');
const mobileMenu = document.getElementById('mobile-menu');

if (burgerBtn && mobileMenu) {
  burgerBtn.addEventListener('click', () => {
    const isOpen = burgerBtn.classList.toggle('open');
    mobileMenu.classList.toggle('open', isOpen);
    burgerBtn.setAttribute('aria-expanded', isOpen);
    mobileMenu.setAttribute('aria-hidden', !isOpen);
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!burgerBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
      burgerBtn.classList.remove('open');
      mobileMenu.classList.remove('open');
      burgerBtn.setAttribute('aria-expanded', 'false');
      mobileMenu.setAttribute('aria-hidden', 'true');
    }
  });

  // Close when a mobile link is clicked
  mobileMenu.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => {
      burgerBtn.classList.remove('open');
      mobileMenu.classList.remove('open');
      burgerBtn.setAttribute('aria-expanded', 'false');
      mobileMenu.setAttribute('aria-hidden', 'true');
    });
  });
}

// ===== SCROLL REVEAL ANIMATIONS =====
const revealEls = document.querySelectorAll(
  '.stat-card, .leader-card, .quote-card, .journal-feature, .about-text, .about-stats'
);

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, i * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
  });
}

// ===== APPLY FORM SUBMISSION =====
const applyForms = document.querySelectorAll('.apply-form');
applyForms.forEach(form => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = form.querySelector('button[type="submit"]');
    if (!btn) return;
    const originalText = btn.innerHTML;

    // Validate
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let valid = true;

    inputs.forEach(input => {
      if (!input.value.trim()) {
        input.style.borderColor = '#ef4444';
        valid = false;
        setTimeout(() => { input.style.borderColor = ''; }, 2500);
      }
    });

    if (!valid) return;

    btn.disabled = true;
    btn.innerHTML = '⌛ Yuborilmoqda...';

    try {
      const formData = new FormData(form);

      // Get CSRF Token
      let csrfToken = '';
      const csrfInput = form.querySelector('[name=csrfmiddlewaretoken]');
      if (csrfInput) {
        csrfToken = csrfInput.value;
      } else {
        const match = document.cookie.match(/csrftoken=([^;]+)/);
        if (match) csrfToken = match[1];
      }

      const response = await fetch('/ariza/', {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken
        },
        body: formData
      });

      const data = await response.json();


      if (response.ok && data.status === 'ok') {
        btn.innerHTML = '✓ Ariza yuborildi!';
        btn.style.background = '#22c55e';
        btn.style.borderColor = '#22c55e';
        btn.style.color = '#fff';

        let alertBox = document.getElementById('form-success-alert');
        if (!alertBox) {
          alertBox = document.createElement('div');
          alertBox.id = 'form-success-alert';
          alertBox.style.cssText = 'background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(16, 185, 129, 0.2)); border: 1.5px solid #22c55e; color: #ffffff; padding: 22px 28px; border-radius: 16px; margin-bottom: 32px; font-weight: 700; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(34, 197, 94, 0.25); display: flex; flex-direction: column; gap: 20px; animation: fadeIn 0.4s ease;';
          alertBox.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; gap: 14px; text-align: center;">
              <svg style="width: 32px; height: 32px; color: #22c55e; flex-shrink: 0;" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span class="success-message-text" style="font-size: 1.1rem; line-height: 1.5;">${data.message}</span>
            </div>
            <div style="border-top: 1px solid rgba(34, 197, 94, 0.3); padding-top: 20px; text-align: center;">
              <p style="font-size: 0.95rem; margin-bottom: 12px; color: #e2e8f0; font-weight: 600;">Ijtimoiy tarmoqlardagi sahifalarimizni kuzatib boring:</p>
              <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                <a href="https://t.me/uzyye_rasmiy" target="_blank" style="background: rgba(0, 136, 204, 0.2); border: 1px solid rgba(0, 136, 204, 0.4); color: #2AABEE; padding: 8px 20px; border-radius: 100px; text-decoration: none; font-size: 0.9rem; font-weight: 700; display: inline-flex; align-items: center; gap: 8px; transition: 0.2s;">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-1.97 9.289c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.932z"/></svg> Telegram
                </a>
                <a href="#" target="_blank" style="background: rgba(225, 48, 108, 0.15); border: 1px solid rgba(225, 48, 108, 0.4); color: #E1306C; padding: 8px 20px; border-radius: 100px; text-decoration: none; font-size: 0.9rem; font-weight: 700; display: inline-flex; align-items: center; gap: 8px; transition: 0.2s;">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg> Instagram
                </a>
              </div>
            </div>
          `;
          form.parentNode.insertBefore(alertBox, form);
        } else {
          alertBox.querySelector('.success-message-text').textContent = data.message;
          alertBox.style.display = 'flex';
        }

        form.reset();

        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.style.background = '';
          btn.style.borderColor = '';
          btn.style.color = '';
          btn.disabled = false;
        }, 4000);
      } else {
        alert('Xatolik yuz berdi. Iltimos qaytadan urinib ko‘ring.');
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    } catch (err) {
      console.error(err);
      alert('Tarmoq xatosi yuz berdi. Iltimos qaytadan urinib ko‘ring.');
      btn.innerHTML = originalText;
      btn.disabled = false;
    }
  });
});


// ===== STAT COUNTER ANIMATION =====
function animateCounter(el, target, suffix = '') {
  const duration = 1500;
  const start = performance.now();
  const isPlus = suffix === '+';
  const numTarget = parseInt(target);

  const update = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(eased * numTarget);
    el.textContent = current.toLocaleString('en-US') + (isPlus ? '+' : suffix);
    if (progress < 1) requestAnimationFrame(update);
  };

  requestAnimationFrame(update);
}

const statNumbers = document.querySelectorAll('.stat-number');
if (statNumbers.length && 'IntersectionObserver' in window) {
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const text = el.textContent;
        const num = parseInt(text.replace(/,/g, ''));
        const suffix = text.includes('+') ? '+' : '';
        animateCounter(el, num, suffix);
        statsObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(el => statsObserver.observe(el));
}

// ===== ACTIVE NAV LINK =====
const navLinks = document.querySelectorAll('.nav-link');
const currentPath = window.location.pathname.split('/').pop() || 'index.html';

navLinks.forEach(link => {
  link.classList.remove('active');
  const href = link.getAttribute('href');
  if (href === currentPath || (currentPath === '' && href === 'index.html')) {
    link.classList.add('active');
  }
});

// ===== CSS GRID MASONRY =====
function initGridMasonry() {
  const grids = document.querySelectorAll('.masonry-grid');
  grids.forEach(grid => {
    const items = grid.querySelectorAll('.masonry-item');
    
    // First, reset all spans to measure natural heights
    items.forEach(item => {
      item.style.gridRowEnd = 'auto';
    });
    
    // Measure and set span
    items.forEach(item => {
      // If hidden (e.g. by search), ignore
      if(window.getComputedStyle(item).display === 'none') return;
      
      const height = item.getBoundingClientRect().height;
      // 10px is grid-auto-rows, 32px is the gap we want between items
      const rowSpan = Math.ceil((height + 32) / 10);
      item.style.gridRowEnd = `span ${rowSpan}`;
    });
  });
}

// Run masonry after images load to ensure correct heights
window.addEventListener('load', initGridMasonry);
window.addEventListener('resize', initGridMasonry);

