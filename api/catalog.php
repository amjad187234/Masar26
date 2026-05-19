<?php
// ═══ MASAR PRINT SHOP — SERVER-SIDE CATALOG ═══
// Mirrors shop.js CATALOG exactly — keep both files in sync when prices change.
declare(strict_types=1);

const RESELLER_MARKUP = 1.30;

$MASAR_CATALOG = [
  [
    'id' => 'flyer-a5', 'name' => 'Flyer A5',
    'options' => [
      'finish' => [['label' => 'Glanz', 'mult' => 1.0], ['label' => 'Matt', 'mult' => 1.06]],
      'sides'  => [['label' => 'Einseitig', 'mult' => 1.0], ['label' => 'Doppelseitig', 'mult' => 1.35]],
    ],
    'tiers' => [
      ['qty' => 250,   'ws' => 18.50],
      ['qty' => 500,   'ws' => 24.00],
      ['qty' => 1000,  'ws' => 32.00],
      ['qty' => 2500,  'ws' => 54.00],
      ['qty' => 5000,  'ws' => 82.00],
      ['qty' => 10000, 'ws' => 140.00],
    ],
  ],
  [
    'id' => 'flyer-a4', 'name' => 'Flyer A4',
    'options' => [
      'finish' => [['label' => 'Glanz', 'mult' => 1.0], ['label' => 'Matt', 'mult' => 1.06]],
      'sides'  => [['label' => 'Einseitig', 'mult' => 1.0], ['label' => 'Doppelseitig', 'mult' => 1.35]],
    ],
    'tiers' => [
      ['qty' => 250,  'ws' => 22.00],
      ['qty' => 500,  'ws' => 30.00],
      ['qty' => 1000, 'ws' => 42.00],
      ['qty' => 2500, 'ws' => 70.00],
      ['qty' => 5000, 'ws' => 108.00],
    ],
  ],
  [
    'id' => 'visitenkarten', 'name' => 'Visitenkarten',
    'options' => [
      'finish' => [
        ['label' => 'Standard Glanz',    'mult' => 1.0],
        ['label' => 'Premium Soft-Touch', 'mult' => 1.32],
      ],
    ],
    'tiers' => [
      ['qty' => 100,  'ws' => 12.00],
      ['qty' => 250,  'ws' => 16.00],
      ['qty' => 500,  'ws' => 22.00],
      ['qty' => 1000, 'ws' => 30.00],
      ['qty' => 2500, 'ws' => 55.00],
    ],
  ],
  [
    'id' => 'aufkleber', 'name' => 'Aufkleber & Etiketten',
    'options' => [
      'finish' => [
        ['label' => 'Glanz',       'mult' => 1.0],
        ['label' => 'Matt',        'mult' => 1.08],
        ['label' => 'Transparent', 'mult' => 1.16],
      ],
    ],
    'tiers' => [
      ['qty' => 50,   'ws' => 14.00],
      ['qty' => 100,  'ws' => 20.00],
      ['qty' => 250,  'ws' => 38.00],
      ['qty' => 500,  'ws' => 62.00],
      ['qty' => 1000, 'ws' => 98.00],
    ],
  ],
  [
    'id' => 'rollup', 'name' => 'Roll-up Display',
    'options' => [
      'model' => [
        ['label' => 'Standard Silber', 'mult' => 1.0],
        ['label' => 'Premium Schwarz', 'mult' => 1.32],
      ],
    ],
    'tiers' => [
      ['qty' => 1, 'ws' => 41.52],
      ['qty' => 2, 'ws' => 39.00],
      ['qty' => 3, 'ws' => 37.00],
      ['qty' => 5, 'ws' => 34.50],
    ],
  ],
  [
    'id' => 'plakate', 'name' => 'Allwetter- & Wahlplakate',
    'options' => [
      'size' => [
        ['label' => 'DIN A2 (42×59cm)',  'mult' => 0.68],
        ['label' => 'DIN A1 (59×84cm)',  'mult' => 1.0],
        ['label' => 'DIN A0 (84×119cm)', 'mult' => 1.62],
      ],
    ],
    'tiers' => [
      ['qty' => 5,   'ws' => 32.00],
      ['qty' => 10,  'ws' => 52.00],
      ['qty' => 25,  'ws' => 98.00],
      ['qty' => 50,  'ws' => 160.00],
      ['qty' => 100, 'ws' => 260.00],
    ],
  ],
  [
    'id' => 'broschuren', 'name' => 'Broschüren & Kataloge',
    'options' => [
      'binding' => [
        ['label' => 'Klammerheftung', 'mult' => 1.0],
        ['label' => 'Klebebindung',   'mult' => 1.22],
      ],
      'pages' => [
        ['label' => '8 Seiten',  'mult' => 0.68],
        ['label' => '16 Seiten', 'mult' => 1.0],
        ['label' => '32 Seiten', 'mult' => 1.55],
        ['label' => '48 Seiten', 'mult' => 2.05],
      ],
    ],
    'tiers' => [
      ['qty' => 100,  'ws' => 58.00],
      ['qty' => 250,  'ws' => 92.00],
      ['qty' => 500,  'ws' => 150.00],
      ['qty' => 1000, 'ws' => 240.00],
    ],
  ],
  [
    'id' => 'standbodenbeutel', 'name' => 'Standbodenbeutel',
    'options' => [
      'size' => [
        ['label' => '70×180mm',  'mult' => 0.78],
        ['label' => '100×150mm', 'mult' => 1.0],
        ['label' => '130×220mm', 'mult' => 1.36],
        ['label' => '160×240mm', 'mult' => 1.68],
      ],
    ],
    'tiers' => [
      ['qty' => 100,  'ws' => 65.00],
      ['qty' => 250,  'ws' => 95.00],
      ['qty' => 500,  'ws' => 145.00],
      ['qty' => 1000, 'ws' => 220.00],
    ],
  ],
  [
    'id' => 'kugelschreiber', 'name' => 'Kugelschreiber Werbeartikel',
    'options' => [
      'print' => [
        ['label' => '1-farbig Druck', 'mult' => 1.0],
        ['label' => '4-farbig Druck', 'mult' => 1.22],
        ['label' => 'Laser-Gravur',   'mult' => 1.38],
      ],
    ],
    'tiers' => [
      ['qty' => 50,   'ws' => 45.00],
      ['qty' => 100,  'ws' => 72.00],
      ['qty' => 250,  'ws' => 140.00],
      ['qty' => 500,  'ws' => 220.00],
      ['qty' => 1000, 'ws' => 360.00],
    ],
  ],
];

