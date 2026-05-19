<?php
// ═══ MASAR PRINT SHOP — CHECKOUT HANDLER ═══
// Accepts POST from /shop/checkout.html
// Returns JSON response

declare(strict_types=1);

// ── Headers ──────────────────────────────────────────────────
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

// ── Load config ───────────────────────────────────────────────
$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Serverkonfiguration fehlt.']);
    exit;
}
require $configPath;

// ── Helper: JSON error response ───────────────────────────────
function jsonError(string $msg, int $code = 400): never {
    http_response_code($code);
    echo json_encode(['success' => false, 'error' => $msg]);
    exit;
}

// ── Only allow POST ───────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonError('Nur POST-Anfragen erlaubt.', 405);
}

// ── CSRF-like: verify Referer contains our domain ─────────────
$referer = $_SERVER['HTTP_REFERER'] ?? '';
$allowed = parse_url(SITE_URL, PHP_URL_HOST) ?: 'masar-werbeagentur.de';
if (!str_contains($referer, $allowed) && !str_contains($referer, 'localhost') && !str_contains($referer, '127.0.0.1')) {
    jsonError('Ungültige Anfrage-Herkunft.', 403);
}

// ── Sanitize helper ───────────────────────────────────────────
function sanitize(string $val): string {
    return htmlspecialchars(strip_tags(trim($val)), ENT_QUOTES, 'UTF-8');
}

// ── Collect & validate required fields ───────────────────────
$required = ['name', 'email', 'company', 'phone', 'address', 'product_id', 'product_name', 'quantity', 'unit_price', 'total_price', 'payment_method'];
// Stripe orders must use create-checkout-session.php — this handler is bank-transfer only
foreach ($required as $field) {
    if (empty($_POST[$field])) {
        jsonError("Pflichtfeld fehlt: {$field}");
    }
}

$name           = sanitize($_POST['name']);
$email          = sanitize($_POST['email']);
$company        = sanitize($_POST['company']);
$phone          = sanitize($_POST['phone']);
$address        = sanitize($_POST['address']);
$productId      = sanitize($_POST['product_id']);
$productName    = sanitize($_POST['product_name']);
$productOptions = sanitize($_POST['product_options'] ?? '');
$notes          = sanitize($_POST['notes'] ?? '');
$paymentMethod  = sanitize($_POST['payment_method']);

// Strip CR/LF from header-injectable fields
$name  = str_replace(["\r", "\n"], ' ', $name);
$email = str_replace(["\r", "\n"], '',  $email);

// Validate email
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    jsonError('Ungültige E-Mail-Adresse.');
}

// Only bank transfer handled here; Stripe orders use create-checkout-session.php
if ($paymentMethod !== 'bank') {
    jsonError('Ungültige Zahlungsart.');
}

// Validate numeric fields
$quantity   = (int)$_POST['quantity'];
$unitPrice  = (float)$_POST['unit_price'];
$totalPrice = (float)$_POST['total_price'];

if ($quantity < 1) jsonError('Ungültige Menge.');
if ($unitPrice <= 0 || $totalPrice <= 0) jsonError('Ungültiger Preis.');

// ── File upload (required) ────────────────────────────────────
if (!isset($_FILES['print_file']) || $_FILES['print_file']['error'] === UPLOAD_ERR_NO_FILE) {
    jsonError('Druckdatei fehlt. Bitte eine PDF oder Bilddatei hochladen.');
}

$file = $_FILES['print_file'];

