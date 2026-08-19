#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORA — 98,9 m², trei dormitoare.

Original Instagram: 13,00 = 5,00 + 8,00, adâncime 9,00 m,
terasă nord 1,50 m pe living, alee est 1,50 m.

  N  terasă 1,50 pe living
     Living 24,21 | D1 11,20 | D2 11,24 | Dressing 5,27
     Living       | Hol 7,30              | Ensuite 3,96
     Bucătărie 8,91 | Tehnic 4,36 | Vest 6,00 | Baie 5,40 | Master 11,13
  S  intrare în vestibul

Pereții 38 / 13 cm lărgesc gabaritul față de 9,00 m original.
Terasa stă în afara anvelopei.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

# coloane: living | D1 | D2 | est (dressing / ensuite / master)
Wliv, Wd1, Wd2, We = 4494, 2589, 2599, 2200
xh = Wliv + PI
x2 = xh + Wd1 + PI
xe = x2 + Wd2 + PI
IL = xe + We                              # 12272

Hdr, Hen = 2395, 1800
Hd = Hdr + PI + Hen                       # 4325 — D1 și D2 până sub dressing+ensuite
y_hol = Hd + PI                           # 4455
Hhol = 1373
y_s = y_hol + Hhol + PI                   # 5958
Hs = 2600
IA = y_s + Hs                             # 8558
Hme = IA - y_hol                          # 4103 — master pe est, lângă hol + sud

Hliv = 5387
y_kit = Hliv + PI                         # 5517
Hs_l = IA - y_kit                         # 3041
Wkit, Wteh = 2930, 1434

Wv, Wb = 2308, 2077
x_baie = xh + Wv + PI
x_mast = x_baie + Wb + PI                 # aripa de sud a masterului
Wm_s = IL - x_mast

L, A = IL + 2 * PE, IA + 2 * PE

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Living · dining", 0, 0, Wliv, Hliv)
n.camera("Bucătărie", 0, y_kit, Wkit, Hs_l)
n.camera("Tehnic", Wkit + PI, y_kit, Wteh, Hs_l)
n.camera("Dormitor 1", xh, 0, Wd1, Hd)
n.camera("Dormitor 2", x2, 0, Wd2, Hd)
n.camera("Hol", xh, y_hol, Wd1 + PI + Wd2, Hhol)
n.camera("Dressing", xe, 0, We, Hdr)
n.camera("Baie matrimonială", xe, Hdr + PI, We, Hen)
n.camera("Dormitor matrimonial", xe, y_hol, We, Hme)
n.camera("Dormitor matrimonial", x_mast, y_s, xe - x_mast, Hs)
n.camera("Vestibul", xh, y_s, Wv, Hs)
n.camera("Baie", x_baie, y_s, Wb, Hs)

for w in [
    (Wliv, 0, PI, IA),                       # living | noapte
    (xh + Wd1, 0, PI, Hd),                   # D1 | D2
    (x2 + Wd2, 0, PI, IA),                   # D2+hol+baie | est
    (0, Hliv, Wliv, PI),                     # living | bucătărie+tehnic
    (Wkit, y_kit, PI, Hs_l),                 # bucătărie | tehnic
    (xh, Hd, Wd1 + PI + Wd2, PI),            # D1+D2 | hol
    (xe, Hdr, We, PI),                       # dressing | ensuite
    (xe, Hdr + PI + Hen, We, PI),            # ensuite | master
    (xh, y_hol + Hhol, Wd1 + PI + Wd2, PI),  # hol | vest+baie
    (xh + Wv, y_s, PI, Hs),                  # vestibul | baie
    (x_baie + Wb, y_s, PI, Hs),              # baie | master sud
]:
    n.perete(*w)

