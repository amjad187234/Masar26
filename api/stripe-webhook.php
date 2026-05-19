<?php
// ═══ MASAR PRINT SHOP — STRIPE WEBHOOK HANDLER ═══
// Handles: checkout.session.completed
// Provides reliable order fulfillment when customer closes browser before
// returning to success.html. Stripe retries webhooks on non-2xx responses.
//
// Setup in Stripe Dashboard:
//   Webhooks → Add endpoint → https://masar-werbeagentur.de/api/stripe-webhook.php
//   Events: checkout.session.completed
//   Copy the signing secret → set STRIPE_WEBHOOK_SECRET env var on Hostinger
declare(strict_types=1);

// Webhook MUST read raw body before any PHP processing
$rawBody = file_get_contents('php://input');

header('Content-Type: application/json');
header('X-Content-Type-Options: nosniff');

$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    http_response_code(500);
    echo json_encode(['error' => 'Config missing']);
    exit;
}
require $configPath;
require __DIR__ . '/email-helper.php';

// ── Signature verification ────────────────────────────────────
// Implements Stripe's webhook signature verification without the PHP SDK.
function verifyStripeSignature(string $payload, string $sigHeader, string $secret): bool
{
    if (empty($secret)) {
        return false;
    }

    $parts     = explode(',', $sigHeader);
    $timestamp = null;
    $signatures = [];

    foreach ($parts as $part) {
        [$k, $v] = array_pad(explode('=', $part, 2), 2, '');
        if ($k === 't') {
            $timestamp = $v;
        } elseif ($k === 'v1') {
            $signatures[] = $v;
        }
    }

    if ($timestamp === null || empty($signatures)) {
        return false;
    }

    // Reject requests older than 5 minutes (replay attack protection)
    if (abs(time() - (int) $timestamp) > 300) {
        return false;
    }

    $signedPayload = $timestamp . '.' . $payload;
    $expected      = hash_hmac('sha256', $signedPayload, $secret);

    foreach ($signatures as $sig) {
        if (hash_equals($expected, $sig)) {
            return true;
        }
    }

    return false;
}

// ── Verify signature ──────────────────────────────────────────
$sigHeader = $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '';

if (empty(STRIPE_WEBHOOK_SECRET)) {
    // Not configured yet — log and return 200 to prevent Stripe retries flooding
    error_log('MASAR: STRIPE_WEBHOOK_SECRET not set. Webhook not verified.');
    http_response_code(200);
    echo json_encode(['received' => true, 'note' => 'webhook_secret_not_configured']);
    exit;
}

if (!verifyStripeSignature($rawBody, $sigHeader, STRIPE_WEBHOOK_SECRET)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid signature']);
    exit;
}

// ── Parse event ───────────────────────────────────────────────
$event = json_decode($rawBody, true);
if (!$event || !isset($event['type'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid event payload']);
    exit;
}

// ── Return 200 immediately (Stripe expects fast response) ─────
http_response_code(200);
echo json_encode(['received' => true]);
flush();

// ── Process event ─────────────────────────────────────────────
if ($event['type'] !== 'checkout.session.completed') {
    exit; // Ignore other events
}

$session = $event['data']['object'] ?? [];

// Validate payment status
$paymentStatus = $session['payment_status'] ?? '';
if (!in_array($paymentStatus, ['paid', 'no_payment_required'], true)) {
    exit; // Not paid, ignore
}

// Get order ID from metadata
$orderId = $session['metadata']['order_id'] ?? '';
if (empty($orderId) || !preg_match('/^MSP-\d{8}-[A-Z0-9]{6}$/', $orderId)) {
    error_log("MASAR Webhook: invalid or missing order_id in metadata for session {$session['id']}");
    exit;
}

$sessionId = $session['id'] ?? '';

// ── Update order in SQLite (idempotent) ───────────────────────
try {
    $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL;');

    // Atomic update: only if still pending (prevents duplicate emails)
    $stmt = $pdo->prepare(
        "UPDATE orders SET payment_status = 'paid'
         WHERE order_number = :n AND payment_status = 'pending'"
    );
    $stmt->execute([':n' => $orderId]);
    $justPaid = $stmt->rowCount() > 0;

    if ($justPaid) {
        // Fetch full order row and send emails
        $fetchStmt = $pdo->prepare('SELECT * FROM orders WHERE order_number = :n LIMIT 1');
        $fetchStmt->execute([':n' => $orderId]);
        $order = $fetchStmt->fetch();

        if ($order) {
            sendOrderEmails($order, $sessionId);
        }
    }

} catch (PDOException $e) {
    error_log('MASAR Webhook DB error for ' . $orderId . ': ' . $e->getMessage());
    // Don't echo — response already sent. Stripe will retry on our 200 regardless.
}
