#!/usr/bin/env bash
# Resize montaj card photos + montaj poster for faster below-fold loading.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CONSTRUCTION="$ROOT/shared/images/construction"
MONTAJ_DIRS=(countries/*/images/montaj)

optimize_jpg() {
  local src="$1"
  local max_w="${2:-800}"
  local q="${3:-82}"
  local tmp="${src}.tmp.jpg"
  sips -Z "$max_w" "$src" --out "$tmp" >/dev/null 2>&1
  mv "$tmp" "$src"
  cwebp -quiet -q "$q" "$src" -o "${src%.jpg}.webp"
}

echo "=== construction cards (shared) ==="
for f in stage1-cofraj stage2-fierbeton stage3-planseu stage4-final; do
  jpg="$CONSTRUCTION/${f}.jpg"
  [[ -f "$jpg" ]] || continue
  optimize_jpg "$jpg" 800 80
  ls -lh "$jpg" "${jpg%.jpg}.webp"
done

echo "=== montaj poster + bg video ==="
for dir in "${MONTAJ_DIRS[@]}"; do
  [[ -d "$dir" ]] || continue
  poster="$dir/montage-houses-poster.jpg"
  if [[ -f "$poster" ]]; then
    optimize_jpg "$poster" 1280 82
  fi
  mp4="$dir/montage-houses.mp4"
  if [[ -f "$mp4" ]]; then
    echo "  → $(basename "$dir") montage-houses.mp4"
    ffmpeg -y -hide_banner -loglevel error -i "$mp4" \
      -vf "scale=-2:720" -r 24 -c:v libx264 -preset medium -crf 32 \
      -maxrate 700k -bufsize 1400k -an -movflags +faststart \
      "$dir/montage-houses.opt.mp4"
    mv "$dir/montage-houses.opt.mp4" "$mp4"
    ls -lh "$mp4"
  fi
done

echo "Done."
