#!/usr/bin/env python3
"""Apply translations/es_overrides.json to countries/es HTML (safe: protects href/src + brands)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from translations.sync_fr_to_es import apply_dict

ES_DIR = ROOT / "countries" / "es"
OVERRIDES = ROOT / "translations" / "es_overrides.json"


def main() -> None:
    mapping = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    changed = 0
    for path in sorted(ES_DIR.rglob("*.html")):
        original = path.read_text(encoding="utf-8")
        text = original
        for _ in range(3):
            text = apply_dict(text, mapping)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    print(f"apply_es_overrides: updated {changed} files ({len(mapping)} keys)")


if __name__ == "__main__":
    main()
