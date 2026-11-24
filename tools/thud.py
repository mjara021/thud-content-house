#!/usr/bin/env python3
"""Draw Thud, the deadpan stone creature, the same way every time.

Thud = 3 stacked rounded slate stones + a small pebble on top, warm amber
glowing seams between stones, two amber half-moon eyes, no mouth.
Style note: soft-shaded shapes with NO black outlines, on purpose, so the
look stays clearly different from thick-outline 2D cartoon styles.

Use from Python:
    from thud import draw
    img = draw("idle", height=360)      # RGBA PIL image

Use from the command line (makes a pose sheet to look at):
    python3 tools/thud.py --sheet thud_poses.png

Poses: idle, blink, half_blink, glance_left, glance_right
Python 3.9 compatible. Needs Pillow only.
"""
import argparse
import math
from functools import lru_cache

from PIL import Image, ImageChops, ImageDraw, ImageFilter

POSES = ("idle", "blink", "half_blink", "glance_left", "glance_right")

# Brand colors (keep in sync with house-rules skill)
STONE = (94, 108, 123)        # slate blue-grey
STONE_HI = (134, 150, 166)    # highlight
STONE_LO = (63, 73, 84)       # shadow
AMBER = (255, 178, 56)        # seams + eyes
AMBER_LIGHT = (255, 214, 130)
AMBER_GLOW = (255, 150, 28)

SS = 4  # supersampling factor for smooth edges

# Stones from bottom to top: (center_x, center_y, width, height, phase) in
# units of the canvas height. Canvas width = 0.9 * height.
STONES = (
    (0.450, 0.800, 0.86, 0.300, 0.3),   # base
    (0.468, 0.548, 0.72, 0.255, 1.7),   # middle
    (0.440, 0.300, 0.64, 0.270, 2.9),   # head (eyes live here)
    (0.560, 0.135, 0.20, 0.085, 4.1),   # pebble on top
)
CANVAS_W = 0.90
HEAD = 2


def _stone_polygon(cx, cy, w, h, phase, scale, n=180):
    """Superellipse with fixed gentle bumps so it reads as a real stone."""
    pts = []
    a, b = w * scale / 2.0, h * scale / 2.0
    p = 2.6
    for i in range(n):
        t = 2 * math.pi * i / n
        ct, st = math.cos(t), math.sin(t)
        x = a * math.copysign(abs(ct) ** (2.0 / p), ct)
        y = b * math.copysign(abs(st) ** (2.0 / p), st)
        bump = 1.0 + 0.035 * math.sin(3 * t + phase) + 0.02 * math.sin(5 * t + 2 * phase)
        pts.append((cx * scale + x * bump, cy * scale + y * bump))
    return pts


def _mask(size, polygon):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(polygon, fill=255)
    return m


