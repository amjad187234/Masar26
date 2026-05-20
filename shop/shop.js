'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// MASAR PRINT SHOP — shop.js
// ─────────────────────────────────────────────────────────────────────────────
// Architecture:
//   CATALOG      → Product definitions with wholesale tier pricing
//   calcPrice()  → Applies reseller markup + option multipliers
//   cartXxx()    → Cart CRUD backed by localStorage
//   renderXxx()  → DOM rendering functions
//   filterXxx()  → Category filter tabs
//   DOMContentLoaded → Bootstrap
// ═══════════════════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────────────────
// RESELLER MARKUP ENGINE
// ─────────────────────────────────────────────────────────────────────────────
// Change RESELLER_MARKUP to adjust your profit margin on ALL products.
// 1.30 = 30% above wholesale. Client pays: wholesale × 1.30
// Example: wholesale unit €0.10 → client pays €0.13/unit
// ───────────────────────────────────────────────────────────────────────────────
const RESELLER_MARKUP = 1.30;

// ───────────────────────────────────────────────────────────────────────────────
// SPEED SURCHARGES
// ─────────────────────────────────────────────────────────────────────────────
// Formula: Client Price = (wsUnit * optMult * RESELLER_MARKUP * qty) * (1 + surcharge)
// ───────────────────────────────────────────────────────────────────────────────
const SPEED_SURCHARGES = {
  standard:  { label: 'Standard (3–5 Werktage)',               surcharge: 0.00 },
  'next-day':{ label: 'Next-Day Service (nächster Werktag)',    surcharge: 0.25 },
  'same-day':{ label: 'Same-Day Service (Bestellung bis 11 Uhr)', surcharge: 0.50 },
};
let activeSurcharge = 0.0;

