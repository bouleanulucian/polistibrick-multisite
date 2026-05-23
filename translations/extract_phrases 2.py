#!/usr/bin/env python3
"""
Extract UNIQUE Romanian phrases from the English country files.
Output: a JSON file with all phrases that need translation.
"""
import re
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "countries" / "en"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

# Tag matcher — used to find user-visible text only
TAG_REGEX = re.compile(r"<[^>]+>")

# Match Romanian-diacritic words OR common Romanian function words
RO_INDICATOR = re.compile(
    r"[ăâîșțĂÂÎȘȚ]"
    r"|\b(despre|pentru|care|este|sunt|fara|fără|asa|așa|toate|noi|nostru|noastră"
    r"|cea|cel|cele|cei|aceasta|acest|aceasta|aceste|acelaș|aceeași"
    r"|sau|dar|cum|cand|când|unde|prin|catre|către|peste|sub|intre|între"
    r"|ce|ca|să|de|în|la|cu|și|si|pe|nu|mai|si"
    r"|cum se|este o|este un|cea mai|cele mai"
    r")\b",
    re.IGNORECASE | re.UNICODE
)


def extract_text_segments(html: str) -> list[str]:
    """Walk through HTML and extract text content between tags.
    Returns each segment of visible text as a separate string."""
    # First strip script/style/comments
    cleaned = SKIP_REGEX.sub(" ", html)
    # Split on tags to get text segments
    parts = TAG_REGEX.split(cleaned)
    return [p.strip() for p in parts if p.strip()]


def is_romanian(text: str) -> bool:
    """Heuristic: text is Romanian if it contains diacritics or RO function words."""
    if not text:
        return False
    if len(text) < 4:
        return False
    return bool(RO_INDICATOR.search(text))


def extract_unique_ro_phrases():
    """Walk all EN HTML files. Collect all Romanian text segments."""
    phrases = Counter()
    for html_file in sorted(EN_DIR.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")
        for segment in extract_text_segments(text):
            # Subdivide long segments by sentence-ending punctuation
            sentences = re.split(r"(?<=[.!?])\s+", segment)
            for s in sentences:
                s = s.strip()
                if not is_romanian(s):
                    continue
                # Skip very short
                if len(s) < 6:
                    continue
                # Skip if entirely numeric/symbols
                if not re.search(r"[a-zA-ZăâîșțĂÂÎȘȚ]{3,}", s):
                    continue
                phrases[s] += 1
    return phrases


def main():
    phrases = extract_unique_ro_phrases()
    total_unique = len(phrases)
    total_occurrences = sum(phrases.values())
    print(f"\n=== UNIQUE Romanian phrases found: {total_unique} ===")
    print(f"=== Total occurrences across all EN files: {total_occurrences} ===\n")

    # Sort by frequency (most common first → highest impact)
    sorted_phrases = phrases.most_common()

    print("Top 20 by frequency:")
    for phrase, count in sorted_phrases[:20]:
        print(f"  {count:3d}× | {phrase[:100]}")

    # Save to JSON
    output = {phrase: {"count": count} for phrase, count in sorted_phrases}
    output_path = ROOT / "translations" / "phrases_to_translate.json"
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ Saved to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
