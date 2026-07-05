/**
 * Homepage media — ZURU-style: poster-first, lazy MP4, one playing video at a time.
 */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var activeVideo = null;

  function isMobile() {
    return window.matchMedia('(max-width: 809px)').matches;
  }

  function schedule(fn) {
    function run() {
      if ('requestIdleCallback' in window) {
        requestIdleCallback(fn, { timeout: 800 });
      } else {
        setTimeout(fn, 150);
      }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', run, { once: true });
    } else {
      run();
    }
  }

  function revealVideo(video) {
    video.classList.add('is-playing');
    var wrap = video.closest('.hero-bg');
    if (wrap) wrap.classList.add('is-video-playing');
  }

  function setActive(video) {
    if (activeVideo && activeVideo !== video && !activeVideo.paused) {
      activeVideo.pause();
    }
    activeVideo = video;
  }

  function pickHeroUrls(video) {
    if (isMobile()) {
      return video.dataset.srcMobile || null;
    }
    return video.dataset.srcDesktop || null;
  }

  function bootHero(video) {
    video = video || document.getElementById('heroVideo');
    if (!video || video.dataset.booted === '1') return;
    var url = pickHeroUrls(video);
    if (!url) return;
    video.dataset.booted = '1';

    var mp4 = document.createElement('source');
    mp4.src = url;
    mp4.type = 'video/mp4';
    video.appendChild(mp4);
    video.load();

    video.addEventListener('playing', function () {
      revealVideo(video);
      setActive(video);
    }, { once: true });

    var play = video.play();
    if (play && play.then) {
      play.then(function () { revealVideo(video); setActive(video); }).catch(function () {});
    }
  }

  function bootVideo(video) {
    if (video.dataset.booted === '1') return;

    // Vidéos type héros (sources via data-src-desktop/mobile, sans <source data-src>)
    // doivent passer par bootHero — sinon on les marque "booted" sans jamais charger la source.
    if (video.dataset.srcDesktop && !video.querySelector('source[data-src]')) {
      bootHero(video);
      return;
    }

    video.dataset.booted = '1';

    var lazySource = video.querySelector('source[data-src]');
    if (!lazySource) return;

    var url = lazySource.dataset.src;
    if (isMobile() && video.dataset.srcMobile) {
      url = video.dataset.srcMobile;
      if (video.dataset.posterMobile) video.poster = video.dataset.posterMobile;
    }
    lazySource.src = url;
    video.load();
  }

  function watchVideo(video, opts) {
    opts = opts || {};
    var threshold = opts.threshold || 0.15;
    var rootMargin = opts.rootMargin || '120px 0px';
    var delay = parseInt(video.dataset.bootDelay || '0', 10) || 0;

    function onVisible() {
      bootVideo(video);
      setActive(video);
      video.play().then(function () {
        video.classList.add('is-playing');
      }).catch(function () {});
    }

    function onHidden() {
      if (!video.paused) video.pause();
      if (activeVideo === video) activeVideo = null;
    }

    if (!('IntersectionObserver' in window)) {
      onVisible();
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          if (delay > 0) {
            setTimeout(onVisible, delay);
          } else {
            onVisible();
          }
        } else {
          onHidden();
        }
      });
    }, { rootMargin: rootMargin, threshold: threshold });

    io.observe(video);
  }

  if (!reduced) {
    var hero = document.getElementById('heroVideo');
    if (hero && hero.dataset.srcDesktop) {
      // Démarrage IMMÉDIAT (pas d'attente idle) — le poster couvre le premier instant,
      // la vidéo prend le relais dès que le réseau la livre.
      bootHero(hero);
      // Déclencheur visibilité : pause dès qu'on scrolle au-delà du héros, reprise au retour.
      watchVideo(hero, { threshold: 0.2, rootMargin: '0px' });
    }
  }

  document.querySelectorAll('video.lazy-video').forEach(function (video) {
    if (video.id === 'heroVideo') return;
    var rootMargin = video.classList.contains('montaj-bg') ? '180px 0px' : '120px 0px';
    watchVideo(video, { rootMargin: rootMargin });
  });
})();
