/*
 * Masar – Abschluss-Animation für Anfragen und Termine
 * Ring zählt 0 → 100 % (gekoppelt an den echten Versand), wird zum Haken, „Danke!“ + Farbregen.
 *
 *   var f = MasarFertig.start({ titel: 'Anfrage wird gesendet' });
 *   f.done({ nr: 'ANF-2026-0012', text: 'Wir melden uns innerhalb von 24 Stunden.', weiter: function () {...} });
 *   f.fail('Fehlertext');
 * Formulare mit action="/kontakt.php" bekommen die Animation automatisch beim Absenden.
 */
(function () {
  'use strict';
  if (window.MasarFertig) return;
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var css = ''
    + '.mf{position:fixed;inset:0;z-index:100000;display:flex;align-items:center;justify-content:center;padding:20px;background:rgba(10,24,44,.62);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);opacity:0;transition:opacity .3s}'
    + '.mf.on{opacity:1}'
    + '.mf-k{position:relative;width:min(380px,100%);background:#fff;border-radius:22px;padding:34px 26px 26px;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.35);transform:translateY(14px) scale(.96);transition:transform .45s cubic-bezier(.2,.9,.3,1.2);overflow:hidden;font-family:Barlow,system-ui,sans-serif}'
    + '.mf.on .mf-k{transform:none}'
    + '.mf-k:before{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#58d0bd,#132e50)}'
    + '.mf-ring{position:relative;width:148px;height:148px;margin:0 auto 18px}'
    + '.mf-ring svg{width:100%;height:100%;transform:rotate(-90deg)}'
    + '.mf-bg{fill:none;stroke:#e8f1f0;stroke-width:9}'
    + '.mf-pr{fill:none;stroke:url(#mfg);stroke-width:9;stroke-linecap:round;transition:stroke-dashoffset .12s linear}'
    + '.mf-orb{transform-origin:74px 74px}.mf-orb circle{fill:#58d0bd;filter:drop-shadow(0 0 6px rgba(88,208,189,.9))}'
    + '.mf-num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 40px/1 "Barlow Condensed",Barlow,sans-serif;color:#132e50;letter-spacing:.5px;transition:opacity .25s,transform .25s}'
    + '.mf-num small{font-size:20px;margin-left:2px;color:#177567}'
    + '.mf-ok{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.6);transition:opacity .3s,transform .45s cubic-bezier(.2,.9,.3,1.5)}'
    + '.mf-ok span{width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,#58d0bd,#2bb39f);display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(43,179,159,.45)}'
    + '.mf-ok svg{width:52px;height:52px;transform:none}.mf-ok path{fill:none;stroke:#fff;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:30;stroke-dashoffset:30;transition:stroke-dashoffset .5s .15s ease}'
    + '.mf.fertig .mf-num{opacity:0;transform:scale(.7)}.mf.fertig .mf-ok{opacity:1;transform:none}.mf.fertig .mf-ok path{stroke-dashoffset:0}.mf.fertig .mf-orb{opacity:0}'
    + '.mf-t{font:900 26px/1.1 "Barlow Condensed",Barlow,sans-serif;text-transform:uppercase;color:#132e50;margin:0 0 6px}'
    + '.mf-s{font-size:15px;color:#5a7070;margin:0;min-height:22px;transition:opacity .2s}'
    + '.mf-nr{display:none;margin:14px auto 0;background:#e8f8f5;border:1px solid #58d0bd;color:#132e50;border-radius:999px;padding:6px 14px;font-weight:700;font-size:14px;width:max-content;max-width:100%}'
    + '.mf.fertig .mf-nr.has{display:block;animation:mfin .4s .2s both}'
    + '.mf-b{display:none;margin:18px auto 0;background:#132e50;color:#fff;border:0;border-radius:10px;padding:12px 26px;font:700 15px Barlow,sans-serif;cursor:pointer}'
    + '.mf.fertig .mf-b{display:inline-block;animation:mfin .4s .35s both}'
    + '.mf-err .mf-pr{stroke:#e57373}.mf-err .mf-t{color:#b3261e}.mf.mf-err .mf-b{display:inline-block}'
    + '.mf canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}'
    + '@keyframes mfin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}'
    + '@media (prefers-reduced-motion:reduce){.mf,.mf-k,.mf-num,.mf-ok,.mf-ok path{transition:none!important;animation:none!important}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var SCHRITTE = ['Angaben werden geprüft …', 'Anfrage wird übertragen …', 'Wird sicher gespeichert …', 'Fast geschafft …'];
  var U = 2 * Math.PI * 64;

  function start(o) {
    o = o || {};
    var el = document.createElement('div'); el.className = 'mf'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-live', 'polite');
    el.innerHTML = '<div class="mf-k"><canvas></canvas><div class="mf-ring">'
      + '<svg viewBox="0 0 148 148" aria-hidden="true"><defs><linearGradient id="mfg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#58d0bd"/><stop offset="1" stop-color="#132e50"/></linearGradient></defs>'
      + '<circle class="mf-bg" cx="74" cy="74" r="64"/><circle class="mf-pr" cx="74" cy="74" r="64" stroke-dasharray="' + U + '" stroke-dashoffset="' + U + '"/>'
      + '<g class="mf-orb"><circle cx="138" cy="74" r="6"/></g></svg>'
      + '<div class="mf-num"><b>0</b><small>%</small></div>'
      + '<div class="mf-ok"><span><svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></span></div></div>'
      + '<p class="mf-t"></p><p class="mf-s"></p><div class="mf-nr"></div><button type="button" class="mf-b">Schließen</button></div>';
    el.querySelector('.mf-t').textContent = o.titel || 'Wird gesendet';
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('on'); });
    var pr = el.querySelector('.mf-pr'), orb = el.querySelector('.mf-orb'), num = el.querySelector('.mf-num b'), sub = el.querySelector('.mf-s');
    var wert = 0, ziel = 90, fertig = false, cb = null, t0 = performance.now();
    sub.textContent = SCHRITTE[0];

    function zeichne(v) {
      pr.style.strokeDashoffset = U * (1 - v / 100);
      orb.style.transform = 'rotate(' + (v * 3.6) + 'deg)';
      num.textContent = Math.round(v);
      sub.textContent = fertig ? sub.textContent : SCHRITTE[Math.min(SCHRITTE.length - 1, Math.floor(v / 26))];
    }
    function tick(now) {
      if (!el.isConnected) return;
      // bis 90 % gleichmäßig verlangsamt, dann warten auf echte Antwort; danach schnell auf 100
      var speed = fertig ? 2.6 : Math.max(0.06, (ziel - wert) * 0.018);
      if (still) wert = fertig ? 100 : Math.min(ziel, wert + 1.5); else wert = Math.min(fertig ? 100 : ziel, wert + speed);
      zeichne(wert);
      if (fertig && wert >= 100) { abschluss(); return; }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);

    function abschluss() {
      el.classList.add('fertig');
      el.querySelector('.mf-t').textContent = cb.titel || 'Danke!';
      sub.textContent = cb.text || 'Ihre Anfrage ist bei uns angekommen.';
      if (cb.nr) { var n = el.querySelector('.mf-nr'); n.textContent = 'Nr. ' + cb.nr; n.classList.add('has'); }
      var b = el.querySelector('.mf-b'); b.textContent = cb.knopf || 'Schließen';
      b.onclick = schliessen; b.focus({ preventScroll: true });
      if (!still) konfetti(el.querySelector('canvas'));
      if (cb.auto) setTimeout(schliessen, cb.auto);
    }
    function schliessen() {
      if (!el.isConnected) return;
      el.classList.remove('on'); setTimeout(function () { el.remove(); }, 300);
      if (cb && cb.weiter) { var w = cb.weiter; cb.weiter = null; w(); }
    }
    el.addEventListener('keydown', function (e) { if (e.key === 'Escape' && (fertig || el.classList.contains('mf-err'))) schliessen(); });
    return {
      done: function (d) {
        cb = d || {};
        var rest = Math.max(0, (o.mindestens || 1400) - (performance.now() - t0));   // kurze Mindestdauer, damit die Animation lesbar bleibt
        setTimeout(function () { fertig = true; }, rest);
      },
      fail: function (msg) {
        el.classList.add('mf-err'); el.querySelector('.mf-t').textContent = 'Nicht gesendet';
        sub.textContent = msg || 'Bitte erneut versuchen oder anrufen: 0178 514 3918.';
        ziel = wert; var b = el.querySelector('.mf-b'); b.onclick = function () { cb = null; schliessen(); };
      },
      close: function () { cb = cb || {}; schliessen(); }
    };
  }

  function konfetti(cv) {
    var k = cv.parentNode, w = cv.width = k.offsetWidth * 2, h = cv.height = k.offsetHeight * 2, c = cv.getContext('2d');
    var farben = ['#58d0bd', '#132e50', '#2bb39f', '#e9b44c', '#7fd8c9'], teile = [];
    for (var i = 0; i < 90; i++) teile.push({ x: w / 2, y: h * .3, vx: (Math.random() - .5) * 26, vy: -Math.random() * 22 - 6, r: Math.random() * 6 + 4, f: farben[i % farben.length], a: Math.random() * 6, va: (Math.random() - .5) * .4, form: i % 3 });
    var t = 0;
    (function lauf() {
      c.clearRect(0, 0, w, h); t++;
      teile.forEach(function (p) {
        p.vy += .7; p.vx *= .985; p.x += p.vx; p.y += p.vy; p.a += p.va;
        c.save(); c.translate(p.x, p.y); c.rotate(p.a); c.globalAlpha = Math.max(0, 1 - t / 110); c.fillStyle = p.f;
        if (p.form === 0) c.fillRect(-p.r, -p.r / 2, p.r * 2, p.r); else if (p.form === 1) { c.beginPath(); c.arc(0, 0, p.r * .7, 0, 7); c.fill(); }
        else { c.beginPath(); c.moveTo(0, -p.r); c.lineTo(p.r, p.r); c.lineTo(-p.r, p.r); c.fill(); }
        c.restore();
      });
      if (t < 110) requestAnimationFrame(lauf); else c.clearRect(0, 0, w, h);
    })();
  }

  window.MasarFertig = { start: start };

  // Klassische Formulare (/kontakt.php): Animation beim Absenden, Weiterleitung auf danke.html übernimmt den Abschluss
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || !/\/kontakt\.php$/.test(f.getAttribute('action') || '') || e.defaultPrevented) return;
    setTimeout(function () { if (!e.defaultPrevented) start({ titel: 'Anfrage wird gesendet' }); }, 0);
  });
})();
