#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HERA — casă cu etaj, ~128 m², trei dormitoare.

Instagram nadiyni_stiny / DbGeDFFDyXU. Ariile scrise:

  PARTER  13,00 × 8,00 m (+ terasă E 3,00, N 1,00, prispa S 1,50)
    Garaj 16,90 · Tehnic 6,40 · Birou 10,66 · Hol 11,14
    Intrare 3,49 · Baie 3,95 · Living·dining·bucătărie 25,20

  ETAJ    11,50 × 7,00 m (+ terasă V 3,00, balcon E 1,00)
    D2 11,06 · D3 11,06 · Baie 4,71 · Dressing 5,96
    Master 12,75 · Hol 4,50

Pereți 38 / 13. Terasa în afara anvelopei. Șarpantă lemn.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

# ═══ PARTER ═════════════════════════════════════════════════════════════════
Lp, Ap = 13000, 8000
ILp, IAp = Lp - 2 * PE, Ap - 2 * PE

Wg = 3280
Hteh = round(6.40e6 / Wg)
y_gar = Hteh + PI
Hgar = IAp - y_gar

Wliv = round(25.20e6 / IAp)
x_mid = Wg + PI
Wm = ILp - x_mid - PI - Wliv
x_liv = x_mid + Wm + PI

Whc = 1200
Woff = Wm - Whc - PI
Hoff = round(10.66e6 / Woff)
Hs = 1460
Wb = round(3.95e6 / Hs)
Wi = Wm - Wb - PI
y_s = IAp - Hs
y_hol = Hoff + PI
# holul principal coboară până la baie, ca să aibă perete comun
Hhol = y_s - PI - y_hol

p = Nivel("PARTER", Lp, Ap)
p.poligon([(-PE, -PE), (ILp + PE, -PE), (ILp + PE, IAp + PE), (-PE, IAp + PE)])

p.camera("Tehnic", 0, 0, Wg, Hteh)
p.camera("Garaj", 0, y_gar, Wg, Hgar)
p.camera("Hol", x_mid, 0, Whc, Hoff)
p.camera("Birou", x_mid + Whc + PI, 0, Woff, Hoff)
p.camera("Hol", x_mid, y_hol, Wm, Hhol)
p.camera("Baie", x_mid, y_s, Wb, Hs)
p.camera("Intrare", x_mid + Wb + PI, y_s, Wi, Hs)
p.camera("Living · dining · bucătărie", x_liv, 0, Wliv, IAp)

for w in [
    (Wg, 0, PI, IAp),
    (x_mid + Wm, 0, PI, IAp),
    (0, Hteh, Wg, PI),
    (x_mid + Whc, 0, PI, Hoff),
    (x_mid, Hoff, Wm, PI),
    (x_mid, y_s - PI, Wm, PI),
    (x_mid + Wb, y_s, PI, Hs),
]:
    p.perete(*w)

p.usa(Wg, 500, 900, False)                            # braț → tehnic
p.usa(x_mid + Whc, 800, 900, False)                   # braț → birou
p.usa(x_mid + 200, Hoff, 800, True)                   # braț → hol
p.usa(Wg, y_hol + 300, 900, False)                    # hol → garaj
p.usa(x_liv - PI, y_hol + 200, min(1400, Hhol - 400), False, False)  # hol ↔ living
p.usa(x_mid + 400, y_s - PI, 800, True)               # hol → baie
p.usa(x_mid + Wb + PI + 250, y_s - PI, 900, True)     # hol → intrare

p.usa_ext("S", x_mid + Wb + PI + 250, 1100)
p.gol_ext(x_mid + Wb + PI + 250, IAp, 1100, PE, usa=True)
p.gol_ext(500, IAp, 2200, PE)
p.fereastra("N", 400, 1100)
p.fereastra("N", x_mid + Whc + PI + 500, 1800)
p.fereastra("N", x_liv + 500, 2200)
p.fereastra("V", y_gar + 1400, 1200)
p.fereastra("S", x_mid + 400, 900)
p.fereastra("S", x_liv + 700, 1800)
p.fereastra("E", 800, 1800)
p.usa_ext("E", 2800, 2400)
p.gol_ext(ILp, 2800, PE, 2400, usa=True)

p.zona("Terasă", ILp + PE, 200, 3000, IAp - 400)
p.zona("Terasă nord", x_liv, -PE - 1000, Wliv + PE, 1000)
p.zona("Prispă", x_mid + Wb, IAp + PE, Wi + 600, 1500)
p.zona("Scară", x_mid + Wm - 1250, y_hol + 200, 1150, min(2400, Hhol - 400))

p.pune("masina", 350, y_gar + 600, 1700, 4000)
p.pune("masina", 200, 250, 600, 600)
p.pune("raft", 1000, 250, 1600, 500)
p.pune("canapea", x_mid + Whc + PI + 200, 350, 1600, 800)
p.pune("birou", x_mid + Whc + PI + 300, 1300, 1400, 700)
p.pune("wc", x_mid + 120, y_s + 200, 400, 600)
p.pune("lavoar", x_mid + 650, y_s + 80, 550, 400)
p.pune("dus", x_mid + Wb - 900, y_s + 250, 800, 800)
p.pune("dulap", x_mid + Wb + PI + 80, y_s + 80, max(400, Wi - 160), 450)
p.pune("blat", x_liv + 80, 80, Wliv - 160, 620)
p.pune("plita", x_liv + 400, 150, 700, 450)
p.pune("chiuveta", x_liv + 1300, 150, 600, 450)
p.pune("insula", x_liv + 700, 1100, 1600, 900)
p.pune("masa", x_liv + 350, 2600, 1900, 1050)
p.pune("canapea", x_liv + Wliv - 950, 4700, 850, 2100)

