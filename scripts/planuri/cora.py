#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CORA — 72,1 m², două dormitoare, lot îngust.

Original nadiyni_stiny / Db8wcgxDe2J, planșa 7,50 × 11,50 m:
  N  terasă 2,00 m pe toată lățimea
     D2 10,30 | Hol 7,40 | Master 15,60
     Baie 4,32 | Hol      | Living 22,73
     WC 2,96  | Hol      | Living (bucătărie în L sub master)
     Tehnic 5,98 | Debara 2,73 | Living
  S  terasă 1,50 m, intrare în tehnic

Debara = walk-in lângă holul de la intrare, ușa din hol, nu fâșie sub pat.
Pereții 38 / 13 cm lărgesc gabaritul față de 7,50 m original.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

# coloane: vest (D2/baie/WC/tehnic) | hol+debară | est (master + living)
W1, Wh = 2600, 1200
Hn = round(10.30e6 / W1)                 # 3962
We = round(15.60e6 / Hn)                 # 3937
xh, xe = W1 + PI, W1 + PI + Wh + PI
IL = W1 + PI + Wh + PI + We              # 7997

h_baie = round(4.32e6 / W1)              # 1662
h_wc = round(2.96e6 / W1)                # 1138
h_teh = round(5.98e6 / W1)               # 2300
y_baie = Hn + PI
y_wc = y_baie + h_baie + PI
y_teh = y_wc + h_wc + PI
IA = y_teh + h_teh                       # 9452

# hol coboară 900 mm în banda de sud ca să aibă perete comun cu tehnicul
HOL_S = 900
h_hol = y_teh + HOL_S
y_deb = h_hol + PI
h_deb = IA - y_deb                       # 1270
w_deb = round(2.73e6 / h_deb)            # 2150 — walk-in, lângă tehnic
# debară începe în coloana holului și intră în living
assert xh + w_deb < xe + We - 1400, "livingul de sud rămâne circulabil"

L, A = IL + 2 * PE, IA + 2 * PE

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Dormitor 2", 0, 0, W1, Hn)
n.camera("Hol", xh, 0, Wh, h_hol)
n.camera("Dormitor matrimonial", xe, 0, We, Hn)
n.camera("Baie", 0, y_baie, W1, h_baie)
n.camera("WC", 0, y_wc, W1, h_wc)
n.camera("Tehnic", 0, y_teh, W1, h_teh)
n.camera("Debara", xh, y_deb, w_deb, h_deb)
# living = tot estul sub master, minus colțul debaralei
liv_s_x = xh + w_deb + PI
n.camera("Living · dining · bucătărie", xe, y_baie, We, y_deb - y_baie)
n.camera("Living · dining · bucătărie", liv_s_x, y_deb,
         xe + We - liv_s_x, h_deb)

for w in [
    (W1, 0, PI, IA),                          # vest | hol+debară
    (xh + Wh, 0, PI, h_hol),                  # hol | master+living (până la debară)
    (0, Hn, W1, PI),                          # D2 | baie
    (xe, Hn, We, PI),                         # master | living
    (0, y_baie + h_baie, W1, PI),             # baie | WC
    (0, y_wc + h_wc, W1, PI),                 # WC | tehnic
    (xh, h_hol, Wh, PI),                      # hol | debară (doar lățimea holului)
    (xh + Wh, y_deb, w_deb - Wh, PI),         # living nord | debară
    (xh + w_deb, y_deb, PI, h_deb),           # debară | living sud
]:
    n.perete(*w)

for t in [
    (W1, 1400, 900, False),                   # hol → D2
    (xh + Wh, 1400, 900, False),              # hol → master
    (W1, y_baie + 400, 800, False),           # hol → baie
    (W1, y_wc + 150, 800, False),             # hol → WC
    (W1, y_teh + 80, 800, False),             # hol → tehnic (suprapunere 900 mm)
    (xh, h_hol, 800, True),                   # hol → debară
    (xh + Wh, y_baie + 500, 1400, False, False),  # hol → living (trecere)
]:
    n.usa(*t)

n.gol_ext(400, IA, 1100, PE, usa=True)        # intrare sud → tehnic
n.gol_ext(liv_s_x + 200, IA, 1600, PE)        # living → terasa de sud
n.fereastra("N", 450, 1600)
n.fereastra("N", xe + 800, 2200)
n.fereastra("V", y_baie + 350, 900)
n.fereastra("V", y_wc + 150, 700)
n.fereastra("V", y_teh + 600, 900)
n.fereastra("E", 600, 1800)
n.fereastra("E", y_baie + 1400, 2400)

n.zona("Terasă", -PE, -PE - 2000, L, 2000)
n.zona("Terasă", -PE, IA + PE, L, 1500)
n.zona("Intrare", 200, IA + PE, 1600, 1100)

n.pune("pat", 250, 400, 1400, 2000)
n.pune("dulap", 200, Hn - 500, 1500, 450)
n.pune("pat", xe + We - 2000, 350, 1800, 2100)
n.pune("dulap", xe + 250, Hn - 500, 2000, 450)
n.pune("cada", 200, y_baie + 80, 1700, 700)
n.pune("lavoar", 200, y_baie + h_baie - 450, 600, 400)
n.pune("wc", W1 - 500, y_baie + 200, 400, 600)
n.pune("wc", 180, y_wc + 80, 400, 600)
n.pune("lavoar", 700, y_wc + 80, 500, 400)
n.pune("raft", 200, y_teh + 400, 800, 1400)
n.pune("dulap", xh + 80, y_deb + 80, w_deb - 200, 600)
n.pune("blat", xe + 80, y_baie + 80, 2200, 600)
n.pune("plita", xe + 250, y_baie + 150, 700, 450)
n.pune("chiuveta", xe + 1200, y_baie + 150, 600, 450)
n.pune("masa", xe + 400, y_baie + 1600, 1400, 900)
n.pune("canapea", xe + We - 1000, y_deb - 2000, 900, 1800)

m = Model(
    nume="Cora",
    titlu="PLAN PARTER",
    subtitlu="Casă parter compactă, două dormitoare, lot îngust · sistem Polistibrick",
    acoperis="Şarpantă în două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2"),
           ("Băi", "1 + WC")],
    observatii=[
        "Reprodusă după un proiect compact de 72,1 m² pe lot îngust:",
        "hol între dormitoare, debară walk-in lângă tehnic, terase 2,00 / 1,50 m."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/cora.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/cora-el-%s.png" % lat)
