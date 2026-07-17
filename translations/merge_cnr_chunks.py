#!/usr/bin/env python3
"""Merge cnr_chunk_*.json translated files into extra_ro_to_cnr.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"


def main() -> None:
    merged: dict[str, str] = {}
    for path in sorted(TRANS.glob("cnr_chunk_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for k, v in data.items():
            if k and v and v.strip():
                merged[k] = v.strip()
    out = TRANS / "extra_ro_to_cnr.json"
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Merged {len(merged)} translations -> {out}")


if __name__ == "__main__":
    main()
