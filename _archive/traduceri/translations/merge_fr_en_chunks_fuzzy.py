#!/usr/bin/env python3
"""Fuzzy-match missing FR phrases to translated_chunk FR→EN pairs."""
from __future__ import annotations

import json
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
CHUNKS = TRANS / "chunks"
THRESHOLD = 0.85


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


def load_chunk_pairs() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for chunk_file in sorted(CHUNKS.glob("translated_chunk_*.json")):
        chunk = json.loads(chunk_file.read_text(encoding="utf-8"))
        for _ro, targets in chunk.items():
            if isinstance(targets, dict):
                fr = targets.get("fr", "").strip()
                en = targets.get("en", "").strip()
                if fr and en and fr != en:
                    pairs.append((fr, en))
    return pairs


def main() -> None:
    extra_path = TRANS / "extra_fr_to_en.json"
    extra = json.loads(extra_path.read_text(encoding="utf-8"))
    missing_path = TRANS / "missing_fr_source_en.json"
    remaining_path = TRANS / "remaining_fr_en.json"
    targets: set[str] = set()
    if missing_path.exists():
        targets |= set(json.loads(missing_path.read_text(encoding="utf-8")).keys())
    if remaining_path.exists():
        targets |= set(json.loads(remaining_path.read_text(encoding="utf-8")).keys())
    pairs = load_chunk_pairs()
    print(f"Chunk pairs: {len(pairs)}, targets: {len(targets)}")

    added = 0
    for fr_phrase in targets:
        if fr_phrase in extra and extra[fr_phrase]:
            continue
        best_ratio, best_en = 0.0, None
        for chunk_fr, chunk_en in pairs:
            ratio = SequenceMatcher(None, fr_phrase, chunk_fr).ratio()
            if ratio > best_ratio:
                best_ratio, best_en = ratio, chunk_en
            # also try if one contains the other
            if len(fr_phrase) > 40 and len(chunk_fr) > 40:
                if fr_phrase in chunk_fr or chunk_fr in fr_phrase:
                    sub_ratio = min(len(fr_phrase), len(chunk_fr)) / max(len(fr_phrase), len(chunk_fr))
                    if sub_ratio > best_ratio:
                        best_ratio, best_en = sub_ratio, chunk_en
        if best_en and best_ratio >= THRESHOLD:
            extra[fr_phrase] = britishise(best_en)
            added += 1

    extra_path.write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fuzzy added: {added}, extra total: {len(extra)}")


if __name__ == "__main__":
    main()
