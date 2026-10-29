#!/bin/sh
# Renders design/*.svg into the PNGs Home Assistant serves from custom_components/weeklymenu/brand/.
# Needs Google Chrome (headless, for a transparent background) and macOS `sips` (for resizing).
# Format rules: https://contributors.home-assistant.io/core/integrations/brands/
set -e
cd "$(dirname "$0")"
OUT=../custom_components/weeklymenu/brand
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TMP=$(mktemp -d)

shot() { # svg width height out
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --default-background-color=00000000 \
    --window-size="$2,$3" --screenshot="$4" "file://$PWD/$1" >/dev/null 2>&1
}

for variant in "" "-dark"; do
  prefix=$([ -z "$variant" ] && echo "" || echo "dark_")
  shot "icon$variant.svg" 1024 1024 "$TMP/icon$variant.png"
  shot "logo$variant.svg" 1600 400 "$TMP/logo$variant.png"
  sips -z 256 256 "$TMP/icon$variant.png" --out "$OUT/${prefix}icon.png" >/dev/null
  sips -z 512 512 "$TMP/icon$variant.png" --out "$OUT/${prefix}icon@2x.png" >/dev/null
  sips -z 200 800 "$TMP/logo$variant.png" --out "$OUT/${prefix}logo.png" >/dev/null
  sips -z 400 1600 "$TMP/logo$variant.png" --out "$OUT/${prefix}logo@2x.png" >/dev/null
done
rm -r "$TMP"
ls -l "$OUT"
