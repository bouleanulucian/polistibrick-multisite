#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NOLA — weekend, un dormitor.

Original cotat 10,50 × 6,50 m: living vertical 4,50 + terasă 2,00,
lățime 6,50 | 4,00. Anvelopă în L: corp 10,5 × 4,5, picior SE 4,0 × 2,0.
Terasă SV 6,5 × 2,0 în AFARA anvelopei. Intrare din terasă în hol.

  N  Living 16,00 | Baie 5,00 | Dormitor 15,04
     Living       | Hol  2,93 | Dormitor
  S  Terasă deschisă          | Tehnic 6,30

Pereții 38 / 13 lărgesc gabaritul. Ariile scrise rămân.
"""
from plansa import (Nivel, Model, plansa, verifica, descriere_fatada,
                    elevatie_png, PE, PI)

Wmid = 2000
Hbaie = round(5.00e6 / Wmid)             # 2500
h_hol = round(2.93e6 / Wmid)             # 1465
y_hol = Hbaie + PI                       # 2630
Hliv = y_hol + h_hol                     # 4095
Wliv = round(16.00e6 / Hliv)             # 3907
Wbed = round(15.04e6 / Hliv)             # 3673
xh = Wliv + PI                           # 4037
xe = xh + Wmid + PI                      # 6167
IL = xe + Wbed                           # 9840

W_ent = 900                              # gol de intrare pe sudul holului
x_tehw = xh + W_ent                      # 4937 — vestul tehnicului
w_teh = IL - x_tehw                      # 4903
Hteh = round(6.30e6 / w_teh)             # 1285
y_teh = Hliv + PI                        # 4225
IA = y_teh + Hteh                        # 5510

L, A = IL + 2 * PE, IA + 2 * PE          # 10600 × 6270

n = Nivel("PARTER", L, A)
n.poligon([
    (-PE, -PE),
    (IL + PE, -PE),
    (IL + PE, IA + PE),
    (x_tehw - PE, IA + PE),
    (x_tehw - PE, Hliv + PE),
    (-PE, Hliv + PE),
])

n.camera("Living · dining · bucătărie", 0, 0, Wliv, Hliv)
n.camera("Baie", xh, 0, Wmid, Hbaie)
n.camera("Hol", xh, y_hol, Wmid, h_hol)
n.camera("Dormitor", xe, 0, Wbed, Hliv)
n.camera("Tehnic", x_tehw, y_teh, w_teh, Hteh)

for w in [
    (Wliv, 0, PI, Hliv),                  # living | baie+hol
    (xh + Wmid, 0, PI, Hliv),             # hol+baie | dormitor
    (xh, Hbaie, Wmid, PI),                # baie | hol
    (x_tehw, Hliv, IL - x_tehw, PI),      # hol-est + dormitor | tehnic
]:
    n.perete(*w)

for t in [
    (Wliv, y_hol + 200, 900, False),      # hol → living
    (xh + 400, Hbaie, 800, True),         # hol → baie
    (xh + Wmid, y_hol + 280, 900, False), # hol → dormitor
    (x_tehw + 80, Hliv, 800, True),       # hol → tehnic
]:
    n.usa(*t)

n.gol_ext(400, Hliv, 2200, PE, usa=True)             # living → terasă
n.gol_ext(xh + 50, Hliv, 800, PE, usa=True)          # intrare terasă → hol
n.fereastra("N", 700, 1800)                          # living
n.fereastra("N", xh + 450, 900)                      # baie
n.fereastra("N", xe + 800, 1800)                     # dormitor
n.fereastra("V", 500, 1400)                          # living vest nord
n.fereastra("V", 2300, 1400)                         # living vest sud
n.fereastra("E", 700, 1800)                          # dormitor
n.fereastra("E", y_teh + 200, 900)                   # tehnic
n.fereastra("S", xe + 400, 1400)                     # tehnic sud

n.zona("Terasă", -PE, Hliv + PE, x_tehw, 2000)
n.zona("Intrare", xh - 200, Hliv + PE, W_ent + 400, 1100)

n.pune("blat", 80, 200, 600, 2400)
n.pune("plita", 140, 500, 450, 700)
n.pune("chiuveta", 140, 1400, 450, 600)
n.pune("masa", 1200, 1400, 1400, 900)
n.pune("canapea", Wliv - 1000, 400, 900, 1800)
n.pune("cada", xh + 150, 80, 1700, 700)
n.pune("lavoar", xh + 80, Hbaie - 480, 600, 400)
n.pune("wc", xh + Wmid - 500, Hbaie - 700, 400, 600)
n.pune("pat", xe + Wbed - 2100, 400, 1800, 2100)
n.pune("dulap", xe + 200, Hliv - 500, 2200, 450)
n.pune("masina", x_tehw + 80, y_teh + 80, 600, 600)
n.pune("raft", x_tehw + 800, y_teh + 80, 1400, 500)

m = Model(
    nume="Nola",
    titlu="PLAN PARTER",
    subtitlu="Casă weekend parter, un dormitor · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape, tablă fălţuită antracit",
    extra=[("Gabarit", "%.2f × %.2f m" % (L / 1000, A / 1000)),
           ("Dormitoare", "1"),
           ("Băi", "1")],
    observatii=[
        "Reprodusă după un proiect weekend de 45 m² utili, anvelopă în L:",
        "living 16,00, dormitor 15,04, terasă SV 2,00 m în afara anvelopei."])
m.nivel(n)

if __name__ == "__main__":
    pr = verifica(n)
    print("circulaţie:", "TRECE" if not pr else " | ".join(pr))
    plansa(m, "/private/tmp/planuri/nola.svg")
    print("gabarit %.2f × %.2f · util %.1f" % (L / 1000, A / 1000, n.util))
    for c in n.camere:
        print("   %-32s %5.2f × %5.2f = %5.2f"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
    for lat in "NSEV":
        print("   %s: %s" % (lat, descriere_fatada(n, lat)))
    for lat in "NS":
        elevatie_png(n, lat, "/private/tmp/planuri/nola-el-%s.png" % lat)
