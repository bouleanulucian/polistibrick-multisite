#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VEGA — reprodusă din proiectul de referinţă Domkamen 89-03 (9,75 × 19,35 m).

Longhouse în formă de I / H alungit: aripi private la nord şi sud, zona de zi
deschisă la mijloc — vitrată spre est şi vest, retrasă între două terase mari
de lemn. Program: 3 dormitoare + birou, 2 băi. Circulaţie pe coridor central;
fiecare cameră se deschide din hol.

PE = 380 · PI = 130. Coordonatele sunt INTERIOARE.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 9750, 19350
IL, IA = L - 2 * PE, A - 2 * PE                  # 8990 × 18590

# retragerile vitrate ale livingului (est+vest) şi porticul de sud-vest
REC_Y0, REC_Y1 = 5300, 11200                     # notch-ul teraselor, în y
REC_V, REC_E = 1300, 7690                        # feţele exterioare ale retragerii
POR_X, POR_Y = 2870, 17250                       # porticul de la intrare

CONTUR = [(-PE, -PE), (IL + PE, -PE),
          (IL + PE, REC_Y0), (REC_E, REC_Y0), (REC_E, REC_Y1), (IL + PE, REC_Y1),
          (IL + PE, IA + PE),
          (POR_X, IA + PE), (POR_X, POR_Y), (-PE, POR_Y),
          (-PE, REC_Y1), (REC_V, REC_Y1), (REC_V, REC_Y0), (-PE, REC_Y0)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── banda de nord: două dormitoare, baie cu cadă, spălătorie, hol cu dulapuri
n.camera("Dormitor 1", 0, 0, 3400, 3400)             # 11,56
n.camera("Baie 1", 3530, 0, 1930, 3400)              # 6,56 · cadă
n.camera("Dormitor 2", 5590, 0, 3400, 3400)          # 11,56
n.camera("Spălătorie", 0, 3530, 1500, 1400)          # 2,10
n.camera("Hol nord", 1630, 3530, 7360, 1400)         # 10,30

# ── mijloc: zona de zi, între cele două terase ──────────────────────────────
S0 = 11190
LX0, LX1 = REC_V + PE, REC_E - PE                # 1680 … 7310
n.camera("Living · dining · bucătărie", LX0, 5060, LX1 - LX0, S0 - PI - 5060)

# ── banda de sud ────────────────────────────────────────────────────────────
GH = 2800                                        # adâncimea gâtului de hol
n.camera("Hol", 3000, S0, 1200, GH)              # gât dinspre living
n.camera("Birou", 0, S0, 2870, GH)               # 8,04
n.camera("Baie 2", 4330, S0, 2100, GH)           # 5,88 · duş
n.camera("Dressing", 6560, S0, 2430, GH)         # 6,80
n.camera("Hol noapte", 3000, S0 + GH + PI, IL - 3000, 1300)
n.camera("Antreu", 0, S0 + GH + PI, 2870,
         POR_Y - PE - (S0 + GH + PI))
n.camera("Dormitor matrimonial", 3000, S0 + GH + PI + 1300 + PI,
         IL - 3000, IA - (S0 + GH + PI + 1300 + PI))

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    # nord
    (3400, 0, PI, 3400),                         # D1 | baie 1
    (5460, 0, PI, 3400),                         # baie 1 | D2
    (0, 3400, IL, PI),                           # dormitoare | hol nord
    (1500, 3530, PI, 1400),                      # spălătorie | hol nord
    (0, 4930, IL, PI),                           # hol nord | living
    # sud
    (0, S0 - PI, IL, PI),                        # living | banda de sud
    (2870, S0, PI, GH),                          # birou | hol
    (4200, S0, PI, GH),                          # hol | baie 2
    (6430, S0, PI, GH),                          # baie 2 | dressing
    (0, S0 + GH, IL, PI),                        # rândul de sus | hol noapte / antreu
    (2870, S0 + GH + PI, PI,
     POR_Y - PE - (S0 + GH + PI)),               # antreu | hol noapte / master
    (3000, S0 + GH + PI + 1300, IL - 3000, PI),  # hol noapte | master
    (0, POR_Y - PE, 2870, PE),                   # fundul porticului — anvelopă
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (2000, 3400, 900, True),         # hol nord → dormitor 1
    (3900, 3400, 800, True),         # hol nord → baie 1
    (6500, 3400, 900, True),         # hol nord → dormitor 2
    (1500, 3800, 800, False),        # hol nord → spălătorie
    (2800, 4930, 1400, True),        # hol nord → living
    (3200, S0 - PI, 900, True),      # living → hol
    (2870, S0 + 700, 900, False),    # hol → birou
    (4200, S0 + 700, 800, False),    # hol → baie 2
    (4800, S0 + GH, 900, True),     # baie 2 → hol noapte
    (7000, S0 + GH, 800, True),     # dressing → hol noapte
    (900, S0 + GH, 900, True),      # birou → antreu
    (3200, S0 + GH, 900, True),     # hol → hol noapte
    (2870, S0 + GH + PI + 300, 900, False),       # antreu → hol noapte
    (5500, S0 + GH + PI + 1300, 1000, True),     # hol noapte → master
]:
    n.usa(*t)

