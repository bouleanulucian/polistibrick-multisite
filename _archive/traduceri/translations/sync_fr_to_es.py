#!/usr/bin/env python3
"""Sync countries/es HTML from countries/fr with safe FR→ES translation + path rewrite."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FR_DIR = ROOT / "countries" / "fr"
ES_DIR = ROOT / "countries" / "es"
TRANS = ROOT / "translations"

sys.path.insert(0, str(ROOT))
from translations.path_maps import FR_TO_ES, FR_TO_IT  # noqa: E402

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

ATTR_PROTECT = re.compile(
    r'((?:href|src|action)=["\'])([^"\']*)(["\'])',
    re.IGNORECASE,
)

BRAND_PROTECT = re.compile(
    r"\b(MBK|PBK|TBK|ICF|EPS|A\+\+\+|REI\s*240)\b"
)

ES_TO_FR = {v: k for k, v in FR_TO_ES.items()}

# Keys too short or ambiguous for naive substring replace
BLOCKED_KEYS = frozenset(
    {
        "brick",
        "site.",
        "place.",
        "noi",
        "el",
        "de",
        "la",
        "cu",
        "si",
        "sau",
        "dar",
        "in",
        "pe",
        "la",
        "un",
        "une",
        "le",
        "les",
        "des",
        "et",
        "ou",
        "en",
        "du",
        "au",
        "ce",
        "se",
        "te",
        "me",
        "ma",
        "ta",
        "tu",
        "vs",
    }
)


def es_rel_to_fr_rel(es_rel: str) -> str:
    rel = es_rel.replace("\\", "/")
    if rel in ("index.html", "polistibrick-mercury-style.html"):
        return rel
    if rel.endswith("/index.html"):
        rel = rel[: -len("/index.html")]
    parts = [p for p in rel.split("/") if p]
    fr_parts: list[str] = []
    for seg in parts:
        fr = ES_TO_FR.get(seg)
        if fr:
            fr_parts.append(fr)
        elif seg in FR_TO_ES:
            fr_parts.append(seg)
        else:
            fr_parts.append(seg)
    if not fr_parts:
        return "index.html"
    return "/".join(fr_parts) + "/index.html"


def filter_mapping(mapping: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in mapping.items():
        if not k or not v or k == v:
            continue
        if k in BLOCKED_KEYS:
            continue
        if len(k) < 8 and " " not in k and "<" not in k:
            continue
        out[k] = v
    return out


def protect_fragile(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}
    idx = 0

    def stash(value: str) -> str:
        nonlocal idx
        key = f"@@PB{idx}@@"
        tokens[key] = value
        idx += 1
        return key

    def attr_repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}{stash(match.group(2))}{match.group(3)}"

    text = ATTR_PROTECT.sub(attr_repl, text)
    text = BRAND_PROTECT.sub(lambda m: stash(m.group(0)), text)
    return text, tokens


def restore_fragile(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace(key, value)
    return text


def apply_dict(text: str, mapping: dict[str, str]) -> str:
    if not mapping:
        return text
    keys = sorted(mapping.keys(), key=len, reverse=True)
    segments: list[tuple[str, str]] = []
    last_end = 0
    for m in SKIP.finditer(text):
        segments.append(("translate", text[last_end : m.start()]))
        segments.append(("skip", m.group(0)))
        last_end = m.end()
    segments.append(("translate", text[last_end:]))
    out: list[str] = []
    for kind, segment in segments:
        if kind == "skip":
            out.append(segment)
            continue
        protected, tokens = protect_fragile(segment)
        for src in keys:
            tr = mapping[src]
            if tr:
                protected = protected.replace(src, tr)
        out.append(restore_fragile(protected, tokens))
    return "".join(out)


def rewrite_paths(html: str) -> str:
    for fr_seg, es_seg in sorted(FR_TO_ES.items(), key=lambda x: -len(x[0])):
        html = html.replace(f"/{fr_seg}/", f"/{es_seg}/")
        html = html.replace(f'"{fr_seg}/', f'"{es_seg}/')
        html = html.replace(f"'{fr_seg}/", f"'{es_seg}/")
    html = html.replace("polistibrick.fr", "polistibrick.es")
    html = html.replace("devis.polistibrick.fr", "devis.polistibrick.es")
    html = html.replace('lang="fr"', 'lang="es"')
    return html


def load_mapping() -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in ("fr_to_es.json", "mercury_fr_to_es.json", "extra_fr_to_es.json", "es_overrides.json"):
        p = TRANS / name
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            for k, v in data.items():
                if k and v:
                    merged[k] = v
    return filter_mapping(merged)


def sync_file(es_path: Path, mapping: dict[str, str]) -> bool:
    es_rel = es_path.relative_to(ES_DIR).as_posix()
    fr_rel = es_rel_to_fr_rel(es_rel)
    fr_path = FR_DIR / fr_rel
    if not fr_path.exists():
        print(f"  ✗ missing FR source: {fr_rel} for {es_rel}")
        return False

    original = es_path.read_text(encoding="utf-8")
    text = fr_path.read_text(encoding="utf-8")
    for _ in range(3):
        text = apply_dict(text, mapping)
    text = rewrite_paths(text)
    if text != original:
        es_path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    mapping = load_mapping()
    print(f"=== sync_fr_to_es: {len(mapping)} safe translation keys ===")
    changed = 0
    for es_path in sorted(ES_DIR.rglob("*.html")):
        if sync_file(es_path, mapping):
            changed += 1
            print(f"  ✓ {es_path.relative_to(ES_DIR)}")
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
