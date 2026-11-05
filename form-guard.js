/* Zeitstempel fuer den Spam-Schutz in kontakt.php.
   Beim Laden der Seite wird die Uhrzeit in das versteckte Feld _t
   geschrieben. kontakt.php verwirft Formulare, die weniger als drei
   Sekunden nach dem Seitenaufruf abgeschickt werden - das schafft
   praktisch nur ein Bot. Ohne JavaScript bleibt das Feld leer und
   die Pruefung entfaellt; das Formular funktioniert trotzdem.

   Dazu (04.11.2026): verstaendliche Fehlermeldungen direkt am Feld statt
   der Browser-Blase. Geprueft wird erst beim Verlassen eines Feldes bzw.
   beim Absenden (nicht schon beim ersten Tastendruck); nach einem Fehler
   verschwindet die Meldung, sobald die Eingabe stimmt. Felder und Namen
   bleiben unveraendert - kontakt.php bekommt dieselben Daten wie vorher.
   Ohne JavaScript greift weiter die normale Browser-Pruefung (required). */
(function () {
  var t = String(Date.now());
  var forms = document.querySelectorAll('form[action="/kontakt.php"]');
  var nr = 0;

  function name(f) {
    var l = f.id && f.form.querySelector('label[for="' + f.id + '"]');
    var s = l ? l.textContent : (f.getAttribute('aria-label') || f.placeholder || '');
    return s.replace(/[*:]/g, '').replace(/\s*\(.*?\)\s*/g, ' ').trim();
  }
  function text(f) {
    var v = f.validity;
    if (f.type === 'checkbox') return 'Bitte setzen Sie hier das Häkchen (Hinweis zur Datenschutzerklärung).';
    if (v.valueMissing) return name(f) ? 'Bitte „' + name(f) + '“ ausfüllen.' : 'Bitte dieses Feld ausfüllen.';
    if (f.type === 'email') return 'Die E-Mail-Adresse scheint unvollständig – bitte im Format name@firma.de eingeben.';
    if (v.tooShort) return 'Bitte etwas ausführlicher (mind. ' + f.minLength + ' Zeichen).';
    if (v.typeMismatch || v.patternMismatch) return 'Bitte die Eingabe prüfen' + (f.title ? ' – ' + f.title : '.');
    return f.validationMessage || 'Bitte die Eingabe prüfen.';
  }
  function box(f) {
    var id = f.getAttribute('data-err-id');
    if (id) return document.getElementById(id);
    var p = document.createElement('span');
    p.className = 'fg-err'; p.id = 'fg-err-' + (++nr); p.setAttribute('aria-live', 'polite');
    f.setAttribute('data-err-id', p.id);
    var d = f.getAttribute('aria-describedby');
    f.setAttribute('aria-describedby', (d ? d + ' ' : '') + p.id);
    // Auf dunklem Untergrund hellere Fehlerfarbe (Kontrast)
    var bg = getComputedStyle(f.closest('form') || document.body).color;
    var m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(bg);
    if (m && (+m[1] + +m[2] + +m[3]) / 3 > 180) p.style.color = '#ffb4ab';
    var ziel = f.type === 'checkbox' ? (f.closest('.consent-row, label, div') || f) : f;
    ziel.insertAdjacentElement('afterend', p);
    return p;
  }
  function pruefen(f) {
    if (f.type === 'hidden' || f.disabled || f.name === '_honey' || !f.willValidate) return true;
    // Leerzeichen allein zählen nicht als Eingabe
    if (f.required && f.type !== 'checkbox' && f.type !== 'file' && f.value && !f.value.trim()) f.value = '';
    var ok = f.checkValidity();
    if (ok && f.type === 'email' && f.value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.value.trim())) ok = false;
    if (ok) {
      if (f.getAttribute('aria-invalid') === 'true') { f.removeAttribute('aria-invalid'); var b = box(f); if (b) b.textContent = ''; }
      return true;
    }
    f.setAttribute('aria-invalid', 'true');
    box(f).textContent = text(f);
    return false;
  }

  for (var i = 0; i < forms.length; i++) {
    var form = forms[i];
    var f = form.querySelector('input[name="_t"]');
    if (!f) {
      f = document.createElement('input');
      f.type = 'hidden';
      f.name = '_t';
      form.appendChild(f);
    }
    f.value = t;

    form.noValidate = true;
    form.addEventListener('focusout', function (e) {
      var el = e.target;
      if (!el.matches || !el.matches('input,textarea,select')) return;
      if (el.value || el.getAttribute('aria-invalid') === 'true') pruefen(el);
    });
    form.addEventListener('input', function (e) { if (e.target.getAttribute && e.target.getAttribute('aria-invalid') === 'true') pruefen(e.target); });
    form.addEventListener('change', function (e) { if (e.target.type === 'checkbox' && e.target.getAttribute('aria-invalid') === 'true') pruefen(e.target); });
    form.addEventListener('submit', function (e) {
      var erstes = null;
      Array.prototype.forEach.call(this.elements, function (el) { if (!pruefen(el) && !erstes) erstes = el; });
      if (erstes) {
        e.preventDefault();
        e.stopImmediatePropagation();
        erstes.focus();
        if (erstes.scrollIntoView) erstes.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }
    });
  }
})();
