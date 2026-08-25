#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SAVA — 110,89 m² parter, trei dormitoare, două băi, terasă acoperită.

Portare a unui proiect real (ARCHPOINT DESIGN, plan parter V1) în sistemul
Polistibrick. Radiografia planului, pe geometria vectorială a PDF-ului:

  contur zidărie (mm):  (0,0) (6929,0) (6929,3200) (9428,3200)
                        (9428,15847) (0,15847)
  gabarit 9,43 × 15,85 m · amprentă 141,4 m² · util 110,89 m²

Colţul din dreapta-sus, 2,50 × 3,20 m, NU e cameră: e terasă acoperită, în
afara anvelopei. Peretele de cofraj trece pe lângă ea, nu în jurul ei — pe
laturile ei deschise nu e niciun perete.

Cotele originale se închid la milimetru pe amândouă direcţiile (15,85 şi 9,43).
Ariile scrise sunt sursa tare: unde dreptunghiul din cote nu dădea aria scrisă,
a câştigat aria. Dormitorul mare e în L — camera 4,23 × 3,90 plus dressingul
de lângă baie, 1,75 × 2,13; împreună 20,22, exact cât scrie pe plan.

Peretele: original 35 cm, Polistibrick 38. Feţele interioare rămân pe loc,
volumul creşte 3 cm pe latură → 9,49 × 15,91 m.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

# ── grila, în coordonate INTERIOARE (0,0 = colţul NV al feţei interioare) ──
# Adâncimile vin din lanţul de cote al originalului (se închid la 15150 exact);
# lăţimile ies din ariile scrise. Pereţii se aşază PE muchiile camerelor, ca
# uşile să prindă amândouă încăperile.
IL, IA = 8730, 15150                    # interior 9430−700 × 15850−700

y_d1, h_d1 =     0, 3180                # dormitor 1   13,01 / 3,180 → 4091
y_b1, h_b1 =  3310, 1800                # baia 1        4,88 / 1,800 → 2711
y_d2, h_d2 =  5240, 3750                # dormitor 2   15,86 / 3,750 → 4229
y_b2, h_b2 =  9120, 2000                # baia 2        4,25 / 2,000 → 2125
y_d3, h_d3 = 11250, 3900                # dormitor 3   4230 × 3900 = 16,50

w_d1, w_b1, w_d2, w_b2, w_d3 = 4091, 2711, 4229, 2125, 4230
w_dres, h_dres = 1862, 2000             # dressingul dormitorului 3 → 3,72

x_zi   = 4360                           # faţa dinspre zona de zi
w_zi   = IL - x_zi                      # 4370
x_hol = 2841
w_hol = 6475 - x_hol                     # până la peretele spaţiului tehnic
h_hol = 1947
x_teh, w_teh, h_teh = 6605, 2125, 2075  # spaţiul tehnic, 4,41
x_ter, y_ter = 6230, 3200               # terasa acoperită, colţul NE

y_zi  = y_ter + h_teh + PI              # sub spaţiul tehnic
h_buc = 2707                            # bucătăria 11,83 / 4,370
h_zi  = IA - y_zi - h_buc               # restul: zona de zi
y_buc = y_zi + h_zi

L, A = IL + 2 * PE, IA + 2 * PE

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (x_ter + PE, -PE), (x_ter + PE, y_ter - PE),
           (IL + PE, y_ter - PE), (IL + PE, IA + PE), (-PE, IA + PE)])

