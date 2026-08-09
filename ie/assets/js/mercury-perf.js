/**
 * Homepage media — poster-first, lazy below-fold MP4.
 * Règle unique : une vidéo joue tant qu'elle est à l'écran, et se met en pause
 * dès qu'elle en sort — dans les deux sens de scroll. Le hero démarre au
 * chargement.
 *
 * Architecture :
 *  - PRÉCHARGEMENT (bootLazy) : observer one-shot avec 120px d'avance — la
 *    vidéo télécharge avant d'arriver à l'écran, pour un démarrage instantané.
 *  - LECTURE/PAUSE : observer strict (0px) — la vidéo joue dès qu'elle entre
 *    réellement dans le viewport, se met en pause dès qu'elle en sort.
 *    L'état est écrit sur l'élément (data-io-visible) : source de vérité
 *    unique, partagée avec visibilitychange / pageshow / retry gestes.
 *  - La classe .is-playing (révélation au-dessus du poster) suit l'événement
 *    réel « playing », jamais la promesse de play() (qui peut être avortée).
 *  - Autoplay refusé (iOS Low Power, « Never Auto-Play », Data Saver) :
 *    on réessaie au premier geste de l'utilisateur.
 */
(function () {
  'use strict';

  function isMobile() {
    return window.matchMedia('(max-width: 809px)').matches;
  }

  function inViewport(v) {
    var r = v.getBoundingClientRect();
    var h = window.innerHeight || document.documentElement.clientHeight;
    return r.bottom > 0 && r.top < h;
  }

  /* Une vidéo peut-elle reprendre ? L'état IO fait foi quand il existe. */
  function canResume(v) {
    if (v.dataset.ioVisible != null) return v.dataset.ioVisible === '1';
    return inViewport(v);
  }

  function safePlay(v) {
    var p = v.play();
    if (p && p.catch) {
      p.catch(function (err) {
        if (err && err.name === 'NotAllowedError') armGestureRetry();
      });
    }
  }

  /* Autoplay bloqué par la politique du navigateur : au premier geste
     (scroll/tap/clic), on relance les vidéos visibles — le geste fournit
     la « user activation » qui autorise play(). */
  var gestureArmed = false;
  function armGestureRetry() {
    if (gestureArmed) return;
    gestureArmed = true;
    var handler = function () {
      document.removeEventListener('pointerup', handler);
      document.removeEventListener('touchend', handler);
      gestureArmed = false;
      document.querySelectorAll('video').forEach(function (v) {
        if (v.dataset.booted === '1' && v.paused && canResume(v)) safePlay(v);
      });
    };
    document.addEventListener('pointerup', handler, { once: true });
    document.addEventListener('touchend', handler, { once: true });
  }

  function revealVideo(video) {
    video.classList.add('is-playing');
    var wrap = video.closest('.hero-bg');
    if (wrap) wrap.classList.add('is-video-playing');
  }

  function heroUrl(video) {
    return isMobile() ? video.dataset.srcMobile : video.dataset.srcDesktop;
  }

  function bootHero(video) {
    if (!video || video.dataset.booted === '1') return;
    var url = heroUrl(video);
    if (!url) return;
    video.dataset.booted = '1';

    var mp4 = document.createElement('source');
    mp4.src = url;
    mp4.type = 'video/mp4';
    video.appendChild(mp4);
    video.load();

    video.addEventListener('playing', function () {
      revealVideo(video);
    }, { once: true });

    // Le play() initial peut être avorté par load() (course au chargement) :
    // dès que la vidéo est prête, on relance si elle est toujours à l'écran.
    video.addEventListener('canplay', function () {
      if (video.paused && !document.hidden && canResume(video)) safePlay(video);
    }, { once: true });

    // Onglet en arrière-plan au chargement : on ne force pas le play ici —
    // visibilitychange le relancera à l'arrivée sur l'onglet.
    if (!document.hidden) safePlay(video);
  }

  function bootLazy(video) {
    if (video.dataset.booted === '1') return;
    var lazySource = video.querySelector('source[data-src]');
    if (!lazySource) return;
    video.dataset.booted = '1';

    var url = lazySource.dataset.src;
    if (isMobile() && video.dataset.srcMobile) {
      url = video.dataset.srcMobile;
      if (video.dataset.posterMobile) video.poster = video.dataset.posterMobile;
    }
    lazySource.src = url;
    video.load();
  }

  function observe(video, opts) {
    opts = opts || {};
    var threshold = opts.threshold || 0; // 0 = joue dès le premier pixel visible
    var bootMargin = opts.bootMargin || '120px 0px';
    var delay = parseInt(video.dataset.bootDelay || '0', 10) || 0;
    var lazy = opts.lazy !== false;
    var delayTimer = null;

    // Révélation au-dessus du poster : sur l'événement réel, pas la promesse.
    video.addEventListener('playing', function () {
      video.classList.add('is-playing');
    });

    function playNow() {
      var play = video.play();
      if (play && play.catch) {
        play.catch(function (err) {
          if (err && err.name === 'NotAllowedError') { armGestureRetry(); return; }
          // play() avorté pendant le chargement : réessayer dès que la vidéo
          // est prête, si elle est toujours à l'écran.
          video.addEventListener('canplay', function () {
            if (!document.hidden && canResume(video)) safePlay(video);
          }, { once: true });
        });
      }
    }

    function onVisible() {
      if (lazy) bootLazy(video);
      playNow();
    }

    function onHidden() {
      if (delayTimer) { clearTimeout(delayTimer); delayTimer = null; }
      if (!video.paused) video.pause();
    }

    if (!('IntersectionObserver' in window)) {
      // Navigateurs très anciens : seul le hero joue (il est à l'écran au
      // chargement) ; les lazy restent sur leur poster — dégradation sobre.
      if (!lazy) { video.dataset.ioVisible = '1'; playNow(); }
      return;
    }

    // 1) Préchargement anticipé, one-shot — télécharge avant l'arrivée.
    if (lazy) {
      var bootIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            bootLazy(video);
            bootIO.unobserve(video);
          }
        });
      }, { rootMargin: bootMargin, threshold: 0 });
      bootIO.observe(video);
    }

    // 2) Lecture/pause — strictement l'écran, état publié sur l'élément.
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        video.dataset.ioVisible = entry.isIntersecting ? '1' : '0';
        if (entry.isIntersecting) {
          if (delay > 0) {
            delayTimer = setTimeout(function () {
              delayTimer = null;
              if (video.dataset.ioVisible === '1' && !document.hidden) onVisible();
            }, delay);
          } else {
            onVisible();
          }
        } else {
          onHidden();
        }
      });
    }, { rootMargin: '0px', threshold: threshold });

    io.observe(video);
  }

  var hero = document.getElementById('heroVideo');
  if (hero && hero.dataset.srcDesktop) {
    bootHero(hero);
    observe(hero, { lazy: false });
  }

  document.querySelectorAll('video.lazy-video').forEach(function (video) {
    if (video.id === 'heroVideo') return;
    observe(video);
  });

  /* Carrousel témoignages (.conf-track) — les vidéos ne jouent que si la
     section est à l'écran ; pause en sortant, reprise du slide actif en
     revenant (dans les deux sens de scroll, y compris le fond flou). */
  var confTrack = document.querySelector('.conf-track');
  if (confTrack && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          confTrack.querySelectorAll('.conf-slide.is-active video').forEach(function (v) {
            if (v.getAttribute('src') && v.paused) safePlay(v);
          });
        } else {
          confTrack.querySelectorAll('.conf-slide video').forEach(function (v) {
            if (!v.paused) v.pause();
          });
        }
      });
    }, { threshold: 0.15 }).observe(confTrack);
  }

  /* Onglet caché → tout mettre en pause (économie CPU/batterie) ;
     onglet visible → relancer uniquement les vidéos encore à l'écran.
     Corrige aussi le hero « mort » quand la page se charge en arrière-plan. */
  document.addEventListener('visibilitychange', function () {
    var vids = document.querySelectorAll('video');
    if (document.hidden) {
      vids.forEach(function (v) {
        if (!v.paused) { v.dataset.wasPlaying = '1'; v.pause(); }
      });
    } else {
      vids.forEach(function (v) {
        var eligible = v.dataset.wasPlaying === '1' || v.dataset.booted === '1';
        delete v.dataset.wasPlaying;
        if (eligible && v.paused && canResume(v)) safePlay(v);
      });
    }
  });

  /* Retour sur la page via le bouton Back (bfcache) : le navigateur restaure
     la page avec les vidéos gelées — on relance celles qui sont à l'écran. */
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    document.querySelectorAll('video').forEach(function (v) {
      if (v.dataset.booted === '1' && v.paused && canResume(v)) safePlay(v);
    });
  });
})();
