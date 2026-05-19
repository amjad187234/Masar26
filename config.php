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

// Stripe — get keys from dashboard.stripe.com → Developers → API keys
// Use pk_test_ / sk_test_ while testing, pk_live_ / sk_live_ for production
define('STRIPE_PUBLIC_KEY', 'pk_REPLACE_WITH_YOUR_STRIPE_PUBLIC_KEY');
define('STRIPE_SECRET_KEY', 'sk_REPLACE_WITH_YOUR_STRIPE_SECRET_KEY');
define('STRIPE_CURRENCY',   'eur');

// Bank transfer details
define('BANK_IBAN',    'DE89 3704 0044 0532 0130 00');
define('BANK_BIC',     'COBADEFFXXX');
define('BANK_NAME',    'Masar Werbeagentur');

define('SMTP_HOST',    'smtp.hostinger.com');
define('SMTP_PORT',    587);
define('SMTP_USER',    'info@masar-werbeagentur.de');
define('SMTP_PASS',    'CHANGE_ME');
