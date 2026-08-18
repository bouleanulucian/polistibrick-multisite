#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IZA — reprodusă din proiectul de referinţă 88-70 (14,95 × 25,13 m cu terase
şi garaj, 165 m²).

Corp principal pe trei coloane, cu două extensii pe axa nord-sud:
· terasa de nord cu şezlonguri, masă de exterior şi colţul de jacuzzi sub
  pergolă (extensia de nord-est, 5,0 m);
· vest — dormitor, baie cu cadă, bucătăria în lungul faţadei şi al doilea
  dormitor la sud;
· centru — livingul traversant deschis cu glisante spre terasă, sufrageria
  şi antreul la sud, cu WC de serviciu;
· est — suita matrimonială (dormitor + dressing + baie), spălătoria şi
  vestibulul spre garajul integrat (extensia de sud-est, 4,1 m).

Grila e măsurată pe radiografia planşei originale (46,3 px/m, cotele scrise
14950 / 25130 / 5000 / 15530 / 4100 ca etalon).
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 14650, 19810
IL, IA = L - 2 * PE, A - 2 * PE                  # 13890 × 19050... interior total

# conturul: corpul principal + piciorul garajului spre sud-est
CONTUR = [(-380, -380), (14270, -380),
          (14270, 19430), (8850, 19430), (8850, 15150),
          (-380, 15150)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── coloana de vest ──────────────────────────────────────────────────────────
n.camera("Dormitor 1", 0, 0, 4100, 3280)               # 13,4
n.camera("Baie 1", 0, 3410, 4100, 1650)                # 6,8
n.camera("Bucătărie", 0, 5190, 4100, 4260)             # 17,5 · pe faţada de vest
n.camera("Hol vest", 0, 9580, 4100, 1460)              # 6,0
n.camera("Dormitor 2", 0, 11170, 4100, 3600)           # 14,8

# ── centru ───────────────────────────────────────────────────────────────────
n.camera("Living · dining", 4230, 0, 5570, 9320)       # 51,9 · glisante spre terasă
n.camera("Sufragerie", 4230, 9450, 2900, 2850)         # 8,3
n.camera("Antreu", 4230, 12430, 2900, 2340)            # 6,8
n.camera("WC", 7260, 11170, 1100, 1500)                # 1,7
n.camera("Hol", 7260, 12800, 2540, 1970)               # 5,0 · spre garaj

# ── coloana de est ───────────────────────────────────────────────────────────
n.camera("Dormitor matrimonial", 9930, 0, 3960, 3200)  # 12,7
n.camera("Dressing", 9930, 3330, 3960, 1500)           # 5,9
n.camera("Baie m.", 9930, 4960, 3960, 2100)            # 8,3
n.camera("Spălătorie", 9930, 7190, 3960, 1200)         # 4,8
n.camera("Vestibul", 9930, 8520, 3960, 2000)           # 7,9

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    # vest
    (4100, 0, 130, 14770),                   # coloana de vest | centru
    (0, 3280, 4100, 130),                    # dormitor 1 | baie 1
    (0, 5060, 4100, 130),                    # baie 1 | bucătărie
    (0, 9450, 4100, 130),                    # bucătărie | hol vest
    (0, 11040, 4100, 130),                   # hol vest | dormitor 2
    # centru
    (4230, 9320, 5570, 130),                 # living | banda de sud
    (4230, 12300, 2900, 130),                # sufragerie | antreu
    (7130, 9450, 130, 5320),                 # sufragerie + antreu | wc + hol
    (7260, 12670, 2540, 130),                # wc | hol
    (7260, 11170, 2540, 0),                  # (aliniament)
    (7390, 10650, 2410, 520),                # bloc dulapuri lângă WC
    # est
    (9800, 0, 130, 14770),                   # centru | coloana de est
    (9930, 3200, 3960, 130),                 # matrimonial | dressing
    (9930, 4830, 3960, 130),                 # dressing | baia m.
    (9930, 7060, 3960, 130),                 # baia m. | spălătorie
    (9930, 8390, 3960, 130),                 # spălătorie | vestibul
    (9930, 10520, 3960, 130),                # vestibul | depozit
    (9930, 12280, 3960, 1740),               # bloc depozitare · instalaţii
    (9230, 14150, 4660, 380),                # peretele garajului spre corp
    (9230, 14150, 380, 4900),                # garaj, peretele de vest
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (4165, 1200, 800, False),         # living → dormitor 1
    (4165, 3800, 750, False),         # living → baie 1
    (4165, 6000, 1800, False, False), # living ↔ bucătărie (trecere largă)
    (4165, 9800, 900, False, False),  # sufrageria ↔ holul de vest (trecere)
    (2000, 11040, 800, True),         # hol vest → dormitor 2
    (5000, 9320, 1500, True, False),  # living ↔ sufragerie (trecere)
    (4800, 12300, 900, True),         # sufragerie → antreu
    (7195, 13300, 800, False),        # antreu → hol
    (7500, 12670, 700, True),         # hol → WC
    (9865, 1500, 800, False),         # living → dormitor matrimonial
    (11500, 3200, 800, True),         # matrimonial → dressing
    (11500, 4830, 800, True),         # dressing → baia m.
    (9865, 8600, 700, False),         # living → vestibul
    (10500, 8390, 750, True),         # vestibul → spălătorie
]:
    n.usa(*t)

