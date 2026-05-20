/**
 * ═══════════════════════════════════════════════════════════
 * MASAR WERBEAGENTUR — app.js
 * Vanilla JS: Multi-step Form • Price Estimator
 *             Before/After Slider • DSGVO Cookie System
 * ═══════════════════════════════════════════════════════════
 */

'use strict';

// ═══════════════════════════════════════════════════════════
// 1. MULTI-STEP B2B BRIEFING FORM
// ═══════════════════════════════════════════════════════════
const MasarForm = {
  current: 1,
  total: 4,
  data: {},

  init() {
    const form = document.getElementById('masarForm');
    if (!form) return;

    this.updateProgress();
    this.bindButtons();
    this.bindFileUpload();
  },

  updateProgress() {
    const pct = ((this.current - 1) / (this.total - 1)) * 100;
    const bar = document.getElementById('formProgress');
    const step = document.getElementById('formStep');
    if (bar) bar.style.width = pct + '%';
    if (step) step.textContent = `Schritt ${this.current} von ${this.total}`;

    // Show/hide steps
    document.querySelectorAll('.form-step').forEach(el => {
      el.classList.toggle('active', parseInt(el.dataset.step) === this.current);
    });

    // Update nav buttons
    const prev = document.getElementById('btnPrev');
    const next = document.getElementById('btnNext');
    const submit = document.getElementById('btnSubmit');
    if (prev)   prev.style.display   = this.current > 1 ? 'block' : 'none';
    if (next)   next.style.display   = this.current < this.total ? 'block' : 'none';
    if (submit) submit.style.display = this.current === this.total ? 'block' : 'none';
  },

  next() {
    if (!this.validateStep(this.current)) return;
    if (this.current < this.total) {
      this.current++;
      this.updateProgress();
      window.scrollTo({ top: document.getElementById('masarForm').offsetTop - 100, behavior: 'smooth' });
    }
  },

  prev() {
    if (this.current > 1) {
      this.current--;
      this.updateProgress();
    }
  },

  validateStep(step) {
    const stepEl = document.querySelector(`.form-step[data-step="${step}"]`);
    if (!stepEl) return true;
    const required = stepEl.querySelectorAll('[required]');
    let valid = true;
    required.forEach(el => {
      el.classList.remove('field-error');
      if (!el.value.trim()) {
        el.classList.add('field-error');
        valid = false;
      }
    });
    if (!valid) {
      stepEl.querySelector('.field-error')?.focus();
    }
    return valid;
  },

  bindButtons() {
    document.getElementById('btnNext')?.addEventListener('click', () => this.next());
    document.getElementById('btnPrev')?.addEventListener('click', () => this.prev());
    document.getElementById('masarForm')?.addEventListener('submit', (e) => this.submit(e));
  },

  bindFileUpload() {
    const zone = document.getElementById('uploadZone');
    const input = document.getElementById('fileInput');
    if (!zone || !input) return;

    zone.addEventListener('click', () => input.click());
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('drag-over');
      if (e.dataTransfer.files[0]) this.handleFile(e.dataTransfer.files[0]);
    });
    input.addEventListener('change', () => {
      if (input.files[0]) this.handleFile(input.files[0]);
    });
  },

  handleFile(file) {
    const MAX = 5 * 1024 * 1024;
    const allowed = ['image/jpeg','image/png','image/gif','application/pdf','image/svg+xml'];
    if (file.size > MAX) {
      this.showNotif('Datei zu groß (max. 5MB)', 'error');
      return;
    }
    if (!allowed.includes(file.type)) {
      this.showNotif('Dateityp nicht erlaubt', 'error');
      return;
    }
    const label = document.getElementById('uploadLabel');
    if (label) label.textContent = `✓ ${file.name} (${(file.size/1024).toFixed(0)} KB)`;
    this.data.file = file;
  },

  async submit(e) {
    e.preventDefault();
    if (!this.validateStep(this.total)) return;

    const consent = document.getElementById('consentCheck');
    if (!consent?.checked) {
      this.showNotif('Bitte stimmen Sie der Datenschutzerklärung zu.', 'error');
      return;
    }

    const btn = document.getElementById('btnSubmit');
    if (btn) { btn.disabled = true; btn.textContent = 'Wird gesendet...'; }

    const fd = new FormData(e.target);
    fd.append('estimate', MasarPrice.getEstimate());
    if (this.data.file) fd.append('attachment', this.data.file);

    try {
      const res = await fetch('/mail.php', { method: 'POST', body: fd });
      const json = await res.json();

      if (json.status === 'success') {
        e.target.innerHTML = `
          <div class="form-success">
            <div class="success-icon">✅</div>
            <h3>Vielen Dank, ${document.getElementById('fieldName')?.value || ''}!</h3>
            <p>Wir haben Ihre Anfrage erhalten und melden uns innerhalb von <strong>24 Stunden</strong>.</p>
            <p style="margin-top:1rem;">
              <a href="tel:+491785143918" class="btn btn-teal">📞 0178 514 3918</a>
            </p>
          </div>`;
      } else {
        this.showNotif(json.message || 'Fehler beim Senden', 'error');
        if (btn) { btn.disabled = false; btn.textContent = 'Anfrage senden'; }
      }
    } catch {
      this.showNotif('Verbindungsfehler. Bitte versuchen Sie es erneut.', 'error');
      if (btn) { btn.disabled = false; btn.textContent = 'Anfrage senden'; }
    }
  },

  showNotif(msg, type = 'info') {
    const el = document.getElementById('formNotif');
    if (!el) return;
    el.className = `form-notif notif-${type}`;
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 5000);
  }
};


