#!/usr/bin/env python3
"""
Merge chunk_A + chunk_B JSON dicts into each lang.json (preserving first-pass entries).
First-pass keys take priority (they were hand-curated brand voice).
"""
import json
from pathlib import Path

OUT_DIR = Path("/Users/polistibrick/Desktop/polistibrick-multisite/translations")

LANGS = ["en", "fr", "it", "es", "nl", "de"]

for lang in LANGS:
    main_path = OUT_DIR / f"{lang}.json"
    chunk_a = OUT_DIR / f"{lang}_chunk_A.json"
    chunk_b = OUT_DIR / f"{lang}_chunk_B.json"
    main_data = json.loads(main_path.read_text(encoding="utf-8")) if main_path.exists() else {}
    a = json.loads(chunk_a.read_text(encoding="utf-8")) if chunk_a.exists() else {}
    b = json.loads(chunk_b.read_text(encoding="utf-8")) if chunk_b.exists() else {}
    before = len(main_data)
    # add chunks A and B but do NOT overwrite first-pass entries
    for src in (a, b):
        for k, v in src.items():
            if k not in main_data:
                main_data[k] = v
    after = len(main_data)
    main_path.write_text(json.dumps(main_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {lang}: {before} → {after} entries (+{after-before})")
