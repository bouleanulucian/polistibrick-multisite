/* ===========================================================================
   POLISTIBRICK — Shared site JS
   - Injects nav + footer into pages
   - Handles scroll-shadow on nav
   - Handles reveal-on-scroll animations
   =========================================================================== */

(function () {
  const BASE = (function () {
    // Determine path prefix back to root. Pages can override by setting
    // <body data-base="/"> or similar. Default: compute from current depth.
    const explicit = document.body.dataset.base;
    if (explicit) return explicit;
    const depth = (window.location.pathname.replace(/\/$/, '').match(/\//g) || []).length;
    return depth <= 1 ? '' : '../'.repeat(depth - 1);
  })();

  const NAV_HTML = `
    <div class="nav-inner">
      <a href="${BASE}" class="nav-logo" aria-label="Polistibrick — home">
        <img src="${BASE}images/logo.png" alt="Polistibrick" loading="eager">
      </a>
      <nav class="nav-menu" aria-label="Hoofdnavigatie">
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Producten
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}produse/pereti-mbk/">MBK-muren<span class="nav-dropdown-item-sub">Isolerende bekisting voor dragende muren</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/planseu-pbk/">PBK-vloeren<span class="nav-dropdown-item-sub">Geprefabriceerde panelen met faseverschuiving 10,8 u</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/acoperis-tbk/">TBK-dak<span class="nav-dropdown-item-sub">Passivhaus-systeem uit de fabriek</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/accesorii/">Accessoires<span class="nav-dropdown-item-sub">Hoekstukken, eindstukken, trappen, ramen</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Oplossingen
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}pentru/proprietari/">Voor eigenaren<span class="nav-dropdown-item-sub">Passiefhuis zonder hoge rekeningen</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/arhitecti/">Voor architecten<span class="nav-dropdown-item-sub">Bouwdetails, BIM, fiches</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/constructori/">Voor bouwers<span class="nav-dropdown-item-sub">Montage, certificering, partnership</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/investitori/">Voor investeerders<span class="nav-dropdown-item-sub">ROI, uitvoeringssnelheid, projecten</span></a>
            <a class="nav-dropdown-item" href="${BASE}devino-partener/" style="color:var(--red);font-weight:600;">→ Word partner<span class="nav-dropdown-item-sub" style="color:rgba(200,16,46,0.7);">Aanvraag gecertificeerde bouwers</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Projecten
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}proiecte/">Gebouwde huizen<span class="nav-dropdown-item-sub">Galerij + kaart van projecten</span></a>
            <a class="nav-dropdown-item" href="${BASE}testimoniale/">Getuigenissen (video)<span class="nav-dropdown-item-sub">Eigenaren spreken, met echte cijfers</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Calculator
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}calculator/">Kostencalculator<span class="nav-dropdown-item-sub">Schat de paneelprijs voor uw huis</span></a>
            <a class="nav-dropdown-item" href="${BASE}economii/">Besparingscalculator<span class="nav-dropdown-item-sub">Polistibrick vs baksteen over 25 jaar</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Bronnen
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}comparatie/">Vergelijking<span class="nav-dropdown-item-sub">Polistibrick vs klassiek systeem vs andere ICF</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/blog/">Blog<span class="nav-dropdown-item-sub">Artikelen over Passiefhuis, ICF</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/faq/">Veelgestelde vragen<span class="nav-dropdown-item-sub">Antwoorden op de meest gestelde vragen</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Over ons
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}despre/">Het bedrijf<span class="nav-dropdown-item-sub">Wie wij zijn, visie, missie</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/patent/">Het Polistibrick-octrooi<span class="nav-dropdown-item-sub">Het octrooi dat ons uniek maakt</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/certificari/">Certificeringen<span class="nav-dropdown-item-sub">CE, ISO, Passivhaus, technische goedkeuringen</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/fabrici/">Onze fabrieken<span class="nav-dropdown-item-sub">Valencia (ES) en Craiova (RO)</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/echipa/">Het team<span class="nav-dropdown-item-sub">Oprichters en onze mensen</span></a>
          </div>
        </div>
      </nav>
      <div class="nav-cta">
        <div class="country-switcher" data-country-switcher>
          <button class="country-switcher-trigger" type="button" aria-label="Kies uw land" aria-expanded="false">
            <span class="country-switcher-flag">🇧🇪</span>
            <span class="country-switcher-code">BE</span>
            <svg class="country-switcher-caret" viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="3,5 6,8 9,5"/></svg>
          </button>
          <div class="country-switcher-panel" role="menu" aria-hidden="true">
            <div class="country-switcher-header">🌍 Kies uw land</div>
            <a href="https://polistibrick.ro" data-country="ro" class="country-switcher-item"><span class="flag">🇷🇴</span><span class="name">România</span><span class="domain">polistibrick.ro</span></a>
            <a href="https://polistibrick.fr" data-country="fr" class="country-switcher-item"><span class="flag">🇫🇷</span><span class="name">France</span><span class="domain">polistibrick.fr</span></a>
            <a href="https://polistibrick.it" data-country="it" class="country-switcher-item"><span class="flag">🇮🇹</span><span class="name">Italia</span><span class="domain">polistibrick.it</span></a>
            <a href="https://polistibrick.es" data-country="es" class="country-switcher-item"><span class="flag">🇪🇸</span><span class="name">España</span><span class="domain">polistibrick.es</span></a>
            <a href="https://polistibrick.be" data-country="be" class="country-switcher-item"><span class="flag">🇧🇪</span><span class="name">België</span><span class="domain">polistibrick.be</span></a>
            <a href="https://polistibrick.ie" data-country="ie" class="country-switcher-item"><span class="flag">🇮🇪</span><span class="name">Ireland</span><span class="domain">polistibrick.ie</span></a>
            <a href="https://polistibrick.uk" data-country="uk" class="country-switcher-item"><span class="flag">🇬🇧</span><span class="name">United Kingdom</span><span class="domain">polistibrick.uk</span></a>
            <a href="https://polistibrick.com" data-country="ch" class="country-switcher-item"><span class="flag">🇨🇭</span><span class="name">Schweiz</span><span class="domain">polistibrick.com</span></a>
          </div>
        </div>
        <a href="${BASE}contact/" class="btn btn-ghost">Contact</a>
        <a href="${BASE}oferta/" class="btn btn-primary btn-arrow">Vraag een offerte</a>
      </div>
    </div>
  `;

  const FOOTER_HTML = `
    <div class="container container--wide">
      <div class="footer-grid">
        <div>
          <a href="${BASE}" class="footer-logo">
            <img src="${BASE}images/logo.png" alt="Polistibrick" style="height:32px;">
          </a>
          <p class="footer-brand-tagline">Het gepatenteerde ICF-systeem voor premium passiefhuizen, zonder energierekeningen. Gemaakt in de EU.</p>
        </div>
        <div class="footer-col">
          <h5>Producten</h5>
          <ul>
            <li><a href="${BASE}produse/pereti-mbk/">MBK-muren</a></li>
            <li><a href="${BASE}produse/planseu-pbk/">PBK-vloeren</a></li>
            <li><a href="${BASE}produse/acoperis-tbk/">TBK-dak</a></li>
            <li><a href="${BASE}produse/accesorii/">Accessoires</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Oplossingen</h5>
          <ul>
            <li><a href="${BASE}pentru/proprietari/">Eigenaren</a></li>
            <li><a href="${BASE}pentru/arhitecti/">Architecten</a></li>
            <li><a href="${BASE}pentru/constructori/">Bouwers</a></li>
            <li><a href="${BASE}pentru/investitori/">Investeerders</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Bronnen</h5>
          <ul>
            <li><a href="${BASE}proiecte/">Gerealiseerde projecten</a></li>
            <li><a href="${BASE}resurse/blog/">Blog</a></li>
            <li><a href="${BASE}resurse/faq/">Veelgestelde vragen</a></li>
            <li><a href="${BASE}calculator/">Kostencalculator</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Bedrijf</h5>
          <ul>
            <li><a href="${BASE}despre/">Over ons</a></li>
            <li><a href="${BASE}despre/patent/">Het Polistibrick-octrooi</a></li>
            <li><a href="${BASE}despre/certificari/">Certificeringen</a></li>
            <li><a href="${BASE}despre/fabrici/">Onze fabrieken</a></li>
            <li><a href="${BASE}contact/">Contact</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Polistibrick. Alle rechten voorbehouden. Gepatenteerd systeem.</span>
        <div class="footer-bottom-links">
          <a href="${BASE}legal/termeni/">Voorwaarden</a>
          <a href="${BASE}legal/confidentialitate/">Privacy</a>
          <a href="${BASE}legal/cookies/">Cookies</a>
          <a href="${BASE}legal/sustenabilitate/">Duurzaamheid</a>
        </div>
      </div>
    </div>
  `;

  // Inject nav and footer
  function inject() {
    const navMount = document.querySelector('[data-include="nav"]');
    const footMount = document.querySelector('[data-include="footer"]');
    if (navMount) navMount.innerHTML = NAV_HTML;
    if (footMount) footMount.innerHTML = FOOTER_HTML;

    // Mark active page in nav
    const path = window.location.pathname;
    document.querySelectorAll('.nav-dropdown-item, .nav-link').forEach(link => {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;
      const linkPath = new URL(href, window.location.origin).pathname;
      if (path === linkPath || (linkPath !== '/' && path.startsWith(linkPath))) {
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  // Scroll shadow on nav
  function navShadow() {
    const nav = document.querySelector('[data-include="nav"]');
    if (!nav) return;
    const update = () => nav.classList.toggle('is-scrolled', window.scrollY > 6);
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  // Country switcher (in shared nav) — toggle + mark active
  function countrySwitcherShared() {
    document.querySelectorAll('[data-country-switcher]').forEach(switcher => {
      const trigger = switcher.querySelector('.country-switcher-trigger');
      const panel = switcher.querySelector('.country-switcher-panel');
      if (!trigger || !panel) return;

      // Mark active based on current URL path (e.g. /fr/, /ro/, etc.)
      const path = window.location.pathname;
      // Try to detect country code from URL: /polistibrick-multisite/fr/... or /fr/...
      const m = path.match(/\/(ro|fr|it|es|nl|de|en|ie)(\/|$)/i);
      const currentFolder = m ? m[1].toLowerCase() : null;
      // Folder → country picker key map
      const folderToKey = { ro: 'ro', fr: 'fr', it: 'it', es: 'es', nl: 'be', de: 'ch', en: 'uk', ie: 'ie' };
      const currentKey = folderToKey[currentFolder];
      if (currentKey) {
        panel.querySelectorAll('.country-switcher-item').forEach(item => {
          if (item.dataset.country === currentKey) item.classList.add('active');
        });
      }

      function setOpen(open) {
        trigger.setAttribute('aria-expanded', String(open));
        panel.setAttribute('aria-hidden', String(!open));
        panel.classList.toggle('open', open);
      }
      trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = trigger.getAttribute('aria-expanded') === 'true';
        setOpen(!isOpen);
      });
      document.addEventListener('click', (e) => {
        if (!switcher.contains(e.target)) setOpen(false);
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') setOpen(false);
      });
    });
  }

  // Reveal-on-scroll
  function reveal() {
    const items = document.querySelectorAll('.reveal');
    if (!items.length || !('IntersectionObserver' in window)) {
      items.forEach(el => el.classList.add('is-visible'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
    items.forEach(el => io.observe(el));
  }

  // Gallery tabs + lightbox
  function gallery() {
    // Tabs
    document.querySelectorAll('[data-gallery]').forEach(gal => {
      const tabs = gal.querySelectorAll('.gallery-tab');
      const items = gal.querySelectorAll('.gallery-item');

      // Update counts on tabs
      tabs.forEach(tab => {
        const filter = tab.dataset.filter;
        const countEl = tab.querySelector('.gallery-tab-count');
        if (!countEl) return;
        let n;
        if (filter === 'all') n = items.length;
        else n = Array.from(items).filter(i => i.dataset.category === filter).length;
        countEl.textContent = n;
      });

      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          tabs.forEach(t => t.classList.toggle('is-active', t === tab));
          const filter = tab.dataset.filter;
          items.forEach(item => {
            const show = filter === 'all' || item.dataset.category === filter;
            item.classList.toggle('is-hidden', !show);
          });
        });
      });
    });

    // Lightbox
    const lb = document.querySelector('.lightbox');
    if (!lb) return;
    const lbImg = lb.querySelector('.lightbox-img');
    const lbCap = lb.querySelector('.lightbox-caption');
    const lbCounter = lb.querySelector('.lightbox-counter');
    const lbClose = lb.querySelector('.lightbox-close');
    const lbPrev = lb.querySelector('.lightbox-prev');
    const lbNext = lb.querySelector('.lightbox-next');

    let allItems = [];
    let currentIdx = 0;

    function buildList(scope) {
      allItems = Array.from(scope.querySelectorAll('.gallery-item')).filter(i => !i.classList.contains('is-hidden'));
    }

    function show(idx) {
      if (!allItems.length) return;
      currentIdx = (idx + allItems.length) % allItems.length;
      const item = allItems[currentIdx];
      const href = item.getAttribute('href');
      const caption = item.dataset.caption || item.querySelector('.gallery-item-caption')?.textContent.trim() || '';
      if (href && href !== '#') {
        lbImg.src = href;
        lbImg.alt = caption;
        lbImg.style.display = 'block';
      } else {
        // Placeholder — show the placeholder text as image alt
        lbImg.style.display = 'none';
      }
      lbCap.textContent = caption;
      lbCounter.textContent = `${currentIdx + 1} / ${allItems.length}`;
    }

    document.querySelectorAll('[data-gallery]').forEach(gal => {
      gal.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', (e) => {
          e.preventDefault();
          buildList(gal);
          const idx = allItems.indexOf(item);
          if (idx < 0) return;
          show(idx);
          lb.classList.add('is-open');
          document.body.style.overflow = 'hidden';
        });
      });
    });

    function close() {
      lb.classList.remove('is-open');
      document.body.style.overflow = '';
    }
    lbClose.addEventListener('click', close);
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    lbPrev.addEventListener('click', (e) => { e.stopPropagation(); show(currentIdx - 1); });
    lbNext.addEventListener('click', (e) => { e.stopPropagation(); show(currentIdx + 1); });
    document.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(currentIdx - 1);
      if (e.key === 'ArrowRight') show(currentIdx + 1);
    });
  }

  // ========================================================================
  // COUNTRY PICKER — redirects users to their country site
  // ========================================================================
  const POLISTIBRICK_COUNTRIES = {
    RO: { name: 'România', flag: '🇷🇴', url: 'https://polistibrick.ro' },
    ES: { name: 'España', flag: '🇪🇸', url: 'https://polistibrick.es' },
    FR: { name: 'France', flag: '🇫🇷', url: 'https://polistibrick.fr' },
    BE: { name: 'Belgique', flag: '🇧🇪', url: 'https://polistibrick.be' },
    IT: { name: 'Italia', flag: '🇮🇹', url: 'https://polistibrick.it' },
    AT: { name: 'Österreich', flag: '🇦🇹', url: 'https://polistibrick.at' },
    GB: { name: 'United Kingdom', flag: '🇬🇧', url: 'https://polistibrick.uk' },
    IE: { name: 'Ireland', flag: '🇮🇪', url: 'https://polistibrick.ie' },
    ME: { name: 'Crna Gora', flag: '🇲🇪', url: 'https://polistibrick.me' },
  };
  // Map non-Polistibrick European codes to nearest country (e.g., DE → AT, NL → BE)
  const FALLBACK_COUNTRY = {
    'DE': 'AT', 'NL': 'BE', 'LU': 'BE', 'CH': 'AT', 'PT': 'ES',
    'HU': 'RO', 'BG': 'RO', 'MD': 'RO', 'PL': 'RO',
    'GR': 'IT', 'HR': 'IT', 'SI': 'IT', 'SK': 'AT', 'CZ': 'AT',
    'RS': 'ME', 'BA': 'ME', 'MK': 'ME', 'AL': 'ME',
    'GB': 'GB', 'UK': 'GB',
  };

  let detectedCountry = null;

  async function detectUserCountry() {
    const cached = localStorage.getItem('pb_country');
    if (cached && POLISTIBRICK_COUNTRIES[cached]) return cached;
    try {
      const resp = await fetch('https://ipapi.co/json/', { signal: AbortSignal.timeout(3000) });
      const data = await resp.json();
      let code = (data.country_code || '').toUpperCase();
      // Direct hit?
      if (POLISTIBRICK_COUNTRIES[code]) {
        localStorage.setItem('pb_country', code);
        return code;
      }
      // Try fallback (nearest Polistibrick country)
      if (FALLBACK_COUNTRY[code] && POLISTIBRICK_COUNTRIES[FALLBACK_COUNTRY[code]]) {
        return FALLBACK_COUNTRY[code];
      }
    } catch (e) {
      // API timeout or fail — silently ignore
    }
    return null;
  }

  function buildCountryPickerModal() {
    const modal = document.createElement('div');
    modal.className = 'country-picker';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Kies uw land');
    modal.innerHTML = `
      <div class="country-picker-backdrop"></div>
      <div class="country-picker-panel">
        <button class="country-picker-close" aria-label="Sluiten">×</button>
        <div class="country-picker-header">
          <span class="country-picker-eyebrow">🌍 Kies uw land</span>
          <h2 class="country-picker-title">In welk land <em>bouwt u?</em></h2>
          <p class="country-picker-sub">Wij sturen u door naar de site van uw land met het lokale team, direct contact en een offerte in uw taal.</p>
        </div>
        <div class="country-picker-grid">
          ${Object.entries(POLISTIBRICK_COUNTRIES).map(([code, c]) => `
            <a href="${c.url}" class="country-picker-item ${code === detectedCountry ? 'is-detected' : ''}" data-country="${code}" target="_blank" rel="noopener">
              <span class="country-picker-flag">${c.flag}</span>
              <span class="country-picker-name">${c.name}</span>
              ${code === detectedCountry ? '<span class="country-picker-tag">★ Uw land</span>' : ''}
            </a>
          `).join('')}
        </div>
        <p class="country-picker-foot">Uw land staat er niet bij? Schrijf ons op <a href="mailto:info@polistibrick.eu">info@polistibrick.eu</a></p>
      </div>
    `;
    document.body.appendChild(modal);
    modal.querySelector('.country-picker-close').addEventListener('click', closeCountryPicker);
    modal.querySelector('.country-picker-backdrop').addEventListener('click', closeCountryPicker);
    return modal;
  }

  function openCountryPicker() {
    let modal = document.querySelector('.country-picker');
    if (!modal) modal = buildCountryPickerModal();
    requestAnimationFrame(() => modal.classList.add('is-open'));
    document.body.style.overflow = 'hidden';
  }

  function closeCountryPicker() {
    const modal = document.querySelector('.country-picker');
    if (modal) modal.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  function wireCountryPickerButtons() {
    // Only trigger on explicit data-action="country-picker" buttons (optional, not used by default)
    document.body.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-action="country-picker"]');
      if (trigger) {
        e.preventDefault();
        openCountryPicker();
      }
    });
    document.addEventListener('keydown', (e) => {
      const modal = document.querySelector('.country-picker');
      if (e.key === 'Escape' && modal && modal.classList.contains('is-open')) closeCountryPicker();
    });
  }

  document.addEventListener('DOMContentLoaded', async () => {
    inject();
    navShadow();
    countrySwitcherShared();
    reveal();
    gallery();
    wireCountryPickerButtons();
    detectedCountry = await detectUserCountry();
  });
})();
