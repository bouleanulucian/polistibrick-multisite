#!/usr/bin/env python3
"""Merge all fr_to_*.json + mercury + remaining extras and apply to country HTML."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
COUNTRIES = ROOT / "countries"

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)


def lang_key_for(code: str) -> str:
    """Country folder code → translation file suffix."""
    return {"ie": "en", "me": "cnr"}.get(code, code)


def load_merged(lang: str) -> dict[str, str]:
    lang_key = lang_key_for(lang)
    merged: dict[str, str] = {}
    for pattern in [
        f"fr_to_{lang_key}.json",
        f"mercury_fr_to_{lang_key}.json",
        f"extra_fr_to_{lang_key}.json",
        f"remaining_fr_{lang_key}.json",  # if filled
    ]:
        p = TRANS / pattern
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            for k, v in data.items():
                if k and v:
                    merged[k] = v
    return merged


def apply_dict(text: str, mapping: dict[str, str]) -> str:
    keys = sorted(mapping.keys(), key=len, reverse=True)
    segments = []
    last_end = 0
    for m in SKIP.finditer(text):
        segments.append(("t", text[last_end : m.start()]))
        segments.append(("s", m.group(0)))
        last_end = m.end()
    segments.append(("t", text[last_end:]))
    out = []
    for kind, seg in segments:
        if kind == "s":
            out.append(seg)
            continue
        for fr in keys:
            tr = mapping[fr]
            if tr:
                seg = seg.replace(fr, tr)
        out.append(seg)
    return "".join(out)


def apply_country(lang: str, passes: int = 3) -> None:
    mapping = load_merged(lang)
    if not mapping:
        print(f"  ✗ no mapping for {lang}")
        return
    country = COUNTRIES / lang
    changed = 0
    for f in sorted(country.rglob("*.html")):
        original = f.read_text(encoding="utf-8")
        text = original
        for _ in range(passes):
            text = apply_dict(text, mapping)
        if text != original:
            f.write_text(text, encoding="utf-8")
            changed += 1
    print(f"  ✓ {lang}: {len(mapping)} keys, {changed} files updated")


def main():
    args = sys.argv[1:]
    if not args or args == ["all"]:
        args = ["en", "it", "es", "nl", "de", "ie"]
    for lang in args:
        apply_country(lang)


if __name__ == "__main__":
    main()
