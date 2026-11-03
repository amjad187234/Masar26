<?php
/**
 * Anfrage-Status für Kunden: POST {nr, kontakt} → Status, Leistung, Stadt, Termin (keine Kontaktdaten).
 * Kontakt = Telefonnummer (letzte 6 Ziffern müssen passen) oder E-Mail-Adresse der Anfrage.
 * Mit aktion = absagen|verschieben (+ text) meldet der Kunde einen Terminwunsch (Termin bleibt, bis wir ihn bearbeiten).
 */

declare(strict_types=1);

require_once __DIR__ . '/inc/anfragen.php';

header('Content-Type: application/json; charset=UTF-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

function antwort(array $d, int $code = 200): void { http_response_code($code); echo json_encode($d, JSON_UNESCAPED_UNICODE); exit; }

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') antwort(['fehler' => 'Methode'], 405);

// Begrenzung: 20 Abfragen pro Stunde und IP (Schutz vor Durchprobieren)
$datei = sys_get_temp_dir() . '/masar_status_' . md5($_SERVER['REMOTE_ADDR'] ?? 'x') . '.txt';
$jetzt = time();
$zeiten = array_filter(array_map('intval', explode(',', (string) @file_get_contents($datei))), static fn($z) => $z > $jetzt - 3600);
if (count($zeiten) >= 20) antwort(['fehler' => 'Zu viele Abfragen. Bitte später erneut versuchen oder anrufen: 0178 514 3918.'], 429);
$zeiten[] = $jetzt;
@file_put_contents($datei, implode(',', $zeiten), LOCK_EX);

$d = json_decode((string) file_get_contents('php://input'), true);
$nr = is_array($d) && is_string($d['nr'] ?? null) ? mb_substr($d['nr'], 0, 20) : '';
$kontakt = is_array($d) && is_string($d['kontakt'] ?? null) ? mb_substr($d['kontakt'], 0, 160) : '';
// Termin verschieben/absagen: {nr, kontakt, aktion: "absagen"|"verschieben", text}
$aktion = is_array($d) && is_string($d['aktion'] ?? null) ? $d['aktion'] : '';
if ($aktion !== '') {
    $text = is_string($d['text'] ?? null) ? mb_substr($d['text'], 0, 500) : '';
    $e = anf_termin_wunsch($nr, $kontakt, $aktion, $text);
    if ($e === 'nicht_gefunden') antwort(['fehler' => 'Keine Anfrage gefunden.'], 404);
    if ($e !== 'ok') antwort(['fehler' => 'Das ist online leider nicht mehr möglich. Bitte rufen Sie uns an: 0178 514 3918.'], 409);
}
$r = anf_status_kunde($nr, $kontakt);
if (!$r) antwort(['fehler' => 'Keine Anfrage gefunden. Bitte Anfragenummer (z. B. ANF-2026-0012) und die Telefonnummer oder E-Mail aus Ihrer Anfrage prüfen.'], 404);
antwort($r);
