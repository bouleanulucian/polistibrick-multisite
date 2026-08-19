#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GALA — 55,1 m², două dormitoare.

Original Instagram, planșă 9,50 × 7,00 m:
  N  terasă 6,00 × 3,00 (est, în fața D2 + living)
     D1 10,05 | D2 9,14 | Living 20,48
     Hol 4,72 (bandă transversală)
     Baie 5,18 | Tehnic 2,34 | Vestibul 3,21 | Living (bucătărie SE)
  S  prispă 1,50 m

Holul e banda E–V sub dormitoare: fiecare cameră se deschide din el.
Pereții 38 / 13 cm lărgesc gabaritul.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

h_hol, Hs = 900, 2150
W1, Wm = 2678, 2436
Whol = W1 + PI + Wm                      # 5244
Hn = round(10.05e6 / W1)                 # 3753
Wbaie = round(5.18e6 / Hs)               # 2409
Wteh = round(2.34e6 / Hs)                # 1088
Wvest = Whol - Wbaie - PI - Wteh - PI    # 1487

xh = W1 + PI
xteh = Wbaie + PI
xvest = xteh + Wteh + PI
y_hol = Hn + PI
y_s = y_hol + h_hol + PI
IA = y_s + Hs
We = round(20.48e6 / IA)
xe = Whol + PI
IL = xe + We
L, A = IL + 2 * PE, IA + 2 * PE

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Dormitor 1", 0, 0, W1, Hn)
n.camera("Dormitor 2", xh, 0, Wm, Hn)
n.camera("Hol", 0, y_hol, Whol, h_hol)
n.camera("Living · dining · bucătărie", xe, 0, We, IA)
n.camera("Baie", 0, y_s, Wbaie, Hs)
n.camera("Tehnic", xteh, y_s, Wteh, Hs)
n.camera("Vestibul", xvest, y_s, Wvest, Hs)

for w in [
    (W1, 0, PI, Hn),
    (Whol, 0, PI, IA),
    (0, Hn, Whol, PI),
    (0, y_hol + h_hol, Whol, PI),
    (Wbaie, y_s, PI, Hs),
    (xteh + Wteh, y_s, PI, Hs),
]:
    n.perete(*w)

for t in [
    (400, Hn, 900, True),
    (xh + 400, Hn, 900, True),
    (400, y_hol + h_hol, 800, True),
    (xteh + 80, y_hol + h_hol, 800, True),
    (xvest + 200, y_hol + h_hol, 800, True),
    (Whol, y_hol, 800, False, False),
]:
    n.usa(*t)

n.gol_ext(xvest + 150, IA, 1100, PE, usa=True)
n.gol_ext(xe + 300, -PE, 2200, PE, usa=True)
n.fereastra("N", 400, 1800)
n.fereastra("N", xh + 400, 1600)
n.fereastra("V", 800, 1600)
n.fereastra("V", y_s + 500, 900)
n.fereastra("S", 400, 1000)
n.fereastra("S", xteh + 80, 800)
n.fereastra("S", xe + 400, 1400)
n.fereastra("E", 800, 1800)
n.fereastra("E", y_s + 200, 1600)

n.zona("Terasă", xh - PE, -PE - 3000, L - (xh - PE), 3000)
n.zona("Intrare", xvest - 200, IA + PE, Wvest + 800, 1500)

n.pune("pat", 200, 400, 1800, 2100)
n.pune("dulap", 200, Hn - 500, 1600, 450)
n.pune("pat", xh + 150, 350, 1400, 2000)
n.pune("dulap", xh + Wm - 550, 200, 500, 1800)
n.pune("cada", 150, y_s + Hs - 750, 1700, 700)
n.pune("lavoar", 150, y_s + 80, 600, 450)
n.pune("wc", Wbaie - 500, y_s + 200, 400, 600)
n.pune("masina", xteh + 80, y_s + 200, 600, 600)
n.pune("raft", xteh + 80, y_s + 1000, 800, 900)
n.pune("dulap", xvest + 80, y_s + 80, 500, Hs - 160)
n.pune("canapea", xe + We - 1000, 400, 900, 2200)
n.pune("masa", xe + 350, 2800, 1400, 1400)
n.pune("blat", xe + 80, IA - 700, 2200, 600)
n.pune("plita", xe + 250, IA - 650, 700, 450)
n.pune("chiuveta", xe + 1200, IA - 650, 600, 450)

m = Model(
    nume="Gala",
    titlu="PLAN PARTER",
    subtitlu="Casă parter compactă 55 m², două dormitoare · sistem Polistibrick",
    acoperis="Şarpantă în două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după un proiect de 55,1 m²: două dormitoare la nord,",
        "terasă 6,00 × 3,00 m, şarpantă clasică din lemn."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/gala.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/gala-el-%s.png" % lat)
