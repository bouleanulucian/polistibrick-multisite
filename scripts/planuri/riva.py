#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RIVA — reprodusă din proiectul de referinţă Domkamen 89-02 (24,8 × 18,4 m).

Casă parter lată: living 8,27 m + dining 6,66 m + aripa de noapte 9,94 m pe
nord. Bucătărie sub dining; prispă acoperită 3,20 m sub living. Garajul
dublu (8,10 × 6,20 m), pe planşă oblic, e aproximat ca aripa L ortogonală
pe sud-est.

PE=380 · PI=130. Coordonatele sunt INTERIOARE.
Cote din planşă (cm): 827|666|994 · 570|320|161 · 890|358 · garaj 810×620.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

# gabarit exterior din cotele de pe planşă
L = 8270 + 6660 + 9940                           # 24870
A = 18400                                        # meta (include aripa garaj)
IL, IA = L - 2 * PE, A - 2 * PE                  # 24110 × 17640

# travee pe X (din segmentele exterioare de nord)
W_LIV = 8270 - PE                                # 7890
W_DIN = 6660 - PI                                # 6530
X_DIN = W_LIV + PI
X_NOI = X_DIN + W_DIN + PI                       # 14550
W_NOI = IL - X_NOI                               # 9560 ≈ 9940 - PE

# pe Y: living 570; aripa dreaptă 890; garaj ortogonal sub SE
H_LIV = 5700 - PE                                # 5320
H_MAIN = 8900 - PE                               # 8520 — adâncimea corpului pe est
Y_GAR = H_MAIN + PI                              # 8650
H_GAR = 6200
# verific: Y_GAR + H_GAR <= IA → 8650+6200=14850 < 17640 OK (rest terasă/ Toleranță)
# umplem restul până la IA cu prelungire? Meta 18,4 = 890+358+? + angled.
# Ajustăm: garajul începe imediat sub corpul principal pe est
# pe vest, sub living: prispă (zonă, nu cameră); bucătăria sub dining

H_BUC = H_MAIN - H_LIV - PI                      # 3070 — bucătărie sub dining
Y_BUC = H_LIV + PI                               # 5450

# pe aripa de noapte (W_NOI): master nord | hol | dormitoare + băi
H_MAST = 4200
Y_HN = H_MAST + PI
H_HN = 1300
Y_SUD_N = Y_HN + H_HN + PI                       # 5760
H_SUD_N = H_MAIN - Y_SUD_N                       # 2760

# master: dormitor | dressing | baie m. pe nordul aripii
W_BM = 2800
W_DR = 1600
W_MAST = W_NOI - W_BM - PI - W_DR - PI
X_DR = X_NOI + W_MAST + PI
X_BM = X_DR + W_DR + PI

# sud noapte: D2 | Baie | D3
W_D2 = 3200
W_BAIE = 2800
X_BAIE = X_NOI + W_D2 + PI
X_D3 = X_BAIE + W_BAIE + PI
W_D3 = IL - X_D3

# hol vertical între dining şi noapte? Hol pe vestul aripii noapte
W_HOL = 1400
# restructure night wing with hol:
# X_NOI: Hol (W_HOL) | rest rooms
X_CAM = X_NOI + W_HOL + PI
W_CAM = IL - X_CAM                               # camere noapte

W_BM = 2600
W_DR = 1500
W_MAST = W_CAM - W_BM - PI - W_DR - PI
X_MAST = X_CAM
X_DR = X_MAST + W_MAST + PI
X_BM = X_DR + W_DR + PI

W_D2 = 2600
W_BAIE = 2000
X_D2 = X_CAM
X_BAIE = X_D2 + W_D2 + PI
X_D3 = X_BAIE + W_BAIE + PI
W_D3 = IL - X_D3                                 # ~3170

# garaj L pe SE: lățime 8100 de la est spre vest, adâncime 6200
W_GAR = 8100
X_GAR = IL - W_GAR
# antreu între bucătărie/dining şi garaj
X_ANT = X_DIN
W_ANT = X_GAR - PI - X_ANT

