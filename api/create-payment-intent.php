<?php
// ═══ MASAR PRINT SHOP — STRIPE PAYMENT INTENT CREATOR ═══
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Nur POST-Anfragen erlaubt.']);
    exit;
}

$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    http_response_code(500);
    echo json_encode(['error' => 'Serverkonfiguration fehlt.']);
    exit;
}
require $configPath;

$input  = json_decode(file_get_contents('php://input'), true) ?? [];
$amount = (int) round((float) ($input['amount'] ?? 0) * 100); // EUR → Cent

if ($amount < 50) {
    http_response_code(400);
    echo json_encode(['error' => 'Ungültiger Betrag (Minimum 0,50 €).']);
    exit;
}
if ($amount > 10_000_000) { // max 100,000 € Plausibilitätsprüfung
    http_response_code(400);
    echo json_encode(['error' => 'Betrag zu hoch.']);
    exit;
}

if (!defined('STRIPE_SECRET_KEY') || str_starts_with(STRIPE_SECRET_KEY, 'sk_REPLACE')) {
    http_response_code(500);
    echo json_encode(['error' => 'Stripe ist noch nicht konfiguriert.']);
    exit;
}

$postFields = http_build_query([
    'amount'                                     => $amount,
    'currency'                                   => STRIPE_CURRENCY,
    'automatic_payment_methods[enabled]'         => 'true',
    'automatic_payment_methods[allow_redirects]' => 'never',
]);

$ch = curl_init('https://api.stripe.com/v1/payment_intents');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_USERPWD        => STRIPE_SECRET_KEY . ':',
    CURLOPT_POSTFIELDS     => $postFields,
    CURLOPT_TIMEOUT        => 15,
    CURLOPT_HTTPHEADER     => ['Stripe-Version: 2024-11-20.acacia'],
]);

$response  = curl_exec($ch);
$httpCode  = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($curlError) {
    http_response_code(502);
    echo json_encode(['error' => 'Verbindung zum Zahlungsanbieter fehlgeschlagen.']);
    exit;
}

$data = json_decode($response, true);

if ($httpCode !== 200 || empty($data['client_secret'])) {
    http_response_code(500);
    echo json_encode(['error' => 'Zahlung konnte nicht initialisiert werden.']);
    exit;
}

echo json_encode(['client_secret' => $data['client_secret']]);
