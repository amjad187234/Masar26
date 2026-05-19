<?php
// ═══ MASAR PRINT SHOP — STRIPE CHECKOUT SESSION CREATOR ═══
// Accepts multipart/form-data POST from checkout.html (Stripe payment flow).
// Steps: validate → upload file → verify price server-side →
//        create pending order → create Stripe Checkout Session → return URL.
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

// ── Load dependencies ─────────────────────────────────────────
$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Serverkonfiguration fehlt.']);
    exit;
}
require $configPath;
require __DIR__ . '/catalog.php';

// ── Helper: JSON error ────────────────────────────────────────
function jsonError(string $msg, int $code = 400): never {
    http_response_code($code);
    echo json_encode(['success' => false, 'error' => $msg]);
    exit;
}

// ── Helper: Stripe API call via cURL ─────────────────────────
function stripePost(string $endpoint, array $fields): array {
    $ch = curl_init('https://api.stripe.com/v1/' . ltrim($endpoint, '/'));
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_USERPWD        => STRIPE_SECRET_KEY . ':',
        CURLOPT_POSTFIELDS     => http_build_query($fields),
        CURLOPT_TIMEOUT        => 20,
        CURLOPT_HTTPHEADER     => ['Stripe-Version: 2024-11-20.acacia'],
    ]);
    $response  = curl_exec($ch);
    $httpCode  = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlErr   = curl_error($ch);
    curl_close($ch);

    if ($curlErr) {
        return ['__http' => 0, '__error' => $curlErr];
    }
    $data = json_decode($response, true) ?? [];
    $data['__http'] = $httpCode;
    return $data;
}

// ── Only POST ─────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonError('Nur POST-Anfragen erlaubt.', 405);
}

// ── Stripe secret key check ───────────────────────────────────
if (empty(STRIPE_SECRET_KEY)) {
    jsonError('Zahlungssystem nicht konfiguriert. Bitte Hostinger-Umgebungsvariable STRIPE_SECRET_KEY setzen.', 500);
}

// ── Sanitize helper ───────────────────────────────────────────
function sanitize(string $val): string {
    return htmlspecialchars(strip_tags(trim($val)), ENT_QUOTES, 'UTF-8');
}

// ── Collect & validate fields ─────────────────────────────────
$required = ['name', 'email', 'company', 'address', 'cart_json'];
foreach ($required as $f) {
    if (empty($_POST[$f])) {
        jsonError("Pflichtfeld fehlt: {$f}");
    }
}

$name    = str_replace(["\r", "\n"], ' ', sanitize($_POST['name']));
$email   = str_replace(["\r", "\n"], '',  sanitize($_POST['email']));
$company = sanitize($_POST['company']);
$phone   = sanitize($_POST['phone']    ?? '');
$address = sanitize($_POST['address']);
$vat     = sanitize($_POST['vat']      ?? '');
$notes   = sanitize($_POST['notes']    ?? '');

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    jsonError('Ungültige E-Mail-Adresse.');
}

// ── Parse & verify cart server-side ──────────────────────────
$cartRaw = $_POST['cart_json'] ?? '[]';
$cartItems = json_decode($cartRaw, true);
if (!is_array($cartItems) || count($cartItems) === 0) {
    jsonError('Warenkorb ist leer oder ungültig.');
}

// Sanitize each cart item (only allow known fields, prevent injection)
$sanitizedCart = [];
foreach ($cartItems as $item) {
    $id   = preg_replace('/[^a-z0-9\-]/', '', (string)($item['id']  ?? ''));
    $qty  = (int)($item['qty'] ?? 0);
    $opts = [];
    foreach ((array)($item['opts'] ?? []) as $k => $v) {
        $opts[preg_replace('/[^a-zA-Z0-9_]/', '', $k)] = (string)$v;
    }
    if ($id === '' || $qty < 1) {
        jsonError('Ungültige Warenkorb-Position.');
    }
    $sanitizedCart[] = ['id' => $id, 'qty' => $qty, 'opts' => $opts];
}

// Calculate verified total using server-side catalog
$cartCalc    = calcCartServer($MASAR_CATALOG, $sanitizedCart);
$serverTotal = $cartCalc['total'];

if ($serverTotal < 0.50) {
    jsonError('Bestellbetrag zu niedrig (Minimum 0,50 €).');
}

// Build product name/description for Stripe line item
$productNames = [];
foreach ($sanitizedCart as $item) {
    foreach ($MASAR_CATALOG as $p) {
        if ($p['id'] === $item['id']) {
            $optStr = implode(', ', array_values($item['opts']));
            $productNames[] = $p['name'] . ($optStr ? " ({$optStr})" : '') . " × {$item['qty']}";
            break;
        }
    }
}
$lineItemName = implode(' | ', $productNames);
$lineItemDesc = "Druckproduktion – Masar Print Shop Berlin";

// ── File upload ───────────────────────────────────────────────
if (!isset($_FILES['print_file']) || $_FILES['print_file']['error'] === UPLOAD_ERR_NO_FILE) {
    jsonError('Druckdatei fehlt. Bitte PDF oder Bilddatei hochladen.');
}

$file = $_FILES['print_file'];

if ($file['error'] !== UPLOAD_ERR_OK) {
    $uploadErrors = [
        UPLOAD_ERR_INI_SIZE   => 'Datei zu groß (Server-Limit).',
        UPLOAD_ERR_FORM_SIZE  => 'Datei zu groß (Formular-Limit).',
        UPLOAD_ERR_PARTIAL    => 'Datei nur teilweise hochgeladen.',
        UPLOAD_ERR_NO_TMP_DIR => 'Temporäres Verzeichnis fehlt.',
        UPLOAD_ERR_CANT_WRITE => 'Datei konnte nicht geschrieben werden.',
    ];
    jsonError($uploadErrors[$file['error']] ?? 'Upload-Fehler.');
}

