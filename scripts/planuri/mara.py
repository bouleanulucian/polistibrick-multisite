#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MARA — reprodusă din proiectul de referinţă 88-72 (15,08 × 18,15 m cu terase,
142 m² total, amprentă ~200 m²).

Casă parter în L, organizată în trei coloane:
· vest — dormitorul matrimonial cu dressing, baie proprie şi spălătorie pe un
  coridor propriu, holul de intrare şi carportul cu depozit;
· centru — terasa acoperită la nord (scobită în volum), livingul traversant cu
  glisante spre terasă, bucătăria şi WC-ul de serviciu la sud, cu antreul de
  intrare;
· est — biroul (cu vitraj spre terasă), două dormitoare şi baia lor comună,
  pe un hol de noapte.

Grila e măsurată pe radiografia planşei originale (55,6 / 56,7 px/m, cotele
scrise 15080 şi 18150 ca etalon). Caption-ul original: casă de 142 m² total,
cu amprentă la sol de 200 m² (carportul intră în amprentă, terasa nu).
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 14500, 17350
IL, IA = L - 2 * PE, A - 2 * PE                  # 13740 × 16590

# conturul: terasa scobită la nord-centru, golul de sud-est, piciorul carportului
CONTUR = [(-380, -380), (3170, -380), (3170, 5075),
          (9280, 5075), (9280, 1160), (14120, 1160),
          (14120, 13340), (9080, 13340), (9080, 12990),
          (3170, 12990), (3170, 16970), (-380, 16970)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── coloana de vest ──────────────────────────────────────────────────────────
n.camera("Dormitor matrimonial", 0, 0, 2790, 4430)     # 12,4
n.camera("Dressing", 0, 4560, 1980, 1480)              # 2,9
n.camera("Baie m.", 0, 6170, 1980, 2310)               # 4,6
n.camera("Spălătorie", 0, 8610, 1980, 1910)            # 3,8
n.camera("Coridor", 2110, 4560, 680, 6090)             # coridorul camerelor de vest
n.camera("Hol", 0, 10650, 2790, 1820)                  # holul de intrare, cu decor

# ── centru ───────────────────────────────────────────────────────────────────
n.camera("Living · dining", 3170, 5455, 7080, 4245)    # 30,1
n.camera("Hol de zi", 9660, 1540, 590, 3915)           # pasajul spre birou
n.camera("Antreu", 3170, 9830, 2170, 2780)             # 6,0
n.camera("WC", 5470, 9830, 1050, 1650)                 # 1,7
n.camera("Bucătărie", 6650, 9830, 2680, 2780)          # 7,5
n.camera("Hol de noapte", 9460, 9830, 790, 3130)       # spre dormitoare

# ── coloana de est ───────────────────────────────────────────────────────────
n.camera("Birou", 10380, 1540, 3360, 2780)             # 9,3
n.camera("Dormitor 2", 10380, 4450, 3360, 3980)        # 13,4
n.camera("Baie 2", 10380, 8560, 3360, 1940)            # 6,5
n.camera("Dormitor 3", 10380, 10630, 3360, 2330)       # 7,8

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    # vest
    (0, 4430, 2790, 130),                    # matrimonial | dressing + coridor
    (1980, 4560, 130, 6090),                 # camerele de vest | coridor
    (0, 6040, 1980, 130),                    # dressing | baia m.
    (0, 8480, 1980, 130),                    # baia m. | spălătorie
    (0, 10520, 1980, 130),                   # spălătorie | hol
    (0, 12470, 2790, 380),                   # hol | carport
    (2790, 5075, 380, 7915),                 # spinarea: vest | centru
    # centru
    (3170, 9700, 6160, 130),                 # living | banda de sud
    (5340, 9830, 130, 2780),                 # antreu | WC + bucătărie
    (5470, 11480, 1180, 130),                # capătul WC-ului
    (5470, 11610, 1180, 1000),               # bloc instalaţii sub WC
    (6520, 9830, 130, 2780),                 # WC | bucătărie
    (9330, 9830, 130, 3130),                 # bucătărie | hol de noapte
    # est
    (10250, 1540, 130, 11420),               # holuri | camerele de est
    (10380, 4320, 3360, 130),                # birou | dormitor 2
    (10380, 8430, 3360, 130),                # dormitor 2 | baie 2
    (10380, 10500, 3360, 130),               # baie 2 | dormitor 3
    # depozitul din carport
    (1760, 12850, 130, 3740),
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (2150, 4430, 600, True),          # coridor → dormitor matrimonial
    (1980, 5200, 750, False),         # coridor → dressing
    (1980, 7000, 750, False),         # coridor → baia m.
    (600, 10520, 800, True),          # hol → spălătorie
    (2150, 10650, 600, True, False),  # coridor → hol (trecere)
    (2980, 11200, 900, False),        # hol → antreu (prin spinare)
    (3600, 9700, 1200, True, False),  # living ↔ antreu (trecere)
    (6800, 9700, 1400, True, False),  # living ↔ bucătărie (trecere)
    (5340, 10100, 750, False),        # antreu → WC
    (9500, 9700, 700, True, False),   # living ↔ hol de noapte (trecere)
    (9700, 5455, 500, True, False),   # living ↔ hol de zi (trecere)
    (10250, 2500, 800, False),        # hol de zi → birou
    (10250, 4700, 750, False),        # hol de zi → dormitor 2
    (10250, 9850, 600, False),        # hol de noapte → baie 2
    (10250, 11500, 800, False),       # hol de noapte → dormitor 3
]:
    n.usa(*t)

