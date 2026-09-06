#!/usr/bin/env python3
"""Extract unique French phrases still present in countries/{lang}/ HTML."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")
FR = re.compile(
    r"[àâäéèêëïîôùûüçœæ]"
    r"|\b(une|des|les|pour|avec|sans|dans|maison|système|demander|devis|produits|"
    r"témoignages|architectes|constructeurs|propriétaires|investisseurs|planchers|"
    r"confidentialité|mentions|légales|votre|nous|vous|être|semaines|construire|"
    r"politique|bientôt|prochainement|merci)\b",
    re.I,
)


def extract(lang: str) -> dict[str, str]:
    country = ROOT / "countries" / lang
    phrases: set[str] = set()
    for html in country.rglob("*.html"):
        cleaned = SKIP.sub(" ", html.read_text(encoding="utf-8"))
        for p in TAG.split(cleaned):
            p = p.strip()
            if 4 <= len(p) <= 350 and FR.search(p) and "{{" not in p:
                phrases.add(p)
    return {s: "" for s in sorted(phrases, key=lambda x: (-len(x), x))}


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    data = extract(lang)
    out = ROOT / "translations" / f"remaining_fr_{lang}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{lang}: {len(data)} unique FR phrases → {out.name}")


if __name__ == "__main__":
    main()
