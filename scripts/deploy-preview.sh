#!/usr/bin/env bash
# Publică preview pe GitHub Pages (NU atinge polistibrick.ro / .fr).
# URL: https://bouleanulucian.github.io/polistibrick-multisite/
#
# Media o SINGURĂ dată: /fr/images/ (setul complet din build/fr).
# Celelalte țări = HTML + assets; path-urile media → /REPO/fr/images/...
#
# Usage:
#   ./scripts/deploy-preview.sh                — toate țările
#   ./scripts/deploy-preview.sh fr ro en       — subset
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKTREE="$ROOT/.gh-pages-worktree"
REPO_NAME="$(basename "$(git -C "$ROOT" rev-parse --show-toplevel)")"
# Media trăiește sub /REPO/fr/images/ pe github.io
PAGES_IMG_PREFIX="/${REPO_NAME}/fr/images/"
ALL_COUNTRIES=(de en es fr ie it me nl ro)
COUNTRIES=("$@")
if [[ ${#COUNTRIES[@]} -eq 0 ]]; then
  COUNTRIES=("${ALL_COUNTRIES[@]}")
fi

# FR trebuie mereu (ține media)
has_fr=0
for c in "${COUNTRIES[@]}"; do [[ "$c" == fr ]] && has_fr=1; done
if [[ "$has_fr" -eq 0 ]]; then
  COUNTRIES=(fr "${COUNTRIES[@]}")
fi

echo "→ Build: ${COUNTRIES[*]}"
python3 "$ROOT/build/build.py" "${COUNTRIES[@]}"

if [[ ! -d "$WORKTREE" ]]; then
  echo "→ Worktree gh-pages…"
  git -C "$ROOT" worktree add "$WORKTREE" gh-pages
fi

git -C "$WORKTREE" pull --ff-only origin gh-pages 2>/dev/null || true

rewrite_media_paths() {
  local dest="$1"
  python3 - "$dest" "$PAGES_IMG_PREFIX" <<'PY'
import re, sys
from pathlib import Path

root = Path(sys.argv[1])
prefix = sys.argv[2]  # /repo/fr/images/

# data-src, data-src-desktop, data-src-mobile, src, poster, href, srcset
attr_pat = re.compile(
    r'''(?P<attr>(?:src|poster|href|srcset|data-src(?:-[a-z0-9]+)*)\s*=\s*["'])(?:\.\./)*images/''',
    re.I,
)
css_pat = re.compile(r'''url\(\s*(['"]?)(?:\.\./)*images/''', re.I)

def rewrite(text: str) -> str:
    text = attr_pat.sub(lambda m: m.group("attr") + prefix, text)
    text = css_pat.sub(lambda m: f"url({m.group(1)}{prefix}", text)
    return text

n = 0
for path in root.rglob("*"):
    if not path.is_file():
        continue
    if path.suffix.lower() not in {".html", ".css", ".js", ".svg", ".json"}:
        continue
    # Nu rescrie fișierele din images/ (nu ar trebui să fie aici la non-fr)
    if "images" in path.parts:
        continue
    raw = path.read_text(encoding="utf-8", errors="replace")
    new = rewrite(raw)
    if new != raw:
        path.write_text(new, encoding="utf-8")
        n += 1
print(f"  rewritten media paths in {n} files → {prefix}")
PY
}

for code in "${COUNTRIES[@]}"; do
  dest="$WORKTREE/$code"
  src="$ROOT/build/$code"
  if [[ ! -d "$src" ]]; then
    echo "❌ Lipsă build/$code"
    exit 1
  fi

  if [[ "$code" == fr ]]; then
    echo "→ Sync fr/ (cu images/ — media comună)…"
    mkdir -p "$dest"
    rsync -a --delete "$src/" "$dest/"
  else
    echo "→ Sync $code/ (fără images/ — folosește fr/images)…"
    mkdir -p "$dest"
    rsync -a --delete --exclude images "$src/" "$dest/"
    rm -rf "$dest/images"
    rewrite_media_paths "$dest"
  fi

  if [[ -f "$dest/polistibrick-mercury-style.html" ]]; then
    cp "$dest/polistibrick-mercury-style.html" "$dest/index.html"
  fi
done

# FR HTML rămâne relativ (images/...) — OK, fișierele sunt în fr/images/
# site.js pe github.io: IMG trebuie → /REPO/fr/  ca nav logo să meargă din orice țară
python3 - "$WORKTREE" "$REPO_NAME" <<'PY'
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
repo = sys.argv[2]
# Patch every country's site.js IMG helper if present, else inject after BASE
IMG_BLOCK = f'''  // Preview github.io: media comună în /{repo}/fr/images/
  const IMG = (function () {{
    if (!location.hostname.includes('github.io')) return BASE;
    const parts = location.pathname.split('/').filter(Boolean);
    if (parts.length < 1) return BASE;
    return '/' + parts[0] + '/fr/';
  }})();
'''
for js in root.glob("*/assets/js/site.js"):
    text = js.read_text(encoding="utf-8")
    text2 = re.sub(
        r"\n  // Pe github\.io[\s\S]*?const IMG = \(function \(\) \{[\s\S]*?\}\)\(\);\n",
        "\n" + IMG_BLOCK,
        text,
        count=1,
    )
    if text2 == text:
        # inject after BASE block closing
        text2 = re.sub(
            r"(const BASE = \(function \(\) \{[\s\S]*?\}\)\(\);)",
            r"\1\n\n" + IMG_BLOCK.rstrip(),
            text,
            count=1,
        )
    text2 = text2.replace("${BASE}images/logo.png", "${IMG}images/logo.png")
    if text2 != text:
        js.write_text(text2, encoding="utf-8")
        print(f"  patched {js.relative_to(root)}")
PY

for f in index.html preview.html .nojekyll; do
  if [[ -f "$ROOT/scripts/gh-pages/$f" ]]; then
    cp "$ROOT/scripts/gh-pages/$f" "$WORKTREE/$f"
  fi
done
touch "$WORKTREE/.nojekyll"

echo "→ Dimensiune worktree:"
du -sh "$WORKTREE" "$WORKTREE/fr/images" 2>/dev/null || true
SIZE_MB=$(du -sm "$WORKTREE" | awk '{print $1}')
if [[ "$SIZE_MB" -gt 900 ]]; then
  echo "❌ Worktree ${SIZE_MB} MB > 900 MB"
  exit 1
fi

cd "$WORKTREE"
git add -A
if git diff --cached --quiet; then
  echo "✓ gh-pages deja la zi"
  exit 0
fi

git commit -m "$(cat <<EOF
Preview GitHub Pages — ${COUNTRIES[*]}

Media o dată în fr/images/; celelalte țări doar HTML.
EOF
)"

echo "→ Push gh-pages…"
git push origin gh-pages

echo ""
echo "✓ Preview:"
echo "  https://bouleanulucian.github.io/polistibrick-multisite/preview.html"
for code in "${COUNTRIES[@]}"; do
  echo "  https://bouleanulucian.github.io/polistibrick-multisite/$code/"
done
