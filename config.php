<?php
// ═══ MASAR PRINT SHOP — CENTRAL CONFIG ═══
// IMPORTANT: This file contains secrets. Add config.php to .gitignore before deploying!
// Run: php -r "echo password_hash('YourPassword', PASSWORD_BCRYPT);" to regenerate hash
define('ADMIN_PASS_HASH', '$2y$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uHV1kz68W'); // default: "password" — CHANGE THIS
define('ADMIN_USERNAME', 'masar-admin');

define('DB_PATH',      __DIR__ . '/data/orders.db');
define('UPLOAD_DIR',   __DIR__ . '/uploads/print-files/');
define('MAX_FILE_MB',  50);
define('SITE_URL',     'https://masar-werbeagentur.de');
define('SHOP_URL',     SITE_URL . '/shop/');
define('ADMIN_EMAIL',  'info@masar-werbeagentur.de');
define('SHOP_NAME',    'Masar Print Shop');

// Stripe — Publishable key is safe in source code (frontend-visible by design).
// SECRET KEY: NEVER commit. Set on Hostinger → Hosting → PHP → Environment Variables:
//   STRIPE_SECRET_KEY    = sk_live_...
//   STRIPE_WEBHOOK_SECRET = whsec_...  (Stripe Dashboard → Webhooks → signing secret)
define('STRIPE_PUBLIC_KEY',     'pk_live_51TUTo5PDPRRzGXEAAu5ic8j1k5EaDR4XZSwt2IsIrRhSBu83pei1jcHtYdCqJ64q01eEBNcqC8NklCCqOPLAeQh200iecJmJDq');
define('STRIPE_SECRET_KEY',     getenv('STRIPE_SECRET_KEY')     ?: '');
define('STRIPE_WEBHOOK_SECRET', getenv('STRIPE_WEBHOOK_SECRET') ?: '');
define('STRIPE_CURRENCY',       'eur');

// Bank transfer details
define('BANK_IBAN',    'DE89 3704 0044 0532 0130 00');
define('BANK_BIC',     'COBADEFFXXX');
define('BANK_NAME',    'Masar Werbeagentur');

define('SMTP_HOST',    'smtp.hostinger.com');
define('SMTP_PORT',    587);
define('SMTP_USER',    'info@masar-werbeagentur.de');
define('SMTP_PASS',    'CHANGE_ME');
