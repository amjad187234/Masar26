<?php
// ═══ MASAR PRINT SHOP — ADMIN DASHBOARD ═══
declare(strict_types=1);

// Cookie params MUST be set before session_start()
session_set_cookie_params([
    'lifetime' => 0,
    'path'     => '/',
    'secure'   => true,
    'httponly' => true,
    'samesite' => 'Strict',
]);
session_start();

// ── Auth check ────────────────────────────────────────────────
if (empty($_SESSION['admin_logged_in'])) {
    header('Location: login.php');
    exit;
}

// ── CSRF token ────────────────────────────────────────────────
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
$csrfToken = $_SESSION['csrf_token'];

// ── Load config ───────────────────────────────────────────────
$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    die('Konfigurationsfehler.');
}
require $configPath;

// ── Open DB ───────────────────────────────────────────────────
try {
    $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL;');
} catch (PDOException $e) {
    die('<p style="color:red;padding:2rem;">Datenbankfehler: ' . htmlspecialchars($e->getMessage()) . '</p>');
}

$msg = '';

// ── Handle POST actions ───────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // CSRF validation
    $submittedCsrf = $_POST['csrf_token'] ?? '';
    if (!hash_equals($csrfToken, $submittedCsrf)) {
        $msg = 'Sicherheitsfehler: Ungültige Anfrage.';
    } else {
    $action = $_POST['action'] ?? '';

    // ── Update order status ──────────────────────────────────
    if ($action === 'update_status') {
        $orderId    = (int)($_POST['order_id'] ?? 0);
        $newStatus  = $_POST['new_status'] ?? '';
        $validStati = ['Eingegangen', 'In Produktion', 'Versendet', 'Storniert'];

        if ($orderId > 0 && in_array($newStatus, $validStati, true)) {
            $stmt = $pdo->prepare('UPDATE orders SET order_status = :s WHERE id = :id');
            $stmt->execute([':s' => $newStatus, ':id' => $orderId]);
            $msg = "Status für Bestellung #{$orderId} auf \"{$newStatus}\" aktualisiert.";
        } else {
            $msg = 'Ungültige Anfrage.';
        }
    }

    // ── Download file ─────────────────────────────────────────
    if ($action === 'download_file') {
        $orderId = (int)($_POST['order_id'] ?? 0);
        if ($orderId > 0) {
            $stmt = $pdo->prepare('SELECT file_path, file_original_name FROM orders WHERE id = :id LIMIT 1');
            $stmt->execute([':id' => $orderId]);
            $row = $stmt->fetch();
            if ($row && $row['file_path']) {
                $fullPath = UPLOAD_DIR . basename($row['file_path']); // basename prevents path traversal
                if (file_exists($fullPath)) {
                    $originalName = $row['file_original_name'] ?: basename($fullPath);
                    $finfo = new finfo(FILEINFO_MIME_TYPE);
                    $mime  = $finfo->file($fullPath) ?: 'application/octet-stream';
                    // RFC 5987 filename encoding to support non-ASCII characters safely
                    $asciiName   = preg_replace('/[^\x20-\x7E]/', '_', $originalName);
                    $encodedName = rawurlencode($originalName);
                    header('Content-Type: ' . $mime);
                    header('Content-Disposition: attachment; filename="' . str_replace('"', '\\"', $asciiName) . '"; filename*=UTF-8\'\'' . $encodedName);
                    header('Content-Length: ' . filesize($fullPath));
                    header('X-Content-Type-Options: nosniff');
                    readfile($fullPath);
                    exit;
                } else {
                    $msg = 'Datei nicht gefunden auf dem Server.';
                }
            }
        }
    }

    // ── Logout ────────────────────────────────────────────────
    if ($action === 'logout') {
        session_destroy();
        header('Location: login.php');
        exit;
    }
    } // end CSRF else
}

// ── Fetch all orders ──────────────────────────────────────────
$filterStatus = $_GET['filter'] ?? 'all';
$validFilters = ['all', 'Eingegangen', 'In Produktion', 'Versendet', 'Storniert'];
if (!in_array($filterStatus, $validFilters, true)) $filterStatus = 'all';

