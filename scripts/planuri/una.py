#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNA — 63 m², două dormitoare.

Original cotat 10,00 × 7,50 m + terasă vest 3,00 × 7,50,
prispă sud 3,50 × 1,80. Pereții 38 / 13 lărgesc gabaritul.

  N  Living 24,50 | Baie 5,11 | D1 13,30
     Living       | Hol  5,71 | D1
     Living (buc.)| Vest 4,17 | D2 11,06
  S  terasă V 3,00 m pe toată adâncimea, prispă pe vestibul
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

IA = 6800
Wliv = round(24.50e6 / IA)               # 3603
We = round((13.30 + 11.06) * 1e6 / (IA - PI))  # 3652
Hd1 = round(13.30e6 / We)                # 3642
Hd2 = IA - PI - Hd1                      # 3028
Wm = round((5.11 + 5.71 + 4.17) * 1e6 / (IA - 2 * PI))  # 2292
Hbaie = round(5.11e6 / Wm)               # 2229
Hhol = round(5.71e6 / Wm)                # 2491
Hvest = IA - 2 * PI - Hbaie - Hhol       # 1820

xh = Wliv + PI
xe = xh + Wm + PI
IL = xe + We
L, A = IL + 2 * PE, IA + 2 * PE          # 10567 × 7560

y_hol = Hbaie + PI
y_vest = y_hol + Hhol + PI
y_d2 = Hd1 + PI

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Living · dining · bucătărie", 0, 0, Wliv, IA)
n.camera("Baie", xh, 0, Wm, Hbaie)
n.camera("Hol", xh, y_hol, Wm, Hhol)
n.camera("Vestibul", xh, y_vest, Wm, Hvest)
n.camera("Dormitor 1", xe, 0, We, Hd1)
n.camera("Dormitor 2", xe, y_d2, We, Hd2)

for w in [
    (Wliv, 0, PI, IA),                    # living | mijloc
    (xh + Wm, 0, PI, IA),                 # mijloc | dormitoare
    (xh, Hbaie, Wm, PI),                  # baie | hol
    (xh, y_hol + Hhol, Wm, PI),           # hol | vestibul
    (xe, Hd1, We, PI),                    # D1 | D2
]:
    n.perete(*w)

for t in [
    (Wliv, y_hol + 400, 1400, False, False),  # hol → living
    (xh + 400, Hbaie, 800, True),             # hol → baie
    (xh + Wm, y_hol + 200, 900, False),       # hol → D1
    (xh + Wm, y_d2 + 80, 900, False),         # hol → D2
    (xh + 400, y_hol + Hhol, 900, True),      # hol → vestibul
]:
    n.usa(*t)

n.usa_ext("S", xh + 350, 1100)
n.usa_ext("V", 1800, 2400)                # living → terasa de vest
n.fereastra("N", 600, 1800)               # living
n.fereastra("N", xh + 500, 900)           # baie
n.fereastra("N", xe + 800, 1600)          # D1 nord
n.fereastra("E", 700, 1800)               # D1
n.fereastra("E", y_d2 + 700, 1600)        # D2
n.fereastra("S", 500, 1400)               # bucătărie
n.fereastra("S", xe + 700, 1600)          # D2 sud
n.fereastra("V", 400, 1400)               # living nord-vest
n.fereastra("V", 4200, 1400)              # living sud-vest

n.zona("Terasă", -PE - 3000, -PE, 3000, A)
n.zona("Prispă", xh - 600, IA + PE, 3500, 1800)

n.pune("canapea", 200, 200, 2200, 900)
n.pune("masa", 400, 2200, 1400, 1000)
n.pune("blat", 80, IA - 700, 2400, 600)
n.pune("chiuveta", 900, IA - 650, 600, 450)
n.pune("plita", Wliv - 750, IA - 2000, 600, 700)
n.pune("cada", xh + 250, 80, 1700, 700)
n.pune("lavoar", xh + 80, Hbaie - 480, 550, 400)
n.pune("wc", xh + Wm - 500, Hbaie - 700, 400, 600)
n.pune("pat", xe + We - 2000, 400, 1800, 2100)
n.pune("dulap", xe + 80, Hd1 - 500, 2200, 450)
n.pune("pat1", xe + We - 1600, y_d2 + Hd2 - 2200, 1400, 2000)
n.pune("dulap", xe + 80, y_d2 + 80, 2000, 450)
n.pune("masa", xe + 80, y_d2 + 900, 700, 1200)
n.pune("dulap", xh + Wm - 550, y_vest + 80, 450, Hvest - 160)

m = Model(
    nume="Una",
    titlu="PLAN PARTER",
    subtitlu="Casă parter 63 m², două dormitoare · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după un proiect de 63 m²: living 24,50, două dormitoare,",
        "terasă vest 3,00 m în afara anvelopei, prispă sud 1,80 m."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/una.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/una-el-%s.png" % lat)
