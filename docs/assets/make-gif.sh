#!/usr/bin/env bash
#
# Turn a screen recording (terminal + Obsidian side by side) into the README hero GIF.
#
# Usage:
#   docs/assets/make-gif.sh <input.mov> [output.gif]
#
# Defaults output to docs/assets/import-url-demo.gif.
# Prefers `gifski` (best quality for GUI/text); falls back to ffmpeg palettegen.
# Tune the knobs below if the file is too big, too jerky, or too slow.

set -euo pipefail

IN="${1:?usage: make-gif.sh <input.mov> [output.gif]}"
OUT="${2:-docs/assets/import-url-demo.gif}"

SPEED=1       # playback speed multiplier: 1 = real time, 2 = 2x, 4 = 4x. Higher = smaller file.
FPS=12        # 12–15 is plenty for terminal + editor; lower = smaller file
WIDTH=1280    # cap width; downscale is the biggest size lever
QUALITY=80    # gifski quality (1–100)

# setpts must come first (rewrites source timestamps), then fps resamples, then scale.
VF="setpts=PTS/${SPEED},fps=${FPS},scale=${WIDTH}:-1:flags=lanczos"

command -v ffmpeg >/dev/null || { echo "ffmpeg not found (brew install ffmpeg)"; exit 1; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

if command -v gifski >/dev/null; then
  echo "→ gifski path (speed=${SPEED}x fps=$FPS width=$WIDTH q=$QUALITY)"
  ffmpeg -y -i "$IN" -vf "$VF" "$tmp/f%05d.png"
  gifski -o "$OUT" --fps "$FPS" --quality "$QUALITY" --width "$WIDTH" "$tmp"/f*.png
else
  echo "→ ffmpeg palettegen path (speed=${SPEED}x; brew install gifski for better quality)"
  ffmpeg -y -i "$IN" -vf "${VF},palettegen=stats_mode=diff" "$tmp/pal.png"
  ffmpeg -y -i "$IN" -i "$tmp/pal.png" \
    -lavfi "${VF} [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3" "$OUT"
fi

bytes=$(wc -c < "$OUT")
printf "✓ %s  (%.1f MB)\n" "$OUT" "$(echo "$bytes/1048576" | bc -l)"
[ "$bytes" -gt 8388608 ] && echo "⚠ >8MB — raise SPEED to 3–4, drop FPS to 12, or WIDTH to 1100." || true
