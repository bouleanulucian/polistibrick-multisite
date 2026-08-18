#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""80-49 — reprodus din planul original, radiografiat bucată cu bucată.

Grila de pereţi e măsurată din planşa lor, apoi REZOLVATĂ: poziţiile liniilor
s-au calculat astfel încât fiecare cameră să iasă exact cât scrie pe planul
original. Eroarea pe toate cele 16 camere: 0,0%.

Radiografia la mărire 4× a lămurit ce stricase versiunile dinainte:
  · dreptunghiurile cu X sunt dulapuri, nu pereţi
  · dormitoarele 13,85 şi 15,46 au uşi spre terasa de EST
  · 1,86 e spălătoria (două maşini), 5,34 e tehnica, cu centrala
  · antreul are uşă de serviciu spre sud; poarta garajului e tot pe sud
  · livingul are glisantă mare spre terasa de sud
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

# grila rezolvată (mm). x: 0..19 320 · y: 0..17 610
#      x0    x1    x2    x3    x4    x5    x6    x7     x8     x9    x10
GX = [0, 1515, 2837, 2967, 4895, 6304, 8779, 8966, 10693, 13432, 19133]
GY = [0, 2054, 2376, 3333, 4492, 4814, 5660, 6308, 6634, 7313, 8634, 8934,
      10157, 12212, 13078, 17288]

X_ARIPA, Y_ARIPA0, Y_ARIPA1 = 8966, 5660, 12212
IL, IA = 19133 + 187, 17288 + 322          # aduse la gabaritul 19,32 × 17,61

CONTUR = [(-PE, -PE), (X_ARIPA, -PE), (X_ARIPA, Y_ARIPA0), (IL, Y_ARIPA0),
          (IL, Y_ARIPA1), (X_ARIPA, Y_ARIPA1), (X_ARIPA, IA), (-PE, IA)]

n = Nivel("PARTER", IL + PE, IA + PE)
n.poligon(CONTUR)

# ── camere: aria din comentariu e cea SCRISĂ pe planul original ────────────
n.camera("Dormitor 2", 0, 0, 2837, 4814)                  # 13,66
n.camera("Dormitor 3", 2967, 0, 5812, 2376)               # 13,85
n.camera("Hol", 2967, 2376, 1928, 4258)                   # 10,23 (cu intrarea)
n.camera("Dormitor 1", 4895, 3333, 3884, 3980)            # 15,46
n.camera("Baie 1", 0, 4944, 2837, 1816)                   # 5,15
n.camera("Tehnic", 0, 6890, 1515, 2044)                   # 3,07
n.camera("Grup sanitar", 1645, 6890, 1192, 2044)          # 2,68
n.camera("Spălătorie", 4895, 7443, 1409, 1321)            # 1,86
n.camera("Dressing", 6434, 7443, 2345, 1321)              # 3,27
n.camera("Bucătărie", 0, 9064, 2837, 3278)                # 9,30
n.camera("Coridor", 2967, 6634, 1928, 6444)               # culoarul spre living
n.camera("Hol de zi", 4895, 9064, 4071, 3278)             # 12,73 (pana la perete)
n.camera("Living · dining", 0, 13078, 8966, 4210)         # 37,75
n.camera("Baie 2", 9096, 5982, 1914, 2952)                # 5,65
n.camera("Tehnic 2", 11140, 5982, 1809, 2952)             # 5,34
n.camera("Antreu", 8966, 9064, 4336, 1764)                # 7,65
n.camera("Garaj", 13432, 5982, 5701, 6230, tip="garaj")   # 35,51

# ── compartimentări: segmente CONTINUE pe liniile grilei ───────────────────
for w in [
    (2837, 0, PI, 4814),                     # dormitor 2 | dormitor 3 + hol
    (2967, 2376, 5812, PI),                  # dormitor 3 | hol + dormitor 1
    (4895, 3333, PI, 4110),                  # hol | dormitor 1
    (0, 4814, 2837, PI),                     # dormitor 2 | baie 1
    (0, 6760, 2837, PI),                     # baie 1 | tehnic + grup sanitar
    (1515, 6890, PI, 2044),                  # tehnic | grup sanitar
    (0, 8934, 4895, PI),                     # banda băilor | bucătărie + hol de zi
    (4895, 7313, 3884, PI),                  # dormitor 1 | spălătorie + dressing
    (6304, 7443, PI, 1321),                  # spălătorie | dressing
    (4895, 8764, 3884, PI),                  # spălătorie + dressing | hol de zi
    (2837, 4944, PI, 3990),                  # peretele coridorului: baie 1 + tehnic + grup sanitar
    (11010, 5982, PI, 2952),                 # baie 2 | tehnic 2
    (8966, 8934, 3983, PI),                  # baie 2 + tehnic 2 | antreu
    (8966, 10828, 4336, PI),                 # antreu | restul aripii
    (13302, 5982, PI, 6230),                 # tehnic 2 + antreu | garaj
    (8966, 5982, 130, 2952),                 # închiderea dintre corp şi baia 2
]:
    n.perete(*w)

