#!/usr/bin/env python3
"""
Rename FR URL folders → local-language slugs and rewrite internal links.

Usage:
    python3 translations/localize_country_paths.py it
    python3 translations/localize_country_paths.py it en es nl de ie
    python3 translations/localize_country_paths.py all
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from path_maps import FR_TO_LANG

SKIP_COUNTRIES = {"ro", "fr"}
ALL_CODES = ["it", "en", "es", "nl", "de", "ie", "me"]

PRIVACY_SLUG = {
    "it": "privacy",
    "en": "privacy",
    "es": "privacidad",
    "nl": "privacy",
    "de": "datenschutz",
    "cnr": "privatnost",
}


def lang_for_country(code: str, cfg: dict) -> str:
    lang = cfg.get("lang", code)
    if code == "ie":
        return "en"
    return lang


def rename_folders(base: Path, mapping: dict[str, str]) -> int:
    dirs = [d for d in base.rglob("*") if d.is_dir()]
    dirs.sort(key=lambda d: len(d.parts), reverse=True)
    count = 0
    for d in dirs:
        old = d.name
        if old not in mapping:
            continue
        new_name = mapping[old]
        if new_name == old:
            continue
        target = d.parent / new_name
        if target.exists():
            continue
        d.rename(target)
        count += 1
    return count


def rewrite_file_text(text: str, mapping: dict[str, str]) -> str:
    for fr, local in sorted(mapping.items(), key=lambda x: -len(x[0])):
        if fr == local:
            continue
        text = re.sub(r'(["\'/`$])' + re.escape(fr) + r'(/)', r"\1" + local + r"\2", text)
        text = text.replace(f"/{fr}/", f"/{local}/")
        text = text.replace(f'/{fr}"', f'/{local}"')
        text = text.replace(f"/{fr}#", f"/{local}#")
        text = text.replace(f"/{fr}?", f"/{local}?")
    return text


def rewrite_all_files(base: Path, mapping: dict[str, str]) -> int:
    n = 0
    exts = {".html", ".css", ".js", ".json", ".xml", ".txt"}
    for f in base.rglob("*"):
        if f.is_dir() or f.name == "_config.json":
            continue
        if f.suffix.lower() not in exts:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = rewrite_file_text(text, mapping)
        if new != text:
            f.write_text(new, encoding="utf-8")
            n += 1
    return n


def update_config_privacy_slug(code: str, lang: str) -> None:
    cfg_path = ROOT / "countries" / code / "_config.json"
    if not cfg_path.exists() or lang not in PRIVACY_SLUG:
        return
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    legal = cfg.setdefault("legal", {})
    legal["privacy_slug"] = PRIVACY_SLUG[lang]
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def localize_country(code: str) -> None:
    if code in SKIP_COUNTRIES:
        print(f"  — {code}: skipped (already native paths)")
        return
    base = ROOT / "countries" / code
    if not base.exists():
        print(f"  ✗ countries/{code}/ missing")
        return
    cfg_path = base / "_config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    lang = lang_for_country(code, cfg)
    mapping = FR_TO_LANG.get(lang)
    if not mapping:
        print(f"  ✗ no path map for lang={lang} (country {code})")
        return
    renamed = rename_folders(base, mapping)
    files = rewrite_all_files(base, mapping)
    update_config_privacy_slug(code, lang)
    print(f"  ✓ {code} ({lang}): {renamed} folders renamed, {files} files updated")


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 translations/localize_country_paths.py <code> [...]")
        sys.exit(1)
    if args == ["all"]:
        args = ALL_CODES
    for code in args:
        localize_country(code)
    print()


if __name__ == "__main__":
    main()