// ───────────────────────────────────────────────────────────────────────────────
// PRODUCT CATALOG
// ─────────────────────────────────────────────────────────────────────────────
// Each product has:
//   id       → unique slug used in DOM element IDs
//   name     → display name
//   emoji    → decorative emoji for the card header
//   category → filter category string
//   desc     → short description
//   options  → key → array of {label, mult} objects
//              (mult is a price multiplier applied on top of tier price)
//   tiers    → array of {qty, ws} where ws = total wholesale price for that qty
// ───────────────────────────────────────────────────────────────────────────────
const CATALOG = [
  {
    id: 'flyer-a5', name: 'Flyer A5', emoji: '📄', category: 'Flyer',
    desc: 'Einseitig & doppelseitig – Papier und Grammatur frei wählbar',
    options: {
      sides: [{label:'Einseitig',mult:1.0},{label:'Doppelseitig',mult:1.35}]
    },
    paperMatrix: {
      'Bilderdruck matt':      { mult:1.00, grammages:[{label:'100g',mult:0.85},{label:'135g',mult:1.00},{label:'170g',mult:1.12},{label:'250g',mult:1.28},{label:'300g',mult:1.38},{label:'350g',mult:1.48}] },
      'Bilderdruck glänzend':  { mult:1.05, grammages:[{label:'100g',mult:0.85},{label:'135g',mult:1.00},{label:'170g',mult:1.12},{label:'250g',mult:1.28},{label:'300g',mult:1.38}] },
      'Naturpapier':           { mult:1.12, grammages:[{label:'300g',mult:1.38}] },
      'Recycling Bilderdruck': { mult:0.95, grammages:[{label:'135g',mult:1.00},{label:'300g',mult:1.38}] },
    },
    tiers: [
      {qty:250,  ws:18.50},
      {qty:500,  ws:24.00},
      {qty:1000, ws:32.00},
      {qty:2500, ws:54.00},
      {qty:5000, ws:82.00},
      {qty:10000,ws:140.00}
    ]
  },
  {
    id: 'flyer-a4', name: 'Flyer A4', emoji: '📰', category: 'Flyer',
    desc: 'DIN A4 – Papier und Grammatur frei wählbar',
    options: {
      sides: [{label:'Einseitig',mult:1.0},{label:'Doppelseitig',mult:1.35}]
    },
    paperMatrix: {
      'Bilderdruck matt':      { mult:1.00, grammages:[{label:'100g',mult:0.85},{label:'135g',mult:1.00},{label:'170g',mult:1.12},{label:'250g',mult:1.28},{label:'300g',mult:1.38},{label:'350g',mult:1.48}] },
      'Bilderdruck glänzend':  { mult:1.05, grammages:[{label:'100g',mult:0.85},{label:'135g',mult:1.00},{label:'170g',mult:1.12},{label:'250g',mult:1.28},{label:'300g',mult:1.38}] },
      'Naturpapier':           { mult:1.12, grammages:[{label:'300g',mult:1.38}] },
      'Recycling Bilderdruck': { mult:0.95, grammages:[{label:'135g',mult:1.00},{label:'300g',mult:1.38}] },
    },
    tiers: [
      {qty:250,  ws:22.00},
      {qty:500,  ws:30.00},
      {qty:1000, ws:42.00},
      {qty:2500, ws:70.00},
      {qty:5000, ws:108.00}
    ]
  },
  {
    id: 'visitenkarten', name: 'Visitenkarten', emoji: '📇', category: 'Visitenkarten',
    desc: '85×55mm, beidseitig 4/4-farbig – Papier und Grammatur frei wählbar',
    options: {},
    paperMatrix: {
      'Bilderdruck matt':          { mult:1.00, grammages:[{label:'300g',mult:1.00},{label:'350g',mult:1.08}] },
      'Bilderdruck glänzend':      { mult:1.05, grammages:[{label:'300g',mult:1.00}] },
      'Naturpapier':               { mult:1.12, grammages:[{label:'300g',mult:1.00}] },
      'Premium Multiloft Rough':   { mult:1.45, grammages:[{label:'750g (3-fach, Farbkern)',mult:1.00},{label:'1020g (4-fach, Farbkern)',mult:1.28}] },
      'Premium Multiloft Smooth':  { mult:1.52, grammages:[{label:'810g (3-fach, Farbkern)',mult:1.00},{label:'1080g (4-fach, Farbkern)',mult:1.28}] },
    },
    tiers: [
      {qty:100,  ws:12.00},
      {qty:250,  ws:16.00},
      {qty:500,  ws:22.00},
      {qty:1000, ws:30.00},
      {qty:2500, ws:55.00}
    ]
  },
  {
    id: 'aufkleber', name: 'Aufkleber & Etiketten', emoji: '🏷️', category: 'Aufkleber',
    desc: 'DIN A5 Bögen, wetterfest, UV-beständig, weiße Folie',
    options: {
      finish: [{label:'Glanz',mult:1.0},{label:'Matt',mult:1.08},{label:'Transparent',mult:1.16}]
    },
    tiers: [
      {qty:50,   ws:14.00},
      {qty:100,  ws:20.00},
      {qty:250,  ws:38.00},
      {qty:500,  ws:62.00},
      {qty:1000, ws:98.00}
    ]
  },
  {
    id: 'rollup', name: 'Roll-up Display', emoji: '🪧', category: 'Werbemittel',
    desc: '85×200cm, inkl. Aluminiumgehäuse & Tragetasche',
    options: {
      model: [{label:'Standard Silber',mult:1.0},{label:'Premium Schwarz',mult:1.32}]
    },
    tiers: [
      {qty:1, ws:41.52},
      {qty:2, ws:39.00},
      {qty:3, ws:37.00},
      {qty:5, ws:34.50}
    ]
  },
  {
    id: 'plakate', name: 'Allwetter- & Wahlplakate', emoji: '📋', category: 'Plakate',
    desc: 'Wetterfest, Hohlkammerplatte 3mm, Außenwerbung',
    options: {
      size: [
        {label:'DIN A2 (42×59cm)', mult:0.68},
        {label:'DIN A1 (59×84cm)', mult:1.0},
        {label:'DIN A0 (84×119cm)',mult:1.62}
      ]
    },
    tiers: [
      {qty:5,   ws:32.00},
      {qty:10,  ws:52.00},
      {qty:25,  ws:98.00},
      {qty:50,  ws:160.00},
      {qty:100, ws:260.00}
    ]
  },
  {
    id: 'broschuren', name: 'Broschüren & Kataloge', emoji: '📚', category: 'Broschüren',
    desc: 'Klammer- oder Klebebindung, 90g/m² Innenseiten, Hochglanzcover',
    options: {
      binding: [{label:'Klammerheftung',mult:1.0},{label:'Klebebindung',mult:1.22}],
      pages:   [
        {label:'8 Seiten',  mult:0.68},
        {label:'16 Seiten', mult:1.0},
        {label:'32 Seiten', mult:1.55},
        {label:'48 Seiten', mult:2.05}
      ]
    },
    tiers: [
      {qty:100,  ws:58.00},
      {qty:250,  ws:92.00},
      {qty:500,  ws:150.00},
      {qty:1000, ws:240.00}
    ]
  },
  {
    id: 'standbodenbeutel', name: 'Standbodenbeutel', emoji: '🛍️', category: 'Verpackung',
    desc: 'Individuelle Verpackungen, lebensmittelecht, Zip-Verschluss optional',
    options: {
      size: [
        {label:'70×180mm',  mult:0.78},
        {label:'100×150mm', mult:1.0},
        {label:'130×220mm', mult:1.36},
        {label:'160×240mm', mult:1.68}
      ]
    },
    tiers: [
      {qty:100,  ws:65.00},
      {qty:250,  ws:95.00},
      {qty:500,  ws:145.00},
      {qty:1000, ws:220.00}
    ]
  },
  {
    id: 'kugelschreiber', name: 'Kugelschreiber Werbeartikel', emoji: '🖊️', category: 'Werbeartikel',
    desc: 'Hochwertige Werbekugelschreiber inkl. Logo-Druck oder Gravur',
    options: {
      print: [
        {label:'1-farbig Druck', mult:1.0},
        {label:'4-farbig Druck', mult:1.22},
        {label:'Laser-Gravur',   mult:1.38}
      ]
    },
    tiers: [
      {qty:50,   ws:45.00},
      {qty:100,  ws:72.00},
      {qty:250,  ws:140.00},
      {qty:500,  ws:220.00},
      {qty:1000, ws:360.00}
    ]
  },
];

