/* Sicherheitsnetz fuer die Einblend-Animation.
   Der IntersectionObserver kann je nach Fenstergroesse einzelne Elemente
   auslassen - dann bliebe Inhalt dauerhaft unsichtbar. Dieses Skript blendet
   alles nach, was sich bereits im sichtbaren Bereich befindet. Es ersetzt die
   Animation nicht, es faengt nur die Ausreisser ab. */
(function () {
  var SEL = '.reveal,.reveal-l,.reveal-r,.fade-up,.svc-card,.why-item,.prob-item';
  var MARGIN = 400;

  function sweep() {
    var edge = window.pageYOffset + window.innerHeight + MARGIN;
    var nodes = document.querySelectorAll(SEL);
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.classList.contains('in') || el.classList.contains('vis')) continue;
      if (el.getBoundingClientRect().top + window.pageYOffset < edge) {
        el.classList.add('in');
        el.classList.add('vis');
      }
    }
  }

  var pending = null;
  function schedule() {
    if (pending) return;
    pending = setTimeout(function () { pending = null; sweep(); }, 160);
  }

  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  window.addEventListener('load', sweep);
  if (document.readyState === 'complete') sweep();
  setTimeout(sweep, 1500);
})();
