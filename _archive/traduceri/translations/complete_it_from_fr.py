#!/usr/bin/env python3
"""
Complete countries/it/ HTML from countries/fr/ reference + translation dicts.

Preserves IT URL slugs, lang=it, {{placeholders}}, href/src paths.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IT_DIR = ROOT / "countries" / "it"
FR_DIR = ROOT / "countries" / "fr"
TRANS = ROOT / "translations"

sys.path.insert(0, str(TRANS))
from path_maps import FR_TO_IT  # noqa: E402

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

IT_TO_FR = {it: fr for fr, it in FR_TO_IT.items()}
FR_TO_IT_PATHS = sorted(FR_TO_IT.items(), key=lambda x: -len(x[0]))


def load_mercury_py() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location(
        "tm", TRANS / "translate_mercury_it.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TRANSLATIONS


def build_translation_dict() -> dict[str, str]:
    merged: dict[str, str] = {}
    for pattern in (
        "fr_to_it.json",
        "mercury_fr_to_it.json",
        "extra_fr_to_it.json",
        "remaining_fr_it.json",
        "pass3_fr_to_it.json",
        "it_chunk_A.json",
        "it_chunk_B.json",
    ):
        p = TRANS / pattern
        if not p.exists():
            continue
        for k, v in json.loads(p.read_text(encoding="utf-8")).items():
            if k and v:
                merged[k] = v
    for k, v in load_mercury_py().items():
        if k and v:
            merged[k] = v
    return merged


def it_rel_to_fr_rel(rel: str) -> str:
    parts = rel.split("/")
    return "/".join(IT_TO_FR.get(p, p) for p in parts)


def localise_fr_paths_to_it(text: str) -> str:
    for fr_seg, it_seg in FR_TO_IT_PATHS:
        text = text.replace(f"/{fr_seg}/", f"/{it_seg}/")
        text = text.replace(f'="{fr_seg}/', f'="{it_seg}/')
        text = text.replace(f"='{fr_seg}/", f"='{it_seg}/")
        text = text.replace(f"/{fr_seg}\"", f"/{it_seg}\"")
        text = text.replace(f"/{fr_seg}'", f"/{it_seg}'")
        text = text.replace(f"../{fr_seg}/", f"../{it_seg}/")
        text = text.replace(f"../../{fr_seg}/", f"../../{it_seg}/")
    text = text.replace("polistibrick.fr", "polistibrick.it")
    text = text.replace("devis.polistibrick.fr", "devis.polistibrick.it")
    return text


def apply_dict(text: str, mapping: dict[str, str], passes: int = 5) -> str:
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


def sync_file(it_path: Path, mapping: dict[str, str]) -> bool:
    rel = it_path.relative_to(IT_DIR).as_posix()

    if rel == "index.html":
        new = (
            '<!DOCTYPE html>\n<html lang="it">\n<head>\n'
            '  <meta charset="UTF-8">\n'
            '  <meta http-equiv="refresh" content="0; url=polistibrick-mercury-style.html">\n'
            "  <title>Polistibrick</title>\n</head>\n<body data-base=\"\">\n"
            '  <p>Reindirizzamento a <a href="polistibrick-mercury-style.html">Polistibrick</a>…</p>\n'
            "</body>\n</html>\n"
        )
        if it_path.read_text(encoding="utf-8") != new:
            it_path.write_text(new, encoding="utf-8")
            return True
        return False

    fr_rel = it_rel_to_fr_rel(rel)
    fr_path = FR_DIR / fr_rel
    if not fr_path.exists():
        print(f"  ⚠ no FR source for {rel} (tried {fr_rel})")
        return False

    text = fr_path.read_text(encoding="utf-8")
    text = text.replace('<html lang="fr">', '<html lang="it">', 1)
    text = text.replace('<html lang="fr" ', '<html lang="it" ', 1)
    text = localise_fr_paths_to_it(text)
    text = apply_dict(text, mapping, passes=5)

    original = it_path.read_text(encoding="utf-8")
    if text != original:
        it_path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    mapping = build_translation_dict()
    print(f"Translation dict: {len(mapping)} keys")
    changed = 0
    for it_file in sorted(IT_DIR.rglob("*.html")):
        if sync_file(it_file, mapping):
            print(f"  ✓ {it_file.relative_to(IT_DIR)}")
            changed += 1
    print(f"\nUpdated {changed} files")


if __name__ == "__main__":
    main()
