#!/usr/bin/env python3
"""Multi-pass FR → IT replacements on countries/it HTML."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IT_DIR = ROOT / "countries" / "it"
TRANS = ROOT / "translations"

sys.path.insert(0, str(ROOT))
from translations.sync_fr_to_es import apply_dict, filter_mapping  # noqa: E402


def load_mercury_py() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location(
        "tm", TRANS / "translate_mercury_it.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TRANSLATIONS


def build_mapping() -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in (
        "fr_to_it.json",
        "mercury_fr_to_it.json",
        "extra_fr_to_it.json",
        "remaining_fr_it.json",
        "pass3_fr_to_it.json",
        "it_chunk_A.json",
        "it_chunk_B.json",
    ):
        p = TRANS / name
        if not p.exists():
            continue
        for k, v in json.loads(p.read_text(encoding="utf-8")).items():
            if k and v:
                merged[k] = v
    for k, v in load_mercury_py().items():
        if k and v:
            merged[k] = v
    return filter_mapping(merged)


def main() -> None:
    mapping = build_mapping()
    changed = 0
    total_replacements = 0
    for path in sorted(IT_DIR.rglob("*.html")):
        original = path.read_text(encoding="utf-8")
        text = original
        for _ in range(5):
            text = apply_dict(text, mapping)
        if text != original:
            # rough replacement count
            total_replacements += sum(
                1 for k, v in mapping.items() if k in original and v in text and k not in text
            )
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  ✓ {path.relative_to(IT_DIR)}")
    print(f"\napply_fr_to_it_pass: {len(mapping)} keys, updated {changed} files")


if __name__ == "__main__":
    main()
