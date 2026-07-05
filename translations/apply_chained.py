#!/usr/bin/env python3
"""
Chain-apply translations:
1. Apply en.json (RO → EN-mixed) to target country HTML
2. Then apply target_lang.json (EN-mixed → target_lang)

This works because our chunks were translated from the EN-modified phrase list,
so target language dicts have keys like "House în 4 weeks" rather than pure RO.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = ROOT / "countries"
TRANSLATIONS_DIR = ROOT / "translations"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)


def apply_dict(text: str, translations: dict) -> str:
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)
    segments = []
    last_end = 0
    for m in SKIP_REGEX.finditer(text):
        segments.append(("translate", text[last_end:m.start()]))
        segments.append(("skip", m.group(0)))
        last_end = m.end()
    segments.append(("translate", text[last_end:]))

    out = []
    for kind, segment in segments:
        if kind == "skip":
            out.append(segment)
            continue
        for ro in sorted_keys:
            tr = translations[ro]
            if not tr:
                continue
            segment = segment.replace(ro, tr)
        out.append(segment)
    return "".join(out)


def chain_apply_lang(lang: str):
    en_dict = json.loads((TRANSLATIONS_DIR / "en.json").read_text(encoding="utf-8"))
    lang_path = TRANSLATIONS_DIR / f"{lang}.json"
    if not lang_path.exists() and lang == "ie":
        lang_path = TRANSLATIONS_DIR / "en.json"
    if not lang_path.exists():
        print(f"  ✗ {lang_path.name} missing")
        return
    lang_dict = json.loads(lang_path.read_text(encoding="utf-8"))
    country_dir = COUNTRIES_DIR / lang
    if not country_dir.exists():
        print(f"  ✗ countries/{lang}/ missing")
        return
    files = sorted(country_dir.rglob("*.html"))
    print(f"\n=== {lang.upper()}: chain-applying EN ({len(en_dict)}) then {lang.upper()} ({len(lang_dict)}) ===")
    changed = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        text = original
        if lang not in ("en", "ie"):
            text = apply_dict(text, en_dict)
        if lang != "ie" or lang_path.name == "en.json":
            text = apply_dict(text, lang_dict)
        if text != original:
            f.write_text(text, encoding="utf-8")
            changed += 1
    print(f"  ✓ Changed {changed}/{len(files)} files")


def main():
    import sys
    args = sys.argv[1:]
    if not args:
        args = ["en", "fr", "it", "es", "nl", "de", "ie"]
    for lang in args:
        chain_apply_lang(lang)


if __name__ == "__main__":
    main()
