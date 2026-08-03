/* ===========================================================================
   POLISTIBRICK — Form handler (Web3Forms)
   Config injected at build from _config.json placeholders.
   =========================================================================== */
(function () {
  // Emailurile NU apar în clar în sursă (anti-spam) — sunt base64, decodate la runtime.
  function dec64(s) {
    try { return s && s.indexOf('{{') === -1 ? atob(s) : ''; } catch (e) { return ''; }
  }
  const CFG = {
    accessKey: '',
    liveDomain: 'polistibrick.uk',
    liveDomainUrl: 'https://polistibrick.uk',
    ccEmail: dec64('{{form_cc_email|b64}}'),
    country: 'GB',
    countryName: 'United Kingdom',
    fallbackEmail: dec64('Y29udGFjdEBwb2xpc3RpYnJpY2suY29t'),
    subjects: {
      contact: 'Contact — Polistibrick UK',
      devis: 'Quote request — Polistibrick UK',
      partner: 'Partner application — Polistibrick UK',
      review: 'New customer review — Polistibrick UK',
    },
  };

  const MSG = {
    errPrivacy: '{{ui.form_err_privacy}}',
    errRatingName: '{{ui.form_err_rating_name}}',
    errVideo: '{{ui.form_err_video}}',
    errReviewText: '{{ui.form_err_review_text}}',
    errNetwork: '{{ui.form_err_network}}',
    errSend: '{{ui.form_err_send}}',
    loading: '{{ui.form_loading}}',
    blockedNoKeyPrefix: '{{ui.form_blocked_no_key_prefix}}',
    blockedNoKeySuffix: '{{ui.form_blocked_no_key_suffix}}',
    blockedPreviewPrefix: '{{ui.form_blocked_preview_prefix}}',
    blockedPreviewMid: '{{ui.form_blocked_preview_mid}}',
    blockedUnavailable: '{{ui.form_blocked_unavailable}}',
  };

  function resolved(str, fallback) {
    if (!str || str.indexOf('{{') !== -1) return fallback;
    return str;
  }

  const ENDPOINT = 'https://api.web3forms.com/submit';

  function hasAccessKey() {
    return CFG.accessKey && CFG.accessKey.indexOf('{{') === -1 && CFG.accessKey.length > 8;
  }

  function isLocalDev() {
    var host = window.location.hostname;
    return host === 'localhost' || host === '127.0.0.1' || host === '[::1]';
  }

  function isOnLiveDomain() {
    if (!CFG.liveDomain || CFG.liveDomain.indexOf('{{') !== -1) return false;
    var host = window.location.hostname.replace(/^www\./, '');
    var live = CFG.liveDomain.replace(/^www\./, '');
    return host === live;
  }

  function isAllowedHost() {
    return isOnLiveDomain() || isLocalDev();
  }

  function isConfigured() {
    return hasAccessKey() && isAllowedHost();
  }

  function formsBlockedMessage() {
    if (!hasAccessKey()) {
      return resolved(MSG.blockedNoKeyPrefix, 'Ajoutez la clé Web3Forms dans _config.json (domaine : ') +
        CFG.liveDomain +
        resolved(MSG.blockedNoKeySuffix, '). En attendant : ') +
        CFG.fallbackEmail;
    }
    if (!isAllowedHost()) {
      return resolved(MSG.blockedPreviewPrefix, 'Prévisualisation — l’envoi fonctionne sur ') +
        CFG.liveDomain + ' ' +
        resolved(MSG.blockedPreviewMid, 'ou en local (localhost). Contact : ') +
        CFG.fallbackEmail;
    }
    return resolved(MSG.blockedUnavailable, 'Formulaire indisponible. Contact : ') + CFG.fallbackEmail;
  }

  function setLoading(form, on) {
    form.classList.toggle('is-loading', on);
    const btn = form.querySelector('[type="submit"]');
    if (btn) {
      btn.disabled = on;
      if (!btn.dataset.pbLabel) btn.dataset.pbLabel = btn.textContent;
      btn.textContent = on ? resolved(MSG.loading, 'Envoi en cours…') : btn.dataset.pbLabel;
    }
  }

  function showError(form, msg) {
    let el = form.querySelector('.pb-form-error');
    if (!el) {
      el = document.createElement('p');
      el.className = 'pb-form-error';
      form.appendChild(el);
    }
    el.textContent = msg;
    el.hidden = false;
  }

  function clearError(form) {
    const el = form.querySelector('.pb-form-error');
    if (el) el.hidden = true;
  }

  function markSent(form) {
    form.classList.add('is-sent');
    const thanks = form.querySelector('.pb-form-thanks');
    if (thanks) thanks.hidden = false;
    const avisModal = form.closest('#avisModal');
    if (avisModal) avisModal.classList.add('sent');
  }

  async function postFormData(fd) {
    const res = await fetch(ENDPOINT, { method: 'POST', body: fd });
    const data = await res.json().catch(function () { return {}; });
    if (!res.ok || !data.success) {
      throw new Error(data.message || resolved(MSG.errNetwork, 'Erreur réseau. Réessayez dans un instant.'));
    }
    return data;
  }

  function baseFields(fd, type) {
    fd.append('access_key', CFG.accessKey);
    fd.append('subject', CFG.subjects[type] || ('Polistibrick — ' + type));
    fd.append('from_name', 'Polistibrick Website');
    fd.append('country_code', CFG.country);
    fd.append('country_name', CFG.countryName);
    if (CFG.liveDomain && CFG.liveDomain.indexOf('{{') === -1) {
      fd.append('site_domain', CFG.liveDomain);
    }
    if (CFG.liveDomainUrl && CFG.liveDomainUrl.indexOf('{{') === -1) {
      fd.append('site_url', CFG.liveDomainUrl);
    }
    if (CFG.ccEmail && CFG.ccEmail.indexOf('{{') === -1) {
      fd.append('cc_email', CFG.ccEmail);
    }
  }

  function appendFiles(fd, input) {
    if (!input || !input.files) return;
    Array.from(input.files).forEach(function (file) {
      fd.append('attachment', file);
    });
  }

  async function submitStandard(form, type) {
    clearError(form);
    const consent = form.querySelector('[name="privacy_consent"]');
    if (consent && !consent.checked) {
      showError(form, resolved(MSG.errPrivacy, 'Merci d’accepter la politique de confidentialité pour continuer.'));
      consent.focus();
      return;
    }
    if (!isConfigured()) {
      showError(form, formsBlockedMessage());
      return;
    }
    setLoading(form, true);
    try {
      const fd = new FormData(form);
      baseFields(fd, type);
      fd.delete('botcheck');
      await postFormData(fd);
      markSent(form);
      form.reset();
    } catch (err) {
      showError(form, err.message || resolved(MSG.errSend, 'Envoi impossible. Réessayez ou contactez-nous par email.'));
    } finally {
      setLoading(form, false);
    }
  }

  async function submitReview(form) {
    clearError(form);
    const err = document.getElementById('avisErr');
    if (err) err.style.display = 'none';

    const stars = form.querySelectorAll('#avisStars button.on');
    const rating = stars.length;
    const nom = (document.getElementById('avisNom')?.value || '').trim();
    const msg = (document.getElementById('avisMsg')?.value || '').trim();
    const modeBtn = form.querySelector('#avisToggle .at-opt.is-on');
    const mode = modeBtn ? modeBtn.getAttribute('data-mode') : 'texte';
    const videoInput = document.getElementById('avisVideo');
    const photosInput = document.getElementById('avisPhotos');
    const profileInput = document.getElementById('avisProfile');

    if (!rating || !nom) {
      if (err) {
        err.textContent = resolved(MSG.errRatingName, 'Merci d’indiquer au moins : une note et votre nom / entreprise.');
        err.style.display = 'block';
      }
      return;
    }
    if (mode === 'video' && (!videoInput || !videoInput.files.length)) {
      if (err) {
        err.textContent = resolved(MSG.errVideo, 'Merci d’ajouter votre vidéo — ou choisissez « Texte + photos ».');
        err.style.display = 'block';
      }
      return;
    }
    if (mode === 'texte' && !msg) {
      if (err) {
        err.textContent = resolved(MSG.errReviewText, 'Merci d’écrire votre avis.');
        err.style.display = 'block';
      }
      return;
    }

    const consent = form.querySelector('[name="privacy_consent"]');
    if (consent && !consent.checked) {
      if (err) {
        err.textContent = resolved(MSG.errPrivacy, 'Merci d’accepter la politique de confidentialité pour continuer.');
        err.style.display = 'block';
      }
      consent.focus();
      return;
    }

    if (!isConfigured()) {
      if (err) {
        err.textContent = formsBlockedMessage();
        err.style.display = 'block';
      }
      return;
    }

    setLoading(form, true);
    try {
      const fd = new FormData();
      baseFields(fd, 'review');
      fd.append('name', nom);
      fd.append('email', dec64('YXZpc0Bwb2xpc3RpYnJpY2suZnI=')); // avis@… (base64, anti-scraping)
      fd.append('rating', String(rating));
      fd.append('role', document.getElementById('avisRole')?.value || '');
      fd.append('location', document.getElementById('avisLieu')?.value || '');
      fd.append('review_type', mode);
      fd.append('message', msg);
      appendFiles(fd, photosInput);
      appendFiles(fd, profileInput);
      if (videoInput && videoInput.files.length) {
        fd.append('attachment', videoInput.files[0]);
      }
      await postFormData(fd);
      markSent(form);
      form.reset();
    } catch (e) {
      if (err) {
        err.textContent = e.message || resolved(MSG.errSend, 'Envoi impossible.');
        err.style.display = 'block';
      }
    } finally {
      setLoading(form, false);
    }
  }

  function initForm(form) {
    const type = form.getAttribute('data-pb-form');
    if (!type) return;

    if (!form.querySelector('[name="botcheck"]')) {
      const hp = document.createElement('input');
      hp.type = 'checkbox';
      hp.name = 'botcheck';
      hp.className = 'pb-honeypot';
      hp.tabIndex = -1;
      hp.autocomplete = 'off';
      form.appendChild(hp);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (type === 'review') submitReview(form);
      else submitStandard(form, type);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-pb-form]').forEach(initForm);
  });
})();
