#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FIRA — casă cu etaj, două dormitoare + suită, după planșele Instagram.

Radiografie ref/fira/parter.jpg + etaj.jpg, 12,00 × 7,50 m cotat pe anvelopă,
terasă nord 3,50 m (decalaj 1,00 m stânga), prispă sud 1,80 m. Ariile scrise
pe camere. Pereții 38 / 13 lărgesc gabaritul față de original.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

# adâncime interioară din radiografie (fețe interioare N–S)
IA = 6770

We = round(21.70e6 / (IA - PI))          # 3268 — D1 12,26 + D2 9,44
Hd1 = round(12.26e6 / We)                # 3752
Hd2 = IA - PI - Hd1                      # 2888

Wm = round(14.65e6 / (IA - 2 * PI))      # 2250 — baie+hol+vestibul
Hb = round(5.83e6 / Wm)                  # 2591
Hh = round(4.97e6 / Wm)                  # 2209
Hv = IA - 2 * PI - Hb - Hh               # 1710

Wu, Hu = 1964, 2266                      # tehnic 4,45, nordul nu e aliniat cu hol|vest
Wliv = round((33.49e6 + (Wu + PI) * (Hu + PI)) / IA)  # 5688, L-ul livingului

xh, xe = Wliv + PI, Wliv + PI + Wm + PI
IL = xe + We
L, A = IL + 2 * PE, IA + 2 * PE

x_ku = Wliv - Wu - PI                    # living | tehnic
y_un = IA - Hu - PI                      # living | tehnic (doar banda tehnicului)
y_hol = Hb + PI
y_vest = y_hol + Hh + PI
y_d2 = Hd1 + PI

# ═══ PARTER ══════════════════════════════════════════════════════════════════
p = Nivel("PARTER", L, A)
p.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

p.camera("Living · dining · bucătărie", 0, 0, Wliv, y_un)
p.camera("Living · dining · bucătărie", 0, y_un, x_ku, IA - y_un)
p.camera("Hol", xh, y_hol, Wm, Hh)
p.camera("Baie", xh, 0, Wm, Hb)
p.camera("Vestibul", xh, y_vest, Wm, Hv)
p.camera("Dormitor 1", xe, 0, We, Hd1)
p.camera("Dormitor 2", xe, y_d2, We, Hd2)
p.camera("Tehnic", x_ku + PI, y_un + PI, Wu, Hu)

for w in [
    (Wliv, 0, PI, IA),                    # living+tehnic | baie+hol+vestibul
    (xh + Wm, 0, PI, IA),                 # hol | dormitoare
    (xh, Hb, Wm, PI),                     # baie | hol
    (xh, y_hol + Hh, Wm, PI),             # hol | vestibul
    (xe, Hd1, We, PI),                    # dormitor 1 | dormitor 2
    (x_ku, y_un, PI, Hu + PI),            # living | tehnic
    (x_ku + PI, y_un, Wu, PI),            # living | tehnic (nord)
]:
    p.perete(*w)

for t in [
    (Wliv, 2750, 1200, False, False),     # hol → living (trecere)
    (6465, Hb, 800, True),                # hol → baie
    (6119, y_hol + Hh, 900, True),        # hol → vestibul
    (xh + Wm, 2800, 850, False),          # hol → dormitor 1
    (xh + Wm, 4000, 850, False),          # hol → dormitor 2
    (x_ku, 5300, 800, False),             # living → tehnic
]:
    p.usa(*t)

