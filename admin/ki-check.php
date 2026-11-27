<?php
/**
 * KI-Chatbot-Generator: Prüfung der Hosting-Voraussetzungen und Nutzungsübersicht.
 * Aufruf nach der Anmeldung in /admin/anfragen.php:  /admin/ki-check.php
 * ?test=1 schickt eine einzige kurze Testfrage an die KI (kostet einen Bruchteil eines Cents).
 */

declare(strict_types=1);

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
header('X-Frame-Options: DENY');
header('Referrer-Policy: no-referrer');

session_set_cookie_params(['lifetime' => 0, 'path' => '/admin/', 'secure' => !empty($_SERVER['HTTPS']), 'httponly' => true, 'samesite' => 'Strict']);
session_name('masar_anf');
session_start();
if (empty($_SESSION['ok'])) { header('Location: /admin/anfragen.php'); exit; }

require_once dirname(__DIR__) . '/inc/ki_generator.php';

function h($s): string { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }

$c = kg_cfg(); $z = [];
$z[] = ['PHP-Version', PHP_VERSION, version_compare(PHP_VERSION, '8.0', '>=')];
$z[] = ['cURL', function_exists('curl_init') ? (curl_version()['version'] ?? 'ja') : 'fehlt', function_exists('curl_init')];
$z[] = ['SQLite (PDO)', class_exists('PDO') && in_array('sqlite', PDO::getAvailableDrivers(), true) ? 'ja' : 'fehlt', class_exists('PDO') && in_array('sqlite', PDO::getAvailableDrivers(), true)];
$z[] = ['Ordner data/ beschreibbar', is_writable(dirname(KG_DB)) ? 'ja' : 'nein', is_writable(dirname(KG_DB))];
$z[] = ['Datenbank', kg_db() ? 'bereit' : 'Fehler', (bool) kg_db()];
$ips = function_exists('gethostbynamel') ? (gethostbynamel('example.com') ?: []) : [];
$z[] = ['Namensauflösung (example.com)', $ips ? implode(', ', $ips) : 'keine Antwort', (bool) $ips];
$abruf = function_exists('curl_init') ? kg_holen('https://example.com/') : 'cURL fehlt';
$z[] = ['Fremde Website lesen (example.com)', is_string($abruf) ? $abruf : 'Status ' . $abruf[1]['status'] . ', ' . strlen($abruf[1]['body']) . ' Bytes', !is_string($abruf) && $abruf[1]['status'] === 200];
$intern = kg_url_pruefen('http://127.0.0.1/');
$z[] = ['Schutz: interne Adresse wird abgelehnt', is_string($intern) ? 'ja' : 'NEIN', is_string($intern)];

// Erreichbarkeit der KI-Schnittstelle (ohne Schlüssel: jede HTTP-Antwort zählt als erreichbar)
$api = ['–', false];
if (function_exists('curl_init')) {
    $ch = curl_init(KG_API); curl_setopt_array($ch, [CURLOPT_NOBODY => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 10]);
    curl_exec($ch); $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE); $err = curl_error($ch); curl_close($ch);
    $api = [$code ? 'erreichbar (Antwort ' . $code . ')' : 'nicht erreichbar: ' . $err, $code > 0];
}
$z[] = ['Verbindung zu api.anthropic.com', $api[0], $api[1]];
$z[] = ['Schlüssel in kontakt-config.php (anthropic_key)', $c['key'] !== '' ? 'eingetragen (…' . substr($c['key'], -4) . ')' : 'fehlt – Generator bleibt unsichtbar', $c['key'] !== ''];
$z[] = ['Modell', $c['model'] . (isset(KG_PREISE[$c['model']]) ? '' : ' (Preis unbekannt – wird wie das teuerste gerechnet)'), true];
$verbraucht = kg_db() ? kg_kosten_monat() : 0.0;
$z[] = ['Monatsbudget', number_format($verbraucht, 4, ',', '.') . ' von ' . number_format($c['budget'], 2, ',', '.') . ' (ca. Euro)', $verbraucht < $c['budget']];
$z[] = ['Notschalter (ki_generator_aus)', $c['aus'] ? 'AN – Generator abgeschaltet' : 'aus', !$c['aus']];

