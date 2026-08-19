#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TARA — 108 m², trei dormitoare, garaj.

PARTER (ref/tara/710474388.jpg): 9,50 × 7,50, split 6,00 | 3,50.
  Living 20,55 · hol 6,50 · vest 4,18 · WC 1,83 · garaj 16,90 · tehnic 4,80
  Terasă N 6,00 × 3,00 + 3,50 × 1,50. Scară în hol.

ETAJ (ref/tara/710746118.jpg): D 10,60 · baie 6,80 · hol 7,44
  debară 3,89 · D 10,11 · master 15,39. Pante h=2,00 / 3,00 pe sud.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

We = 3280
Hteh = round(4.80e6 / We)                # 1463
Hgar = round(16.90e6 / We)               # 5152
IA = Hteh + PI + Hgar                    # 6745
A = IA + 2 * PE                          # 7505

Ww = round(20.55e6 / IA)                 # 3047
Wm = 2150
Hvest = round(4.18e6 / Wm)               # 1944
Wwc = 1200
Hwc = round(1.83e6 / Wwc)                # 1525
Hhol = IA - Hvest - PI

IL = Ww + PI + Wm + PI + We              # 8737
L = IL + 2 * PE                          # 9497  ≈ 9,50 m
xh = Ww + PI
xe = xh + Wm + PI
y_gar = Hteh + PI
y_vest = Hhol + PI

# hol 6,50 = bandă centrală minus WC
# Wm * Hhol = 6,50 + 1,83 dacă WC e tăiat din hol — îl țin separat


# ═══ PARTER ═════════════════════════════════════════════════════════════════
p = Nivel("PARTER", L, A)
p.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

p.camera("Living · dining · bucătărie", 0, 0, Ww, IA)
p.camera("WC", xh, 0, Wwc, Hwc)
p.camera("Hol", xh + Wwc + PI, 0, Wm - Wwc - PI, Hwc)
p.camera("Hol", xh, Hwc + PI, Wm, Hhol - Hwc - PI)
p.camera("Vestibul", xh, y_vest, Wm, Hvest)
p.camera("Tehnic", xe, 0, We, Hteh)
p.camera("Garaj", xe, y_gar, We, Hgar)

for w in [
    (Ww, 0, PI, IA),
    (xh + Wm, 0, PI, IA),
    (xe, Hteh, We, PI),
    (xh + Wwc, 0, PI, Hwc),
    (xh, Hwc, Wm, PI),
    (xh, y_vest - PI, Wm, PI),
]:
    p.perete(*w)

p.usa(Ww, Hwc + PI + 400, 1400, False, False)                    # living ↔ hol
p.usa(xh + Wwc, 350, 800, False)                                 # hol → WC
p.usa(xh + 400, y_vest - PI, 900, True)                          # hol → vest
p.usa(xh + Wm, y_gar + 500, 900, False)                          # hol → garaj
p.usa(xe, 300, 800, False)                                       # (hol/living) → tehnic via est
p.usa(xh + 80, Hwc + PI + 200, 900, False)                       # hol → scară

p.usa_ext("S", xh + 400, 1100)
p.gol_ext(xh + 400, IA, 1100, PE, usa=True)
p.usa_ext("S", xe + 400, 2400)
p.gol_ext(xe + 400, IA, 2400, PE, usa=True)
p.gol_ext(500, -PE, 2200, PE, usa=True)
p.fereastra("N", xe + 600, 1600)
p.fereastra("V", 600, 1800)
p.fereastra("V", 2800, 1600)
p.fereastra("V", 5200, 900)
p.fereastra("E", y_gar + 1400, 1200)

p.zona("Scară", xh + 80, Hwc + PI + 80, min(1250, Wm - 160), 2300)
p.zona("Terasă", -PE, -PE - 3000, Ww + PI + Wm + PE, 3000)
p.zona("Terasă", xe - PE, -PE - 1500, We + 2 * PE, 1500)
p.zona("Prispă", xh - 200, IA + PE, Wm + 800, 1000)

p.pune("canapea", 200, 400, 900, 2200)
p.pune("masa", 1400, 800, 1400, 1400)
p.pune("blat", 80, IA - 680, min(2800, Ww - 160), 600)
p.pune("plita", 400, IA - 620, 700, 450)
p.pune("chiuveta", 1300, IA - 620, 600, 450)
p.pune("wc", xh + 80, 80, 400, 600)
p.pune("lavoar", xh + 550, 80, 500, 400)
p.pune("dulap", xh + 80, y_vest + 80, Wm - 160, 450)
p.pune("masina", xe + 400, y_gar + 400, 1800, 4200)
p.pune("raft", xe + 80, 80, We - 160, 500)


# ═══ ETAJ ═══════════════════════════════════════════════════════════════════
Hs = round(10.11e6 / 3400)               # 2974
Wd2 = round(10.11e6 / Hs)                # 3400
Wmast = IL - PI - Wd2
Hn = IA - Hs - PI
Wd1 = round(10.60e6 / Hn)
We_e = We
Hb = round(6.80e6 / We_e)
Hdeb = round(3.89e6 / We_e)
xh_e = Wd1 + PI
xe_e = IL - We_e
Whol = xe_e - PI - xh_e
y_s = Hn + PI
y_deb = Hb + PI

e = Nivel("ETAJ", L, A)
e.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

e.camera("Dormitor 1", 0, 0, Wd1, Hn)
e.camera("Hol", xh_e, 0, Whol, Hn)
e.camera("Baie", xe_e, 0, We_e, Hb)
e.camera("Debară", xe_e, y_deb, We_e, Hdeb)
e.camera("Hol", xh_e, y_s, Whol, min(Hs, IA - y_s) if y_deb + Hdeb + PI < y_s else (y_s and 0) or (IA - y_s))
e.camera("Dormitor 2", 0, y_s, Wd2, Hs)
e.camera("Dormitor matrimonial", Wd2 + PI, y_s, Wmast, Hs)

