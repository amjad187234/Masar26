/*
 * Kundenstimmen – lädt freigegebene Bewertungen aus bewertung.php?liste=1
 * und zeigt sie in jeder Section mit [data-bewertungen] an.
 * Ohne freigegebene Bewertung bleibt die Section unsichtbar (hidden).
 * Optional: data-max="6" begrenzt die Anzahl.
 */
(function () {
  var sections = document.querySelectorAll('[data-bewertungen]');
  if (!sections.length || !window.fetch) return;

  var css = ''
    + '.kst-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),360px));justify-content:center;gap:1.2rem;margin-top:2rem}'
    + '.kst-card{background:#fff;border:1px solid var(--border,#e0eaea);border-radius:var(--r,12px);padding:1.5rem 1.4rem;display:flex;flex-direction:column;gap:.9rem;margin:0}'
    + '.kst-stars{color:#e0a800;font-size:1.15rem;letter-spacing:2px;line-height:1}'
    + '.kst-stars .kst-off{color:#cfd8d8}'
    + '.kst-text{color:var(--text,#1a2a2a);font-size:15.5px;line-height:1.7;white-space:pre-line;margin:0;flex:1}'
    + '.kst-who{font-size:14px;color:var(--muted,#5a7070);line-height:1.5}'
    + '.kst-who strong{display:block;color:var(--navy,#132e50);font-size:15px}'
    + '.kst-note{font-size:13px;color:var(--muted,#5a7070);line-height:1.6;max-width:760px;margin:1.6rem auto 0;text-align:center}';
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  var monate = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];

  function karte(b) {
    var fig = document.createElement('figure');
    fig.className = 'kst-card';

    var s = Math.max(1, Math.min(5, parseInt(b.sterne, 10) || 0));
    var stars = document.createElement('div');
    stars.className = 'kst-stars';
    stars.setAttribute('role', 'img');
    stars.setAttribute('aria-label', s + ' von 5 Sternen');
    stars.innerHTML = '★★★★★'.slice(0, s) + '<span class="kst-off">' + '★★★★★'.slice(0, 5 - s) + '</span>';
    fig.appendChild(stars);

    var text = document.createElement('blockquote');
    text.className = 'kst-text';
    text.textContent = '„' + b.text + '“';
    fig.appendChild(text);

    var who = document.createElement('figcaption');
    who.className = 'kst-who';
    var name = document.createElement('strong');
    name.textContent = b.name;
    who.appendChild(name);
    var info = [];
    if (b.firma) info.push(b.firma);
    if (b.leistung) info.push(b.leistung);
    var d = /^(\d{4})-(\d{2})/.exec(b.datum || '');
    if (d) info.push(monate[parseInt(d[2], 10) - 1] + ' ' + d[1]);
    if (info.length) who.appendChild(document.createTextNode(info.join(' · ')));
    fig.appendChild(who);
    return fig;
  }

  fetch('/bewertung.php?liste=1', { headers: { 'Accept': 'application/json' } })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (liste) {
      if (!Array.isArray(liste) || !liste.length) return;
      Array.prototype.forEach.call(sections, function (sec) {
        var ziel = sec.querySelector('[data-bewertungen-liste]');
        if (!ziel) return;
        var max = parseInt(sec.getAttribute('data-max'), 10) || liste.length;
        liste.slice(0, max).forEach(function (b) { ziel.appendChild(karte(b)); });
        sec.hidden = false;
      });
    })
    .catch(function () {});
})();
