#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SILVA — refăcută. Casă cu etaj şi garaj, 3 dormitoare.

Planşa veche avea desenat 12,46 × 7,38 m = 92,0 m², dar în tablou scria
amprentă 115,1 m², iar parterul cerea 73,4 m² utili plus 21,8 m² de garaj —
95,2 m² închişi, care nu intrau. Amprenta din tablou era cea bună: aici casa
are 13,40 × 8,60 m = 115,2 m² şi programul se închide.

Garajul e doar la parter; etajul nu se ridică peste el.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 13400, 8600
IL, IA = L - 2 * PE, A - 2 * PE                # 12640 × 7840
LE, AE = 10200, 8600                           # etajul, fără garaj
ILE, IAE = LE - 2 * PE, AE - 2 * PE            # 9440 × 7840

# ── PARTER ─────────────────────────────────────────────────────────────────
p = Nivel("PARTER", L, A)
GAR = 3200                                     # garajul, la est
ZI = IL - GAR - PI                             # 9310
SUD = 4900                                     # banda de sud

p.camera("Living · bucătărie · dining", 0, 0, ZI, SUD)
p.camera("Intrare · scară", 0, SUD + PI, 4200, IA - SUD - PI)
p.camera("WC", 4330, SUD + PI, 2100, IA - SUD - PI)
p.camera("Cămară", 6560, SUD + PI, 1600, IA - SUD - PI)
p.camera("Hol", 8290, SUD + PI, ZI - 8290, IA - SUD - PI)
p.camera("Garaj", ZI + PI, 0, GAR, IA, tip="garaj")

for w in [(ZI, 0, PI, IA), (0, SUD, ZI, PI), (4200, SUD + PI, PI, IA - SUD - PI),
          (6430, SUD + PI, PI, IA - SUD - PI), (8160, SUD + PI, PI, IA - SUD - PI)]:
    p.perete(*w)

for (x, y, l, oriz) in [(1400, SUD, 1600, True),        # living → intrare·scară
                        (4200, 5800, 900, False),        # intrare → WC
                        (6430, 5800, 900, False),        # WC → cămară
                        (8160, 5800, 900, False),        # cămară → hol
                        (ZI, 5800, 900, False)]:         # hol → garaj
    p.usa(x, y, l, oriz)
p.usa_ext("S", 1500, 1100)
p.usa_ext("E", 2400, 2600)
for lat, poz, lung in (("N", 900, 3000), ("N", 5200, 2600), ("V", 800, 2400),
                       ("V", 5600, 1600), ("S", 900, 1800), ("S", 4600, 900)):
    p.fereastra(lat, poz, lung)

p.pune("canapea", 700, 800, 2800, 950).pune("masa", 4600, 1400, 2300, 1050)
p.pune("scaune", 4700, 800, 2100, 430).pune("scaune", 4700, 2600, 2100, 430)
p.pune("blat", 7400, 400, 1700, 650).pune("plita", 7600, 500, 700, 450)
p.pune("chiuveta", 8500, 500, 600, 450)
p.pune("cada", 4450, 5300, 1600, 700).pune("lavoar", 4450, 6400, 700, 450)
p.pune("wc", 4450, 7100, 400, 600)
p.pune("raft", 6700, 5300, 1300, 700).pune("masina", 6700, 6600, 600, 600)

# ── ETAJ ───────────────────────────────────────────────────────────────────
e = Nivel("ETAJ", LE, AE)
N1 = 3400                                      # banda de nord
PA, PB = N1 + PI, N1 + PI + 1200               # palierul, pe mijloc
S0 = PB + PI

e.camera("Dormitor 1", 0, 0, 4600, N1)
e.camera("Dormitor 2", 4730, 0, ILE - 4730, N1)
e.camera("Palier", 0, PA, ILE, 1200)
e.camera("Dormitor 3", 0, S0, 5200, IAE - S0)
e.camera("Baie", 5330, S0, 2670, IAE - S0)
e.camera("Debara", 8130, S0, ILE - 8130, IAE - S0)

for w in [(4600, 0, PI, N1), (0, N1, ILE, PI), (0, PB, ILE, PI),
          (5200, S0, PI, IAE - S0), (8000, S0, PI, IAE - S0)]:
    e.perete(*w)

for (x, y, l, oriz) in [(1500, N1, 900, True), (6300, N1, 900, True),
                        (1400, PB, 900, True), (5900, PB, 800, True),
                        (8400, PB, 800, True)]:
    e.usa(x, y, l, oriz)
for lat, poz, lung in (("N", 900, 2600), ("N", 5600, 2600), ("V", 700, 1900),
                       ("V", 5200, 1900), ("S", 900, 2400), ("S", 5600, 900),
                       ("E", 700, 1900)):
    e.fereastra(lat, poz, lung)

e.pune("pat", 800, 600, 1800, 2100).pune("dulap", 2800, 600, 700, 2100)
e.pune("pat", 5200, 600, 1800, 2100).pune("dulap", 7300, 600, 700, 2100)
e.pune("pat", 900, 5300, 1800, 2100).pune("dulap", 3100, 5300, 700, 2100)
e.pune("cada", 5450, 5100, 1700, 750).pune("lavoar", 5450, 6200, 700, 450)
e.pune("wc", 5450, 7000, 400, 600).pune("masina", 6700, 7000, 600, 600)
e.pune("raft", 8250, 5200, 1000, 700)

m = Model(nume="Silva", titlu="PLAN PARTER ŞI ETAJ",
          subtitlu="Casă cu etaj şi garaj, 3 dormitoare · sistem Polistibrick",
          acoperis="Şarpantă clasică din lemn, două ape 30°",
          extra=[("Suprafaţă construită", "202,9 m²"), ("Garaj (opţional)", "25,1 m²"),
                 ("Dormitoare", "3")],
          observatii=["Garajul se construieşte doar la parter; etajul nu se ridică peste el.",
                      "Zona de zi ocupă tot nordul parterului, într-o singură cameră.",
                      "Trei dormitoare aproape egale, toate cu fereastră pe două laturi."])
m.nivel(p).nivel(e)

if __name__ == "__main__":
    for nv in (p, e):
        pr = verifica(nv)
        print("%-7s %s" % (nv.nume, "circulaţie OK" if not pr else "; ".join(pr)))
    plansa(m, "/private/tmp/planuri/silva.svg")
    print("amprentă %.1f m² · util %.1f m² (parter %.1f + etaj %.1f)"
          % (p.amprenta, p.util + e.util, p.util, e.util))
    for nv in (p, e):
        for c in nv.camere:
            print("   %-28s %5.1f m²" % (nv.nume + " · " + c["nume"], c["w"] * c["h"] / 1e6))
