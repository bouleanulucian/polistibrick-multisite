#!/usr/bin/env python3
"""
Polistibrick Multi-site Build Script
-------------------------------------
Reads countries/[code]/_config.json and country HTML files,
copies shared assets, replaces {{placeholders}}, outputs to build/[code]/.

Usage:
    python3 build/build.py              # build all countries
    python3 build/build.py ro           # build only RO
    python3 build/build.py ro en fr     # build specific countries
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = ROOT / "countries"
SHARED_DIR = ROOT / "shared"
BUILD_DIR = ROOT / "build"
FALLBACK_COUNTRY = "ro"   # used when a country has only _config.json

PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")


def load_config(country_code: str) -> dict:
    cfg_path = COUNTRIES_DIR / country_code / "_config.json"
    if not cfg_path.exists():
        raise SystemExit(f"[ERROR] Missing config: {cfg_path}")
    with cfg_path.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_placeholder(key: str, config: dict) -> str:
    """Walk dotted path like 'contact.email_general' through config."""
    value = config
    for part in key.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return "{{" + key + "}}"  # leave un-resolved
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def apply_placeholders(text: str, config: dict) -> str:
    return PLACEHOLDER_RE.sub(lambda m: resolve_placeholder(m.group(1), config), text)


def copy_tree(src: Path, dst: Path, transform: bool, config: dict):
    """Copy src→dst. If transform=True, replace placeholders in .html/.css/.js."""
    if not src.exists():
        return
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if transform and item.suffix.lower() in {".html", ".css", ".js", ".xml", ".txt", ".json"}:
            try:
                content = item.read_text(encoding="utf-8")
                content = apply_placeholders(content, config)
                target.write_text(content, encoding="utf-8")
                continue
            except UnicodeDecodeError:
                pass  # fall through to binary copy
        shutil.copy2(item, target)


def generate_sitemap(out_dir: Path, config: dict):
    base = config.get("domain_url", "").rstrip("/")
    urls = []
    for html in out_dir.rglob("*.html"):
        rel = html.relative_to(out_dir).as_posix()
        if rel.endswith("/index.html"):
            rel = rel[:-10]
        elif rel == "index.html":
            rel = ""
        urls.append(f"{base}/{rel}")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(set(urls)):
        lines.append(f"  <url><loc>{u}</loc></url>")
    lines.append("</urlset>")
    (out_dir / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def generate_robots(out_dir: Path, config: dict):
    base = config.get("domain_url", "").rstrip("/")
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )
    (out_dir / "robots.txt").write_text(content, encoding="utf-8")


def build_country(code: str):
    config = load_config(code)
    out_dir = BUILD_DIR / code
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) shared assets → build/[code]/assets/ + images/
    copy_tree(SHARED_DIR / "css", out_dir / "assets" / "css", transform=True, config=config)
    copy_tree(SHARED_DIR / "js",  out_dir / "assets" / "js",  transform=True, config=config)
    copy_tree(SHARED_DIR / "images", out_dir / "images", transform=False, config=config)

    # 2) Country HTML (if missing, fall back to RO template)
    country_src = COUNTRIES_DIR / code
    html_files = [p for p in country_src.iterdir() if p.is_file() and p.suffix == ".html"]
    subfolders = [p for p in country_src.iterdir() if p.is_dir()]
    if not html_files and code != FALLBACK_COUNTRY:
        print(f"  [info] {code} has only _config.json → using {FALLBACK_COUNTRY} as template")
        copy_tree(COUNTRIES_DIR / FALLBACK_COUNTRY, out_dir, transform=True, config=config)
        # Remove the fallback's _config from output
    else:
        copy_tree(country_src, out_dir, transform=True, config=config)

    # Strip _config.json from output (not needed publicly)
    cfg_out = out_dir / "_config.json"
    if cfg_out.exists():
        cfg_out.unlink()

    # 3) sitemap + robots
    generate_sitemap(out_dir, config)
    generate_robots(out_dir, config)

    pages = sum(1 for _ in out_dir.rglob("*.html"))
    print(f"✓ {code:3} ({config.get('country_name','?')}) → {out_dir.relative_to(ROOT)} ({pages} pages)")


def main():
    codes = sys.argv[1:] or sorted(p.name for p in COUNTRIES_DIR.iterdir() if p.is_dir())
    print(f"\n→ Building {len(codes)} countries: {', '.join(codes)}\n")
    BUILD_DIR.mkdir(exist_ok=True)
    for code in codes:
        try:
            build_country(code)
        except SystemExit as e:
            print(e)
    print(f"\n✓ Done. Output: {BUILD_DIR.relative_to(ROOT)}/\n")


if __name__ == "__main__":
    main()
