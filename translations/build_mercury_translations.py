#!/usr/bin/env python3
"""Build FR→lang mercury translations from translate_mercury_ro.py + lang JSON files."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
LANGS = ["en", "it", "es", "nl", "de"]


def load_mercury_fr_ro() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location(
        "tmr", TRANS / "translate_mercury_ro.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fr_ro = dict(mod.TRANSLATIONS)
    fr_json = json.loads((TRANS / "fr.json").read_text(encoding="utf-8"))
    for ro, fr in fr_json.items():
        if fr and ro and fr != ro and fr not in fr_ro:
            fr_ro[fr] = ro
    return fr_ro


def build_all():
    fr_ro = load_mercury_fr_ro()
    for lang in LANGS:
        lang_dict = json.loads((TRANS / f"{lang}.json").read_text(encoding="utf-8"))
        mapping = {}
        for fr, ro in fr_ro.items():
            if ro in lang_dict:
                target = lang_dict[ro]
                if target and fr != target:
                    mapping[fr] = target
        out = TRANS / f"mercury_fr_to_{lang}.json"
        out.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {lang}: {len(mapping)} mercury entries → {out.name}")


if __name__ == "__main__":
    build_all()
