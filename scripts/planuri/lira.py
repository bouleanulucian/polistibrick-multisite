#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LIRA — casă parter pentru lot îngust: 9,75 m lăţime, 19,35 m adâncime.

Tema vine din proiectul de referinţă măsurat (9,75 × 19,35 m, util 122 m²):
zona de zi la mijloc, dormitoare la ambele capete, terase acoperite pe laturi.
Casa noastră ţine gabaritul şi logica, dar e desenată pe cofrajul Polistibrick
de 38 cm şi rezolvată cu coridor lateral la sud, ca să nu se treacă prin camere.

Coordonatele sunt INTERIOARE. Interiorul are 8,97 × 18,57 m.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 9750, 19350
IL, IA = L - 2 * PE, A - 2 * PE              # 8970 × 18570

# benzile pe adâncime
N1 = 3900                                     # dormitoare nord
H1a, H1b = N1 + PI, N1 + PI + 1200            # hol nord
ZI0 = H1b + PI
ZI1 = ZI0 + 5230                              # zona de zi
H2a, H2b = ZI1 + PI, ZI1 + PI + 1200          # hol sud
S0 = H2b + PI                                 # zona de noapte sud
SD = IA - S0                                  # 6520

COR0, COR1 = 3470, 4670                       # coridorul lateral, 1,20 m

n = Nivel("PARTER", L, A)

# ── nord: două dormitoare şi baia ──────────────────────────────────────────
n.camera("Dormitor 1", 0, 0, 3350, N1)
n.camera("Baie 1", 3480, 0, 1670, N1)
n.camera("Dormitor 2", 5280, 0, IL - 5280, N1)
n.camera("Hol nord", 0, H1a, IL, 1200)

# ── mijloc: zona de zi, pe toată lăţimea ───────────────────────────────────
n.camera("Living · bucătărie · dining", 0, ZI0, IL, ZI1 - ZI0)
n.camera("Hol sud", 0, H2a, IL, 1200)

# ── sud: coridor lateral, camere de o parte şi de alta ─────────────────────
n.camera("Coridor", COR0, S0, COR1 - COR0, SD)
n.camera("Dormitor 3", 0, S0, COR0, 3150)
n.camera("Intrare", 0, S0 + 3150 + PI, COR0, SD - 3150 - PI)
n.camera("Baie 2", COR1, S0, 1670, 3150)
n.camera("Cămară · tehnic", COR1 + 1670 + PI, S0, IL - COR1 - 1670 - PI, 3150)
n.camera("Dormitor 4", COR1, S0 + 3150 + PI, IL - COR1, SD - 3150 - PI)

# ── compartimentări ────────────────────────────────────────────────────────
for w in [(3350, 0, PI, N1), (5150, 0, PI, N1),
          (0, N1, IL, PI), (0, H1b, IL, PI),
          (0, ZI1, IL, PI), (0, H2b, IL, PI),
          (COR0 - PI, S0, PI, SD), (COR1, S0, PI, SD),
          (0, S0 + 3150, COR0, PI), (COR1, S0 + 3150, IL - COR1, PI),
          (COR1 + 1670, S0, PI, 3150)]:
    n.perete(*w)

# ── uşi ────────────────────────────────────────────────────────────────────
for (x, y, l, oriz) in [
        (1000, N1, 900, True),                 # hol nord → dormitor 1
        (4000, N1, 800, True),                 # hol nord → baie 1
        (6600, N1, 900, True),                 # hol nord → dormitor 2
        (2000, H1b, 1600, True),               # hol nord → zona de zi
        (2000, ZI1, 1600, True),               # zona de zi → hol sud
        (3600, H2b, 900, True),                # hol sud → coridor
        (COR0 - PI, S0 + 900, 900, False),     # coridor → dormitor 3
        (COR0 - PI, S0 + 4400, 900, False),    # coridor → intrare
        (COR1, S0 + 800, 800, False),          # coridor → baie 2
        (COR1, S0 + 4400, 900, False),         # coridor → dormitor 4
        (COR1 + 1670, S0 + 900, 800, False),   # baie 2 → cămară
]:
    n.usa(x, y, l, oriz)

