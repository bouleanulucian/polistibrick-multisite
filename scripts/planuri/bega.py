#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BEGA — reprodusă din proiectul de referinţă 88-23 (14,15 × 25,55 m,
194 m² cu garaj dublu).

Casă parter alungită pe nord-sud, cu o curte interioară cu deck între suita
matrimonială şi bucătărie, living de 34 m² deschis spre terasa de est şi
garaj dublu ieşit spre sud-vest. Suprafeţele sunt scrise pe planşa originală
(3,39 · 4,66 · 10,61 · 17,63 · 2,07 · 8,61 · 10,32 · 34,07 · 12,30 · 10,56 ·
14,38 · 3,38 · 3,96 · 6,88 · 9,01 · 38,08 — sumă ≈ 190 m²).

Grila: 89,5 px/m pe radiografia planşei, cotele scrise 14150 / 25550.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 14750, 24480
IL, IA = L - 2 * PE, A - 2 * PE

# conturul: corp alungit, curtea interioară scobită pe vest, garajul pe sud-vest
CONTUR = [(-380, -380), (10920, -380),
          (10920, 20030), (7310, 20030), (7310, 20530), (4020, 20530),
          (4020, 24100), (-3070, 24100), (-3070, 17320), (-380, 17320),
          (-380, 12420), (4120, 12420), (4120, 6860), (-380, 6860)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── suita matrimonială + camerele de nord ───────────────────────────────────
n.camera("Baie m.", 750, 0, 1850, 1830)                # 3,39
n.camera("Dressing", 2730, 0, 1790, 1830)
n.camera("Baie", 4650, 0, 2450, 1900)                  # 4,66
n.camera("Dormitor matrimonial", 0, 1960, 3900, 4520)  # 17,63
n.camera("WC", 4030, 2160, 1100, 1300)                 # 2,07
n.camera("Coridor NE", 5500, 2030, 1700, 1470)
n.camera("Dormitor 1", 7300, 0, 3240, 3270)            # 10,61
n.camera("Hol de noapte", 4100, 3500, 3100, 2780)      # 8,61
n.camera("Dormitor 2", 7300, 3400, 3240, 3190)         # 10,32

# ── zona de zi ───────────────────────────────────────────────────────────────
n.camera("Living", 4500, 6590, 6040, 5640)             # 34,07
n.camera("Bucătărie", 0, 12800, 3640, 3380)            # 12,30
n.camera("Dining", 6700, 12360, 3840, 2750)            # 10,56
n.camera("Hol", 3770, 12360, 2800, 5140)               # 14,38

# ── banda de sud ─────────────────────────────────────────────────────────────
n.camera("Cămară", 0, 16310, 2000, 1260)
n.camera("Tehnic", 2100, 16310, 1540, 1260)            # 3,38
n.camera("Coridor sud", 6700, 15240, 1370, 1690)
n.camera("Baie 2", 8200, 15240, 2340, 1690)            # 3,96
n.camera("Dormitor 3", 7060, 17060, 3480, 2590)        # 9,01
n.camera("Antreu", 4200, 17630, 2730, 2520)            # 6,88
n.camera("Garaj dublu", -2690, 17700, 6330, 6020)      # 38,08

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    (0, 1830, 5130, 130),                    # băile de sus | master + WC
    (2600, 0, 130, 1830),                    # baia m. | dressing
    (4520, 0, 130, 3460),                    # dressing + WC | baie + coridor
    (5130, 2030, 370, 1470),                 # WC | coridor NE (bloc instalaţii)
    (4650, 1900, 2550, 130),                 # baie | coridor NE
    (7200, 0, 130, 6590),                    # camerele de est | coridor + hol
    (7300, 3270, 3240, 130),                 # dormitor 1 | dormitor 2
    (3900, 1960, 130, 4320),                 # master | WC + hol
    (4100, 6280, 3100, 310),                 # hol de noapte | living
    (0, 6480, 3900, 380),                    # master | curtea interioară
    (4120, 6590, 380, 5640),                 # curtea | living (vitraj)
    (0, 12420, 3640, 380),                   # curtea | bucătărie
    (3640, 12360, 130, 5140),                # bucătărie | hol
    (3770, 12230, 6770, 130),                # living | hol + dining
    (6570, 12360, 130, 5140),                # hol | dining + coridor sud
    (6700, 15110, 3840, 130),                # dining | coridor sud + baie 2
    (8070, 15240, 130, 1690),                # coridor sud | baie 2
    (6700, 16930, 3840, 130),                # coridor sud + baie 2 | dormitor 3
    (0, 16180, 3640, 130),                   # bucătărie | cămară + tehnic
    (2000, 16310, 100, 1260),                # cămară | tehnic
    (0, 17570, 3640, 130),                   # cămară + tehnic | garaj
    (6930, 17630, 130, 2520),                # antreu | dormitor 3
    (4070, 17500, 2860, 130),                # hol | antreu
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (3050, 1830, 700, True),          # master → dressing
    (2665, 900, 750, False),          # dressing → baia m.
    (3965, 4500, 800, False),         # hol → dormitor matrimonial
    (4400, 3460, 700, True),          # hol → WC
    (6000, 3500, 900, True, False),   # hol ↔ coridor NE (trecere)
    (5700, 1900, 750, True),          # coridor NE → baie
    (7265, 2300, 800, False),         # coridor NE → dormitor 1
    (7235, 4200, 800, False),         # hol → dormitor 2
    (5000, 6280, 1600, True, False),  # hol ↔ living (trecere)
    (4500, 12230, 1200, True, False), # living ↔ hol (trecere)
    (7500, 12230, 1800, True, False), # living ↔ dining (trecere)
    (3705, 13500, 900, False),        # hol → bucătărie
    (6635, 13000, 1200, False, False),# hol ↔ dining (trecere)
    (900, 16180, 800, True),          # bucătărie → cămară
    (3705, 16600, 700, False),        # hol → tehnic
    (7150, 15110, 800, True, False),  # dining ↔ coridor sud (trecere)
    (8135, 15700, 750, False),        # coridor sud → baie 2
    (7250, 16930, 750, True),         # coridor sud → dormitor 3
    (4800, 17500, 1000, True),        # hol → antreu
    (6995, 18000, 800, False),        # antreu → dormitor 3
    (2700, 17570, 800, True),         # tehnic → garaj
]:
    n.usa(*t)

