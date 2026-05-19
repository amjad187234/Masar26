/* ═══════════════════════════════════════════════════════════════
   MASAR — Brand Visualizer v2
   Canvas engine with dpr-aware rendering + ResizeObserver
   Exit intent with opacity/visibility (no display flicker)
   BFSG/WCAG 2.1 AA — Vanilla JS, zero dependencies
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── State ──────────────────────────────────────────────────── */
  var S = {
    name:     'IHRE FIRMA',
    logoImg:  null,
    template: 'van',
    color:    '#58d0bd',
    night:    false,
    mx: 0.5, my: 0.5,  // normalised mouse position inside canvas
  };

  var canvas, ctx, dpr = 1;
  var raf = null;           // requestAnimationFrame handle for night glow
  var glowPhase = 0;        // glow animation phase (0–2π)

  /* ── Ticker messages ───────────────────────────────────────── */
  var TICKS = [
    { msg: 'Jemand aus Berlin-Mitte hat gerade eine Fahrzeugfolierung berechnet', ago: 'vor 2 Min.' },
    { msg: 'Neuer Auftrag: Leuchtreklame aus Hamburg-Altona',                      ago: 'vor 4 Min.' },
    { msg: 'Flyer-Anfrage aus München — 500 Stück DIN A5',                         ago: 'vor 7 Min.' },
    { msg: 'Schaufensterbeklebung angefragt aus Frankfurt',                         ago: 'vor 11 Min.' },
    { msg: 'Van-Wrap Simulation gestartet aus Düsseldorf',                          ago: 'vor 14 Min.' },
    { msg: 'Webdesign-Paket bestellt — Berlin-Prenzlauer Berg',                     ago: 'vor 18 Min.' },
    { msg: 'Jemand aus Stuttgart berechnet gerade Messeplane',                      ago: 'vor 23 Min.' },
    { msg: 'Neon-Leuchtreklame für Restaurant in Berlin Wedding angefragt',         ago: 'vor 28 Min.' },
  ];
  var tickIdx = 0;

  /* ═════════════════════════════════════════════════════════════
     BOOT
     ═════════════════════════════════════════════════════════════ */
  function boot() {
    initTicker();
    initExitIntent();
    initVisualizer();
    initKineticHeadings();
    readURLParams();
  }

  /* ═════════════════════════════════════════════════════════════
     ORDER TICKER
     ═════════════════════════════════════════════════════════════ */
  function initTicker() {
    var wrap = document.getElementById('orderTicker');
    if (!wrap) return;
    var msgEl  = wrap.querySelector('.ticker-msg');
    var timeEl = wrap.querySelector('.ticker-time');
    if (!msgEl || !timeEl) return;

    function tick() {
      var t = TICKS[tickIdx++ % TICKS.length];
      /* Remove class, force reflow, add back → restarts CSS animation */
      msgEl.classList.remove('ticker-msg');
      void msgEl.offsetWidth;
      msgEl.classList.add('ticker-msg');
      msgEl.textContent  = t.msg;
      timeEl.textContent = t.ago;
    }
    tick();
    setInterval(tick, 6500);
  }

  /* ═════════════════════════════════════════════════════════════
     EXIT INTENT
     Key fix: we use opacity+visibility, NOT display, so that
     pointer events on the close buttons are never blocked.
     ═════════════════════════════════════════════════════════════ */
  function initExitIntent() {
    var overlay    = document.getElementById('exitOverlay');
    if (!overlay) return;

    /* Don't re-show in the same browser session */
    if (sessionStorage.getItem('ei_shown')) return;

    var shown      = false;
    var closeBtn   = document.getElementById('exitClose');
    var dismissBtn = document.getElementById('exitDismiss');
    var ctaBtn     = document.getElementById('exitCta');

    function show() {
      if (shown) return;
      shown = true;
      sessionStorage.setItem('ei_shown', '1');
      overlay.classList.add('open');
      overlay.removeAttribute('aria-hidden');
      /* Focus first interactive element for keyboard users */
      var first = overlay.querySelector('button, a[href]');
      if (first) setTimeout(function () { first.focus(); }, 50);
    }

    function hide() {
      overlay.classList.remove('open');
      overlay.setAttribute('aria-hidden', 'true');
    }

    /* Desktop: cursor leaves toward the top of viewport */
    document.addEventListener('mouseleave', function (e) {
      if (e.clientY < 25) show();
    });

    /* Mobile: detect a fast upward swipe toward top of page */
    var touchStartY = 0;
    document.addEventListener('touchstart', function (e) {
      touchStartY = e.touches[0].clientY;
    }, { passive: true });
    document.addEventListener('touchend', function (e) {
      var dy = touchStartY - e.changedTouches[0].clientY;
      if (dy > 90 && window.scrollY < 200) show();
    }, { passive: true });

    /* Close handlers — all three close paths */
    if (closeBtn)   closeBtn.addEventListener('click',   hide);
    if (dismissBtn) dismissBtn.addEventListener('click', hide);
    if (ctaBtn) {
      ctaBtn.addEventListener('click', function (e) {
        e.preventDefault();
        hide();
        setTimeout(function () {
          var kontakt = document.getElementById('kontakt');
          if (kontakt) kontakt.scrollIntoView({ behavior: 'smooth' });
        }, 80);
      });
    }

    /* Click outside the card closes overlay */
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) hide();
    });

    /* Escape key */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('open')) hide();
    });
  }

  /* ═════════════════════════════════════════════════════════════
     BRAND VISUALIZER
     ═════════════════════════════════════════════════════════════ */
  function initVisualizer() {
    canvas = document.getElementById('visCanvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    dpr = window.devicePixelRatio || 1;

    /* Resize canvas whenever its container changes size */
    var ro = new ResizeObserver(function () { resizeCanvas(); renderNow(); });
    ro.observe(canvas.parentElement);
    resizeCanvas();

    /* Controls ─────────────────────────────────────────────── */
    bindInput('visName', function (val) {
      S.name = val.toUpperCase().trim() || 'IHRE FIRMA';
      renderNow(); announce('Markenname: ' + S.name);
    });

    /* Template buttons */
    document.querySelectorAll('.vis-tpl-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setTemplate(btn.dataset.tpl, btn);
      });
      btn.addEventListener('keydown', keyClick);
    });

    /* Color swatches */
    document.querySelectorAll('.vis-swatch').forEach(function (sw) {
      sw.addEventListener('click', function () { setColor(sw.dataset.color, sw); });
      sw.addEventListener('keydown', keyClick);
    });

    /* Night toggle */
    var tog = document.getElementById('nightToggle');
    if (tog) {
      tog.addEventListener('click', function () { toggleNight(tog); });
      tog.addEventListener('keydown', keyClick);
    }

    /* Logo upload */
    var fileIn = document.getElementById('visLogo');
    if (fileIn) {
      fileIn.addEventListener('change', function () {
        var f = fileIn.files[0];
        if (!f || !f.type.startsWith('image/')) return;
        var reader = new FileReader();
        reader.onload = function (ev) {
          var img = new Image();
          img.onload = function () { S.logoImg = img; renderNow(); announce('Logo hochgeladen und visualisiert'); };
          img.src = ev.target.result;
        };
        reader.readAsDataURL(f);
      });
    }

    /* Download */
    on('visDownload', 'click', function () {
      renderNow();
      var a = document.createElement('a');
      a.download = 'masar-brand-simulation.png';
      a.href = canvas.toDataURL('image/png');
      a.click();
      toast('Simulation gespeichert als PNG 📥');
    });

    /* Share URL */
    on('visShare', 'click', function () {
      var p = new URLSearchParams({ vis:'1', name:S.name, tpl:S.template, col:S.color.replace('#','') });
      var url = window.location.origin + '/#brand-visualizer?' + p.toString();
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(function () {
          toast('Simulations-Link kopiert! 🔗 Jetzt teilen.');
        });
      } else {
        toast('URL: ' + url);
      }
    });

    /* RESET — neu starten */
    on('visReset', 'click', function () {
      S.name    = 'IHRE FIRMA';
      S.logoImg = null;
      S.template= 'van';
      S.color   = '#58d0bd';
      S.night   = false;
      S.mx = 0.5; S.my = 0.5;

      var inp = document.getElementById('visName');
      if (inp) inp.value = '';

      document.querySelectorAll('.vis-tpl-btn').forEach(function (b) {
        var active = b.dataset.tpl === 'van';
        b.classList.toggle('active', active);
        b.setAttribute('aria-pressed', active ? 'true' : 'false');
      });

      document.querySelectorAll('.vis-swatch').forEach(function (s) {
        var active = s.dataset.color === '#58d0bd';
        s.classList.toggle('active', active);
        s.setAttribute('aria-checked', active ? 'true' : 'false');
      });

      var tog2 = document.getElementById('nightToggle');
      if (tog2) { tog2.classList.remove('on'); tog2.setAttribute('aria-checked','false'); }
      var badge = document.getElementById('modeBadge');
      if (badge) badge.textContent = '☀️ Tag';

      var fileIn2 = document.getElementById('visLogo');
      if (fileIn2) fileIn2.value = '';

      stopGlowLoop();
      renderNow();
      announce('Visualizer zurückgesetzt. Starten Sie von vorne.');
      toast('Zurückgesetzt — von vorne beginnen 🔄');
    });

    /* Mouse tracking inside canvas for building glow */
    canvas.addEventListener('mousemove', function (e) {
      var r = canvas.getBoundingClientRect();
      S.mx = (e.clientX - r.left) / r.width;
      S.my = (e.clientY - r.top)  / r.height;
    }, { passive: true });
    canvas.addEventListener('mouseleave', function () { S.mx = 0.5; S.my = 0.5; }, { passive: true });

    renderNow();
  }

  /* ── Resize canvas with devicePixelRatio support ──────────── */
  function resizeCanvas() {
    if (!canvas) return;
    dpr = window.devicePixelRatio || 1;
    var wrap = canvas.parentElement;
    var cssW = wrap.clientWidth  || 640;
    var cssH = Math.round(cssW * 9 / 16);
    /* Physical pixels */
    canvas.width  = Math.round(cssW * dpr);
    canvas.height = Math.round(cssH * dpr);
    /* CSS pixels */
    canvas.style.width  = cssW + 'px';
    canvas.style.height = cssH + 'px';
    /* Scale all draw calls to match dpr */
    ctx.scale(dpr, dpr);
  }

  /* ── Render dispatcher ─────────────────────────────────────── */
  function renderNow() {
    if (!ctx) return;
    /* Logical (CSS) dimensions for draw calls */
    var W = canvas.width  / dpr;
    var H = canvas.height / dpr;
    ctx.clearRect(0, 0, W, H);
    if (S.template === 'van') drawVan(W, H);
    else                       drawBuilding(W, H);
  }

  /* ── Animated glow loop (night mode) ──────────────────────── */
  function startGlowLoop() {
    if (raf) return;
    function loop() {
      glowPhase = (glowPhase + 0.04) % (Math.PI * 2);
      renderNow();
      raf = requestAnimationFrame(loop);
    }
    raf = requestAnimationFrame(loop);
  }
  function stopGlowLoop() {
    if (raf) { cancelAnimationFrame(raf); raf = null; }
  }

  /* ═══════════════════════════════════════════════════════════
     CANVAS: VAN
     ═══════════════════════════════════════════════════════════ */
  function drawVan(W, H) {
    var N = S.night;

    /* Sky background */
    var sky = ctx.createLinearGradient(0, 0, 0, H * 0.72);
    if (N) { sky.addColorStop(0,'#020608'); sky.addColorStop(1,'#0c1c34'); }
    else   { sky.addColorStop(0,'#9abcd8'); sky.addColorStop(1,'#d4ecfa'); }
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    if (N) drawStars(W, H);

    /* Ground */
    var ground = ctx.createLinearGradient(0, H * 0.73, 0, H);
    if (N) { ground.addColorStop(0,'#090f1a'); ground.addColorStop(1,'#050a12'); }
    else   { ground.addColorStop(0,'#b0b0b0'); ground.addColorStop(1,'#c8c8c8'); }
    ctx.fillStyle = ground;
    ctx.fillRect(0, H * 0.73, W, H * 0.27);

    /* Road lines (day only) */
    if (!N) {
      ctx.fillStyle = '#a8a8a8';
      ctx.fillRect(0, H * 0.73, W, 2);
      ctx.fillStyle = 'rgba(255,255,255,0.5)';
      for (var x = 0; x < W; x += 60) {
        ctx.fillRect(x, H * 0.82, 36, 4);
      }
    }

    /* Van dimensions */
    var vX = W * 0.06, vY = H * 0.17;
    var vW = W * 0.88, vH = H * 0.54;

    /* Drop shadow */
    ctx.fillStyle = N ? 'rgba(0,0,0,.65)' : 'rgba(0,0,0,.12)';
    ctx.beginPath();
    ctx.ellipse(vX + vW / 2, H * 0.735, vW * 0.44, H * 0.021, 0, 0, Math.PI * 2);
    ctx.fill();

    /* Van body */
    var bodyGrad = ctx.createLinearGradient(0, vY, 0, vY + vH);
    if (N) { bodyGrad.addColorStop(0,'#1e3050'); bodyGrad.addColorStop(1,'#0f1e30'); }
    else   { bodyGrad.addColorStop(0,'#f8f8f8'); bodyGrad.addColorStop(1,'#e8e8e8'); }
    ctx.fillStyle   = bodyGrad;
    ctx.strokeStyle = N ? 'rgba(88,208,189,.14)' : '#bbb';
    ctx.lineWidth   = 1.5;
    rr(vX, vY, vW, vH, 10); ctx.fill(); ctx.stroke();

    /* Roof ridge line */
    ctx.strokeStyle = N ? 'rgba(255,255,255,.05)' : 'rgba(0,0,0,.06)';
    ctx.lineWidth   = 1;
    ctx.beginPath(); ctx.moveTo(vX + 10, vY + 8); ctx.lineTo(vX + vW * 0.78, vY + 8); ctx.stroke();

    /* Cab section */
    var cW = vW * 0.21, cH = vH * 0.65;
    var cX = vX + vW - cW, cY = vY + vH - cH;
    var cabGrad = ctx.createLinearGradient(cX, cY, cX + cW, cY);
    if (N) { cabGrad.addColorStop(0,'#0e1c2e'); cabGrad.addColorStop(1,'#0a1422'); }
    else   { cabGrad.addColorStop(0,'#e0e0e0'); cabGrad.addColorStop(1,'#d0d0d0'); }
    ctx.fillStyle   = cabGrad;
    ctx.strokeStyle = N ? 'rgba(88,208,189,.08)' : '#bbb';
    ctx.lineWidth   = 1;
    rr(cX, cY, cW, cH, [0, 8, 4, 0]); ctx.fill(); ctx.stroke();

    /* Windshield */
    ctx.fillStyle = N ? 'rgba(88,208,189,.1)' : 'rgba(120,190,240,.55)';
    rr(cX + 5, cY + 7, cW - 10, cH * 0.44, 4); ctx.fill();

    /* Windshield glare */
    ctx.fillStyle = N ? 'rgba(255,255,255,.04)' : 'rgba(255,255,255,.3)';
    rr(cX + 8, cY + 10, (cW - 14) * 0.4, cH * 0.18, 2); ctx.fill();

    /* ── Brand panel ─────────────────────────────────────── */
    var pX = vX + 8, pY = vY + 6, pW = vW - cW - 16, pH = vH - 12;
    ctx.fillStyle   = N ? 'rgba(255,255,255,.02)' : 'rgba(0,0,0,.01)';
    ctx.strokeStyle = N ? 'rgba(88,208,189,.07)' : 'rgba(0,0,0,.05)';
    ctx.lineWidth   = 1;
    rr(pX, pY, pW, pH, 5); ctx.fill(); ctx.stroke();
    renderBrand(pX, pY, pW, pH, N, false);

    /* Wheels */
    wheel(vX + vW * 0.18, H * 0.73, W * 0.065, N);
    wheel(vX + vW * 0.77, H * 0.73, W * 0.065, N);

    /* Headlight */
    ctx.fillStyle = N ? '#ffffc0' : '#eee';
    rr(vX + vW - 17, cY + cH * 0.52, 13, 9, 2); ctx.fill();
    if (N) {
      ctx.save();
      ctx.shadowColor = '#ffffa0'; ctx.shadowBlur = 50;
      ctx.fillStyle   = 'rgba(255,255,160,.08)';
      ctx.fillRect(vX + vW - 100, cY + cH * 0.45, 100, 24);
      ctx.restore();
    }

    /* Tail light */
    ctx.fillStyle = N ? '#ff3333' : '#cc1100';
    rr(vX + 4, vY + vH - 20, 9, 14, 2); ctx.fill();

    /* Door line */
    ctx.strokeStyle = N ? 'rgba(255,255,255,.06)' : 'rgba(0,0,0,.06)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(vX + pW + 12, vY + 4);
    ctx.lineTo(vX + pW + 12, vY + vH - 4);
    ctx.stroke();
  }

  function wheel(cx, gy, r, N) {
    /* Tyre */
    ctx.fillStyle = N ? '#0a0a0a' : '#181818';
    ctx.beginPath(); ctx.arc(cx, gy, r, 0, Math.PI * 2); ctx.fill();
    /* Rim */
    var rimGrad = ctx.createRadialGradient(cx - r * 0.2, gy - r * 0.2, 0, cx, gy, r * 0.58);
    rimGrad.addColorStop(0, N ? '#2a3a4a' : '#e0e0e0');
    rimGrad.addColorStop(1, N ? '#18263a' : '#b8b8b8');
    ctx.fillStyle = rimGrad;
    ctx.beginPath(); ctx.arc(cx, gy, r * 0.58, 0, Math.PI * 2); ctx.fill();
    /* Spokes */
    ctx.strokeStyle = N ? '#1a2a38' : '#a0a0a0';
    ctx.lineWidth = r * 0.08;
    for (var i = 0; i < 5; i++) {
      var a = (i / 5) * Math.PI * 2;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a) * r * 0.18, gy + Math.sin(a) * r * 0.18);
      ctx.lineTo(cx + Math.cos(a) * r * 0.52, gy + Math.sin(a) * r * 0.52);
      ctx.stroke();
    }
    /* Hub */
    ctx.fillStyle = N ? '#10202e' : '#a8a8a8';
    ctx.beginPath(); ctx.arc(cx, gy, r * 0.17, 0, Math.PI * 2); ctx.fill();
  }

  /* ═══════════════════════════════════════════════════════════
     CANVAS: BUILDING
     ═══════════════════════════════════════════════════════════ */
  function drawBuilding(W, H) {
    var N = S.night;

    /* Sky */
    var sky = ctx.createLinearGradient(0, 0, 0, H);
    if (N) { sky.addColorStop(0,'#010305'); sky.addColorStop(1,'#081828'); }
    else   { sky.addColorStop(0,'#88b4d4'); sky.addColorStop(1,'#cce4f8'); }
    ctx.fillStyle = sky; ctx.fillRect(0, 0, W, H);
    if (N) drawStars(W, H);

    /* Ground */
    ctx.fillStyle = N ? '#050a12' : '#a8b0b8';
    ctx.fillRect(0, H * 0.82, W, H * 0.18);
    if (!N) {
      ctx.fillStyle = '#c0c8d0';
      ctx.fillRect(0, H * 0.82, W, 4);
    }

    /* Side buildings (skyline) */
    if (N) {
      ctx.fillStyle = '#06101a';
      ctx.fillRect(0, H * 0.2, W * 0.12, H * 0.62);
      ctx.fillRect(W * 0.88, H * 0.25, W * 0.12, H * 0.57);
    } else {
      ctx.fillStyle = '#c4c8cc';
      ctx.fillRect(0, H * 0.18, W * 0.12, H * 0.64);
      ctx.fillRect(W * 0.88, H * 0.22, W * 0.12, H * 0.6);
    }

    var bX = W * 0.15, bY = H * 0.03;
    var bW = W * 0.7,  bH = H * 0.79;

    /* Building shadow */
    if (!N) {
      ctx.fillStyle = 'rgba(0,0,0,.08)';
      ctx.fillRect(bX + 10, bY + 10, bW, bH);
    }

    /* Building body */
    var wallGrad = ctx.createLinearGradient(bX, bY, bX + bW, bY);
    if (N) { wallGrad.addColorStop(0,'#0c1a28'); wallGrad.addColorStop(.5,'#0f2035'); wallGrad.addColorStop(1,'#0c1a28'); }
    else   { wallGrad.addColorStop(0,'#d0d4d8'); wallGrad.addColorStop(.5,'#dcdfdf'); wallGrad.addColorStop(1,'#d0d4d8'); }
    ctx.fillStyle   = wallGrad;
    ctx.strokeStyle = N ? '#182c40' : '#b8bcc0';
    ctx.lineWidth   = 1.5;
    ctx.beginPath(); ctx.rect(bX, bY, bW, bH); ctx.fill(); ctx.stroke();

    /* Windows */
    var wCols = 5, wRows = 6;
    var wPad  = bW * 0.09;
    var wStep = (bW - wPad * 2) / wCols;
    var wW    = wStep - 8, wH = bH * 0.078;
    for (var r = 0; r < wRows; r++) {
      for (var c = 0; c < wCols; c++) {
        var wx = bX + wPad + c * wStep + 2;
        var wy = bY + bH * 0.38 + r * (wH + 9);
        /* Deterministic lit/unlit (no Math.random — stable on re-render) */
        var lit = N && ((r * 7 + c * 3 + r + c) % 3 !== 0);
        if (N && lit) {
          ctx.save();
          ctx.shadowColor = 'rgba(255,230,150,.7)'; ctx.shadowBlur = 10;
          ctx.fillStyle   = 'rgba(255,235,160,.38)';
          ctx.fillRect(wx, wy, wW, wH);
          ctx.restore();
        } else {
          ctx.fillStyle = N ? 'rgba(255,255,255,.02)' : 'rgba(130,190,240,.5)';
          ctx.fillRect(wx, wy, wW, wH);
          if (!N) {
            /* Window glare */
            ctx.fillStyle = 'rgba(255,255,255,.25)';
            ctx.fillRect(wx + 2, wy + 2, wW * 0.35, wH * 0.4);
          }
        }
      }
    }

    /* ── Neon sign panel ─────────────────────────────────── */
    var sX = bX + bW * 0.07, sY = bY + bH * 0.05;
    var sW = bW * 0.86, sH = bH * 0.24;

    ctx.fillStyle = N ? '#030810' : '#111';
    rr(sX, sY, sW, sH, 6); ctx.fill();

    /* Night: animated radial glow behind letters */
    if (N) {
      var glowAmp  = 0.55 + 0.3 * Math.sin(glowPhase);
      var gx       = sX + sW * (0.3 + S.mx * 0.4);
      var gy       = sY + sH * (0.2 + S.my * 0.6);
      var gRad     = ctx.createRadialGradient(gx, gy, 0, gx, gy, sW * 0.65);
      gRad.addColorStop(0, hexRgba(S.color, glowAmp * 0.28));
      gRad.addColorStop(1, 'transparent');
      ctx.fillStyle = gRad;
      rr(sX - 18, sY - 18, sW + 36, sH + 36, 8); ctx.fill();
    }

    renderBrand(sX, sY, sW, sH, N, true);

    /* Sign mounting brackets */
    [0.22, 0.78].forEach(function (f) {
      ctx.fillStyle = N ? '#152030' : '#888';
      ctx.fillRect(sX + sW * f - 3, sY + sH, 6, 18);
    });

    /* Subtle edge glow on building in night */
    if (N) {
      ctx.save();
      ctx.shadowColor = hexRgba(S.color, 0.12 + 0.06 * Math.sin(glowPhase));
      ctx.shadowBlur  = 30;
      ctx.strokeStyle = hexRgba(S.color, 0.08);
      ctx.lineWidth   = 2;
      ctx.beginPath(); ctx.rect(bX, bY, bW, bH); ctx.stroke();
      ctx.restore();
    }
  }

  /* ── Shared: brand content ─────────────────────────────────── */
  function renderBrand(px, py, pw, ph, N, isSign) {
    var cx = px + pw / 2, cy = py + ph / 2;

    if (S.logoImg) {
      var ratio = S.logoImg.width / S.logoImg.height;
      var mxW = pw * 0.7, mxH = ph * 0.62;
      var lW = mxW, lH = mxW / ratio;
      if (lH > mxH) { lH = mxH; lW = lH * ratio; }
      if (N && isSign) { ctx.save(); ctx.shadowColor = S.color; ctx.shadowBlur = 30; }
      ctx.drawImage(S.logoImg, cx - lW / 2, cy - lH / 2, lW, lH);
      if (N && isSign) ctx.restore();
    } else {
      var name = S.name || 'IHRE FIRMA';
      var fs   = Math.min(pw * 0.115, ph * 0.36, 64);
      ctx.font         = '900 ' + fs + 'px "Barlow Condensed","Arial Narrow",Impact,sans-serif';
      ctx.textAlign    = 'center';
      ctx.textBaseline = 'middle';
      var ty = cy - fs * 0.08;

      if (N && isSign) {
        /* Triple glow layers for realism */
        ctx.save();
        ctx.shadowColor = S.color; ctx.shadowBlur = 60;
        ctx.fillStyle   = S.color; ctx.fillText(name, cx, ty);
        ctx.shadowBlur  = 25;
        ctx.fillStyle   = '#fff';  ctx.fillText(name, cx, ty);
        ctx.shadowBlur  = 8;
        ctx.fillStyle   = '#fff';  ctx.fillText(name, cx, ty);
        ctx.restore();
      } else if (N) {
        ctx.save();
        ctx.shadowColor = S.color; ctx.shadowBlur = 16;
        ctx.fillStyle   = S.color; ctx.fillText(name, cx, ty);
        ctx.restore();
      } else {
        ctx.fillStyle = S.color;
        ctx.fillText(name, cx, ty);
      }

      /* Tagline */
      var tf = Math.min(pw * 0.033, ph * 0.1, 14);
      ctx.font      = '600 ' + tf + 'px Barlow,sans-serif';
      ctx.fillStyle = N ? 'rgba(255,255,255,.35)' : 'rgba(0,0,0,.25)';
      ctx.shadowBlur = 0;
      ctx.fillText('MASAR WERBEAGENTUR BERLIN', cx, ty + fs * 0.64);
    }
  }

  /* ── Stars (night sky) ─────────────────────────────────────── */
  function drawStars(W, H) {
    /* Fixed positions for stable render */
    var pts = [
      [.06,.04],[.19,.07],[.34,.03],[.48,.06],[.62,.04],[.75,.08],[.91,.05],
      [.12,.12],[.55,.1],[.86,.13],[.28,.08],[.7,.06],[.4,.14],[.82,.04],
    ];
    pts.forEach(function (p) {
      ctx.fillStyle = 'rgba(255,255,255,' + (0.5 + 0.4 * Math.sin(glowPhase + p[0] * 10)) + ')';
      ctx.beginPath();
      ctx.arc(p[0] * W, p[1] * H, 0.85, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  /* ═══════════════════════════════════════════════════════════
     KINETIC HEADINGS
     ═══════════════════════════════════════════════════════════ */
  function initKineticHeadings() {
    var lastY = 0, timer;
    window.addEventListener('scroll', function () {
      var dy = Math.abs(window.scrollY - lastY);
      lastY = window.scrollY;
      if (dy > 10) {
        document.querySelectorAll('.kinetic-heading').forEach(function (h) { h.classList.add('is-scrolling'); });
        clearTimeout(timer);
        timer = setTimeout(function () {
          document.querySelectorAll('.kinetic-heading').forEach(function (h) { h.classList.remove('is-scrolling'); });
        }, 300);
      }
    }, { passive: true });
  }

  /* ═══════════════════════════════════════════════════════════
     URL PARAM SHARING
     ═══════════════════════════════════════════════════════════ */
  function readURLParams() {
    var p = new URLSearchParams(window.location.search);
    if (p.get('vis') !== '1') return;
    if (p.get('name')) {
      S.name = p.get('name').toUpperCase();
      var inp = document.getElementById('visName');
      if (inp) inp.value = S.name;
    }
    if (p.get('tpl')) {
      setTemplate(p.get('tpl'), document.querySelector('[data-tpl="' + p.get('tpl') + '"]'));
    }
    if (p.get('col')) {
      var col = '#' + p.get('col');
      setColor(col, document.querySelector('[data-color="' + col + '"]'));
    }
    renderNow();
    var sec = document.getElementById('brand-visualizer');
    if (sec) setTimeout(function () { sec.scrollIntoView({ behavior: 'smooth' }); }, 200);
  }

  /* ═══════════════════════════════════════════════════════════
     HELPERS
     ═══════════════════════════════════════════════════════════ */
  function setTemplate(tpl, activeBtn) {
    S.template = tpl;
    document.querySelectorAll('.vis-tpl-btn').forEach(function (b) {
      var act = b.dataset.tpl === tpl;
      b.classList.toggle('active', act);
      b.setAttribute('aria-pressed', act ? 'true' : 'false');
    });
    renderNow();
    announce('Vorlage: ' + tpl);
  }

  function setColor(col, activeSwatch) {
    S.color = col;
    document.querySelectorAll('.vis-swatch').forEach(function (s) {
      var act = s.dataset.color === col;
      s.classList.toggle('active', act);
      s.setAttribute('aria-checked', act ? 'true' : 'false');
    });
    renderNow();
  }

  function toggleNight(tog) {
    S.night = !S.night;
    tog.classList.toggle('on', S.night);
    tog.setAttribute('aria-checked', S.night ? 'true' : 'false');
    var badge = document.getElementById('modeBadge');
    if (badge) badge.textContent = S.night ? '🌙 Nacht' : '☀️ Tag';
    if (S.night) startGlowLoop(); else stopGlowLoop();
    announce(S.night ? 'Nachtmodus aktiviert — LED Beleuchtung an' : 'Tagmodus');
  }

  function bindInput(id, fn) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', function () { fn(el.value); });
  }

  function on(id, ev, fn) {
    var el = document.getElementById(id);
    if (el) el.addEventListener(ev, fn);
  }

  function keyClick(e) {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.currentTarget.click(); }
  }

  function announce(msg) {
    var el = document.getElementById('visAnnounce');
    if (!el) return;
    el.textContent = '';
    setTimeout(function () { el.textContent = msg; }, 60);
  }

  function toast(msg) {
    var t = document.getElementById('visToast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._tid);
    t._tid = setTimeout(function () { t.classList.remove('show'); }, 3400);
  }

  /* rounded rect polyfill for older Safari */
  function rr(x, y, w, h, r) {
    var tl = Array.isArray(r) ? r[0] : r;
    var tr = Array.isArray(r) ? r[1] : r;
    var br = Array.isArray(r) ? r[2] : r;
    var bl = Array.isArray(r) ? r[3] : r;
    ctx.beginPath();
    ctx.moveTo(x + tl, y);
    ctx.lineTo(x + w - tr, y);
    ctx.quadraticCurveTo(x + w, y,         x + w,     y + tr);
    ctx.lineTo(x + w,         y + h - br);
    ctx.quadraticCurveTo(x + w, y + h,     x + w - br,y + h);
    ctx.lineTo(x + bl,         y + h);
    ctx.quadraticCurveTo(x,    y + h,      x,          y + h - bl);
    ctx.lineTo(x,              y + tl);
    ctx.quadraticCurveTo(x,    y,          x + tl,     y);
    ctx.closePath();
  }

  function hexRgba(hex, a) {
    var r = parseInt(hex.slice(1,3),16);
    var g = parseInt(hex.slice(3,5),16);
    var b = parseInt(hex.slice(5,7),16);
    return 'rgba(' + r + ',' + g + ',' + b + ',' + a.toFixed(2) + ')';
  }

  /* ═══════════════════════════════════════════════════════════
     KICK-OFF
     ═══════════════════════════════════════════════════════════ */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  window.MasarVis = { state: S, render: renderNow };
})();
