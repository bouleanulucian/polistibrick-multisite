#!/usr/bin/env python3
"""
Build complete FR → target mappings by bridging through RO keys in fr.json + {lang}.json,
plus direct extraction of French phrases from countries/fr/ HTML.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FR_DIR = ROOT / "countries" / "fr"
TRANS = ROOT / "translations"
LANGS = ["en", "it", "es", "nl", "de"]

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")


def extract_fr_segments(html: str) -> list[str]:
    cleaned = SKIP.sub(" ", html)
    return [p.strip() for p in TAG.split(cleaned) if 3 <= len(p.strip()) <= 400]


def build_mapping(lang: str) -> dict[str, str]:
    fr_dict = json.loads((TRANS / "fr.json").read_text(encoding="utf-8"))
    lang_path = TRANS / f"{lang}.json"
    if not lang_path.exists() and lang == "ie":
        lang_path = TRANS / "en.json"
    lang_dict = json.loads(lang_path.read_text(encoding="utf-8"))

    mapping: dict[str, str] = {}
    # RO key bridge
    for ro, fr_val in fr_dict.items():
        if not fr_val or ro not in lang_dict:
            continue
        target = lang_dict[ro]
        if target and fr_val != target:
            mapping[fr_val] = target

    # FR value → RO reverse lookup for extracted phrases
    fr_to_ro = {v: k for k, v in fr_dict.items() if v}
    fr_phrases: set[str] = set()
    for html in FR_DIR.rglob("*.html"):
        fr_phrases.update(extract_fr_segments(html.read_text(encoding="utf-8")))

    for fr_phrase in fr_phrases:
        if fr_phrase in mapping:
            continue
        ro = fr_to_ro.get(fr_phrase)
        if ro and ro in lang_dict:
            target = lang_dict[ro]
            if target and fr_phrase != target:
                mapping[fr_phrase] = target

    return mapping


def main():
    for lang in LANGS + ["ie"]:
        m = build_mapping(lang if lang != "ie" else "en")
        out = TRANS / f"fr_to_{lang if lang != 'ie' else 'en'}.json"
        out.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {lang}: {len(m)} FR→{lang} entries → {out.name}")


if __name__ == "__main__":
    main()
