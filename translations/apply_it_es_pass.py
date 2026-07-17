#!/usr/bin/env python3
"""Second-pass IT/FR → ES replacements on countries/es HTML."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ES_DIR = ROOT / "countries" / "es"
TRANS = ROOT / "translations"

sys.path.insert(0, str(ROOT))
from translations.sync_fr_to_es import apply_dict, filter_mapping  # noqa: E402


def build_mapping() -> dict[str, str]:
    it_dict = json.loads((TRANS / "it.json").read_text(encoding="utf-8"))
    es_dict = json.loads((TRANS / "es.json").read_text(encoding="utf-8"))
    merged: dict[str, str] = {}
    for ro, it_val in it_dict.items():
        es_val = es_dict.get(ro)
        if it_val and es_val and it_val != es_val:
            merged[it_val] = es_val
    for name in (
        "fr_to_es.json",
        "mercury_fr_to_es.json",
        "extra_fr_to_es.json",
        "es_overrides.json",
        "remaining_fr_es.json",
        "es_it_manual_fixes.json",
    ):
        p = TRANS / name
        if p.exists():
            for k, v in json.loads(p.read_text(encoding="utf-8")).items():
                if k and v:
                    merged[k] = v
    return filter_mapping(merged)


def main() -> None:
    mapping = build_mapping()
    changed = 0
    for path in sorted(ES_DIR.rglob("*.html")):
        original = path.read_text(encoding="utf-8")
        text = original
        for _ in range(4):
            text = apply_dict(text, mapping)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    print(f"apply_it_es_pass: {len(mapping)} keys, updated {changed} files")


if __name__ == "__main__":
    main()
