#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""«Răspuns-întâi» pe paginile RO — 17.09.2026, varianta B aprobată de patron.

Sub H1, înaintea textului existent: întrebarea exact cum o pune omul unui AI, răspunsul cu
cifra în prima frază, sursa lângă cifră, data. Textul paginii rămâne neatins dedesubt.
Stil: regulile din scriitura-lucian (cifre, nu adjective; propoziții scurte; fără triplete,
fără «nu e doar X», fără liniuță lungă în text de client).

Plasa de siguranță: fiecare număr din fiecare bloc trebuie să existe DEJA undeva pe site
(în build/ro). Dacă un număr nu există, scriptul se oprește fără să scrie nimic — ca să nu
inventăm cifre în numele patronului.

Idempotent: dacă blocul e deja în pagină, nu-l pune a doua oară.
"""
import re, sys, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RO = ROOT / 'countries' / 'ro'
BUILD = ROOT / 'build' / 'ro'
META = 'Actualizat: septembrie 2026'
P = 'preturi/'; C = 'despre/certificari/'; B = 'despre/patent/'; E = 'economii/'

def bloc(intrebare: str, raspuns: str, meta: str) -> str:
    return (f'\n<section class="raspuns" aria-label="Răspuns pe scurt">'
            f'<h2>{intrebare}</h2><p>{raspuns}</p><p class="raspuns-meta">{meta}</p></section>\n')

def a(href: str, text: str) -> str:
    return f'<a href="{href}">{text}</a>'

# adâncimea paginii decide prefixul relativ (build-ul rescrie doar ${BASE}, nu link-urile din text)
def L(pagina: str, tinta: str, text: str) -> str:
    sus = '../' * (pagina.count('/') + 1) if pagina else ''
    return a(sus + tinta, text)

BRIG = a('https://brig.ro/blog/ghid-complet-2026-cat-costa-constructia-unei-case-la-cheie-in-romania', 'Brig.ro')
WOLF = a('https://wolfconstruct.ro/blogs/constructii-case-structura-metalica-proiecte-case/cat-costa-sa-construiesti-o-casa-in-2026', 'Wolf Construct')

BLOCURI = {
 'resurse/cat-costa-o-casa': (
   'Cât costă o casă la cheie în 2026?',
   'Între 900 și 1.350 € pe metru pătrat construit, pentru o casă clasică din România. La roșu, între 450 și 700 €/m². '
   f'Ghidurile de cost ale firmelor de construcții dau pentru 2026, la standard, 1.250–1.650 €/m² ({BRIG}, {WOLF}). '
   'O casă Polistibrick a ieșit pe șantierele noastre la 950–1.280 €/m² la cheie, cu peretele la nivel de casă pasivă inclus.',
   f'{META} · Prețurile Polistibrick: august 2026, ' + L('resurse/cat-costa-o-casa', P, 'lista de prețuri')),

 'resurse/bca-sau-caramida': (
   'BCA sau cărămidă: care e mai ieftin?',
   'BCA-ul. Zid finit cu manoperă, orientativ pentru 2026: 240–300 lei/m² de perete la BCA, 320–390 lei/m² la cărămidă. '
   'În bugetul casei diferența se topește: la cheie plătești oricum 900–1.350 €/m² construit, fiindcă finisajele și instalațiile '
   'cântăresc mai mult decât zidăria. Cofrajul Polistibrick vine cu izolația în perete: 197–281 €/m² construit, livrat.',
   f'{META} · Reper de piață 2026: {BRIG}, {WOLF} · ' + L('resurse/bca-sau-caramida', P, 'Prețuri Polistibrick')),

 'resurse/casa-din-polistiren-pareri': (
   'Casa din polistiren e sigură?',
   'Da. Structura e beton armat monolit, turnat în cofraj. Polistirenul nu duce nicio sarcină: e cofraj și izolație. '
   'Fața e fibrociment, incombustibil, Euroclasa A1 la foc (EN 13501-1). Peretele iese la U 0,10–0,14 W/m²K, nivel de casă pasivă. '
   'Cofrajul costă 197–281 €/m² construit, livrat.',
   f'{META} · ' + L('resurse/casa-din-polistiren-pareri', C, 'Certificări') + ' · ' + L('resurse/casa-din-polistiren-pareri', P, 'Prețuri')),

 'resurse/cofraj-izolant': (
   'Ce este cofrajul izolant și cât costă?',
   'Un perete din beton armat turnat între două panouri de izolație care rămân în perete. Nu scoți cofrajul, nu pui izolație după. '
   'Polistibrick: 197–281 €/m² construit, livrat, cu fibrociment pe ambele fețe. La gri, cu montaj, 690–810 €/m². '
   'Perete U 0,10–0,14 W/m²K. Prețul e public, pe suprafață, în ' + L('resurse/cofraj-izolant', P, 'lista de prețuri') + '.',
   f'{META} · Prețuri: august 2026'),

 'resurse/polistibrick-vs-icf-clasic': (
   'Polistibrick sau ICF clasic: ce diferă?',
   'Fața. La ICF-ul clasic, fețele sunt polistiren și se finisează după. La Polistibrick, ambele fețe sunt fibrociment, '
   'Euroclasa A1 la foc, gata de glet la interior și de adeziv la exterior. Perete U 0,10–0,14 W/m²K. '
   'Prețul e public: 197–281 €/m² construit, livrat.',
   f'{META} · ' + L('resurse/polistibrick-vs-icf-clasic', P, 'Prețuri') + ': august 2026 · ' + L('resurse/polistibrick-vs-icf-clasic', C, 'Certificări')),

 'resurse/faq': (
   'Ce este Polistibrick, pe scurt?',
   'Un cofraj izolant brevetat, EP 4372168 B1: panouri din EPS grafitat cu fibrociment pe ambele fețe, în care se toarnă beton armat. '
   'Peretele iese la U 0,10–0,14 W/m²K, nivel de casă pasivă, dintr-un singur strat. 197–281 €/m² construit, livrat. '
   'Fabricat lângă Balș, în Olt.',
   f'{META} · ' + L('resurse/faq', B, 'Brevet') + ' · ' + L('resurse/faq', P, 'Prețuri')),

 'preturi': (
   'Cât costă sistemul Polistibrick pe metru pătrat?',
   '197–281 €/m² construit cofrajul, fără TVA, livrat, în funcție de suprafața casei. La gri, cu montaj, 690–810 €/m². '
   'La cheie, pe șantierele Polistibrick, 950–1.280 €/m². Polistiwall pleacă de la 153 €/m², PolistiSIP de la 201 €/m². '
   'Grila completă, pe suprafețe, e mai jos.',
   'Prețuri valabile din august 2026 · ' + META),

 'produse/polistibrick': (
   'Ce este cofrajul Polistibrick?',
   'Un panou din EPS grafitat cu fibrociment pe ambele fețe. Se montează, se toarnă beton armat, și peretele e gata de glet la interior '
   'și de adeziv la exterior. U 0,10–0,14 W/m²K, nivel de casă pasivă. Fibrocimentul e incombustibil, Euroclasa A1. '
   'Cofrajul costă 197–281 €/m² construit, livrat.',
   f'{META} · ' + L('produse/polistibrick', P, 'Prețuri') + ': august 2026 · ' + L('produse/polistibrick', C, 'Certificări')),

 'produse/polistiwall': (
   'Ce este Polistiwall?',
   'Cofrajul Polistibrick fără panoul interior. Izolația de 20 sau 25 cm stă doar la exterior; fața interioară rămâne beton, '
   'gata de finisat cum vrei. Perete U 0,15 W/m²K cu Wall 200, U 0,12 cu Wall 250. Cofrajul costă 153–204 €/m² construit, livrat. '
   'La gri, cu montaj, 640–720 €/m².',
   f'{META} · ' + L('produse/polistiwall', P, 'Prețuri') + ': august 2026'),

 'produse/polistisip': (
   'Ce este PolistiSIP?',
   'O casă din panouri sandwich de lemn: OSB/3 pe ambele fețe, EPS grafitat la mijloc, structură I-Joist STEICO. '
   'Fără beton turnat pe șantier. Perete U 0,11 W/m²K. Kitul costă 201–242 €/m² construit, livrat. La gri, cu montaj, 590–640 €/m².',
   f'{META} · ' + L('produse/polistisip', P, 'Prețuri') + ': august 2026'),

 'pentru/proprietari': (
   'Cât costă o casă Polistibrick?',
   'Cofrajul: 197–281 €/m² construit, livrat. La gri, cu constructor: 690–810 €/m². La cheie, pe șantierele Polistibrick: 950–1.280 €/m². '
   'O casă clasică se face în 2026 la 900–1.350 €/m² la cheie. Diferența o vezi pe factură: 25–45 kWh/m²/an la încălzire și răcire, '
   'față de 100–180 la o casă din cărămidă neizolată.',
   f'{META} · ' + L('pentru/proprietari', P, 'Prețuri') + ': august 2026 · ' + L('pentru/proprietari', E, 'Calculator de economii')),
}

# pagini care deschid deja cu cifră și sursă: doar data
META_DOAR = {
 'resurse/casa-pasiva': f'{META} · Sursa: Passivhaus Institut, Darmstadt',
 'resurse/nzeb':        f'{META} · Sursa: Legea 372/2005, republicată',
}

# alinieri: prețul pieței «la cheie» era în 4 variante — trece pe cel canonic (cat-costa-o-casa)
ALINIERI = [
 ('resurse/bca-sau-caramida',
  r'Piața din 2026 cere la roșu 500–800 €/m² construit, iar la cheie 900–1\.300 €/m²; calculele mai conservatoare urcă la 1\.\d{3}–1\.\d{3} €/m²',
  'Piața din 2026 cere la roșu 450–700 €/m² construit, iar la cheie 900–1.350 €/m²; ghidurile prudente ale firmelor de construcții urcă la 1.250–1.650 €/m²'),
 ('resurse/cofraj-izolant',
  r'Piața generală cere la cheie 900–1\.650 €/m², după nivelul de finisaj \(orientativ\)',
  'Piața cere la cheie 900–1.350 €/m² pentru o casă clasică; ghidurile prudente ale firmelor de construcții urcă la 1.250–1.650 €/m² (Brig.ro, Wolf Construct, 2026)'),
 ('pentru/proprietari',
  r'structura la roșu pleacă de la circa 900 €/m² cu TVA\s*, iar la cheie ajunge în jur de 1\.300 €/m² cu TVA\s*',
  'structura la roșu costă 450–700 €/m², iar la cheie 900–1.350 €/m² (ghidurile firmelor de construcții pentru 2026)'),
 # prima pagină: U-ul peretelui în text, pe cardul Polistibrick
 ('', r'Torni betonul: casa e izolată, protejată, gata de finisat\.(?! Perete U)',
  'Torni betonul: casa e izolată, protejată, gata de finisat. Perete U = 0,14 W/m²K.'),
]

def text_site() -> str:
    t = []
    for f in BUILD.rglob('*.html'):
        h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', f.read_text(encoding='utf-8'), flags=re.S | re.I)
        t.append(html.unescape(re.sub(r'<[^>]+>', ' ', h)))
    s = ' '.join(t)
    return re.sub(r'\s*–\s*', '–', re.sub(r'[\s\xa0  ]+', ' ', s))

def numere(s: str) -> set:
    s = re.sub(r'<[^>]+>', ' ', s)
    # «Wall 200,» → «200», nu «200,» (virgula/punctul de la sfârșit sunt punctuație, nu cifră)
    return {n.rstrip('.,') for n in re.findall(r'\d[\d.,]*(?:–\d[\d.,]*)?', s)}

def main():
    if not BUILD.exists():
        sys.exit('rulează întâi build/build.py ro (verificarea cifrelor se face pe build)')
    site = text_site()
    # 1) plasa de siguranță: fiecare număr din blocuri există deja pe site
    lipsa = []
    for pag, (q, r, m) in BLOCURI.items():
        for n in numere(q + ' ' + r):
            if n in ('2026',):  # anul apare peste tot
                continue
            if n not in site and n.replace('.', '') not in site:
                lipsa.append(f'{pag}: {n}')
    if lipsa:
        print('CIFRE CARE NU EXISTĂ PE SITE — nimic scris:'); [print('  ✗', x) for x in lipsa]; sys.exit(1)
    # 2) blocurile — un bloc existent se ÎNLOCUIEȘTE (textul de aici e sursa lui), nu se dublează
    for pag, (q, r, m) in BLOCURI.items():
        f = RO / pag / 'index.html'; h = f.read_text(encoding='utf-8')
        nou = bloc(q, r, m)
        if 'class="raspuns"' in h:
            h2 = re.sub(r'\n?<section class="raspuns".*?</section>\n?', nou, h, count=1, flags=re.S)
            if h2 != h:
                f.write_text(h2, encoding='utf-8'); print(f'  ↻ {pag}: bloc actualizat')
            else:
                print(f'  = {pag}: bloc neschimbat')
            continue
        i = h.find('</h1>'); assert i > 0, pag
        i += len('</h1>')
        f.write_text(h[:i] + nou + h[i:], encoding='utf-8'); print(f'  + {pag}: bloc adăugat')
    # 3) doar data, pe paginile care deschid deja corect
    for pag, m in META_DOAR.items():
        f = RO / pag / 'index.html'; h = f.read_text(encoding='utf-8')
        if 'raspuns-meta' in h:
            print(f'  = {pag}: data deja prezentă'); continue
        i = h.find('<div class="ghid-intro">'); assert i > 0, pag
        j = h.find('</p>', i) + len('</p>')
        f.write_text(h[:j] + f'<p class="raspuns-meta">{m}</p>' + h[j:], encoding='utf-8'); print(f'  + {pag}: data adăugată')
    # 4) alinierile — exact o potrivire fiecare, altfel nu scriem
    for pag, rx, nou in ALINIERI:
        f = RO / pag / 'index.html' if pag else RO / 'index.html'; h = f.read_text(encoding='utf-8')
        n = len(re.findall(rx, h))
        if n == 0 and nou in h:
            print(f'  = {pag or "/"}: aliniat deja'); continue
        if n != 1:
            sys.exit(f'{pag or "/"}: {n} potriviri pentru «{rx[:50]}…» — nu scriu nimic')
        f.write_text(re.sub(rx, nou, h, count=1), encoding='utf-8'); print(f'  ~ {pag or "/"}: aliniat')

if __name__ == '__main__':
    main()
