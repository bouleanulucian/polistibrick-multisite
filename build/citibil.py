"""Site citibil de AI — pașii de build care fac faptele consecvente și extractibile.

Rulează după copy_tree + inject_seo + sitemap (are nevoie de HTML-ul final și de sitemap.xml).
Nu atinge textul vizibil al paginilor; atinge doar <head> (og:locale), blocurile JSON-LD și
fișierele generate (llms.txt, llms-full.txt).

  injecteaza_organization  un singur Organization pe tot site-ul, din _config.json + fapte.py;
                           dateModified din git și inLanguage pe WebPage/Article
  injecteaza_og_locale     <meta property="og:locale"> din _config.json (exista în config,
                           dar nu ajungea în pagină — audit 17.09.2026)
  genereaza_llms           llms.txt (scurt, fapte + lista paginilor) și llms-full.txt (tot
                           textul, pagină cu pagină) — generate, ca să nu rămână în urmă
  check_fapte              fiecare cifră din fapte.py există pe pagina ei → altfel build oprit
  check_organization       exact o variantă de Organization pe site → altfel build oprit
"""
import json
import re
import html as _html
from pathlib import Path

try:
    from fapte import fapte as _fapte
except ImportError:  # rulat din altă rădăcină
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fapte import fapte as _fapte

LD_RE = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)


# ───────────────────────────────────────────────────────────────── utilitare ──
def _text(fragment: str) -> str:
    return re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<[^>]+>', ' ', fragment))).strip()


def _fara_zgomot(h: str) -> str:
    """HTML-ul fără script/style/nav/header/footer — ce citește un crawler ca «pagină»."""
    return re.sub(r'<(script|style|nav|header|footer)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)


def _meta(h: str, nume: str) -> str:
    m = re.search(r'<meta[^>]+name=["\']' + nume + r'["\'][^>]+content=["\'](.*?)["\']', h, re.S | re.I)
    return _html.unescape(m.group(1)).strip() if m else ''


def _title(h: str) -> str:
    m = re.search(r'<title[^>]*>(.*?)</title>', h, re.S | re.I)
    return _text(m.group(1)) if m else ''


def _norm(s: str) -> str:
    """Pentru comparat cifre: spații de orice fel → spațiu, liniuțe de orice fel → «–»,
    fără spații în jurul liniuței («640 – 720» pe pagină = «640–720» în fapte)."""
    s = re.sub(r'[\s\xa0\u202f\u2009]+', ' ', s).replace('-', '–').replace('—', '–')
    return re.sub(r'\s*–\s*', '–', s)


def _url_pagina(rel: str, base: str) -> str:
    rel = rel[:-10] if rel.endswith('index.html') else rel
    return f'{base}/{rel}'


def _pagini_din_sitemap(out_dir: Path, base: str) -> list[Path]:
    """Paginile în ordinea sitemap-ului (adică doar cele indexabile), ca fișiere."""
    sm = (out_dir / 'sitemap.xml').read_text(encoding='utf-8')
    pagini = []
    for u in re.findall(r'<loc>(.*?)</loc>', sm):
        rel = u[len(base):].lstrip('/')
        f = out_dir / rel / 'index.html' if rel else out_dir / 'index.html'
        if f.exists():
            pagini.append(f)
    return pagini


# ────────────────────────────────────────────────────────────── organization ──
def organization_canonic(config: dict, code: str) -> dict:
    c, k = config.get('company', {}), config.get('contact', {})
    base = config.get('domain_url', '').rstrip('/')
    same_as = []
    for f in _fapte(code).get('marci', []):
        same_as.append(f['url'])
    b = _fapte(code).get('brevet', {})
    if b.get('url'):
        same_as.insert(0, b['url'])
    for retea in ('linkedin', 'youtube', 'instagram', 'facebook', 'tiktok'):
        u = (k.get('social') or {}).get(retea)
        if u:
            same_as.append(u)
    # logo ca ImageObject cu dimensiunile reale (auditul de schemă: string-ul simplu dă
    # avertisment și la Article.publisher.logo); dimensiunile din antetul PNG, fără PIL
    logo = {'@type': 'ImageObject', 'url': f'{base}/images/logo.png'}
    try:
        cap = (Path(__file__).resolve().parent.parent / 'shared' / 'images' / 'logo.png').read_bytes()[:24]
        if cap[:8] == b'\x89PNG\r\n\x1a\n':
            logo['width'], logo['height'] = int.from_bytes(cap[16:20], 'big'), int.from_bytes(cap[20:24], 'big')
    except OSError:
        pass
    ent = _fapte(code).get('organization', {})   # ce avea blocul bogat de pe prima pagină
    org = {
        '@type': 'Organization',
        '@id': f'{base}/#organizatie',
        'name': c.get('name_legal') or c.get('name_short'),
        'legalName': c.get('name_legal'),
        'alternateName': ent.get('alternateName') or ([c.get('name_short')] if c.get('name_short') else None),
        'description': ent.get('description'),
        'url': f'{base}/',
        'logo': logo,
        'telephone': k.get('phone'),
        'email': k.get('email_general'),
        'vatID': c.get('vat'),
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': c.get('address_street'),
            'addressLocality': c.get('address_city'),
            'postalCode': c.get('address_zip'),
            'addressCountry': config.get('country'),
        },
        'sameAs': same_as or None,
    }
    return {k2: v for k2, v in org.items() if v not in (None, '', [], {})}


