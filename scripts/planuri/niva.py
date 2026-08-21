#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NIVA — reprodusă din proiectul de referinţă Domkamen 88-99 (16,35 × 18,40 m).

Casă parter: zona de zi pe vest (living · dining · bucătărie, vitrată spre
terasa de nord 5,00 m), trei dormitoare + birou pe est, două băi centrale,
garaj dublu pe sud-est. Intrare sud.

PE=380 · PI=130. Coordonatele sunt INTERIOARE.
Cote din planşă: 1635 × 1840 cm.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 16350, 18400
IL, IA = L - 2 * PE, A - 2 * PE                  # 15590 × 17640

W_ZI = 6000
W_HOL = 1300
X_HOL = W_ZI + PI                                # 6130
X_EST = X_HOL + W_HOL + PI                       # 7560
W_EST = IL - X_EST                               # 8030

W_D2, W_DEB = 2600, 1300
X_D2 = X_EST
X_MAST = X_D2 + W_D2 + PI
X_DEB = IL - W_DEB
W_MAST = X_DEB - PI - X_MAST

H_NORD = 3800
Y_HN = H_NORD + PI                               # 3930
H_HN = 1200
Y_MID = Y_HN + H_HN + PI                         # 5260
H_MID = 3200
Y_JOI = Y_MID + H_MID + PI                       # 8590

H_GAR = 6000
Y_GAR = IA - H_GAR                               # 11640
H_JOI = Y_GAR - PI - Y_JOI                       # 2920

W_B1, W_B2 = 2900, 2500
X_B2 = X_EST + W_B1 + PI
X_DR = X_B2 + W_B2 + PI
W_DR = IL - X_DR

W_D3 = 4000
W_WC = 1500
W_GAR = 5800
X_GAR = IL - W_GAR                               # 9790
W_SPA = 1600
X_SPA = X_GAR - PI - W_SPA                       # 8060
# antreu acoperă holul pe X
assert X_SPA - PI >= X_HOL + W_HOL, (X_SPA - PI, X_HOL + W_HOL)

CONTUR = [(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)]

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

n.camera("Living", 0, 0, W_ZI, H_NORD)
n.camera("Dining · bucătărie", 0, Y_HN, W_ZI, Y_GAR - PI - Y_HN)
n.camera("Dormitor 2", X_D2, 0, W_D2, H_NORD)
n.camera("Dormitor matrimonial", X_MAST, 0, W_MAST, H_NORD)
n.camera("Debara", X_DEB, 0, W_DEB, H_NORD)
n.camera("Hol de noapte", X_EST, Y_HN, W_EST, H_HN)
n.camera("Hol", X_HOL, 0, W_HOL, Y_GAR - PI)
n.camera("Baie", X_EST, Y_MID, W_B1, H_MID)
n.camera("Baie 2", X_B2, Y_MID, W_B2, H_MID)
n.camera("Dressing", X_DR, Y_MID, W_DR, H_MID)
n.camera("Dormitor 3", X_EST, Y_JOI, W_D3, H_JOI)
n.camera("Birou", X_EST + W_D3 + PI, Y_JOI, IL - (X_EST + W_D3 + PI), H_JOI)
n.camera("WC", 0, Y_GAR, W_WC, H_GAR)
n.camera("Antreu", W_WC + PI, Y_GAR, X_SPA - PI - (W_WC + PI), H_GAR)
n.camera("Spălătorie", X_SPA, Y_GAR, W_SPA, H_GAR)
n.camera("Garaj dublu", X_GAR, Y_GAR, W_GAR, H_GAR)

for w in [
    (W_ZI, 0, PI, Y_GAR - PI),
    (X_EST - PI, 0, PI, Y_GAR - PI),
    (0, H_NORD, W_ZI, PI),
    (X_EST, H_NORD, W_EST, PI),
    (X_D2 + W_D2, 0, PI, H_NORD),
    (X_MAST + W_MAST, 0, PI, H_NORD),
    (X_EST, Y_MID - PI, W_EST, PI),
    (X_EST + W_B1, Y_MID, PI, H_MID),
    (X_B2 + W_B2, Y_MID, PI, H_MID),
    (X_EST, Y_JOI - PI, W_EST, PI),
    (X_EST + W_D3, Y_JOI, PI, H_JOI),
    (0, Y_GAR - PI, IL, PI),
    (W_WC, Y_GAR, PI, H_GAR),
    (X_SPA - PI, Y_GAR, PI, H_GAR),
    (X_GAR - PI, Y_GAR, PI, H_GAR),
]:
    n.perete(*w)