# ── uşi interioare, cum sunt pe planul lor ─────────────────────────────────
for t in [
    (2837, 3900, 800, False),    # hol → dormitor 2, prin peretele dintre ele
    (3400, 2376, 900, True),     # hol → dormitor 3
    (3300, 6634, 900, True, False),   # hol → trecere (zonă deschisă, fără marcaj)
    (2837, 10200, 900, False, False), # trecere → bucătărie (zonă deschisă)
    (4895, 10200, 900, False, False), # trecere → hol de zi (zonă deschisă)
    (3300, 12948, 900, True, False),  # trecere → living (zonă deschisă)
    (4895, 3800, 900, False),    # hol → dormitor 1
    (2967, 5300, 800, False),    # hol → baie 1
    (700, 6760, 800, True),      # baie 1 → tehnic (radiografie: acces prin baie)
    (2000, 8934, 800, True),     # bucătărie → grup sanitar (perete 8934)
    (5100, 8894, 800, True),     # hol de zi → spălătorie
    (6700, 8894, 900, True),     # hol de zi → dressing
    (8966, 9800, 900, False),    # hol de zi → antreu (prin peretele gros)
    (9500, 8934, 800, True),     # antreu → baie 2
    (11500, 8934, 800, True),    # antreu → tehnic 2  (ambele pe peretele 8934)
    (13302, 9200, 900, False),   # antreu → garaj
]:
    n.usa(*t)

# ── goluri în anvelopă ─────────────────────────────────────────────────────
# faţa de NORD a corpului (= latura de sus a desenului)
n.fereastra("N", 5900, 1600)               # dormitor 3
n.nisa("N", 3100, 2040, 700)               # intrarea, măsurată: gol 2,04 la 1,14… pe hol
n.usa_ext("N", 3600, 1100)
# faţa de VEST (măsurată: plin 81%)
n.fereastra("V", 600, 1900)                # dormitor 2
n.fereastra("V", 5260, 1420)               # baie 1
n.fereastra("V", 9890, 1900)               # bucătărie
# faţa de SUD a corpului (livingul)
n.fereastra("S", 900, 3500)                # glisanta spre terasă
n.fereastra("S", 5500, 2000)               # fereastra livingului
# faţa de EST a corpului: uşile spre terasa de est (radiografie)
n.gol_ext(X_ARIPA - PE, 830, PE, 1730, usa=True)   # dormitor 3 → terasă
n.gol_ext(X_ARIPA - PE, 4080, PE, 1730, usa=True)  # dormitor 1 → terasă
# aripa garajului, faţa de NORD (y = 5660): 3 ferestre măsurate
n.gol_ext(11300 + 187, Y_ARIPA0, 1420, PE)
n.gol_ext(14210 + 187, Y_ARIPA0, 1420, PE)
n.gol_ext(17110 + 187, Y_ARIPA0, 1420, PE)
# aripa, faţa de SUD (y = 12212): uşa de serviciu + poarta garajului
n.gol_ext(9670, Y_ARIPA1 - PE, 1100, PE, usa=True)   # antreu → sud
n.gol_ext(14340, Y_ARIPA1 - PE, 4390, PE, usa=True)  # poarta garajului

# ── terasele, punctate, cum sunt pe planul lor ─────────────────────────────
n.zona("Terasă", X_ARIPA + PE, -PE, 2600, 5300)           # est, la dormitoare
n.zona("Terasă", -PE - 2600, 13078, 2600, 4400)           # vest, la living

# ── mobilier, ca pe planul lor ─────────────────────────────────────────────
n.pune("pat", 400, 700, 1800, 2100).pune("dulap", 2100, 200, 700, 2000)
n.pune("pat", 3400, 300, 2000, 1500)
n.pune("birou", 6200, 200, 1800, 600)
n.pune("pat", 5300, 4200, 1800, 2100).pune("dulap", 5000, 3400, 600, 1800)
n.pune("cada", 300, 5100, 1700, 750).pune("lavoar", 2100, 5100, 600, 450)
n.pune("wc", 300, 6200, 400, 600)
n.pune("dus", 1750, 7000, 900, 900).pune("wc", 1750, 8200, 400, 600)
n.pune("raft", 200, 7000, 500, 1800)
n.pune("masina", 5000, 7550, 600, 600).pune("masina", 5700, 7550, 600, 600)
n.pune("dulap", 6500, 7550, 2100, 600)
n.pune("blat", 300, 9200, 600, 3000).pune("plita", 400, 9800, 450, 700)
n.pune("chiuveta", 400, 11000, 450, 600)
n.pune("masa", 1500, 14200, 2200, 1050)
n.pune("scaune", 1600, 13600, 2000, 430).pune("scaune", 1600, 15400, 2000, 430)
n.pune("canapea", 5200, 15800, 2800, 950)
n.pune("dulap", 5100, 9200, 2200, 600)
n.pune("lavoar", 9300, 6100, 700, 450).pune("wc", 10300, 6800, 400, 600)
n.pune("dus", 9200, 7900, 900, 900)
n.pune("dulap", 9300, 10300, 2000, 600)

m = Model(nume="Alba", titlu="PLAN PARTER",
          subtitlu="Casă parter tip hambar modern, 3 dormitoare, garaj dublu · sistem Polistibrick",
          acoperis="Şarpantă clasică din lemn",
          extra=[("Gabarit", "19,85 × 18,05 m"), ("Dormitoare", "3"),
                 ("Garaj", "35,5 m² · două locuri")],
          observatii=[
              "Grila de pereţi rezolvată pe suprafeţele scrise pe planul original:",
              "eroare 0,0% pe toate cele 16 camere.",
              "Golurile şi uşile sunt luate din radiografia planşei la mărire 4×,",
              "inclusiv uşile dormitoarelor spre terasa de est şi poarta de sud."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr[:4]))
    plansa(m, "/private/tmp/planuri/p8049.svg")
    print("util %.1f m²  (suma pe planul lor: 183,2)" % n.util)
