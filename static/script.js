/* =============================================
   script.js — OʻzYYE Website JS
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

        // Check if dynamic success banner exists or create one
        let alertBox = document.getElementById('form-success-alert');
        if (!alertBox) {
          alertBox = document.createElement('div');
          alertBox.id = 'form-success-alert';
          alertBox.style.cssText = 'background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(16, 185, 129, 0.2)); border: 1.5px solid #22c55e; color: #ffffff; padding: 22px 28px; border-radius: 16px; margin-bottom: 32px; font-weight: 700; text-align: center; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(34, 197, 94, 0.25); display: flex; align-items: center; justify-content: center; gap: 14px; animation: fadeIn 0.4s ease;';
          alertBox.innerHTML = `
            <svg style="width: 32px; height: 32px; color: #22c55e; flex-shrink: 0;" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span style="font-size: 1.1rem; line-height: 1.5;">${data.message}</span>
          `;
          form.parentNode.insertBefore(alertBox, form);
        } else {
          alertBox.querySelector('span').textContent = data.message;
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
        alert('Xatolik yuz berdi. Iltimos qaytadan urinib koʻring.');
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    } catch (err) {
      console.error(err);
      alert('Tarmoq xatosi yuz berdi. Iltimos qaytadan urinib koʻring.');
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
    const current = Math.floor(eased * numTarget);
    el.textContent = current + (isPlus ? '+' : suffix);
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
        const num = parseInt(text);
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