# contur L: corp principal + aripa antreu+garaj pe sud-est
CONTUR = [
    (-PE, -PE),
    (IL + PE, -PE),
    (IL + PE, Y_GAR + H_GAR + PE),
    (X_ANT - PE, Y_GAR + H_GAR + PE),
    (X_ANT - PE, H_MAIN + PE),
    (-PE, H_MAIN + PE),
]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

n.camera("Living", 0, 0, W_LIV, H_LIV)
n.camera("Dining", X_DIN, 0, W_DIN, H_LIV)
n.camera("Bucătărie", X_DIN, Y_BUC, W_DIN, H_BUC)
n.camera("Hol", X_NOI, 0, W_HOL, H_MAIN)
n.camera("Dormitor matrimonial", X_MAST, 0, W_MAST, H_MAST)
n.camera("Dressing", X_DR, 0, W_DR, H_MAST)
n.camera("Baie m.", X_BM, 0, W_BM, H_MAST)
n.camera("Hol de noapte", X_CAM, Y_HN, W_CAM, H_HN)
n.camera("Dormitor 2", X_D2, Y_SUD_N, W_D2, H_SUD_N)
n.camera("Baie", X_BAIE, Y_SUD_N, W_BAIE, H_SUD_N)
n.camera("Dormitor 3", X_D3, Y_SUD_N, W_D3, H_SUD_N)
n.camera("Antreu", X_ANT, Y_GAR, W_ANT, H_GAR)
n.camera("Garaj dublu", X_GAR, Y_GAR, W_GAR, H_GAR)
# WC / tehnic lângă bucătărie pe vestul antreului — taie din antreu
# Mai simplu: cameră tehnică mică pe colțul vest al benzii garaj, sub living-porch
n.camera("Tehnic", 0, Y_BUC, W_LIV, H_BUC)       # sub living, lângă prispa

for w in [
    (W_LIV, 0, PI, H_MAIN),                       # living/tehnic | dining/buc
    (X_NOI - PI, 0, PI, H_MAIN),                  # dining | hol
    (X_CAM - PI, 0, PI, H_MAIN),                  # hol | camere
    (0, H_LIV, W_LIV + PI + W_DIN, PI),           # living/dining | tehnic/buc
    (X_MAST + W_MAST, 0, PI, H_MAST),
    (X_DR + W_DR, 0, PI, H_MAST),
    (X_CAM, H_MAST, W_CAM, PI),                   # master band | hol noapte
    (X_CAM, Y_SUD_N - PI, W_CAM, PI),
    (X_D2 + W_D2, Y_SUD_N, PI, H_SUD_N),
    (X_BAIE + W_BAIE, Y_SUD_N, PI, H_SUD_N),
    (0, H_MAIN, IL, PI),                          # corp | antreu/garaj (doar pe est real)
    (X_GAR - PI, Y_GAR, PI, H_GAR),
]:
    n.perete(*w)

for t in [
    (W_LIV, 1500, 1200, False, False),            # living ↔ dining
    (X_DIN + 1500, H_LIV, 1600, True, False),     # dining ↔ bucătărie
    (X_NOI - PI, 2000, 1100, False, False),       # dining ↔ hol
    (X_CAM - PI, 1200, 900, False),                # hol → master
    (X_MAST + W_MAST, 1000, 800, False),          # master → dressing
    (X_DR + W_DR, 1000, 800, False),              # dressing → baie m.
    (X_CAM - PI, Y_HN + 200, 900, False, False),  # hol ↔ hol noapte
    (X_D2 + 600, Y_SUD_N - PI, 800, True),        # hol noapte → D2
    (X_BAIE + 500, Y_SUD_N - PI, 800, True),      # → baie
    (X_D3 + 400, Y_SUD_N - PI, 800, True),        # → D3
    (X_NOI - PI, Y_BUC + 800, 900, False),        # bucătărie → hol
    (W_LIV, Y_BUC + 800, 800, False),             # tehnic ↔ bucătărie
    (X_ANT + 400, H_MAIN, 1100, True, False),     # hol/buc → antreu
    (X_GAR - PI, Y_GAR + 2000, 900, False),       # antreu → garaj
]:
    n.usa(*t)

