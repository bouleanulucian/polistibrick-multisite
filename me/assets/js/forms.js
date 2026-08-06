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
    liveDomain: 'polistibrick.me',
    liveDomainUrl: 'https://polistibrick.me',
    ccEmail: dec64('{{form_cc_email|b64}}'),
    country: 'ME',
    countryName: 'Montenegro',
    fallbackEmail: dec64('Y29udGFjdEBwb2xpc3RpYnJpY2suY29t'),
    subjects: {
      contact: 'Kontakt — Polistibrick Crna Gora',
      devis: 'Zahtjev za ponudu — Polistibrick Crna Gora',
      partner: 'Prijava partnera — Polistibrick Crna Gora',
      review: 'Nova recenzija klijenta — Polistibrick Crna Gora',
    },
  };

  const MSG = {
    errPrivacy: 'Prihvatite politiku privatnosti da biste nastavili.',
    errRatingName: 'Navedite barem: ocjenu i ime / firmu.',
    errVideo: 'Dodajte video — ili odaberite « Tekst + fotografije ».',
    errReviewText: 'Napišite recenziju.',
    errNetwork: 'Greška mreže. Pokušajte ponovo za nekoliko trenutaka.',
    errSend: 'Slanje nije moguće. Pokušajte ponovo ili nas kontaktirajte putem e-maila.',
    loading: 'Šalje se…',
    blockedNoKeyPrefix: 'Dodajte Web3Forms ključ u _config.json (domen:',
    blockedNoKeySuffix: '). U međuvremenu:',
    blockedPreviewPrefix: 'Pregled — slanje radi na',
    blockedPreviewMid: 'ili lokalno (localhost). Kontakt:',
    blockedUnavailable: 'Formular nije dostupan. Kontakt:',
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

  function isGitHubPages() {
    // găzduirea curentă, până mutăm site-ul pe domeniile proprii
    return window.location.hostname === 'bouleanulucian.github.io';
  }

  function isAllowedHost() {
    return isOnLiveDomain() || isGitHubPages() || isLocalDev();
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

  // Vine dintr-un model de casă: /contact/?model=PBK+7&sistem=Polistibrick
  // Completează subiectul, mesajul, şi trimite alegerea ca două câmpuri separate.
  function prefillFromUrl(form) {
    const q = new URLSearchParams(location.search);
    const model = q.get('model');
    const sistem = q.get('sistem');
    const subiect = q.get('subiect') || q.get('subject');
    if (!model && !sistem && !subiect) return;

    const sel = form.querySelector('select[name="subject"]');
    if (sel) {
      // subjects.devis e linia de email ("Cerere ofertă — Polistibrick România"),
      // nu o opţiune din listă. Potrivim după cuvinte comune, ca să meargă în orice limbă.
      const norm = function (t) {
        return (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
      };
      const radacini = function (t) {
        return norm(t).split(/[^a-z0-9]+/).filter(function (w) { return w.length > 3; })
                      .map(function (w) { return w.slice(0, 5); });
      };
      const tinta = subiect || (model ? resolved(CFG.subjects.devis, '').split('—')[0] : '');
      const cautate = radacini(tinta);
      if (cautate.length) {
        let castigator = null, maxim = 0;
        Array.from(sel.options).forEach(function (o) {
          const ale = radacini(o.textContent);
          const scor = cautate.filter(function (r) { return ale.indexOf(r) !== -1; }).length;
          if (scor > maxim) { maxim = scor; castigator = o; }
        });
        if (castigator) sel.value = castigator.value || castigator.textContent.trim();
      }
    }

    const msg = form.querySelector('textarea[name="message"]');
    if (msg && !msg.value.trim() && (model || sistem)) {
        // mesajul precompletat, în limba paginii
        const L = (document.documentElement.lang || 'ro').slice(0, 2);
        const SABLOANE = {
          ro: ['Mă interesează modelul ', 'Mă interesează un model din catalog', ', construit în sistemul ', ''],
          fr: ['Je suis intéressé par le modèle ', 'Je suis intéressé par un modèle du catalogue', ', construit avec le système ', ''],
          en: ['I am interested in the ', 'I am interested in a model from the catalogue', ', built with the ', ' system'],
          es: ['Me interesa el modelo ', 'Me interesa un modelo del catálogo', ', construido con el sistema ', ''],
          it: ['Mi interessa il modello ', 'Mi interessa un modello del catalogo', ', costruito con il sistema ', ''],
          sr: ['Zanima me model ', 'Zanima me model iz kataloga', ', građen sistemom ', ''],
          me: ['Zanima me model ', 'Zanima me model iz kataloga', ', građen sistemom ', '']
        };
        const S = SABLOANE[L] || SABLOANE.ro;
        let t = model ? S[0] + model + (L === 'en' ? ' model' : '') : S[1];
        if (sistem) t += S[2] + sistem + S[3];
      msg.value = t + '.\n\n';
      msg.setSelectionRange(msg.value.length, msg.value.length);
    }

    // ajung în email ca linii proprii, nu doar topite în mesaj
    [['house_model', model], ['building_system', sistem]].forEach(function (p) {
      if (!p[1] || form.querySelector('[name="' + p[0] + '"]')) return;
      const h = document.createElement('input');
      h.type = 'hidden'; h.name = p[0]; h.value = p[1];
      form.appendChild(h);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-pb-form]').forEach(function (form) {
      initForm(form);
      prefillFromUrl(form);
    });
  });
})();
