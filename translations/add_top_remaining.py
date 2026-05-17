#!/usr/bin/env python3
"""
Add direct translations for the top recurring Romanian phrases
that survived the first two passes. These are short phrases I can
translate manually with confidence.
"""
import json
from pathlib import Path

OUT_DIR = Path("/Users/polistibrick/Desktop/polistibrick-multisite/translations")

# Format: { "RO_phrase": { "en":..., "fr":..., "it":..., "es":..., "nl":..., "de":... } }
TOP = {
    "Perete finit 5 în 1": {
        "en": "Finished wall 5-in-1",
        "fr": "Mur fini 5 en 1",
        "it": "Muro finito 5 in 1",
        "es": "Muro acabado 5 en 1",
        "nl": "Afgewerkte muur 5-in-1",
        "de": "Fertige Wand 5-in-1",
    },
    "Polistibrick e structura, tu alegi aspectul": {
        "en": "Polistibrick is the structure, you choose the look",
        "fr": "Polistibrick est la structure, vous choisissez l'apparence",
        "it": "Polistibrick è la struttura, tu scegli l'aspetto",
        "es": "Polistibrick es la estructura, tú eliges el aspecto",
        "nl": "Polistibrick is de structuur, jij kiest het uiterlijk",
        "de": "Polistibrick ist die Struktur, Sie wählen das Aussehen",
    },
    "Premium integrat": {
        "en": "Integrated premium",
        "fr": "Premium intégré",
        "it": "Premium integrato",
        "es": "Premium integrado",
        "nl": "Geïntegreerd premium",
        "de": "Integriertes Premium",
    },
    "Premium accesibil": {
        "en": "Accessible premium",
        "fr": "Premium accessible",
        "it": "Premium accessibile",
        "es": "Premium accesible",
        "nl": "Toegankelijk premium",
        "de": "Zugängliches Premium",
    },
    "Un sistem protejat european": {
        "en": "A European protected system",
        "fr": "Un système protégé européen",
        "it": "Un sistema protetto europeo",
        "es": "Un sistema protegido europeo",
        "nl": "Een Europees beschermd systeem",
        "de": "Ein europäisch geschütztes System",
    },
    "Sistem principal folosit acum": {
        "en": "Main system used today",
        "fr": "Système principal utilisé aujourd'hui",
        "it": "Sistema principale usato oggi",
        "es": "Sistema principal usado hoy",
        "nl": "Belangrijkste systeem dat nu wordt gebruikt",
        "de": "Heute hauptsächlich verwendetes System",
    },
    "De ce aleg dezvoltatorii": {
        "en": "Why developers choose",
        "fr": "Pourquoi les développeurs choisissent",
        "it": "Perché gli sviluppatori scelgono",
        "es": "Por qué los desarrolladores eligen",
        "nl": "Waarom ontwikkelaars kiezen",
        "de": "Warum Entwickler wählen",
    },
    "Sistem flexibil": {
        "en": "Flexible system",
        "fr": "Système flexible",
        "it": "Sistema flessibile",
        "es": "Sistema flexible",
        "nl": "Flexibel systeem",
        "de": "Flexibles System",
    },
    "Sistem MBK 270 + PBK 250 + TBK": {
        "en": "System MBK 270 + PBK 250 + TBK",
        "fr": "Système MBK 270 + PBK 250 + TBK",
        "it": "Sistema MBK 270 + PBK 250 + TBK",
        "es": "Sistema MBK 270 + PBK 250 + TBK",
        "nl": "Systeem MBK 270 + PBK 250 + TBK",
        "de": "System MBK 270 + PBK 250 + TBK",
    },
    "Trei produse premium": {
        "en": "Three premium products",
        "fr": "Trois produits premium",
        "it": "Tre prodotti premium",
        "es": "Tres productos premium",
        "nl": "Drie premium producten",
        "de": "Drei Premium-Produkte",
    },
    "Construire premium": {
        "en": "Premium building",
        "fr": "Construction premium",
        "it": "Costruzione premium",
        "es": "Construcción premium",
        "nl": "Premium bouwen",
        "de": "Premium-Bauweise",
    },
    "Polistibrick in cifre": {
        "en": "Polistibrick in numbers",
        "fr": "Polistibrick en chiffres",
        "it": "Polistibrick in cifre",
        "es": "Polistibrick en cifras",
        "nl": "Polistibrick in cijfers",
        "de": "Polistibrick in Zahlen",
    },
    "O casa completa": {
        "en": "A complete house",
        "fr": "Une maison complète",
        "it": "Una casa completa",
        "es": "Una casa completa",
        "nl": "Een compleet huis",
        "de": "Ein komplettes Haus",
    },
    "Fără isolation suplimentară": {
        "en": "No additional insulation",
        "fr": "Sans isolation supplémentaire",
        "it": "Senza isolamento aggiuntivo",
        "es": "Sin aislamiento adicional",
        "nl": "Zonder extra isolatie",
        "de": "Ohne zusätzliche Dämmung",
    },
    "Premium Wide-Span": {
        "en": "Premium Wide-Span",
        "fr": "Premium Grandes Portées",
        "it": "Premium Wide-Span",
        "es": "Premium Wide-Span",
        "nl": "Premium Wide-Span",
        "de": "Premium Wide-Span",
    },
    "1 — Plăcă suport]": {
        "en": "1 — Support board]",
        "fr": "1 — Plaque support]",
        "it": "1 — Lastra di supporto]",
        "es": "1 — Placa de soporte]",
        "nl": "1 — Steunplaat]",
        "de": "1 — Stützplatte]",
    },
    "2 — Montaj echipă]": {
        "en": "2 — Team installation]",
        "fr": "2 — Installation équipe]",
        "it": "2 — Installazione squadra]",
        "es": "2 — Instalación equipo]",
        "nl": "2 — Teamsmontage]",
        "de": "2 — Team-Montage]",
    },
    "4 — Tâmplărie]": {
        "en": "4 — Joinery]",
        "fr": "4 — Menuiserie]",
        "it": "4 — Serramenti]",
        "es": "4 — Carpintería]",
        "nl": "4 — Schrijnwerk]",
        "de": "4 — Schreinerei]",
    },
    "5 — Învelitoare]": {
        "en": "5 — Roofing]",
        "fr": "5 — Couverture]",
        "it": "5 — Copertura]",
        "es": "5 — Cubierta]",
        "nl": "5 — Dakbedekking]",
        "de": "5 — Dacheindeckung]",
    },
    "5 — Pregătire fațadă]": {
        "en": "5 — Façade preparation]",
        "fr": "5 — Préparation façade]",
        "it": "5 — Preparazione facciata]",
        "es": "5 — Preparación fachada]",
        "nl": "5 — Geveldebereiding]",
        "de": "5 — Fassadenvorbereitung]",
    },
    "calculăm exact pentru proiectul tău, pe baza planurilor tale": {
        "en": "we calculate exactly for your project, based on your plans",
        "fr": "nous calculons exactement pour votre projet, sur la base de vos plans",
        "it": "calcoliamo esattamente per il tuo progetto, sulla base dei tuoi piani",
        "es": "calculamos exactamente para tu proyecto, basándonos en tus planos",
        "nl": "wij berekenen precies voor uw project, op basis van uw plannen",
        "de": "wir berechnen genau für Ihr Projekt, basierend auf Ihren Plänen",
    },
}

LANGS = ["en", "fr", "it", "es", "nl", "de"]

for lang in LANGS:
    path = OUT_DIR / f"{lang}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    before = len(data)
    for ro, langs_dict in TOP.items():
        if lang in langs_dict and ro not in data:
            data[ro] = langs_dict[lang]
    after = len(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {lang}: {before} → {after}")