def _rescrie_ld(h: str, org: dict, data_mod: str, lang: str) -> tuple[str, bool]:
    """Înlocuiește orice nod Organization cu cel canonic; completează dateModified/inLanguage.
    Returnează (html_nou, a_avut_organization)."""
    avut = False

    def _pe_nod(x: dict) -> dict:
        nonlocal avut
        t = x.get('@type')
        if t == 'Organization':
            avut = True
            return dict(org)
        if t in ('WebPage', 'Article', 'NewsArticle', 'CollectionPage', 'ContactPage') or \
                (isinstance(t, list) and 'WebPage' in t):
            if data_mod:
                x['dateModified'] = data_mod
            x.setdefault('inLanguage', lang)
        return x

    def _pe_bloc(m: re.Match) -> str:
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        if isinstance(d, dict) and '@graph' in d:
            d['@graph'] = [_pe_nod(x) if isinstance(x, dict) else x for x in d['@graph']]
        elif isinstance(d, list):
            d = [_pe_nod(x) if isinstance(x, dict) else x for x in d]
        elif isinstance(d, dict):
            d = _pe_nod(d)
        return m.group(0)[:m.start(1) - m.start()] + json.dumps(d, ensure_ascii=False) + '</script>'

    h2 = LD_RE.sub(_pe_bloc, h)
    return h2, avut


def injecteaza_organization(out_dir: Path, config: dict, code: str, data_git, countries_dir: Path):
    org = organization_canonic(config, code)
    lang = config.get('lang', code)
    n_inloc, n_adaug = 0, 0
    for f in out_dir.rglob('*.html'):
        h = f.read_text(encoding='utf-8')
        if 'ld+json' not in h and '</head>' not in h:
            continue
        rel = f.relative_to(out_dir)
        sursa = countries_dir / code / rel
        data_mod = data_git(sursa) if sursa.exists() else ''
        h2, avut = _rescrie_ld(h, org, data_mod, lang)
        # pagini fără niciun nod WebPage/Article (audit 17.09: /preturi/ și două pagini de produs
        # au doar Product + FAQPage) → primesc un WebPage minim, ca să existe dateModified și limba
        if '</head>' in h2 and 'noindex' not in h2[:4000] and not re.search(
                r'"@type":\s*"(?:WebPage|Article|NewsArticle|CollectionPage|ContactPage)"', h2):
            base = config.get('domain_url', '').rstrip('/')
            rel_url = rel.as_posix()
            rel_url = rel_url[:-10] if rel_url.endswith('index.html') else rel_url
            wp = {'@type': 'WebPage', '@id': f'{base}/{rel_url}#webpage', 'url': f'{base}/{rel_url}',
                  'name': _title(h2), 'description': _meta(h2, 'description') or None,
                  'inLanguage': lang, 'dateModified': data_mod or None,
                  'isPartOf': {'@id': f'{base}/#website'}, 'about': {'@id': org['@id']}}
            wp = {k: v for k, v in wp.items() if v}
            bloc_wp = ('<script type="application/ld+json">'
                       + json.dumps({'@context': 'https://schema.org', '@graph': [wp]}, ensure_ascii=False)
                       + '</script>\n')
            h2 = h2.replace('</head>', bloc_wp + '</head>', 1)
        if avut:
            n_inloc += 1
        elif '</head>' in h2 and 'noindex' not in h2[:4000]:
            # același nod ca pe celelalte pagini (în @graph, fără @context în nod), altfel
            # check_organization îl vede ca a doua variantă — s-a întâmplat la prima rulare
            bloc = ('<script type="application/ld+json">'
                    + json.dumps({'@context': 'https://schema.org', '@graph': [org]}, ensure_ascii=False)
                    + '</script>\n')
            h2 = h2.replace('</head>', bloc + '</head>', 1)
            n_adaug += 1
        if h2 != h:
            f.write_text(h2, encoding='utf-8')
    print(f'  · Organization canonic: {n_inloc} înlocuite, {n_adaug} adăugate')


