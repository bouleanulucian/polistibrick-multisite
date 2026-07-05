/**
 * ZURU-style media loading: poster-first hero, responsive MP4, lazy below-fold.
 */
(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function isMobile() {
    return window.matchMedia('(max-width: 809px)').matches;
  }

  function isTablet() {
    return window.matchMedia('(min-width: 810px) and (max-width: 1199px)').matches;
  }

  function pickDataSrc(video) {
    if (isMobile() && video.dataset.srcMobile) return video.dataset.srcMobile;
    if (isTablet() && video.dataset.srcTablet) return video.dataset.srcTablet;
    return video.dataset.srcDesktop || '';
  }

  function ensureMp4Source(video, url) {
    if (!url) return false;
    var src = video.querySelector('source');
    if (!src) {
      src = document.createElement('source');
      src.type = 'video/mp4';
      video.appendChild(src);
    }
    if (src.getAttribute('src') === url) return false;
    src.src = url;
    return true;
  }

  function playVideo(video) {
    var p = video.play();
    if (p && p.then) {
      p.then(function () { video.classList.add('is-playing'); }).catch(function () {});
    }
  }

  function bootVideo(video) {
    if (video.dataset.booted === '1') return;
    video.dataset.booted = '1';

    var lazySource = video.querySelector('source[data-src]');
    if (lazySource) {
      var url = lazySource.dataset.src;
      if (isMobile() && video.dataset.srcMobile) {
        url = video.dataset.srcMobile;
        if (video.dataset.posterMobile) video.poster = video.dataset.posterMobile;
      }
      lazySource.src = url;
    } else {
      ensureMp4Source(video, pickDataSrc(video));
    }

    video.load();
    playVideo(video);
  }

  function watchPlayPause(video, opts) {
    opts = opts || {};
    if (!('IntersectionObserver' in window)) {
      bootVideo(video);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          bootVideo(video);
          playVideo(video);
        } else {
          video.pause();
        }
      });
    }, {
      rootMargin: opts.rootMargin || '0px',
      threshold: opts.threshold != null ? opts.threshold : 0.08
    });
    io.observe(video);
  }

  var hero = document.getElementById('heroVideo');
  if (hero) watchPlayPause(hero, { rootMargin: '40px 0px' });

  document.querySelectorAll('video.lazy-video').forEach(function (video) {
    if (video.id === 'morphVideo') {
      watchPlayPause(video, { threshold: 0.12 });
      return;
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            bootVideo(entry.target);
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '120px 0px', threshold: 0.01 });
      io.observe(video);
    } else {
      bootVideo(video);
    }
  });
})();
