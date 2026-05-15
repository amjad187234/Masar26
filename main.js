/* ═══════════════════════════════════════════════
   MASAR WERBEAGENTUR – Style Sheet
   ═══════════════════════════════════════════════ */

:root {
  --teal: #58d0bd;
  --teal-dark: #3ab8a5;
  --teal-deep: #0d8a78;
  --navy: #132e50;
  --navy-light: #1e4275;
  --white: #ffffff;
  --off-white: #f5f8f8;
  --text: #1a2a2a;
  --muted: #5a7070;
  --border: #e2ecec;
  --gray-soft: #cfd2d2;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,.06);
  --shadow-md: 0 8px 32px rgba(0,0,0,.06);
  --shadow-lg: 0 16px 48px rgba(88,208,189,.12);
  --font-body: 'Barlow', sans-serif;
  --font-heading: 'Barlow Condensed', sans-serif;
  --max-w: 1200px;
  --nav-h: 68px;
}

/* ─── RESET ─── */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; font-size: 16px; }
body { font-family: var(--font-body); background: var(--white); color: var(--text); overflow-x: hidden; }
img { max-width: 100%; display: block; }
a { text-decoration: none; color: inherit; }
ul { list-style: none; }

/* ─── COOKIE BANNER ─── */
.cookie-banner {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
  background: var(--navy); color: #fff;
  padding: 18px 32px;
  display: flex; align-items: center; justify-content: space-between;
  gap: 20px; flex-wrap: wrap;
  border-top: 2px solid var(--teal);
  transform: translateY(100%);
  transition: transform .4s ease;
}
.cookie-banner.show { transform: translateY(0); }
.cookie-banner p { font-size: 13px; color: rgba(255,255,255,.75); max-width: 700px; line-height: 1.6; }
.cookie-banner a { color: var(--teal); text-decoration: underline; }
.cookie-btn {
  background: var(--teal); color: var(--navy); border: none;
  padding: 10px 28px; font-family: var(--font-body);
  font-weight: 700; font-size: 13px; cursor: pointer; white-space: nowrap;
  transition: background .2s;
}
.cookie-btn:hover { background: var(--teal-dark); }

/* ─── WHATSAPP FLOAT ─── */
.wa-float {
  position: fixed; bottom: 28px; right: 28px; z-index: 999;
  width: 58px; height: 58px; border-radius: 50%;
  background: #25d366;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(37,211,102,.4);
  transition: transform .2s, box-shadow .2s;
}
.wa-float:hover { transform: scale(1.1); box-shadow: 0 6px 28px rgba(37,211,102,.5); }
.wa-float svg { width: 30px; height: 30px; fill: white; }

