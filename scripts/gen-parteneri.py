#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generează pagina /parteneri/ (hartă interactivă a României) și câte o pagină
pentru fiecare constructor partener.

    python3 scripts/gen-parteneri.py

Citește:
    countries/ro/_parteneri.json      — datele partenerilor (sursa de adevăr)
    scripts/parteneri/harta-ro.json   — conturul celor 42 de județe, proiectat

Scrie:
    countries/ro/parteneri/index.html
    countries/ro/parteneri/<slug>/index.html

Harta a fost proiectată o singură dată din Natural Earth (ne_10m_admin_1).
Proiecția e echirectangulară, corectată cu cos(lat_mijloc), și e salvată în
harta-ro.json împreună cu constantele — pinurile se așază cu aceeași formulă,
deci un partener nou are nevoie doar de lat/lon în _parteneri.json.
"""
import json
import math
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = ROOT / "countries" / "ro" / "_parteneri.json"
HARTA = ROOT / "scripts" / "parteneri" / "harta-ro.json"
OUT = ROOT / "countries" / "ro" / "parteneri"

SISTEM_URL = {
    "Polistibrick": "produse/polistibrick/",
    "Polistiwall": "produse/polistiwall/",
    "PolistiSIP": "produse/polistisip/",
}


def e(s):
    return escape(str(s), quote=True)


def tel_link(t):
    return "+4" + re.sub(r"[^0-9]", "", t) if re.search(r"[0-9]", t) else ""


# ────────────────────────────────────────────────────────── date

harta = json.loads(HARTA.read_text(encoding="utf-8"))
date = json.loads(DATE.read_text(encoding="utf-8"))
parteneri = date["parteneri"]
JUD = {j["cod"]: j for j in harta["judete"]}
W, H = harta["w"], harta["h"]


def proiecteaza(lon, lat):
    x = (lon - harta["lon0"]) * harta["k"] * harta["s"]
    y = (harta["lat1"] - lat) * harta["s"]
    return x, y


# pinuri, cu împrăștiere când doi parteneri cad unul peste altul
for p in parteneri:
    p["x"], p["y"] = proiecteaza(p["lon"], p["lat"])
PRAG = 26.0
for i, p in enumerate(parteneri):
    vecini = [q for q in parteneri[:i] if math.hypot(q["x"] - p["x"], q["y"] - p["y"]) < PRAG]
    if vecini:
        unghi = math.radians(35 * len(vecini))
        p["x"] += math.cos(unghi) * PRAG
        p["y"] -= math.sin(unghi) * PRAG

# Clientul îşi alege singur constructorul de pe hartă (decizia patronului, 29.08.2026),
# deci doi constructori POT acoperi acelaşi judeţ. Nu e eroare, dar se spune —
# suprapunerile sunt exact locurile unde doi parteneri ajung să se bată pe acelaşi om.
_revendicat = {}
for p in parteneri:
    for c in {p["judet_cod"], *p.get("acopera", [])}:
        _revendicat.setdefault(c, []).append(p["slug"])
SUPRAPUNERI = {c: s for c, s in sorted(_revendicat.items()) if len(s) > 1}

CU_PARTENER = {p["judet_cod"] for p in parteneri}
ACOPERIT = {c for p in parteneri for c in p.get("acopera", [])} - CU_PARTENER
ARE_DEMO = any(p.get("demo") for p in parteneri)


# ────────────────────────────────────────────────────────── bucăți comune

def cap(titlu, descriere, base, cale, extra_css=""):
    """Antetul <head> + deschiderea <body>, în tiparul celorlalte pagini RO."""
    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(titlu)}</title>
  <link rel="icon" type="image/png" href="{base}images/favicon.png">
  <link rel="apple-touch-icon" href="{base}images/apple-touch-icon.png">
  <meta name="description" content="{e(descriere)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(titlu)}">
  <meta property="og:description" content="{e(descriere)}">
  <meta property="og:image" content="https://polisti.ro/images/hero/hero-house-1.jpg">
  <meta property="og:url" content="{{{{domain_url}}}}/{cale}">
  <meta property="og:locale" content="ro_RO">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{base}assets/css/site.css">
  <style>
{CSS_PARTENERI}
{extra_css}
  </style>
</head>
<body data-base="{base}">

<header class="nav" data-include="nav"></header>
"""


