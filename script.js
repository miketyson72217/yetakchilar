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
const applyForm = document.getElementById('apply-form');
if (applyForm) {
  applyForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const btn = applyForm.querySelector('#btn-submit');
    const originalText = btn.textContent;

    // Validate
    const inputs = applyForm.querySelectorAll('input, select, textarea');
    let valid = true;

    inputs.forEach(input => {
      if (input.required && !input.value.trim()) {
        input.style.borderColor = '#ef4444';
        valid = false;
        setTimeout(() => { input.style.borderColor = ''; }, 2000);
      }
    });

    if (!valid) return;

    // Success animation
    btn.textContent = '✓ Ariza yuborildi!';
    btn.style.background = '#22c55e';
    btn.style.borderColor = '#22c55e';
    btn.style.color = '#fff';
    btn.disabled = true;

    setTimeout(() => {
      btn.textContent = originalText;
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.style.color = '';
      btn.disabled = false;
      applyForm.reset();
    }, 3500);
  });
}

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
