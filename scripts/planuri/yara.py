#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YARA — casă cu etaj, L-terasă, anexă de bucătărie.

Radiografie ref/yara/parter.jpg + etaj.jpg:
  PARTER  anvelopă 10,00 × 8,00 m, split 7,00 corp + 3,00 anexă NE,
          terasă sud 2,00 m, terasă est (L).
    D 9,86 · Living 23,87 · Bucătărie 6,48 · Tehnic 3,92 · Hol 2,99 · Baie 3,92
    Scară pe vest, între dormitor și baie. Intrare sud în hol.

  ETAJ  doar corpul 7,00 × 8,00 m (anexa rămâne parter).
    Master 21,98 · D2 10,94 · Baie 3,70 · Hol 4,56

Pereți 38 / 13. Terasa deschisă în AFARA anvelopei. Gabaritul crește
față de 10×8 ca scara U și PE=380 să încapă; ariile scrise nu se taie.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

# ── corp principal, din ariile scrise ──────────────────────────────────────
Hs = 1800                                 # banda de sud (baie / hol / tehnic)
Ws = round(3.92e6 / Hs)                   # 2178 — baie 3,92
Wh = round(2.99e6 / Hs)                   # 1661 — hol 2,99
Wt = round(3.92e6 / Hs)                   # 2178 — tehnic 3,92
Hd = round(9.86e6 / Ws)                   # 4527 — dormitor 9,86
Hst = 2150                                # casa scării U
Wp = 800                                  # palier îngust; livingul ține 23,87
Hholn = 900                               # ușa dormitorului, 800 mm + joc

xh = Ws + PI
xe = xh + Wh + PI
IL = xe + Wt                              # 6277
IA = Hd + PI + Hst + PI + Hs              # 8587
y_sc = Hd + PI
y_so = y_sc + Hst + PI
y_holn = Hd - Hholn
# living: nordul coloanei palierului + tot estul până la banda de sud
liv_e_x = xh + Wp + PI
liv_e_w = IL - liv_e_x

# anexă bucătărie NE, 6,48 m² — original 3,00 m la exterior
Hk = 2600
Wk = round(6.48e6 / Hk)                   # 2492
IL_k = IL + PI + Wk

L, A = IL_k + 2 * PE, IA + 2 * PE         # gabarit parter (cu anexa)
Le, Ae = IL + 2 * PE, IA + 2 * PE         # etajul = corpul


# ═══ PARTER ═════════════════════════════════════════════════════════════════
p = Nivel("PARTER", L, A)
p.poligon([
    (-PE, -PE),
    (IL_k + PE, -PE),
    (IL_k + PE, Hk + PE),
    (IL + PE, Hk + PE),
    (IL + PE, IA + PE),
    (-PE, IA + PE),
])

p.camera("Dormitor", 0, 0, Ws, Hd)
p.camera("Palier", xh, y_holn, Wp, y_so - y_holn)
p.camera("Hol", xh, y_so, Wh, Hs)
p.camera("Living · dining", xh, 0, Wp, y_holn)
p.camera("Living · dining", liv_e_x, 0, liv_e_w, y_so)
p.camera("Baie", 0, y_so, Ws, Hs)
p.camera("Tehnic", xe, y_so, Wt, Hs)
p.camera("Bucătărie", IL + PI, 0, Wk, Hk)

for w in [
    (Ws, 0, PI, IA),                      # vest | palier+hol
    (xh + Wp, y_holn, PI, y_so - y_holn), # palier | living
    (xh + Wh, y_so, PI, Hs),              # hol | tehnic
    (liv_e_x - PI, 0, PI, y_holn),        # living nord palier | living est
    (IL, 0, PI, Hk),                      # living | bucătărie
    (0, Hd, Ws, PI),                      # dormitor | scară
    (xe, y_so - PI, Wt, PI),              # living sud | tehnic
    (0, y_sc + Hst, Ws, PI),              # scară | baie
    (xh, y_so - PI, Wh, PI),              # palier/hol sud
]:
    p.perete(*w)

for t in [
    (Ws, Hd - 850, 800, False),           # palier → dormitor
    (xh + 50, y_so - PI, min(700, Wp - 100), True, False),  # palier ↔ hol
    (Ws, y_so + 400, 800, False),         # hol → baie
    (xh + Wh, y_so + 400, 800, False),    # hol → tehnic
    (xh + Wp, y_holn + 200, 1400, False, False),  # palier ↔ living
    (xh + Wp, 400, 800, False, False),    # living nord palier ↔ living est
    (IL, 400, 1100, False, False),        # living ↔ bucătărie
]:
    p.usa(*t)

p.usa_ext("S", xh + 200, 1100)            # intrare sud → hol
p.fereastra("N", xh + 300, 1500)
p.fereastra("N", xh + 2100, 1500)
p.fereastra("N", IL + PI + 500, 1400)     # bucătărie nord
p.fereastra("V", 800, 1600)               # dormitor
p.fereastra("V", y_sc + 400, 900)         # casa scării
p.fereastra("S", 400, 900)                # baie
p.fereastra("S", xe + 400, 1200)          # tehnic
p.fereastra("E", 500, 1400)               # bucătărie est
p.gol_ext(IL, y_holn + 300, PE, 2200, usa=True)          # living → terasa est
p.gol_ext(IL + PI + 400, Hk, 1400, PE, usa=True)         # bucătărie → terasă

p.zona("Scară", 80, y_sc, Ws - 160, Hst)
p.zona("Terasă", IL + PE, Hk + PE, IL_k - IL, IA - Hk)
p.zona("Terasă", -PE, IA + PE, IL + 2 * PE, 2000)

