#!/usr/bin/env python3
"""
make-logos.py - render Bedrock Linux's logos as clean vector art

Bedrock Linux's logo is ASCII art: the wordmark in the installer banner and on
bedrocklinux.org, the full "bedrock linux" form in paradigm's gist
(https://gist.github.com/paradigm/3319799), and a 32 px favicon that draws the
wordmark's "b". No vector or high resolution version is published, so this
script draws one from the characters themselves.

Each character occupies a cell one unit wide and two tall, a monospace aspect:
a backslash or slash is the cell's diagonal and an underscore is its baseline.
Strokes from neighbouring cells meet end to end, as the art reads in a
terminal. The square mark follows the favicon, which leaves out the wordmark's
underscore inside the "b".

Usage:
    make-logos.py [output-directory]    # default: the directory of this script
"""

import sys
from pathlib import Path

WORDMARK = [
    r"__          __             __",
    r"\ \_________\ \____________\ \___",
    r" \  _ \  _\ _  \  _\ __ \ __\   /",
    r"  \___/\__/\__/ \_\ \___/\__/\_\_\ ",
]

FULL = WORDMARK + [
    r"        \ \  _  ________ __",
    r"         \ \( )/  \ \ \ \ /",
    r"          \_\\_\_\_\__/_\_\ ",
]

MARK = [
    r"__",
    r"\ \___",
    r" \    \ ",
    r"  \___/",
]

CELL_W = 10
CELL_H = 20
INK_LIGHT = "#1c1c1c"
INK_DARK = "#ffffff"
TILE = "#2b2b30"
TILE_RIM = "#ffffff1f"


def segments(lines):
    """Yield the strokes of the art as ((x1, y1), (x2, y2)) in cell units."""
    for row, line in enumerate(lines):
        col = 0
        while col < len(line):
            char = line[col]
            top, bottom = row * 2, row * 2 + 2
            if char == "_":
                end = col
                while end < len(line) and line[end] == "_":
                    end += 1
                yield (col, bottom), (end, bottom)
                col = end
                continue
            if char == "\\":
                yield (col, top), (col + 1, bottom)
            elif char == "/":
                yield (col, bottom), (col + 1, top)
            col += 1


def dots(lines):
    """Yield the dot of the "i" as cubic curves (start, control, control, end).

    In the art the dot is "( )" under an underscore. Each bracket bows outward
    from an end of that underscore and a base closes them half a unit above
    the cell's floor, so the dot reads as one round shape apart from the stem.
    """
    for row, line in enumerate(lines):
        top, floor = row * 2, row * 2 + 1.5
        start = line.find("( )")
        while start != -1:
            left, right = start + 1, start + 2
            yield (left, top), (left - 0.6, top), (left - 0.6, floor), (left, floor)
            yield (right, top), (right + 0.6, top), (right + 0.6, floor), (right, floor)
            yield (left, floor), (left, floor), (right, floor), (right, floor)
            start = line.find("( )", start + 1)


def bounds(lines):
    xs, ys = [], []
    for (x1, y1), (x2, y2) in segments(lines):
        xs += [x1, x2]
        ys += [y1, y2]
    for curve in dots(lines):
        xs += [x for x, _ in curve]
        ys += [y for _, y in curve]
    return min(xs), min(ys), max(xs), max(ys)


def art_paths(lines, ink, stroke, dx=0.0, dy=0.0, scale=1.0):
    """Return SVG elements drawing the art, offset by (dx, dy) after scaling."""
    def point(x, y):
        return f"{dx + x * CELL_W * scale:.2f} {dy + y * (CELL_H / 2) * scale:.2f}"

    data = [f"M{point(*a)} L{point(*b)}" for a, b in segments(lines)]
    data += [f"M{point(*a)} C{point(*b)} {point(*c)} {point(*d)}"
             for a, b, c, d in dots(lines)]
    return (
        f'<path d="{" ".join(data)}" fill="none" stroke="{ink}" '
        f'stroke-width="{stroke * scale:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def svg(width, height, body, title):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.2f} {height:.2f}">\n'
        f"  <title>{title}</title>\n  {body}\n</svg>\n"
    )


def wordmark_svg(lines, ink, title, stroke=3.0, pad=4.0):
    x1, y1, x2, y2 = bounds(lines)
    width = (x2 - x1) * CELL_W + 2 * pad
    height = (y2 - y1) * (CELL_H / 2) + 2 * pad
    body = art_paths(lines, ink, stroke, pad - x1 * CELL_W, pad - y1 * CELL_H / 2)
    return svg(width, height, body, title)


def mark_svg(size=128, tiled=True, ink=INK_DARK):
    x1, y1, x2, y2 = bounds(MARK)
    art_w = (x2 - x1) * CELL_W
    art_h = (y2 - y1) * (CELL_H / 2)
    inner = size * (0.62 if tiled else 0.86)
    scale = inner / max(art_w, art_h)
    dx = (size - art_w * scale) / 2 - x1 * CELL_W * scale
    dy = (size - art_h * scale) / 2 - y1 * (CELL_H / 2) * scale
    stroke = 4.2 if tiled else 3.4
    parts = []
    if tiled:
        radius = size * 0.22
        parts.append(
            f'<rect x="1" y="1" width="{size - 2}" height="{size - 2}" rx="{radius:.1f}" '
            f'fill="{TILE}" stroke="{TILE_RIM}" stroke-width="2"/>'
        )
    parts.append(art_paths(MARK, ink, stroke, dx, dy, scale))
    return svg(size, size, "\n  ".join(parts), "Bedrock Linux")


def outputs():
    return {
        "bedrock-logo.svg": mark_svg(tiled=True),
        "bedrock-logo-mark.svg": mark_svg(tiled=False, ink=INK_LIGHT),
        "bedrock-logo-mark-dark.svg": mark_svg(tiled=False, ink=INK_DARK),
        "bedrock-logo-text.svg": wordmark_svg(WORDMARK, INK_LIGHT, "Bedrock Linux"),
        "bedrock-logo-text-dark.svg": wordmark_svg(WORDMARK, INK_DARK, "Bedrock Linux"),
        "bedrock-linux-logo.svg": wordmark_svg(FULL, INK_LIGHT, "Bedrock Linux"),
        "bedrock-linux-logo-dark.svg": wordmark_svg(FULL, INK_DARK, "Bedrock Linux"),
    }


def main():
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in outputs().items():
        (directory / name).write_text(content)
        print(directory / name)


if __name__ == "__main__":
    main()
