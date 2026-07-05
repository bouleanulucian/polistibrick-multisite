#!/usr/bin/env python3
"""
Apply FR → target-language translations to countries seeded from FR.

Builds mapping from translations/fr.json + translations/{lang}.json
(shared RO keys → FR value + target value), then replaces French
user-visible text in HTML (skips script/style/comments).

Usage:
    python3 translations/apply_fr_to_lang.py en
    python3 translations/apply_fr_to_lang.py en it es nl de
    python3 translations/apply_fr_to_lang.py all
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

LANGS = ["en", "it", "es", "nl", "de", "ie"]


def build_fr_to_lang(lang: str) -> dict[str, str]:
    built = TRANSLATIONS_DIR / f"fr_to_{lang if lang != 'ie' else 'en'}.json"
    if built.exists():
        return json.loads(built.read_text(encoding="utf-8"))

    fr_path = TRANSLATIONS_DIR / "fr.json"
    lang_path = TRANSLATIONS_DIR / f"{lang}.json"
    if not lang_path.exists() and lang == "ie":
        lang_path = TRANSLATIONS_DIR / "en.json"
    if not fr_path.exists() or not lang_path.exists():
        raise SystemExit(f"Missing fr.json or {lang_path.name}")

    fr_dict = json.loads(fr_path.read_text(encoding="utf-8"))
    lang_dict = json.loads(lang_path.read_text(encoding="utf-8"))

    mapping: dict[str, str] = {}
    for ro_key, fr_val in fr_dict.items():
        if not fr_val or ro_key not in lang_dict:
            continue
        target = lang_dict[ro_key]
        if not target or fr_val == target:
            continue
        mapping[fr_val] = target
    return mapping


def apply_dict(text: str, translations: dict[str, str]) -> str:
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)
    segments = []
    last_end = 0
    for m in SKIP_REGEX.finditer(text):
        segments.append(("translate", text[last_end : m.start()]))
        segments.append(("skip", m.group(0)))
        last_end = m.end()
    segments.append(("translate", text[last_end:]))

    out = []
    for kind, segment in segments:
        if kind == "skip":
            out.append(segment)
            continue
        for fr in sorted_keys:
            tr = translations[fr]
            if tr:
                segment = segment.replace(fr, tr)
        out.append(segment)
    return "".join(out)


def apply_lang(lang: str) -> None:
    mapping = build_fr_to_lang(lang)
    country_dir = COUNTRIES_DIR / lang
    if not country_dir.exists():
        print(f"  ✗ countries/{lang}/ missing — run seed_from_fr.py first")
        return

    cfg_path = country_dir / "_config.json"
    html_lang = lang
    if cfg_path.exists():
        html_lang = json.loads(cfg_path.read_text(encoding="utf-8")).get("lang", lang)

    files = sorted(country_dir.rglob("*.html"))
    changed = 0
    print(f"\n=== {lang.upper()}: applying {len(mapping)} FR→{lang.upper()} replacements ===")
    for f in files:
        original = f.read_text(encoding="utf-8")
        text = apply_dict(original, mapping)
        text = text.replace('<html lang="fr">', f'<html lang="{html_lang}">', 1)
        if text != original:
            f.write_text(text, encoding="utf-8")
            changed += 1
    print(f"  ✓ Changed {changed}/{len(files)} files")


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 translations/apply_fr_to_lang.py <lang> [...]")
        sys.exit(1)
    if args == ["all"]:
        args = LANGS
    for lang in args:
        apply_lang(lang)
    print()


if __name__ == "__main__":
    main()