def coada(base, scripturi=""):
    return f"""
<footer class="site-footer" data-include="footer"></footer>
<script src="{base}assets/js/site.js" defer></script>
{scripturi}
</body>
</html>
"""


CSS_PARTENERI = """
    .pt-hero { padding: calc(var(--nav-height) + 56px) 0 0; background: var(--cream); }
    .pt-hero h1 { max-width: 16ch; }
    .pt-hero .lead { max-width: 60ch; margin-top: 18px; color: var(--gray); font-size: 18px; }
    .pt-demo {
      margin: 28px 0 0; padding: 14px 18px; border-left: 3px solid var(--red);
      background: var(--red-soft); font-size: 14px; border-radius: 0 6px 6px 0;
    }
    .pt-demo strong { color: var(--red-dark); }

    /* ── harta ── */
    .pt-map-section { padding: 40px 0 24px; }
    .pt-map-wrap {
      position: relative; max-width: 1120px; margin: 0 auto;
    }
    .pt-map { width: 100%; height: auto; display: block; overflow: visible; }
    .pt-jud { fill: #EAE4D7; stroke: #FBF9F4; stroke-width: 1.4; transition: fill .18s; }
    .pt-jud.is-acoperit { fill: #D8CDB6; }
    .pt-jud.is-sediu { fill: #EFC3CB; }
    .pt-pin { cursor: pointer; }
    .pt-pin .pin-halo { fill: var(--red); opacity: .16; transition: r .18s, opacity .18s; }
    .pt-pin .pin-dot { fill: var(--red); stroke: #fff; stroke-width: 2.2; transition: r .18s; }
    .pt-pin:hover .pin-halo, .pt-pin:focus .pin-halo { r: 26; opacity: .28; }
    .pt-pin:hover .pin-dot, .pt-pin:focus .pin-dot { r: 11; }
    .pt-pin:focus { outline: none; }
    .pt-pin:focus .pin-dot { stroke: var(--ink); }

    .pt-tip {
      position: absolute; pointer-events: none; opacity: 0; transform: translate(-50%, -100%);
      background: var(--ink); color: #fff; padding: 9px 13px; border-radius: 8px;
      font-size: 13px; line-height: 1.35; white-space: nowrap; transition: opacity .14s;
      z-index: 5; box-shadow: var(--shadow-md);
    }
    .pt-tip.on { opacity: 1; }
    .pt-tip b { display: block; font-weight: 600; }
    .pt-tip span { color: var(--gray-light); font-size: 12px; }

    .pt-legend { display: flex; flex-wrap: wrap; justify-content: center; gap: 22px; margin-top: 10px; font-size: 13px; color: var(--gray); }
    .pt-legend i { width: 13px; height: 13px; border-radius: 3px; display: inline-block; margin-right: 7px; vertical-align: -2px; }

    .pt-subsol { text-align: center; margin-top: 26px; font-size: 15px; color: var(--gray); }
    .pt-subsol a { color: var(--red); font-weight: 600; }

    /* ── pagina unui partener ── */
    .pp-head { padding: calc(var(--nav-height) + 46px) 0 0; }
    .pp-back { font-size: 14px; color: var(--gray); display: inline-block; margin-bottom: 22px; }
    .pp-back:hover { color: var(--red); }
    .pp-grid { display: grid; grid-template-columns: 1fr 360px; gap: 46px; align-items: start; padding: 34px 0 90px; }
    .pp-block { margin-bottom: 34px; }
    .pp-block h2 { font-size: 14px; text-transform: uppercase; letter-spacing: .08em; color: var(--gray); margin-bottom: 12px; }
    .pp-block p { color: var(--ink-soft); line-height: 1.7; }
    .pp-fapte { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1px; background: var(--border); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
    .pp-fapt { background: var(--cream-light); padding: 18px 20px; }
    .pp-fapt b { display: block; font-size: 22px; font-weight: 600; letter-spacing: -.02em; }
    .pp-fapt span { font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--gray); }
    .pp-zone { display: flex; flex-wrap: wrap; gap: 7px; }

    .pp-contact { position: sticky; top: calc(var(--nav-height) + 20px); background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 26px; box-shadow: var(--shadow-sm); }
    .pp-contact h3 { font-size: 18px; margin-bottom: 4px; }
    .pp-contact .sub { font-size: 13px; color: var(--gray); margin-bottom: 20px; }
    .pp-rand { padding: 13px 0; border-top: 1px solid var(--border); font-size: 15px; }
    .pp-rand .et { font-size: 11px; text-transform: uppercase; letter-spacing: .07em; color: var(--gray); display: block; margin-bottom: 3px; }
    .pp-rand a:hover { color: var(--red); }
    .pp-mini { width: 100%; height: auto; margin-top: 20px; border-radius: 10px; background: var(--cream); display: block; }
    .pp-mini .mj { fill: #EDE8DD; stroke: #fff; stroke-width: 1.1; }
    .pp-mini .mj.on { fill: #F3D2D8; }
    .pp-legal { font-size: 12px; color: var(--gray); line-height: 1.6; margin-top: 18px; }

    @media (max-width: 980px) {
      .pp-grid { grid-template-columns: 1fr; }
      .pp-contact { position: static; }
    }
"""


