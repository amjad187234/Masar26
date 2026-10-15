<?php
/**
 * Kostenlose Beratung – Terminbuchung (Masar Werbeagentur)
 *
 *   GET  termin.php?tage=1&art=telefon          → buchbare Tage mit Anzahl freier Zeiten
 *   GET  termin.php?tag=2026-10-20&art=telefon  → freie Uhrzeiten des Tages
 *   POST termin.php (JSON)                      → Termin buchen, Antwort {nr, termin}
 *
 * Termine werden als Anfrage gespeichert (inc/anfragen.php, Quelle „Terminbuchung“)
 * und erscheinen in /admin/anfragen.php. Ein Termin mit Status „Kein Auftrag“
 * gibt die Zeit wieder frei; Löschen ebenso.
 */

declare(strict_types=1);

require_once __DIR__ . '/inc/anfragen.php';

header('Content-Type: application/json; charset=UTF-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

function aus(array $d, int $code = 200): void
{
    http_response_code($code);
    echo json_encode($d, JSON_UNESCAPED_UNICODE);
    exit;
}

$art = (string) ($_GET['art'] ?? 'telefon');
if (!isset(ANF_TERMIN_ARTEN[$art])) $art = 'telefon';

// ─── Abfragen ──────────────────────────────────────────────────────────
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'GET') {
    if (isset($_GET['tage'])) {
        $liste = [];
        for ($i = 1; $i <= ANF_TERMIN_TAGE; $i++) {
            $tag = date('Y-m-d', strtotime("+$i day"));
            $liste[] = ['tag' => $tag, 'frei' => count(anf_termin_frei($tag, $art))];
        }
        aus(['tage' => $liste]);
    }
    $tag = (string) ($_GET['tag'] ?? '');
    aus(['zeiten' => array_map(static fn($t) => date('H:i', $t), anf_termin_frei($tag, $art))]);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') aus(['fehler' => 'Methode'], 405);

// ─── Buchen ────────────────────────────────────────────────────────────
$d = json_decode((string) file_get_contents('php://input'), true);
if (!is_array($d)) aus(['fehler' => 'Ungültige Daten'], 400);
$f = static fn(string $k, int $n = 300): string => is_string($d[$k] ?? null) ? mb_substr(trim(str_replace(["\r", "\0"], '', $d[$k])), 0, $n) : '';

// Spam-Schutz: Honeypot, Mindestzeit, Begrenzung je IP
if ($f('_honey') !== '') aus(['nr' => ''], 200);
if ((int) ($d['_t'] ?? 0) < 3000) aus(['fehler' => 'Bitte kurz warten und erneut senden.'], 429);   // _t = Millisekunden seit Öffnen der Seite
$datei = sys_get_temp_dir() . '/masar_termin_' . md5($_SERVER['REMOTE_ADDR'] ?? 'x') . '.txt';
$jetzt = time();
$zeiten = array_filter(array_map('intval', explode(',', (string) @file_get_contents($datei))), static fn($z) => $z > $jetzt - 3600);
if (count($zeiten) >= 5) aus(['fehler' => 'Zu viele Buchungen. Bitte rufen Sie uns an: 0178 514 3918.'], 429);

$art = $f('art', 20); if (!isset(ANF_TERMIN_ARTEN[$art])) aus(['fehler' => 'Bitte die Art der Beratung wählen.'], 422);
$spr = $f('sprache', 5); if (!isset(ANF_SPRACHEN[$spr])) aus(['fehler' => 'Bitte eine Sprache wählen.'], 422);
$name = $f('name', 120); if (mb_strlen($name) < 2) aus(['fehler' => 'Bitte Ihren Namen angeben.'], 422);
$tel = $f('telefon', 60); if (strlen(preg_replace('/\D/', '', $tel) ?? '') < 6) aus(['fehler' => 'Bitte eine Telefonnummer angeben.'], 422);
$mail = $f('email', 160); if ($mail !== '' && !filter_var($mail, FILTER_VALIDATE_EMAIL)) aus(['fehler' => 'Die E-Mail-Adresse ist ungültig.'], 422);
$adr = $f('adresse', 200);
if ($art === 'vorort') {
    if (!preg_match('/\b(1[0-4]\d{3})\b/', $adr, $m) || (int) $m[1] < 10115 || (int) $m[1] > 14199) {
        aus(['fehler' => 'Termine vor Ort bieten wir nur in Berlin an. Bitte Straße und Berliner PLZ angeben – oder Telefon/Video wählen.'], 422);
    }
}
if (empty($d['consent'])) aus(['fehler' => 'Bitte der Datenschutzerklärung zustimmen.'], 422);
$tag = $f('tag', 10); $uhr = $f('zeit', 5);
$ts = preg_match('/^\d{2}:\d{2}$/', $uhr) ? strtotime($tag . ' ' . $uhr) : false;
if ($ts === false) aus(['fehler' => 'Bitte Tag und Uhrzeit wählen.'], 422);

$db = anf_db(); if (!$db) aus(['fehler' => 'Buchung gerade nicht möglich. Bitte rufen Sie uns an: 0178 514 3918.'], 500);
$thema = $f('thema', 120); $info = $f('nachricht', 1000); $firma = $f('firma', 120);

try {
    $db->exec('BEGIN IMMEDIATE');   // verhindert Doppelbuchungen bei gleichzeitigen Anfragen
    if (!in_array($ts, anf_termin_frei($tag, $art), true)) {
        $db->exec('ROLLBACK');
        aus(['fehler' => 'Diese Uhrzeit ist leider gerade vergeben worden. Bitte eine andere wählen.', 'vergeben' => true], 409);
    }
    $wann = anf_termin_text($ts);
    $text = "Kostenlose Beratung – Termin\n\n"
          . "Termin:   {$wann} (" . anf_termin_dauer($art) . " Min.)\n"
          . "Art:      " . ANF_TERMIN_ARTEN[$art] . "\n"
          . "Sprache:  " . ANF_SPRACHEN[$spr] . "\n"
          . ($art === 'vorort' ? "Adresse:  {$adr}\n" : '')
          . ($thema !== '' ? "Thema:    {$thema}\n" : '')
          . "\nName:     {$name}" . ($firma !== '' ? " ({$firma})" : '') . "\nTelefon:  {$tel}\n" . ($mail !== '' ? "E-Mail:   {$mail}\n" : '')
          . ($info !== '' ? "\nNachricht:\n{$info}\n" : '');
    $nr = anf_speichern([
        'quelle' => 'Terminbuchung', 'seite' => 'https://masar-werbeagentur.de/termin.html',
        'name' => $name, 'firma' => $firma, 'email' => $mail, 'telefon' => $tel,
        'ort' => $art === 'vorort' ? $adr : ($f('ort', 120) !== '' ? $f('ort', 120) : ''),
        'leistung' => 'Beratung' . ($thema !== '' ? ': ' . $thema : ''), 'zusammenfassung' => $text,
        'daten' => ['Termin' => $wann, 'Art' => ANF_TERMIN_ARTEN[$art], 'Sprache' => ANF_SPRACHEN[$spr], 'Adresse' => $adr, 'Thema' => $thema],
        'termin' => $ts, 'termin_dauer' => anf_termin_dauer($art), 'termin_art' => ANF_TERMIN_ARTEN[$art], 'sprache' => ANF_SPRACHEN[$spr],
    ]);
    $db->exec('COMMIT');
} catch (Throwable $e) {
    try { $db->exec('ROLLBACK'); } catch (Throwable $e2) {}
    error_log('Terminbuchung: ' . $e->getMessage());
    aus(['fehler' => 'Buchung gerade nicht möglich. Bitte rufen Sie uns an: 0178 514 3918.'], 500);
}
if ($nr === '') aus(['fehler' => 'Buchung gerade nicht möglich. Bitte rufen Sie uns an: 0178 514 3918.'], 500);

$zeiten[] = $jetzt;
@file_put_contents($datei, implode(',', $zeiten), LOCK_EX);

// E-Mail an uns
anf_mail('info@masar-werbeagentur.de', "[{$nr}] Beratungstermin {$wann} – " . ANF_TERMIN_ARTEN[$art] . ', ' . ANF_SPRACHEN[$spr],
    "Anfragenummer: {$nr}\n\n" . $text . "\nÜbersicht: https://masar-werbeagentur.de/admin/anfragen.php?nr=" . rawurlencode($nr) . "\n", $mail);

// Bestätigung an den Kunden (Deutsch + gewählte Sprache)
if ($mail !== '') {
    $wie = ['telefon' => 'Wir rufen Sie zum Termin unter ' . $tel . ' an.',
            'video'   => 'Wir rufen Sie zum Termin per WhatsApp-Video unter ' . $tel . ' an.',
            'vorort'  => 'Wir kommen zum Termin zu Ihnen: ' . $adr . '.'][$art];
    $extra = [
        'en' => "Your free consultation is booked for {$wann} (Berlin time). Reference: {$nr}. To change or cancel, simply reply to this e-mail or message us on WhatsApp.",
        'ar' => "تم حجز موعد الاستشارة المجانية: {$wann} (بتوقيت برلين). رقم الحجز: {$nr}. لتغيير الموعد أو إلغائه يكفي الرد على هذه الرسالة أو مراسلتنا على واتساب.",
        'tr' => "Ücretsiz danışmanlık randevunuz: {$wann} (Berlin saati). Randevu numarası: {$nr}. Değiştirmek veya iptal etmek için bu e-postayı yanıtlamanız ya da bize WhatsApp'tan yazmanız yeterli.",
    ][$spr] ?? '';
    anf_mail($mail, "Ihr Beratungstermin am {$wann} – Masar Werbeagentur",
        "Guten Tag {$name},\n\nvielen Dank! Ihre kostenlose Beratung ist gebucht:\n\n"
        . "  {$wann} (" . anf_termin_dauer($art) . " Min.)\n  " . ANF_TERMIN_ARTEN[$art] . ' · ' . ANF_SPRACHEN[$spr] . "\n  Terminnummer: {$nr}\n\n"
        . $wie . "\n\nSie möchten den Termin verschieben oder absagen? Antworten Sie einfach auf diese E-Mail "
        . "oder schreiben Sie uns per WhatsApp: https://wa.me/491785143918\n\n"
        . ($extra !== '' ? $extra . "\n\n" : '')
        . "Mit freundlichen Grüßen\nMasar Werbeagentur\nBristolstraße 19E · 13349 Berlin · 0178 514 3918\nhttps://masar-werbeagentur.de\n");
}

aus(['nr' => $nr, 'termin' => $wann, 'start' => date('c', $ts), 'dauer' => anf_termin_dauer($art)]);
