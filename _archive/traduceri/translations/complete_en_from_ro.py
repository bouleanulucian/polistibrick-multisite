#!/usr/bin/env python3
"""Rebuild countries/en/ from RO source + en.json + path localisation."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "countries" / "en"
RO_DIR = ROOT / "countries" / "ro"
TRANS = ROOT / "translations"

sys.path.insert(0, str(TRANS))
from path_maps import RO_TO_EN  # noqa: E402

EN_TO_RO = {v: k for k, v in RO_TO_EN.items()}
EN_TO_RO.update(
    {
        "about": "despre",
        "resources": "resurse",
        "projects": "proiecte",
        "savings": "economii",
        "quote": "oferta",
        "testimonials": "testimoniale",
        "become-a-partner": "devino-partener",
        "products": "produse",
        "for": "pentru",
        "walls-mbk": "pereti-mbk",
        "floors-pbk": "planseu-pbk",
        "roof-tbk": "acoperis-tbk",
        "homeowners": "proprietari",
        "architects": "arhitecti",
        "builders": "constructori",
        "investors": "investitori",
        "certifications": "certificari",
        "factories": "fabrici",
        "founder": "echipa",
        "house-cluj-napoca": "casa-cluj-napoca",
        "lyon-development": "ansamblu-lyon",
        "villa-valencia": "villa-valencia",
        "privacy": "confidentialitate",
        "sustainability": "sustenabilitate",
        "terms": "termeni",
        "legal-notice": "mentiuni-legale",
        "installation": "montaj",
        "what-is-a-passive-house": "ce-este-casa-passiva",
    }
)

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)


def en_rel_to_ro_rel(rel: str) -> str:
    return "/".join(EN_TO_RO.get(p, p) for p in rel.split("/"))


def localise_paths(text: str) -> str:
    for ro, en in sorted(RO_TO_EN.items(), key=lambda x: -len(x[0])):
        text = text.replace(f"/{ro}/", f"/{en}/")
        text = text.replace(f'="../{ro}/', f'="../{en}/')
        text = text.replace(f'="../../{ro}/', f'="../../{en}/')
        text = text.replace(f'="../../../{ro}/', f'="../../../{en}/')
    return text


def apply_dict(text: str, mapping: dict[str, str], passes: int = 6) -> str:
    keys = sorted(mapping.keys(), key=len, reverse=True)
    segments: list[tuple[str, str]] = []
    last_end = 0
    for m in SKIP_REGEX.finditer(text):
        segments.append(("translate", text[last_end : m.start()]))
        segments.append(("skip", m.group(0)))
        last_end = m.end()
    segments.append(("translate", text[last_end:]))
    out: list[str] = []
    for kind, segment in segments:
        if kind == "skip":
            out.append(segment)
            continue
        for _ in range(passes):
            for key in keys:
                val = mapping[key]
                if val:
                    segment = segment.replace(key, val)
        out.append(segment)
    return "".join(out)


def build_mapping() -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in ("en.json", "fr_to_en.json", "mercury_fr_to_en.json", "en_fr_supplement.json"):
        p = TRANS / name
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            for k, v in data.items():
                if k and v:
                    merged[k] = v
    return merged


def main():
    mapping = build_mapping()
    print(f"Mapping: {len(mapping)} keys")
    changed = 0
    for en_file in sorted(EN_DIR.rglob("*.html")):
        rel = en_file.relative_to(EN_DIR).as_posix()
        if rel == "index.html":
            continue
        ro_rel = en_rel_to_ro_rel(rel)
        ro_file = RO_DIR / ro_rel
        if not ro_file.exists():
            print(f"  ⚠ no RO: {rel} → {ro_rel}")
            continue
        text = ro_file.read_text(encoding="utf-8")
        text = text.replace('<html lang="ro">', '<html lang="en">', 1)
        text = localise_paths(text)
        text = apply_dict(text, mapping)
        if text != en_file.read_text(encoding="utf-8"):
            en_file.write_text(text, encoding="utf-8")
            print(f"  ✓ {rel}")
            changed += 1
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
