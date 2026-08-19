#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ELDA — 119,3 m², familie, trei dormitoare.

Original Instagram: 14,50 = 5,00 + 9,50 m, adâncime stânga 11,50 m.
Living stânga 36,18 + bucătărie 8,91 + cămară 3,80.
Dreapta: vest 4,24 · hol 10,49 · D1 10,79 · D2 10,79 · master 12,65
         dressing 5,26 · baie 5,99 · baie2 5,15 · rufe 5,08.
Terasă spate ~9,50 × 3,00 m pe stâlpi, în afara anvelopei (contur în L).
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

Wl, Wr = 4435, 9174
Hter = 3000                                 # livingul iese 3,00 m nord de aripa de noapte
Hn, Hc, Hs = 3840, 1143, 2972
Wd, Wm = 2810, 3294
Hs_l, Hliv = 2952, 8158

xh = Wl + PI
x2 = xh + Wd + PI
xe = x2 + Wd + PI
IL = xe + Wm                                # 13739
IA = Hliv + PI + Hs_l                       # 11240 — se aliniază pe living
# forțăm IA din living; aripa dreaptă începe sub terasă
y_bed = Hter
y_hol = y_bed + Hn + PI
y_s = y_hol + Hc + PI
# Hs se potrivește în restul până la IA
Hs = IA - y_s
IAr_check = IA - Hter

Wv = round(4.24e6 / Hs)
Wla = round(5.08e6 / Hs)
Wb2 = round(5.15e6 / Hs)
Wens = round(5.99e6 / Hs)
Wdres = IL - xh - Wv - PI - Wla - PI - Wb2 - PI - Wens - PI

x_la = xh + Wv + PI
x_b2 = x_la + Wla + PI
x_dr = x_b2 + Wb2 + PI
x_en = x_dr + Wdres + PI

L, A = IL + 2 * PE, IA + 2 * PE

# contur L: livingul nord-vest, terasa scobită nord-est (în AFARA anvelopei)
n = Nivel("PARTER", L, A)
n.poligon([
    (-PE, -PE),
    (xh - PI, -PE),                         # colțul NE al livingului
    (xh - PI, y_bed - PE),                  # coboară la terasă
    (IL + PE, y_bed - PE),
    (IL + PE, IA + PE),
    (-PE, IA + PE),
])

Wp = round(3.80e6 / Hs_l)
Wkit = Wl - PI - Wp
y_kit = Hliv + PI

n.camera("Living · dining", 0, 0, Wl, Hliv)
n.camera("Cămară", 0, y_kit, Wp, Hs_l)
n.camera("Bucătărie", Wp + PI, y_kit, Wkit, Hs_l)
n.camera("Dormitor 1", xh, y_bed, Wd, Hn)
n.camera("Dormitor 2", x2, y_bed, Wd, Hn)
n.camera("Dormitor matrimonial", xe, y_bed, Wm, Hn)
n.camera("Hol", xh, y_hol, Wr, Hc)
n.camera("Vestibul", xh, y_s, Wv, Hs)
n.camera("Spălătorie", x_la, y_s, Wla, Hs)
n.camera("Baie 2", x_b2, y_s, Wb2, Hs)
n.camera("Dressing", x_dr, y_s, Wdres, Hs)
n.camera("Baie", x_en, y_s, Wens, Hs)

for w in [
    (Wl, 0, PI, IA),                         # living | noapte (pe toată adâncimea stângă)
    (0, Hliv, Wl, PI),                       # living | cămară+bucătărie
    (Wp, y_kit, PI, Hs_l),                   # cămară | bucătărie
    (xh + Wd, y_bed, PI, Hn),                # D1 | D2
    (x2 + Wd, y_bed, PI, Hn),                # D2 | master
    (xh, y_bed + Hn, Wr, PI),                # dormitoare | hol
    (xh, y_hol + Hc, Wr, PI),                # hol | sud
    (xh + Wv, y_s, PI, Hs),
    (x_la + Wla, y_s, PI, Hs),
    (x_b2 + Wb2, y_s, PI, Hs),
    (x_dr + Wdres, y_s, PI, Hs),
]:
    n.perete(*w)