# intrarea: prin porticul scobit, în peretele lui de fund
n.gol_ext(700, POR_Y - PE, 1100, 380, usa=True)

# ── goluri în anvelopă ──────────────────────────────────────────────────────
n.fereastra("N", 700, 2000)                      # dormitor 1
n.fereastra("N", 3900, 900)                      # baie 1
n.fereastra("N", 6200, 2000)                     # dormitor 2
n.fereastra("V", 600, 1600)                      # dormitor 1
n.fereastra("E", 600, 1600)                      # dormitor 2
n.fereastra("V", S0 + 500, 1600)                 # birou
n.fereastra("S", 5600, 2200)                     # dormitor matrimonial
n.fereastra("E", S0 + 4200, 1800)                # dormitor matrimonial
n.gol_ext(REC_V, 5600, 380, 4800, usa=True)      # vitraj vest → terasă
n.gol_ext(REC_E - 380, 5600, 380, 4800, usa=True)  # vitraj est → terasă

# ── terasele şi porticul, punctate ──────────────────────────────────────────
n.zona("Terasă", -PE - 2200, REC_Y0, 2200 + REC_V + PE, REC_Y1 - REC_Y0)
n.zona("Terasă", REC_E, REC_Y0, 2200 + (IL + PE - REC_E), REC_Y1 - REC_Y0)
n.zona("Intrare", -PE, POR_Y, POR_X + PE, IA + PE - POR_Y)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 500, 600, 1800, 2100).pune("dulap", 2600, 400, 650, 2000)
n.pune("birou", 400, 2800, 1400, 500)
n.pune("cada", 3650, 200, 1650, 750).pune("lavoar", 3650, 1200, 650, 450)
n.pune("wc", 4900, 2000, 400, 600)
n.pune("pat1", 5900, 600, 1100, 2100).pune("dulap", 7800, 400, 650, 2000)
n.pune("birou", 7200, 2800, 1400, 500)
n.pune("masina", 200, 3650, 600, 600).pune("masina", 850, 3650, 600, 600)
n.pune("dulap", 1800, 4200, 6800, 600)
n.pune("canapea", 2200, 5600, 2400, 950)
n.pune("canapea", 2200, 7200, 2400, 950)
n.pune("masuta", 2800, 6650, 1200, 500)
n.pune("masa", 2800, 8500, 2400, 1050)
n.pune("scaune", 2900, 8000, 2200, 430).pune("scaune", 2900, 9600, 2200, 430)
n.pune("blat", 2000, 10450, 3200, 620).pune("plita", 2500, 10550, 700, 450)
n.pune("chiuveta", 4000, 10550, 600, 450)
n.pune("blat", 5500, 9800, 1400, 800)
n.pune("plita", 5750, 9950, 700, 450)
n.pune("birou", 400, S0 + 500, 1800, 700)
n.pune("dulap", 200, S0 + 3000, 600, 1800)
n.pune("dus", 4500, S0 + 200, 900, 900).pune("lavoar", 5600, S0 + 200, 650, 450)
n.pune("wc", 5600, S0 + 1000, 400, 600)
n.pune("dulap", 6700, S0 + 200, 2000, 600).pune("dulap", 6700, S0 + 1000, 2000, 600)
n.pune("pat", 5200, S0 + 4200, 2000, 1800)
n.pune("dulap", 4800, S0 + 4000, 600, 1600)

m = Model(
    nume="Vanda",
    titlu="PLAN PARTER",
    subtitlu="Casă parter în formă de I, living vitrat între două terase · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape",
    extra=[("Gabarit", "9,75 × 19,35 m"),
           ("Dormitoare", "3 + birou"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după proiectul de referinţă Domkamen 89-03: longhouse",
        "în formă de I / H alungit, cu aripi private la capete şi zona de zi",
        "deschisă la mijloc, vitrată spre terasele de est şi vest.",
        "Intrarea: printr-un portic scobit în colţul de sud-vest."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    plansa(m, "/tmp/planuri/vega.svg")
