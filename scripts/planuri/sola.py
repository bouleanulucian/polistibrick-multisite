#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SOLA — reprodusă din proiectul de referinţă 89-01 (Domkamen).

Planşa originală (07-plan.jpg) e cotată în centimetri pe desen:
  nord  490 | 726 | 578 | 111  → 1906
  sud   437 | 350 | 1008 | 113 → 1908
  vest  300 (terasă) | 900 (casă) | 136 (prispă) → 1336
  est   300 | 406 | 205 | 288 | 135 → 1334 ≈ 1336

Corpul principal: 17,94 × 9,00 m (490+726+578 pe nord, 900 pe vest).
Protruzia tehnică de est +1,11 m pe banda de sud. Terasa nord 3,00 m pe
traveea centrală; prispă sud 3,50 × 1,36 m; deck lateral est pe banda 2,05 m
între master şi blocul de sud (baie + tehnic).

PE=380, PI=130. Circulaţie prin hub-ul living · dining · bucătărie.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

# ── gabarit din cotele desenate ──────────────────────────────────────────────
L_MAIN = 4900 + 7260 + 5780          # 17940 — corp fără protruzie
UTIL_E = 1110                         # protruzia tehnică (111 pe nord)
L = L_MAIN + UTIL_E                   # 19050
A = 9000                              # adâncimea casei (900 pe vest)
IL_MAIN = L_MAIN - 2 * PE             # 17180
IL = L - 2 * PE                       # 18290
IA = A - 2 * PE                       # 8240

# travee pe X (feţe interioare, din segmentele exterioare de nord)
x_liv = 4900 - PE                     # 4520 — după aripa de vest
W_liv = 7260 - PI                     # 7130
x_mast = x_liv + W_liv + PI           # 11780
W_mast = IL_MAIN - x_mast             # 5400  (= 5780 − PE)

W_hol = 1150
W_left = x_liv - PI - W_hol           # 3240

# pe Y, din cotele de est: master 406, bandă deck 205, sud 288
H_mast = 4060 - PE                    # 3680
H_se = 2880 - PE                      # 2500
y_se = IA - H_se                      # 5740  (gap 2060 ≈ 2050)

W_teh = 1800                          # protruzie 1110 + fâşie din corp
x_teh = IL - W_teh                    # 16490
W_baie = x_teh - PI - x_mast          # 4580 — baie mare (cada + dublu lavoar)

# aripa de vest: două dormitoare cu baia comună între ele
H_d1 = 3050
H_baie_m = 1720
H_d2 = IA - H_d1 - PI - H_baie_m - PI  # 3210

y_baie_m = H_d1 + PI
y_d2 = y_baie_m + H_baie_m + PI

CONTUR = [
    (-PE, -PE),
    (IL_MAIN + PE, -PE),              # NE master
    (IL_MAIN + PE, y_se),             # coboară pe estul masterului → deck
    (IL + PE, y_se),                  # protruzia tehnică
    (IL + PE, IA + PE),
    (-PE, IA + PE),
]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── camere ───────────────────────────────────────────────────────────────────
n.camera("Dormitor 1", 0, 0, W_left, H_d1)
n.camera("Baie", 0, y_baie_m, W_left, H_baie_m)
n.camera("Dormitor 2", 0, y_d2, W_left, H_d2)
n.camera("Hol", W_left + PI, 0, W_hol, IA)
n.camera("Living · dining · bucătărie", x_liv, 0, W_liv, IA)
n.camera("Dormitor matrimonial", x_mast, 0, W_mast, H_mast)
n.camera("Baie principală", x_mast, y_se, W_baie, H_se)
n.camera("Tehnic", x_teh, y_se, W_teh, H_se)

# ── compartimentări ──────────────────────────────────────────────────────────
for w in [
    (W_left, 0, PI, IA),                          # dormitoare + baie | hol
    (x_liv - PI, 0, PI, IA),                      # hol | living
    (x_mast - PI, 0, PI, IA),                     # living | master + baie pr.
    (0, H_d1, W_left, PI),                        # dormitor 1 | baie
    (0, y_d2 - PI, W_left, PI),                   # baie | dormitor 2
    (x_mast, H_mast, W_mast, PI),                 # master | (deck / gol)
    (x_mast, y_se - PI, IL - x_mast, PI),         # living / deck | baie + tehnic
    (x_teh - PI, y_se, PI, H_se),                 # baie principală | tehnic
]:
    n.perete(*w)