# intrarea principală: din sud, în antreu
n.gol_ext(5000, 20150, 1100, 380, usa=True)
# poarta garajului dublu
n.gol_ext(-1800, 23720, 2600, 380)

# ── goluri în anvelopă ──────────────────────────────────────────────────────
n.fereastra("N", 1200, 900)                    # baia m.
n.fereastra("N", 5200, 900)                    # baie
n.fereastra("N", 8000, 1800)                   # dormitor 1
n.fereastra("V", 3500, 2000)                   # dormitor matrimonial
n.gol_ext(4120, 7500, 380, 3000, usa=True)     # living → curtea interioară
n.gol_ext(10540, 8000, 380, 3600, usa=True)    # living → terasa de est
n.fereastra("E", 1000, 1600)                   # dormitor 1
n.fereastra("E", 4200, 1600)                   # dormitor 2
n.fereastra("E", 13200, 1800)                  # dining
n.fereastra("V", 13500, 1500)                  # bucătăria
n.gol_ext(8000, 19650, 1600, 380)              # dormitor 3, spre sud

# ── zone punctate ───────────────────────────────────────────────────────────
n.zona("Curte interioară", -380, 6860, 4500, 5560)
n.zona("Terasă", 10920, -380, 2500, 15800)
n.zona("Intrare", 4200, 20530, 3000, 1300)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("wc", 900, 150, 400, 600).pune("lavoar", 1900, 150, 650, 450)
n.pune("dulap", 2850, 150, 1550, 620)
n.pune("cada", 4800, 150, 1700, 750).pune("lavoar", 4200, 2300, 500, 400)
n.pune("wc", 4200, 2900, 400, 600)
n.pune("pat", 1000, 2600, 1800, 2100).pune("dulap", 100, 2100, 620, 1800)
n.pune("pat1", 8000, 300, 1600, 2000).pune("dulap", 9800, 300, 620, 1800)
n.pune("pat1", 8000, 3700, 1600, 2000).pune("dulap", 9800, 4500, 620, 1800)
n.pune("canapea", 5200, 8200, 950, 2600).pune("canapea", 6150, 10300, 2400, 950)
n.pune("masuta", 6500, 9000, 900, 700).pune("tv", 4650, 8500, 250, 1800)
n.pune("blat", 100, 12950, 620, 3100).pune("plita", 150, 13500, 450, 700)
n.pune("chiuveta", 150, 14700, 450, 600).pune("insula", 1600, 13600, 900, 1800)
n.pune("masa", 7600, 13000, 1900, 1050)
n.pune("scaune", 7650, 12550, 1800, 430).pune("scaune", 7650, 14100, 1800, 430)
n.pune("raft", 100, 16400, 1800, 500).pune("masina", 2300, 16450, 600, 600)
n.pune("dus", 9400, 15350, 900, 900).pune("wc", 8400, 15350, 400, 600)
n.pune("lavoar", 8400, 16300, 500, 400)
n.pune("pat1", 8600, 17400, 1600, 2000).pune("dulap", 7200, 17300, 620, 1600)
n.pune("dulap", 4400, 19400, 2200, 620)

m = Model(
    nume="Bega",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu curte interioară, terasă pe est şi garaj dublu · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "14,15 × 25,55 m"),
           ("Dormitoare", "4"),
           ("Băi", "3 + WC + tehnic")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-23, cotat 14,15 × 25,55 m,",
        "cu suprafeţele scrise pe camere. Curte interioară cu deck."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/bega.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-24s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
