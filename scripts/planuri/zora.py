#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ZORA — 114 m², casă cu etaj, terasă L la etaj.

PARTER (ref/zora/691330640.jpg): 9,50 = 5,50 | 4,00, corp 8,50 + terasă S 1,50.
  D 10,56 · baie 4,68 · rufe 4,68 · hol 14,35 · vest 4,32
  living 19,77 · bucătărie 6,43 · tehnic 4,74. Scară sus-centru.

ETAJ (ref/zora/691482229.jpg): anvelopă 6,60 = 2,60 | 4,00, terasă V 2,90.
  hol 9,07 · baie 4,32 · D 14,09 · D 17,27.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

We = 3620
Wd = 2800
Wh = 2540
IL = Wd + PI + Wh + PI + We              # 9220
L = IL + 2 * PE                          # 9980

Hd = round(10.56e6 / Wd)                 # 3771
Hb = round(4.68e6 / Wd)                  # 1671
Hu = round(4.68e6 / Wd)                  # 1671
Hk = round(6.43e6 / We)                  # 1776
Hvest = round(4.32e6 / Wh)               # 1701
Hteh = round(4.74e6 / Wh)                # 1866
IA = Hd + PI + Hb + PI + Hu              # 7374
A = IA + 2 * PE
H_ter = 1500

xh = Wd + PI
xe = xh + Wh + PI
y_baie = Hd + PI
y_u = y_baie + Hb + PI
y_liv = Hk + PI
y_vest = IA - Hvest

# tehnic nord în coloana holului; holul sub el până la vest
# dacă Hteh + hol + vest > IA, tehnicul stă lângă bucătărie (est, sub kit)


# ═══ PARTER ═════════════════════════════════════════════════════════════════
p = Nivel("PARTER", L, A)
p.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

p.camera("Dormitor", 0, 0, Wd, Hd)
p.camera("Baie", 0, y_baie, Wd, Hb)
p.camera("Rufe", 0, y_u, Wd, Hu)
p.camera("Tehnic", xh, 0, Wh, Hteh)
p.camera("Hol", xh, Hteh + PI, Wh, y_vest - Hteh - PI)
p.camera("Vestibul", xh, y_vest, Wh, Hvest)
p.camera("Bucătărie", xe, 0, We, Hk)
p.camera("Living · dining", xe, y_liv, We, IA - y_liv)

for w in [
    (Wd, 0, PI, IA),
    (xh + Wh, 0, PI, IA),
    (0, Hd, Wd, PI),
    (0, y_baie + Hb, Wd, PI),
    (xh, Hteh, Wh, PI),
    (xh, y_vest - PI, Wh, PI),
    (xe, Hk, We, PI),
]:
    p.perete(*w)

# hol y = Hteh+PI .. y_vest-PI. Trebuie să atingă D, baie, rufe, vest, living, tehnic
p.usa(Wd, Hd - 950, 800, False)                                  # hol → D (dacă holul ajunge în Hd)
p.usa(Wd, y_baie + 400, 800, False)
p.usa(Wd, y_u + 400, 800, False)                                 # rufe → vest / hol
p.usa(xh + 200, Hteh, 800, True)                                 # hol → tehnic
p.usa(xh + 200, y_vest - PI, 900, True)                          # hol → vest
p.usa(xh + Wh, y_liv + 600, 1400, False, False)                  # hol ↔ living
p.usa(xe + 500, Hk, 1400, True, False)                           # living ↔ bucătărie
p.usa(xh + 80, Hteh + PI + 80, 900, False)                       # hol → scară

p.usa_ext("S", xh + 300, 1100)
p.gol_ext(xh + 300, IA, 1100, PE, usa=True)
p.gol_ext(xe + 500, IA, 2000, PE, usa=True)
p.fereastra("N", 600, 1600)
p.fereastra("N", xe + 800, 1600)
p.fereastra("V", y_baie + 300, 900)
p.fereastra("V", y_u + 400, 900)
p.fereastra("E", 400, 1100)
p.fereastra("E", y_liv + 800, 1800)
p.fereastra("E", y_liv + 3200, 1400)

p.zona("Scară", xh + 80, Hteh + PI + 80, Wh - 160,
       min(2200, y_vest - Hteh - PI - 160))
p.zona("Terasă", -PE, IA + PE, L, H_ter)

p.pune("pat1", 200, 300, 1400, 2000)
p.pune("dulap", Wd - 550, 200, 500, 2200)
p.pune("cada", 80, y_baie + 80, 1700, 700)
p.pune("lavoar", 80, y_baie + Hb - 480, 550, 400)
p.pune("wc", Wd - 500, y_baie + 200, 400, 600)
p.pune("dulap", 80, y_u + 80, Wd - 160, 500)
p.pune("masina", 80, y_u + Hu - 700, 600, 600)
p.pune("blat", xe + 80, 80, We - 160, 600)
p.pune("chiuveta", xe + 400, 150, 600, 450)
p.pune("plita", xe + 1400, 150, 700, 450)
p.pune("canapea", xe + We - 950, y_liv + 800, 850, 2200)
p.pune("masa", xe + 400, y_liv + 400, 1600, 1600)
p.pune("dulap", xh + 80, y_vest + 80, Wh - 160, 450)


