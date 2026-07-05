/* ===========================================================================
   POLISTIBRICK — Shared site JS
   - Injects nav + footer into pages
   - Handles scroll-shadow on nav
   - Handles reveal-on-scroll animations
   =========================================================================== */

(function () {
  const BASE = (function () {
    const explicit = document.body.getAttribute('data-base');
    if (explicit !== null) return explicit;

    const parts = window.location.pathname.split('/').filter(Boolean);
    const countryFolders = ['ro', 'fr', 'it', 'es', 'nl', 'ie', 'en', 'de'];
    const countryIdx = parts.findIndex(function (p) { return countryFolders.includes(p); });

    // GitHub Pages preview: /user/repo/ro/devis/ → depth from country folder
    if (location.hostname.includes('github.io') && countryIdx >= 0) {
      var depth = parts.length - countryIdx - 1;
      return depth <= 0 ? '' : '../'.repeat(depth);
    }

    var depth = (window.location.pathname.replace(/\/$/, '').match(/\//g) || []).length;
    return depth <= 1 ? '' : '../'.repeat(depth - 1);
  })();

  const NAV_HTML = `
    <div class="nav-inner">
      <a href="${BASE}" class="logo nav-logo" aria-label="Polistibrick — accueil">
        <img src="${BASE}images/logo.png" alt="Polistibrick" class="logo-img" loading="eager">
      </a>
      <div class="nav-cta">
        <!-- COUNTRY SWITCHER -->
        <div class="country-switcher" data-country-switcher>
          <button class="country-switcher-trigger" type="button" aria-label="Choisissez votre pays" aria-expanded="false">
            <span class="country-switcher-flag">🇫🇷</span>
            <span class="country-switcher-code">FR</span>
            <svg class="country-switcher-caret" viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="3,5 6,8 9,5"/></svg>
          </button>
          <div class="country-switcher-panel" role="menu" aria-hidden="true">
            <div class="country-switcher-header">🌍 Choisissez votre pays</div>
            <a href="#" data-country="ro" data-domain="https://polistibrick.ro" data-folder="ro" class="country-switcher-item"><span class="flag">🇷🇴</span><span class="name">România</span><span class="domain">polistibrick.ro</span></a>
            <a href="#" data-country="fr" data-domain="https://polistibrick.fr" data-folder="fr" class="country-switcher-item"><span class="flag">🇫🇷</span><span class="name">France</span><span class="domain">polistibrick.fr</span></a>
            <a href="#" data-country="it" data-domain="https://polistibrick.it" data-folder="it" class="country-switcher-item"><span class="flag">🇮🇹</span><span class="name">Italie</span><span class="domain">polistibrick.it</span></a>
            <a href="#" data-country="es" data-domain="https://polistibrick.es" data-folder="es" class="country-switcher-item"><span class="flag">🇪🇸</span><span class="name">Espagne</span><span class="domain">polistibrick.es</span></a>
            <a href="#" data-country="be" data-domain="https://polistibrick.be" data-folder="nl" class="country-switcher-item"><span class="flag">🇧🇪</span><span class="name">Belgique</span><span class="domain">polistibrick.be</span></a>
            <a href="#" data-country="ie" data-domain="https://polistibrick.ie" data-folder="ie" class="country-switcher-item"><span class="flag">🇮🇪</span><span class="name">Irlande</span><span class="domain">polistibrick.ie</span></a>
            <a href="#" data-country="uk" data-domain="https://polistibrick.uk" data-folder="en" class="country-switcher-item"><span class="flag">🇬🇧</span><span class="name">Royaume-Uni</span><span class="domain">polistibrick.uk</span></a>
            <a href="#" data-country="ch" data-domain="https://polistibrick.com" data-folder="de" class="country-switcher-item"><span class="flag">🇨🇭</span><span class="name">Suisse</span><span class="domain">polistibrick.com</span></a>
          </div>
        </div>
        <a href="${BASE}devis/" class="btn btn-primary nav-cta-devis">Devis</a>
        <button class="nav-burger nav-toggle" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="navDrawerShared">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <div class="nav-drawer-overlay" data-nav-overlay aria-hidden="true"></div>
    <aside class="nav-drawer" id="navDrawerShared" aria-label="Menu de navigation" aria-hidden="true">
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Produits<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}produits/murs-mbk/">Murs MBK</a>
          <a href="${BASE}produits/planchers-pbk/">Planchers PBK</a>
          <a href="${BASE}produits/toit-tbk/">Toit TBK</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Solutions<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}pour/proprietaires/">Pour les propriétaires</a>
          <a href="${BASE}pour/architectes/">Pour les architectes</a>
          <a href="${BASE}pour/constructeurs/">Pour les constructeurs</a>
          <a href="${BASE}pour/investisseurs/">Pour les investisseurs</a>
          <a href="${BASE}devenir-partenaire/" class="partner-link">→ Devenez partenaire</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Projets<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}projets/">Maisons construites</a>
          <a href="${BASE}temoignages/">Témoignages (vidéo)</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Calculateur<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}calculateur/">Calculateur de coût</a>
          <a href="${BASE}economies/">Calculateur d'économies</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Ressources<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}ressources/blog/">Blog</a>
          <a href="${BASE}ressources/faq/">Questions fréquentes</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">À propos<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}a-propos/">L'entreprise</a>
          <a href="${BASE}a-propos/brevet/">Le brevet Polistibrick</a>
          <a href="${BASE}a-propos/certifications/">Certifications</a>
          <a href="${BASE}a-propos/usines/">Nos usines</a>
          <a href="${BASE}a-propos/fondateur/">L'équipe</a>
        </div>
      </div>
      <div class="nav-drawer-cta">
        <a href="${BASE}contact/" class="btn btn-ghost">Contact</a>
        <a href="${BASE}devis/" class="btn btn-primary">Demander un devis</a>
      </div>
    </aside>
  `;

  const FOOTER_HTML = `
    <div class="container container--wide">
      <div class="footer-grid">
        <div>
          <a href="${BASE}" class="footer-logo">
            <img src="${BASE}images/logo.png" alt="Polistibrick" style="height:32px;">
          </a>
          <p class="footer-brand-tagline">Le système ICF breveté pour maisons passives haut de gamme, sans factures d'énergie. Fabriqué dans l'UE.</p>
        </div>
        <div class="footer-col">
          <h5>Produits</h5>
          <ul>
            <li><a href="${BASE}produits/murs-mbk/">Murs MBK</a></li>
            <li><a href="${BASE}produits/planchers-pbk/">Planchers PBK</a></li>
            <li><a href="${BASE}produits/toit-tbk/">Toit TBK</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Solutions</h5>
          <ul>
            <li><a href="${BASE}pour/proprietaires/">Propriétaires</a></li>
            <li><a href="${BASE}pour/architectes/">Architectes</a></li>
            <li><a href="${BASE}pour/constructeurs/">Constructeurs</a></li>
            <li><a href="${BASE}pour/investisseurs/">Investisseurs</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Ressources</h5>
          <ul>
            <li><a href="${BASE}projets/">Projets réalisés</a></li>
            <li><a href="${BASE}ressources/blog/">Blog</a></li>
            <li><a href="${BASE}ressources/faq/">Questions fréquentes</a></li>
            <li><a href="${BASE}calculateur/">Calculateur de coût</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Entreprise</h5>
          <ul>
            <li><a href="${BASE}a-propos/">À propos</a></li>
            <li><a href="${BASE}a-propos/brevet/">Le brevet Polistibrick</a></li>
            <li><a href="${BASE}a-propos/certifications/">Certifications</a></li>
            <li><a href="${BASE}a-propos/usines/">Nos usines</a></li>
            <li><a href="${BASE}contact/">Contact</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Polistibrick. Tous droits réservés. Système breveté.</span>
        <div class="footer-bottom-links">
          <a href="${BASE}legal/mentions-legales/">Mentions légales</a>
          <a href="${BASE}legal/conditions/">Conditions</a>
          <a href="${BASE}legal/confidentialite/">Confidentialité</a>
          <a href="${BASE}legal/cookies/">Cookies</a>
          <a href="${BASE}legal/durabilite/">Développement durable</a>
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

    // Mobile floating contact bar (call + email) — all pages
    if (!document.querySelector('.mobile-contact-bar')) {
      const bar = document.createElement('div');
      bar.className = 'mobile-contact-bar';
      bar.setAttribute('aria-label', 'Contact rapide');
      bar.innerHTML =
        '<a href="tel:+33161304009" class="mcb-btn mcb-call" aria-label="Appeler Polistibrick">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>' +
          '<span>Appeler</span>' +
        '</a>' +
        '<a href="mailto:contact@polistibrick.fr" class="mcb-btn mcb-email" aria-label="Envoyer un email">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg>' +
          '<span>E-mail</span>' +
        '</a>';
      document.body.appendChild(bar);
    }

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

  // Country switcher (in shared nav) — toggle + mark active + rewrite for preview
  function countrySwitcherShared() {
    // Detect preview mode (github.io / localhost) vs production (real domain)
    const isPreview = location.hostname.includes('github.io') || location.hostname === 'localhost' || location.hostname.startsWith('127.');
    // Find current folder in path (e.g. /polistibrick-multisite/fr/... or /fr/...)
    const pathParts = location.pathname.split('/').filter(p => p);
    const folders = ['ro','fr','it','es','nl','ie','en','de'];
    const currentFolderIdx = pathParts.findIndex(p => folders.includes(p));
    const currentFolder = currentFolderIdx >= 0 ? pathParts[currentFolderIdx] : null;
    // Folder → switcher key map (which item gets .active)
    const folderToKey = { ro: 'ro', fr: 'fr', it: 'it', es: 'es', nl: 'be', de: 'ch', en: 'uk', ie: 'ie' };
    const currentKey = folderToKey[currentFolder];

    function rewriteUrl(folder, fullDomain) {
      if (!isPreview) return fullDomain;  // production → real domain
      // preview → swap current folder with target folder in current path
      if (currentFolderIdx >= 0) {
        const newParts = pathParts.slice();
        newParts[currentFolderIdx] = folder;
        // Preserve trailing slash if present, keep rest of path so user stays on same page
        return '/' + newParts.join('/') + (location.pathname.endsWith('/') ? '/' : '');
      }
      // fallback: go to country root
      return '/' + folder + '/';
    }

    document.querySelectorAll('[data-country-switcher]').forEach(switcher => {
      const trigger = switcher.querySelector('.country-switcher-trigger');
      const panel = switcher.querySelector('.country-switcher-panel');
      if (!trigger || !panel) return;

      // Mark active country + rewrite hrefs for preview vs production
      panel.querySelectorAll('.country-switcher-item').forEach(item => {
        if (currentKey && item.dataset.country === currentKey) item.classList.add('active');
        const folder = item.dataset.folder || item.dataset.country;
        const domain = item.dataset.domain || item.getAttribute('href');
        item.href = rewriteUrl(folder, domain);
      });

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
    if (localStorage.getItem('pb_cookie_consent') !== 'accepted') return null;
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
    modal.setAttribute('aria-label', 'Choisissez votre pays');
    modal.innerHTML = `
      <div class="country-picker-backdrop"></div>
      <div class="country-picker-panel">
        <button class="country-picker-close" aria-label="Fermer">×</button>
        <div class="country-picker-header">
          <span class="country-picker-eyebrow">🌍 Choisissez votre pays</span>
          <h2 class="country-picker-title">Dans quel pays <em>construisez-vous ?</em></h2>
          <p class="country-picker-sub">Nous vous redirigeons vers le site de votre pays avec l'équipe locale, un contact direct et un devis dans votre langue.</p>
        </div>
        <div class="country-picker-grid">
          ${Object.entries(POLISTIBRICK_COUNTRIES).map(([code, c]) => `
            <a href="${c.url}" class="country-picker-item ${code === detectedCountry ? 'is-detected' : ''}" data-country="${code}" target="_blank" rel="noopener">
              <span class="country-picker-flag">${c.flag}</span>
              <span class="country-picker-name">${c.name}</span>
              ${code === detectedCountry ? '<span class="country-picker-tag">★ Votre pays</span>' : ''}
            </a>
          `).join('')}
        </div>
        <p class="country-picker-foot">Votre pays n'est pas listé ? Écrivez-nous à <a href="mailto:info@polistibrick.eu">info@polistibrick.eu</a></p>
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

  // Hamburger drawer + accordion (style ZURU) pour la nav partagée
  function navDrawerShared() {
    const toggle = document.querySelector('.nav-toggle');
    const drawer = document.getElementById('navDrawerShared');
    const overlay = document.querySelector('[data-nav-overlay]');
    if (!toggle || !drawer) return;
    function setOpen(open) {
      drawer.classList.toggle('open', open);
      if (overlay) overlay.classList.toggle('open', open);
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      drawer.setAttribute('aria-hidden', String(!open));
    }
    toggle.addEventListener('click', () => setOpen(!drawer.classList.contains('open')));
    if (overlay) overlay.addEventListener('click', () => setOpen(false));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
    drawer.querySelectorAll('.nav-drawer-title').forEach(btn => {
      btn.addEventListener('click', () => {
        const g = btn.closest('.nav-drawer-group');
        const willOpen = !g.classList.contains('open');
        drawer.querySelectorAll('.nav-drawer-group.open').forEach(o => {
          if (o !== g) { o.classList.remove('open'); const b = o.querySelector('.nav-drawer-title'); if (b) b.setAttribute('aria-expanded', 'false'); }
        });
        g.classList.toggle('open', willOpen);
        btn.setAttribute('aria-expanded', String(willOpen));
      });
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    inject();
    navShadow();
    countrySwitcherShared();
    navDrawerShared();
    reveal();
    gallery();
    wireCountryPickerButtons();

    var cs = document.createElement('script');
    cs.src = BASE + 'assets/js/cookies.js';
    cs.defer = true;
    document.head.appendChild(cs);

    function runGeoIfAllowed() {
      if (localStorage.getItem('pb_cookie_consent') !== 'accepted') return;
      const idle = window.requestIdleCallback || ((cb) => setTimeout(cb, 2500));
      idle(() => {
        detectUserCountry().then((code) => { detectedCountry = code; });
      });
    }
    runGeoIfAllowed();
    window.addEventListener('pb-cookie-consent', (e) => {
      if (e.detail && e.detail.level === 'accepted') runGeoIfAllowed();
    });
  });
})();