if ($filterStatus === 'all') {
    $orders = $pdo->query('SELECT * FROM orders ORDER BY created_at DESC')->fetchAll();
} else {
    $stmt = $pdo->prepare('SELECT * FROM orders WHERE order_status = :s ORDER BY created_at DESC');
    $stmt->execute([':s' => $filterStatus]);
    $orders = $stmt->fetchAll();
}

// ── Stats ─────────────────────────────────────────────────────
$allOrders    = $pdo->query('SELECT COUNT(*) as n FROM orders')->fetch()['n'] ?? 0;
$countNew     = $pdo->query("SELECT COUNT(*) as n FROM orders WHERE order_status='Eingegangen'")->fetch()['n'] ?? 0;
$countProd    = $pdo->query("SELECT COUNT(*) as n FROM orders WHERE order_status='In Produktion'")->fetch()['n'] ?? 0;
$countShipped = $pdo->query("SELECT COUNT(*) as n FROM orders WHERE order_status='Versendet'")->fetch()['n'] ?? 0;
$totalRevenue = $pdo->query("SELECT SUM(total_price) as t FROM orders WHERE order_status != 'Storniert'")->fetch()['t'] ?? 0;

function fmtEur(float $n): string {
    return number_format($n, 2, ',', '.') . ' €';
}

$statusColors = [
    'Eingegangen'   => '#f5c000',
    'In Produktion' => '#58d0bd',
    'Versendet'     => '#48bb78',
    'Storniert'     => '#fc8181',
];
?><!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin Dashboard – Masar Print Shop</title>
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<style>
/* ── Tokens ── */
:root {
  --teal:#58d0bd; --teal-d:#3ab8a5; --teal-l:rgba(88,208,189,.1);
  --navy:#132e50; --navy2:#1e4275; --navy3:#0a1628;
  --off:#f4f7f7; --text:#1a2a2a; --muted:#5a7070;
  --border:#e0eaea; --r:10px;
  --shadow:0 4px 20px rgba(0,0,0,.08);
}
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { font-size:15px; }
body { font-family:'Segoe UI',system-ui,Arial,sans-serif; background:var(--off); color:var(--text); min-height:100vh; }
a { text-decoration:none; color:inherit; }