p.pune("pat", 250, 300, 1400, 2000)
p.pune("masa", 200, 2500, 700, 1200)
p.pune("dulap", 200, Hd - 500, 1800, 450)
p.pune("canapea", xh + 80, 200, 900, 2200)
p.pune("masa", xe + 200, 600, 1400, 1400)
p.pune("soba", IL - 700, 150, 600, 600)
p.pune("dus", 150, y_so + 80, 900, 900)
p.pune("lavoar", Ws - 700, y_so + 200, 600, 400)
p.pune("wc", 200, y_so + Hs - 700, 400, 600)
p.pune("masina", xe + 80, y_so + 80, 600, 600)
p.pune("raft", xe + Wt - 550, y_so + 80, 450, 1400)
p.pune("blat", IL + PI + 80, 80, Wk - 160, 600)
p.pune("chiuveta", IL + PI + 800, 130, 600, 450)
p.pune("blat", IL + PI + 80, 80, 600, Hk - 160)
p.pune("plita", IL + PI + 130, 900, 450, 700)


# ═══ ETAJ — aceleași IL, IA; D2 și hol țin ariile scrise ────────────────────
Hm = round(21.98e6 / IL)
Hs_e = IA - Hm - PI
Wu2 = round(10.94e6 / Hs_e)               # D2 10,94
Wh2 = round(4.56e6 / Hs_e)                # hol 4,56
Wx = IL - Wu2 - PI - Wh2 - PI             # restul = casa scării (vest)
xh2 = Wx + PI
xe2 = xh2 + Wh2 + PI
y_sc_e = Hm + PI
Hb2 = max(1680, round(3.70e6 / Wx))
y_baie_e = IA - Hb2

e = Nivel("ETAJ", L, A)                   # același gabarit pe planșă, fără rotație
e.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

e.camera("Dormitor matrimonial", 0, 0, IL, Hm)
e.camera("Hol", xh2, y_sc_e, Wh2, Hs_e)
e.camera("Dormitor 2", xe2, y_sc_e, Wu2, Hs_e)
e.camera("Baie", 0, y_baie_e, Wx, Hb2)

for w in [
    (Wx, y_sc_e, PI, Hs_e),               # scară+baie | hol
    (xh2 + Wh2, y_sc_e, PI, Hs_e),        # hol | dormitor 2
    (0, Hm, IL, PI),                      # master | banda de sud
    (0, y_baie_e - PI, Wx, PI),           # scară | baie
]:
    e.perete(*w)

for t in [
    (xh2 + 40, Hm, min(800, Wh2 - 80), True),    # hol → master
    (Wx, y_baie_e + 200, min(800, Hb2 - 300), False),  # hol → baie
    (xh2 + Wh2, y_sc_e + 600, 900, False),       # hol → dormitor 2
]:
    e.usa(*t)

e.fereastra("N", 600, 1800)
e.fereastra("N", IL // 2 + 400, 1800)
e.fereastra("S", 300, 900)                 # baie
e.fereastra("S", xe2 + 400, 1600)          # dormitor 2
e.fereastra("E", y_sc_e + 800, 1400)       # dormitor 2 est

e.zona("Scară", 80, y_sc_e, Wx - 160, y_baie_e - PI - y_sc_e)

e.pune("pat", 200, 400, 2100, 1800)
e.pune("masa", IL - 1400, 200, 1200, 700)
e.pune("dulap", IL - 550, 1100, 500, 1800)
e.pune("pat", xe2 + Wu2 - 1600, y_sc_e + 400, 1400, 2000)
e.pune("dulap", xe2 + 80, y_sc_e + 80, 500, 1600)
e.pune("cada", 150, y_baie_e + 80, 1700, 700)
e.pune("lavoar", 200, y_baie_e + Hb2 - 500, 600, 400)
e.pune("wc", min(Ws, Wx) - 500, y_baie_e + 200, 400, 600)


m = Model(
    nume="Yara",
    titlu="PLAN PARTER + ETAJ",
    subtitlu="Casă cu etaj, L-terasă, anexa de bucătărie · sistem Polistibrick",
    acoperis="Şarpantă în două ape, tablă fălţuită antracit",
    extra=[("Gabarit parter", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Etaj (corp)", "%.2f × %.2f m" % (Le / 1000, Ae / 1000)),
           ("Dormitoare", "3"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după planșele cotate 10,00 × 8,00 m + terasă sud 2,00 m:",
        "anexă de bucătărie pe nord-est, terasă în L în afara anvelopei de 38 cm,",
        "etajul stă doar pe corpul principal. Şarpantă clasică din lemn."])
m.nivel(p)
m.nivel(e)

if __name__ == "__main__":
    for niv in (p, e):
        pr = verifica(niv)
        print("%s circulaţie:" % niv.nume, "TRECE" if not pr else " | ".join(pr))
    print("gabarit parter %.2f × %.2f · etaj %.2f × %.2f"
          % (L / 1000, A / 1000, Le / 1000, Ae / 1000))
    print("amprentă %.1f m² · util %.1f (parter %.1f + etaj %.1f)"
          % (p.amprenta, p.util + e.util, p.util, e.util))
    for niv in (p, e):
        print(" %s" % niv.nume)
        for c in niv.camere:
            print("   %-32s %5.2f × %5.2f = %5.2f"
                  % (c["nume"], c["w"] / 1000, c["h"] / 1000,
                     c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   parter %s: %s" % (lat, descriere_fatada(p, lat)))
    for lat in "NS":
        elevatie_png(p, lat, "/private/tmp/planuri/yara-el-%s.png" % lat)
        elevatie_png(e, lat, "/private/tmp/planuri/yara-el-etaj-%s.png" % lat)
    plansa(m, "/private/tmp/planuri/yara.svg")
