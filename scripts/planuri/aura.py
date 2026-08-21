#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AURA — reprodusă din proiectul de referinţă 89-06 (9,65 × 21,95 m,
163 m²).

Longhouse pe un nivel: zona de zi deschisă pe vest (living · dining ·
bucătărie), patru dormitoare pe banda de nord, coridor est-vest pe mijloc,
băi şi tehnic pe banda de sud. Intrarea retrasă pe faţada de sud, în
vestibul. Terasă acoperită pe colţul de nord-vest.

Grila: calibrată pe planşa Instagram (≈31,4 px/m) şi pe gabaritul cotat
9,65 × 21,95 m; pereţi PE 380 / PI 130.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 21950, 9650
IL, IA = L - 2 * PE, A - 2 * PE          # 21190 × 8890

CONTUR = [(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)]

# ── adâncimi (N → S) ─────────────────────────────────────────────────────────
Hn = 3860                                 # dormitoarele
y_cor = Hn + PI                           # 3990
Hc = 1180                                 # coridor
y_s = y_cor + Hc + PI                     # 5300
Hs = IA - y_s                             # 3590

# ── lăţimi (V → E) ───────────────────────────────────────────────────────────
Wliv = 7180                               # living pe toată adâncimea
x0 = Wliv + PI                            # 7310 — aripa de noapte
W1, W2, W3, W4 = 2650, 3370, 3470, 4000  # 4 dormitoare; D4 mai mare
assert x0 + W1 + PI + W2 + PI + W3 + PI + W4 == IL

x1 = x0 + W1 + PI                         # 10090
x2 = x1 + W2 + PI                         # 13590
x3 = x2 + W3 + PI                         # 17190

# banda de sud: baie mică · vestibul · tehnic · debara · baie mare
Wb1 = 2100
Wvest = 2200
Wteh = 1950
Wdeb = 1750
Wb2 = IL - x0 - Wb1 - PI - Wvest - PI - Wteh - PI - Wdeb - PI
assert Wb2 > 2000

xv = x0 + Wb1 + PI
xt = xv + Wvest + PI
xd = xt + Wteh + PI
xb = xd + Wdeb + PI

n = Nivel("PARTER", L, A)
n.poligon(CONTUR)

# ── zona de zi ───────────────────────────────────────────────────────────────
n.camera("Living · dining · bucătărie", 0, 0, Wliv, IA)

# ── dormitoare (nord) ────────────────────────────────────────────────────────
n.camera("Dormitor 1", x0, 0, W1, Hn)
n.camera("Dormitor 2", x1, 0, W2, Hn)
n.camera("Dormitor 3", x2, 0, W3, Hn)
n.camera("Dormitor 4", x3, 0, W4, Hn)

# ── coridor ──────────────────────────────────────────────────────────────────
n.camera("Coridor", x0, y_cor, IL - x0, Hc)

# ── banda de sud ─────────────────────────────────────────────────────────────
n.camera("Baie 1", x0, y_s, Wb1, Hs)
n.camera("Vestibul", xv, y_s, Wvest, Hs)
n.camera("Tehnic", xt, y_s, Wteh, Hs)
n.camera("Debara", xd, y_s, Wdeb, Hs)
n.camera("Baie 2", xb, y_s, Wb2, Hs)

# ── compartimentări ─────────────────────────────────────────────────────────
for w in [
    (Wliv, 0, PI, IA),                    # living | aripa de noapte
    (x0 + W1, 0, PI, Hn),                 # D1 | D2
    (x1 + W2, 0, PI, Hn),                 # D2 | D3
    (x2 + W3, 0, PI, Hn),                 # D3 | D4
    (x0, Hn, IL - x0, PI),                # dormitoare | coridor
    (x0, y_cor + Hc, IL - x0, PI),        # coridor | banda de sud
    (x0 + Wb1, y_s, PI, Hs),              # baie 1 | vestibul
    (xv + Wvest, y_s, PI, Hs),            # vestibul | tehnic
    (xt + Wteh, y_s, PI, Hs),             # tehnic | debara
    (xd + Wdeb, y_s, PI, Hs),             # debara | baie 2
]:
    n.perete(*w)

# ── uşi ─────────────────────────────────────────────────────────────────────
for t in [
    (Wliv, y_cor + 150, Hc - 300, False, False),  # living ↔ coridor (trecere)
    (x0 + 700, Hn, 800, True),                    # coridor → D1
    (x1 + 900, Hn, 800, True),                    # coridor → D2
    (x2 + 900, Hn, 800, True),                    # coridor → D3
    (x3 + 1100, Hn, 800, True),                   # coridor → D4
    (x0 + 500, y_cor + Hc, 800, True),            # coridor → baie 1
    (xv + 500, y_cor + Hc, 900, True),            # coridor → vestibul
    (xt + 400, y_cor + Hc, 750, True),            # coridor → tehnic
    (xd + 350, y_cor + Hc, 700, True),            # coridor → debara
    (xb + 800, y_cor + Hc, 800, True),            # coridor → baie 2
]:
    n.usa(*t)

