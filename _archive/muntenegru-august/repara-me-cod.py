#!/usr/bin/env python3
"""
Repară identificatorii tehnici stricaţi în countries/me/.

O traducere automată a înlocuit «an» cu «godina» în tot fişierul, inclusiv în
cod, şi s-a aplicat de două ori (panneau → pgodinaneau → pgodingodinaeau).
Aici se repară DOAR ce e cod: atribute HTML, proprietăţi CSS, clase, ancore,
nume de fişiere. Textul muntenegrean nu se atinge — acolo trebuie retradus.

  python3 scripts/repara-me-cod.py            # arată ce ar schimba
  python3 scripts/repara-me-cod.py --aplica   # scrie
"""
import re, sys
from pathlib import Path

ME = Path(__file__).resolve().parent.parent / "countries" / "me"
APLICA = "--aplica" in sys.argv

# perechi sigure: stânga e cod stricat, dreapta e forma corectă
REPARATII = [
    # atribute şi proprietăţi
    ("aria-expgodinaded", "aria-expanded"),
    ("trgodinasform",     "transform"),
    ("trgodinaslate",     "translate"),
    ("sgodinas-serif",    "sans-serif"),
    ("Sgodinas-serif",    "Sans-serif"),
    ("data-pgodinael",    "data-panel"),
    ("pgodinael-",        "panel-"),
    ("-pgodinael",        "-panel"),
    ("#pgodinael",        "#panel"),
    ("text-godinachor",   "text-anchor"),
    ("cta-bgodinad",      "cta-band"),
    ("stgodinadard",      "standard"),
    ("performgodinace",   "performance"),
    ("compgodinay",       "company"),
    ("mgodinager",        "manager"),
    ("lgodinag",          "lang"),
    ("blgodinak",         "blank"),
    ("demgodinade",       "demande"),
    ("isolgodinat",       "isolant"),
    ("chgodinatier",      "chantier"),
    ("plgodinacher",      "plancher"),
    ("pgodingodinaeau",   "panneau"),
    ("pgodingodinaeaux",  "panneaux"),
    ("pgodinaneau",       "panneau"),
    # nume de fişiere
    ("godinaatomy",       "anatomy"),
    ("sataway",           "cutaway"),
    ("mbk-oplata-v",      "mbk-cofraj-v"),
    ("mbk-zid-v",         "mbk-perete-v"),
    ("polistiwall-oplata-v", "polistiwall-cofraj-v"),
    ("polistiwall-zid-v",    "polistiwall-perete-v"),
    ("zid-polistisip-v",     "perete-polistisip-v"),
    ("presenšta",         "presence"),
    ("mersary-home",      "mercury-home"),
    ("mersary-perf",      "mercury-perf"),
    ("mersary-style",     "mercury-style"),
    ("stage1-oplata",     "stage1-cofraj"),
    ("stage3-plgodinaseu","stage3-planseu"),
    ("plgodinaseu",       "planseu"),
    ("-oplata.jpg",       "-cofraj.jpg"),
]
# ordonez descrescător după lungime, ca formele lungi să prindă înaintea celor scurte
REPARATII.sort(key=lambda p: -len(p[0]))

total, fisiere = 0, 0
for f in sorted(ME.rglob("*.html")):
    t = f.read_text(encoding="utf-8")
    nou, aici = t, 0
    for vechi, bun in REPARATII:
        if vechi == bun: continue
        n = nou.count(vechi)
        if n:
            nou = nou.replace(vechi, bun); aici += n
    if aici:
        fisiere += 1; total += aici
        print("  %-46s %3d reparaţii" % (str(f.relative_to(ME.parent.parent)), aici))
        if APLICA: f.write_text(nou, encoding="utf-8")

print("\n  %d reparaţii în %d fişiere" % (total, fisiere))
if not APLICA:
    print("  (probă — rulează cu --aplica ca să scrie)")
else:
    ramase = sum(len(re.findall(r'[A-Za-z-]godina|godina[A-Za-z-]', f.read_text(encoding="utf-8")))
                 for f in ME.rglob("*.html"))
    print("  cuvinte încă lipite de «godina»: %d (text muntenegrean, se retraduce)" % ramase)
