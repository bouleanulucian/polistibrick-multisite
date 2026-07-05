#!/usr/bin/env python3
"""Restore ZURU-style background videos (poster layer + lazy MP4) on all mercury homepages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA_CSS = """
  /* ZURU-style: poster instant, video fade-in when playing */
  .media-poster {
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;
  }
  .media-poster img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .morph-media { position: relative; }
  .morph-media .morph-video {
    position: relative;
    z-index: 1;
    opacity: 0;
    transition: opacity 0.35s ease;
  }
  .morph-media .morph-video.is-playing { opacity: 1; }
  .presence-section { position: relative; }
  .presence-poster { z-index: 0; }
  .presence-bg {
    opacity: 0;
    transition: opacity 0.35s ease;
  }
  .presence-bg.is-playing { opacity: 0.55; }
  .montaj-section { position: relative; }
  .montaj-bg {
    opacity: 0;
    transition: opacity 0.35s ease;
  }
  .montaj-bg.is-playing { opacity: 1; }
  .cinq-media { position: relative; }
  .cinq-media .cinq-video {
    position: relative;
    z-index: 1;
    opacity: 0;
    transition: opacity 0.35s ease;
  }
  .cinq-media .cinq-video.is-playing { opacity: 1; }
"""

MORPH_IMG = re.compile(
    r'<img class="morph-video" src="images/morph/morph-poster\.jpg" alt="([^"]*)" loading="lazy" decoding="async">',
    re.DOTALL,
)

PRESENCE_IMG = re.compile(
    r'<img class="presence-bg" src="images/presence/presence-factory\.jpg" alt="([^"]*)" loading="lazy" decoding="async">',
    re.DOTALL,
)

CINQ_IMG = re.compile(
    r'<img class="cinq-video" src="images/bundle/bundle-test-poster\.jpg\?v=3" alt="([^"]*)" loading="lazy" decoding="async">',
    re.DOTALL,
)

MONTAJ_RO = re.compile(
    r'<img class="montaj-bg" src="images/montaj/montage-houses-poster\.webp" alt="" loading="lazy" decoding="async">',
)

MONTAJ_INTL = re.compile(
    r'<img class="montaj-bg" src="images/montage/montage-houses-poster\.jpg" alt="" loading="lazy" decoding="async">',
)


def morph_block(alt: str) -> str:
    return f"""    <picture class="media-poster" aria-hidden="true">
      <img src="images/morph/morph-poster.jpg" alt="" loading="lazy" decoding="async">
    </picture>
    <video id="morphVideo" class="morph-video lazy-video" muted loop playsinline preload="none"
           poster="images/morph/morph-poster.jpg"
           aria-label="{alt}">
      <source data-src="images/morph/morphing-polistibrick.mp4" type="video/mp4">
    </video>"""


def presence_block(alt: str) -> str:
    return f"""  <picture class="media-poster presence-poster" aria-hidden="true">
    <img src="images/presence/presence-factory.jpg" alt="" loading="lazy" decoding="async">
  </picture>
  <video class="presence-bg lazy-video" loop muted playsinline preload="none"
         poster="images/presence/presence-factory.jpg"
         aria-label="{alt}">
    <source data-src="images/presence/presence-factory-film.mp4?v=5" type="video/mp4">
  </video>"""


def cinq_block(alt: str) -> str:
    return f"""    <picture class="media-poster" aria-hidden="true">
      <img src="images/bundle/bundle-test-poster.jpg?v=3" alt="" loading="lazy" decoding="async">
    </picture>
    <video class="cinq-video lazy-video" muted loop playsinline preload="none"
           poster="images/bundle/bundle-test-poster.jpg?v=3"
           data-src-mobile="images/bundle/bundle-test-mobile.mp4?v=2"
           data-poster-mobile="images/bundle/bundle-test-mobile-poster.jpg?v=1"
           aria-label="{alt}">
      <source data-src="images/bundle/bundle-test.mp4?v=3" type="video/mp4">
    </video>"""


def montaj_ro_block() -> str:
    return """  <picture class="media-poster montaj-poster" aria-hidden="true">
    <img src="images/montaj/montage-houses-poster.webp" alt="" loading="lazy" decoding="async">
  </picture>
  <video class="montaj-bg lazy-video" muted loop playsinline preload="none" data-boot-delay="400"
         poster="images/montaj/montage-houses-poster.webp">
    <source data-src="images/montaj/montage-houses.mp4" type="video/mp4">
  </video>"""


def montaj_intl_block() -> str:
    return """  <picture class="media-poster montaj-poster" aria-hidden="true">
    <img src="images/montage/montage-houses-poster.jpg" alt="" loading="lazy" decoding="async">
  </picture>
  <video class="montaj-bg lazy-video" muted loop playsinline preload="none" data-boot-delay="400"
         poster="images/montage/montage-houses-poster.jpg">
    <source data-src="images/montage/montage-houses.mp4" type="video/mp4">
  </video>"""


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    is_ro = "/ro/" in str(path)

    text = MORPH_IMG.sub(lambda m: morph_block(m.group(1)), text)
    text = PRESENCE_IMG.sub(lambda m: presence_block(m.group(1)), text)
    text = CINQ_IMG.sub(lambda m: cinq_block(m.group(1)), text)
    if is_ro:
        text = MONTAJ_RO.sub(montaj_ro_block(), text)
    else:
        text = MONTAJ_INTL.sub(montaj_intl_block(), text)

    if MEDIA_CSS.strip() not in text:
        text = text.replace("</head>", f"<style>{MEDIA_CSS}\n</style>\n</head>", 1)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.glob("countries/*/polistibrick-mercury-style.html")):
        if patch_file(path):
            print(f"✓ {path.relative_to(ROOT)}")
            changed += 1
    print(f"\n{changed} file(s) patched.")


if __name__ == "__main__":
    main()
