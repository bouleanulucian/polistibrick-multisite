#!/usr/bin/env python3
"""
Overwrite RO HTML with FR design (same structure), rewrite FR paths → RO paths,
then apply FR→RO text via inverted translations/fr.json.

Does NOT copy images (shared/ only). Keeps countries/ro/_config.json and case/.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FR = ROOT / "countries" / "fr"
RO = ROOT / "countries" / "ro"
TRANS = ROOT / "translations"

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

# FR segment → RO segment (inverse of RO_TO_LANG['fr'])
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
    "toit-tbk-sip250": "acoperis-tbk-sip250",
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


def rewrite_paths(text: str) -> str:
    for fr, ro in sorted(FR_TO_RO.items(), key=lambda x: -len(x[0])):
        text = re.sub(r'(["\'/`$])' + re.escape(fr) + r'(/)', r"\1" + ro + r"\2", text)
        text = text.replace(f"/{fr}/", f"/{ro}/")
        text = text.replace(f'/{fr}"', f'/{ro}"')
        text = text.replace(f"/{fr}#", f"/{ro}#")
        text = text.replace(f"/{fr}?", f"/{ro}?")
    return text


def fr_path_to_ro(rel: Path) -> Path:
    parts = []
    for p in rel.parts:
        parts.append(FR_TO_RO.get(p, p))
    return Path(*parts)


def load_fr_to_ro() -> dict[str, str]:
    """Invert translations/fr.json (RO→FR) to FR→RO."""
    data = json.loads((TRANS / "fr.json").read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for ro, fr in data.items():
        if not fr or not ro or fr == ro:
            continue
        # Prefer longer / first-seen; skip if FR already mapped to different RO
        if fr not in out or len(ro) > len(out[fr]):
            out[fr] = ro
    return out


def apply_dict(text: str, mapping: dict[str, str]) -> str:
    keys = sorted(mapping.keys(), key=len, reverse=True)
    segments = []
    last_end = 0
    for m in SKIP.finditer(text):
        segments.append(("t", text[last_end : m.start()]))
        segments.append(("s", m.group(0)))
        last_end = m.end()
    segments.append(("t", text[last_end:]))
    out = []
    for kind, seg in segments:
        if kind == "s":
            out.append(seg)
            continue
        for fr in keys:
            tr = mapping[fr]
            if tr:
                seg = seg.replace(fr, tr)
        out.append(seg)
    return "".join(out)


def main() -> None:
    keep_case = RO / "case"
    case_backup = None
    if keep_case.exists():
        case_backup = ROOT / ".tmp_ro_case_backup"
        if case_backup.exists():
            shutil.rmtree(case_backup)
        shutil.copytree(keep_case, case_backup)

    cfg_path = RO / "_config.json"
    cfg_text = cfg_path.read_text(encoding="utf-8")

    # Wipe RO except config (and restore case later)
    for item in list(RO.iterdir()):
        if item.name == "_config.json":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    mapping = load_fr_to_ro()
    n_files = 0
    for src in FR.rglob("*"):
        if src.is_dir():
            continue
        if src.name == "_config.json":
            continue
        rel = src.relative_to(FR)
        if rel.parts and rel.parts[0] == "images":
            continue
        dest_rel = fr_path_to_ro(rel)
        dest = RO / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix.lower() == ".html":
            text = src.read_text(encoding="utf-8")
            text = text.replace('<html lang="fr">', '<html lang="ro">', 1)
            text = rewrite_paths(text)
            for _ in range(3):
                text = apply_dict(text, mapping)
            dest.write_text(text, encoding="utf-8")
            n_files += 1
        else:
            shutil.copy2(src, dest)

    cfg_path.write_text(cfg_text, encoding="utf-8")

    if case_backup and case_backup.exists():
        if (RO / "case").exists():
            shutil.rmtree(RO / "case")
        shutil.copytree(case_backup, RO / "case")
        shutil.rmtree(case_backup)

    print(f"✓ RO synced from FR design ({n_files} HTML, no images, case/ kept)")
    print(f"  FR→RO dict size: {len(mapping)}")


if __name__ == "__main__":
    main()
