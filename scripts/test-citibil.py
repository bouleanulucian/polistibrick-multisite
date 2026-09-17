#!/usr/bin/env python3
"""Testul «ce vede un AI» pe HTML-ul construit — fără JavaScript, fără cod, doar ce ar
extrage un crawler (GPTBot, PerplexityBot, Google-Extended) din pagină.

Rulare:  python3 scripts/test-citibil.py [ro] [--json raport.json]
Compară două rulări (înainte/după) cu:  python3 scripts/test-citibil.py --diff a.json b.json

Pentru fiecare pagină-țintă scoate exact ce ar lua un AI:
  · H1 și primul paragraf de sub el — pasajul candidat la citare
  · dacă primul paragraf are o CIFRĂ și o SURSĂ numită (asta decide dacă e citabil)
  · «Actualizat» / dateModified — semnal de prospețime
  · tipurile JSON-LD și dacă Organization e complet (telefon, email, CUI, sameAs)
  · dacă emailul și telefonul apar în TEXT (nu doar în schemă)
Nu judecă stilul; doar prezența faptelor. Verdictul de citabilitate = cifră + sursă în P1.
"""
import sys, re, json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TINTE = ['', 'resurse/cat-costa-o-casa', 'resurse/casa-pasiva', 'resurse/bca-sau-caramida',
         'resurse/casa-din-polistiren-pareri', 'resurse/cofraj-izolant', 'resurse/nzeb',
         'resurse/polistibrick-vs-icf-clasic', 'resurse/faq', 'preturi', 'produse/polistibrick',
         'produse/polistiwall', 'produse/polistisip', 'pentru/proprietari']
# o «sursă» = o entitate numită sau un număr de normă/brevet pe care AI-ul îl poate verifica
SURSA_RX = re.compile(r'(?i)(surs[aă]|conform|potrivit|ghidul|ghidurile|Eurostat|INS\b|ANRE|Passivhaus|'
                      r'Institut|EOTA|Espacenet|EUIPO|Legea\s\d|Brig\.ro|Wolf|EN\s\d{4,5}|EP\s\d{7}|ISO\s\d{4}|EAD\s\d|'
                      # prețurile proprii: sursa primară e chiar lista de prețuri a producătorului, datată
                      r'Prețuri(?:le)?[^.]{0,30}(?:august|septembrie) 2026|valabile din)')

def text(s: str) -> str:
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def analizeaza(p: pathlib.Path) -> dict:
    h = p.read_text(encoding='utf-8')
    corp = re.sub(r'<(script|style|nav|header)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    ld = [b for b in re.findall(r'application/ld\+json[^>]*>(.*?)</script>', h, re.S)]
    tipuri, org, dm = [], {}, None
    for b in ld:
        try: d = json.loads(b)
        except Exception: tipuri.append('STRICAT'); continue
        for x in (d.get('@graph') if isinstance(d, dict) and '@graph' in d else (d if isinstance(d, list) else [d])):
            t = x.get('@type'); tipuri.append(t if isinstance(t, str) else '/'.join(t))
            if t == 'Organization' and (x.get('telephone') or not org):
                org = {k: bool(x.get(k)) for k in ('telephone', 'email', 'vatID', 'legalName', 'sameAs', 'address')}
            if t in ('WebPage', 'Article') and x.get('dateModified'): dm = x['dateModified']
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', corp, re.S)
    dupa = corp[h1m.end():] if h1m else corp
    # pasajul pe care îl extrage un AI: blocul «răspuns» întreg (întrebare + răspuns + sursă/dată)
    # dacă există, altfel primul paragraf de sub H1
    rm = re.search(r'<section class="raspuns"[^>]*>(.*?)</section>', dupa, re.S)
    if rm:
        p1 = text(rm.group(1))
    else:
        pm = re.search(r'<p[^>]*>(.*?)</p>', dupa, re.S)
        p1 = text(pm.group(1)) if pm else ''
    vizibil = text(re.sub(r'<footer.*?</footer>', ' ', corp, flags=re.S))
    subsol = text(''.join(re.findall(r'<footer.*?</footer>', h, re.S)))
    return {
        'h1': text(h1m.group(1)) if h1m else '',
        'p1': p1[:300],
        'p1_cifra': bool(re.search(r'\d', p1)),
        'p1_sursa': bool(SURSA_RX.search(p1)),
        'actualizat_in_text': bool(re.search(r'(?i)actualizat', vizibil)),
        'dateModified': dm,
        'jsonld': sorted(set(tipuri)),
        'organization': org,
        'email_in_text': bool(re.search(r'[\w.]+@polisti\w*\.\w+', vizibil + ' ' + subsol)),
        'telefon_in_text': bool(re.search(r'\+40|031\s?630', vizibil + ' ' + subsol)),
        'U_in_text': bool(re.search(r'U\s?=?\s?0,\d\d', vizibil)),
        'euro_mp_in_text': len(re.findall(r'€\s?/\s?m', vizibil)),
    }

def raport(tara: str) -> dict:
    B = ROOT / 'build' / tara
    if not B.exists(): sys.exit(f'lipsește {B} — rulează întâi build/build.py {tara}')
    out = {}
    for t in TINTE:
        f = B / t / 'index.html' if t else B / 'index.html'
        if f.exists(): out['/' + t + ('/' if t else '')] = analizeaza(f)
    return out

def tipareste(r: dict):
    citabile = sum(1 for v in r.values() if v['p1_cifra'] and v['p1_sursa'])
    print(f'pagini: {len(r)} · citabile (cifră + sursă în primul paragraf): {citabile}')
    for u, v in r.items():
        org_ok = all(v['organization'].get(k) for k in ('telephone', 'email', 'vatID', 'sameAs')) if v['organization'] else False
        flag = '✓' if v['p1_cifra'] and v['p1_sursa'] else ('~' if v['p1_cifra'] else '✗')
        print(f'{flag} {u:40} P1: cifră={"da" if v["p1_cifra"] else "NU"} sursă={"da" if v["p1_sursa"] else "NU"} · '
              f'dateModified={v["dateModified"] or "—"} · Org complet={"da" if org_ok else "NU"} · '
              f'email în text={"da" if v["email_in_text"] else "nu"} · U în text={"da" if v["U_in_text"] else "nu"}')

def diff(a: dict, b: dict):
    chei = ['p1_cifra', 'p1_sursa', 'actualizat_in_text', 'dateModified', 'email_in_text', 'telefon_in_text', 'U_in_text']
    for u in b:
        va, vb = a.get(u, {}), b[u]
        sch = [f'{k}: {va.get(k)}→{vb.get(k)}' for k in chei if va.get(k) != vb.get(k)]
        oa = va.get('organization') or {}; ob = vb.get('organization') or {}
        if oa != ob: sch.append(f'organization: {sum(oa.values())}→{sum(ob.values())} câmpuri')
        print(f'{u:40} {"; ".join(sch) if sch else "neschimbat"}')

if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] == ['--diff']:
        a = json.loads(pathlib.Path(args[1]).read_text()); b = json.loads(pathlib.Path(args[2]).read_text())
        diff(a, b); sys.exit(0)
    tara = next((x for x in args if not x.startswith('--') and not x.endswith('.json')), 'ro')
    r = raport(tara); tipareste(r)
    if '--json' in args:
        pathlib.Path(args[args.index('--json') + 1]).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding='utf-8')
