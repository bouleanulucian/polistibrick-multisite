#!/usr/bin/env python3
"""Add WebM sources + data attrs for ZURU-style hero video boot."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = sorted((ROOT / "countries").glob("*/polistibrick-mercury-style.html"))

HERO_VIDEO = re.compile(
    r'(<video id="heroVideo" class="hero-bg-video" muted loop playsinline preload="none"\s+'
    r'poster="images/hero/hero-house-1\.webp"\s+'
    r'data-src-desktop="images/hero/hero-houses-reel-desktop\.mp4"\s+'
    r'data-src-mobile="images/hero/hero-houses-reel-mobile\.mp4")></video>'
)

HERO_REPLACEMENT = (
    '<video id="heroVideo" class="hero-bg-video" muted loop playsinline preload="none"\n'
    '           poster="images/hero/hero-house-1.webp"\n'
    '           data-src-desktop="images/hero/hero-houses-reel-desktop.mp4"\n'
    '           data-src-mobile="images/hero/hero-houses-reel-mobile.mp4"\n'
    '           data-src-desktop-webm="images/hero/hero-houses-reel-desktop.webm"\n'
    '           data-src-mobile-webm="images/hero/hero-houses-reel-mobile.webm"></video>'
)

CSS_POSTER_HIDE = """  .hero-bg video.hero-bg-video.is-playing {
    opacity: 1;
  }
  .hero-bg.is-video-playing .hero-bg-poster {
    opacity: 0;
    transition: opacity 0.45s ease;
  }"""

CSS_PLAYING_ONLY = """  .hero-bg video.hero-bg-video.is-playing {
    opacity: 1;
  }"""


def patch(text: str) -> str:
    text = HERO_VIDEO.sub(HERO_REPLACEMENT, text)
    if CSS_PLAYING_ONLY in text and ".is-video-playing" not in text:
        text = text.replace(CSS_PLAYING_ONLY, CSS_POSTER_HIDE)
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
