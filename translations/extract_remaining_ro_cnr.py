#!/usr/bin/env python3
"""Extract Romanian phrases still visible in countries/me/ after CNR sync."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ME_DIR = ROOT / "countries" / "me"
OUT = ROOT / "translations" / "remaining_ro_cnr.json"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")
RO = re.compile(
    r"[ăâîșțĂÂÎȘȚ]"
    r"|\b(despre|pentru|este|sunt|fără|așa|toate|noi|nostru|noastră"
    r"|aceasta|acest|aceste|fiecare|astfel|așadar|deasemenea"
    r"|sau|dar|când|cum|unde|prin|către|peste|sub|între|orice"
    r"|trebuie|poate|construiește|construim|construiți"
    r"|primește|trimite|trimitem|certificări|fabrică|șantier"
    r"|locuințe|încălzire|economii|proprietar|solicitați)\b",
    re.IGNORECASE | re.UNICODE,
)
FR = re.compile(
    r"\b(votre|nous |pour |avec |une |des |le |la |du |au |est |sont "
    r"|Demander|Propriétaire|Constructeur|système|maison)\b",
    re.IGNORECASE,
)


def extract_segments(html: str) -> list[str]:
    cleaned = SKIP_REGEX.sub(" ", html)
    parts = TAG.split(cleaned)
    out: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", part):
            sentence = sentence.strip()
            if 6 <= len(sentence) <= 400:
                out.append(sentence)
    return out


def main() -> None:
    phrases: set[str] = set()
    for html_path in sorted(ME_DIR.rglob("*.html")):
        for segment in extract_segments(html_path.read_text(encoding="utf-8")):
            if RO.search(segment) or FR.search(segment):
                phrases.add(segment)

    existing = {}
    ro_cnr = ROOT / "translations" / "ro_to_cnr.json"
    if ro_cnr.exists():
        existing = json.loads(ro_cnr.read_text(encoding="utf-8"))

    missing = {p: "" for p in sorted(phrases, key=lambda x: (-len(x), x)) if p not in existing}
    OUT.write_text(json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Found {len(phrases)} RO/FR-like segments, {len(missing)} missing from ro_to_cnr.json")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
