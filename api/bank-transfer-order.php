<?php
// ═══ MASAR PRINT SHOP — BANK TRANSFER (VORKASSE) ORDER HANDLER ═══
// Validates the order, saves it to SQLite with status "Pending Payment",
// sends a confirmation email with IBAN to the customer, and notifies the admin.
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

// ── Request method gate ───────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method Not Allowed']);
    exit;
}

// ── Load config & helpers ─────────────────────────────────────
$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Serverkonfiguration fehlt.']);
    exit;
}
require $configPath;
require __DIR__ . '/email-helper.php';

// ── Sanitise & validate input ─────────────────────────────────
$name    = trim(strip_tags($_POST['name']    ?? ''));
$email   = trim($_POST['email']              ?? '');
$company = trim(strip_tags($_POST['company'] ?? ''));
$phone   = trim(strip_tags($_POST['phone']   ?? ''));
$address = trim(strip_tags($_POST['address'] ?? ''));
$product = trim(strip_tags($_POST['product'] ?? ''));
$options = trim(strip_tags($_POST['options'] ?? ''));
$qty     = max(1, (int)($_POST['qty']        ?? 1));
$total   = round((float)($_POST['total']     ?? 0), 2);
$notes   = trim(strip_tags($_POST['notes']   ?? ''));

if (!$name || !filter_var($email, FILTER_VALIDATE_EMAIL) || !$product || $total <= 0) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Pflichtfelder fehlen oder ungültige E-Mail-Adresse.']);
    exit;
}

// ── Handle optional file upload ───────────────────────────────
$filePath         = null;
$fileOriginalName = null;

if (!empty($_FILES['print_file']['name'])) {
    $file     = $_FILES['print_file'];
    $maxBytes = MAX_FILE_MB * 1024 * 1024;

    if ($file['error'] !== UPLOAD_ERR_OK) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'Datei-Upload-Fehler (Code ' . $file['error'] . ').']);
        exit;
    }
    if ($file['size'] > $maxBytes) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'Datei zu groß (max. ' . MAX_FILE_MB . ' MB).']);
        exit;
    }

    // Strict MIME validation via finfo
    $finfo    = new finfo(FILEINFO_MIME_TYPE);
    $mimeType = $finfo->file($file['tmp_name']);
    $allowed  = ['application/pdf', 'image/svg+xml', 'image/webp', 'image/png', 'image/jpeg'];
    if (!in_array($mimeType, $allowed, true)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'error' => 'Ungültiger Dateityp. Erlaubt: PDF, SVG, WebP, PNG, JPG.']);
        exit;
    }

    if (!is_dir(UPLOAD_DIR)) {
        mkdir(UPLOAD_DIR, 0750, true);
    }

    $ext      = pathinfo($file['name'], PATHINFO_EXTENSION);
    $safeName = bin2hex(random_bytes(16)) . '.' . strtolower($ext);
    $dest     = UPLOAD_DIR . $safeName;

    if (!move_uploaded_file($file['tmp_name'], $dest)) {
        http_response_code(500);
        echo json_encode(['success' => false, 'error' => 'Datei konnte nicht gespeichert werden.']);
        exit;
    }

    $filePath         = $dest;
    $fileOriginalName = basename($file['name']);
}

// ── Generate order number ─────────────────────────────────────
$orderNumber = 'MSR-' . strtoupper(substr(bin2hex(random_bytes(4)), 0, 8));

