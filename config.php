<?php
// ═══ MASAR WERBEAGENTUR — CENTRAL CONFIG ═══
// Secrets (SMTP_PASS) must be set via Hostinger → Hosting → PHP → Environment Variables.
// Run: php -r "echo password_hash('YourPassword', PASSWORD_BCRYPT);" to regenerate admin hash.
// Admin hash is a fallback — change the password in the admins DB table first.
define('ADMIN_PASS_HASH', getenv('ADMIN_PASS_HASH') ?: '$2y$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uHV1kz68W');
define('ADMIN_USERNAME',  getenv('ADMIN_USERNAME')  ?: 'masar-admin');

define('DB_PATH',    __DIR__ . '/data/orders.db');
define('SITE_URL',   'https://masar-werbeagentur.de');
define('ADMIN_EMAIL','info@masar-werbeagentur.de');

define('SMTP_HOST', 'smtp.hostinger.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'info@masar-werbeagentur.de');
// Set SMTP_PASS via Hostinger → Hosting → PHP → Environment Variables
define('SMTP_PASS', getenv('SMTP_PASS') ?: '');
