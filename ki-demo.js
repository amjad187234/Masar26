/*
 * Masar – Vorführungen digitaler Assistenten für Praxen und Pflegedienste.
 * Reine Demo im Browser: keine KI-Anfrage, keine Daten werden gesendet oder gespeichert.
 *   <div data-ki-demo="praxis|pflege"></div>          Chat-/WhatsApp-Assistent (Knöpfe + freie Eingabe)
 *   <div data-ki-bausteine="praxis|pflege"></div>     weitere Bausteine: Online-Termin, Postfach, Wissens-Assistent
 *   <script src="/ki-demo.js" defer></script>
 */
(function () {
  'use strict';
  var RUHIG = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function warte(ms, f) { setTimeout(f, RUHIG ? 0 : ms); }

  // ─── Chat-Szenarien ───────────────────────────────────────────────
  var NOT_PRAXIS = [['bot', 'Das klingt dringend – dafür bin ich nicht da. Im Notfall rufen Sie bitte sofort 112 an. Außerhalb der Sprechzeiten erreichen Sie den ärztlichen Bereitschaftsdienst unter 116 117.'],
    ['karte', ['Notfall erkannt – kein Termin, keine Bewertung', 'Hinweis auf 112 / 116 117 sofort ausgegeben', 'Der Assistent schätzt keine Beschwerden ein', 'Sicherheit vor Bequemlichkeit']]];
  var SZ = {
    praxis: {
      name: 'Praxis-Assistent', sub: 'Beispielpraxis · Berlin · antwortet sofort',
      start: 'Guten Tag! Ich bin der digitale Assistent der Praxis. Wählen Sie ein Anliegen oder schreiben Sie einfach.',
      wahl: [['Neuen Termin buchen', 'neu'], ['Termin verschieben', 'termin'], ['Folgerezept', 'rezept'], ['Ist mein Befund da?', 'befund'], ['Öffnungszeiten', 'zeiten'], ['Andere Sprache', 'sprache']],
      ph: 'z. B. „Kann ich meinen Termin verschieben?“',
      erkennen: [[/notfall|schmerz|atemnot|luftnot|blut|bewusstlos|brust|herz|ohnmacht|ağrı|acil|ألم|طوارئ|pain|emergency/i, 'notfall'],
        [/[؀-ۿ]/, 'ar'], [/[ğşı]|randevu|merhaba|ilaç/i, 'tr'], [/\b(appointment|hello|hi|prescription|english|opening)\b/i, 'en'],
        [/befund|ergebnis|labor|blutwert/i, 'befund'], [/rezept|medikament|tablette|überweisung/i, 'rezept'],
        [/verschieb|absag|umbuch|später|anderen termin|kann nicht/i, 'termin'], [/neu|buchen|termin/i, 'neu'],
        [/öffnung|offen|geöffnet|sprechzeit|urlaub|wann|zeiten|adresse|anfahrt/i, 'zeiten']],
      wege: {
        neu: [['bot', 'Gern. Welche Art von Termin brauchen Sie?'], ['wahl', [['Vorsorge / Check-up', 'neu2'], ['Impfung', 'neu2'], ['Kontrolltermin', 'neu2']]]],
        neu2: [['bot', 'Diese Zeiten sind frei:'], ['wahl', [['Mo 09:30', 'neu3'], ['Di 11:00', 'neu3'], ['Do 16:15', 'neu3']]]],
        neu3: [['bot', 'Erledigt! Sie bekommen eine Bestätigung und am Vortag eine Erinnerung. Absagen geht mit einer Antwort auf die Erinnerung.'],
          ['karte', ['Neuer Termin – direkt im Kalender', 'Terminart per Auswahl, kein Freitext zu Beschwerden', 'Erinnerung am Vortag (mit Einwilligung)', 'Absage mit einer Antwort – der Platz wird wieder frei']]],
        termin: [['bot', 'Gern. An welchem Tag ist Ihr bisheriger Termin?'], ['wahl', [['Donnerstag, 14:30 Uhr', 'termin2']]]],
        termin2: [['bot', 'Danke. Wann würde es Ihnen besser passen?'], ['wahl', [['Nächste Woche vormittags', 'termin3'], ['So bald wie möglich', 'termin3']]]],
        termin3: [['bot', 'Ich gebe Ihren Wunsch an das Praxisteam weiter. Sie bekommen den neuen Termin als Bestätigung per SMS.'],
          ['karte', ['Terminverschiebung', 'Bisher: Do 14:30 · Wunsch: nächste Woche vormittags', 'Alter Termin wird freigegeben', 'Team bestätigt mit einem Klick']]],
        rezept: [['bot', 'Für welches Medikament? Am besten so, wie es auf der Packung steht.'], ['wahl', [['Dauermedikament wie im letzten Quartal', 'rezept2']]]],
        rezept2: [['bot', 'Möchten Sie das Rezept abholen oder als E-Rezept auf Ihre Karte?'], ['wahl', [['E-Rezept auf die Karte', 'rezept3'], ['Abholen in der Praxis', 'rezept3']]]],
        rezept3: [['bot', 'Danke, Ihre Anfrage ist vollständig. Die Praxis prüft sie und meldet sich, sobald das Rezept bereitliegt.'],
          ['karte', ['Folgerezept', 'Dauermedikament wie im letzten Quartal · E-Rezept oder Abholung', 'Ärztliche Prüfung in der Praxis', 'eine vollständige Anfrage statt drei Rückrufen']]],
        befund: [['bot', 'Aus Datenschutzgründen nenne ich keine Befunde. Ich bitte das Praxisteam um einen Rückruf. Wann sind Sie am besten erreichbar?'], ['wahl', [['Heute ab 15 Uhr', 'befund2'], ['Morgen vormittags', 'befund2']]]],
        befund2: [['bot', 'Notiert. Die Praxis ruft Sie zurück.'],
          ['karte', ['Rückruf-Wunsch zum Befund', 'Erreichbar: wie angegeben · keine Befunde im Chat', 'Rückruf durch Ärztin / Arzt oder MFA', 'Vertrauliches bleibt im Gespräch']]],
        zeiten: [['bot', 'Wir sind Mo–Fr 8–12 Uhr und Di + Do 15–18 Uhr für Sie da. Vom 23.12. bis 2.1. vertritt uns die Praxis in der Nachbarstraße. Die Anfahrt: U-Bahn bis Seestraße, dann 3 Minuten zu Fuß.'], ['wahl', [['Danke!', 'neu-start']]]],
        sprache: [['bot', 'Ich kann Ihr Anliegen auch in Ihrer Sprache aufnehmen. Schreiben Sie einfach los – oder wählen Sie:'], ['wahl', [['Türkçe', 'tr'], ['العربية', 'ar'], ['English', 'en']]]],
        tr: [['bot', 'Elbette! Randevunuzu değiştirmek mi istiyorsunuz? Talebinizi ekibe Almanca olarak iletiyorum.'], ['karte', ['Anliegen auf Türkisch', 'Für das Team übersetzt: „Patient möchte den Termin verschieben“', 'Antwort an den Patienten auf Türkisch', 'weniger Missverständnisse']]],
        ar: [['bot', 'بكل سرور! هل تريد تغيير موعدك؟ سأرسل طلبك إلى فريق العيادة باللغة الألمانية.'], ['karte', ['Anliegen auf Arabisch', 'Für das Team übersetzt: „Patient möchte den Termin verschieben“', 'Antwort an den Patienten auf Arabisch', 'weniger Missverständnisse']]],
        en: [['bot', 'Of course! Would you like to reschedule your appointment? I will pass your request on to the team in German.'], ['karte', ['Anliegen auf Englisch', 'Für das Team übersetzt: „Patient möchte den Termin verschieben“', 'Antwort an den Patienten auf Englisch', 'weniger Missverständnisse']]],
        notfall: NOT_PRAXIS
      }
    },
    pflege: {
      name: 'Pflegedienst-Assistent', sub: 'Beispiel-Pflegedienst · Berlin · antwortet sofort',
      start: 'Guten Morgen! Ich bin der digitale Assistent des Pflegedienstes. Wählen Sie ein Anliegen oder schreiben Sie einfach.',
      wahl: [['Ich bin krank (Mitarbeiter)', 'krank'], ['Dienst tauschen', 'tausch'], ['Frage als Angehörige/r', 'angeh'], ['Neue Pflege anfragen', 'neu'], ['Andere Sprache', 'sprache']],
      ph: 'z. B. „Ich bin heute krank“',
      erkennen: [[/notfall|gestürzt|sturz|bewusstlos|atemnot|blut|schmerz|acil|طوارئ|ألم|emergency/i, 'notfall'],
        [/[؀-ۿ]/, 'ar'], [/[ğşı]|merhaba|bakım|hasta/i, 'tr'], [/\b(hello|hi|care|english|sick)\b/i, 'en'],
        [/krank|ausfall|fieber|arbeitsunfähig|au\b/i, 'krank'], [/tausch|schicht|dienstplan|frei nehmen/i, 'tausch'],
        [/besuch|mutter|vater|oma|opa|angehörig|rückruf/i, 'angeh'], [/pflege|pflegegrad|anfrage|neu|aufnehm/i, 'neu']],
      wege: {
        krank: [['bot', 'Gute Besserung! Ab wann und voraussichtlich bis wann fallen Sie aus?'], ['wahl', [['Heute, voraussichtlich 3 Tage', 'krank2'], ['Ab morgen, 1 Woche', 'krank2']]]],
        krank2: [['bot', 'Danke. Die Einsatzleitung ist sofort informiert. Bitte reichen Sie die Krankmeldung wie gewohnt nach.'],
          ['karte', ['Krankmeldung – sofort an die Einsatzleitung', 'Ausfall wie angegeben · betroffene Tour aus dem Dienstplan', 'Benachrichtigung sofort, nicht erst um 8 Uhr', 'Umplanung entscheidet die Einsatzleitung']]],
        tausch: [['bot', 'Welchen Dienst möchten Sie tauschen?'], ['wahl', [['Samstag Frühdienst', 'tausch2']]]],
        tausch2: [['bot', 'Danke. Ich frage die Einsatzleitung, ob ein Tausch möglich ist, und melde mich.'],
          ['karte', ['Tauschwunsch', 'Sa Frühdienst · Wunsch: Sonntag', 'Liegt sortiert bei der Einsatzleitung', 'Freigabe durch die Einsatzleitung']]],
        angeh: [['bot', 'Gern. Geht es um einen Besuchstermin, eine Rückfrage oder eine Änderung?'], ['wahl', [['Besuch morgen später möglich?', 'angeh2'], ['Bitte um Rückruf der PDL', 'angeh2']]]],
        angeh2: [['bot', 'Ich gebe Ihre Frage an die Pflegedienstleitung weiter. Sie bekommen heute noch eine Rückmeldung. Auskünfte zur Pflege gibt das Team persönlich.'],
          ['karte', ['Angehörigen-Anfrage', 'Anliegen wie angegeben · Rückruf erbeten', 'Auskunft nur an Berechtigte (Schweigepflicht)', 'Antwort gibt das Büro']]],
        neu: [['bot', 'Schön, dass Sie an uns denken. Für wen und in welchem Bezirk wird Pflege gesucht?'], ['wahl', [['Für meine Mutter, Berlin-Wedding', 'neu2']]]],
        neu2: [['bot', 'Danke! Ist bereits ein Pflegegrad vorhanden?'], ['wahl', [['Ja, Pflegegrad 2', 'neu3'], ['Noch nicht beantragt', 'neu3']]]],
        neu3: [['bot', 'Perfekt, die Anfrage ist bei der Pflegedienstleitung. Sie meldet sich für ein Erstgespräch.'],
          ['karte', ['Neuanfrage Pflege', 'Bezirk und Pflegegrad-Status erfasst', 'Kapazität prüft die PDL', 'keine Anfrage geht im Postfach verloren']]],
        sprache: [['bot', 'Ich kann Ihr Anliegen auch in Ihrer Sprache aufnehmen. Schreiben Sie einfach los – oder wählen Sie:'], ['wahl', [['Türkçe', 'tr'], ['العربية', 'ar'], ['English', 'en']]]],
        tr: [['bot', 'Elbette! Annenizin bakımıyla ilgili bir sorunuz mu var? Talebinizi ekibe Almanca olarak iletiyorum.'], ['karte', ['Anliegen auf Türkisch', 'Für das Team übersetzt: „Angehörige bittet um Rückruf“', 'Antwort auf Türkisch', 'weniger Missverständnisse']]],
        ar: [['bot', 'بكل سرور! هل لديك سؤال عن رعاية والدتك؟ سأرسل طلبك إلى الفريق باللغة الألمانية.'], ['karte', ['Anliegen auf Arabisch', 'Für das Team übersetzt: „Angehörige bittet um Rückruf“', 'Antwort auf Arabisch', 'weniger Missverständnisse']]],
        en: [['bot', 'Of course! Do you have a question about your relative’s care? I will pass it on to the team in German.'], ['karte', ['Anliegen auf Englisch', 'Für das Team übersetzt: „Angehörige bittet um Rückruf“', 'Antwort auf Englisch', 'weniger Missverständnisse']]],
        notfall: [['bot', 'Im Notfall rufen Sie bitte sofort 112 an. Dieser Chat ist nicht für Notfälle gedacht.'],
          ['karte', ['Notfall erkannt', 'Hinweis auf 112 sofort ausgegeben', 'Keine Einschätzung durch die KI', 'Sicherheit vor Bequemlichkeit']]]
      }
    }
  };

  var CSS = ''
    + '.kd{max-width:380px;width:100%;margin:0 auto;background:#0e2340;border-radius:30px;padding:10px;box-shadow:0 24px 60px rgba(0,0,0,.32);font-family:Barlow,system-ui,sans-serif;text-align:left}'
    + '.kd-in{background:#f4f7f7;border-radius:22px;overflow:hidden;display:flex;flex-direction:column;height:540px}'
    + '.kd-top{background:#132e50;color:#fff;padding:12px 14px;display:flex;gap:10px;align-items:center}'
    + '.kd-av{width:36px;height:36px;border-radius:50%;background:#58d0bd;color:#0e2340;display:flex;align-items:center;justify-content:center;font-weight:800;flex:0 0 auto}'
    + '.kd-top b{display:block;font-size:15px}.kd-top small{color:rgba(255,255,255,.72);font-size:12px}'
    + '.kd-ki{background:#e8f8f5;color:#177567;font-size:12px;line-height:1.4;padding:7px 14px;border-bottom:1px solid #d6eeea}'
    + '.kd-log{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;scroll-behavior:smooth}'
    + '.kd-m{max-width:86%;padding:9px 12px;border-radius:14px;font-size:14.5px;line-height:1.45;animation:kdIn .25s ease both;word-wrap:break-word}'
    + '.kd-b{background:#fff;color:#1a2a2a;border:1px solid #e0eaea;border-bottom-left-radius:4px;align-self:flex-start}'
    + '.kd-u{background:#58d0bd;color:#0e2340;border-bottom-right-radius:4px;align-self:flex-end;font-weight:600}'
    + '.kd-m[dir=rtl]{text-align:right}'
    + '.kd-k{align-self:stretch;background:#fff;border:2px solid #58d0bd;border-radius:14px;padding:10px 12px;font-size:13.5px;line-height:1.45;animation:kdIn .3s ease both}'
    + '.kd-k em{font-style:normal;display:block;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#177567;font-weight:700;margin-bottom:2px}'
    + '.kd-k b{display:block;color:#132e50;font-size:14.5px}.kd-k span{display:block;color:#5a7070}'
    + '.kd-w{display:flex;flex-wrap:wrap;gap:6px;padding:8px 10px 4px;background:#fff;border-top:1px solid #e0eaea;max-height:118px;overflow-y:auto}'
    + '.kd-w button,.kb-chip{border:1.5px solid #58d0bd;background:#fff;color:#132e50;border-radius:18px;padding:7px 11px;font:600 13.5px Barlow,system-ui,sans-serif;cursor:pointer}'
    + '.kd-w button:hover,.kd-w button:focus-visible,.kb-chip:hover,.kb-chip:focus-visible{background:#e8f8f5;outline:none}'
    + '.kd-f{display:flex;gap:6px;padding:6px 10px 10px;background:#fff}.kd-f input{flex:1;min-width:0;border:1.5px solid #e0eaea;border-radius:20px;padding:9px 12px;font:15px Barlow,system-ui,sans-serif;color:#132e50}'
    + '.kd-f input:focus{outline:none;border-color:#58d0bd}.kd-f button{border:0;background:#58d0bd;color:#0e2340;border-radius:20px;padding:0 14px;font:700 14px Barlow,system-ui,sans-serif;cursor:pointer}'
    + '.kd-tip{display:flex;gap:4px;padding:10px 12px;background:#fff;border:1px solid #e0eaea;border-radius:14px;align-self:flex-start}.kd-tip i{width:6px;height:6px;border-radius:50%;background:#8fa4c0;animation:kdT 1s infinite}.kd-tip i:nth-child(2){animation-delay:.15s}.kd-tip i:nth-child(3){animation-delay:.3s}'
    + '.kd-note{max-width:380px;margin:.7rem auto 0;text-align:center;font-size:12.5px;line-height:1.5;color:inherit;opacity:.75}'
    // Bausteine
    + '.kb{max-width:980px;margin:0 auto;font-family:Barlow,system-ui,sans-serif}'
    + '.kb-tabs{display:flex;gap:.5rem;flex-wrap:wrap;justify-content:center;margin-bottom:1.2rem}'
    + '.kb-tab{border:1.5px solid #d6e2e2;background:#fff;color:#132e50;border-radius:999px;padding:10px 18px;font:700 14.5px Barlow,system-ui,sans-serif;cursor:pointer}'
    + '.kb-tab[aria-selected=true]{background:#132e50;border-color:#132e50;color:#fff}'
    + '.kb-p{background:#fff;border:1px solid #e0eaea;border-radius:16px;padding:1.3rem;box-shadow:0 10px 30px rgba(19,46,80,.07);display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:1.3rem}'
    + '.kb-p h3{font:900 1.3rem/1.1 "Barlow Condensed",sans-serif;text-transform:uppercase;color:#132e50;margin:0 0 .4rem}.kb-p p.kb-sub{color:#5a7070;font-size:14.5px;margin:0 0 1rem;line-height:1.5}'
    + '.kb-step{font:700 12px Barlow,sans-serif;letter-spacing:1px;text-transform:uppercase;color:#177567;margin:.8rem 0 .4rem}'
    + '.kb-row{display:flex;flex-wrap:wrap;gap:6px}.kb-chip[aria-pressed=true]{background:#58d0bd;color:#0e2340}'
    + '.kb-go{margin-top:1rem;border:0;background:#132e50;color:#fff;border-radius:8px;padding:11px 18px;font:700 14.5px Barlow,sans-serif;cursor:pointer}.kb-go[disabled]{opacity:.4;cursor:default}'
    + '.kb-out{background:#f4f7f7;border-radius:12px;padding:1rem;font-size:14px;line-height:1.5;color:#1a2a2a;min-height:200px}'
    + '.kb-out .kb-lbl{font:700 11px Barlow,sans-serif;letter-spacing:1px;text-transform:uppercase;color:#177567;display:block;margin-bottom:.4rem}'
    + '.kb-sms{background:#fff;border:1px solid #e0eaea;border-radius:12px 12px 12px 4px;padding:.7rem .9rem;margin:.4rem 0 .8rem;animation:kdIn .3s ease both}'
    + '.kb-mail{display:flex;gap:.6rem;align-items:flex-start;background:#fff;border:1px solid #e0eaea;border-radius:10px;padding:.6rem .75rem;margin-bottom:.45rem;cursor:pointer;text-align:left;width:100%;font:inherit;color:inherit}'
    + '.kb-mail b{display:block;color:#132e50;font-size:14px}.kb-mail small{color:#5a7070;font-size:13px}'
    + '.kb-tag{flex:0 0 84px;font:700 11px Barlow,sans-serif;letter-spacing:.5px;text-transform:uppercase;border-radius:6px;padding:3px 7px;background:#e0eaea;color:#5a7070;min-width:74px;text-align:center;transition:background .3s,color .3s}'
    + '.kb-tag.on{background:#58d0bd;color:#0e2340}.kb-tag.hoch{background:#132e50;color:#fff}.kb-tag.aus{background:#f4f7f7;color:#8fa4c0}'
    + '.kb-draft{background:#fff;border:2px solid #58d0bd;border-radius:12px;padding:.8rem .9rem;white-space:pre-line;animation:kdIn .3s ease both}'
    + '.kb-ok{display:inline-block;margin-top:.6rem;border:0;background:#58d0bd;color:#0e2340;border-radius:8px;padding:8px 14px;font:700 13.5px Barlow,sans-serif;cursor:pointer}'
    + '.kb-src{display:block;margin-top:.5rem;font-size:12.5px;color:#177567;font-weight:600}'
    + '@media(max-width:760px){.kb-p{grid-template-columns:1fr}}'
    + '@keyframes kdIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@keyframes kdT{50%{opacity:.3}}'
    + '@media(prefers-reduced-motion:reduce){.kd-m,.kd-k,.kb-sms,.kb-draft{animation:none}.kd-tip i{animation:none}}';

  // ─── Chat ─────────────────────────────────────────────────────────
  function chat(root) {
    var sz = SZ[root.getAttribute('data-ki-demo')] || SZ.praxis;
    var box = el('div', 'kd'), inn = el('div', 'kd-in'), top = el('div', 'kd-top');
    top.appendChild(el('div', 'kd-av', 'M')); var tt = el('div'); tt.appendChild(el('b', '', sz.name)); tt.appendChild(el('small', '', sz.sub)); top.appendChild(tt);
    var ki = el('div', 'kd-ki', 'Hinweis: Sie schreiben mit einem digitalen Assistenten (KI). Keine medizinische Beratung – im Notfall 112.');
    var log = el('div', 'kd-log'); log.setAttribute('role', 'log'); log.setAttribute('aria-live', 'polite'); log.setAttribute('aria-label', 'Gesprächsverlauf');
    var wahl = el('div', 'kd-w'); wahl.setAttribute('role', 'group'); wahl.setAttribute('aria-label', 'Antwort auswählen');
    var form = el('form', 'kd-f'); var inp = el('input'); inp.type = 'text'; inp.placeholder = sz.ph; inp.setAttribute('aria-label', 'Nachricht schreiben'); inp.maxLength = 160; inp.autocomplete = 'off';
    var send = el('button', '', 'Senden'); send.type = 'submit'; form.appendChild(inp); form.appendChild(send);
    inn.appendChild(top); inn.appendChild(ki); inn.appendChild(log); inn.appendChild(wahl); inn.appendChild(form); box.appendChild(inn);
    root.innerHTML = ''; root.appendChild(box);
    root.appendChild(el('p', 'kd-note', 'Vorführung mit Beispieltexten – es werden keine Daten gesendet. Die türkis umrandeten Karten zeigen, was bei Ihrem Team ankommt.'));
    function unten() { log.scrollTop = log.scrollHeight; }
    function bot(text, weiter) {
      var tip = el('div', 'kd-tip'); tip.appendChild(el('i')); tip.appendChild(el('i')); tip.appendChild(el('i')); log.appendChild(tip); unten();
      warte(600, function () { tip.remove(); var m = el('div', 'kd-m kd-b', text); if (/[؀-ۿ]/.test(text)) m.setAttribute('dir', 'rtl'); log.appendChild(m); unten(); weiter && weiter(); });
    }
    function nutzer(t) { var m = el('div', 'kd-m kd-u', t); if (/[؀-ۿ]/.test(t)) m.setAttribute('dir', 'rtl'); log.appendChild(m); unten(); }
    function knoepfe(liste) {
      wahl.innerHTML = '';
      liste.forEach(function (w) {
        var b = el('button', '', w[0]); b.type = 'button';
        b.addEventListener('click', function () { wahl.innerHTML = ''; nutzer(w[0]); geh(w[1]); });
        wahl.appendChild(b);
      });
    }
    function geh(schritt) {
      if (schritt === 'neu-start') { start(); return; }
      if (schritt === 'reset') { log.innerHTML = ''; start(); return; }
      var teile = (sz.wege[schritt] || []).slice();
      (function weiter() {
        var t = teile.shift(); if (!t) return;
        if (t[0] === 'bot') bot(t[1], weiter);
        else if (t[0] === 'wahl') knoepfe(t[1]);
        else if (t[0] === 'karte') warte(300, function () {
          var k = el('div', 'kd-k'); k.appendChild(el('em', '', 'So kommt es bei Ihrem Team an'));
          k.appendChild(el('b', '', t[1][0])); t[1].slice(1).forEach(function (z) { k.appendChild(el('span', '', z)); });
          log.appendChild(k); unten(); knoepfe([['Anderes Anliegen ausprobieren', 'reset']]);
        });
      })();
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault(); var t = inp.value.trim(); if (!t) return; inp.value = ''; wahl.innerHTML = ''; nutzer(t);
      for (var i = 0; i < sz.erkennen.length; i++) if (sz.erkennen[i][0].test(t)) { geh(sz.erkennen[i][1]); return; }
      bot('Das habe ich nicht sicher verstanden. In einer echten Einrichtung würde ich jetzt an das Team weitergeben – hier können Sie eines dieser Anliegen ausprobieren:', function () { knoepfe(sz.wahl); });
    });
    function start() { bot(sz.start, function () { knoepfe(sz.wahl); }); }
    start();
  }

  // ─── Weitere Bausteine ────────────────────────────────────────────
  var B = {
    praxis: {
      termin: { arten: ['Vorsorge / Check-up', 'Impfung', 'Kontrolltermin', 'Erstgespräch'], wer: 'Patienten', ort: 'Beispielpraxis, Müllerstraße' },
      mails: [
        ['Hr. K.', 'Folgerezept für März?', 'Rezept', 'Guten Tag Herr K.,\nvielen Dank für Ihre Anfrage. Wir prüfen das Folgerezept und melden uns, sobald es bereitliegt – als E-Rezept auf Ihrer Karte oder zur Abholung.\nFreundliche Grüße, Ihr Praxisteam'],
        ['Praxis Dr. S.', 'Überweisung Fr. M. – Rückfrage', 'Praxis', 'Sehr geehrte Frau Dr. S.,\nvielen Dank. Wir haben Ihre Rückfrage erhalten und melden uns heute bis 16 Uhr telefonisch.\nMit freundlichen Grüßen'],
        ['Fr. A.', 'Termin morgen absagen', 'Termin', 'Guten Tag Frau A.,\nIhr Termin morgen ist abgesagt. Möchten Sie einen neuen Termin? Freie Zeiten finden Sie hier: [Link]\nFreundliche Grüße, Ihr Praxisteam'],
        ['L. Y.', 'Bewerbung als MFA (Teilzeit)', 'Bewerbung', 'Guten Tag,\nvielen Dank für Ihre Bewerbung als MFA. Wir haben Ihre Unterlagen erhalten und melden uns innerhalb von zwei Wochen.\nFreundliche Grüße'],
        ['Praxisbedarf-Shop', 'Neue Angebote im November', 'Werbung', null]
      ],
      wissen: [['Wer hat Samstag Telefondienst?', 'Laut Dienstplan November: Frau B. (8–12 Uhr). Vertretung: Herr T.', 'Dienstplan November, Woche 46'],
        ['Wie läuft die Urlaubsvertretung?', 'Vom 23.12. bis 2.1. vertritt uns Praxis Dr. L. (Nachbarstraße 12). Hinweis auf Ansage und Website ist hinterlegt.', 'Praxishandbuch, Abschnitt 2.4'],
        ['Was kommt in die Willkommensmappe für Neupatienten?', 'Anamnesebogen, Datenschutzinfo, Hinweis zu Online-Terminen und Rezeptanfragen, Notfallnummern 112 und 116 117.', 'QM-Handbuch, Checkliste Empfang']]
    },
    pflege: {
      termin: { arten: ['Erstgespräch Pflege', 'Beratungsbesuch (§ 37.3)', 'Rückruf der PDL'], wer: 'Angehörige', ort: 'Beispiel-Pflegedienst, Wedding' },
      mails: [
        ['Pflegekasse', 'Rückfrage Kostenvoranschlag Fr. M.', 'Kasse', 'Sehr geehrte Damen und Herren,\nvielen Dank für Ihre Rückfrage. Die gewünschten Unterlagen senden wir Ihnen bis Freitag zu.\nMit freundlichen Grüßen'],
        ['Hausarztpraxis', 'Neue Verordnung Hr. P.', 'Praxis', 'Guten Tag,\nvielen Dank, die Verordnung ist eingegangen und liegt bei der Pflegedienstleitung.\nFreundliche Grüße'],
        ['Fr. S. (Tochter)', 'Bitte um Rückruf wegen Besuchszeit', 'Angehörige', 'Guten Tag Frau S.,\nvielen Dank für Ihre Nachricht. Unsere Pflegedienstleitung ruft Sie heute zwischen 14 und 16 Uhr zurück.\nFreundliche Grüße'],
        ['M. D.', 'Bewerbung Pflegefachkraft (Vollzeit)', 'Bewerbung', 'Guten Tag,\nvielen Dank für Ihre Bewerbung. Wir haben Ihre Unterlagen erhalten und melden uns innerhalb einer Woche für ein Gespräch.\nFreundliche Grüße'],
        ['Messe-Newsletter', 'Einladung Pflegebedarf-Messe', 'Werbung', null]
      ],
      wissen: [['Wie melde ich eine Tourenänderung?', 'Änderungen bis 14 Uhr an die Einsatzleitung über die Pflegesoftware, danach telefonisch an den Bereitschaftsdienst.', 'QM-Handbuch, Abschnitt 3.2'],
        ['Was gilt bei der Schlüsselübergabe?', 'Übergabe nur mit Unterschrift im Schlüsselbuch, Aufbewahrung im Schlüsseltresor, Verlust sofort an die PDL.', 'Verfahrensanweisung Schlüssel, Stand 2026'],
        ['Wer ist diese Woche Bereitschaft?', 'Laut Bereitschaftsplan KW 46: Herr D., Vertretung Frau K.', 'Bereitschaftsplan KW 46']]
    }
  };

  function tage() {
    var out = [], d = new Date(); d.setDate(d.getDate() + 1);
    var n = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
    while (out.length < 4) { if (d.getDay() !== 0 && d.getDay() !== 6) out.push(n[d.getDay()] + ' ' + ('0' + d.getDate()).slice(-2) + '.' + ('0' + (d.getMonth() + 1)).slice(-2) + '.'); d.setDate(d.getDate() + 1); }
    return out;
  }
  function chips(row, liste, auf) {
    liste.forEach(function (t) {
      var b = el('button', 'kb-chip', t); b.type = 'button'; b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () { row.querySelectorAll('.kb-chip').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); }); b.setAttribute('aria-pressed', 'true'); auf(t); });
      row.appendChild(b);
    });
  }

  function panelTermin(p, cfg) {
    var l = el('div'), out = el('div', 'kb-out');
    l.appendChild(el('h3', '', 'Online-Termin mit Erinnerung'));
    l.appendChild(el('p', 'kb-sub', cfg.wer + ' wählen Terminart, Tag und Uhrzeit selbst. Bestätigung kommt sofort, die Erinnerung am Vortag – absagen geht mit einer Antwort.'));
    var wahl = {}, go = el('button', 'kb-go', 'Termin buchen'); go.type = 'button'; go.disabled = true;
    function pruef() { go.disabled = !(wahl.art && wahl.tag && wahl.zeit); }
    [['1 · Terminart', cfg.arten, 'art'], ['2 · Tag', tage(), 'tag'], ['3 · Uhrzeit', ['09:00', '10:30', '14:00', '16:15'], 'zeit']].forEach(function (s) {
      l.appendChild(el('div', 'kb-step', s[0])); var r = el('div', 'kb-row'); chips(r, s[1], function (v) { wahl[s[2]] = v; pruef(); }); l.appendChild(r);
    });
    l.appendChild(go);
    out.appendChild(el('span', 'kb-lbl', 'Vorschau')); out.appendChild(el('p', '', 'Wählen Sie links einen Termin – hier sehen Sie, was danach passiert.'));
    go.addEventListener('click', function () {
      out.innerHTML = '';
      out.appendChild(el('span', 'kb-lbl', 'Sofort: Bestätigung'));
      out.appendChild(el('div', 'kb-sms', 'Ihr Termin „' + wahl.art + '“ am ' + wahl.tag + ' um ' + wahl.zeit + ' Uhr ist bestätigt. ' + cfg.ort + '.'));
      warte(700, function () {
        out.appendChild(el('span', 'kb-lbl', 'Am Vortag: Erinnerung'));
        out.appendChild(el('div', 'kb-sms', 'Erinnerung: morgen um ' + wahl.zeit + ' Uhr. Passt es nicht? Antworten Sie ABSAGEN – der Platz wird frei.'));
        warte(700, function () {
          out.appendChild(el('span', 'kb-lbl', 'Im Kalender Ihres Teams'));
          var k = el('div', 'kd-k'); k.appendChild(el('b', '', wahl.tag + ' · ' + wahl.zeit + ' · ' + wahl.art)); k.appendChild(el('span', '', 'automatisch eingetragen · Erinnerung mit Einwilligung · kein Freitext zu Beschwerden')); out.appendChild(k);
        });
      });
    });
    p.appendChild(l); p.appendChild(out);
  }

  function panelPost(p, mails) {
    var l = el('div'), out = el('div', 'kb-out');
    l.appendChild(el('h3', '', 'Postfach vorsortieren'));
    l.appendChild(el('p', 'kb-sub', 'Der Assistent liest neue E-Mails, ordnet sie zu und bereitet eine Antwort vor. Abgeschickt wird erst, wenn Ihr Team freigibt.'));
    var liste = el('div'), go = el('button', 'kb-go', 'Jetzt vorsortieren'); go.type = 'button';
    var tags = [];
    mails.forEach(function (m, i) {
      var b = el('button', 'kb-mail'); b.type = 'button'; var tg = el('span', 'kb-tag', 'neu'); tags.push(tg);
      var t = el('div'); t.appendChild(el('b', '', m[1])); t.appendChild(el('small', '', 'von ' + m[0]));
      b.appendChild(tg); b.appendChild(t);
      b.addEventListener('click', function () { zeigen(i); });
      liste.appendChild(b);
    });
    var sortiert = false;
    function zeigen(i) {
      var m = mails[i]; out.innerHTML = '';
      if (!sortiert) { out.appendChild(el('span', 'kb-lbl', 'Noch unsortiert')); out.appendChild(el('p', '', 'Klicken Sie zuerst auf „Jetzt vorsortieren“.')); return; }
      out.appendChild(el('span', 'kb-lbl', 'Zugeordnet: ' + m[2]));
      if (!m[3]) { out.appendChild(el('p', '', 'Werbung erkannt – aussortiert, keine Antwort nötig.')); return; }
      out.appendChild(el('div', 'kb-draft', m[3]));
      var ok = el('button', 'kb-ok', 'Entwurf freigeben'); ok.type = 'button';
      ok.addEventListener('click', function () { ok.replaceWith(el('p', 'kb-src', '✓ Nach Freigabe durch Ihr Team gesendet (Vorführung – nichts wird verschickt).')); });
      out.appendChild(ok);
    }
    go.addEventListener('click', function () {
      go.disabled = true;
      mails.forEach(function (m, i) { warte(250 * (i + 1), function () { tags[i].textContent = m[2]; tags[i].className = 'kb-tag ' + (m[3] ? (i === 1 ? 'hoch' : 'on') : 'aus'); if (i === mails.length - 1) { sortiert = true; go.textContent = 'Sortiert – E-Mail anklicken'; zeigen(0); } }); });
    });
    l.appendChild(liste); l.appendChild(go);
    out.appendChild(el('span', 'kb-lbl', 'Vorschau')); out.appendChild(el('p', '', 'Fünf neue E-Mails – mal sehen, wohin sie gehören.'));
    p.appendChild(l); p.appendChild(out);
  }

  function panelWissen(p, fragen) {
    var l = el('div'), out = el('div', 'kb-out');
    l.appendChild(el('h3', '', 'Assistent für Ihre Unterlagen'));
    l.appendChild(el('p', 'kb-sub', 'Für Ihr Team: Fragen zu Abläufen, Plänen und Checklisten – beantwortet nur aus Ihren eigenen Dokumenten, mit Quelle.'));
    l.appendChild(el('div', 'kb-step', 'Frage auswählen'));
    var r = el('div', 'kb-row');
    chips(r, fragen.map(function (f) { return f[0]; }), function (v) {
      var f = fragen.filter(function (x) { return x[0] === v; })[0]; out.innerHTML = '';
      out.appendChild(el('span', 'kb-lbl', 'Antwort'));
      var d = el('div', 'kb-draft', f[1]); d.appendChild(el('span', 'kb-src', 'Quelle: ' + f[2])); out.appendChild(d);
      out.appendChild(el('p', '', 'Findet der Assistent nichts in Ihren Unterlagen, sagt er das – er erfindet keine Antwort.'));
    });
    l.appendChild(r);
    out.appendChild(el('span', 'kb-lbl', 'Vorschau')); out.appendChild(el('p', '', 'Wählen Sie links eine Frage. Beispielunterlagen, keine echten Daten.'));
    p.appendChild(l); p.appendChild(out);
  }

  function bausteine(root) {
    var art = root.getAttribute('data-ki-bausteine') === 'pflege' ? 'pflege' : 'praxis', cfg = B[art];
    var box = el('div', 'kb'), tabs = el('div', 'kb-tabs'); tabs.setAttribute('role', 'tablist'); tabs.setAttribute('aria-label', 'Bausteine');
    var panel = el('div', 'kb-p'); panel.setAttribute('role', 'tabpanel');
    var T = [['Online-Termin', function () { panelTermin(panel, cfg.termin); }], ['Postfach vorsortieren', function () { panelPost(panel, cfg.mails); }], ['Assistent für Unterlagen', function () { panelWissen(panel, cfg.wissen); }]];
    T.forEach(function (t, i) {
      var b = el('button', 'kb-tab', t[0]); b.type = 'button'; b.setAttribute('role', 'tab'); b.id = 'kb-' + art + '-' + i; b.setAttribute('aria-selected', String(i === 0));
      b.addEventListener('click', function () { tabs.querySelectorAll('.kb-tab').forEach(function (x) { x.setAttribute('aria-selected', 'false'); }); b.setAttribute('aria-selected', 'true'); panel.setAttribute('aria-labelledby', b.id); panel.innerHTML = ''; t[1](); });
      tabs.appendChild(b);
    });
    box.appendChild(tabs); box.appendChild(panel); root.innerHTML = ''; root.appendChild(box);
    panel.setAttribute('aria-labelledby', 'kb-' + art + '-0'); T[0][1]();
    var n = el('p', 'kd-note', 'Vorführung mit Beispieldaten – es wird nichts gesendet oder gespeichert.'); n.style.maxWidth = '980px'; root.appendChild(n);
  }

  function los() {
    if (!document.getElementById('kd-css')) { var s = el('style'); s.id = 'kd-css'; s.textContent = CSS; document.head.appendChild(s); }
    document.querySelectorAll('[data-ki-demo]').forEach(chat);
    document.querySelectorAll('[data-ki-bausteine]').forEach(bausteine);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', los); else los();
})();
