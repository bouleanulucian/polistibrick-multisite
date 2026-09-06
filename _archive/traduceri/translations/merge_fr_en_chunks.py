#!/usr/bin/env python3
"""Merge FR→EN pairs from translated_chunk_*.json into extra_fr_to_en.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
CHUNKS = TRANS / "chunks"


def britishise(text: str) -> str:
    repl = (
        ("personalized", "personalised"),
        ("Personalized", "Personalised"),
        ("recognized", "recognised"),
        ("Recognized", "Recognised"),
        ("organization", "organisation"),
        ("Organization", "Organisation"),
        ("center", "centre"),
        ("Center", "Centre"),
        ("behavior", "behaviour"),
        ("Behavior", "Behaviour"),
        ("authorization", "authorisation"),
        ("Authorization", "Authorisation"),
    )
    for a, b in repl:
        text = text.replace(a, b)
    return text


def main() -> None:
    extra_path = TRANS / "extra_fr_to_en.json"
    extra = json.loads(extra_path.read_text(encoding="utf-8"))
    added = 0
    for chunk_file in sorted(CHUNKS.glob("translated_chunk_*.json")):
        chunk = json.loads(chunk_file.read_text(encoding="utf-8"))
        for _ro, targets in chunk.items():
            if not isinstance(targets, dict):
                continue
            fr = targets.get("fr", "").strip()
            en = targets.get("en", "").strip()
            if fr and en and fr != en and fr not in extra:
                extra[fr] = britishise(en)
                added += 1
            elif fr and en and fr != en:
                extra[fr] = britishise(en)

    extra_path.write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added {added} new FR→EN pairs; extra total {len(extra)}")


if __name__ == "__main__":
    main()
