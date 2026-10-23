#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: [ ps.pillow ])"
"""Draw the aly.engineer ribbon as text art, fully offline.

The ribbon is a band of threads that leaves the "Aly" signature thin, opens
and twists along a slow S, like the portfolio hero and the profile banners
(portfolio scripts/card-kit.ts: width ramps open from the tail, the band turns
by `twist` radians per unit, threads facing the viewer are brighter).

Styles:
  threads  one line character per thread per cell: ' - . _ / \\ | and = x where they meet
  shade    the band as density, through a ten step ramp
  braille  every thread drawn as dots, 2x4 per cell

  scripts/ascii_ribbon.py --style threads --signature
  scripts/ascii_ribbon.py --style shade --cols 92 --rows 14
  scripts/ascii_ribbon.py --style threads --signature --svg assets/ribbon-dark.svg --theme dark

`--svg` also writes the art as an SVG of monospace text with the lavender to
pink gradient, every glyph placed by x so it lines up in any font. It has no
scripts, no external fonts and no links, so GitHub serves it as an <img>.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from image_to_ascii import BRAILLE_BITS, RAMPS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
# the signature's outlines in glyph units: portfolio src/lib/glyphs.ts ALY_GLYPHS, as scripts/card-kit.ts draws them
GLYPHS = ROOT / "assets/aly-signature-dark.svg"
# its ink box in glyph units, and where the ribbon leaves it: portfolio src/lib/ribbon.ts TAIL,
# the end of the y's flourish, the direction it is heading and the stroke's width there
INK = (11, -190, 340, 91)
TAIL = {"x": 325.5, "y": -28.8, "dx": 0.833, "dy": -0.554, "w": 19.6}
# a cell is twice as tall as it is wide: 10 by 20 units keeps the geometry isotropic
UX, UY = 10, 20
# the portfolio tokens (src/styles/global.css): ink, then the ribbon's rb-1, rb-2, rb-3
THEMES = {
    "dark": ("#eeecfb", "#8e80ff", "#c5b4ff", "#ff9ccc"),
    "light": ("#15123a", "#4b3cf0", "#8457ee", "#e0679b"),
}
# SVG cell size in px: a 14 px monospace advances about 8.4 px; rows sit tight like a terminal
SVG_CW, SVG_CH, SVG_FONT = 8.4, 16.8, 14


# ---------------------------------------------------------------- geometry


def catmull(points: list[tuple[float, float]], steps: int) -> list[tuple[float, float]]:
    pts = [points[0], *points, points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1 : i + 3]
        for k in range(steps):
            t = k / steps
            out.append(
                tuple(
                    0.5 * (2 * p1[j] + (p2[j] - p0[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t + (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * t**3)
                    for j in (0, 1)
                )
            )
    out.append(points[-1])
    return out


def glyph_outlines() -> list[list[list[tuple[float, float]]]]:
    """Each glyph as closed polygons in glyph units, from the SVG's absolute M, L, Q, Z paths."""
    import re

    glyphs = []
    for d in re.findall(r' d="([^"]+)"', GLYPHS.read_text()):
        polys: list[list[tuple[float, float]]] = []
        tokens = re.findall(r"[MLQZ]|-?\d*\.?\d+", d)
        i, cmd, pen = 0, "", (0.0, 0.0)
        while i < len(tokens):
            if tokens[i] in "MLQZ":
                cmd = tokens[i]
                i += 1
                if cmd == "Z":
                    continue
            nums = lambda n: [float(v) for v in tokens[i : i + n]]  # noqa: E731
            if cmd == "M":
                pen = tuple(nums(2))
                polys.append([pen])
                i += 2
                cmd = "L"
            elif cmd == "L":
                pen = tuple(nums(2))
                polys[-1].append(pen)
                i += 2
            elif cmd == "Q":
                cx, cy, x, y = nums(4)
                (px, py) = pen
                for k in range(1, 9):
                    t = k / 8
                    polys[-1].append(((1 - t) ** 2 * px + 2 * (1 - t) * t * cx + t * t * x, (1 - t) ** 2 * py + 2 * (1 - t) * t * cy + t * t * y))
                pen = (x, y)
                i += 4
        glyphs.append(polys)
    return glyphs


