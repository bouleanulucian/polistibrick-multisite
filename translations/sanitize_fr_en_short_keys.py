#!/usr/bin/env python3
"""Remove dangerously short FR→EN keys that cause partial hybrid replacements."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"

# Keys that must never be used (substring false positives)
REMOVE = {
    "Pour le",
    ", votre",
    "Nous vous",
    "et notre",
    ". Dès votre",
    "ont conçu.",
    "portée.",
    "Concrètement,",
    "ne brûle pas",
    "Gros œuvre en",
    "Vous comparez",
    "Nous avons un",
}

# Full-phrase replacements to add instead
ADD = {
    "Pour les propriétaires": "For homeowners",
    "Pour les architectes": "For architects",
    "Pour les constructeurs": "For builders",
    "Pour les investisseurs": "For investors",
    "Pour le propriétaire": "For the homeowner",
    "Pour le constructeur": "For the builder",
    "Pour le BET": "For the structural engineer",
    "Pour le promoteur": "For the developer",
}


def main() -> None:
    for name in ("fr_en_glossary_short.json", "extra_fr_to_en.json"):
        path = TRANS / name
        data = json.loads(path.read_text(encoding="utf-8"))
        removed = sum(1 for k in REMOVE if k in data and data.pop(k, None))
        added = 0
        for k, v in ADD.items():
            if k not in data or not data[k]:
                data[k] = v
                added += 1
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{name}: removed {removed}, added {added}")


if __name__ == "__main__":
    main()