/* ─── NAVIGATION ─── */
nav {
  position: fixed; top: 0; width: 100%; z-index: 500;
  background: var(--white);
  backdrop-filter: blur(14px);
  border-bottom: 2px solid var(--teal);
  transition: box-shadow .3s;
}
nav.scrolled { box-shadow: 0 4px 24px rgba(0,0,0,.25); }
.nav-inner {
  max-width: var(--max-w); margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 2rem; height: var(--nav-h);
}
.nav-logo { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.nav-logo img { height: 72px; object-fit: contain; }
.nav-logo-fb {
  font-family: var(--font-heading); font-weight: 900; font-size: 26px;
  color: var(--navy); letter-spacing: 2px; display: none;
}
.nav-links { display: flex; gap: 2rem; align-items: center; }
.nav-links a {
  color: var(--navy); font-size: 14px; font-weight: 500;
  letter-spacing: .5px; padding: 4px 0; position: relative;
  transition: color .2s;
}
.nav-links a::after {
  content: ''; position: absolute; bottom: -2px; left: 0;
  width: 0; height: 2px; background: var(--teal);
  transition: width .3s;
}
.nav-links a:hover, .nav-links a.active { color: var(--teal); }
.nav-links a:hover::after, .nav-links a.active::after { width: 100%; }
.nav-cta {
  background: var(--teal) !important; color: var(--navy) !important;
  padding: 10px 24px; font-weight: 700 !important;
  border-radius: var(--radius-sm);
  transition: background .2s !important;
}
.nav-cta::after { display: none !important; }
.nav-cta:hover { background: var(--teal-dark) !important; }
.nav-hamburger {
  display: none; flex-direction: column; gap: 5px;
  background: none; border: none; cursor: pointer; padding: 4px;
}
.nav-hamburger span {
  width: 24px; height: 2px; background: var(--navy); border-radius: 2px;
  transition: all .3s;
}
.mobile-menu {
  display: none; position: fixed; top: var(--nav-h); left: 0; right: 0;
  background: var(--white); padding: 20px;
  border-bottom: 2px solid var(--teal); z-index: 499;
}
.mobile-menu.open { display: block; }
.mobile-menu a {
  display: block; padding: 12px 16px; color: var(--navy);
  font-size: 15px; font-weight: 500;
  border-bottom: 1px solid rgba(0,0,0,.04);
  transition: color .2s;
}
.mobile-menu a:hover { color: var(--teal); }

/* ─── BUTTONS ─── */
.btn-primary {
  display: inline-block;
  background: var(--teal); color: var(--navy);
  padding: 15px 36px; border-radius: var(--radius-sm);
  font-weight: 700; font-size: 14px; letter-spacing: .5px;
  transition: all .2s;
}
.btn-primary:hover {
  background: var(--teal-dark); transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(88,208,189,.3);
}
.btn-ghost {
  display: inline-block;
  border: 2px solid rgba(255,255,255,.3); color: white;
  padding: 13px 32px; border-radius: var(--radius-sm);
  font-weight: 600; font-size: 14px;
  transition: all .2s;
}
.btn-ghost:hover { border-color: var(--teal); color: var(--teal); }
.btn-white {
  display: inline-block;
  background: white; color: var(--teal-dark);
  padding: 15px 40px; border-radius: var(--radius-sm);
  font-weight: 700; font-size: 14px;
  transition: all .2s;
}
.btn-white:hover { transform: translateY(-2px); box-shadow: 0 12px 36px rgba(0,0,0,.2); }
.btn-outline-teal {
  display: inline-block;
  border: 2px solid var(--teal); color: var(--teal);
  padding: 13px 32px; border-radius: var(--radius-sm);
  font-weight: 600; font-size: 14px;
  transition: all .2s;
}
.btn-outline-teal:hover { background: var(--teal); color: var(--navy); }

/* ─── PAGE HERO ─── */
.page-hero {
  padding: 140px 2rem 80px;
  background: linear-gradient(155deg, var(--navy) 0%, #1a3d6b 50%, #0d5a5a 100%);
  position: relative; overflow: hidden;
}
.page-hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 70% 50%, rgba(88,208,189,.1) 0%, transparent 60%);
}
.page-hero-inner { max-width: var(--max-w); margin: 0 auto; position: relative; z-index: 2; }
.page-label {
  display: inline-block;
  background: rgba(88,208,189,.12);
  border: 1px solid rgba(88,208,189,.35);
  color: var(--teal); font-size: 11px; font-weight: 600;
  letter-spacing: 2.5px; text-transform: uppercase;
  padding: 6px 16px; border-radius: var(--radius-sm); margin-bottom: 1.2rem;
}
.page-hero h1 {
  font-family: var(--font-heading); font-weight: 900;
  font-size: clamp(2.8rem, 6vw, 5rem);
  line-height: .92; color: white; text-transform: uppercase; margin-bottom: 1rem;
}
.page-hero h1 em { color: var(--teal); font-style: normal; }
.page-hero p {
  font-size: 17px; color: rgba(255,255,255,.65);
  max-width: 560px; line-height: 1.7;
}