# ═══ ETAJ ═══════════════════════════════════════════════════════════════════
Le, Ae = 11500, 7000
ILe, IAe = Le - 2 * PE, Ae - 2 * PE

Hn = (IAe - PI) // 2
Hs = IAe - Hn - PI
W1 = round(11.06e6 / Hn)
Wb = round(4.71e6 / Hn)
Wd = round(5.96e6 / Hn)
Wmast = round(12.75e6 / Hs)
y_s = Hn + PI

xd = ILe - Wd
xb = xd - PI - Wb
xm = ILe - Wmast
xh = W1 + PI
# palier în L: nord până la baie, sud până la master — fără suprapunere
Wn = xb - PI - xh
Ws = xm - PI - xh
Hn_hol = 1200
Hs_hol = 1400
yhn = Hn - Hn_hol

e = Nivel("ETAJ", Le, Ae)
e.poligon([(-PE, -PE), (ILe + PE, -PE), (ILe + PE, IAe + PE), (-PE, IAe + PE)])

e.camera("Dormitor 2", 0, 0, W1, Hn)
e.camera("Dormitor 3", 0, y_s, W1, Hs)
e.camera("Hol etaj", xh, yhn, Wn, Hn_hol)
e.camera("Hol etaj", xh, y_s, Ws, Hs_hol)
e.camera("Baie", xb, 0, Wb, Hn)
e.camera("Dressing", xd, 0, Wd, Hn)
e.camera("Dormitor matrimonial", xm, y_s, Wmast, Hs)

for w in [
    (W1, 0, PI, IAe),
    (0, Hn, ILe, PI),
    (xb - PI, 0, PI, Hn),
    (xd - PI, 0, PI, Hn),
    (xm - PI, y_s, PI, Hs),
]:
    e.perete(*w)

e.usa(W1, yhn + 200, 800, False)                         # hol N → D2
e.usa(W1, y_s + 200, 800, False)                         # hol S → D3
e.usa(xh + 200, Hn, 800, True)                           # hol N → hol S
e.usa(xm - PI, y_s + 250, 800, False)                    # hol S → master
e.usa(xb - PI, yhn + 200, 800, False)                    # hol N → baie
e.usa(xd - PI, 400, 800, False)                          # baie → dressing
e.usa(xd + 200, Hn, 800, True)                           # master → dressing

e.fereastra("V", 500, 1800)
e.fereastra("V", y_s + 500, 1800)
e.fereastra("N", xb + 200, 1000)
e.fereastra("E", 400, 1100)
e.fereastra("E", y_s + 700, 1800)
e.fereastra("S", xm + 800, 1600)

e.zona("Terasă", -PE - 3000, 200, 3000, IAe - 400)
e.zona("Balcon", ILe + PE, 800, 1000, 4000)
e.zona("Scară", xh + 100, y_s + 150, min(1100, Ws - 200), 2000)

e.pune("pat", 350, 350, 1400, 2000)
e.pune("dulap", W1 - 650, 300, 550, 1600)
e.pune("pat", 350, y_s + 350, 1400, 2000)
e.pune("dulap", W1 - 650, y_s + 300, 550, 1600)
e.pune("cada", xb + 80, 80, 1380, 700)
e.pune("lavoar", xb + 80, Hn - 480, 550, 400)
e.pune("wc", xb + Wb - 480, Hn - 680, 400, 600)
e.pune("dulap", xd + 80, 80, Wd - 160, 550)
e.pune("pat", xm + 500, y_s + 400, 1800, 2100)

m = Model(
    nume="Hera",
    titlu="PLAN PARTER + ETAJ",
    subtitlu="Casă cu etaj, trei dormitoare, garaj · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit parter", "13,00 × 8,00 m"),
           ("Gabarit etaj", "11,50 × 7,00 m"),
           ("Dormitoare", "3 + birou"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după nadiyni_stiny DbGeDFFDyXU, ~128 m², trei dormitoare.",
        "Garajul e doar la parter. Terasa de est 3,00 m stă în afara anvelopei.",
        "La etaj: două dormitoare pe vest cu terasă, master cu dressing pe est."])
m.nivel(p)
m.nivel(e)

if __name__ == "__main__":
    for niv in (p, e):
        pr = verifica(niv)
        print("%s circulaţie:" % niv.nume, "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/hera.svg")
    print("gabarit parter %.2f × %.2f · etaj %.2f × %.2f"
          % (Lp / 1000, Ap / 1000, Le / 1000, Ae / 1000))
    print("amprentă %.1f m² · util %.1f (parter %.1f + etaj %.1f)"
          % (p.amprenta, p.util + e.util, p.util, e.util))
    for niv in (p, e):
        print("— %s —" % niv.nume)
        for c in niv.camere:
            print("   %-32s %5.2f × %5.2f = %5.2f"
                  % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   P %s: %s" % (lat, descriere_fatada(p, lat)))
    for lat in "NS":
        elevatie_png(p, lat, "/private/tmp/planuri/hera-el-%s.png" % lat)
        elevatie_png(e, lat, "/private/tmp/planuri/hera-e-el-%s.png" % lat)