// ═══════════════════════════════════════════════════════════
// 2. INTERACTIVE PRICE ESTIMATOR
// ═══════════════════════════════════════════════════════════
const MasarPrice = {
  prices: {
    fahrzeug: {
      klein:        { base: 125,  chip: 'Kleinwagen',    label: 'Kleinwagen Teilbeklebung' },
      transporter:  { base: 369,  chip: 'Transporter',   label: 'Transporter Teilbeklebung' },
      vollfolierung:{ base: 1500, chip: 'Vollfolierung',  label: 'Vollfolierung Transporter' },
      lkw:          { base: 2500, chip: 'LKW',           label: 'LKW-Beschriftung' },
    },
    leuchtreklame: {
      small:  { base: 299,  chip: 'bis 50 cm',   label: 'Leuchtreklame bis 50 cm' },
      medium: { base: 599,  chip: 'bis 100 cm',  label: 'Leuchtreklame bis 100 cm' },
      large:  { base: 1200, chip: 'bis 200 cm',  label: 'Leuchtreklame bis 200 cm' },
      custom: { base: 2500, chip: 'Großanlage',  label: 'Individuelle Großanlage' },
    },
    print: {
      flyer:       { base: 49,  chip: 'Flyer A5',     label: 'Flyer A5 (500 Stück)' },
      visitenkarte:{ base: 39,  chip: 'Visitenkarte', label: 'Visitenkarten (250 Stück)' },
      broschure:   { base: 149, chip: 'Broschüre',    label: 'Broschüre A5 (100 Stück)' },
      plakat:      { base: 79,  chip: 'Plakat A3',    label: 'Plakate A3 (50 Stück)' },
    }
  },

  currentEstimate: 0,

  init() {
    const calc = document.getElementById('priceCalc');
    if (!calc) return;

    // Category tab clicks
    calc.querySelectorAll('.calc-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        calc.querySelectorAll('.calc-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.buildVariants(btn.dataset.val);
        this.calculate();
      });
    });

    // Checkbox changes
    document.getElementById('calcExpress')?.addEventListener('change', () => this.calculate());
    document.getElementById('calcDesign')?.addEventListener('change', () => this.calculate());

    // Initialize with first category
    this.buildVariants(Object.keys(this.prices)[0]);
    this.calculate();
  },

  buildVariants(category) {
    const container = document.getElementById('calcVariantChips');
    const hidden    = document.getElementById('calcVariant');
    if (!container || !hidden) return;

    const opts = this.prices[category] || {};
    const keys = Object.keys(opts);

    container.innerHTML = keys.map((key, i) =>
      `<button class="calc-chip${i === 0 ? ' active' : ''}" data-val="${key}" type="button">${opts[key].chip}</button>`
    ).join('');

    hidden.value = keys[0] || '';

    container.querySelectorAll('.calc-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        container.querySelectorAll('.calc-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        hidden.value = chip.dataset.val;
        this.calculate();
      });
    });
  },

  calculate() {
    const activeTab = document.querySelector('#priceCalc .calc-tab.active');
    const category  = activeTab?.dataset.val || Object.keys(this.prices)[0];
    const variant   = document.getElementById('calcVariant')?.value;
    const express   = document.getElementById('calcExpress')?.checked;
    const design    = document.getElementById('calcDesign')?.checked;

    if (!variant) return;
    const item = this.prices[category]?.[variant];
    if (!item) return;

    let price = item.base;
    if (express) price = Math.round(price * 1.25);
    if (design)  price += 80;

    this.currentEstimate = price;

    const display = document.getElementById('priceDisplay');
    const label   = document.getElementById('priceLabel');
    if (display) {
      display.textContent = `ab ${price.toLocaleString('de-DE')} €`;
      display.classList.remove('price-pop');
      void display.offsetWidth;
      display.classList.add('price-pop');
    }
    if (label) label.textContent = item.label.toUpperCase();
  },

  getEstimate() {
    return this.currentEstimate > 0
      ? `ab ${this.currentEstimate.toLocaleString('de-DE')} € (unverbindlich)`
      : 'Nicht berechnet';
  },

  requestOffer() {
    // Fill contact form service field if present
    const serviceField = document.getElementById('fieldService');
    const activeTab    = document.querySelector('#priceCalc .calc-tab.active');
    const category     = activeTab?.dataset.val || Object.keys(this.prices)[0];
    const variant      = document.getElementById('calcVariant')?.value;
    const item         = this.prices[category]?.[variant];
    if (serviceField && item) serviceField.value = item.label;

    // Scroll to contact section
    const target = document.getElementById('masarForm') || document.getElementById('kontakt');
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};


