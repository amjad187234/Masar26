/* ═══════════════════════════════════════════════
   MASAR WERBEAGENTUR – Main JavaScript
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  // ─── COOKIE BANNER ───
  const cookieBanner = document.getElementById('cookieBanner');
  if (cookieBanner) {
    if (!localStorage.getItem('cookies')) {
      setTimeout(function () { cookieBanner.classList.add('show'); }, 1500);
    }
    window.acceptCookies = function () {
      localStorage.setItem('cookies', '1');
      cookieBanner.classList.remove('show');
    };
  }

  // ─── NAV SCROLL SHADOW ───
  var mainNav = document.getElementById('mainNav');
  if (mainNav) {
    window.addEventListener('scroll', function () {
      mainNav.classList.toggle('scrolled', window.scrollY > 40);
    });
  }

  // ─── HAMBURGER ───
  var hamburger = document.getElementById('hamburger');
  var mobileMenu = document.getElementById('mobileMenu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function () {
      mobileMenu.classList.toggle('open');
    });
  }

  // ─── SMOOTH SCROLL ───
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var href = a.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      var el = document.querySelector(href);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (mobileMenu) mobileMenu.classList.remove('open');
    });
  });

  // ─── HERO SLIDER ───
  var heroTrack = document.getElementById('heroTrack');
  var heroDots = document.getElementById('heroDots');
  if (heroTrack && heroDots) {
    var hCur = 0;
    var hSlides = heroTrack.children.length;
    // Create dots
    for (var i = 0; i < hSlides; i++) {
      var d = document.createElement('button');
      d.className = 'sdot' + (i === 0 ? ' active' : '');
      d.setAttribute('aria-label', 'Slide ' + (i + 1));
      d.onclick = (function (n) { return function () { goHero(n); }; })(i);
      heroDots.appendChild(d);
    }
    function goHero(n) {
      hCur = (n + hSlides) % hSlides;
      heroTrack.style.transform = 'translateX(-' + (hCur * 100) + '%)';
      var dots = document.querySelectorAll('.sdot');
      for (var j = 0; j < dots.length; j++) {
        dots[j].classList.toggle('active', j === hCur);
      }
    }
    window.heroSlide = function (dir) { goHero(hCur + dir); };
    setInterval(function () { goHero(hCur + 1); }, 4500);
  }

  // ─── SERVICE TOGGLE (Mehr lesen) ───
  window.toggleSvc = function (btn) {
    var long = btn.previousElementSibling;
    if (!long) return;
    var isOpen = long.classList.toggle('open');
    btn.classList.toggle('open', isOpen);
    var textNode = btn.childNodes[0];
    if (textNode) textNode.textContent = isOpen ? 'Weniger anzeigen ' : 'Mehr lesen ';
  };

  // ─── FADE UP ON SCROLL ───
  var fadeObs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) e.target.classList.add('vis');
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-up').forEach(function (el) {
    fadeObs.observe(el);
  });

});
