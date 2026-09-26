/* WhatsApp-Knopf ueber der Sticky-Leiste halten.
   Die Leiste ist je nach Textlaenge und Bildschirmbreite unterschiedlich hoch
   (am Handy 100-180 px). Ein fester Abstand im CSS reicht deshalb nicht: der
   Knopf wuerde den Text der Leiste verdecken. Dieses Skript hebt den Knopf
   genau so weit an, wie die Leiste gerade sichtbar ist - und nie tiefer als
   seine urspruengliche Position. */
(function () {
  var bar = document.getElementById('stickyCta') || document.querySelector('.sticky-cta');
  var fabs = Array.prototype.slice.call(document.querySelectorAll('a.wa'));
  if (!bar || !fabs.length) return;

  var base = fabs.map(function (f) { return parseFloat(getComputedStyle(f).bottom) || 20; });
  fabs.forEach(function (f) { f.style.transition = (f.style.transition ? f.style.transition + ',' : '') + 'bottom .3s ease'; });

  function place() {
    var r = bar.getBoundingClientRect();
    var shown = getComputedStyle(bar).display !== 'none' && r.top < window.innerHeight - 1;
    var lift = shown ? Math.max(0, window.innerHeight - r.top) : 0;
    fabs.forEach(function (f, i) {
      f.style.bottom = Math.max(base[i], lift ? lift + 12 : 0) + 'px';
    });
  }

  place();
  new MutationObserver(place).observe(bar, { attributes: true, attributeFilter: ['class', 'style'] });
  if (window.ResizeObserver) new ResizeObserver(place).observe(bar);
  bar.addEventListener('transitionend', place);
  window.addEventListener('resize', place, { passive: true });
  window.addEventListener('scroll', place, { passive: true });
})();
