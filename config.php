<?php
// ═══ MASAR WERBEAGENTUR — CENTRAL CONFIG ═══
// Secrets (SMTP_PASS) must be set via Hostinger → Hosting → PHP → Environment Variables.
// Run: php -r "echo password_hash('YourPassword', PASSWORD_BCRYPT);" to regenerate admin hash.
// Admin hash is a fallback — change the password in the admins DB table first.
// SECURITY: Move this to environment variable (Hostinger → PHP → Environment Variables).
// The hardcoded bcrypt hash below is a fallback-only credential. If ADMIN_PASS_HASH is not
// set via the environment, the fallback hash exposes a known credential in source control.
// Run: php -r "echo password_hash('YourPassword', PASSWORD_BCRYPT);" to generate a new hash,
// then set it exclusively via the environment variable and remove the fallback value.
define('ADMIN_PASS_HASH', getenv('ADMIN_PASS_HASH') ?: '$2y$12$DeiKE9EbzDGlL4jovtU.LeFdmHKcBRzW6PKYUfOWNDMC7CEBGG8QK'); // SECURITY: Remove hardcoded fallback hash — set ADMIN_PASS_HASH env var only
define('ADMIN_USERNAME',  getenv('ADMIN_USERNAME')  ?: 'masar-admin');

define('DB_PATH',    __DIR__ . '/data/orders.db');
define('UPLOAD_DIR', __DIR__ . '/uploads/print-files/');
define('SITE_URL',   'https://masar-werbeagentur.de');
define('ADMIN_EMAIL','info@masar-werbeagentur.de');
define('SHOP_NAME',  'Masar Werbeagentur Berlin');

define('SMTP_HOST', 'smtp.hostinger.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'info@masar-werbeagentur.de');
// Set SMTP_PASS via Hostinger → Hosting → PHP → Environment Variables
define('SMTP_PASS', getenv('SMTP_PASS') ?: '');
