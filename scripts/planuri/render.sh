#!/bin/bash
# SVG -> PNG 2000x1678 prin Chrome headless
S="$1"; O="${2:-${1%.svg}.png}"
cat > /tmp/wrap.html <<HTML
<!doctype html><meta charset="utf-8">
<style>html,body{margin:0;padding:0;background:#fff}</style>
$(cat "$S")
HTML
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=2000,1678 --screenshot="$O" --default-background-color=FFFFFFFF \
  /tmp/wrap.html 2>/dev/null
echo "$O"
