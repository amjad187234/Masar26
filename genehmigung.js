/* Masar Genehmigungs-Check Werbeanlage – Fragen-Assistent ohne Preise (Einordnung, keine Rechtsberatung).
   Regeln (Stand 11/2026, Quellen auf der Seite): Berlin § 61 Abs. 1 BauO Bln (bis 1 m², an der Stätte der Leistung bis 2,5 m²),
   Gerüst/Bauzaun Berlin seit 2010 nicht verfahrensfrei; NRW § 62 Abs. 1 Nr. 12 BauO NRW (bis 1 m², Flächen zusammengerechnet;
   vorübergehend bis 2 Monate); Hamburg Anlage 2 HBauO (bis 1 m²), Kundenstopper laut Stadt grundsätzlich nicht gestattet;
   Brandenburg: vorübergehend bis 2 Monate (§ 61 BbgBO). Gehweg → Sondernutzung. Denkmal → zusätzliche Genehmigung. */
(function () {
  'use strict';
  var root = document.getElementById('gcheck');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(root.querySelectorAll(s)); };
  var WA = '491785143918';
  var A = { region: null, wo: null, flaeche: null, eigen: null, dauer: null, denkmal: null, miete: null, licht: null };
  var FRAGEN = ['region', 'wo', 'flaeche', 'eigen', 'dauer', 'denkmal', 'miete', 'licht'];
  var TXT = {
    region: { berlin: 'Berlin', nrw: 'NRW', hamburg: 'Hamburg', brandenburg: 'Brandenburg', andere: 'anderes Bundesland' },
    wo: { fassade: 'an der Fassade', fenster: 'im Schaufenster', ausleger: 'Ausleger über dem Gehweg', gehweg: 'Kundenstopper / Aufsteller auf dem Gehweg', geruest: 'Bauzaun oder Gerüst', frei: 'freistehend (Pylon, Mast)' },
    flaeche: { k1: 'bis 1 m²', k25: '1 bis 2,5 m²', g: 'über 2,5 m²' },
    eigen: { ja: 'am eigenen Geschäft', nein: 'Fremdwerbung' },
    dauer: { dauer: 'dauerhaft', kurz: 'vorübergehend, höchstens 2 Monate' },
    denkmal: { ja: 'Denkmal oder Satzungsgebiet', nein: 'kein Denkmal bekannt', unklar: 'Denkmal unklar' },
    miete: { ja: 'gemietet', nein: 'eigenes Gebäude' },
    licht: { ja: 'beleuchtet', nein: 'unbeleuchtet' }
  };
  var RATGEBER = {
    berlin: ['/blog/aussenwerbung-berlin-ratgeber.html', 'Außenwerbung in Berlin'],
    hamburg: ['/blog/werbeanlage-hamburg.html', 'Werbeanlagen in Hamburg'],
    nrw: ['/blog/werbeanlage-koeln.html', 'Werbeanlagen in NRW (Beispiel Köln)'],
    brandenburg: ['/blog/werbeanlage-potsdam.html', 'Werbeanlagen in Potsdam'],
    andere: ['/blog/aussenwerbung-berlin-ratgeber.html', 'Außenwerbung – Grundlagen']
  };

  function bewerten() {
    var r = A.region, wo = A.wo, out = { stufe: 'gruen', titel: '', punkte: [], links: [] };
    var klein = A.flaeche === 'k1', mittel = A.flaeche === 'k25', kurz = A.dauer === 'kurz';
    var bau; // 'frei' | 'antrag' | 'pruefen'
    if (wo === 'gehweg') bau = 'gehweg';
    else if (wo === 'frei') bau = 'antrag';
    else if (r === 'berlin') {
      if (wo === 'geruest') bau = 'antrag';
      else if (klein) bau = 'frei';
      else if (mittel && A.eigen === 'ja') bau = 'frei';
      else bau = 'antrag';
    } else if (r === 'nrw') bau = klein || kurz ? 'frei' : 'antrag';
    else if (r === 'hamburg') bau = klein ? 'frei' : 'antrag';
    else if (r === 'brandenburg') bau = kurz ? 'frei' : 'pruefen';
    else bau = 'pruefen';

    if (bau === 'frei') {
      out.titel = 'Baurechtlich voraussichtlich verfahrensfrei';
      out.punkte.push(r === 'berlin' ? (klein ? 'Berlin: Werbeanlagen bis 1 m² Ansichtsfläche sind verfahrensfrei (§ 61 Abs. 1 BauO Bln).' : 'Berlin: Werbung am eigenen Geschäft ist bis 2,5 m² verfahrensfrei (§ 61 Abs. 1 BauO Bln).')
        : r === 'nrw' ? (klein ? 'NRW: verfahrensfrei bis 1 m² (§ 62 Abs. 1 Nr. 12 BauO NRW). Wichtig: Mehrere Flächen nebeneinander werden zusammengerechnet.' : 'NRW: vorübergehende Werbeanlagen bis zwei Monate sind verfahrensfrei (§ 62 Abs. 1 Nr. 12 BauO NRW), nicht im Außenbereich.')
        : r === 'hamburg' ? 'Hamburg: bis 1 m² genehmigungsfrei (Anlage 2 HBauO).'
        : 'Brandenburg: vorübergehende Werbeanlagen bis zwei Monate sind verfahrensfrei (§ 61 BbgBO).');
      out.punkte.push('Verfahrensfrei heißt nicht regelfrei: Gestaltungsregeln, Denkmalschutz und Nachbarrecht gelten trotzdem.');
    } else if (bau === 'antrag') {
      out.stufe = 'rot'; out.titel = 'Voraussichtlich Genehmigung nötig';
      out.punkte.push(wo === 'frei' ? 'Freistehende Werbeanlagen wie Pylone oder Masten brauchen in der Regel eine Baugenehmigung.'
        : wo === 'geruest' && r === 'berlin' ? 'Berlin: Werbung an Gerüsten und Bauzäunen ist seit 2010 nicht mehr verfahrensfrei und zeitlich begrenzt (Merkblatt Bezirksamt Neukölln).'
        : r === 'berlin' ? 'Berlin: Über 1 m² (am eigenen Geschäft über 2,5 m²) braucht die Werbeanlage eine Genehmigung – meist im vereinfachten Verfahren beim Bezirksamt.'
        : r === 'nrw' ? 'NRW: Über 1 m² Ansichtsfläche ist die Werbeanlage nicht mehr verfahrensfrei; zuständig ist die Bauaufsicht Ihrer Stadt.'
        : 'Hamburg: Über 1 m² ist meist eine Baugenehmigung nötig; zuständig ist das Bezirksamt.');
      out.punkte.push('Für den Antrag braucht es unter anderem eine Zeichnung mit Maßen und einen Lageplan – wir bereiten die Unterlagen auf Wunsch vor.');
    } else if (bau === 'gehweg') {
      out.stufe = r === 'hamburg' ? 'rot' : 'gelb'; out.titel = r === 'hamburg' ? 'In Hamburg meist nicht erlaubt' : 'Sondernutzungserlaubnis nötig';
      out.punkte.push(r === 'hamburg' ? 'Hamburg: Kundenstopper sind laut Stadt bis auf wenige Ausnahmen grundsätzlich nicht gestattet. Alternative: Werbung im Schaufenster.'
        : r === 'berlin' ? 'Berlin: Werbeaufsteller nur während der Öffnungszeiten direkt vor dem eigenen Geschäft, höchstens 1,50 m von der Hauswand, höchstens 1,20 × 0,80 m – mit Erlaubnis des Bezirksamts.'
        : 'Ein Aufsteller auf dem öffentlichen Gehweg ist eine Sondernutzung – die Erlaubnis und die Regeln kommen von Ihrer Stadt.');
    } else {
      out.stufe = 'gelb'; out.titel = 'Bitte beim Bauamt prüfen';
      out.punkte.push(r === 'brandenburg' ? 'Brandenburg: Für dauerhafte Werbeanlagen prüfen wir die Regeln mit dem zuständigen Bauamt Ihrer Stadt.' : 'Die Regeln unterscheiden sich je Bundesland – in vielen Ländern sind kleine Werbeanlagen bis 1 m² verfahrensfrei. Wir prüfen das für Ihren Standort.');
    }
    if (wo === 'ausleger') {
      if (out.stufe === 'gruen') out.stufe = 'gelb';
      out.punkte.push('Ein Ausleger ragt über den Gehweg: Zusätzlich ist meist eine Sondernutzungserlaubnis der Stadt bzw. des Bezirksamts nötig.');
    }
    if (A.denkmal === 'ja') { if (out.stufe === 'gruen') out.stufe = 'gelb'; out.punkte.push('Denkmal oder Gestaltungssatzung: Dafür ist meist eine zusätzliche Genehmigung nötig – auch wenn die Anlage sonst verfahrensfrei wäre (in Berlin § 11 DSchG Bln).'); }
    else if (A.denkmal === 'unklar') out.punkte.push('Ob Ihr Gebäude unter Denkmalschutz steht, zeigt die Denkmalliste Ihres Landes – wir prüfen das mit.');
    if (A.miete === 'ja') out.punkte.push('Gemietet: Die schriftliche Zustimmung des Vermieters bzw. der Eigentümergemeinschaft ist zusätzlich nötig.');
    if (A.licht === 'ja') out.punkte.push('Beleuchtet: Achten Sie auf Helligkeit und Schaltzeiten in Wohnlagen; den Anschluss übernimmt ein Elektrofachbetrieb.');
    out.links.push(RATGEBER[r] || RATGEBER.andere);
    if (wo === 'gehweg' || wo === 'ausleger') out.links.push(['/blog/kundenstopper-erlaubnis.html', 'Kundenstopper & Ausleger: Erlaubnis']);
    if (A.miete === 'ja') out.links.push(['/blog/werbeschild-mietobjekt-vermieter.html', 'Werbeschild am gemieteten Laden']);
    if (wo === 'geruest') out.links.push(['/blog/bauzaunbanner-ratgeber.html', 'Bauzaunbanner-Ratgeber']);
    if (A.licht === 'ja') out.links.push(['/blog/leuchtreklame-strom-betriebszeiten.html', 'Leuchtreklame: Strom & Schaltzeiten']);
    return out;
  }

  function sichtbar() {
    // Fragen ausblenden, die nicht passen
    var wo = A.wo;
    $('[data-q="flaeche"]').hidden = wo === 'gehweg';
    $('[data-q="eigen"]').hidden = !(A.region === 'berlin' && A.flaeche !== 'k1' && wo !== 'gehweg' && wo !== 'geruest' && wo !== 'frei');
    $('[data-q="dauer"]').hidden = !((A.region === 'nrw' || A.region === 'brandenburg') && wo !== 'gehweg');
    $('[data-q="licht"]').hidden = wo === 'gehweg';
  }
  function fertig() {
    return FRAGEN.every(function (k) { var el = $('[data-q="' + k + '"]'); return el.hidden || A[k]; });
  }
  function zeige() {
    sichtbar();
    var out = $('#gc-out');
    var offen = FRAGEN.filter(function (k) { var el = $('[data-q="' + k + '"]'); return !el.hidden && !A[k]; });
    $('#gc-fort').textContent = offen.length ? 'Noch ' + offen.length + (offen.length === 1 ? ' Frage' : ' Fragen') : 'Alle Fragen beantwortet';
    if (!fertig()) { out.hidden = true; return; }
    var e = bewerten();
    var stufeTxt = { gruen: 'Gute Nachricht', gelb: 'Mit Erlaubnis möglich', rot: e.titel.indexOf('nicht erlaubt') > -1 ? 'Schwierig' : 'Antrag nötig' }[e.stufe];
    out.innerHTML = '<div class="gc-res gc-' + e.stufe + '"><span class="gc-tag">' + stufeTxt + '</span><h3>' + e.titel + '</h3><ul>' +
      e.punkte.map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul>' +
      '<p class="gc-links"><strong>Mehr dazu:</strong> ' + e.links.map(function (l) { return '<a href="' + l[0] + '">' + l[1] + '</a>'; }).join(' · ') + '</p>' +
      '<p class="gc-hinweis">Keine Rechtsberatung – eine erste Einordnung nach den Regeln mit Stand 11/2026. Verbindlich ist die Auskunft der Bauaufsicht bzw. des Bezirksamts. Wir klären die Genehmigung bei jedem Angebot mit.</p>' +
      '<div class="gc-act"><a class="btn btn-teal" href="#kontakt" id="gc-anfrage">Genehmigung mit uns klären</a><a class="btn gc-btn2" target="_blank" rel="noopener noreferrer" href="https://wa.me/' + ((A.region === 'nrw') ? '491782410682' : WA) + '?text=' + encodeURIComponent(zusammen(e)) + '">Per WhatsApp fragen</a><button type="button" class="gc-again" id="gc-neu">Neu starten</button></div></div>';
    out.hidden = false;
    $('#gc-anfrage').addEventListener('click', function () { var ta = document.getElementById('fo-nachricht'); if (ta) ta.value = zusammen(e) + '\n\n' + (ta.value || ''); });
    $('#gc-neu').addEventListener('click', function () { FRAGEN.forEach(function (k) { A[k] = null; }); $$('[data-v]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); }); zeige(); root.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
  }
  function zusammen(e) {
    var z = FRAGEN.filter(function (k) { return A[k] && !$('[data-q="' + k + '"]').hidden; }).map(function (k) { return TXT[k][A[k]]; }).join(', ');
    return 'Hallo, ich habe den Genehmigungs-Check auf Ihrer Website gemacht: ' + z + '. Ergebnis: ' + e.titel + '. Können Sie die Genehmigung für mich klären?';
  }
  $$('[data-q]').forEach(function (q) {
    var key = q.getAttribute('data-q');
    q.querySelectorAll('[data-v]').forEach(function (b) {
      b.addEventListener('click', function () {
        q.querySelectorAll('[data-v]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true'); A[key] = b.getAttribute('data-v');
        zeige();
        if (fertig()) setTimeout(function () { var o = $('#gc-out'); if (o && !o.hidden) o.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, 60);
      });
    });
  });
  zeige();
})();
