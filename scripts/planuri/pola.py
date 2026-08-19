#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POLA — 70,7 m², două dormitoare.

Original cotat 11,50 × 7,50 m, trei travee 4,50 | 2,50 | 4,50.
Terasă nord 3,00 m pe traveea de vest. Prispă sud 0,80 m pe vestibul.
Serviciile (21 m²) nu încap în traveea de 2,50 — se lărgește mijlocul.
Holul e bandă plină între baie și vest/tehnic, ca să deschidă D1, D2 și livingul
fără să treci prin altă cameră.

  N  Living 27,93 | Baie 5,75 | D1 10,27
     Living       | Hol       | D1 / D2
     Living (buc.)| Tehnic | Vest | D2 11,20
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

Wm = 3700
Hbaie = round(5.75e6 / Wm)               # 1554
h_hol = 2620                             # crescut ca holul să atingă D1 şi D2
Hsouth = 2950
Wteh = round(4.34e6 / Hsouth)            # 1471
Wvest = Wm - PI - Wteh                   # 2099
y_hol = Hbaie + PI                       # 1684
y_so = y_hol + h_hol + PI                # 4434
IA = y_so + Hsouth                       # 7384

Wliv = round(27.93e6 / IA)               # 3783
We = round((10.27 + 11.20) * 1e6 / (IA - PI))  # 2960
Hd1 = round(10.27e6 / We)                # 3470
Hd2 = IA - PI - Hd1                      # 3784

xh = Wliv + PI
xe = xh + Wm + PI
IL = xe + We
L, A = IL + 2 * PE, IA + 2 * PE          # 11463 × 8144

y_d2 = Hd1 + PI

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Living · dining · bucătărie", 0, 0, Wliv, IA)
n.camera("Baie", xh, 0, Wm, Hbaie)
n.camera("Hol", xh, y_hol, Wm, h_hol)
n.camera("Tehnic", xh, y_so, Wteh, Hsouth)
n.camera("Vestibul", xh + Wteh + PI, y_so, Wvest, Hsouth)
n.camera("Dormitor 1", xe, 0, We, Hd1)
n.camera("Dormitor 2", xe, y_d2, We, Hd2)

for w in [
    (Wliv, 0, PI, IA),
    (xh + Wm, 0, PI, IA),
    (xh, Hbaie, Wm, PI),
    (xh, y_hol + h_hol, Wm, PI),
    (xh + Wteh, y_so, PI, Hsouth),
    (xe, Hd1, We, PI),
]:
    n.perete(*w)

for t in [
    (Wliv, y_hol + 400, 1400, False, False),          # hol → living
    (xh + 800, Hbaie, 900, True),                     # hol → baie
    (xh + Wm, y_hol + 200, 900, False),               # hol → D1
    (xh + Wm, y_d2 + 40, 650, False),                 # hol → D2
    (xh + 80, y_hol + h_hol, 800, True),              # hol → tehnic
    (xh + Wteh + PI + 200, y_hol + h_hol, 900, True), # hol → vestibul
]:
    n.usa(*t)

n.usa_ext("N", 500, 2400)
n.usa_ext("S", xh + Wteh + PI + 250, 1100)
n.fereastra("N", xh + 1200, 900)
n.fereastra("N", xe + 600, 1400)
n.fereastra("E", 600, 1600)
n.fereastra("E", y_d2 + 800, 1800)
n.fereastra("S", 400, 1400)
n.fereastra("S", xh + 200, 800)           # tehnic
n.fereastra("S", xe + 500, 1600)
n.fereastra("V", 800, 1600)
n.fereastra("V", 3200, 1600)
n.fereastra("V", 5600, 1400)

n.zona("Terasă", -PE, -PE - 3000, Wliv + 2 * PE, 3000)
n.zona("Prispă", xh + Wteh, IA + PE, Wvest + 2 * PE, 800)

n.pune("canapea", 200, 200, 900, 2200)
n.pune("masa", 1400, 2800, 1600, 1600)
n.pune("blat", 80, IA - 700, 2600, 600)
n.pune("plita", 400, IA - 650, 700, 450)
n.pune("chiuveta", 1400, IA - 650, 600, 450)
n.pune("dus", xh + 80, 80, 900, 900)
n.pune("lavoar", xh + 1200, 80, 600, 450)
n.pune("wc", xh + Wm - 500, 200, 400, 600)
n.pune("pat1", xe + 200, 400, 1400, 2000)
n.pune("dulap", xe + 80, Hd1 - 500, We - 160, 450)
n.pune("pat", xe + We - 2000, y_d2 + 400, 1800, 2100)
n.pune("dulap", xe + 80, y_d2 + 80, 500, 2200)
n.pune("masina", xh + 80, y_so + 80, 600, 600)
n.pune("raft", xh + 80, y_so + 900, 800, 1400)
n.pune("dulap", xh + Wteh + PI + Wvest - 550, y_so + 80, 450, Hsouth - 160)

m = Model(
    nume="Pola",
    titlu="PLAN PARTER",
    subtitlu="Casă parter 70,7 m², două dormitoare · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, țiglă ceramică antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după un proiect de 70,7 m²: living 27,93 pe vest,",
        "terasă nord 3,00 m pe living, prispă sud 0,80 m pe vestibul."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/pola.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/pola-el-%s.png" % lat)
