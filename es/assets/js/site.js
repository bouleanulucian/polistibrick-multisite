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
      <a href="${BASE}" class="nav-logo" aria-label="Polistibrick — inicio">
        <img src="${BASE}images/logo.png" alt="Polistibrick" loading="eager">
      </a>
      <nav class="nav-menu" aria-label="Navegación principal">
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Productos
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}produse/pereti-mbk/">Muros MBK<span class="nav-dropdown-item-sub">Encofrado aislante para muros portantes</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/planseu-pbk/">Forjados PBK<span class="nav-dropdown-item-sub">Paneles prefabricados con desfase 10,8 h</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/acoperis-tbk/">Tejado TBK<span class="nav-dropdown-item-sub">Sistema Passivhaus de fábrica</span></a>
            <a class="nav-dropdown-item" href="${BASE}produse/accesorii/">Accesorios<span class="nav-dropdown-item-sub">Esquineros, terminales, escaleras, ventanas</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Soluciones
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}pentru/proprietari/">Para propietarios<span class="nav-dropdown-item-sub">Casa pasiva sin facturas altas</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/arhitecti/">Para arquitectos<span class="nav-dropdown-item-sub">Detalles constructivos, BIM, fichas</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/constructori/">Para constructores<span class="nav-dropdown-item-sub">Montaje, certificación, asociación</span></a>
            <a class="nav-dropdown-item" href="${BASE}pentru/investitori/">Para inversores<span class="nav-dropdown-item-sub">ROI, velocidad de ejecución, conjuntos</span></a>
            <a class="nav-dropdown-item" href="${BASE}devino-partener/" style="color:var(--red);font-weight:600;">→ Hazte socio<span class="nav-dropdown-item-sub" style="color:rgba(200,16,46,0.7);">Solicitud para constructores certificados</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Proyectos
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}proiecte/">Casas construidas<span class="nav-dropdown-item-sub">Galería + mapa de proyectos</span></a>
            <a class="nav-dropdown-item" href="${BASE}testimoniale/">Testimonios (vídeo)<span class="nav-dropdown-item-sub">Los propietarios hablan, con cifras reales</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Calculadora
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}calculator/">Calculadora de costes<span class="nav-dropdown-item-sub">Estima el precio de los paneles de tu casa</span></a>
            <a class="nav-dropdown-item" href="${BASE}economii/">Calculadora de ahorros<span class="nav-dropdown-item-sub">Polistibrick vs ladrillo en 25 años</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Recursos
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}comparatie/">Comparación<span class="nav-dropdown-item-sub">Polistibrick vs sistema clásico vs otro ICF</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/blog/">Blog<span class="nav-dropdown-item-sub">Artículos sobre Casa Pasiva, ICF</span></a>
            <a class="nav-dropdown-item" href="${BASE}resurse/faq/">Preguntas frecuentes<span class="nav-dropdown-item-sub">Respuestas a las preguntas más habituales</span></a>
          </div>
        </div>
        <div class="nav-item">
          <button class="nav-link" aria-haspopup="true" aria-expanded="false">
            Sobre nosotros
            <svg class="nav-link-caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 5l3 3 3-3"/></svg>
          </button>
          <div class="nav-dropdown">
            <a class="nav-dropdown-item" href="${BASE}despre/">La empresa<span class="nav-dropdown-item-sub">Quiénes somos, visión, misión</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/patent/">La patente Polistibrick<span class="nav-dropdown-item-sub">La patente que nos hace únicos</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/certificari/">Certificaciones<span class="nav-dropdown-item-sub">CE, ISO, Passivhaus, aprobaciones técnicas</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/fabrici/">Nuestras fábricas<span class="nav-dropdown-item-sub">Valencia (ES) y Craiova (RO)</span></a>
            <a class="nav-dropdown-item" href="${BASE}despre/echipa/">El equipo<span class="nav-dropdown-item-sub">Fundadores y nuestro equipo</span></a>
          </div>
        </div>
      </nav>
      <div class="nav-cta">
        <div class="country-switcher" data-country-switcher>
          <button class="country-switcher-trigger" type="button" aria-label="Elige tu país" aria-expanded="false">
            <span class="country-switcher-flag">🇪🇸</span>
            <span class="country-switcher-code">ES</span>
            <svg class="country-switcher-caret" viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="3,5 6,8 9,5"/></svg>
          </button>
          <div class="country-switcher-panel" role="menu" aria-hidden="true">
            <div class="country-switcher-header">🌍 Elige tu país</div>
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
        <a href="${BASE}contact/" class="btn btn-ghost">Contacto</a>
        <a href="${BASE}oferta/" class="btn btn-primary btn-arrow">Pedir presupuesto</a>
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
          <p class="footer-brand-tagline">El sistema ICF patentado para casas pasivas premium, sin facturas de energía. Fabricado en la UE.</p>
        </div>
        <div class="footer-col">
          <h5>Productos</h5>
          <ul>
            <li><a href="${BASE}produse/pereti-mbk/">Muros MBK</a></li>
            <li><a href="${BASE}produse/planseu-pbk/">Forjados PBK</a></li>
            <li><a href="${BASE}produse/acoperis-tbk/">Tejado TBK</a></li>
            <li><a href="${BASE}produse/accesorii/">Accesorios</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Soluciones</h5>
          <ul>
            <li><a href="${BASE}pentru/proprietari/">Propietarios</a></li>
            <li><a href="${BASE}pentru/arhitecti/">Arquitectos</a></li>
            <li><a href="${BASE}pentru/constructori/">Constructores</a></li>
            <li><a href="${BASE}pentru/investitori/">Inversores</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Recursos</h5>
          <ul>
            <li><a href="${BASE}proiecte/">Proyectos realizados</a></li>
            <li><a href="${BASE}resurse/blog/">Blog</a></li>
            <li><a href="${BASE}resurse/faq/">Preguntas frecuentes</a></li>
            <li><a href="${BASE}calculator/">Calculadora de costes</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Empresa</h5>
          <ul>
            <li><a href="${BASE}despre/">Sobre nosotros</a></li>
            <li><a href="${BASE}despre/patent/">La patente Polistibrick</a></li>
            <li><a href="${BASE}despre/certificari/">Certificaciones</a></li>
            <li><a href="${BASE}despre/fabrici/">Nuestras fábricas</a></li>
            <li><a href="${BASE}contact/">Contacto</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Polistibrick. Todos los derechos reservados. Sistema patentado.</span>
        <div class="footer-bottom-links">
          <a href="${BASE}legal/termeni/">Términos</a>
          <a href="${BASE}legal/confidentialitate/">Privacidad</a>
          <a href="${BASE}legal/cookies/">Cookies</a>
          <a href="${BASE}legal/sustenabilitate/">Sostenibilidad</a>
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
    modal.setAttribute('aria-label', 'Elige tu país');
    modal.innerHTML = `
      <div class="country-picker-backdrop"></div>
      <div class="country-picker-panel">
        <button class="country-picker-close" aria-label="Cerrar">×</button>
        <div class="country-picker-header">
          <span class="country-picker-eyebrow">🌍 Elige tu país</span>
          <h2 class="country-picker-title">¿En qué país <em>estás construyendo?</em></h2>
          <p class="country-picker-sub">Te redirigimos al sitio de tu país con el equipo local, contacto directo y presupuesto en tu idioma.</p>
        </div>
        <div class="country-picker-grid">
          ${Object.entries(POLISTIBRICK_COUNTRIES).map(([code, c]) => `
            <a href="${c.url}" class="country-picker-item ${code === detectedCountry ? 'is-detected' : ''}" data-country="${code}" target="_blank" rel="noopener">
              <span class="country-picker-flag">${c.flag}</span>
              <span class="country-picker-name">${c.name}</span>
              ${code === detectedCountry ? '<span class="country-picker-tag">★ Tu país</span>' : ''}
            </a>
          `).join('')}
        </div>
        <p class="country-picker-foot">¿Tu país no está en la lista? Escríbenos a <a href="mailto:info@polistibrick.eu">info@polistibrick.eu</a></p>
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
