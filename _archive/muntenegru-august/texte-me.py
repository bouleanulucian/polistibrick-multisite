#!/usr/bin/env python3
"""
Scoate din countries/me textele care se văd, ca să fie traduse, şi le pune la loc.

  python3 scripts/texte-me.py scoate   > /tmp/me-texte.json
  python3 scripts/texte-me.py pune     < /tmp/me-traduse.json

Se ating doar: textul dintre tag-uri, şi atributele alt, title, placeholder,
aria-label, content de pe meta description/og. Codul, clasele, căile şi
scripturile rămân neatinse.
"""
import json, re, sys
from pathlib import Path
from html import unescape

ME = Path(__file__).resolve().parent.parent / "countries" / "me"

SARI_TAG = re.compile(r'<(script|style|svg)\b.*?</\1>', re.S | re.I)
TEXT     = re.compile(r'>([^<>]+)<')
ATRIBUTE = re.compile(r'\b(alt|title|placeholder|aria-label)\s*=\s*"([^"]*)"', re.I)
META     = re.compile(r'<meta\s+(?:name|property)="(?:description|og:title|og:description|twitter:title|twitter:description)"\s+content="([^"]*)"', re.I)
TITLU    = re.compile(r'<title>([^<]*)</title>', re.I)

def merita(s):
    s = s.strip()
    if len(s) < 2: return False
    if not re.search(r'[A-Za-zÀ-ÿ]{2}', s): return False          # trebuie litere
    if re.fullmatch(r'[\d\s.,;:%°€–—+×/-]+', s): return False      # doar cifre şi semne
    if re.match(r'^[a-z-]+:[^ ]', s): return False                 # arată a cod
    return True

def bucati(text):
    """textele traductibile, cu poziţiile lor, sărind peste script/style/svg"""
    zone_sarite = [(m.start(), m.end()) for m in SARI_TAG.finditer(text)]
    def in_zona_sarita(p):
        return any(a <= p < b for a, b in zone_sarite)
    out = []
    for m in TEXT.finditer(text):
        if in_zona_sarita(m.start()): continue
        s = m.group(1)
        if merita(s): out.append((m.start(1), m.end(1), s))
    for m in ATRIBUTE.finditer(text):
        if in_zona_sarita(m.start()): continue
        if merita(m.group(2)): out.append((m.start(2), m.end(2), m.group(2)))
    for rx in (META, TITLU):
        for m in rx.finditer(text):
            if merita(m.group(1)): out.append((m.start(1), m.end(1), m.group(1)))
    return sorted(set(out))

if len(sys.argv) < 2 or sys.argv[1] not in ("scoate", "pune"):
    sys.exit(__doc__)

if sys.argv[1] == "scoate":
    unice = {}
    for f in sorted(ME.rglob("*.html")):
        for _, _, s in bucati(f.read_text(encoding="utf-8")):
            cheie = s.strip()
            unice.setdefault(cheie, 0)
            unice[cheie] += 1
    lista = sorted(unice.items(), key=lambda x: -x[1])
    json.dump([{"fr": k, "n": v} for k, v in lista], sys.stdout, ensure_ascii=False, indent=1)
    print("", file=sys.stderr)
    print("  %d texte unice, %d apariţii" % (len(lista), sum(unice.values())), file=sys.stderr)

else:
    perechi = {d["fr"]: d["me"] for d in json.load(sys.stdin) if d.get("me")}
    print("  %d traduceri primite" % len(perechi), file=sys.stderr)
    schimbate = 0
    for f in sorted(ME.rglob("*.html")):
        t = f.read_text(encoding="utf-8")
        buc = bucati(t)
        nou, cursor, out = t, 0, []
        for a, b, s in sorted(buc):
            tr = perechi.get(s.strip())
            if not tr: continue
            out.append(t[cursor:a]); out.append(s.replace(s.strip(), tr)); cursor = b
        if out:
            out.append(t[cursor:])
            f.write_text("".join(out), encoding="utf-8"); schimbate += 1
    print("  aplicat în %d pagini" % schimbate, file=sys.stderr)
