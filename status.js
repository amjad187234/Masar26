/*
 * Masar – Anfrage-Status für Kunden (/status.html)
 * Anfragenummer + Telefon oder E-Mail → Ablauf (Eingegangen → In Bearbeitung → Angebot → In Arbeit → Fertig).
 * Gemerkte Anfragen (nur wenn der Kunde „auf diesem Gerät merken“ gewählt hat) stehen als Liste darunter.
 */
(function () {
  'use strict';
  var root = document.querySelector('[data-status]');
  if (!root) return;
  var KUNDE = 'masar-kunde';
  function kLesen() { try { return JSON.parse(localStorage.getItem(KUNDE) || 'null'); } catch (e) { return null; } }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function txt(tag, cls, t) { var e = el(tag, cls); e.textContent = t; return e; }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var SCHRITTE = ['Eingegangen', 'In Bearbeitung', 'Angebot', 'In Arbeit', 'Fertig'];
  var WA = '491785143918';

  var css = ''
    + '.st{max-width:760px;margin:0 auto;text-align:left}'
    + '.st-card{background:#fff;border:1px solid var(--border,#e0eaea);border-radius:16px;padding:1.5rem;box-shadow:0 10px 30px rgba(19,46,80,.07)}'
    + '.st-card+.st-card{margin-top:1rem}'
    + '.st h3{font:900 clamp(1.3rem,3vw,1.7rem)/1.1 "Barlow Condensed",sans-serif;text-transform:uppercase;color:var(--navy,#132e50);margin:0 0 1rem}'
    + '.st label{display:block;font:700 14px Barlow,sans-serif;color:var(--navy,#132e50);margin:.9rem 0 .4rem}.st label small{font-weight:400;color:var(--muted,#5a7070)}'
    + '.st input{width:100%;font:16px Barlow,sans-serif;border:1px solid var(--border,#e0eaea);border-radius:8px;padding:12px 14px;color:#132e50;background:#fff}'
    + '.st input:focus{outline:2px solid var(--teal,#58d0bd);outline-offset:1px}'
    + '.st-go{margin-top:1.1rem;background:var(--navy,#132e50);color:#fff;border:0;border-radius:8px;padding:13px 22px;font:700 15px Barlow,sans-serif;cursor:pointer;width:100%}.st-go[disabled]{opacity:.5}'
    + '.st-err{color:#b3261e;font-size:14px;margin:.7rem 0 0;min-height:1em}'
    + '.st-res{background:linear-gradient(135deg,#132e50,#0e2340);color:#fff;border:0}'
    + '.st-res .st-nr{font:700 13px Barlow,sans-serif;letter-spacing:1.2px;color:#58d0bd;text-transform:uppercase}'
    + '.st-res h4{font:900 clamp(1.6rem,4vw,2.1rem)/1.05 "Barlow Condensed",sans-serif;text-transform:uppercase;margin:.3rem 0 .6rem;color:#fff}'
    + '.st-res p{color:rgba(255,255,255,.85);line-height:1.6;margin:0 0 .8rem;font-size:15px}'
    + '.st-weg{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin:1.2rem 0 1rem;position:relative}'
    + '.st-weg div{text-align:center;font:600 12px/1.3 Barlow,sans-serif;color:rgba(255,255,255,.5)}'
    + '.st-weg i{display:block;height:8px;border-radius:4px;background:rgba(255,255,255,.15);margin-bottom:6px;overflow:hidden;position:relative}'
    + '.st-weg i:after{content:"";position:absolute;inset:0;background:#58d0bd;transform:scaleX(0);transform-origin:left;transition:transform .45s ease}'
    + '.st-weg .an{color:#fff}.st-weg .an i:after{transform:scaleX(1)}'
    + '.st-weg .jetzt{color:#58d0bd;font-weight:800}'
    + '.st-info{list-style:none;margin:.4rem 0 1rem;padding:0;border-top:1px solid rgba(255,255,255,.12)}'
    + '.st-info li{display:flex;gap:.8rem;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:14.5px}.st-info b{flex:0 0 110px;color:rgba(255,255,255,.6);font-weight:600}'
    + '.st-btns{display:flex;gap:.6rem;flex-wrap:wrap}'
    + '.st-btn{display:inline-flex;align-items:center;justify-content:center;border-radius:8px;padding:11px 16px;font:700 14.5px Barlow,sans-serif;text-decoration:none;background:#fff;color:#132e50}.st-btn.gr{background:#25d366;color:#08331a}.st-btn.tl{background:#58d0bd;color:#0e2340}'
    + '.st-list{list-style:none;margin:0;padding:0}'
    + '.st-list li{display:flex;align-items:center;justify-content:space-between;gap:.8rem;padding:.8rem 0;border-bottom:1px solid var(--border,#e0eaea)}'
    + '.st-list li b{display:block;color:var(--navy,#132e50)}.st-list li small{color:var(--muted,#5a7070)}'
    + '.st-list button{background:#e8f8f5;border:1px solid var(--teal,#58d0bd);color:var(--navy,#132e50);border-radius:8px;padding:8px 12px;font:700 13.5px Barlow,sans-serif;cursor:pointer;white-space:nowrap}'
    + '.st-weg-l{background:none;border:0;color:var(--muted,#5a7070);text-decoration:underline;font:13px Barlow,sans-serif;cursor:pointer;margin-top:.8rem;padding:0}'
    + '@media(max-width:560px){.st-card{padding:1.1rem}.st-weg div{font-size:10.5px}.st-info b{flex-basis:92px}}';
  css += '.st-res{animation:masarIn .45s ease both}@keyframes masarIn{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}@media(prefers-reduced-motion:reduce){.st-res{animation:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var kunde = kLesen();
  var q = new URLSearchParams(location.search);
  var box = el('div', 'st'); root.innerHTML = ''; root.appendChild(box);

  // Formular
  var f = el('form', 'st-card');
  f.appendChild(txt('h3', '', 'Status abfragen'));
  f.appendChild(el('label', '', 'Anfragenummer <small>(steht in der Bestätigung, z. B. ANF-2026-0012)</small>'));
  var inNr = el('input'); inNr.placeholder = 'ANF-2026-…'; inNr.autocomplete = 'off'; inNr.value = q.get('nr') || ''; inNr.maxLength = 20; f.appendChild(inNr);
  f.appendChild(el('label', '', 'Telefonnummer oder E-Mail <small>(wie in Ihrer Anfrage)</small>'));
  var inK = el('input'); inK.placeholder = 'z. B. 0176 … oder name@firma.de'; inK.autocomplete = 'tel'; inK.maxLength = 160;
  inK.value = kunde ? (kunde.tel || kunde.mail || '') : ''; f.appendChild(inK);
  var go = txt('button', 'st-go', 'Status anzeigen'); go.type = 'submit'; f.appendChild(go);
  var err = el('p', 'st-err'); err.setAttribute('role', 'alert'); f.appendChild(err);
  box.appendChild(f);
  var aus = el('div'); box.appendChild(aus);

  function abfragen(nr, kontakt) {
    err.textContent = ''; go.disabled = true; go.textContent = 'Wird geladen …';
    fetch('/status.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ nr: nr, kontakt: kontakt }), credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        go.disabled = false; go.textContent = 'Status anzeigen';
        if (!x.ok) { err.textContent = (x.j && x.j.fehler) || 'Keine Anfrage gefunden.'; return; }
        zeigen(x.j);
      })
      .catch(function () { go.disabled = false; go.textContent = 'Status anzeigen'; err.textContent = 'Keine Verbindung. Bitte später erneut versuchen.'; });
  }

  function zeigen(j) {
    aus.innerHTML = '';
    var c = el('div', 'st-card st-res');
    c.appendChild(txt('div', 'st-nr', j.nr + ' · Anfrage vom ' + j.datum));
    c.appendChild(txt('h4', '', j.titel));
    c.appendChild(txt('p', '', j.text));
    if (j.schritt > 0) {
      var weg = el('div', 'st-weg');
      SCHRITTE.forEach(function (n, i) { var d = el('div', i + 1 === j.schritt ? 'jetzt' : '', '<i></i>' + n); weg.appendChild(d); });
      c.appendChild(weg);
      // Balken nacheinander füllen
      Array.prototype.forEach.call(weg.children, function (d, i) { if (i < j.schritt) setTimeout(function () { d.classList.add('an'); }, 120 + i * 180); });
    }
    var ul = el('ul', 'st-info');
    [['Leistung', j.leistung], ['Ort', j.stadt], ['Termin', j.termin], ['Aktualisiert', j.aktualisiert]].forEach(function (z) {
      if (z[1]) ul.appendChild(el('li', '', '<b>' + z[0] + '</b><span>' + esc(z[1]) + '</span>'));
    });
    c.appendChild(ul);
    var b = el('div', 'st-btns');
    var wa = txt('a', 'st-btn gr', 'Frage per WhatsApp'); wa.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent('Hallo, ich habe eine Frage zu meiner Anfrage ' + j.nr + '.'); wa.target = '_blank'; wa.rel = 'noopener noreferrer'; b.appendChild(wa);
    if (j.schritt === 5 || j.schritt === 0) { var nb = txt('a', 'st-btn tl', 'Neue Anfrage stellen'); nb.href = '/#kontakt'; b.appendChild(nb); }
    var tb = txt('a', 'st-btn', 'Beratung buchen'); tb.href = '/termin.html'; b.appendChild(tb);
    c.appendChild(b);
    aus.appendChild(c);
    c.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var nr = inNr.value.trim().toUpperCase().replace(/\s+/g, '');
    if (!/^ANF-\d{4}-\d{4}$/.test(nr)) { err.textContent = 'Bitte die Anfragenummer im Format ANF-2026-0012 eingeben.'; return; }
    if (inK.value.trim().length < 5) { err.textContent = 'Bitte Telefonnummer oder E-Mail aus Ihrer Anfrage eingeben.'; return; }
    abfragen(nr, inK.value.trim());
  });

  // Gemerkte Anfragen auf diesem Gerät
  if (kunde && kunde.anfragen && kunde.anfragen.length) {
    var l = el('div', 'st-card');
    l.appendChild(txt('h3', '', 'Ihre Anfragen auf diesem Gerät'));
    var ul = el('ul', 'st-list');
    kunde.anfragen.forEach(function (a) {
      var li = el('li', '', '<span><b>' + esc(a.nr) + '</b><small>' + esc(a.leistung || '') + (a.datum ? ' · ' + esc(a.datum) : '') + '</small></span>');
      var bt = txt('button', '', 'Status ansehen'); bt.type = 'button';
      bt.addEventListener('click', function () { inNr.value = a.nr; if (!inK.value) inK.value = kunde.tel || kunde.mail || ''; abfragen(a.nr, inK.value.trim()); });
      li.appendChild(bt); ul.appendChild(li);
    });
    l.appendChild(ul);
    var v = txt('button', 'st-weg-l', 'Gespeicherte Daten auf diesem Gerät löschen'); v.type = 'button';
    v.addEventListener('click', function () { try { localStorage.removeItem(KUNDE); } catch (e) {} l.remove(); inK.value = ''; });
    l.appendChild(v);
    box.appendChild(l);
  }

  // Direkt abfragen, wenn Nummer im Link und Kontakt bekannt
  if (inNr.value && inK.value) abfragen(inNr.value.trim().toUpperCase(), inK.value.trim());
})();
