#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Radiografia planului: citirea pe pixeli + poarta de suprapunere.

Stilul de lucru (după seara pierdută din 17.08 — vezi CITIRE-PIXELI.md):

1. `tigla`     — taie poza în țigle mărite 4×, ca să CITEȘTI planul bucată cu
                 bucată înainte să desenezi orice. Dulapurile cu X nu-s pereți,
                 ușile spre terase există, mobila e cu linie subțire.
2. `ziduri`    — extrage DOAR pereții din poză: cerneala groasă rămâne,
                 mobila/textul/cotele (linii subțiri) dispar morfologic.
3. `profil`    — procentul de plin de-a lungul unei linii de perete:
                 ~80% = perete cu ferestre, golurile sunt golurile;
                 sub 50% = conturul e greșit ACOLO — nu inventa, remăsoară.
4. `suprapune` — POARTA FINALĂ: pereții modelului meu, rasterizați la scara
                 originalului, peste radiografia lui. Negru = amândoi,
                 roșu = doar eu, gri = doar originalul. Sub 60% potrivire
                 nu există „gata".

Nicio valoare nemăsurată în fișierul de model. Ce lipsește se spune că lipsește.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


# ─── citirea pozei ──────────────────────────────────────────────────────────

def cerneala(cale, prag=110):
    """masca de cerneală (True = întunecat)"""
    g = np.array(Image.open(cale).convert("L"))
    return g < prag


def ziduri(masca, pxm, gros_min_m=0.14):
    """păstrează doar cerneala GROASĂ = pereții.

    Deschidere morfologică cu pătrat de ~gros_min_m: liniile de mobilier,
    textul și cotele (1–2 px) dispar; zidurile pline rămân.
    """
    r = max(2, int(round(gros_min_m * pxm)))
    el = np.ones((r, r), bool)
    return ndimage.binary_opening(masca, structure=el)


def cutia(masca):
    """dreptunghiul care cuprinde tot ce e True: (x0, y0, x1, y1) inclusiv"""
    ys, xs = np.where(masca)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def tigla(cale, out_dir, zoom=4, nt=3, suprapunere=0.15):
    """taie poza în nt×nt țigle mărite `zoom`×, cu suprapunere între ele"""
    im = Image.open(cale)
    W, H = im.size
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    pw, ph = W / nt, H / nt
    cai = []
    for j in range(nt):
        for i in range(nt):
            x0 = max(0, int(i * pw - suprapunere * pw))
            y0 = max(0, int(j * ph - suprapunere * ph))
            x1 = min(W, int((i + 1) * pw + suprapunere * pw))
            y1 = min(H, int((j + 1) * ph + suprapunere * ph))
            t = im.crop((x0, y0, x1, y1))
            t = t.resize((t.width * zoom, t.height * zoom), Image.LANCZOS)
            c = out / f"t{j}{i}.png"
            t.save(c); cai.append(str(c))
    return cai


def profil(masca_ziduri, axa, poz, a, b, gros_px=6):
    """procent de plin de-a lungul liniei; întoarce (procent, goluri).

    axa='x': linia orizontală y=poz, de la x=a la x=b.
    axa='y': linia verticală  x=poz, de la y=a la y=b.
    golurile = liste (start_px, lungime_px) unde nu e perete.
    """
    g2 = gros_px // 2
    if axa == "x":
        banda = masca_ziduri[poz - g2:poz + g2 + 1, a:b + 1]
    else:
        banda = masca_ziduri[a:b + 1, poz - g2:poz + g2 + 1].T
    plin = banda.any(axis=0)
    goluri, i = [], 0
    while i < len(plin):
        if not plin[i]:
            j = i
            while j + 1 < len(plin) and not plin[j + 1]:
                j += 1
            goluri.append((a + i, j - i + 1))
            i = j + 1
        else:
            i += 1
    return float(plin.mean()), goluri


# ─── rasterizarea modelului ─────────────────────────────────────────────────

