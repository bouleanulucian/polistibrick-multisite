#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LUNA — reprodusă din proiectul de referinţă Domkamen 89-08
(17,70 × 16,20 m; meta 172 m² — util Polistibrick 166 + garaj 38).

Casă parter în L: zona de zi pe nord-vest (living · dining · bucătărie U
cu bară şi cămară), suită matrimonială pe vest, dormitoare pe sud, baie
mare centrală, antreu cu WC şi prispă, aripa de est cu tehnic + garaj
dublu. Terasa în L pe nord şi vest — în afara anvelopei.

PE = 380 · PI = 130. Util ≈ 166 m² + garaj dublu ≈ 38 m².
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 17700, 16200
IL, IA = L - 2 * PE, A - 2 * PE                  # 16940 × 15440

W_gar = 5600
x_gar = IL - W_gar                               # 11340
W_corp = x_gar - PI                              # 11210

# ── X în corp (înainte de Y, ca prispa să ştie x_ant) ───────────────────────
W_hol, W_ant, W_en = 1200, 2000, 1900
W_w = W_corp - (W_hol + W_ant + W_en + 3 * PI)   # 5780
x1 = W_w + PI
x_hol = x1 + W_en + PI
x_ant = x_hol + W_hol + PI
assert abs(x_ant + W_ant - W_corp) < 2

# ── Y ───────────────────────────────────────────────────────────────────────
H_n = 5600
y_m = H_n + PI                                   # 5730
H_teh = 2400
y_g0 = H_teh + PI                                # 2530
H_gar = 6800
y_gar_s = y_g0 + H_gar                           # 9330
H_m = 4000
POR_Y = y_m + H_m                                # 9730
y_h = POR_Y + PI                                 # 9860
H_h = 1000
y_s = y_h + H_h + PI                             # 10990
H_s = IA - y_s                                   # 4450

# Prispa sub antreu (între x_ant şi x_gar)
POR_X0 = x_ant

CONTUR = [
    (-PE, -PE),
    (IL + PE, -PE),
    (IL + PE, y_gar_s + PE),                     # SE garaj
    (x_gar, y_gar_s + PE),
    (x_gar, POR_Y + PE),                         # est antreu, sub garaj
    (POR_X0, POR_Y + PE),                        # fund prispă
    (POR_X0, IA + PE),
    (-PE, IA + PE),
]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── camere ──────────────────────────────────────────────────────────────────
W_cam, H_cam = 1850, 1950
x_cam = W_corp - W_cam
y_cam = H_n - H_cam

n.camera("Living · dining · bucătărie", 0, 0, W_corp, y_cam - PI)
n.camera("Living · dining · bucătărie", 0, y_cam, x_cam - PI, H_cam)
n.camera("Cămară", x_cam, y_cam, W_cam, H_cam)
n.camera("Tehnic", x_gar, 0, W_gar, H_teh)

H_dr = 1850
n.camera("Dormitor matrimonial", 0, y_m, W_w, H_m)
n.camera("Dressing", x1, y_m, W_en, H_dr)
n.camera("Baie master", x1, y_m + H_dr + PI, W_en, H_m - H_dr - PI)
n.camera("Hol", x_hol, y_m, W_hol, H_m)
n.camera("Coridor", 0, y_h, x_ant, H_h)          # până la prispă (x_ant)

H_wc = 1400
n.camera("WC", x_ant, y_m, W_ant, H_wc)
n.camera("Antreu", x_ant, y_m + H_wc + PI, W_ant, H_m - H_wc - PI)
n.camera("Garaj dublu", x_gar, y_g0, W_gar, H_gar, tip="garaj")

W_d2, W_d3 = 3400, 2800
x_d3 = W_d2 + PI
x_baie = x_d3 + W_d3 + PI
W_baie = x_ant - x_baie
assert W_baie >= 2000, W_baie

n.camera("Dormitor 2", 0, y_s, W_d2, H_s)
n.camera("Dormitor 3", x_d3, y_s, W_d3, H_s)
n.camera("Baie", x_baie, y_s, W_baie, H_s)

# ── pereţi ──────────────────────────────────────────────────────────────────
for w in [
    (x_cam - PI, y_cam, PI, H_cam),
    (x_cam, y_cam - PI, W_cam, PI),
    (x_gar - PI, 0, PI, max(y_gar_s, POR_Y)),
    (x_gar, H_teh, W_gar, PI),
    (0, H_n, W_corp, PI),
    (W_w, y_m, PI, H_m),
    (x1, y_m + H_dr, W_en, PI),
    (x1 + W_en, y_m, PI, H_m),
    (x_hol + W_hol, y_m, PI, H_m),
    (x_ant, y_m + H_wc, W_ant, PI),
    (0, POR_Y, x_ant, PI),                       # mijloc | coridor (vest de prispă)
    (0, y_h + H_h, x_ant, PI),                   # coridor | dormitoare
    (W_d2, y_s, PI, H_s),
    (x_d3 + W_d3, y_s, PI, H_s),
    (POR_X0, POR_Y, x_gar - POR_X0, PE),          # fundul prispei
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (x_hol + 120, H_n, 900, True, False),
    (x_cam - PI, y_cam + 350, 800, False),
    (x_gar - PI, 600, 900, False),
    (x_gar + 900, H_teh, 900, True),
    (x_hol - PI, y_m + 300, 900, False),
    (x1 - PI, y_m + 400, 900, False),
    (x1 - PI, y_m + H_dr + PI + 250, 800, False),
    (x_hol + W_hol, y_m + 200, 750, False),
    (x_hol + W_hol, y_m + H_wc + PI + 300, 900, False),
    (x_gar - PI, y_m + H_wc + PI + 200, 900, False),
    (x_hol + 120, POR_Y, 900, True, False),       # hol ↔ coridor
    (500, y_h + H_h, 900, True),
    (x_d3 + 400, y_h + H_h, 900, True),
    (x_baie + 400, y_h + H_h, 800, True),
]:
    n.usa(*t)

