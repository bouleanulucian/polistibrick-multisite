#!/usr/bin/env python3
"""Split phrases_ro_for_cnr.json into chunk files for parallel translation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "translations" / "phrases_ro_for_cnr.json"
CHUNK_SIZE = 400


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    items = list(data.items())
    for i in range(0, len(items), CHUNK_SIZE):
        chunk = dict(items[i : i + CHUNK_SIZE])
        n = i // CHUNK_SIZE + 1
        out = ROOT / "translations" / f"cnr_chunk_{n}.json"
        out.write_text(json.dumps(chunk, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {out.name}: {len(chunk)} phrases")


if __name__ == "__main__":
    main()
