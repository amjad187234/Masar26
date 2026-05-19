<?php
// ═══ MASAR PRINT SHOP — DATABASE INITIALIZER ═══
// Security: only runs with correct secret key GET parameter
// Usage: https://masar-werbeagentur.de/api/init-db.php?key=MASAR_INIT_2026
// DELETE OR RENAME THIS FILE after first run in production!

declare(strict_types=1);
header('Content-Type: text/html; charset=utf-8');

// ── Secret key gate ──────────────────────────────────────────
$REQUIRED_KEY = 'MASAR_INIT_2026';
$provided     = $_GET['key'] ?? '';

if (!hash_equals($REQUIRED_KEY, $provided)) {
    http_response_code(403);
    die('<!DOCTYPE html><html><body><h2>403 Forbidden</h2><p>Falscher oder fehlender Schlüssel.</p></body></html>');
}

// ── Load config ───────────────────────────────────────────────
$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    die('<h2>Fehler</h2><p>config.php nicht gefunden unter: ' . htmlspecialchars($configPath) . '</p>');
}
require $configPath;

$log = [];
$errors = [];

function logOk(string $msg): void  { global $log;    $log[]    = $msg; }
function logErr(string $msg): void { global $errors; $errors[] = $msg; }

// ── Create /data/ directory ───────────────────────────────────
$dataDir = dirname(DB_PATH);
if (!is_dir($dataDir)) {
    if (mkdir($dataDir, 0750, true)) {
        logOk("Verzeichnis erstellt: {$dataDir}");
    } else {
        logErr("Konnte Verzeichnis nicht erstellen: {$dataDir}");
    }
} else {
    logOk("Verzeichnis vorhanden: {$dataDir}");
}

// ── Create /uploads/print-files/ directory ────────────────────
if (!is_dir(UPLOAD_DIR)) {
    if (mkdir(UPLOAD_DIR, 0750, true)) {
        logOk('Upload-Verzeichnis erstellt: ' . UPLOAD_DIR);
    } else {
        logErr('Konnte Upload-Verzeichnis nicht erstellen: ' . UPLOAD_DIR);
    }
} else {
    logOk('Upload-Verzeichnis vorhanden: ' . UPLOAD_DIR);
}

// ── Open / create SQLite database ────────────────────────────
try {
    $pdo = new PDO('sqlite:' . DB_PATH, null, null, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA journal_mode=WAL;');
    $pdo->exec('PRAGMA foreign_keys=ON;');
    logOk('SQLite-Datenbank geöffnet: ' . DB_PATH);
} catch (PDOException $e) {
    logErr('Datenbankfehler: ' . $e->getMessage());
    renderPage($log, $errors);
    exit;
}

// ── Create orders table ───────────────────────────────────────
$pdo->exec("
CREATE TABLE IF NOT EXISTS orders (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number        TEXT    NOT NULL UNIQUE,
    created_at          TEXT    NOT NULL DEFAULT (datetime('now')),
    customer_name       TEXT    NOT NULL,
    customer_email      TEXT    NOT NULL,
    customer_company    TEXT,
    customer_phone      TEXT,
    customer_address    TEXT,
    product_name        TEXT    NOT NULL,
    product_options     TEXT,
    quantity            INTEGER NOT NULL DEFAULT 1,
    unit_price          REAL    NOT NULL DEFAULT 0,
    total_price         REAL    NOT NULL DEFAULT 0,
    payment_method      TEXT    NOT NULL DEFAULT 'bank',
    payment_status      TEXT    NOT NULL DEFAULT 'pending',
    order_status        TEXT    NOT NULL DEFAULT 'Eingegangen',
    file_path           TEXT,
    file_original_name  TEXT,
    notes               TEXT
);
");
logOk('Tabelle "orders" OK.');

// ── Create admins table ───────────────────────────────────────
$pdo->exec("
CREATE TABLE IF NOT EXISTS admins (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT    NOT NULL UNIQUE,
    pass_hash   TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
");
logOk('Tabelle "admins" OK.');

// ── Insert default admin if not exists ────────────────────────
$defaultPassword = 'MasarAdmin2026!';
$hash            = password_hash($defaultPassword, PASSWORD_BCRYPT, ['cost' => 12]);
$username        = 'masar-admin';

$exists = $pdo->prepare('SELECT id FROM admins WHERE username = :u');
$exists->execute([':u' => $username]);

if (!$exists->fetch()) {
    $ins = $pdo->prepare('INSERT INTO admins (username, pass_hash) VALUES (:u, :h)');
    $ins->execute([':u' => $username, ':h' => $hash]);
    logOk("Standard-Admin erstellt: <strong>{$username}</strong> / Passwort: <strong>{$defaultPassword}</strong>");
    logOk("Bitte Passwort sofort ändern nach dem ersten Login!");
} else {
    logOk("Admin-Benutzer \"{$username}\" bereits vorhanden – kein Eintrag überschrieben.");
}

// ── Set file permissions ──────────────────────────────────────
chmod(DB_PATH, 0640);
logOk('Datenbankberechtigungen gesetzt (0640).');

// ── Render result page ────────────────────────────────────────
renderPage($log, $errors);

function renderPage(array $log, array $errors): void {
    $success = empty($errors);
    $statusColor = $success ? '#58d0bd' : '#e53e3e';
    $statusText  = $success ? 'Initialisierung erfolgreich!' : 'Es sind Fehler aufgetreten!';
    ?>
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DB Init – Masar Print Shop</title>
<style>
  body { font-family: system-ui, sans-serif; background: #0a1628; color: #e0eaea; margin: 0; padding: 2rem; }
  .card { background: #132e50; border-radius: 12px; max-width: 700px; margin: 2rem auto; padding: 2rem; border-top: 4px solid <?= $statusColor ?>; }
  h1 { font-size: 1.5rem; margin-bottom: .5rem; color: <?= $statusColor ?>; }
  h2 { font-size: 1.1rem; margin: 1.5rem 0 .5rem; color: #58d0bd; }
  .item { padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,.06); font-size: 14px; }
  .item::before { content: '✓ '; color: #58d0bd; }
  .err { color: #fc8181; }
  .err::before { content: '✗ '; color: #fc8181; }
  .warn { background: rgba(245,192,0,.1); border: 1px solid rgba(245,192,0,.3); border-radius: 8px; padding: 1rem; margin-top: 1.5rem; font-size: 13px; color: #f5c000; }
</style>
</head>
<body>
<div class="card">
  <h1><?= $statusText ?></h1>
  <p style="color:rgba(255,255,255,.5);font-size:13px;">Masar Print Shop · Datenbankinitialisierung</p>

  <?php if (!empty($log)): ?>
  <h2>Protokoll</h2>
  <?php foreach ($log as $entry): ?>
    <div class="item"><?= $entry ?></div>
  <?php endforeach; ?>
  <?php endif; ?>

  <?php if (!empty($errors)): ?>
  <h2>Fehler</h2>
  <?php foreach ($errors as $err): ?>
    <div class="item err"><?= htmlspecialchars($err) ?></div>
  <?php endforeach; ?>
  <?php endif; ?>

  <div class="warn">
    ⚠ <strong>Sicherheitshinweis:</strong> Bitte diese Datei nach der Initialisierung
    sofort umbenennen oder löschen! Sie sollte nie öffentlich zugänglich bleiben.
    <br><br>
    Standard-Login: <strong>masar-admin</strong> / <strong>MasarAdmin2026!</strong>
    &rarr; Bitte sofort in der Datenbank ändern.
  </div>
</div>
</body>
</html>
<?php
}
