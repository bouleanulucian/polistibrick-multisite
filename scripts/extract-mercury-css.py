#!/usr/bin/env python3
"""Extract inline <style> blocks from mercury homepage → shared/css/mercury-home.css"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "countries" / "ro" / "polistibrick-mercury-style.html"
OUT_CSS = ROOT / "shared" / "css" / "mercury-home.css"
LINK = '<link rel="stylesheet" href="assets/css/mercury-home.css?v=1">\n'

STYLE_RE = re.compile(r"<style>\s*(.*?)\s*</style>", re.DOTALL)


def extract_styles(html: str) -> tuple[str, str]:
    chunks: list[str] = []

    def collect(m: re.Match) -> str:
        chunks.append(m.group(1).strip())
        return ""

    body = STYLE_RE.sub(collect, html)
    css = "\n\n/* --- section --- */\n\n".join(chunks)
    return body, css


def inject_link(html: str) -> str:
    if "mercury-home.css" in html:
        return html
    marker = '<link rel="preload" as="image" href="images/hero/hero-house-1.webp"'
    if marker in html:
        idx = html.find(">", html.find(marker)) + 1
        return html[:idx] + "\n" + LINK + html[idx:]
    return html.replace("</head>", LINK + "</head>", 1)


def patch_mercury_file(path: Path, css_link_only: bool = False) -> None:
    html = path.read_text(encoding="utf-8")
    if css_link_only:
        html = inject_link(html)
        html = STYLE_RE.sub("", html)
    else:
        html, _ = extract_styles(html)
        html = inject_link(html)
    path.write_text(html, encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing {SOURCE}")

    html = SOURCE.read_text(encoding="utf-8")
    stripped, css = extract_styles(html)
    OUT_CSS.write_text(css + "\n", encoding="utf-8")
    print(f"✓ {OUT_CSS.relative_to(ROOT)} ({len(css) // 1024} KB)")

    for path in sorted(ROOT.glob("countries/*/polistibrick-mercury-style.html")):
        if path == SOURCE:
            stripped = inject_link(stripped)
            path.write_text(stripped, encoding="utf-8")
        else:
            patch_mercury_file(path, css_link_only=True)
        print(f"✓ {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