def injecteaza_og_locale(out_dir: Path, config: dict):
    loc = (config.get('metadata') or {}).get('og_locale')
    if not loc:
        return
    tag = f'<meta property="og:locale" content="{loc}">\n'
    n = 0
    for f in out_dir.rglob('*.html'):
        h = f.read_text(encoding='utf-8')
        if 'og:locale' in h or '</head>' not in h:
            continue
        f.write_text(h.replace('</head>', tag + '</head>', 1), encoding='utf-8')
        n += 1
    print(f'  · og:locale {loc}: {n} pagini')


# ──────────────────────────────────────────────────────────────────── llms ──
def _numara_modele(out_dir: Path) -> tuple[int, str]:
    f = next((out_dir / d / 'index.html' for d in ('proiecte', 'projets', 'progetti', 'proyectos')
              if (out_dir / d / 'index.html').exists()), None)
    if f is None:
        return 0, ''
    h = f.read_text(encoding='utf-8')
    nume = set()
    for card in re.findall(r'<article class="case-card"[^>]*>(.*?)</article>', h, re.S):
        m = re.search(r'<h2[^>]*>(.*?)(?:<span|</h2>)', card, re.S)
        if m:
            nume.add(_text(m.group(1)))
    mp = [int(x) for x in re.findall(r'<b>(\d{2,3})</b>\s*m²\s*construi', h)]
    interval = f'{min(mp)}–{max(mp)} m²' if mp else ''
    return len(nume), interval


