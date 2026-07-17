#!/usr/bin/env python3
"""
Complete countries/en/ HTML by syncing from countries/it/ reference pages.

1. Map EN paths → IT paths (via RO_TO_EN / RO_TO_IT)
2. Copy IT HTML structure with EN-localised URL segments
3. Apply IT→EN translation dict (fr pivot + it.json values as EN where keyed)
4. Preserve lang=en, {{placeholders}}, href/src path localisation EN
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "countries" / "en"
IT_DIR = ROOT / "countries" / "it"
TRANS = ROOT / "translations"

sys.path.insert(0, str(TRANS))
from path_maps import RO_TO_EN, RO_TO_IT  # noqa: E402

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

RO_MARK = re.compile(r"[ăâîșțĂÂÎȘȚ]")


def build_it_to_en() -> dict[str, str]:
    mapping: dict[str, str] = {}

    fr_en = json.loads((TRANS / "fr_to_en.json").read_text(encoding="utf-8"))
    fr_it = json.loads((TRANS / "fr_to_it.json").read_text(encoding="utf-8"))
    for fr, en in fr_en.items():
        it = fr_it.get(fr)
        if it and en:
            mapping[it] = en

    me = json.loads((TRANS / "mercury_fr_to_en.json").read_text(encoding="utf-8"))
    mi_path = TRANS / "mercury_fr_to_it.json"
    if mi_path.exists():
        mi = json.loads(mi_path.read_text(encoding="utf-8"))
        for fr in set(me) & set(mi):
            if me[fr] and mi.get(fr):
                mapping[mi[fr]] = me[fr]

    it_json = json.loads((TRANS / "it.json").read_text(encoding="utf-8"))
    en_json = json.loads((TRANS / "en.json").read_text(encoding="utf-8"))
    # it.json keys are often RO-mixed → en values; also copy direct IT snippets from fr pivot
    for ro_key, en_val in en_json.items():
        if en_val and RO_MARK.search(ro_key):
            mapping[ro_key] = en_val

    # British English fixes for mercury banner / nav (RO strings on EN homepage)
    mapping.update(
        {
            "Detectăm că ești în": "We detect that you are in",
            "Da, mergi": "Yes, go there",
            "Rămân aici": "Stay here",
            "Navigare principală": "Main navigation",
            "Redirecționare către": "Redirecting to",
            "Vizitezi": "You are visiting",
            "Choisir le pays": "Choose country",
        }
    )

    return {k: v for k, v in mapping.items() if k and v}


def build_path_replacements() -> list[tuple[str, str]]:
    """IT URL segment → EN URL segment (longest first)."""
    it_to_en: dict[str, str] = {}
    for ro, en in RO_TO_EN.items():
        it = RO_TO_IT.get(ro)
        if it:
            it_to_en[it] = en
    # FR-origin IT slugs not in RO map
    extra = {
        "chi-siamo": "about",
        "risorse": "resources",
        "progetti": "projects",
        "risparmi": "savings",
        "preventivo": "quote",
        "confronto": "comparison",
        "calcolatore": "calculator",
        "testimonianze": "testimonials",
        "diventa-partner": "become-a-partner",
        "prodotti": "products",
        "per": "for",
        "pareti-mbk": "walls-mbk",
        "solai-pbk": "floors-pbk",
        "tetto-tbk": "roof-tbk",
        "accessori": "accessories",
        "proprietari": "homeowners",
        "architetti": "architects",
        "costruttori": "builders",
        "investitori": "investors",
        "certificazioni": "certifications",
        "fabbriche": "factories",
        "fondatore": "founder",
        "brevetto": "patent",
        "casa-cluj-napoca": "house-cluj-napoca",
        "complesso-lyon": "lyon-development",
        "villa-valencia": "villa-valencia",
        "privacy": "privacy",
        "sostenibilita": "sustainability",
        "condizioni": "terms",
        "note-legali": "legal-notice",
        "montaggio": "installation",
        "cookie": "cookies",
        "cos-e-la-casa-passiva": "what-is-a-passive-house",
    }
    it_to_en.update(extra)
    return sorted(it_to_en.items(), key=lambda x: -len(x[0]))


EN_TO_IT_SEG = {}
for ro, en in RO_TO_EN.items():
    it = RO_TO_IT.get(ro)
    if it:
        EN_TO_IT_SEG[en] = it
for k, v in {
    "about": "chi-siamo",
    "resources": "risorse",
    "projects": "progetti",
    "savings": "risparmi",
    "quote": "preventivo",
    "calculator": "calcolatore",
    "testimonials": "testimonianze",
    "become-a-partner": "diventa-partner",
    "products": "prodotti",
    "for": "per",
    "walls-mbk": "pareti-mbk",
    "floors-pbk": "solai-pbk",
    "roof-tbk": "tetto-tbk",
    "homeowners": "proprietari",
    "architects": "architetti",
    "builders": "costruttori",
    "investors": "investitori",
    "certifications": "certificazioni",
    "factories": "fabbriche",
    "founder": "fondatore",
    "patent": "brevetto",
    "house-cluj-napoca": "casa-cluj-napoca",
    "lyon-development": "complesso-lyon",
    "villa-valencia": "villa-valencia",
    "sustainability": "sostenibilita",
    "terms": "condizioni",
    "legal-notice": "note-legali",
    "installation": "montaggio",
    "what-is-a-passive-house": "cos-e-la-casa-passiva",
}.items():
    EN_TO_IT_SEG[k] = v


def en_rel_to_it_rel(rel: str) -> str:
    parts = rel.split("/")
    return "/".join(EN_TO_IT_SEG.get(p, p) for p in parts)


def localise_paths(text: str, path_pairs: list[tuple[str, str]]) -> str:
    for it_seg, en_seg in path_pairs:
        text = text.replace(f"/{it_seg}/", f"/{en_seg}/")
        text = text.replace(f'="{it_seg}/', f'="{en_seg}/')
        text = text.replace(f"='{it_seg}/", f"='{en_seg}/")
        text = text.replace(f"/{it_seg}\"", f"/{en_seg}\"")
        text = text.replace(f"/{it_seg}'", f"/{en_seg}'")
    return text


def apply_dict(text: str, mapping: dict[str, str], passes: int = 3) -> str:
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


def sync_file(en_path: Path, mapping: dict[str, str], path_pairs: list[tuple[str, str]]) -> bool:
    rel = en_path.relative_to(EN_DIR).as_posix()
    if rel == "index.html":
        new = (
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '  <meta charset="UTF-8">\n'
            '  <meta http-equiv="refresh" content="0; url=polistibrick-mercury-style.html">\n'
            "  <title>Polistibrick</title>\n</head>\n<body data-base=\"\">\n"
            '  <p>Redirecting to <a href="polistibrick-mercury-style.html">Polistibrick</a>…</p>\n'
            "</body>\n</html>\n"
        )
        if en_path.read_text(encoding="utf-8") != new:
            en_path.write_text(new, encoding="utf-8")
            return True
        return False

    it_rel = en_rel_to_it_rel(rel)
    it_path = IT_DIR / it_rel
    if not it_path.exists():
        print(f"  ⚠ no IT source for {rel} (tried {it_rel})")
        return False

    text = it_path.read_text(encoding="utf-8")
    text = text.replace('<html lang="it">', '<html lang="en">', 1)
    text = text.replace('<html lang="it" ', '<html lang="en" ', 1)
    text = localise_paths(text, path_pairs)
    text = apply_dict(text, mapping, passes=4)

    # British English preference
    text = text.replace("certified and internationally recognized", "certified and internationally recognised")
    text = text.replace("Certified and internationally recognized", "Certified and internationally recognised")

    original = en_path.read_text(encoding="utf-8")
    if text != original:
        en_path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    mapping = build_it_to_en()
    path_pairs = build_path_replacements()
    print(f"IT→EN mapping: {len(mapping)} keys")
    changed = 0
    for en_file in sorted(EN_DIR.rglob("*.html")):
        if sync_file(en_file, mapping, path_pairs):
            print(f"  ✓ {en_file.relative_to(EN_DIR)}")
            changed += 1
    print(f"\nUpdated {changed} files")


if __name__ == "__main__":
    main()
