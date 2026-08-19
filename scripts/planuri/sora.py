#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SORA — 106 m², 1,5 etaje.

ETAJ  (ref/sora/a.jpg): corp 8,00, terasă S 4,00 × 2,00.
  D 11,58 | D 11,58 · hol 5,66 · baie 3,99 · debară 7,16 · birou 7,99
  h=2,00 pe SE.

PARTER (ref/sora/b.jpg): corp 8,00 × 8,00, terasă N 3,00,
  reces S 4,00 × 2,00 (terasă deschisă vest, dormitor est).
  Living 16,47 · bucătărie 7,06 · hol 10,20 · baie 3,85
  dormitor 13,60 · tehnic 4,16 · vest 3,20
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

# ── grilă din ariile de la etaj ─────────────────────────────────────────────
Hs = 2100
Wst = round(7.16e6 / Hs)                 # 3410
Wof = round(7.99e6 / Hs)                 # 3805
IL = Wst + PI + Wof                      # 7345
L = IL + 2 * PE                          # 8105
W1 = (IL - PI) // 2                      # 3607
We = IL - PI - W1
Hn = round(11.58e6 / W1)                 # 3210

Hm = 1650
Wb = round(3.99e6 / Hm)                  # 2418
Wh = round(5.66e6 / Hm)                  # 3430
Wsc = IL - Wh - Wb - 2 * PI              # 1237
xh = Wsc + PI
xb = xh + Wh + PI
xe = W1 + PI
xof = Wst + PI

IA_e = Hn + PI + Hm + PI + Hs            # 7190
A_e = IA_e + 2 * PE

# parter: hol 10,20 împărțit vest/est, corp aliniat, reces S în afara vestului
Hliv = round(16.47e6 / Wst)              # 4830
Hk = round(7.06e6 / Wof)                 # 1855
Hbed = round(13.60e6 / Wof)              # 3574
Hsv = round((4.16 + 3.20) * 1e6 / (Wst - PI))
Wteh = round(4.16e6 / Hsv)
Wvest = Wst - PI - Wteh
Hbaie_p = round(3.85e6 / Wb)
Hhe = 1378
Hhol_p = 1454
IA_body = Hliv + PI + Hhol_p + PI + Hsv  # 8789
H_ext = 2000                             # reces S, în afara anvelopei
IA_p = IA_body
A_p = IA_p + 2 * PE
x_rec = Wst + PI                         # perete 38 cm terasă S | dormitor

y_hol = Hliv + PI
y_sv = y_hol + Hhol_p + PI
y_baie = Hk + PI
y_hol_e = y_baie + Hbaie_p + PI
y_bed = IA_p - Hbed


# ═══ ETAJ ═══════════════════════════════════════════════════════════════════
e = Nivel("ETAJ", L, A_e)
e.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA_e + PE), (-PE, IA_e + PE)])

e.camera("Dormitor 1", 0, 0, W1, Hn)
e.camera("Dormitor 2", xe, 0, We, Hn)
e.camera("Hol", xh, Hn + PI, Wh, Hm)
e.camera("Baie", xb, Hn + PI, Wb, Hm)
e.camera("Debară", 0, Hn + PI + Hm + PI, Wst, Hs)
e.camera("Birou", xof, Hn + PI + Hm + PI, Wof, Hs)

for w in [
    (W1, 0, PI, Hn),
    (0, Hn, IL, PI),
    (Wsc, Hn + PI, PI, Hm),
    (xh + Wh, Hn + PI, PI, Hm),
    (0, Hn + PI + Hm, IL, PI),
    (Wst, Hn + PI + Hm + PI, PI, Hs),
]:
    e.perete(*w)

ym = Hn + PI
e.usa(max(xh, 80) + 40, Hn, 900, True)                           # hol → D1
e.usa(max(xe, xh) + 80, Hn, 900, True)                           # hol → D2
e.usa(xh + Wh, ym + 400, 800, False)                             # hol → baie
e.usa(xh + 200, ym + Hm, 900, True)                              # hol → debară
e.usa(max(xh, xof) + 80, ym + Hm, 900, True)                     # hol → birou
e.usa(Wsc, ym + 200, 900, False)                                 # hol → scară

e.fereastra("N", 700, 1800)
e.fereastra("N", xe + 800, 1800)
e.fereastra("V", ym + Hm + PI + 400, 1100)
e.fereastra("E", ym + 350, 900)
e.fereastra("E", ym + Hm + PI + 500, 1400)
e.usa_ext("S", xof + 600, 1600)
e.gol_ext(xof + 600, IA_e, 1600, PE, usa=True)

e.zona("Scară", 80, ym + 80, Wsc - 160, Hm - 160)
e.zona("h=2,00", 0, ym + Hm + PI + 800, IL, 350)
e.zona("Terasă", xof - PE, IA_e + PE, Wof + 2 * PE, 2000)

e.pune("pat1", 250, 350, 1400, 2000)
e.pune("dulap", W1 - 550, 200, 500, 1800)
e.pune("pat", xe + We - 2100, 350, 1800, 2100)
e.pune("dulap", xe + 200, Hn - 500, 2000, 450)
e.pune("cada", xb + 80, ym + 80, 1700, 700)
e.pune("lavoar", xb + 80, ym + Hm - 480, 600, 400)
e.pune("wc", xb + Wb - 500, ym + 200, 400, 600)
e.pune("dulap", 80, ym + Hm + PI + 80, Wst - 160, 550)
e.pune("masa", xof + 400, ym + Hm + PI + 400, 1600, 800)
e.pune("canapea", xof + Wof - 1000, ym + Hm + PI + 200, 850, 1600)


