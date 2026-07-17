#!/usr/bin/env python3
"""Sync countries/es HTML from countries/it with safe IT→ES text + localized path rewrite."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IT_DIR = ROOT / "countries" / "it"
ES_DIR = ROOT / "countries" / "es"
TRANS = ROOT / "translations"

sys.path.insert(0, str(ROOT))
from translations.path_maps import FR_TO_ES, FR_TO_IT  # noqa: E402
from translations.sync_fr_to_es import (  # noqa: E402
    BLOCKED_KEYS,
    apply_dict,
    filter_mapping,
    protect_fragile,
    restore_fragile,
)

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

SEG_IT_TO_ES: dict[str, str] = {}
for fr, it_seg in FR_TO_IT.items():
    es_seg = FR_TO_ES.get(fr, fr)
    if it_seg != es_seg:
        SEG_IT_TO_ES[it_seg] = es_seg

ES_TO_FR = {v: k for k, v in FR_TO_ES.items()}


def es_rel_to_it_rel(es_rel: str) -> str:
    rel = es_rel.replace("\\", "/")
    if rel in ("index.html", "polistibrick-mercury-style.html"):
        return rel
    if rel.endswith("/index.html"):
        rel = rel[: -len("/index.html")]
    parts = [p for p in rel.split("/") if p]
    it_parts: list[str] = []
    for seg in parts:
        fr = ES_TO_FR.get(seg)
        if fr:
            it_parts.append(FR_TO_IT.get(fr, seg))
        elif seg in FR_TO_IT:
            it_parts.append(FR_TO_IT[seg])
        else:
            it_parts.append(seg)
    if not it_parts:
        return "index.html"
    return "/".join(it_parts) + "/index.html"


def rewrite_paths(html: str) -> str:
    for it_seg, es_seg in sorted(SEG_IT_TO_ES.items(), key=lambda x: -len(x[0])):
        html = html.replace(f"/{it_seg}/", f"/{es_seg}/")
        html = html.replace(f'"{it_seg}/', f'"{es_seg}/')
        html = html.replace(f"'{it_seg}/", f"'{es_seg}/")
    html = html.replace("polistibrick.it", "polistibrick.es")
    html = html.replace("devis.polistibrick.it", "devis.polistibrick.es")
    html = html.replace('lang="it"', 'lang="es"')
    return html


def load_merged_mapping() -> dict[str, str]:
    merged: dict[str, str] = {}

    it_dict = json.loads((TRANS / "it.json").read_text(encoding="utf-8"))
    es_dict = json.loads((TRANS / "es.json").read_text(encoding="utf-8"))
    for ro, it_val in it_dict.items():
        es_val = es_dict.get(ro)
        if it_val and es_val and it_val != es_val:
            merged[it_val] = es_val

    for name in ("fr_to_es.json", "mercury_fr_to_es.json", "extra_fr_to_es.json"):
        p = TRANS / name
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            for k, v in data.items():
                if k and v:
                    merged[k] = v

    overrides = TRANS / "es_overrides.json"
    if overrides.exists():
        data = json.loads(overrides.read_text(encoding="utf-8"))
        merged.update({k: v for k, v in data.items() if k and v})

    return filter_mapping(merged)


def sync_file(es_path: Path, mapping: dict[str, str]) -> bool:
    es_rel = es_path.relative_to(ES_DIR).as_posix()
    it_rel = es_rel_to_it_rel(es_rel)
    it_path = IT_DIR / it_rel
    if not it_path.exists():
        print(f"  ✗ missing IT source: {it_rel} for {es_rel}")
        return False

    original = es_path.read_text(encoding="utf-8")
    text = it_path.read_text(encoding="utf-8")
    for _ in range(3):
        text = apply_dict(text, mapping)
    text = rewrite_paths(text)
    if text != original:
        es_path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    mapping = load_merged_mapping()
    print(f"=== sync_it_to_es: {len(mapping)} safe translation keys ===")
    changed = 0
    for es_path in sorted(ES_DIR.rglob("*.html")):
        if sync_file(es_path, mapping):
            changed += 1
            print(f"  ✓ {es_path.relative_to(ES_DIR)}")
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
