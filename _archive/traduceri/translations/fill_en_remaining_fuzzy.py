#!/usr/bin/env python3
"""Fill extra_fr_to_en.json from remaining phrases via fr.json → en.json bridge + fuzzy match."""
from __future__ import annotations

import json
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"


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
        ("labor", "labour"),
        ("Labor", "Labour"),
        ("modeling", "modelling"),
        ("Modeling", "Modelling"),
    )
    for a, b in repl:
        text = text.replace(a, b)
    return text


def main() -> None:
    fr_dict = json.loads((TRANS / "fr.json").read_text(encoding="utf-8"))
    en_dict = json.loads((TRANS / "en.json").read_text(encoding="utf-8"))
    fr_to_ro = {v: k for k, v in fr_dict.items() if v}
    extra_path = TRANS / "extra_fr_to_en.json"
    extra = json.loads(extra_path.read_text(encoding="utf-8"))
    remaining_path = TRANS / "remaining_fr_en.json"
    remaining = json.loads(remaining_path.read_text(encoding="utf-8")) if remaining_path.exists() else {}

    added_exact = added_fuzzy = 0
    for fr_phrase in remaining:
        if fr_phrase in extra and extra[fr_phrase]:
            continue
        ro = fr_to_ro.get(fr_phrase)
        if ro and ro in en_dict and en_dict[ro] and en_dict[ro] != fr_phrase:
            extra[fr_phrase] = britishise(en_dict[ro])
            added_exact += 1
            continue
        best_ratio, best_ro = 0.0, None
        for fv, rk in fr_to_ro.items():
            if len(fv) < 10:
                continue
            ratio = SequenceMatcher(None, fr_phrase, fv).ratio()
            if ratio > best_ratio:
                best_ratio, best_ro = ratio, rk
        if best_ratio >= 0.90 and best_ro and best_ro in en_dict and en_dict[best_ro]:
            extra[fr_phrase] = britishise(en_dict[best_ro])
            added_fuzzy += 1

    extra_path.write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added exact: {added_exact}, fuzzy: {added_fuzzy}, extra total: {len(extra)}")


if __name__ == "__main__":
    main()