def rasterizeaza(n, pxm):
    """pereții unui Nivel din plansa.py, ca mască de pixeli.

    Coordonatele camerelor/pereților sunt INTERIOARE; conturul e al zidăriei
    (colțul NV al feței interioare = (0,0), deci conturul începe la (-PE,-PE)).
    Originea imaginii = colțul NV al zidăriei exterioare.
    """
    from plansa import PE, PI, _inset
    pe = n.pe
    ext = n.contur if n.contur else [(-pe, -pe), (n.L - pe, -pe),
                                     (n.L - pe, n.A - pe), (-pe, n.A - pe)]
    X = lambda mm: (mm + pe) * pxm / 1000.0
    Y = lambda mm: (mm + pe) * pxm / 1000.0
    xs = [X(p[0]) for p in ext]; ys = [Y(p[1]) for p in ext]
    W = int(max(xs) + 2); H = int(max(ys) + 2)
    im = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(im)

    # banda peretelui exterior: poligonul plin minus interiorul retras cu PE
    # (_inset poate retrage în oricare sens, după orientarea conturului —
    #  se alege varianta a cărei cutie e MAI MICĂ decât a conturului)
    dr.polygon([(X(x), Y(y)) for x, y in ext], fill=255)
    cut = lambda pts: (min(p[0] for p in pts), min(p[1] for p in pts),
                       max(p[0] for p in pts), max(p[1] for p in pts))
    interior = _inset(ext, pe)
    ce, ci = cut(ext), cut(interior)
    if not (ci[0] >= ce[0] and ci[1] >= ce[1] and ci[2] <= ce[2] and ci[3] <= ce[3]):
        interior = _inset(ext, -pe)
    dr.polygon([(X(x), Y(y)) for x, y in interior], fill=0)

    # compartimentările
    for (x, y, w, h) in n.pereti:
        dr.rectangle([X(x), Y(y), X(x + w), Y(y + h)], fill=255)

    # golurile: uși interioare, ferestre/uși pe laturi, goluri absolute, nișe
    IL, IA = n.L - 2 * pe, n.A - 2 * pe
    taie = lambda x0, y0, x1, y1: dr.rectangle([X(x0), Y(y0), X(x1), Y(y1)], fill=0)
    for g in n.goluri:
        f = g["fel"]
        if f == "usa":
            if g.get("oriz", True):
                taie(g["x"], g["y"] - PI, g["x"] + g["l"], g["y"] + 2 * PI)
            else:
                taie(g["x"] - PI, g["y"], g["x"] + 2 * PI, g["y"] + g["l"])
        elif f in ("fereastra", "usa_ext"):
            lat, p, l = g["latura"], g["poz"], g["l"]
            if lat == "N":   taie(p, -pe, p + l, 0)
            elif lat == "S": taie(p, IA, p + l, IA + pe)
            elif lat == "V": taie(-pe, p, 0, p + l)
            elif lat == "E": taie(IL, p, IL + pe, p + l)
        elif f == "ext_abs":
            taie(g["x"], g["y"], g["x"] + g["l"], g["y"] + g["h"])
    for z in n.nise:
        lat, p, la, ad = z["latura"], z["poz"], z["lat"], z["adanc"]
        if lat == "N":   taie(p, -pe, p + la, -pe + ad)
        elif lat == "S": taie(p, IA + pe - ad, p + la, IA + pe)
        elif lat == "V": taie(-pe, p, -pe + ad, p + la)
        elif lat == "E": taie(IL + pe - ad, p, IL + pe, p + la)

    return np.array(im) > 127


# ─── poarta de suprapunere ──────────────────────────────────────────────────

def suprapune(orig_ziduri, model_ziduri, out, marire=2):
    """aliniază pe cutii (scară separată pe x și y), colorează, măsoară.

    Negru  = perete în amândouă.
    Roșu   = perete DOAR la mine (eu am zid unde ei n-au).
    Gri    = perete DOAR la ei (le lipsește zidul meu).
    Întoarce procentul de suprapunere (IoU pe pixeli de perete).
    """
    ox0, oy0, ox1, oy1 = cutia(orig_ziduri)
    o = orig_ziduri[oy0:oy1 + 1, ox0:ox1 + 1]
    mx0, my0, mx1, my1 = cutia(model_ziduri)
    m = model_ziduri[my0:my1 + 1, mx0:mx1 + 1]
    mi = Image.fromarray((m * 255).astype(np.uint8)).resize(
        (o.shape[1], o.shape[0]), Image.NEAREST)
    m2 = np.array(mi) > 127

    iou = (o & m2).sum() / max(1, (o | m2).sum())

    rgb = np.full((*o.shape, 3), 255, np.uint8)
    rgb[o & ~m2] = (170, 170, 170)
    rgb[m2 & ~o] = (220, 40, 40)
    rgb[o & m2] = (20, 20, 20)
    im = Image.fromarray(rgb)
    im = im.resize((im.width * marire, im.height * marire), Image.NEAREST)
    im.save(out)
    return iou


def alaturi(cale_orig, cale_plansa, out, H=760):
    """planul meu LÂNGĂ original, la aceeași înălțime — ultima privire umană"""
    a = Image.open(cale_orig); b = Image.open(cale_plansa)
    a2 = a.resize((int(a.width * H / a.height), H))
    b2 = b.resize((int(b.width * H / b.height), H))
    c = Image.new("RGB", (a2.width + b2.width + 24, H), "white")
    c.paste(a2, (0, 0)); c.paste(b2, (a2.width + 24, 0))
    c.save(out)
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "tigla":
        for c in tigla(sys.argv[2], sys.argv[3],
                       zoom=int(sys.argv[4]) if len(sys.argv) > 4 else 4):
            print(c)
    elif cmd == "ziduri":
        cale, pxm, out = sys.argv[2], float(sys.argv[3]), sys.argv[4]
        z = ziduri(cerneala(cale), pxm)
        Image.fromarray((~z * 255).astype(np.uint8)).save(out)
        print(out, "cutie:", cutia(z))
    else:
        print(__doc__)