def svg_harta(clasa="pt-map", ids=True):
    out = []
    for j in harta["judete"]:
        cls = "pt-jud"
        if j["cod"] in CU_PARTENER:
            cls += " is-sediu"
        elif j["cod"] in ACOPERIT:
            cls += " is-acoperit"
        idattr = f' id="jud-{j["cod"]}"' if ids else ""
        out.append(f'<path{idattr} class="{cls}" d="{j["d"]}"><title>{e(j["nume"])}</title></path>')
    return "\n      ".join(out)


def svg_pinuri():
    out = []
    for p in parteneri:
        url = f'{p["slug"]}/'
        out.append(
            f'<a class="pt-pin" href="{url}" data-slug="{e(p["slug"])}" '
            f'data-nume="{e(p["nume"])}" data-oras="{e(p["oras"])}, jud. {e(p["judet"])}" '
            f'data-x="{p["x"]:.1f}" data-y="{p["y"]:.1f}">'
            f'<circle class="pin-halo" cx="{p["x"]:.1f}" cy="{p["y"]:.1f}" r="19"/>'
            f'<circle class="pin-dot" cx="{p["x"]:.1f}" cy="{p["y"]:.1f}" r="8.5"/>'
            f'<title>{e(p["nume"])} — {e(p["oras"])}</title></a>'
        )
    return "\n      ".join(out)


# ────────────────────────────────────────────────────────── pagina hartă

