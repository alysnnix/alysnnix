#!/usr/bin/env bash
# Regenerates the README header: "Aly" from the portfolio signature exiting
# through its y into the ribbon, drawn in braille, then turned into dot SVGs
# (light and dark) so GitHub shows it without a code box.
#
#   nix-shell -p 'python3.withPackages(p: [p.pillow])' --run scripts/gen_ascii.sh
#
# Tune the art with ascii_ribbon.py flags: --rows, --sig-height, --twist, --open.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=assets/ascii
mkdir -p "$OUT"

python3 scripts/ascii_ribbon.py --style braille --signature --cols 80 --rows 11 --threads 7 --sig-height 0.8 >"$OUT/ribbon-signature-braille-80.txt"
python3 scripts/braille_svg.py "$OUT/ribbon-signature-braille-80.txt" --ink '#e6edf3' >"$OUT/ribbon-signature-dots-dark.svg"
python3 scripts/braille_svg.py "$OUT/ribbon-signature-braille-80.txt" --ink '#1f2328' >"$OUT/ribbon-signature-dots-light.svg"

ls -1 "$OUT"
