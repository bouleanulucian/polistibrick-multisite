#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LENA — reprodusă din proiectul de referinţă 99-31 (14,75 × 15,95 m,
226 m² cu etaj şi garaj dublu).

Casă cu etaj, în plan pinwheel: living pe nord-est, aripa de vest cu
camera tehnică şi garajul dublu, bucătăria pe sud-est. La etaj: suita
matrimonială cu două dressinguri şi baie proprie, două dormitoare,
baia copiilor şi debara. Suprafeţele scrise pe planşele originale
însumează 226 m².
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

# ═══ PARTER ══════════════════════════════════════════════════════════════════
p = Nivel("PARTER", 14030, 16110)
p.poligon([(-380, 5110), (4590, 5110), (4590, 1160), (7600, 1160),
           (7600, -380), (13650, -380), (13650, 8830), (13005, 8830),
           (13005, 12100), (5920, 12100), (5920, 15730), (-380, 15730)])

p.camera("Living", 7980, 0, 5290, 4840)                 # 25,60
p.camera("Dining", 9670, 4970, 3600, 3480)              # 12,53
p.camera("Hol cu scară", 6100, 4970, 3440, 3215)        # 11,06
p.camera("Birou", 4970, 1540, 2880, 3320)               # 9,56
p.camera("Coridor", 4230, 5490, 1740, 3190)             # 5,55
p.camera("Baie de serviciu", 6100, 8315, 1100, 2790)    # 3,07
p.camera("Tehnic · spălătorie", 0, 5490, 4100, 3710)    # 15,21
p.camera("Antreu", 7330, 8315, 1865, 3405)              # 6,35
p.camera("Bucătărie", 9325, 8580, 3300, 3140)           # 10,36
p.camera("Garaj dublu", 0, 9330, 5540, 6020)            # 33,35

for w in [
    (4100, 5490, 130, 3710),             # tehnic | coridor
    (0, 9200, 5540, 130),                # tehnic | garaj
    (5970, 5490, 130, 5615),             # coridor + WC, peretele de est
    (4970, 4860, 2880, 110),             # birou | hol
    (4970, 4970, 1130, 520),             # bloc între birou şi coridor
    (7850, 1540, 130, 3320),             # birou | living
    (9540, 4970, 130, 3215),             # hol | dining
    (6100, 8185, 3440, 130),             # hol | antreu + WC
    (7200, 8315, 130, 3405),             # WC | antreu
    (9195, 8315, 130, 3405),             # antreu | bucătărie
    (9325, 8450, 3300, 130),             # dining | bucătărie
    (6100, 11105, 1100, 615),            # bloc depozitare sub WC
]:
    p.perete(*w)

for t in [
    (8000, 8185, 900, True),            # antreu → hol
    (2000, 9200, 900, True),            # tehnic → garaj
    (4165, 6500, 900, False),           # tehnic → coridor
    (6035, 6000, 900, False, False),    # coridor ↔ hol (trecere)
    (6500, 4860, 900, True),            # hol → birou
    (7265, 8600, 750, False),           # antreu → baie de serviciu
    (8100, 4840, 1300, True, False),    # hol ↔ living (trecere)
    (9605, 5500, 1800, False, False),   # hol ↔ dining (trecere)
    (10500, 4840, 2000, True, False),   # living ↔ dining (trecere)
    (10500, 8450, 1000, True, False),   # dining ↔ bucătărie (trecere)
]:
    p.usa(*t)

# intrarea principală: din sud, în antreu
p.gol_ext(7600, 11720, 1100, 380, usa=True)
# porţile garajului dublu, spre sud
p.gol_ext(700, 15350, 2000, 380)
p.gol_ext(2900, 15350, 2000, 380)

p.fereastra("N", 8700, 2400)                    # living
p.gol_ext(5500, 1160, 1500, 380)                # birou, spre nord
p.fereastra("E", 2000, 2400)                    # living, spre est
p.gol_ext(13270, 6200, 380, 1800, usa=True)     # dining → terasa de est
p.gol_ext(12625, 9500, 380, 1200)               # bucătăria, spre est
p.gol_ext(10200, 11720, 1400, 380)              # bucătăria, spre sud
p.fereastra("V", 6500, 1200)                    # tehnic
p.fereastra("V", 11000, 900)                    # garaj

p.zona("Terasă", 13650, 3500, 2200, 5330)
p.zona("Intrare", 6950, 12100, 2600, 1400)
p.zona("Scară", 6250, 5100, 1200, 2800)

p.pune("canapea", 12200, 1000, 950, 2800).pune("masuta", 10900, 2000, 900, 600)
p.pune("tv", 8100, 1600, 250, 1800).pune("soba", 8100, 3800, 700, 700)
p.pune("masa", 10800, 6000, 1900, 1050)
p.pune("scaune", 10850, 5550, 1800, 430).pune("scaune", 10850, 7100, 1800, 430)
p.pune("blat", 9425, 11000, 3000, 620).pune("plita", 10000, 11080, 700, 450)
p.pune("chiuveta", 11500, 11080, 600, 450).pune("blat", 12000, 8700, 620, 2200)
p.pune("canapea", 5100, 1800, 2400, 950).pune("masa", 5300, 3600, 1400, 700)
p.pune("masina", 300, 5700, 600, 600).pune("masina", 1000, 5700, 600, 600)
p.pune("soba", 3300, 8300, 700, 700).pune("raft", 300, 6600, 500, 2000)
p.pune("wc", 6250, 8500, 400, 600).pune("lavoar", 6250, 9600, 550, 420)
p.pune("dulap", 8500, 8500, 620, 1800)