def place_signature(h: float, left: float, height: float):
    """The signature `height` units tall at `left`, vertically centred: its polygons and the ribbon's tail, in scene units."""
    k = height / (INK[3] - INK[1])
    x0 = left - INK[0] * k
    y0 = (h - height) / 2 - INK[1] * k
    to = lambda x, y: (x0 + x * k, y0 + y * k)  # noqa: E731
    glyphs = [[[to(x, y) for x, y in poly] for poly in g] for g in glyph_outlines()]
    tail = (*to(TAIL["x"], TAIL["y"]), TAIL["dx"], TAIL["dy"], TAIL["w"] * k)
    return glyphs, tail


def lay_threads(center: list[tuple[float, float]], n: int, open_: float, ramp: float, twist: float, born_open: bool, neck: float = 2) -> list[list[tuple[float, float, float]]]:
    """Each thread as (x, y, depth) samples; depth > 0 faces the viewer. The band starts `neck` wide, the stroke it leaves."""
    threads: list[list[tuple[float, float, float]]] = [[] for _ in range(n)]
    offsets = [-1 + 2 * i / (n - 1) for i in range(n)]
    s = 0.0
    for i, (x, y) in enumerate(center):
        if i:
            s += math.dist(center[i - 1], (x, y))
        ax, ay = center[max(i - 1, 0)]
        bx, by = center[min(i + 1, len(center) - 1)]
        length = math.hypot(bx - ax, by - ay) or 1
        nx, ny = -(by - ay) / length, (bx - ax) / length
        r = 1.0 if born_open else min(1.0, s / ramp)
        r = r * r * (3 - 2 * r)
        width = neck + (open_ - neck) * r * (0.84 + 0.16 * math.sin(s / 170))
        theta = r * (s * twist + 0.35) + (1.1 if born_open else 0)
        for t, thread in zip(offsets, threads):
            off = width / 2 * t * math.cos(theta)
            thread.append((x + nx * off, y + ny * off, t * math.sin(theta)))
    return threads


def scene(cols: int, rows: int, n: int, with_signature: bool, sig_height: float = 0.9, twist: float = 1.2, open_share: float = 0.42):
    w, h = cols * UX, rows * UY
    sig = None
    if with_signature:
        sig, (tx, ty, dx, dy, tw) = place_signature(h, UX * 1, h * sig_height)
        # out of the y's flourish along its own heading, one shallow crest, one wide dip, off the right edge.
        # The band stays narrow through the crest and opens on the long run after it: a turn tighter than
        # half the band's width folds the inner threads over and tangles them into loops.
        path = [(tx, ty), (tx + dx * 40, ty + dy * 40), (0.56 * w, h * 0.22), (0.8 * w, h * 0.58), (1.12 * w, h * 0.3)]
        center = catmull(path, 200)
        threads = lay_threads(center, n, h * open_share, ramp=w * 0.42, twist=twist / w, born_open=False, neck=tw)
        return w, h, threads, sig
    path = [(-0.06 * w, h * 0.30), (0.22 * w, h * 0.68), (0.5 * w, h * 0.30), (0.76 * w, h * 0.70), (1.06 * w, h * 0.36)]
    center = catmull(path, 160)
    threads = lay_threads(center, n, h * 0.56, ramp=w * 0.22, twist=4.6 / w, born_open=True)
    return w, h, threads, sig


# ---------------------------------------------------------------- rasters


