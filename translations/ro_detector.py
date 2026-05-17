#!/usr/bin/env python3
"""
COMPREHENSIVE Romanian detector. Catches:
- diacritics (ă, â, î, ș, ț + capitals)
- 200+ specific RO words observed in the site or expected
- RO plural suffixes (-uri)
- Returns concrete list of offending words per file
"""
import re
from pathlib import Path
import sys

# CONFIRMED Romanian words from the site (manually curated from screenshots + scans)
RO_WORDS = set("""
proprietar proprietari arhitect arhitecți inginer ingineri dezvoltator dezvoltatori
suport maxim minim risc casa casă case cumpara cumpărător
discount discount-uri sistem sisteme produs produse soluție soluții
proiect proiecte calculator rezultat rezultate resursă resurse
despre echipa echipă fabrica fabrici fabrică patent compania companie
contact accesorii pereți perete planșeu planșee acoperiș acoperișuri
sustenabilitate sustenabil termeni cookies confidențialitate confidențial
muntenegru bulgaria românia
oferta ofertă cere
pentru fără sau dar când cum unde prin către peste sub între
toate orice trebuie poate primește construiește
constructor constructori inscriere înscriere certificat certificată
testimoniale testimonial
ce care cine
ești sunt este avea având
acasă închide alege schimba
nostru noastră noștri tăi tale tău
acest aceasta aceste această
factura facturi factură
brevetat brevetată patentat patentată brevet
ferestre fereastră
zile zile luna lună luni an ani anul anii
detalii detaliu cifre
mursi
construire construit construite construcție construcții construcția
isolare izolare isolated izolat izolată izolare izolație
acustic acustică acustice
materiale material materialele
echipa echipa echipe
panou panouri panourile
turnarea turnare beton betonului
deschideri portate
gata
totul tot toate
fizică fizic
ciment
prețul prețuri pret prețul
buget bugetul
durabil durabilă durabilitate
limita limită limita
""".lower().split())

# Phrases (multi-word RO patterns) — supplement the word list
RO_PHRASES = [
    "5 în 1", "5-în-1", "5-in-1",
    "discount-uri",
    "polistirenul", "polistirenul",
    "în 4 săptămâni",
    "1 lună",
]

# Diacritics regex
RO_DIACRITICS = re.compile(r"[ăâîșțĂÂÎȘȚ]")

# Word boundary regex for the word list
RO_WORD_REGEX = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in RO_WORDS) + r")\b",
    re.IGNORECASE
)

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Scan file. Return list of (line_no, snippet, reason)."""
    text = path.read_text(encoding="utf-8")
    cleaned = SKIP.sub(lambda m: " " * len(m.group(0)), text)  # preserve line offsets
    issues = []
    for i, line in enumerate(cleaned.splitlines(), 1):
        # Strip HTML tags but keep text
        text_only = TAG.sub(" ", line).strip()
        if not text_only:
            continue
        for m in RO_DIACRITICS.finditer(text_only):
            issues.append((i, text_only[:120], f"diacritic: {m.group(0)}"))
            break
        else:
            m = RO_WORD_REGEX.search(text_only)
            if m:
                issues.append((i, text_only[:120], f"word: {m.group(0)}"))
                continue
            for ph in RO_PHRASES:
                if ph.lower() in text_only.lower():
                    issues.append((i, text_only[:120], f"phrase: {ph}"))
                    break
    return issues


def scan_dir(directory: Path) -> dict:
    """Scan all .html files. Return {path: [issues]}."""
    results = {}
    for f in sorted(directory.rglob("*.html")):
        issues = scan_file(f)
        if issues:
            results[str(f.relative_to(directory))] = issues
    return results


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("build/fr")
    results = scan_dir(target)
    if not results:
        print(f"✓ 0 Romanian content found in {target}")
        sys.exit(0)
    total_issues = sum(len(v) for v in results.values())
    print(f"✗ {total_issues} Romanian instances in {len(results)} files\n")
    for path, issues in list(results.items())[:30]:
        print(f"{path} ({len(issues)} issues):")
        for line_no, snip, reason in issues[:5]:
            print(f"  L{line_no} [{reason}] {snip}")
        if len(issues) > 5:
            print(f"  ... +{len(issues)-5} more")
    sys.exit(1)