// ═══════════════════════════════════════════════════════════
// 3. BEFORE/AFTER SLIDER (No dependencies, keyboard accessible)
// ═══════════════════════════════════════════════════════════
const BeforeAfterSlider = {
  init() {
    document.querySelectorAll('.ba-slider').forEach(slider => this.setup(slider));
  },

  setup(slider) {
    const handle   = slider.querySelector('.ba-handle');
    const overlay  = slider.querySelector('.ba-after');
    if (!handle || !overlay) return;

    let dragging = false;
    let startX = 0;
    let startPct = 50;

    const getPercent = (clientX) => {
      const rect = slider.getBoundingClientRect();
      const pct = ((clientX - rect.left) / rect.width) * 100;
      return Math.max(2, Math.min(98, pct));
    };

    const move = (pct) => {
      overlay.style.width = pct + '%';
      handle.style.left   = pct + '%';
      handle.setAttribute('aria-valuenow', Math.round(pct));
    };

    // Initialize at 50%
    move(50);

    // Pointer Events (mouse + touch + pen)
    handle.addEventListener('pointerdown', e => {
      dragging = true;
      handle.setPointerCapture(e.pointerId);
      e.preventDefault();
    });

    slider.addEventListener('pointermove', e => {
      if (!dragging) return;
      move(getPercent(e.clientX));
    });

    slider.addEventListener('pointerup',     () => { dragging = false; });
    slider.addEventListener('pointercancel', () => { dragging = false; });

    // Click on slider track
    slider.addEventListener('click', e => {
      if (e.target === handle) return;
      move(getPercent(e.clientX));
    });

    // Keyboard accessibility (← →)
    handle.setAttribute('tabindex', '0');
    handle.setAttribute('role', 'slider');
    handle.setAttribute('aria-label', 'Vorher/Nachher Vergleich');
    handle.setAttribute('aria-valuemin', '0');
    handle.setAttribute('aria-valuemax', '100');
    handle.setAttribute('aria-valuenow', '50');

    handle.addEventListener('keydown', e => {
      const curr = parseFloat(overlay.style.width) || 50;
      if (e.key === 'ArrowLeft')  { move(Math.max(2, curr - 2));  e.preventDefault(); }
      if (e.key === 'ArrowRight') { move(Math.min(98, curr + 2)); e.preventDefault(); }
      if (e.key === 'Home')       { move(2);  e.preventDefault(); }
      if (e.key === 'End')        { move(98); e.preventDefault(); }
    });
  }
};


