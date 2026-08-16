/* ===========================================================================
   POLISTIBRICK — Cookie consent banner (RGPD / ePrivacy)
   Preference: localStorage pb_cookie_consent = "accepted" | "essential"
   =========================================================================== */
(function () {
  var STORAGE_KEY = 'pb_cookie_consent';

  var TEXT = {
    body: '{{ui.cookie_banner_text}}',
    link: '{{ui.cookie_banner_link}}',
    and: '{{ui.cookie_banner_and}}',
    privacy: '{{ui.cookie_banner_privacy_link}}',
    aria: '{{ui.cookie_banner_aria}}',
    accept: '{{ui.cookie_accept}}',
    refuse: '{{ui.cookie_refuse}}',
    privacySlug: '{{legal.privacy_slug}}',
  };

  function basePath() {
    var explicit = document.body && document.body.dataset.base;
    if (explicit) return explicit;
    var depth = (window.location.pathname.replace(/\/$/, '').match(/\//g) || []).length;
    return depth <= 1 ? '' : '../'.repeat(depth - 1);
  }

  function resolved(str, fallback) {
    if (!str || str.indexOf('{{') !== -1) return fallback;
    return str;
  }

  // Politica de cookies promite: „Alegerea ta este salvată timp de 13 luni."
  // Până pe 16.08.2026 alegerea se salva FĂRĂ dată, deci rămânea pe viaţă —
  // exact genul de nepotrivire document/cod pe care îl caută un control.
  var MAX_AGE_MS = 13 * 30 * 24 * 60 * 60 * 1000; // ~13 luni
  var STAMP_KEY = STORAGE_KEY + '_ts';

  function getConsent() {
    try {
      var level = localStorage.getItem(STORAGE_KEY);
      if (!level) return null;
      var ts = parseInt(localStorage.getItem(STAMP_KEY), 10);
      // Consimţămintele vechi (fără dată) expiră acum: se cere din nou acordul.
      if (!ts || Date.now() - ts > MAX_AGE_MS) {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(STAMP_KEY);
        return null;
      }
      return level;
    } catch (e) {
      return null;
    }
  }

  function setConsent(level) {
    try {
      localStorage.setItem(STORAGE_KEY, level);
      localStorage.setItem(STAMP_KEY, String(Date.now()));
    } catch (e) { /* ignore */ }
    window.dispatchEvent(new CustomEvent('pb-cookie-consent', { detail: { level: level } }));
  }

  window.pbCookieConsent = getConsent;
  window.pbHasOptionalConsent = function () {
    return getConsent() === 'accepted';
  };

  var CSS = [
    '.pb-cookie-overlay { position: fixed; inset: 0; z-index: 10050; background: rgba(15, 14, 12, 0.62);',
    '  display: flex; align-items: center; justify-content: center; padding: 20px;',
    '  animation: pbFadeIn 0.25s ease; -webkit-backdrop-filter: blur(3px); backdrop-filter: blur(3px); }',
    '@keyframes pbFadeIn { from { opacity: 0; } to { opacity: 1; } }',
    '.pb-cookie-modal { background: #ffffff; color: #1a1714; max-width: 540px; width: 100%;',
    '  border-radius: 18px; padding: 30px 28px 24px; box-shadow: 0 30px 80px rgba(0,0,0,0.35);',
    '  font-family: Inter, system-ui, sans-serif; animation: pbPopIn 0.3s cubic-bezier(0.22,1,0.36,1); }',
    '@keyframes pbPopIn { from { transform: translateY(14px) scale(0.97); opacity: 0; } to { transform: none; opacity: 1; } }',
    '.pb-cookie-title { font-size: 17px; font-weight: 700; margin: 0 0 10px; }',
    '.pb-cookie-text { font-size: 14px; line-height: 1.6; color: #55504a; margin: 0 0 20px; }',
    '.pb-cookie-text a { color: #c8102e; font-weight: 600; text-decoration: none; }',
    '.pb-cookie-actions { display: flex; gap: 10px; flex-wrap: wrap; }',
    '.pb-cookie-btn { flex: 1; min-width: 150px; padding: 12px 18px; border-radius: 10px; font-size: 14px;',
    '  font-weight: 600; cursor: pointer; font-family: inherit; transition: all 0.15s ease; }',
    '.pb-cookie-btn--ghost { background: #fff; color: #1a1714; border: 1.5px solid #d9d4cc; }',
    '.pb-cookie-btn--ghost:hover { border-color: #1a1714; }',
    '.pb-cookie-btn--primary { background: #c8102e; color: #fff; border: 1.5px solid #c8102e; }',
    '.pb-cookie-btn--primary:hover { background: #a60d26; }',
    'body.pb-cookie-open { overflow: hidden; }'
  ].join('\n');

  function buildBanner() {
    if (document.getElementById('pbCookieOverlay')) return;
    var base = basePath();
    var bodyText = resolved(TEXT.body, 'Nous utilisons des cookies et services tiers pour améliorer votre expérience. Consultez notre');
    var linkText = resolved(TEXT.link, 'politique de cookies');
    var andText = resolved(TEXT.and, 'et');
    var privacyText = resolved(TEXT.privacy, 'politique de confidentialité');
    var privacySlug = resolved(TEXT.privacySlug, 'confidentialite');
    var ariaLabel = resolved(TEXT.aria, 'Consentement cookies');
    var acceptLabel = resolved(TEXT.accept, 'Tout accepter');
    var refuseLabel = resolved(TEXT.refuse, 'Essentiels uniquement');

    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    var overlay = document.createElement('div');
    overlay.id = 'pbCookieOverlay';
    overlay.className = 'pb-cookie-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', ariaLabel);
    overlay.innerHTML =
      '<div class="pb-cookie-modal">' +
        '<p class="pb-cookie-title">' + ariaLabel + '</p>' +
        '<p class="pb-cookie-text">' + bodyText + ' ' +
          '<a href="' + base + 'legal/cookies/">' + linkText + '</a> ' +
          andText + ' <a href="' + base + 'legal/' + privacySlug + '/">' + privacyText + '</a>.</p>' +
        '<div class="pb-cookie-actions">' +
          '<button type="button" class="pb-cookie-btn pb-cookie-btn--ghost" data-pb-cookie="essential">' + refuseLabel + '</button>' +
          '<button type="button" class="pb-cookie-btn pb-cookie-btn--primary" data-pb-cookie="accepted">' + acceptLabel + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(overlay);
    document.body.classList.add('pb-cookie-open');

    function alege(nivel) {
      setConsent(nivel);
      overlay.remove();
      document.body.classList.remove('pb-cookie-open');
    }
    overlay.querySelector('[data-pb-cookie="accepted"]').addEventListener('click', function () { alege('accepted'); });
    overlay.querySelector('[data-pb-cookie="essential"]').addEventListener('click', function () { alege('essential'); });
  }

  function porneste() {
    if (getConsent()) return;
    buildBanner();
  }
  // scriptul poate fi încărcat async — nu ne bazăm pe DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', porneste);
  } else {
    porneste();
  }
})();
