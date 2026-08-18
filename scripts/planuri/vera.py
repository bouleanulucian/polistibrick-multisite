#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VERA — reprodusă din proiectul de referinţă 88-49 (19,85 × 20,45 m,
200 m² cu garaj dublu).

Casă parter în L: corpul principal pe nord-sud (patru dormitoare, dintre care
suita matrimonială cu dressing, plus living · dining de ~38 m² pe sud) şi
aripa garajului dublu spre est, cu terasa prinsă în colţul dintre ele.
Suprafeţele scrise pe planşa originală însumează 199,80 m².

Grila: reconstruită din suprafeţele scrise şi topologia planşei.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 16530, 21750
IL, IA = L - 2 * PE, A - 2 * PE

# conturul: corp principal + crestătura terasei NE + aripa garajului
CONTUR = [(-380, -380), (7400, -380), (7400, 6330), (9720, 6330),
          (9720, 8320), (16150, 8320), (16150, 14950), (9720, 14950),
          (9720, 21370), (-380, 21370)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── dormitoarele de nord ─────────────────────────────────────────────────────
n.camera("Dormitor 1", 0, 0, 3500, 3450)               # 12,07
n.camera("Dormitor 2", 3630, 0, 3640, 3450)            # 12,54
n.camera("Coridor N", 0, 3580, 4150, 750)
n.camera("Dormitor 3", 0, 4460, 4150, 3000)            # 12,46
n.camera("Hol de noapte", 4280, 3580, 950, 7400)       # 13,83 (spinarea)
n.camera("Dressing", 5360, 3580, 1910, 3000)           # 5,82
n.camera("Dormitor matrimonial", 5360, 6710, 3980, 4140)   # 15,03

# ── banda de mijloc ──────────────────────────────────────────────────────────
n.camera("Baie", 0, 7590, 2280, 2260)                  # 5,15
n.camera("Cămară", 2790, 7590, 1360, 2260)             # 3,07
n.camera("Spălătorie", 0, 9980, 2660, 980)             # 2,68
n.camera("Baie 3", 2790, 9980, 1360, 2450)             # 3,34
n.camera("Bucătărie", 0, 11090, 2660, 3500)            # 9,30
n.camera("Coridor", 4280, 11110, 1170, 3480)
n.camera("Baie 2", 5580, 11110, 2170, 2600)            # 5,65
n.camera("Vestibul", 7880, 11110, 1460, 3480)          # 5,34
n.camera("Debara", 2790, 12560, 1360, 2030)

# ── zona de zi ───────────────────────────────────────────────────────────────
n.camera("Hol de zi", 0, 14720, 6150, 2240)            # 12,61
n.camera("Antreu", 6280, 14720, 3060, 2240)            # 7,65
n.camera("Living · dining", 0, 17090, 9340, 3900)      # 37,75
n.camera("Garaj dublu", 9720, 8700, 6050, 5870)        # 35,51

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    (0, 3450, 7270, 130),                    # dormitoarele 1–2 | coridor N + hol
    (3500, 0, 130, 3450),                    # dormitor 1 | dormitor 2
    (0, 4330, 4150, 130),                    # coridor N | dormitor 3
    (4150, 3580, 130, 11140),                # vest | spinarea holului
    (5230, 3580, 130, 7270),                 # hol | dressing + master
    (5360, 6580, 3980, 130),                 # dressing | master
    (0, 7460, 4150, 130),                    # dormitor 3 | baie + cămară
    (2410, 7590, 380, 2260),                 # baie | cămară (bloc instalaţii)
    (0, 9850, 4150, 130),                    # baie + cămară | spălătorie + baie 3
    (0, 10960, 2660, 130),                   # spălătorie | bucătărie
    (2660, 9850, 130, 4740),                 # bucătărie | baie 3 + debara
    (2790, 12430, 1360, 130),                # baie 3 | debara
    (5360, 10850, 3980, 260),                # master | banda vestibulului
    (5450, 11110, 130, 3480),                # coridor | baie 2
    (7750, 11110, 130, 3480),                # baie 2 | vestibul
    (5580, 13710, 2170, 880),                # bloc dulapuri sub baia 2
    (0, 14590, 9340, 130),                   # banda de mijloc | hol de zi + antreu
    (6150, 14720, 130, 2240),                # hol de zi | antreu
    (0, 16960, 9340, 130),                   # hol de zi + antreu | living
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (1500, 3450, 800, True),          # coridor N → dormitor 1
    (4400, 3450, 800, True),          # hol → dormitor 2
    (1500, 4330, 800, True),          # coridor N → dormitor 3
    (4215, 3700, 600, False, False),  # coridor N ↔ hol (trecere)
    (5295, 4200, 800, False),         # hol → dressing
    (5295, 7500, 800, False),         # hol → dormitor matrimonial
    (4215, 8000, 750, False),         # hol → cămară
    (900, 9850, 750, True),           # spălătorie → baie
    (900, 10960, 750, True),          # bucătărie → spălătorie
    (4215, 10100, 700, False),        # hol → baie 3
    (4215, 13000, 700, False),        # coridor → debara
    (5515, 11500, 750, False),        # coridor → baie 2
    (4400, 10980, 800, True, False),  # hol ↔ coridor (trecere)
    (8300, 14590, 800, True),         # vestibul → antreu
    (4500, 14590, 900, True, False),  # coridor ↔ hol de zi (trecere)
    (1200, 14590, 1400, True, False), # bucătărie ↔ hol de zi (trecere)
    (2500, 16960, 1800, True, False), # hol de zi ↔ living (trecere)
    (6215, 15400, 900, False),        # hol de zi → antreu
    (9530, 12000, 900, False),        # vestibul → garaj
]:
    n.usa(*t)

