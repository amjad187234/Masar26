<?php
// ═══ MASAR PRINT SHOP — STRIPE PAYMENT VERIFIER ═══
// Called by success.html after Stripe redirects back.
// Verifies session with Stripe, updates DB, triggers confirmation emails.
// Idempotent: safe to call multiple times for the same session.
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Serverkonfiguration fehlt.']);
    exit;
}
require $configPath;
require __DIR__ . '/email-helper.php';

function jsonError(string $msg, int $code = 400): never {
    http_response_code($code);
    echo json_encode(['success' => false, 'error' => $msg]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    jsonError('Nur GET-Anfragen erlaubt.', 405);
}

if (empty(STRIPE_SECRET_KEY)) {
    jsonError('Zahlungssystem nicht konfiguriert.', 500);
}

// ── Validate session_id format ────────────────────────────────
$sessionId = trim($_GET['session_id'] ?? '');
if (!preg_match('/^cs_[a-zA-Z0-9_]+$/', $sessionId)) {
    jsonError('Ungültige Session-ID.');
}

// ── Retrieve Stripe Checkout Session ─────────────────────────
$ch = curl_init('https://api.stripe.com/v1/checkout/sessions/' . urlencode($sessionId));
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_USERPWD        => STRIPE_SECRET_KEY . ':',
    CURLOPT_TIMEOUT        => 15,
    CURLOPT_HTTPHEADER     => ['Stripe-Version: 2024-11-20.acacia'],
]);
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200) {
    jsonError('Zahlungsstatus konnte nicht abgerufen werden.', 502);
}

$session = json_decode($response, true);

// ── Check payment status ──────────────────────────────────────
$paymentStatus = $session['payment_status'] ?? '';
$sessionStatus = $session['status']         ?? '';

if (!in_array($paymentStatus, ['paid', 'no_payment_required'], true)
    && $sessionStatus !== 'complete') {
    jsonError('Zahlung ist noch nicht abgeschlossen (Status: ' . $paymentStatus . ').', 402);
}

// ── Get order number from metadata ────────────────────────────
$orderId = $session['metadata']['order_id'] ?? '';
if (empty($orderId) || !preg_match('/^MSP-\d{8}-[A-Z0-9]{6}$/', $orderId)) {
    jsonError('Bestellreferenz in Stripe-Metadaten nicht gefunden.', 422);
}

// ── Open SQLite ───────────────────────────────────────────────
try {
    $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL;');
} catch (PDOException $e) {
    jsonError('Datenbankfehler.', 500);
}

// ── Atomically mark order as paid (idempotent) ────────────────
// Only updates + sends emails if transitioning FROM 'pending'.
// If already 'paid', just return order data without re-sending emails.
$updateStmt = $pdo->prepare(
    "UPDATE orders SET payment_status = 'paid'
     WHERE order_number = :n AND payment_status = 'pending'"
);
$updateStmt->execute([':n' => $orderId]);
$justPaid = $updateStmt->rowCount() > 0;

// ── Fetch order row ───────────────────────────────────────────
$fetchStmt = $pdo->prepare('SELECT * FROM orders WHERE order_number = :n LIMIT 1');
$fetchStmt->execute([':n' => $orderId]);
$order = $fetchStmt->fetch();

if (!$order) {
    jsonError('Bestellung nicht gefunden.', 404);
}

// ── Send confirmation emails (only on first successful verification) ──
if ($justPaid) {
    sendOrderEmails($order, $sessionId);
}

// ── Return order data for success.html display ────────────────
echo json_encode([
    'success'          => true,
    'order_number'     => $order['order_number'],
    'customer_name'    => $order['customer_name'],
    'customer_email'   => $order['customer_email'],
    'product_name'     => $order['product_name'],
    'product_options'  => $order['product_options'],
    'quantity'         => (int) $order['quantity'],
    'total_price'      => (float) $order['total_price'],
    'payment_method'   => $order['payment_method'],
    'payment_status'   => $order['payment_status'],
    'already_processed'=> !$justPaid,
]);
