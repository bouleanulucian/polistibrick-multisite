#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINA — 82 m² compactă, două dormitoare.

Original Instagram: 11,00 = 2,00 + 9,00 m, adâncime 9,00 m,
terasă 1,50 m în L pe nord + est. Fâșia vest 2,00 m e interior
(master, baie, D2), nu pasaj. Instagram avea acoperiș plat — la noi
șarpantă de lemn, tablă fălțuită.

  N  terasă 1,50
     Master 16,00 | Hol | Living 27,81
     Baie 5,54    | Hol | Living
     D2 10,04     | Vest 3,76 | Tehnic 3,78 | Bucătărie 8,03
  S  prispă 1,50, intrare în vestibul
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

Ww, Wh = 3900, 1150
Hm = round(16.00e6 / Ww)                    # 4103
Hb = round(5.54e6 / Ww)                     # 1421
Hd2 = round(10.04e6 / Ww)                   # 2574
y_baie = Hm + PI
y_d2 = y_baie + Hb + PI
IA = y_d2 + Hd2                             # 8358

Hliv = y_d2 - PI                            # 5654 — livingul până la banda de sud
Hk = Hd2                                    # bucătăria aliniată cu D2
Wliv = round(27.81e6 / Hliv)
Wkit = round(8.03e6 / Hk)
Wteh = round(3.78e6 / Hk)
Wve = round(3.76e6 / Hk)

xh = Ww + PI
xe = xh + Wh + PI
y_s = y_d2
x_teh = xh + Wve + PI
x_kit = x_teh + Wteh + PI
# livingul și bucătăria se întâlnesc pe est; IL e max(living, sud)
IL = max(xe + Wliv, x_kit + Wkit)
if IL > xe + Wliv:
    # fâșia de 11 cm deasupra bucătăriei rămâne living, ca să nu rămână gol
    Wliv = IL - xe
# holul rămâne 6,47: lățimea e Wh, înălțimea Hliv

L, A = IL + 2 * PE, IA + 2 * PE

n = Nivel("PARTER", L, A)
n.poligon([(-PE, -PE), (IL + PE, -PE), (IL + PE, IA + PE), (-PE, IA + PE)])

n.camera("Dormitor matrimonial", 0, 0, Ww, Hm)
n.camera("Baie", 0, y_baie, Ww, Hb)
n.camera("Dormitor 2", 0, y_d2, Ww, Hd2)
n.camera("Hol", xh, 0, Wh, Hliv)
n.camera("Living · dining", xe, 0, Wliv, Hliv)
n.camera("Vestibul", xh, y_s, Wve, Hk)
n.camera("Tehnic", x_teh, y_s, Wteh, Hk)
n.camera("Bucătărie", x_kit, y_s, Wkit, Hk)

for w in [
    (Ww, 0, PI, IA),                         # vest (dormitoare) | hol+living
    (xh + Wh, 0, PI, Hliv),                  # hol | living
    (0, Hm, Ww, PI),                         # master | baie
    (0, y_baie + Hb, Ww, PI),                # baie | D2
    (xh, Hliv, IL - xh, PI),                 # hol+living | sud
    (xh + Wve, y_s, PI, Hk),                 # vestibul | tehnic
    (x_teh + Wteh, y_s, PI, Hk),             # tehnic | bucătărie
]:
    n.perete(*w)

for t in [
    (Ww, 800, 900, False),                   # hol → master
    (Ww, y_baie + 200, 800, False),          # hol → baie
    (Ww, y_d2 + 400, 900, False),            # vestibul → D2
    (xh + 150, Hliv, 800, True),             # hol → vestibul
    (xh + Wh, 1800, 1400, False, False),     # hol → living
    (xh + Wve, y_s + 400, 800, False),       # vestibul → tehnic
    (max(xe, x_kit) + 200, Hliv, 1600, True, False),  # living ↔ bucătărie
]:
    n.usa(*t)

n.usa_ext("S", xh + 80, 1100)
n.gol_ext(xh + 80, IA, 1100, PE, usa=True)
n.usa_ext("N", xe + 400, 2400)               # living → terasa nord
n.gol_ext(xe + 400, -PE, 2400, PE, usa=True)
n.usa_ext("E", 800, 2000)                    # living → terasa est
n.gol_ext(IL, 800, PE, 2000, usa=True)
n.fereastra("N", 600, 1800)                  # master
n.fereastra("V", y_baie + 250, 900)          # baie
n.fereastra("V", y_d2 + 600, 1400)           # D2
n.fereastra("S", 400, 1400)                  # D2 sud
n.fereastra("S", x_teh + 200, 800)           # tehnic
n.fereastra("S", x_kit + 800, 1400)          # bucătărie
n.fereastra("E", y_s + 500, 1200)            # bucătărie est

n.zona("Terasă", -PE, -PE - 1500, L + 1500, 1500)
n.zona("Terasă", IL + PE, 0, 1500, IA + PE)
n.zona("Intrare", xh - 400, IA + PE, Wve + Wteh + 800, 1500)

n.pune("pat", 400, 400, 1800, 2100)
n.pune("dulap", Ww - 550, 200, 500, 2800)
n.pune("cada", 80, y_baie + 80, 1700, 700)
n.pune("lavoar", 80, y_baie + Hb - 450, 600, 400)
n.pune("wc", Ww - 500, y_baie + 200, 400, 600)
n.pune("pat1", 250, y_d2 + 400, 1400, 2000)
n.pune("dulap", Ww - 550, y_d2 + 80, 500, Hd2 - 160)
n.pune("canapea", xe + Wliv - 1000, 400, 900, 2200)
n.pune("masa", xe + 400, 2800, 1600, 1000)
n.pune("blat", x_kit + 80, y_s + Hk - 700, Wkit - 160, 600)
n.pune("chiuveta", x_kit + 300, y_s + Hk - 650, 600, 450)
n.pune("plita", IL - 700, y_s + 200, 600, 700)
n.pune("raft", x_teh + 80, y_s + 200, 800, 1400)
n.pune("dulap", xh + 80, y_s + 80, 500, Hk - 160)

m = Model(
    nume="Fina",
    titlu="PLAN PARTER",
    subtitlu="Casă parter compactă 82 m², două dormitoare · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "2"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după un proiect compact de 82 m². Acoperişul original era plat;",
        "aici şarpantă de lemn cu tablă fălţuită. Terasă 1,50 m în L, în afara anvelopei."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/fina.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/fina-el-%s.png" % lat)