// ═══════════════════════════════════════════════════════════
// 4. TESTIMONIAL SLIDER
// ═══════════════════════════════════════════════════════════
const TestiSlider = {
  current: 0,
  auto: null,

  init() {
    const slider = document.querySelector('.testi-slider');
    if (!slider) return;

    const items = slider.querySelectorAll('.testi-item');
    const dots  = slider.querySelectorAll('.testi-dot');
    if (!items.length) return;

    const show = (idx) => {
      items.forEach((el, i) => el.classList.toggle('active', i === idx));
      dots.forEach((el, i)  => el.classList.toggle('active', i === idx));
      this.current = idx;
    };

    dots.forEach((dot, i) => dot.addEventListener('click', () => {
      clearInterval(this.auto);
      show(i);
    }));

    slider.querySelector('.testi-prev')?.addEventListener('click', () => {
      clearInterval(this.auto);
      show((this.current - 1 + items.length) % items.length);
    });

    slider.querySelector('.testi-next')?.addEventListener('click', () => {
      clearInterval(this.auto);
      show((this.current + 1) % items.length);
    });

    show(0);
    this.auto = setInterval(() => show((this.current + 1) % items.length), 5000);
  }
};


// ═══════════════════════════════════════════════════════════
// 5. STICKY CTA
// ═══════════════════════════════════════════════════════════
const StickyCta = {
  init() {
    const el = document.getElementById('stickyCta');
    if (!el) return;
    window.addEventListener('scroll', () => {
      el.classList.toggle('visible', window.scrollY > 500);
    }, { passive: true });
    // Hide banner when CTA button clicked
    document.getElementById('stickyCtaBtn')?.addEventListener('click', () => {
      el.style.display = 'none';
    });
  }
};


// ═══════════════════════════════════════════════════════════
// 6. SMOOTH SCROLL & NAV
// ═══════════════════════════════════════════════════════════
const Nav = {
  init() {
    // Hamburger
    const ham = document.getElementById('hamburger');
    const mob = document.getElementById('mobNav');
    ham?.addEventListener('click', () => mob?.classList.toggle('open'));

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', e => {
        const target = document.querySelector(a.getAttribute('href'));
        if (!target) return;
        e.preventDefault();
        const offset = target.getBoundingClientRect().top + window.scrollY - 90;
        window.scrollTo({ top: offset, behavior: 'smooth' });
        mob?.classList.remove('open');
      });
    });
  }
};


// ═══════════════════════════════════════════════════════════
// 7. SCROLL REVEAL ANIMATIONS
// ═══════════════════════════════════════════════════════════
const Reveal = {
  init() {
    const obs = new IntersectionObserver(entries => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          setTimeout(() => e.target.classList.add('in'), i * 80);
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.08 });

    document.querySelectorAll('.reveal, .reveal-l, .reveal-r').forEach(el => obs.observe(el));
  }
};


// ═══════════════════════════════════════════════════════════
// 8. FAQ ACCORDION
// ═══════════════════════════════════════════════════════════
const FAQ = {
  init() {
    document.querySelectorAll('.faq-q').forEach(btn => {
      btn.addEventListener('click', () => {
        const answer = btn.nextElementSibling;
        const icon   = btn.querySelector('.faq-ic');
        const isOpen = answer?.classList.toggle('open');
        if (icon) {
          icon.classList.toggle('open', isOpen);
          icon.textContent = isOpen ? '−' : '+';
        }
      });
    });
  }
};



// ═══════════════════════════════════════════════════════════
// INIT ALL MODULES
// ═══════════════════════════════════════════════════════════
function initAll() {
  Nav.init();
  Reveal.init();
  StickyCta.init();
  FAQ.init();
  MasarForm.init();
  MasarPrice.init();
  BeforeAfterSlider.init();
  TestiSlider.init();
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAll);
} else {
  initAll();
}

// Export for use in HTML
window.MasarForm  = MasarForm;
window.MasarPrice = MasarPrice;