# hol sud: doar dacă rămâne loc între palier și dormitoare
# (y_s == Hn+PI, hol sud = aceeași bandă cu dormitoarele — NU)
# scot holul sud dacă s-a pus pe banda dormitoarelor
e.camere = [c for c in e.camere if not (c["nume"] == "Hol" and c["y"] == y_s)]
# palierul nord trebuie să ajungă la master: ușa pe peretele orizontal Hn
# debară sub baie, deasupra masterului
# dacă y_deb+Hdeb > Hn, debară coboară în banda de sud — ajustez
if y_deb + Hdeb > Hn:
    Hdeb = Hn - y_deb
    # aria debară: recalculez după verificare

for w in [
    (Wd1, 0, PI, Hn),
    (xe_e - PI, 0, PI, Hn),
    (0, Hn, IL, PI),
    (xe_e, Hb, We_e, PI),
    (Wd2, y_s, PI, Hs),
]:
    e.perete(*w)

e.usa(Wd1, 400, 800, False)                                      # hol N → D1
e.usa(xe_e - PI, 350, 800, False)                                # hol N → baie
e.usa(xe_e - PI, y_deb + 80, min(800, max(400, Hdeb - 120)), False)
e.usa(xh_e + 80, 80, 900, False)                                 # hol → scară

# D2 din hol: holul nord nu atinge D2. Ușa D2 pe peretele de vest al masterului
# e greșită (trecere prin master). Holul coboară o fâșie vest lângă D2:
# adaug hol sud vest, lățime 1100, din Hn până la sud — taie din D2? 
# Mai bine: D2 se deschide dintr-un palier de 1100 pe estul lui, luat din master.

# palier sud = 1100 din master, hol continuat
Wpal = 1100
e.camere = [c for c in e.camere if c["nume"] != "Dormitor matrimonial"]
e.camera("Hol", Wd2 + PI, y_s, Wpal, Hs)
e.camera("Dormitor matrimonial", Wd2 + PI + Wpal + PI, y_s, Wmast - Wpal - PI, Hs)
e.perete(Wd2 + PI + Wpal, y_s, PI, Hs)

e.usa(Wd2, y_s + 400, 900, False)                                # hol sud → D2
e.usa(Wd2 + PI + Wpal, y_s + 400, 900, False)                    # hol sud → master
e.usa(Wd2 + PI + 80, Hn, 800, True)                              # hol nord → hol sud

e.fereastra("V", 500, 1600)
e.fereastra("V", y_s + 600, 1600)
e.fereastra("N", xe_e + 400, 1100)
e.fereastra("E", 400, 1100)
e.fereastra("E", y_deb + 80, 800)
e.fereastra("E", y_s + 800, 1600)
e.fereastra("S", Wd2 + PI + Wpal + PI + 600, 1800)
e.fereastra("S", 500, 1600)

e.zona("Scară", xh_e + 80, 80, min(1250, Whol - 160), 2200)
e.zona("h=3,00", 0, y_s + 500, IL, 180)
e.zona("h=2,00", 0, IA - 650, IL, 180)

e.pune("pat1", 250, 250, 1400, 2000)
e.pune("dulap", 200, Hn - 500, min(1800, Wd1 - 400), 450)
e.pune("cada", xe_e + 80, 80, min(1700, We_e - 160), 700)
e.pune("lavoar", xe_e + 80, Hb - 480, 600, 400)
e.pune("wc", xe_e + We_e - 500, 80, 400, 600)
e.pune("dulap", xe_e + 80, y_deb + 80, We_e - 160, min(450, Hdeb - 100))
e.pune("pat1", 250, y_s + 400, 1400, 2000)
e.pune("pat", Wd2 + PI + Wpal + PI + 300, y_s + Hs - 2300, 2100, 1800)


m = Model(
    nume="Tara",
    titlu="PLAN PARTER + ETAJ",
    subtitlu="Casă cu etaj, trei dormitoare şi garaj · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, țiglă ceramică teracotă",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "3"),
           ("Băi", "1 + WC"),
           ("Garaj", "da")],
    observatii=[
        "Reprodusă după planșele cotate 9,50 × 7,50 m, split 6,00 | 3,50 m.",
        "Terasă nord 6,00 × 3,00 + 3,50 × 1,50 m în afara anvelopei de 38 cm.",
        "La etaj camerele de sud rămân sub panta h=2,00 / 3,00. Scară ca zonă."])
m.nivel(p)
m.nivel(e)

if __name__ == "__main__":
    for niv in (p, e):
        pr = verifica(niv)
        print("%s circulaţie:" % niv.nume, "TRECE" if not pr else " | ".join(pr))
    print("gabarit %.2f × %.2f · util %.1f (parter %.1f + etaj %.1f)"
          % (L / 1000, A / 1000, p.util + e.util, p.util, e.util))
    for niv in (p, e):
        print("— %s —" % niv.nume)
        for c in niv.camere:
            print("   %-32s %5.2f × %5.2f = %5.2f"
                  % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   P %s: %s" % (lat, descriere_fatada(p, lat)))
    for lat in "NS":
        elevatie_png(p, lat, "/private/tmp/planuri/tara-el-%s.png" % lat)
        elevatie_png(e, lat, "/private/tmp/planuri/tara-e-el-%s.png" % lat)
    plansa(m, "/private/tmp/planuri/tara.svg")
