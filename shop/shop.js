'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// MASAR PRINT SHOP — shop.js  (Visitenkarten · Flyer · Planen)
// ═══════════════════════════════════════════════════════════════════════════════

const RESELLER_MARKUP = 1.30;

const SPEED_SURCHARGES = {
  standard:  { surcharge: 0.00 },
  'next-day':{ surcharge: 0.25 },
  'same-day':{ surcharge: 0.50 },
};
let activeSurcharge = 0.0;

// ─────────────────────────────────────────────────────────────────────────────
// PRODUCT CATALOG
// type:'standard'  → tier-based pricing per piece
// type:'banner'    → m²-based pricing, special rendering
// ─────────────────────────────────────────────────────────────────────────────
const CATALOG = [

  // ── VISITENKARTEN ─────────────────────────────────────────────────────────
  {
    id: 'visitenkarten', name: 'Visitenkarten', type: 'standard',
    category: 'Visitenkarten',
    desc: '85 × 55 mm · 4/4-farbig · beidseitig',
    steps: [
      {
        num: 1, key: 'papier', label: 'Papiersorte',
        opts: [
          { label: 'Bilderdruck matt',          sub: 'Klassisch & edel',       mult: 1.00 },
          { label: 'Bilderdruck glänzend',       sub: 'Lebendige Farben',       mult: 1.05 },
          { label: 'Naturpapier',                sub: 'Natürliche Optik',       mult: 1.12 },
          { label: 'Multiloft Rough',            sub: '3–4 Lagen · Farbkern',  mult: 1.45, badge: 'PREMIUM' },
          { label: 'Multiloft Smooth',           sub: '3–4 Lagen · Farbkern',  mult: 1.52, badge: 'PREMIUM' },
        ]
      },
      {
        num: 2, key: 'grammatur', label: 'Grammatur',
        dependsOn: 'papier',
        optsMap: {
          'Bilderdruck matt':    [{ label:'300 g/m²', mult:1.00 },{ label:'350 g/m²', mult:1.08 }],
          'Bilderdruck glänzend':[{ label:'300 g/m²', mult:1.00 }],
          'Naturpapier':         [{ label:'300 g/m²', mult:1.00 }],
          'Multiloft Rough':     [{ label:'750 g (3-fach, Farbkern)', mult:1.00 },{ label:'1020 g (4-fach, Farbkern)', mult:1.28 }],
          'Multiloft Smooth':    [{ label:'810 g (3-fach, Farbkern)', mult:1.00 },{ label:'1080 g (4-fach, Farbkern)', mult:1.28 }],
        }
      },
      {
        num: 3, key: 'veredelung', label: 'Veredelung',
        opts: [
          { label: 'Ohne Veredelung',   sub: 'Standard',           mult: 1.00 },
          { label: 'Glanzlaminierung',  sub: 'Hochglanz',          mult: 1.15 },
          { label: 'Mattlaminierung',   sub: 'Seidenmatt',         mult: 1.15 },
          { label: 'Soft-Touch',        sub: 'Samtartige Haptik',  mult: 1.22 },
        ]
      },
    ],
    tiers: [
      { qty: 100,  ws: 12.00 },
      { qty: 250,  ws: 16.00 },
      { qty: 500,  ws: 22.00 },
      { qty: 1000, ws: 30.00 },
      { qty: 2500, ws: 55.00 },
    ]
  },

  // ── FLYER A5 ──────────────────────────────────────────────────────────────
  {
    id: 'flyer-a5', name: 'Flyer A5', type: 'standard',
    category: 'Flyer',
    desc: '148 × 210 mm · 4/4-farbig',
    steps: [
      {
        num: 1, key: 'seiten', label: 'Seitenanzahl',
        opts: [
          { label: 'Einseitig',    sub: 'Nur Vorderseite',           mult: 1.00 },
          { label: 'Doppelseitig', sub: 'Vorder- & Rückseite',       mult: 1.35 },
        ]
      },
      {
        num: 2, key: 'papier', label: 'Papiersorte',
        opts: [
          { label: 'Bilderdruck matt',     sub: 'Klassisch',          mult: 1.00 },
          { label: 'Bilderdruck glänzend', sub: 'Kräftige Farben',    mult: 1.05 },
          { label: 'Naturpapier',          sub: 'Natürliche Optik',   mult: 1.12 },
          { label: 'Recycling',            sub: 'Nachhaltig',         mult: 0.95 },
        ]
      },
      {
        num: 3, key: 'grammatur', label: 'Grammatur',
        dependsOn: 'papier',
        optsMap: {
          'Bilderdruck matt':     [{ label:'100 g/m²',mult:0.85 },{ label:'135 g/m²',mult:1.00 },{ label:'170 g/m²',mult:1.12 },{ label:'250 g/m²',mult:1.28 },{ label:'300 g/m²',mult:1.38 },{ label:'350 g/m²',mult:1.48 }],
          'Bilderdruck glänzend': [{ label:'100 g/m²',mult:0.85 },{ label:'135 g/m²',mult:1.00 },{ label:'170 g/m²',mult:1.12 },{ label:'250 g/m²',mult:1.28 },{ label:'300 g/m²',mult:1.38 }],
          'Naturpapier':          [{ label:'300 g/m²',mult:1.38 }],
          'Recycling':            [{ label:'135 g/m²',mult:1.00 },{ label:'300 g/m²',mult:1.38 }],
        }
      },
      {
        num: 4, key: 'veredelung', label: 'Veredelung',
        opts: [
          { label: 'Ohne Veredelung',  sub: 'Standard',         mult: 1.00 },
          { label: 'Glanzlaminierung', sub: 'Hochglanz',        mult: 1.15 },
          { label: 'Mattlaminierung',  sub: 'Seidenmatt',       mult: 1.15 },
          { label: 'Soft-Touch',       sub: 'Samtartig',        mult: 1.22 },
        ]
      },
    ],
    tiers: [
      { qty: 250,   ws: 18.50 },
      { qty: 500,   ws: 24.00 },
      { qty: 1000,  ws: 32.00 },
      { qty: 2500,  ws: 54.00 },
      { qty: 5000,  ws: 82.00 },
      { qty: 10000, ws: 140.00 },
    ]
  },

  // ── FLYER A4 ──────────────────────────────────────────────────────────────
  {
    id: 'flyer-a4', name: 'Flyer A4', type: 'standard',
    category: 'Flyer',
    desc: '210 × 297 mm · 4/4-farbig',
    steps: [
      {
        num: 1, key: 'seiten', label: 'Seitenanzahl',
        opts: [
          { label: 'Einseitig',    sub: 'Nur Vorderseite',           mult: 1.00 },
          { label: 'Doppelseitig', sub: 'Vorder- & Rückseite',       mult: 1.35 },
        ]
      },
      {
        num: 2, key: 'papier', label: 'Papiersorte',
        opts: [
          { label: 'Bilderdruck matt',     sub: 'Klassisch',          mult: 1.00 },
          { label: 'Bilderdruck glänzend', sub: 'Kräftige Farben',    mult: 1.05 },
          { label: 'Naturpapier',          sub: 'Natürliche Optik',   mult: 1.12 },
          { label: 'Recycling',            sub: 'Nachhaltig',         mult: 0.95 },
        ]
      },
      {
        num: 3, key: 'grammatur', label: 'Grammatur',
        dependsOn: 'papier',
        optsMap: {
          'Bilderdruck matt':     [{ label:'100 g/m²',mult:0.85 },{ label:'135 g/m²',mult:1.00 },{ label:'170 g/m²',mult:1.12 },{ label:'250 g/m²',mult:1.28 },{ label:'300 g/m²',mult:1.38 },{ label:'350 g/m²',mult:1.48 }],
          'Bilderdruck glänzend': [{ label:'100 g/m²',mult:0.85 },{ label:'135 g/m²',mult:1.00 },{ label:'170 g/m²',mult:1.12 },{ label:'250 g/m²',mult:1.28 },{ label:'300 g/m²',mult:1.38 }],
          'Naturpapier':          [{ label:'300 g/m²',mult:1.38 }],
          'Recycling':            [{ label:'135 g/m²',mult:1.00 },{ label:'300 g/m²',mult:1.38 }],
        }
      },
      {
        num: 4, key: 'veredelung', label: 'Veredelung',
        opts: [
          { label: 'Ohne Veredelung',  sub: 'Standard',         mult: 1.00 },
          { label: 'Glanzlaminierung', sub: 'Hochglanz',        mult: 1.15 },
          { label: 'Mattlaminierung',  sub: 'Seidenmatt',       mult: 1.15 },
          { label: 'Soft-Touch',       sub: 'Samtartig',        mult: 1.22 },
        ]
      },
    ],
    tiers: [
      { qty: 250,  ws: 22.00 },
      { qty: 500,  ws: 30.00 },
      { qty: 1000, ws: 42.00 },
      { qty: 2500, ws: 70.00 },
      { qty: 5000, ws: 108.00 },
    ]
  },

  // ── PLANEN / BANNER ───────────────────────────────────────────────────────
  {
    id: 'planen', name: 'PVC-Planen & Banner', type: 'banner',
    category: 'Planen',
    desc: 'Wetterfest · Innen & Außen · Individuell auf Maß bedruckt',
    materials: [
      { label: 'PVC 510 g/m²',      sub: 'Klassisch, wetterfest, robust', wsPerSqm: 5.50, mult: 1.00 },
      { label: 'PVC 340 g/m²',      sub: 'Leichter, günstige Option',     wsPerSqm: 4.20, mult: 1.00 },
      { label: 'Mesh 280 g/m²',     sub: 'Winddurchlässig, für Gerüste',  wsPerSqm: 5.00, mult: 1.00 },
      { label: 'Textilstoff 210 g/m²', sub: 'Indoor, edles Erscheinungsbild', wsPerSqm: 8.50, mult: 1.00 },
    ],
    sizes: [
      { label: '50 × 100 cm',  w: 0.5, h: 1.0 },
      { label: '100 × 100 cm', w: 1.0, h: 1.0 },
      { label: '100 × 200 cm', w: 1.0, h: 2.0 },
      { label: '100 × 300 cm', w: 1.0, h: 3.0 },
      { label: '100 × 500 cm', w: 1.0, h: 5.0 },
      { label: '150 × 300 cm', w: 1.5, h: 3.0 },
      { label: '200 × 100 cm', w: 2.0, h: 1.0 },
      { label: '200 × 200 cm', w: 2.0, h: 2.0 },
      { label: '200 × 300 cm', w: 2.0, h: 3.0 },
      { label: '200 × 400 cm', w: 2.0, h: 4.0 },
      { label: '200 × 500 cm', w: 2.0, h: 5.0 },
      { label: '300 × 200 cm', w: 3.0, h: 2.0 },
      { label: '300 × 300 cm', w: 3.0, h: 3.0 },
      { label: '400 × 200 cm', w: 4.0, h: 2.0 },
      { label: '500 × 200 cm', w: 5.0, h: 2.0 },
      { label: 'Individuell',  custom: true },
    ],
    oesen: [
      { label: 'Keine Ösen',      mult: 1.00 },
      { label: 'Ösen alle 50 cm', mult: 1.05 },
      { label: 'Ösen alle 25 cm', mult: 1.08 },
    ],
    saum: [
      { label: 'Ohne Saum',   mult: 1.00 },
      { label: 'Saum rundum', mult: 1.06 },
    ],
    minPrice: 8.00, // minimum wholesale price per banner
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// CART STATE
// ─────────────────────────────────────────────────────────────────────────────
let cart = [];
try {
  const stored = localStorage.getItem('masarCart');
  if (stored) cart = JSON.parse(stored);
  if (!Array.isArray(cart)) cart = [];
} catch (e) { cart = []; }

// ─────────────────────────────────────────────────────────────────────────────
// PRICE CALCULATION — standard (tier-based)
// ─────────────────────────────────────────────────────────────────────────────
function calcPrice(product, qty, selectedOpts) {
  const sorted = [...product.tiers].sort((a, b) => a.qty - b.qty);
  let tier = sorted[0];
  for (const t of sorted) { if (qty >= t.qty) tier = t; }

  const wsUnit = tier.ws / tier.qty;
  let optMult  = 1.0;

  if (selectedOpts) {
    for (const step of (product.steps || [])) {
      if (step.dependsOn) continue; // grammatur handled below
      const chosen = step.opts?.find(o => o.label === selectedOpts[step.key]);
      if (chosen) optMult *= chosen.mult;
    }
    // Grammatur step
    const gramStep = product.steps?.find(s => s.dependsOn);
    if (gramStep) {
      const paperVal = selectedOpts[gramStep.dependsOn];
      const gramOpts = gramStep.optsMap?.[paperVal] || [];
      const chosen   = gramOpts.find(o => o.label === selectedOpts[gramStep.key]);
      if (chosen) optMult *= chosen.mult;
    }
  }

  const clientUnit  = wsUnit * optMult * RESELLER_MARKUP;
  const clientTotal = clientUnit * qty * (1 + activeSurcharge);
  return { clientUnit, clientTotal, displayUnit: formatEur(clientUnit), displayTotal: formatEur(clientTotal) };
}

// ─────────────────────────────────────────────────────────────────────────────
// PRICE CALCULATION — banner (m²-based)
// ─────────────────────────────────────────────────────────────────────────────
function calcBannerPrice(product, widthM, heightM, qty, materialLabel, oesenLabel, saumLabel) {
  const area     = Math.max(0.1, widthM * heightM);
  const mat      = product.materials.find(m => m.label === materialLabel) || product.materials[0];
  const oesen    = product.oesen.find(o => o.label === oesenLabel) || product.oesen[0];
  const saum     = product.saum.find(s => s.label === saumLabel)   || product.saum[0];

  const wsPerBanner   = Math.max(product.minPrice, mat.wsPerSqm * area);
  const finishMult    = oesen.mult * saum.mult;
  const clientUnit    = wsPerBanner * finishMult * RESELLER_MARKUP;
  const clientTotal   = clientUnit * qty * (1 + activeSurcharge);
  const sqmPrice      = clientUnit / area;

  return {
    area, clientUnit, clientTotal, sqmPrice,
    displayUnit:  formatEur(clientUnit),
    displayTotal: formatEur(clientTotal),
    displaySqm:   formatEur(sqmPrice),
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────────────────────
function formatEur(n) {
  return n.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
}
function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
function escapeAttr(str) { return escapeHtml(String(str)); }

// ─────────────────────────────────────────────────────────────────────────────
// CART OPERATIONS
// ─────────────────────────────────────────────────────────────────────────────
function cartSave() {
  try { localStorage.setItem('masarCart', JSON.stringify(cart)); } catch(e) {}
}
function cartCount() { return cart.reduce((s,i) => s + i.qty, 0); }
function cartTotal() { return cart.reduce((s,i) => s + i.clientTotal, 0); }

function cartAdd(item) {
  const key = JSON.stringify(item.opts);
  const ex  = cart.find(c => c.id === item.id && JSON.stringify(c.opts) === key);
  if (ex) { ex.qty += item.qty; ex.clientTotal = ex.clientUnit * ex.qty; }
  else     cart.push(item);
  cartSave(); cartRender(); cartFlash();
  const drawer = document.getElementById('cartDrawer');
  if (drawer) drawer.classList.add('open');
}
function cartRemove(idx) { cart.splice(idx, 1); cartSave(); cartRender(); }

function cartRender() {
  const badge = document.getElementById('cartBadge');
  if (badge) badge.textContent = cartCount();
  const panel  = document.getElementById('cartItems');
  const empty  = document.getElementById('cartEmpty');
  const totEl  = document.getElementById('cartTotal');
  const chkBtn = document.getElementById('cartCheckout');
  if (!panel) return;
  if (cart.length === 0) {
    panel.innerHTML = '';
    if (empty)  empty.style.display  = 'block';
    if (totEl)  totEl.textContent    = '0,00 €';
    if (chkBtn) chkBtn.disabled      = true;
    return;
  }
  if (empty)  empty.style.display = 'none';
  if (chkBtn) chkBtn.disabled     = false;
  panel.innerHTML = cart.map((item, i) => `
    <div class="cart-item">
      <div class="cart-item-info">
        <span class="cart-item-name">${escapeHtml(item.name)}</span>
        <span class="cart-item-opts">${escapeHtml(Object.values(item.opts||{}).join(' · '))} · ${item.qty} Stk.</span>
      </div>
      <div class="cart-item-right">
        <span class="cart-item-price">${formatEur(item.clientTotal)}</span>
        <button class="cart-item-del" onclick="cartRemove(${i})" aria-label="Entfernen">×</button>
      </div>
    </div>`).join('');
  if (totEl) totEl.textContent = formatEur(cartTotal());
}
function cartFlash() {
  const btn = document.getElementById('cartBtn');
  if (!btn) return;
  btn.classList.add('cart-flash');
  setTimeout(() => btn.classList.remove('cart-flash'), 600);
}
function cartToggle() {
  document.getElementById('cartDrawer')?.classList.toggle('open');
}
function cartGoCheckout() {
  if (!cart.length) return;
  try { sessionStorage.setItem('masarCheckoutCart', JSON.stringify(cart)); } catch(e) {}
  window.location.href = '/shop/checkout.html';
}

// ─────────────────────────────────────────────────────────────────────────────
// CONFIGURATOR RENDERING — standard products
// ─────────────────────────────────────────────────────────────────────────────
function renderStandardCard(p) {
  const minTier   = [...p.tiers].sort((a,b) => a.qty - b.qty)[0];
  const baseUnit  = (minTier.ws / minTier.qty) * RESELLER_MARKUP;

  const stepsHtml = p.steps.map(step => {
    const isDependent = !!step.dependsOn;
    const initOpts    = isDependent
      ? (step.optsMap[p.steps.find(s => s.key === step.dependsOn)?.opts[0]?.label] || [])
      : (step.opts || []);

    const chipsHtml = initOpts.map((o, i) => `
      <button class="cfg-chip${i===0?' active':''}"
              data-key="${step.key}" data-val="${escapeAttr(o.label)}"
              onclick="chipSelect(this,'${p.id}')"
              type="button">
        <span class="cfg-chip-label">${escapeHtml(o.label)}</span>
        ${o.sub ? `<span class="cfg-chip-sub">${escapeHtml(o.sub)}</span>` : ''}
        ${o.badge ? `<span class="cfg-chip-badge">${escapeHtml(o.badge)}</span>` : ''}
      </button>`).join('');

    return `
      <div class="cfg-step" data-step-key="${step.key}">
        <div class="cfg-step-head">
          <span class="cfg-step-num">${step.num}</span>
          <span class="cfg-step-label">${escapeHtml(step.label)}</span>
        </div>
        <div class="cfg-chips" id="chips-${p.id}-${step.key}">${chipsHtml}</div>
      </div>`;
  }).join('');

  const tierRows = p.tiers.map(t => {
    const u = (t.ws / t.qty) * RESELLER_MARKUP;
    return `<tr><td>${t.qty} Stk.</td><td>${formatEur(u)}/Stk.</td><td>${formatEur(u * t.qty)}</td></tr>`;
  }).join('');

  return `
  <div class="cfg-card" id="card-${p.id}">
    <div class="cfg-header">
      <div class="cfg-header-info">
        <h2 class="cfg-name">${escapeHtml(p.name)}</h2>
        <p class="cfg-desc">${escapeHtml(p.desc)}</p>
      </div>
      <div class="cfg-header-from">
        ab <strong id="from-${p.id}">${formatEur(baseUnit)}</strong><span>/Stk.</span>
      </div>
    </div>
    <div class="cfg-body">
      <div class="cfg-steps-col">
        ${stepsHtml}
        <div class="cfg-step">
          <div class="cfg-step-head">
            <span class="cfg-step-num">${p.steps.length + 1}</span>
            <span class="cfg-step-label">Menge</span>
          </div>
          <div class="cfg-qty-row">
            <button class="cfg-qty-btn" onclick="cfgQtyStep('${p.id}',-1)" type="button">−</button>
            <input class="cfg-qty-inp" id="qty-${p.id}" type="number"
                   value="${minTier.qty}" min="${minTier.qty}" step="1"
                   oninput="cfgPriceUpdate('${p.id}')" aria-label="Menge">
            <button class="cfg-qty-btn" onclick="cfgQtyStep('${p.id}',1)" type="button">+</button>
            <span class="cfg-qty-hint">mind. ${minTier.qty} Stk.</span>
          </div>
        </div>
      </div>
      <div class="cfg-price-col">
        <div class="cfg-price-box" id="price-${p.id}">
          <div class="cfg-price-unit-row">
            <span class="cfg-price-unit-lbl">Stückpreis</span>
            <span class="cfg-price-unit-val" id="punit-${p.id}">${formatEur(baseUnit)}</span>
          </div>
          <div class="cfg-price-total-row">
            <span class="cfg-price-total-lbl">Gesamtpreis</span>
            <span class="cfg-price-total-val" id="ptotal-${p.id}">${formatEur(baseUnit * minTier.qty)}</span>
          </div>
        </div>
        <details class="cfg-tiers">
          <summary>Staffelpreise</summary>
          <table class="cfg-tier-table">
            <thead><tr><th>Menge</th><th>pro Stück</th><th>Gesamt</th></tr></thead>
            <tbody>${tierRows}</tbody>
          </table>
        </details>
        <button class="cfg-cart-btn" onclick="addToCart('${p.id}')" type="button">
          In den Warenkorb →
        </button>
      </div>
    </div>
  </div>`;
}

// ─────────────────────────────────────────────────────────────────────────────
// CONFIGURATOR RENDERING — banner product
// ─────────────────────────────────────────────────────────────────────────────
function renderBannerCard(p) {
  const defMat  = p.materials[0];
  const defSize = p.sizes[0];
  const initPrice = calcBannerPrice(p, defSize.w, defSize.h, 1, defMat.label, p.oesen[0].label, p.saum[0].label);

  const matsHtml = p.materials.map((m, i) => `
    <button class="cfg-chip cfg-mat-chip${i===0?' active':''}"
            data-key="material" data-val="${escapeAttr(m.label)}"
            onclick="bannerChip(this,'${p.id}')" type="button">
      <span class="cfg-chip-label">${escapeHtml(m.label)}</span>
      <span class="cfg-chip-sub">${escapeHtml(m.sub)}</span>
    </button>`).join('');

  const sizesHtml = p.sizes.map((s, i) => {
    const isCustom = !!s.custom;
    return `
    <button class="cfg-size-chip${i===0?' active':''}${isCustom?' cfg-size-custom':''}"
            data-custom="${isCustom}"
            data-w="${s.w || 0}" data-h="${s.h || 0}"
            onclick="bannerSize(this,'${p.id}')" type="button">
      ${escapeHtml(s.label)}
    </button>`;
  }).join('');

  const oesenHtml = p.oesen.map((o, i) => `
    <button class="cfg-chip${i===0?' active':''}"
            data-key="oesen" data-val="${escapeAttr(o.label)}"
            onclick="bannerChip(this,'${p.id}')" type="button">
      <span class="cfg-chip-label">${escapeHtml(o.label)}</span>
    </button>`).join('');

  const saumHtml = p.saum.map((s, i) => `
    <button class="cfg-chip${i===0?' active':''}"
            data-key="saum" data-val="${escapeAttr(s.label)}"
            onclick="bannerChip(this,'${p.id}')" type="button">
      <span class="cfg-chip-label">${escapeHtml(s.label)}</span>
    </button>`).join('');

  return `
  <div class="cfg-card" id="card-${p.id}">
    <div class="cfg-header">
      <div class="cfg-header-info">
        <h2 class="cfg-name">${escapeHtml(p.name)}</h2>
        <p class="cfg-desc">${escapeHtml(p.desc)}</p>
      </div>
      <div class="cfg-header-from">
        ab <strong id="from-${p.id}">${initPrice.displaySqm}</strong><span>/m²</span>
      </div>
    </div>
    <div class="cfg-body">
      <div class="cfg-steps-col">

        <div class="cfg-step">
          <div class="cfg-step-head">
            <span class="cfg-step-num">1</span>
            <span class="cfg-step-label">Material</span>
          </div>
          <div class="cfg-chips cfg-mat-chips" id="chips-${p.id}-material">${matsHtml}</div>
        </div>

        <div class="cfg-step">
          <div class="cfg-step-head">
            <span class="cfg-step-num">2</span>
            <span class="cfg-step-label">Format / Größe</span>
          </div>
          <div class="cfg-size-grid" id="chips-${p.id}-size">${sizesHtml}</div>
          <div class="cfg-custom-size" id="customSize-${p.id}" style="display:none;">
            <label>Breite (cm)</label>
            <input class="cfg-custom-inp" id="cw-${p.id}" type="number" min="10" max="1000"
                   value="100" placeholder="z. B. 150" oninput="bannerPriceUpdate('${p.id}')">
            <span class="cfg-custom-x">×</span>
            <label>Höhe (cm)</label>
            <input class="cfg-custom-inp" id="ch-${p.id}" type="number" min="10" max="1000"
                   value="200" placeholder="z. B. 200" oninput="bannerPriceUpdate('${p.id}')">
            <span class="cfg-custom-unit">cm</span>
          </div>
        </div>

        <div class="cfg-step">
          <div class="cfg-step-head">
            <span class="cfg-step-num">3</span>
            <span class="cfg-step-label">Ösen</span>
          </div>
          <div class="cfg-chips" id="chips-${p.id}-oesen">${oesenHtml}</div>
        </div>

        <div class="cfg-step">
          <div class="cfg-step-head">
            <span class="cfg-step-num">4</span>
            <span class="cfg-step-label">Saum</span>
          </div>
          <div class="cfg-chips" id="chips-${p.id}-saum">${saumHtml}</div>
        </div>

        <div class="cfg-step">
          <div class="cfg-step-head">
            <span class="cfg-step-num">5</span>
            <span class="cfg-step-label">Menge</span>
          </div>
          <div class="cfg-qty-row">
            <button class="cfg-qty-btn" onclick="cfgQtyStep('${p.id}',-1)" type="button">−</button>
            <input class="cfg-qty-inp" id="qty-${p.id}" type="number"
                   value="1" min="1" step="1"
                   oninput="bannerPriceUpdate('${p.id}')" aria-label="Menge">
            <button class="cfg-qty-btn" onclick="cfgQtyStep('${p.id}',1)" type="button">+</button>
          </div>
        </div>

      </div>
      <div class="cfg-price-col">
        <div class="cfg-price-box" id="price-${p.id}">
          <div class="cfg-banner-area-row">
            <span class="cfg-price-unit-lbl">Fläche</span>
            <span class="cfg-price-unit-val" id="parea-${p.id}">${initPrice.area.toFixed(2)} m²</span>
          </div>
          <div class="cfg-price-unit-row">
            <span class="cfg-price-unit-lbl">Preis pro Stück</span>
            <span class="cfg-price-unit-val" id="punit-${p.id}">${initPrice.displayUnit}</span>
          </div>
          <div class="cfg-price-total-row">
            <span class="cfg-price-total-lbl">Gesamtpreis</span>
            <span class="cfg-price-total-val" id="ptotal-${p.id}">${initPrice.displayTotal}</span>
          </div>
        </div>
        <div class="cfg-banner-info">
          <p>✓ Inkl. Druck, ohne Montage</p>
          <p>✓ Lieferung aufgerollt</p>
          <p>✓ Farbprofil: CMYK · 720 dpi</p>
        </div>
        <button class="cfg-cart-btn" onclick="addBannerToCart('${p.id}')" type="button">
          In den Warenkorb →
        </button>
      </div>
    </div>
  </div>`;
}

// ─────────────────────────────────────────────────────────────────────────────
// RENDER CATALOG
// ─────────────────────────────────────────────────────────────────────────────
function renderCatalog(filterCategory) {
  const grid = document.getElementById('catalogGrid');
  if (!grid) return;

  const items = filterCategory
    ? CATALOG.filter(p => p.category === filterCategory)
    : CATALOG;

  grid.innerHTML = items.map(p =>
    p.type === 'banner' ? renderBannerCard(p) : renderStandardCard(p)
  ).join('');

  setTimeout(() => {
    items.forEach(p => {
      if (p.type === 'standard') cfgPriceUpdate(p.id);
      else bannerPriceUpdate(p.id);
    });
  }, 50);
}

// ─────────────────────────────────────────────────────────────────────────────
// INTERACTION — standard configurator
// ─────────────────────────────────────────────────────────────────────────────
function chipSelect(btn, productId) {
  const key  = btn.dataset.key;
  const val  = btn.dataset.val;
  const wrap = document.getElementById(`chips-${productId}-${key}`);
  if (wrap) wrap.querySelectorAll('.cfg-chip').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  // If this chip controls a dependent step (grammatur), repopulate it
  const product = CATALOG.find(p => p.id === productId);
  if (!product) return;
  const depStep = product.steps?.find(s => s.dependsOn === key);
  if (depStep) {
    const newOpts = depStep.optsMap?.[val] || [];
    const depWrap = document.getElementById(`chips-${productId}-${depStep.key}`);
    if (depWrap) {
      depWrap.innerHTML = newOpts.map((o, i) => `
        <button class="cfg-chip${i===0?' active':''}"
                data-key="${depStep.key}" data-val="${escapeAttr(o.label)}"
                onclick="chipSelect(this,'${productId}')" type="button">
          <span class="cfg-chip-label">${escapeHtml(o.label)}</span>
          ${o.sub ? `<span class="cfg-chip-sub">${escapeHtml(o.sub)}</span>` : ''}
        </button>`).join('');
    }
  }

  cfgPriceUpdate(productId);
}

function cfgGetOpts(productId) {
  const card = document.getElementById(`card-${productId}`);
  const opts = {};
  if (!card) return opts;
  card.querySelectorAll('.cfg-chip.active').forEach(btn => {
    if (btn.dataset.key) opts[btn.dataset.key] = btn.dataset.val;
  });
  return opts;
}

function cfgPriceUpdate(productId) {
  const product = CATALOG.find(p => p.id === productId);
  if (!product || product.type === 'banner') return;

  const qtyInp = document.getElementById(`qty-${productId}`);
  const minQty = product.tiers[0].qty;
  const qty    = Math.max(minQty, parseInt(qtyInp?.value, 10) || minQty);
  if (qtyInp && parseInt(qtyInp.value,10) < minQty) qtyInp.value = minQty;

  const opts  = cfgGetOpts(productId);
  const calc  = calcPrice(product, qty, opts);

  const unitEl  = document.getElementById(`punit-${productId}`);
  const totEl   = document.getElementById(`ptotal-${productId}`);
  const fromEl  = document.getElementById(`from-${productId}`);
  if (unitEl)  unitEl.textContent  = calc.displayUnit + '/Stk.';
  if (totEl)   totEl.textContent   = calc.displayTotal;
  if (fromEl)  fromEl.textContent  = calc.displayUnit;
}

function cfgQtyStep(productId, delta) {
  const inp     = document.getElementById(`qty-${productId}`);
  if (!inp) return;
  const product = CATALOG.find(p => p.id === productId);
  const isStd   = product?.type !== 'banner';
  const minQty  = isStd ? (product?.tiers[0].qty || 1) : 1;
  const step    = isStd && minQty > 1 ? minQty : 1;
  const cur     = parseInt(inp.value, 10) || minQty;
  inp.value     = Math.max(minQty, cur + delta * step);
  if (isStd) cfgPriceUpdate(productId);
  else bannerPriceUpdate(productId);
}

function addToCart(productId) {
  const product = CATALOG.find(p => p.id === productId);
  if (!product) return;
  const qtyInp  = document.getElementById(`qty-${productId}`);
  const minQty  = product.tiers[0].qty;
  const qty     = Math.max(minQty, parseInt(qtyInp?.value,10) || minQty);
  const opts    = cfgGetOpts(productId);
  const calc    = calcPrice(product, qty, opts);
  cartAdd({ id:product.id, name:product.name, opts, qty, clientUnit:calc.clientUnit, clientTotal:calc.clientTotal });
}

// ─────────────────────────────────────────────────────────────────────────────
// INTERACTION — banner configurator
// ─────────────────────────────────────────────────────────────────────────────
function bannerChip(btn, productId) {
  const key  = btn.dataset.key;
  const wrap = document.getElementById(`chips-${productId}-${key}`);
  if (wrap) wrap.querySelectorAll('.cfg-chip').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  bannerPriceUpdate(productId);
}

function bannerSize(btn, productId) {
  const grid = document.getElementById(`chips-${productId}-size`);
  if (grid) grid.querySelectorAll('.cfg-size-chip').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const customBox = document.getElementById(`customSize-${productId}`);
  if (customBox) customBox.style.display = btn.dataset.custom === 'true' ? 'flex' : 'none';

  bannerPriceUpdate(productId);
}

function bannerGetDims(productId) {
  const activeSize = document.querySelector(`#chips-${productId}-size .cfg-size-chip.active`);
  if (!activeSize) return { w: 1, h: 1 };
  if (activeSize.dataset.custom === 'true') {
    const w = parseFloat(document.getElementById(`cw-${productId}`)?.value) || 100;
    const h = parseFloat(document.getElementById(`ch-${productId}`)?.value) || 200;
    return { w: w / 100, h: h / 100 };
  }
  return { w: parseFloat(activeSize.dataset.w) || 1, h: parseFloat(activeSize.dataset.h) || 1 };
}

function bannerPriceUpdate(productId) {
  const product = CATALOG.find(p => p.id === productId);
  if (!product || product.type !== 'banner') return;

  const { w, h }    = bannerGetDims(productId);
  const qty         = Math.max(1, parseInt(document.getElementById(`qty-${productId}`)?.value, 10) || 1);
  const materialBtn = document.querySelector(`#chips-${productId}-material .active`);
  const oesenBtn    = document.querySelector(`#chips-${productId}-oesen .active`);
  const saumBtn     = document.querySelector(`#chips-${productId}-saum .active`);
  const matLabel    = materialBtn?.dataset.val || product.materials[0].label;
  const oesenLabel  = oesenBtn?.dataset.val    || product.oesen[0].label;
  const saumLabel   = saumBtn?.dataset.val     || product.saum[0].label;

  const calc = calcBannerPrice(product, w, h, qty, matLabel, oesenLabel, saumLabel);

  const areaEl  = document.getElementById(`parea-${productId}`);
  const unitEl  = document.getElementById(`punit-${productId}`);
  const totEl   = document.getElementById(`ptotal-${productId}`);
  const fromEl  = document.getElementById(`from-${productId}`);
  if (areaEl) areaEl.textContent = calc.area.toFixed(2) + ' m²';
  if (unitEl) unitEl.textContent = calc.displayUnit;
  if (totEl)  totEl.textContent  = calc.displayTotal;
  if (fromEl) fromEl.textContent = calc.displaySqm;
}

function addBannerToCart(productId) {
  const product = CATALOG.find(p => p.id === productId);
  if (!product) return;
  const { w, h }    = bannerGetDims(productId);
  const qty         = Math.max(1, parseInt(document.getElementById(`qty-${productId}`)?.value,10) || 1);
  const materialBtn = document.querySelector(`#chips-${productId}-material .active`);
  const oesenBtn    = document.querySelector(`#chips-${productId}-oesen .active`);
  const saumBtn     = document.querySelector(`#chips-${productId}-saum .active`);
  const matLabel    = materialBtn?.dataset.val || product.materials[0].label;
  const oesenLabel  = oesenBtn?.dataset.val    || product.oesen[0].label;
  const saumLabel   = saumBtn?.dataset.val     || product.saum[0].label;
  const activeSz    = document.querySelector(`#chips-${productId}-size .cfg-size-chip.active`);
  const sizeLabel   = activeSz?.dataset.custom === 'true' ? `${Math.round(w*100)}×${Math.round(h*100)} cm` : (activeSz?.textContent?.trim() || '');
  const calc = calcBannerPrice(product, w, h, qty, matLabel, oesenLabel, saumLabel);
  cartAdd({
    id: product.id, name: product.name,
    opts: { Material: matLabel, Format: sizeLabel, Ösen: oesenLabel, Saum: saumLabel },
    qty, clientUnit: calc.clientUnit, clientTotal: calc.clientTotal
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// FILTER TABS & SPEED
// ─────────────────────────────────────────────────────────────────────────────
function filterCatalog(category, el) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
  renderCatalog(category === 'all' ? null : category);
}

function setSpeed(speed, el) {
  activeSurcharge = SPEED_SURCHARGES[speed]?.surcharge ?? 0;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
  CATALOG.forEach(p => {
    if (document.getElementById(`price-${p.id}`)) {
      if (p.type === 'banner') bannerPriceUpdate(p.id);
      else cfgPriceUpdate(p.id);
    }
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderCatalog(null);
  cartRender();

  document.getElementById('cartOverlay')?.addEventListener('click', () => {
    document.getElementById('cartDrawer')?.classList.remove('open');
  });

  const hamburger = document.getElementById('hamburger');
  const mobNav    = document.getElementById('mobNav');
  if (hamburger && mobNav) {
    hamburger.addEventListener('click', () => mobNav.classList.toggle('open'));
  }
});
