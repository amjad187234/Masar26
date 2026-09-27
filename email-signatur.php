<?php
/**
 * Kopiervorlage der E-Mail-Signatur fuer Webmail, Outlook und Gmail.
 * Nicht fuer Suchmaschinen gedacht (noindex).
 */
declare(strict_types=1);
require __DIR__ . '/signatur.php';
header('X-Robots-Tag: noindex, nofollow');
header('Content-Type: text/html; charset=UTF-8');
$sig = masar_signatur_html();
?><!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>E-Mail-Signatur | Masar Werbeagentur</title>
<style>
  body{margin:0;background:#f4f7f7;font-family:Arial,Helvetica,sans-serif;color:#1a2a2a}
  .wrap{max-width:720px;margin:0 auto;padding:32px 16px}
  h1{font-size:22px;color:#132e50;margin:0 0 6px}
  p.hint{color:#5a7070;font-size:14px;line-height:1.6;margin:0 0 22px}
  .card{background:#fff;border:1px solid #e0eaea;border-radius:10px;padding:24px;margin-bottom:16px;overflow-x:auto}
  .btns{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:28px}
  button{font:inherit;font-weight:bold;font-size:14px;border:0;border-radius:6px;padding:11px 18px;cursor:pointer}
  .b1{background:#58d0bd;color:#132e50}
  .b2{background:#132e50;color:#fff}
  #status{font-size:13px;color:#177567;min-height:1.2em;margin:-18px 0 22px}
  pre{background:#fff;border:1px solid #e0eaea;border-radius:10px;padding:16px;font-size:13px;white-space:pre-wrap;margin:0}
  h2{font-size:15px;color:#132e50;margin:0 0 10px}
</style>
</head>
<body>
<div class="wrap">
  <h1>E-Mail-Signatur</h1>
  <p class="hint">Auf „Signatur kopieren“ klicken und im Mailprogramm in das Signaturfeld einfügen.</p>

  <div class="card" id="sig"><?= $sig ?></div>
  <div class="btns">
    <button class="b1" type="button" id="copyRich">Signatur kopieren</button>
    <button class="b2" type="button" id="copyHtml">HTML-Code kopieren</button>
  </div>
  <div id="status" role="status"></div>

  <h2>Reine Text-Version</h2>
  <pre><?= htmlspecialchars(masar_signatur_text(), ENT_QUOTES, 'UTF-8') ?></pre>
</div>
<script>
(function () {
  var html = document.getElementById('sig').innerHTML;
  var status = document.getElementById('status');
  function done(msg) { status.textContent = msg; }
  document.getElementById('copyRich').addEventListener('click', function () {
    if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {
      navigator.clipboard.write([new ClipboardItem({
        'text/html': new Blob([html], { type: 'text/html' }),
        'text/plain': new Blob([document.getElementById('sig').innerText], { type: 'text/plain' })
      })]).then(function () { done('Kopiert – jetzt im Mailprogramm einfügen.'); },
                function () { selectSig(); });
    } else { selectSig(); }
  });
  function selectSig() {
    var r = document.createRange(); r.selectNodeContents(document.getElementById('sig'));
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    done('Markiert – jetzt Strg+C (Mac: Cmd+C) drücken.');
  }
  document.getElementById('copyHtml').addEventListener('click', function () {
    navigator.clipboard.writeText(html).then(function () { done('HTML-Code kopiert.'); },
      function () { done('Kopieren nicht möglich – bitte manuell markieren.'); });
  });
})();
</script>
</body>
</html>