# ── camerele ── ariile scrise pe planul original sunt ţinta tare
n.camera("Dormitor 1", 0, y_d1, w_d1, h_d1)                    # 13,01
n.camera("Baie 1", 0, y_b1, w_b1, h_b1)                        #  4,88
n.camera("Hol", x_hol, y_b1, w_hol, h_hol)                     #  5,55
n.camera("Spaţiu tehnic", x_teh, y_ter, w_teh, h_teh)          #  4,41
n.camera("Dormitor 2", 0, y_d2, w_d2, h_d2)                    # 15,86
n.camera("Baie 2", 0, y_b2, w_b2, h_b2)                        #  4,25
n.camera("Dressing", w_b2 + PI, y_b2, w_dres, h_dres)          #  3,72 ┐ 20,22
n.camera("Dormitor 3", 0, y_d3, w_d3, h_d3)                    # 16,50 ┘
n.camera("Zona de zi", x_zi, y_zi, w_zi, h_zi)                 # 30,89
n.camera("Bucătărie", x_zi, y_buc, w_zi, h_buc)                # 11,83

# ── compartimentări ── aşezate exact pe muchiile camerelor
for w in [
    (0, y_d1 + h_d1, w_d1, PI),                 # dormitor 1 / baie 1 + hol
    (w_b1, y_b1, PI, h_b1),                     # baia 1 / hol
    (0, y_b1 + h_b1, x_zi, PI),                 # baia 1 + hol / dormitor 2
    (w_d2, y_d2, PI, h_d2),                     # dormitor 2 / zona de zi
    (0, y_d2 + h_d2, x_zi, PI),                 # dormitor 2 / baia 2
    (w_b2, y_b2, PI, h_b2),                     # baia 2 / dressing
    (w_b2 + PI + w_dres, y_b2, PI, h_dres),     # dressing / zona de zi
    (0, y_b2 + h_b2, x_zi, PI),                 # baia 2 + dressing / dormitor 3
    (w_d3, y_d3, PI, h_d3),                     # dormitor 3 / bucătărie
    (x_zi - PI, y_zi, PI, h_zi + h_buc),        # zona de zi / dormitoare
    (x_teh - PI, y_ter, PI, h_teh),             # spaţiul tehnic / hol
    (x_teh, y_ter + h_teh, w_teh, PI),          # spaţiul tehnic / zona de zi
]:
    n.perete(*w)

# ── uşi interioare ── fiecare pe muchia comună a două camere
for t in [
    (2900, y_d1 + h_d1, 900, True),             # dormitor 1 → hol
    (w_b1, y_b1 + 400, 800, False),             # baia 1 → hol
    (600, y_b1 + h_b1, 900, True),              # hol → dormitor 2
    (x_teh + 700, y_ter + h_teh, 800, True),     # spaţiu tehnic → zona de zi
    (2600, y_d2 + h_d2, 800, True),             # dormitor 2 → baia 2
    (w_b2, y_b2 + 500, 800, False),             # baia 2 → dressing
    (600, y_b2 + h_b2, 900, True),              # dressing → dormitor 3
    (w_b2 + PI + w_dres, y_b2 + 700, 900, False),  # dressing → zona de zi
    (w_d2, y_d2 + 2600, 900, False),            # dormitor 2 → zona de zi
    (w_d3, y_d3 + 2800, 900, False),            # dormitor 3 → bucătărie
]:
    n.usa(*t)

# ── intrarea: sub terasa acoperită, în peretele gros din fundul ei ──
n.gol_ext(x_ter, y_ter - PE, 1100, PE, usa=True)

# ── ferestrele ── fiecare cameră care atinge exteriorul are golul ei
n.fereastra("N", 900, 2400)                     # dormitor 1
n.fereastra("V", 700, 1400)                     # dormitor 1
n.fereastra("V", y_b1 + 300, 900)               # baia 1
n.fereastra("V", y_d2 + 900, 1800)              # dormitor 2
n.fereastra("V", y_b2 + 400, 800)               # baia 2
n.fereastra("V", y_d3 + 1000, 1800)             # dormitor 3
n.fereastra("S", 900, 2200)                     # dormitor 3
n.fereastra("S", x_zi + 700, 2400)              # bucătărie
n.fereastra("E", y_d2 + 600, 2600)              # zona de zi
n.fereastra("E", y_d2 + 4200, 2600)             # zona de zi
n.fereastra("E", y_buc + 700, 1600)             # bucătărie
n.gol_ext(x_ter + 400, y_ter - PE, 1600, PE)    # spaţiu tehnic, spre terasă

