#!/usr/bin/env python3
"""Turn braille text art into an SVG of dots, so a README can show it without a code block.

GitHub draws every fenced block with a grey box and a copy button. This keeps the
same art as plain dots on a transparent background: one round dot per raised
braille dot, so it looks the same in any font and scales down on phones.

  python3 scripts/braille_svg.py art.txt --ink '#e6edf3' > art-dark.svg
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Braille cell bits to (column, row) of the 2x4 dot grid, Unicode order.
DOTS = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 3), (1, 3))
# Dot pitch: a monospace cell is about 0.6 wide by 1.45 tall in a code block,
# so 2 dots across and 4 down keep the art's proportions.
DX, DY = 5.0, 6.0


def dots(text: str) -> list[tuple[int, int]]:
    out = []
    for row, line in enumerate(text.splitlines()):
        for col, ch in enumerate(line):
            code = ord(ch) - 0x2800
            if 0 < code <= 0xFF:
                out += [(col * 2 + dx, row * 4 + dy) for bit, (dx, dy) in enumerate(DOTS) if code >> bit & 1]
    return out


def svg(points: list[tuple[int, int]], ink: str, pad: float = 4.0) -> str:
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    x0, y0 = min(xs), min(ys)
    w = (max(xs) - x0) * DX + pad * 2
    h = (max(ys) - y0) * DY + pad * 2
    # zero-length segments with round caps draw dots in about a dozen bytes each
    d = "".join(f"M{(x - x0) * DX + pad:g} {(y - y0) * DY + pad:g}h0" for x, y in points)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" role="img" aria-label="Aly">'
        f'<path d="{d}" stroke="{ink}" stroke-width="3.4" stroke-linecap="round" fill="none"/></svg>\n'
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("art", type=Path, help="braille text art")
    ap.add_argument("--ink", default="#e6edf3", help="dot color")
    args = ap.parse_args()
    points = dots(args.art.read_text(encoding="utf-8"))
    if not points:
        print("no braille dots found", file=sys.stderr)
        return 1
    sys.stdout.write(svg(points, args.ink))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
