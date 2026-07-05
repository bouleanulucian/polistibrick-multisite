#!/usr/bin/env python3
"""
Rename RO URL folders → French slugs and update internal links.
Used for all non-RO country sites (en, it, es, nl, de, ie, fr).

Usage:
    python3 translations/rename_paths.py en
    python3 translations/rename_paths.py en it es nl de ie
    python3 translations/rename_paths.py all
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RENAME = {
    "produse": "produits",
    "pentru": "pour",
    "despre": "a-propos",
    "resurse": "ressources",
    "proiecte": "projets",
    "economii": "economies",
    "oferta": "devis",
    "comparatie": "comparaison",
    "calculator": "calculateur",
    "testimoniale": "testimoniale",
    "devino-partener": "devenir-partenaire",
    "legal": "legal",
    "pereti-mbk": "murs-mbk",
    "planseu-pbk": "planchers-pbk",
    "acoperis-tbk": "toit-tbk",
    "accesorii": "accessoires",
    "proprietari": "proprietaires",
    "arhitecti": "architectes",
    "constructori": "constructeurs",
    "investitori": "investisseurs",
    "certificari": "certifications",
    "fabrici": "usines",
    "echipa": "fondateur",
    "patent": "brevet",
    "casa-cluj-napoca": "maison-cluj-napoca",
    "ansamblu-lyon": "ensemble-lyon",
    "villa-valencia": "villa-valencia",
    "confidentialitate": "confidentialite",
    "cookies": "cookies",
    "sustenabilitate": "durabilite",
    "termeni": "conditions",
    "mentiuni-legale": "mentions-legales",
    "montaj": "montage",
    "produse": "produits",
}

# testimoniale → temoignages (override duplicate key issue)
RENAME["testimoniale"] = "temoignages"


def rename_folders(base: Path) -> int:
    dirs = [d for d in base.rglob("*") if d.is_dir()]
    dirs.sort(key=lambda d: len(d.parts), reverse=True)
    count = 0
    for d in dirs:
        old_name = d.name
        if old_name in RENAME:
            new_name = RENAME[old_name]
            if new_name != old_name:
                new_path = d.parent / new_name
                if new_path.exists():
                    continue
                d.rename(new_path)
                count += 1
    return count


def update_links(base: Path) -> int:
    replacements = []
    for old, new in sorted(RENAME.items(), key=lambda x: -len(x[0])):
        if old != new:
            replacements.append(
                (re.compile(r'(["\'/])' + re.escape(old) + r'(/)'), r"\1" + new + r"\2")
            )
            replacements.append(
                (re.compile(r'(["\'])' + re.escape(old) + r'(/)'), r"\1" + new + r"\2")
            )

    total = 0
    for f in base.rglob("*.html"):
        txt = f.read_text(encoding="utf-8")
        orig = txt
        for pat, repl in replacements:
            txt = pat.sub(repl, txt)
        if txt != orig:
            f.write_text(txt, encoding="utf-8")
            total += 1
    return total


def rename_country(code: str) -> None:
    base = ROOT / "countries" / code
    if not base.exists():
        print(f"  ✗ countries/{code}/ missing")
        return
    n_dirs = rename_folders(base)
    n_files = update_links(base)
    print(f"  ✓ {code}: {n_dirs} folders renamed, {n_files} HTML files updated")


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 translations/rename_paths.py <code> [...]")
        sys.exit(1)
    if args == ["all"]:
        args = ["en", "it", "es", "nl", "de", "ie"]
    for code in args:
        rename_country(code)
    print()


if __name__ == "__main__":
    main()
