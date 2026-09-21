#!/bin/sh
# Amprenta build-ului fiecărei țări (fără fr): dovada că munca pe FR nu atinge restul.
# Rulare: sh scripts/amprente.sh   (după python3 build/build.py)
cd "$(dirname "$0")/.." || exit 1
for c in ro it es de nl en ie me; do
  [ -d "build/$c" ] && (cd "build/$c" && find . -type f -exec md5 -q {} + | sort | md5 -q | sed "s/^/$c /")
done
