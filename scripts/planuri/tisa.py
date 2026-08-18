#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TISA — reprodusă din proiectul de referinţă 88-60 (17,75 × 16,85 m cu
streşini, 175 m² cu garaj dublu).

Planşa originală e cotată şi are suprafeţele scrise pe camere — suma lor dă
exact 175,03 m². Casă parter cu terasă acoperită pe toată faţada de nord
(prelungirea şarpantei), trei dormitoare + birou, două băi + WC tehnic,
bucătărie-dining de 22 m² deschisă spre terasă, hol central în T şi garaj
dublu de 35,3 m² ieşit spre sud.

Grila: 64–65 px/m pe radiografia planşei, verificată pe suprafeţele scrise.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 16530, 16790
IL, IA = L - 2 * PE, A - 2 * PE

# conturul: corpul principal + piciorul garajului dublu spre sud
CONTUR = [(-380, -380), (16150, -380), (16150, 9610),
          (8730, 9610), (8730, 16410), (2470, 16410),
          (2470, 9610), (-380, 9610)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── coloana de vest ──────────────────────────────────────────────────────────
n.camera("Dormitor 1", 0, 0, 3720, 3340)               # 12,44 în original
n.camera("Birou", 0, 3470, 3720, 2800)                 # 9,79
n.camera("Dormitor 2", 0, 6530, 3720, 2700)            # 10,70

# ── banda de nord ────────────────────────────────────────────────────────────
n.camera("Cămară", 3850, 0, 1550, 1550)                # 2,39
n.camera("Hol bucătărie", 3850, 1680, 1550, 2295)      # 3,33
n.camera("Bucătărie · dining", 5530, 0, 5560, 3975)    # 22,10
n.camera("Living", 11220, 0, 4550, 4430)               # 21,17

# ── holul central în T ───────────────────────────────────────────────────────
n.camera("Hol", 3850, 4105, 7240, 2295)                # 19,43 (cu braţele)
n.camera("Hol est", 11220, 4560, 1620, 1840)
n.camera("Coridor", 3850, 6530, 650, 2700)

# ── banda de sud ─────────────────────────────────────────────────────────────
n.camera("Baie", 4630, 6530, 2380, 2700)               # 7,62
n.camera("Tehnic", 7140, 6530, 2100, 2700)             # 6,45
n.camera("Antreu", 9370, 6530, 1980, 2700)             # 6,07
n.camera("Baie 2", 11480, 6530, 1360, 2700)            # 4,21
n.camera("Dormitor matrimonial", 12970, 4560, 2800, 4670)  # 14,02
n.camera("Garaj dublu", 2850, 9610, 5500, 6420)        # 35,31

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    (0, 3340, 3720, 130),                    # dormitor 1 | birou
    (0, 6400, 3720, 130),                    # birou | dormitor 2
    (3720, 0, 130, 9230),                    # coloana de vest | centru
    (3850, 1550, 1550, 130),                 # cămară | hol bucătărie
    (5400, 0, 130, 3975),                    # cămară + hol | bucătărie
    (3850, 3975, 7240, 130),                 # banda de nord | hol
    (11090, 0, 130, 6530),                   # bucătărie + hol | living + hol est
    (11220, 4430, 4550, 130),                # living | hol est + dormitor m.
    (3850, 6400, 8990, 130),                 # hol | banda de sud
    (12840, 4560, 130, 4670),                # hol est + baie 2 | dormitor m.
    (4500, 6530, 130, 2700),                 # coridor | baie
    (7010, 6530, 130, 2700),                 # baie | tehnic
    (9240, 6530, 130, 2700),                 # tehnic | antreu
    (11350, 6530, 130, 2700),                # antreu | baie 2
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (3785, 2200, 750, False),         # hol bucătărie → dormitor 1
    (4200, 1550, 700, True),          # hol bucătărie → cămară
    (4400, 3975, 800, True),          # hol bucătărie → hol
    (3785, 4400, 800, False),         # hol → birou
    (5800, 3975, 1500, True, False),  # hol ↔ bucătărie (trecere)
    (4000, 6400, 500, True, False),   # hol ↔ coridor (trecere)
    (3785, 7200, 800, False),         # coridor → dormitor 2
    (4800, 6400, 750, True),          # hol → baie
    (9500, 6400, 900, True),          # hol → antreu
    (9305, 7200, 750, False),         # antreu → tehnic
    (11155, 4800, 900, False, False), # hol ↔ hol est (trecere)
    (11800, 4430, 900, True),         # hol est → living
    (12905, 5000, 800, False),        # hol est → dormitor matrimonial
    (11500, 6400, 700, True),         # hol est → baie 2
    (7300, 9420, 900, True),          # tehnic → garaj
]:
    n.usa(*t)

