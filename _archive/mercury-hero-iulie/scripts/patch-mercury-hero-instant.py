#!/usr/bin/env python3
"""Hero video instant start: head preload, no fade, native poster only."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = sorted((ROOT / "countries").glob("*/polistibrick-mercury-style.html"))

HEAD_OLD = '<link rel="preload" as="image" href="images/hero/hero-house-1.webp" type="image/webp">'
HEAD_NEW = """<link rel="preload" as="image" href="images/hero/hero-house-1.webp" type="image/webp" fetchpriority="high">
<link rel="preload" as="video" href="images/hero/hero-houses-reel-mobile.mp4" type="video/mp4" media="(max-width: 809px)">
<link rel="preload" as="video" href="images/hero/hero-houses-reel-desktop.mp4" type="video/mp4" media="(min-width: 810px)">"""

CSS_OLD = re.compile(
    r"  \.hero-bg-poster \{[^}]+\}\n"
    r"  \.hero-bg-poster img \{[^}]+\}\n"
    r"  \.hero-bg video\.hero-bg-video \{[^}]+\}\n"
    r"  \.hero-bg video\.hero-bg-video\.is-playing \{[^}]+\}\n"
    r"  \.hero-bg\.is-video-playing \.hero-bg-poster \{[^}]+\}\n",
    re.MULTILINE,
)
CSS_NEW = """  .hero-bg video.hero-bg-video {
    z-index: 1;
    opacity: 1;
    background: #14120F;
  }
"""

HERO_BLOCK_OLD = re.compile(
    r'    <picture class="hero-bg-poster">\n'
    r'      <source type="image/webp" srcset="images/hero/hero-house-1\.webp">\n'
    r'      <img src="images/hero/hero-house-1\.jpg" alt="" width="1920" height="1080" decoding="async" fetchpriority="high">\n'
    r'    </picture>\n'
    r'    <video id="heroVideo" class="hero-bg-video"[^>]*>.*?</video>\n',
    re.DOTALL,
)
HERO_BLOCK_NEW = """    <video id="heroVideo" class="hero-bg-video" muted loop playsinline autoplay preload="auto"
           poster="images/hero/hero-house-1.webp">
      <source src="images/hero/hero-houses-reel-mobile.mp4" media="(max-width: 809px)" type="video/mp4">
      <source src="images/hero/hero-houses-reel-desktop.mp4" type="video/mp4">
    </video>
"""

REVEAL_SCRIPT = re.compile(
    r"<script>\n\(function \(\) \{\n"
    r"  if \(window\.matchMedia\('\(prefers-reduced-motion: reduce\)'\)\.matches\) return;\n"
    r"  var v = document\.getElementById\('heroVideo'\);\n"
    r"  var bg = v && v\.closest\('\.hero-bg'\);\n"
    r"  if \(!v \|\| !bg\) return;\n"
    r"  function revealVideo\(\) \{[^}]+\}\n"
    r"  v\.addEventListener\('playing', revealVideo\);\n"
    r"  if \(!v\.paused && v\.currentTime > 0\) revealVideo\(\);\n"
    r"  else \{\n"
    r"    var p = v\.play\(\);\n"
    r"    if \(p && p\.then\) p\.then\(revealVideo\)\.catch\(function \(\) \{\}\);\n"
    r"  \}\n"
    r"\}\)\(\);\n"
    r"</script>\n",
    re.MULTILINE,
)


def patch(text: str) -> str:
    if HEAD_OLD in text:
        text = text.replace(HEAD_OLD, HEAD_NEW)
    text = CSS_OLD.sub(CSS_NEW, text)
    text = HERO_BLOCK_OLD.sub(HERO_BLOCK_NEW, text)
    text = REVEAL_SCRIPT.sub("", text)
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
