<?php
/**
 * Erfasst Anfragen, die der Anfrage-Assistent per WhatsApp verschickt.
 * Der Besucher sendet die Nachricht selbst in WhatsApp; parallel landet die
 * Zusammenfassung mit Anfragenummer in der Übersicht /admin/anfragen.php.
 * Antwort: JSON {"nr": "ANF-2026-0001"} oder {"nr": ""}.
 * Schutz: nur POST, Honeypot, Mindestzeit, Begrenzung pro IP, Längenlimits.
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=UTF-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

function antwort(string $nr = '', int $code = 200): void
{
    http_response_code($code);
    echo json_encode(['nr' => $nr]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') antwort('', 405);

$roh = (string) file_get_contents('php://input', false, null, 0, 20000);
$d = json_decode($roh, true);
if (!is_array($d)) antwort('', 400);

$f = static fn(string $k, int $n = 300): string => is_string($d[$k] ?? null) ? mb_substr(trim(str_replace(["\r", "\0"], '', $d[$k])), 0, $n) : '';

// Honeypot und Mindestzeit (Assistent sendet die Ladezeit der Seite in ms)
if ($f('_honey') !== '') antwort('');
$t = $f('_t', 20);
if ($t !== '' && ctype_digit($t) && (microtime(true) * 1000 - (int) $t) < 3000) antwort('');

// Begrenzung: höchstens 10 Meldungen pro Stunde und IP
$ip = $_SERVER['REMOTE_ADDR'] ?? 'x';
$datei = sys_get_temp_dir() . '/masar_wa_' . md5($ip) . '.txt';
$jetzt = time();
$zeiten = array_filter(array_map('intval', explode(',', (string) @file_get_contents($datei))), static fn($z) => $z > $jetzt - 3600);
if (count($zeiten) >= 10) antwort('', 429);
$zeiten[] = $jetzt;
@file_put_contents($datei, implode(',', $zeiten), LOCK_EX);

$name = $f('name', 120);
if (mb_strlen($name) < 2) antwort('', 422);

require_once __DIR__ . '/inc/anfragen.php';
$nr = anf_speichern([
    'quelle' => 'WhatsApp-Assistent',
    'seite' => mb_substr((string) ($_SERVER['HTTP_REFERER'] ?? ''), 0, 200),
    'name' => $name, 'firma' => $f('firma', 120), 'email' => $f('email', 160), 'telefon' => $f('telefon', 60),
    'ort' => $f('ort', 120), 'leistung' => $f('leistung', 200), 'zusammenfassung' => $f('zusammenfassung', 4000),
    'daten' => ['Leistung' => $f('leistung', 200), 'Details' => $f('details', 400), 'Für' => $f('wer', 40), 'Zeitrahmen' => $f('wann', 60)],
]);
antwort($nr);
