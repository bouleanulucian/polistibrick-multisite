#!/usr/bin/env python3
"""Rename FR URL folders → RO folders and rewrite links in countries/ro/."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RO = ROOT / "countries" / "ro"

# FR folder segment → RO folder segment (inverse of build PATH_REWRITES fr map)
FR_TO_RO = {
    "produits": "produse",
    "pour": "pentru",
    "a-propos": "despre",
    "ressources": "resurse",
    "projets": "proiecte",
    "economies": "economii",
    "devis": "oferta",
    "comparaison": "comparatie",
    "calculateur": "calculator",
    "temoignages": "testimoniale",
    "devenir-partenaire": "devino-partener",
    "murs-mbk": "pereti-mbk",
    "planchers-pbk": "planseu-pbk",
    "toit-tbk": "acoperis-tbk",
    "accessoires": "accesorii",
    "proprietaires": "proprietari",
    "architectes": "arhitecti",
    "constructeurs": "constructori",
    "investisseurs": "investitori",
    "certifications": "certificari",
    "usines": "fabrici",
    "fondateur": "echipa",
    "brevet": "patent",
    "maison-cluj-napoca": "casa-cluj-napoca",
    "ensemble-lyon": "ansamblu-lyon",
    "confidentialite": "confidentialitate",
    "durabilite": "sustenabilitate",
    "conditions": "termeni",
    "mentions-legales": "mentiuni-legale",
    "montage": "montaj",
}


def rename_folders(base: Path) -> int:
    dirs = [d for d in base.rglob("*") if d.is_dir()]
    dirs.sort(key=lambda d: len(d.parts), reverse=True)
    count = 0
    for d in dirs:
        old = d.name
        if old in FR_TO_RO:
            new_name = FR_TO_RO[old]
            if new_name != old:
                d.rename(d.parent / new_name)
                count += 1
    return count


def rewrite_file_text(text: str) -> str:
    for fr, ro in sorted(FR_TO_RO.items(), key=lambda x: -len(x[0])):
        if fr == ro:
            continue
        text = re.sub(r'(["\'/`$])' + re.escape(fr) + r'(/)', r"\1" + ro + r"\2", text)
        text = text.replace(f"/{fr}/", f"/{ro}/")
        text = text.replace(f'/{fr}"', f'/{ro}"')
        text = text.replace(f"/{fr}#", f"/{ro}#")
    return text


def rewrite_all_files() -> int:
    n = 0
    for f in RO.rglob("*"):
        if f.is_dir() or f.name == "_config.json":
            continue
        if f.suffix.lower() not in {".html", ".css", ".js", ".json", ".xml", ".txt"}:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = rewrite_file_text(text)
        if new != text:
            f.write_text(new, encoding="utf-8")
            n += 1
    return n


def main():
    if not RO.exists():
        raise SystemExit("Run seed_from_fr.py ro first")
    renamed = rename_folders(RO)
    files = rewrite_all_files()
    print(f"✓ RO paths: {renamed} folders renamed, {files} files updated")


if __name__ == "__main__":
    main()