n.usa_ext("S", 900, 1100)                      # uşa de intrare, la sud
n.usa_ext("V", ZI0 + 1400, 2600)               # zona de zi → terasa de vest
n.usa_ext("E", ZI0 + 1400, 2600)               # zona de zi → terasa de est

# ── ferestre ───────────────────────────────────────────────────────────────
n.fereastra("N", 700, 1900)                    # dormitor 1
n.fereastra("N", 3800, 800)                    # baie 1
n.fereastra("N", 6100, 2000)                   # dormitor 2
n.fereastra("V", 600, 1500)                    # dormitor 1
n.fereastra("E", 600, 1500)                    # dormitor 2
n.fereastra("V", ZI0 + 4400, 700)              # zona de zi
n.fereastra("E", ZI0 + 4400, 700)
n.fereastra("V", S0 + 700, 1600)               # dormitor 3
n.fereastra("E", S0 + 700, 900)                # baie 2
n.fereastra("E", S0 + 4200, 1800)              # dormitor 4
n.fereastra("S", 4900, 1800)                   # dormitor 4, spre sud

# ── terasele acoperite, pe laturile zonei de zi ────────────────────────────
n.zona("Terasă", -PE - 1800, ZI0 - PI, 1800, ZI1 - ZI0 + 2 * PI)
n.zona("Terasă", IL + PE, ZI0 - PI, 1800, ZI1 - ZI0 + 2 * PI)

# ── mobilier ───────────────────────────────────────────────────────────────
n.pune("pat", 700, 700, 1800, 2100).pune("dulap", 2600, 700, 650, 2100)
n.pune("cada", 3600, 300, 1450, 700).pune("lavoar", 3600, 1400, 700, 450)
n.pune("wc", 3600, 2400, 400, 600)
n.pune("pat", 5600, 700, 1800, 2100).pune("dulap", 7700, 700, 650, 2100)

n.pune("canapea", 900, ZI0 + 700, 950, 2500)
n.pune("canapea", 6900, ZI0 + 700, 950, 2500)
n.pune("masa", 3400, ZI0 + 1000, 2200, 1050)
n.pune("blat", 2600, ZI0 + 3700, 3800, 700).pune("plita", 3100, ZI0 + 3800, 700, 450)
n.pune("chiuveta", 4600, ZI0 + 3800, 600, 450)
n.pune("scaune", 3500, ZI0 + 2300, 2000, 430)

n.pune("pat", 400, S0 + 600, 1800, 2100).pune("dulap", 2400, S0 + 600, 650, 2100)
n.pune("dus", 4800, S0 + 300, 900, 900).pune("lavoar", 4800, S0 + 1500, 700, 450)
n.pune("wc", 4800, S0 + 2300, 400, 600)
n.pune("raft", 6700, S0 + 400, 1900, 700).pune("masina", 6700, S0 + 1600, 600, 600)
n.pune("pat", 5000, S0 + 4200, 1800, 2100).pune("dulap", 7000, S0 + 4200, 650, 2100)
n.pune("dulap", 500, S0 + 4300, 1400, 600)

m = Model(
    nume="Lira",
    titlu="PLAN PARTER",
    subtitlu="Casă pe un nivel, pentru lot îngust · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape 30°",
    extra=[("Lăţime la stradă", "9,75 m"),
           ("Terase acoperite", "2 × 9,4 m²"),
           ("Dormitoare", "4")],
    observatii=[
        "Nouă metri şaptezeci şi cinci la stradă: intră pe lot îngust.",
        "Zona de zi stă la mijloc, între cele două zone de noapte.",
        "Coridorul de sud deschide toate camerele: nu se trece prin niciuna.",
    ])
m.nivel(n)

if __name__ == "__main__":
    p = verifica(n)
    print("verificare circulaţie: %s" % ("TRECE" if not p else "%d probleme" % len(p)))
    for x in p:
        print("   ✗", x)
    plansa(m, "/private/tmp/planuri/lira.svg")
    print("\namprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