for t in [
    (xh + 400, y_bed + Hn, 900, True),       # hol → D1
    (x2 + 400, y_bed + Hn, 900, True),       # hol → D2
    (xe + 600, y_bed + Hn, 900, True),       # hol → master
    (xh + 200, y_hol + Hc, 800, True),       # hol → vestibul
    (x_la + 200, y_hol + Hc, 800, True),     # hol → rufe
    (x_b2 + 200, y_hol + Hc, 800, True),     # hol → baie 2
    (x_dr + 200, y_hol + Hc, 800, True),     # hol → dressing
    (x_en + 200, y_hol + Hc, 800, True),     # hol → baie
    (x_dr + Wdres, y_s + 400, 800, False),   # dressing → baie
    (Wl, y_hol + 80, min(1000, Hc - 160), False, False),  # hol → living
    (Wp + PI + 200, Hliv, 1600, True, False),  # living ↔ bucătărie
    (Wp, y_kit + 400, 800, False),           # bucătărie → cămară
]:
    n.usa(*t)

n.usa_ext("S", xh + 150, 1100)
n.gol_ext(xh + 150, IA, 1100, PE, usa=True)
n.usa_ext("N", 500, 2400)                    # living → terasă (nordul livingului)
n.gol_ext(500, -PE, 2400, PE, usa=True)
n.gol_ext(Wl, 400, PE, 1800, usa=True)       # living → terasă est
n.fereastra("V", 2200, 1800)                 # living vest
n.fereastra("V", y_kit + 800, 1400)          # bucătărie
n.fereastra("S", Wp + PI + 400, 1400)        # bucătărie sud
n.fereastra("S", x_la + 300, 900)            # rufe
n.fereastra("S", x_b2 + 300, 900)            # baie 2
n.fereastra("E", y_s + 600, 1100)            # baie master
# ferestrele dormitoarelor stau pe fața de nord a aripii (y_bed), nu pe y=0
n.gol_ext(xh + 500, y_bed - PE, 1600, PE)
n.gol_ext(x2 + 500, y_bed - PE, 1600, PE)
n.gol_ext(xe + 700, y_bed - PE, 1800, PE)

n.zona("Terasă", xh - PI, -PE - 0, Wr + PI + PE + 800, y_bed)
n.zona("Intrare", xh - 200, IA + PE, Wv + 800, 800)

n.pune("canapea", 200, 2500, 2200, 900)
n.pune("masa", 400, 400, 2200, 1100)
n.pune("blat", 80, y_kit + 80, Wkit + Wp - 80, 600)
n.pune("chiuveta", Wp + PI + 200, y_kit + 140, 600, 450)
n.pune("plita", Wp + PI + 1100, y_kit + 140, 700, 450)
n.pune("raft", 80, y_kit + 700, 500, 1800)
n.pune("pat1", xh + 200, y_bed + 400, 1400, 2000)
n.pune("dulap", xh + 200, y_bed + Hn - 500, 1800, 450)
n.pune("pat1", x2 + 200, y_bed + 400, 1400, 2000)
n.pune("dulap", x2 + 200, y_bed + Hn - 500, 1800, 450)
n.pune("pat", xe + 400, y_bed + 400, 1800, 2100)
n.pune("dulap", x_dr + 80, y_s + 80, Wdres - 160, 550)
n.pune("cada", x_en + 80, y_s + Hs - 750, 1700, 700)
n.pune("lavoar", x_en + 80, y_s + 80, 600, 450)
n.pune("wc", x_en + Wens - 500, y_s + 200, 400, 600)
n.pune("dus", x_b2 + 80, y_s + Hs - 900, 900, 850)
n.pune("lavoar", x_b2 + 80, y_s + 80, 600, 450)
n.pune("wc", x_b2 + Wb2 - 500, y_s + 200, 400, 600)
n.pune("masina", x_la + 80, y_s + 80, 600, 600)
n.pune("dulap", xh + 80, y_s + 80, 500, Hs - 160)

m = Model(
    nume="Elda",
    titlu="PLAN PARTER",
    subtitlu="Casă parter 119 m², trei dormitoare, terasă pe stâlpi · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "3"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după un proiect de 119,3 m²: living vest 36,18 m²,",
        "terasă nord 9,50 × 3,00 m pe stâlpi, în afara anvelopei."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/elda.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    print("IA living %.0f  Hs sud %.0f  Wens %.0f" % (IA, Hs, Wens))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/elda-el-%s.png" % lat)
