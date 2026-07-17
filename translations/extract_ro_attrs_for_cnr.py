#!/usr/bin/env python3
"""Extract RO phrases from HTML attributes (meta, title, aria-label, alt) for CNR."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RO_DIR = ROOT / "countries" / "ro"
OUT = ROOT / "translations" / "extra2_ro_to_cnr.json"

DIAC = re.compile(r"[ăâîșțĂÂÎȘȚ]")
ATTR = re.compile(
    r'(?:content|aria-label|alt|title|placeholder)=["\']([^"\']+)["\']',
    re.I,
)
TITLE = re.compile(r"<title>([^<]+)</title>", re.I)


def main() -> None:
    existing: dict[str, str] = {}
    for name in ("ro_to_cnr.json", "extra_ro_to_cnr.json"):
        p = ROOT / "translations" / name
        if p.exists():
            existing.update(json.loads(p.read_text(encoding="utf-8")))

    phrases: set[str] = set()
    for html_path in RO_DIR.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        for m in TITLE.finditer(text):
            if DIAC.search(m.group(1)):
                phrases.add(m.group(1).strip())
        for m in ATTR.finditer(text):
            val = m.group(1).strip()
            if len(val) >= 4 and DIAC.search(val):
                phrases.add(val)

    missing = {p: "" for p in sorted(phrases, key=lambda x: (-len(x), x)) if p not in existing}
    OUT.write_text(json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Attribute phrases: {len(phrases)}, missing: {len(missing)} -> {OUT}")


if __name__ == "__main__":
    main()
