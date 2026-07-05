#!/usr/bin/env bash
# Publică preview pe GitHub Pages (NU atinge polistibrick.ro / .fr).
# URL: https://bouleanulucian.github.io/polistibrick-multisite/
#
# Usage:
#   ./scripts/deploy-preview.sh           — build ro + fr, push gh-pages
#   ./scripts/deploy-preview.sh ro        — doar România
#   ./scripts/deploy-preview.sh fr        — doar France
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKTREE="$ROOT/.gh-pages-worktree"
COUNTRIES=("$@")
if [[ ${#COUNTRIES[@]} -eq 0 ]]; then
  COUNTRIES=(ro fr)
fi

echo "→ Build: ${COUNTRIES[*]}"
python3 "$ROOT/build/build.py" "${COUNTRIES[@]}"

if [[ ! -d "$WORKTREE" ]]; then
  echo "→ Worktree gh-pages…"
  git -C "$ROOT" worktree add "$WORKTREE" gh-pages
fi

git -C "$WORKTREE" pull --ff-only origin gh-pages 2>/dev/null || true

for code in "${COUNTRIES[@]}"; do
  dest="$WORKTREE/$code"
  src="$ROOT/build/$code"
  if [[ ! -d "$src" ]]; then
    echo "❌ Lipsă build/$code — rulează build.py"
    exit 1
  fi
  echo "→ Sync $code/ …"
  mkdir -p "$dest"
  rsync -a --delete "$src/" "$dest/"
done

# Root files (redirect + hub țări)
for f in index.html preview.html .nojekyll; do
  if [[ -f "$ROOT/scripts/gh-pages/$f" ]]; then
    cp "$ROOT/scripts/gh-pages/$f" "$WORKTREE/$f"
  fi
done

touch "$WORKTREE/.nojekyll"

cd "$WORKTREE"
if git diff --quiet && git diff --cached --quiet; then
  echo "✓ gh-pages deja la zi — nimic de publicat."
  exit 0
fi

git add -A
git commit -m "$(cat <<EOF
Preview GitHub Pages — ${COUNTRIES[*]}

Build din main pentru review (fără domenii live).
EOF
)"

echo "→ Push gh-pages…"
git push origin gh-pages

echo ""
echo "✓ Preview live (1–2 min cache GitHub):"
echo "  https://bouleanulucian.github.io/polistibrick-multisite/preview.html"
for code in "${COUNTRIES[@]}"; do
  echo "  https://bouleanulucian.github.io/polistibrick-multisite/$code/"
done
