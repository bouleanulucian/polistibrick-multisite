/* ===========================================================================
   POLISTIBRICK — Cookie consent banner (RGPD / ePrivacy)
   Preference: localStorage pb_cookie_consent = "accepted" | "essential"
   =========================================================================== */
(function () {
  var STORAGE_KEY = 'pb_cookie_consent';

  var TEXT = {
    body: 'Nous utilisons des cookies et services tiers (géolocalisation, polices web) pour améliorer le site. Consultez notre',
    link: 'politique de cookies',
    and: 'et',
    privacy: 'politique de confidentialité',
    aria: 'Consentement cookies',
    accept: 'Accepter',
    refuse: 'Refuser',
    privacySlug: 'confidentialite',
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

  function getConsent() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function setConsent(level) {
    try {
      localStorage.setItem(STORAGE_KEY, level);
    } catch (e) { /* ignore */ }
    window.dispatchEvent(new CustomEvent('pb-cookie-consent', { detail: { level: level } }));
  }

  window.pbCookieConsent = getConsent;
  window.pbHasOptionalConsent = function () {
    return getConsent() === 'accepted';
  };

  function buildBanner() {
    if (document.getElementById('pbCookieBanner')) return;
    var base = basePath();
    var bodyText = resolved(TEXT.body, 'Nous utilisons des cookies et services tiers pour améliorer votre expérience. Consultez notre');
    var linkText = resolved(TEXT.link, 'politique de cookies');
    var andText = resolved(TEXT.and, 'et');
    var privacyText = resolved(TEXT.privacy, 'politique de confidentialité');
    var privacySlug = resolved(TEXT.privacySlug, 'confidentialite');
    var ariaLabel = resolved(TEXT.aria, 'Consentement cookies');
    var acceptLabel = resolved(TEXT.accept, 'Accepter');
    var refuseLabel = resolved(TEXT.refuse, 'Refuser');

    var bar = document.createElement('div');
    bar.id = 'pbCookieBanner';
    bar.className = 'pb-cookie-banner';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-live', 'polite');
    bar.setAttribute('aria-label', ariaLabel);
    bar.innerHTML =
      '<div class="pb-cookie-inner">' +
        '<p class="pb-cookie-text">' + bodyText + ' ' +
          '<a href="' + base + 'legal/cookies/">' + linkText + '</a> ' +
          andText + ' <a href="' + base + 'legal/' + privacySlug + '/">' + privacyText + '</a>.</p>' +
        '<div class="pb-cookie-actions">' +
          '<button type="button" class="pb-cookie-btn pb-cookie-btn--ghost" data-pb-cookie="essential">' + refuseLabel + '</button>' +
          '<button type="button" class="pb-cookie-btn pb-cookie-btn--primary" data-pb-cookie="accepted">' + acceptLabel + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(bar);

    bar.querySelector('[data-pb-cookie="accepted"]').addEventListener('click', function () {
      setConsent('accepted');
      bar.remove();
    });
    bar.querySelector('[data-pb-cookie="essential"]').addEventListener('click', function () {
      setConsent('essential');
      bar.remove();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (getConsent()) return;
    buildBanner();
  });
})();