/**
 * Calculate the server-verified total for a single cart item.
 * Mirrors calcPrice() in shop.js exactly.
 *
 * @param array  $catalog   The $MASAR_CATALOG array
 * @param string $productId Product id slug
 * @param int    $qty       Requested quantity
 * @param array  $opts      Map of optionKey => chosen label
 * @return float Client-facing total price (RESELLER_MARKUP applied), or 0.0 if unknown product
 */
function calcServerPrice(array $catalog, string $productId, int $qty, array $opts): float
{
    $product = null;
    foreach ($catalog as $p) {
        if ($p['id'] === $productId) {
            $product = $p;
            break;
        }
    }
    if ($product === null || $qty < 1) {
        return 0.0;
    }

    // Sort tiers ascending by qty
    $tiers = $product['tiers'];
    usort($tiers, static fn($a, $b) => $a['qty'] <=> $b['qty']);

    // Find best tier: largest tier.qty <= requested qty; fallback to minimum tier
    $tier = $tiers[0];
    foreach ($tiers as $t) {
        if ($qty >= $t['qty']) {
            $tier = $t;
        }
    }

    $wsUnit = $tier['ws'] / $tier['qty'];

    // Stack option multipliers
    $optMult = 1.0;
    foreach ($opts as $key => $label) {
        if (!isset($product['options'][$key])) {
            continue;
        }
        foreach ($product['options'][$key] as $opt) {
            if ($opt['label'] === $label) {
                $optMult *= $opt['mult'];
                break;
            }
        }
    }

    return round($wsUnit * $optMult * RESELLER_MARKUP * $qty, 2);
}

/**
 * Calculate and verify a full cart from the client.
 *
 * @param array $catalog    The $MASAR_CATALOG array
 * @param array $cartItems  Array of {id, opts, qty} from frontend
 * @return array{total: float, lineItems: array}
 */
function calcCartServer(array $catalog, array $cartItems): array
{
    $total     = 0.0;
    $lineItems = [];

    foreach ($cartItems as $item) {
        $id   = (string)  ($item['id']  ?? '');
        $qty  = (int)     ($item['qty'] ?? 0);
        $opts = (array)   ($item['opts'] ?? []);

        $itemTotal = calcServerPrice($catalog, $id, $qty, $opts);
        $total    += $itemTotal;

        $lineItems[] = [
            'id'    => $id,
            'qty'   => $qty,
            'opts'  => $opts,
            'total' => $itemTotal,
        ];
    }

    return ['total' => round($total, 2), 'lineItems' => $lineItems];
}
