#!/usr/bin/env bash
# Regenerates the text art in assets/ascii/: the ribbon (the README headers),
# plus a portrait from a picture and the signature.
#
#   scripts/gen_ascii.sh [photo.jpg]
#
# The photo defaults to assets/avatar.jpg. Crop and tone flags are tuned for
# the current avatar (face in the left two thirds, flat light background); for
# another picture, adjust CROP (left,top,right,bottom in source pixels) first.
# The SVGs are linked from the READMEs directly; the .txt files are pasted into
# their code blocks by hand, so rerun this, look at them, then update the block.
set -euo pipefail
cd "$(dirname "$0")/.."

PHOTO=${1:-assets/avatar.jpg}
CROP=${CROP:-0,40,420,500}
TONE="--contrast 1.6 --gamma 1.3"
ART=scripts/image_to_ascii.py
OUT=assets/ascii
mkdir -p "$OUT"

# the ribbon: color SVG headers (text art with the gradient) and monochrome code block versions
RIBBON=scripts/ascii_ribbon.py
for theme in dark light; do
  "$RIBBON" --style threads --threads 7 --signature --svg "$OUT/ribbon-signature-$theme.svg" --theme "$theme" >/dev/null
done
"$RIBBON" --style threads --threads 7 --signature >"$OUT/ribbon-signature-threads.txt"
"$RIBBON" --style threads --threads 7 --cols 80 --rows 12 >"$OUT/ribbon-threads-80.txt"
"$RIBBON" --style braille --threads 9 --cols 80 --rows 12 >"$OUT/ribbon-braille-80.txt"
"$RIBBON" --style shade --threads 12 --cols 80 --rows 12 >"$OUT/ribbon-shade-80.txt"

# the portrait in two styles and two sizes: dense characters and braille dots
"$ART" "$PHOTO" --style ascii --width 34 --crop "$CROP" $TONE >"$OUT/avatar-ascii-34.txt"
"$ART" "$PHOTO" --style ascii --width 60 --crop "$CROP" $TONE >"$OUT/avatar-ascii-60.txt"
"$ART" "$PHOTO" --style braille --width 34 --crop "$CROP" $TONE --threshold 200 >"$OUT/avatar-braille-34.txt"
"$ART" "$PHOTO" --style braille --width 60 --crop "$CROP" $TONE --threshold 200 >"$OUT/avatar-braille-60.txt"

# the "Aly" signature: crisp shapes, so a hard cut instead of dithering
"$ART" assets/aly-signature-mono.png --style braille --width 24 --no-dither --threshold 128 >"$OUT/signature-braille-24.txt"
"$ART" assets/aly-signature-mono.png --style ascii --width 32 >"$OUT/signature-ascii-32.txt"

# neofetch style cards: the art with an attrset beside it, what the README code blocks hold
"$ART" "$PHOTO" --style ascii --width 32 --crop "$CROP" $TONE --beside "$OUT/profile.nix" --gap 2 >"$OUT/card-avatar.txt"
"$ART" assets/aly-signature-mono.png --style ascii --width 32 --beside "$OUT/signature.nix" --gap 3 >"$OUT/card-signature.txt"

ls -1 "$OUT"
