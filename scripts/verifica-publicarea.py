#!/usr/bin/env python3
"""
Verifică un site publicat: deschide fiecare pagină, adună toate fişierele pe care
le cere (poze, video, 3D, css, js) şi spune care lipsesc şi de unde sunt cerute.

  python3 scripts/verifica-publicarea.py                      # preview GitHub Pages
  python3 scripts/verifica-publicarea.py http://localhost:8902/polistibrick-multisite/
"""
import re, sys, urllib.parse, urllib.request, concurrent.futures as cf
from pathlib import Path

BAZA = sys.argv[1] if len(sys.argv) > 1 else \
    "https://bouleanulucian.github.io/polistibrick-multisite/"
if not BAZA.endswith("/"): BAZA += "/"

# paginile de produs au nume de folder diferite pe fiecare ţară; le citesc din build
RADACINA = Path(__file__).resolve().parent.parent
def pagini(tara):
    cai = [""]
    d = RADACINA / "build" / tara
    for produs in ("polistiwall", "polistisip", "polistibrick"):
        gasit = list(d.glob("*/%s/index.html" % produs)) if d.exists() else []
        cai += [str(g.parent.relative_to(d)) + "/" for g in gasit]
    return cai

TARI = ["ro", "fr", "de", "en", "es", "it", "me", "nl", "ie"]
TIPAR = re.compile(
    r'(?:src|href|poster|content)\s*=\s*"([^"]+)"'
    r'|(?:src|href|poster|content)\s*=\s*\'([^\']+)\''
    r'|"fisier"\s*:\s*"([^"]+)"'
    r'|url\(\s*[\'"]?([^\'")]+)', re.I)
EXT = re.compile(r'\.(png|jpe?g|webp|svg|mp4|webm|glb|gltf|css|js|pdf|ico|woff2?)(\?|$)', re.I)

def stare(url):
    try:
        r = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "verif/1"})
        with urllib.request.urlopen(r, timeout=25) as f: return f.status
    except urllib.error.HTTPError as e: return e.code
    except Exception: return 0

def ia(url):
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "verif/1"})
        with urllib.request.urlopen(r, timeout=30) as f:
            return f.read().decode("utf-8", "replace"), f.status
    except urllib.error.HTTPError as e: return "", e.code
    except Exception: return "", 0

def verifica(tara, cale):
    url = urllib.parse.urljoin(BAZA, tara + "/" + cale)
    html, st = ia(url)
    if st != 200:
        return tara, cale, st, [], 0
    resurse = set()
    for m in TIPAR.finditer(html):
        v = next((g for g in m.groups() if g), None)
        if not v or v.startswith(("http", "//", "data:", "#", "mailto:", "tel:", "javascript:")):
            continue
        if EXT.search(v):
            resurse.add(urllib.parse.urljoin(url, v))
    rupte = []
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for r, s in zip(resurse, ex.map(stare, resurse)):
            if s != 200:
                rupte.append((s, urllib.parse.urlparse(r).path))
    return tara, cale, 200, rupte, len(resurse)

sarcini = [(t, c) for t in TARI for c in pagini(t)]
print("\n  %s\n  %d pagini de verificat\n" % (BAZA, len(sarcini)))
total, pagini_rupte = 0, 0
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for tara, cale, st, rupte, n in sorted(ex.map(lambda a: verifica(*a), sarcini)):
        et = "/%s/%s" % (tara, cale)
        if st != 200:
            print("  ✗ %-38s pagina răspunde %s" % (et, st)); pagini_rupte += 1
        elif rupte:
            print("  ✗ %-38s %d din %d fişiere lipsesc:" % (et, len(rupte), n))
            for s, r in sorted(set(rupte))[:5]: print("        %s  %s" % (s, r))
            total += len(rupte); pagini_rupte += 1
        else:
            print("  ✓ %-38s %d fişiere, toate prezente" % (et, n))
print("\n  %d pagini cu probleme, %d fişiere lipsă" % (pagini_rupte, total))
sys.exit(1 if pagini_rupte else 0)
