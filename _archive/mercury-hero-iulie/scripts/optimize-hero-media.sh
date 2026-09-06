#!/usr/bin/env bash
# ZURU-style hero: sharp poster + responsive MP4 at ~2 Mbps (not tiny low-res).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

pick_source() {
  local dir="$1"
  if [[ -f "$dir/hero-houses-reel.mp4" ]]; then
    echo "$dir/hero-houses-reel.mp4"
    return
  fi
  if [[ -f "$dir/hero-houses-reel.opt.mp4" ]]; then
    echo "$dir/hero-houses-reel.opt.mp4"
    return
  fi
  echo "$dir/hero-houses-reel-desktop.mp4"
}

encode_zuru() {
  local src="$1"
  local dir="$2"
  echo "  → ZURU-style encode from $(basename "$src")"

  # Desktop: native up to 1080p, ~2 Mbps like zuru (process_v4_*_2kbitrate)
  ffmpeg -y -hide_banner -loglevel error -i "$src" \
    -vf "scale='min(1920,iw)':-2:flags=lanczos" -r 24 -c:v libx264 -preset slow -crf 20 \
    -maxrate 2000k -bufsize 4000k -profile:v high -pix_fmt yuv420p -an -movflags +faststart \
    "$dir/hero-houses-reel-desktop.mp4"

  # Mobile: 720p-class, still high bitrate
  ffmpeg -y -hide_banner -loglevel error -i "$src" \
    -vf "scale='min(1280,iw)':-2:flags=lanczos" -r 24 -c:v libx264 -preset slow -crf 22 \
    -maxrate 1500k -bufsize 3000k -profile:v high -pix_fmt yuv420p -an -movflags +faststart \
    "$dir/hero-houses-reel-mobile.mp4"

  # WebM VP9 for modern browsers (better quality/size than H.264)
  if ffmpeg -hide_banner -encoders 2>/dev/null | rg -q libvpx-vp9; then
    ffmpeg -y -hide_banner -loglevel error -i "$src" \
      -vf "scale='min(1920,iw)':-2:flags=lanczos" -r 24 -c:v libvpx-vp9 -crf 28 -b:v 0 \
      -row-mt 1 -an "$dir/hero-houses-reel-desktop.webm" 2>/dev/null || true
    ffmpeg -y -hide_banner -loglevel error -i "$src" \
      -vf "scale='min(1280,iw)':-2:flags=lanczos" -r 24 -c:v libvpx-vp9 -crf 30 -b:v 0 \
      -row-mt 1 -an "$dir/hero-houses-reel-mobile.webm" 2>/dev/null || true
  fi
}

poster_from_video() {
  local src="$1"
  local dir="$2"
  # Sharp still frame for instant LCP (ZURU uses 2560px WebP under the video)
  ffmpeg -y -hide_banner -loglevel error -ss 1 -i "$src" -vframes 1 \
    -vf "scale='min(1920,iw)':-2:flags=lanczos" -q:v 2 \
    "$dir/hero-house-1.jpg"
  cwebp -quiet -q 88 "$dir/hero-house-1.jpg" -o "$dir/hero-house-1.webp"
}

poster_webp() {
  local dir="$1"
  for j in hero-house-2.jpg hero-house-3.jpg; do
    if [[ -f "$dir/$j" ]]; then
      cwebp -quiet -q 85 "$dir/$j" -o "${dir}/${j%.jpg}.webp"
    fi
  done
}

for code in ro fr en es it de nl ie; do
  dir="countries/$code/images/hero"
  [[ -d "$dir" ]] || continue
  echo "=== $code ==="
  src="$(pick_source "$dir")"
  [[ -f "$src" ]] || { echo "  skip (no source)"; continue; }
  encode_zuru "$src" "$dir"
  poster_from_video "$src" "$dir"
  poster_webp "$dir"
  ls -lh "$dir"/hero-house-1.webp "$dir"/hero-houses-reel-desktop.mp4 "$dir"/hero-houses-reel-mobile.mp4 2>/dev/null || true
done

echo "Done."
