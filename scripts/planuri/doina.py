#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DOINA — reprodusă din proiectul de referinţă 88-77 (17,15 × 8,75 m,
100 m² util).

Casă parter compactă, dreptunghiulară, cu terasă acoperită pe toată
latura de est. Trei dormitoare pe vest, living · dining de 31 m² pe est,
bucătărie deschisă pe colţul de sud-est. Suprafeţele scrise pe planşa
originală însumează 95,80 m² (fără camera tehnică).

Grila: calibrată la 51,3 px/m pe planşa 05.jpg (măsurat.json).
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 15280, 8750
IL, IA = L - 2 * PE, A - 2 * PE          # 14520 × 7990

CONTUR = [(-380, -380), (14900, -380), (14900, 8370), (-380, 8370)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── banda de nord ────────────────────────────────────────────────────────────
n.camera("Dormitor matrimonial", 0, 0, 3140, 3800)      # 11,93
n.camera("Dressing", 3270, 0, 1100, 2500)               # 2,75
n.camera("Baie mică", 3270, 2630, 1462, 1170)           # 1,71
n.camera("Dormitor 2", 4862, 0, 2355, 3800)             # 8,95
n.camera("Living · dining", 8830, 0, 5690, 5445)        # 30,98

# ── spinarea holului ─────────────────────────────────────────────────────────
n.camera("Hol", 2340, 3930, 6360, 1099)                 # 6,99

# ── banda de sud ─────────────────────────────────────────────────────────────
n.camera("Dormitor 3", 0, 5159, 3630, 2831)             # 10,28
n.camera("Baie", 3760, 5159, 1915, 2831)                # 5,42
n.camera("WC", 5805, 5159, 710, 2831)                   # 2,01
n.camera("Tehnic", 6645, 5159, 1015, 2831)              # 2,87
n.camera("Vestibul", 8960, 5575, 1453, 2415)            # 3,51
n.camera("Debara", 7790, 6067, 1040, 1923)              # 2,00
n.camera("Bucătărie", 10682, 5575, 3838, 2415)          # 9,27

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    (3140, 0, 130, 3800),                # dormitor matrimonial | dressing + baie mică
    (3270, 2500, 1462, 130),             # dressing | baie mică
    (4732, 0, 130, 3800),                # baie mică | dormitor 2
    (7217, 0, 130, 3800),                # dormitor 2 | nişa dulapurilor
    (8700, 0, 130, 5445),                # nişă + hol | living
    (0, 3800, 8700, 130),                # banda de nord | hol
    (2340, 5029, 6360, 130),             # hol | banda de sud
    (3630, 5159, 130, 2831),             # dormitor 3 | baie
    (5675, 5159, 130, 2831),             # baie | WC
    (6515, 5159, 130, 2831),             # WC | tehnic
    (7660, 5159, 130, 2831),             # tehnic | debara + vestibul
    (7790, 5575, 1170, 492),             # bloc instalaţii peste debara
    (8830, 6067, 130, 1923),             # debara | vestibul
    (8830, 5445, 5690, 130),             # living | vestibul + bucătărie
    (10413, 5575, 269, 2415),            # vestibul | bucătărie (bloc)
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (2360, 3800, 750, True),          # hol → dormitor matrimonial
    (3205, 800, 800, False),          # dormitor matrimonial → dressing
    (3600, 3800, 700, True),          # hol → baie mică
    (5800, 3800, 800, True),          # hol → dormitor 2
    (2800, 5029, 800, True),          # hol → dormitor 3
    (4400, 5029, 750, True),          # hol → baie
    (5900, 5029, 600, True),          # hol → WC
    (6900, 5029, 650, True),          # hol → tehnic
    (8765, 4000, 900, False, False),  # hol ↔ living (trecere)
    (9500, 5445, 900, True),          # vestibul → living
    (11500, 5445, 1600, True, False), # living ↔ bucătărie (trecere)
    (8895, 6300, 700, False),         # vestibul → debara
]:
    n.usa(*t)

# intrarea principală: din sud, în vestibul
n.gol_ext(9400, 7990, 1100, 380, usa=True)

# ── goluri în anvelopă ──────────────────────────────────────────────────────
n.fereastra("N", 800, 1800)                    # dormitor matrimonial
n.fereastra("N", 5300, 1500)                   # dormitor 2
n.fereastra("N", 10500, 2400)                  # living, spre nord
n.gol_ext(14520, 1500, 380, 2400, usa=True)    # living → terasa de est
n.fereastra("E", 6300, 1200)                   # bucătăria, spre terasă
n.fereastra("S", 1400, 1800)                   # dormitor 3
n.fereastra("S", 4300, 900)                    # baie
n.fereastra("S", 12200, 1500)                  # bucătăria
n.fereastra("V", 1200, 1800)                   # dormitor matrimonial
n.fereastra("V", 6200, 1800)                   # dormitor 3

# ── zone punctate ───────────────────────────────────────────────────────────
n.zona("Terasă", 14900, -380, 1870, 8750)
n.zona("Intrare", 9000, 8370, 2000, 1200)

# ── mobilier ────────────────────────────────────────────────────────────────
n.pune("pat", 500, 700, 1800, 2100).pune("dulap", 2400, 200, 620, 1800)
n.pune("dulap", 3320, 100, 1000, 600).pune("dulap", 3370, 1800, 1000, 600)
n.pune("wc", 3400, 3050, 400, 600).pune("lavoar", 4100, 2700, 550, 420)
n.pune("pat", 4950, 500, 1600, 2000).pune("dulap", 6500, 2800, 620, 900)
n.pune("dulap", 7450, 300, 1150, 3300)
n.pune("dulap", 200, 4100, 1900, 700)
n.pune("pat", 600, 5800, 1800, 2100).pune("dulap", 2900, 5350, 620, 1800)
n.pune("cada", 3850, 7100, 1700, 750).pune("lavoar", 3850, 5350, 650, 450)
n.pune("wc", 5100, 5350, 400, 600)
n.pune("wc", 5900, 5350, 400, 600).pune("lavoar", 5900, 7350, 550, 420)
n.pune("masina", 6750, 5350, 600, 600).pune("masina", 6750, 6100, 600, 600)
n.pune("raft", 7900, 6250, 500, 1600)
n.pune("dulap", 9900, 5700, 450, 1800)
n.pune("blat", 10800, 7280, 3600, 620).pune("plita", 11500, 7350, 700, 450)
n.pune("chiuveta", 13100, 7350, 600, 450)
n.pune("blat", 11200, 5900, 2200, 620).pune("scaune", 11300, 6650, 1900, 430)
n.pune("masa", 9400, 800, 1800, 1000)
n.pune("scaune", 9450, 400, 1700, 380).pune("scaune", 9450, 1830, 1700, 380)
n.pune("canapea", 12000, 2900, 2500, 950).pune("masuta", 12400, 4200, 900, 600)
n.pune("tv", 8880, 3000, 250, 1600)

m = Model(
    nume="Doina",
    titlu="PLAN PARTER",
    subtitlu="Casă parter compactă cu trei dormitoare şi terasă de est · sistem Polistibrick",
    acoperis="Şarpantă în două ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "17,15 × 8,75 m"),
           ("Dormitoare", "3"),
           ("Băi", "2 + WC de serviciu")],
    observatii=[
        "Reprodusă după proiectul de referinţă 88-77, cotat 17,15 × 8,75 m,",
        "cu suprafeţele scrise pe camere — sumă 95,80 m², fără camera tehnică."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/doina.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-24s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