# ═══ ETAJ ════════════════════════════════════════════════════════════════════
e = Nivel("ETAJ", 9510, 12840)
e.poligon([(-380, 720), (2650, 720), (2650, -380), (9130, -380),
           (9130, 12216), (4990, 12216), (4990, 12460), (-380, 12460)])

e.camera("Dormitor matrimonial", 3030, 0, 3900, 4830)   # 18,84
e.camera("Dressing", 7060, 0, 1690, 2284)               # 3,86
e.camera("Dressing 2", 7060, 2414, 1690, 2286)          # 3,86
e.camera("Baie matrimonială", 0, 1100, 2560, 3730)      # 9,55
e.camera("Hol etaj", 1650, 4960, 2960, 2950)            # 8,73
e.camera("Debara", 0, 5090, 1520, 2200)                 # 3,34
e.camera("Dormitor 2", 4740, 4960, 4010, 3791)          # 15,20
e.camera("Dormitor 3", 0, 8097, 4610, 3983)             # 18,36
e.camera("Baie copii", 4740, 8881, 4010, 2955)          # 11,85

for w in [
    (2560, 1100, 470, 3730),             # bloc baie | dormitor matrimonial
    (6930, 0, 130, 4830),                # dormitor matrimonial | dressinguri
    (7060, 2284, 1690, 130),             # dressing | dressing 2
    (7060, 4700, 1690, 130),             # dressing 2, peretele de jos
    (0, 4830, 8750, 130),                # banda de nord | hol + dormitor 2
    (4610, 4960, 130, 3791),             # hol | dormitor 2
    (1520, 5090, 130, 2200),             # debara | hol
    (0, 4960, 1520, 130),                # bloc peste debara
    (0, 7910, 4610, 187),                # hol | dormitor 3
    (4740, 8751, 4010, 130),             # dormitor 2 | baie copii
    (4610, 8097, 130, 3983),             # dormitor 3 | baie copii
    (0, 7290, 1520, 620),                # bloc sub debara (gol scară)
]:
    e.perete(*w)

for t in [
    (1800, 4830, 700, True),            # hol → baie matrimonială
    (3300, 4830, 900, True),            # hol → dormitor matrimonial
    (6995, 900, 800, False),            # dormitor matrimonial → dressing
    (6995, 3000, 800, False),           # dormitor matrimonial → dressing 2
    (1585, 5400, 800, False),           # hol → debara
    (4675, 5500, 900, False),           # hol → dormitor 2
    (2500, 7910, 900, True),            # hol → dormitor 3
    (4675, 9500, 800, False),           # dormitor 3 → baie copii
]:
    e.usa(*t)

e.fereastra("N", 4500, 1800)                    # dormitor matrimonial
e.gol_ext(800, 720, 1000, 380)                  # baie matrimonială, spre nord
e.fereastra("E", 1000, 900)                     # dressing
e.fereastra("E", 6500, 1800)                    # dormitor 2
e.fereastra("E", 9900, 900)                     # baie copii
e.gol_ext(1500, 12080, 1800, 380)               # dormitor 3, spre sud
e.gol_ext(6000, 11836, 1000, 380)               # baie copii, spre sud
e.fereastra("V", 2500, 900)                     # baie matrimonială
e.fereastra("V", 9700, 1800)                    # dormitor 3

e.zona("Scară", 1750, 5100, 1100, 2600)

e.pune("pat", 4400, 700, 1800, 2100).pune("dulap", 3150, 3800, 620, 900)
e.pune("dulap", 7150, 100, 1500, 600).pune("dulap", 7150, 4000, 1500, 600)
e.pune("cada", 150, 1250, 1700, 750).pune("dus", 1750, 1250, 750, 750)
e.pune("lavoar", 200, 4200, 650, 450).pune("wc", 1500, 4150, 400, 600)
e.pune("raft", 100, 5200, 450, 1900)
e.pune("pat", 5400, 5400, 1800, 2100).pune("dulap", 8000, 5100, 620, 1800)
e.pune("pat", 700, 9000, 1800, 2100).pune("dulap", 3800, 8300, 620, 1800)
e.pune("masa", 2800, 11200, 1200, 700)
e.pune("cada", 6900, 9100, 1600, 750).pune("dus", 4900, 9200, 900, 900)
e.pune("lavoar", 4900, 10800, 650, 450).pune("wc", 5800, 11200, 400, 600)
e.pune("masina", 8000, 11100, 600, 600)

m = Model(
    nume="Lena",
    titlu="PLAN PARTER + ETAJ",
    subtitlu="Casă cu etaj, trei dormitoare, birou şi garaj dublu · sistem Polistibrick",
    acoperis="Şarpantă în două ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "14,75 × 15,95 m"),
           ("Dormitoare", "3 + birou"),
           ("Băi", "3 + WC de serviciu")],
    observatii=[
        "Reprodusă după proiectul de referinţă 99-31, cotat 14,75 × 15,95 m,",
        "cu suprafeţele scrise pe camere — sumă 226 m², cu etaj şi garaj dublu."])
m.nivel(p)
m.nivel(e)

if __name__ == "__main__":
    for niv in (p, e):
        pr = verifica(niv)
        print("%s circulaţie:" % niv.nume, "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/lena.svg")
    print("amprentă %.1f m² · util %.1f m²"
          % (p.amprenta, p.util + e.util))
    for niv in (p, e):
        for c in niv.camere:
            print("   %-24s %5.2f × %5.2f = %5.1f m²"
                  % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
