#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pune cotele exterioare peste planşele existente.

Planşele au scară grafică, deci se pot măsura. Nu se redesenează nimic:
se citeşte scara, se măsoară conturul fiecărui bloc desenat (unele planşe
au parter şi etaj alăturate), se trag liniile de cotă în spaţiul alb.
Originalul rămâne neatins.

  python3 coteaza.py nova
  python3 coteaza.py --toate
"""
import sys, glob, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SURSA = "/Users/polistibrick/Desktop/Aplicatii site web/polistibrick-multisite/shared/images/case"
IESIRE = "/private/tmp/planuri/cotate"
NEGRU = (26, 23, 20)


def font(marime):
    for c in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/Library/Fonts/Arial.ttf"):
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, marime)
            except Exception:
                pass
    return ImageFont.load_default()


def maxrun(v):
    """cel mai lung traseu continuu de pixeli închişi"""
    m = c = 0
    for x in v:
        c = c + 1 if x else 0
        if c > m:
            m = c
    return m


def runuri(rand):
    idx = np.where(rand)[0]
    if not len(idx):
        return []
    r, s, p = [], idx[0], idx[0]
    for x in idx[1:]:
        if x > p + 1:
            r.append((s, p))
            s = x
        p = x
    r.append((s, p))
    return r


def scara(inchis, h, w):
    """px pe metru din bara de scară: 3 blocuri pline egale, cu goluri egale.

    Semnătura e strictă tocmai ca să nu prindă pereţii sau roza vânturilor.
    Întoarce şi dreptunghiul barei, ca să poată fi mascată: la unele planşe
    bara stă la aceeaşi înălţime cu casa.
    """
    gasite = []
    for y in range(int(h * 0.42), int(h * 0.84)):
        rr = [t for t in runuri(inchis[y, :int(w * 0.5)])
              if 30 <= t[1] - t[0] <= 250 and t[0] > 40]
        if len(rr) < 3:
            continue
        a, b, c = rr[0], rr[1], rr[2]
        li = [t[1] - t[0] for t in (a, b, c)]
        med = sum(li) / 3.0
        if max(abs(v - med) for v in li) > med * 0.12:
            continue
        goluri = [b[0] - a[1], c[0] - b[1]]
        if max(abs(g - med) for g in goluri) > med * 0.30:
            continue
        gasite.append(((c[1] - a[0]) / 5.0, y, a[0], c[1]))
    if not gasite:
        return None, None
    valori = [round(g[0], 1) for g in gasite]
    v = max(set(valori), key=valori.count)
    ale = [g for g in gasite if round(g[0], 1) == v]
    # bara + eticheta „0 1 3 5 m" de sub ea
    caseta = (min(g[2] for g in ale) - 12, min(g[1] for g in ale) - 10,
              max(g[3] for g in ale) + 40, max(g[1] for g in ale) + 46)
    return v, caseta


def blocuri(inchis, h, w, caseta, px_m):
    """un bloc = un plan desenat. Planşele cu parter + etaj au două."""
    z = inchis.copy()
    x0c, y0c, x1c, y1c = caseta
    z[max(y0c, 0):y1c, max(x0c, 0):x1c] = False        # scot bara de scară

    sus, jos = int(h * 0.085), min(y1c + 10, h)
    st, dr = int(w * 0.03), int(w * 0.97)
    banda = z[sus:jos, st:dr]
    # gruparea pe coloane se face din partea de sus a benzii: notele scrise
    # între cele două planuri le-ar lipi într-un singur bloc
    col = banda[:int(banda.shape[0] * 0.75)].sum(axis=0)
    orice = col > 4                                      # orice urmă de desen
    # peretele e linie CONTINUĂ; terasa punctată şi textul au trasee scurte
    lung_col = np.array([maxrun(banda[:, k]) for k in range(banda.shape[1])])
    perete = lung_col > banda.shape[0] * 0.25

    gr, i = [], 0
    while i < len(orice):
        if not orice[i]:
            i += 1
            continue
        j, gol = i, 0
        while j + 1 < len(orice) and gol < 30:
            j += 1
            gol = 0 if orice[j] else gol + 1
        gr.append((i, j - gol))
        i = j + 1

    out = []
    for g0, g1 in gr:
        if g1 - g0 < w * 0.14:
            continue
        pc = [k for k in range(g0, g1 + 1) if perete[k]]
        if len(pc) < 2:                                  # text lung, nu casă
            continue
        pereche = fete(pc, px_m)
        if not pereche:
            continue
        x0, x1 = pereche[0] + st, pereche[1] + st
        sub = z[sus:jos, x0:x1 + 1]
        # un metru de perete continuu; liniuţele terasei au 10-15 px
        minim = max(60, 2.5 * 0.38 * px_m)
        pr = [k for k in range(sub.shape[0]) if maxrun(sub[k]) > minim]
        pereche = fete(pr, px_m)
        if pereche:
            out.append((x0, x1, pereche[0] + sus, pereche[1] + sus))
    return out


def fete(linii, px_m):
    """feţele exterioare: peretele de 38 cm are DOUĂ linii paralele.

    Terasa punctată şi chenarele tabelului n-au pereche la distanţa asta,
    deci pică singure.
    """
    if len(linii) < 2:
        return None
    jos_, sus_ = 0.38 * px_m * 0.70, 0.38 * px_m * 1.40
    prima = next((a for i, a in enumerate(linii)
                  for b in linii[i + 1:] if jos_ <= b - a <= sus_), None)
    ultima = next((b for i, b in enumerate(reversed(linii))
                   for a in list(reversed(linii))[i + 1:] if jos_ <= b - a <= sus_), None)
    if prima is None or ultima is None or ultima <= prima:
        return None
    return prima, ultima


def cota(d, x1, y1, x2, y2, eticheta, f, vertical=False):
    d.line([(x1, y1), (x2, y2)], fill=NEGRU, width=2)
    if vertical:
        for y in (y1, y2):
            d.line([(x1 - 8, y), (x1 + 8, y)], fill=NEGRU, width=2)
        img = Image.new("RGBA", (260, 34), (255, 255, 255, 0))
        ImageDraw.Draw(img).text((130, 17), eticheta, font=f, fill=NEGRU, anchor="mm")
        img = img.rotate(90, expand=True)
        d._image.paste(img, (int(x1 + 10), int((y1 + y2) / 2 - img.height // 2)), img)
    else:
        for x in (x1, x2):
            d.line([(x, y1 - 8), (x, y1 + 8)], fill=NEGRU, width=2)
        d.rectangle([((x1 + x2) / 2 - 70, y1 - 30), ((x1 + x2) / 2 + 70, y1 - 6)],
                    fill=(255, 255, 255))
        d.text(((x1 + x2) / 2, y1 - 18), eticheta, font=f, fill=NEGRU, anchor="mm")


def rescrie_nota(im, inchis, h, w):
    """Planşa scrie «Plan fără cote». Acum are cote, deci rândul se schimbă.

    Rândul se găseşte singur: rândurile de date au valoarea aliniată la
    marginea din dreapta, rândurile de notă nu ajung acolo.
    """
    st, dr = int(w * 0.672), int(w * 0.963)
    # marginea de test se opreşte înainte de chenarul casetei, altfel
    # linia lui verticală face să pară că orice rând are valoare
    marg, capat = int(dr - (dr - st) * 0.12), dr - 16
    # pornesc de sub chenarul de sus al casetei, altfel prind text din desen
    randuri = [y for y in range(int(h * 0.55), int(h * 0.97))
               if inchis[y, st:dr].sum() > 3]
    linii, cur = [], []
    for y in randuri:
        if cur and y - cur[-1] > 4:
            linii.append(cur)
            cur = []
        cur.append(y)
    if cur:
        linii.append(cur)
    # chenarele şi liniile de cotă nu sunt rânduri de text
    linii = [ln for ln in linii
             if max(maxrun(inchis[y, st:dr]) for y in ln) < (dr - st) * 0.6]
    # nota începe imediat după ultimul rând cu valoare aliniată la dreapta
    ultim = max((i for i, ln in enumerate(linii)
                 if inchis[ln[0]:ln[-1] + 1, marg:capat].sum() > 6), default=None)
    if ultim is None or ultim + 1 >= len(linii):
        return False
    ln = linii[ultim + 1]
    d = ImageDraw.Draw(im)
    d.rectangle([st - 4, ln[0] - 6, capat, ln[-1] + 6], fill=(255, 255, 255))
    d.text((st, (ln[0] + ln[-1]) / 2),
           "Cote exterioare pe contur. Suprafețele sunt cele din tabloul alăturat.",
           font=font(16), fill=(96, 92, 88), anchor="lm")
    return True
    return False


def lucreaza(nume):
    cale = os.path.join(SURSA, nume + "-plan.png")
    if not os.path.exists(cale):
        return None
    im = Image.open(cale).convert("RGB")
    a = np.array(im.convert("L"))
    inchis = a < 150
    h, w = a.shape
    px_m, caseta = scara(inchis, h, w)
    if not px_m:
        return "fără scară grafică"
    bl = blocuri(inchis, h, w, caseta, px_m)
    if not bl:
        return "nu găsesc conturul"
    d = ImageDraw.Draw(im)
    f = font(30)
    masuri = []
    for x0, x1, y0, y1 in bl:
        L, A = (x1 - x0) / px_m, (y1 - y0) / px_m
        liber_sus = not inchis[max(y0 - 84, 0):y0 - 40, x0:x1].any()
        yc = y0 - 52 if liber_sus else y1 + 64
        cota(d, x0, yc, x1, yc, "%.2f m" % L, f)
        liber_dr = not inchis[y0:y1, x1 + 20:min(x1 + 96, w)].any()
        xc = x1 + 52 if liber_dr else x0 - 52
        cota(d, xc, y0, xc, y1, "%.2f m" % A, f, vertical=True)
        masuri.append("%.2f × %.2f m" % (L, A))
    rescrie_nota(im, inchis, h, w)
    os.makedirs(IESIRE, exist_ok=True)
    im.save(os.path.join(IESIRE, nume + "-plan-cotat.png"))
    return "%s   (%.1f px/m, %d bloc%s)" % (" | ".join(masuri), px_m, len(bl),
                                            "" if len(bl) == 1 else "uri")


# desenul nu se potriveşte cu tabloul lui de suprafeţe — nu le cotez
SARITE = {"aria": "amprentă scrisă 89,6 m², dreptunghi desenat 72,4 m²",
          "e3":   "amprentă scrisă 115,1 m², dreptunghi desenat 92,0 m²",
          "terra": "cele două niveluri nu se măsoară sigur"}


if __name__ == "__main__":
    arg = sys.argv[1:] or ["nova"]
    nume = ([os.path.basename(p).replace("-plan.png", "")
             for p in sorted(glob.glob(SURSA + "/*-plan.png"))]
            if "--toate" in arg else arg)
    for n in nume:
        if n in SARITE:
            print("  %-8s SĂRIT — %s" % (n, SARITE[n]))
            continue
        print("  %-8s %s" % (n, lucreaza(n) or "lipseşte"))