def draw(w: float, h: float, threads, sig, scale: float, line: int) -> tuple[Image.Image, Image.Image, Image.Image]:
    """Front threads, back threads and signature ink as L images at `scale` px per unit."""
    size = (round(w * scale), round(h * scale))
    front, back, ink = (Image.new("L", size, 0) for _ in range(3))
    df, db = ImageDraw.Draw(front), ImageDraw.Draw(back)
    for thread in threads:
        for (x0, y0, z0), (x1, y1, _) in zip(thread, thread[1:]):
            (df if z0 >= 0 else db).line((x0 * scale, y0 * scale, x1 * scale, y1 * scale), fill=255, width=line)
    if sig:
        # fill at 4x and box filter down, so edge pixels carry coverage instead of jaggies;
        # even-odd per glyph (a counter is a subpath inside its outline), union across glyphs
        big = Image.new("L", (size[0] * 4, size[1] * 4), 0)
        for glyph in sig:
            g = Image.new("L", big.size, 0)
            for poly in glyph:
                p = Image.new("L", big.size, 0)
                ImageDraw.Draw(p).polygon([(x * scale * 4, y * scale * 4) for x, y in poly], fill=255)
                g = ImageChops.difference(g, p)
            big = ImageChops.lighter(big, g)
        ink.paste(big.resize(size, Image.BOX))
    return front, back, ink


def cells(img: Image.Image, cols: int, rows: int) -> list[list[float]]:
    small = img.resize((cols, rows), Image.BOX).load()
    return [[small[c, r] / 255 for c in range(cols)] for r in range(rows)]


# ---------------------------------------------------------------- styles
# each returns rows of (char, tier): tier 0 empty, 1 back thread, 2 front thread, 3 signature ink


def style_shade(cols, rows, w, h, threads, sig):
    front, back, ink = (cells(i, cols, rows) for i in draw(w, h, threads, sig, 3, 2))
    ramp = RAMPS["short"]
    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if ink[r][c] > 0.12:
                row.append((ramp[min(9, round(ink[r][c] * 14))], 3))
                continue
            # one 2 px line across a 30 by 60 px cell covers about 1/30 of it: one thread reads as step 3, three as the darkest
            v = front[r][c] + 0.5 * back[r][c]
            k = min(9, round(v * 90))
            row.append((ramp[k], 0 if k == 0 else 2 if front[r][c] >= back[r][c] else 1))
        out.append(row)
    return out


def style_braille(cols, rows, w, h, threads, sig):
    scale = 2 / UX  # 2 dots per cell across, 4 down
    front, back, ink = draw(w, h, threads, sig, scale, 1)
    px = [i.load() for i in (front, back, ink)]
    out = []
    for cy in range(rows):
        row = []
        for cx in range(cols):
            code, tiers = 0, [0, 0, 0]
            for dx, dy, bit in BRAILLE_BITS:
                x, y = cx * 2 + dx, cy * 4 + dy
                # a thread dot lights at any touch; signature ink needs half the dot covered, so its edges stay clean
                hit = [px[0][x, y] > 100, px[1][x, y] > 100, px[2][x, y] > 120]
                if any(hit):
                    code |= bit
                    tiers[2 if hit[2] else 0 if hit[0] else 1] += 1
            tier = 0 if not code else 3 if tiers[2] else 2 if tiers[0] >= tiers[1] else 1
            row.append((chr(0x2800 + code), tier))
        out.append(row)
    return out


def line_char(sub: float, slope: float) -> str:
    if abs(slope) >= 2.4:
        return "|"
    if slope <= -0.6:
        return "/"
    if slope >= 0.6:
        return "\\"
    return "'" if sub < 0.3 else "-" if sub < 0.56 else "." if sub < 0.8 else "_"


