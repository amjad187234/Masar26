<?php
// ═══ MASAR PRINT SHOP — ADMIN LOGIN ═══
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

// Load config
$configPath = dirname(__DIR__) . '/config.php';
if (!file_exists($configPath)) {
    die('Konfigurationsfehler: config.php nicht gefunden.');
}
require $configPath;

// Already logged in → redirect
if (!empty($_SESSION['admin_logged_in'])) {
    header('Location: dashboard.php');
    exit;
}

$error        = '';
$loginAttempt = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $loginAttempt = true;
    $username     = trim($_POST['username'] ?? '');
    $password     = $_POST['password'] ?? '';

    // Basic brute-force protection via session counter
    if (!isset($_SESSION['fail_count'])) {
        $_SESSION['fail_count']    = 0;
        $_SESSION['fail_lockout'] = 0;
    }

    // Lockout check (15 minutes after 5 failed attempts)
    if ($_SESSION['fail_count'] >= 5 && (time() - $_SESSION['fail_lockout']) < 900) {
        $remaining = ceil((900 - (time() - $_SESSION['fail_lockout'])) / 60);
        $error = "Zu viele fehlgeschlagene Versuche. Bitte warten Sie noch {$remaining} Minute(n).";
    } elseif (empty($username) || empty($password)) {
        $error = 'Benutzername und Passwort sind erforderlich.';
        $_SESSION['fail_count']++;
        $_SESSION['fail_lockout'] = time();
    } else {
        // Look up admin in database
        $dbOk = false;
        $storedHash = null;

        try {
            if (file_exists(DB_PATH)) {
                $pdo  = new PDO('sqlite:' . DB_PATH, null, null, [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                ]);
                $stmt = $pdo->prepare('SELECT pass_hash FROM admins WHERE username = :u LIMIT 1');
                $stmt->execute([':u' => $username]);
                $row  = $stmt->fetch(PDO::FETCH_ASSOC);
                if ($row) {
                    $storedHash = $row['pass_hash'];
                    $dbOk       = true;
                }
            }
        } catch (PDOException $e) {
            // Fall through to config-based fallback
        }

        // Fallback: also check against hardcoded config hash if DB unavailable
        $validUsername = ($username === ADMIN_USERNAME);
        $validPassword = false;

        if ($dbOk && $storedHash) {
            $validPassword = password_verify($password, $storedHash);
        } else {
            // Fallback to config hash
            $validPassword = ($validUsername && password_verify($password, ADMIN_PASS_HASH));
        }

        if ($validUsername && $validPassword) {
            // Regenerate session ID to prevent session fixation
            session_regenerate_id(true);
            $_SESSION['admin_logged_in'] = true;
            $_SESSION['admin_user']      = $username;
            $_SESSION['fail_count']      = 0;
            header('Location: dashboard.php');
            exit;
        } else {
            $error = 'Ungültiger Benutzername oder Passwort.';
            $_SESSION['fail_count']++;
            $_SESSION['fail_lockout'] = time();
            // Small delay to slow brute force
            usleep(500000);
        }
    }
}
?><!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin Login – Masar Print Shop</title>
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<style>
/* ── Tokens ── */
:root {
  --teal:#58d0bd; --teal-d:#3ab8a5;
  --navy:#132e50; --navy2:#1e4275; --navy3:#0a1628;
  --border:#e0eaea; --r:10px;
}
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { height:100%; }
body {
  font-family:'Segoe UI',system-ui,Arial,sans-serif;
  background:linear-gradient(150deg,var(--navy3) 0%,var(--navy) 60%,#0d4a4a 100%);
  min-height:100vh;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  padding:2rem;
  position:relative;
  overflow:hidden;
}
body::before {
  content:'';
  position:absolute; inset:0;
  background:radial-gradient(ellipse at 60% 40%,rgba(88,208,189,.1) 0%,transparent 60%);
  pointer-events:none;
}

/* ── Card ── */
.login-card {
  background:rgba(255,255,255,.04);
  border:1px solid rgba(88,208,189,.18);
  border-radius:16px;
  padding:2.5rem;
  width:100%;
  max-width:400px;
  backdrop-filter:blur(12px);
  box-shadow:0 24px 64px rgba(0,0,0,.4);
  position:relative;
  z-index:1;
}

/* ── Brand ── */
.login-brand {
  text-align:center;
  margin-bottom:2rem;
}
.login-logo {
  font-family:'Arial Black',Arial,sans-serif;
  font-weight:900;
  font-size:32px;
  color:#fff;
  letter-spacing:4px;
  margin-bottom:.25rem;
}
.login-logo span { color:var(--teal); }
.login-subtitle {
  font-size:11px;
  letter-spacing:2.5px;
  text-transform:uppercase;
  color:rgba(88,208,189,.6);
}

/* ── Form ── */
.form-group { margin-bottom:1.2rem; }
.form-label {
  display:block;
  font-size:11px;
  font-weight:700;
  letter-spacing:1.5px;
  text-transform:uppercase;
  color:rgba(255,255,255,.5);
  margin-bottom:.5rem;
}
.form-input {
  width:100%;
  background:rgba(255,255,255,.06);
  border:1.5px solid rgba(255,255,255,.12);
  border-radius:8px;
  padding:12px 16px;
  color:#fff;
  font-size:15px;
  font-family:inherit;
  outline:none;
  transition:border-color .2s, background .2s;
  -webkit-appearance:none;
}
.form-input::placeholder { color:rgba(255,255,255,.2); }
.form-input:focus {
  border-color:var(--teal);
  background:rgba(88,208,189,.06);
}

/* ── Error ── */
.login-error {
  background:rgba(229,62,62,.12);
  border:1px solid rgba(229,62,62,.3);
  border-radius:8px;
  padding:.75rem 1rem;
  color:#fc8181;
  font-size:13px;
  margin-bottom:1.2rem;
  display:flex;
  align-items:center;
  gap:.5rem;
}

/* ── Submit ── */
.btn-login {
  width:100%;
  background:var(--teal);
  color:var(--navy);
  border:none;
  border-radius:8px;
  padding:14px;
  font-size:15px;
  font-weight:800;
  font-family:inherit;
  cursor:pointer;
  letter-spacing:.5px;
  transition:background .2s, transform .2s, box-shadow .2s;
  margin-top:.5rem;
}
.btn-login:hover {
  background:var(--teal-d);
  transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(88,208,189,.35);
}
.btn-login:active { transform:translateY(0); }

/* ── Footer ── */
.login-footer {
  text-align:center;
  margin-top:1.5rem;
  font-size:12px;
  color:rgba(255,255,255,.2);
}
.login-footer a { color:rgba(88,208,189,.5); text-decoration:none; }
.login-footer a:hover { color:var(--teal); }
</style>
</head>
<body>

<div class="login-card">
  <div class="login-brand">
    <div class="login-logo">M<span>A</span>SAR</div>
    <div class="login-subtitle">Admin · Print Shop</div>
  </div>

  <?php if ($error): ?>
  <div class="login-error">
    <span>⚠</span>
    <span><?= htmlspecialchars($error) ?></span>
  </div>
  <?php endif; ?>

  <form method="POST" action="login.php" autocomplete="off" novalidate>
    <div class="form-group">
      <label class="form-label" for="username">Benutzername</label>
      <input
        class="form-input"
        type="text"
        id="username"
        name="username"
        value="<?= htmlspecialchars($_POST['username'] ?? '') ?>"
        placeholder="masar-admin"
        autocomplete="username"
        required
        autofocus
      >
    </div>
    <div class="form-group">
      <label class="form-label" for="password">Passwort</label>
      <input
        class="form-input"
        type="password"
        id="password"
        name="password"
        placeholder="••••••••••••"
        autocomplete="current-password"
        required
      >
    </div>
    <button type="submit" class="btn-login">Anmelden →</button>
  </form>

  <div class="login-footer">
    <a href="/">← Zurück zur Website</a>
  </div>
</div>

</body>
</html>