/* ─── HOMEPAGE HERO ─── */
.hero {
  min-height: 100vh; padding-top: var(--nav-h);
  background: linear-gradient(155deg, var(--navy) 0%, #1a3d6b 50%, #0d5a5a 100%);
  display: flex; align-items: center;
  position: relative; overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 75% 40%, rgba(88,208,189,.12) 0%, transparent 60%);
}
.hero-lines {
  position: absolute; top: 0; right: 0; bottom: 0; width: 45%;
  opacity: .05;
  background: repeating-linear-gradient(-20deg, transparent, transparent 28px, rgba(88,208,189,1) 28px, rgba(88,208,189,1) 29px);
}
.hero-inner {
  max-width: var(--max-w); margin: 0 auto;
  padding: 5rem 2rem;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 4rem; align-items: center;
  position: relative; z-index: 2;
}
.hero-label {
  display: inline-block;
  background: rgba(88,208,189,.12);
  border: 1px solid rgba(88,208,189,.35);
  color: var(--teal); font-size: 11px; font-weight: 600;
  letter-spacing: 2.5px; text-transform: uppercase;
  padding: 6px 16px; border-radius: var(--radius-sm); margin-bottom: 1.5rem;
}
.hero h1 {
  font-family: var(--font-heading); font-weight: 900;
  font-size: clamp(3rem, 6vw, 5.5rem);
  line-height: .9; color: white; text-transform: uppercase;
  margin-bottom: 1.5rem;
}
.hero h1 em { color: var(--teal); font-style: normal; }
.hero-sub {
  font-size: 17px; color: rgba(255,255,255,.65);
  line-height: 1.75; margin-bottom: 2.5rem; max-width: 520px;
}
.hero-btns { display: flex; gap: 1rem; flex-wrap: wrap; }
.hero-stats {
  display: flex; gap: 2.5rem; margin-top: 3rem;
  padding-top: 2rem; border-top: 1px solid rgba(255,255,255,.1);
}
.stat-num {
  font-family: var(--font-heading); font-weight: 900;
  font-size: 2.4rem; color: var(--teal); line-height: 1;
}
.stat-lbl { font-size: 12px; color: rgba(255,255,255,.5); margin-top: 4px; }

/* HERO SLIDER */
.hero-slider-wrap {
  position: relative; border-radius: var(--radius-lg); overflow: hidden;
  box-shadow: 0 24px 64px rgba(0,0,0,.4);
  aspect-ratio: 4/5;
}
.hero-slider-track { display: flex; transition: transform .6s cubic-bezier(.4,0,.2,1); height: 100%; }
.hero-slide { min-width: 100%; height: 100%; position: relative; }
.hero-slide img { width: 100%; height: 100%; object-fit: cover; }
.hero-slide-overlay {
  position: absolute; bottom: 0; left: 0; right: 0;
  background: linear-gradient(to top, rgba(19,46,80,.9) 0%, transparent 60%);
  padding: 28px 24px 22px;
}
.hero-slide-overlay h3 {
  font-family: var(--font-heading); font-weight: 700;
  font-size: 1.5rem; color: white; text-transform: uppercase; letter-spacing: 1px;
}
.hero-slide-overlay p { font-size: 13px; color: rgba(255,255,255,.7); margin-top: 4px; }
.slider-nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  width: 40px; height: 40px; border-radius: 50%;
  background: rgba(19,46,80,.8); border: 1px solid rgba(88,208,189,.4);
  color: var(--teal); font-size: 16px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all .2s; z-index: 10;
}
.slider-nav:hover { background: var(--teal); color: var(--navy); }
.slider-prev { left: 12px; }
.slider-next { right: 12px; }
.slider-dots {
  position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 6px; z-index: 10;
}
.sdot {
  width: 7px; height: 7px; border-radius: 50%;
  background: rgba(255,255,255,.4); border: none; cursor: pointer;
  transition: all .3s; padding: 0;
}
.sdot.active { background: var(--teal); transform: scale(1.4); }

