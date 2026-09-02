#!/usr/bin/env python3
"""Poster Polistiwall — perete în picioare 120×340 cm, polistiren grafit 20 cm + beton 20 cm."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "shared" / "images" / "polistiwall" / "polistiwall-3d-poster-v2.jpg"

W_CM, H_CM = 120, 340
T_PSE, T_BETON = 20, 20

IMG_W = 600
IMG_H = int(IMG_W * H_CM / W_CM)


def noise_rect(img, box, base, var=16, seed=0):
    x0, y0, x1, y1 = [int(v) for v in box]
    rnd = random.Random(seed)
    px = img.load()
    for y in range(max(0, y0), min(img.height, y1)):
        for x in range(max(0, x0), min(img.width, x1)):
            n = rnd.randint(-var, var)
            px[x, y] = tuple(max(0, min(255, c + n)) for c in base)


def pse_texture(draw, img, x0, y0, x1, y1, rows=20):
    """Față polistiren grafit — rosturi orizontale."""
    C = (36, 36, 40)
    C2 = (52, 52, 56)
    h = y1 - y0
    gap = 2
    rh = h / rows
    for r in range(rows):
        ry0 = int(y0 + r * rh + gap)
        ry1 = int(y0 + (r + 1) * rh - gap)
        draw.rectangle([x0, ry0, x1, ry1], fill=C)
        draw.line([x0, ry0, x1, ry0], fill=C2, width=1)
    noise_rect(img, (x0, y0, x1, y1), C, 14, 3)


def main():
    random.seed(42)
    BG = (245, 240, 234)
    C_BETON = (172, 168, 160)
    C_BETON_D = (145, 142, 135)

    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    draw = ImageDraw.Draw(img)

    mx, my = 70, 50
    fw = IMG_W - mx * 2 - 50   # față perete (120 cm)
    fh = IMG_H - my * 2 - 30   # înălțime (340 cm)
    cut = int(fw * T_PSE / (T_PSE + T_BETON))  # lățime secțiune tăiată

    fx0, fy0 = mx, my
    fx1, fy1 = fx0 + fw, fy0 + fh

    # Umbră
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([fx0, fy1 + 5, fx1 + cut + 30, fy1 + 35], fill=(0, 0, 0, 40))
    img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Fața peretelui — polistiren grafit (120×340)
    pse_texture(draw, img, fx0, fy0, fx1, fy1)

    # Colț tăiat — arată grosimea: PSE 20 + beton 20
    # Beton (interior)
    bx0 = fx1
    bx1 = fx1 + cut
    draw.rectangle([bx0, fy0, bx1, fy1], fill=C_BETON)
    noise_rect(img, (bx0, fy0, bx1, fy1), C_BETON, 10, 8)

    # Muchie superioară beton (perspectivă)
    draw.polygon(
        [(fx1, fy0), (bx1, fy0 - 12), (bx1 + 12, fy0 - 6), (fx1, fy0 + 6)],
        fill=C_BETON_D,
    )
    # Muchie PSE pe tăietură (20 cm)
    pse_texture(draw, img, fx1 - cut, fy0, fx1, fy1, rows=20)

    # Linie între PSE și beton pe tăietură
    draw.line([fx1, fy0, fx1, fy1], fill=(25, 25, 28), width=2)

    # Contur perete
    draw.rectangle([fx0, fy0, fx1, fy1], outline=(190, 185, 178), width=1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "JPEG", quality=93, optimize=True)
    print(f"✓ Perete {W_CM}×{H_CM} cm, PSE {T_PSE} cm + beton {T_BETON} cm → {OUT.name}")


if __name__ == "__main__":
    main()
