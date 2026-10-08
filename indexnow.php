<?php
/**
 * IndexNow – neue und geänderte Seiten sofort an Bing & Co. melden
 *
 * Nach jedem „Bereitstellen“ einmal im Browser öffnen:
 *   https://masar-werbeagentur.de/indexnow.php
 *
 * Ablauf: sitemap.xml lesen, nur URLs melden, deren <lastmod> sich seit der
 * letzten Meldung geändert hat, Stand in data/indexnow.json merken.
 * ?alle=1 meldet einmalig alle URLs (z. B. beim ersten Mal).
 * ?test=1 zeigt nur an, was gemeldet würde, ohne zu senden.
 *
 * Schutz: höchstens ein Versand alle 10 Minuten; doppelte Aufrufe melden
 * nichts doppelt. Der Schlüssel ist öffentlich (so verlangt es IndexNow).
 */

declare(strict_types=1);

const HOST     = 'masar-werbeagentur.de';
const KEY      = '016f0c80ae1bc78d09f7ee8a1473682a';
const ENDPOINT = 'https://api.indexnow.org/indexnow';
const SITEMAP  = __DIR__ . '/sitemap.xml';
const STAND    = __DIR__ . '/data/indexnow.json';
const PAUSE    = 600;

header('Content-Type: text/html; charset=UTF-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

function seite(string $titel, string $inhalt): void
{
    echo '<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
       . '<meta name="robots" content="noindex, nofollow"><title>' . h($titel) . '</title>'
       . '<style>body{font-family:Arial,Helvetica,sans-serif;background:#f4f7fa;color:#132e50;margin:0;padding:24px}'
       . '.k{max-width:640px;margin:0 auto;background:#fff;border:1px solid #dce6ee;border-radius:12px;padding:24px}'
       . 'h1{font-size:22px;margin:0 0 12px}ul{padding-left:18px;font-size:14px;line-height:1.6;max-height:50vh;overflow:auto}'
       . '.ok{color:#177567;font-weight:700}.err{color:#c0392b;font-weight:700}.m{color:#5a7070;font-size:14px}</style></head>'
       . '<body><div class="k">' . $inhalt . '</div></body></html>';
    exit;
}

// 1. Sitemap lesen
$xml = @simplexml_load_file(SITEMAP);
if ($xml === false) {
    seite('IndexNow', '<h1>Fehler</h1><p class="err">sitemap.xml konnte nicht gelesen werden.</p>');
}
$aktuell = [];
foreach ($xml->url as $u) {
    $loc = trim((string) $u->loc);
    if ($loc !== '' && parse_url($loc, PHP_URL_HOST) === HOST) {
        $aktuell[$loc] = trim((string) $u->lastmod);
    }
}

// 2. Letzten Stand laden
$stand = ['zeit' => 0, 'urls' => []];
if (is_readable(STAND)) {
    $d = json_decode((string) file_get_contents(STAND), true);
    if (is_array($d)) { $stand = array_merge($stand, $d); }
}

$alle = isset($_GET['alle']);
$test = isset($_GET['test']);
$neu = [];
foreach ($aktuell as $loc => $lastmod) {
    if ($alle || !isset($stand['urls'][$loc]) || $stand['urls'][$loc] !== $lastmod) {
        $neu[] = $loc;
    }
}

$liste = '<ul>' . implode('', array_map(fn($u) => '<li>' . h($u) . '</li>', array_slice($neu, 0, 200))) . '</ul>';

if (!$neu) {
    seite('IndexNow', '<h1>Alles aktuell ✓</h1><p>Seit der letzten Meldung hat sich laut Sitemap keine Seite geändert. Es wurde nichts gesendet.</p>'
        . '<p class="m">Letzte Meldung: ' . ($stand['zeit'] ? date('d.m.Y H:i', (int) $stand['zeit']) : '–') . ' · ' . count($aktuell) . ' Seiten in der Sitemap</p>');
}

if ($test) {
    seite('IndexNow – Test', '<h1>Test: ' . count($neu) . ' Seite(n) würden gemeldet</h1>' . $liste . '<p class="m">Nichts gesendet. Ohne <code>?test=1</code> aufrufen, um wirklich zu melden.</p>');
}

if (time() - (int) $stand['zeit'] < PAUSE) {
    seite('IndexNow', '<h1>Bitte kurz warten</h1><p>Die letzte Meldung ist weniger als 10 Minuten her. Bitte später noch einmal öffnen.</p>');
}

// 3. Senden (max. 10.000 URLs pro Anfrage laut IndexNow)
$body = json_encode([
    'host'        => HOST,
    'key'         => KEY,
    'keyLocation' => 'https://' . HOST . '/' . KEY . '.txt',
    'urlList'     => array_values(array_slice($neu, 0, 10000)),
], JSON_UNESCAPED_SLASHES);

$code = 0; $antwort = '';
if (function_exists('curl_init')) {
    $ch = curl_init(ENDPOINT);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $body,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json; charset=utf-8'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 20,
    ]);
    $antwort = (string) curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
} else {
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'header' => "Content-Type: application/json; charset=utf-8\r\n", 'content' => $body, 'timeout' => 20, 'ignore_errors' => true]]);
    $antwort = (string) @file_get_contents(ENDPOINT, false, $ctx);
    if (isset($http_response_header[0]) && preg_match('/\s(\d{3})\s/', $http_response_header[0], $m)) { $code = (int) $m[1]; }
}

// 200 = angenommen, 202 = angenommen (Schlüssel wird noch geprüft)
if ($code === 200 || $code === 202) {
    foreach ($neu as $loc) { $stand['urls'][$loc] = $aktuell[$loc]; }
    $stand['zeit'] = time();
    @file_put_contents(STAND, json_encode($stand, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT), LOCK_EX);
    seite('IndexNow', '<h1>Gemeldet ✓</h1><p class="ok">' . count($neu) . ' Seite(n) an IndexNow gesendet (Antwort ' . $code . ').</p>' . $liste
        . '<p class="m">Bing, Yandex und weitere Suchmaschinen erhalten die Meldung. Beim nächsten „Bereitstellen“ diese Seite einfach wieder öffnen.</p>');
}

$hinweis = [
    400 => 'Ungültige Anfrage.',
    403 => 'Schlüssel nicht gültig – ist die Datei ' . KEY . '.txt online erreichbar?',
    422 => 'Die URLs passen nicht zur Domain oder zum Schlüssel.',
    429 => 'Zu viele Anfragen – bitte später erneut versuchen.',
][$code] ?? 'Keine Verbindung oder unbekannter Fehler.';
seite('IndexNow', '<h1>Nicht gesendet</h1><p class="err">Antwort ' . ($code ?: '–') . ': ' . h($hinweis) . '</p><p class="m">' . h(substr($antwort, 0, 300)) . '</p>');