/* ─── STATS BAR ─── */
.stats-bar {
  background: var(--navy);
  display: grid; grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid rgba(88,208,189,.12);
}
.sbar-item {
  padding: 36px 24px; text-align: center;
  border-right: 1px solid rgba(255,255,255,.06);
}
.sbar-item:last-child { border-right: none; }
.sbar-num {
  font-family: var(--font-heading); font-weight: 900;
  font-size: 3rem; color: var(--teal); line-height: 1;
}
.sbar-lbl {
  font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
  color: rgba(255,255,255,.45); margin-top: 6px;
}

/* ─── SECTION COMMON ─── */
.section { padding: 7rem 2rem; }
.section.bg-off { background: var(--off-white); }
.section.bg-navy { background: var(--navy); }
.section.bg-gradient {
  background: linear-gradient(135deg, var(--teal-deep), var(--teal-dark), var(--teal));
}
.sec-inner { max-width: var(--max-w); margin: 0 auto; }
.sec-tag {
  display: inline-block;
  background: rgba(88,208,189,.1); color: var(--teal-deep);
  font-size: 11px; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; padding: 5px 14px;
  border-radius: var(--radius-sm); margin-bottom: 1rem;
}
.sec-tag.light { background: rgba(88,208,189,.15); color: var(--teal); }
.sec-title {
  font-family: var(--font-heading); font-weight: 900;
  font-size: clamp(2.2rem, 4.5vw, 3.8rem);
  text-transform: uppercase; line-height: .95;
  color: var(--navy); margin-bottom: 1rem;
}
.sec-title em { color: var(--teal); font-style: normal; }
.sec-title.white { color: white; }
.sec-sub {
  font-size: 16px; color: var(--muted); line-height: 1.7; max-width: 540px;
}
.sec-sub.light { color: rgba(255,255,255,.55); }
.sec-sub.white { color: rgba(255,255,255,.75); }
.sec-header { margin-bottom: 4rem; }
.sec-header.center { text-align: center; }
.sec-header.center .sec-sub { margin: 0 auto; }

/* ─── BRIDGE SECTION (Offline + Online) ─── */
.bridge-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 2rem; margin-top: 1rem;
}
.bridge-card {
  background: white; border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 2.5rem 2rem;
  text-align: center; position: relative; overflow: hidden;
  transition: all .3s;
}
.bridge-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--teal), var(--teal-dark));
  transform: scaleX(0); transform-origin: left; transition: transform .35s;
}
.bridge-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: rgba(88,208,189,.3); }
.bridge-card:hover::before { transform: scaleX(1); }
.bridge-icon {
  width: 72px; height: 72px; margin: 0 auto 1.2rem;
  background: rgba(88,208,189,.1); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.bridge-icon svg { width: 36px; height: 36px; stroke: var(--teal); fill: none; stroke-width: 1.5; }
.bridge-card h3 {
  font-family: var(--font-heading); font-weight: 700; font-size: 1.4rem;
  text-transform: uppercase; color: var(--navy); margin-bottom: .8rem;
}
.bridge-card p { font-size: 14px; color: var(--muted); line-height: 1.65; margin-bottom: .5rem; }
.bridge-services { margin-top: 1rem; }
.bridge-service-item {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 0; border-top: 1px solid var(--border);
  font-size: 14px; color: var(--text);
}
.bridge-service-item:last-child { border-bottom: 1px solid var(--border); }
.bridge-service-item .bsi-dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--teal); flex-shrink: 0;
}

