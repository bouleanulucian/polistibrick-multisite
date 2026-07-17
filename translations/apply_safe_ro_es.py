#!/usr/bin/env python3
"""Apply safe RO→ES translations from es.json (long keys only, protects brands/urls)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from translations.sync_fr_to_es import apply_dict, filter_mapping

ES_DIR = ROOT / "countries" / "es"
ES_JSON = ROOT / "translations" / "es.json"


def main() -> None:
    mapping = filter_mapping(json.loads(ES_JSON.read_text(encoding="utf-8")))
    changed = 0
    for path in sorted(ES_DIR.rglob("*.html")):
        original = path.read_text(encoding="utf-8")
        text = original
        for _ in range(2):
            text = apply_dict(text, mapping)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    print(f"apply_safe_ro_es: updated {changed} files ({len(mapping)} keys)")


if __name__ == "__main__":
    main()
