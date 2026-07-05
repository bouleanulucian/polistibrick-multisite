/**
 * Homepage media: ZURU-style poster-first hero, lazy below-fold videos.
 */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function isMobile() {
    return window.matchMedia('(max-width: 809px)').matches;
  }

  function schedule(fn) {
    if (window.requestIdleCallback) {
      window.requestIdleCallback(fn, { timeout: 400 });
    } else {
      setTimeout(fn, 80);
    }
  }

  function pickHeroUrls(video) {
    var desktop = video.dataset.srcDesktop;
    var mobile = video.dataset.srcMobile;
    var desktopWebm = video.dataset.srcDesktopWebm;
    var mobileWebm = video.dataset.srcMobileWebm;
    if (isMobile()) {
      return {
        mp4: mobile,
        webm: mobileWebm && canPlayWebm() ? mobileWebm : null
      };
    }
    return {
      mp4: desktop,
      webm: desktopWebm && canPlayWebm() ? desktopWebm : null
    };
  }

  function canPlayWebm() {
    var v = document.createElement('video');
    return v.canPlayType('video/webm; codecs="vp9"') !== '';
  }

  function bootHero() {
    var video = document.getElementById('heroVideo');
    if (!video || video.dataset.booted === '1') return;
    video.dataset.booted = '1';

    var urls = pickHeroUrls(video);
    if (!urls.mp4 && !urls.webm) return;

    if (urls.webm) {
      var webm = document.createElement('source');
      webm.src = urls.webm;
      webm.type = 'video/webm';
      video.appendChild(webm);
    }
    if (urls.mp4) {
      var mp4 = document.createElement('source');
      mp4.src = urls.mp4;
      mp4.type = 'video/mp4';
      video.appendChild(mp4);
    }

    video.load();

    function reveal() {
      video.classList.add('is-playing');
      var bg = video.closest('.hero-bg');
      if (bg) bg.classList.add('is-video-playing');
    }

    video.addEventListener('playing', reveal, { once: true });
    var play = video.play();
    if (play && play.then) {
      play.then(reveal).catch(function () {});
    }
  }

  function bootVideo(video) {
    if (video.dataset.booted === '1') return;
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
    var p = video.play();
    if (p && p.catch) p.catch(function () {});
  }

  function watchPlayPause(video, threshold) {
    if (!('IntersectionObserver' in window)) {
      bootVideo(video);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          bootVideo(video);
          video.play().catch(function () {});
        } else {
          video.pause();
        }
      });
    }, { threshold: threshold || 0.12 });
    io.observe(video);
  }

  if (!reduced) {
    var hero = document.getElementById('heroVideo');
    if (hero && hero.dataset.srcDesktop) {
      schedule(bootHero);
    }
  }

  document.querySelectorAll('video.lazy-video').forEach(function (video) {
    if (video.id === 'morphVideo') {
      watchPlayPause(video, 0.12);
      return;
    }

    var delay = parseInt(video.dataset.bootDelay || '0', 10) || 0;
    var rootMargin = video.classList.contains('montaj-bg') ? '200px 0px' : '120px 0px';

    function trigger() {
      if (delay > 0) {
        setTimeout(function () { bootVideo(video); }, delay);
      } else {
        bootVideo(video);
      }
    }

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            trigger();
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: rootMargin, threshold: 0.01 });
      io.observe(video);
    } else {
      trigger();
    }
  });
})();