/* ─── SERVICES GRID ─── */
.services-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
}
.svc-card {
  background: white; border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 2rem;
  position: relative; overflow: hidden;
  transition: all .3s; cursor: default;
}
.svc-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--teal), var(--teal-dark));
  transform: scaleX(0); transform-origin: left; transition: transform .35s;
}
.svc-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-lg); border-color: rgba(88,208,189,.3); }
.svc-card:hover::before { transform: scaleX(1); }
.svc-img {
  width: 100%; aspect-ratio: 4/5; object-fit: cover;
  border-radius: 8px; margin-bottom: 1.2rem;
}
.svc-icon {
  width: 56px; height: 56px; margin-bottom: 1rem;
  background: rgba(88,208,189,.1); border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
}
.svc-icon svg { width: 28px; height: 28px; stroke: var(--teal); fill: none; stroke-width: 1.5; }
.svc-num {
  font-family: var(--font-heading); font-size: 11px; font-weight: 700;
  letter-spacing: 3px; color: var(--teal); opacity: .7; margin-bottom: 8px;
}
.svc-card h3 {
  font-family: var(--font-heading); font-weight: 700;
  font-size: 1.3rem; text-transform: uppercase;
  color: var(--navy); margin-bottom: .5rem; line-height: 1.1;
}
.svc-short { font-size: 14px; color: var(--muted); line-height: 1.65; }
.svc-long {
  font-size: 14px; color: var(--muted); line-height: 1.65;
  margin-top: 10px; display: none;
}
.svc-long.open { display: block; }
.svc-toggle {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--teal); font-size: 12px; font-weight: 700;
  letter-spacing: .5px; text-transform: uppercase;
  background: none; border: none; cursor: pointer;
  margin-top: 1rem; padding: 0; transition: gap .2s;
}
.svc-toggle:hover { gap: 10px; }
.svc-toggle svg { width: 14px; height: 14px; transition: transform .3s; }
.svc-toggle.open svg { transform: rotate(180deg); }

/* ─── PRICING ─── */
.pricing-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 2rem; margin-top: 2rem;
}
.pricing-card {
  background: white; border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 2.5rem 2rem;
  position: relative; transition: all .3s; text-align: center;
}
.pricing-card:hover {
  transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: rgba(88,208,189,.3);
}
.pricing-card.featured {
  border-color: var(--teal); box-shadow: 0 0 0 1px var(--teal), var(--shadow-md);
  transform: scale(1.03);
}
.pricing-card.featured:hover { transform: scale(1.03) translateY(-4px); }
.pricing-badge {
  position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
  background: var(--teal); color: var(--navy);
  font-size: 10px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; padding: 4px 16px; border-radius: 20px;
}
.pricing-card h4 {
  font-family: var(--font-heading); font-weight: 700;
  font-size: 1.2rem; text-transform: uppercase;
  color: var(--navy); margin-bottom: .3rem;
}
.pricing-card .pricing-sub {
  font-size: 13px; color: var(--muted); margin-bottom: 1.5rem;
}
.pricing-price {
  font-family: var(--font-heading); font-weight: 900;
  font-size: 2.8rem; color: var(--navy); line-height: 1;
  margin-bottom: .2rem;
}
.pricing-price span { font-size: 1rem; font-weight: 600; color: var(--muted); }
.pricing-duration { font-size: 12px; color: var(--muted); margin-bottom: 1.5rem; }
.pricing-features { text-align: left; margin-bottom: 2rem; }
.pricing-features li {
  padding: 8px 0; font-size: 14px; color: var(--text);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 8px;
}
.pricing-features li::before {
  content: ''; width: 5px; height: 5px; border-radius: 50%;
  background: var(--teal); flex-shrink: 0;
}

/* ─── TARGET GROUPS ─── */
.target-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem; margin-top: 2rem;
}
.target-card {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: var(--radius-lg); padding: 2rem 1.5rem;
  text-align: center; transition: all .3s;
}
.target-card:hover {
  background: rgba(88,208,189,.1); border-color: rgba(88,208,189,.3);
  transform: translateY(-4px);
}
.target-card .target-icon {
  width: 56px; height: 56px; margin: 0 auto 1rem;
  background: rgba(88,208,189,.15); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px;
}
.target-card h4 { font-size: 16px; font-weight: 700; color: white; margin-bottom: .4rem; }
.target-card p { font-size: 13px; color: rgba(255,255,255,.5); line-height: 1.5; }

