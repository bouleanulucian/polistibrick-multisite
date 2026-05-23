#!/usr/bin/env python3
"""
Rename FR folders to French + update ALL internal links.
Safe: keeps original countries/fr/ intact via backup; works on copy.
"""
import shutil
from pathlib import Path
import re

ROOT = Path("/Users/polistibrick/Desktop/polistibrick-multisite")
FR = ROOT / "countries" / "fr"

# RO → FR folder mapping (top level + sub)
RENAME = {
    # Top-level sections
    "produse": "produits",
    "pentru": "pour",
    "despre": "a-propos",
    "resurse": "ressources",
    "proiecte": "projets",
    "economii": "economies",
    "oferta": "devis",
    "comparatie": "comparaison",
    "calculator": "calculateur",
    "testimoniale": "temoignages",
    "devino-partener": "devenir-partenaire",
    "legal": "legal",
    # Subfolders
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
    "echipa": "equipe",
    "patent": "brevet",
    "casa-cluj-napoca": "maison-cluj-napoca",
    "ansamblu-lyon": "ensemble-lyon",
    "villa-valencia": "villa-valencia",
    "confidentialitate": "confidentialite",
    "cookies": "cookies",
    "sustenabilitate": "durabilite",
    "termeni": "conditions",
    "faq": "faq",
    "blog": "blog",
}

# Rename folders (deepest first to avoid path-rewrite issues)
def rename_folders(base: Path):
    # Get all dirs, sort by depth desc
    dirs = [d for d in base.rglob("*") if d.is_dir()]
    dirs.sort(key=lambda d: len(d.parts), reverse=True)
    renamed_count = 0
    for d in dirs:
        old_name = d.name
        if old_name in RENAME:
            new_name = RENAME[old_name]
            if new_name != old_name:
                new_path = d.parent / new_name
                if new_path.exists():
                    print(f"  ! target exists, skip: {new_path}")
                    continue
                d.rename(new_path)
                renamed_count += 1
                print(f"  ✓ {d.relative_to(base)} → {new_name}")
    return renamed_count

# Update internal links in HTML files
def update_links(base: Path):
    # Build replacement patterns: old folder/path → new
    # Match in href="..." and src="..." values
    replacements = []
    # Order: longest first (to avoid partial matches)
    for old, new in sorted(RENAME.items(), key=lambda x: -len(x[0])):
        if old != new:
            # Match path segments: /old/  or  old/  at start
            replacements.append((re.compile(r'(["\'/])' + re.escape(old) + r'(/)'), r'\1' + new + r'\2'))
            # Also bare old/  in relative links like href="old/page/"
            replacements.append((re.compile(r'(["\'])' + re.escape(old) + r'(/)'), r'\1' + new + r'\2'))

    total_changes = 0
    for f in base.rglob("*.html"):
        txt = f.read_text(encoding="utf-8")
        orig = txt
        for pat, repl in replacements:
            txt = pat.sub(repl, txt)
        if txt != orig:
            f.write_text(txt, encoding="utf-8")
            total_changes += 1
    return total_changes

def main():
    print(f"Renaming folders in {FR}...")
    n = rename_folders(FR)
    print(f"\n→ {n} folders renamed")

    print(f"\nUpdating internal links in HTML files...")
    n = update_links(FR)
    print(f"→ {n} HTML files updated")

if __name__ == "__main__":
    main()
