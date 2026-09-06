#!/usr/bin/env python3
"""Extract all user-visible Romanian phrases from countries/ro/ and find gaps in lang JSON."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RO_DIR = ROOT / "countries" / "ro"
TRANS = ROOT / "translations"

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")
RO_MARK = re.compile(r"[ăâîșțĂÂÎȘȚ]|\b(pentru|despre|construi|facturi|casa|casă|ofertă|sistem)\b", re.I)


def segments(html: str) -> list[str]:
    cleaned = SKIP.sub(" ", html)
    parts = TAG.split(cleaned)
    out = []
    for p in parts:
        p = p.strip()
        if 3 <= len(p) <= 400:
            out.append(p)
    return out


def main():
    phrases: set[str] = set()
    for html in sorted(RO_DIR.rglob("*.html")):
        for s in segments(html.read_text(encoding="utf-8")):
            if RO_MARK.search(s):
                phrases.add(s)

    en = json.loads((TRANS / "en.json").read_text(encoding="utf-8"))
    missing = sorted(p for p in phrases if p not in en)
    print(f"Total RO phrases: {len(phrases)}")
    print(f"In en.json: {len(phrases) - len(missing)}")
    print(f"Missing: {len(missing)}")

    out = TRANS / "missing_ro_phrases.json"
    out.write_text(json.dumps({p: "" for p in missing}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"→ {out}")


if __name__ == "__main__":
    main()
