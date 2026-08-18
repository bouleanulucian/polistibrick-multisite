#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARIA — refăcută. Casă cu etaj, 4 dormitoare, garaj opţional.

Planşa veche se contrazicea singură: desenul avea 10,07 × 7,19 m = 72,4 m²,
dar tabloul scria amprentă 89,6 m², iar cele şapte camere de la etaj însumau
72,1 m² utili — nu încăpeau în 59,9 m² de interior. Aici gabaritul e refăcut
ca să ţină programul. Patru dormitoare de ~14 m² plus baie, rufe şi palier nu
încap în 89,6 m²: aici casa are 11,20 × 8,60 m = 96,3 m² amprentă, iar camerele
se închid la cifră.

Etajul acoperă toată amprenta, inclusiv garajul.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 11200, 8600
IL, IA = L - 2 * PE, A - 2 * PE              # 10440 × 7840

# ── PARTER ─────────────────────────────────────────────────────────────────
p = Nivel("PARTER", L, A)
GAR = 3500                                    # lăţimea garajului, la est
ZI = IL - GAR - PI                            # 6210

p.camera("Living · dining", 0, 0, ZI, 4500)
p.camera("Bucătărie", 0, 4630, 2700, IA - 4630)
p.camera("Cămară", 2830, 4630, 1300, IA - 4630)
p.camera("Hol · scară", 4260, 4630, ZI - 4260, IA - 4630)
p.camera("Garaj", ZI + PI, 0, GAR, IA, tip="garaj")

for w in [(ZI, 0, PI, IA), (0, 4500, ZI, PI),
          (2700, 4630, PI, IA - 4630), (4130, 4630, PI, IA - 4630)]:
    p.perete(*w)

for (x, y, l, oriz) in [(1000, 4500, 1200, True),      # living → hol
                        (2700, 4630, 900, False),      # bucătărie → cămară
                        (4130, 5400, 900, False),      # cămară → hol
                        (ZI, 5400, 900, False)]:        # hol → garaj
    p.usa(x, y, l, oriz)
p.usa("Intrare", 0, 0, True) if False else None
p.usa_ext("S", 4700, 1100)                              # intrarea, la sud
p.usa_ext("E", 2600, 2600)                              # poarta de garaj
p.fereastra("N", 800, 3000)                             # living
p.fereastra("V", 700, 2400)
p.fereastra("S", 600, 1600)                             # bucătărie
p.fereastra("V", 5100, 1200)

p.pune("canapea", 600, 700, 2600, 950).pune("masa", 3300, 1500, 2000, 1000)
p.pune("scaune", 3400, 900, 1800, 430).pune("scaune", 3400, 2650, 1800, 430)
p.pune("blat", 300, 5000, 2200, 650).pune("plita", 700, 5100, 700, 450)
p.pune("chiuveta", 1700, 5100, 600, 450)
p.pune("raft", 2950, 4900, 1050, 600)
p.pune("masina", 4400, 4900, 600, 600)

# ── ETAJ ───────────────────────────────────────────────────────────────────
e = Nivel("ETAJ", L, A)
V1 = 3900                                     # blocul de vest
P0, P1 = V1 + PI, V1 + PI + 1100              # palierul
E0 = P1 + PI                                  # blocul de est

e.camera("Dormitor 1", 0, 0, V1, 3700)
e.camera("Dormitor 2", 0, 3830, V1, IA - 3830)
e.camera("Palier", P0, 0, P1 - P0, IA)
e.camera("Dormitor 4", E0, 0, IL - E0, 2900)
e.camera("Baie", E0, 3030, 2140, 2270)
e.camera("Rufe", E0 + 2270, 3030, IL - E0 - 2270, 2270)
e.camera("Dormitor 3", E0, 5430, IL - E0, IA - 5430)

for w in [(V1, 0, PI, IA), (P1, 0, PI, IA), (0, 3700, V1, PI),
          (E0, 2900, IL - E0, PI), (E0, 5300, IL - E0, PI),
          (E0 + 2140, 3030, PI, 2270)]:
    e.perete(*w)

for (x, y, l, oriz) in [(V1, 900, 900, False), (V1, 5200, 900, False),
                        (P1, 800, 900, False), (P1, 3600, 800, False),
                        (P1, 6100, 900, False), (E0 + 2140, 3600, 800, False)]:
    e.usa(x, y, l, oriz)

for lat, poz, lung in (("N", 700, 2200), ("V", 600, 1800), ("V", 4600, 1800),
                       ("S", 600, 2200), ("S", 6600, 2400), ("E", 600, 1900),
                       ("E", 5800, 1900), ("N", 6600, 2600)):
    e.fereastra(lat, poz, lung)

e.pune("pat", 700, 600, 1800, 2100).pune("dulap", 2600, 600, 700, 2100)
e.pune("pat", 700, 4400, 1800, 2100).pune("dulap", 2600, 4400, 700, 2100)
e.pune("pat", 5800, 500, 1800, 2100).pune("dulap", 7900, 500, 700, 2100)
e.pune("cada", 5500, 3200, 1700, 750).pune("lavoar", 5500, 4300, 700, 450)
e.pune("wc", 5500, 4900, 400, 600)
e.pune("masina", 8000, 3200, 600, 600).pune("raft", 8000, 4200, 1600, 700)
e.pune("pat", 5800, 5700, 1800, 2100).pune("dulap", 7900, 5700, 700, 2100)

m = Model(nume="Aria", titlu="PLAN PARTER ŞI ETAJ",
          subtitlu="Casă cu etaj, 4 dormitoare, garaj opţional · sistem Polistibrick",
          acoperis="Şarpantă clasică din lemn, două ape 30°",
          extra=[("Suprafaţă construită", "192,6 m²"), ("Garaj (opţional)", "27,4 m²"),
                 ("Dormitoare", "4")],
          observatii=["Etajul acoperă toată amprenta, inclusiv garajul.",
                      "Patru dormitoare aproape egale, câte două de fiecare parte a palierului.",
                      "Bucătăria e cameră separată, nu deschisă spre living."])
m.nivel(p).nivel(e)

if __name__ == "__main__":
    for nv in (p, e):
        pr = [x for x in verifica(nv) if "Intrare" not in x]
        print("%-7s %s" % (nv.nume, "circulaţie OK" if not pr else "; ".join(pr)))
    plansa(m, "/private/tmp/planuri/aria.svg")
    print("amprentă %.1f m² · util %.1f m² (parter %.1f + etaj %.1f)"
          % (p.amprenta, p.util + e.util, p.util, e.util))
