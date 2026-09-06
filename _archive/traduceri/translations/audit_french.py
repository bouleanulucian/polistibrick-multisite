#!/usr/bin/env python3
"""Find likely French leftover text in countries/ro HTML."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "countries" / (sys.argv[1] if len(sys.argv) > 1 else "ro")

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
FR_ACCENT = re.compile(r"[àâäéèêëïîôùûüçœæ]", re.IGNORECASE)
FR_WORDS = re.compile(
    r"\b(le|la|les|des|une|un|pour|avec|sans|dans|maison|système|"
    r"demander|télécharger|politique|confidentialité|mentions|légales|"
    r"devis|produits|architectes|constructeurs|investisseurs|témoignages|"
    r"bientôt|prochainement|merci|votre|nous|vous|être|étape|semaines)\b",
    re.IGNORECASE,
)


def scan_html(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    cleaned = SKIP.sub(" ", text)
    hits = []
    for i, line in enumerate(cleaned.splitlines(), 1):
        if FR_ACCENT.search(line) or FR_WORDS.search(line):
            snippet = line.strip()[:120]
            if snippet and "{{" not in snippet:
                hits.append(f"  L{i}: {snippet}")
    return hits


def main():
    total = 0
    for html in sorted(TARGET.rglob("*.html")):
        hits = scan_html(html)
        if hits:
            rel = html.relative_to(ROOT)
            print(f"\n{rel} ({len(hits)} suspect lines)")
            for h in hits[:8]:
                print(h)
            if len(hits) > 8:
                print(f"  ... +{len(hits) - 8} more")
            total += len(hits)
    print(f"\n{'='*40}\nTotal suspect lines: {total}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
