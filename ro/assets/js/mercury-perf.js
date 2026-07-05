/**
 * Lazy media below the hero — hero video is eager/autoplay in HTML.
 */
(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function isMobile() {
    return window.matchMedia('(max-width: 809px)').matches;
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

  document.querySelectorAll('video.lazy-video').forEach(function (video) {
    if (video.id === 'morphVideo') {
      watchPlayPause(video, 0.12);
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