# ═══ PARTER ═════════════════════════════════════════════════════════════════
p = Nivel("PARTER", L, A_p)
p.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA_p + PE), (-PE, IA_p + PE)])

p.camera("Living · dining", 0, 0, Wst, Hliv)
p.camera("Bucătărie", xof, 0, Wof, Hk)
p.camera("Hol", 0, y_hol, Wst, Hhol_p)
p.camera("Hol", xof, y_hol_e, Wof, y_bed - PI - y_hol_e)
p.camera("Baie", xof + Wof - Wb, y_baie, Wb, Hbaie_p)
p.camera("Hol", xof, y_baie, Wof - Wb - PI, Hbaie_p)
p.camera("Dormitor", xof, y_bed, Wof, Hbed)
p.camera("Tehnic", 0, y_sv, Wteh, Hsv)
p.camera("Vestibul", Wteh + PI, y_sv, Wvest, Hsv)

for w in [
    (Wst, 0, PI, IA_p),
    (0, Hliv, Wst, PI),
    (0, y_hol + Hhol_p, Wst, PI),
    (Wteh, y_sv, PI, Hsv),
    (xof, Hk, Wof, PI),
    (xof + Wof - Wb - PI, y_baie, PI, Hbaie_p),
    (xof, y_hol_e - PI, Wof, PI),
    (xof, y_bed - PI, Wof, PI),
]:
    p.perete(*w)

p.usa(Wst, 200, min(1400, Hk - 280), False, False)               # living → bucătărie
p.usa(400, Hliv, 1400, True, False)                              # living → hol V
p.usa(xof + 80, y_hol_e - PI, 900, True)                         # hol lângă baie → hol E
p.usa(xof + Wof - Wb - PI, y_baie + 400, 800, False)             # hol → baie
p.usa(xof + 400, y_bed - PI, 900, True)                          # hol E → dormitor
p.usa(Wteh + PI + 80, y_hol + Hhol_p, 900, True)                 # hol → vestibul
p.usa(200, y_hol + Hhol_p, 800, True)                            # hol → tehnic
p.usa(80, y_hol + 80, 900, True)                                 # hol → scară (zona)

p.gol_ext(Wteh + PI + 150, IA_p, 1100, PE, usa=True)
p.usa_ext("S", Wteh + PI + 150, 1100)
p.gol_ext(800, -PE, 2200, PE, usa=True)
p.fereastra("N", xof + 400, 1400)
p.fereastra("E", 400, 1100)
p.fereastra("E", y_baie + 300, 900)
p.fereastra("E", y_bed + 900, 1600)
p.fereastra("S", xof + 800, 1600)
p.fereastra("V", 900, 1600)
p.fereastra("V", 2800, 1400)
p.fereastra("V", y_sv + 500, 900)

p.zona("Scară", 80, y_hol + 80, min(Wsc, Wst) - 160, Hhol_p - 160)
p.zona("Terasă", -PE, -PE - 3000, L, 3000)
p.zona("Terasă", -PE, IA_body + PE, x_rec + PE, H_ext)

p.pune("canapea", 200, 300, 2200, 900)
p.pune("masa", 800, 1800, 1800, 1000)
p.pune("blat", xof + Wof - 620, 80, 600, 1600)
p.pune("chiuveta", xof + Wof - 550, 200, 450, 600)
p.pune("plita", xof + Wof - 550, 900, 450, 700)
p.pune("dus", xof + Wof - Wb + 80, y_baie + 80, 900, 900)
p.pune("lavoar", xof + Wof - Wb + 80, y_baie + Hbaie_p - 480, 550, 400)
p.pune("wc", xof + Wof - 500, y_baie + 200, 400, 600)
p.pune("pat", xof + Wof - 2100, y_bed + 500, 1800, 2100)
p.pune("dulap", xof + 80, y_bed + 80, Wof - 160, 500)
p.pune("raft", 80, y_sv + 200, 450, 1400)
p.pune("dulap", Wteh + PI + 80, y_sv + 80, 450, Hsv - 160)


m = Model(
    nume="Sora",
    titlu="PLAN PARTER + ETAJ",
    subtitlu="Casă 1,5 etaje, 106 m², două dormitoare + birou · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit parter", "%.2f × %.2f m" % (L / 1000, A_p / 1000)),
           ("Gabarit etaj", "%.2f × %.2f m" % (L / 1000, A_e / 1000)),
           ("Dormitoare", "2 + birou"),
           ("Băi", "2")],
    observatii=[
        "Reprodusă după planșele cotate 8,00 × 8,00 m: mansardă cu h=2,00 pe SE,",
        "terasă sud 4,00 × 2,00 m în afara anvelopei de 38 cm, reces de intrare la parter.",
        "Şarpantă clasică din lemn. Scara e zonă, nu cameră."])
m.nivel(p)
m.nivel(e)

if __name__ == "__main__":
    for niv in (p, e):
        pr = verifica(niv)
        print("%s circulaţie:" % niv.nume, "TRECE" if not pr else " | ".join(pr))
    print("gabarit parter %.2f × %.2f · etaj %.2f × %.2f"
          % (L / 1000, A_p / 1000, L / 1000, A_e / 1000))
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
        elevatie_png(p, lat, "/private/tmp/planuri/sora-el-%s.png" % lat)
        elevatie_png(e, lat, "/private/tmp/planuri/sora-e-el-%s.png" % lat)
    plansa(m, "/private/tmp/planuri/sora.svg")
