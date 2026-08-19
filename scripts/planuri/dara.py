#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DARA — 61,4 m² compact, două dormitoare.

Original cotat 10,50 × 7,00 m, trei travee de 3,50 + terasă vest 3,00 × 7,00.
Pereții 38 / 13 lărgesc gabaritul. Ariile scrise rămân (holul crește
ca să atingă ambele dormitoare).

  N  Living 22,69 | Tehnic 3,05 | Baie 4,43 | D1 11,55
     Living       | Hol                     | D1 / D2
     Living       | Vest 4,17               | D2 10,78
  S  terasă vest 3,00 m, prispă pe vestibul
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

Wm = 2950
Wteh = 1150
Wbaie = Wm - PI - Wteh                   # 1670
Hnorth = round(3.05e6 / Wteh)            # 2652 — tehnic 3,05
h_hol = 2543                             # crescut pentru uși la D1 și D2
Hvest = round(4.17e6 / Wm)               # 1414
y_hol = Hnorth + PI                      # 2782
y_vest = y_hol + h_hol + PI              # 5455
IA = y_vest + Hvest                      # 6869

Wliv = round(22.69e6 / IA)               # 3303
We = round((11.55 + 10.78) * 1e6 / (IA - PI))  # 3314
Hd1 = round(11.55e6 / We)                # 3485
Hd2 = IA - PI - Hd1                      # 3254

xh = Wliv + PI
xe = xh + Wm + PI
IL = xe + We
L, A = IL + 2 * PE, IA + 2 * PE          # 10587 × 7629

y_d2 = Hd1 + PI

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Living · dining · bucătărie", 0, 0, Wliv, IA)
n.camera("Tehnic", xh, 0, Wteh, Hnorth)
n.camera("Baie", xh + Wteh + PI, 0, Wbaie, Hnorth)
n.camera("Hol", xh, y_hol, Wm, h_hol)
n.camera("Vestibul", xh, y_vest, Wm, Hvest)
n.camera("Dormitor 1", xe, 0, We, Hd1)
n.camera("Dormitor 2", xe, y_d2, We, Hd2)

for w in [
    (Wliv, 0, PI, IA),
    (xh + Wm, 0, PI, IA),
    (xh + Wteh, 0, PI, Hnorth),
    (xh, Hnorth, Wm, PI),
    (xh, y_hol + h_hol, Wm, PI),
    (xe, Hd1, We, PI),
]:
    n.perete(*w)

for t in [
    (Wliv, y_hol + 400, 1400, False, False),     # hol → living
    (xh + 80, Hnorth, 800, True),                # hol → tehnic
    (xh + Wteh + PI + 200, Hnorth, 800, True),   # hol → baie
    (xh + Wm, y_hol + 20, 600, False),           # hol → D1 (suprapunere 703 mm)
    (xh + Wm, y_d2 + 200, 900, False),           # hol → D2
    (xh + 500, y_hol + h_hol, 900, True),        # hol → vestibul
]:
    n.usa(*t)

n.usa_ext("S", xh + 600, 1100)
n.usa_ext("V", 2800, 2400)                # living → terasă
n.fereastra("N", 500, 1600)               # living / bucătărie
n.fereastra("N", xh + 150, 700)           # tehnic
n.fereastra("N", xh + Wteh + PI + 300, 900)  # baie
n.fereastra("N", xe + 700, 1600)          # D1
n.fereastra("E", 600, 1600)               # D1
n.fereastra("E", y_d2 + 700, 1600)        # D2
n.fereastra("S", 400, 1400)               # living sud
n.fereastra("S", xe + 700, 1600)          # D2
n.fereastra("V", 500, 1400)               # living nord-vest
n.fereastra("V", 4800, 1400)              # living sud-vest

n.zona("Terasă", -PE - 3000, -PE, 3000, A)
n.zona("Prispă", xh - 200, IA + PE, Wm + 400, 1800)

n.pune("blat", 80, 80, 2200, 600)
n.pune("plita", 300, 150, 700, 450)
n.pune("chiuveta", 1200, 150, 600, 450)
n.pune("masa", 400, 1600, 1400, 900)
n.pune("canapea", 200, IA - 2200, 900, 2000)
n.pune("masina", xh + 80, 80, 600, 600)
n.pune("raft", xh + 80, 900, 500, 1400)
n.pune("cada", xh + Wteh + PI + 80, 80, Wbaie - 160, 700)
n.pune("lavoar", xh + Wteh + PI + 80, Hnorth - 480, 550, 400)
n.pune("wc", xh + Wteh + PI + Wbaie - 500, Hnorth - 700, 400, 600)
n.pune("pat", xe + We - 2000, 350, 1800, 2100)
n.pune("dulap", xe + 80, Hd1 - 500, We - 160, 450)
n.pune("pat1", xe + 200, y_d2 + Hd2 - 2200, 1400, 2000)
n.pune("dulap", xe + 80, y_d2 + 80, 500, 2000)
n.pune("dulap", xh + Wm - 550, y_vest + 80, 450, Hvest - 160)

m = Model(
    nume="Dara",
    titlu="PLAN PARTER",
    subtitlu="Casă parter compactă 61 m², două dormitoare · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după un proiect compact de 61,4 m² pe trei travee,",
        "terasă vest 3,00 m în afara anvelopei, şarpantă de lemn."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/dara.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/dara-el-%s.png" % lat)