$test = '';
if (isset($_GET['test']) && $c['key'] !== '' && function_exists('curl_init')) {
    $ch = curl_init(KG_API);
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'x-api-key: ' . $c['key'], 'anthropic-version: ' . KG_API_VERSION],
        CURLOPT_POSTFIELDS => json_encode(['model' => $c['model'], 'max_tokens' => 50, 'thinking' => ['type' => 'disabled'], 'messages' => [['role' => 'user', 'content' => 'Antworte nur mit dem Wort: bereit']]])]);
    $roh = (string) curl_exec($ch); $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE); curl_close($ch);
    $a = json_decode($roh, true);
    $txt = ''; foreach (($a['content'] ?? []) as $b) { if (($b['type'] ?? '') === 'text') $txt .= $b['text']; }
    $test = $code === 200 ? 'KI-Test erfolgreich: „' . trim($txt) . '“ (' . (int) ($a['usage']['input_tokens'] ?? 0) . ' + ' . (int) ($a['usage']['output_tokens'] ?? 0) . ' Tokens)'
                          : 'KI-Test fehlgeschlagen (Antwort ' . $code . '): ' . substr((string) ($a['error']['message'] ?? $roh), 0, 200);
}

$tage = []; $domains = [];
if ($db = kg_db()) {
    $tage = $db->query("SELECT tag, SUM(typ = 'start') AS s, SUM(typ = 'chat') AS c, SUM(typ = 'fehler') AS f, SUM(kosten) AS k FROM nutzung GROUP BY tag ORDER BY tag DESC LIMIT 14")->fetchAll();
    $domains = $db->query("SELECT domain, MAX(zeit) AS z, SUM(typ = 'chat') AS c FROM nutzung WHERE domain <> '' GROUP BY domain ORDER BY z DESC LIMIT 30")->fetchAll();
}
?><!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>KI-Generator – Prüfung | Masar</title>
<style>body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f4f7fa;color:#132e50;font-size:15px;padding:16px}.k{max-width:760px;margin:0 auto 16px;background:#fff;border:1px solid #dce6ee;border-radius:12px;padding:18px}h1{font-size:21px;margin:0 0 10px}h2{font-size:17px;margin:0 0 10px}table{width:100%;border-collapse:collapse}td,th{padding:7px 6px;border-bottom:1px solid #e8eef3;text-align:left;vertical-align:top;font-size:14px}.ok{color:#177567;font-weight:700}.no{color:#b3261e;font-weight:700}a{color:#177567}.m{color:#5a7070;font-size:14px}</style></head><body>
<div class="k"><h1>KI-Chatbot-Generator – Prüfung</h1>
<table><?php foreach ($z as [$n, $w, $ok]) echo '<tr><td>' . h($n) . '</td><td>' . h($w) . '</td><td class="' . ($ok ? 'ok">✓' : 'no">✗') . '</td></tr>'; ?></table>
<?php if ($test !== '') echo '<p class="' . (str_starts_with($test, 'KI-Test erfolgreich') ? 'ok' : 'no') . '">' . h($test) . '</p>'; ?>
<p class="m"><?php echo $c['key'] !== '' ? '<a href="?test=1">KI-Verbindung mit einer Testfrage prüfen</a> (kostet einen Bruchteil eines Cents)' : 'Sobald der Schlüssel eingetragen ist, erscheint hier der Verbindungstest.'; ?> · <a href="/admin/anfragen.php">zurück zu den Anfragen</a></p></div>
<div class="k"><h2>Nutzung (letzte 14 Tage)</h2><table><tr><th>Tag</th><th>Websites</th><th>Fragen</th><th>Fehler</th><th>Kosten ca.</th></tr>
<?php foreach ($tage as $t) echo '<tr><td>' . h($t['tag']) . '</td><td>' . (int) $t['s'] . '</td><td>' . (int) $t['c'] . '</td><td>' . (int) $t['f'] . '</td><td>' . number_format((float) $t['k'], 4, ',', '.') . '</td></tr>'; if (!$tage) echo '<tr><td colspan="5" class="m">Noch keine Nutzung.</td></tr>'; ?></table></div>
<div class="k"><h2>Getestete Websites (Interessenten)</h2><table><tr><th>Domain</th><th>zuletzt</th><th>Fragen</th></tr>
<?php foreach ($domains as $d) echo '<tr><td>' . h($d['domain']) . '</td><td>' . h(date('d.m.Y H:i', (int) $d['z'])) . '</td><td>' . (int) $d['c'] . '</td></tr>'; if (!$domains) echo '<tr><td colspan="3" class="m">Noch keine.</td></tr>'; ?></table>
<p class="m">Gespeichert werden nur die Domain und die Zählung. Gelesener Text und Verlauf werden nach 24 Stunden gelöscht.</p></div>
</body></html>
