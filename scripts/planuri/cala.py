#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CALA — reprodusă din proiectul de referinţă 88-13 (9,75 × 19,35 m, 122 m²).

Casa-longhouse cu trei benzi: dormitoare la nord, zona de zi vitrată la mijloc
(retrasă între două terase acoperite, est şi vest), zona de noapte la sud, cu
intrarea printr-un portic scobit în colţul de sud-vest.

Grila e măsurată pe radiografia planşei originale (etalon separat pe axe:
61,7 px/m pe lăţime, 58,9 px/m pe înălţime) şi rezolvată pe suprafeţele
SCRISE pe planul lor: 10,38 · 4,38 · 10,35 · 1,86 · 7,21 · 46,94 · 6,99 ·
3,70 · 3,70 · 2,50 · 3,68 · 4,79 · 4,45 · 11,85. Camerele închise ies exact;
holurile şi livingul se recalculează pe pereţii noştri de 38.

Goluri măsurate pe faţade: N: 2,90 / 0,91 / 1,39 · S: 0,89 / 2,90 ·
vitraje 4,5 m pe pereţii retraşi ai livingului. Est şi vest, în rest: pline.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 9750, 19350
IL, IA = L - 2 * PE, A - 2 * PE                  # 8990 × 18590

# retragerile vitrate ale livingului (est+vest) şi porticul de sud-vest
REC_Y0, REC_Y1 = 5370, 10470                     # notch-ul teraselor, în y
REC_V, REC_E = 1220, 7770                        # feţele exterioare ale retragerii
POR_X, POR_Y = 2970, 17244                       # porticul de la intrare

CONTUR = [(-PE, -PE), (IL + PE, -PE),
          (IL + PE, REC_Y0), (REC_E, REC_Y0), (REC_E, REC_Y1), (IL + PE, REC_Y1),
          (IL + PE, IA + PE),
          (POR_X, IA + PE), (POR_X, POR_Y), (-PE, POR_Y),
          (-PE, REC_Y1), (REC_V, REC_Y1), (REC_V, REC_Y0), (-PE, REC_Y0)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── banda de nord: dormitoare + baie + spălătorie + hol ─────────────────────
n.camera("Dormitor 1", 0, 0, 4325, 2400)             # 10,38
n.camera("Baie 1", 4455, 0, 1825, 2400)              # 4,38
n.camera("Dormitor 2", 6410, 0, 2580, 4010)          # 10,35
n.camera("Spălătorie", 0, 2530, 1260, 1480)          # 1,86
n.camera("Hol nord", 1390, 2530, 4890, 1480)         # 7,2

# ── mijloc: zona de zi, între cele două terase ──────────────────────────────
n.camera("Living · dining · bucătărie", 1600, 4140, 6170, 7940)   # 49,0

# ── banda de sud ────────────────────────────────────────────────────────────
n.camera("Dressing · birou", 0, 12210, 2513, 2781)   # 6,99
n.camera("Hol", 2643, 12210, 900, 2911)              # gâtul dinspre living
n.camera("Baie 2", 3673, 12210, 2965, 1248)          # 3,70
n.camera("Cămară", 6768, 12210, 2222, 1125)          # 2,50
n.camera("Dressing 2", 6768, 13465, 2222, 1656)      # 3,68
n.camera("Hol noapte", 3543, 13588, 3095, 1533)      # bara transversală
n.camera("Antreu", 0, 15251, 2970, 1613)             # 4,79
n.camera("Baie 3", 3100, 15251, 1332, 3339)          # 4,45
n.camera("Tehnic", 4562, 15251, 749, 3339)           # 2,50
n.camera("Dormitor 3", 5441, 15251, 3549, 3339)      # 11,85

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    # nord
    (4325, 0, 130, 2400), (6280, 0, 130, 4010),
    (0, 2400, 6280, 130), (1260, 2530, 130, 1480),
    (0, 4010, 6280, 130),                       # hol nord | living (până la D2)
    # sud: peretele living | banda de sud
    (0, 12080, 8990, 130),
    (2513, 12210, 130, 2781),                   # 6,99 | gât
    (3543, 12210, 130, 1378),                   # gât | baie 2
    (3673, 13458, 2965, 130),                   # baie 2 | hol noapte
    (6638, 12210, 130, 2911),                   # baie2/hol | coloana cămară-dressing
    (6768, 13335, 2222, 130),                   # cămară | dressing 2
    (0, 14991, 2513, 130),                      # 6,99 | antreu
    (0, 15121, 8990, 130),                      # holurile | rândul de jos
    (2970, 15251, 130, 3339),                   # antreu/portic | baie 3
    (4432, 15251, 130, 3339),                   # baie 3 | tehnic
    (5311, 15251, 130, 3339),                   # tehnic | dormitor 3
    (0, 16864, 2970, 130),                      # antreul se opreşte la portic
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (1700, 2400, 900, True),        # hol nord → dormitor 1
    (4700, 2400, 800, True),        # hol nord → baie 1
    (1260, 3100, 800, False),       # hol nord → spălătorie
    (6280, 3100, 900, False),       # hol nord → dormitor 2
    (1800, 4010, 1200, True),       # hol nord → living (trecere largă)
    (2700, 12080, 800, True),       # living → gâtul holului de sud
    (6850, 12080, 800, True),       # bucătărie → cămară
    (2513, 13700, 900, False),      # gât → dressing · birou
    (3543, 14000, 900, False, False),   # gât → hol noapte (zonă deschisă)
    (4500, 13458, 900, True),       # hol noapte → baie 2
    (6638, 13800, 900, False),      # hol noapte → dressing 2
    (900, 15121, 900, True),        # dressing · birou → antreu
    (3600, 15121, 760, True),       # hol noapte → baie 3
    (4600, 15121, 700, True),       # hol noapte → tehnic
    (5600, 15121, 1000, True),      # hol noapte → dormitor 3
]:
    n.usa(*t)