/* ─── WHY US ─── */
.why-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5rem; align-items: center; }
.why-features { display: flex; flex-direction: column; gap: 1rem; margin-top: 2rem; }
.why-feat {
  display: flex; gap: 14px; align-items: flex-start;
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 10px; padding: 16px 18px;
  transition: all .3s;
}
.why-feat:hover { background: rgba(88,208,189,.08); border-color: rgba(88,208,189,.25); }
.why-feat-icon {
  width: 36px; height: 36px; flex-shrink: 0;
  background: rgba(88,208,189,.15); border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}
.why-feat h4 { font-size: 15px; font-weight: 600; color: white; margin-bottom: 3px; }
.why-feat p { font-size: 13px; color: rgba(255,255,255,.5); }
.why-nums { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
.wnum {
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: var(--radius-lg); padding: 2rem; text-align: center;
  transition: all .3s;
}
.wnum:hover { background: rgba(88,208,189,.1); border-color: rgba(88,208,189,.3); transform: scale(1.02); }
.wnum-big {
  font-family: var(--font-heading); font-weight: 900;
  font-size: 3.5rem; color: var(--teal); line-height: 1;
}
.wnum-big span { color: #f5c000; }
.wnum p { font-size: 13px; color: rgba(255,255,255,.45); margin-top: 8px; }

/* ─── PROCESS ─── */
.process-steps {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 0; margin-top: 4rem; position: relative;
}
.process-steps::before {
  content: ''; position: absolute; top: 40px; left: 12%; right: 12%;
  height: 2px; background: linear-gradient(90deg, var(--teal), rgba(88,208,189,.15));
}
.pstep { text-align: center; padding: 0 1rem; }
.pstep-num {
  width: 80px; height: 80px; border-radius: 50%;
  background: linear-gradient(135deg, var(--teal), var(--teal-dark));
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-heading); font-weight: 900;
  font-size: 2rem; color: white;
  margin: 0 auto 1.5rem; position: relative; z-index: 2;
  box-shadow: 0 8px 28px rgba(88,208,189,.3);
}
.pstep h4 {
  font-family: var(--font-heading); font-weight: 700;
  font-size: 1.15rem; text-transform: uppercase;
  color: var(--navy); margin-bottom: .5rem;
}
.pstep p { font-size: 14px; color: var(--muted); line-height: 1.6; }

/* ─── CONTACT ─── */
.contact-grid { display: grid; grid-template-columns: 1fr 1.3fr; gap: 4rem; }
.contact-info-item {
  display: flex; gap: 14px; align-items: flex-start;
  padding: 20px 0; border-bottom: 1px solid var(--border);
}
.cinfo-icon {
  width: 46px; height: 46px; background: var(--teal);
  border-radius: var(--radius-md); display: flex;
  align-items: center; justify-content: center;
  flex-shrink: 0; font-size: 20px;
}
.cinfo-lbl {
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--teal); font-weight: 700; margin-bottom: 4px;
}
.cinfo-val { font-size: 15px; color: var(--navy); font-weight: 600; }
.cinfo-val a { color: inherit; }
.cform {
  background: white; border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 2.5rem;
  box-shadow: var(--shadow-md);
}
.cform h3 {
  font-family: var(--font-heading); font-weight: 700;
  font-size: 1.6rem; text-transform: uppercase;
  color: var(--navy); margin-bottom: 1.5rem;
}
.fg { margin-bottom: 1rem; }
.fg label {
  display: block; font-size: 12px; font-weight: 600;
  letter-spacing: 1px; text-transform: uppercase;
  color: var(--muted); margin-bottom: 6px;
}
.fg input, .fg textarea, .fg select {
  width: 100%; background: var(--off-white);
  border: 2px solid var(--border); color: var(--text);
  padding: 13px 16px; font-family: var(--font-body); font-size: 15px;
  outline: none; transition: border-color .2s, background .2s;
  border-radius: var(--radius-md); -webkit-appearance: none;
}
.fg input:focus, .fg textarea:focus, .fg select:focus { border-color: var(--teal); background: white; }
.fg textarea { height: 120px; resize: none; }
.fg-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.submit-btn {
  width: 100%; background: var(--navy); color: white;
  border: none; padding: 16px; border-radius: var(--radius-md);
  font-family: var(--font-body); font-weight: 700;
  font-size: 14px; letter-spacing: 1px; text-transform: uppercase;
  cursor: pointer; transition: background .2s; margin-top: .5rem;
}
.submit-btn:hover { background: var(--teal); color: var(--navy); }
.form-success {
  display: none; background: rgba(88,208,189,.1);
  border: 1px solid var(--teal); border-radius: var(--radius-md);
  padding: 16px; margin-top: 1rem;
  text-align: center; color: var(--teal-deep); font-weight: 600;
}

