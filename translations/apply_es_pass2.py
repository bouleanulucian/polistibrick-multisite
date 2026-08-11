#!/usr/bin/env python3
"""Apply pass2 FR→ES batch to countries/es/ HTML and merge into extra_fr_to_es.json."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
ES_DIR = ROOT / "countries" / "es"

sys.path.insert(0, str(ROOT))
from translations.sync_fr_to_es import apply_dict, filter_mapping  # noqa: E402


def load_py_batch(name: str) -> dict[str, str]:
    path = TRANS / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return dict(mod.BATCH)


def load_json(name: str) -> dict[str, str]:
    p = TRANS / name
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if k and v}


def main() -> None:
    merged: dict[str, str] = {}
    for name in (
        "fr_to_es.json",
        "mercury_fr_to_es.json",
        "extra_fr_to_es.json",
        "es_overrides.json",
        "es_it_manual_fixes.json",
    ):
        merged.update(load_json(name))

    merged.update(load_py_batch("batch_fr_es_2026-08-10.py"))
    merged.update(load_py_batch("batch_fr_es_pass2.py"))

    mapping = filter_mapping(merged)
    extra_path = TRANS / "extra_fr_to_es.json"
    extra = load_json("extra_fr_to_es.json")
    extra.update(load_py_batch("batch_fr_es_2026-08-10.py"))
    extra.update(load_py_batch("batch_fr_es_pass2.py"))
    extra_path.write_text(
        json.dumps(dict(sorted(extra.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    changed = 0
    total_replacements = 0
    for f in sorted(ES_DIR.rglob("*.html")):
        original = f.read_text(encoding="utf-8")
        text = original
        for _ in range(5):
            text = apply_dict(text, mapping)
        if text != original:
            # rough count: chars diff / avg key len heuristic — count actual batch hits
            hits = sum(1 for k, v in mapping.items() if k in original and v and k != v)
            total_replacements += hits
            f.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  ✓ {f.relative_to(ES_DIR)} (~{hits} keys matched)")

    print(f"\napply_es_pass2: {len(mapping)} keys in mapping, {len(extra)} in extra_fr_to_es.json")
    print(f"Updated {changed} files, ~{total_replacements} key matches in changed files")


if __name__ == "__main__":
    main()