p.usa_ext("N", 800, 2400)                 # living → terasă, glisante
p.usa_ext("S", xh + 80, 1100)             # intrare vestibul
p.fereastra("N", xh + (Wm - 870) // 2, 870)
p.fereastra("N", xe + (We - 1456) // 2, 1456)
p.fereastra("S", 1150, 1460)              # bucătărie, chiuvetă
p.fereastra("S", x_ku + PI + (Wu - 870) // 2, 870)
p.fereastra("S", xe + (We - 1456) // 2, 1456)
p.fereastra("V", 2700, 1460)              # dining
p.fereastra("E", 900, 1400)               # D1
p.fereastra("E", y_d2 + 600, 1400)        # D2

# terasa în AFARA anvelopei; muchia de est = peretele baie | dormitor 1
p.zona("Terasă", -PE - 1000, -PE - 3500, 1000 + PE + Wliv + PI + Wm, 3500)
p.zona("Prispă", xh - 900, IA + PE, Wm + 2400, 1800)
p.zona("Scară", Wliv - 2300, 180, 2200, 2500)

p.pune("blat", 80, IA - 680, 2900, 600)
p.pune("chiuveta", 1200, IA - 620, 600, 450)
p.pune("blat", 80, y_un + 80, 600, 2000)
p.pune("plita", 140, y_un + 400, 450, 700)
p.pune("masa", 900, 1800, 1000, 1800)
p.pune("scaune", 500, 1900, 380, 1600)
p.pune("canapea", 2400, 2800, 1800, 900)
p.pune("raft", 80, 400, 450, 1600)
p.pune("cada", xh + 250, 80, 1700, 700)
p.pune("lavoar", xh + 80, 900, 600, 450)
p.pune("wc", xh + Wm - 500, Hb - 700, 400, 600)
p.pune("pat", xe + We - 2000, 500, 1900, 2100)
p.pune("dulap", xe + 200, Hd1 - 520, 2200, 450)
p.pune("pat1", xe + We - 1600, y_d2 + Hd2 - 2200, 1400, 2000)
p.pune("dulap", xe + 200, y_d2 + 80, 1800, 450)
p.pune("masa", xe + 80, y_d2 + 900, 700, 1400)
p.pune("dulap", xh + Wm - 550, y_vest + 80, 450, Hv - 160)
p.pune("masina", x_ku + PI + 80, y_un + PI + 80, 600, 600)
p.pune("raft", x_ku + PI + Wu - 550, y_un + PI + 200, 450, 1400)

# ═══ ETAJ ════════════════════════════════════════════════════════════════════
# aceeași anvelopă; podul de peste living (NV) nu e cameră; 45,40 m² utili
h_sit = round((45.40e6 - (IL - xh) * IA) / Wliv)
e = Nivel("ETAJ", L, A)
e.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

e.camera("Hol · suită matrimonială", xh, 0, IL - xh, IA)
e.camera("Hol · suită matrimonială", 0, IA - h_sit, Wliv, h_sit)

e.fereastra("E", 2660, 1470)
e.fereastra("S", xe + 400, 1800)
e.fereastra("N", xh + 400, 1600)

# podul e în volum, nu terasă scobită — inset ca descriere_fatada să nu-l ia drept gol
e.zona("Pod h=2,00 / 3,00", 80, 80, Wliv - 160, IA - h_sit - 160)
e.zona("Scară", Wliv - 2300, 180, 2200, 2500)

e.pune("pat", xe + 400, IA - 2200, 2100, 1800)
e.pune("dulap", xh + 200, 80, IL - xh - 400, 500)
e.pune("masa", IL - 1400, IA - 1600, 700, 1200)
e.pune("canapea", 400, IA - h_sit + 80, 1600, 900)
e.pune("raft", xh + 80, 2200, 450, 1800)

m = Model(
    nume="Fira",
    titlu="PLAN PARTER + ETAJ",
    subtitlu="Casă cu etaj, două dormitoare şi suită deschisă · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, ţiglă ceramică teracotă",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2 + suită"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după planșele cotate 12,00 × 7,50 m: living deschis 33,49 m²,",
        "terasă nord 3,50 m în afara anvelopei, prispă sud 1,80 m pe stâlpi."])
m.nivel(p)
m.nivel(e)

if __name__ == "__main__":
    for n in (p, e):
        pr = verifica(n)
        print("%s circulaţie:" % n.nume, "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/fira.svg")
    print("gabarit %.2f × %.2f · util %.1f (parter %.1f + etaj %.1f)"
          % (L / 1000, A / 1000, p.util + e.util, p.util, e.util))
    for n in (p, e):
        for c in n.camere:
            print("   %-36s %5.2f × %5.2f = %5.2f"
                  % (n.nume + " · " + c["nume"],
                     c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   P %s: %s" % (lat, descriere_fatada(p, lat)))
    for lat in "NSEV":
        print("   E %s: %s" % (lat, descriere_fatada(e, lat)))
    for lat in "NS":
        elevatie_png(p, lat, "/private/tmp/planuri/fira-el-%s.png" % lat)
