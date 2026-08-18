#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Motor de planşe pentru modelele Polistibrick.

Desenează o planşă în limbajul celor 11 existente: perete exterior de 38 cm
în trei straturi hașurate, compartimentări de 13 cm, goluri de uşă marcate cu
pragul (fără sensul de deschidere), ferestre în trei linii, mobilier, tablou
de suprafeţe, alcătuirea pereţilor, observaţii, scară grafică, nord.

Noutatea faţă de planşele vechi: COTELE, pe fiecare latură.

Un model se descrie în milimetri. Coordonatele camerelor sunt INTERIOARE:
(0,0) e colţul nord-vest al feţei interioare a peretelui exterior.
"""
import math
from pathlib import Path

LINIE = "#1a1714"
SLAB = "#8a8178"
STINS = "#b3aca3"
FONT = "'Inter','Helvetica Neue','Helvetica',Arial,sans-serif"

PE = 380          # cofraj Polistibrick MBK 210
IZO_EXT = 148     # PSE 140 + fibrociment 8, la exterior
BETON = 150       # miezul de beton armat
IZO_INT = 82      # PSE 70 + fibrociment 12, la interior
PI = 130          # compartimentare



def _inset(pts, d):
    """retrage un poligon rectiliniu cu d spre interior.
    Se retrage fiecare muchie pe normala ei interioară, apoi vârful e
    intersecţia muchiilor retrase. Aşa ies corect şi colţurile reflexe."""
    n = len(pts)
    A2 = sum(pts[i][0]*pts[(i+1) % n][1] - pts[(i+1) % n][0]*pts[i][1] for i in range(n))
    s = 1.0 if A2 > 0 else -1.0
    lin = []                                   # pentru fiecare muchie: ('H', y) sau ('V', x)
    for i in range(n):
        x0, y0 = pts[i]; x1, y1 = pts[(i+1) % n]
        dx, dy = x1 - x0, y1 - y0
        nx, ny = s * dy, -s * dx
        m = max(abs(nx), abs(ny)) or 1.0
        nx, ny = nx / m, ny / m
        lin.append(('H', y0 + d * ny) if abs(dy) < 1e-9 else ('V', x0 + d * nx))
    out = []
    for i in range(n):
        a = lin[(i - 1) % n]; b = lin[i]
        if a[0] == 'H' and b[0] == 'V':   out.append((b[1], a[1]))
        elif a[0] == 'V' and b[0] == 'H': out.append((a[1], b[1]))
        else:                             out.append(pts[i])
    return out


# ─── model ──────────────────────────────────────────────────────────────────

class Nivel:
    def __init__(self, nume, L, A, pe=PE):
        self.nume, self.L, self.A, self.pe = nume, L, A, pe
        self.rotit = False
        self.contur = None                 # poligon rectiliniu, în mm; None = dreptunghi L×A
        self.camere, self.pereti, self.goluri, self.mobila = [], [], [], []
        self.zone = []                     # terase etc., punctate
        self.nise = []                     # goluri tăiate în volum

    def poligon(self, puncte):
        """conturul exterior al zidăriei, rectiliniu, în mm, sens orar"""
        self.contur = list(puncte)
        return self

    def camera(self, nume, x, y, w, h, tip="camera"):
        self.camere.append(dict(nume=nume, x=x, y=y, w=w, h=h, tip=tip))
        return self

    def gol_ext(self, x, y, w, h, usa=False):
        """gol tăiat în peretele exterior, în coordonate absolute.
        Se foloseşte când casa nu e dreptunghi şi faţa nu e N/S/E/V."""
        self.goluri.append(dict(fel="ext_abs", x=x, y=y, l=w, h=h, usa=usa))
        return self

    def perete(self, x, y, w, h):
        """compartimentare, în coordonate interioare"""
        self.pereti.append((x, y, w, h))
        return self

    def usa(self, x, y, lung, orizontal=True, desen=True):
        self.goluri.append(dict(fel="usa", x=x, y=y, l=lung, oriz=orizontal, desen=desen))
        return self

    def usa_ext(self, latura, poz, lung):
        self.goluri.append(dict(fel="usa_ext", latura=latura, poz=poz, l=lung))
        return self

    def fereastra(self, latura, poz, lung):
        """latura: N S E V — poziţia se măsoară pe faţa interioară"""
        self.goluri.append(dict(fel="fereastra", latura=latura, poz=poz, l=lung))
        return self

    def nisa(self, latura, poz, lat, adanc):
        """gol dreptunghiular tăiat în volum — intrarea retrasă, ca la Oaxaca"""
        self.nise.append(dict(latura=latura, poz=poz, lat=lat, adanc=adanc))
        return self

    def zona(self, nume, x, y, w, h):
        self.zone.append(dict(nume=nume, x=x, y=y, w=w, h=h))
        return self

    def roteste(self):
        """Roteşte nivelul 90° în sens orar: casa adâncă se aşază pe orizontală.

        Se rotesc DATELE, nu desenul — aşa etichetele rămân drepte şi se întoarce
        doar nordul. Punct: (x, y) → (IA − y, x).
        """
        IA = self.A - 2 * self.pe
        def rot(x, y, w, h):
            return IA - y - h, x, h, w
        if self.contur:
            self.contur = [(IA - y, x) for (x, y) in self.contur]
        self.camere = [dict(c, **dict(zip("xywh", rot(c["x"], c["y"], c["w"], c["h"]))))
                       for c in self.camere]
        self.pereti = [rot(*w) for w in self.pereti]
        self.mobila = [dict(m, **dict(zip("xywh", rot(m["x"], m["y"], m["w"], m["h"]))))
                       for m in self.mobila]
        self.zone = [dict(z, **dict(zip("xywh", rot(z["x"], z["y"], z["w"], z["h"]))))
                     for z in self.zone]
        LAT = {"N": "E", "E": "S", "S": "V", "V": "N"}
        gol = []
        for g in self.goluri:
            if g["fel"] == "ext_abs":
                x2, y2, w2, h2 = IA - g["y"] - g["h"], g["x"], g["h"], g["l"]
                gol.append(dict(g, x=x2, y=y2, l=w2, h=h2))
                continue
            if g["fel"] == "usa":
                if g["oriz"]:
                    x, y, w, h = rot(g["x"], g["y"], g["l"], PI)
                    gol.append(dict(g, x=x, y=y, l=h, oriz=False))
                else:
                    x, y, w, h = rot(g["x"], g["y"], PI, g["l"])
                    gol.append(dict(g, x=x, y=y, l=w, oriz=True))
            else:
                lat, p, l = g["latura"], g["poz"], g["l"]
                nou = LAT[lat]
                poz = p if lat in "NS" else IA - p - l
                if lat == "E":
                    poz = IA - p - l
                elif lat == "V":
                    poz = IA - p - l
                gol.append(dict(g, latura=nou, poz=poz))
        self.goluri = gol
        LATN = {"N": "E", "E": "S", "S": "V", "V": "N"}
        self.nise = [dict(z, latura=LATN[z["latura"]],
                          poz=(z["poz"] if z["latura"] in "NS" else IA - z["poz"] - z["lat"]))
                     for z in self.nise]
        self.L, self.A = self.A, self.L
        self.rotit = True
        return self

    def pune(self, fel, x, y, w, h, rot=0):
        self.mobila.append(dict(fel=fel, x=x, y=y, w=w, h=h, rot=rot))
        return self

    @property
    def amprenta(self):
        if self.contur:
            p = self.contur
            a = sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1]
                    for i in range(len(p)))
            return abs(a) / 2 / 1e6
        return self.L * self.A / 1e6

    @property
    def util(self):
        return sum(c["w"] * c["h"] for c in self.camere if c["tip"] == "camera") / 1e6


def verifica(n):
    """fiecare cameră trebuie să fie ajunsă din intrare, fără să treci prin alta"""
    def atinge(c, g):
        if g["fel"] == "usa":
            if g["oriz"]:
                in_x = c["x"] - 1 <= g["x"] and g["x"] + g["l"] <= c["x"] + c["w"] + 1
                pe_y = (abs(g["y"] - c["y"]) < 200
                        or abs(g["y"] + PI - c["y"]) < 200
                        or abs(g["y"] - (c["y"] + c["h"])) < 200)
                return in_x and pe_y
            in_y = c["y"] - 1 <= g["y"] and g["y"] + g["l"] <= c["y"] + c["h"] + 1
            pe_x = (abs(g["x"] - c["x"]) < 200
                    or abs(g["x"] + PI - c["x"]) < 200
                    or abs(g["x"] - (c["x"] + c["w"])) < 200)
            return in_y and pe_x
        return False

    prob = []
    leg = {c["nume"]: set() for c in n.camere}
    for g in n.goluri:
        if g["fel"] != "usa":
            continue
        au = [c["nume"] for c in n.camere if atinge(c, g)]
        # o uşă poate da şi într-o terasă, care nu e cameră
        spre_zona = any(atinge(z, g) for z in n.zone)
        if len(au) < 2 and not (len(au) == 1 and spre_zona):
            prob.append("uşă la (%d,%d) leagă %d cameră(e): %s"
                        % (g["x"], g["y"], len(au), ", ".join(au) or "niciuna"))
        for a in au:
            for b in au:
                if a != b:
                    leg[a].add(b)

    start = next((c["nume"] for c in n.camere if "ntrare" in c["nume"]), None)
    if start and not [g for g in n.goluri if g["fel"] == "usa_ext"]:
        prob.append("nu există uşă de intrare în peretele exterior")
    if not start:      # etaj: se pleacă de la scară / palier
        start = next((c["nume"] for c in n.camere
                      if any(k in c["nume"].lower() for k in ("palier", "hol", "coridor"))), None)
    if start:
        vaz, cd = {start}, [start]
        while cd:
            for v in leg[cd.pop()]:
                if v not in vaz:
                    vaz.add(v); cd.append(v)
        for c in n.camere:
            if c["nume"] not in vaz:
                prob.append("«%s» nu se poate ajunge din intrare" % c["nume"])
    else:
        prob.append("nivelul nu are nici intrare, nici palier/hol de pornire")

    return prob


TBK_MAX = 4500          # deschidere max. între reazeme, panou acoperiş TBK/SIP250


def verifica_acoperis(n, panta_grade=30, coama_pe_lung=True):
    """panoul de acoperiş nu poate sări mai mult de 4,5 m între reazeme"""
    lat = n.A if coama_pe_lung else n.L
    orizontal = lat / 2
    pe_panta = orizontal / math.cos(math.radians(panta_grade))
    return dict(orizontal=orizontal, pe_panta=pe_panta, ok=pe_panta <= TBK_MAX,
                pane=max(1, math.ceil(pe_panta / TBK_MAX)))


class Model:
    def __init__(self, nume, titlu, subtitlu, acoperis, observatii=(), extra=()):
        self.nume, self.titlu, self.subtitlu = nume, titlu, subtitlu
        self.acoperis, self.observatii, self.extra = acoperis, list(observatii), list(extra)
        self.niveluri = []

    def nivel(self, n):
        self.niveluri.append(n)
        return self


# ─── primitive de desen ─────────────────────────────────────────────────────

def T(x, y, s, m=15, anc="middle", col=LINIE, sp=0, gr=400, op=1):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{m}" '
            f'fill="{col}" text-anchor="{anc}" letter-spacing="{sp}" font-weight="{gr}" '
            f'opacity="{op}">{s}</text>')


def L_(x1, y1, x2, y2, w=1.0, col=LINIE, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{col}" stroke-width="{w}"{d}/>')


def R(x, y, w, h, fill="none", stroke=LINIE, sw=1.0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


# ─── mobilier: linie subţire, ca pe planşele vechi ──────────────────────────

def mobila(fel, x, y, w, h):
    o, s, c = [], 1.0, LINIE
    if fel == "pat":                                   # pat cu pernă
        o.append(R(x, y, w, h, "none", c, s))
        o.append(R(x + w * .08, y + h * .06, w * .84, h * .26, "none", c, .8))
    elif fel == "pat1":
        o.append(R(x, y, w, h, "none", c, s))
        o.append(R(x + w * .12, y + h * .05, w * .76, h * .2, "none", c, .8))
    elif fel == "dulap":
        o.append(R(x, y, w, h, "none", c, s))
        o.append(L_(x, y, x + w, y + h, .7))
        o.append(L_(x + w, y, x, y + h, .7))
    elif fel == "canapea":
        o.append(R(x, y, w, h, "none", c, s))
        o.append(R(x, y, w, h * .3, "none", c, .8))
    elif fel == "masa":
        o.append(R(x, y, w, h, "none", c, s))
    elif fel == "scaune":                               # şir de scaune
        n = max(2, int(w // 520))
        p = w / n
        for i in range(n):
            o.append(R(x + i * p + p * .16, y, p * .68, h, "none", c, .8))
    elif fel == "blat":                                 # blat de bucătărie
        o.append(R(x, y, w, h, "none", c, s))
        o.append(L_(x, y + h * .5, x + w, y + h * .5, .5, STINS))
    elif fel == "plita":
        o.append(R(x, y, w, h, "none", c, .9))
        for i in range(2):
            for j in range(2):
                cx, cy = x + w * (.28 + .44 * i), y + h * (.3 + .4 * j)
                o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{min(w,h)*.11:.1f}" '
                         f'fill="none" stroke="{c}" stroke-width="0.8"/>')
    elif fel == "chiuveta":
        o.append(R(x, y, w, h, "none", c, .9))
        o.append(f'<circle cx="{x+w*.5:.1f}" cy="{y+h*.55:.1f}" r="{min(w,h)*.22:.1f}" '
                 f'fill="none" stroke="{c}" stroke-width="0.8"/>')
    elif fel == "cada":
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{min(w,h)*.12:.1f}" '
                 f'fill="none" stroke="{c}" stroke-width="1"/>')
        o.append(f'<circle cx="{x+w*.86:.1f}" cy="{y+h*.5:.1f}" r="{min(w,h)*.07:.1f}" '
                 f'fill="none" stroke="{c}" stroke-width="0.7"/>')
    elif fel == "dus":
        o.append(R(x, y, w, h, "none", c, 1))
        o.append(L_(x, y, x + w, y + h, .6, STINS))
    elif fel == "lavoar":
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{min(w,h)*.2:.1f}" '
                 f'fill="none" stroke="{c}" stroke-width="0.9"/>')
    elif fel == "wc":
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{min(w,h)*.34:.1f}" '
                 f'fill="none" stroke="{c}" stroke-width="0.9"/>')
    elif fel == "masina":                               # maşină de spălat
        o.append(R(x, y, w, h, "none", c, .9))
        o.append(f'<circle cx="{x+w*.5:.1f}" cy="{y+h*.5:.1f}" r="{min(w,h)*.28:.1f}" '
                 f'fill="none" stroke="{c}" stroke-width="0.7"/>')
    elif fel == "soba":                                 # şemineu
        o.append(R(x, y, w, h, "none", c, 1))
        o.append(R(x + w * .2, y + h * .25, w * .6, h * .5, "none", c, .7))
    elif fel == "raft":
        o.append(R(x, y, w, h, "none", c, .8))
        n = max(2, int(h // 380))
        for i in range(1, n):
            o.append(L_(x, y + h * i / n, x + w, y + h * i / n, .5, STINS))
    return "".join(o)


# ─── planul propriu-zis ─────────────────────────────────────────────────────

def deseneaza(n: Nivel, ox, oy, k):
    """k = px pe mm"""
    def X(mm): return ox + mm * k
    def Y(mm): return oy + mm * k
    def D(mm): return mm * k

    pe = n.pe
    o = []

    # ── cofrajul Polistibrick: izolaţie 14,8 · beton 15 · izolaţie 8,2
    W, H = D(n.L), D(n.A)
    ox0, oy0 = X(0) - D(pe), Y(0) - D(pe)
    straturi = [(0, "url(#izo)"), (IZO_EXT, "url(#bet)"),
                (IZO_EXT + BETON, "url(#izo)"), (pe, "#ffffff")]
    if n.contur:
        ext = list(n.contur)   # conturul dat e chiar faţa exterioară

        def _aria(pl):
            return abs(sum(pl[i][0] * pl[(i + 1) % len(pl)][1]
                           - pl[(i + 1) % len(pl)][0] * pl[i][1]
                           for i in range(len(pl)))) / 2

        def spre_interior(pl, d):
            """retragere care chiar micşorează poligonul, oricare i-ar fi sensul"""
            if d == 0:
                return list(pl)
            cand = _inset(pl, d)
            return cand if _aria(cand) < _aria(pl) else _inset(pl, -d)
        for (adanc, umplere) in straturi:
            pl = spre_interior(ext, adanc)
            pts = " ".join("%.1f,%.1f" % (X(px), Y(py)) for px, py in pl)
            o.append('<polygon points="%s" fill="%s" stroke="none"/>' % (pts, umplere))
        for adanc, gros in ((0, 1.4), (IZO_EXT, 0.7), (IZO_EXT + BETON, 0.7), (pe, 1.4)):
            pl = spre_interior(ext, adanc)
            pts = " ".join("%.1f,%.1f" % (X(px), Y(py)) for px, py in pl)
            o.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="%s"/>'
                     % (pts, LINIE, gros))
    else:
        for (adanc, umplere) in straturi:
            d_ = D(adanc)
            o.append(R(ox0 + d_, oy0 + d_, W - 2 * d_, H - 2 * d_, umplere, "none", 0))
        for adanc, gros in ((0, 1.4), (IZO_EXT, 0.7), (IZO_EXT + BETON, 0.7), (pe, 1.4)):
            d_ = D(adanc)
            o.append(R(ox0 + d_, oy0 + d_, W - 2 * d_, H - 2 * d_, "none", LINIE, gros))

    # ── zonele punctate (terasă) — sub casă
    for z in n.zone:
        o.append(R(X(z["x"]), Y(z["y"]), D(z["w"]), D(z["h"]), "none", STINS, 1.0, "7 5"))
        zx, zy = X(z["x"] + z["w"] / 2), Y(z["y"] + z["h"] / 2)
        if z["w"] < z["h"]:
            o.append(f'<g transform="translate({zx:.1f},{zy:.1f}) rotate(-90)">'
                     + T(0, 5, z["nume"].upper(), 15, "middle", STINS, 3.2, 400) + '</g>')
        else:
            o.append(T(zx, zy + 5, z["nume"].upper(), 15, "middle", STINS, 3.2, 400))

    # ── nişele tăiate în volum
    for z in n.nise:
        lat, p, l, ad = z["latura"], z["poz"], z["lat"], z["adanc"]
        if lat in "NS":
            x0 = X(p)
            y0 = Y(0) - D(pe) if lat == "N" else Y(n.A - 2 * pe) + D(pe) - D(ad)
            o.append(R(x0, y0, D(l), D(ad), "#ffffff", "none", 0))
            o.append(R(x0, y0, D(l), D(ad), "none", LINIE, 1.2))
        else:
            y0 = Y(p)
            x0 = X(0) - D(pe) if lat == "V" else X(n.L - 2 * pe) + D(pe) - D(ad)
            o.append(R(x0, y0, D(ad), D(l), "#ffffff", "none", 0))
            o.append(R(x0, y0, D(ad), D(l), "none", LINIE, 1.2))

    # ── compartimentări
    for (x, y, w, h) in n.pereti:
        o.append(R(X(x), Y(y), D(w), D(h), "url(#p3)", LINIE, 0.9))

    # ── goluri: se albesc peste perete, apoi se marchează pragul / fereastra
    for g in n.goluri:
        if g["fel"] == "ext_abs":
            gx, gy, gw, gh = g["x"], g["y"], g["l"], g["h"]
            oriz = gw >= gh
            o.append(R(X(gx), Y(gy), D(gw), D(gh), "#ffffff", "none", 0))
            usa_ = g.get("usa")
            if oriz:
                for i in ([0.5] if usa_ else range(3)):
                    yy = Y(gy) + D(gh) * (0.86 if usa_ else (0.22 + 0.28 * i))
                    o.append(L_(X(gx), yy, X(gx + gw), yy, 1.0 if usa_ else 0.8))
                o.append(L_(X(gx), Y(gy), X(gx), Y(gy + gh), 1.0))
                o.append(L_(X(gx + gw), Y(gy), X(gx + gw), Y(gy + gh), 1.0))
            else:
                for i in ([0.5] if usa_ else range(3)):
                    xx = X(gx) + D(gw) * (0.86 if usa_ else (0.22 + 0.28 * i))
                    o.append(L_(xx, Y(gy), xx, Y(gy + gh), 1.0 if usa_ else 0.8))
                o.append(L_(X(gx), Y(gy), X(gx + gw), Y(gy), 1.0))
                o.append(L_(X(gx), Y(gy + gh), X(gx + gw), Y(gy + gh), 1.0))
            continue
        if g["fel"] == "usa":
            if not g.get("desen", True):
                continue
            if g["oriz"]:
                o.append(R(X(g["x"]), Y(g["y"]) - 1, D(g["l"]), D(PI) + 2, "#ffffff", "none", 0))
                o.append(L_(X(g["x"]), Y(g["y"]) + D(PI) / 2, X(g["x"] + g["l"]),
                            Y(g["y"]) + D(PI) / 2, 0.8, STINS))
            else:
                o.append(R(X(g["x"]) - 1, Y(g["y"]), D(PI) + 2, D(g["l"]), "#ffffff", "none", 0))
                o.append(L_(X(g["x"]) + D(PI) / 2, Y(g["y"]), X(g["x"]) + D(PI) / 2,
                            Y(g["y"] + g["l"]), 0.8, STINS))
        else:
            lat, p, l = g["latura"], g["poz"], g["l"]
            ext_usa = g["fel"] == "usa_ext"
            if lat in "NS":
                y0 = Y(0) - D(pe) if lat == "N" else Y(n.A - 2 * pe)
                o.append(R(X(p), y0, D(l), D(pe), "#ffffff", "none", 0))
                for i in ([0.5] if ext_usa else range(3)):
                    yy = y0 + D(pe) * (0.86 if ext_usa else (0.22 + 0.28 * i))
                    o.append(L_(X(p), yy, X(p + l), yy, 1.0 if ext_usa else 0.8))
                o.append(L_(X(p), y0, X(p), y0 + D(pe), 1.0))
                o.append(L_(X(p + l), y0, X(p + l), y0 + D(pe), 1.0))
            else:
                x0 = X(0) - D(pe) if lat == "V" else X(n.L - 2 * pe)
                o.append(R(x0, Y(p), D(pe), D(l), "#ffffff", "none", 0))
                for i in ([0.5] if ext_usa else range(3)):
                    xx = x0 + D(pe) * (0.86 if ext_usa else (0.22 + 0.28 * i))
                    o.append(L_(xx, Y(p), xx, Y(p + l), 1.0 if ext_usa else 0.8))
                o.append(L_(x0, Y(p), x0 + D(pe), Y(p), 1.0))
                o.append(L_(x0, Y(p + l), x0 + D(pe), Y(p + l), 1.0))

    # ── mobilier
    for m in n.mobila:
        o.append(mobila(m["fel"], X(m["x"]), Y(m["y"]), D(m["w"]), D(m["h"])))

    # ── etichetele camerelor
    for c in n.camere:
        cx, cy = X(c["x"] + c["w"] / 2), Y(c["y"] + c["h"] / 2)
        s = c["w"] * c["h"] / 1e6
        et = c["nume"].upper()
        def lat(mm_):
            return len(et) * (mm_ * 0.60 + 2.6)
        vert = lat(10.5) > D(c["w"]) - 14 and c["h"] > c["w"]
        loc = D(c["h"] if vert else c["w"]) - 14
        m = 16.0
        while m > 9.0 and lat(m) > loc:
            m -= 0.5
        if vert:
            lt = lat(m) / 2 + 10
            o.append(R(cx - m - 6, cy - lt, 2 * m + 18, 2 * lt, "#ffffff", "none", 0))
            o.append(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate(-90)">'
                     + T(0, -2, et, m, "middle", LINIE, 2.6, 400)
                     + T(0, m + 5, f"{s:.1f} m²", m - 2, "middle", SLAB) + '</g>')
        else:
            lt = lat(m) / 2 + 10
            o.append(R(cx - lt, cy - m - 6, 2 * lt, 2 * m + 18, "#ffffff", "none", 0))
            o.append(T(cx, cy - 2, et, m, "middle", LINIE, 2.6, 400))
            o.append(T(cx, cy + m + 5, f"{s:.1f} m²", m - 2, "middle", SLAB))

    return "".join(o), (X(0) - D(pe), Y(0) - D(pe), W, H)


def fatada(n, latura, ox, oy, k, h_perete=3000, atic=500):
    """Faţada desenată DIN PLAN: aceleaşi goluri, la aceleaşi poziţii.

    De aici iese şi descrierea randării, deci desenul şi imaginea nu au cum
    să difere: nu poate apărea o fereastră în 3D care nu e pe plan.
    """
    IL, IA = n.L - 2 * n.pe, n.A - 2 * n.pe
    lung = n.L if latura in "NS" else n.A
    o = [R(ox, oy, lung * k, (h_perete + atic) * k, "#ffffff", LINIE, 1.4)]
    o.append(L_(ox, oy + atic * k, ox + lung * k, oy + atic * k, 0.7, STINS))

    for g in n.goluri:
        if g["fel"] not in ("fereastra", "usa_ext") or g["latura"] != latura:
            continue
        p, l = g["poz"], g["l"]
        # poziţia pe faţă, măsurată din colţul din stânga al elevaţiei
        if latura in ("N", "S"):
            x = p + n.pe if latura == "N" else (IL - p - l) + n.pe
        else:
            x = p + n.pe if latura == "E" else (IA - p - l) + n.pe
        usa = g["fel"] == "usa_ext"
        sus = atic + (200 if usa else 900)
        jos = atic + h_perete - (0 if usa else 200)
        o.append(R(ox + x * k, oy + sus * k, l * k, (jos - sus) * k,
                   "#eef1f2" if not usa else "#f6f2ea", LINIE, 1.1))
        if usa:
            o.append(L_(ox + (x + l / 2) * k, oy + sus * k,
                        ox + (x + l / 2) * k, oy + jos * k, 0.7, STINS))
    o.append(T(ox + lung * k / 2, oy + (h_perete + atic) * k + 26,
               {"N": "NORD", "S": "SUD", "E": "EST", "V": "VEST"}[latura],
               13, "middle", SLAB, 2.2, 400))
    return "".join(o), lung * k


def descriere_fatada(n, latura, h_perete=3000):
    """Aceleaşi goluri, dar în cuvinte — pentru descrierea randării."""
    IL, IA = n.L - 2 * n.pe, n.A - 2 * n.pe
    lung = (n.L if latura in "NS" else n.A) / 1000
    fer = [g for g in n.goluri if g["fel"] == "fereastra" and g["latura"] == latura]
    usi = [g for g in n.goluri if g["fel"] == "usa_ext" and g["latura"] == latura]
    buc = []
    for g in sorted(fer, key=lambda g: g["poz"]):
        buc.append("%.2f m wide window" % (g["l"] / 1000))
    txt = "%.2f metre facade" % lung
    if buc:
        txt += " with exactly %d window%s (%s)" % (len(buc), "" if len(buc) == 1 else "s",
                                                   ", ".join(buc))
    else:
        txt += " with NO windows at all, a completely blank wall"
    if usi:
        txt += " and %d door opening%s" % (len(usi), "" if len(usi) == 1 else "s")
    IL_, IA_ = n.L - 2 * n.pe, n.A - 2 * n.pe
    nis = [z for z in n.nise if z["latura"] == latura]
    # terasele scobite ating peretele exterior: contează tot ca gol în volum
    for z in n.zone:
        atinge = {"N": z["y"] <= 1, "S": z["y"] + z["h"] >= IA_ - 1,
                  "V": z["x"] <= 1, "E": z["x"] + z["w"] >= IL_ - 1}[latura]
        if atinge:
            lat_ = z["w"] if latura in "NS" else z["h"]
            ad_ = z["h"] if latura in "NS" else z["w"]
            txt += (". A large %.2f m wide and %.2f m deep open-air terrace is carved "
                    "into the volume on this facade, its side walls in the same plaster"
                    % (lat_ / 1000, ad_ / 1000))
            nis = nis + ["terasa"]
    for z in [x for x in nis if isinstance(x, dict)]:
        txt += (". A %.2f m wide and %.2f m deep rectangular niche is cut into this "
                "facade, the entrance door sits at the back of it" % (z["lat"]/1000, z["adanc"]/1000))
    if not nis:
        txt += ". This facade is FLAT — no recess, no niche, no porch, nothing sticking out or cut in"
    return txt


def elevatie_png(n, latura, cale, h_perete=3000, atic=500, soclu=1100, px_m=110):
    """Elevaţia unei feţe, desenată DIN PLAN, ca imagine de referinţă pentru randare.

    Asta înlocuieşte descrierile în cuvinte: modelul vede geometria, nu o citeşte.
    Golurile ies exact la lăţimea şi poziţia din plan, glaful pe soclu.
    """
    lung = n.L if latura in "NS" else n.A
    W = int(lung / 1000 * px_m) + 80
    H = int((h_perete + atic) / 1000 * px_m) + 80
    k = px_m / 1000.0
    ox, oy = 40, 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    # volumul: soclu de beton jos, tencuială deasupra, atic drept
    o.append(R(ox, oy, lung * k, atic * k, "#d9d2c6", "#1a1714", 1.6))
    o.append(R(ox, oy + atic * k, lung * k, (h_perete - soclu) * k, "#efe7d9", "#1a1714", 1.6))
    o.append(R(ox, oy + (atic + h_perete - soclu) * k, lung * k, soclu * k, "#bdb7ad", "#1a1714", 1.6))

    IL, IA = n.L - 2 * n.pe, n.A - 2 * n.pe
    def poz_pe_fata(p, l):
        if latura in ("N", "S"):
            return (p + n.pe) if latura == "N" else (IL - p - l) + n.pe
        return (p + n.pe) if latura == "E" else (IA - p - l) + n.pe

    sus = atic + (h_perete - soclu) - 1500          # buiandrug
    jos = atic + (h_perete - soclu)                  # glaf, exact pe soclu
    for g in n.goluri:
        if g.get("latura") != latura:
            continue
        x = poz_pe_fata(g["poz"], g["l"])
        if g["fel"] == "fereastra":
            o.append(R(ox + x * k, oy + sus * k, g["l"] * k, (jos - sus) * k, "#3d4a52", "#1a1714", 1.4))
        else:
            o.append(R(ox + x * k, oy + sus * k, g["l"] * k, (atic + h_perete - sus) * k,
                       "#6b4f32", "#1a1714", 1.4))
    for z in n.nise:
        if z["latura"] != latura:
            continue
        x = poz_pe_fata(z["poz"], z["lat"])
        o.append(R(ox + x * k, oy + sus * k, z["lat"] * k, (atic + h_perete - sus) * k,
                   "#2b2b2b", "#1a1714", 1.6))
    for z in n.zone:
        atinge = {"N": z["y"] <= 1, "S": z["y"] + z["h"] >= IA - 1,
                  "V": z["x"] <= 1, "E": z["x"] + z["w"] >= IL - 1}[latura]
        if not atinge:
            continue
        l_ = z["w"] if latura in "NS" else z["h"]
        p_ = z["x"] if latura in "NS" else z["y"]
        x = poz_pe_fata(p_, l_)
        o.append(R(ox + x * k, oy + atic * k, l_ * k, h_perete * k, "#2b2b2b", "#1a1714", 1.6))
    o.append("</svg>")
    Path(cale).write_text("".join(o), encoding="utf-8")
    return cale


def cota(x1, y1, x2, y2, eticheta, vertical=False):
    o = [L_(x1, y1, x2, y2, 1.1)]
    if vertical:
        for yy in (y1, y2):
            o.append(L_(x1 - 6, yy, x1 + 6, yy, 1.1))
        o.append(f'<g transform="translate({x1 - 8:.1f},{(y1+y2)/2:.1f}) rotate(-90)">'
                 + T(0, 0, eticheta, 17, "middle", LINIE, 0.6, 400) + '</g>')
    else:
        for xx in (x1, x2):
            o.append(L_(xx, y1 - 6, xx, y1 + 6, 1.1))
        o.append(f'<rect x="{(x1+x2)/2-58:.1f}" y="{y1-16:.1f}" width="116" height="22" fill="#fff"/>')
        o.append(T((x1 + x2) / 2, y1 - 1, eticheta, 17, "middle", LINIE, 0.6, 400))
    return "".join(o)


def plansa(model: Model, cale, W=2000, H=1678):
    niv = model.niveluri
    for nv in niv:                     # planul stă mereu pe orizontală
        if nv.A > nv.L and not nv.rotit:
            nv.roteste()
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs>',
         '<pattern id="izo" width="7" height="7" patternUnits="userSpaceOnUse">'
         '<rect width="7" height="7" fill="#f4f2ee"/>'
         '<circle cx="1.8" cy="1.8" r="0.85" fill="#a9a196"/>'
         '<circle cx="5.3" cy="5.3" r="0.85" fill="#a9a196"/></pattern>',
         '<pattern id="bet" width="8" height="8" patternUnits="userSpaceOnUse">'
         '<rect width="8" height="8" fill="#e8e4dd"/>'
         '<path d="M0,8 L8,0" stroke="#8f877c" stroke-width="0.9"/>'
         '<path d="M-2,2 L2,-2 M6,10 L10,6" stroke="#8f877c" stroke-width="0.9"/></pattern>',
         '<pattern id="p3" width="7" height="7" patternUnits="userSpaceOnUse">'
         '<rect width="7" height="7" fill="#faf9f6"/>'
         '<path d="M0,7 L7,0" stroke="#b8b0a5" stroke-width="0.7"/></pattern>',
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         R(30, 30, W - 60, H - 60, "none", LINIE, 1.0),
         R(46, 46, W - 92, H - 92, "none", LINIE, 0.7)]

    o.append(T(84, 108, model.titlu, 27, "start", LINIE, 5.0, 400))
    o.append(T(84, 140, model.subtitlu, 15, "start", SLAB))
    o.append(T(W - 84, 108, "MODEL " + model.nume.upper(), 20, "end", LINIE, 5.0, 400))
    o.append(L_(84, 166, W - 84, 166, 1.0))

    # scara: cât încape pe lăţime cu toate nivelurile alăturate
    GOL = 1400 if len(niv) > 1 else 0          # spaţiu între niveluri, în mm
    latimi = []
    for n in niv:
        dr_ = max([z["x"] + z["w"] for z in n.zone] + [n.L - n.pe]) + n.pe
        st_ = min([z["x"] - n.pe for z in n.zone] + [-n.pe])
        latimi.append(dr_ - st_)
    total_mm = sum(latimi) + GOL * (len(niv) - 1)
    k = min(1620 / total_mm, 700 / max(n.A for n in niv))

    oy = 320
    ox = (W - total_mm * k) / 2
    for i, n in enumerate(niv):
        st_ = min([z["x"] - n.pe for z in n.zone] + [-n.pe])
        corp, (bx, by, bw, bh) = deseneaza(n, ox - st_ * k + n.pe * k, oy + n.pe * k, k)
        o.append(corp)
        o.append(T((bx + bx + bw) / 2, by - 74, n.nume, 17, "middle", LINIE, 4.0, 400))
        o.append(cota(bx, by - 44, bx + bw, by - 44, f"{n.L/1000:.2f} m"))
        lat = i == 0
        xc = bx - 46 if lat else bx + bw + 46
        o.append(cota(xc, by, xc, by + bh, f"{n.A/1000:.2f} m", vertical=True))
        if i == 0:
            jos = by + bh
        ox += (latimi[i] + GOL) * k

    n0 = niv[0]
    sx, sy = 130, min(jos + 120, H - 520)
    for i in range(5):
        o.append(R(sx + i * 1000 * k, sy, 1000 * k, 11,
                   LINIE if i % 2 == 0 else "#fff", LINIE, 0.8))
    for i in (0, 1, 3, 5):
        o.append(T(sx + i * 1000 * k, sy + 30, str(i), 13, "middle", SLAB))
    o.append(T(sx + 5 * 1000 * k + 22, sy + 30, "m", 13, "start", SLAB))

    nx, ny = W - 150, jos + 86
    o.append(f'<circle cx="{nx}" cy="{ny}" r="20" fill="none" stroke="{LINIE}" stroke-width="1"/>')
    if niv[0].rotit:                   # planul e rotit 90°: nordul arată spre dreapta
        o.append(f'<path d="M{nx+14},{ny} L{nx-11},{ny-7} L{nx-5},{ny} L{nx-11},{ny+7} Z" fill="{LINIE}"/>')
        o.append(T(nx + 30, ny + 5, "N", 14, "middle", LINIE, 0, 400))
    else:
        o.append(f'<path d="M{nx},{ny-14} L{nx-7},{ny+11} L{nx},{ny+5} L{nx+7},{ny+11} Z" fill="{LINIE}"/>')
        o.append(T(nx, ny - 28, "N", 14, "middle", LINIE, 0, 400))
    n = n0

    # ── cele trei casete de jos
    ty = H - 460
    col = (W - 168) / 3
    o.append(L_(84, ty, W - 84, ty, 1.0))
    o.append(L_(84, ty + 46, W - 84, ty + 46, 0.7))
    o.append(R(84, ty, W - 168, H - 84 - ty, "none", LINIE, 1.0))
    for i, cap in enumerate(("TABLOU DE SUPRAFEŢE", "ALCĂTUIREA PEREŢILOR", "OBSERVAŢII")):
        o.append(T(84 + i * col + 26, ty + 32, cap, 15, "start", LINIE, 3.0, 400))
        if i:
            o.append(L_(84 + i * col, ty, 84 + i * col, H - 84, 0.8))

    # coloana 1 — tabloul de suprafeţe
    y = ty + 78
    rinduri = sum(len([c for c in nv.camere if c["tip"] == "camera"]) for nv in niv)
    rinduri += len(niv) if len(niv) > 1 else 0
    pas = max(15, min(24 if len(niv) == 1 else 21, int((H - 84 - ty - 130) / (rinduri + 1))))
    for nv in niv:
        if len(niv) > 1:
            o.append(T(110, y, nv.nume, 13, "start", LINIE, 1.4, 500)); y += pas
        for c in sorted([c for c in nv.camere if c["tip"] == "camera"],
                        key=lambda c: -c["w"] * c["h"]):
            o.append(T(122 if len(niv) > 1 else 110, y, c["nume"].capitalize(), 13.5, "start", SLAB))
            o.append(T(84 + col - 26, y, f"{c['w']*c['h']/1e6:.1f} m²", 13.5, "end", LINIE))
            y += pas
        y += 4
    o.append(L_(110, y + 2, 84 + col - 26, y + 2, 0.8))
    o.append(T(110, y + 26, "TOTAL UTIL", 15, "start", LINIE, 1.0, 400))
    o.append(T(84 + col - 26, y + 26, f"{sum(x.util for x in niv):.1f} m²", 15, "end", LINIE, 0, 500))

    # coloana 2 — alcătuirea pereţilor
    x2 = 84 + col + 26
    for j, (patt, cod, tit, sub) in enumerate((
            ("izo", "P1", "Cofraj Polistibrick MBK 210 — 38 cm",
             "Interior 8,2 (fibrociment + PSE) · beton armat 15 · exterior 14,8 (PSE + fibrociment)."),
            ("p3", "P3", "Pereţi de compartimentare — 13 cm",
             "Interiori, fără rol de anvelopă."))):
        yy = ty + 90 + j * 72
        if cod == "P1":                      # se arată chiar cele trei straturi
            for (dx, w_, p_) in ((0, 20, "izo"), (20, 21, "bet"), (41, 11, "izo")):
                o.append(R(x2 + dx, yy - 17, w_, 24, f"url(#{p_})", "none", 0))
            o.append(R(x2, yy - 17, 52, 24, "none", LINIE, 0.8))
            o.append(L_(x2 + 20, yy - 17, x2 + 20, yy + 7, 0.6))
            o.append(L_(x2 + 41, yy - 17, x2 + 41, yy + 7, 0.6))
        else:
            o.append(R(x2, yy - 17, 52, 24, f"url(#{patt})", LINIE, 0.8))
        o.append(T(x2 + 68, yy, f"{cod} · {tit}", 14, "start", LINIE))
        o.append(T(x2 + 68, yy + 21, sub, 13, "start", SLAB))
    yy = ty + 90 + 2 * 72
    for s in ("Golurile de uşă sunt marcate cu pragul, fără sensul de deschidere.",
              "Terasa acoperită e desenată punctat: stă sub prelungirea şarpantei,",
              "pe aceeaşi structură, fără pereţi."):
        o.append(T(x2, yy, s, 13, "start", SLAB)); yy += 22

    # coloana 3 — observaţii
    x3 = 84 + 2 * col + 26
    randuri = [("Amprentă la sol", f"{niv[0].amprenta:.1f} m²"),
               ("Suprafaţă utilă", f"{sum(x.util for x in niv):.1f} m²"),
               ("Gabarit exterior", f"{niv[0].L/1000:.2f} × {niv[0].A/1000:.2f} m"),
               ("Acoperiş", model.acoperis)] + list(model.extra)
    yy = ty + 90
    for a, b in randuri:
        o.append(T(x3, yy, a, 14, "start", SLAB))
        o.append(T(W - 110, yy, b, 14, "end", LINIE)); yy += 27
    yy += 10
    o.append(T(x3, yy, "Cofrajul e MBK 210: U = 0,14 W/m²K, R = 7,14 m²K/W, defazaj 12,7 h.",
               13, "start", SLAB)); yy += 22
    o.append(T(x3, yy, "Cote exterioare pe contur. Suprafeţele sunt cele din tabloul alăturat.",
               13, "start", SLAB)); yy += 22
    for s in model.observatii:
        o.append(T(x3, yy, s, 13, "start", SLAB)); yy += 22
    o.append(T(x3, max(yy + 14, H - 108), f"POLISTIBRICK · {model.nume.upper()} · {model.subtitlu.split('·')[0].strip().lower()}",
               13, "start", STINS))

    o.append("</svg>")
    Path(cale).write_text("".join(o), encoding="utf-8")
    return cale