# intrarea principală: din aleea de sud-est, în antreu
n.gol_ext(9800, 9230, 1000, 380, usa=True)
# poarta garajului dublu
n.gol_ext(4200, 16030, 2600, 380)

# ── goluri în anvelopă ──────────────────────────────────────────────────────
n.gol_ext(6000, -380, 2400, 380, usa=True)     # glisantele diningului spre terasă
n.fereastra("N", 800, 1800)                    # dormitor 1
n.fereastra("N", 12000, 2600)                  # living
n.fereastra("N", 4100, 800)                    # cămară
n.fereastra("V", 4200, 1500)                   # birou
n.fereastra("V", 7000, 1500)                   # dormitor 2
n.fereastra("S", 800, 1600)                    # dormitor 2, spre sud
n.fereastra("E", 1200, 2200)                   # living, spre est
n.fereastra("E", 6500, 1600)                   # dormitor matrimonial
n.fereastra("S", 13800, 1600)                  # dormitor matrimonial, spre sud

# ── zone punctate ───────────────────────────────────────────────────────────
n.zona("Terasă acoperită", -380, -2400, 16910, 2020)
n.zona("Intrare", 8730, 9610, 3200, 1300)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 900, 500, 1800, 2100).pune("dulap", 3000, 400, 620, 2400)
n.pune("canapea", 200, 3700, 950, 1900).pune("birou", 2900, 3700, 700, 1600)
n.pune("pat", 700, 6600, 1800, 2100).pune("dulap", 2350, 6300, 620, 2400)
n.pune("raft", 3950, 150, 1350, 500)
n.pune("blat", 5650, 100, 620, 3300).pune("plita", 5700, 800, 450, 700)
n.pune("chiuveta", 5700, 1900, 450, 600)
n.pune("insula", 7200, 1500, 900, 2000)
n.pune("masa", 8800, 1200, 1800, 1050)
n.pune("scaune", 8850, 700, 1700, 430).pune("scaune", 8850, 2300, 1700, 430)
n.pune("canapea", 12200, 500, 2800, 950).pune("canapea", 14600, 1450, 950, 1700)
n.pune("masuta", 13000, 1800, 900, 600).pune("tv", 11350, 1200, 250, 1800)
n.pune("cada", 4100, 8400, 1700, 750).pune("wc", 4100, 6700, 400, 600)
n.pune("lavoar", 5200, 6700, 650, 450).pune("lavoar", 5950, 6700, 500, 450)
n.pune("masina", 6800, 6700, 600, 600).pune("masina", 7500, 6700, 600, 600)
n.pune("raft", 6800, 8500, 2000, 620)
n.pune("dulap", 9200, 8500, 1800, 620)
n.pune("dus", 11450, 6700, 900, 900).pune("wc", 11450, 8400, 400, 600)
n.pune("lavoar", 12300, 7500, 500, 450)
n.pune("pat", 13400, 5300, 1800, 2100).pune("dulap", 13100, 8500, 2400, 620)

m = Model(
    nume="Tisa",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu terasă acoperită pe nord şi garaj dublu · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, prelungită peste terasa de nord",
    extra=[("Gabarit", "17,75 × 16,85 m (cu streşini)"),
           ("Dormitoare", "3 + birou"),
           ("Băi", "2 + tehnic + cămară")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-60, cotat 17,75 × 16,85 m,",
        "cu suprafeţele scrise pe camere — suma lor dă exact 175,03 m²."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/tisa.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-24s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
