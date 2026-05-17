#!/usr/bin/env python3
"""For each lang, extract pure-RO phrases remaining in countries/{lang}/ HTML."""
import re
import json
from pathlib import Path

ROOT = Path("/Users/polistibrick/Desktop/polistibrick-multisite")
COUNTRIES = ROOT / "countries"
OUT = ROOT / "translations"
LANGS = ["en", "fr", "it", "es", "nl", "de"]

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")
# Strong Romanian indicators: diacritics OR very-RO function words
RO = re.compile(
    r"[ăâîșțĂÂÎȘȚ]"
    r"|\b(despre|pentru|este|sunt|fără|așa|toate|noi|nostru|noastră"
    r"|aceasta|acest|aceste|fiecare|astfel|așadar|deasemenea"
    r"|sau|dar|când|cum|unde|prin|către|peste|sub|între|orice|oricărui"
    r"|săi|sale|ții|tau|tăi|fie|ești|avea|având|fiind"
    r"|trebuie|poate|poți|pot|vrea|vrei|vreți|vreau"
    r"|niciun|niciodată|mereu|întotdeauna|așteaptă|așteptăm"
    r"|primește|primești|primim|trimite|trimitem|trimiți"
    r"|construiește|construim|construiți|construiți"
    r"|aceeași|același|acelaș"
    r"|cea|cele|cei"
    r"|tăi|tale|tău"
    r")\b",
    re.IGNORECASE | re.UNICODE
)
# False-positive filter — words that ALSO exist in target langs
NOT_REALLY_RO_IF_SHORT = re.compile(
    r"^(case|casa|premium|sistem|noi|el|ei|tu|de|la|cu)\b",
    re.IGNORECASE
)


def extract_segments(html: str):
    cleaned = SKIP_REGEX.sub(" ", html)
    parts = TAG.split(cleaned)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # split on sentence boundaries to keep keys manageable
        for s in re.split(r"(?<=[.!?])\s+", p):
            s = s.strip()
            if 8 <= len(s) <= 300:
                out.append(s)
    return out


def is_really_ro(text: str) -> bool:
    if not RO.search(text):
        return False
    if NOT_REALLY_RO_IF_SHORT.match(text) and len(text) < 25:
        return False
    return True


for lang in LANGS:
    country = COUNTRIES / lang
    if not country.exists():
        continue
    phrases = set()
    for html in country.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        for s in extract_segments(text):
            if is_really_ro(s):
                phrases.add(s)
    sorted_phrases = sorted(phrases, key=lambda x: (-len(x), x))
    out_path = OUT / f"remaining_{lang}.txt"
    with out_path.open("w", encoding="utf-8") as f:
        for i, p in enumerate(sorted_phrases, 1):
            esc = p.replace('"', '\\"')
            f.write(f'{i}. "{esc}"\n')
    print(f"  {lang}: {len(sorted_phrases)} remaining → {out_path.name}")