// ───────────────────────────────────────────────────────────────────────────────
// CART STATE
// Persisted in localStorage under key 'masarCart'.
// Each cart item: { id, name, emoji, opts:{}, qty, clientUnit, clientTotal }
// ───────────────────────────────────────────────────────────────────────────────
let cart = [];

try {
  const stored = localStorage.getItem('masarCart');
  if (stored) cart = JSON.parse(stored);
  if (!Array.isArray(cart)) cart = [];
} catch (e) {
  cart = [];
}

// ───────────────────────────────────────────────────────────────────────────────
// PRICE CALCULATION
// ─────────────────────────────────────────────────────────────────────────────
/**
 * Calculate client-facing price for a product.
 *
 * Algorithm:
 *   1. Find the best matching price tier (largest tier qty <= requested qty,
 *      or the smallest tier if qty < all tiers).
 *   2. Compute per-unit wholesale: tier.ws / tier.qty
 *   3. Multiply by all selected option multipliers (stacked).
 *   4. Apply RESELLER_MARKUP.
 *   5. Multiply by requested qty for the total.
 *
 * @param {Object}  product      - Product from CATALOG
 * @param {number}  qty          - Requested quantity
 * @param {Object}  selectedOpts - Map of optionKey → chosen label
 * @returns {Object} { wsUnit, clientUnit, clientTotal, displayUnit, displayTotal, markup }
 */
function calcPrice(product, qty, selectedOpts) {
  // Sort tiers ascending by qty
  const sorted = [...product.tiers].sort((a, b) => a.qty - b.qty);

  // Find the appropriate tier: last tier whose qty <= requested qty
  let tier = sorted[0]; // fallback to minimum tier
  for (const t of sorted) {
    if (qty >= t.qty) tier = t;
  }

  // Per-unit wholesale cost at this tier
  const wsUnit = tier.ws / tier.qty;

  // Stack standard option multipliers (button groups)
  let optMult = 1.0;
  if (selectedOpts) {
    for (const key of Object.keys(selectedOpts)) {
      if (key === 'papier' || key === 'grammatur') continue; // handled below
      const optGroup = product.options?.[key];
      if (!optGroup) continue;
      const chosen = optGroup.find(o => o.label === selectedOpts[key]);
      if (chosen) optMult *= chosen.mult;
    }
  }

  // Paper matrix multipliers (paper type × grammage)
  if (product.paperMatrix && selectedOpts?.papier) {
    const paperCfg = product.paperMatrix[selectedOpts.papier];
    if (paperCfg) {
      optMult *= paperCfg.mult;
      if (selectedOpts.grammatur) {
        const gramCfg = paperCfg.grammages.find(g => g.label === selectedOpts.grammatur);
        if (gramCfg) optMult *= gramCfg.mult;
      }
    }
  }

  // Apply reseller markup, then speed surcharge on total
  const clientUnitPrice = wsUnit * optMult * RESELLER_MARKUP;
  const clientTotal     = clientUnitPrice * qty * (1 + activeSurcharge);

  return {
    wsUnit:       wsUnit,
    clientUnit:   clientUnitPrice,
    clientTotal:  clientTotal,
    displayUnit:  formatEur(clientUnitPrice),
    displayTotal: formatEur(clientTotal),
    markup:       RESELLER_MARKUP,
    surcharge:    activeSurcharge,
  };
}