for t in [
    (xh + 400, Hd, 900, True),               # hol → D1
    (x2 + 400, Hd, 900, True),               # hol → D2
    (x2 + Wd2, y_hol + 200, 900, False),     # hol → ensuite
    (xe + 400, Hdr, 800, True),              # ensuite → dressing
    (xe + 400, Hdr + PI + Hen, 800, True),   # ensuite → master
    (x_baie + 200, y_hol + Hhol, 800, True), # hol → baie
    (xh + 400, y_hol + Hhol, 900, True),     # hol → vestibul
    (Wliv, y_hol + 80, min(800, Hliv - y_hol - 160), False, False),  # hol → living
    (Wliv, y_s + 400, 800, False),           # vestibul → tehnic
    (400, Hliv, 1800, True, False),          # living ↔ bucătărie
    (Wkit, y_kit + 400, 800, False),         # bucătărie → tehnic
]:
    n.usa(*t)

n.usa_ext("S", xh + 250, 1100)
n.gol_ext(xh + 250, IA, 1100, PE, usa=True)
n.usa_ext("N", 600, 2400)                    # living → terasa nord
n.gol_ext(600, -PE, 2400, PE, usa=True)
n.fereastra("N", xh + 500, 1600)             # D1
n.fereastra("N", x2 + 500, 1600)             # D2
n.fereastra("V", 800, 1800)                  # living
n.fereastra("V", y_kit + 800, 1400)          # bucătărie
n.fereastra("S", 400, 1200)                  # bucătărie
n.fereastra("S", Wkit + PI + 200, 900)       # tehnic
n.fereastra("S", x_baie + 400, 1100)         # baie
n.fereastra("E", 400, 1100)                  # dressing
n.fereastra("E", Hdr + PI + 400, 900)        # ensuite
n.fereastra("E", y_s + 400, 1800)            # master
n.fereastra("E", y_hol + 200, 900)           # master lângă hol

n.zona("Terasă", -PE, -PE - 1500, Wliv + 2 * PE + 800, 1500)
n.zona("Alee", IL + PE, -PE, 1500, A)
n.zona("Intrare", xh - 200, IA + PE, Wv + 600, 1500)

n.pune("canapea", 200, 400, 2200, 900)
n.pune("masa", 800, 2800, 1800, 1000)
n.pune("blat", 80, y_kit + 80, 600, 2200)
n.pune("chiuveta", 140, y_kit + 400, 450, 600)
n.pune("plita", 140, y_kit + 1400, 450, 700)
n.pune("raft", Wkit + PI + 80, y_kit + 200, 800, 1400)
n.pune("masina", Wkit + PI + 80, y_kit + Hs_l - 700, 600, 600)
n.pune("pat1", xh + 200, 400, 1400, 2000)
n.pune("dulap", xh + Wd1 - 550, 200, 500, 1800)
n.pune("pat1", x2 + Wd2 - 1600, 400, 1400, 2000)
n.pune("dulap", x2 + 80, 200, 500, 1800)
n.pune("dulap", xe + 80, 80, We - 160, 550)
n.pune("dus", xe + We - 900, Hdr + PI + 80, 800, 800)
n.pune("wc", xe + 80, Hdr + PI + 80, 400, 600)
n.pune("lavoar", xe + 80, Hdr + PI + Hen - 480, 600, 400)
n.pune("pat", xe + 200, y_s + 300, 1800, 2100)
n.pune("cada", x_baie + 80, y_s + Hs - 750, 1700, 700)
n.pune("lavoar", x_baie + 80, y_s + 80, 600, 450)
n.pune("wc", x_baie + Wb - 500, y_s + 200, 400, 600)
n.pune("dulap", xh + 80, y_s + 80, 500, Hs - 160)

m = Model(
    nume="Ora",
    titlu="PLAN PARTER",
    subtitlu="Casă parter 99 m², trei dormitoare · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "3"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după un proiect de 98,9 m²: living vest, trei dormitoare est,",
        "terasă nord 1,50 m şi alee est 1,50 m, amândouă în afara anvelopei."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/ora.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/ora-el-%s.png" % lat)
