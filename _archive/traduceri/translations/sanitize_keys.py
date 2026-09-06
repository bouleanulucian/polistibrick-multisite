#!/usr/bin/env python3
"""Remove translation keys that cause substring corruption (e.g. 'an' → 'year' breaks 'lang')."""
import json
from pathlib import Path

TRANS = Path(__file__).resolve().parent
BLOCKLIST = {"an", "zi", "ore", "ani"}  # only keys that corrupt HTML (e.g. lang→lyearg)

for path in TRANS.glob("*.json"):
    if path.name in ("ui_strings.json",) or path.name.startswith(
        ("fr_to_", "mercury_", "remaining_", "still_", "extra_", "missing_", "phrases_")
    ):
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    removed = [k for k in list(data) if k in BLOCKLIST]
    for k in removed:
        del data[k]
    if removed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {path.name}: removed {removed}")
