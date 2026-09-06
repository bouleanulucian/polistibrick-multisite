#!/usr/bin/env python3
"""Extract RO phrases (with diacritics) from countries/ro/ for CNR translation."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RO_DIR = ROOT / "countries" / "ro"
OUT = ROOT / "translations" / "phrases_ro_for_cnr.json"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")
DIAC = re.compile(r"[ăâîșțĂÂÎȘȚ]")


def segments(html: str) -> list[str]:
    cleaned = SKIP_REGEX.sub(" ", html)
    out: list[str] = []
    for part in TAG.split(cleaned):
        part = part.strip()
        if not part:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", part):
            sentence = sentence.strip()
            if 8 <= len(sentence) <= 500 and DIAC.search(sentence):
                out.append(sentence)
    return out


def main() -> None:
    phrases: set[str] = set()
    for html_path in sorted(RO_DIR.rglob("*.html")):
        phrases.update(segments(html_path.read_text(encoding="utf-8")))

    existing: dict[str, str] = {}
    for name in ("ro_to_cnr.json", "extra_ro_to_cnr.json", "remaining_ro_cnr.json"):
        p = ROOT / "translations" / name
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            for k, v in data.items():
                if k and v:
                    existing[k] = v

    missing = {p: "" for p in sorted(phrases, key=lambda x: (-len(x), x)) if p not in existing}
    OUT.write_text(json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Total RO phrases: {len(phrases)}, missing CNR: {len(missing)}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