# ── terasa acoperită, în afara anvelopei ──
n.zona("Terasă acoperită", x_ter + PE, -PE, IL - x_ter - PE + PE, y_ter)

# ── mobilier ──
n.pune("pat", 1500, 500, 1800, 2100)
n.pune("dulap", 200, 300, 500, 2000)
n.pune("cada", 150, y_b1 + 300, 1700, 700)
n.pune("lavoar", 2000, y_b1 + 200, 600, 450)
n.pune("wc", 2300, y_b1 + 1000, 400, 600)
n.pune("pat", 1100, y_d2 + 700, 1800, 2100)
n.pune("dulap", 200, y_d2 + 200, 500, 1800)
n.pune("cada", 150, y_b2 + 200, 1700, 700)
n.pune("lavoar", 1600, y_b2 + 1100, 600, 450)
n.pune("dulap", w_b2 + PI + 200, y_b2 + 200, 600, 1700)
n.pune("pat", 1100, y_d3 + 900, 1800, 2100)
n.pune("dulap", 200, y_d3 + 300, 500, 1800)
n.pune("canapea", x_zi + 300, y_zi + 500, 2400, 900)
n.pune("masa", x_zi + 900, y_zi + 3400, 1600, 1600)
n.pune("blat", x_zi + 3400, y_buc + 200, 700, 2400)
n.pune("plita", x_zi + 3450, y_buc + 500, 550, 500)
n.pune("chiuveta", x_zi + 3450, y_buc + 1500, 550, 450)
n.pune("masina", x_teh + 200, y_ter + 200, 600, 600)
n.pune("raft", x_teh + 200, y_ter + 1100, 1700, 500)

m = Model(
    nume="Sava",
    titlu="PLAN PARTER",
    subtitlu="Casă parter 110,89 m² · trei dormitoare, două băi · sistem Polistibrick",
    acoperis="Şarpantă într-o apă, streaşină subţire, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "3"), ("Băi", "2"),
           ("Terasă acoperită", "2,50 × 3,20 m")],
    observatii=[
        "Portare a unui proiect real de 110,89 m², cotele originale respectate.",
        "Terasa din colţul de nord-est e în afara anvelopei: peretele de cofraj",
        "trece pe lângă ea, pe laturile deschise nu e niciun perete.",
        "Perete original 35 cm; cofrajul Polistibrick are 38, feţele interioare",
        "rămân pe loc, volumul creşte 3 cm pe latură."])
m.nivel(n)

if __name__ == "__main__":
    SCRIS = {"Dormitor 1": 13.01, "Baie 1": 4.88, "Hol": 5.55, "Spaţiu tehnic": 4.41,
             "Dormitor 2": 15.86, "Baie 2": 4.25, "Zona de zi": 30.89,
             "Bucătărie": 11.83}
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    print("gabarit %.2f × %.2f m · amprentă %.2f · util %.2f"
          % (L / 1000, A / 1000, n.amprenta, n.util))
    dorm3 = 0
    for c in n.camere:
        a = c["w"] * c["h"] / 1e6
        if c["nume"] in ("Dressing", "Dormitor 3"):
            dorm3 += a
        s = SCRIS.get(c["nume"])
        dif = ("  scris %5.2f  dif %+5.2f" % (s, a - s)) if s else ""
        print("   %-16s %5.2f × %5.2f = %6.2f%s" % (c["nume"], c["w"]/1000, c["h"]/1000, a, dif))
    print("   %-16s %s = %6.2f  scris 20.22  dif %+5.2f"
          % ("Dormitor 3 (L)", " " * 15, dorm3, dorm3 - 20.22))
    print("   TOTAL util %.2f  ·  scris 110.89  ·  dif %+.2f" % (n.util, n.util - 110.89))
    plansa(m, "/private/tmp/planuri/sava.svg")
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
