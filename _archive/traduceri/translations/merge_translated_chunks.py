#!/usr/bin/env python3
"""Merge translated_chunk_*.json into translations/{lang}.json and re-apply."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
CHUNKS = TRANS / "chunks"


def merge():
    langs = ["en", "fr", "it", "es", "nl", "de"]
    for lang in langs:
        data = json.loads((TRANS / f"{lang}.json").read_text(encoding="utf-8"))
        added = 0
        for chunk_file in sorted(CHUNKS.glob("translated_chunk_*.json")):
            chunk = json.loads(chunk_file.read_text(encoding="utf-8"))
            for ro, targets in chunk.items():
                if lang in targets and targets[lang]:
                    if ro not in data:
                        added += 1
                    data[ro] = targets[lang]
        (TRANS / f"{lang}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  {lang}: merged (+{added} new, total {len(data)})")


def main():
    merge()
    langs = sys.argv[1:] if len(sys.argv) > 1 else ["en", "it", "es", "nl", "de", "ie", "fr"]
    for lang in langs:
        subprocess.run(
            ["python3", str(TRANS / "apply_lang.py"), lang if lang != "ie" else "ie"],
            cwd=ROOT,
            check=False,
        )
    # IE uses en.json copy
    if "ie" in langs:
        ie_json = TRANS / "ie.json"
        ie_json.write_text((TRANS / "en.json").read_text(encoding="utf-8"), encoding="utf-8")
        subprocess.run(["python3", str(TRANS / "apply_lang.py"), "ie"], cwd=ROOT)


if __name__ == "__main__":
    main()
