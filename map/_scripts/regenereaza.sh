#!/usr/bin/env bash
# Reface ce e generat în hartă, ca să nu se editeze de mână:
#   1. map/objects/_index.md  — un rând pe fișă, din antetele YAML
#   2. map/AGENTS.md, map/routing.md — copii byte-cu-byte ale map/CLAUDE.md
#   3. AGENTS.md la rădăcină — copie a CLAUDE.md de la rădăcină
# Rulează din oriunde: bash map/_scripts/regenereaza.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MAP="$ROOT/map"

python3 - "$MAP" <<'PY'
import sys, re, pathlib
MAP = pathlib.Path(sys.argv[1])
rows = []
for p in sorted((MAP / "objects").glob("*.md")):
    if p.name.startswith("_") or p.name == "CONTEXT.md":
        continue
    txt = p.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    title = next((l[2:].strip() for l in txt.splitlines() if l.startswith("# ")), p.stem)
    rows.append((meta.get("cluster", "?"), p.name, title, meta.get("universe", "?"), meta.get("status", "?"), meta.get("verified_at", "")))
rows.sort()
out = ["# objects — index (generat de _scripts/regenereaza.sh; nu edita de mână)", "",
       "| Cluster | Fișă | Ce e | Univers | Stare |", "|---|---|---|---|---|"]
for cl, name, title, uni, st, when in rows:
    stare = f"{st} {when}".strip()
    out.append(f"| {cl} | [{name}]({name}) | {title} | {uni} | {stare} |")
(MAP / "objects" / "_index.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"_index.md: {len(rows)} fișe")
PY

cp "$MAP/CLAUDE.md" "$MAP/AGENTS.md"
cp "$MAP/CLAUDE.md" "$MAP/routing.md"
cp "$ROOT/CLAUDE.md" "$ROOT/AGENTS.md"
echo "gemeni: map/AGENTS.md, map/routing.md, AGENTS.md"