// ── Persist order to SQLite ───────────────────────────────────
try {
    $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL;');

    $stmt = $pdo->prepare('
        INSERT INTO orders
          (order_number, customer_name, customer_email, customer_company,
           customer_phone, customer_address, product_name, product_options,
           quantity, unit_price, total_price, payment_method, payment_status,
           order_status, file_path, file_original_name, notes)
        VALUES
          (:on, :cn, :ce, :cc, :cp, :ca, :pn, :po,
           :qty, :up, :tp, :pm, :ps,
           :os, :fp, :fo, :nt)
    ');
    $stmt->execute([
        ':on'  => $orderNumber,
        ':cn'  => $name,
        ':ce'  => $email,
        ':cc'  => $company,
        ':cp'  => $phone,
        ':ca'  => $address,
        ':pn'  => $product,
        ':po'  => $options,
        ':qty' => $qty,
        ':up'  => $total / max(1, $qty),
        ':tp'  => $total,
        ':pm'  => 'bank',
        ':ps'  => 'pending',
        ':os'  => 'Eingegangen',
        ':fp'  => $filePath,
        ':fo'  => $fileOriginalName,
        ':nt'  => $notes,
    ]);
} catch (PDOException $e) {
    error_log('[bank-transfer] DB error: ' . $e->getMessage());
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Datenbankfehler. Bitte versuchen Sie es erneut.']);
    exit;
}

// ── Format total for display ──────────────────────────────────
$totalFormatted = number_format($total, 2, ',', '.') . ' €';

// ── Send confirmation email to customer ──────────────────────
$customerSubject = "Ihre Bestellung bei Masar Print Shop – {$orderNumber}";
$customerHtml    = buildBankTransferEmail($name, $orderNumber, $product, $options, $qty, $totalFormatted);
sendMail($email, $customerSubject, $customerHtml);

// ── Notify admin ──────────────────────────────────────────────
$adminSubject = "[Masar Shop] Neue Vorkasse-Bestellung {$orderNumber}";
$adminHtml    = "<h2>Neue Bestellung (Vorkasse)</h2>
<table style='border-collapse:collapse;font-family:sans-serif;font-size:14px;'>
  <tr><td style='padding:6px 12px;font-weight:700;'>Bestellnummer</td><td style='padding:6px 12px;'>{$orderNumber}</td></tr>
  <tr><td style='padding:6px 12px;font-weight:700;'>Kunde</td><td style='padding:6px 12px;'>" . htmlspecialchars($name) . "</td></tr>
  <tr><td style='padding:6px 12px;font-weight:700;'>E-Mail</td><td style='padding:6px 12px;'>" . htmlspecialchars($email) . "</td></tr>
  <tr><td style='padding:6px 12px;font-weight:700;'>Produkt</td><td style='padding:6px 12px;'>" . htmlspecialchars($product) . "</td></tr>
  <tr><td style='padding:6px 12px;font-weight:700;'>Menge</td><td style='padding:6px 12px;'>{$qty} Stk.</td></tr>
  <tr><td style='padding:6px 12px;font-weight:700;'>Gesamtbetrag</td><td style='padding:6px 12px;'>{$totalFormatted}</td></tr>
</table>";
sendMail(ADMIN_EMAIL, $adminSubject, $adminHtml);

// ── Return success ────────────────────────────────────────────
echo json_encode([
    'success'      => true,
    'orderNumber'  => $orderNumber,
    'total'        => $totalFormatted,
    'bankName'     => BANK_NAME,
    'iban'         => BANK_IBAN,
    'bic'          => BANK_BIC,
    'reference'    => $orderNumber,
]);

// ── Email builder ─────────────────────────────────────────────
function buildBankTransferEmail(
    string $name, string $orderNumber, string $product,
    string $options, int $qty, string $total
): string {
    $iban = BANK_IBAN;
    $bic  = BANK_BIC;
    $bn   = BANK_NAME;
    $n    = htmlspecialchars($name);
    $p    = htmlspecialchars($product);
    $o    = htmlspecialchars($options);

    return <<<HTML
<!DOCTYPE html>
<html lang="de">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f7fa;font-family:'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f7fa;padding:32px 16px;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08);">
      <tr><td style="background:linear-gradient(135deg,#132e50,#0a1628);padding:32px 40px;text-align:center;">
        <h1 style="margin:0;font-size:26px;font-weight:900;color:#fff;letter-spacing:2px;">MASAR PRINT SHOP</h1>
        <p style="margin:6px 0 0;color:rgba(88,208,189,.8);font-size:13px;">Bestellbestätigung – Vorkasse</p>
      </td></tr>
      <tr><td style="padding:32px 40px;">
        <p style="margin:0 0 12px;font-size:16px;color:#132e50;">Hallo {$n},</p>
        <p style="color:#555;line-height:1.7;">vielen Dank für Ihre Bestellung! Bitte überweisen Sie den Betrag auf das unten angegebene Konto. Nach Zahlungseingang beginnen wir sofort mit der Produktion.</p>
        <h3 style="margin:24px 0 12px;color:#132e50;font-size:15px;text-transform:uppercase;letter-spacing:1px;">Ihre Bestellung</h3>
        <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;font-size:14px;">
          <tr style="background:#f9fafb;"><td style="padding:10px 16px;font-weight:700;color:#555;width:40%;">Bestellnummer</td><td style="padding:10px 16px;color:#132e50;font-weight:700;">{$orderNumber}</td></tr>
          <tr><td style="padding:10px 16px;font-weight:700;color:#555;">Produkt</td><td style="padding:10px 16px;color:#132e50;">{$p}</td></tr>
          <tr style="background:#f9fafb;"><td style="padding:10px 16px;font-weight:700;color:#555;">Optionen</td><td style="padding:10px 16px;color:#132e50;">{$o}</td></tr>
          <tr><td style="padding:10px 16px;font-weight:700;color:#555;">Menge</td><td style="padding:10px 16px;color:#132e50;">{$qty} Stk.</td></tr>
          <tr style="background:#132e50;"><td style="padding:12px 16px;font-weight:800;color:#58d0bd;font-size:15px;">Gesamtbetrag</td><td style="padding:12px 16px;font-weight:800;color:#fff;font-size:17px;">{$total}</td></tr>
        </table>
        <h3 style="margin:28px 0 12px;color:#132e50;font-size:15px;text-transform:uppercase;letter-spacing:1px;">🏦 Bankverbindung</h3>
        <table width="100%" cellpadding="0" cellspacing="0" style="border:2px solid #58d0bd;border-radius:8px;overflow:hidden;font-size:14px;background:#f0fdfa;">
          <tr><td style="padding:10px 16px;font-weight:700;color:#555;width:40%;">Empfänger</td><td style="padding:10px 16px;color:#132e50;font-weight:700;">{$bn}</td></tr>
          <tr style="background:#fff;"><td style="padding:10px 16px;font-weight:700;color:#555;">IBAN</td><td style="padding:10px 16px;color:#132e50;font-family:monospace;font-size:15px;letter-spacing:1px;">{$iban}</td></tr>
          <tr><td style="padding:10px 16px;font-weight:700;color:#555;">BIC</td><td style="padding:10px 16px;color:#132e50;">{$bic}</td></tr>
          <tr style="background:#fff;"><td style="padding:10px 16px;font-weight:700;color:#555;">Verwendungszweck</td><td style="padding:10px 16px;color:#e53e3e;font-weight:800;">{$orderNumber}</td></tr>
          <tr><td style="padding:10px 16px;font-weight:700;color:#555;">Betrag</td><td style="padding:10px 16px;color:#132e50;font-weight:800;">{$total}</td></tr>
        </table>
        <p style="margin:20px 0 0;font-size:13px;color:#888;line-height:1.7;">Bitte geben Sie unbedingt die Bestellnummer <strong>{$orderNumber}</strong> als Verwendungszweck an.<br>Bei Fragen erreichen Sie uns unter <a href="tel:+491785143918" style="color:#58d0bd;">0178 514 3918</a> oder per E-Mail.</p>
      </td></tr>
      <tr><td style="background:#f9fafb;padding:20px 40px;text-align:center;border-top:1px solid #e5e7eb;">
        <p style="margin:0;font-size:12px;color:#aaa;">© 2026 Masar Werbeagentur · Berlin-Wedding · Bristolstraße 19HN<br>
        <a href="https://masar-werbeagentur.de/impressum.html" style="color:#aaa;">Impressum</a> &nbsp;·&nbsp;
        <a href="https://masar-werbeagentur.de/datenschutz.html" style="color:#aaa;">Datenschutz</a></p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body>
</html>
HTML;
}
