#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIMA — reprodusă din proiectul de referinţă Domkamen 88-98 (16,64 × 17,04 m).

Casă parter: zona de zi pe vest (living · dining · bucătărie, vitrată spre
terasa în L nord-vest), trei dormitoare pe nord-est (matrimonial cu baie
proprie), garaj dublu pe sud-est. Intrare sud, lângă garaj.

PE=380 · PI=130. Coordonatele sunt INTERIOARE.
Cote din planşă: 1664 × 1704 cm.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 16640, 17040
IL, IA = L - 2 * PE, A - 2 * PE                  # 15880 × 16280

W_ZI = 6800
W_HOL = 1400
X_HOL = W_ZI + PI
X_EST = X_HOL + W_HOL + PI
W_EST = IL - X_EST                               # 7420

W_D1, W_D2 = 2400, 2300
X_D2 = X_EST + W_D1 + PI
X_MAST = X_D2 + W_D2 + PI
W_MAST = IL - X_MAST                             # 2460

H_DORM = 3700
Y_HN = H_DORM + PI
H_HN = 1300
Y_SERV = Y_HN + H_HN + PI                        # 5260
H_SERV = 3000
H_SUD = 6200                                     # adâncime garaj / bucătărie
Y_SUD = IA - H_SUD                               # 10080

# servicii: WC | Baie | Baie m.
W_WC = 1400
W_BAIE = X_MAST - PI - (X_EST + W_WC + PI)
X_BAIE = X_EST + W_WC + PI
X_BM = X_MAST
W_BM = W_MAST

W_GAR = 6200
X_GAR = IL - W_GAR
W_ANT = X_GAR - PI - X_HOL                       # antreu de la hol până la garaj (include holul pe X)

