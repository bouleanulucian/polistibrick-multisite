#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TERRA — refăcută. Casă cu etaj, 4 dormitoare, garaj opţional.

Planşa veche avea parterul şi etajul desenate alături, iar conturul nu se putea
măsura: nu i-am putut pune nici cote, nici preţ. Aici e redesenată de la zero,
pe programul ei: un dormitor jos şi trei sus, trei băi, garaj opţional.

Etajul se ridică doar peste corpul principal; peste dormitorul de la parter şi
peste garaj rămâne acoperiş.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 13600, 8800
IL, IA = L - 2 * PE, A - 2 * PE                # 12840 × 8040
LE, AE = 10400, 8800                           # etajul, doar corpul principal
ILE, IAE = LE - 2 * PE, AE - 2 * PE            # 9640 × 8040

# ── PARTER ─────────────────────────────────────────────────────────────────
p = Nivel("PARTER", L, A)
GAR = 2500
CORP = IL - GAR - PI                           # 10210
SUD = 5600

p.camera("Living · bucătărie · dining", 0, 0, 7000, SUD)
p.camera("Dormitor 1", 7130, 0, CORP - 7130, 3400)
p.camera("Baie 3", 7130, 3530, CORP - 7130, SUD - 3530)
p.camera("Hol · scară", 0, SUD + PI, 3800, IA - SUD - PI)
p.camera("Cămară", 3930, SUD + PI, 1870, IA - SUD - PI)
p.camera("Intrare", 5930, SUD + PI, 1870, IA - SUD - PI)
p.camera("Tehnic", 7930, SUD + PI, CORP - 7930, IA - SUD - PI)
p.camera("Garaj", CORP + PI, 0, GAR, IA, tip="garaj")

for w in [(CORP, 0, PI, IA), (0, SUD, CORP, PI), (7000, 0, PI, SUD),
          (7130, 3400, CORP - 7130, PI),
          (3800, SUD + PI, PI, IA - SUD - PI), (5800, SUD + PI, PI, IA - SUD - PI),
          (7800, SUD + PI, PI, IA - SUD - PI)]:
    p.perete(*w)

for (x, y, l, oriz) in [(1200, SUD, 1400, True),        # living → hol·scară
                        (7000, 900, 900, False),         # living → dormitor 1
                        (7130, 3400, 900, True),         # dormitor 1 → baie 3
                        (3800, 6400, 900, False),        # hol → cămară
                        (5800, 6400, 900, False),        # cămară → intrare
                        (7800, 6400, 900, False),        # intrare → tehnic
                        (CORP, 6400, 900, False)]:       # tehnic → garaj
    p.usa(x, y, l, oriz)
p.usa_ext("S", 6200, 1100)
p.usa_ext("E", 2600, 2400)
for lat, poz, lung in (("N", 900, 3200), ("N", 7600, 2200), ("V", 800, 2600),
                       ("V", 6200, 1800), ("S", 900, 2000), ("E", 4000, 900)):
    p.fereastra(lat, poz, lung)

p.pune("canapea", 700, 800, 2800, 950).pune("masa", 4300, 1500, 2200, 1050)
p.pune("scaune", 4400, 900, 2000, 430).pune("scaune", 4400, 2700, 2000, 430)
p.pune("blat", 700, 4600, 3000, 650).pune("plita", 1100, 4700, 700, 450)
p.pune("chiuveta", 2400, 4700, 600, 450)
p.pune("pat", 7500, 500, 1800, 2100).pune("dulap", 9400, 500, 650, 2100)
p.pune("dus", 7400, 3800, 900, 900).pune("lavoar", 8600, 3800, 700, 450)
p.pune("wc", 9500, 3800, 400, 600)
p.pune("raft", 4100, 5900, 1500, 700).pune("masina", 8100, 5900, 600, 600)

# ── ETAJ ───────────────────────────────────────────────────────────────────
e = Nivel("ETAJ", LE, AE)
N1 = 3600
PA, PB = N1 + PI, N1 + PI + 1200
S0 = PB + PI

e.camera("Dormitor 2", 0, 0, 4200, N1)
e.camera("Dormitor 3", 4330, 0, 3170, N1)
e.camera("Baie 1", 7630, 0, ILE - 7630, N1)
e.camera("Palier", 0, PA, ILE, 1200)
e.camera("Dormitor 4", 0, S0, 4200, IAE - S0)
e.camera("Baie 2", 4330, S0, 1970, IAE - S0)
e.camera("Debara", 6430, S0, ILE - 6430, IAE - S0)

for w in [(4200, 0, PI, N1), (7500, 0, PI, N1), (0, N1, ILE, PI), (0, PB, ILE, PI),
          (4200, S0, PI, IAE - S0), (6300, S0, PI, IAE - S0)]:
    e.perete(*w)

for (x, y, l, oriz) in [(1300, N1, 900, True), (5300, N1, 900, True),
                        (8300, N1, 800, True), (1300, PB, 900, True),
                        (4900, PB, 800, True), (7500, PB, 800, True)]:
    e.usa(x, y, l, oriz)
for lat, poz, lung in (("N", 800, 2400), ("N", 4800, 1900), ("N", 8000, 900),
                       ("V", 700, 1900), ("V", 5600, 1900), ("S", 800, 2400),
                       ("S", 6800, 1600), ("E", 700, 1900)):
    e.fereastra(lat, poz, lung)

e.pune("pat", 700, 600, 1800, 2100).pune("dulap", 2700, 600, 700, 2100)
e.pune("pat", 4600, 600, 1800, 2100)
e.pune("dus", 7800, 400, 900, 900).pune("lavoar", 7800, 1600, 700, 450)
e.pune("wc", 7800, 2400, 400, 600)
e.pune("pat", 700, 5500, 1800, 2100).pune("dulap", 2700, 5500, 700, 2100)
e.pune("cada", 4450, 5300, 1700, 750).pune("lavoar", 4450, 6500, 700, 450)
e.pune("wc", 4450, 7300, 400, 600)
e.pune("raft", 6600, 5300, 1400, 700).pune("masina", 6600, 6600, 600, 600)

m = Model(nume="Terra", titlu="PLAN PARTER ŞI ETAJ",
          subtitlu="Casă cu etaj, 4 dormitoare, garaj opţional · sistem Polistibrick",
          acoperis="Şarpantă clasică din lemn, două ape 30°",
          extra=[("Suprafaţă construită", "211,2 m²"), ("Garaj (opţional)", "20,1 m²"),
                 ("Dormitoare", "4")],
          observatii=["Un dormitor la parter şi trei la etaj: camera de jos e pentru bunici,",
                      "birou sau oaspeţi, fără scări.",
                      "Trei băi la patru dormitoare — una jos, două sus.",
                      "Etajul se ridică doar peste corpul principal."])
m.nivel(p).nivel(e)

if __name__ == "__main__":
    for nv in (p, e):
        pr = verifica(nv)
        print("%-7s %s" % (nv.nume, "circulaţie OK" if not pr else "; ".join(pr)))
    plansa(m, "/private/tmp/planuri/terra.svg")
    print("amprentă %.1f m² · util %.1f m² (parter %.1f + etaj %.1f)"
          % (p.amprenta, p.util + e.util, p.util, e.util))
    for nv in (p, e):
        for c in nv.camere:
            print("   %-30s %5.1f m²" % (nv.nume + " · " + c["nume"], c["w"] * c["h"] / 1e6))
