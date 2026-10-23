#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: [ ps.pillow ])"
"""Turn a picture into text art for the profile README, fully offline.

Three styles:
  ascii    a character density ramp, plain ASCII, so it aligns in any font
  braille  2x4 dots per cell, Floyd-Steinberg dithered, the most detail per column
  blocks   half blocks, two pixels per cell, dithered

Examples:
  scripts/image_to_ascii.py avatar.jpg --style ascii --width 36 --crop 0,30,440,470
  scripts/image_to_ascii.py avatar.jpg --style braille --width 60 --invert
  scripts/image_to_ascii.py avatar.jpg --style ascii --width 36 --beside info.txt

Output goes to stdout. `--beside FILE` prints FILE's lines to the right of the
art, neofetch style, so the art and the Nix attrset can share one code block.
GitHub renders code blocks light on dark or dark on light depending on the
reader's theme: by default dense characters mean dark pixels (ink on paper);
`--invert` flips that for art meant to glow on a dark page.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# light to dark: a space for the brightest pixels, the heaviest glyph for the darkest
RAMPS = {
    "short": " .:-=+*#%@",
    "fine": " .'`^,:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
}
# a terminal cell is about twice as tall as it is wide
CELL_ASPECT = 0.5
BRAILLE_BITS = ((0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (1, 0, 0x08), (1, 1, 0x10), (1, 2, 0x20), (0, 3, 0x40), (1, 3, 0x80))


def load(path: Path, crop: str | None, equalize: bool, contrast: float, gamma: float, invert: bool, sharpen: bool) -> Image.Image:
    img = Image.open(path).convert("L")
    if crop:
        img = img.crop(tuple(int(v) for v in crop.split(",")))
    img = ImageOps.equalize(img) if equalize else ImageOps.autocontrast(img, cutoff=1)
    if contrast != 1:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if gamma != 1:
        img = img.point(lambda v: round(255 * (v / 255) ** gamma))
    if sharpen:
        img = img.filter(ImageFilter.SHARPEN)
    return ImageOps.invert(img) if invert else img


def to_ascii(img: Image.Image, width: int, ramp: str) -> list[str]:
    height = max(1, round(img.height / img.width * width * CELL_ASPECT))
    small = img.resize((width, height), Image.LANCZOS)
    px = small.load()
    last = len(ramp) - 1
    return ["".join(ramp[round((255 - px[x, y]) / 255 * last)] for x in range(width)).rstrip() for y in range(height)]


def bilevel(img: Image.Image, size: tuple[int, int], threshold: int, dither: bool) -> Image.Image:
    """Black and white at `size`: dithered, or a hard cut at `threshold`."""
    small = img.resize(size, Image.LANCZOS)
    if dither:
        return small.point(lambda v: 255 if v > threshold else v).convert("1")
    return small.point(lambda v: 255 if v > threshold else 0).convert("1", dither=Image.Dither.NONE)


def to_braille(img: Image.Image, width: int, threshold: int, dither: bool) -> list[str]:
    w = width * 2
    h = round(img.height / img.width * w * CELL_ASPECT * 2 / 4) * 4  # 4 dot rows per cell, 2 dots wide
    dots = bilevel(img, (w, h), threshold, dither)
    px = dots.load()
    lines = []
    for cy in range(0, h, 4):
        row = []
        for cx in range(0, w, 2):
            code = 0
            for dx, dy, bit in BRAILLE_BITS:
                if px[cx + dx, cy + dy] == 0:  # a dark dot is a raised dot
                    code |= bit
            row.append(chr(0x2800 + code))
        lines.append("".join(row).rstrip("\u2800"))
    return lines


def to_blocks(img: Image.Image, width: int, threshold: int, dither: bool) -> list[str]:
    h = round(img.height / img.width * width * CELL_ASPECT) * 2
    dots = bilevel(img, (width, h), threshold, dither)
    px = dots.load()
    glyph = {(False, False): " ", (True, False): "\u2580", (False, True): "\u2584", (True, True): "\u2588"}
    return ["".join(glyph[(px[x, y] == 0, px[x, y + 1] == 0)] for x in range(width)).rstrip() for y in range(0, h, 2)]


def beside(art: list[str], info: list[str], gap: int) -> list[str]:
    col = max((len(line) for line in art), default=0) + gap
    top = max(0, (len(art) - len(info)) // 2)
    rows = max(len(art), top + len(info))
    out = []
    for i in range(rows):
        left = art[i] if i < len(art) else ""
        right = info[i - top] if 0 <= i - top < len(info) else ""
        out.append((left.ljust(col) + right).rstrip() if right else left)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", type=Path)
    ap.add_argument("--style", choices=("ascii", "braille", "blocks"), default="ascii")
    ap.add_argument("--width", type=int, default=40, help="columns of art")
    ap.add_argument("--crop", help="left,top,right,bottom in source pixels")
    ap.add_argument("--ramp", choices=tuple(RAMPS), default="short", help="ascii: glyph ramp, short reads cleaner at small sizes")
    ap.add_argument("--equalize", action="store_true", help="spread the tones evenly, for flat or tinted photos")
    ap.add_argument("--contrast", type=float, default=1.0)
    ap.add_argument("--gamma", type=float, default=1.0, help="above 1 darkens midtones, below 1 lightens them")
    ap.add_argument("--threshold", type=int, default=235, help="braille, blocks: pixels brighter than this stay empty")
    ap.add_argument("--no-dither", dest="dither", action="store_false", help="braille, blocks: hard cut at --threshold instead of dithering")
    ap.add_argument("--invert", action="store_true", help="dense glyphs for bright pixels")
    ap.add_argument("--sharpen", action="store_true")
    ap.add_argument("--beside", type=Path, help="text file printed to the right of the art")
    ap.add_argument("--gap", type=int, default=3)
    a = ap.parse_args()

    img = load(a.image, a.crop, a.equalize, a.contrast, a.gamma, a.invert, a.sharpen)
    if a.style == "ascii":
        art = to_ascii(img, a.width, RAMPS[a.ramp])
    elif a.style == "braille":
        art = to_braille(img, a.width, a.threshold, a.dither)
    else:
        art = to_blocks(img, a.width, a.threshold, a.dither)
    if a.beside:
        art = beside(art, a.beside.read_text().rstrip("\n").splitlines(), a.gap)
    sys.stdout.write("\n".join(art) + "\n")


if __name__ == "__main__":
    main()
