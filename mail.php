<?php
/**
 * Masar Werbeagentur — Secure Mail Handler
 * Handles multi-step briefing form (app.js) + file attachments
 * Hostinger PHP 8.x compatible
 */

declare(strict_types=1);

// ─── CONFIG ───────────────────────────────────────────────────────────────────
const RECIPIENT_EMAIL  = 'amjadbalili97@gmail.com';
const RECIPIENT_NAME   = 'Masar Werbeagentur';
const FROM_EMAIL       = 'noreply@masar-werbeagentur.de';
const FROM_NAME        = 'Masar Werbeagentur Kontaktformular';
const MAX_UPLOAD_BYTES = 5 * 1024 * 1024; // 5 MB
const ALLOWED_TYPES    = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf'];
const RATE_LIMIT_FILE  = '/tmp/masar_rl_';
const RATE_LIMIT_MAX   = 5;   // max submissions per window
const RATE_LIMIT_WIN   = 300; // 5-minute window (seconds)

// ─── HEADERS ──────────────────────────────────────────────────────────────────
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

// ─── HELPERS ──────────────────────────────────────────────────────────────────
function json_out(string $status, string $message = ''): never {
    echo json_encode(['status' => $status, 'message' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

function sanitize(string $input, int $max = 500): string {
    return mb_substr(strip_tags(trim($input)), 0, $max);
}

function is_valid_email(string $email): bool {
    return (bool) filter_var($email, FILTER_VALIDATE_EMAIL);
}

// ─── METHOD CHECK ──────────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_out('error', 'Methode nicht erlaubt.');
}

// ─── ORIGIN CHECK ─────────────────────────────────────────────────────────────
$allowed_origins = ['https://masar-werbeagentur.de', 'https://www.masar-werbeagentur.de'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin && !in_array($origin, $allowed_origins, true)) {
    http_response_code(403);
    json_out('error', 'Nicht erlaubter Ursprung.');
}

// ─── RATE LIMITING (IP-based, file-based) ─────────────────────────────────────
$ip_hash = hash('sha256', ($_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR']));
$rl_file = RATE_LIMIT_FILE . $ip_hash;
$now     = time();
$hits    = [];

if (file_exists($rl_file)) {
    $hits = array_filter(
        (array) json_decode(file_get_contents($rl_file), true),
        fn($t) => ($now - $t) < RATE_LIMIT_WIN
    );
}

if (count($hits) >= RATE_LIMIT_MAX) {
    http_response_code(429);
    json_out('error', 'Zu viele Anfragen. Bitte warten Sie einige Minuten.');
}

$hits[] = $now;
if (file_put_contents($rl_file, json_encode(array_values($hits))) === false) {
    error_log('[Masar] Rate-limit write failed for IP hash: ' . substr($ip_hash, 0, 16));
}

// ─── HONEYPOT ─────────────────────────────────────────────────────────────────
if (!empty($_POST['website'])) {
    json_out('error', 'Spam erkannt.');
}

// ─── READ & VALIDATE FIELDS ───────────────────────────────────────────────────
$name     = sanitize($_POST['name']     ?? $_POST['fieldName'] ?? '');
$email    = sanitize($_POST['email']    ?? '', 254);
$phone    = sanitize($_POST['telefon']  ?? $_POST['phone'] ?? '', 50);
$service  = sanitize($_POST['leistung'] ?? $_POST['fieldService'] ?? $_POST['service'] ?? '');
$message  = sanitize($_POST['nachricht'] ?? $_POST['message'] ?? '', 2000);
$company  = sanitize($_POST['company']  ?? $_POST['firma'] ?? '', 200);
$budget   = sanitize($_POST['budget']   ?? '', 100);
$estimate = sanitize($_POST['estimate'] ?? '', 200);
$step_data = sanitize($_POST['step_data'] ?? '', 1000);

if ($name === '') {
    json_out('error', 'Bitte geben Sie Ihren Namen an.');
}
if (!is_valid_email($email)) {
    json_out('error', 'Bitte geben Sie eine gültige E-Mail-Adresse an.');
}
if ($service === '') {
    json_out('error', 'Bitte wählen Sie eine Leistung aus.');
}

// ─── FILE UPLOAD ──────────────────────────────────────────────────────────────
$attachment_data = null;
$attachment_name = null;
$attachment_type = null;

if (!empty($_FILES['attachment']) && $_FILES['attachment']['error'] !== UPLOAD_ERR_NO_FILE) {
    $file = $_FILES['attachment'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        json_out('error', 'Fehler beim Datei-Upload (Code: ' . $file['error'] . ').');
    }
    if ($file['size'] > MAX_UPLOAD_BYTES) {
        json_out('error', 'Datei zu groß. Maximale Dateigröße: 5 MB.');
    }

    // Verify MIME type via finfo (not just extension)
    $finfo    = new finfo(FILEINFO_MIME_TYPE);
    $detected = $finfo->file($file['tmp_name']);

    if (!in_array($detected, ALLOWED_TYPES, true)) {
        json_out('error', 'Dateityp nicht erlaubt. Erlaubt: JPG, PNG, GIF, WebP, PDF.');
    }

    $attachment_data = chunk_split(base64_encode(file_get_contents($file['tmp_name'])));
    $attachment_name = preg_replace('/[^a-zA-Z0-9._\-]/', '_', basename($file['name']));
    $attachment_type = $detected;
}

// ─── BUILD EMAIL ───────────────────────────────────────────────────────────────
$boundary = '----=_Part_' . md5(uniqid('masar', true));
$date_str  = date('d.m.Y \u\m H:i \U\h\r');

$body_rows = [
    ['Name',        $name],
    ['E-Mail',      $email],
    ['Telefon',     $phone ?: '—'],
    ['Unternehmen', $company ?: '—'],
    ['Leistung',    $service],
    ['Budget',      $budget ?: '—'],
    ['Preisschätzung', $estimate ?: '—'],
    ['Nachricht',   nl2br(htmlspecialchars($message, ENT_QUOTES, 'UTF-8'))],
    ['Datum',       $date_str],
    ['IP (Hash)',   substr($ip_hash, 0, 16) . '...'],
];

$table_html = '<table style="font-family:Arial,sans-serif;border-collapse:collapse;width:100%;">';
foreach ($body_rows as [$label, $value]) {
    if ($value === '') continue;
    $table_html .= '<tr>'
        . '<td style="padding:10px 14px;background:#f5f8f8;font-weight:700;color:#132e50;white-space:nowrap;border:1px solid #e2ecec;width:30%;">' . htmlspecialchars($label) . '</td>'
        . '<td style="padding:10px 14px;border:1px solid #e2ecec;color:#1a2a2a;">' . $value . '</td>'
        . '</tr>';
}
$table_html .= '</table>';

$html_body = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>'
    . '<div style="max-width:640px;margin:0 auto;font-family:Arial,sans-serif;">'
    . '<div style="background:#132e50;padding:28px 32px;border-radius:8px 8px 0 0;">'
    . '<h1 style="color:#58d0bd;margin:0;font-size:22px;font-weight:900;letter-spacing:1px;">MASAR WERBEAGENTUR</h1>'
    . '<p style="color:rgba(255,255,255,.6);margin:6px 0 0;font-size:14px;">Neue Projektanfrage – ' . $date_str . '</p>'
    . '</div>'
    . '<div style="background:#fff;padding:28px 32px;border:1px solid #e2ecec;border-top:none;">'
    . '<h2 style="color:#132e50;margin:0 0 20px;font-size:18px;">Anfrage-Details</h2>'
    . $table_html
    . '<div style="margin-top:24px;padding:16px;background:#f5f8f8;border-radius:6px;font-size:13px;color:#5a7070;">'
    . 'Diese Nachricht wurde über das Kontaktformular auf masar-werbeagentur.de gesendet.'
    . '</div>'
    . '</div>'
    . '<div style="padding:16px 32px;text-align:center;font-size:12px;color:#9a9a9a;">'
    . '© 2026 Masar Werbeagentur · Amjad Albill · Berlin'
    . '</div>'
    . '</div></body></html>';

$plain_body = "Neue Anfrage – Masar Werbeagentur\n"
    . str_repeat('-', 40) . "\n"
    . "Name:           {$name}\n"
    . "E-Mail:         {$email}\n"
    . "Telefon:        " . ($phone ?: '—') . "\n"
    . "Unternehmen:    " . ($company ?: '—') . "\n"
    . "Leistung:       {$service}\n"
    . "Budget:         " . ($budget ?: '—') . "\n"
    . "Preisschätzung: " . ($estimate ?: '—') . "\n"
    . "Nachricht:\n{$message}\n"
    . str_repeat('-', 40) . "\n"
    . "Gesendet am: {$date_str}\n";

// ─── HEADERS & MIME ───────────────────────────────────────────────────────────
$subject = '=?UTF-8?B?' . base64_encode("Neue Anfrage von {$name} – Masar Werbeagentur") . '?=';

$headers  = "From: =?UTF-8?B?" . base64_encode(FROM_NAME) . "?= <" . FROM_EMAIL . ">\r\n";
$headers .= "Reply-To: =?UTF-8?B?" . base64_encode($name) . "?= <{$email}>\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "X-Mailer: Masar-PHP-Mailer/1.0\r\n";
$headers .= "X-Priority: 1\r\n";

if ($attachment_data) {
    $headers .= "Content-Type: multipart/mixed; boundary=\"{$boundary}\"\r\n";
    $mail_body  = "--{$boundary}\r\n";
    $mail_body .= "Content-Type: multipart/alternative; boundary=\"alt_{$boundary}\"\r\n\r\n";
    $mail_body .= "--alt_{$boundary}\r\n";
    $mail_body .= "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n";
    $mail_body .= $plain_body . "\r\n";
    $mail_body .= "--alt_{$boundary}\r\n";
    $mail_body .= "Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n";
    $mail_body .= $html_body . "\r\n";
    $mail_body .= "--alt_{$boundary}--\r\n";
    $mail_body .= "--{$boundary}\r\n";
    $mail_body .= "Content-Type: {$attachment_type}; name=\"{$attachment_name}\"\r\n";
    $mail_body .= "Content-Disposition: attachment; filename=\"{$attachment_name}\"\r\n";
    $mail_body .= "Content-Transfer-Encoding: base64\r\n\r\n";
    $mail_body .= $attachment_data . "\r\n";
    $mail_body .= "--{$boundary}--";
} else {
    $headers .= "Content-Type: multipart/alternative; boundary=\"{$boundary}\"\r\n";
    $mail_body  = "--{$boundary}\r\n";
    $mail_body .= "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n";
    $mail_body .= $plain_body . "\r\n";
    $mail_body .= "--{$boundary}\r\n";
    $mail_body .= "Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n";
    $mail_body .= $html_body . "\r\n";
    $mail_body .= "--{$boundary}--";
}

// ─── SEND ─────────────────────────────────────────────────────────────────────
$sent = mail(RECIPIENT_EMAIL, $subject, $mail_body, $headers);

if (!$sent) {
    error_log('[Masar] mail() failed for: ' . $email);
    json_out('error', 'E-Mail konnte nicht gesendet werden. Bitte versuchen Sie es später erneut oder rufen Sie uns an.');
}

// ─── AUTO-REPLY ───────────────────────────────────────────────────────────────
$ar_subject = '=?UTF-8?B?' . base64_encode('Ihre Anfrage bei Masar Werbeagentur Berlin') . '?=';
$ar_headers  = "From: =?UTF-8?B?" . base64_encode(RECIPIENT_NAME) . "?= <" . FROM_EMAIL . ">\r\n";
$ar_headers .= "MIME-Version: 1.0\r\n";
$ar_headers .= "Content-Type: text/html; charset=UTF-8\r\n";
$ar_body = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>'
    . '<div style="max-width:580px;margin:0 auto;font-family:Arial,sans-serif;">'
    . '<div style="background:#132e50;padding:24px 28px;border-radius:8px 8px 0 0;">'
    . '<h1 style="color:#58d0bd;margin:0;font-size:20px;">MASAR WERBEAGENTUR</h1>'
    . '</div>'
    . '<div style="padding:28px;border:1px solid #e2ecec;border-top:none;background:#fff;">'
    . "<p style='color:#132e50;font-size:16px;'>Hallo {$name},</p>"
    . '<p style="color:#5a7070;line-height:1.8;">vielen Dank für Ihre Anfrage! Wir haben Ihre Nachricht erhalten und werden uns <strong>innerhalb von 24 Stunden (Mo–Fr)</strong> bei Ihnen melden.</p>'
    . '<p style="color:#5a7070;line-height:1.8;">Individuelle Angebote sind ab Ausstellungsdatum <strong>14 Kalendertage gültig</strong>.</p>'
    . '<p style="color:#5a7070;line-height:1.8;">Bei dringenden Fragen erreichen Sie uns direkt:</p>'
    . '<p style="margin:20px 0;">'
    . '<a href="tel:01785143918" style="background:#58d0bd;color:#132e50;padding:12px 24px;border-radius:6px;font-weight:700;text-decoration:none;display:inline-block;">📞 0178 514 3918</a>'
    . '</p>'
    . '<p style="color:#9a9a9a;font-size:13px;margin-top:24px;">Mit freundlichen Grüßen<br><strong style="color:#132e50;">Amjad Albill</strong><br>Masar Werbeagentur · Berlin-Wedding</p>'
    . '</div>'
    . '<div style="padding:12px;text-align:center;font-size:11px;color:#bbb;">© 2026 Masar Werbeagentur · masar-werbeagentur.de</div>'
    . '</div></body></html>';

mail($email, $ar_subject, $ar_body, $ar_headers);

json_out('success', 'Ihre Anfrage wurde erfolgreich gesendet. Wir melden uns innerhalb von 24 Stunden!');