# ═══ ETAJ ═══════════════════════════════════════════════════════════════════
Wh_e = 2220
We_e = 3620
IL_e = Wh_e + PI + We_e
L_e = IL_e + 2 * PE
Hn_e = round(14.09e6 / We_e)
Hs_e = round(17.27e6 / We_e)
IA_e = Hn_e + PI + Hs_e
A_e = IA_e + 2 * PE
xe_e = Wh_e + PI

Hb_e = round(4.32e6 / Wh_e)
Hhol_e = round(9.07e6 / Wh_e)
Hst_e = max(1600, IA_e - Hhol_e - PI - Hb_e)
if Hst_e + PI + Hhol_e + PI + Hb_e > IA_e:
    Hst_e = 1800
    Hhol_e = IA_e - Hst_e - PI - Hb_e
y_hol_e = Hst_e + PI
y_baie_e = IA_e - Hb_e

e = Nivel("ETAJ", L_e, A_e)
e.poligon([(-PE, -PE), (IL_e + PE, -PE), (IL_e + PE, IA_e + PE), (-PE, IA_e + PE)])

e.camera("Hol", 0, y_hol_e, Wh_e, y_baie_e - PI - y_hol_e)
e.camera("Baie", 0, y_baie_e, Wh_e, Hb_e)
e.camera("Dormitor 1", xe_e, 0, We_e, Hn_e)
e.camera("Dormitor 2", xe_e, Hn_e + PI, We_e, Hs_e)

for w in [
    (Wh_e, 0, PI, IA_e),
    (0, y_hol_e - PI, Wh_e, PI),
    (0, y_baie_e - PI, Wh_e, PI),
    (xe_e, Hn_e, We_e, PI),
]:
    e.perete(*w)

# hol trebuie să atingă ambele dormitoare: y_hol_e .. y_baie_e
e.usa(Wh_e, max(y_hol_e, 0) + 200, 800, False)                   # hol → D1
e.usa(Wh_e, Hn_e + PI + 400, 800, False)                         # hol → D2
e.usa(300, y_baie_e - PI, 800, True)                             # hol → baie
e.usa(200, y_hol_e - PI, 900, True)                              # hol → scară

e.fereastra("N", xe_e + 800, 1800)
e.fereastra("E", 800, 1800)
e.fereastra("E", Hn_e + PI + 1000, 1800)
e.fereastra("S", xe_e + 800, 1800)
e.fereastra("S", 400, 900)
e.fereastra("V", y_hol_e + 400, 1100)

e.zona("Scară", 80, 80, Wh_e - 160, y_hol_e - PI - 80)
e.zona("Terasă", -PE - 2900, -PE, 2900, A_e)
e.zona("Terasă", -PE, IA_e + PE, Wh_e + PE, 1500)

e.pune("pat", xe_e + 400, 400, 2100, 1800)
e.pune("dulap", xe_e + 200, Hn_e - 500, We_e - 400, 450)
e.pune("pat", xe_e + 400, Hn_e + PI + 400, 2100, 1800)
e.pune("dulap", xe_e + 200, IA_e - 550, We_e - 400, 500)
e.pune("cada", 80, y_baie_e + 80, min(1700, Wh_e - 160), 700)
e.pune("lavoar", 80, y_baie_e + Hb_e - 480, 550, 400)
e.pune("wc", Wh_e - 500, y_baie_e + 200, 400, 600)


m = Model(
    nume="Zora",
    titlu="PLAN PARTER + ETAJ",
    subtitlu="Casă cu etaj, 114 m², terasă L la etaj · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, patru ape, țiglă ceramică antracit",
    extra=[("Gabarit parter", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Gabarit etaj", "%.2f × %.2f m" % (L_e / 1000, A_e / 1000)),
           ("Dormitoare", "3"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după planșele 9,50 = 5,50 | 4,00 m, terasă sud 1,50 m.",
        "Etajul stă pe 6,60 m (2,60 | 4,00); terasa de vest 2,90 m e în afara anvelopei.",
        "Scara e zonă, nu cameră. Şarpantă clasică din lemn."])
m.nivel(p)
m.nivel(e)

if __name__ == "__main__":
    for niv in (p, e):
        pr = verifica(niv)
        print("%s circulaţie:" % niv.nume, "TRECE" if not pr else " | ".join(pr))
    print("gabarit parter %.2f × %.2f · etaj %.2f × %.2f"
          % (L / 1000, A / 1000, L_e / 1000, A_e / 1000))
    print("amprentă %.1f m² · util %.1f (parter %.1f + etaj %.1f)"
          % (p.amprenta, p.util + e.util, p.util, e.util))
    for niv in (p, e):
        print("— %s —" % niv.nume)
        for c in niv.camere:
            print("   %-32s %5.2f × %5.2f = %5.2f"
                  % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   P %s: %s" % (lat, descriere_fatada(p, lat)))
    for lat in "NS":
        elevatie_png(p, lat, "/private/tmp/planuri/zora-el-%s.png" % lat)
        elevatie_png(e, lat, "/private/tmp/planuri/zora-e-el-%s.png" % lat)
    plansa(m, "/private/tmp/planuri/zora.svg")
