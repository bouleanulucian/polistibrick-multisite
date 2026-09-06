#!/usr/bin/env python3
"""Build extra_fr_to_en entries from exact FR source strings + en.json bridge."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FR_DIR = ROOT / "countries" / "fr"
TRANS = ROOT / "translations"

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)
TAG = re.compile(r"<[^>]+>")
FR_MARK = re.compile(
    r"[àâäéèêëïîôùûüçœæ]"
    r"|\b(Nous|Vous|Votre|Notre|Les|Des|Une|Pour|Comment|Demandez|devis|maison|système|"
    r"construire|propriétaire|architecte|constructeur|investisseur|témoignage|économies|"
    r"ressources|mentions|confidentialité|politique|bientôt|Sélectionnez|Écrivez|Téléversez)\b",
    re.I,
)


def load_merged_dict() -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in (
        "en.json",
        "fr_to_en.json",
        "mercury_fr_to_en.json",
        "extra_fr_to_en.json",
        "en_fr_bridge.json",
    ):
        p = TRANS / name
        if p.exists():
            for k, v in json.loads(p.read_text(encoding="utf-8")).items():
                if k and v:
                    merged[k] = v
    return merged


def extract_phrases(html: str) -> set[str]:
    cleaned = SKIP.sub(" ", html)
    phrases: set[str] = set()
    for part in TAG.split(cleaned):
        p = part.strip()
        if 3 <= len(p) <= 400 and FR_MARK.search(p) and "{{" not in p:
            phrases.add(p)
    return phrases


def britishise(text: str) -> str:
    repl = (
        ("personalized", "personalised"),
        ("Personalized", "Personalised"),
        ("recognized", "recognised"),
        ("Recognized", "Recognised"),
        ("organization", "organisation"),
        ("Organization", "Organisation"),
        ("center", "centre"),
        ("Center", "Centre"),
        ("color", "colour"),
        ("Color", "Colour"),
    )
    for a, b in repl:
        text = text.replace(a, b)
    return text


def main():
    fr_dict = json.loads((TRANS / "fr.json").read_text(encoding="utf-8"))
    en_dict = json.loads((TRANS / "en.json").read_text(encoding="utf-8"))
    fr_to_ro = {v: k for k, v in fr_dict.items() if v}
    existing = load_merged_dict()
    extra_path = TRANS / "extra_fr_to_en.json"
    extra = json.loads(extra_path.read_text(encoding="utf-8"))

    needed: set[str] = set()
    for html in FR_DIR.rglob("*.html"):
        needed |= extract_phrases(html.read_text(encoding="utf-8"))

    added = 0
    for fr_phrase in sorted(needed, key=len, reverse=True):
        if fr_phrase in existing and existing[fr_phrase]:
            continue
        if fr_phrase in extra and extra[fr_phrase]:
            continue
        ro = fr_to_ro.get(fr_phrase)
        if ro and ro in en_dict and en_dict[ro] and en_dict[ro] != fr_phrase:
            extra[fr_phrase] = britishise(en_dict[ro])
            added += 1
            continue
        # fuzzy: strip HTML for short inner text
        inner = TAG.sub("", fr_phrase).strip()
        if inner != fr_phrase:
            ro = fr_to_ro.get(inner)
            if ro and ro in en_dict and en_dict[ro]:
                extra[fr_phrase] = britishise(en_dict[ro])
                added += 1

    extra_path.write_text(json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FR source phrases: {len(needed)}")
    print(f"Added via bridge: {added}")
    print(f"Extra total: {len(extra)}")


if __name__ == "__main__":
    main()
