#!/usr/bin/env python3
"""Passive section: single static winter image, no season slideshow."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = sorted((ROOT / "countries").glob("*/polistibrick-mercury-style.html"))

COPY = {
    "ro": (
        "Casă Polistibrick iarna: confort constant în interior",
        "Vederea din living iarna — confort constant",
    ),
    "fr": (
        "Maison Polistibrick en hiver : confort constant à l'intérieur",
        "Vue depuis le salon en hiver — confort constant",
    ),
}
DEFAULT = (
    "Polistibrick home in winter: constant indoor comfort",
    "Living room view in winter — constant comfort",
)

CSS_OLD = """  /* Slideshow 4 saisons — fondu enchaîné, 1,5 s par image */
  .passif-slides { position: relative; width: 100%; aspect-ratio: 16 / 9; overflow: hidden; }
  .passif-slides .ps {
    position: absolute; inset: 0; width: 100%; height: 100%;
    object-fit: cover; opacity: 0;
    transition: opacity .9s ease-in-out; will-change: opacity;
  }
  .passif-slides .ps.active { opacity: 1; }
  /* Prim-plan fix: intérieur identique, seul le paysage derrière la vitre change */"""

CSS_NEW = """  /* Iarnă statică — fără slideshow, fără video */
  .passif-slides { position: relative; width: 100%; aspect-ratio: 16 / 9; overflow: hidden; }
  .passif-slides .passif-bg {
    position: absolute; inset: 0; width: 100%; height: 100%;
    object-fit: cover; object-position: center;
  }
  /* Prim-plan fix: interior identic */"""

SLIDES_RE = re.compile(
    r'    <div class="passif-slides" aria-label="[^"]*">\n'
    r'(?:      <img class="ps[^"]*"[^>]*>\n){4}'
    r'      <img class="passif-fg"[^>]*>\n'
    r"    </div>",
    re.MULTILINE,
)

SCRIPT_RE = re.compile(
    r'\n  <script>\(function\(\)\{var s=document\.querySelectorAll\(\'#passif \.ps\'\);[^<]+</script>',
    re.MULTILINE,
)


def patch_file(path: Path) -> bool:
    code = path.parent.name
    aria, alt = COPY.get(code, DEFAULT)
    text = path.read_text(encoding="utf-8")
    original = text

    block = (
        f'    <div class="passif-slides" aria-label="{aria}">\n'
        f'      <img class="passif-bg" src="images/passive/passive-winter.jpg?v=4" alt="{alt}" loading="lazy">\n'
        f'      <img class="passif-fg" src="images/passive/passive-interior-fg.png?v=3" alt="" aria-hidden="true" loading="lazy">\n'
        f"    </div>"
    )
    text = SLIDES_RE.sub(block, text)
    text = SCRIPT_RE.sub("", text)
    if CSS_OLD in text:
        text = text.replace(CSS_OLD, CSS_NEW)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    for path in FILES:
        if patch_file(path):
            print(f"patched {path.relative_to(ROOT)}")
        else:
            print(f"unchanged {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