for t in [
    (W_ZI, 1500, 1000, False, False),
    (2000, H_NORD, 1600, True, False),
    (X_EST - PI, Y_HN + 200, 900, False, False),
    (X_D2 + 500, H_NORD, 800, True),
    (X_MAST + 600, H_NORD, 900, True),
    (X_DEB + 200, H_NORD, 700, True),             # hol noapte → debara
    (X_EST - PI, Y_MID + 500, 800, False),
    (X_EST + W_B1, Y_MID + 600, 800, False),
    (X_B2 + W_B2, Y_MID + 600, 800, False),
    (X_DR + 200, Y_MID - PI, 800, True),          # hol noapte → dressing
    (X_EST - PI, Y_JOI + 600, 800, False),
    (X_EST + W_D3, Y_JOI + 600, 800, False),
    (X_HOL + 100, Y_GAR - PI, 1000, True, False),
    (W_WC + PI + 400, Y_GAR - PI, 1200, True, False),
    (W_WC, Y_GAR + 2000, 900, False),
    (X_SPA - PI, Y_GAR + 1500, 800, False),
    (X_GAR - PI, Y_GAR + 2000, 900, False),
]:
    n.usa(*t)

n.gol_ext(W_WC + PI + 600, IA, 1100, PE, usa=True)
n.gol_ext(X_GAR + 700, IA, 4400, PE)

n.gol_ext(1000, -PE, 3200, PE, usa=True)
n.fereastra("N", X_D2 + 500, 1400)
n.fereastra("N", X_MAST + 600, 1600)
n.fereastra("V", Y_HN + 2000, 2800)
n.fereastra("V", Y_GAR + 1500, 900)
n.fereastra("E", 800, 1400)
n.fereastra("E", Y_MID + 600, 1000)
n.fereastra("E", Y_JOI + 800, 1400)
n.fereastra("E", Y_GAR + 2000, 900)
n.fereastra("S", W_WC + PI + 2000, 1200)

n.zona("Terasă", -PE, -PE - 5000, IL + 2 * PE, 5000)
n.zona("Intrare", W_WC + PI, IA + PE, 3000, 1400)

n.pune("canapea", 800, 1200, 2800, 950).pune("canapea", 800, 2200, 950, 1600)
n.pune("masuta", 1600, 1800, 900, 600)
n.pune("masa", 1200, Y_HN + 800, 2000, 1100)
n.pune("scaune", 1250, Y_HN + 400, 1900, 380).pune("scaune", 1250, Y_HN + 1950, 1900, 380)
n.pune("blat", 200, Y_GAR - 800, 4000, 600)
n.pune("plita", 400, Y_GAR - 750, 700, 450)
n.pune("chiuveta", 2000, Y_GAR - 750, 600, 450)
n.pune("pat1", X_D2 + 400, 500, 1100, 2100)
n.pune("pat", X_MAST + 500, 600, 1800, 2100)
n.pune("cada", X_EST + 200, Y_MID + 200, 1700, 750)
n.pune("lavoar", X_EST + 200, Y_MID + 2200, 1200, 450)
n.pune("dus", X_B2 + 200, Y_MID + 300, 900, 900)
n.pune("wc", X_B2 + 1500, Y_MID + 400, 400, 600)
n.pune("pat1", X_EST + 400, Y_JOI + 400, 1100, 2100)
n.pune("birou", X_EST + W_D3 + PI + 300, Y_JOI + 400, 1600, 700)
n.pune("wc", 300, Y_GAR + 800, 400, 600)
n.pune("lavoar", 300, Y_GAR + 2000, 650, 450)
n.pune("masina", X_SPA + 200, Y_GAR + 400, 600, 600)
n.pune("masina", X_SPA + 900, Y_GAR + 400, 600, 600)

m = Model(
    nume="Niva",
    titlu="PLAN PARTER",
    subtitlu="Casă parter cu terasă de nord, patru camere şi garaj dublu · sistem Polistibrick",
    acoperis="Şarpantă în patru ape, pantă mică, tablă fălţuită",
    extra=[("Gabarit", "16,35 × 18,40 m"),
           ("Dormitoare", "3 + birou"),
           ("Băi", "2 + WC + spălătorie")],
    observatii=[
        "Reprodusă după proiectul de referinţă Domkamen 88-99, cotat",
        "16,35 × 18,40 m (terasă nord 5,00 m în afara anvelopei).",
        "Zona de zi pe vest; dormitoare şi birou pe est; garaj sud-est."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/tmp/planuri/niva.svg")
    print("gabarit %.2f × %.2f · amprentă %.1f m² · util %.1f m²"
          % (L / 1000, A / 1000, n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
