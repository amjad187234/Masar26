/* WhatsApp-Knopf (und Cookie-Symbol unten links) ueber der Sticky-Leiste halten.
   Die Leiste ist je nach Textlaenge und Bildschirmbreite unterschiedlich hoch
   (am Handy 100-180 px). Ein fester Abstand im CSS reicht deshalb nicht: der
   Knopf wuerde den Text der Leiste verdecken. Dieses Skript hebt die Knoepfe
   genau so weit an, wie die Leiste gerade sichtbar ist - und nie tiefer als
   ihre urspruengliche Position. Das Cookie-Symbol entsteht erst nach dem
   Laden (cookie-consent.js) und wird deshalb bei jedem Durchlauf neu gesucht. */
(function () {
  var bar = document.getElementById('stickyCta') || document.querySelector('.sticky-cta');
  if (!bar) return;
  var base = new WeakMap();

  function knoepfe() {
    var l = Array.prototype.slice.call(document.querySelectorAll('a.wa'));
    var c = document.getElementById('masar-cookie-widget');
    if (c) l.push(c);
    l.forEach(function (f) {
      if (base.has(f)) return;
      base.set(f, parseFloat(getComputedStyle(f).bottom) || 20);
      f.style.transition = (f.style.transition ? f.style.transition + ',' : '') + 'bottom .3s ease';
    });
    return l;
  }

  // Knoepfe im Seitenkopf (z. B. „Angebot anfordern“), die der runde WhatsApp-Knopf am Handy verdecken wuerde
  var kopf = Array.prototype.slice.call(document.querySelectorAll('.hero-btns, .hero .btn, .ph-btns'));
  function deckt(a, b) { return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top; }

  // Platz am Seitenende, damit die Leiste die letzten Links (Impressum, Datenschutz, Cookie-Einstellungen) nicht verdeckt
  var pad0 = parseFloat(getComputedStyle(document.body).paddingBottom) || 0;
  function platz() {
    var h = getComputedStyle(bar).display !== 'none' && bar.style.display !== 'none' ? bar.offsetHeight : 0;
    var v = h > pad0 ? h + 'px' : '';
    if (document.body.style.paddingBottom !== v) document.body.style.paddingBottom = v;
  }

  function place() {
    platz();
    var r = bar.getBoundingClientRect();
    var shown = getComputedStyle(bar).display !== 'none' && r.top < window.innerHeight - 1;
    var lift = shown ? Math.max(0, window.innerHeight - r.top) : 0;
    knoepfe().forEach(function (f) {
      f.style.bottom = Math.max(base.get(f), lift ? lift + 12 : 0) + 'px';
      if (f.id === 'masar-cookie-widget') return;
      // Solange der WhatsApp-Knopf auf einem Kopf-Knopf liegt: kurz ausblenden (der Kopf hat eigene Kontakt-Knoepfe)
      var fr = f.getBoundingClientRect(), weg = false;
      if (window.innerWidth <= 900) for (var i = 0; i < kopf.length && !weg; i++) { var k = kopf[i].getBoundingClientRect(); if (k.height && deckt(fr, k)) weg = true; }
      f.classList.toggle('fab-weg', weg);
    });
  }
  var st = document.createElement('style');
  st.textContent = 'a.wa{transition:opacity .2s ease,bottom .3s ease}a.wa.fab-weg{opacity:0;pointer-events:none;visibility:hidden}';
  document.head.appendChild(st);

  place();
  new MutationObserver(place).observe(bar, { attributes: true, attributeFilter: ['class', 'style'] });
  if (window.ResizeObserver) new ResizeObserver(place).observe(bar);
  bar.addEventListener('transitionend', place);
  window.addEventListener('resize', place, { passive: true });
  window.addEventListener('scroll', place, { passive: true });
  window.addEventListener('load', place);
})();
