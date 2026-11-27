<?php
/**
 * IndexNow – neue und geänderte Seiten sofort an Bing & Co. melden
 *
 * Läuft automatisch über cron.php, sobald sich sitemap.xml geändert hat.
 * Von Hand (z. B. ohne Cronjob) nach dem „Bereitstellen“ im Browser öffnen:
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

require_once __DIR__ . '/inc/indexnow.php';

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

$e = indexnow_melden(isset($_GET['alle']), isset($_GET['test']));
$liste = '<ul>' . implode('', array_map(fn($u) => '<li>' . h($u) . '</li>', array_slice($e['urls'], 0, 200))) . '</ul>';
$n = count($e['urls']);

switch ($e['status']) {
    case 'fehler_sitemap':
        seite('IndexNow', '<h1>Fehler</h1><p class="err">sitemap.xml konnte nicht gelesen werden.</p>');
    case 'aktuell':
        seite('IndexNow', '<h1>Alles aktuell ✓</h1><p>Seit der letzten Meldung hat sich laut Sitemap keine Seite geändert. Es wurde nichts gesendet.</p>'
            . '<p class="m">Letzte Meldung: ' . ($e['zeit'] ? date('d.m.Y H:i', $e['zeit']) : '–') . ' · ' . $e['gesamt'] . ' Seiten in der Sitemap</p>');
    case 'test':
        seite('IndexNow – Test', '<h1>Test: ' . $n . ' Seite(n) würden gemeldet</h1>' . $liste . '<p class="m">Nichts gesendet. Ohne <code>?test=1</code> aufrufen, um wirklich zu melden.</p>');
    case 'pause':
        seite('IndexNow', '<h1>Bitte kurz warten</h1><p>Die letzte Meldung ist weniger als 10 Minuten her. Bitte später noch einmal öffnen.</p>');
    case 'gemeldet':
        seite('IndexNow', '<h1>Gemeldet ✓</h1><p class="ok">' . $n . ' Seite(n) an IndexNow gesendet (Antwort ' . $e['code'] . ').</p>' . $liste
            . '<p class="m">Bing, Yandex und weitere Suchmaschinen erhalten die Meldung. Läuft der Cronjob (cron.php), geschieht das nach jedem „Bereitstellen“ von selbst.</p>');
}

$hinweis = [
    400 => 'Ungültige Anfrage.',
    403 => 'Schlüssel nicht gültig – ist die Datei ' . INDEXNOW_KEY . '.txt online erreichbar?',
    422 => 'Die URLs passen nicht zur Domain oder zum Schlüssel.',
    429 => 'Zu viele Anfragen – bitte später erneut versuchen.',
][$e['code']] ?? 'Keine Verbindung oder unbekannter Fehler.';
seite('IndexNow', '<h1>Nicht gesendet</h1><p class="err">Antwort ' . ($e['code'] ?: '–') . ': ' . h($hinweis) . '</p><p class="m">' . h(substr($e['antwort'], 0, 300)) . '</p>');
