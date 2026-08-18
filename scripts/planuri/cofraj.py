#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Preţul cofrajului pentru un model de casă, în cele trei sisteme.

Portat din motorul de devize al CRM-ului, aşa cum rulează el azi:
  crm/functions/src/ziiDevisConfig.ts
  crm/functions/src/ziiDevisEngine.ts
  crm/functions/src/ziiDevisPolistisip.ts

«Cofraj» = DOAR panourile. Zero beton, zero fier, zero manoperă, zero fundaţie.
  Polistibrick → panouri MBK (două feţe) + planşeu PBK
  Polistiwall  → panou WALL (o singură faţă, betonul rămâne aparent) + planşeu PBK
  PolistiSIP   → kitul: tălpi, pereţi, planşeu, I-joist, dulapi, prinderi, accesorii

Se verifică singur pe exemplele de control din cele două specuri: rulează
`python3 cofraj.py --control`.
"""
import math

# ── geometrie panouri (ziiDevisConfig.ts) ───────────────────────────────────
MBK_LAT = 1.20             # lăţime panou
MBK_H = 3.00               # înălţime panou
WALL_WASTE = 1.05          # +5% pierderi pe perimetru
H_STD = {"mbk_int": 3.00, "mbk_ext": 3.40, "wall_ext": 3.40}

PBK_M2 = 2.88              # un panou de planşeu
SIP_M2 = 3.40              # un panou de acoperiş
SIP_WASTE = 1.08

# ── preţuri EUR/buc (catalog, prin config) ──────────────────────────────────
PRET = {"MBK 70": 210.60, "MBK 100": 264.60, "MBK 140": 210.57, "MBK 200": 240.00,
        "PBK 200+": 193.00, "PBK 250+": 202.00, "PBK 300": 216.00,
        "WALL200": 225.00, "SIP300": 230.01, "SIP250": 205.19}

MBK_COMP = {"MBK 210+": ("MBK 70", "MBK 140"),
            "MBK 270+": ("MBK 70", "MBK 200"),
            "MBK 300+": ("MBK 100", "MBK 200")}

PBK_REGULI = [("PBK 200+", 5.5), ("PBK 250+", 7.0), ("PBK 300", 9.0)]

# ── PolistiSIP (ziiPolistisipConfig.ts) ─────────────────────────────────────
SIP_LAT, SIP_LUNG = 1.22, 2.80
P_IJOIST, P_DULAP, P_CONESPAN, P_HIDRO, P_ACCES = 10.51, 10.00, 2.00, 5.00, 50.00

# spumă adezivă: o cutie la 60 mp de cofraj (pereţi + planşee)
SPUMA_EUR, SPUMA_M2 = 72.00, 60.0
PBK_FIX = "PBK 250+"        # ordinul patronului: acelaşi planşeu peste tot

TVA = 0.21


def pozitii(perimetru):
    return math.ceil(perimetru / MBK_LAT * WALL_WASTE - 1e-9)


def panouri_pe_fata(perimetru, h_calcul):
    """poziţii × panouri întregi + panourile din care se taie benzile"""
    p = pozitii(perimetru)
    if p <= 0 or h_calcul <= 0:
        return 0
    intregi = math.floor(h_calcul / MBK_H + 1e-9)
    banda = round(h_calcul - intregi * MBK_H, 3)
    benzi = 0
    if banda > 0:
        benzi = math.ceil(p / max(1, math.floor(MBK_H / banda + 1e-9)))
    return p * intregi + benzi


def h_calcul(h_plan, standard):
    return h_plan if (h_plan is not None and h_plan > standard) else standard


def alege_pbk(deschidere):
    for ref, maxim in PBK_REGULI:
        if deschidere <= maxim:
            return ref
    return None


def panouri_sip(lungime, dim):
    """rest ≤ 0,5 panou → se adaugă jumătate; peste → panou întreg"""
    if lungime <= 0:
        return 0
    n = lungime / dim
    intreg = math.floor(n)
    rest = n - intreg
    if rest < 1e-6:
        return float(intreg)
    return float(intreg) + (0.5 if rest <= 0.5 else 1.0)


def dreptunghi(S, P):
    """laturile dreptunghiului cu suprafaţa S şi perimetrul P"""
    s = P / 2
    d = s * s - 4 * S
    if d < 0:
        L = math.sqrt(S)
        return L, L
    r = math.sqrt(d)
    return (s + r) / 2, (s - r) / 2


# ── cele trei sisteme, KITUL COMPLET ────────────────────────────────────────

def kit_beton(niveluri, wall=False, mbk_ref="MBK 210+"):
    """Polistibrick sau Polistiwall: panouri de perete + planşeu PBK + spumă."""
    linii, colle = [], 0.0
    for k, n in enumerate(niveluri):
        h_ext = h_calcul(n.get("h"), H_STD["wall_ext"] if wall else H_STD["mbk_ext"])
        h_int = round(h_ext - (H_STD["mbk_ext"] - H_STD["mbk_int"]), 2)
        n_ext = panouri_pe_fata(n["perimetru"], h_ext)
        if wall:
            linii.append(("Panou WALL200 · cofraj exterior 20 cm", n_ext, "buc", PRET["WALL200"]))
        else:
            i_ref, e_ref = MBK_COMP[mbk_ref]
            linii.append(("Panou %s · cofraj interior" % i_ref,
                          panouri_pe_fata(n["perimetru"], h_int), "buc", PRET[i_ref]))
            linii.append(("Panou %s · cofraj exterior" % e_ref, n_ext, "buc", PRET[e_ref]))
        colle += n["perimetru"] * (n.get("h") or 3.0)

        plan = niveluri[k + 1]["suprafata"] if k + 1 < len(niveluri) else n["suprafata"]
        linii.append(("Planşeu %s" % PBK_FIX, math.ceil(plan / PBK_M2 - 1e-9), "buc", PRET[PBK_FIX]))
        colle += plan

    cutii = max(1, math.ceil(colle / SPUMA_M2 - 1e-9))
    linii.append(("Spumă adezivă PU 750 ml · cutie de 12 (1 la 60 mp)", cutii, "buc", SPUMA_EUR))
    return linii, sum(q * p for _, q, _, p in linii)


def kit_sip(niveluri, acoperis="pente"):
    """PolistiSIP: kitul întreg — tălpi, pereţi, planşeu, grinzi, prinderi, accesorii."""
    perim = niveluri[0]["perimetru"]
    linii = [("Dulap 50×230 · talpă", round(perim, 2), "ml", P_DULAP),
             ("Prinderi Conespan", math.ceil(perim / 0.30), "buc", P_CONESPAN),
             ("Hidroizolaţie sub dulap", round(perim * 0.23, 2), "mp", P_HIDRO)]
    for i, n in enumerate(niveluri):
        pan = panouri_sip(n["perimetru"], SIP_LAT)
        linii.append(("Panouri perete SIP300", pan, "buc", PRET["SIP300"]))
        linii.append(("Grinzi I-joist · pereţi", round(pan * SIP_LUNG, 2), "ml", P_IJOIST))
        linii.append(("Dulap colţuri", 22.4, "ml", P_DULAP))
        linii.append(("Dulap coronament", round(n["perimetru"], 2), "ml", P_DULAP))
        if not (i == len(niveluri) - 1 and acoperis == "plate"):
            L, l = dreptunghi(n["suprafata"], n["perimetru"])
            a_l, a_s = panouri_sip(L, SIP_LAT), panouri_sip(l, SIP_LUNG)
            linii.append(("Panouri planşeu SIP250", a_l * a_s, "buc", PRET["SIP250"]))
            linii.append(("Grinzi I-joist · planşeu", round(a_l * 2 * l, 2), "ml", P_IJOIST))
        linii.append(("Accesorii montaj · şuruburi, cuie, spumă, conectori",
                      round(n["suprafata"], 2), "mp", P_ACCES))
    return linii, sum(q * p for _, q, _, p in linii)


def preturi(niveluri, acoperis="pente", mbk_ref="MBK 210+"):
    out = {}
    for cheie, (l, t) in (
            ("brick", kit_beton(niveluri, False, mbk_ref)),
            ("wall", kit_beton(niveluri, True)),
            ("sip", kit_sip(niveluri, acoperis))):
        out[cheie] = dict(linii=l, ht=round(t, 2), ttc=round(t * (1 + TVA), 2))
    return out


# ── verificare pe exemplele de control din specuri ──────────────────────────

def control():
    n = [dict(suprafata=100, perimetru=40, h=3.0, deschidere=5.0)]
    ok = True

    p = pozitii(40)
    ok &= (p == 35)
    print("  poziţii pe perimetru 40 m ......... %d   %s" % (p, "OK" if p == 35 else "AŞTEPTAT 35"))

    ext = panouri_pe_fata(40, 3.40)
    inte = panouri_pe_fata(40, 3.00)
    print("  panouri faţa exterioară (3,40 m) .. %d   %s" % (ext, "OK" if ext == 40 else "AŞTEPTAT 40"))
    print("  panouri faţa interioară (3,00 m) .. %d   %s" % (inte, "OK" if inte == 35 else "AŞTEPTAT 35"))
    ok &= (ext == 40 and inte == 35)

    pbk = alege_pbk(5.0)
    buc = math.ceil(100 / PBK_M2 - 1e-9)
    print("  planşeu: %s, %d buc ......... %s" % (pbk, buc, "OK" if (pbk, buc) == ("PBK 200+", 35) else "AŞTEPTAT PBK 200+ / 35"))
    ok &= (pbk, buc) == ("PBK 200+", 35)

    ps = panouri_sip(40, 1.22)
    print("  SIP: panouri perete ............... %.1f %s" % (ps, "OK" if ps == 33 else "AŞTEPTAT 33"))
    L, l = dreptunghi(100, 40)
    print("  SIP: dreptunghi echivalent ........ %.2f × %.2f m   %s" % (L, l, "OK" if abs(L - 10) < .01 else "AŞTEPTAT 10 × 10"))
    a_l, a_s = panouri_sip(L, 1.22), panouri_sip(l, 2.80)
    print("  SIP: panouri planşeu .............. %.1f × %.1f = %.1f   %s"
          % (a_l, a_s, a_l * a_s, "OK" if a_l * a_s == 34 else "AŞTEPTAT 34"))
    ok &= (ps == 33 and abs(L - 10) < .01 and a_l * a_s == 34)
    print("  Conespan .......................... %d   %s"
          % (math.ceil(40 / .3), "OK" if math.ceil(40 / .3) == 134 else "AŞTEPTAT 134"))
    ok &= math.ceil(40 / .3) == 134

    print()
    for k, v in preturi(n).items():
        print("  %-6s HT %9.2f €   TTC %9.2f €" % (k, v["ht"], v["ttc"]))
    return ok


if __name__ == "__main__":
    import sys
    if "--control" in sys.argv:
        print("VERIFICARE pe exemplele din specuri (casă 100 mp, perimetru 40 m):\n")
        print("\n  TOATE VERIFICĂRILE TREC" if control() else "\n  ✗ NU TRECE")
