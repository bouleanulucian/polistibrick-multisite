/**
 * Homepage media — poster-first, lazy below-fold MP4, one playing video at a time.
 */
(function () {
  'use strict';

  var activeVideo = null;

  function isMobile() {
    return window.matchMedia('(max-width: 809px)').matches;
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
      setActive(video);
    }, { once: true });

    var play = video.play();
    if (play && play.then) {
      play.then(function () {
        revealVideo(video);
        setActive(video);
      }).catch(function () {});
    }
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
    var threshold = opts.threshold || 0.12;
    var rootMargin = opts.rootMargin || '120px 0px';
    var delay = parseInt(video.dataset.bootDelay || '0', 10) || 0;
    var lazy = opts.lazy !== false;

    function playNow() {
      setActive(video);
      var play = video.play();
      if (play && play.then) {
        play.then(function () {
          video.classList.add('is-playing');
        }).catch(function () {});
      }
    }

    function onVisible() {
      if (lazy) bootLazy(video);
      playNow();
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

  var hero = document.getElementById('heroVideo');
  if (hero && hero.dataset.srcDesktop) {
    bootHero(hero);
    observe(hero, { lazy: false, threshold: 0.2, rootMargin: '0px' });
  }

  document.querySelectorAll('video.lazy-video').forEach(function (video) {
    if (video.id === 'heroVideo') return;
    var rootMargin = video.classList.contains('montaj-bg') ? '180px 0px' : '120px 0px';
    observe(video, { rootMargin: rootMargin });
  });
})();
