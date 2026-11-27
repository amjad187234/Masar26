/* KI-Chatbot-Generator (Versuch): Besucher geben ihre Website ein und testen einen Assistenten,
 * der nur aus dem öffentlichen Inhalt dieser Website antwortet.
 * Einbau: <div data-ki-generator></div>. Der Abschnitt bleibt unsichtbar, solange der Server
 * den Generator nicht freigibt (kein Schlüssel, Notschalter oder Monatsbudget erreicht).
 * Alle Texte vom Server werden als reiner Text eingesetzt (kein innerHTML). */
(function () {
  'use strict';
  var API = '/ki-generator.php';
  var CSS = '.kg [hidden]{display:none!important}.kg{max-width:680px;margin:0 auto;background:#fff;border:1px solid #dce6ee;border-radius:16px;padding:1.4rem;color:#1a2a2a;text-align:left}' +
    '.kg label{display:block;font-weight:700;color:#132e50;margin-bottom:.4rem}.kg-row{display:flex;gap:.6rem;flex-wrap:wrap}' +
    '.kg input[type=text]{flex:1 1 220px;min-width:0;padding:.8rem 1rem;border:1px solid #b9c7d3;border-radius:10px;font:inherit;font-size:16px}' +
    '.kg button{font:inherit;font-weight:700;border:0;border-radius:10px;padding:.8rem 1.2rem;background:#132e50;color:#fff;cursor:pointer}' +
    '.kg button[disabled]{opacity:.55;cursor:default}.kg-ok{display:flex;gap:.6rem;align-items:flex-start;font-size:14px;color:#3d5252;margin:.9rem 0 0}' +
    '.kg-ok input{margin-top:.2rem;width:18px;height:18px;flex:none}.kg-err{color:#b3261e;font-weight:600;margin:.8rem 0 0;min-height:1.2em}' +
    '.kg-hin{background:#e8f8f5;color:#177567;border-radius:10px;padding:.6rem .8rem;font-size:14px;margin-bottom:.8rem}' +
    '.kg-log{display:flex;flex-direction:column;gap:.6rem;max-height:340px;overflow:auto;padding:.2rem 0 .8rem}' +
    '.kg-m{max-width:86%;padding:.65rem .9rem;border-radius:14px;line-height:1.5;white-space:pre-wrap;overflow-wrap:anywhere}' +
    '.kg-b{background:#f4f7f7;border:1px solid #e1e8e8;align-self:flex-start}.kg-u{background:#58d0bd;color:#132e50;font-weight:600;align-self:flex-end}' +
    '.kg-chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.8rem}.kg-chips button{background:#fff;color:#132e50;border:1px solid #58d0bd;padding:.5rem .8rem;font-weight:600}' +
    '.kg-cta{margin-top:1rem;padding-top:1rem;border-top:1px solid #e1e8e8;font-size:15px}.kg-cta a{display:inline-block;margin:.5rem .6rem 0 0;padding:.7rem 1rem;border-radius:10px;background:#58d0bd;color:#132e50;font-weight:700;text-decoration:none}' +
    '.kg-cta a.kg-2{background:#fff;border:1px solid #132e50}.kg-rest{font-size:13px;color:#5a7070;margin-top:.5rem}';

  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function post(d) {
    return fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d), credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .catch(function () { return { ok: false, fehler: 'Keine Verbindung. Bitte noch einmal versuchen.' }; });
  }

  function bau(root) {
    var sek = root.closest('section'); 
    var box = el('div', 'kg'); root.appendChild(box);
    var st = { id: '', domain: '', n: 0 };

    function start() {
      box.innerHTML = '';
      var f = el('form'); f.noValidate = true;
      var l = el('label', '', 'Adresse Ihrer Website'); l.htmlFor = 'kg-url';
      var row = el('div', 'kg-row'), inp = el('input'); inp.type = 'text'; inp.id = 'kg-url'; inp.inputMode = 'url'; inp.autocomplete = 'url'; inp.placeholder = 'z. B. www.ihr-betrieb.de'; inp.maxLength = 200;
      var go = el('button', '', 'Assistent erstellen'); go.type = 'submit';
      row.appendChild(inp); row.appendChild(go);
      var ok = el('label', 'kg-ok'), cb = el('input'); cb.type = 'checkbox'; cb.id = 'kg-ok';
      ok.appendChild(cb);
      var t = el('span', '', 'Das ist meine Website oder ich darf sie testen. Ich bin einverstanden, dass ihr öffentlicher Text und meine Fragen zur Beantwortung an den KI-Dienst Anthropic (USA) übermittelt und 24 Stunden gespeichert werden. Bitte keine personenbezogenen Daten eingeben. ');
      var dl = el('a', '', 'Datenschutz'); dl.href = '/datenschutz.html#ki-generator'; t.appendChild(dl); ok.appendChild(t);
      var err = el('p', 'kg-err'); err.setAttribute('role', 'alert');
      f.appendChild(l); f.appendChild(row); f.appendChild(ok); f.appendChild(err); box.appendChild(f);
      f.addEventListener('submit', function (ev) {
        ev.preventDefault(); err.textContent = '';
        if (!inp.value.trim()) { err.textContent = 'Bitte die Adresse Ihrer Website eingeben.'; inp.focus(); return; }
        if (!cb.checked) { err.textContent = 'Bitte den Hinweis bestätigen.'; cb.focus(); return; }
        go.disabled = true; go.textContent = 'Website wird gelesen …';
        post({ a: 'start', url: inp.value.trim(), ok: true }).then(function (r) {
          if (!r.ok) { go.disabled = false; go.textContent = 'Assistent erstellen'; err.textContent = r.fehler || 'Das hat nicht geklappt.'; return; }
          st.id = r.id; st.domain = r.domain; st.n = 0; chat(r);
        });
      });
    }

    function chat(r) {
      box.innerHTML = '';
      box.appendChild(el('div', 'kg-hin', 'Vorführung für ' + r.domain + ' – Sie schreiben mit einem digitalen Assistenten (KI). Er kennt nur den öffentlichen Text Ihrer Website; Antworten können Fehler enthalten.'));
      var log = el('div', 'kg-log'); log.setAttribute('aria-live', 'polite'); box.appendChild(log);
      var chips = el('div', 'kg-chips'); box.appendChild(chips);
      var f = el('form'), row = el('div', 'kg-row'), inp = el('input'); inp.type = 'text'; inp.maxLength = 300; inp.placeholder = 'Frage stellen, wie es Ihre Kunden tun würden'; inp.setAttribute('aria-label', 'Ihre Frage');
      var go = el('button', '', 'Senden'); go.type = 'submit'; row.appendChild(inp); row.appendChild(go); f.appendChild(row); box.appendChild(f);
      var rest = el('p', 'kg-rest'); box.appendChild(rest);
      var cta = el('div', 'kg-cta'); cta.hidden = true; box.appendChild(cta);
      cta.appendChild(el('strong', '', 'So könnte der Assistent auf Ihrer Website antworten.'));
      cta.appendChild(el('div', '', 'Auf Ihrer Seite arbeitet er mit Ihren geprüften Angaben, nimmt Anfragen vollständig auf und meldet sie Ihnen aufs Handy.'));
      var wa = el('a', '', 'Per WhatsApp anfragen'); wa.target = '_blank'; wa.rel = 'noopener noreferrer';
      wa.href = 'https://wa.me/491785143918?text=' + encodeURIComponent('Hallo, ich habe den Chatbot-Generator mit ' + r.domain + ' getestet und möchte den Assistenten für meine Website anfragen.');
      var k = el('a', 'kg-2', 'Erstgespräch anfragen'); k.href = document.getElementById('kontakt') ? '#kontakt' : '/ki-fuer-handwerker-berlin.html#kontakt';
      cta.appendChild(wa); cta.appendChild(k);
      var neu = el('button', '', 'Andere Website testen'); neu.type = 'button'; neu.style.cssText = 'background:none;color:#177567;padding:.4rem 0;margin-top:.6rem;text-decoration:underline;font-weight:600'; neu.addEventListener('click', start); cta.appendChild(neu);

      function sag(wer, text) { var m = el('div', 'kg-m ' + (wer === 'u' ? 'kg-u' : 'kg-b'), text); log.appendChild(m); log.scrollTop = log.scrollHeight; return m; }
      function frag(text) {
        text = (text || '').trim(); if (!text || go.disabled) return;
        chips.hidden = true; sag('u', text); inp.value = ''; go.disabled = true;
        var w = sag('b', '…');
        post({ a: 'chat', id: st.id, text: text }).then(function (a) {
          go.disabled = false;
          w.textContent = a.ok ? a.antwort : (a.fehler || 'Das hat nicht geklappt.');
          if (a.ok) { st.n++; rest.textContent = a.rest > 0 ? 'Noch ' + a.rest + ' Fragen in dieser Vorführung.' : ''; if (a.rest <= 0) { f.hidden = true; } }
          if (st.n >= 2 || a.ende || (a.ok && a.rest <= 0)) cta.hidden = false;
          if (a.ende) f.hidden = true;
          if (!f.hidden) inp.focus();
        });
      }
      sag('b', 'Hallo! Ich bin ein digitaler Assistent (KI) und habe gerade die Website ' + r.domain + ' gelesen. Stellen Sie mir eine Frage, wie es Ihre Kunden tun würden.');
      (r.fragen || []).forEach(function (q) { var b = el('button', '', q); b.type = 'button'; b.addEventListener('click', function () { frag(q); }); chips.appendChild(b); });
      f.addEventListener('submit', function (ev) { ev.preventDefault(); frag(inp.value); });
    }
    start();
    if (sek) sek.hidden = false;
  }

  function los() {
    var orte = document.querySelectorAll('[data-ki-generator]'); if (!orte.length) return;
    fetch(API + '?a=status', { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (s) {
      if (!s || !s.an) return;
      if (!document.getElementById('kg-css')) { var c = el('style'); c.id = 'kg-css'; c.textContent = CSS; document.head.appendChild(c); }
      orte.forEach(bau);
    }).catch(function () { /* bleibt unsichtbar */ });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', los); else los();
})();
