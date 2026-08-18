#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ELVA — reproducere proiect 88-77 (domkamen), citit pe pixeli, 18.08.2026.

Radiografia: ref/p88-77/05.jpg, scara 61,355 px/m verificată din DOUĂ cote
scrise (17,15 lățime totală cu terasa de est; 8,75 adâncimea casei — diferență
0,05%). Toate liniile de perete măsurate pe întinderea lor reală; toate
golurile (ferestre + uși) scanate numeric pe fiecare perete; nimic inventat.

Camera de centrală NU are arie scrisă pe planșa lor: ținta ei (4,2 m²) e
diferența dintre totalul din descriere (100 m²) și suma etichetelor (95,8).

Grila se rezolvă least-squares pe ariile scrise (greu) + pozițiile măsurate
(ușor). Pereții: sistemul nostru — 38 exterior (crescut spre exterior),
13 compartimentări. Porticul de intrare e scobit în volum (contur poligonal),
cu peretele de 38 pe fundul lui — acolo se schimbă temperatura.
"""
import sys

import numpy as np

sys.path.insert(0, ".")
from plansa import Nivel, Model, plansa, verifica, PE, PI

MM = lambda v: int(round(v * 1000))

# ─── axele măsurate pe pixeli (metri, în cadrul planșei lor) ────────────────
# exterioarele: fețe interioare fixate din radiografie
XW, YN = 0.45, 0.58          # fața interioară vest / nord
XE, YS = 15.17, 8.28         # fața interioară est / sud
# interioarele: (centru măsurat); grosimea la noi = 0,13
AX0 = dict(a1=4.15, a2=5.68, a3=8.63, s1=2.97, s2=5.22, s3=6.31,
           s4=8.66, s5=10.83, s6=12.00,
           y1=2.49, y2=3.92, y3=5.44, y4=6.13, y5=7.55, ky=5.29)
PW, PE2 = 5.44, 10.50        # marginile porticului (fețele lui laterale)

# ariile scrise pe planșa lor; Centrală = 100 − 95,80 (nemarcată)
ARII = {"Dormitor 1": 11.94, "Dressing": 2.75, "Spălătorie": 1.71,
        "Dormitor 2": 8.95, "Living · dining": 30.98, "Hol": 6.99,
        "Dormitor 3": 10.27, "Baie": 5.42, "WC": 2.01,
        "Centrală": 4.20, "Antreu": 3.51, "Cămară": 2.00,
        "Bucătărie": 9.27}
MOI = {"Centrală"}           # țintă moale (nemarcată pe planșa lor)

H = PI / 1000 / 2            # semigrosimea compartimentării, în metri


def celule(A):
    """camerele ca dreptunghiuri între fețe, în cadrul planșei lor (metri).
    Fundul porticului la noi e perete de 38: fața camerelor = y5 − 0,38/2…
    — folosim fața interioară y5c − 0.19."""
    y5N = A["y5"] - 0.19
    return {
        "Dormitor 1": (XW, A["a1"] - H, YN, A["y2"] - H),
        "Dressing":   (A["a1"] + H, A["a2"] - H, YN, A["y1"] - H),
        "Spălătorie": (A["a1"] + H, A["a2"] - H, A["y1"] + H, A["y2"] - H),
        "Dormitor 2": (A["a2"] + H, A["a3"] - H, YN, A["y2"] - H),
        "Living · dining": (A["a3"] + H, XE, YN, A["ky"]),
        "Hol":        (A["s1"] + H, A["a3"] - H, A["y2"] + H, A["y3"] - H),
        "Dormitor 3": (XW, A["s1"] - H, A["y2"] + H, YS),
        "Baie":       (A["s1"] + H, A["s2"] - H, A["y3"] + H, YS),
        "WC":         (A["s2"] + H, A["s3"] - H, A["y3"] + H, y5N),
        "Centrală":   (A["s3"] + H, A["s4"] - H, A["y3"] + H, y5N),
        "Antreu":     (A["s4"] + H, A["s5"] - H, A["y3"] + H, y5N),
        "Cămară":     (A["s5"] + H, A["s6"] - H, A["y4"] + H, YS),
        "Bucătărie":  (A["s6"] + H, XE, A["ky"], YS),
    }


def rezolva():
    chei = list(AX0)
    x0 = np.array([AX0[k] for k in chei])

    def rez(p):
        A = dict(zip(chei, p))
        r = []
        for nume, (xa, xb, ya, yb) in celule(A).items():
            arie = (xb - xa) * (yb - ya)
            w = 20.0 if nume in MOI else 200.0
            r.append((arie - ARII[nume]) * w)
        for k in chei:                       # nu fugi de pixelii măsurați
            r.append((A[k] - AX0[k]) / 0.08)
        return r

    from scipy.optimize import least_squares
    sol = least_squares(rez, x0, method="lm", xtol=1e-12)
    return dict(zip(chei, sol.x))


A = rezolva()

# ─── nivelul, în coordonate interioare (mm), originea = colțul NV interior ──
ox, oy = XW, YN
X = lambda v: MM(v - ox)
Y = lambda v: MM(v - oy)
IL = X(XE) + PE              # fața exterioară est, în coordonatele interioare
IA = Y(YS) + PE
PWm, PE2m = X(PW), X(PE2)
Y5e = Y(A["y5"] - 0.19) + PE  # fața exterioară a fundului porticului

n = Nivel("PARTER", IL + PE, IA + PE)
n.poligon([(-PE, -PE), (IL, -PE), (IL, IA),
           (PE2m, IA), (PE2m, Y5e), (PWm, Y5e), (PWm, IA), (-PE, IA)])

C = celule(A)
TIP = {"Living · dining": "camera"}
for nume, (xa, xb, ya, yb) in C.items():
    n.camera(nume, X(xa), Y(ya), X(xb) - X(xa), Y(yb) - Y(ya))

# ─── compartimentările (segmente pe axe, fețe din celule) ───────────────────
per = lambda x, y, w, h: n.perete(x, y, w, h)
a1, a2, a3 = X(A["a1"] - H), X(A["a2"] - H), X(A["a3"] - H)
s1, s2, s3 = X(A["s1"] - H), X(A["s2"] - H), X(A["s3"] - H)
s4, s5, s6 = X(A["s4"] - H), X(A["s5"] - H), X(A["s6"] - H)
y1, y2, y3 = Y(A["y1"] - H), Y(A["y2"] - H), Y(A["y3"] - H)
y4, y5 = Y(A["y4"] - H), Y(A["y5"] - 0.19)
per(a1, 0, PI, y2)                          # dormitor 1 | dressing+spălătorie
per(a2, 0, PI, y2)                          # dressing+spălătorie | dormitor 2
per(X(A["a1"]), y1, X(A["a2"]) - X(A["a1"]), PI)   # dressing | spălătorie
per(0, y2, a3, PI)                          # banda de nord | hol + dormitor 3
per(a3, 0, PI, Y(A["ky"]))                  # dormitor 2 + hol | living
per(s1, y2 + PI, PI, IA - y2 - PI)          # dormitor 3 | nișa holului + baie
per(s1 + PI, y3, s2 - s1 - PI, PI)          # nișa holului | baie
per(X(A["s2"]) - MM(0.30), y3, s6 - X(A["s2"]) + MM(0.30), PI)  # hol | WC…antreu
per(s2, y3, PI, IA - y3)                    # baie | WC
per(s3, y3, PI, Y5e - PE - y3)              # WC | centrală
per(s4, y3, PI, Y5e - PE - y3)              # centrală | antreu
per(s5, y3, PI, IA - y3)                    # antreu | cămară (+ colțul portic)
per(s5, y4, s6 - s5, PI)                    # cămara: peretele de nord
per(s6, y4, PI, IA - y4)                    # cămară | bucătărie

# ─── ușile, de pe scanările golurilor (poziții măsurate, lățimi reale) ──────
# pe peretele y2 (banda de nord | hol):
n.usa(X(3.15), y2, MM(0.85))                # hol → dormitor 1
n.usa(X(4.27), y2, MM(0.80))                # hol → spălătorie
n.usa(X(7.06), y2, MM(0.88))                # hol → dormitor 2
# glisanta dressingului, în peretele a1:
n.usa(a1, Y(1.30), MM(1.10), orizontal=False)
# pe peretele y3 (hol | banda de sud):
n.usa(X(3.50), y3, MM(0.90))                # hol → baie
n.usa(X(5.30), y3, MM(0.86))                # hol → WC
n.usa(X(9.00), y3, MM(0.95))                # hol → antreu
# ușa dormitorului 3, în peretele lui de est (din nișa holului):
n.usa(s1, Y(4.20), MM(0.90), orizontal=False)
# antreu → centrală: aşezată din feţele rezolvate (camerele se opresc la
# fundul porticului, mai sus decât cota măsurată brută)
_yc = Y(A["y5"] - 0.19)
n.usa(s4, _yc - MM(1.00), MM(0.85), orizontal=False)
# bucătărie → cămară:
n.usa(s6, Y(6.35), MM(0.85), orizontal=False)
# pasajul deschis hol → living (fără foaie de uşă): pe adâncimea comună
# a holului şi a livingului, cu 8 cm siguranţă la capete
_p0 = max(Y(A["y2"] + H), 0) + MM(0.08)
_p1 = min(Y(A["y3"] - H), Y(A["ky"])) - MM(0.08)
n.usa(a3, _p0, _p1 - _p0, orizontal=False, desen=False)
# bucătăria e deschisă spre living (graniţa e doar de calcul, fără perete):
n.usa(X(12.20), Y(A["ky"]), MM(2.20), desen=False)

# ─── golurile din anvelopă (scanate pe fiecare față) ────────────────────────
n.fereastra("N", X(1.60), MM(2.31))         # dormitor 1
n.usa_ext("N", X(6.68), MM(1.14))           # dormitor 2 → terasa de nord
n.fereastra("N", X(9.49), MM(2.91))         # living, vitrajul lung
n.fereastra("S", X(0.99), MM(1.72))         # dormitor 3
n.fereastra("S", X(3.39), MM(1.01))         # baie
n.fereastra("S", X(12.75), MM(2.16))        # bucătărie
n.fereastra("E", Y(1.21), MM(2.95))         # living, spre terasa de est
n.usa_ext("E", Y(5.57), MM(1.99))           # bucătărie → terasa de est
# fundul porticului: ușa de intrare + fereastra centralei (gol absolut)
n.gol_ext(X(9.03), Y5e - PE, MM(0.94), PE, usa=True)
n.gol_ext(X(7.04), Y5e - PE, MM(0.91), PE)

# ─── terasa de est e flancată de prelungirile faţadelor N şi S ──────────────
# (ca în original: cele două ziduri duc acoperişul peste terasă; spre est e gol)
TER = MM(1.51)                               # adâncimea terasei, măsurată
n.perete(IL, -PE, TER, PE)                   # prelungirea faţadei de nord
n.perete(IL, IA - PE, TER, PE)               # prelungirea faţadei de sud

# ─── terasele, punctate ─────────────────────────────────────────────────────
n.zona("Terasă acoperită", -PE, -PE - MM(2.30), MM(15.6), MM(2.30))
n.zona("Terasă", IL, 0, TER, IA - 2 * PE)
n.zona("Portic", PWm, Y5e, PE2m - PWm, IA + PE - Y5e)

# ─── mobilierul, aşezat din feţele REZOLVATE ale camerelor ──────────────────
F = {k: (X(v[0]), X(v[1]), Y(v[2]), Y(v[3])) for k, v in C.items()}

def mob(cam, fel, dx, dy, w, h):
    """dx/dy de la colţul camerei; negativ = de la faţa opusă"""
    xa, xb, ya, yb = F[cam]
    x = xa + MM(dx) if dx >= 0 else xb + MM(dx) - MM(w)
    y = ya + MM(dy) if dy >= 0 else yb + MM(dy) - MM(h)
    n.pune(fel, x, y, MM(w), MM(h))

mob("Dormitor 1", "pat", 0.25, 0.30, 1.85, 2.15)
mob("Dormitor 1", "dulap", -0.05, 0.10, 0.55, 1.60)
mob("Dressing", "dulap", 0.05, 0.05, 1.20, 0.60)
mob("Dressing", "dulap", -0.05, 0.75, 0.55, 1.00)
mob("Spălătorie", "masina", -0.05, 0.05, 0.60, 0.60)
mob("Spălătorie", "masina", -0.05, 0.68, 0.60, 0.60)
mob("Dormitor 2", "pat", 0.10, 0.85, 0.95, 2.05)
mob("Dormitor 2", "dulap", -0.05, 0.10, 0.55, 2.55)
mob("Living · dining", "masa", 1.45, 0.85, 1.15, 1.90)
mob("Living · dining", "scaune", 0.95, 0.95, 0.45, 1.70)
mob("Living · dining", "scaune", 2.65, 0.95, 0.45, 1.70)
mob("Living · dining", "canapea", -0.35, 1.60, 2.55, 0.95)
mob("Living · dining", "dulap", -0.40, 0.10, 2.30, 0.45)
mob("Dormitor 3", "pat", 0.15, -0.15, 1.65, 2.05)
mob("Dormitor 3", "dulap", 0.05, 0.15, 0.50, 1.75)
mob("Baie", "wc", 0.10, 0.45, 0.42, 0.62)
mob("Baie", "lavoar", -0.08, 0.25, 0.45, 0.55)
mob("Baie", "cada", 0.10, -0.10, 1.80, 0.78)
mob("WC", "lavoar", 0.10, 0.20, 0.50, 0.42)
mob("WC", "wc", 0.15, -0.15, 0.42, 0.62)
mob("Centrală", "raft", 0.15, 0.25, 0.90, 0.95)
mob("Antreu", "dulap", -0.08, 0.10, 0.72, 1.50)
mob("Cămară", "raft", 0.08, 0.20, 0.85, 0.50)
mob("Bucătărie", "blat", 0.05, 0.12, 2.90, 0.60)
mob("Bucătărie", "blat", 0.05, -0.08, 2.90, 0.60)
mob("Bucătărie", "plita", 0.70, -0.13, 0.60, 0.50)
mob("Bucătărie", "chiuveta", 1.80, -0.16, 0.50, 0.42)

m = Model(nume="Elva", titlu="PLAN PARTER",
          subtitlu="Casă parter tip hambar modern, 3 dormitoare · sistem Polistibrick",
          acoperis="Şarpantă clasică din lemn",
          extra=[("Gabarit", "15,48 × 8,46 m"), ("Dormitoare", "3"),
                 ("Terase", "nord + est, acoperite · portic la intrare")],
          observatii=[
              "Reproducere după proiectul 88-77: grila rezolvată pe suprafeţele",
              "scrise pe planşa originală + poziţiile pereţilor măsurate pe pixeli.",
              "Golurile (ferestre, uşi, portic) scanate numeric pe fiecare faţă.",
              "Camera centralei nu are arie pe planşa lor: 4,2 m² = diferenţa",
              "până la totalul de 100 m² utili din descrierea proiectului."])
m.nivel(n)

if __name__ == "__main__":
    print("axele rezolvate:")
    for k in sorted(A):
        print("  %-3s %7.3f  (măsurat %7.3f  %+0.0f mm)" % (k, A[k], AX0[k], (A[k]-AX0[k])*1000))
    print("\narii (scris → obţinut):")
    rau = 0.0
    for nume, (xa, xb, ya, yb) in celule(A).items():
        arie = (xb-xa)*(yb-ya)
        err = arie - ARII[nume]
        if nume not in MOI:
            rau = max(rau, abs(err))
        print("  %-16s %6.2f → %6.2f   %+0.3f" % (nume, ARII[nume], arie, err))
    print("  eroarea maximă (arii scrise): %.3f m²" % rau)
    print("util: %.1f m²" % n.util)
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr[:5]))
    plansa(m, "elva.svg")
    print("→ elva.svg")
