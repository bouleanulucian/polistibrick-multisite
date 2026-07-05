#!/usr/bin/env python3
"""
Copy the complete RO site into another country folder (keeps existing _config.json).

Usage:
    python3 translations/seed_from_ro.py en it es nl de ie
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "countries" / "ro"


def seed(code: str) -> None:
    dest = ROOT / "countries" / code
    cfg_path = dest / "_config.json"
    if not cfg_path.exists():
        raise SystemExit(f"[ERROR] Missing {cfg_path} — create _config.json first.")

    cfg_text = cfg_path.read_text(encoding="utf-8")
    lang = json.loads(cfg_text).get("lang", code)

    for item in list(dest.iterdir()):
        if item.name == "_config.json":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    for item in TEMPLATE.iterdir():
        if item.name == "_config.json":
            continue
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)

    cfg_path.write_text(cfg_text, encoding="utf-8")

    for html in dest.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        updated = text.replace('<html lang="ro">', f'<html lang="{lang}">', 1)
        if updated != text:
            html.write_text(updated, encoding="utf-8")

    pages = sum(1 for _ in dest.rglob("*.html"))
    print(f"✓ Seeded countries/{code}/ from RO ({pages} HTML pages, lang={lang})")


def main():
    codes = sys.argv[1:]
    if not codes:
        print("Usage: python3 translations/seed_from_ro.py <country-code> [...]")
        sys.exit(1)
    for code in codes:
        seed(code)
    print()


if __name__ == "__main__":
    main()