# intrarea: din puntea de sud, în antreu
n.gol_ext(3600, 12610, 1100, 380, usa=True)

# ── goluri în anvelopă ──────────────────────────────────────────────────────
n.fereastra("N", 600, 1600)                    # dormitor matrimonial
n.gol_ext(2790, 1200, 380, 2400, usa=True)     # matrimonial → terasă (vitraj est)
n.gol_ext(3600, 5075, 5600, 380, usa=True)     # glisantele livingului spre terasă
n.gol_ext(9280, 2300, 380, 1900)               # vitrajul holului de zi, spre terasă
n.gol_ext(10500, 1160, 1600, 380)              # fereastra biroului, spre nord
n.fereastra("E", 5800, 1500)                   # dormitor 2
n.fereastra("E", 9300, 900)                    # baie 2
n.gol_ext(11200, 12960, 1800, 380)             # ferestrele dormitorului 3, spre sud
n.gol_ext(7000, 12610, 1500, 380)              # fereastra bucătăriei, spre sud
n.fereastra("V", 11300, 1200)                  # holul de intrare
n.fereastra("V", 7000, 900)                    # baia m.
n.fereastra("V", 9200, 900)                    # spălătoria

# ── zone punctate ───────────────────────────────────────────────────────────
n.zona("Terasă", 3170, -1840, 6110, 6915)
n.zona("Terasă", 9280, -1840, 4840, 3000)
n.zona("Carport", -380, 12850, 2140, 4120)
n.zona("Depozit", 1890, 12850, 900, 3740)
n.zona("Intrare", 3170, 12990, 3910, 1500)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 400, 1100, 1800, 2100).pune("dulap", 300, 3700, 1600, 620)
n.pune("dulap", 150, 4700, 620, 1200).pune("dulap", 1250, 4700, 620, 1200)
n.pune("dus", 150, 6300, 900, 900).pune("wc", 150, 7800, 400, 600)
n.pune("lavoar", 1100, 6300, 650, 450)
n.pune("masina", 150, 8750, 600, 600).pune("masina", 800, 8750, 600, 600)
n.pune("raft", 150, 9800, 1700, 620)
n.pune("masuta", 700, 11500, 900, 600)
n.pune("canapea", 4200, 6200, 2800, 950).pune("canapea", 4200, 7250, 950, 1700)
n.pune("masuta", 5600, 7600, 700, 700)
n.pune("masa", 7600, 6500, 1800, 1050)
n.pune("scaune", 7650, 6000, 1700, 430).pune("scaune", 7650, 7600, 1700, 430)
n.pune("blat", 6700, 11980, 2600, 620).pune("plita", 7200, 12050, 700, 450)
n.pune("chiuveta", 8300, 12050, 600, 450).pune("blat", 6650, 9900, 620, 1800)
n.pune("wc", 5600, 10100, 400, 600).pune("lavoar", 6100, 9900, 500, 400)
n.pune("birou", 10600, 1700, 1800, 700).pune("dulap", 13100, 1700, 620, 2400)
n.pune("pat", 11000, 4700, 1800, 2100).pune("dulap", 13100, 4600, 620, 1800)
n.pune("cada", 12000, 8700, 1700, 750)
n.pune("lavoar", 10600, 8700, 650, 450).pune("lavoar", 10600, 9350, 650, 450)
n.pune("wc", 11600, 9950, 400, 600)
n.pune("pat1", 10600, 10900, 1600, 2000).pune("birou", 12600, 10800, 1100, 600)
n.pune("dulap", 13100, 11600, 620, 1300)
n.pune("raft", 1950, 13050, 780, 3200)

m = Model(
    nume="Mara",
    titlu="PLAN PARTER",
    subtitlu="Casă parter în L cu terasă acoperită centrală şi carport · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "14,50 × 17,35 m"),
           ("Dormitoare", "3 + birou"),
           ("Băi", "2 + WC serviciu + spălătorie")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-72: grila de pereţi",
        "e măsurată pe radiografia planşei (56 px/m, cote 15080/18150).",
        "Terasa acoperită e scobită în volum, între matrimonial şi birou;",
        "carportul cu depozit intră în amprentă. Total cu anexe ≈ 142 m²."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/mara.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-24s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
