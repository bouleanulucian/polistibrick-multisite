#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PURA — reprodusă din proiectul de referinţă Domkamen 89-10 (17,15 × 15,05 m,
137 m² cu garaj dublu).

Casă parter în L: garaj dublu ieşit pe sud-vest, terasă de lemn pe nord şi est
(în afara anvelopei). Aripa de noapte pe vest, hol orizontal central, zona de
zi deschisă pe est (bucătărie cu ostrov · dining · living) vitrată spre terasă.

PE = 380 · PI = 130. Coordonatele sunt INTERIOARE.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

# ── anvelopă + garaj; terasa N/E în afară (gabarit cotat 17,15 × 15,05) ──────
IL, Hm, Hgi = 12600, 6750, 4050

Ww = 3400                                   # matrimonial / birou
Wteh = 1400                                 # tehnic (lângă garaj, din hol)
Wbaie = 1650                                # baie cu cadă
Wbaie2 = 1300                               # baie oaspeţi cu duş (lângă antreu)
Wb = Wteh + PI + Wbaie + PI + Wbaie2        # 4530 — sub dormitor 2
Wl = IL - Ww - PI - Wb - PI                 # 4310
x_b = Ww + PI                               # 3430 — începutul benzii D2/băi
x_teh = x_b
x_ba = x_teh + Wteh + PI                    # 4960
x_b2 = x_ba + Wbaie + PI                    # 6790
x_liv = x_b + Wb + PI                       # 8090
Wgi = x_liv - PI                            # 7960

L = IL + 2 * PE                             # 13160
A = Hm + PI + Hgi + 2 * PE                  # 12590
IA = A - 2 * PE
y_gar = Hm + PI

CONTUR = [(-PE, -PE),
          (IL + PE, -PE),
          (IL + PE, Hm + PE),
          (Wgi + PE, Hm + PE),
          (Wgi + PE, IA + PE),
          (-PE, IA + PE)]

Hn, Hh = 3000, 1100
Hs = Hm - Hn - Hh - 2 * PI                  # 2440
y_h = Hn + PI
y_s = y_h + Hh + PI
Hant, Want = 1900, 2000

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

n.camera("Dormitor matrimonial", 0, 0, Ww, Hn)
n.camera("Dormitor 2", x_b, 0, Wb, Hn)
n.camera("Hol", 0, y_h, Ww + PI + Wb, Hh)
n.camera("Birou", 0, y_s, Ww, Hs)
n.camera("Tehnic", x_teh, y_s, Wteh, Hs)
n.camera("Baie", x_ba, y_s, Wbaie, Hs)
n.camera("Baie 2", x_b2, y_s, Wbaie2, Hs)
n.camera("Antreu", x_liv, Hm - Hant, Want, Hant)
n.camera("Living · dining · bucătărie", x_liv, 0, Wl, Hm - Hant)
n.camera("Living sud", x_liv + Want + PI, Hm - Hant,
         Wl - Want - PI, Hant)
n.camera("Garaj dublu", 0, y_gar, Wgi, Hgi)

for w in [
    (Ww, 0, PI, Hn),
    (x_b + Wb, 0, PI, Hn),
    (0, Hn, Ww + PI + Wb, PI),
    (0, y_h + Hh, Ww + PI + Wb, PI),
    (Ww, y_s, PI, Hs),
    (x_teh + Wteh, y_s, PI, Hs),
    (x_ba + Wbaie, y_s, PI, Hs),
    (x_b + Wb, y_h, PI, Hh + PI + Hs),
    (x_liv, Hm - Hant - PI, Want, PI),
    (x_liv + Want, Hm - Hant, PI, Hant),
    (0, Hm, Wgi, PI),
]:
    n.perete(*w)

for t in [
    (800, Hn, 900, True),                       # hol → master
    (x_b + 1000, Hn, 900, True),                # hol → D2
    (800, y_h + Hh, 900, True),                 # hol → birou
    (x_teh + 250, y_h + Hh, 800, True),         # hol → tehnic
    (x_ba + 350, y_h + Hh, 800, True),          # hol → baie
    (x_b2 + 200, y_h + Hh, 800, True),          # hol → baie 2
    (x_b + Wb, y_h + 150, Hh - 300, False, False),
    (x_liv + 350, Hm - Hant - PI, 900, True),   # living → antreu
    (x_liv + Want, Hm - Hant + 400, 900, False, False),
    (x_liv + Want + PI + 200, Hm - Hant - PI, 1400, True, False),
    (x_teh + 250, Hm, 800, True),               # tehnic → garaj
]:
    n.usa(*t)

