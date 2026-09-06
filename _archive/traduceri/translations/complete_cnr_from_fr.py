#!/usr/bin/env python3
"""Complete countries/me/ HTML from FR + path rewrite (Montenegrin / cnr)."""
from __future__ import annotations

import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
ME_DIR = ROOT / "countries" / "me"
FR_DIR = ROOT / "countries" / "fr"
TRANS = ROOT / "translations"

sys.path.insert(0, str(TRANS))
from path_maps import FR_TO_CNR  # noqa: E402

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

CNR_TO_FR = {cnr: fr for fr, cnr in FR_TO_CNR.items()}
FR_TO_CNR_PATHS = sorted(FR_TO_CNR.items(), key=lambda x: -len(x[0]))


def build_translation_dict() -> dict[str, str]:
    merged: dict[str, str] = {}
    for pattern in ["cnr.json", "fr_to_cnr.json", "mercury_fr_to_cnr.json", "extra_fr_to_cnr.json"]:
        p = TRANS / pattern
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for k, v in data.items():
            if k and v:
                merged[k] = v
    return merged


def me_rel_to_fr_rel(rel: str) -> str:
    parts = rel.split("/")
    return "/".join(CNR_TO_FR.get(p, p) for p in parts)


def localise_fr_paths_to_cnr(text: str) -> str:
    for fr_seg, cnr_seg in FR_TO_CNR_PATHS:
        text = text.replace(f"/{fr_seg}/", f"/{cnr_seg}/")
        text = text.replace(f'="{fr_seg}/', f'="{cnr_seg}/')
        text = text.replace(f"='{fr_seg}/", f"='{cnr_seg}/")
        text = text.replace(f"/{fr_seg}\"", f"/{cnr_seg}\"")
        text = text.replace(f"/{fr_seg}'", f"/{cnr_seg}'")
        text = text.replace(f"../{fr_seg}/", f"../{cnr_seg}/")
        text = text.replace(f"../../{fr_seg}/", f"../../{cnr_seg}/")
    return text


def apply_dict(text: str, mapping: dict[str, str], passes: int = 4) -> str:
    keys = sorted(mapping.keys(), key=len, reverse=True)
    word_re: dict[str, re.Pattern[str]] = {}
    for key in keys:
        if " " not in key and len(key) < 12:
            word_re[key] = re.compile(
                r"(?<![\wÀ-ſ])" + re.escape(key) + r"(?![\wÀ-ſ])"
            )

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
                if not val:
                    continue
                if key in word_re:
                    segment = word_re[key].sub(val, segment)
                else:
                    segment = segment.replace(key, val)
        out.append(segment)
    return "".join(out)


def sync_file(me_path: Path, mapping: dict[str, str]) -> bool:
    rel = me_path.relative_to(ME_DIR).as_posix()
    if rel == "index.html":
        new = (
            '<!DOCTYPE html>\n<html lang="cnr">\n<head>\n'
            '  <meta charset="UTF-8">\n'
            '  <meta http-equiv="refresh" content="0; url=polistibrick-mercury-style.html">\n'
            "  <title>Polistibrick</title>\n</head>\n<body data-base=\"\">\n"
            '  <p>Preusmjeravanje na <a href="polistibrick-mercury-style.html">Polistibrick</a>…</p>\n'
            "</body>\n</html>\n"
        )
        if me_path.read_text(encoding="utf-8") != new:
            me_path.write_text(new, encoding="utf-8")
            return True
        return False

    fr_rel = me_rel_to_fr_rel(rel)
    fr_path = FR_DIR / fr_rel
    if not fr_path.exists():
        print(f"  ⚠ no FR source for {rel} (tried {fr_rel})")
        return False

    text = fr_path.read_text(encoding="utf-8")
    text = text.replace('<html lang="fr">', '<html lang="cnr">', 1)
    text = text.replace('<html lang="fr" ', '<html lang="cnr" ', 1)
    text = localise_fr_paths_to_cnr(text)
    text = apply_dict(text, mapping, passes=5)

    original = me_path.read_text(encoding="utf-8")
    if text != original:
        me_path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    mapping = build_translation_dict()
    print(f"Translation dict: {len(mapping)} keys")
    changed = 0
    for me_file in sorted(ME_DIR.rglob("*.html")):
        if sync_file(me_file, mapping):
            print(f"  ✓ {me_file.relative_to(ME_DIR)}")
            changed += 1
    print(f"\nUpdated {changed} files")


if __name__ == "__main__":
    main()