# ── anvelopă ────────────────────────────────────────────────────────────────
n.gol_ext(x_ant + 400, POR_Y, 1100, PE, usa=True)
n.usa_ext("S", x_ant + 400, 1100)
n.gol_ext(x_gar + 700, y_gar_s, 3400, PE)
n.gol_ext(1800, -PE, 2800, PE, usa=True)
n.gol_ext(-PE, 1200, PE, 2400, usa=True)
n.fereastra("N", x_cam + 100, 1400)
n.fereastra("N", x_gar + 900, 1400)
n.fereastra("E", 400, 1100)
n.fereastra("E", y_g0 + 2000, 1400)
n.fereastra("V", y_m + 900, 1700)
n.fereastra("V", y_s + 800, 1600)
n.fereastra("S", 500, 1600)
n.fereastra("S", x_d3 + 300, 1500)
n.fereastra("S", x_baie + 300, 1000)

n.zona("Terasă", -PE - 2800, -PE - 2600, 2800 + 6500, 2600)
n.zona("Terasă", -PE - 2800, -PE, 2800, H_n + PE)
n.zona("Intrare", POR_X0, POR_Y + PE, x_gar - POR_X0 + PE, IA + PE - POR_Y - PE)

n.pune("canapea", 300, 400, 900, 2600)
n.pune("canapea", 1300, 2800, 2400, 900)
n.pune("masuta", 1500, 1900, 900, 600)
n.pune("tv", 80, 1000, 250, 1600)
n.pune("masa", 4000, 600, 2200, 1050)
n.pune("scaune", 4050, 150, 2100, 430)
n.pune("scaune", 4050, 1700, 2100, 430)
n.pune("blat", W_corp - 2700, 80, 2500, 600)
n.pune("chiuveta", W_corp - 1900, 130, 600, 450)
n.pune("blat", W_corp - 680, 80, 600, 2400)
n.pune("plita", W_corp - 630, 1000, 450, 700)
n.pune("blat", W_corp - 2700, 2000, 1900, 700)
n.pune("scaune", W_corp - 2500, 2800, 1500, 430)
n.pune("raft", x_cam + 60, y_cam + 60, W_cam - 120, 500)
n.pune("masina", x_gar + 150, 150, 600, 600)
n.pune("raft", x_gar + 1000, 150, 2000, 500)
n.pune("pat", 600, y_m + 350, 2000, 1800)
n.pune("dulap", x1 + 50, y_m + 50, W_en - 100, 550)
n.pune("dulap", x1 + 50, y_m + 700, W_en - 100, 550)
n.pune("dus", x1 + 60, y_m + H_dr + PI + 60, 900, 900)
n.pune("wc", x1 + W_en - 460, y_m + H_dr + PI + 120, 400, 600)
n.pune("lavoar", x1 + 60, y_m + H_m - 460, 650, 400)
n.pune("wc", x_ant + 60, y_m + 120, 400, 600)
n.pune("lavoar", x_ant + 600, y_m + 60, 550, 400)
n.pune("dulap", x_ant + 50, y_m + H_wc + PI + 50, 500, 1500)
n.pune("masina", x_gar + 300, y_g0 + 400, 1800, 4200)
n.pune("masina", x_gar + 3000, y_g0 + 400, 1800, 4200)
n.pune("pat1", 250, y_s + 400, 1200, 2000)
n.pune("dulap", W_d2 - 500, y_s + 100, 450, 1800)
n.pune("pat1", x_d3 + 200, y_s + 400, 1200, 2000)
n.pune("dulap", x_d3 + W_d3 - 500, y_s + 100, 450, 1800)
n.pune("cada", x_baie + 50, y_s + H_s - 800, 1600, 720)
n.pune("dus", x_baie + W_baie - 950, y_s + 50, 900, 900)
n.pune("lavoar", x_baie + 50, y_s + 50, 600, 450)
n.pune("lavoar", x_baie + 700, y_s + 50, 600, 450)
n.pune("wc", x_baie + W_baie - 460, y_s + 1100, 400, 600)

m = Model(
    nume="Livia",
    titlu="PLAN PARTER",
    subtitlu="Casă parter în L, trei dormitoare, garaj dublu · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, patru ape, tablă fălţuită antracit",
    extra=[("Gabarit", "17,70 × 16,20 m"),
           ("Dormitoare", "3"),
           ("Băi", "2 + WC"),
           ("Garaj", "dublu")],
    observatii=[
        "Reprodusă după proiectul de referinţă Domkamen 89-08,",
        "cotat 17,70 × 16,20 m — util 166 m² + garaj dublu 38 m² (meta 172).",
        "Terasa în L pe nord şi vest, în afara anvelopei calde.",
        "Prispă acoperită pe sud, sub antreu."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/tmp/planuri/luna.svg")
    gar = next(c for c in n.camere if c["tip"] == "garaj")
    g = gar["w"] * gar["h"] / 1e6
    print("amprentă %.1f m² · util %.1f m² · garaj %.1f · total %.1f"
          % (n.amprenta, n.util, g, n.util + g))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²%s"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6,
                 "" if c["tip"] == "camera" else "  [garaj]"))
