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
      <a href="${BASE}" class="nav-logo" aria-label="Polistibrick — Startseite">
        <img src="${BASE}images/logo.png" alt="Polistibrick" loading="eager">
      </a>
      <nav class="nav-menu" aria-label="Hauptnavigation">
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Produkte
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}produse/pereti-mbk/">MBK-Wände<span class="nav-dropdown-item-sub">Wärmedämmschalung für tragende Wände</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/planseu-pbk/">PBK-Decken<span class="nav-dropdown-item-sub">Fertigplatten mit Phasenverschiebung 10,8 h</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/acoperis-tbk/">TBK-Dach<span class="nav-dropdown-item-sub">Passivhaus-System aus dem Werk</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/accesorii/">Zubehör<span class="nav-dropdown-item-sub">Ecken, Abschlüsse, Treppen, Fenster</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Lösungen
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}pentru/proprietari/">Für Eigentümer<span class="nav-dropdown-item-sub">Passivhaus ohne hohe Rechnungen</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/arhitecti/">Für Architekten<span class="nav-dropdown-item-sub">Konstruktive Details, BIM, Datenblätter</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/constructori/">Für Bauunternehmen<span class="nav-dropdown-item-sub">Montage, Zertifizierung, Partnerschaft</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/investitori/">Für Investoren<span class="nav-dropdown-item-sub">ROI, Ausführungstempo, Wohnanlagen</span></a>
            <a class="nav-dropdown-item" href="${BASE}devino-partener/" style="color:var(--red);font-weight:600;">→ Partner werden<span class="nav-dropdown-item-sub" style="color:rgba(200,16,46,0.7);">Bewerbung zertifizierte Bauunternehmen</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Projekte
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}proiecte/">Realisierte Häuser<span class="nav-dropdown-item-sub">Galerie + Karte mit Projekten</span></a>
            <a class="nav-dropdown-item" href="${BASE}testimoniale/">Erfahrungsberichte (Video)<span class="nav-dropdown-item-sub">Eigentümer sprechen, mit echten Zahlen</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Rechner
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}calculator/">Kostenrechner<span class="nav-dropdown-item-sub">Schätzen Sie den Paneelpreis für Ihr Haus</span></a>
            <a class="nav-dropdown-item" href="${BASE}economii/">Einsparrechner<span class="nav-dropdown-item-sub">Polistibrick vs. Ziegel über 25 Jahre</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Ressourcen
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}comparatie/">Vergleich<span class="nav-dropdown-item-sub">Polistibrick vs. klassisches System vs. anderes ICF</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/blog/">Blog<span class="nav-dropdown-item-sub">Artikel über Passivhaus, ICF</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/faq/">Häufige Fragen<span class="nav-dropdown-item-sub">Antworten auf die häufigsten Fragen</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Über uns
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}despre/">Das Unternehmen<span class="nav-dropdown-item-sub">Wer wir sind, Vision, Mission</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/patent/">Das Polistibrick-Patent<span class="nav-dropdown-item-sub">Das Patent, das uns einzigartig macht</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/certificari/">Zertifizierungen<span class="nav-dropdown-item-sub">CE, ISO, Passivhaus, technische Zulassungen</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/fabrici/">Unsere Werke<span class="nav-dropdown-item-sub">Valencia (ES) und Craiova (RO)</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/echipa/">Das Team<span class="nav-dropdown-item-sub">Gründer und unsere Mitarbeiter</span></a>
          </div>
        </div>
      </nav>
      <div class="nav-cta">
        <!-- COUNTRY SWITCHER — identique à celui du homepage -->
        <div class="country-switcher" data-country-switcher>
          <button class="country-switcher-trigger" type="button" aria-label="Wählen Sie Ihr Land" aria-expanded="false">
            <span class="country-switcher-flag">🇨🇭</span>
            <span class="country-switcher-code">CH</span>
            <svg class="country-switcher-caret" viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="3,5 6,8 9,5"/></svg>
          </button>
          <div class="country-switcher-panel" role="menu" aria-hidden="true">
            <div class="country-switcher-header">🌍 Wählen Sie Ihr Land</div>
            <a href="#" data-country="ro" data-domain="https://polistibrick.ro" data-folder="ro" class="country-switcher-item"><span class="flag">🇷🇴</span><span class="name">România</span><span class="domain">polistibrick.ro</span></a>
            <a href="#" data-country="fr" data-domain="https://polistibrick.fr" data-folder="fr" class="country-switcher-item"><span class="flag">🇫🇷</span><span class="name">France</span><span class="domain">polistibrick.fr</span></a>
            <a href="#" data-country="it" data-domain="https://polistibrick.it" data-folder="it" class="country-switcher-item"><span class="flag">🇮🇹</span><span class="name">Italia</span><span class="domain">polistibrick.it</span></a>
            <a href="#" data-country="es" data-domain="https://polistibrick.es" data-folder="es" class="country-switcher-item"><span class="flag">🇪🇸</span><span class="name">España</span><span class="domain">polistibrick.es</span></a>
            <a href="#" data-country="be" data-domain="https://polistibrick.be" data-folder="nl" class="country-switcher-item"><span class="flag">🇧🇪</span><span class="name">België</span><span class="domain">polistibrick.be</span></a>
            <a href="#" data-country="ie" data-domain="https://polistibrick.ie" data-folder="ie" class="country-switcher-item"><span class="flag">🇮🇪</span><span class="name">Ireland</span><span class="domain">polistibrick.ie</span></a>
            <a href="#" data-country="uk" data-domain="https://polistibrick.uk" data-folder="en" class="country-switcher-item"><span class="flag">🇬🇧</span><span class="name">United Kingdom</span><span class="domain">polistibrick.uk</span></a>
            <a href="#" data-country="ch" data-domain="https://polistibrick.com" data-folder="de" class="country-switcher-item"><span class="flag">🇨🇭</span><span class="name">Schweiz</span><span class="domain">polistibrick.com</span></a>
          </div>
        </div>
        <a href="${BASE}contact/" class="btn btn-ghost">Kontakt</a>
        <a href="${BASE}oferta/" class="btn btn-primary btn-arrow">Angebot anfordern</a>
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
          <p class="footer-brand-tagline">Das patentierte ICF-System für Premium-Passivhäuser ohne Energierechnungen. Hergestellt in der EU.</p>
        </div>
        <div class="footer-col">
          <h5>Produkte</h5>
          <ul>
            <li><a href="${BASE}produse/pereti-mbk/">MBK-Wände</a></li>
            <li><a href="${BASE}produse/planseu-pbk/">PBK-Decken</a></li>
            <li><a href="${BASE}produse/acoperis-tbk/">TBK-Dach</a></li>
            <li><a href="${BASE}produse/accesorii/">Zubehör</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Lösungen</h5>
          <ul>
            <li><a href="${BASE}pentru/proprietari/">Eigentümer</a></li>
            <li><a href="${BASE}pentru/arhitecti/">Architekten</a></li>
            <li><a href="${BASE}pentru/constructori/">Bauunternehmen</a></li>
            <li><a href="${BASE}pentru/investitori/">Investoren</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Ressourcen</h5>
          <ul>
            <li><a href="${BASE}proiecte/">Realisierte Projekte</a></li>
            <li><a href="${BASE}resurse/blog/">Blog</a></li>
            <li><a href="${BASE}resurse/faq/">Häufige Fragen</a></li>
            <li><a href="${BASE}calculator/">Kostenrechner</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Unternehmen</h5>
          <ul>
            <li><a href="${BASE}despre/">Über uns</a></li>
            <li><a href="${BASE}despre/patent/">Das Polistibrick-Patent</a></li>
            <li><a href="${BASE}despre/certificari/">Zertifizierungen</a></li>
            <li><a href="${BASE}despre/fabrici/">Unsere Werke</a></li>
            <li><a href="${BASE}contact/">Kontakt</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Polistibrick. Alle Rechte vorbehalten. Patentiertes System.</span>
        <div class="footer-bottom-links">
          <a href="${BASE}legal/termeni/">Bedingungen</a>
          <a href="${BASE}legal/confidentialitate/">Datenschutz</a>
          <a href="${BASE}legal/cookies/">Cookies</a>
          <a href="${BASE}legal/sustenabilitate/">Nachhaltigkeit</a>
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
    modal.setAttribute('aria-label', 'Wählen Sie Ihr Land');
    modal.innerHTML = `
      <div class="country-picker-backdrop"></div>
      <div class="country-picker-panel">
        <button class="country-picker-close" aria-label="Schließen">×</button>
        <div class="country-picker-header">
          <span class="country-picker-eyebrow">🌍 Wählen Sie Ihr Land</span>
          <h2 class="country-picker-title">In welchem Land <em>bauen Sie?</em></h2>
          <p class="country-picker-sub">Wir leiten Sie auf die Seite Ihres Landes weiter — mit lokalem Team, direktem Kontakt und einem Angebot in Ihrer Sprache.</p>
        </div>
        <div class="country-picker-grid">
          ${Object.entries(POLISTIBRICK_COUNTRIES).map(([code, c]) => `
            <a href="${c.url}" class="country-picker-item ${code === detectedCountry ? 'is-detected' : ''}" data-country="${code}" target="_blank" rel="noopener">
              <span class="country-picker-flag">${c.flag}</span>
              <span class="country-picker-name">${c.name}</span>
              ${code === detectedCountry ? '<span class="country-picker-tag">★ Ihr Land</span>' : ''}
            </a>
          `).join('')}
        </div>
        <p class="country-picker-foot">Ihr Land ist nicht aufgeführt? Schreiben Sie uns an <a href="mailto:info@polistibrick.eu">info@polistibrick.eu</a></p>
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