/* ── Header ── */
.adm-header {
  background:var(--navy3);
  border-bottom:3px solid var(--teal);
  padding:0 2rem;
  position:sticky; top:0; z-index:200;
}
.adm-header-inner {
  max-width:1400px; margin:0 auto;
  display:flex; align-items:center; justify-content:space-between;
  height:64px; gap:1rem;
}
.adm-logo {
  font-family:'Arial Black',Arial,sans-serif;
  font-weight:900; font-size:22px; color:#fff; letter-spacing:3px;
}
.adm-logo span { color:var(--teal); }
.adm-title { font-size:13px; color:rgba(255,255,255,.4); margin-left:1rem; }
.adm-user { font-size:13px; color:rgba(255,255,255,.5); }
.adm-user strong { color:var(--teal); }
.btn-logout {
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.12);
  color:rgba(255,255,255,.6);
  padding:7px 16px;
  border-radius:6px;
  font-size:13px;
  font-family:inherit;
  cursor:pointer;
  transition:all .2s;
}
.btn-logout:hover { background:rgba(229,62,62,.15); color:#fc8181; border-color:rgba(229,62,62,.3); }

/* ── Layout ── */
.adm-main { max-width:1400px; margin:0 auto; padding:2rem; }

/* ── Flash message ── */
.adm-msg {
  background:rgba(88,208,189,.1);
  border:1px solid rgba(88,208,189,.3);
  border-left:4px solid var(--teal);
  border-radius:0 var(--r) var(--r) 0;
  padding:.8rem 1.2rem;
  font-size:13px; color:var(--navy);
  margin-bottom:1.5rem;
}

/* ── Stats ── */
.stats-row {
  display:grid;
  grid-template-columns:repeat(5,1fr);
  gap:1rem;
  margin-bottom:2rem;
}
.stat-card {
  background:#fff;
  border:1px solid var(--border);
  border-radius:var(--r);
  padding:1.2rem 1.5rem;
  box-shadow:var(--shadow);
}
.stat-label {
  font-size:10px;
  letter-spacing:2px;
  text-transform:uppercase;
  color:var(--muted);
  margin-bottom:.4rem;
}
.stat-value {
  font-size:2rem;
  font-weight:900;
  color:var(--navy);
  line-height:1;
}
.stat-value.teal { color:var(--teal); }

/* ── Filter tabs ── */
.filter-tabs { display:flex; gap:.5rem; margin-bottom:1.5rem; flex-wrap:wrap; }
.filter-tab {
  padding:8px 18px;
  border:1.5px solid var(--border);
  border-radius:30px;
  font-size:13px; font-weight:700;
  cursor:pointer;
  transition:all .2s;
  background:#fff;
  color:var(--muted);
  text-decoration:none;
  display:inline-block;
}
.filter-tab:hover { border-color:var(--teal); color:var(--navy); }
.filter-tab.active { background:var(--navy); color:#fff; border-color:var(--navy); }

/* ── Table ── */
.table-wrap {
  background:#fff;
  border:1px solid var(--border);
  border-radius:var(--r);
  box-shadow:var(--shadow);
  overflow-x:auto;
}
table { width:100%; border-collapse:collapse; min-width:900px; }
thead th {
  background:var(--navy);
  color:#fff;
  padding:12px 14px;
  text-align:left;
  font-size:11px;
  letter-spacing:1.5px;
  text-transform:uppercase;
  white-space:nowrap;
}
thead th:first-child { border-radius:var(--r) 0 0 0; }
thead th:last-child  { border-radius:0 var(--r) 0 0; }
tbody tr { border-bottom:1px solid var(--border); transition:background .15s; }
tbody tr:last-child { border-bottom:none; }
tbody tr:hover { background:var(--teal-l); }
tbody td { padding:12px 14px; font-size:13px; vertical-align:middle; }
.order-num { font-family:monospace; font-weight:700; color:var(--navy); font-size:13px; letter-spacing:.5px; }
.order-date { color:var(--muted); font-size:12px; white-space:nowrap; }
.customer-name { font-weight:700; color:var(--navy); }
.customer-email { font-size:11px; color:var(--muted); }
.product-name { font-weight:600; }
.product-opts { font-size:11px; color:var(--muted); }
.price-val { font-weight:700; color:var(--navy); white-space:nowrap; }
.pay-badge {
  display:inline-block;
  padding:3px 8px;
  border-radius:4px;
  font-size:11px; font-weight:700;
  background:var(--off);
  color:var(--muted);
}
.pay-badge.bank  { background:rgba(245,192,0,.12); color:#b7860a; }
.pay-badge.paypal{ background:rgba(0,112,243,.1); color:#0070f3; }

/* ── Status badge ── */
.status-badge {
  display:inline-block;
  padding:4px 10px;
  border-radius:30px;
  font-size:11px;
  font-weight:700;
}

/* ── Status form ── */
.status-form { display:flex; gap:.4rem; align-items:center; }
.status-select {
  border:1.5px solid var(--border);
  border-radius:6px;
  padding:5px 8px;
  font-size:12px; font-family:inherit;
  background:#fff;
  color:var(--text);
  cursor:pointer;
  outline:none;
  transition:border-color .2s;
}
.status-select:focus { border-color:var(--teal); }
.btn-update {
  background:var(--teal);
  color:var(--navy);
  border:none;
  border-radius:6px;
  padding:5px 10px;
  font-size:12px;
  font-weight:700;
  font-family:inherit;
  cursor:pointer;
  transition:background .2s;
  white-space:nowrap;
}
.btn-update:hover { background:var(--teal-d); }

/* ── Download button ── */
.btn-dl {
  background:var(--navy);
  color:#fff;
  border:none;
  border-radius:6px;
  padding:5px 10px;
  font-size:12px;
  font-weight:600;
  font-family:inherit;
  cursor:pointer;
  transition:background .2s;
  white-space:nowrap;
  width:100%;
}
.btn-dl:hover { background:var(--navy2); }
.no-file { color:var(--muted); font-size:12px; }

/* ── Empty state ── */
.empty-state { text-align:center; padding:4rem 2rem; color:var(--muted); }
.empty-state .icon { font-size:3rem; margin-bottom:1rem; }
.empty-state p { font-size:14px; }

/* ── Responsive ── */
@media(max-width:1100px) {
  .stats-row { grid-template-columns:repeat(3,1fr); }
}
@media(max-width:720px) {
  .adm-main { padding:1rem; }
  .stats-row { grid-template-columns:1fr 1fr; }
  .adm-title { display:none; }
}
@media(max-width:480px) {
  .stats-row { grid-template-columns:1fr; }
}
</style>
</head>
<body>

<!-- HEADER -->
<header class="adm-header">
  <div class="adm-header-inner">
    <div style="display:flex;align-items:center;gap:.5rem;">
      <div class="adm-logo">M<span>A</span>SAR</div>
      <span class="adm-title">Admin – Bestellverwaltung</span>
    </div>
    <div style="display:flex;align-items:center;gap:1rem;">
      <span class="adm-user">Angemeldet als <strong><?= htmlspecialchars($_SESSION['admin_user'] ?? '') ?></strong></span>
      <form method="POST" action="dashboard.php" style="margin:0;">
        <input type="hidden" name="action" value="logout">
        <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($csrfToken) ?>">
        <button type="submit" class="btn-logout">Abmelden</button>
      </form>
    </div>
  </div>
</header>

<main class="adm-main">

  <?php if ($msg): ?>
  <div class="adm-msg"><?= htmlspecialchars($msg) ?></div>
  <?php endif; ?>

  <!-- STATS ROW -->
  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-label">Alle Bestellungen</div>
      <div class="stat-value"><?= $allOrders ?></div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Eingegangen (Neu)</div>
      <div class="stat-value" style="color:#f5c000;"><?= $countNew ?></div>
    </div>
    <div class="stat-card">
      <div class="stat-label">In Produktion</div>
      <div class="stat-value teal"><?= $countProd ?></div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Versendet</div>
      <div class="stat-value" style="color:#48bb78;"><?= $countShipped ?></div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Umsatz (gesamt)</div>
      <div class="stat-value teal" style="font-size:1.4rem;"><?= fmtEur((float)$totalRevenue) ?></div>
    </div>
  </div>

  <!-- FILTER TABS -->
  <div class="filter-tabs">
    <?php
    $tabs = ['all' => 'Alle', 'Eingegangen' => 'Neu', 'In Produktion' => 'In Produktion', 'Versendet' => 'Versendet', 'Storniert' => 'Storniert'];
    foreach ($tabs as $key => $label):
      $active = ($filterStatus === $key) ? ' active' : '';
      $qs     = $key === 'all' ? '' : '?filter=' . urlencode($key);
    ?>
    <a href="dashboard.php<?= $qs ?>" class="filter-tab<?= $active ?>"><?= $label ?></a>
    <?php endforeach; ?>
  </div>

  <!-- ORDERS TABLE -->
  <div class="table-wrap">
    <?php if (empty($orders)): ?>
    <div class="empty-state">
      <div class="icon">📋</div>
      <p>Keine Bestellungen vorhanden<?= $filterStatus !== 'all' ? ' für diesen Filter' : '' ?>.</p>
    </div>
    <?php else: ?>
    <table>
      <thead>
        <tr>
          <th>Bestellung</th>
          <th>Datum</th>
          <th>Kunde</th>
          <th>Produkt</th>
          <th style="text-align:center;">Menge</th>
          <th>Preis</th>
          <th>Zahlung</th>
          <th>Status</th>
          <th>Druckdatei</th>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($orders as $order): ?>
        <tr>
          <!-- Order number -->
          <td>
            <div class="order-num"><?= htmlspecialchars($order['order_number']) ?></div>
          </td>

          <!-- Date -->
          <td>
            <div class="order-date">
              <?= htmlspecialchars(date('d.m.Y', strtotime($order['created_at']))) ?><br>
              <span style="font-size:10px;"><?= htmlspecialchars(date('H:i', strtotime($order['created_at']))) ?> Uhr</span>
            </div>
          </td>

          <!-- Customer -->
          <td>
            <div class="customer-name"><?= htmlspecialchars($order['customer_name']) ?></div>
            <?php if ($order['customer_company']): ?>
            <div class="customer-email"><?= htmlspecialchars($order['customer_company']) ?></div>
            <?php endif; ?>
            <div class="customer-email">
              <a href="mailto:<?= htmlspecialchars($order['customer_email']) ?>" style="color:var(--teal);">
                <?= htmlspecialchars($order['customer_email']) ?>
              </a>
            </div>
          </td>

          <!-- Product -->
          <td>
            <div class="product-name"><?= htmlspecialchars($order['product_name']) ?></div>
            <?php if ($order['product_options']): ?>
            <div class="product-opts"><?= htmlspecialchars($order['product_options']) ?></div>
            <?php endif; ?>
          </td>

          <!-- Quantity -->
          <td style="text-align:center;">
            <strong><?= htmlspecialchars((string)$order['quantity']) ?></strong><br>
            <span style="font-size:11px;color:var(--muted);">Stk.</span>
          </td>

          <!-- Price -->
          <td>
            <div class="price-val"><?= fmtEur((float)$order['total_price']) ?></div>
            <div style="font-size:11px;color:var(--muted);"><?= fmtEur((float)$order['unit_price']) ?>/Stk.</div>
          </td>

          <!-- Payment -->
          <td>
            <?php if ($order['payment_method'] === 'paypal'): ?>
            <span class="pay-badge paypal">💳 PayPal</span>
            <?php else: ?>
            <span class="pay-badge bank">🏦 Vorkasse</span>
            <?php endif; ?>
            <div style="font-size:11px;color:var(--muted);margin-top:3px;">
              <?= $order['payment_status'] === 'paid' ? '<span style="color:#48bb78;">✓ Bezahlt</span>' : '<span style="color:#f5c000;">◷ Ausstehend</span>' ?>
            </div>
          </td>

          <!-- Status (with update form) -->
          <td>
            <div style="margin-bottom:.4rem;">
              <?php
              $sc = $statusColors[$order['order_status']] ?? '#5a7070';
              ?>
              <span class="status-badge" style="background:<?= $sc ?>22;color:<?= $sc ?>;border:1px solid <?= $sc ?>44;">
                <?= htmlspecialchars($order['order_status']) ?>
              </span>
            </div>
            <form method="POST" action="dashboard.php<?= $filterStatus !== 'all' ? '?filter='.urlencode($filterStatus) : '' ?>" class="status-form">
              <input type="hidden" name="action" value="update_status">
              <input type="hidden" name="order_id" value="<?= (int)$order['id'] ?>">
              <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($csrfToken) ?>">
              <select name="new_status" class="status-select">
                <option value="Eingegangen"   <?= $order['order_status']==='Eingegangen'   ? 'selected':'' ?>>Eingegangen</option>
                <option value="In Produktion" <?= $order['order_status']==='In Produktion' ? 'selected':'' ?>>In Produktion</option>
                <option value="Versendet"     <?= $order['order_status']==='Versendet'     ? 'selected':'' ?>>Versendet</option>
                <option value="Storniert"     <?= $order['order_status']==='Storniert'     ? 'selected':'' ?>>Storniert</option>
              </select>
              <button type="submit" class="btn-update">OK</button>
            </form>
          </td>

          <!-- File download -->
          <td>
            <?php if ($order['file_path']): ?>
            <form method="POST" action="dashboard.php<?= $filterStatus !== 'all' ? '?filter='.urlencode($filterStatus) : '' ?>">
              <input type="hidden" name="action" value="download_file">
              <input type="hidden" name="order_id" value="<?= (int)$order['id'] ?>">
              <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($csrfToken) ?>">
              <button type="submit" class="btn-dl" title="<?= htmlspecialchars($order['file_original_name'] ?? '') ?>">
                ↓ <?= htmlspecialchars(strlen($order['file_original_name'] ?? '') > 18 ? substr($order['file_original_name'], 0, 15).'...' : ($order['file_original_name'] ?? 'Download')) ?>
              </button>
            </form>
            <?php else: ?>
            <span class="no-file">— keine Datei</span>
            <?php endif; ?>
          </td>
        </tr>
        <?php endforeach; ?>
      </tbody>
    </table>
    <?php endif; ?>
  </div>

  <div style="margin-top:1.5rem;font-size:12px;color:var(--muted);text-align:center;">
    <?= count($orders) ?> Bestellung(en) angezeigt
    · Masar Print Shop Admin
    · <a href="dashboard.php" style="color:var(--teal);">Alle anzeigen</a>
  </div>

</main>
</body>
</html>
