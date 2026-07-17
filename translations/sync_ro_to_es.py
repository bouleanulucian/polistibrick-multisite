#!/usr/bin/env python3
"""Sync countries/es HTML from countries/ro with RO→ES translation + path rewrite."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RO_DIR = ROOT / "countries" / "ro"
ES_DIR = ROOT / "countries" / "es"
TRANS = ROOT / "translations"

sys.path.insert(0, str(ROOT))
from translations.path_maps import RO_TO_ES  # noqa: E402
from translations.sync_fr_to_es import (  # noqa: E402
    apply_dict,
    filter_mapping,
    protect_fragile,
    restore_fragile,
)

ES_TO_RO = {v: k for k, v in RO_TO_ES.items()}

ES_INDEX = (
    '<!DOCTYPE html>\n<html lang="es">\n<head>\n'
    '  <meta charset="UTF-8">\n'
    '  <meta http-equiv="refresh" content="0; url=polistibrick-mercury-style.html">\n'
    "  <title>Polistibrick</title>\n</head>\n<body data-base=\"\">\n"
    '  <p>Redirección a <a href="polistibrick-mercury-style.html">Polistibrick</a>…</p>\n'
    "</body>\n</html>\n"
)


def es_rel_to_ro_rel(es_rel: str) -> str:
    rel = es_rel.replace("\\", "/")
    if rel in ("index.html", "polistibrick-mercury-style.html"):
        return rel
    if rel.endswith("/index.html"):
        rel = rel[: -len("/index.html")]
    parts = [p for p in rel.split("/") if p]
    ro_parts = [ES_TO_RO.get(seg, seg) for seg in parts]
    if not ro_parts:
        return "index.html"
    return "/".join(ro_parts) + "/index.html"


def rewrite_paths(html: str) -> str:
    for ro_seg, es_seg in sorted(RO_TO_ES.items(), key=lambda x: -len(x[0])):
        html = html.replace(f"/{ro_seg}/", f"/{es_seg}/")
        html = html.replace(f'"{ro_seg}/', f'"{es_seg}/')
        html = html.replace(f"'{ro_seg}/", f"'{es_seg}/")
        html = html.replace(f"../{ro_seg}/", f"../{es_seg}/")
        html = html.replace(f"../../{ro_seg}/", f"../../{es_seg}/")
        html = html.replace(f"../../../{ro_seg}/", f"../../../{es_seg}/")
    html = html.replace("polistibrick.ro", "polistibrick.es")
    html = html.replace("devis.polistibrick.ro", "devis.polistibrick.es")
    html = html.replace('<html lang="ro">', '<html lang="es">', 1)
    html = html.replace('<html lang="ro" ', '<html lang="es" ', 1)
    return html


def load_merged_mapping() -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in (
        "es.json",
        "es_overrides.json",
        "mercury_fr_to_es.json",
        "extra_fr_to_es.json",
        "fr_to_es.json",
        "remaining_fr_es.json",
    ):
        p = TRANS / name
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for k, v in data.items():
            if k and v:
                merged[k] = v
    return filter_mapping(merged)


def fix_url_params(text: str) -> str:
    """Spanish contact/presupuesto query params."""
    replacements = [
        ("Demande+de+devis", "Solicitud+de+presupuesto"),
        ("Demande+de+documentation", "Solicitud+de+documentacion"),
        ("Demande+d+un+dossier+technique+complet", "Solicitud+de+dossier+tecnico+completo"),
        ("Demande+de+document", "Solicitud+de+documento"),
        ("Demande+de+dossier+technique", "Solicitud+de+dossier+tecnico"),
        ("Demande de document : ", "Solicitud de documento: "),
        ("Demande de document :", "Solicitud de documento:"),
        ("role=particulier", "role=particular"),
        ("role=promoteur", "role=promotor"),
        ("type=document", "type=documento"),
        ("doc=Documentation+investisseurs", "doc=Documentacion+inversores"),
        ("Dossier+Technique+Complet", "Dossier+Tecnico+Completo"),
        ("Dossier Technique - ", "Dossier Tecnico - "),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def sync_file(es_path: Path, mapping: dict[str, str]) -> bool:
    es_rel = es_path.relative_to(ES_DIR).as_posix()

    if es_rel == "index.html":
        if es_path.read_text(encoding="utf-8") != ES_INDEX:
            es_path.write_text(ES_INDEX, encoding="utf-8")
            return True
        return False

    ro_rel = es_rel_to_ro_rel(es_rel)
    ro_path = RO_DIR / ro_rel
    if not ro_path.exists():
        print(f"  ✗ missing RO source: {ro_rel} for {es_rel}")
        return False

    text = ro_path.read_text(encoding="utf-8")
    text = rewrite_paths(text)
    text, tokens = protect_fragile(text)
    for _ in range(5):
        text = apply_dict(text, mapping)
    text = restore_fragile(text, tokens)
    text = fix_url_params(text)

    original = es_path.read_text(encoding="utf-8")
    if text != original:
        es_path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    mapping = load_merged_mapping()
    print(f"=== sync_ro_to_es: {len(mapping)} translation keys ===")
    changed = 0
    for es_path in sorted(ES_DIR.rglob("*.html")):
        if sync_file(es_path, mapping):
            changed += 1
            print(f"  ✓ {es_path.relative_to(ES_DIR)}")
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
