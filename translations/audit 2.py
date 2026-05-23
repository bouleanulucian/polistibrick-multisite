#!/usr/bin/env python3
"""
Audit translation completeness per page per language.

For each non-RO country, count Romanian words/phrases remaining
in user-visible HTML text (excludes <script>, <style>, comments).
"""
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = ROOT / "countries"
LANGS = ["en", "fr", "it", "es", "nl", "de"]

# Romanian-specific words/diacritics (high-confidence RO indicators)
RO_WORDS = re.compile(
    r"\b("
    # diacritic words
    r"\w*[ăâîșțĂÂÎȘȚ]\w*"
    # Common Romanian words without diacritics that are dead giveaway
    r"|despre|pentru|care|este|sunt|fara|asa|toate|tu|noi|el|ei|tine|tu"
    r"|cea|cel|cele|cei|aceasta|acest|aceasta|aceste"
    r"|sau|dar|cum|cand|unde|de|in|la|cu|si"
    r"|prin|catre|peste|sub|intre"
    r"|case|casa|sistem|premium|produse"  # words that may be RO
    r")\b",
    re.IGNORECASE | re.UNICODE
)

# Skip these — pure noise (English, code, brand names, numbers)
SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)"
    r"|(<[^>]+>)",  # all tags
    re.DOTALL | re.IGNORECASE,
)

def extract_visible_text(html: str) -> str:
    """Return only the user-visible text from HTML."""
    # Remove script/style/comments/tags
    return SKIP_REGEX.sub(" ", html)

def romanian_phrases_in(text: str) -> list[str]:
    """Return Romanian phrases (sentences) found."""
    # Split into sentences/clauses
    candidates = re.split(r"[.!?\n\r\t]\s+", text)
    phrases = []
    for c in candidates:
        c = c.strip()
        if len(c) < 8:
            continue
        # Skip if no Romanian markers
        if not RO_WORDS.search(c):
            continue
        # Skip if it's mostly code/numbers
        if re.search(r"^\W*\d", c) and len(re.findall(r"[a-zA-Z]", c)) < 4:
            continue
        phrases.append(c[:120])  # cap at 120 chars for display
    return phrases

def audit_lang(lang: str):
    country_dir = COUNTRIES_DIR / lang
    if not country_dir.exists():
        return None
    files = sorted(country_dir.rglob("*.html"))
    file_stats = []
    all_phrases = Counter()
    for f in files:
        text = f.read_text(encoding="utf-8")
        visible = extract_visible_text(text)
        phrases = romanian_phrases_in(visible)
        file_stats.append((f.relative_to(country_dir).as_posix(), len(phrases)))
        for p in phrases:
            all_phrases[p] += 1
    return file_stats, all_phrases

def main():
    print("=" * 75)
    print("TRANSLATION AUDIT — Romanian phrases remaining per file per language")
    print("=" * 75)

    grand_total = {}
    for lang in LANGS:
        result = audit_lang(lang)
        if not result:
            print(f"\n  [{lang}] folder missing, skipped")
            continue
        file_stats, all_phrases = result
        total = sum(c for _, c in file_stats)
        grand_total[lang] = total

        print(f"\n[{lang.upper()}] total Romanian phrases remaining: {total}")
        # Show worst-offender files
        sorted_files = sorted(file_stats, key=lambda x: -x[1])
        for fname, count in sorted_files[:10]:
            if count > 0:
                print(f"  {count:4d}  {fname}")

    print("\n" + "=" * 75)
    print("GRAND TOTALS (Romanian phrases per language)")
    print("=" * 75)
    for lang in LANGS:
        if lang in grand_total:
            print(f"  {lang}: {grand_total[lang]}")
    print()

    # Top 30 most common phrases across all languages (these are top candidates
    # to add to the glossary for the biggest impact)
    combined = Counter()
    for lang in LANGS:
        result = audit_lang(lang)
        if result:
            _, phrases = result
            for p, c in phrases.items():
                combined[p] += c
    print("=" * 75)
    print(f"TOP 30 RECURRING ROMANIAN PHRASES (translate these next for max impact)")
    print("=" * 75)
    for phrase, count in combined.most_common(30):
        print(f"  {count:4d}× : {phrase}")

if __name__ == "__main__":
    main()