# intrarea: prin porticul scobit, în peretele lui de fund
n.gol_ext(700, 16864, 1100, 380, usa=True)

# ── goluri în anvelopă (măsurate pe radiografie) ────────────────────────────
n.fereastra("N", 706, 2900)                     # dormitor 1
n.fereastra("N", 4709, 908)                     # baie 1
n.fereastra("N", 6719, 1394)                    # dormitor 2
n.fereastra("S", 4790, 900)                     # baie 3  (int-x 3300..4200)
n.fereastra("S", 290, 2900)                     # dormitor 3 (int-x 5800..8700)
# vitrajele livingului, pe pereţii retraşi (glisante mari)
n.gol_ext(REC_V, 5670, 380, 4500, usa=True)     # spre terasa de vest
n.gol_ext(REC_E - 380, 5670, 380, 4500, usa=True)   # spre terasa de est

# ── terasele şi porticul, punctate ──────────────────────────────────────────
n.zona("Terasă", -2880, REC_Y0, 2500 + 1600, REC_Y1 - REC_Y0)
n.zona("Terasă", REC_E, REC_Y0, 1600 + 1700, REC_Y1 - REC_Y0)
n.zona("Intrare", -PE, POR_Y, POR_X + PE, IA + PE - POR_Y)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 700, 200, 2100, 1800).pune("dulap", 3500, 200, 700, 2000)
n.pune("cada", 4600, 150, 1650, 750).pune("lavoar", 4600, 1100, 600, 450)
n.pune("wc", 5700, 1700, 400, 600)
n.pune("pat1", 6700, 300, 1100, 2100).pune("dulap", 8200, 300, 650, 1900)
n.pune("masina", 150, 2700, 600, 600).pune("masina", 150, 3400, 600, 600)
n.pune("dulap", 1600, 3300, 4400, 620)
n.pune("canapea", 2200, 5400, 950, 2400).pune("canapea", 5300, 5400, 950, 2400)
n.pune("masa", 3400, 8600, 2100, 1000)
n.pune("scaune", 3500, 8100, 1900, 420).pune("scaune", 3500, 9700, 1900, 420)
n.pune("blat", 2200, 11350, 3600, 620).pune("plita", 2700, 11450, 700, 450)
n.pune("chiuveta", 4200, 11450, 600, 450)
n.pune("raft", 6900, 12300, 2000, 700)
n.pune("dulap", 6900, 13600, 600, 1400).pune("dulap", 8400, 13600, 590, 1400)
n.pune("dulap", 100, 12300, 620, 2300).pune("dulap", 1800, 12300, 620, 2300)
n.pune("dus", 3800, 12300, 900, 900).pune("lavoar", 5100, 12300, 700, 450)
n.pune("wc", 6100, 12300, 400, 600)
n.pune("dulap", 200, 15400, 620, 1300)
n.pune("cada", 3200, 15400, 700, 1600).pune("lavoar", 3250, 17400, 650, 450)
n.pune("wc", 3250, 18000, 400, 600)
n.pune("pat", 6300, 16200, 1800, 2100).pune("dulap", 5550, 15400, 600, 1800)

m = Model(
    nume="Cala",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu living vitrat între două terase · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape",
    extra=[("Gabarit", "9,75 × 19,35 m"),
           ("Dormitoare", "3"),
           ("Terase acoperite", "2, est şi vest")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-13: grila de pereţi",
        "e măsurată pe radiografia planşei şi rezolvată pe suprafeţele",
        "scrise. Zona de zi e retrasă între două terase acoperite,",
        "cu vitraje glisante de 4,5 m pe ambele laturi.",
        "Intrarea: printr-un portic scobit în colţul de sud-vest."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/cala.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
