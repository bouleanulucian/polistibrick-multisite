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
    const countryFolders = ['ro', 'fr', 'it', 'es', 'nl', 'ie', 'en', 'de', 'me'];
    const countryIdx = parts.findIndex(function (p) { return countryFolders.includes(p); });

    // GitHub Pages preview: /user/repo/ro/presupuesto/ → depth from country folder
    if (location.hostname.includes('github.io') && countryIdx >= 0) {
      var depth = parts.length - countryIdx - 1;
      return depth <= 0 ? '' : '../'.repeat(depth);
    }

    var depth = (window.location.pathname.replace(/\/$/, '').match(/\//g) || []).length;
    return depth <= 1 ? '' : '../'.repeat(depth - 1);
  })();

  // Pe github.io media e o dată la /REPO/images/ (user e în hostname, nu în path)
  const IMG = (function () {
    if (!location.hostname.includes('github.io')) return BASE;
    const parts = location.pathname.split('/').filter(Boolean);
    if (parts.length < 1) return BASE;
    return '/' + parts[0] + '/';
  })();

  const NAV_HTML = `
    <div class="nav-inner">
      <a href="${BASE}" class="logo nav-logo" aria-label="Polistibrick — inicio">
        <img src="${IMG}images/logo.png" alt="Polistibrick" class="logo-img" loading="eager">
      </a>
      <div class="nav-cta">
        <!-- COUNTRY SWITCHER -->
        <div class="country-switcher" data-country-switcher>
          <button class="country-switcher-trigger" type="button" aria-label="Elige tu país" aria-expanded="false">
            <span class="country-switcher-flag">🇪🇸</span>
            <span class="country-switcher-code">ES</span>
            <svg class="country-switcher-caret" viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="3,5 6,8 9,5"/></svg>
          </button>
          <div class="country-switcher-panel" role="menu" aria-hidden="true">
            <div class="country-switcher-header">🌍 Elige tu país</div>
            <a href="#" data-country="ro" data-domain="https://polistibrick.ro" data-folder="ro" class="country-switcher-item"><span class="flag">🇷🇴</span><span class="name">România</span><span class="domain">polistibrick.ro</span></a>
            <a href="#" data-country="fr" data-domain="https://polistibrick.fr" data-folder="fr" class="country-switcher-item"><span class="flag">🇫🇷</span><span class="name">Francia</span><span class="domain">polistibrick.fr</span></a>
            <a href="#" data-country="it" data-domain="https://polistibrick.it" data-folder="it" class="country-switcher-item"><span class="flag">🇮🇹</span><span class="name">Italia</span><span class="domain">polistibrick.it</span></a>
            <a href="#" data-country="es" data-domain="https://polistibrick.es" data-folder="es" class="country-switcher-item"><span class="flag">🇪🇸</span><span class="name">España</span><span class="domain">polistibrick.es</span></a>
            <a href="#" data-country="be" data-domain="https://polistibrick.be" data-folder="nl" class="country-switcher-item"><span class="flag">🇧🇪</span><span class="name">Bélgica</span><span class="domain">polistibrick.be</span></a>
            <a href="#" data-country="ie" data-domain="https://polistibrick.ie" data-folder="ie" class="country-switcher-item"><span class="flag">🇮🇪</span><span class="name">Irlanda</span><span class="domain">polistibrick.ie</span></a>
            <a href="#" data-country="uk" data-domain="https://polistibrick.uk" data-folder="en" class="country-switcher-item"><span class="flag">🇬🇧</span><span class="name">Reino Unido</span><span class="domain">polistibrick.uk</span></a>
            <a href="#" data-country="ch" data-domain="https://polistibrick.com" data-folder="de" class="country-switcher-item"><span class="flag">🇨🇭</span><span class="name">Suiza</span><span class="domain">polistibrick.com</span></a>
            <a href="#" data-country="me" data-domain="https://polistibrick.me" data-folder="me" class="country-switcher-item"><span class="flag">🇲🇪</span><span class="name">Crna Gora</span><span class="domain">polistibrick.me</span></a>
          </div>
        </div>
        <a href="${BASE}presupuesto/" class="btn btn-primary nav-cta-devis">Presupuesto gratis</a>
        <button class="nav-burger nav-toggle" type="button" aria-label="Abrir el menú" aria-expanded="false" aria-controls="navDrawerShared">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <div class="nav-drawer-overlay" data-nav-overlay aria-hidden="true"></div>
    <aside class="nav-drawer" id="navDrawerShared" aria-label="Menú de navegación" aria-hidden="true">
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Productos<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}productos/polistibrick/">Polistibrick</a>
          <a href="${BASE}productos/polistiwall/">Polistiwall</a>
          <a href="${BASE}productos/polistisip/">PolistiSIP</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Soluciones<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}para/propietarios/">Para propietarios</a>
          <a href="${BASE}para/arquitectos/">Para arquitectos</a>
          <a href="${BASE}para/constructores/">Para constructores</a>
          <a href="${BASE}para/inversores/">Para inversores</a>
          <a href="${BASE}ser-socio/" class="partner-link">→ Hazte socio</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Proyectos<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}proyectos/">Todos los proyectos</a>
          <a href="${BASE}testimonios/">Testimonios (vídeo)</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Recursos<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}recursos/faq/">Preguntas frecuentes</a>
          <a href="${BASE}ahorros/">Calculadora de ahorros</a>
        </div>
      </div>
      <div class="nav-drawer-group">
        <button class="nav-drawer-title" aria-expanded="false">Sobre nosotros<span class="nd-caret">▾</span></button>
        <div class="nav-acc">
          <a href="${BASE}sobre-nosotros/">La empresa</a>
          <a href="${BASE}sobre-nosotros/patente/">La patente Polistibrick</a>
          <a href="${BASE}sobre-nosotros/certificaciones/">Certificaciones</a>
          <a href="${BASE}sobre-nosotros/fabricas/">Nuestras fábricas</a>
          <a href="${BASE}sobre-nosotros/fundador/">El equipo</a>
        </div>
      </div>
      <div class="nav-drawer-cta">
        <a href="${BASE}contact/" class="btn btn-ghost">Contacto</a>
        <a href="${BASE}presupuesto/" class="btn btn-primary">Pedir presupuesto</a>
      </div>
    </aside>
  `;

  const FOOTER_HTML = `
    <div class="container container--wide">
      <div class="footer-grid">
        <div>
          <a href="${BASE}" class="footer-logo">
            <img src="${IMG}images/logo.png" alt="Polistibrick" style="height:32px;">
          </a>
          <p class="footer-brand-tagline">El sistema ICF patentado para casas pasivas premium, sin facturas de energía. Fabricado en la UE.</p>
        </div>
        <div class="footer-col">
          <h5>Productos</h5>
          <ul>
            <li><a href="${BASE}productos/polistibrick/">Polistibrick</a></li>
            <li><a href="${BASE}productos/polistiwall/">Polistiwall</a></li>
            <li><a href="${BASE}productos/polistisip/">PolistiSIP</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Soluciones</h5>
          <ul>
            <li><a href="${BASE}para/propietarios/">Propietarios</a></li>
            <li><a href="${BASE}para/arquitectos/">Arquitectos</a></li>
            <li><a href="${BASE}para/constructores/">Constructores</a></li>
            <li><a href="${BASE}para/inversores/">Inversores</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Recursos</h5>
          <ul>
            <li><a href="${BASE}proyectos/">Proyectos</a></li>
            <li><a href="${BASE}ahorros/">Calculadora de ahorros</a></li>
            <li><a href="${BASE}recursos/faq/">Preguntas frecuentes</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Empresa</h5>
          <ul>
            <li><a href="${BASE}sobre-nosotros/">Sobre nosotros</a></li>
            <li><a href="${BASE}sobre-nosotros/patente/">La patente Polistibrick</a></li>
            <li><a href="${BASE}sobre-nosotros/certificaciones/">Certificaciones</a></li>
            <li><a href="${BASE}sobre-nosotros/fabricas/">Nuestras fábricas</a></li>
            <li><a href="${BASE}contact/">Contacto</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Polistibrick. Todos los derechos reservados. Sistema patentado.</span>
        <div class="footer-bottom-links">
          <a href="${BASE}legal/aviso-legal/">Aviso legal</a>
          <a href="${BASE}legal/condiciones/">Términos</a>
          <a href="${BASE}legal/privacidad/">Privacidad</a>
          <a href="${BASE}legal/cookies/">Cookies</a>
          <a href="${BASE}legal/sostenibilidad/">Sostenibilidad</a>
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
      bar.setAttribute('aria-label', 'Contacto rápido');
      // Hide the Call button when the country has no usable phone number yet
      // (unfilled config leaves "[to fill in]" or an unsubstituted placeholder).
      const phoneRaw = '+34642777216';
      const hasPhone = phoneRaw && phoneRaw.indexOf('[') === -1 && phoneRaw.indexOf('{') === -1;
      bar.innerHTML =
        (hasPhone ?
        '<a href="tel:' + phoneRaw + '" class="mcb-btn mcb-call" aria-label="Llamar a Polistibrick">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>' +
          '<span>Llamar</span>' +
        '</a>' : '') +
        '<a href="#" data-m64="aW5mb0Bwb2xpc3RpYnJpY2suZXM=" class="mcb-btn mcb-email" aria-label="Enviar email">' +
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

/* Carte des slugs traduits — générée depuis translations/path_maps.py.
   Permet au sélecteur de pays d'envoyer sur la page équivalente et non sur un 404. */
window.PB_SLUGS = {"ro":{},"fr":{"produse":"produits","pentru":"pour","despre":"a-propos","resurse":"ressources","proiecte":"projets","economii":"economies","oferta":"devis","comparatie":"comparaison","calculator":"calculateur","testimoniale":"temoignages","devino-partener":"devenir-partenaire","pereti-mbk":"murs-mbk","planseu-pbk":"planchers-pbk","acoperis-tbk":"toit-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"toit-tbk-sip250","accesorii":"accessoires","proprietari":"proprietaires","arhitecti":"architectes","constructori":"constructeurs","investitori":"investisseurs","certificari":"certifications","fabrici":"usines","echipa":"fondateur","patent":"brevet","casa-cluj-napoca":"maison-cluj-napoca","ansamblu-lyon":"ensemble-lyon","confidentialitate":"confidentialite","sustenabilitate":"durabilite","termeni":"conditions","mentiuni-legale":"mentions-legales","montaj":"montage"},"de":{"produse":"produits","pentru":"pour","despre":"a-propos","resurse":"ressources","proiecte":"projets","economii":"economies","oferta":"devis","comparatie":"comparaison","calculator":"calculateur","testimoniale":"temoignages","devino-partener":"devenir-partenaire","pereti-mbk":"murs-mbk","planseu-pbk":"planchers-pbk","acoperis-tbk":"toit-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"toit-tbk-sip250","accesorii":"accessoires","proprietari":"proprietaires","arhitecti":"architectes","constructori":"constructeurs","investitori":"investisseurs","certificari":"certifications","fabrici":"usines","echipa":"fondateur","patent":"brevet","casa-cluj-napoca":"maison-cluj-napoca","ansamblu-lyon":"ensemble-lyon","confidentialitate":"confidentialite","sustenabilitate":"durabilite","termeni":"conditions","mentiuni-legale":"mentions-legales","montaj":"montage"},"nl":{"produse":"produits","pentru":"pour","despre":"a-propos","resurse":"ressources","proiecte":"projets","economii":"economies","oferta":"devis","comparatie":"comparaison","calculator":"calculateur","testimoniale":"temoignages","devino-partener":"devenir-partenaire","pereti-mbk":"murs-mbk","planseu-pbk":"planchers-pbk","acoperis-tbk":"toit-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"toit-tbk-sip250","accesorii":"accessoires","proprietari":"proprietaires","arhitecti":"architectes","constructori":"constructeurs","investitori":"investisseurs","certificari":"certifications","fabrici":"usines","echipa":"fondateur","patent":"brevet","casa-cluj-napoca":"maison-cluj-napoca","ansamblu-lyon":"ensemble-lyon","confidentialitate":"confidentialite","sustenabilitate":"durabilite","termeni":"conditions","mentiuni-legale":"mentions-legales","montaj":"montage"},"en":{"produse":"products","pentru":"for","despre":"about","resurse":"resources","proiecte":"projects","economii":"savings","oferta":"quote","comparatie":"comparison","calculator":"calculator","testimoniale":"testimonials","devino-partener":"become-a-partner","pereti-mbk":"walls-mbk","planseu-pbk":"floors-pbk","acoperis-tbk":"roof-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"roof-tbk-sip250","accesorii":"accessories","proprietari":"homeowners","arhitecti":"architects","constructori":"builders","investitori":"investors","certificari":"certifications","fabrici":"factories","echipa":"founder","patent":"patent","casa-cluj-napoca":"house-cluj-napoca","ansamblu-lyon":"lyon-development","confidentialitate":"privacy","sustenabilitate":"sustainability","termeni":"terms","mentiuni-legale":"legal-notice","montaj":"installation"},"ie":{"produse":"products","pentru":"for","despre":"about","resurse":"resources","proiecte":"projects","economii":"savings","oferta":"quote","comparatie":"comparison","calculator":"calculator","testimoniale":"testimonials","devino-partener":"become-a-partner","pereti-mbk":"walls-mbk","planseu-pbk":"floors-pbk","acoperis-tbk":"roof-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"roof-tbk-sip250","accesorii":"accessories","proprietari":"homeowners","arhitecti":"architects","constructori":"builders","investitori":"investors","certificari":"certifications","fabrici":"factories","echipa":"founder","patent":"patent","casa-cluj-napoca":"house-cluj-napoca","ansamblu-lyon":"lyon-development","confidentialitate":"privacy","sustenabilitate":"sustainability","termeni":"terms","mentiuni-legale":"legal-notice","montaj":"installation"},"es":{"produse":"productos","pentru":"para","despre":"sobre-nosotros","resurse":"recursos","proiecte":"proyectos","economii":"ahorros","oferta":"presupuesto","comparatie":"comparacion","calculator":"calculadora","testimoniale":"testimonios","devino-partener":"ser-socio","pereti-mbk":"muros-mbk","planseu-pbk":"forjados-pbk","acoperis-tbk":"techo-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"techo-tbk-sip250","accesorii":"accesorios","proprietari":"propietarios","arhitecti":"arquitectos","constructori":"constructores","investitori":"inversores","certificari":"certificaciones","fabrici":"fabricas","echipa":"fundador","patent":"patente","casa-cluj-napoca":"casa-cluj-napoca","ansamblu-lyon":"conjunto-lyon","confidentialitate":"privacidad","sustenabilitate":"sostenibilidad","termeni":"condiciones","mentiuni-legale":"aviso-legal","montaj":"montaje","ce-este-casa-passiva":"que-es-una-casa-pasiva"},"it":{"produse":"prodotti","pentru":"per","despre":"chi-siamo","resurse":"risorse","proiecte":"progetti","economii":"risparmi","oferta":"preventivo","comparatie":"confronto","calculator":"calcolatore","testimoniale":"testimonianze","devino-partener":"diventa-partner","pereti-mbk":"pareti-mbk","planseu-pbk":"solai-pbk","acoperis-tbk":"tetto-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"tetto-tbk-sip250","accesorii":"accessori","proprietari":"proprietari","arhitecti":"architetti","constructori":"costruttori","investitori":"investitori","certificari":"certificazioni","fabrici":"fabbriche","echipa":"fondatore","patent":"brevetto","casa-cluj-napoca":"casa-cluj-napoca","ansamblu-lyon":"complesso-lyon","confidentialitate":"privacy","sustenabilitate":"sostenibilita","termeni":"condizioni","mentiuni-legale":"note-legali","montaj":"montaggio","cookies":"cookie"},"me":{"produse":"proizvodi","pentru":"za","despre":"o-nama","resurse":"resursi","proiecte":"projekti","economii":"ustede","oferta":"ponuda","comparatie":"poredjenje","calculator":"kalkulator","testimoniale":"svjedocanstva","devino-partener":"postani-partner","pereti-mbk":"zidovi-mbk","planseu-pbk":"podovi-pbk","acoperis-tbk":"krov-tbk","polistibrick":"polistibrick","polistisip":"polistisip","polistiwall":"polistiwall","acoperis-tbk-sip250":"krov-tbk-sip250","accesorii":"pribor","proprietari":"vlasnici","arhitecti":"arhitekti","constructori":"gradjevinci","investitori":"investitori","certificari":"sertifikati","fabrici":"fabrike","echipa":"osnivac","patent":"patent","casa-cluj-napoca":"kuca-cluj-napoca","ansamblu-lyon":"kompleks-lyon","villa-valencia":"vila-valencia","confidentialitate":"privatnost","sustenabilitate":"odrzivost","termeni":"uslovi","mentiuni-legale":"pravne-napomene","montaj":"montaza","cookies":"kolacici"}};

  // Country switcher (in shared nav) — toggle + mark active + rewrite for preview
  function countrySwitcherShared() {
    // Detect preview mode (github.io / localhost) vs production (real domain)
    const isPreview = location.hostname.includes('github.io') || location.hostname === 'localhost' || location.hostname.startsWith('127.');
    // Find current folder in path (e.g. /polistibrick-multisite/fr/... or /fr/...)
    const pathParts = location.pathname.split('/').filter(p => p);
    const folders = ['ro','fr','it','es','nl','ie','en','de','me'];
    const currentFolderIdx = pathParts.findIndex(p => folders.includes(p));
    const currentFolder = currentFolderIdx >= 0 ? pathParts[currentFolderIdx] : null;
    // Folder → switcher key map (which item gets .active)
    const folderToKey = { ro: 'ro', fr: 'fr', it: 'it', es: 'es', nl: 'be', de: 'ch', en: 'uk', ie: 'ie', me: 'me' };
    const currentKey = folderToKey[currentFolder];

    // Les slugs sont traduits : /ro/presupuesto/ existe en français sous /fr/devis/.
    // Échanger seulement le dossier pays produisait /fr/presupuesto/ — un 404 sur presque
    // toutes les pages intérieures (seuls contact/ et legal/ portent le même nom partout).
    // On traduit donc chaque segment : slug local → slug canonique (roumain) → slug cible.
    function translateSegment(seg, fromFolder, toFolder) {
      const from = (window.PB_SLUGS || {})[fromFolder] || {};
      const to = (window.PB_SLUGS || {})[toFolder] || {};
      // slug local → canonique : la carte est {canonique: local}, on l'inverse
      let canonical = seg;
      for (const key in from) { if (from[key] === seg) { canonical = key; break; } }
      return to[canonical] || canonical;   // canonique → cible (ro = canonique, donc tel quel)
    }

    function rewriteUrl(folder, fullDomain) {
      if (!isPreview) return fullDomain;  // production → real domain
      if (currentFolderIdx >= 0) {
        const newParts = pathParts.slice();
        newParts[currentFolderIdx] = folder;
        for (let i = currentFolderIdx + 1; i < newParts.length; i++) {
          if (newParts[i].includes('.')) continue;   // fichier (index.html…) : on n'y touche pas
          newParts[i] = translateSegment(newParts[i], currentFolder, folder);
        }
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
        <p class="country-picker-foot">¿Tu país no está en la lista? Escríbenos a <a href="#" data-m64="aW5mb0Bwb2xpc3RpYnJpY2suZXU=">Email</a></p>
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

  /* -------------------------------------------------------------------------
     Email obfuscation — the address is NEVER in the page source (anti-spam).
     Buttons carry data-m64 (base64); the mailto: is assembled only on click.
     ------------------------------------------------------------------------- */
  document.addEventListener('click', function (e) {
    const el = e.target && e.target.closest ? e.target.closest('[data-m64]') : null;
    if (!el) return;
    e.preventDefault();
    try { window.location.href = 'mailto:' + atob(el.getAttribute('data-m64')); } catch (err) { /* ignore */ }
  });
})();
