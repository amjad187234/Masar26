<?php
// ═══ MASAR PRINT SHOP — SHARED EMAIL HELPER ═══
// Used by verify-payment.php and stripe-webhook.php.
declare(strict_types=1);

/**
 * Send order confirmation to customer + admin notification.
 * Returns true if emails were dispatched (does not guarantee delivery).
 *
 * @param array $order  Full order row from SQLite
 * @param string $stripeSessionId  Optional Stripe session ID for reference
 */
function sendOrderEmails(array $order, string $stripeSessionId = ''): bool
{
    $orderNumber  = $order['order_number'] ?? '–';
    $custName     = $order['customer_name'] ?? '';
    $custEmail    = $order['customer_email'] ?? '';
    $company      = $order['customer_company'] ?? '';
    $phone        = $order['customer_phone'] ?? '';
    $address      = nl2br(htmlspecialchars($order['customer_address'] ?? '', ENT_QUOTES, 'UTF-8'));
    $productName  = $order['product_name'] ?? '';
    $productOpts  = $order['product_options'] ?? '';
    $qty          = (int)   ($order['quantity']    ?? 1);
    $totalPrice   = (float) ($order['total_price'] ?? 0);
    $storedFile   = $order['file_path']          ?? '';
    $origFile     = $order['file_original_name'] ?? '';
    $notes        = $order['notes']             ?? '';

    $totalFmt = number_format($totalPrice, 2, ',', '.') . ' €';

    // ── Shared header / footer (HTML email templates) ──────────────────────
    $emailHeader = "<!DOCTYPE html><html lang='de'>
<head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head>
<body style='margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f4f7f7;'>
<div style='max-width:620px;margin:30px auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08);'>
  <div style='background:linear-gradient(135deg,#0a1628,#132e50);padding:2rem;text-align:center;border-bottom:3px solid #58d0bd;'>
    <div style='font-family:Arial Black,sans-serif;font-size:26px;font-weight:900;color:#fff;letter-spacing:3px;margin-bottom:.3rem;'>MASAR</div>
    <div style='color:#58d0bd;font-size:12px;letter-spacing:2px;text-transform:uppercase;'>Print Shop · Berlin</div>
  </div>";

    $emailFooter = "  <div style='background:#0a1628;padding:1.2rem 2rem;text-align:center;'>
    <p style='color:rgba(255,255,255,.35);font-size:12px;margin:0;'>Masar Werbeagentur · Bristolstraße 19HN · 13349 Berlin · <a href='https://masar-werbeagentur.de' style='color:#58d0bd;'>masar-werbeagentur.de</a></p>
  </div>
</div></body></html>";

    // ── Customer confirmation email ─────────────────────────────────────────
    $customerBody = $emailHeader . "
  <div style='padding:2rem;'>
    <h2 style='color:#132e50;font-size:20px;margin:0 0 .5rem;'>Vielen Dank für Ihre Bestellung!</h2>
    <p style='color:#5a7070;margin:0 0 1.5rem;'>Hallo <strong style='color:#132e50;'>{$custName}</strong>, Ihre Zahlung wurde erfolgreich bestätigt. Wir beginnen sofort mit der Produktion.</p>

    <div style='background:#f4f7f7;border-radius:8px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;text-align:center;'>
      <div style='font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#5a7070;margin-bottom:.4rem;'>Bestellnummer</div>
      <div style='font-size:24px;font-weight:900;color:#132e50;letter-spacing:2px;'>{$orderNumber}</div>
    </div>

    <table style='width:100%;border-collapse:collapse;font-size:14px;margin-bottom:1.5rem;'>
      <tr style='background:#132e50;color:#fff;'>
        <th style='padding:10px 12px;text-align:left;border-radius:6px 0 0 0;'>Produkt</th>
        <th style='padding:10px 12px;text-align:center;'>Menge</th>
        <th style='padding:10px 12px;text-align:right;border-radius:0 6px 0 0;'>Betrag</th>
      </tr>
      <tr style='border-bottom:1px solid #e0eaea;'>
        <td style='padding:12px;color:#1a2a2a;'>
          <strong>" . htmlspecialchars($productName, ENT_QUOTES, 'UTF-8') . "</strong>
          " . ($productOpts ? "<br><span style='color:#5a7070;font-size:12px;'>" . htmlspecialchars($productOpts, ENT_QUOTES, 'UTF-8') . "</span>" : '') . "
        </td>
        <td style='padding:12px;text-align:center;color:#5a7070;'>{$qty} Stk.</td>
        <td style='padding:12px;text-align:right;font-weight:700;color:#132e50;'>{$totalFmt}</td>
      </tr>
      <tr style='background:#f4f7f7;'>
        <td colspan='2' style='padding:12px;font-weight:700;color:#132e50;'>Gesamtbetrag (inkl. MwSt.)</td>
        <td style='padding:12px;text-align:right;font-size:18px;font-weight:900;color:#58d0bd;'>{$totalFmt}</td>
      </tr>
    </table>

    <div style='background:#f0f7f5;border-left:4px solid #58d0bd;padding:1.2rem 1.5rem;border-radius:0 8px 8px 0;margin-bottom:1.5rem;'>
      <strong style='color:#132e50;'>💳 Ihre Zahlung wurde erfolgreich verarbeitet.</strong>
      " . ($stripeSessionId ? "<br><span style='color:#5a7070;font-size:12px;'>Stripe-Referenz: " . htmlspecialchars($stripeSessionId, ENT_QUOTES, 'UTF-8') . "</span>" : '') . "
    </div>

    <div style='border:1px solid #e0eaea;border-radius:8px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;'>
      <strong style='color:#132e50;display:block;margin-bottom:.8rem;'>Was passiert als nächstes?</strong>
      <div style='font-size:13px;color:#5a7070;line-height:2;'>
        ✅ <strong style='color:#132e50;'>Bestellung eingegangen</strong> — soeben bestätigt<br>
        🔍 Druckdatei wird geprüft — innerhalb von 24 Stunden<br>
        🏭 Produktion startet nach Freigabe<br>
        📦 Lieferung an Ihre Adresse
      </div>
    </div>

    <p style='font-size:13px;color:#5a7070;'>Bei Fragen: <a href='mailto:" . ADMIN_EMAIL . "' style='color:#58d0bd;'>" . ADMIN_EMAIL . "</a> oder <a href='https://wa.me/491785143918' style='color:#58d0bd;'>WhatsApp</a></p>
  </div>" . $emailFooter;

    // ── Admin notification email ────────────────────────────────────────────
    $downloadLink = SITE_URL . '/admin/dashboard.php';

    $adminBody = $emailHeader . "
  <div style='background:#132e50;padding:1.5rem 2rem;'>
    <div style='font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#58d0bd;'>Neue Bestellung — Zahlung bestätigt</div>
    <div style='font-size:22px;font-weight:900;color:#fff;letter-spacing:2px;margin-top:.3rem;'>{$orderNumber}</div>
  </div>
  <div style='padding:2rem;'>
    <table style='width:100%;border-collapse:collapse;font-size:14px;'>
      <tr><td style='padding:8px 0;color:#5a7070;width:140px;'>Kunde</td><td style='padding:8px 0;font-weight:700;color:#132e50;'>" . htmlspecialchars($custName, ENT_QUOTES, 'UTF-8') . " (" . htmlspecialchars($company, ENT_QUOTES, 'UTF-8') . ")</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>E-Mail</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'><a href='mailto:" . htmlspecialchars($custEmail, ENT_QUOTES, 'UTF-8') . "' style='color:#58d0bd;'>" . htmlspecialchars($custEmail, ENT_QUOTES, 'UTF-8') . "</a></td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Telefon</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>" . htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Adresse</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>{$address}</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Produkt</td><td style='padding:8px 0;border-top:1px solid #e0eaea;font-weight:700;'>" . htmlspecialchars($productName, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Optionen</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>" . htmlspecialchars($productOpts, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Menge</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>{$qty} Stück</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Betrag</td><td style='padding:8px 0;border-top:1px solid #e0eaea;font-size:18px;font-weight:900;color:#58d0bd;'>{$totalFmt}</td></tr>
      <tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Druckdatei</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>" . htmlspecialchars($origFile, ENT_QUOTES, 'UTF-8') . "</td></tr>
      " . ($notes ? "<tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Anmerkungen</td><td style='padding:8px 0;border-top:1px solid #e0eaea;'>" . htmlspecialchars($notes, ENT_QUOTES, 'UTF-8') . "</td></tr>" : '') . "
      " . ($stripeSessionId ? "<tr><td style='padding:8px 0;color:#5a7070;border-top:1px solid #e0eaea;'>Stripe</td><td style='padding:8px 0;border-top:1px solid #e0eaea;font-size:12px;color:#5a7070;'>" . htmlspecialchars($stripeSessionId, ENT_QUOTES, 'UTF-8') . "</td></tr>" : '') . "
    </table>
    <div style='margin-top:1.5rem;'>
      <a href='{$downloadLink}' style='background:#58d0bd;color:#132e50;padding:12px 24px;border-radius:6px;font-weight:700;font-size:14px;text-decoration:none;display:inline-block;'>Dashboard öffnen →</a>
    </div>
  </div>" . $emailFooter;

    // ── Send both emails ────────────────────────────────────────────────────
    $headers  = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "From: " . SHOP_NAME . " <" . SMTP_USER . ">\r\n";
    $headers .= "X-Mailer: Masar-Mailer/1.0\r\n";

    $cleanName  = str_replace(["\r", "\n"], ' ', $custName);
    $cleanEmail = str_replace(["\r", "\n"], '',  $custEmail);

    $subjectCustomer = "Bestellbestätigung {$orderNumber} – " . SHOP_NAME;
    $subjectAdmin    = "Neue Bestellung: {$orderNumber} – {$cleanName}";

    $adminHeaders  = $headers;
    $adminHeaders .= "Reply-To: " . SMTP_USER . "\r\n";

    $customerHeaders  = $headers;
    $customerHeaders .= "Reply-To: " . SMTP_USER . "\r\n";

    @mail($cleanEmail, $subjectCustomer, $customerBody, $customerHeaders);
    @mail(ADMIN_EMAIL, $subjectAdmin,    $adminBody,    $adminHeaders);

    return true;
}
