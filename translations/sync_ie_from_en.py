#!/usr/bin/env python3
"""
Sync countries/ie/ HTML from countries/en/ (same English content, IE config preserved).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IE_DIR = ROOT / "countries" / "ie"
EN_DIR = ROOT / "countries" / "en"


def main() -> None:
    cfg_path = IE_DIR / "_config.json"
    if not cfg_path.exists():
        raise SystemExit(f"Missing {cfg_path}")

    cfg_text = cfg_path.read_text(encoding="utf-8")
    lang = json.loads(cfg_text).get("lang", "en")

    for item in list(IE_DIR.iterdir()):
        if item.name == "_config.json":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    for item in EN_DIR.iterdir():
        if item.name == "_config.json":
            continue
        target = IE_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)

    cfg_path.write_text(cfg_text, encoding="utf-8")

    for html in IE_DIR.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        updated = text.replace('<html lang="en">', f'<html lang="{lang}">', 1)
        if updated != text:
            html.write_text(updated, encoding="utf-8")

    pages = sum(1 for _ in IE_DIR.rglob("*.html"))
    print(f"✓ Synced countries/ie/ from EN ({pages} HTML pages, config preserved)")


if __name__ == "__main__":
    main()
