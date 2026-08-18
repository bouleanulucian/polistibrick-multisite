#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NERA — reprodusă din proiectul de referinţă 88-68 (9,05 × 20,75 m, 128 m²).

Longhouse pe trei benzi: dormitoare la nord (matrimonial cu baie proprie),
zona de zi traversantă la mijloc — vitrată spre vest şi retrasă cu 2,4 m
faţă de faţada de est, unde terasa acoperită intră în amprentă — şi zona
de servicii la sud (birou, băi, tehnic), cu intrarea printr-un portic
adânc scobit în faţada de sud.

Grila e măsurată pe radiografia planşei originale (106,97 px/m, izotrop;
pereţii desenaţi au ~48 cm la exterior şi 15 cm la interior) şi rezolvată
pe suprafeţele SCRISE: 15,13 · 9,20 · 9,52 · 3,61 · 3,58 · 5,84 · 42,31 ·
2,93 · 5,38 · 3,05 · 12,42 · 3,56. Camerele închise ies exact.

Goluri măsurate pe faţade: N: 1,42 / 1,42 / 1,41 · S: 2,62 la birou ·
vitraj V 5,64 m · vitraj E (retras) 6,84 m · porticul de intrare pe sud.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 9050, 20750
IL, IA = L - 2 * PE, A - 2 * PE                  # 8290 × 19990

# nişa terasei de est: livingul se retrage la 5,89 m lăţime interioară
REC_E = 6270                                     # faţa exterioară a vitrajului retras
REC_Y0, REC_Y1 = 7800, 14483                     # colţurile nişei (feţe exterioare)

CONTUR = [(-PE, -PE), (IL + PE, -PE),
          (IL + PE, REC_Y0), (REC_E, REC_Y0), (REC_E, REC_Y1), (IL + PE, REC_Y1),
          (IL + PE, IA + PE), (-PE, IA + PE)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── banda de nord ───────────────────────────────────────────────────────────
n.camera("Dormitor matrimonial", 0, 0, 2664, 5680)     # 15,13
n.camera("Baie m.", 0, 5810, 2664, 1355)               # 3,61 · baia matrimonială
n.camera("Dormitor 2", 2794, 0, 2521, 3649)            # 9,20
n.camera("Dormitor 3", 5445, 0, 2845, 3346)            # 9,52
n.camera("Hol", 2794, 3779, 2521, 1111)                # bara holului
n.camera("Hol de noapte", 2794, 5020, 934, 2400)       # piciorul spre living
n.camera("Spălătorie", 3858, 5020, 1457, 2400)         # 3,50
n.camera("Coridor", 5445, 3476, 940, 3944)             # spre dormitor 3 şi baie
n.camera("Baie 2", 6515, 3476, 1775, 3290)             # 5,84

# ── mijloc: zona de zi, retrasă între vitrajul de vest şi terasa de est ─────
n.camera("Living · dining · bucătărie", 0, 7550, 5890, 7183)     # 42,31

# ── banda de sud ────────────────────────────────────────────────────────────
n.camera("Cămară", 0, 14863, 2017, 1453)               # 2,93
n.camera("Hol sud", 2147, 14863, 3780, 1423)           # 5,38
n.camera("Baie 3", 6057, 14863, 2233, 1366)            # 3,05
n.camera("Birou", 0, 16877, 3990, 3113)                # 12,42
n.camera("Antreu", 4120, 16416, 1732, 2237)            # 3,87
n.camera("Tehnic", 5982, 16877, 2308, 1542)            # 3,56

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    # nord
    (2664, 0, 130, 7165),                    # matrimonial + baia m. | mijloc
    (0, 5680, 2664, 130),                    # matrimonial | baia m.
    (0, 7165, 2794, 385),                    # capăt baia m. — perete instalaţii
    (5315, 0, 130, 3476),                    # dormitor 2 | dormitor 3
    (2794, 3649, 2521, 130),                 # dormitor 2 | bara holului
    (5445, 3346, 2845, 130),                 # dormitor 3 | coridor + baie 2
    (2794, 4890, 2521, 130),                 # bara | picior + spălătorie
    (3728, 5020, 130, 2400),                 # picior | spălătorie
    (5315, 3476, 130, 3944),                 # bara + spălătorie | coridor
    (6385, 3476, 130, 3944),                 # coridor | baie 2
    (6515, 6766, 1775, 654),                 # bloc instalaţii sub baia 2
    (2794, 7420, 3096, 130),                 # picior + spălătorie | living
    # sud
    (0, 14733, 5890, 130),                   # living | banda de sud
    (2017, 14863, 130, 1884),                # cămară | hol sud
    (0, 16316, 2017, 431),                   # umplutură sub cămară (dulap zidit)
    (2017, 16286, 2103, 461),                # fundul holului — dulapuri zidite
    (4120, 16286, 1732, 130),                # hol sud | antreu
    (0, 16747, 4120, 130),                   # dulapuri | birou
    (3990, 16877, 130, 3113),                # birou | antreu
    (5852, 16416, 130, 3574),                # antreu | tehnic
    (5982, 16747, 2308, 130),                # baie 3 | tehnic
    (5927, 14863, 130, 1553),                # hol sud | baie 3
    (5927, 16229, 2363, 187),                # fund baie 3
    (5982, 18419, 2308, 1571),               # bloc instalaţii SE
    (4120, 18653, 1732, 380),                # fundul porticului — anvelopă
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (2664, 4100, 700, False),        # bara hol → dormitor matrimonial
    (800, 5680, 750, True),          # matrimonial → baia m.
    (3200, 3649, 700, True),         # bara → dormitor 2
    (5600, 3346, 700, True),         # coridor → dormitor 3
    (5315, 3850, 500, False, False), # bara → coridor (trecere)
    (3000, 4890, 600, True, False),  # bara → picior (trecere)
    (3728, 5300, 750, False),        # picior → spălătorie
    (6385, 3700, 750, False),        # coridor → baie 2
    (2900, 7420, 700, True),         # picior → living
    (600, 14733, 800, True),         # bucătărie → cămară
    (4300, 14733, 1100, True),       # living → hol sud (trecere largă)
    (5927, 15200, 750, False),       # hol sud → baie 3
    (4400, 16286, 900, True),        # hol sud → antreu
    (3990, 17200, 750, False),       # antreu → birou
    (5852, 17000, 700, False),       # antreu → tehnic
]:
    n.usa(*t)

