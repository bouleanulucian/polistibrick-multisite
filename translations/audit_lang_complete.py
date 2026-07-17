#!/usr/bin/env python3
"""Audit visible non-target-language text in country HTML."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATTERNS = {
    "es": {
        "lang": "es",
        "bad": re.compile(
            r"\b(Demander|votre |nous |Propriétaire|Constructeur|"
            r"Redirecționare|Construi|pentru |despre |ofertă|"
            r"Il sistema|Un sistema protetto|mattone|Testimonianza|"
            r"verificato|prevedibilità|tempi |CALCOLATORE|"
            r"Rappresentazione|REPUBBLICA FRANCÉS|pubblicaz)\b",
            re.I,
        ),
    },
    "en": {
        "lang": "en",
        "bad": re.compile(
            r"\b(Demander|votre |nous |Propriétaire|Constructeur|"
            r"Redirecționare|Construi|pentru |despre |"
            r"Comment pouvons|Qu'est-ce|lequel est|Answers aux|"
            r"Il faut distinguer|La plaque de finition|"
            r"Surface area area|COPY-PASTE pentru)\b",
            re.I,
        ),
    },
}


def strip_non_visible(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<script\b.*?</script>", "", text, flags=re.I | re.S)
    text = re.sub(r"<style\b.*?</style>", "", text, flags=re.I | re.S)
    return text


def audit(code: str) -> int:
    cfg = PATTERNS[code]
    base = ROOT / "countries" / code
    issues: list[str] = []
    for f in sorted(base.rglob("*.html")):
        raw = f.read_text(encoding="utf-8")
        rel = f.relative_to(base).as_posix()
        if f'lang="{cfg["lang"]}"' not in raw[:600]:
            issues.append(f"  ! {rel}: missing lang=\"{cfg['lang']}\"")
        visible = strip_non_visible(raw)
        for i, line in enumerate(visible.splitlines(), 1):
            if cfg["bad"].search(line):
                snippet = line.strip()[:100]
                issues.append(f"  ! {rel}:{i}: {snippet}")
    print(f"\n=== Audit {code.upper()} ({len(issues)} issues) ===")
    for x in issues[:80]:
        print(x)
    if len(issues) > 80:
        print(f"  ... +{len(issues) - 80} more")
    return len(issues)


if __name__ == "__main__":
    codes = sys.argv[1:] or ["es", "en"]
    total = sum(audit(c) for c in codes)
    sys.exit(0 if total == 0 else 1)
