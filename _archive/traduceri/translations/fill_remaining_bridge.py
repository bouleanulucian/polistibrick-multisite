#!/usr/bin/env python3
"""Auto-fill remaining FR phrases using RO key bridge (fr.json values → lang.json)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
LANGS = ["en", "it", "es", "nl", "de"]


def fill(lang: str) -> int:
    lang_key = "en" if lang == "ie" else lang
    remaining_path = TRANS / f"remaining_fr_{lang_key}.json"
    if not remaining_path.exists():
        return 0

    fr_dict = json.loads((TRANS / "fr.json").read_text(encoding="utf-8"))
    lang_dict = json.loads((TRANS / f"{lang_key}.json").read_text(encoding="utf-8"))
    fr_to_ro = {v: k for k, v in fr_dict.items() if v}

    remaining = json.loads(remaining_path.read_text(encoding="utf-8"))
    extra_path = TRANS / f"extra_fr_to_{lang_key}.json"
    extra = json.loads(extra_path.read_text(encoding="utf-8")) if extra_path.exists() else {}

    filled = 0
    still_empty = {}
    for fr_phrase, _ in remaining.items():
        if fr_phrase in extra and extra[fr_phrase]:
            continue
        ro = fr_to_ro.get(fr_phrase)
        if ro and ro in lang_dict:
            target = lang_dict[ro]
            if target and fr_phrase != target:
                extra[fr_phrase] = target
                filled += 1
                continue
        still_empty[fr_phrase] = ""

    extra_path.write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8")
    still_path = TRANS / f"still_missing_fr_{lang_key}.json"
    still_path.write_text(json.dumps(still_empty, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {lang_key}: filled {filled}, still missing {len(still_empty)}")
    return len(still_empty)


if __name__ == "__main__":
    for lang in LANGS + ["ie"]:
        fill(lang)
