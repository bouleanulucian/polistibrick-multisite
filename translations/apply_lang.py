#!/usr/bin/env python3
"""
Apply language-specific translation dicts from translations/{lang}.json
to country HTML files. Preserves <script>/<style>/comments.

Usage:
    python3 translations/apply_lang.py en          # apply en.json to countries/en/
    python3 translations/apply_lang.py en fr it    # multiple
    python3 translations/apply_lang.py all         # all 6
"""
import json
import re
import sys
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
    """Apply translation dict to text. Skip script/style/comments.
    Longest keys first to avoid partial matches inside longer phrases."""
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

def apply_lang(lang: str):
    json_file = TRANSLATIONS_DIR / f"{lang}.json"
    if not json_file.exists():
        print(f"  ✗ {lang}.json not found, skipped")
        return
    translations = json.loads(json_file.read_text(encoding="utf-8"))
    print(f"\n=== Applying {len(translations)} translations to {lang.upper()} ===")
    country_dir = COUNTRIES_DIR / lang
    files = sorted(country_dir.rglob("*.html"))
    changed = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        new = apply_dict(original, translations)
        if new != original:
            f.write_text(new, encoding="utf-8")
            changed += 1
    print(f"  ✓ Changed {changed}/{len(files)} files")

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 translations/apply_lang.py <lang> [lang ...]")
        sys.exit(1)
    if args == ["all"]:
        args = ["en", "fr", "it", "es", "nl", "de"]
    for lang in args:
        apply_lang(lang)
    print()

if __name__ == "__main__":
    main()
