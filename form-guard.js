/* Zeitstempel fuer den Spam-Schutz in kontakt.php.
   Beim Laden der Seite wird die Uhrzeit in das versteckte Feld _t
   geschrieben. kontakt.php verwirft Formulare, die weniger als drei
   Sekunden nach dem Seitenaufruf abgeschickt werden - das schafft
   praktisch nur ein Bot. Ohne JavaScript bleibt das Feld leer und
   die Pruefung entfaellt; das Formular funktioniert trotzdem. */
(function () {
  var t = String(Date.now());
  var forms = document.querySelectorAll('form[action="/kontakt.php"]');
  for (var i = 0; i < forms.length; i++) {
    var f = forms[i].querySelector('input[name="_t"]');
    if (!f) {
      f = document.createElement('input');
      f.type = 'hidden';
      f.name = '_t';
      forms[i].appendChild(f);
    }
    f.value = t;
  }
})();
