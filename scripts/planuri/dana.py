#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DANA — 85 m², două dormitoare, living spațios.

Original nadiyni_stiny / Db1CEYpEgi7: 10,50 × 9,50 m + terasă nord 1,50 m
pe living și terasă de intrare sud.

  N  terasă 1,50 pe living
     Living 27,50 | Hol | Dormitor 1 13,30
     Bucătărie 11,41 | Tehnic 5,41 | Baie 6,86
                     | Vestibul 3,38 | Dormitor 2 12,38
  S  terasă de intrare

Fațadă Instagram: tencuială albă + lambriu lemn orizontal, acoperiș șold.
"""
from plansa import Nivel, Model, plansa, verifica, descriere_fatada, PE, PI

Ww, Wh, We = 4950, 1400, 3650
Hliv = round(27.50e6 / Ww)               # 5556
Hbed1 = round(13.30e6 / We)
Hbaie = round(6.86e6 / We)
Hbed2 = round(12.38e6 / We)
IA = Hbed1 + PI + Hbaie + PI + Hbed2     # 9175
Hkit = IA - Hliv - PI
Wkit = round(11.41e6 / Hkit)
wteh = Ww - Wkit - PI
h_vest = round(3.38e6 / Wh)
h_hol = IA - h_vest - PI

xh, xe = Ww + PI, Ww + PI + Wh + PI
IL = xe + We
L, A = IL + 2 * PE, IA + 2 * PE

y_teh = Hliv + PI
y_baie = Hbed1 + PI
y_bed2 = y_baie + Hbaie + PI
y_vest = h_hol + PI

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Living · dining", 0, 0, Ww, Hliv)
n.camera("Hol", xh, 0, Wh, h_hol)
n.camera("Dormitor 1", xe, 0, We, Hbed1)
n.camera("Baie", xe, y_baie, We, Hbaie)
n.camera("Dormitor 2", xe, y_bed2, We, Hbed2)
n.camera("Bucătărie", 0, y_teh, Wkit, Hkit)
n.camera("Tehnic", Wkit + PI, y_teh, wteh, Hkit)
n.camera("Vestibul", xh, y_vest, Wh, h_vest)

for w in [
    (Ww, 0, PI, IA),                      # vest | hol+vestibul
    (xh + Wh, 0, PI, IA),                 # hol | dormitoare
    (0, Hliv, Ww, PI),                    # living | bucătărie+tehnic
    (xe, Hbed1, We, PI),                  # dormitor 1 | baie
    (xe, y_baie + Hbaie, We, PI),         # baie | dormitor 2
    (Wkit, y_teh, PI, Hkit),              # bucătărie | tehnic
    (xh, h_hol, Wh, PI),                  # hol | vestibul
]:
    n.perete(*w)

for t in [
    (xh + Wh, 1200, 900, False),          # hol → dormitor 1
    (xh + Wh, y_baie + 400, 800, False),  # hol → baie
    (xh + Wh, y_bed2 + 40, 750, False),   # hol → dormitor 2 (suprapunere scurtă)
    (Ww, 2000, 1400, False, False),       # hol → living
    (Ww, y_teh + 40, 750, False),         # hol → tehnic
    (xh, h_hol, 900, True),               # hol → vestibul
    (Ww, y_vest + 400, 800, False),       # vestibul → tehnic
    (400, Hliv, 1800, True, False),       # living ↔ bucătărie (deschis)
]:
    n.usa(*t)

n.gol_ext(xh + 150, IA, 1100, PE, usa=True)          # intrare sud → vestibul
n.gol_ext(800, -PE, 2800, PE, usa=True)              # living → terasa nord
n.fereastra("N", xe + 800, 1800)
n.fereastra("E", 700, 1600)
n.fereastra("E", y_baie + 400, 1000)
n.fereastra("E", y_bed2 + 800, 1600)
n.fereastra("S", 600, 1400)                          # bucătărie
n.fereastra("S", xe + 800, 1600)                     # dormitor 2
n.fereastra("V", 1500, 1800)                         # living
n.fereastra("V", y_teh + 800, 1400)                  # bucătărie

n.zona("Terasă", -PE, -PE - 1500, Ww + 2 * PE, 1500)
n.zona("Intrare", xh - 400, IA + PE, Wh + 800, 1500)

n.pune("canapea", 200, 200, 2200, 900)
n.pune("canapea", 200, 1100, 900, 1800)
n.pune("masa", 2800, 1800, 1600, 1000)
n.pune("scaune", 2850, 1400, 1500, 380)
n.pune("blat", 150, y_teh + 150, 600, 2200)
n.pune("plita", 200, y_teh + 400, 450, 700)
n.pune("chiuveta", 200, y_teh + 1400, 450, 600)
n.pune("raft", Wkit - 500, y_teh + 200, 450, 1400)
n.pune("pat", xe + We - 2100, 400, 1800, 2100)
n.pune("dulap", xe + 80, 200, 500, 2800)
n.pune("cada", xe + 200, y_baie + 80, 1700, 750)
n.pune("lavoar", xe + We - 700, y_baie + 100, 600, 450)
n.pune("wc", xe + We - 500, y_baie + Hbaie - 700, 400, 600)
n.pune("pat", xe + 250, y_bed2 + 400, 1400, 2000)
n.pune("dulap", xe + We - 550, y_bed2 + 200, 500, 2200)
n.pune("masina", Wkit + PI + 80, y_teh + 200, 600, 600)
n.pune("dulap", xh + 80, y_vest + 80, 500, h_vest - 160)

m = Model(
    nume="Dana",
    titlu="PLAN PARTER",
    subtitlu="Casă parter, două dormitoare, living spațios · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, țiglă ceramică antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după un proiect de 85 m² cu living de 27,5 m²;",
        "fațadă tencuială albă şi lambriu de lemn, terasă nord 1,50 m."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/dana.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