def scrie_index():
    """Doar harta. Clientul îşi alege singur constructorul, văzând cine îi e aproape."""
    demo_bloc = ""
    if ARE_DEMO:
        demo_bloc = """
      <div class="pt-demo">
        <strong>Pagină în lucru.</strong> Constructorii de pe hartă sunt exemple, puse ca să se vadă
        cum arată. Datele reale intră când avem lista partenerilor.
      </div>"""

    html = cap(
        "Constructor partener Polistibrick — harta rețelei din România",
        "Harta constructorilor parteneri Polistibrick. Alege-l pe cel mai apropiat de tine și vezi datele lui de contact.",
        "../", "parteneri/",
    ) + f"""
<section class="pt-hero">
  <div class="container">
    <h1>Constructorul care <em>îți ridică</em> casa.</h1>
    <p class="lead">Noi fabricăm sistemul. Casa o montează un constructor partener, instruit de noi.
      Caută-l pe hartă pe cel mai apropiat de tine și dă clic pe el.</p>{demo_bloc}
  </div>
</section>

<section class="pt-map-section">
  <div class="container">
    <div class="pt-map-wrap reveal">
      <svg class="pt-map" viewBox="0 0 {W} {H}" role="img" aria-label="Harta constructorilor parteneri din România">
      {svg_harta()}
      {svg_pinuri()}
      </svg>
      <div class="pt-tip" id="tip"></div>
    </div>
    <div class="pt-legend">
      <span><i style="background:#EFC3CB"></i>Sediul unui constructor partener</span>
      <span><i style="background:#D8CDB6"></i>Județ acoperit</span>
      <span><i style="background:#EAE4D7"></i>Încă fără constructor</span>
    </div>
    <p class="pt-subsol">Nu vezi pe nimeni în zona ta? <a href="../oferta/">Scrie-ne unde construiești</a>
      și îți trimitem kitul, cu un constructor instruit de noi.</p>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    <div class="cta-band reveal">
      <h2>Ești constructor? <em>Intră în rețea.</em></h2>
      <p>Curs de certificare de 3 zile, gratuit. Primești teritoriu alocat și clienții din zona ta.</p>
      <div class="cta-band-actions">
        <a href="../devino-partener/" class="btn btn-on-dark btn-large btn-arrow">Devino partener</a>
        <a href="../contact/" class="btn btn-on-dark-ghost btn-large">Întreabă-ne întâi</a>
      </div>
    </div>
  </div>
</section>
""" + coada("../", """<script>
(function () {
  var wrap = document.querySelector('.pt-map-wrap');
  var svg = document.querySelector('.pt-map');
  var tip = document.getElementById('tip');

  function aratTip(pin) {
    var r = svg.getBoundingClientRect();
    var sc = r.width / svg.viewBox.baseVal.width;
    var wr = wrap.getBoundingClientRect();
    tip.innerHTML = '<b>' + pin.dataset.nume + '</b><span>' + pin.dataset.oras + '</span>';
    tip.style.left = (r.left - wr.left + parseFloat(pin.dataset.x) * sc) + 'px';
    tip.style.top = (r.top - wr.top + parseFloat(pin.dataset.y) * sc - 14) + 'px';
    tip.classList.add('on');
  }

  [].slice.call(document.querySelectorAll('.pt-pin')).forEach(function (pin) {
    ['mouseenter', 'focus'].forEach(function (ev) {
      pin.addEventListener(ev, function () { aratTip(pin); });
    });
    ['mouseleave', 'blur'].forEach(function (ev) {
      pin.addEventListener(ev, function () { tip.classList.remove('on'); });
    });
    // pe telefon nu există hover: prima atingere arată cine e, a doua deschide pagina
    pin.addEventListener('click', function (ev) {
      if (!matchMedia('(hover: none)').matches) return;
      if (tip.classList.contains('on') && tip.dataset.slug === pin.dataset.slug) return;
      ev.preventDefault();
      aratTip(pin);
      tip.dataset.slug = pin.dataset.slug;
    });
  });

  document.addEventListener('click', function (ev) {
    if (!ev.target.closest('.pt-pin')) { tip.classList.remove('on'); tip.dataset.slug = ''; }
  });
})();
</script>""")
    (OUT / "index.html").write_text(html, encoding="utf-8")


# ────────────────────────────────────────────────────────── pagina fiecărui partener

