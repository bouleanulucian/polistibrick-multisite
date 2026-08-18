#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regla grila lui 80-49 pe AMBELE surse: ariile scrise + pozițiile pe pixeli.

Aseară grila a fost rezolvată doar pe arii → arii 0,0% dar pereții nu stau
unde stau în original (mai multe grile dau aceleași arii). Aici:

  · fiecare linie de perete se MĂSOARĂ în radiografia originalului, doar pe
    întinderea ei reală (nu pe tot planul — altfel liniile străine murdăresc);
  · grila se rezolvă least-squares: ariile scrise ca reziduuri grele,
    pozițiile măsurate ca reziduuri ușoare;
  · modelul de aseară primește un WARP liniar pe bucăți (nodurile = grila):
    topologia, ușile, mobilierul rămân, doar proporțiile se așază.

Poarta finală: suprapunerea + planul lângă original.
"""
import copy
import sys

import numpy as np
from scipy import ndimage, optimize

sys.path.insert(0, ".")
from radiografie import cerneala, ziduri, cutia, rasterizeaza, suprapune
from plansa import PE, PI

# ─── originalul: radiografie + măști separate pe direcții ───────────────────

GAB_X, GAB_Y = 19850.0, 18050.0            # gabaritul SCRIS pe planșa lor

m = cerneala("ref/p80-49/04.jpg")
z = ziduri(m, 30)
lab, nlab = ndimage.label(z)
margine = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
for i in margine:
    if i:
        z[lab == i] = False
bx0, by0, bx1, by1 = cutia(z)
zc = z[by0:by1 + 1, bx0:bx1 + 1]
PXX = (bx1 - bx0 + 1) / GAB_X * 1000        # px pe metru, separat pe axe
PXY = (by1 - by0 + 1) / GAB_Y * 1000
el = max(3, int(0.9 * PXX / 1000 * 1000 / 1000 * 900 / 900))  # ~0,9 m
el = max(3, int(0.9 * PXX))
ZV = ndimage.binary_opening(zc, structure=np.ones((el, 1), bool))
ZH = ndimage.binary_opening(zc, structure=np.ones((1, el), bool))


def masoara_linie(oriz, centru_mm, span_mm, fereastra=900):
    """centrul de cerneală al liniei, căutat în ±fereastra, doar pe span.

    oriz=False → linie verticală (poziţie pe x), se caută în ZV.
    Întoarce (mm, încredere 0..1) sau (None, 0) dacă nu e destulă cerneală.
    """
    if not oriz:
        px, span_px = PXX, (int(span_mm[0] / 1000 * PXY), int(span_mm[1] / 1000 * PXY))
        M = ZV[span_px[0]:span_px[1] + 1, :]
        prof = M.sum(axis=0).astype(float)
    else:
        px, span_px = PXY, (int(span_mm[0] / 1000 * PXX), int(span_mm[1] / 1000 * PXX))
        M = ZH[:, span_px[0]:span_px[1] + 1]
        prof = M.sum(axis=1).astype(float)
    c = int(centru_mm / 1000 * px)
    f = int(fereastra / 1000 * px)
    a, b = max(0, c - f), min(len(prof) - 1, c + f)
    w = prof[a:b + 1]
    if w.sum() < 0.5 * px:                          # sub 0,5 m de cerneală: nu măsor
        return None, 0.0
    idx = np.arange(a, b + 1)
    centru = (idx * w).sum() / w.sum()
    incredere = min(1.0, w.max() / ((span_px[1] - span_px[0] + 1) * 0.5 + 1e-9))
    return centru / px * 1000, incredere


# ─── nodurile warpului și măsurătorile lor ──────────────────────────────────
# coordonate INTERIOARE (ca în p8049). ext = int + 380.
E = lambda v: v + PE

NODX = [-380, 1515, 2837, 4895, 6304, 8779, 8966, 11010, 13302, 19133, 19320]
RIGX = {2967: (2837, 130)}                   # perechi de feţe: nod legat = bază + gol
NODY = [-380, 2376, 3333, 4814, 6634, 6760, 7313, 8764, 8934, 10828,
        12212, 13078, 17288, 17610]
RIGY = {2054: (2376, -322), 4944: (4814, 130), 5660: (5660, 0), 5982: (5982, 0),
        6890: (6760, 130), 7443: (7313, 130), 8894: (8764, 130),
        9064: (8934, 130), 10157: (10828, -671)}
# 5660/5982 (aripa) sunt noduri proprii:
NODY += [5660, 5982]
NODY = sorted(set(NODY))

# măsurători: (nod, oriz, centru aşteptat ext mm, span ext mm)
MASURI_X = [
    (-380, False, 190, (0, 18050)),
    (1515, False, E(1515) + 65, (E(6890), E(8934))),
    (2837, False, E(2902) + 0, (380, E(8934))),          # perechea 2837/2967
    (4895, False, E(4895) + 65, (E(3333), E(8764))),
    (6304, False, E(6304) + 65, (E(7443), E(8764))),
    (8966, False, E(8966) - 190, (380, E(5660))),        # zid contur corp-est
    (11010, False, E(11010) + 65, (E(5982), E(8934))),
    (13302, False, E(13367), (E(5982), E(12212))),       # perechea 13302/13432
    (19320, False, E(19320) - 190, (E(5982), E(12212))),
]
MASURI_Y = [
    (-380, True, 190, (0, E(8966))),
    (2376, True, E(2376) + 65, (E(2967), E(8779))),
    (4814, True, E(4879), (380, E(2837))),
    (5660, True, E(5660) + 190, (E(8966), 19700)),
    (6760, True, E(6825), (380, E(2837))),
    (7313, True, E(7378), (E(4895), E(8779))),
    (8764, True, E(8829), (E(4895), E(8779))),
    (8934, True, E(8999), (380, E(13302))),
    (10828, True, E(10893), (E(8966), E(13302))),
    (12212, True, E(12212) + 190, (E(8966), 19700)),
    (17288, True, E((17288 + 17610) / 2 + 380 - 380) + 161, (380, E(8966))),
]

# ariile SCRISE pe planul original (m²) — nimic neetichetat nu intră
ARII = {"Dormitor 2": 13.66, "Dormitor 3": 13.85, "Hol": 10.23,
        "Dormitor 1": 15.46, "Baie 1": 5.15, "Tehnic": 3.07,
        "Grup sanitar": 2.68, "Spălătorie": 1.86, "Dressing": 3.27,
        "Bucătărie": 9.30, "Hol de zi": 12.73, "Living · dining": 37.75,
        "Baie 2": 5.65, "Tehnic 2": 5.34, "Antreu": 7.65, "Garaj": 35.51}


def masoara_tot():
    tx, ty = {}, {}
    for nod, oriz, c, span in MASURI_X:
        v, k = masoara_linie(oriz, c, span)
        if v is not None:
            # ținta pt. NOD: nodul e faţa stângă/altă referinţă — păstrez offsetul aşteptat
            tx[nod] = (v - (c - E(nod)), k)     # v_mm(ext) − offset → poziţia ext a nodului
    for nod, oriz, c, span in MASURI_Y:
        v, k = masoara_linie(oriz, c, span)
        if v is not None:
            ty[nod] = (v - (c - E(nod)), k)
    return tx, ty


# ─── warpul ─────────────────────────────────────────────────────────────────

def fa_warp(noduri, valori):
    nd = np.array(noduri, float)
    vl = np.array(valori, float)
    def f(x):
        return float(np.interp(x, nd, vl))
    return f


def aplica(n0, fx, fy):
    n = copy.deepcopy(n0)
    W = lambda x, w: (fx(x), fx(x + w) - fx(x))
    Hh = lambda y, h: (fy(y), fy(y + h) - fy(y))
    for c in n.camere:
        c["x"], c["w"] = W(c["x"], c["w"]); c["y"], c["h"] = Hh(c["y"], c["h"])
    n.pereti = [(fx(x), fy(y), fx(x + w) - fx(x) if w > PI else w,
                 fy(y + h) - fy(y) if h > PI else h) for (x, y, w, h) in n.pereti]
    for g in n.goluri:
        if g["fel"] == "usa":
            g["x"], g["y"] = fx(g["x"]), fy(g["y"])
        elif g["fel"] in ("fereastra", "usa_ext"):
            g["poz"] = fx(g["poz"]) if g["latura"] in "NS" else fy(g["poz"])
        elif g["fel"] == "ext_abs":
            g["x"], g["y"] = fx(g["x"]), fy(g["y"])
    for z_ in n.zone:
        z_["x"], z_["y"] = fx(z_["x"]), fy(z_["y"])
    for mo in n.mobila:
        mo["x"], mo["y"] = fx(mo["x"]), fy(mo["y"])
    for ni in n.nise:
        ni["poz"] = fx(ni["poz"]) if ni["latura"] in "NS" else fy(ni["poz"])
    if n.contur:
        n.contur = [(fx(x), fy(y)) for (x, y) in n.contur]
    n.L = fx(n.L - n.pe) + n.pe                     # L,A erau ext = IL+PE
    n.A = fy(n.A - n.pe) + n.pe
    return n


def rezolva(n0, tinte_x, tinte_y, W_ARIE=60.0, W_POZ=1 / 60.0):
    """noduri libere; reziduuri: arii (m²·W_ARIE) + poziţii (mm·W_POZ)"""
    libere_x = [v for v in NODX]
    libere_y = [v for v in NODY]
    x0 = np.array([float(v) for v in libere_x] + [float(v) for v in libere_y])
    nx = len(libere_x)
    cam0 = {c["nume"]: c for c in n0.camere}

    def rez(p):
        vx, vy = p[:nx], p[nx:]
        fx = fa_warp(libere_x, vx); fy = fa_warp(libere_y, vy)
        r = []
        for nume, a in ARII.items():
            c = cam0[nume]
            w = fx(c["x"] + c["w"]) - fx(c["x"])
            h = fy(c["y"] + c["h"]) - fy(c["y"])
            r.append((w * h / 1e6 - a) * W_ARIE)
        for nod, (tinta_ext, k) in tinte_x.items():
            fxn = fx(nod) + PE
            r.append((fxn - tinta_ext) * W_POZ * (0.4 + 0.6 * k))
        for nod, (tinta_ext, k) in tinte_y.items():
            fyn = fy(nod) + PE
            r.append((fyn - tinta_ext) * W_POZ * (0.4 + 0.6 * k))
        # gabaritul scris, tare
        r.append((fx(19320) + PE - GAB_X) * 0.5)
        r.append((fy(17610) + PE - GAB_Y) * 0.5)
        r.append((fx(-380) + PE - 0) * 0.5)
        r.append((fy(-380) + PE - 0) * 0.5)
        # monotonie
        for v in (np.diff(vx), np.diff(vy)):
            r.extend(np.minimum(0, v - 60) * 0.2)
        return r

    sol = optimize.least_squares(rez, x0, method="lm", xtol=1e-10)
    vx, vy = sol.x[:nx], sol.x[nx:]
    return fa_warp(libere_x, vx), fa_warp(libere_y, vy)


if __name__ == "__main__":
    import p8049
    n0 = p8049.n
    tx, ty = masoara_tot()
    print("ținte măsurate pe pixeli:")
    for nod, (v, k) in sorted(tx.items()):
        print("  x nod %6d: ext %7.0f (era %7.0f)  încredere %.2f" % (nod, v, E(nod), k))
    for nod, (v, k) in sorted(ty.items()):
        print("  y nod %6d: ext %7.0f (era %7.0f)  încredere %.2f" % (nod, v, E(nod), k))

    fx, fy = rezolva(n0, tx, ty)
    n = aplica(n0, fx, fy)

    print("\narii după rezolvare (scris → obţinut):")
    rau = 0
    for c in n.camere:
        if c["nume"] in ARII:
            a = c["w"] * c["h"] / 1e6
            err = a - ARII[c["nume"]]
            rau = max(rau, abs(err))
            print("  %-16s %6.2f → %6.2f   %+0.3f" % (c["nume"], ARII[c["nume"]], a, err))
    print("  eroarea maximă: %.3f m²" % rau)
    print("gabarit: %.2f × %.2f m" % (n.L / 1000 + 0.38 * 0, (n.A / 1000)))

    from plansa import verifica
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr[:4]))

    mz = rasterizeaza(n, PXX)
    iou = suprapune(z, mz, "/tmp/sup8049b.png", marire=2)
    print("suprapunere: %.1f%%  → /tmp/sup8049b.png" % (iou * 100))

    import pickle
    pickle.dump(n, open("/tmp/n8049_rezolvat.pkl", "wb"))