if ($file['error'] !== UPLOAD_ERR_OK) {
    $uploadErrors = [
        UPLOAD_ERR_INI_SIZE   => 'Datei überschreitet maximale Upload-Größe (Server).',
        UPLOAD_ERR_FORM_SIZE  => 'Datei überschreitet maximale Upload-Größe (Formular).',
        UPLOAD_ERR_PARTIAL    => 'Datei nur teilweise hochgeladen.',
        UPLOAD_ERR_NO_TMP_DIR => 'Temporäres Verzeichnis fehlt.',
        UPLOAD_ERR_CANT_WRITE => 'Datei konnte nicht geschrieben werden.',
        UPLOAD_ERR_EXTENSION  => 'Upload durch PHP-Extension blockiert.',
    ];
    jsonError($uploadErrors[$file['error']] ?? 'Unbekannter Upload-Fehler.');
}

// Check file size
$maxBytes = MAX_FILE_MB * 1024 * 1024;
if ($file['size'] > $maxBytes) {
    jsonError('Datei zu groß. Maximum: ' . MAX_FILE_MB . ' MB.');
}

// Validate MIME type with finfo (not just extension)
$allowedMimes = [
    'application/pdf',
    'image/webp',
    'image/png',
    'image/jpeg',
    // SVG excluded: can contain embedded JavaScript (XSS risk)
];

// Blocked / dangerous MIME types
$blockedMimes = [
    'application/x-php',
    'application/php',
    'text/x-php',
    'application/x-httpd-php',
    'application/x-httpd-php-source',
    'application/x-sh',
    'application/x-csh',
    'application/x-perl',
    'application/x-python',
    'text/html',
    'application/javascript',
];

if (function_exists('finfo_open')) {
    $finfo    = finfo_open(FILEINFO_MIME_TYPE);
    $mimeType = finfo_file($finfo, $file['tmp_name']);
    finfo_close($finfo);
} else {
    $mimeType = mime_content_type($file['tmp_name']) ?: 'application/octet-stream';
}

if (in_array($mimeType, $blockedMimes, true)) {
    jsonError('Dieser Dateityp ist aus Sicherheitsgründen nicht erlaubt.');
}

if (!in_array($mimeType, $allowedMimes, true)) {
    jsonError("Nicht unterstützter Dateityp: {$mimeType}. Erlaubt: PDF, WebP, PNG, JPEG.");
}

// Ensure UPLOAD_DIR exists
if (!is_dir(UPLOAD_DIR)) {
    if (!mkdir(UPLOAD_DIR, 0750, true)) {
        jsonError('Upload-Verzeichnis konnte nicht erstellt werden.', 500);
    }
}

// Generate safe filename
$uuid         = sprintf('%s-%s-%s-%s-%s',
    bin2hex(random_bytes(4)),
    bin2hex(random_bytes(2)),
    bin2hex(random_bytes(2)),
    bin2hex(random_bytes(2)),
    bin2hex(random_bytes(6))
);
$originalName = basename($file['name']);
$extension    = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));
// Double-check extension against MIME
$mimeExtMap = [
    'application/pdf'  => 'pdf',
    'image/webp'       => 'webp',
    'image/png'        => 'png',
    'image/jpeg'       => 'jpg',
];
$safeExt    = $mimeExtMap[$mimeType] ?? $extension;
$storedName = $uuid . '.' . $safeExt;
$destPath   = UPLOAD_DIR . $storedName;

if (!move_uploaded_file($file['tmp_name'], $destPath)) {
    jsonError('Datei konnte nicht gespeichert werden.', 500);
}

// Set restrictive permissions on the uploaded file
chmod($destPath, 0640);

// ── Generate order number ─────────────────────────────────────
$orderNumber = 'MSP-' . date('Ymd') . '-' . strtoupper(substr(uniqid(), -6));

// ── Open SQLite and insert order ──────────────────────────────
try {
    $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL;');
    $pdo->exec('PRAGMA foreign_keys=ON;');
} catch (PDOException $e) {
    @unlink($destPath);
    jsonError('Datenbankfehler. Bitte versuchen Sie es erneut.', 500);
}

// Bank transfer orders always start as pending
$paymentStatus = 'pending';