# ── uşi ──────────────────────────────────────────────────────────────────────
for t in [
    (W_left, 900, 800, False),                    # hol → dormitor 1
    (W_left, y_baie_m + 400, 700, False),         # hol → baie
    (W_left, y_d2 + 800, 800, False),             # hol → dormitor 2
    (x_liv - PI, 2800, 1400, False, False),       # hol ↔ living
    (x_mast - PI, 1200, 900, False),              # living → master
    (x_mast - PI, y_se + 600, 900, False),        # living → baie principală
    (x_teh - PI, y_se + 700, 800, False),         # baie → tehnic
]:
    n.usa(*t)

# intrare sud, pe prispa de 350 cm (după aripa vest 437)
n.usa_ext("S", 5600, 1100)
n.gol_ext(5600, IA, 1100, PE, usa=True)

# ── goluri anvelopă ──────────────────────────────────────────────────────────
n.fereastra("N", 700, 1600)                       # dormitor 1
n.fereastra("N", x_liv + 800, 2800)               # dining → terasa nord (vitraj)
n.gol_ext(x_liv + 800, -PE, 2800, PE, usa=True)   # living → terasă nord
n.fereastra("N", x_mast + 1200, 1800)             # master
n.fereastra("V", 800, 1400)                       # dormitor 1
n.fereastra("V", y_baie_m + 400, 700)             # baie mică
n.fereastra("V", y_d2 + 900, 1400)                # dormitor 2
n.fereastra("S", 600, 1400)                       # dormitor 2
n.fereastra("S", x_liv + 1800, 1500)              # bucătărie
n.fereastra("S", x_mast + 1200, 1400)             # baie principală
n.fereastra("E", 800, 1600)                       # master, pe est
n.gol_ext(IL, y_se + 600, PE, 1100, usa=True)     # tehnic → deck lateral

# ── terase ───────────────────────────────────────────────────────────────────
n.zona("Terasă", x_liv - PE, -PE - 3000, W_liv + 2 * PE, 3000)
n.zona("Prispă", 3990, IA + PE, 3500, 1360)
n.zona("Terasă", IL_MAIN + PE, H_mast + PE, 2050, y_se - H_mast - PE)

# ── mobilier ─────────────────────────────────────────────────────────────────
n.pune("pat", 400, 500, 1800, 2100)
n.pune("dulap", W_left - 550, 200, 500, 1800)
n.pune("dus", 150, y_baie_m + 100, 900, 900)
n.pune("wc", 1200, y_baie_m + 600, 400, 600)
n.pune("lavoar", 1800, y_baie_m + 100, 600, 450)
n.pune("pat", 400, y_d2 + 500, 1800, 2100)
n.pune("dulap", W_left - 550, y_d2 + 200, 500, 1800)

n.pune("masa", x_liv + 600, 600, 2000, 1100)
n.pune("scaune", x_liv + 650, 200, 1900, 380)
n.pune("scaune", x_liv + 650, 1750, 1900, 380)
n.pune("canapea", x_liv + 3200, 2200, 2800, 950)
n.pune("canapea", x_liv + 5050, 2200, 950, 2200)
n.pune("masuta", x_liv + 3600, 3400, 900, 600)
n.pune("tv", x_mast - PI - 250, 2800, 250, 1600)

n.pune("blat", x_liv + 200, IA - 680, 3200, 600)
n.pune("plita", x_liv + 400, IA - 620, 700, 450)
n.pune("chiuveta", x_liv + 1600, IA - 620, 600, 450)
n.pune("blat", x_liv + 200, IA - 2800, 600, 2000)

n.pune("pat", x_mast + 800, 600, 1800, 2100)
n.pune("dulap", x_mast + 200, H_mast - 550, W_mast - 400, 500)

n.pune("cada", x_mast + 200, IA - 900, 1700, 750)
n.pune("lavoar", x_mast + 2200, y_se + 150, 1200, 450)
n.pune("wc", x_mast + 3800, y_se + 200, 400, 600)
n.pune("raft", x_teh + 100, y_se + 200, 500, 2000)
n.pune("masina", x_teh + 800, y_se + 200, 600, 600)

m = Model(
    nume="Sola",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu living central şi două aripi de dormitoare · sistem Polistibrick",
    acoperis="Şarpantă în două ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "17,94 × 9,00 m (+1,11 m tehnic est)"),
           ("Dormitoare", "3"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după proiectul de referinţă 89-01: cotele de pe planşa",
        "desenată (17,94 × 9,00 m corpul, protruzie tehnică 1,11 m).",
        "Hub living · dining · bucătărie; terasă nord 3,00 m; prispă sud 3,50 m."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/sola.svg")
    print("gabarit %.2f × %.2f · amprentă %.1f m² · util %.1f m²"
          % (L / 1000, A / 1000, n.amprenta, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