# intrarea principală: din sud, în vestibul
n.usa_ext("S", xv + 400, 1100)
n.nisa("S", xv - 200, Wvest + 600, 1400)

# ── goluri în anvelopă ───────────────────────────────────────────────────────
n.fereastra("N", 900, 2400)                       # dining, spre terasă
n.gol_ext(-PE, 2800, PE, 3200, usa=True)          # living → terasa de vest
n.fereastra("N", x0 + 400, 1400)                  # D1
n.fereastra("N", x1 + 600, 1600)                  # D2
n.fereastra("N", x2 + 600, 1600)                  # D3
n.fereastra("N", x3 + 800, 1800)                  # D4
n.fereastra("E", 800, 1600)                       # D4, est
n.fereastra("S", 1200, 1600)                      # bucătărie
n.fereastra("S", x0 + 400, 900)                   # baie 1
n.fereastra("S", xt + 400, 900)                   # tehnic
n.fereastra("S", xd + 300, 800)                   # debara
n.fereastra("S", xb + 900, 1400)                  # baie 2
n.fereastra("V", 500, 1800)                       # dining, vest

# ── zone punctate ────────────────────────────────────────────────────────────
n.zona("Terasă", -PE - 2800, -PE - 2200, 2800 + PE + 5200, 2200)
n.zona("Terasă", -PE - 2800, -PE, 2800, IA + 2 * PE)
n.zona("Intrare", xv - 400, IA + PE, Wvest + 1000, 1400)

# ── mobilier ─────────────────────────────────────────────────────────────────
# living / dining / bucătărie
n.pune("masa", 800, 600, 2200, 1000)
n.pune("scaune", 850, 200, 2100, 380).pune("scaune", 850, 1650, 2100, 380)
n.pune("canapea", 3800, 900, 2800, 950).pune("masuta", 4300, 2200, 900, 600)
n.pune("tv", Wliv - 280, 1200, 250, 1600)
n.pune("blat", 100, IA - 700, 3400, 620)
n.pune("chiuveta", 800, IA - 620, 600, 450)
n.pune("plita", 2200, IA - 620, 700, 450)
n.pune("blat", 100, IA - 2800, 620, 2000)
n.pune("blat", 2200, IA - 2200, 1600, 700)        # insulă
n.pune("scaune", 2400, IA - 2800, 1300, 430)

# dormitoare
n.pune("pat1", x0 + 400, 400, 1100, 2000).pune("dulap", x0 + 200, Hn - 700, 1800, 600)
n.pune("masa", x0 + W1 - 900, 500, 700, 1200)
n.pune("pat1", x1 + 500, 400, 1100, 2000).pune("dulap", x1 + 200, Hn - 700, 2000, 600)
n.pune("masa", x1 + W2 - 900, 500, 700, 1200)
n.pune("pat1", x2 + 500, 400, 1100, 2000).pune("dulap", x2 + 200, Hn - 700, 2000, 600)
n.pune("masa", x2 + W3 - 900, 500, 700, 1200)
n.pune("pat", x3 + 600, 500, 1800, 2100).pune("dulap", x3 + 200, Hn - 700, 2400, 600)
n.pune("masa", x3 + W4 - 1000, 500, 700, 1400)

# băi + tehnic
n.pune("dus", x0 + 200, y_s + 200, 900, 900)
n.pune("wc", x0 + 1300, y_s + 200, 400, 600)
n.pune("lavoar", x0 + 1200, y_s + 1400, 650, 450)
n.pune("dulap", xv + 200, y_s + 200, 1800, 600)
n.pune("boiler", xt + 200, y_s + 300, 600, 600)
n.pune("masina", xt + 1000, y_s + 300, 600, 600)
n.pune("raft", xd + 200, y_s + 300, 500, 2000)
n.pune("cada", xb + Wb2 - 1700, y_s + Hs - 900, 1500, 750)
n.pune("dus", xb + 200, y_s + 200, 1000, 1000)
n.pune("wc", xb + 1400, y_s + 200, 400, 600)
n.pune("lavoar", xb + 200, y_s + 1600, 1200, 450)

m = Model(
    nume="Anda",
    titlu="PLAN PARTER",
    subtitlu="Casă parter alungită, 4 dormitoare, living pe vest · sistem Polistibrick",
    acoperis="Şarpantă în două ape, pantă mare, tablă fălţuită",
    extra=[("Gabarit", "9,65 × 21,95 m"),
           ("Dormitoare", "4"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după proiectul de referinţă 89-06 (Domkamen), cotat",
        "9,65 × 21,95 m, circa 163 m². Living deschis pe vest, patru",
        "dormitoare pe nord, băi şi tehnic pe sud, coridor central.",
        "Intrarea retrasă pe faţada de sud, terasă pe colţul NV."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/tmp/planuri/aura.svg")
    print("amprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