/* ─── CTA STRIP ─── */
.cta-strip {
  background: linear-gradient(135deg, var(--teal-deep), var(--teal-dark), var(--teal));
  padding: 5rem 2rem; text-align: center;
}
.cta-strip h2 {
  font-family: var(--font-heading); font-weight: 900;
  font-size: clamp(2rem, 4vw, 3.5rem);
  color: white; text-transform: uppercase; margin-bottom: 1rem;
}
.cta-strip h2 em { color: #f5c000; font-style: normal; }
.cta-strip p { font-size: 17px; color: rgba(255,255,255,.75); margin-bottom: 2rem; }

/* ─── LEGAL PAGES ─── */
.legal-section {
  max-width: 900px; margin: 0 auto; padding: 5rem 2rem;
}
.legal-block { margin-bottom: 3rem; }
.legal-block h2 {
  font-family: var(--font-heading); font-weight: 700;
  font-size: 1.5rem; text-transform: uppercase;
  color: var(--navy); margin-bottom: 1rem;
  padding-bottom: .8rem; border-bottom: 2px solid var(--teal);
}
.legal-block h3 {
  font-size: 15px; font-weight: 600; color: var(--navy);
  margin: 1.2rem 0 .5rem;
}
.legal-block p {
  font-size: 14.5px; color: var(--muted);
  line-height: 1.9; margin-bottom: .8rem;
}
.legal-block ul { margin: .5rem 0 1rem 1.5rem; }
.legal-block ul li {
  font-size: 14.5px; color: var(--muted);
  line-height: 1.9; margin-bottom: .3rem;
}
.legal-block a { color: var(--teal); text-decoration: underline; }
.legal-info-box {
  background: var(--off-white); border: 1px solid var(--border);
  border-left: 3px solid var(--teal);
  padding: 1.5rem 2rem; margin: 1rem 0;
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
}
.legal-info-box p {
  margin-bottom: .4rem; font-size: 14.5px; color: var(--muted); line-height: 1.8;
}

/* ─── FOOTER ─── */
footer {
  background: #060e1a;
  padding: 4rem 2rem 2rem;
  color: rgba(255,255,255,.45);
}
.foot-inner {
  max-width: var(--max-w); margin: 0 auto;
  display: grid; grid-template-columns: 2fr 1fr 1fr;
  gap: 3rem; padding-bottom: 3rem;
  border-bottom: 1px solid rgba(255,255,255,.06);
}
.foot-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 1rem; }
.foot-logo img { height: 72px; object-fit: contain; }
.foot-logo-fb {
  font-family: var(--font-heading); font-weight: 900;
  font-size: 24px; color: var(--teal); letter-spacing: 2px; display: none;
}
.foot-brand p { font-size: 14px; line-height: 1.75; }
.foot-social { display: flex; gap: .8rem; margin-top: 1.5rem; }
.fsoc {
  width: 38px; height: 38px; border-radius: 50%;
  border: 1px solid rgba(255,255,255,.15);
  display: flex; align-items: center; justify-content: center;
  transition: all .2s;
}
.fsoc:hover { border-color: var(--teal); background: rgba(88,208,189,.1); transform: scale(1.1); }
.fsoc svg { width: 18px; height: 18px; fill: rgba(255,255,255,.5); }
.fsoc:hover svg { fill: var(--teal); }
.foot-col h5 {
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: white; margin-bottom: 1.2rem;
}
.foot-col a {
  display: block; font-size: 14px; color: rgba(255,255,255,.4);
  margin-bottom: .6rem; transition: color .2s;
}
.foot-col a:hover { color: var(--teal); }
.foot-bottom {
  max-width: var(--max-w); margin: 2rem auto 0;
  display: flex; justify-content: space-between; align-items: center;
  font-size: 12px; flex-wrap: wrap; gap: 1rem;
}

