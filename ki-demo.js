/*
 * Masar – Demo eines digitalen Assistenten (Chat/WhatsApp) für Praxen und Pflegedienste.
 * Reine Vorführung im Browser: keine KI-Anfrage, keine Daten werden gesendet oder gespeichert.
 * Einbau: <div data-ki-demo="praxis|pflege"></div> + <script src="/ki-demo.js" defer></script>
 */
(function () {
  'use strict';
  var SZ = {
    praxis: {
      name: 'Praxis-Assistent', sub: 'Beispielpraxis · Berlin',
      start: ['Guten Tag! Ich bin der digitale Assistent der Praxis. Wobei kann ich helfen?'],
      wahl: [['Termin verschieben', 'termin'], ['Folgerezept anfragen', 'rezept'], ['Öffnungszeiten', 'zeiten'], ['Andere Sprache', 'sprache'], ['Ich habe starke Schmerzen', 'notfall']],
      wege: {
        termin: [['bot', 'Gern. An welchem Tag ist Ihr bisheriger Termin?'], ['wahl', [['Donnerstag, 14:30 Uhr', 'termin2']]]],
        termin2: [['bot', 'Danke. Wann würde es Ihnen besser passen?'], ['wahl', [['Nächste Woche vormittags', 'termin3'], ['Egal, Hauptsache bald', 'termin3']]]],
        termin3: [['bot', 'Ich gebe Ihren Wunsch an das Praxisteam weiter. Sie bekommen den neuen Termin als Bestätigung per SMS.'], ['karte', ['Terminverschiebung', 'Bisher: Do 14:30 · Wunsch: nächste Woche vormittags', 'Rückmeldung an Patient per SMS', 'Team bestätigt mit einem Klick']]],
        rezept: [['bot', 'Für welches Medikament? Am besten so, wie es auf der Packung steht.'], ['wahl', [['Dauermedikament wie im letzten Quartal', 'rezept2']]]],
        rezept2: [['bot', 'Möchten Sie das Rezept abholen oder als E-Rezept auf Ihre Karte?'], ['wahl', [['E-Rezept auf die Karte', 'rezept3'], ['Abholen in der Praxis', 'rezept3']]]],
        rezept3: [['bot', 'Danke, Ihre Anfrage ist vollständig. Die Praxis prüft sie und meldet sich, sobald das Rezept bereitliegt.'], ['karte', ['Folgerezept', 'Dauermedikament wie im letzten Quartal · E-Rezept oder Abholung', 'Ärztliche Prüfung in der Praxis', 'statt drei Rückrufen eine vollständige Anfrage']]],
        zeiten: [['bot', 'Wir sind Mo–Fr 8–12 Uhr und Di + Do 15–18 Uhr für Sie da. Vom 23.12. bis 2.1. vertritt uns die Praxis in der Nachbarstraße.'], ['wahl', [['Danke!', 'ende']]]],
        sprache: [['bot', 'Ich kann Ihr Anliegen auch in Ihrer Sprache aufnehmen.'], ['wahl', [['Türkçe', 'tr'], ['العربية', 'ar'], ['English', 'en']]]],
        tr: [['bot', 'Elbette! Randevunuzu değiştirmek mi istiyorsunuz? Talebinizi ekibe Almanca olarak iletiyorum.'], ['karte', ['Anliegen auf Türkisch', 'Für das Team übersetzt: „Patient möchte den Termin verschieben“', 'Antwort an den Patienten auf Türkisch', 'weniger Missverständnisse am Telefon']]],
        ar: [['bot', 'بكل سرور! هل تريد تغيير موعدك؟ سأرسل طلبك إلى فريق العيادة باللغة الألمانية.'], ['karte', ['Anliegen auf Arabisch', 'Für das Team übersetzt: „Patient möchte den Termin verschieben“', 'Antwort an den Patienten auf Arabisch', 'weniger Missverständnisse am Telefon']]],
        en: [['bot', 'Of course! Would you like to reschedule your appointment? I will pass your request on to the team in German.'], ['karte', ['Anliegen auf Englisch', 'Für das Team übersetzt: „Patient möchte den Termin verschieben“', 'Antwort an den Patienten auf Englisch', 'weniger Missverständnisse am Telefon']]],
        notfall: [['bot', 'Das klingt dringend – dafür bin ich nicht da. Im Notfall rufen Sie bitte sofort 112 an. Außerhalb der Sprechzeiten erreichen Sie den ärztlichen Bereitschaftsdienst unter 116 117.'], ['karte', ['Kein Termin, keine Bewertung', 'Der Assistent erkennt Notfall-Wörter und verweist sofort an 112 / 116 117', 'Keine medizinische Einschätzung durch die KI', 'Sicherheit vor Bequemlichkeit']]],
      }
    },
    pflege: {
      name: 'Pflegedienst-Assistent', sub: 'Beispiel-Pflegedienst · Berlin',
      start: ['Guten Morgen! Ich bin der digitale Assistent des Pflegedienstes. Worum geht es?'],
      wahl: [['Ich bin krank (Mitarbeiter)', 'krank'], ['Frage als Angehörige/r', 'angeh'], ['Neue Pflege anfragen', 'neu'], ['Notfall beim Patienten', 'notfall']],
      wege: {
        krank: [['bot', 'Gute Besserung! Ab wann und voraussichtlich bis wann fallen Sie aus?'], ['wahl', [['Heute, voraussichtlich 3 Tage', 'krank2']]]],
        krank2: [['bot', 'Danke. Die Einsatzleitung ist sofort informiert. Bitte reichen Sie die Krankmeldung wie gewohnt nach.'], ['karte', ['Krankmeldung – sofort an die Einsatzleitung', 'Ausfall: heute + ca. 3 Tage · Tour Nord betroffen', 'Benachrichtigung um 05:52 Uhr, nicht erst um 8', 'Umplanung entscheidet die Einsatzleitung']]],
        angeh: [['bot', 'Gern. Geht es um einen Besuchstermin, eine Rückfrage oder eine Änderung?'], ['wahl', [['Besuch morgen später möglich?', 'angeh2']]]],
        angeh2: [['bot', 'Ich gebe Ihre Frage an die Pflegedienstleitung weiter. Sie bekommen heute noch eine Rückmeldung.'], ['karte', ['Angehörigen-Anfrage', 'Wunsch: Besuch morgen später · Rückruf erbeten', 'Liegt sortiert in der Liste statt auf einem Zettel', 'Antwort gibt das Büro']]],
        neu: [['bot', 'Schön, dass Sie an uns denken. Für wen und in welchem Bezirk wird Pflege gesucht?'], ['wahl', [['Für meine Mutter, Berlin-Wedding', 'neu2']]]],
        neu2: [['bot', 'Danke! Ist bereits ein Pflegegrad vorhanden?'], ['wahl', [['Ja, Pflegegrad 2', 'neu3'], ['Noch nicht beantragt', 'neu3']]]],
        neu3: [['bot', 'Perfekt, die Anfrage ist bei der Pflegedienstleitung. Sie meldet sich für ein Erstgespräch.'], ['karte', ['Neuanfrage Pflege', 'Bezirk Wedding · Pflegegrad-Status erfasst', 'Kapazität prüft die PDL', 'keine Anfrage geht im Postfach verloren']]],
        notfall: [['bot', 'Im Notfall rufen Sie bitte sofort 112 an. Dieser Chat ist nicht für Notfälle gedacht und wird nicht durchgehend gelesen.'], ['karte', ['Notfall-Hinweis', 'Notfall-Wörter führen sofort zu 112', 'Keine medizinische Einschätzung durch die KI', 'Sicherheit vor Bequemlichkeit']]],
      }
    }
  };
  var CSS = ''
    + '.kd{max-width:380px;margin:0 auto;background:#0e2340;border-radius:30px;padding:12px;box-shadow:0 24px 60px rgba(19,46,80,.28);font-family:Barlow,system-ui,sans-serif}'
    + '.kd-in{background:#f4f7f7;border-radius:22px;overflow:hidden;display:flex;flex-direction:column;height:560px}'
    + '.kd-top{background:#132e50;color:#fff;padding:14px 16px;display:flex;gap:10px;align-items:center}'
    + '.kd-av{width:36px;height:36px;border-radius:50%;background:#58d0bd;color:#0e2340;display:flex;align-items:center;justify-content:center;font-weight:800}'
    + '.kd-top b{display:block;font-size:15px}.kd-top small{color:rgba(255,255,255,.7);font-size:12px}'
    + '.kd-ki{background:#e8f8f5;color:#177567;font-size:12px;padding:7px 14px;border-bottom:1px solid #d6eeea}'
    + '.kd-log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:8px}'
    + '.kd-m{max-width:84%;padding:9px 12px;border-radius:14px;font-size:14.5px;line-height:1.45;animation:kdIn .25s ease both}'
    + '.kd-b{background:#fff;color:#1a2a2a;border:1px solid #e0eaea;border-bottom-left-radius:4px;align-self:flex-start}'
    + '.kd-u{background:#58d0bd;color:#0e2340;border-bottom-right-radius:4px;align-self:flex-end;font-weight:600}'
    + '.kd-m[dir=rtl]{text-align:right}'
    + '.kd-k{align-self:stretch;background:#fff;border:2px solid #58d0bd;border-radius:14px;padding:10px 12px;font-size:13.5px;line-height:1.45;animation:kdIn .3s ease both}'
    + '.kd-k em{font-style:normal;display:block;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#177567;font-weight:700;margin-bottom:2px}'
    + '.kd-k b{display:block;color:#132e50;font-size:14.5px}.kd-k span{display:block;color:#5a7070}'
    + '.kd-w{display:flex;flex-wrap:wrap;gap:6px;padding:10px 12px 14px;background:#fff;border-top:1px solid #e0eaea;min-height:60px}'
    + '.kd-w button{border:1.5px solid #58d0bd;background:#fff;color:#132e50;border-radius:18px;padding:8px 12px;font:600 13.5px Barlow,system-ui,sans-serif;cursor:pointer}'
    + '.kd-w button:hover,.kd-w button:focus-visible{background:#e8f8f5;outline:none}'
    + '.kd-tip{display:flex;gap:4px;padding:10px 12px;background:#fff;border:1px solid #e0eaea;border-radius:14px;align-self:flex-start}.kd-tip i{width:6px;height:6px;border-radius:50%;background:#8fa4c0;animation:kdT 1s infinite}.kd-tip i:nth-child(2){animation-delay:.15s}.kd-tip i:nth-child(3){animation-delay:.3s}'
    + '.kd-note{max-width:380px;margin:.7rem auto 0;text-align:center;font-size:12.5px;color:#5a7070}'
    + '@keyframes kdIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@keyframes kdT{50%{opacity:.3}}'
    + '@media(prefers-reduced-motion:reduce){.kd-m,.kd-k{animation:none}.kd-tip i{animation:none}}';
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }

  function demo(root) {
    var sz = SZ[root.getAttribute('data-ki-demo')] || SZ.praxis;
    var schnell = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var box = el('div', 'kd'), inn = el('div', 'kd-in'), top = el('div', 'kd-top');
    top.appendChild(el('div', 'kd-av', 'M')); var tt = el('div'); tt.appendChild(el('b', '', sz.name)); tt.appendChild(el('small', '', sz.sub)); top.appendChild(tt);
    var ki = el('div', 'kd-ki', 'Hinweis: Sie schreiben mit einem digitalen Assistenten (KI). Keine medizinische Beratung – im Notfall 112.');
    var log = el('div', 'kd-log'); log.setAttribute('role', 'log'); log.setAttribute('aria-live', 'polite');
    var wahl = el('div', 'kd-w'); wahl.setAttribute('aria-label', 'Antwort auswählen');
    inn.appendChild(top); inn.appendChild(ki); inn.appendChild(log); inn.appendChild(wahl); box.appendChild(inn);
    root.innerHTML = ''; root.appendChild(box);
    var note = el('p', 'kd-note', 'Vorführung mit Beispieltexten – es werden keine Daten gesendet. So sieht es für Patienten bzw. Angehörige aus; die türkis umrandeten Karten zeigen, was bei Ihrem Team ankommt.');
    root.appendChild(note);
    function unten() { log.scrollTop = log.scrollHeight; }
    function bot(text, weiter) {
      var tip = el('div', 'kd-tip'); tip.appendChild(el('i')); tip.appendChild(el('i')); tip.appendChild(el('i')); log.appendChild(tip); unten();
      setTimeout(function () { tip.remove(); var m = el('div', 'kd-m kd-b', text); if (/[؀-ۿ]/.test(text)) m.setAttribute('dir', 'rtl'); log.appendChild(m); unten(); weiter && weiter(); }, schnell ? 0 : 650);
    }
    function knoepfe(liste) {
      wahl.innerHTML = '';
      liste.forEach(function (w) {
        var b = el('button', '', w[0]); b.type = 'button';
        b.addEventListener('click', function () { wahl.innerHTML = ''; log.appendChild(el('div', 'kd-m kd-u', w[0])); unten(); geh(w[1]); });
        wahl.appendChild(b);
      });
    }
    function geh(schritt) {
      if (schritt === 'ende' || schritt === 'neu') { if (schritt === 'neu') { log.innerHTML = ''; } start(); return; }
      var teile = (sz.wege[schritt] || []).slice();
      (function weiter() {
        var t = teile.shift(); if (!t) return;
        if (t[0] === 'bot') bot(t[1], weiter);
        else if (t[0] === 'wahl') knoepfe(t[1]);
        else if (t[0] === 'karte') {
          setTimeout(function () {
            var k = el('div', 'kd-k'); k.appendChild(el('em', '', 'So kommt es bei Ihrem Team an'));
            k.appendChild(el('b', '', t[1][0])); t[1].slice(1).forEach(function (z) { k.appendChild(el('span', '', z)); });
            log.appendChild(k); unten(); knoepfe([['Anderes Anliegen ausprobieren', 'neu']]);
          }, schnell ? 0 : 350);
        }
      })();
    }
    function start() { bot(sz.start[0], function () { knoepfe(sz.wahl); }); }
    start();
  }
  function los() {
    if (!document.getElementById('kd-css')) { var s = el('style'); s.id = 'kd-css'; s.textContent = CSS; document.head.appendChild(s); }
    document.querySelectorAll('[data-ki-demo]').forEach(demo);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', los); else los();
})();