# hol → antreu: hol ends at H_MAIN, antreu starts Y_GAR = H_MAIN+PI at X_ANT
# Hol x = X_NOI..X_NOI+W_HOL; Antreu x = X_ANT..X_GAR-PI with X_ANT=X_DIN
# Overlap: X_NOI to X_NOI+W_HOL is within antreu if X_ANT <= X_NOI
assert X_ANT <= X_NOI
n.usa(X_NOI + 200, H_MAIN, 1000, True, False)

n.gol_ext(X_ANT + 800, Y_GAR + H_GAR, 1100, PE, usa=True)  # intrare pe sudul antreului
n.gol_ext(X_GAR + 1000, Y_GAR + H_GAR, 5000, PE)           # poartă garaj

n.fereastra("N", 800, 2800)                       # living
n.fereastra("N", X_DIN + 1000, 2800)              # dining
n.gol_ext(X_DIN + 1000, -PE, 2800, PE, usa=True)
n.fereastra("N", X_MAST + 400, 1600)
n.fereastra("V", 800, 2800)                       # living vest
n.gol_ext(-PE, 1000, PE, 2800, usa=True)
n.fereastra("E", 800, 1600)
n.fereastra("E", Y_SUD_N + 400, 1400)
n.fereastra("S", X_DIN + 800, 1500)               # bucătărie — pe peretele de sud al corpului
n.gol_ext(X_DIN + 500, H_MAIN, 2000, PE, usa=True)  # buc → prispă/terasă?

n.zona("Prispă", -PE, H_MAIN + PE, W_LIV + 2 * PE, 3200)
n.zona("Terasă", -PE - 2000, -PE - 2000, 2000, H_LIV + 2000)
n.zona("Intrare", X_ANT + 400, Y_GAR + H_GAR + PE, 2800, 1200)

n.pune("canapea", 800, 1500, 2800, 950).pune("canapea", 800, 2800, 950, 1800)
n.pune("masuta", 1600, 2200, 900, 600)
n.pune("masa", X_DIN + 1200, 800, 2400, 1200)
n.pune("scaune", X_DIN + 1250, 400, 2300, 380)
n.pune("scaune", X_DIN + 1250, 2050, 2300, 380)
n.pune("blat", X_DIN + 200, Y_BUC + H_BUC - 700, 4000, 600)
n.pune("plita", X_DIN + 400, Y_BUC + H_BUC - 650, 700, 450)
n.pune("chiuveta", X_DIN + 2000, Y_BUC + H_BUC - 650, 600, 450)
n.pune("pat", X_MAST + 400, 600, 1800, 2100)
n.pune("dulap", X_DR + 200, 400, 500, 2000)
n.pune("cada", X_BM + 200, 400, 1700, 750)
n.pune("dus", X_BM + 200, 2000, 900, 900)
n.pune("lavoar", X_BM + 1400, 2000, 1000, 450)
n.pune("pat1", X_D2 + 400, Y_SUD_N + 300, 1100, 2100)
n.pune("pat1", X_D3 + 400, Y_SUD_N + 300, 1100, 2100)
n.pune("cada", X_BAIE + 200, Y_SUD_N + 200, 1700, 750)
n.pune("wc", X_BAIE + 200, Y_SUD_N + 1500, 400, 600)

m = Model(
    nume="Rada",
    titlu="PLAN PARTER",
    subtitlu="Casă parter lată cu living · dining şi garaj în L · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "24,87 × 18,40 m"),
           ("Dormitoare", "3"),
           ("Băi", "2 + tehnic")],
    observatii=[
        "Reprodusă după proiectul de referinţă Domkamen 89-02: cotele",
        "827 | 666 | 994 cm pe nord; garaj 810 × 620 cm, pe planşă oblic,",
        "aproximat ca aripa L ortogonală pe sud-est. Prispă 3,20 m sub living."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/tmp/planuri/riva.svg")
    print("gabarit %.2f × %.2f · amprentă %.1f m² · util %.1f m²"
          % (L / 1000, A / 1000, n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