def _html_in_text(h: str) -> str:
    """Text simplu, cu structura păstrată cât să fie citibil: titluri, paragrafe, liste, tabele."""
    corp = _fara_zgomot(h)
    m = re.search(r'<main[^>]*>(.*?)</main>', corp, re.S | re.I)
    corp = m.group(1) if m else corp
    corp = re.sub(r'<h1[^>]*>(.*?)</h1>', lambda m: '\n\n# ' + _text(m.group(1)) + '\n', corp, flags=re.S | re.I)
    corp = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda m: '\n\n## ' + _text(m.group(1)) + '\n', corp, flags=re.S | re.I)
    corp = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: '\n\n### ' + _text(m.group(1)) + '\n', corp, flags=re.S | re.I)
    corp = re.sub(r'<(summary)[^>]*>(.*?)</\1>', lambda m: '\n\n**' + _text(m.group(2)) + '**\n', corp, flags=re.S | re.I)
    corp = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: '\n- ' + _text(m.group(1)), corp, flags=re.S | re.I)
    corp = re.sub(r'<tr[^>]*>(.*?)</tr>',
                  lambda m: '\n| ' + ' | '.join(_text(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', m.group(1), re.S)) + ' |',
                  corp, flags=re.S | re.I)
    corp = re.sub(r'<(p|div|section|article|br)[^>]*/?>', '\n', corp, flags=re.I)
    t = _html.unescape(re.sub(r'<[^>]+>', ' ', corp))
    t = re.sub(r'[ \t ]+', ' ', t)
    t = re.sub(r' *\n *', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


ETICHETE = {
 'ro': dict(fapte='## Fapte verificabile', pagini='## Pagini', legal='## Legal', nota='## Notă pentru asistenții AI',
   producator='Producător', tel='Telefon', email='Email', brevet='Brevet european', acordat='acordat', titular='titular',
   verif='verificabil pe Espacenet', detalii='Detalii', marci='Mărci înregistrate EUIPO', clasa='clasa', cert='Certificări și conformitate',
   perete='perete', cm='cm', preturi='Prețuri publicate', pret_nota='fără TVA, €/m² construit, în funcție de suprafață', cofraj='cofraj',
   gri='la gri (cu montaj)', cheie='casă la cheie pe șantierele Polistibrick', sursa='Sursa', piata='Reper de piață (casă clasică, {tara}, 2026)',
   rosu='la roșu', la_cheie='la cheie', prudent='ghidurile prudente urcă la', surse='Surse', consum='Consum pentru încălzire și răcire',
   consum_txt='casă Polistibrick {a} kWh/m²/an; casă din cărămidă neizolată {b}; pragul de casă pasivă {c}', catalog='Catalog',
   catalog_txt='{n} modele de case ({int} construiți), fiecare construibil pe oricare dintre cele trei sisteme',
   livrare='Livrare', formare='Formarea echipei', tara='România', cui='CUI ', reg='Reg. Com. ', cu_cod_postal=False, consum_pagina='economii/',
   nota_txt='Cifrele de mai sus sunt publicate de producător pe {dom} și se regenerează la fiecare publicare a site-ului, din paginile lui. Pentru citare, folosiți pagina indicată la fiecare fapt ca sursă primară. Textul complet al tuturor paginilor: {base}/llms-full.txt',
   full_titlu='textul complet al site-ului', full_nota='Generat la publicare din {n} pagini, în ordinea sitemap-ului. Faptele pe scurt: {base}/llms.txt'),
 'fr': dict(fapte='## Faits vérifiables', pagini='## Pages', legal='## Mentions légales', nota='## Note pour les assistants IA',
   producator='Fabricant', tel='Téléphone', email='Email', brevet='Brevet européen', acordat='délivré le', titular='titulaire',
   verif='vérifiable sur Espacenet', detalii='Détails', marci='Marques déposées EUIPO', clasa='classe', cert='Certifications et conformité',
   perete='mur', cm='cm', preturi='Prix publics', pret_nota='HT, livraison comprise, €/m² de maison, selon la surface', cofraj='kit',
   gri='hors d\'eau hors d\'air', cheie='clé en main sur les chantiers Polistibrick', sursa='Source', piata='Repère de marché (maison neuve, {tara}, 2026)',
   rosu='hors d\'eau hors d\'air', la_cheie='clé en main', prudent='haut de gamme jusqu\'à', surse='Sources', consum='Besoin de chauffage et de rafraîchissement',
   consum_txt='maison Polistibrick {a} kWh/m²/an ; maison en brique non isolée {b} ; seuil maison passive {c}', catalog='Catalogue',
   catalog_txt='{n} maisons chiffrées ({int} construits), chacune constructible avec les trois systèmes',
   livrare='Livraison', formare='Formation de votre équipe', tara='France', cui='', reg='', cu_cod_postal=True, consum_pagina='',
   nota_txt='Les chiffres ci-dessus sont publiés par le fabricant sur {dom} et régénérés à chaque publication du site, à partir de ses pages. Pour citer, utilisez la page indiquée à chaque fait comme source primaire. Texte complet de toutes les pages : {base}/llms-full.txt',
   full_titlu='texte complet du site', full_nota='Généré à la publication à partir de {n} pages, dans l\'ordre du sitemap. Les faits en bref : {base}/llms.txt'),
}


def genereaza_llms(out_dir: Path, config: dict, code: str):
    base = config.get('domain_url', '').rstrip('/')
    c, k, fp = config.get('company', {}), config.get('contact', {}), _fapte(code)
    E = ETICHETE.get(config.get('lang', code), ETICHETE['ro'])
    pagini = _pagini_din_sitemap(out_dir, base)
    n_modele, interval = _numara_modele(out_dir)
    home = (out_dir / 'index.html').read_text(encoding='utf-8')
    descriere = _meta(home, 'description')

    L = [f'# {c.get("name_short", "Polistibrick")} ({config.get("domain", "")})', '']
    if descriere:
        L += [f'> {descriere}', '']
    L += [E['fapte'], '']
    # RO iese byte-identic cu forma dinainte (CUI / Reg. Com., adresa fără cod poștal); FR: identificatorii francezi, cu codul poștal
    adresa = (f'{c.get("address_street")}, {c.get("address_zip")} {c.get("address_city")}' if E['cu_cod_postal']
              else f'{c.get("address_street")}, {c.get("address_city")}')
    L.append(f'- {E["producator"]}: {c.get("name_legal")}, {E["cui"]}{c.get("vat")}, {E["reg"]}{c.get("registration")}, '
             f'{adresa}. {E["tel"]}: {k.get("phone")}. {E["email"]}: {k.get("email_general")}.')
    if fp.get('brevet'):
        b = fp['brevet']
        L.append(f'- {E["brevet"]}: {b["numar"]}, {E["acordat"]} {b["acordat"]}, {E["titular"]} {b["titular"]} '
                 f'({E["verif"]}: {b["url"]}). {E["detalii"]}: {base}/{b["pagina"]}')
    if fp.get('marci'):
        L.append(f'- {E["marci"]}: ' + ', '.join(f'{m["numar"]} ({E["clasa"]} {m["clase"]})' for m in fp['marci']) + '.')
    if fp.get('certificari'):
        L.append(f'- {E["cert"]}: ' + '; '.join(fp['certificari']) + f'. {E["detalii"]}: {base}/' +
                 ('a-propos/certifications/' if code == 'fr' else 'despre/certificari/'))
    for nume, s_ in fp.get('sisteme', {}).items():
        L.append(f'- {nume}: U = {s_.get("U_text", s_["U"])} W/m²K, {E["perete"]} {s_["perete_cm"]} {E["cm"]}, {s_["compozitie"]}. {E["detalii"]}: {base}/{s_["pagina"]}')
    if fp.get('preturi'):
        p = fp['preturi']
        rand = (f'- {E["preturi"]} ({p["luna"]}, {E["pret_nota"]}): {E["cofraj"]} — '
                + ', '.join(f'{n} {v}' for n, v in p['cofraj'].items()))
        if p.get('la_gri'):
            rand += f'; {E["gri"]} — ' + ', '.join(f'{n} {v}' for n, v in p['la_gri'].items())
        if p.get('la_cheie_polistibrick'):
            rand += f'; {E["cheie"]} — {p["la_cheie_polistibrick"]}'
        L.append(rand + f'. {E["sursa"]}: {base}/{p["pagina"]}')
    if fp.get('livrare'):
        L.append(f'- {E["livrare"]}: {fp["livrare"]}.')
    if fp.get('formare'):
        L.append(f'- {E["formare"]}: {fp["formare"]}.')
    if fp.get('piata'):
        pi = fp['piata']
        rand = f'- {E["piata"].format(tara=E["tara"])}: {E["rosu"]} {pi["la_rosu"]} €/m², {E["la_cheie"]} {pi["la_cheie"]} €/m²'
        if pi.get('la_cheie_prudent'):
            rand += f'; {E["prudent"]} {pi["la_cheie_prudent"]} €/m²'
        L.append(rand + f'. {E["surse"]}: ' + '; '.join(f'{s_["nume"]} ({s_["url"]})' for s_ in pi['surse']) + f'. {E["detalii"]}: {base}/{pi["pagina"]}')
    if fp.get('consum_kwh'):
        cs = fp['consum_kwh']
        L.append(f'- {E["consum"]}: ' + E['consum_txt'].format(a=cs['polistibrick'], b=cs['caramida_neizolata'], c=cs['pasiv_max']) + '.'
                 + (f' {E["detalii"]}: {base}/{E["consum_pagina"]}' if E['consum_pagina'] else ''))
    if n_modele:
        L.append(f'- {E["catalog"]}: ' + E['catalog_txt'].format(n=n_modele, int=interval) + f': {base}/' + ('projets/' if code == 'fr' else 'proiecte/'))
    L += ['', E['pagini'], '']
    legal = []
    for f in pagini:
        h = f.read_text(encoding='utf-8')
        rel = f.relative_to(out_dir).as_posix()
        u = _url_pagina(rel, base)
        rand = f'- [{_title(h)}]({u}): {_meta(h, "description")}'.rstrip(': ')
        (legal if '/legal/' in u else L).append(rand)
    if legal:
        L += ['', E['legal'], ''] + legal
    L += ['', E['nota'], '', E['nota_txt'].format(dom=config.get('domain'), base=base), '']
    (out_dir / 'llms.txt').write_text('\n'.join(L), encoding='utf-8')

    F = [f'# {c.get("name_short", "Polistibrick")} ({config.get("domain", "")}) — {E["full_titlu"]}', '',
         E['full_nota'].format(n=len(pagini), base=base), '']
    for f in pagini:
        h = f.read_text(encoding='utf-8')
        u = _url_pagina(f.relative_to(out_dir).as_posix(), base)
        F += ['', '---', '', f'# {_title(h)}', f'URL: {u}', '']
        d = _meta(h, 'description')
        if d:
            F += [f'> {d}', '']
        F.append(_html_in_text(h))
    (out_dir / 'llms-full.txt').write_text('\n'.join(F) + '\n', encoding='utf-8')
    print(f'  · llms.txt ({len(pagini)} pagini, {n_modele} modele) + llms-full.txt ({(out_dir / "llms-full.txt").stat().st_size // 1024} KB)')


# ─────────────────────────────────────────────────────────────── verificări ──
def check_fapte(out_dir: Path, code: str):
    """Fiecare cifră din fapte.py trebuie să existe în TEXTUL paginii indicate. Altfel llms.txt
    ar afirma ceva ce pagina nu spune — exact boala pe care o vindecăm."""
    fp = _fapte(code)
    if not fp:
        return
    lipsuri = []

    def _cere(pagina: str, *cifre: str):
        f = out_dir / pagina / 'index.html'
        if not f.exists():
            lipsuri.append(f'{pagina}: pagina lipsește'); return
        t = _norm(_text(_fara_zgomot(f.read_text(encoding='utf-8'))))
        for c in cifre:
            if _norm(c) not in t:
                lipsuri.append(f'{pagina}: «{c}» nu apare în text')

    if fp.get('brevet'):
        _cere(fp['brevet']['pagina'], fp['brevet']['numar'])
    for s in fp.get('sisteme', {}).values():
        # U-ul e scris pe pagini ca «U = 0,14» sau «U 0,10–0,14»: cerem capetele intervalului
        for cap in s['U'].split('–'):
            _cere(s['pagina'], cap)
    if fp.get('preturi'):
        p = fp['preturi']
        # cofrajul e scris pe pagină ca «de la 153 €/m² … 204 €/m² la 100 m²», nu ca interval:
        # cerem fiecare capăt; la gri și la cheie sunt intervale pe pagină («640 – 720»)
        capete = [c for v in p['cofraj'].values() for c in v.split('–')]
        _cere(p['pagina'], *capete, *[v for v in p.get('la_gri', {}).values()],
              *([p['la_cheie_polistibrick']] if p.get('la_cheie_polistibrick') else []), p['luna'])
    if fp.get('piata'):
        pi = fp['piata']
        _cere(pi['pagina'], pi['la_cheie'], pi['la_rosu'])
    if code == 'fr':
        _cere('a-propos/certifications', 'ISO 9001', 'ISO 14001', 'ISO 45001', 'A1', 'CE')
    else:
        _cere('despre/certificari', 'EAD 040287-00-1201', 'ISO 9001', 'ISO 14001', 'ISO 45001', 'A1', 'CPR')
    if lipsuri:
        print('\n  ✗ FAPTE NECONCORDANTE — build oprit:')
        for l in lipsuri:
            print('      ' + l)
        raise SystemExit('fapte.py spune ceva ce pagina nu spune. Corectează pagina sau fapte.py.')
    print('  · check_fapte: toate cifrele din fapte.py există pe paginile lor')


def check_organization(out_dir: Path):
    variante = {}
    for f in out_dir.rglob('*.html'):
        h = f.read_text(encoding='utf-8')
        for b in LD_RE.findall(h):
            try:
                d = json.loads(b)
            except Exception:
                raise SystemExit(f'JSON-LD stricat în {f.relative_to(out_dir)}')
            noduri = d.get('@graph') if isinstance(d, dict) and '@graph' in d else (d if isinstance(d, list) else [d])
            for x in noduri:
                if isinstance(x, dict) and x.get('@type') == 'Organization':
                    variante.setdefault(json.dumps(x, sort_keys=True, ensure_ascii=False), []).append(f.relative_to(out_dir).as_posix())
    if len(variante) > 1:
        print('\n  ✗ ORGANIZATION ÎN MAI MULTE VARIANTE — build oprit:')
        for v, pagini in variante.items():
            print(f'      {len(pagini)} pagini, ex. {pagini[:3]}')
        raise SystemExit('Organization trebuie să fie identic pe tot site-ul.')
    print(f'  · check_organization: o singură variantă pe {sum(len(v) for v in variante.values())} pagini')
