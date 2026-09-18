#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cardurile din /proiecte/ pe un singur rând — 18.09.2026, cerut de patron pe Doina:
«134 m² construiți · 3 · 2 · parter · terasă. Să intre pe un singur rând, ca să arate cadrul la fel.
Nu mai pune nimic după terasă.»

Regula aplicată tuturor cardurilor RO: după nivel (parter / P+1) rămâne CEL MULT UN element, scurt:
  terasă …, două terase …, terase …  → «terasă» / «terase»
  garaj dublu NN m²                   → «garaj dublu»       garaj NN m² → «garaj»
  carport + depozit → «carport»        birou + 2 terase → «birou»
  «parter + etaj» → «P+1» (site-ul folosește deja P+1)
  orice altceva mai lung de 16 caractere → se scoate (regula Doina: nimic după)
Jurnalul de schimbări se tipărește; idempotent.
"""
import re, html, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / 'countries' / 'ro' / 'proiecte' / 'index.html'
h = p.read_text(encoding='utf-8')

def scurt(t: str) -> str | None:
    t = t.strip()
    if re.match(r'(?i)(două |2 )?teras[eă]', t): return 'terase' if re.match(r'(?i)(două |2 )?terase', t) else 'terasă'
    if t.startswith('garaj dublu'): return 'garaj dublu'
    if re.match(r'garaj \d', t): return 'garaj'
    if t.startswith('carport'): return 'carport'
    if t.startswith('birou'): return 'birou'
    return t if len(t) <= 16 else None

jurnal = []
def pe_card(m: re.Match) -> str:
    card = m.group(0)
    nume = re.search(r'<h2[^>]*>(.*?)(?:<span|</h2>)', card, re.S)
    nume = html.unescape(re.sub(r'<[^>]+>', '', nume.group(1))).strip() if nume else '?'
    sm = re.search(r'(<p class="case-spec">)(.*?)(</p>)', card, re.S)
    if not sm: return card
    items = re.findall(r'<i>.*?</i>', sm.group(2), re.S)
    if len(items) < 4: return card
    def txt(i): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', i))).strip()
    inainte = [txt(i) for i in items[3:]]
    nivel = items[3]
    if txt(nivel) == 'parter + etaj':
        nivel = nivel.replace('parter + etaj', 'P+1')
    # cel mult DOUĂ elemente scurte după nivel («garaj | terasă» încape); ce nu se poate scurta se scoate
    extras = []
    for it in items[4:]:
        s = scurt(txt(it))
        if s and len(extras) < 2:
            # se schimbă DOAR textul dintre </svg> și </i>; prima variantă mânca și </i> (Riva a ieșit «garaj terasă»)
            extras.append(re.sub(r'(</svg>\s*).*?(</i>)$', lambda mm: mm.group(1) + s + mm.group(2), it, flags=re.S)
                          if '</svg>' in it else f'<i>{s}</i>')
    # două elemente doar dacă împreună sunt scurte («garaj | terasă» = 11); «garaj opțional | terasă» (20) → doar primul
    if len(extras) == 2 and sum(len(txt(e)) for e in extras) > 14:
        extras = extras[:1]
    noi = items[:3] + [nivel] + extras
    dupa = [txt(i) for i in noi[3:]]
    if dupa != inainte:
        jurnal.append(f'{nume:7} {" | ".join(inainte)}  →  {" | ".join(dupa)}')
    return card.replace(sm.group(0), sm.group(1) + ''.join(noi) + sm.group(3))

h2 = re.sub(r'<article class="case-card"[^>]*>.*?</article>', pe_card, h, flags=re.S)
p.write_text(h2, encoding='utf-8')
print(f'carduri schimbate: {len(jurnal)}')
for j in jurnal: print('  ', j)