n.gol_ext(x_liv + 400, Hm + PE, 1100, PE, usa=True)
n.gol_ext(1600, IA + PE, 2800, PE)

n.fereastra("N", 500, 1800)
n.fereastra("N", x_b + 800, 2000)
n.gol_ext(x_liv + 500, -PE, 2200, PE, usa=True)
n.gol_ext(IL, 500, PE, 2400, usa=True)
n.gol_ext(IL, Hm - Hant - 1500, PE, 1200, usa=True)
n.fereastra("V", 600, 1400)
n.fereastra("V", y_s + 400, 1400)

n.zona("Terasă", -PE, -PE - 2200, IL + 2 * PE + 3600, 2200)
n.zona("Terasă", IL + PE, -PE, 3600, Hm + 2 * PE)
n.zona("Intrare", Wgi + PE, Hm + PE, IL - Wgi + 200, 1500)

n.pune("pat", 400, 400, 2000, 1800).pune("dulap", 2600, 200, 600, 2200)
n.pune("pat1", x_b + 400, 300, 1100, 2000)
n.pune("dulap", x_b + Wb - 700, 200, 600, 2200)
n.pune("birou", x_b + 400, 2400, 1600, 500)
n.pune("pat1", 300, y_s + 200, 1100, 2000)
n.pune("dulap", 2500, y_s + 150, 600, 1800)
n.pune("birou", 300, y_s + 1800, 1500, 500)
n.pune("masina", x_teh + 200, y_s + 300, 600, 600)
n.pune("masina", x_teh + 200, y_s + 1200, 600, 600)
n.pune("cada", x_ba + 50, y_s + Hs - 750, 1600, 700)
n.pune("lavoar", x_ba + 50, y_s + 120, 600, 400)
n.pune("wc", x_ba + 1100, y_s + 120, 400, 600)
n.pune("dus", x_b2 + 150, y_s + 200, 900, 900)
n.pune("lavoar", x_b2 + 150, y_s + 1300, 500, 400)
n.pune("wc", x_b2 + 700, y_s + 1300, 400, 600)
n.pune("dulap", x_liv + 60, Hm - Hant + 80, 600, 1600)
n.pune("masa", x_liv + 400, 600, 1900, 1050)
n.pune("scaune", x_liv + 450, 200, 1800, 400)
n.pune("scaune", x_liv + 450, 1700, 1800, 400)
n.pune("canapea", x_liv + 2800, 400, 900, 2400)
n.pune("canapea", x_liv + 2900, 2200, 2200, 900)
n.pune("masuta", x_liv + 3200, 1400, 800, 600)
n.pune("tv", IL - 280, 800, 250, 1500)
n.pune("insula", x_liv + 600, Hm - Hant - 1500, 1500, 900)
n.pune("plita", x_liv + 900, Hm - Hant - 1350, 700, 450)
n.pune("scaune", x_liv + 2200, Hm - Hant - 1400, 400, 1100)
n.pune("blat", x_liv + Want + PI + 80, Hm - 650, Wl - Want - PI - 160, 550)
n.pune("chiuveta", x_liv + Want + PI + 300, Hm - 550, 600, 450)

m = Model(
    nume="Petra",
    titlu="PLAN PARTER",
    subtitlu="Casă parter în L, trei dormitoare, garaj dublu şi terasă · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape",
    extra=[("Gabarit", "17,15 × 15,05 m"),
           ("Dormitoare", "2 + birou"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după proiectul de referinţă Domkamen 89-10, cotat 17,15 × 15,05 m,",
        "137 m² cu garaj dublu. Terasă pe nord şi est, în afara anvelopei de 38 cm."])
m.nivel(n)

if __name__ == "__main__":
    import os
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    os.makedirs("/tmp/planuri", exist_ok=True)
    plansa(m, "/tmp/planuri/pura.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    print("gabarit anvelopă %.2f × %.2f m" % (L / 1000, A / 1000))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
