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
      <a href="${BASE}" class="nav-logo" aria-label="{{ui.home_aria}}">
        <img src="${BASE}images/logo.png" alt="Polistibrick" loading="eager">
      </a>
      <nav class="nav-menu" aria-label="{{ui.nav_aria}}">
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            {{ui.produse}}
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}produse/pereti-mbk/">{{ui.pereti_mbk}}<span class="nav-dropdown-item-sub">{{ui.pereti_mbk_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/planseu-pbk/">{{ui.planseu_pbk}}<span class="nav-dropdown-item-sub">{{ui.planseu_pbk_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/acoperis-tbk/">{{ui.acoperis_tbk}}<span class="nav-dropdown-item-sub">{{ui.acoperis_tbk_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/accesorii/">{{ui.accesorii}}<span class="nav-dropdown-item-sub">{{ui.accesorii_sub}}</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            {{ui.solutii}}
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}pentru/proprietari/">{{ui.pentru_proprietari}}<span class="nav-dropdown-item-sub">{{ui.pentru_proprietari_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/arhitecti/">{{ui.pentru_arhitecti}}<span class="nav-dropdown-item-sub">{{ui.pentru_arhitecti_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/constructori/">{{ui.pentru_constructori}}<span class="nav-dropdown-item-sub">{{ui.pentru_constructori_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/investitori/">{{ui.pentru_investitori}}<span class="nav-dropdown-item-sub">{{ui.pentru_investitori_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}devino-partener/" style="color:var(--red);font-weight:600;">{{ui.devino_partener}}<span class="nav-dropdown-item-sub" style="color:rgba(200,16,46,0.7);">{{ui.devino_partener_sub}}</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            {{ui.proiecte}}
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}proiecte/">{{ui.case_construite}}<span class="nav-dropdown-item-sub">{{ui.case_construite_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}testimoniale/">{{ui.testimoniale}}<span class="nav-dropdown-item-sub">{{ui.testimoniale_sub}}</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            {{ui.calculator}}
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}calculator/">{{ui.calc_cost}}<span class="nav-dropdown-item-sub">{{ui.calc_cost_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}economii/">{{ui.calc_econ}}<span class="nav-dropdown-item-sub">{{ui.calc_econ_sub}}</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            {{ui.resurse}}
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}comparatie/">{{ui.comparaison}}<span class="nav-dropdown-item-sub">{{ui.comparaison_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/blog/">{{ui.blog}}<span class="nav-dropdown-item-sub">{{ui.blog_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/faq/">{{ui.faq}}<span class="nav-dropdown-item-sub">{{ui.faq_sub}}</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            {{ui.despre}}
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}despre/">{{ui.compania}}<span class="nav-dropdown-item-sub">{{ui.compania_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/patent/">{{ui.patent}}<span class="nav-dropdown-item-sub">{{ui.patent_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/certificari/">{{ui.certificari}}<span class="nav-dropdown-item-sub">{{ui.certificari_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/fabrici/">{{ui.fabrici}}<span class="nav-dropdown-item-sub">{{ui.fabrici_sub}}</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/echipa/">{{ui.echipa}}<span class="nav-dropdown-item-sub">{{ui.echipa_sub}}</span></a>
          </div>
        </div>
      </nav>
      <div class="nav-cta">
        <!-- COUNTRY SWITCHER — identique à celui du homepage -->
        <div class="country-switcher" data-country-switcher>
          <button class="country-switcher-trigger" type="button" aria-label="{{ui.cp_label}}" aria-expanded="false">
            <span class="country-switcher-flag">{{country_flag}}</span>
            <span class="country-switcher-code">{{country}}</span>
            <svg class="country-switcher-caret" viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="3,5 6,8 9,5"/></svg>
          </button>
          <div class="country-switcher-panel" role="menu" aria-hidden="true">
            <div class="country-switcher-header">{{ui.cp_eyebrow}}</div>
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
        <a href="${BASE}contact/" class="btn btn-ghost">{{ui.contact}}</a>
        <a href="${BASE}oferta/" class="btn btn-primary btn-arrow">{{ui.cere_oferta}}</a>
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
          <p class="footer-brand-tagline">{{ui.footer_tagline}}</p>
        </div>
        <div class="footer-col">
          <h5>{{ui.footer_h_produse}}</h5>
          <ul>
            <li><a href="${BASE}produse/pereti-mbk/">{{ui.pereti_mbk}}</a></li>
            <li><a href="${BASE}produse/planseu-pbk/">{{ui.planseu_pbk}}</a></li>
            <li><a href="${BASE}produse/acoperis-tbk/">{{ui.acoperis_tbk}}</a></li>
            <li><a href="${BASE}produse/accesorii/">{{ui.accesorii}}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>{{ui.footer_h_solutii}}</h5>
          <ul>
            <li><a href="${BASE}pentru/proprietari/">{{ui.footer_proprietari}}</a></li>
            <li><a href="${BASE}pentru/arhitecti/">{{ui.footer_arhitecti}}</a></li>
            <li><a href="${BASE}pentru/constructori/">{{ui.footer_constructori}}</a></li>
            <li><a href="${BASE}pentru/investitori/">{{ui.footer_investitori}}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>{{ui.footer_h_resurse}}</h5>
          <ul>
            <li><a href="${BASE}proiecte/">{{ui.footer_proiecte_realizate}}</a></li>
            <li><a href="${BASE}resurse/blog/">{{ui.blog}}</a></li>
            <li><a href="${BASE}resurse/faq/">{{ui.faq}}</a></li>
            <li><a href="${BASE}calculator/">{{ui.calc_cost}}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>{{ui.footer_h_companie}}</h5>
          <ul>
            <li><a href="${BASE}despre/">{{ui.footer_despre_noi}}</a></li>
            <li><a href="${BASE}despre/patent/">{{ui.patent}}</a></li>
            <li><a href="${BASE}despre/certificari/">{{ui.certificari}}</a></li>
            <li><a href="${BASE}despre/fabrici/">{{ui.fabrici}}</a></li>
            <li><a href="${BASE}contact/">{{ui.contact}}</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>{{ui.footer_copyright}}</span>
        <div class="footer-bottom-links">
          <a href="${BASE}legal/termeni/">{{ui.footer_termeni}}</a>
          <a href="${BASE}legal/confidentialitate/">{{ui.footer_confidentialitate}}</a>
          <a href="${BASE}legal/cookies/">{{ui.footer_cookies}}</a>
          <a href="${BASE}legal/sustenabilitate/">{{ui.footer_sustenabilitate}}</a>
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
    modal.setAttribute('aria-label', '{{ui.cp_label}}');
    modal.innerHTML = `
      <div class="country-picker-backdrop"></div>
      <div class="country-picker-panel">
        <button class="country-picker-close" aria-label="{{ui.cp_close}}">×</button>
        <div class="country-picker-header">
          <span class="country-picker-eyebrow">{{ui.cp_eyebrow}}</span>
          <h2 class="country-picker-title">{{ui.cp_title}} <em>{{ui.cp_title_em}}</em></h2>
          <p class="country-picker-sub">{{ui.cp_sub}}</p>
        </div>
        <div class="country-picker-grid">
          ${Object.entries(POLISTIBRICK_COUNTRIES).map(([code, c]) => `
            <a href="${c.url}" class="country-picker-item ${code === detectedCountry ? 'is-detected' : ''}" data-country="${code}" target="_blank" rel="noopener">
              <span class="country-picker-flag">${c.flag}</span>
              <span class="country-picker-name">${c.name}</span>
              ${code === detectedCountry ? '<span class="country-picker-tag">{{ui.cp_your_country}}</span>' : ''}
            </a>
          `).join('')}
        </div>
        <p class="country-picker-foot">{{ui.cp_foot}} <a href="mailto:info@polistibrick.eu">info@polistibrick.eu</a></p>
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
