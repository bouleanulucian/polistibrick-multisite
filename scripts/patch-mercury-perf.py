#!/usr/bin/env python3
"""Apply ZURU-style performance patches to all mercury homepage HTML files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNTRIES = ROOT / "countries"

FONT_OLD = (
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Inter:wght@400;500;600;700&family=Manrope:wght@600&display=swap" rel="stylesheet">'
)
FONT_NEW = """<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&family=Manrope:wght@600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&family=Manrope:wght@600&display=swap"></noscript>
<link rel="preload" as="image" href="images/hero/hero-house-1.webp" type="image/webp">"""

HERO_OLD = """  <div class="hero-bg" aria-hidden="true">
    <video id="heroVideo" autoplay muted loop playsinline preload="none"
           poster="images/hero/hero-house-1.jpg">
      <source src="images/hero/hero-houses-reel.mp4" type="video/mp4">
    </video>
    <div class="hero-bg-scrim"></div>
  </div>"""

HERO_NEW = """  <div class="hero-bg" aria-hidden="true">
    <picture class="hero-bg-poster">
      <source type="image/webp" srcset="images/hero/hero-house-1.webp">
      <img src="images/hero/hero-house-1.jpg" alt="" width="1920" height="1080" decoding="async" fetchpriority="high">
    </picture>
    <video id="heroVideo" class="hero-bg-video" muted loop playsinline preload="none"
           data-src-desktop="images/hero/hero-houses-reel-desktop.mp4"
           data-src-mobile="images/hero/hero-houses-reel-mobile.mp4"></video>
    <div class="hero-bg-scrim"></div>
  </div>"""

CSS_MARKER = """  .hero-bg video {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }"""

CSS_ADD = """  .hero-bg video {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }
  .hero-bg-poster {
    position: absolute;
    inset: 0;
    z-index: 0;
  }
  .hero-bg-poster img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    display: block;
  }
  .hero-bg video.hero-bg-video {
    z-index: 0;
    opacity: 0;
    transition: opacity 0.55s ease;
  }
  .hero-bg video.hero-bg-video.is-playing {
    opacity: 1;
  }"""

VIDEO_OBSERVER = """  ['morphVideo', 'heroVideo'].forEach((id) => {
    const v = document.getElementById(id);
    if (!v) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      v.removeAttribute('autoplay');
      v.pause();
      return;
    }
    if ('IntersectionObserver' in window) {
      const vio = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) { v.play().catch(() => {}); }
          else { v.pause(); }
        });
      }, { threshold: 0.1 });
      vio.observe(v);
    }
  });"""

LAZY_SCRIPT = """<script>
(function(){
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  function bootVideo(v){
    var s=v.querySelector('source[data-src]');
    if(!s||s.src) return;
    var mobile=v.dataset.srcMobile;
    if(mobile&&window.matchMedia('(max-width:1080px)').matches){
      s.dataset.src=mobile;
      if(v.dataset.posterMobile) v.poster=v.dataset.posterMobile;
    }
    s.src=s.dataset.src;
    v.load();
    var p=v.play();
    if(p&&p.catch) p.catch(function(){});
  }
  var vids=document.querySelectorAll('video.lazy-video');
  if(!vids.length) return;
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ bootVideo(e.target); io.unobserve(e.target); }
      });
    },{rootMargin:'80px 0px',threshold:0.01});
    vids.forEach(function(v){ io.observe(v); });
  } else { vids.forEach(bootVideo); }
})();
</script>"""


def patch(text: str) -> str:
    if FONT_OLD in text:
        text = text.replace(FONT_OLD, FONT_NEW)
    if HERO_OLD in text:
        text = text.replace(HERO_OLD, HERO_NEW)
    if CSS_MARKER in text and ".hero-bg-poster" not in text:
        text = text.replace(CSS_MARKER, CSS_ADD)
    text = text.replace(
        'fetchpriority="high" width="1500" height="1362"',
        'fetchpriority="low" loading="lazy" width="1500" height="1362"',
    )
    text = text.replace(
        'data-conf-video="images/hero/hero-houses-reel.mp4"',
        'data-conf-video="images/hero/hero-houses-reel-desktop.mp4"',
    )
    for j in ("hero-house-2.jpg", "hero-house-3.jpg", "hero-house-1.jpg"):
        text = text.replace(
            f'class="histoire-bg" src="images/hero/{j}"',
            f'class="histoire-bg" src="images/hero/{j}" loading="lazy"',
        )
    if VIDEO_OBSERVER in text:
        text = text.replace(VIDEO_OBSERVER, "  /* video IO → assets/js/mercury-perf.js */")
    if LAZY_SCRIPT in text:
        text = text.replace(LAZY_SCRIPT, '<script src="assets/js/mercury-perf.js" defer></script>')
    elif 'assets/js/mercury-perf.js' not in text:
        text = text.replace(
            '<script src="assets/js/forms.js" defer></script>',
            '<script src="assets/js/mercury-perf.js" defer></script>\n<script src="assets/js/forms.js" defer></script>',
        )
    return text


def main():
    files = sorted(COUNTRIES.glob("*/polistibrick-mercury-style.html"))
    for path in files:
        original = path.read_text(encoding="utf-8")
        updated = patch(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"patched {path.relative_to(ROOT)}")
        else:
            print(f"unchanged {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
