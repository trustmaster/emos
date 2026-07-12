#!/usr/bin/env bash
#
# Turn a screen recording (terminal + Obsidian side by side) into the README hero GIF.
#
# Usage:
#   docs/assets/make-gif.sh <input.mov> [output.gif]
#
# Defaults output to docs/assets/import-url-demo.gif.
# Prefers `gifski` (best quality for GUI/text); falls back to ffmpeg palettegen.
# Tune the three knobs below if the file is too big or too jerky.

set -euo pipefail

IN="${1:?usage: make-gif.sh <input.mov> [output.gif]}"
OUT="${2:-docs/assets/import-url-demo.gif}"

FPS=15        # 12–15 is plenty for terminal + editor; lower = smaller file
WIDTH=1280    # cap width; downscale is the biggest size lever
QUALITY=90    # gifski quality (1–100)

command -v ffmpeg >/dev/null || { echo "ffmpeg not found (brew install ffmpeg)"; exit 1; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

if command -v gifski >/dev/null; then
  echo "→ gifski path (fps=$FPS width=$WIDTH q=$QUALITY)"
  ffmpeg -y -i "$IN" -vf "fps=$FPS,scale=$WIDTH:-1:flags=lanczos" "$tmp/f%05d.png"
  gifski -o "$OUT" --fps "$FPS" --quality "$QUALITY" "$tmp"/f*.png
else
  echo "→ ffmpeg palettegen path (gifski not installed → brew install gifski for better quality)"
  ffmpeg -y -i "$IN" -vf "fps=$FPS,scale=$WIDTH:-1:flags=lanczos,palettegen=stats_mode=diff" "$tmp/pal.png"
  ffmpeg -y -i "$IN" -i "$tmp/pal.png" \
    -lavfi "fps=$FPS,scale=$WIDTH:-1:flags=lanczos,paletteuse=dither=bayer:bayer_scale=3" "$OUT"
fi

bytes=$(wc -c < "$OUT")
printf "✓ %s  (%.1f MB)\n" "$OUT" "$(echo "$bytes/1048576" | bc -l)"
[ "$bytes" -gt 8388608 ] && echo "⚠ >8MB — drop FPS to 12, WIDTH to 1100, or trim dead air." || true
