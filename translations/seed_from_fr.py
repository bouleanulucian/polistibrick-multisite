#!/usr/bin/env python3
"""
Copy the complete FR site into another country folder (keeps existing _config.json).

Usage:
    python3 translations/seed_from_fr.py en
    python3 translations/seed_from_fr.py en it es nl de ie

Then:
    python3 translations/extract_fr_phrases.py > translations/phrases_fr_source.txt
    # translate phrases → translations/{lang}.json
    python3 translations/apply_lang.py en
    python3 build/build.py en
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "countries" / "fr"


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
        # Images/videos/GLBs live in shared/ — do not multiply per country
        if item.name == "images":
            continue
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)

    cfg_path.write_text(cfg_text, encoding="utf-8")

    for html in dest.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        updated = text.replace('<html lang="fr">', f'<html lang="{lang}">', 1)
        if updated != text:
            html.write_text(updated, encoding="utf-8")

    pages = sum(1 for _ in dest.rglob("*.html"))
    print(f"✓ Seeded countries/{code}/ from FR ({pages} HTML pages, lang={lang})")
    print(f"  1. Extract phrases:  python3 translations/extract_fr_phrases.py")
    print(f"  2. Translate →       translations/{code}.json  (FR text as keys)")
    print(f"  3. Apply:             python3 translations/apply_lang.py {code}")
    print(f"  4. Build:             python3 build/build.py {code}")


def main():
    codes = sys.argv[1:]
    if not codes:
        print("Usage: python3 translations/seed_from_fr.py <country-code> [...]")
        sys.exit(1)
    for code in codes:
        seed(code)
    print()


if __name__ == "__main__":
    main()