# intrarea principală: din terasa de sud, în antreu
n.gol_ext(5200, 14770, 1100, 380, usa=True)
# poarta garajului, spre sud
n.gol_ext(10800, 19050, 2600, 380)
# uşa dintre hol şi garaj (gol în peretele garajului)
n.gol_ext(9350, 14150, 900, 380)

# ── goluri în anvelopă ──────────────────────────────────────────────────────
n.gol_ext(4700, -380, 4200, 380, usa=True)     # glisantele livingului spre terasă
n.fereastra("N", 800, 1800)                    # dormitor 1
n.gol_ext(10800, -380, 2200, 380, usa=True)    # matrimonial → terasa cu jacuzzi
n.fereastra("V", 3900, 900)                    # baie 1
n.fereastra("V", 6000, 1800)                   # bucătăria
n.fereastra("V", 12000, 1600)                  # dormitor 2
n.fereastra("S", 1000, 1800)                   # dormitor 2, spre sud
n.fereastra("E", 1000, 1800)                   # dormitor matrimonial
n.fereastra("E", 5500, 900)                    # baia m.
n.fereastra("E", 9000, 900)                    # vestibul

# ── zone punctate ───────────────────────────────────────────────────────────
n.zona("Terasă", -380, -2680, 11080, 2300)
n.zona("Terasă · jacuzzi", 10700, -5310, 3570, 4930)
n.zona("Garaj", 9610, 14530, 4280, 4520)
n.zona("Depozit", 9930, 10650, 3960, 1630)
n.zona("Intrare", 4230, 15150, 3000, 1300)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 1900, 400, 1800, 2100).pune("birou", 200, 400, 700, 1600)
n.pune("dulap", 300, 2600, 2400, 620)
n.pune("cada", 200, 3500, 1700, 750).pune("wc", 2400, 3500, 400, 600)
n.pune("lavoar", 3200, 3500, 650, 450)
n.pune("blat", 100, 5300, 620, 3000).pune("plita", 150, 5900, 450, 700)
n.pune("chiuveta", 150, 7200, 450, 600)
n.pune("dulap", 500, 9700, 2400, 620)
n.pune("pat", 1000, 12100, 1800, 2100).pune("birou", 3200, 11400, 700, 1600)
n.pune("masa", 5200, 700, 2400, 1050)
n.pune("scaune", 5300, 200, 2200, 430).pune("scaune", 5300, 1800, 2200, 430)
n.pune("blat", 4600, 3600, 620, 2600)
n.pune("canapea", 6800, 3600, 2400, 950).pune("canapea", 8250, 4550, 950, 1700)
n.pune("masuta", 7000, 5200, 900, 600)
n.pune("masa", 4900, 10000, 1800, 1050)
n.pune("scaune", 4950, 9550, 1700, 430).pune("scaune", 4950, 11050, 1700, 430)
n.pune("wc", 7500, 11300, 400, 600).pune("lavoar", 8200, 11300, 500, 400)
n.pune("dulap", 7500, 13500, 1800, 620)
n.pune("pat", 10800, 400, 1800, 2100)
n.pune("dulap", 10100, 3400, 620, 1300).pune("dulap", 13200, 3400, 620, 1300)
n.pune("dus", 12900, 5100, 900, 900).pune("wc", 10200, 5100, 400, 600)
n.pune("lavoar", 11200, 5100, 650, 450).pune("lavoar", 12000, 5100, 650, 450)
n.pune("masina", 10200, 7300, 600, 600).pune("masina", 10900, 7300, 600, 600)
n.pune("dulap", 10100, 8700, 620, 1600)
n.pune("raft", 10100, 10750, 3600, 620)

m = Model(
    nume="Iza",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu terasă cu jacuzzi, suită matrimonială şi garaj integrat · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "14,95 × 25,13 m (cu terase şi garaj)"),
           ("Dormitoare", "3"),
           ("Băi", "2 + WC serviciu + spălătorie")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-70: grila de pereţi",
        "e măsurată pe radiografia planşei (46,3 px/m, cote 14950/25130).",
        "Terasă de nord cu jacuzzi sub pergolă, garaj integrat pe sud-est."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/iza.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-24s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
