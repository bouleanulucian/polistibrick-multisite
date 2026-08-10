#!/usr/bin/env python3
"""
Reface countries/me pornind de la countries/fr.

Vechiul ME era stricat de o traducere automată care a înlocuit litere în
interiorul cuvintelor (an→godina), în tot fişierul: cod, clase, atribute, nume
de fişiere. Aici se ia structura franceză, curată, se redenumesc folderele în
muntenegreană şi se rescriu linkurile interne. Textul rămâne deocamdată în
franceză şi se traduce separat.

  python3 scripts/reface-me-din-fr.py            # arată ce ar face
  python3 scripts/reface-me-din-fr.py --aplica
"""
import json, re, shutil, sys
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent
FR = RADACINA / "countries" / "fr"
ME = RADACINA / "countries" / "me"
APLICA = "--aplica" in sys.argv

# folder francez -> folder muntenegrean (numele vechi ME, păstrate pentru URL-uri)
HARTA = {
    "a-propos": "o-nama", "brevet": "patent", "certifications": "sertifikati",
    "fondateur": "osnivac", "usines": "fabrike",
    "devenir-partenaire": "postani-partner", "devis": "ponuda",
    "economies": "ustede", "montage": "montaza",
    "conditions": "uslovi", "confidentialite": "privatnost", "cookies": "kolacici",
    "durabilite": "odrzivost", "mentions-legales": "pravne-napomene",
    "pour": "za", "architectes": "arhitekti", "constructeurs": "gradjevinci",
    "investisseurs": "investitori", "proprietaires": "vlasnici",
    "produits": "proizvodi", "murs-mbk": "zidovi-mbk", "planchers-pbk": "podovi-pbk",
    "toit-tbk": "krov-tbk", "toit-tbk-sip250": "krov-tbk-sip250",
    "projets": "projekti", "ressources": "resursi", "temoignages": "svjedocanstva",
}

config_vechi = json.loads((ME / "_config.json").read_text(encoding="utf-8")) if (ME / "_config.json").exists() else None
if config_vechi is None:
    sys.exit("! nu găsesc countries/me/_config.json — nu pornesc fără el")

print("  păstrez configuraţia: %s, %s, %s" %
      (config_vechi.get("lang"), config_vechi.get("country_name"), config_vechi.get("domain_url")))

if not APLICA:
    print("\n  ar şterge  countries/me (%d pagini)" % len(list(ME.rglob("*.html"))))
    print("  ar copia   countries/fr (%d pagini)" % len(list(FR.rglob("*.html"))))
    print("  ar redenumi %d foldere" % len(HARTA))
    print("\n  (probă — rulează cu --aplica)")
    sys.exit(0)

# ── 1. şterg vechiul ME şi copiez FR ────────────────────────────────────────
shutil.rmtree(ME)
shutil.copytree(FR, ME, ignore=shutil.ignore_patterns("images"))
print("  copiat FR → ME")

# ── 2. redenumesc folderele, de la cele adânci spre rădăcină ────────────────
redenumite = 0
for d in sorted((p for p in ME.rglob("*") if p.is_dir()),
                key=lambda p: -len(p.parts)):
    nou = HARTA.get(d.name)
    if nou and nou != d.name:
        d.rename(d.parent / nou); redenumite += 1
print("  redenumit %d foldere" % redenumite)

# ── 3. rescriu linkurile interne ────────────────────────────────────────────
# doar segmente întregi de cale, ancorate pe ghilimea sau pe /
TIPARE = [(re.compile(r'(?<=["\'/])%s(?=[/"\'])' % re.escape(fr)), me)
          for fr, me in sorted(HARTA.items(), key=lambda x: -len(x[0]))]

atinse = 0
for f in ME.rglob("*.html"):
    t = f.read_text(encoding="utf-8")
    nou = t
    for tipar, inloc in TIPARE:
        nou = tipar.sub(inloc, nou)
    if nou != t:
        f.write_text(nou, encoding="utf-8"); atinse += 1
print("  linkuri interne rescrise în %d pagini" % atinse)

# ── 4. pun configuraţia ţării la loc ────────────────────────────────────────
(ME / "_config.json").write_text(
    json.dumps(config_vechi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("  configuraţia Muntenegrului pusă la loc")

# ── 5. control ──────────────────────────────────────────────────────────────
stricate = sum(len(re.findall(r'[A-Za-z]godina|godina[A-Za-z]', f.read_text(encoding="utf-8")))
               for f in ME.rglob("*.html"))
franceze = sum(len(re.findall(r'["\'/](?:%s)[/"\']' % "|".join(map(re.escape, HARTA)), f.read_text(encoding="utf-8")))
               for f in ME.rglob("*.html"))
print("\n  pagini      : %d" % len(list(ME.rglob("*.html"))))
print("  cuvinte stricate rămase : %d" % stricate)
print("  linkuri franceze rămase : %d" % franceze)
