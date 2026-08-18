#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Măsoară un plan 2D dintr-o poză şi îl scoate în milimetri.

Ideea patronului: nu inventez compartimentarea, o măsor. Poza are o cotă
scrisă (ex. 8,75 m), deci am etalonul.

Metoda: se caută BENZILE DE PERETE (coloane/rânduri cu multă cerneală), se
astupă golurile de uşă doar pe lungimea benzii respective, şi se desenează
grila de axe. Camerele sunt celulele grilei. Golurile astupate se reţin: alea
sunt uşile.

Verificarea e gratuită: suprafeţele măsurate trebuie să dea cifrele scrise pe
planul original. Dacă nu dau, măsurătoarea e greşită.
"""
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

USA_MAX = 1.45          # m — peste atât nu mai e uşă, e trecere deschisă
PERETE_MIN = 0.55       # m — sub atât nu e perete, e mobilă


def benzi(marcat, lipire=2):
    """grupează indicii marcaţi în benzi contigue"""
    out, i = [], 0
    idx = np.where(marcat)[0]
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and idx[j + 1] - idx[j] <= lipire:
            j += 1
        out.append((int(idx[i]), int(idx[j])))
        i = j + 1
    return out


def linii(z, pxm, axa):
    """benzile de perete pe o axă, cu golurile de uşă închise.

    axa=0 → pereţi verticali (se caută pe coloane)
    axa=1 → pereţi orizontali
    """
    zz = z if axa == 0 else z.T
    H, W = zz.shape
    acop = zz.sum(axis=0) / H
    out = []
    for (a, b) in benzi(acop > 0.055):
        if b - a + 1 < 2:
            continue
        prof = zz[:, a:b + 1].mean(axis=1) > 0.5      # unde e plin peretele
        seg = benzi(prof, lipire=1)
        if not seg:
            continue
        if sum(s[1] - s[0] + 1 for s in seg) < PERETE_MIN * pxm:
            continue
        usi, plin = [], [list(seg[0])]
        for s in seg[1:]:
            gol = s[0] - plin[-1][1] - 1
            if gol <= USA_MAX * pxm:
                usi.append((plin[-1][1] + 1, gol))
                plin[-1][1] = s[1]
            else:
                plin.append(list(s))
        for (p0, p1) in plin:
            out.append(dict(a=a, b=b, p0=p0, p1=p1,
                            usi=[u for u in usi if p0 <= u[0] <= p1]))
    return out


def masoara(cale, cutie, cota_m, prag=110):
    a = np.array(Image.open(cale).convert("L"))
    x0, x1, y0, y1 = cutie
    z = (a < prag)[y0:y1, x0:x1]
    H, W = z.shape
    pxm = (y1 - y0) / cota_m

    vert = linii(z, pxm, 0)
    oriz = linii(z, pxm, 1)

    # grila se desenează pe LĂŢIMEA REALĂ a peretelui, ca să măsor între feţe
    grila = np.zeros_like(z)
    for L in vert:
        grila[L["p0"]:L["p1"] + 1, L["a"]:L["b"] + 1] = True
    for L in oriz:
        grila[L["a"]:L["b"] + 1, L["p0"]:L["p1"] + 1] = True
    grila[0, :] = grila[-1, :] = grila[:, 0] = grila[:, -1] = True

    lab, n = ndimage.label(~grila)
    cam = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < (0.85 * pxm) ** 2:
            continue
        ys, xs = np.where(m)
        cam.append(dict(x=int(xs.min()), y=int(ys.min()),
                        w=int(xs.max() - xs.min() + 1),
                        h=int(ys.max() - ys.min() + 1),
                        arie=float(m.sum()) / pxm ** 2))
    cam.sort(key=lambda c: -c["arie"])

    usi, vazut = [], set()
    for L in vert:
        c = (L["a"] + L["b"]) // 2
        for (p, l) in L["usi"]:
            k = (round(c / 8), round(p / 8))
            if k in vazut: continue
            vazut.add(k); usi.append(dict(fel="perete vertical", x=c, y=p, l=l))
    for L in oriz:
        c = (L["a"] + L["b"]) // 2
        for (p, l) in L["usi"]:
            k = (round(p / 8), round(c / 8))
            if k in vazut: continue
            vazut.add(k); usi.append(dict(fel="perete orizontal", x=p, y=c, l=l))

    mm = lambda p: int(round(p / pxm * 1000))
    return dict(
        sursa=cale, px_pe_metru=round(pxm, 2), gabarit_mm=[mm(W), mm(H)],
        camere=[dict(x=mm(c["x"]), y=mm(c["y"]), w=mm(c["w"]), h=mm(c["h"]),
                     arie=round(c["arie"], 2)) for c in cam],
        usi=[dict(fel=u["fel"], x=mm(u["x"]), y=mm(u["y"]), l=mm(u["l"])) for u in usi])


if __name__ == "__main__":
    cale = sys.argv[1] if len(sys.argv) > 1 else "ref/p88-77/05.jpg"
    d = masoara(cale, (60, 863, 329, 778), 8.75)
    json.dump(d, open("ref/p88-77/masurat.json", "w"), ensure_ascii=False, indent=1)
    print("etalon %.2f px/m · gabarit %d × %d mm" % (d["px_pe_metru"], *d["gabarit_mm"]))
    print("\n  camere (%d):" % len(d["camere"]))
    tot = 0
    for c in d["camere"]:
        tot += c["arie"]
        print("   %6.2f m²   x=%5d y=%5d   %5d × %5d mm"
              % (c["arie"], c["x"], c["y"], c["w"], c["h"]))
    print("   ─────── total %.2f m²" % tot)
    scris = [30.98, 11.94, 10.27, 9.27, 8.95, 6.99, 5.42, 3.51, 2.75, 2.01, 2.00, 1.71]
    print("   scris pe planul lor: %.2f m² în %d camere" % (sum(scris), len(scris)))
    print("\n  uşi (%d):" % len(d["usi"]))
    for u in sorted(d["usi"], key=lambda u: -u["l"])[:18]:
        print("   %-18s x=%5d y=%5d  lăţime %4d mm" % (u["fel"], u["x"], u["y"], u["l"]))