/**
 * Format a number as Euro currency string (German locale).
 * Example: 24.5 → "24,50 €"
 */
function formatEur(n) {
  return n.toLocaleString('de-DE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }) + ' €';
}

// ───────────────────────────────────────────────────────────────────────────────
// CART OPERATIONS
// ───────────────────────────────────────────────────────────────────────────────

/** Persist cart to localStorage. */
function cartSave() {
  try {
    localStorage.setItem('masarCart', JSON.stringify(cart));
  } catch (e) {
    console.warn('localStorage nicht verfügbar:', e);
  }
}

/** Return total item count across all cart lines. */
function cartCount() {
  return cart.reduce((sum, item) => sum + item.qty, 0);
}

/** Return total price across all cart lines. */
function cartTotal() {
  return cart.reduce((sum, item) => sum + item.clientTotal, 0);
}

/**
 * Add an item to the cart.
 * If the same product + same options already exists, merge quantities.
 */
function cartAdd(item) {
  // Check if identical item (same id + same options) already in cart
  const optsKey = JSON.stringify(item.opts);
  const existing = cart.find(c => c.id === item.id && JSON.stringify(c.opts) === optsKey);

  if (existing) {
    // Merge: add quantities, recalculate total
    existing.qty        += item.qty;
    existing.clientTotal = existing.clientUnit * existing.qty;
  } else {
    cart.push(item);
  }

  cartSave();
  cartRender();
  cartFlash();

  // Open drawer briefly to confirm
  const drawer = document.getElementById('cartDrawer');
  if (drawer) drawer.classList.add('open');
}

/**
 * Remove item at index from cart.
 */
function cartRemove(idx) {
  cart.splice(idx, 1);
  cartSave();
  cartRender();
}

/**
 * Render the cart drawer UI.
 * Updates badge count, item list, total, and checkout button state.
 */
function cartRender() {
  // Badge count
  const badge = document.getElementById('cartBadge');
  if (badge) badge.textContent = cartCount();

  const panel  = document.getElementById('cartItems');
  const empty  = document.getElementById('cartEmpty');
  const totEl  = document.getElementById('cartTotal');
  const chkBtn = document.getElementById('cartCheckout');

  if (!panel) return;

  if (cart.length === 0) {
    panel.innerHTML = '';
    if (empty)  empty.style.display = 'block';
    if (totEl)  totEl.textContent   = '0,00 €';
    if (chkBtn) chkBtn.disabled     = true;
    return;
  }

  if (empty) empty.style.display = 'none';
  if (chkBtn) chkBtn.disabled = false;

  // Render each cart line
  panel.innerHTML = cart.map((item, i) => `
    <div class="cart-item">
      <div class="cart-item-info">
        <span class="cart-item-name">${item.emoji} ${escapeHtml(item.name)}</span>
        <span class="cart-item-opts">${escapeHtml(Object.values(item.opts || {}).join(' · '))} · ${item.qty} Stk.</span>
      </div>
      <div class="cart-item-right">
        <span class="cart-item-price">${formatEur(item.clientTotal)}</span>
        <button class="cart-item-del" onclick="cartRemove(${i})" aria-label="Entfernen">×</button>
      </div>
    </div>
  `).join('');

  if (totEl) totEl.textContent = formatEur(cartTotal());
}

/**
 * Flash animation on the cart button to indicate item was added.
 */
function cartFlash() {
  const btn = document.getElementById('cartBtn');
  if (!btn) return;
  btn.classList.add('cart-flash');
  setTimeout(() => btn.classList.remove('cart-flash'), 600);
}

/**
 * Toggle cart drawer open/closed.
 */
function cartToggle() {
  const drawer = document.getElementById('cartDrawer');
  if (!drawer) return;
  drawer.classList.toggle('open');
}

/**
 * Transfer cart to sessionStorage and navigate to checkout.
 */
function cartGoCheckout() {
  if (cart.length === 0) return;
  try {
    sessionStorage.setItem('masarCheckoutCart', JSON.stringify(cart));
  } catch (e) {
    console.warn('sessionStorage nicht verfügbar:', e);
  }
  window.location.href = '/shop/checkout.html';
}

// ───────────────────────────────────────────────────────────────────────────────
// CATALOG RENDERING
// ───────────────────────────────────────────────────────────────────────────────

/**
 * Render the product catalog grid.
 * @param {string|null} filterCategory - Category to filter by, or null for all.
 */
function renderCatalog(filterCategory) {
  const grid = document.getElementById('catalogGrid');
  if (!grid) return;

  const items = filterCategory
    ? CATALOG.filter(p => p.category === filterCategory)
    : CATALOG;

  grid.innerHTML = items.map(p => renderProductCard(p)).join('');
}

/**
 * Generate HTML for a single product card.
 * Includes: header, description, option buttons, qty control, live price, tier table.
 */
function renderProductCard(p) {
  // Base price from first (cheapest) tier, no option multipliers, for "ab X/Stk." display
  const firstTier  = p.tiers[0];
  const basePrice  = (firstTier.ws / firstTier.qty) * RESELLER_MARKUP;

  // Render each option group
  const optGroupsHtml = Object.keys(p.options || {}).map(key => {
    const opts = p.options[key];
    // Human-readable label for the key
    const keyLabel = {
      finish:  'Veredelung',
      sides:   'Seiten',
      model:   'Modell',
      size:    'Format',
      binding: 'Bindung',
      pages:   'Seitenanzahl',
      print:   'Druckverfahren',
    }[key] || (key.charAt(0).toUpperCase() + key.slice(1));

    const btnHtml = opts.map((o, i) =>
      `<button class="opt-btn${i === 0 ? ' active' : ''}" data-val="${escapeAttr(o.label)}" onclick="optSelect(this,'${p.id}','${key}')">${escapeHtml(o.label)}</button>`
    ).join('');

    return `
      <div class="prod-opt-group">
        <label class="prod-opt-lbl">${keyLabel}</label>
        <div class="prod-opt-btns" data-key="${key}">${btnHtml}</div>
      </div>`;
  }).join('');

  // Paper & Grammage dependent selectors (for products with paperMatrix)
  let paperHtml = '';
  if (p.paperMatrix) {
    const papers       = Object.keys(p.paperMatrix);
    const firstGrams   = p.paperMatrix[papers[0]]?.grammages || [];
    const paperOpts    = papers.map((paper, i) =>
      `<option value="${escapeAttr(paper)}"${i === 0 ? ' selected' : ''}>${escapeHtml(paper)}</option>`
    ).join('');
    const grammageOpts = firstGrams.map((g, i) =>
      `<option value="${escapeAttr(g.label)}"${i === 0 ? ' selected' : ''}>${escapeHtml(g.label)}</option>`
    ).join('');
    paperHtml = `
      <div class="prod-opt-group">
        <label class="prod-opt-lbl" for="paper-${p.id}">Papiersorte</label>
        <select class="paper-sel" id="paper-${p.id}" onchange="paperChange('${p.id}')" aria-label="Papiersorte wählen">
          ${paperOpts}
        </select>
      </div>
      <div class="prod-opt-group">
        <label class="prod-opt-lbl" for="grammage-${p.id}">Grammatur</label>
        <select class="paper-sel" id="grammage-${p.id}" onchange="updateLivePrice('${p.id}')" aria-label="Grammatur wählen">
          ${grammageOpts}
        </select>
      </div>`;
  }

  // Tier table rows
  const tierRows = p.tiers.map(t => {
    const up = (t.ws / t.qty) * RESELLER_MARKUP;
    return `<tr>
      <td>${t.qty} Stk.</td>
      <td>${formatEur(up)}/Stk.</td>
      <td>${formatEur(up * t.qty)}</td>
    </tr>`;
  }).join('');

  // Min qty for the quantity input
  const minQty = firstTier.qty;

  return `
  <div class="prod-card" id="card-${p.id}">
    <div class="prod-card-header">
      <span class="prod-emoji">${p.emoji}</span>
      <div class="prod-cat">${escapeHtml(p.category)}</div>
    </div>
    <div class="prod-card-body">
      <h3 class="prod-name">${escapeHtml(p.name)}</h3>
      <p class="prod-desc">${escapeHtml(p.desc)}</p>
      <div class="prod-price-from">ab <strong>${formatEur(basePrice)}</strong>/Stk.</div>

      ${optGroupsHtml}
      ${paperHtml}

      <div class="prod-qty-row">
        <label class="prod-opt-lbl">Menge</label>
        <div class="qty-ctrl">
          <button class="qty-btn" onclick="qtyStep('${p.id}',-1)" aria-label="Weniger">−</button>
          <input
            class="qty-inp"
            id="qty-${p.id}"
            type="number"
            value="${minQty}"
            min="${minQty}"
            step="1"
            onchange="qtyUpdate('${p.id}')"
            aria-label="Menge"
          >
          <button class="qty-btn" onclick="qtyStep('${p.id}',1)" aria-label="Mehr">+</button>
        </div>
      </div>

      <div class="prod-price-live" id="price-${p.id}">
        <div class="price-unit">— €/Stk.</div>
        <div class="price-total">— €</div>
      </div>

      <details class="tier-table-wrap">
        <summary>Staffelpreise anzeigen</summary>
        <table class="tier-table">
          <thead>
            <tr><th>Menge</th><th>Pro Stück</th><th>Gesamt</th></tr>
          </thead>
          <tbody>${tierRows}</tbody>
        </table>
      </details>

      <button class="add-to-cart-btn" onclick="addToCart('${p.id}')">
        In den Warenkorb →
      </button>
    </div>
  </div>`;
}

// ───────────────────────────────────────────────────────────────────────────────
// OPTION & QUANTITY HELPERS
// ───────────────────────────────────────────────────────────────────────────────

/**
 * Handle option button click: deactivate siblings, activate clicked button,
 * then refresh live price display.
 */
function optSelect(btn, productId, key) {
  const group = btn.closest('[data-key]');
  if (!group) return;
  group.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  updateLivePrice(productId);
}

/**
 * Read currently selected options from a product card's DOM.
 * Returns object like { finish: 'Glanz', sides: 'Einseitig' }
 */
function getSelectedOpts(productId) {
  const card = document.getElementById(`card-${productId}`);
  if (!card) return {};
  const opts = {};
  card.querySelectorAll('[data-key]').forEach(grp => {
    const active = grp.querySelector('.opt-btn.active');
    if (active) opts[grp.dataset.key] = active.dataset.val;
  });
  // Paper matrix selects
  const paperSel   = document.getElementById(`paper-${productId}`);
  const grammSel   = document.getElementById(`grammage-${productId}`);
  if (paperSel) opts.papier    = paperSel.value;
  if (grammSel) opts.grammatur = grammSel.value;
  return opts;
}

/**
 * Called when the paper <select> changes — repopulates grammage options
 * then refreshes the live price.
 */
function paperChange(productId) {
  const product = CATALOG.find(p => p.id === productId);
  if (!product?.paperMatrix) return;
  const paperSel = document.getElementById(`paper-${productId}`);
  const grammSel = document.getElementById(`grammage-${productId}`);
  if (!paperSel || !grammSel) return;
  const grammages = product.paperMatrix[paperSel.value]?.grammages || [];
  grammSel.innerHTML = grammages.map(g =>
    `<option value="${escapeAttr(g.label)}">${escapeHtml(g.label)}</option>`
  ).join('');
  updateLivePrice(productId);
}

/**
 * Set active speed surcharge and refresh all visible live prices.
 */
function setSpeed(speed, el) {
  activeSurcharge = SPEED_SURCHARGES[speed]?.surcharge ?? 0;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
  CATALOG.forEach(p => { if (document.getElementById(`price-${p.id}`)) updateLivePrice(p.id); });
}

/**
 * Step qty up or down. Uses product minimum tier qty as step for products
 * with high minimums (e.g. 250 flyers). For qty=1 products (roll-ups), steps by 1.
 */
function qtyStep(productId, delta) {
  const inp = document.getElementById(`qty-${productId}`);
  if (!inp) return;

  const product = CATALOG.find(p => p.id === productId);
  const minQty  = product ? product.tiers[0].qty : 1;
  const step    = minQty === 1 ? 1 : minQty;
  const current = parseInt(inp.value, 10) || minQty;
  const newVal  = Math.max(minQty, current + delta * step);

  inp.value = newVal;
  updateLivePrice(productId);
}

/**
 * Called on manual qty input change — just refresh the price display.
 */
function qtyUpdate(productId) {
  updateLivePrice(productId);
}

/**
 * Recalculate and display the live unit + total price for a product card.
 */
function updateLivePrice(productId) {
  const product = CATALOG.find(p => p.id === productId);
  if (!product) return;

  const qtyInput = document.getElementById(`qty-${productId}`);
  const minQty   = product.tiers[0].qty;
  const qty      = Math.max(minQty, parseInt(qtyInput?.value, 10) || minQty);

  // Clamp displayed value to minimum
  if (qtyInput && parseInt(qtyInput.value, 10) < minQty) {
    qtyInput.value = minQty;
  }

  const opts = getSelectedOpts(productId);
  const calc = calcPrice(product, qty, opts);
  const box  = document.getElementById(`price-${productId}`);
  if (!box) return;

  const unitEl  = box.querySelector('.price-unit');
  const totEl   = box.querySelector('.price-total');
  if (unitEl) unitEl.textContent = calc.displayUnit + '/Stk.';
  if (totEl)  totEl.textContent  = calc.displayTotal + ' gesamt';
}

/**
 * Add the currently configured product to the cart.
 */
function addToCart(productId) {
  const product = CATALOG.find(p => p.id === productId);
  if (!product) return;

  const qtyInput = document.getElementById(`qty-${productId}`);
  const minQty   = product.tiers[0].qty;
  const qty      = Math.max(minQty, parseInt(qtyInput?.value, 10) || minQty);
  const opts     = getSelectedOpts(productId);
  const calc     = calcPrice(product, qty, opts);

  cartAdd({
    id:          product.id,
    name:        product.name,
    emoji:       product.emoji,
    opts:        opts,
    qty:         qty,
    clientUnit:  calc.clientUnit,
    clientTotal: calc.clientTotal,
  });
}

// ───────────────────────────────────────────────────────────────────────────────
// FILTER TABS
// ───────────────────────────────────────────────────────────────────────────────

/**
 * Filter catalog to a specific category.
 * @param {string} category - Category slug or 'all'
 * @param {HTMLElement} el  - The clicked tab element
 */
function filterCatalog(category, el) {
  // Update active state on tabs
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');

  // Re-render catalog
  renderCatalog(category === 'all' ? null : category);

  // After render, initialize live prices for all visible cards
  setTimeout(() => {
    CATALOG
      .filter(p => category === 'all' || p.category === category)
      .forEach(p => updateLivePrice(p.id));
  }, 50);
}

// ───────────────────────────────────────────────────────────────────────────────
// UTILITY — XSS PREVENTION
// ───────────────────────────────────────────────────────────────────────────────

/** Escape HTML special chars for safe innerHTML insertion. */
function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** Escape a value for use inside an HTML attribute. */
function escapeAttr(str) {
  return escapeHtml(String(str));
}

// ───────────────────────────────────────────────────────────────────────────────
// INIT — BOOTSTRAP ON DOM READY
// ───────────────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Render all products
  renderCatalog(null);

  // Initialize cart UI from localStorage
  cartRender();

  // Initialize live price on every product card after render
  setTimeout(() => {
    CATALOG.forEach(p => updateLivePrice(p.id));
  }, 100);

  // Close drawer when clicking the overlay background
  const overlay = document.getElementById('cartOverlay');
  if (overlay) {
    overlay.addEventListener('click', () => {
      const drawer = document.getElementById('cartDrawer');
      if (drawer) drawer.classList.remove('open');
    });
  }

  // Hamburger menu (shared across all pages)
  const hamburger = document.getElementById('hamburger');
  const mobNav    = document.getElementById('mobNav');
  if (hamburger && mobNav) {
    hamburger.addEventListener('click', () => {
      mobNav.classList.toggle('open');
    });
  }
});
