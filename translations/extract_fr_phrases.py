#!/usr/bin/env python3
"""
Extract unique French phrases from countries/fr/ for translation dicts.
Output: JSON { "phrase": "" } ready to fill in translations/{lang}.json

Usage:
    python3 translations/extract_fr_phrases.py
    python3 translations/extract_fr_phrases.py --min-len 4 --out translations/phrases_fr_source.json
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FR_DIR = ROOT / "countries" / "fr"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG_REGEX = re.compile(r"<[^>]+>")
PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")
FR_INDICATOR = re.compile(
    r"[àâäéèêëïîôùûüçœæ]"
    r"|\b(une|des|les|pour|avec|sans|dans|maison|système|construction|projet)\b",
    re.IGNORECASE,
)


def extract_segments(html: str) -> list[str]:
    cleaned = SKIP_REGEX.sub(" ", html)
    parts = TAG_REGEX.split(cleaned)
    return [p.strip() for p in parts if p.strip()]


def is_french(text: str) -> bool:
    if PLACEHOLDER.search(text):
        return False
    if len(text) < 3:
        return False
    if re.fullmatch(r"[\d\s\W]+", text):
        return False
    return bool(FR_INDICATOR.search(text)) or " " in text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-len", type=int, default=3)
    parser.add_argument("--out", type=str, default="")
    args = parser.parse_args()

    counter: Counter[str] = Counter()
    for html in sorted(FR_DIR.rglob("*.html")):
        for seg in extract_segments(html.read_text(encoding="utf-8")):
            if len(seg) < args.min_len:
                continue
            if is_french(seg):
                counter[seg] += 1

    phrases = {
        s: ""
        for s in sorted(counter.keys(), key=lambda s: (-counter[s], -len(s)))
    }
    print(f"# {len(phrases)} unique French phrases from {FR_DIR.relative_to(ROOT)}")

    if args.out:
        out = Path(args.out)
        out.write_text(json.dumps(phrases, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"→ wrote {out}")
    else:
        print(json.dumps(phrases, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