def style_threads(cols, rows, w, h, threads, sig):
    ink = cells(draw(w, h, threads, sig, 2, 1)[2], cols, rows) if sig else None
    hits: dict[tuple[int, int], dict[int, list[tuple[float, float, float]]]] = {}
    for ti, thread in enumerate(threads):
        for (x0, y0, z), (x1, y1, _) in zip(thread, thread[1:]):
            c, r = int(x0 // UX), int(y0 // UY)
            if 0 <= c < cols and 0 <= r < rows and x1 != x0:
                slope = ((y1 - y0) / UY) / ((x1 - x0) / UX)
                hits.setdefault((r, c), {}).setdefault(ti, []).append(((y0 % UY) / UY, slope, z))
    ramp = RAMPS["short"]
    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if ink and ink[r][c] > 0.08:
                row.append((ramp[min(9, max(1, round(ink[r][c] * 16)))], 3))
                continue
            here = hits.get((r, c))
            if not here:
                row.append((" ", 0))
                continue
            marks = []
            for samples in here.values():
                sub = sum(s[0] for s in samples) / len(samples)
                slope = sum(s[1] for s in samples) / len(samples)
                depth = sum(s[2] for s in samples) / len(samples)
                marks.append((line_char(sub, slope), depth))
            # the thread nearest the viewer draws the cell; a / meeting a \ is a crossing, many threads a fold
            chars = {m[0] for m in marks}
            front_ch, depth = max(marks, key=lambda m: m[1])
            tier = 2 if depth >= 0 else 1
            if {"/", "\\"} <= chars:
                ch = "x"
            elif len(marks) >= 4:
                ch = "="
            else:
                ch = front_ch
            row.append((ch, tier))
        out.append(row)
    return out


STYLES = {"threads": style_threads, "shade": style_shade, "braille": style_braille}


# ---------------------------------------------------------------- output


def to_text(grid, blank: str) -> str:
    return "\n".join("".join(ch for ch, _ in row).rstrip(blank) for row in grid) + "\n"


def to_svg(grid, theme: str, title: str) -> str:
    ink, c1, c2, c3 = THEMES[theme]
    cols, rows = len(grid[0]), len(grid)
    width, height = cols * SVG_CW, rows * SVG_CH + 6
    esc = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    layers = {1: [], 2: [], 3: []}
    for r, row in enumerate(grid):
        for tier in layers:
            xs = [f"{c * SVG_CW:.1f}" for c, (ch, t) in enumerate(row) if t == tier and ch.strip()]
            text = "".join(esc.get(ch, ch) for ch, t in row if t == tier and ch.strip())
            if text:
                layers[tier].append(f'<text x="{" ".join(xs)}" y="{(r + 1) * SVG_CH - 4:.1f}">{text}</text>')
    opacity = {1: 0.42 if theme == "dark" else 0.5, 2: 1, 3: 1}
    groups = "".join(
        f'<g fill="url(#rb)" fill-opacity="{opacity[t]}">{"".join(rows_)}</g>' for t, rows_ in layers.items() if rows_
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.1f} {height:.1f}" role="img">'
        f"<title>{title}</title>"
        f'<defs><linearGradient id="rb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{width:.1f}" y2="0">'
        f'<stop offset="0" stop-color="{ink}"/><stop offset="0.24" stop-color="{c1}"/><stop offset="0.6" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/>'
        f"</linearGradient></defs>"
        f'<g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, \'Liberation Mono\', monospace" font-size="{SVG_FONT}" xml:space="preserve">{groups}</g></svg>\n'
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--style", choices=tuple(STYLES), default="threads")
    ap.add_argument("--cols", type=int, default=92)
    ap.add_argument("--rows", type=int, default=14)
    ap.add_argument("--threads", type=int, default=9, help="threads in the band")
    ap.add_argument("--signature", action="store_true", help='start from the "Aly" signature, like the site')
    ap.add_argument("--sig-height", type=float, default=0.9, help="signature ink height as a share of the rows")
    ap.add_argument("--twist", type=float, default=1.2, help="with --signature: band turns across the width, radians; high values turn it edge on")
    ap.add_argument("--open", type=float, default=0.42, help="with --signature: widest the band opens, as a share of the rows")
    ap.add_argument("--svg", type=Path, help="also write a gradient SVG of the same art here")
    ap.add_argument("--theme", choices=tuple(THEMES), default="dark", help="SVG colors")
    a = ap.parse_args()

    w, h, threads, sig = scene(a.cols, a.rows, a.threads, a.signature, a.sig_height, a.twist, a.open)
    grid = STYLES[a.style](a.cols, a.rows, w, h, threads, sig)
    sys.stdout.write(to_text(grid, "\u2800 " if a.style == "braille" else " "))
    if a.svg:
        title = "Aly, handwritten, unwinding into a ribbon of threads" if a.signature else "A ribbon of threads, lavender to pink"
        a.svg.write_text(to_svg(grid, a.theme, title))


if __name__ == "__main__":
    main()