/* ─── ANIMATIONS ─── */
.fade-up { opacity: 0; transform: translateY(28px); transition: opacity .65s ease, transform .65s ease; }
.fade-up.vis { opacity: 1; transform: translateY(0); }

/* ─── RESPONSIVE: TABLET (≤960px) ─── */
@media (max-width: 960px) {
  .nav-links { display: none; }
  .nav-hamburger { display: flex; }
  .hero-inner { grid-template-columns: 1fr; }
  .hero-slider-wrap { max-width: 440px; margin: 0 auto; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .services-grid { grid-template-columns: 1fr 1fr; }
  .bridge-grid { grid-template-columns: 1fr; max-width: 480px; margin-left: auto; margin-right: auto; }
  .pricing-grid { grid-template-columns: 1fr; max-width: 420px; margin-left: auto; margin-right: auto; }
  .pricing-card.featured { transform: none; }
  .pricing-card.featured:hover { transform: translateY(-4px); }
  .why-grid { grid-template-columns: 1fr; }
  .process-steps { grid-template-columns: 1fr 1fr; gap: 2rem; }
  .process-steps::before { display: none; }
  .contact-grid { grid-template-columns: 1fr; }
  .target-grid { grid-template-columns: 1fr 1fr; }
  .foot-inner { grid-template-columns: 1fr 1fr; }
}

/* ─── RESPONSIVE: MOBILE (≤600px) ─── */
@media (max-width: 600px) {
  .hero { min-height: auto; padding: 100px 0 60px; }
  .hero-inner { padding: 0 1.5rem; gap: 2rem; }
  .hero h1 { font-size: clamp(2.8rem, 13vw, 4rem); }
  .hero-sub { font-size: 15px; }
  .hero-btns { flex-direction: column; }
  .hero-btns a { text-align: center; width: 100%; }
  .hero-stats { flex-direction: column; gap: 1rem; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .sbar-item { padding: 24px 12px; }
  .sbar-num { font-size: 2.2rem; }
  .services-grid { grid-template-columns: 1fr; }
  .section { padding: 4rem 1.5rem; }
  .sec-header { margin-bottom: 2.5rem; }
  .fg-row { grid-template-columns: 1fr; }
  .foot-inner { grid-template-columns: 1fr; }
  .target-grid { grid-template-columns: 1fr; }
  .why-nums { grid-template-columns: 1fr; }
  .page-hero { padding: 120px 1.5rem 60px; }
  .page-hero h1 { font-size: clamp(2rem, 10vw, 3.5rem); }
  .legal-section { padding: 3rem 1.5rem; }
  .pricing-card.featured { transform: none; }
  .bridge-grid { gap: 1.2rem; }
  .fb-row { grid-template-columns: 1fr; }
}

/* ─── MOBILE HERO SLIDER HIDE ─── */
@media (max-width: 768px) {
  .hero-slider-wrap { display: none; }
  .hero-lines { display: none; }
}