def scrie_partener(p):
    d = OUT / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    tel = tel_link(p["telefon"])
    demo = '<span class="pt-chip pt-chip--demo" style="vertical-align:middle;margin-left:10px">date de exemplu</span>' if p.get("demo") else ""

    randuri = [f'<div class="pp-rand"><span class="et">Telefon</span>'
               + (f'<a href="tel:{e(tel)}">{e(p["telefon"])}</a>' if tel else e(p["telefon"]))
               + "</div>",
               f'<div class="pp-rand"><span class="et">E-mail</span><a href="mailto:{e(p["email"])}">{e(p["email"])}</a></div>',
               f'<div class="pp-rand"><span class="et">Adresă</span>{e(p["adresa"])}<br>{e(p["oras"])}, jud. {e(p["judet"])}</div>']
    if p.get("persoana"):
        randuri.insert(0, f'<div class="pp-rand"><span class="et">Persoană de contact</span>{e(p["persoana"])}</div>')
    if p.get("website"):
        randuri.append(f'<div class="pp-rand"><span class="et">Site</span><a href="{e(p["website"])}" rel="nofollow noopener" target="_blank">{e(p["website"])}</a></div>')

    zone = "".join(
        f'<span class="pt-chip">{e(JUD[c]["nume"])}</span>' for c in p.get("acopera", []) if c in JUD
    )
    sisteme = "".join(
        f'<a class="pt-chip" href="../../{SISTEM_URL[s]}" style="text-decoration:none">{e(s)}</a>'
        if s in SISTEM_URL else f'<span class="pt-chip">{e(s)}</span>'
        for s in p.get("sisteme", [])
    )

    fapte = [(str(p.get("din_anul", "—")), "partener din anul")]
    if p.get("case_livrate"):
        fapte.append((str(p["case_livrate"]), "case livrate în sistem"))
    fapte_html = "".join(
        f'<div class="pp-fapt"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in fapte
    )

    mini = "".join(
        f'<path class="mj{" on" if j["cod"] == p["judet_cod"] else ""}" d="{j["d"]}"/>'
        for j in harta["judete"]
    )

    html = cap(
        f'{p["nume"]} — constructor partener Polistibrick, {p["oras"]}',
        f'{p["firma"]}, constructor partener Polistibrick în {p["oras"]}, judeţul {p["judet"]}. Date de contact şi zona acoperită.',
        "../../", f'parteneri/{p["slug"]}/',
    ) + f"""
<section class="pp-head">
  <div class="container">
    <a class="pp-back" href="../">&larr; Harta constructorilor parteneri</a>
    <h1>{e(p['nume'])}{demo}</h1>
    <p class="lead" style="color:var(--gray);font-size:18px;margin-top:10px">
      {e(p['eticheta'])} &middot; {e(p['oras'])}, jud. {e(p['judet'])}</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="pp-grid">

      <div>
        <div class="pp-block">
          <h2>Despre constructor</h2>
          <p>{e(p['descriere'])}</p>
        </div>

        <div class="pp-block">
          <div class="pp-fapte">{fapte_html}</div>
        </div>

        <div class="pp-block">
          <h2>Sisteme pe care le montează</h2>
          <div class="pp-zone">{sisteme}</div>
        </div>

        <div class="pp-block">
          <h2>Județe acoperite</h2>
          <div class="pp-zone">{zone}</div>
        </div>

        <div class="pp-block">
          <h2>Cine răspunde de ce</h2>
          <p>Polistibrick e producătorul sistemului: fabricăm și livrăm kitul pe șantier.
            Construcția o execută {e(p['nume'])}, cu contract direct între tine și el.
            Pentru preț de kit și termen de livrare, scrie-ne pe
            <a href="../../oferta/" style="color:var(--red);font-weight:600">pagina de ofertă</a>.</p>
        </div>
      </div>

      <aside>
        <div class="pp-contact">
          <h3>Date de contact</h3>
          <div class="sub">{e(p['firma'])}</div>
          {chr(10).join('          ' + r for r in randuri)}
          <svg class="pp-mini" viewBox="0 0 {W} {H}" role="img" aria-label="Poziția pe harta României">
            {mini}
            <circle cx="{p['x']:.1f}" cy="{p['y']:.1f}" r="26" fill="#C8102E" opacity=".18"/>
            <circle cx="{p['x']:.1f}" cy="{p['y']:.1f}" r="11" fill="#C8102E" stroke="#fff" stroke-width="3"/>
          </svg>
          <div class="pp-legal">
            {e(p['firma'])}<br>CUI {e(p['cui'])} &middot; Reg. com. {e(p['reg_com'])}
          </div>
        </div>
      </aside>

    </div>
  </div>
</section>
""" + coada("../../")
    (d / "index.html").write_text(html, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # curăță paginile partenerilor scoși din listă
    slugs = {p["slug"] for p in parteneri}
    for vechi in OUT.iterdir():
        if vechi.is_dir() and vechi.name not in slugs:
            for f in vechi.rglob("*"):
                f.unlink()
            vechi.rmdir()
            print(f"  [scos] {vechi.name}")
    scrie_index()
    for p in parteneri:
        scrie_partener(p)
    print(f"✓ /parteneri/ + {len(parteneri)} pagini de partener")
    if SUPRAPUNERI:
        print(f"ℹ {len(SUPRAPUNERI)} judeţe acoperite de 2+ constructori:")
        for c, s in SUPRAPUNERI.items():
            print(f"    {JUD[c]['nume'] if c in JUD else c}: {', '.join(s)}")
    fara = [j["nume"] for j in harta["judete"]
            if j["cod"] not in CU_PARTENER and j["cod"] not in ACOPERIT]
    if fara:
        print(f"ℹ {len(fara)} judeţe fără niciun constructor: {', '.join(fara)}")
    if ARE_DEMO:
        n = sum(1 for p in parteneri if p.get("demo"))
        print(f"⚠ {n} din {len(parteneri)} sunt DEMONSTRATIVI — de înlocuit cu partenerii reali")


if __name__ == "__main__":
    main()
