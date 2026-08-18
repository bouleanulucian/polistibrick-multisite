#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIENA — casă parter cu curte interioară, acoperiş plat.

Alt limbaj decât restul catalogului: volum dreptunghiular cu acoperiş terasă,
tencuială colorată, goluri tăiate adânc, curte în mijloc. Tema vine din
proiectul de referinţă 88-72 (15,08 × 18,15 m, 142 m² utili, amprentă 200 m²);
curtea scoate exact diferenţa dintre dreptunghi şi amprenta construită.

Faţadele se desenează din acelaşi tabel de goluri ca planul, iar descrierea
randării se scrie din el — deci nu poate apărea o fereastră într-un loc şi nu
în celălalt.
"""
from plansa import Nivel, Model, plansa, verifica, fatada, descriere_fatada, PE, PI

L, A = 12000, 16000
IL, IA = L - 2 * PE, A - 2 * PE                # 11240 × 15240

N1 = 5400                                       # zona de zi, la nord
C1a, C1b = N1 + PI, N1 + PI + 1300              # coridorul de nord
B1a = C1b + PI
B1b = B1a + 3440                                # banda dormitoarelor 1 şi 2
C2a, C2b = B1b + PI, B1b + PI + 1300            # coridorul de mijloc
B2a = C2b + PI                                  # banda de sud, cu curtea

LEG_X0, LEG_X1 = 3930, 5130                     # legătura dintre coridoare
CU_X0, CU_X1 = 4130, 8000                       # curtea, în banda de sud

n = Nivel("PARTER", L, A)

# ── nord: zona de zi, cămara, intrarea ─────────────────────────────────────
n.camera("Living · bucătărie · dining", 0, 0, 7000, N1)
n.camera("Cămară · tehnic", 7130, 0, 1670, N1)
n.camera("Intrare", 8930, 0, IL - 8930, N1)

# ── circulaţia: două coridoare şi legătura dintre ele ──────────────────────
n.camera("Coridor nord", 0, C1a, IL, 1300)
n.camera("Coridor sud", 0, C2a, IL, 1300)
n.camera("Legătură", LEG_X0, B1a, LEG_X1 - LEG_X0, B1b - B1a)

# ── banda dormitoarelor ────────────────────────────────────────────────────
n.camera("Dormitor 1", 0, B1a, LEG_X0 - PI, B1b - B1a)
n.camera("Dormitor 2", LEG_X1 + PI, B1a, 3040, B1b - B1a)
n.camera("Baie 1", LEG_X1 + PI + 3170, B1a, IL - LEG_X1 - PI - 3170, B1b - B1a)

# ── banda de sud: dormitor, curte, baie ────────────────────────────────────
n.camera("Dormitor 3", 0, B2a, CU_X0 - PI, IA - B2a)
n.camera("Baie 2", CU_X1 + PI, B2a, IL - CU_X1 - PI, IA - B2a)

# ── curtea ─────────────────────────────────────────────────────────────────
n.zona("Terasă scobită", CU_X0, B2a, CU_X1 - CU_X0, IA - B2a)

# ── compartimentări ────────────────────────────────────────────────────────
for w in [(7000, 0, PI, N1), (8800, 0, PI, N1),
          (0, N1, IL, PI), (0, C1b, IL, PI),
          (LEG_X0 - PI, B1a, PI, B1b - B1a), (LEG_X1, B1a, PI, B1b - B1a),
          (LEG_X1 + PI + 3040, B1a, PI, B1b - B1a),
          (0, B1b, IL, PI), (0, C2b, IL, PI),
          (CU_X0 - PI, B2a, PI, IA - B2a), (CU_X1, B2a, PI, IA - B2a)]:
    n.perete(*w)

# ── uşi ────────────────────────────────────────────────────────────────────
for (x, y, l, oriz) in [
        (1200, N1, 1600, True),                  # zona de zi → coridor nord
        (7500, N1, 900, True),                   # cămară → coridor nord
        (9500, N1, 1000, True),                  # intrare → coridor nord
        (1400, C1b, 900, True),                  # coridor nord → dormitor 1
        (LEG_X0, C1b, 1000, True),               # coridor nord → legătură
        (6200, C1b, 900, True),                  # coridor nord → dormitor 2
        (9200, C1b, 800, True),                  # coridor nord → baie 1
        (LEG_X0, B1b, 1000, True),               # legătură → coridor sud
        (1600, C2b, 900, True),                  # coridor sud → dormitor 3
        (8900, C2b, 800, True),                  # coridor sud → baie 2
]:
    n.usa(x, y, l, oriz)

# ── goluri în pereţii exteriori ────────────────────────────────────────────
n.nisa("N", 8930, 2100, 900)                    # intrarea retrasă, tăiată în volum
n.usa_ext("N", 9300, 1200)                      # uşa, în fundul nişei
n.usa(CU_X0 + 1200, B2a - PI, 1600, True)       # coridor sud → terasa scobită
n.fereastra("N", 700, 2400)                     # zona de zi: gol mare
n.fereastra("N", 3500, 1100)                    # zona de zi: gol îngust, ritm
n.fereastra("N", 5300, 1100)                    # zona de zi: al treilea gol
n.fereastra("N", 7300, 600)                     # cămara: fantă înaltă
n.fereastra("V", 700, 2000)                     # zona de zi, spre vest
n.fereastra("E", 600, 1600)                     # intrarea
n.fereastra("V", B1a + 600, 1600)               # dormitor 1
n.fereastra("E", B1a + 600, 1600)               # baie 1
n.fereastra("V", B2a + 500, 1800)               # dormitor 3
n.fereastra("E", B2a + 500, 1200)               # baie 2
n.fereastra("S", 1000, 2200)                    # dormitor 3, spre sud
n.fereastra("S", 8600, 1400)                    # baie 2, spre sud

# ── mobilier ───────────────────────────────────────────────────────────────
n.pune("canapea", 600, 600, 2600, 950).pune("masa", 3800, 1400, 2100, 1050)
n.pune("scaune", 3900, 800, 1900, 430).pune("scaune", 3900, 2600, 1900, 430)
n.pune("blat", 500, 4300, 3000, 700).pune("plita", 900, 4400, 700, 450)
n.pune("chiuveta", 2100, 4400, 600, 450)
n.pune("raft", 7300, 500, 1300, 700).pune("masina", 7300, 1900, 600, 600)
n.pune("dulap", 9200, 500, 1400, 600)

n.pune("pat", 500, B1a + 500, 1800, 2100).pune("dulap", 2500, B1a + 500, 700, 2100)
n.pune("pat", LEG_X1 + PI + 400, B1a + 500, 1800, 2100)
n.pune("cada", LEG_X1 + PI + 3400, B1a + 300, 1600, 700)
n.pune("lavoar", LEG_X1 + PI + 3400, B1a + 1400, 700, 450)
n.pune("wc", LEG_X1 + PI + 3400, B1a + 2300, 400, 600)

n.pune("pat", 600, B2a + 500, 1800, 2100).pune("dulap", 2600, B2a + 500, 700, 2100)
n.pune("dus", CU_X1 + PI + 200, B2a + 400, 900, 900)
n.pune("lavoar", CU_X1 + PI + 200, B2a + 1600, 700, 450)
n.pune("wc", CU_X1 + PI + 200, B2a + 2400, 400, 600)

m = Model(
    nume="Siena",
    titlu="PLAN PARTER",
    subtitlu="Casă pe un nivel, cu curte interioară · acoperiş terasă · sistem Polistibrick",
    acoperis="Terasă, atic drept",
    extra=[("Terasă scobită", "%.1f m²" % ((CU_X1-CU_X0)*(IA-B2a)/1e6)),
           ("Gabarit volum", "12,00 × 16,00 m"),
           ("Dormitoare", "3")],
    observatii=[
        "Terasa e scobită în volum, deschisă spre sud: casa rămâne un dreptunghi curat.",
        "Acoperiş terasă cu atic drept: casa se citeşte ca un volum tăiat curat.",
        "Două coridoare şi o legătură între ele: fiecare cameră are uşa ei.",
    ])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie: %s" % ("TRECE" if not pr else "; ".join(pr)))
    plansa(m, "/private/tmp/planuri/siena.svg")
    curte = (CU_X1-CU_X0)*(IA-B2a)/1e6
    amp = n.amprenta - curte
    print("volum %.1f m² · curte %.1f m² · construit %.1f m² · util %.1f m²"
          % (n.amprenta, curte, amp, n.util))
    for c in n.camere:
        print("   %-28s %5.1f m²" % (c["nume"], c["w"]*c["h"]/1e6))
    print("\nFAŢADE — descrierea vine din acelaşi tabel de goluri:")
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
