#!/usr/bin/env bash
# Encode web hero variants once from 4K master, copy to all countries.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MASTER="${1:-$ROOT/masters/hero/hero-production-master-4k.mp4}"
OUT="$ROOT/.tmp/hero-web"

if [[ ! -f "$MASTER" ]]; then
  echo "Missing master: $MASTER" >&2
  exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT"

echo "→ Master: $(basename "$MASTER") ($(du -h "$MASTER" | cut -f1))"

ffmpeg -y -hide_banner -loglevel error -ss 0.04 -i "$MASTER" -vframes 1 \
  -vf "scale='min(2560,iw)':-2:flags=lanczos" -q:v 2 \
  "$OUT/hero-house-1.jpg"
cwebp -quiet -q 88 "$OUT/hero-house-1.jpg" -o "$OUT/hero-house-1.webp"

ffmpeg -y -hide_banner -loglevel error -i "$MASTER" \
  -vf "scale=-2:1440:flags=lanczos" -r 24 -c:v libx264 -preset slow -crf 20 \
  -maxrate 2000k -bufsize 4000k -profile:v high -pix_fmt yuv420p -an -movflags +faststart \
  "$OUT/hero-houses-reel-desktop.mp4"

ffmpeg -y -hide_banner -loglevel error -i "$MASTER" \
  -vf "scale=-2:1080:flags=lanczos" -r 24 -c:v libx264 -preset slow -crf 22 \
  -maxrate 1500k -bufsize 3000k -profile:v high -pix_fmt yuv420p -an -movflags +faststart \
  "$OUT/hero-houses-reel-mobile.mp4"

if ffmpeg -hide_banner -encoders 2>/dev/null | rg -q libvpx-vp9; then
  ffmpeg -y -hide_banner -loglevel error -i "$MASTER" \
    -vf "scale=-2:1440:flags=lanczos" -r 24 -c:v libvpx-vp9 -crf 28 -b:v 0 -row-mt 1 -an \
    "$OUT/hero-houses-reel-desktop.webm"
  ffmpeg -y -hide_banner -loglevel error -i "$MASTER" \
    -vf "scale=-2:1080:flags=lanczos" -r 24 -c:v libvpx-vp9 -crf 30 -b:v 0 -row-mt 1 -an \
    "$OUT/hero-houses-reel-mobile.webm"
fi

cp "$OUT/hero-houses-reel-desktop.mp4" "$OUT/hero-houses-reel.mp4"

ls -lh "$OUT"/hero-house-1.webp "$OUT"/hero-houses-reel-desktop.mp4 "$OUT"/hero-houses-reel-mobile.mp4

for code in ro fr en es it de nl ie; do
  dest="$ROOT/countries/$code/images/hero"
  mkdir -p "$dest"
  cp "$OUT"/hero-house-1.jpg "$OUT"/hero-house-1.webp \
     "$OUT"/hero-houses-reel*.mp4 "$dest/"
  [[ -f "$OUT/hero-houses-reel-desktop.webm" ]] && cp "$OUT"/hero-houses-reel*.webm "$dest/"
  echo "  ✓ $code"
done

echo "Done."
