#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RUNA — casă parter, acoperiş în două ape, fronton vitrat spre terasă.

Tema e luată din proiectul de referinţă măsurat (15,65 × 8,75 m, 12 camere,
95,8 m² utili): zi la est, noapte la vest, hol la mijloc, terasă acoperită sub
prelungirea şarpantei. Desenul e al nostru, pe perete Polistibrick de 38 cm.

Coordonatele sunt INTERIOARE: (0,0) e colţul nord-vest al feţei interioare.
Interiorul are 14,84 × 8,04 m.
"""
from plansa import Nivel, Model, plansa, verifica, PE, PI

L, A = 14000, 8800          # casa închisă; cu terasa scobită, volumul e 15,60 × 8,80
IL, IA = L - 2 * PE, A - 2 * PE            # 14840 × 8040

N1 = 3450                                   # banda de nord
H0, H1 = N1 + PI, N1 + PI + 1200            # holul, 1,20 m
S0 = H1 + PI                                # banda de sud
SD = IA - S0                                # 3130
DIV = 8000                                  # despărţirea zi / noapte

n = Nivel("PARTER", L, A)

# ── noapte, la vest ────────────────────────────────────────────────────────
n.camera("Dormitor 1", 0, 0, 3300, N1)
n.camera("Dormitor 2", 3430, 0, 3070, N1)
n.camera("Baie 2", 6630, 0, 1370, N1)

n.camera("Hol", 0, H0, DIV, 1200)

n.camera("Dormitor 3", 0, S0, 3100, SD)
n.camera("Baie", 3230, S0, 1870, SD)
n.camera("Cămară · tehnic", 5230, S0, 1170, SD)
n.camera("Intrare", 6530, S0, 1470, SD)

# ── zi, la est ─────────────────────────────────────────────────────────────
ZI = DIV + PI
n.camera("Living · bucătărie · dining", ZI, 0, IL - ZI, IA)

# ── compartimentări ────────────────────────────────────────────────────────
for w in [(3300, 0, PI, N1), (6500, 0, PI, N1),
          (0, N1, DIV, PI), (0, H1, DIV, PI),
          (3100, S0, PI, SD), (5100, S0, PI, SD), (6400, S0, PI, SD),
          (DIV, 0, PI, IA)]:
    n.perete(*w)

# ── uşi: totul se deschide din hol, nu se trece prin nicio cameră ──────────
for (x, y, l, oriz) in [
        (1200, N1, 900, True),        # hol → dormitor 1
        (4600, N1, 900, True),        # hol → dormitor 2
        (6900, N1, 800, True),        # hol → baie 2
        (1100, H1, 900, True),        # hol → dormitor 3
        (3700, H1, 800, True),        # hol → baie
        (5500, H1, 800, True),        # hol → cămară
        (6800, H1, 900, True),        # hol → intrare
        (DIV, 3750, 1000, False),     # hol → living
]:
    n.usa(x, y, l, oriz)

n.usa_ext("S", 6800, 1100)                  # uşa de intrare
n.usa_ext("E", 1200, 2400)                  # living → terasa acoperită

# ── ferestre ───────────────────────────────────────────────────────────────
n.fereastra("N", 900, 1800)                 # dormitor 1
n.fereastra("N", 4200, 1800)                # dormitor 2
n.fereastra("N", 6900, 800)                 # baie 2
n.fereastra("V", 800, 1500)                 # dormitor 1, spre vest
n.fereastra("V", 5400, 1600)                # dormitor 3, spre vest
n.fereastra("S", 700, 1800)                 # dormitor 3
n.fereastra("S", 3800, 900)                 # baie
n.fereastra("N", 8600, 3200)                # living, nord
n.fereastra("S", 8600, 2400)                # bucătărie, sud
n.fereastra("E", 4200, 3200)                # frontonul vitrat

# ── terasa acoperită, sub prelungirea şarpantei ────────────────────────────
n.zona("Terasă acoperită", IL + PE, -PE, 1600, A)   # scobită: pereţii şi acoperişul continuă

# ── mobilier ───────────────────────────────────────────────────────────────
n.pune("pat", 800, 600, 1800, 2100).pune("dulap", 2750, 600, 700, 2100)
n.pune("pat", 4300, 600, 1800, 2100).pune("dulap", 6250, 600, 650, 2100)
n.pune("dus", 7250, 300, 900, 900).pune("lavoar", 7250, 1500, 700, 450)
n.pune("wc", 7300, 2400, 400, 600).pune("masina", 8000, 2400, 600, 600)

n.pune("pat", 500, 5400, 1800, 2100).pune("dulap", 2500, 5400, 650, 2100)
n.pune("cada", 3550, 5150, 1750, 750).pune("lavoar", 3600, 6400, 700, 450)
n.pune("wc", 3600, 7300, 400, 600)
n.pune("raft", 5650, 5150, 1100, 700).pune("raft", 5650, 6500, 1100, 700)
n.pune("dulap", 7150, 5150, 1400, 600)

n.pune("blat", 8400, 6900, 3200, 650).pune("plita", 9700, 7000, 700, 450)
n.pune("chiuveta", 10200, 7000, 600, 450)
n.pune("blat", 8400, 5300, 2800, 950).pune("scaune", 9500, 4750, 2200, 430)
n.pune("masa", 10600, 1500, 2300, 1050).pune("scaune", 11500, 950, 2100, 430)
n.pune("scaune", 10700, 2650, 2100, 430)
n.pune("canapea", 8600, 1400, 950, 2500).pune("canapea", 9400, 4000, 2700, 950)
n.pune("soba", 12600, 3600, 850, 400)

m = Model(
    nume="Runa",
    titlu="PLAN PARTER",
    subtitlu="Casă pe un nivel, şarpantă clasică · sistem Polistibrick",
    acoperis="Şarpantă clasică din lemn, două ape 30°",
    extra=[("Terasă acoperită", "14,1 m²"),
           ("Volum sub acoperiş", "15,60 × 8,80 m"),
           ("Dormitoare", "3")],
    observatii=[
        "Zi şi noapte despărţite de hol: nu se trece prin nicio cameră.",
        "Terasa e scobită în volum: pereţii laterali şi acoperişul merg până la capăt,\n        fără niciun stâlp.",
        "Cele două băi şi cămara tehnică stau pe aceeaşi coloană de instalaţii.",
    ])
m.nivel(n)

if __name__ == "__main__":
    p = verifica(n)
    print("verificare circulaţie: %s" % ("TRECE" if not p else "%d probleme" % len(p)))
    for x in p:
        print("   ✗", x)
    plansa(m, "/private/tmp/planuri/runa.svg")
    print("\namprentă %.1f m² · util %.1f m²" % (n.amprenta, n.util))
    for c in n.camere:
        print("   %-28s %5.2f × %5.2f = %5.1f m²"
              % (c["nume"], c["w"] / 1000, c["h"] / 1000, c["w"] * c["h"] / 1e6))
