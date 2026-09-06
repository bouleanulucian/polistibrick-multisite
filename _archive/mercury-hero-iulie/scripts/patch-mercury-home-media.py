#!/usr/bin/env python3
"""Poster-first hero + WebP montaj cards + staggered montaj bg video."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = sorted((ROOT / "countries").glob("*/polistibrick-mercury-style.html"))

HEAD_VIDEO_PRELOADS = re.compile(
    r'\n<link rel="preload" as="video" href="images/hero/hero-houses-reel-mobile\.mp4"[^>]+>\n'
    r'<link rel="preload" as="video" href="images/hero/hero-houses-reel-desktop\.mp4"[^>]+>'
)

CSS_VIDEO_ONLY = """  .hero-bg video.hero-bg-video {
    z-index: 1;
    opacity: 1;
    background: #14120F;
  }"""

CSS_POSTER_FIRST = """  .hero-bg-poster {
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
    z-index: 1;
    opacity: 0;
    transition: opacity 0.45s ease;
    background: #14120F;
  }
  .hero-bg video.hero-bg-video.is-playing {
    opacity: 1;
  }"""

HERO_BLOCK = re.compile(
    r'    <video id="heroVideo" class="hero-bg-video"[^>]*>.*?</video>\n',
    re.DOTALL,
)
HERO_REPLACEMENT = """    <picture class="hero-bg-poster">
      <source type="image/webp" srcset="images/hero/hero-house-1.webp">
      <img src="images/hero/hero-house-1.jpg" alt="" width="1920" height="1080" decoding="async" fetchpriority="high">
    </picture>
    <video id="heroVideo" class="hero-bg-video" muted loop playsinline preload="none"
           poster="images/hero/hero-house-1.webp"
           data-src-desktop="images/hero/hero-houses-reel-desktop.mp4"
           data-src-mobile="images/hero/hero-houses-reel-mobile.mp4"></video>
"""

MONTAJ_BG_OLD = (
    '  <video class="montaj-bg lazy-video" muted loop playsinline preload="none" '
    'poster="images/montaj/montage-houses-poster.jpg">'
)
MONTAJ_BG_NEW = (
    '  <video class="montaj-bg lazy-video" muted loop playsinline preload="none" '
    'data-boot-delay="700" poster="images/montaj/montage-houses-poster.webp">'
)

CARD_IMAGES = {
    "stage1-cofraj.jpg": "Cofraj asamblat cu sprijin lateral",
    "stage3-planseu.jpg": "Planșeu PBK montat",
    "stage2-fierbeton.jpg": "Armătură oțel-beton pe planșeu",
    "stage4-final.jpg": "Cofraj închis, gata pentru turnarea betonului",
}

# FR / other locales use same filenames; alt text stays as in source file.


def patch_montaj_card(text: str, jpg: str) -> str:
    old = f'<img src="images/construction/{jpg}" alt="'
    if old not in text:
        return text
    # Preserve existing alt text between quotes
    pattern = re.compile(
        rf'<img src="images/construction/{re.escape(jpg)}" alt="([^"]*)" loading="lazy">'
    )
    repl = (
        rf'<picture><source type="image/webp" srcset="images/construction/{jpg.replace(".jpg", ".webp")}">'
        rf'<img src="images/construction/{jpg}" alt="\1" loading="lazy" decoding="async" width="800" height="600"></picture>'
    )
    return pattern.sub(repl, text)


def patch(text: str) -> str:
    text = HEAD_VIDEO_PRELOADS.sub("", text)
    text = text.replace(CSS_VIDEO_ONLY, CSS_POSTER_FIRST)
    text = HERO_BLOCK.sub(HERO_REPLACEMENT, text)
    text = text.replace(MONTAJ_BG_OLD, MONTAJ_BG_NEW)
    text = text.replace(
        'poster="images/montaj/montage-houses-poster.jpg"',
        'poster="images/montaj/montage-houses-poster.webp"',
    )
    for jpg in CARD_IMAGES:
        text = patch_montaj_card(text, jpg)
    return text


def main():
    for path in FILES:
        original = path.read_text(encoding="utf-8")
        updated = patch(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"patched {path.relative_to(ROOT)}")
        else:
            print(f"unchanged {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
