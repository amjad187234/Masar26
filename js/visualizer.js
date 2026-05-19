/* ═══════════════════════════════════════════════════════════════
   MASAR — Brand Visualizer · Order Ticker · Exit Intent · Spring UX
   Vanilla JS · No dependencies · BFSG/WCAG 2.1 AA compliant
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── Visualizer state ─────────────────────────────────────── */
  var state = {
    name: 'IHRE FIRMA',
    logoImg: null,
    template: 'van',
    color: '#58d0bd',
    night: false,
    mouseX: 0, mouseY: 0,
  };

  var canvas, ctx;

  /* ── Ticker messages ──────────────────────────────────────── */
  var TICKS = [
    { msg: 'Jemand aus Berlin-Mitte hat gerade eine Fahrzeugfolierung berechnet', ago: 'vor 2 Min.' },
    { msg: 'Neuer Auftrag: Leuchtreklame aus Hamburg-Altona', ago: 'vor 4 Min.' },
    { msg: 'Flyer-Anfrage aus München — 500 Stück DIN A5', ago: 'vor 7 Min.' },
    { msg: 'Schaufensterbeklebung angefragt aus Frankfurt', ago: 'vor 11 Min.' },
    { msg: 'Van-Wrap Simulation gestartet aus Düsseldorf', ago: 'vor 14 Min.' },
    { msg: 'Webdesign-Paket bestellt — Berlin-Prenzlauer Berg', ago: 'vor 18 Min.' },
    { msg: 'Jemand aus Stuttgart berechnet gerade Messeplane', ago: 'vor 23 Min.' },
    { msg: 'Neues Angebot: Neon-Leuchtreklame für Restaurant Berlin', ago: 'vor 28 Min.' },
  ];
  var tickIdx = 0;

  /* ── Color presets ────────────────────────────────────────── */
  var COLORS = [
    '#58d0bd', '#ffffff', '#132e50',
    '#e74c3c', '#f5c000', '#3498db',
    '#9b59b6', '#2ecc71',
  ];

  /* ─────────────────────────────────────────────────────────── */
  /*  INIT                                                       */
  /* ─────────────────────────────────────────────────────────── */
  function init() {
    initTicker();
    initExitIntent();
    initVisualizer();
    initSpringEffects();
    initKineticHeadings();
    readURLParams();
  }

  /* ─────────────────────────────────────────────────────────── */
  /*  ORDER TICKER                                               */
  /* ─────────────────────────────────────────────────────────── */
  function initTicker() {
    var el = document.getElementById('orderTicker');
    if (!el) return;
    var msgEl  = el.querySelector('.ticker-msg');
    var timeEl = el.querySelector('.ticker-time');
    if (!msgEl || !timeEl) return;

    function showTick() {
      var t = TICKS[tickIdx % TICKS.length];
      tickIdx++;
      msgEl.classList.remove('ticker-msg');
      // Force reflow to restart animation
      void msgEl.offsetWidth;
      msgEl.classList.add('ticker-msg');
      msgEl.textContent = t.msg;
      timeEl.textContent = t.ago;
    }
    showTick();
    setInterval(showTick, 6000);
  }

  /* ─────────────────────────────────────────────────────────── */
  /*  EXIT INTENT                                                */
  /* ─────────────────────────────────────────────────────────── */
  function initExitIntent() {
    var overlay = document.getElementById('exitOverlay');
    if (!overlay) return;
    if (sessionStorage.getItem('exitShown')) return;

    var triggered = false;
    var closeBtn  = document.getElementById('exitClose');
    var dismissBtn= document.getElementById('exitDismiss');
    var ctaBtn    = document.getElementById('exitCta');

    function show() {
      if (triggered) return;
      triggered = true;
      sessionStorage.setItem('exitShown', '1');
      overlay.classList.add('open');
      overlay.removeAttribute('aria-hidden');
      var firstFocus = overlay.querySelector('button, a');
      if (firstFocus) firstFocus.focus();
    }
    function hide() {
      overlay.classList.remove('open');
      overlay.setAttribute('aria-hidden', 'true');
    }

    /* Detect cursor leaving toward top of viewport */
    document.addEventListener('mouseleave', function (e) {
      if (e.clientY < 20) show();
    });

    /* Keyboard trap inside overlay */
    overlay.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') hide();
    });

    if (closeBtn)   closeBtn.addEventListener('click', hide);
    if (dismissBtn) dismissBtn.addEventListener('click', hide);
    if (ctaBtn) {
      ctaBtn.addEventListener('click', function () {
        hide();
        var el = document.getElementById('kontakt');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      });
    }

    /* Click backdrop to close */
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) hide();
    });
  }

  /* ─────────────────────────────────────────────────────────── */
  /*  BRAND VISUALIZER                                           */
  /* ─────────────────────────────────────────────────────────── */
  function initVisualizer() {
    canvas = document.getElementById('visCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    resizeCanvas();
    window.addEventListener('resize', function () { resizeCanvas(); render(); });

    /* Name input */
    var nameInput = document.getElementById('visName');
    if (nameInput) {
      nameInput.addEventListener('input', function () {
        state.name = nameInput.value.toUpperCase().trim() || 'IHRE FIRMA';
        render();
        announce('Markenname aktualisiert: ' + state.name);
      });
    }

    /* Template buttons */
    document.querySelectorAll('.vis-tpl-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.vis-tpl-btn').forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        state.template = btn.dataset.tpl;
        render();
        announce('Vorlage gewechselt zu: ' + btn.textContent.trim());
      });
      btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); btn.click(); }
      });
    });

    /* Color swatches */
    document.querySelectorAll('.vis-swatch').forEach(function (sw) {
      sw.addEventListener('click', function () {
        document.querySelectorAll('.vis-swatch').forEach(function (s) { s.classList.remove('active'); s.setAttribute('aria-checked', 'false'); });
        sw.classList.add('active');
        sw.setAttribute('aria-checked', 'true');
        state.color = sw.dataset.color;
        render();
        announce('Farbe gewählt: ' + sw.dataset.color);
      });
    });

    /* Night mode toggle */
    var toggle = document.getElementById('nightToggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        state.night = !state.night;
        toggle.classList.toggle('on', state.night);
        toggle.setAttribute('aria-checked', state.night ? 'true' : 'false');
        var badge = document.getElementById('modeBadge');
        if (badge) badge.textContent = state.night ? '🌙 Nacht' : '☀️ Tag';
        render();
        announce(state.night ? 'Nachtmodus aktiviert – LED Beleuchtung an' : 'Tagmodus aktiviert');
      });
      toggle.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle.click(); }
      });
    }

    /* Logo upload */
    var fileInput = document.getElementById('visLogo');
    if (fileInput) {
      fileInput.addEventListener('change', function () {
        var file = fileInput.files[0];
        if (!file || !file.type.startsWith('image/')) return;
        var reader = new FileReader();
        reader.onload = function (ev) {
          var img = new Image();
          img.onload = function () { state.logoImg = img; render(); announce('Logo hochgeladen und visualisiert'); };
          img.src = ev.target.result;
        };
        reader.readAsDataURL(file);
      });
    }

    /* Download */
    var dlBtn = document.getElementById('visDownload');
    if (dlBtn) {
      dlBtn.addEventListener('click', function () {
        render();
        var link = document.createElement('a');
        link.download = 'masar-brand-simulation.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
        showToast('PNG gespeichert!');
      });
    }

    /* Share URL */
    var shareBtn = document.getElementById('visShare');
    if (shareBtn) {
      shareBtn.addEventListener('click', function () {
        var params = new URLSearchParams({
          vis: '1',
          name: state.name,
          tpl: state.template,
          col: state.color.replace('#', ''),
        });
        var url = window.location.origin + '/#brand-visualizer?' + params.toString();
        if (navigator.clipboard) {
          navigator.clipboard.writeText(url).then(function () {
            showToast('Simulations-Link kopiert – jetzt mit Partnern teilen!');
          });
        } else {
          showToast('URL: ' + url);
        }
      });
    }

    /* Magnetic mouse effect on canvas */
    canvas.addEventListener('mousemove', function (e) {
      var rect = canvas.getBoundingClientRect();
      state.mouseX = (e.clientX - rect.left) / rect.width;
      state.mouseY = (e.clientY - rect.top)  / rect.height;
    });
    canvas.addEventListener('mouseleave', function () {
      state.mouseX = 0.5;
      state.mouseY = 0.5;
    });

    /* Initial render */
    render();
  }

  function resizeCanvas() {
    if (!canvas) return;
    var wrap = canvas.parentElement;
    canvas.width  = wrap.offsetWidth  || 800;
    canvas.height = wrap.offsetHeight || Math.round((wrap.offsetWidth || 800) * 9 / 16);
  }

  /* ── Main render ────────────────────────────────────────────── */
  function render() {
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (state.template === 'van') drawVan(); else drawBuilding();
  }

  /* ── Van template ───────────────────────────────────────────── */
  function drawVan() {
    var W = canvas.width, H = canvas.height, N = state.night;

    /* Sky */
    var sky = ctx.createLinearGradient(0, 0, 0, H * 0.72);
    if (N) { sky.addColorStop(0, '#030810'); sky.addColorStop(1, '#0d1f38'); }
    else   { sky.addColorStop(0, '#a8c8e8'); sky.addColorStop(1, '#d8eef8'); }
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    if (N) drawStars(W, H);

    /* Ground */
    ctx.fillStyle = N ? '#080f1a' : '#b8b8b8';
    ctx.fillRect(0, H * 0.73, W, H * 0.27);
    if (!N) {
      ctx.fillStyle = '#a0a0a0';
      ctx.fillRect(0, H * 0.73, W, 2);
    }

    var vX = W * 0.07, vY = H * 0.18, vW = W * 0.86, vH = H * 0.52;

    /* Shadow */
    ctx.fillStyle = N ? 'rgba(0,0,0,0.7)' : 'rgba(0,0,0,0.13)';
    ctx.beginPath();
    ctx.ellipse(vX + vW / 2, H * 0.735, vW * 0.44, H * 0.022, 0, 0, Math.PI * 2);
    ctx.fill();

    /* Van body */
    ctx.fillStyle = N ? '#16243a' : '#f2f2f2';
    ctx.strokeStyle = N ? 'rgba(88,208,189,0.12)' : '#ccc';
    ctx.lineWidth = 1.5;
    rrect(vX, vY, vW, vH, 10);
    ctx.fill(); ctx.stroke();

    /* Cab */
    var cW = vW * 0.21, cH = vH * 0.64;
    var cX = vX + vW - cW, cY = vY + vH - cH;
    ctx.fillStyle = N ? '#0e1a28' : '#e0e0e0';
    ctx.beginPath();
    ctx.rect(cX, cY, cW, cH);
    ctx.fill();

    /* Windshield */
    ctx.fillStyle = N ? 'rgba(88,208,189,0.1)' : 'rgba(140,200,240,0.55)';
    rrect(cX + 5, cY + 6, cW - 10, cH * 0.44, 4);
    ctx.fill();

    /* Brand panel */
    var pX = vX + 8, pY = vY + 6, pW = vW - cW - 16, pH = vH - 12;
    ctx.fillStyle   = N ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.015)';
    ctx.strokeStyle = N ? 'rgba(88,208,189,0.08)' : 'rgba(0,0,0,0.06)';
    ctx.lineWidth = 1;
    rrect(pX, pY, pW, pH, 5);
    ctx.fill(); ctx.stroke();

    renderBrand(pX, pY, pW, pH, N, false);

    /* Wheels */
    wheel(vX + vW * 0.19, H * 0.73, W * 0.062, N);
    wheel(vX + vW * 0.76, H * 0.73, W * 0.062, N);

    /* Headlight */
    ctx.fillStyle = N ? '#ffffaa' : '#eee';
    rrect(vX + vW - 16, cY + cH * 0.52, 12, 9, 2);
    ctx.fill();
    if (N) {
      ctx.shadowColor = '#ffffaa'; ctx.shadowBlur = 40;
      ctx.fillStyle = 'rgba(255,255,180,0.12)';
      ctx.fillRect(vX + vW - 90, cY + cH * 0.46, 90, 22);
      ctx.shadowBlur = 0;
    }

    /* Tail light */
    ctx.fillStyle = N ? '#ff3333' : '#cc1100';
    rrect(vX + 3, vY + vH - 20, 9, 14, 2);
    ctx.fill();
  }

  function wheel(cx, ground, r, N) {
    ctx.fillStyle = N ? '#0d0d0d' : '#1a1a1a';
    ctx.beginPath(); ctx.arc(cx, ground, r, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = N ? '#223344' : '#d0d0d0';
    ctx.beginPath(); ctx.arc(cx, ground, r * 0.58, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = N ? '#14202e' : '#aaaaaa';
    ctx.beginPath(); ctx.arc(cx, ground, r * 0.2, 0, Math.PI * 2); ctx.fill();
  }

  function drawStars(W, H) {
    ctx.fillStyle = 'rgba(255,255,255,0.85)';
    [[.08,.04],[.22,.07],[.38,.03],[.52,.06],[.67,.04],[.81,.08],[.93,.05],
     [.14,.13],[.58,.11],[.88,.14],[.3,.09]].forEach(function (s) {
      ctx.beginPath(); ctx.arc(s[0]*W, s[1]*H, 0.9, 0, Math.PI*2); ctx.fill();
    });
  }

  /* ── Building template ──────────────────────────────────────── */
  function drawBuilding() {
    var W = canvas.width, H = canvas.height, N = state.night;

    /* Sky */
    var sky = ctx.createLinearGradient(0, 0, 0, H);
    if (N) { sky.addColorStop(0, '#010508'); sky.addColorStop(1, '#0a1a30'); }
    else   { sky.addColorStop(0, '#a0bcd8'); sky.addColorStop(1, '#d0e8f8'); }
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    if (N) drawStars(W, H);

    /* Ground */
    ctx.fillStyle = N ? '#060c14' : '#aab0b8';
    ctx.fillRect(0, H * 0.8, W, H * 0.2);

    var bX = W * 0.14, bY = H * 0.04, bW = W * 0.72, bH = H * 0.76;

    /* Building shadow */
    if (!N) {
      ctx.fillStyle = 'rgba(0,0,0,0.08)';
      ctx.fillRect(bX + 8, bY + 8, bW, bH);
    }

    /* Building */
    ctx.fillStyle   = N ? '#0b1826' : '#d4d4d4';
    ctx.strokeStyle = N ? '#16283c' : '#b8b8b8';
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.rect(bX, bY, bW, bH); ctx.fill(); ctx.stroke();

    /* Windows */
    var wCols = 5, wRows = 5;
    var wPad = bW * 0.09;
    var wW   = (bW - wPad * 2) / wCols - 7;
    var wH   = bH * 0.09;
    for (var r = 0; r < wRows; r++) {
      for (var c = 0; c < wCols; c++) {
        var wx = bX + wPad + c * ((bW - wPad * 2) / wCols) + 2;
        var wy = bY + bH * 0.38 + r * (wH + 9);
        var lit = N && (Math.sin(r * 7 + c * 3) > 0);
        ctx.fillStyle = N
          ? (lit ? 'rgba(255,235,160,0.35)' : 'rgba(255,255,255,0.02)')
          : 'rgba(140,195,240,0.5)';
        if (N && lit) { ctx.shadowColor = 'rgba(255,235,150,0.6)'; ctx.shadowBlur = 6; }
        ctx.fillRect(wx, wy, wW, wH);
        ctx.shadowBlur = 0;
      }
    }

    /* Sign panel */
    var sX = bX + bW * 0.07, sY = bY + bH * 0.05;
    var sW = bW * 0.86, sH = bH * 0.24;
    ctx.fillStyle = N ? '#040c18' : '#111';
    rrect(sX, sY, sW, sH, 6); ctx.fill();

    /* Night glow behind sign */
    if (N) {
      var mx = state.mouseX || 0.5;
      var my = state.mouseY || 0.5;
      var glowX = sX + sW * (0.3 + mx * 0.4);
      var glowY = sY + sH * (0.2 + my * 0.6);
      var grad = ctx.createRadialGradient(glowX, glowY, 0, glowX, glowY, sW * 0.7);
      grad.addColorStop(0, hexRgba(state.color, 0.25));
      grad.addColorStop(1, 'transparent');
      ctx.fillStyle = grad;
      rrect(sX - 20, sY - 20, sW + 40, sH + 40, 8);
      ctx.fill();
    }

    renderBrand(sX, sY, sW, sH, N, true);

    /* Mounting brackets */
    [0.22, 0.78].forEach(function (f) {
      ctx.fillStyle = N ? '#152030' : '#888';
      ctx.fillRect(sX + sW * f - 3, sY + sH, 6, 18);
    });
  }

  /* ── Brand content on panel ─────────────────────────────────── */
  function renderBrand(px, py, pw, ph, N, isSign) {
    var cx = px + pw / 2, cy = py + ph / 2;

    if (state.logoImg) {
      var ratio = state.logoImg.width / state.logoImg.height;
      var mxW = pw * 0.68, mxH = ph * 0.58;
      var lW = mxW, lH = mxW / ratio;
      if (lH > mxH) { lH = mxH; lW = lH * ratio; }
      if (N && isSign) { ctx.shadowColor = state.color; ctx.shadowBlur = 28; }
      ctx.drawImage(state.logoImg, cx - lW / 2, cy - lH / 2, lW, lH);
      ctx.shadowBlur = 0;
    } else {
      var name = state.name || 'IHRE FIRMA';
      var fs   = Math.min(pw * 0.12, ph * 0.36, 62);
      ctx.font          = '900 ' + fs + 'px "Barlow Condensed","Arial Narrow",Impact,sans-serif';
      ctx.textAlign     = 'center';
      ctx.textBaseline  = 'middle';
      ctx.letterSpacing = '2px';

      var textY = cy - fs * 0.1;

      if (N && isSign) {
        /* Neon glow layers */
        ctx.shadowColor = state.color; ctx.shadowBlur = 50;
        ctx.fillStyle = state.color; ctx.fillText(name, cx, textY);
        ctx.shadowBlur = 20;
        ctx.fillStyle = '#fff'; ctx.fillText(name, cx, textY);
        ctx.shadowBlur = 0;
      } else if (N) {
        ctx.shadowColor = state.color; ctx.shadowBlur = 14;
        ctx.fillStyle = state.color; ctx.fillText(name, cx, textY);
        ctx.shadowBlur = 0;
      } else {
        ctx.fillStyle = state.color; ctx.fillText(name, cx, textY);
      }

      /* Tagline */
      var tf = Math.min(pw * 0.035, ph * 0.1, 14);
      ctx.font      = '600 ' + tf + 'px Barlow,sans-serif';
      ctx.fillStyle = N ? 'rgba(255,255,255,0.38)' : 'rgba(0,0,0,0.28)';
      ctx.shadowBlur = 0;
      ctx.fillText('MASAR WERBEAGENTUR BERLIN', cx, textY + fs * 0.62);
    }
  }

  /* ── Helpers ────────────────────────────────────────────────── */
  function rrect(x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) {
      ctx.roundRect(x, y, w, h, r);
    } else {
      ctx.moveTo(x + r, y);
      ctx.lineTo(x + w - r, y);
      ctx.quadraticCurveTo(x + w, y, x + w, y + r);
      ctx.lineTo(x + w, y + h - r);
      ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
      ctx.lineTo(x + r, y + h);
      ctx.quadraticCurveTo(x, y + h, x, y + h - r);
      ctx.lineTo(x, y + r);
      ctx.quadraticCurveTo(x, y, x + r, y);
      ctx.closePath();
    }
  }

  function hexRgba(hex, a) {
    var r = parseInt(hex.slice(1,3),16);
    var g = parseInt(hex.slice(3,5),16);
    var b = parseInt(hex.slice(5,7),16);
    return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
  }

  function announce(msg) {
    var el = document.getElementById('visAnnounce');
    if (!el) return;
    el.textContent = '';
    setTimeout(function () { el.textContent = msg; }, 50);
  }

  function showToast(msg) {
    var t = document.getElementById('visToast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._tid);
    t._tid = setTimeout(function () { t.classList.remove('show'); }, 3200);
  }

  /* ── URL param sharing ──────────────────────────────────────── */
  function readURLParams() {
    var p = new URLSearchParams(window.location.search);
    if (p.get('vis') !== '1') return;
    if (p.get('name')) {
      state.name = p.get('name').toUpperCase();
      var inp = document.getElementById('visName');
      if (inp) inp.value = state.name;
    }
    if (p.get('tpl')) {
      state.template = p.get('tpl');
      document.querySelectorAll('.vis-tpl-btn').forEach(function (b) {
        b.classList.toggle('active', b.dataset.tpl === state.template);
        b.setAttribute('aria-pressed', b.dataset.tpl === state.template ? 'true' : 'false');
      });
    }
    if (p.get('col')) {
      state.color = '#' + p.get('col');
      document.querySelectorAll('.vis-swatch').forEach(function (s) {
        s.classList.toggle('active', s.dataset.color === state.color);
      });
    }
    if (canvas) render();
    var section = document.getElementById('brand-visualizer');
    if (section) setTimeout(function () { section.scrollIntoView({ behavior: 'smooth' }); }, 300);
  }

  /* ─────────────────────────────────────────────────────────── */
  /*  SPRING EFFECTS                                             */
  /* ─────────────────────────────────────────────────────────── */
  function initSpringEffects() {
    /* Extra spring on price buttons using JS for finer control */
    document.querySelectorAll('.price-btn, .calc-cta-btn').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        el.style.transition = 'transform 0.4s cubic-bezier(0.34,1.56,0.64,1)';
      });
      el.addEventListener('mouseleave', function () {
        el.style.transform = '';
      });
    });
  }

  /* ─────────────────────────────────────────────────────────── */
  /*  KINETIC HEADINGS — letter-spacing on scroll velocity       */
  /* ─────────────────────────────────────────────────────────── */
  function initKineticHeadings() {
    var lastY = 0, timer;
    window.addEventListener('scroll', function () {
      var dy = Math.abs(window.scrollY - lastY);
      lastY = window.scrollY;
      if (dy > 12) {
        document.querySelectorAll('.kinetic-heading').forEach(function (h) {
          h.classList.add('is-scrolling');
        });
        clearTimeout(timer);
        timer = setTimeout(function () {
          document.querySelectorAll('.kinetic-heading').forEach(function (h) {
            h.classList.remove('is-scrolling');
          });
        }, 250);
      }
    }, { passive: true });
  }

  /* ─────────────────────────────────────────────────────────── */
  /*  BOOT                                                       */
  /* ─────────────────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* Re-render canvas on mouse move (for building glow effect) */
  document.addEventListener('mousemove', function (e) {
    if (state.template === 'building' && state.night && canvas) {
      var rect = canvas.getBoundingClientRect();
      if (e.clientX >= rect.left && e.clientX <= rect.right &&
          e.clientY >= rect.top  && e.clientY <= rect.bottom) {
        render();
      }
    }
  }, { passive: true });

  window.MasarVis = { render: render, state: state };
})();