# intrarea principală: din est, lângă garaj, în antreu
n.gol_ext(9340, 15400, 380, 1100, usa=True)
# poarta garajului dublu, spre nord
n.gol_ext(11500, 8320, 2600, 380)

# ── goluri în anvelopă ──────────────────────────────────────────────────────
n.fereastra("N", 800, 1800)                    # dormitor 1
n.fereastra("N", 4500, 1800)                   # dormitor 2
n.gol_ext(7270, 900, 380, 1800)                # dormitor 2, spre terasa NE
n.gol_ext(9340, 8000, 380, 1800)               # dormitor matrimonial, spre est
n.fereastra("V", 5200, 1800)                   # dormitor 3
n.fereastra("V", 8200, 900)                    # baie
n.fereastra("V", 12000, 1500)                  # bucătăria
n.fereastra("V", 18500, 2000)                  # living, spre vest
n.gol_ext(2000, 20990, 2800, 380, usa=True)    # living → terasa de sud
n.gol_ext(9340, 18500, 380, 2200)              # living, spre est

# ── zone punctate ───────────────────────────────────────────────────────────
n.zona("Terasă", 7400, -380, 1940, 6710)
n.zona("Terasă", 9720, -380, 4200, 8300)
n.zona("Terasă", -380, 21370, 6000, 1800)
n.zona("Intrare", 10100, 15400, 1800, 1100)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 800, 500, 1800, 2100).pune("dulap", 2800, 300, 620, 1800)
n.pune("pat", 4600, 500, 1800, 2100).pune("dulap", 6600, 300, 620, 1800)
n.pune("pat", 1200, 4900, 1800, 2100).pune("dulap", 3450, 4700, 620, 1800)
n.pune("dulap", 5500, 3700, 620, 1400).pune("dulap", 6600, 3700, 620, 1400)
n.pune("pat", 6300, 7300, 1800, 2100).pune("dulap", 8600, 7000, 620, 2400)
n.pune("cada", 300, 7700, 1700, 750).pune("lavoar", 300, 9200, 650, 450)
n.pune("wc", 1700, 9200, 400, 600)
n.pune("raft", 2900, 7700, 1150, 500)
n.pune("masina", 200, 10100, 600, 600).pune("masina", 900, 10100, 600, 600)
n.pune("dus", 2900, 10100, 900, 900).pune("wc", 2900, 11600, 400, 600)
n.pune("blat", 100, 11200, 620, 3200).pune("plita", 150, 11800, 450, 700)
n.pune("chiuveta", 150, 13000, 450, 600)
n.pune("dus", 5700, 11250, 900, 900).pune("wc", 7200, 11250, 400, 600)
n.pune("lavoar", 5700, 12800, 650, 450)
n.pune("raft", 2900, 12700, 1150, 500)
n.pune("dulap", 8000, 11250, 620, 2000)
n.pune("dulap", 6500, 15000, 2400, 620)
n.pune("masa", 1200, 17600, 1900, 1050)
n.pune("scaune", 1250, 17150, 1800, 430).pune("scaune", 1250, 18700, 1800, 430)
n.pune("canapea", 5200, 18200, 2800, 950).pune("canapea", 7950, 19150, 950, 1700)
n.pune("masuta", 6000, 19400, 900, 600).pune("tv", 4500, 18400, 250, 1800)

m = Model(
    nume="Vera",
    titlu="PLAN PARTER",
    subtitlu="Casă parter în L cu patru dormitoare şi garaj dublu · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "19,85 × 20,45 m"),
           ("Dormitoare", "4"),
           ("Băi", "3 + spălătorie + cămară")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-49, cotat 19,85 × 20,45 m,",
        "cu suprafeţele scrise pe camere — sumă 199,80 m², cu garajul dublu."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/vera.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-24s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