$maxBytes = MAX_FILE_MB * 1024 * 1024;
if ($file['size'] > $maxBytes) {
    jsonError('Datei zu groß. Maximum: ' . MAX_FILE_MB . ' MB.');
}

// MIME type validation with finfo (SVG excluded — can contain embedded JS)
$allowedMimes = ['application/pdf', 'image/webp', 'image/png', 'image/jpeg'];
$finfo    = finfo_open(FILEINFO_MIME_TYPE);
$mimeType = finfo_file($finfo, $file['tmp_name']);
finfo_close($finfo);

if (!in_array($mimeType, $allowedMimes, true)) {
    jsonError("Dateityp nicht erlaubt: {$mimeType}. Erlaubt: PDF, WebP, PNG, JPEG.");
}

// Generate UUID filename and move file
if (!is_dir(UPLOAD_DIR)) {
    if (!mkdir(UPLOAD_DIR, 0750, true)) {
        jsonError('Upload-Verzeichnis konnte nicht erstellt werden.', 500);
    }
}

$uuid         = sprintf('%s-%s-%s-%s-%s',
    bin2hex(random_bytes(4)), bin2hex(random_bytes(2)),
    bin2hex(random_bytes(2)), bin2hex(random_bytes(2)),
    bin2hex(random_bytes(6))
);
$mimeExtMap   = ['application/pdf' => 'pdf', 'image/webp' => 'webp', 'image/png' => 'png', 'image/jpeg' => 'jpg'];
$safeExt      = $mimeExtMap[$mimeType];
$storedName   = $uuid . '.' . $safeExt;
$destPath     = UPLOAD_DIR . $storedName;
$originalName = basename($file['name']);

if (!move_uploaded_file($file['tmp_name'], $destPath)) {
    jsonError('Datei konnte nicht gespeichert werden.', 500);
}
chmod($destPath, 0640);

// ── Create pending order in SQLite ────────────────────────────
$orderNumber = 'MSP-' . date('Ymd') . '-' . strtoupper(substr(uniqid(), -6));

try {
    $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL;');
    $pdo->exec('PRAGMA foreign_keys=ON;');
} catch (PDOException $e) {
    @unlink($destPath);
    jsonError('Datenbankfehler. Bitte erneut versuchen.', 500);
}

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
            :quantity, :unit_price, :total_price, 'stripe', 'pending',
            'Eingegangen', :file_path, :file_original_name, :notes
        )
    ");

    $totalQty = array_sum(array_column($sanitizedCart, 'qty'));

    $stmt->execute([
        ':order_number'       => $orderNumber,
        ':customer_name'      => $name,
        ':customer_email'     => $email,
        ':customer_company'   => $company,
        ':customer_phone'     => $phone,
        ':customer_address'   => $address,
        ':product_name'       => $lineItemName,
        ':product_options'    => $vat ? "USt-IdNr.: {$vat}" : '',
        ':quantity'           => $totalQty,
        ':unit_price'         => round($serverTotal / max($totalQty, 1), 4),
        ':total_price'        => $serverTotal,
        ':file_path'          => $storedName,
        ':file_original_name' => $originalName,
        ':notes'              => $notes,
    ]);
} catch (PDOException $e) {
    @unlink($destPath);
    jsonError('Bestellung konnte nicht gespeichert werden. Bitte erneut versuchen.', 500);
}

// ── Create Stripe Checkout Session ────────────────────────────
$amountCents = (int) round($serverTotal * 100);

// Payment methods available in Germany (sofort/giropay discontinued by Stripe in 2024)
$sessionFields = [
    'mode'                                          => 'payment',
    'line_items[0][price_data][currency]'           => STRIPE_CURRENCY,
    'line_items[0][price_data][unit_amount]'        => $amountCents,
    'line_items[0][price_data][product_data][name]' => mb_substr($lineItemName, 0, 255),
    'line_items[0][price_data][product_data][description]' => $lineItemDesc,
    'line_items[0][quantity]'                       => 1,
    'payment_method_types[0]'                       => 'card',
    'payment_method_types[1]'                       => 'klarna',
    // PayPal excluded per business requirement.
    // giropay removed by Stripe July 2024; sofort deprecated.
    'customer_email'                                => $email,
    'success_url'                                   => SITE_URL . '/shop/success.html?session_id={CHECKOUT_SESSION_ID}',
    'cancel_url'                                    => SITE_URL . '/shop/checkout.html',
    'locale'                                        => 'de',
    'metadata[order_id]'                            => $orderNumber,
    'metadata[customer_email]'                      => $email,
    'metadata[file_path]'                           => $storedName,
    // Billing address collection for DSGVO / invoice purposes
    'billing_address_collection'                    => 'auto',
    // Allow promo codes if enabled in Stripe Dashboard
    'allow_promotion_codes'                         => 'true',
];

$session = stripePost('checkout/sessions', $sessionFields);

if (($session['__http'] ?? 0) !== 200 || empty($session['url'])) {
    // Roll back: delete pending order and uploaded file
    try {
        $pdo->prepare('DELETE FROM orders WHERE order_number = :n')
            ->execute([':n' => $orderNumber]);
    } catch (PDOException) {}
    @unlink($destPath);
    jsonError('Checkout-Session konnte nicht erstellt werden. Bitte erneut versuchen.', 500);
}

echo json_encode([
    'success'   => true,
    'sessionId' => $session['id'],
    'url'       => $session['url'],
]);
