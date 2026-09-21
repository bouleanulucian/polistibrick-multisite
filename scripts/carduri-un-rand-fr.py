#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cardurile din /projets/ (FR) pe un singur rând — aceeași regulă ca scripts/carduri-un-rand-ro.py
(cerută de patron pe 18.09.2026 pe Doina): după nivel rămân cel mult două elemente scurte
(«garage | terrasse» încape); ce nu se poate scurta se scoate. Idempotent; tipărește jurnalul."""
import re, html, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / 'countries' / 'fr' / 'projets' / 'index.html'
h = p.read_text(encoding='utf-8')

def scurt(t: str) -> str | None:
    t = t.strip()
    if re.match(r'(?i)(deux |2 )?terrasses?', t): return 'terrasses' if re.match(r'(?i)(deux |2 )?terrasses', t) else 'terrasse'
    if t.startswith('garage double'): return 'garage double'
    if re.match(r'garage( \d|$)', t): return 'garage'
    if t.startswith('carport'): return 'carport'
    if t.startswith('bureau'): return 'bureau'
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
    if txt(nivel) == 'rez-de-chaussée + étage':      # site-ul folosește deja «R+1»
        nivel = nivel.replace('rez-de-chaussée + étage', 'R+1')
    extras = []
    for it in items[4:]:
        s = scurt(txt(it))
        if s and len(extras) < 2:
            extras.append(re.sub(r'(</svg>\s*).*?(</i>)$', lambda mm: mm.group(1) + s + mm.group(2), it, flags=re.S)
                          if '</svg>' in it else f'<i>{s}</i>')
    if len(extras) == 2 and sum(len(txt(e)) for e in extras) > 15:
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