CONTUR = [(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

n.camera("Living · dining", 0, 0, W_ZI, Y_SUD - PI)
n.camera("Dormitor 1", X_EST, 0, W_D1, H_DORM)
n.camera("Dormitor 2", X_D2, 0, W_D2, H_DORM)
n.camera("Dormitor matrimonial", X_MAST, 0, W_MAST, H_DORM)
n.camera("Hol de noapte", X_EST, Y_HN, W_EST, H_HN)
n.camera("Hol", X_HOL, 0, W_HOL, Y_SUD - PI)
n.camera("WC", X_EST, Y_SERV, W_WC, H_SERV)
n.camera("Baie", X_BAIE, Y_SERV, W_BAIE, H_SERV)
n.camera("Baie m.", X_BM, Y_SERV, W_BM, H_SERV)
n.camera("Bucătărie", 0, Y_SUD, W_ZI, H_SUD)
n.camera("Antreu", X_HOL, Y_SUD, W_ANT, H_SUD)
n.camera("Garaj dublu", X_GAR, Y_SUD, W_GAR, H_SUD)

for w in [
    (W_ZI, 0, PI, Y_SUD - PI),
    (X_EST - PI, 0, PI, Y_SUD - PI),
    (X_EST, H_DORM, W_EST, PI),
    (X_EST + W_D1, 0, PI, H_DORM),
    (X_D2 + W_D2, 0, PI, H_DORM),
    (X_EST, Y_SERV - PI, W_EST, PI),
    (X_EST + W_WC, Y_SERV, PI, H_SERV),
    (X_BM - PI, Y_SERV, PI, H_SERV),
    (0, Y_SUD - PI, IL, PI),
    (X_GAR - PI, Y_SUD, PI, H_SUD),
]:
    n.perete(*w)

for t in [
    (W_ZI, 2800, 1200, False, False),             # living ↔ hol
    (X_EST - PI, Y_HN + 200, 900, False, False),  # hol ↔ hol noapte
    (X_EST + 500, H_DORM, 800, True),             # → D1
    (X_D2 + 500, H_DORM, 800, True),              # → D2
    (X_MAST + 500, H_DORM, 900, True),            # → master
    (X_EST - PI, Y_SERV + 400, 800, False),       # hol → WC
    (X_EST + W_WC, Y_SERV + 600, 800, False),     # WC → baie (sau hol→baie)
    (X_EST - PI, Y_SERV + 1600, 800, False),      # hol → baie (pe lângă WC: need door on baie west)
    (X_BM - PI, Y_SERV + 800, 800, False),        # baie → baie m.? Better from hol noapte/master
    (X_MAST + 400, Y_SERV - PI, 800, True),       # hol noapte → baie m.
    (X_HOL, Y_SUD - PI, 1100, True, False),       # hol ↔ antreu
    (1800, Y_SUD - PI, 2000, True, False),        # living ↔ bucătărie
    (X_GAR - PI, Y_SUD + 2000, 900, False),       # antreu → garaj
]:
    n.usa(*t)

# baie access: door from vertical hol into baie (baie left edge = X_BAIE, hol right = X_EST)
# gap is WC. So door hol→baie must go through... door on north of baie from hol de noapte:
n.usa(X_BAIE + 600, Y_SERV - PI, 800, True)      # hol noapte → baie

n.gol_ext(X_HOL + 400, IA, 1100, PE, usa=True)
n.gol_ext(X_GAR + 700, IA, 4600, PE)

n.gol_ext(1200, -PE, 3000, PE, usa=True)
n.fereastra("N", X_EST + 400, 1400)
n.fereastra("N", X_D2 + 400, 1300)
n.fereastra("N", X_MAST + 400, 1500)
n.gol_ext(-PE, 2000, PE, 3600, usa=True)
n.fereastra("V", Y_SUD + 1500, 2000)
n.fereastra("E", Y_SERV + 600, 1200)
n.fereastra("E", Y_SUD + 2500, 1000)
n.fereastra("S", 1500, 1800)

n.zona("Terasă", -PE - 4000, -PE - 2800, 4000 + W_ZI + 2 * PE, 2800)
n.zona("Terasă", -PE - 4000, -PE, 4000, Y_SUD)
n.zona("Intrare", X_HOL, IA + PE, 3200, 1500)

n.pune("masa", 1000, 1600, 2200, 1100)
n.pune("scaune", 1050, 1200, 2100, 380).pune("scaune", 1050, 2750, 2100, 380)
n.pune("canapea", 3600, 2500, 2800, 950).pune("canapea", 5400, 3500, 950, 2200)
n.pune("masuta", 4100, 3700, 900, 600)
n.pune("pat1", X_EST + 300, 500, 1100, 2100)
n.pune("pat1", X_D2 + 300, 500, 1100, 2100)
n.pune("pat", X_MAST + 300, 600, 1800, 2100)
n.pune("wc", X_EST + 400, Y_SERV + 400, 400, 600)
n.pune("lavoar", X_EST + 400, Y_SERV + 1500, 650, 450)
n.pune("cada", X_BAIE + 200, Y_SERV + 2000, 1700, 750)
n.pune("lavoar", X_BAIE + 200, Y_SERV + 200, 1200, 450)
n.pune("dus", X_BM + 200, Y_SERV + 300, 900, 900)
n.pune("wc", X_BM + 1400, Y_SERV + 400, 400, 600)
n.pune("blat", 200, Y_SUD + 300, 600, 5000)
n.pune("plita", 250, Y_SUD + 1200, 450, 700)
n.pune("chiuveta", 250, Y_SUD + 3000, 450, 600)
n.pune("blat", 1200, Y_SUD + 300, 3500, 600)

m = Model(
    nume="Cima",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu terasă în L, trei dormitoare şi garaj dublu · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "16,64 × 17,04 m"),
           ("Dormitoare", "3"),
           ("Băi", "2 + WC")],
    observatii=[
        "Reprodusă după proiectul de referinţă Domkamen 88-98, cotat",
        "16,64 × 17,04 m. Zona de zi pe vest, vitrată spre terasa în L;",
        "dormitoare pe nord-est; garaj dublu pe sud-est."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/tmp/planuri/cima.svg")
    print("gabarit %.2f × %.2f · amprentă %.1f m² · util %.1f m²"
          % (L / 1000, A / 1000, n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
