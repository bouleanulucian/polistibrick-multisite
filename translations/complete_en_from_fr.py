#!/usr/bin/env python3
"""
Complete countries/en/ HTML from countries/fr/ reference + translation dicts.

Preserves EN URL slugs, lang=en, {{placeholders}}, href/src paths.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "countries" / "en"
FR_DIR = ROOT / "countries" / "fr"
TRANS = ROOT / "translations"

sys.path.insert(0, str(TRANS))
from path_maps import FR_TO_EN  # noqa: E402

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

EN_TO_FR = {en: fr for fr, en in FR_TO_EN.items()}
FR_TO_EN_PATHS = sorted(FR_TO_EN.items(), key=lambda x: -len(x[0]))


def build_translation_dict() -> dict[str, str]:
    merged: dict[str, str] = {}
    for pattern in [
        "fr_to_en.json",
        "mercury_fr_to_en.json",
        "extra_fr_to_en.json",
        "en_fr_bridge.json",
        "fr_en_glossary_short.json",
        "remaining_fr_en.json",
    ]:
        p = TRANS / pattern
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for k, v in data.items():
            if k and v:
                merged[k] = v

    # Targeted British English (safe phrases only)
    merged.update(
        {
            "internationally recognized": "internationally recognised",
            "Internationally recognized": "Internationally recognised",
            "certified and internationally recognized": "certified and internationally recognised",
            "Certified and internationally recognized": "Certified and internationally recognised",
        }
    )
    return merged


def en_rel_to_fr_rel(rel: str) -> str:
    parts = rel.split("/")
    return "/".join(EN_TO_FR.get(p, p) for p in parts)


def localise_fr_paths_to_en(text: str) -> str:
    for fr_seg, en_seg in FR_TO_EN_PATHS:
        text = text.replace(f"/{fr_seg}/", f"/{en_seg}/")
        text = text.replace(f'="{fr_seg}/', f'="{en_seg}/')
        text = text.replace(f"='{fr_seg}/", f"='{en_seg}/")
        text = text.replace(f"/{fr_seg}\"", f"/{en_seg}\"")
        text = text.replace(f"/{fr_seg}'", f"/{en_seg}'")
        text = text.replace(f"../{fr_seg}/", f"../{en_seg}/")
        text = text.replace(f"../../{fr_seg}/", f"../../{en_seg}/")
    return text


def apply_dict(text: str, mapping: dict[str, str], passes: int = 4) -> str:
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


def sync_file(en_path: Path, mapping: dict[str, str]) -> bool:
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

    fr_rel = en_rel_to_fr_rel(rel)
    fr_path = FR_DIR / fr_rel
    if not fr_path.exists():
        print(f"  ⚠ no FR source for {rel} (tried {fr_rel})")
        return False

    text = fr_path.read_text(encoding="utf-8")
    text = text.replace('<html lang="fr">', '<html lang="en">', 1)
    text = text.replace('<html lang="fr" ', '<html lang="en" ', 1)
    text = localise_fr_paths_to_en(text)
    text = apply_dict(text, mapping, passes=5)

    original = en_path.read_text(encoding="utf-8")
    if text != original:
        en_path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    mapping = build_translation_dict()
    print(f"Translation dict: {len(mapping)} keys")
    changed = 0
    for en_file in sorted(EN_DIR.rglob("*.html")):
        if sync_file(en_file, mapping):
            print(f"  ✓ {en_file.relative_to(EN_DIR)}")
            changed += 1
    print(f"\nUpdated {changed} files")


if __name__ == "__main__":
    main()