def _fill(size, color, mask, alpha=255):
    layer = Image.new("RGBA", size, color + (0,))
    a = mask if alpha == 255 else mask.point(lambda v: v * alpha // 255)
    layer.putalpha(a)
    return layer


def _eye_masks(size, scale, pose):
    cx, cy, w, h, _ = STONES[HEAD]
    shift = {"glance_left": -0.035, "glance_right": 0.035}.get(pose, 0.0)
    lid = {"idle": 0.45, "glance_left": 0.45, "glance_right": 0.45,
           "half_blink": 0.74, "blink": 0.93}[pose]
    ew, eh = 0.115 * scale, 0.085 * scale
    masks = []
    for side in (-1, 1):
        ex = (cx + side * 0.15 + shift) * scale
        ey = (cy - 0.005) * scale
        m = Image.new("L", size, 0)
        ImageDraw.Draw(m).ellipse((ex - ew / 2, ey - eh / 2, ex + ew / 2, ey + eh / 2), fill=255)
        # heavy upper lid: clear everything above the lid line -> half-moon
        lid_y = int(ey - eh / 2 + eh * lid)
        ImageDraw.Draw(m).rectangle((0, 0, size[0], lid_y), fill=0)
        masks.append(m)
    return masks


@lru_cache(maxsize=64)
def draw(pose="idle", height=360):
    """Return Thud as an RGBA image `height` pixels tall."""
    if pose not in POSES:
        raise ValueError("unknown pose %r; use one of %s" % (pose, ", ".join(POSES)))
    scale = height * SS
    size = (int(CANVAS_W * scale), int(scale))
    img = Image.new("RGBA", size, (0, 0, 0, 0))

    # ground shadow so Thud sits on the photo
    sh = Image.new("L", size, 0)
    bx, by, bw, bh, _ = STONES[0]
    ImageDraw.Draw(sh).ellipse(((bx - bw * 0.55) * scale, (by + bh * 0.34) * scale,
                                (bx + bw * 0.55) * scale, (by + bh * 0.50) * scale), fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(scale * 0.02))
    img.alpha_composite(_fill(size, (10, 10, 12), sh))

    masks = [_mask(size, _stone_polygon(*s, scale=scale)) for s in STONES]
    # slightly bigger copies of each stone, used to find the seams (fast "dilation")
    grown = [_mask(size, _stone_polygon(cx, cy, w + 0.03, h + 0.03, ph, scale))
             for (cx, cy, w, h, ph) in STONES]

    for i, m in enumerate(masks):
        if i > 0:
            # amber seam where this stone sits on the one below
            below = grown[i - 1]
            ring = ImageChops.subtract(grown[i], m)
            seam = ImageChops.multiply(ring, below)
            glow = seam.filter(ImageFilter.GaussianBlur(scale * 0.018))
            img.alpha_composite(_fill(size, AMBER_GLOW, glow.point(lambda v: min(255, v * 3))))
            img.alpha_composite(_fill(size, AMBER, seam))
        cx, cy, w, h, ph = STONES[i]
        img.alpha_composite(_fill(size, STONE, m))
        # shadow on the lower part of each stone
        lo = _mask(size, _stone_polygon(cx + 0.01, cy + h * 0.22, w * 0.98, h * 0.7, ph, scale))
        lo = ImageChops.multiply(lo.filter(ImageFilter.GaussianBlur(scale * 0.02)), m)
        img.alpha_composite(_fill(size, STONE_LO, lo, alpha=170))
        # highlight up and to the left
        hi = _mask(size, _stone_polygon(cx - w * 0.12, cy - h * 0.18, w * 0.55, h * 0.45, ph, scale))
        hi = ImageChops.multiply(hi.filter(ImageFilter.GaussianBlur(scale * 0.025)), m)
        img.alpha_composite(_fill(size, STONE_HI, hi, alpha=150))

    # eyes: glow, fill, bright core
    for em in _eye_masks(size, scale, pose):
        img.alpha_composite(_fill(size, AMBER_GLOW, em.filter(ImageFilter.GaussianBlur(scale * 0.02)), alpha=230))
        img.alpha_composite(_fill(size, AMBER, em))
        core = em.filter(ImageFilter.GaussianBlur(scale * 0.006)).point(lambda v: 255 if v > 235 else 0)
        img.alpha_composite(_fill(size, AMBER_LIGHT, core, alpha=200))

    out = img.resize((max(1, size[0] // SS), max(1, size[1] // SS)), Image.LANCZOS)
    return out


def pose_sheet(height=360, bg=(200, 182, 150)):
    tiles = [draw(p, height) for p in POSES]
    pad = 40
    w = sum(t.width for t in tiles) + pad * (len(tiles) + 1)
    h = height + pad * 2 + 50
    sheet = Image.new("RGBA", (w, h), bg + (255,))
    d = ImageDraw.Draw(sheet)
    x = pad
    for p, t in zip(POSES, tiles):
        sheet.alpha_composite(t, (x, pad))
        d.text((x, pad + height + 10), p, fill=(30, 30, 30))
        x += t.width + pad
    return sheet.convert("RGB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Draw Thud poses")
    ap.add_argument("--sheet", required=True, help="output PNG path for a sheet of all poses")
    ap.add_argument("--height", type=int, default=360)
    a = ap.parse_args()
    pose_sheet(a.height).save(a.sheet)
    print(a.sheet)
