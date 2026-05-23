<?php
/**
 * Masar Werbeagentur — Secure Mail Handler
 * Handles multi-step briefing form (app.js) + file attachments
 * Hostinger PHP 8.x compatible
 */

declare(strict_types=1);

// ─── CONFIG ───────────────────────────────────────────────────────────────────
const RECIPIENT_EMAIL  = 'info@masar-werbeagentur.de';
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
$allowed_hosts   = ['masar-werbeagentur.de', 'www.masar-werbeagentur.de'];
$origin  = $_SERVER['HTTP_ORIGIN']  ?? '';
$referer = $_SERVER['HTTP_REFERER'] ?? '';

if ($origin !== '') {
    if (!in_array($origin, $allowed_origins, true)) {
        http_response_code(403);
        json_out('error', 'Nicht erlaubter Ursprung.');
    }
} elseif ($referer !== '') {
    $refHost = parse_url($referer, PHP_URL_HOST);
    if (!in_array($refHost, $allowed_hosts, true)) {
        http_response_code(403);
        json_out('error', 'Nicht erlaubter Ursprung.');
    }
}

// ─── RATE LIMITING (IP-based, file-based with flock) ──────────────────────────
$ip_hash = hash('sha256', ($_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR']));
$rl_file = RATE_LIMIT_FILE . $ip_hash;
$now     = time();

// Periodic old-file cleanup (1% chance to avoid overhead)
if (random_int(1, 100) === 1) {
    foreach (glob(RATE_LIMIT_FILE . '*') ?: [] as $f) {
        if (filemtime($f) < $now - 86400) @unlink($f);
    }
}

$fh = fopen($rl_file, 'c+');
if ($fh && flock($fh, LOCK_EX)) {
    fseek($fh, 0);
    $raw  = stream_get_contents($fh);
    $hits = array_values(array_filter(
        (array) json_decode($raw, true),
        fn($t) => is_int($t) && ($now - $t) < RATE_LIMIT_WIN
    ));

    if (count($hits) >= RATE_LIMIT_MAX) {
        flock($fh, LOCK_UN);
        fclose($fh);
        http_response_code(429);
        json_out('error', 'Zu viele Anfragen. Bitte warten Sie einige Minuten.');
    }

    $hits[] = $now;
    ftruncate($fh, 0);
    fseek($fh, 0);
    fwrite($fh, json_encode($hits));
    flock($fh, LOCK_UN);
    fclose($fh);
} else {
    error_log('[Masar] Rate-limit flock failed for IP hash: ' . substr($ip_hash, 0, 16));
}

// ─── HONEYPOT ─────────────────────────────────────────────────────────────────
if (!empty($_POST['website'])) {
    json_out('error', 'Spam erkannt.');
}

// ─── READ & VALIDATE FIELDS ───────────────────────────────────────────────────
$name     = str_replace(["\r", "\n", "\0"], ' ', sanitize($_POST['name'] ?? $_POST['fieldName'] ?? ''));
$email    = str_replace(["\r", "\n", "\0"], '', sanitize($_POST['email'] ?? '', 254));
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
$ar_subject = '=?UTF-8?B?' . base64_encode('✔ Anfrage erhalten – Masar Werbeagentur Berlin') . '?=';
$ar_headers  = "From: =?UTF-8?B?" . base64_encode('Masar Werbeagentur Berlin') . "?= <" . FROM_EMAIL . ">\r\n";
$ar_headers .= "Reply-To: info@masar-werbeagentur.de\r\n";
$ar_headers .= "MIME-Version: 1.0\r\n";
$ar_headers .= "Content-Type: text/html; charset=UTF-8\r\n";
$ar_headers .= "Content-Transfer-Encoding: 8bit\r\n";

$service_esc = htmlspecialchars($service, ENT_QUOTES, 'UTF-8');
$name_esc    = htmlspecialchars($name,    ENT_QUOTES, 'UTF-8');
$date_fmt    = date('d.m.Y');

$ar_body = <<<HTML
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anfrage erhalten</title>
</head>
<body style="margin:0;padding:0;background:#f0f4f8;font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#f0f4f8;padding:40px 16px;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

  <!-- HEADER -->
  <tr>
    <td style="background:linear-gradient(135deg,#0a1628 0%,#132e50 60%,#0d4a4a 100%);border-radius:12px 12px 0 0;padding:36px 40px 28px;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <div style="font-family:Arial Black,Arial,sans-serif;font-weight:900;font-size:26px;color:#fff;letter-spacing:4px;">
              M<span style="color:#58d0bd;">A</span>SAR
            </div>
            <div style="font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(88,208,189,.65);margin-top:4px;">
              Werbeagentur · Berlin
            </div>
          </td>
          <td align="right">
            <div style="background:rgba(88,208,189,.15);border:1px solid rgba(88,208,189,.35);border-radius:20px;padding:6px 16px;display:inline-block;font-size:12px;color:#58d0bd;font-weight:700;">
              ✔ Anfrage eingegangen
            </div>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- GREEN BAR -->
  <tr>
    <td style="background:#58d0bd;height:4px;line-height:4px;font-size:4px;">&nbsp;</td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="background:#ffffff;padding:40px 40px 32px;border-left:1px solid #e2ecec;border-right:1px solid #e2ecec;">

      <p style="margin:0 0 8px;font-size:22px;font-weight:700;color:#0a1628;">Hallo {$name_esc},</p>
      <p style="margin:0 0 24px;font-size:15px;color:#5a7070;line-height:1.7;">
        vielen Dank für Ihre Anfrage! Wir haben Ihre Nachricht erhalten und ein Mitarbeiter wird sich <strong style="color:#132e50;">innerhalb von 24 Stunden (Mo–Fr)</strong> persönlich bei Ihnen melden.
      </p>

      <!-- SUMMARY BOX -->
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fbfb;border:1px solid #e2ecec;border-left:4px solid #58d0bd;border-radius:0 8px 8px 0;margin-bottom:28px;">
        <tr>
          <td style="padding:20px 24px;">
            <p style="margin:0 0 12px;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#58d0bd;">Ihre Anfrage im Überblick</p>
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td style="padding:5px 0;font-size:13px;color:#9aafaf;width:130px;">Gewünschte Leistung</td>
                <td style="padding:5px 0;font-size:13px;font-weight:700;color:#132e50;">{$service_esc}</td>
              </tr>
              <tr>
                <td style="padding:5px 0;font-size:13px;color:#9aafaf;">Eingangsdatum</td>
                <td style="padding:5px 0;font-size:13px;font-weight:700;color:#132e50;">{$date_fmt}</td>
              </tr>
              <tr>
                <td style="padding:5px 0;font-size:13px;color:#9aafaf;">Bearbeitungszeit</td>
                <td style="padding:5px 0;font-size:13px;font-weight:700;color:#132e50;">bis zu 24 Stunden (Mo–Fr)</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <!-- NEXT STEPS -->
      <p style="margin:0 0 16px;font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#132e50;">Was passiert als Nächstes?</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
        <tr>
          <td style="padding:8px 0;vertical-align:top;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="width:32px;height:32px;background:#132e50;border-radius:50%;text-align:center;vertical-align:middle;font-size:13px;font-weight:700;color:#58d0bd;">1</td>
                <td style="padding-left:14px;font-size:14px;color:#3a5050;line-height:1.6;">Wir prüfen Ihre Anfrage und bereiten ein <strong>individuelles Angebot</strong> vor.</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;vertical-align:top;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="width:32px;height:32px;background:#132e50;border-radius:50%;text-align:center;vertical-align:middle;font-size:13px;font-weight:700;color:#58d0bd;">2</td>
                <td style="padding-left:14px;font-size:14px;color:#3a5050;line-height:1.6;">Ein Berater meldet sich per <strong>E-Mail oder Telefon</strong> bei Ihnen.</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:8px 0;vertical-align:top;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="width:32px;height:32px;background:#132e50;border-radius:50%;text-align:center;vertical-align:middle;font-size:13px;font-weight:700;color:#58d0bd;">3</td>
                <td style="padding-left:14px;font-size:14px;color:#3a5050;line-height:1.6;">Nach Freigabe starten wir umgehend mit der <strong>Umsetzung</strong>.</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <!-- URGENT -->
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a1628;border-radius:10px;margin-bottom:8px;">
        <tr>
          <td style="padding:22px 28px;">
            <p style="margin:0 0 14px;font-size:13px;color:rgba(255,255,255,.55);font-weight:700;letter-spacing:1px;text-transform:uppercase;">Dringende Anfrage? Rufen Sie uns direkt an:</p>
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="padding-right:12px;">
                  <a href="tel:01785143918" style="display:inline-block;background:#58d0bd;color:#0a1628;padding:12px 22px;border-radius:6px;font-weight:700;font-size:14px;text-decoration:none;">
                    📞 &nbsp;0178 514 3918
                  </a>
                </td>
                <td>
                  <a href="https://wa.me/491785143918" style="display:inline-block;background:#25d366;color:#fff;padding:12px 22px;border-radius:6px;font-weight:700;font-size:14px;text-decoration:none;">
                    💬 &nbsp;WhatsApp
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

    </td>
  </tr>

  <!-- SIGNATURE -->
  <tr>
    <td style="background:#f8fbfb;border:1px solid #e2ecec;border-top:none;border-radius:0 0 12px 12px;padding:24px 40px;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <p style="margin:0;font-size:14px;color:#5a7070;line-height:1.8;">
              Mit freundlichen Grüßen,<br>
              <strong style="color:#132e50;font-size:15px;">Amjad Albill</strong><br>
              <span style="color:#58d0bd;font-size:12px;">Masar Werbeagentur · Bristolstraße 19HN · 13349 Berlin</span>
            </p>
          </td>
          <td align="right" style="vertical-align:top;">
            <a href="https://masar-werbeagentur.de" style="font-family:Arial Black,Arial,sans-serif;font-weight:900;font-size:18px;color:#132e50;text-decoration:none;letter-spacing:3px;">
              M<span style="color:#58d0bd;">A</span>SAR
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="padding:20px 0;text-align:center;">
      <p style="margin:0 0 8px;font-size:11px;color:#9aafaf;">
        <a href="https://masar-werbeagentur.de" style="color:#58d0bd;text-decoration:none;">masar-werbeagentur.de</a>
        &nbsp;·&nbsp;
        <a href="mailto:info@masar-werbeagentur.de" style="color:#9aafaf;text-decoration:none;">info@masar-werbeagentur.de</a>
        &nbsp;·&nbsp;
        <a href="tel:01785143918" style="color:#9aafaf;text-decoration:none;">0178 514 3918</a>
      </p>
      <p style="margin:0;font-size:10px;color:#c0c8c8;">
        © 2026 Masar Werbeagentur · Amjad Albill · Berlin-Wedding<br>
        Diese E-Mail wurde automatisch versandt. Bitte antworten Sie direkt auf diese E-Mail.
      </p>
    </td>
  </tr>

</table>
</td></tr>
</table>

</body>
</html>
HTML;

mail($email, $ar_subject, $ar_body, $ar_headers);

json_out('success', 'Ihre Anfrage wurde erfolgreich gesendet. Wir melden uns innerhalb von 24 Stunden!');
