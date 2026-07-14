#!/usr/bin/env python3
"""Audit visible non-Montenegrin text in countries/me/ (excludes comments)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ME_DIR = ROOT / "countries" / "me"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

RO_DIAC = re.compile(r"[ăâîșțĂÂÎȘȚ]")
FR = re.compile(
    r"\b(votre|nous |pour |avec |une |des |Demander|Propriétaire|Constructeur|"
    r"système|maison |été |climatisation|navigateur|mémoriser|essentiels)\b",
    re.I,
)
CORRUPT = re.compile(r"godina|spgodina|lgodinag|Frgodina|Špgodin", re.I)


def strip_non_visible(text: str) -> str:
    text = SKIP_REGEX.sub("", text)
    return text


def audit() -> int:
    issues: list[str] = []
    for f in sorted(ME_DIR.rglob("*.html")):
        raw = f.read_text(encoding="utf-8")
        rel = f.relative_to(ME_DIR).as_posix()
        if 'lang="cnr"' not in raw[:800] and 'lgodinag="cnr"' not in raw[:800]:
            issues.append(f"  ! {rel}: missing lang=\"cnr\"")
        visible = strip_non_visible(raw)
        for i, line in enumerate(visible.splitlines(), 1):
            if RO_DIAC.search(line) or FR.search(line) or CORRUPT.search(line):
                snippet = line.strip()[:120]
                if snippet:
                    issues.append(f"  ! {rel}:{i}: {snippet}")
    print(f"\n=== Audit ME/CNR ({len(issues)} issues) ===")
    for x in issues[:100]:
        print(x)
    if len(issues) > 100:
        print(f"  ... +{len(issues) - 100} more")
    return len(issues)


if __name__ == "__main__":
    sys.exit(0 if audit() == 0 else 1)