try {
    $stmt = $pdo->prepare("
        INSERT INTO orders (
            order_number, customer_name, customer_email, customer_company,
            customer_phone, customer_address, product_name, product_options,
            quantity, unit_price, total_price, payment_method, payment_status,
            order_status, file_path, file_original_name, notes
        ) VALUES (
            :order_number, :customer_name, :customer_email, :customer_company,
            :customer_phone, :customer_address, :product_name, :product_options,
            :quantity, :unit_price, :total_price, :payment_method, :payment_status,
            'Eingegangen', :file_path, :file_original_name, :notes
        )
    ");

    $stmt->execute([
        ':order_number'       => $orderNumber,
        ':customer_name'      => $name,
        ':customer_email'     => $email,
        ':customer_company'   => $company,
        ':customer_phone'     => $phone,
        ':customer_address'   => $address,
        ':product_name'       => $productName,
        ':product_options'    => $productOptions,
        ':quantity'           => $quantity,
        ':unit_price'         => $unitPrice,
        ':total_price'        => $totalPrice,
        ':payment_method'     => $paymentMethod,
        ':payment_status'     => $paymentStatus,
        ':file_path'          => $storedName,
        ':file_original_name' => $originalName,
        ':notes'              => $notes,
    ]);
} catch (PDOException $e) {
    @unlink($destPath);
    jsonError('Bestellung konnte nicht gespeichert werden. Bitte versuchen Sie es erneut.', 500);
}

// ── Format price helper ───────────────────────────────────────
function fmtEur(float $n): string {
    return number_format($n, 2, ',', '.') . ' €';
}

// ── Send customer confirmation email ─────────────────────────
$bankSection = '';
if ($paymentMethod === 'bank') {
    $bankSection = "
<div style='background:#f0f7f5;border-left:4px solid #58d0bd;padding:1.2rem 1.5rem;border-radius:0 8px 8px 0;margin:1.5rem 0;'>
  <strong style='color:#132e50;display:block;margin-bottom:.8rem;font-size:15px;'>Bankverbindung für Ihre Überweisung</strong>
  <table style='font-size:14px;color:#1a2a2a;border-collapse:collapse;'>
    <tr><td style='padding:3px 16px 3px 0;color:#5a7070;white-space:nowrap;'>Empfänger</td><td><strong>" . BANK_NAME . "</strong></td></tr>
    <tr><td style='padding:3px 16px 3px 0;color:#5a7070;'>IBAN</td><td><strong style='letter-spacing:1px;'>" . BANK_IBAN . "</strong></td></tr>
    <tr><td style='padding:3px 16px 3px 0;color:#5a7070;'>BIC</td><td><strong>" . BANK_BIC . "</strong></td></tr>
    <tr><td style='padding:3px 16px 3px 0;color:#5a7070;'>Verwendungszweck</td><td><strong style='color:#132e50;'>{$orderNumber}</strong></td></tr>
    <tr><td style='padding:3px 16px 3px 0;color:#5a7070;'>Betrag</td><td><strong style='font-size:16px;color:#132e50;'>" . fmtEur($totalPrice) . "</strong></td></tr>
  </table>
</div>
<p style='color:#5a7070;font-size:13px;'>Bitte geben Sie die Bestellnummer <strong>{$orderNumber}</strong> als Verwendungszweck an. Nach Zahlungseingang beginnen wir sofort mit der Produktion.</p>";
}

$customerEmailHtml = "<!DOCTYPE html>
<html lang='de'>
<head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head>
<body style='margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f4f7f7;'>
<div style='max-width:600px;margin:30px auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08);'>
  <div style='background:linear-gradient(135deg,#0a1628,#132e50);padding:2rem 2rem 1.5rem;text-align:center;'>
    <div style='font-family:Arial Black,sans-serif;font-size:26px;font-weight:900;color:#fff;letter-spacing:3px;margin-bottom:.3rem;'>MASAR</div>
    <div style='color:#58d0bd;font-size:12px;letter-spacing:2px;text-transform:uppercase;'>Print Shop Bestellbestätigung</div>
  </div>
  <div style='padding:2rem;'>
    <h2 style='color:#132e50;font-size:20px;margin:0 0 .5rem;'>Vielen Dank für Ihre Bestellung!</h2>
    <p style='color:#5a7070;margin:0 0 1.5rem;'>Hallo <strong style='color:#132e50;'>{$name}</strong>, wir haben Ihre Bestellung erhalten und werden sie schnellstmöglich bearbeiten.</p>

    <div style='background:#f4f7f7;border-radius:8px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;'>
      <div style='font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#5a7070;margin-bottom:.5rem;'>Bestellnummer</div>
      <div style='font-size:22px;font-weight:900;color:#132e50;letter-spacing:2px;'>{$orderNumber}</div>
    </div>

    <table style='width:100%;border-collapse:collapse;font-size:14px;margin-bottom:1.5rem;'>
      <tr style='background:#132e50;color:#fff;'>
        <th style='padding:10px 12px;text-align:left;border-radius:6px 0 0 0;'>Produkt</th>
        <th style='padding:10px 12px;text-align:center;'>Menge</th>
        <th style='padding:10px 12px;text-align:right;border-radius:0 6px 0 0;'>Betrag</th>
      </tr>
      <tr style='border-bottom:1px solid #e0eaea;'>
        <td style='padding:12px;color:#1a2a2a;'>
          <strong>{$productName}</strong><br>
          <span style='color:#5a7070;font-size:12px;'>{$productOptions}</span>
        </td>
        <td style='padding:12px;text-align:center;color:#5a7070;'>{$quantity} Stk.</td>
        <td style='padding:12px;text-align:right;font-weight:700;color:#132e50;'>" . fmtEur($totalPrice) . "</td>
      </tr>
      <tr style='background:#f4f7f7;'>
        <td colspan='2' style='padding:12px;font-weight:700;color:#132e50;'>Gesamtbetrag (inkl. MwSt.)</td>
        <td style='padding:12px;text-align:right;font-size:18px;font-weight:900;color:#58d0bd;'>" . fmtEur($totalPrice) . "</td>
      </tr>
    </table>

    {$bankSection}

    <div style='border:1px solid #e0eaea;border-radius:8px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;'>
      <strong style='color:#132e50;display:block;margin-bottom:.8rem;'>Lieferdetails</strong>
      <table style='font-size:13px;color:#5a7070;border-collapse:collapse;'>
        <tr><td style='padding:3px 16px 3px 0;white-space:nowrap;'>Firma</td><td><strong style='color:#1a2a2a;'>{$company}</strong></td></tr>
        <tr><td style='padding:3px 16px 3px 0;'>Name</td><td style='color:#1a2a2a;'>{$name}</td></tr>
        <tr><td style='padding:3px 16px 3px 0;'>E-Mail</td><td style='color:#1a2a2a;'>{$email}</td></tr>
        <tr><td style='padding:3px 16px 3px 0;'>Telefon</td><td style='color:#1a2a2a;'>{$phone}</td></tr>
        <tr><td style='padding:3px 16px 3px 0;'>Adresse</td><td style='color:#1a2a2a;'>" . nl2br($address) . "</td></tr>
      </table>
    </div>

    <p style='font-size:13px;color:#5a7070;'>Bei Fragen erreichen Sie uns unter <a href='mailto:" . ADMIN_EMAIL . "' style='color:#58d0bd;'>" . ADMIN_EMAIL . "</a> oder <a href='https://wa.me/491785143918' style='color:#58d0bd;'>WhatsApp</a>.</p>
  </div>
  <div style='background:#0a1628;padding:1.2rem 2rem;text-align:center;'>
    <p style='color:rgba(255,255,255,.35);font-size:12px;margin:0;'>Masar Werbeagentur · Bristolstraße 19HN · 13349 Berlin · <a href='https://masar-werbeagentur.de' style='color:#58d0bd;'>masar-werbeagentur.de</a></p>
  </div>
</div>
</body></html>";

// ── Send admin notification email ─────────────────────────────
$adminEmailHtml = "<!DOCTYPE html>
<html lang='de'>
<head><meta charset='UTF-8'></head>
<body style='font-family:Arial,sans-serif;background:#f4f7f7;margin:0;padding:0;'>
<div style='max-width:600px;margin:30px auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08);'>
  <div style='background:#132e50;padding:1.5rem 2rem;'>
    <div style='font-size:13px;letter-spacing:2px;text-transform:uppercase;color:#58d0bd;'>Neue Bestellung eingegangen</div>
    <div style='font-size:22px;font-weight:900;color:#fff;letter-spacing:2px;margin-top:.3rem;'>{$orderNumber}</div>
  </div>
  <div style='padding:2rem;'>
    <table style='width:100%;border-collapse:collapse;font-size:14px;'>
      <tr><td style='padding:8px 0;color:#5a7070;width:140px;vertical-align:top;'>Kunde</td><td style='padding:8px 0;font-weight:700;color:#132e50;'>{$name} ({$company})</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>E-Mail</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'><a href='mailto:{$email}' style='color:#58d0bd;'>{$email}</a></td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Telefon</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>{$phone}</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Adresse</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>" . nl2br($address) . "</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Produkt</td><td style='padding:8px 0;border-top:1px solid #e0eaea;font-weight:700;'>{$productName}</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Optionen</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>{$productOptions}</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Menge</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>{$quantity} Stück</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Gesamtbetrag</td><td style='padding:8px 0;border-top:1px solid #e0eaea;font-size:18px;font-weight:900;color:#58d0bd;'>" . fmtEur($totalPrice) . "</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Zahlung</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>🏦 Vorkasse (Überweisung)</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Druckdatei</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>{$originalName}<br><span style='font-size:12px;color:#5a7070;'>Gespeichert als: {$storedName}</span></td></tr>
      " . ($notes ? "<tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Anmerkungen</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>{$notes}</td></tr>" : '') . "
    </table>
    <div style='margin-top:1.5rem;'>
      <a href='" . SITE_URL . "/admin/dashboard.php' style='background:#58d0bd;color:#132e50;padding:12px 24px;border-radius:6px;font-weight:700;font-size:14px;text-decoration:none;display:inline-block;'>Zum Admin-Dashboard →</a>
    </div>
  </div>
</div>
</body></html>";

// ── Attempt email sending ─────────────────────────────────────
$subjectCustomer = "Ihre Bestellung {$orderNumber} – " . SHOP_NAME;
$subjectAdmin    = "Neue Bestellung: {$orderNumber} – {$name}";

$headers  = "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/html; charset=UTF-8\r\n";
$headers .= "From: " . SHOP_NAME . " <" . SMTP_USER . ">\r\n";
$headers .= "Reply-To: " . SMTP_USER . "\r\n";
$headers .= "X-Mailer: PHP/" . PHP_VERSION . "\r\n";

// Customer email
@mail($email, $subjectCustomer, $customerEmailHtml, $headers);

// Admin notification
$adminHeaders  = "MIME-Version: 1.0\r\n";
$adminHeaders .= "Content-Type: text/html; charset=UTF-8\r\n";
$adminHeaders .= "From: " . SHOP_NAME . " <" . SMTP_USER . ">\r\n";
$adminHeaders .= "Reply-To: {$email}\r\n";
@mail(ADMIN_EMAIL, $subjectAdmin, $adminEmailHtml, $adminHeaders);

// ── Return success ────────────────────────────────────────────
echo json_encode([
    'success'        => true,
    'order_number'   => $orderNumber,
    'payment_method' => $paymentMethod,
    'total_price'    => $totalPrice,
]);
