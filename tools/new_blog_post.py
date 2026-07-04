#!/usr/bin/env python3
"""
Generează un articol blog RO din JSON.

Usage:
  python3 tools/new_blog_post.py drafts/blog/exemplu.json
  python3 tools/new_blog_post.py drafts/blog/exemplu.json --publish

JSON fields:
  slug, title, meta_desc, category, date (YYYY-MM-DD),
  headline (HTML ok with <em>), lead, hero_image, hero_alt,
  read_min (int), watermark (optional), content_html (string)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "templates" / "blog-article.html"
OUT_BASE = ROOT / "countries" / "ro" / "resurse" / "blog"
DRAFTS = ROOT / "drafts" / "blog"
LISTING = OUT_BASE / "index.html"


def slug_ok(s: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s))


def render(data: dict) -> str:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    repl = {
        "{{TITLE}}": data["title"],
        "{{META_DESC}}": data["meta_desc"],
        "{{CATEGORY}}": data["category"],
        "{{DATE}}": data["date"],
        "{{READ_MIN}}": str(data.get("read_min", 5)),
        "{{WATERMARK}}": data.get("watermark", "Articole"),
        "{{HEADLINE}}": data["headline"],
        "{{LEAD}}": data["lead"],
        "{{HERO_IMAGE}}": data["hero_image"],
        "{{HERO_ALT}}": data.get("hero_alt", data["title"]),
        "{{CONTENT_HTML}}": data["content_html"].strip(),
    }
    out = tpl
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


def update_listing_card(slug: str, data: dict) -> None:
    """Înlocuiește primul card „În curând” cu același titlu sau adaugă link pe slug."""
    if not LISTING.exists():
        return
    text = LISTING.read_text(encoding="utf-8")
    href = f"./{slug}/"
    title_plain = re.sub(r"<[^>]+>", "", data["headline"])
    # Link card care conține titlul (fără tag-uri)
    pattern = rf'(<h3[^>]*>){re.escape(title_plain)}(</h3>.*?<a )href="#"([^>]*>)(În curând|En cours)(</a>)'
    if re.search(pattern, text, re.DOTALL):
        text = re.sub(
            pattern,
            rf'\1{title_plain}\2href="{href}"\3Citește articolul →\4',
            text,
            count=1,
            flags=re.DOTALL,
        )
        LISTING.write_text(text, encoding="utf-8")
        return
    # fallback: primul „În curând”
    old = '<a href="#" style="color:var(--gray);font-weight:600;font-size:13px;cursor:default;">În curând</a>'
    new = f'<a href="{href}" style="color:var(--red);font-weight:600;font-size:13px;">Citește articolul →</a>'
    if old in text:
        text = text.replace(old, new, 1)
        LISTING.write_text(text, encoding="utf-8")


def main() -> None:
    publish = "--publish" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("Usage: python3 tools/new_blog_post.py <draft.json> [--publish]")
        sys.exit(1)

    src = Path(args[0])
    if not src.is_absolute():
        src = ROOT / src
    if not src.exists():
        print(f"❌ Nu găsesc: {src}")
        sys.exit(1)

    data = json.loads(src.read_text(encoding="utf-8"))
    slug = data.get("slug", "").strip()
    if not slug_ok(slug):
        print("❌ slug invalid (ex: ce-este-casa-passiva)")
        sys.exit(1)

    required = ("title", "meta_desc", "category", "date", "headline", "lead", "hero_image", "content_html")
    missing = [k for k in required if not data.get(k)]
    if missing:
        print(f"❌ Câmpuri lipsă: {', '.join(missing)}")
        sys.exit(1)

    html = render(data)
    if publish:
        out_dir = OUT_BASE / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        update_listing_card(slug, data)
        print(f"✓ Publicat: countries/ro/resurse/blog/{slug}/index.html")
        print("  Rulează: python3 build/build.py ro")
    else:
        DRAFTS.mkdir(parents=True, exist_ok=True)
        draft_html = DRAFTS / f"{slug}.html"
        draft_html.write_text(html, encoding="utf-8")
        print(f"✓ Draft: {draft_html.relative_to(ROOT)}")
        print("  Aprobă cu: python3 tools/new_blog_post.py drafts/blog/{slug}.json --publish".format(slug=slug))


if __name__ == "__main__":
    main()
