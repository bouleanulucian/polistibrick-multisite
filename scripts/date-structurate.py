#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pune date structurate (JSON-LD) pe fiecare pagină.

Google şi motoarele cu AI citesc blocurile astea ca să înţeleagă ce e pe pagină
şi ca să te citeze. Fără ele, o pagină e doar text.

Se scrie în sursă, cu {{domain_url}} şi celelalte variabile, ca schema să urmeze
singură configuraţia fiecărei ţări. Nu se inventează nimic: totul iese din ce e
deja pe pagină (titlu, descriere, întrebări, adresă din _config.json).

  python3 scripts/date-structurate.py ro          # arată ce ar pune
  python3 scripts/date-structurate.py ro --aplica
  python3 scripts/date-structurate.py --toate --aplica
"""
import json, re, sys
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent
APLICA = "--aplica" in sys.argv
TOATE = "--toate" in sys.argv
CERUTE = [a for a in sys.argv[1:] if not a.startswith("--")]

MARCA = "<!-- date-structurate -->"

# ── recunosc tipul paginii după numele folderului, în toate limbile ──────────
FELURI = {
    "contact":  {"contact", "kontakt", "contatti"},
    "faq":      {"faq"},
    "fabrici":  {"fabrici", "usines", "factories", "fabricas", "fabbriche", "fabrike"},
    "fondator": {"echipa", "fondateur", "founder", "fondatore", "fundador", "osnivac"},
    "proiecte": {"proiecte", "projets", "projects", "progetti", "proyectos", "projekti"},
    "case":     {"case", "maisons", "houses", "casas", "kuce", "modele"},
    "oferta":   {"oferta", "devis", "quote", "preventivo", "presupuesto", "ponuda"},
}
PRODUSE = {"produse", "produits", "products", "prodotti", "productos", "proizvodi"}


def fel_de_pagina(rel: Path) -> str:
    parti = list(rel.parts)
    if rel.name == "index.html" and len(parti) == 1:
        return "prima"
    folder = parti[-2] if len(parti) >= 2 else ""
    for fel, nume in FELURI.items():
        if folder in nume:
            return fel
    if any(p in PRODUSE for p in parti):
        return "produs" if len(parti) >= 3 else "lista-produse"
    return "pagina"


def curata(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<")
          .replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"'))
    return re.sub(r"\s+", " ", s).strip()


def titlu(t: str) -> str:
    m = re.search(r"<title>([^<]*)</title>", t, re.I)
    if not m:
        return ""
    return re.split(r"\s*[·|—]\s*", curata(m.group(1)))[0].strip()


def descriere(t: str) -> str:
    m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', t, re.I)
    return curata(m.group(1)) if m else ""


def intrebari(t: str):
    out = []
    for d in re.findall(r"<details\b.*?</details>", t, re.S | re.I):
        q = re.search(r"<summary[^>]*>(.*?)</summary>", d, re.S | re.I)
        if not q:
            continue
        corp = re.sub(r"<summary[^>]*>.*?</summary>", "", d, flags=re.S | re.I)
        a = curata(corp)
        if q and a and len(a) > 20:
            out.append((curata(q.group(1)), a[:1200]))
    return out


def firimituri(rel: Path, t: str):
    """calea paginii, ca lanţ, pentru bara de navigare din rezultatele Google"""
    parti = [p for p in rel.parts[:-1]]
    lista = [{"@type": "ListItem", "position": 1, "name": "{{country_name}}",
              "item": "{{domain_url}}/"}]
    drum = ""
    for i, p in enumerate(parti, start=2):
        drum += p + "/"
        lista.append({"@type": "ListItem", "position": i,
                      "name": p.replace("-", " ").capitalize(),
                      "item": "{{domain_url}}/" + drum})
    if len(lista) > 1:
        lista[-1]["name"] = titlu(t) or lista[-1]["name"]
    return lista


def organizatia():
    return {
        "@type": "Organization",
        "@id": "{{domain_url}}/#organizatie",
        "name": "{{company.name_legal}}",
        "alternateName": "Polistibrick",
        "url": "{{domain_url}}/",
        "logo": "{{domain_url}}/images/logo.png",
        "telephone": "{{contact.phone}}",
        "email": "{{contact.email_general}}",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "{{company.address_street}}",
            "addressLocality": "{{company.address_city}}",
            "postalCode": "{{company.address_zip}}",
            "addressCountry": "{{country}}",
        },
        "sameAs": ["{{contact.social.facebook}}", "{{contact.social.instagram}}",
                   "{{contact.social.linkedin}}"],
    }


def construieste(rel: Path, t: str, fel: str):
    url = "{{domain_url}}/" + ("" if fel == "prima" else str(rel.parent).replace("\\", "/") + "/")
    nod_pagina = {
        "@type": "WebPage",
        "@id": url + "#pagina",
        "url": url,
        "name": titlu(t),
        "inLanguage": "{{lang}}",
        "isPartOf": {"@id": "{{domain_url}}/#site"},
        "publisher": {"@id": "{{domain_url}}/#organizatie"},
    }
    d = descriere(t)
    if d:
        nod_pagina["description"] = d

    graf = [nod_pagina]
    fir = firimituri(rel, t)
    if len(fir) > 1:
        graf.append({"@type": "BreadcrumbList", "itemListElement": fir})

    if fel == "prima":
        graf.append(organizatia())
        graf.append({"@type": "WebSite", "@id": "{{domain_url}}/#site",
                     "url": "{{domain_url}}/", "name": "Polistibrick",
                     "inLanguage": "{{lang}}",
                     "publisher": {"@id": "{{domain_url}}/#organizatie"}})
    if fel == "contact":
        graf[0]["@type"] = ["WebPage", "ContactPage"]
        graf.append(organizatia())
    if fel == "faq":
        qa = intrebari(t)
        if qa:
            graf.append({"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]})
    if fel == "fondator":
        graf.append({"@type": "Person", "name": "Lucian Bouleanu",
                     "jobTitle": "Fondator", "worksFor": {"@id": "{{domain_url}}/#organizatie"}})
    return {"@context": "https://schema.org", "@graph": graf}


def lucreaza(tara: str):
    rad = RADACINA / "countries" / tara
    puse = sarite = 0
    for f in sorted(rad.rglob("*.html")):
        rel = f.relative_to(rad)
        t = f.read_text(encoding="utf-8")
        if MARCA in t:
            t = re.sub(re.escape(MARCA) + r".*?</script>", "", t, flags=re.S)
        if "application/ld+json" in t or "</head>" not in t or len(t) < 3000:
            sarite += 1
            continue
        fel = fel_de_pagina(rel)
        d = construieste(rel, t, fel)
        if len(d["@graph"]) < 2 and fel == "pagina":
            pass
        bloc = (MARCA + '\n<script type="application/ld+json">\n'
                + json.dumps(d, ensure_ascii=False, indent=1) + "\n</script>\n")
        nou = t.replace("</head>", bloc + "</head>", 1)
        puse += 1
        print("  %-42s %-12s %d noduri" % (str(rel)[:42], fel, len(d["@graph"])))
        if APLICA:
            f.write_text(nou, encoding="utf-8")
    print("  → %s: %d pagini cu schemă nouă, %d sărite (aveau deja sau prea mici)" % (tara, puse, sarite))


tari = [p.name for p in sorted((RADACINA / "countries").iterdir()) if p.is_dir()] if TOATE else CERUTE
for t in tari:
    lucreaza(t)
if not APLICA:
    print("\n  (probă — rulează cu --aplica)")
