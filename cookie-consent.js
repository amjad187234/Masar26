/**
 * ═══════════════════════════════════════════════════════════
 * MASAR WERBEAGENTUR — Cookie Consent System
 * DSGVO / TDDDG konform (§25 TDDDG, Art. 6 DSGVO)
 * 
 * Features:
 * - Kein Dark Pattern (Ablehnen = gleiche Gewichtung)
 * - Tracking blockiert bis zur Einwilligung
 * - Persistente Widerrufsmöglichkeit
 * - localStorage Speicherung
 * ═══════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ─── CONFIG ───────────────────────────────────────────────
  var CONSENT_KEY  = 'masarCookieConsent';
  var DATE_KEY     = 'masarConsentDate';
  var EXPIRY_DAYS  = 365;

  // ─── STATE ────────────────────────────────────────────────
  var consentState = {
    necessary: true,    // immer aktiv
    analytics: false,
    marketing: false,
    decided: false
  };

  // ─── localStorage AVAILABILITY CHECK ─────────────────────
  var storageOk = (function() {
    try { localStorage.setItem('__t', '1'); localStorage.removeItem('__t'); return true; }
    catch(e) { return false; }
  })();

  // ─── LOAD SAVED CONSENT ──────────────────────────────────
  function loadConsent() {
    if (!storageOk) return null; // localStorage disabled → always show banner
    var saved = localStorage.getItem(CONSENT_KEY);
    if (!saved) return null;

    try {
      var parsed = JSON.parse(saved);
      var savedDate = new Date(localStorage.getItem(DATE_KEY) || 0);
      var expiryDate = new Date(savedDate.getTime() + EXPIRY_DAYS * 86400000);

      if (new Date() > expiryDate) {
        localStorage.removeItem(CONSENT_KEY);
        localStorage.removeItem(DATE_KEY);
        return null;
      }
      return parsed;
    } catch(e) {
      return null;
    }
  }

  // ─── SAVE CONSENT ─────────────────────────────────────────
  function saveConsent(state) {
    consentState = Object.assign({}, state, { decided: true });
    if (!storageOk) return; // gracefully skip if storage unavailable
    localStorage.setItem(CONSENT_KEY, JSON.stringify(consentState));
    localStorage.setItem(DATE_KEY, new Date().toISOString());
  }

  // ─── LOAD TRACKING (nur nach Einwilligung) ────────────────
  function loadAnalytics() {
    // Google Analytics — nur wenn eingewilligt
    // window.dataLayer = window.dataLayer || [];
    // function gtag(){dataLayer.push(arguments);}
    // gtag('js', new Date());
    // var s = document.createElement('script');
    // s.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
    // s.async = true;
    // document.head.appendChild(s);
  }

  function loadMarketing() {
    // Meta Pixel — nur wenn eingewilligt
    // !function(f,b,e,v,n,t,s){...}
    // fbq('init', 'XXXXXXXXXXXXXXXXX');
    // fbq('track', 'PageView');
  }

  function applyConsent(state) {
    if (state.analytics) loadAnalytics();
    if (state.marketing) loadMarketing();
  }

  // ─── CREATE BANNER HTML ───────────────────────────────────
  function createBanner() {
    var div = document.createElement('div');
    div.id = 'masar-cookie-root';
    div.innerHTML = [
      '<style>',
      '#masar-cookie-root *{box-sizing:border-box;margin:0;padding:0;font-family:inherit;}',
      '#masar-cookie-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:99997;backdrop-filter:blur(3px);}',
      '#masar-cookie-overlay.show{display:block;}',
      '#masar-cookie-banner{',
        'display:none;position:fixed;bottom:0;left:0;right:0;z-index:99998;',
        'background:#fff;border-top:3px solid #58d0bd;',
        'box-shadow:0 -8px 40px rgba(0,0,0,.15);',
        'padding:1.5rem 2rem;',
        'font-family:system-ui,-apple-system,sans-serif;',
        'max-height:90vh;overflow-y:auto;',
      '}',
      '#masar-cookie-banner.show{display:block;}',
      '.mck-wrap{display:flex;align-items:center;justify-content:space-between;gap:2rem;flex-wrap:wrap;}',
      '.mck-title{font-weight:800;font-size:1rem;color:#132e50;margin-bottom:.35rem;}',
      '.mck-text{font-size:13px;color:#5a7070;line-height:1.55;max-width:680px;}',
      '.mck-text a{color:#58d0bd;font-weight:600;text-decoration:none;}',
      '.mck-actions{display:flex;gap:.7rem;flex-shrink:0;flex-wrap:wrap;}',
      /* KEIN DARK PATTERN — beide Buttons gleich gewichtet */
      '.mck-btn{',
        'padding:10px 22px;border-radius:6px;font-size:13px;font-weight:700;',
        'cursor:pointer;border:2px solid;transition:all .2s;',
        'font-family:system-ui,sans-serif;white-space:nowrap;',
        'min-width:140px;text-align:center;',
      '}',
      '.mck-reject{background:#fff;color:#132e50;border-color:#e2ecec;}',
      '.mck-reject:hover{background:#f5f8f8;border-color:#132e50;}',
      '.mck-settings-btn{background:#f5f8f8;color:#132e50;border-color:#e2ecec;}',
      '.mck-settings-btn:hover{border-color:#58d0bd;}',
      '.mck-accept{background:#58d0bd;color:#132e50;border-color:#58d0bd;}',
      '.mck-accept:hover{background:#3ab8a5;border-color:#3ab8a5;}',
      /* SETTINGS PANEL */
      '.mck-settings{display:none;margin-top:1.2rem;border-top:1px solid #e2ecec;padding-top:1.2rem;}',
      '.mck-settings.open{display:block;}',
      '.mck-setting{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;padding:.7rem 0;border-bottom:1px solid #f0f4f4;}',
      '.mck-setting-info strong{font-size:14px;color:#132e50;font-weight:700;}',
      '.mck-setting-info p{font-size:12px;color:#5a7070;margin-top:.2rem;line-height:1.45;}',
      '.mck-toggle{min-width:52px;padding:6px 12px;border-radius:20px;font-size:11px;font-weight:800;cursor:pointer;border:none;transition:all .2s;letter-spacing:.5px;}',
      '.mck-toggle.off{background:#e2ecec;color:#5a7070;}',
      '.mck-toggle.on{background:#58d0bd;color:#132e50;}',
      '.mck-toggle.locked{opacity:.6;cursor:not-allowed;}',
      '.mck-save-row{display:flex;gap:.7rem;justify-content:flex-end;margin-top:1rem;flex-wrap:wrap;}',
      /* REVOKE WIDGET (persistent) */
      '#masar-cookie-widget{',
        'position:fixed;bottom:24px;left:20px;z-index:99996;',
        'width:38px;height:38px;border-radius:50%;',
        'background:#fff;border:2px solid #e2ecec;',
        'display:flex;align-items:center;justify-content:center;',
        'cursor:pointer;box-shadow:0 2px 12px rgba(0,0,0,.12);',
        'transition:all .25s;',
        'font-size:16px;',
        'title:"Cookie-Einstellungen ändern"',
      '}',
      '#masar-cookie-widget:hover{border-color:#58d0bd;transform:scale(1.1);}',
      /* RESPONSIVE */
      '@media(max-width:640px){',
        '#masar-cookie-banner{padding:1rem 1.2rem;}',
        '.mck-wrap{flex-direction:column;align-items:flex-start;}',
        '.mck-actions{width:100%;}',
        '.mck-btn{flex:1;min-width:0;}',
        '.mck-save-row{justify-content:stretch;}',
        '.mck-save-row .mck-btn{flex:1;min-width:0;}',
        '.mck-setting{flex-direction:row;align-items:center;}',
      '}',
      '</style>',

      '<div id="masar-cookie-overlay"></div>',

      '<div id="masar-cookie-banner" role="dialog" aria-modal="true" aria-label="Cookie-Einstellungen">',
        '<div class="mck-wrap">',
          '<div>',
            '<div class="mck-title">🍪 Wir respektieren Ihre Privatsphäre</div>',
            '<p class="mck-text">',
              'Wir verwenden Cookies. Notwendige Cookies sind für den Betrieb der Website erforderlich. ',
              'Analyse- und Marketing-Cookies helfen uns, die Website zu verbessern – ',
              'sie werden nur mit Ihrer Einwilligung gesetzt. ',
              '<a href="/datenschutz.html" target="_blank">Datenschutzerklärung</a>',
            '</p>',
          '</div>',
          '<div class="mck-actions">',
            '<button class="mck-btn mck-reject" id="mck-reject">Alle ablehnen</button>',
            '<button class="mck-btn mck-settings-btn" id="mck-settings-toggle">Einstellungen</button>',
            '<button class="mck-btn mck-accept" id="mck-accept">Alle akzeptieren</button>',
          '</div>',
        '</div>',

        '<div class="mck-settings" id="mck-settings">',
          '<div class="mck-setting">',
            '<div class="mck-setting-info">',
              '<strong>Notwendige Cookies</strong>',
              '<p>Technisch erforderlich für Grundfunktionen (z.B. Cookie-Einwilligung, Sprachauswahl). Können nicht deaktiviert werden.</p>',
            '</div>',
            '<button class="mck-toggle on locked" disabled>AKTIV</button>',
          '</div>',
          '<div class="mck-setting">',
            '<div class="mck-setting-info">',
              '<strong>Analyse-Cookies</strong>',
              '<p>Helfen uns zu verstehen, wie Besucher unsere Website nutzen (z.B. Google Analytics, Matomo).</p>',
            '</div>',
            '<button class="mck-toggle off" id="mck-analytics-toggle">AUS</button>',
          '</div>',
          '<div class="mck-setting">',
            '<div class="mck-setting-info">',
              '<strong>Marketing-Cookies</strong>',
              '<p>Ermöglichen personalisierte Werbung (z.B. Meta Pixel, Google Ads). Ihre Daten können an Dritte übertragen werden.</p>',
            '</div>',
            '<button class="mck-toggle off" id="mck-marketing-toggle">AUS</button>',
          '</div>',
          '<div class="mck-save-row">',
            '<button class="mck-btn mck-reject" id="mck-save">Auswahl speichern</button>',
            '<button class="mck-btn mck-accept" id="mck-accept-settings">Alle akzeptieren</button>',
          '</div>',
        '</div>',
      '</div>',

      '<button id="masar-cookie-widget" title="Cookie-Einstellungen" aria-label="Cookie-Einstellungen ändern">⚙️</button>',
    ].join('');

    document.body.appendChild(div);
  }

  // ─── SHOW / HIDE ──────────────────────────────────────────
  function showBanner() {
    document.getElementById('masar-cookie-banner').classList.add('show');
    document.getElementById('masar-cookie-overlay').classList.add('show');
  }
  function hideBanner() {
    document.getElementById('masar-cookie-banner').classList.remove('show');
    document.getElementById('masar-cookie-overlay').classList.remove('show');
    document.getElementById('mck-settings').classList.remove('open');
  }

  // ─── TOGGLE HELPERS ───────────────────────────────────────
  function toggleSwitch(btn, state) {
    if (state) {
      btn.className = 'mck-toggle on';
      btn.textContent = 'AN';
    } else {
      btn.className = 'mck-toggle off';
      btn.textContent = 'AUS';
    }
  }

  // ─── BIND EVENTS ──────────────────────────────────────────
  function bindEvents() {
    var analyticsToggle = document.getElementById('mck-analytics-toggle');
    var marketingToggle = document.getElementById('mck-marketing-toggle');
    var analyticsState  = false;
    var marketingState  = false;

    analyticsToggle.addEventListener('click', function(){
      analyticsState = !analyticsState;
      toggleSwitch(analyticsToggle, analyticsState);
    });
    marketingToggle.addEventListener('click', function(){
      marketingState = !marketingState;
      toggleSwitch(marketingToggle, marketingState);
    });

    document.getElementById('mck-accept').addEventListener('click', function(){
      var state = {necessary:true, analytics:true, marketing:true, decided:true};
      saveConsent(state);
      hideBanner();
      applyConsent(state);
    });

    document.getElementById('mck-reject').addEventListener('click', function(){
      var state = {necessary:true, analytics:false, marketing:false, decided:true};
      saveConsent(state);
      hideBanner();
    });

    document.getElementById('mck-settings-toggle').addEventListener('click', function(){
      document.getElementById('mck-settings').classList.toggle('open');
    });

    document.getElementById('mck-save').addEventListener('click', function(){
      var state = {necessary:true, analytics:analyticsState, marketing:marketingState, decided:true};
      saveConsent(state);
      hideBanner();
      applyConsent(state);
    });

    document.getElementById('mck-accept-settings').addEventListener('click', function(){
      var state = {necessary:true, analytics:true, marketing:true, decided:true};
      saveConsent(state);
      hideBanner();
      applyConsent(state);
    });

    // PERSISTENT REVOKE WIDGET
    document.getElementById('masar-cookie-widget').addEventListener('click', function(){
      // Reset toggles to current state
      var curr = loadConsent() || {};
      toggleSwitch(analyticsToggle, curr.analytics || false);
      toggleSwitch(marketingToggle, curr.marketing || false);
      analyticsState = curr.analytics || false;
      marketingState = curr.marketing || false;
      showBanner();
      document.getElementById('mck-settings').classList.add('open');
    });

    // Close on overlay click
    document.getElementById('masar-cookie-overlay').addEventListener('click', hideBanner);
  }

  // ─── INIT ─────────────────────────────────────────────────
  function init() {
    createBanner();
    bindEvents();

    var saved = loadConsent();
    if (saved && saved.decided) {
      // Consent already given — apply & hide banner
      applyConsent(saved);
    } else {
      // No consent yet — show immediately (TDDDG §25: consent required before non-essential cookies)
      showBanner();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