# intrarea: prin porticul adânc de pe sud, în peretele lui de fund
n.gol_ext(4400, 18653, 1100, 380, usa=True)

# ── goluri în anvelopă (măsurate) ───────────────────────────────────────────
n.fereastra("N", 588, 1421)                   # dormitor matrimonial
n.fereastra("N", 3364, 1421)                  # dormitor 2
n.fereastra("N", 6141, 1411)                  # dormitor 3
n.fereastra("V", 8320, 5638)                  # vitrajul livingului, vest
n.gol_ext(REC_E - 380, 7720, 380, 6843, usa=True)   # vitrajul retras, spre terasa de est
n.fereastra("S", 600, 2617)                   # biroul, spre grădină

# porticul de intrare, scobit în volum
n.nisa("S", 4120, 1732, 1337)

# ── terase, punctate ────────────────────────────────────────────────────────
n.zona("Terasă", -2780, 8320, 2400, 5638)
n.zona("Terasă", REC_E, REC_Y0, IL + PE - REC_E, REC_Y1 - REC_Y0)
n.zona("Intrare", 4120, 19033, 1732, 1337)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 500, 900, 1800, 2100).pune("dulap", 150, 3600, 620, 1700)
n.pune("dulap", 2000, 3600, 620, 1700)
n.pune("dus", 150, 5950, 900, 900).pune("lavoar", 1250, 5950, 650, 450)
n.pune("wc", 2100, 6450, 400, 600)
n.pune("pat1", 3100, 300, 1100, 2100).pune("dulap", 4600, 200, 620, 1800)
n.pune("pat1", 6800, 300, 1100, 2100).pune("dulap", 7600, 2200, 620, 1000)
n.pune("masina", 4000, 6600, 600, 600).pune("masina", 4650, 6600, 600, 600)
n.pune("raft", 3950, 5150, 500, 1200)
n.pune("dus", 6700, 3700, 900, 900).pune("cada", 6700, 5900, 1500, 750)
n.pune("lavoar", 7700, 4700, 650, 450).pune("wc", 7800, 5400, 400, 600)
n.pune("blat", 100, 14113, 3400, 620).pune("plita", 600, 14200, 700, 450)
n.pune("chiuveta", 2200, 14200, 600, 450)
n.pune("canapea", 800, 8300, 2800, 950)
n.pune("masuta", 1700, 9800, 900, 600)
n.pune("masa", 1500, 11300, 2400, 1050)
n.pune("scaune", 1600, 10750, 2200, 430).pune("scaune", 1600, 12450, 2200, 430)
n.pune("raft", 100, 14950, 1800, 620)
n.pune("birou", 400, 17300, 1800, 700).pune("canapea", 500, 19000, 2400, 900)
n.pune("dulap", 4250, 16550, 1500, 600)
n.pune("lavoar", 6300, 14950, 650, 450).pune("wc", 7200, 14950, 400, 600)
n.pune("dus", 7300, 15450, 900, 700)
n.pune("boiler", 7600, 17000, 600, 600).pune("masina", 6200, 17000, 600, 600)

m = Model(
    nume="Nera",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu living traversant, vitrat spre terasa de est · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape",
    extra=[("Gabarit", "9,05 × 20,75 m"),
           ("Dormitoare", "3 + birou"),
           ("Băi", "3 + spălătorie")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-68: grila de pereţi",
        "e măsurată pe radiografia planşei (106,97 px/m, izotrop) şi",
        "rezolvată pe suprafeţele scrise. Living traversant, vitrat",
        "spre vest şi retras cu 2,4 m spre est, unde terasa acoperită",
        "intră în amprentă. Intrarea: portic adânc pe faţada de sud."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/nera.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
