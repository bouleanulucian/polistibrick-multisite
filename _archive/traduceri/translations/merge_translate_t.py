#!/usr/bin/env python3
"""Merge translate.py T dict into translations/{lang}.json files."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"

spec = importlib.util.spec_from_file_location("tr", TRANS / "translate.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
T = mod.T

for lang in ["en", "fr", "it", "es", "nl", "de"]:
    path = TRANS / f"{lang}.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    added = 0
    for ro, targets in T.items():
        if lang in targets and ro not in data:
            data[ro] = targets[lang]
            added += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {lang}: +{added} entries (total {len(data)})")
