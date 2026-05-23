#!/usr/bin/env python3
"""
Polistibrick translation script — Romanian → 6 target languages.

Mechanically translates user-visible text in HTML files using a comprehensive
glossary. Preserves HTML structure, CSS, JS, placeholders, product codes.

Usage:
    python3 translations/translate.py en      # translate to English
    python3 translations/translate.py en fr it es nl de   # all 6
    python3 translations/translate.py all     # alias for all 6

What it does:
1. Reads each HTML file in countries/{lang}/
2. Skips <style>...</style>, <script>...</script>, and HTML comments
3. Replaces Romanian phrases with target-language equivalents (longest match wins)
4. Updates `lang="ro"` → `lang="{target}"`
5. Updates <title> and <meta description>
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = ROOT / "countries"

# ============================================================
# TRANSLATIONS — keyed by Romanian source phrase
# Longest phrases first (auto-sorted in apply step)
# ============================================================

T = {
    # ============= TAGLINES & HERO =============
    "O casă. Un sistem.": {
        "en": "One house. One system.",
        "fr": "Une maison. Un système.",
        "it": "Una casa. Un sistema.",
        "es": "Una casa. Un sistema.",
        "nl": "Eén huis. Eén systeem.",
        "de": "Ein Haus. Ein System.",
    },
    "Fără compromis. Fără facturi.": {
        "en": "No compromise. No bills.",
        "fr": "Sans compromis. Sans factures.",
        "it": "Senza compromessi. Senza bollette.",
        "es": "Sin compromisos. Sin facturas.",
        "nl": "Geen compromis. Geen rekeningen.",
        "de": "Kein Kompromiss. Keine Rechnungen.",
    },
    "Nu doar casă pasivă.": {
        "en": "Not just a passive house.",
        "fr": "Pas seulement une maison passive.",
        "it": "Non solo una casa passiva.",
        "es": "No solo una casa pasiva.",
        "nl": "Niet alleen een passiefhuis.",
        "de": "Nicht nur ein Passivhaus.",
    },
    "Casă premium fără facturi.": {
        "en": "Premium home, no bills.",
        "fr": "Maison premium, sans factures.",
        "it": "Casa premium, senza bollette.",
        "es": "Casa premium, sin facturas.",
        "nl": "Premium huis, geen rekeningen.",
        "de": "Premium-Haus, keine Rechnungen.",
    },

    # ============= NAVIGATION =============
    "Produse": {"en": "Products", "fr": "Produits", "it": "Prodotti", "es": "Productos", "nl": "Producten", "de": "Produkte"},
    "Pereți MBK": {"en": "MBK Walls", "fr": "Murs MBK", "it": "Pareti MBK", "es": "Muros MBK", "nl": "MBK Muren", "de": "MBK Wände"},
    "Planșee PBK": {"en": "PBK Floors", "fr": "Planchers PBK", "it": "Solai PBK", "es": "Forjados PBK", "nl": "PBK Vloeren", "de": "PBK Decken"},
    "Acoperiș TBK": {"en": "TBK Roof", "fr": "Toit TBK", "it": "Tetto TBK", "es": "Tejado TBK", "nl": "TBK Dak", "de": "TBK Dach"},
    "Accesorii": {"en": "Accessories", "fr": "Accessoires", "it": "Accessori", "es": "Accesorios", "nl": "Accessoires", "de": "Zubehör"},
    "Soluții": {"en": "Solutions", "fr": "Solutions", "it": "Soluzioni", "es": "Soluciones", "nl": "Oplossingen", "de": "Lösungen"},
    "Pentru proprietari": {"en": "For Homeowners", "fr": "Pour propriétaires", "it": "Per proprietari", "es": "Para propietarios", "nl": "Voor eigenaren", "de": "Für Eigentümer"},
    "Pentru arhitecți": {"en": "For Architects", "fr": "Pour architectes", "it": "Per architetti", "es": "Para arquitectos", "nl": "Voor architecten", "de": "Für Architekten"},
    "Pentru constructori": {"en": "For Builders", "fr": "Pour constructeurs", "it": "Per costruttori", "es": "Para constructores", "nl": "Voor bouwers", "de": "Für Bauunternehmer"},
    "Pentru investitori": {"en": "For Investors", "fr": "Pour investisseurs", "it": "Per investitori", "es": "Para inversores", "nl": "Voor investeerders", "de": "Für Investoren"},
    "→ Devino partener": {"en": "→ Become a partner", "fr": "→ Devenez partenaire", "it": "→ Diventa partner", "es": "→ Hazte socio", "nl": "→ Word partner", "de": "→ Partner werden"},
    "Devino partener": {"en": "Become a partner", "fr": "Devenez partenaire", "it": "Diventa partner", "es": "Hazte socio", "nl": "Word partner", "de": "Partner werden"},
    "Proiecte": {"en": "Projects", "fr": "Projets", "it": "Progetti", "es": "Proyectos", "nl": "Projecten", "de": "Projekte"},
    "Case construite": {"en": "Completed homes", "fr": "Maisons construites", "it": "Case costruite", "es": "Casas construidas", "nl": "Gebouwde huizen", "de": "Gebaute Häuser"},
    "Testimoniale (video)": {"en": "Testimonials (video)", "fr": "Témoignages (vidéo)", "it": "Testimonianze (video)", "es": "Testimonios (vídeo)", "nl": "Getuigenissen (video)", "de": "Erfahrungsberichte (Video)"},
    "Testimoniale": {"en": "Testimonials", "fr": "Témoignages", "it": "Testimonianze", "es": "Testimonios", "nl": "Getuigenissen", "de": "Erfahrungsberichte"},
    "Calculator": {"en": "Calculator", "fr": "Calculateur", "it": "Calcolatore", "es": "Calculadora", "nl": "Calculator", "de": "Rechner"},
    "Calculator cost": {"en": "Cost calculator", "fr": "Calculateur de coût", "it": "Calcolatore costi", "es": "Calculadora de costes", "nl": "Kostencalculator", "de": "Kostenrechner"},
    "Calculator economii (vs cărămidă)": {"en": "Savings calculator (vs brick)", "fr": "Calculateur d'économies (vs brique)", "it": "Calcolatore di risparmi (vs mattone)", "es": "Calculadora de ahorros (vs ladrillo)", "nl": "Besparingscalculator (vs baksteen)", "de": "Sparrechner (vs Ziegel)"},
    "Resurse": {"en": "Resources", "fr": "Ressources", "it": "Risorse", "es": "Recursos", "nl": "Bronnen", "de": "Ressourcen"},
    "Blog": {"en": "Blog", "fr": "Blog", "it": "Blog", "es": "Blog", "nl": "Blog", "de": "Blog"},
    "Întrebări frecvente": {"en": "FAQ", "fr": "FAQ", "it": "FAQ", "es": "FAQ", "nl": "FAQ", "de": "FAQ"},
    "Comparație vs cărămidă": {"en": "Comparison vs brick", "fr": "Comparaison vs brique", "it": "Confronto con il mattone", "es": "Comparación con ladrillo", "nl": "Vergelijking met baksteen", "de": "Vergleich mit Ziegel"},
    "Despre": {"en": "About", "fr": "À propos", "it": "Su di noi", "es": "Acerca de", "nl": "Over ons", "de": "Über uns"},
    "Compania": {"en": "The company", "fr": "L'entreprise", "it": "L'azienda", "es": "La empresa", "nl": "Het bedrijf", "de": "Das Unternehmen"},
    "Patent": {"en": "Patent", "fr": "Brevet", "it": "Brevetto", "es": "Patente", "nl": "Octrooi", "de": "Patent"},
    "Certificări": {"en": "Certifications", "fr": "Certifications", "it": "Certificazioni", "es": "Certificaciones", "nl": "Certificeringen", "de": "Zertifikate"},
    "Fabrici": {"en": "Factories", "fr": "Usines", "it": "Fabbriche", "es": "Fábricas", "nl": "Fabrieken", "de": "Werke"},
    "Echipa": {"en": "Team", "fr": "Équipe", "it": "Squadra", "es": "Equipo", "nl": "Team", "de": "Team"},
    "Contact": {"en": "Contact", "fr": "Contact", "it": "Contatti", "es": "Contacto", "nl": "Contact", "de": "Kontakt"},

    # ============= CTAs =============
    "Cere o ofertă →": {"en": "Request a quote →", "fr": "Demander un devis →", "it": "Richiedi un preventivo →", "es": "Pide un presupuesto →", "nl": "Vraag een offerte aan →", "de": "Angebot anfordern →"},
    "Cere o ofertă": {"en": "Request a quote", "fr": "Demander un devis", "it": "Richiedi un preventivo", "es": "Pide un presupuesto", "nl": "Vraag een offerte aan", "de": "Angebot anfordern"},
    "Calculează costul casei": {"en": "Calculate house cost", "fr": "Calculer le coût de la maison", "it": "Calcola il costo della casa", "es": "Calcula el coste de la casa", "nl": "Bereken huiskosten", "de": "Hauskosten berechnen"},
    "Cere o ofertă personalizată": {"en": "Request a personalized quote", "fr": "Demander un devis personnalisé", "it": "Richiedi un preventivo personalizzato", "es": "Pide un presupuesto personalizado", "nl": "Vraag een persoonlijke offerte aan", "de": "Individuelles Angebot anfordern"},
    "Cere ofertă personalizată": {"en": "Request a personalized quote", "fr": "Demander un devis personnalisé", "it": "Richiedi un preventivo personalizzato", "es": "Pide un presupuesto personalizado", "nl": "Vraag een persoonlijke offerte aan", "de": "Individuelles Angebot anfordern"},
    "Vorbește cu un specialist": {"en": "Talk to a specialist", "fr": "Parler à un spécialiste", "it": "Parla con uno specialista", "es": "Habla con un especialista", "nl": "Spreek met een specialist", "de": "Mit einem Spezialisten sprechen"},
    "Vorbește cu noi": {"en": "Talk to us", "fr": "Parlez-nous", "it": "Parla con noi", "es": "Habla con nosotros", "nl": "Praat met ons", "de": "Mit uns sprechen"},
    "Vezi proiectele construite": {"en": "See completed projects", "fr": "Voir les projets construits", "it": "Vedi i progetti costruiti", "es": "Ver los proyectos construidos", "nl": "Bekijk gebouwde projecten", "de": "Gebaute Projekte ansehen"},
    "Vezi case construite": {"en": "See completed homes", "fr": "Voir maisons construites", "it": "Vedi case costruite", "es": "Ver casas construidas", "nl": "Bekijk gebouwde huizen", "de": "Gebaute Häuser ansehen"},
    "Vezi comparația completă": {"en": "See the full comparison", "fr": "Voir la comparaison complète", "it": "Vedi il confronto completo", "es": "Ver la comparación completa", "nl": "Bekijk de volledige vergelijking", "de": "Vollständigen Vergleich ansehen"},
    "Vezi mai mult": {"en": "See more", "fr": "Voir plus", "it": "Vedi di più", "es": "Ver más", "nl": "Bekijk meer", "de": "Mehr ansehen"},
    "Citește mai mult": {"en": "Read more", "fr": "Lire la suite", "it": "Leggi di più", "es": "Leer más", "nl": "Lees meer", "de": "Weiterlesen"},
    "Aflați mai mult": {"en": "Learn more", "fr": "En savoir plus", "it": "Scopri di più", "es": "Más información", "nl": "Meer informatie", "de": "Mehr erfahren"},
    "Află mai multe": {"en": "Learn more", "fr": "En savoir plus", "it": "Scopri di più", "es": "Más información", "nl": "Meer informatie", "de": "Mehr erfahren"},

    # ============= SECTIONS & HEADINGS =============
    "Construiește cu noi": {"en": "BUILD WITH US", "fr": "CONSTRUIRE AVEC NOUS", "it": "COSTRUISCI CON NOI", "es": "CONSTRUYE CON NOSOTROS", "nl": "BOUW MET ONS", "de": "MIT UNS BAUEN"},
    "CONSTRUIEȘTE CU NOI": {"en": "BUILD WITH US", "fr": "CONSTRUIRE AVEC NOUS", "it": "COSTRUISCI CON NOI", "es": "CONSTRUYE CON NOSOTROS", "nl": "BOUW MET ONS", "de": "MIT UNS BAUEN"},
    "Hai să construim": {"en": "Let's build", "fr": "Construisons", "it": "Costruiamo", "es": "Construyamos", "nl": "Laten we bouwen", "de": "Lass uns bauen"},
    "casa ta din viitor.": {"en": "your home of the future.", "fr": "votre maison du futur.", "it": "la tua casa del futuro.", "es": "tu casa del futuro.", "nl": "jouw huis van de toekomst.", "de": "dein Haus der Zukunft."},
    "Spune-ne despre proiectul tău. Îți pregătim o ofertă personalizată în 48 de ore — fără obligații.": {
        "en": "Tell us about your project. We'll prepare a personalized quote within 48 hours — no obligations.",
        "fr": "Parlez-nous de votre projet. Nous vous préparons un devis personnalisé sous 48 heures — sans engagement.",
        "it": "Raccontaci del tuo progetto. Ti prepariamo un preventivo personalizzato entro 48 ore — senza impegno.",
        "es": "Cuéntanos sobre tu proyecto. Te preparamos un presupuesto personalizado en 48 horas — sin compromiso.",
        "nl": "Vertel ons over je project. We bereiden binnen 48 uur een persoonlijke offerte voor — vrijblijvend.",
        "de": "Erzähl uns von deinem Projekt. Wir bereiten innerhalb von 48 Stunden ein individuelles Angebot vor — unverbindlich.",
    },

    # ============= TIME UNITS =============
    "săptămâni": {"en": "weeks", "fr": "semaines", "it": "settimane", "es": "semanas", "nl": "weken", "de": "Wochen"},
    "săptămână": {"en": "week", "fr": "semaine", "it": "settimana", "es": "semana", "nl": "week", "de": "Woche"},
    "luni": {"en": "months", "fr": "mois", "it": "mesi", "es": "meses", "nl": "maanden", "de": "Monate"},
    "lună": {"en": "month", "fr": "mois", "it": "mese", "es": "mes", "nl": "maand", "de": "Monat"},
    "ani": {"en": "years", "fr": "ans", "it": "anni", "es": "años", "nl": "jaar", "de": "Jahre"},
    "an": {"en": "year", "fr": "an", "it": "anno", "es": "año", "nl": "jaar", "de": "Jahr"},
    "zile": {"en": "days", "fr": "jours", "it": "giorni", "es": "días", "nl": "dagen", "de": "Tage"},
    "zi": {"en": "day", "fr": "jour", "it": "giorno", "es": "día", "nl": "dag", "de": "Tag"},
    "ore": {"en": "hours", "fr": "heures", "it": "ore", "es": "horas", "nl": "uren", "de": "Stunden"},
    "iarna": {"en": "winter", "fr": "hiver", "it": "inverno", "es": "invierno", "nl": "winter", "de": "Winter"},
    "vara": {"en": "summer", "fr": "été", "it": "estate", "es": "verano", "nl": "zomer", "de": "Sommer"},

    # ============= TECHNICAL CONSTRUCTION =============
    "sistem brevetat ICF complet": {"en": "complete patented ICF system", "fr": "système ICF complet breveté", "it": "sistema ICF completo brevettato", "es": "sistema ICF completo patentado", "nl": "compleet gepatenteerd ICF-systeem", "de": "vollständiges patentiertes ICF-System"},
    "Sistem brevetat ICF complet": {"en": "Complete patented ICF system", "fr": "Système ICF complet breveté", "it": "Sistema ICF completo brevettato", "es": "Sistema ICF completo patentado", "nl": "Compleet gepatenteerd ICF-systeem", "de": "Vollständiges patentiertes ICF-System"},
    "sistem brevetat european": {"en": "European patented system", "fr": "système breveté européen", "it": "sistema brevettato europeo", "es": "sistema patentado europeo", "nl": "Europees gepatenteerd systeem", "de": "europäisches patentiertes System"},
    "Sistem brevetat european · ICF": {"en": "European patented system · ICF", "fr": "Système breveté européen · ICF", "it": "Sistema brevettato europeo · ICF", "es": "Sistema patentado europeo · ICF", "nl": "Europees gepatenteerd systeem · ICF", "de": "Europäisches patentiertes System · ICF"},
    "Sistem brevetat ICF cu panouri de 3 m": {"en": "Patented ICF system with 3 m panels", "fr": "Système ICF breveté avec panneaux de 3 m", "it": "Sistema ICF brevettato con pannelli da 3 m", "es": "Sistema ICF patentado con paneles de 3 m", "nl": "Gepatenteerd ICF-systeem met 3 m panelen", "de": "Patentiertes ICF-System mit 3 m Paneelen"},
    "5 produse premium într-un singur panou": {"en": "5 premium products in a single panel", "fr": "5 produits premium dans un seul panneau", "it": "5 prodotti premium in un singolo pannello", "es": "5 productos premium en un solo panel", "nl": "5 premium producten in één paneel", "de": "5 Premium-Produkte in einem einzigen Paneel"},
    "izolație": {"en": "insulation", "fr": "isolation", "it": "isolamento", "es": "aislamiento", "nl": "isolatie", "de": "Dämmung"},
    "rezistență la foc A1": {"en": "A1 fire resistance", "fr": "résistance au feu A1", "it": "resistenza al fuoco A1", "es": "resistencia al fuego A1", "nl": "brandweerstand A1", "de": "Feuerwiderstand A1"},
    "antiseismic": {"en": "seismic-resistant", "fr": "parasismique", "it": "antisismico", "es": "antisísmico", "nl": "aardbevingsbestendig", "de": "erdbebensicher"},
    "hidrofug": {"en": "waterproof", "fr": "hydrofuge", "it": "impermeabile", "es": "impermeable", "nl": "waterdicht", "de": "wasserdicht"},
    "acustic": {"en": "acoustic", "fr": "acoustique", "it": "acustico", "es": "acústico", "nl": "akoestisch", "de": "akustisch"},
    "Vara fără AC, iarna fără centrală.": {"en": "Summer without AC, winter without boiler.", "fr": "L'été sans clim, l'hiver sans chaudière.", "it": "Estate senza aria condizionata, inverno senza caldaia.", "es": "Verano sin aire acondicionado, invierno sin caldera.", "nl": "Zomer zonder airco, winter zonder cv-ketel.", "de": "Sommer ohne Klimaanlage, Winter ohne Heizung."},
    "Construit în 4 săptămâni.": {"en": "Built in 4 weeks.", "fr": "Construit en 4 semaines.", "it": "Costruito in 4 settimane.", "es": "Construido en 4 semanas.", "nl": "Gebouwd in 4 weken.", "de": "In 4 Wochen gebaut."},
    "Standard A+++": {"en": "A+++ standard", "fr": "standard A+++", "it": "standard A+++", "es": "estándar A+++", "nl": "A+++ standaard", "de": "A+++ Standard"},
    "casă pasivă": {"en": "passive house", "fr": "maison passive", "it": "casa passiva", "es": "casa pasiva", "nl": "passiefhuis", "de": "Passivhaus"},
    "Casă pasivă": {"en": "Passive house", "fr": "Maison passive", "it": "Casa passiva", "es": "Casa pasiva", "nl": "Passiefhuis", "de": "Passivhaus"},
    "casa pasivă": {"en": "passive house", "fr": "maison passive", "it": "casa passiva", "es": "casa pasiva", "nl": "passiefhuis", "de": "Passivhaus"},
    "casă premium": {"en": "premium home", "fr": "maison premium", "it": "casa premium", "es": "casa premium", "nl": "premium huis", "de": "Premium-Haus"},
    "Casa premium": {"en": "Premium home", "fr": "Maison premium", "it": "Casa premium", "es": "Casa premium", "nl": "Premium huis", "de": "Premium-Haus"},

    # Core nouns
    "pereți": {"en": "walls", "fr": "murs", "it": "pareti", "es": "muros", "nl": "muren", "de": "Wände"},
    "planșee": {"en": "floors", "fr": "planchers", "it": "solai", "es": "forjados", "nl": "vloeren", "de": "Decken"},
    "acoperiș": {"en": "roof", "fr": "toit", "it": "tetto", "es": "tejado", "nl": "dak", "de": "Dach"},
    "cărămidă": {"en": "brick", "fr": "brique", "it": "mattone", "es": "ladrillo", "nl": "baksteen", "de": "Ziegel"},
    "Cărămidă": {"en": "Brick", "fr": "Brique", "it": "Mattone", "es": "Ladrillo", "nl": "Baksteen", "de": "Ziegel"},
    "BCA": {"en": "AAC block", "fr": "béton cellulaire", "it": "blocchi AAC", "es": "bloque AAC", "nl": "AAC-blok", "de": "Porenbeton"},
    "beton": {"en": "concrete", "fr": "béton", "it": "calcestruzzo", "es": "hormigón", "nl": "beton", "de": "Beton"},
    "Beton": {"en": "Concrete", "fr": "Béton", "it": "Calcestruzzo", "es": "Hormigón", "nl": "Beton", "de": "Beton"},
    "fier-beton": {"en": "rebar", "fr": "armature acier", "it": "tondino", "es": "acero de refuerzo", "nl": "wapeningsstaal", "de": "Bewehrungsstahl"},
    "Fier-beton": {"en": "Rebar", "fr": "Armature acier", "it": "Tondino", "es": "Acero de refuerzo", "nl": "Wapeningsstaal", "de": "Bewehrungsstahl"},
    "cofraj": {"en": "formwork", "fr": "coffrage", "it": "cassero", "es": "encofrado", "nl": "bekisting", "de": "Schalung"},
    "Cofraj": {"en": "Formwork", "fr": "Coffrage", "it": "Cassero", "es": "Encofrado", "nl": "Bekisting", "de": "Schalung"},
    "polistiren": {"en": "polystyrene", "fr": "polystyrène", "it": "polistirene", "es": "poliestireno", "nl": "polystyreen", "de": "Polystyrol"},
    "facturi": {"en": "bills", "fr": "factures", "it": "bollette", "es": "facturas", "nl": "rekeningen", "de": "Rechnungen"},
    "factură": {"en": "bill", "fr": "facture", "it": "bolletta", "es": "factura", "nl": "rekening", "de": "Rechnung"},
    "fără facturi": {"en": "no bills", "fr": "sans factures", "it": "senza bollette", "es": "sin facturas", "nl": "geen rekeningen", "de": "keine Rechnungen"},
    "Fără facturi": {"en": "No bills", "fr": "Sans factures", "it": "Senza bollette", "es": "Sin facturas", "nl": "Geen rekeningen", "de": "Keine Rechnungen"},
    "fără compromis": {"en": "no compromise", "fr": "sans compromis", "it": "senza compromessi", "es": "sin compromisos", "nl": "geen compromis", "de": "kein Kompromiss"},
    "Fără compromis": {"en": "No compromise", "fr": "Sans compromis", "it": "Senza compromessi", "es": "Sin compromisos", "nl": "Geen compromis", "de": "Kein Kompromiss"},

    # Heating / energy
    "centrală termică": {"en": "boiler", "fr": "chaudière", "it": "caldaia", "es": "caldera", "nl": "cv-ketel", "de": "Heizkessel"},
    "centrală": {"en": "boiler", "fr": "chaudière", "it": "caldaia", "es": "caldera", "nl": "cv-ketel", "de": "Heizkessel"},
    "încălzire": {"en": "heating", "fr": "chauffage", "it": "riscaldamento", "es": "calefacción", "nl": "verwarming", "de": "Heizung"},

    # ============= COMMON UI STRINGS =============
    "Trei oameni diferiți, aceeași casă perfectă.": {"en": "Three different people, the same perfect house.", "fr": "Trois personnes différentes, la même maison parfaite.", "it": "Tre persone diverse, la stessa casa perfetta.", "es": "Tres personas diferentes, la misma casa perfecta.", "nl": "Drie verschillende mensen, hetzelfde perfecte huis.", "de": "Drei verschiedene Menschen, das gleiche perfekte Haus."},
    "PENTRU CINE ESTE POLISTIBRICK": {"en": "WHO IS POLISTIBRICK FOR", "fr": "POUR QUI EST POLISTIBRICK", "it": "PER CHI È POLISTIBRICK", "es": "PARA QUIÉN ES POLISTIBRICK", "nl": "VOOR WIE IS POLISTIBRICK", "de": "FÜR WEN IST POLISTIBRICK"},
    "Pentru cine este Polistibrick": {"en": "Who is Polistibrick for", "fr": "Pour qui est Polistibrick", "it": "Per chi è Polistibrick", "es": "Para quién es Polistibrick", "nl": "Voor wie is Polistibrick", "de": "Für wen ist Polistibrick"},
    "Polistibrick rezolvă probleme diferite pentru fiecare. Alege-ți rolul ca să vezi ce primești concret.": {
        "en": "Polistibrick solves different problems for everyone. Choose your role to see what you get specifically.",
        "fr": "Polistibrick résout des problèmes différents pour chacun. Choisissez votre rôle pour voir ce que vous obtenez concrètement.",
        "it": "Polistibrick risolve problemi diversi per ognuno. Scegli il tuo ruolo per vedere cosa ottieni concretamente.",
        "es": "Polistibrick resuelve problemas diferentes para cada uno. Elige tu rol para ver qué obtienes concretamente.",
        "nl": "Polistibrick lost verschillende problemen op voor iedereen. Kies je rol om te zien wat je concreet krijgt.",
        "de": "Polistibrick löst unterschiedliche Probleme für jeden. Wählen Sie Ihre Rolle, um zu sehen, was Sie konkret bekommen.",
    },
    "PROPRIETAR": {"en": "OWNER", "fr": "PROPRIÉTAIRE", "it": "PROPRIETARIO", "es": "PROPIETARIO", "nl": "EIGENAAR", "de": "EIGENTÜMER"},
    "ARHITECT · INGINER": {"en": "ARCHITECT · ENGINEER", "fr": "ARCHITECTE · INGÉNIEUR", "it": "ARCHITETTO · INGEGNERE", "es": "ARQUITECTO · INGENIERO", "nl": "ARCHITECT · INGENIEUR", "de": "ARCHITEKT · INGENIEUR"},
    "DEZVOLTATOR": {"en": "DEVELOPER", "fr": "PROMOTEUR", "it": "SVILUPPATORE", "es": "PROMOTOR", "nl": "ONTWIKKELAAR", "de": "BAUTRÄGER"},

    # ============= FOOTER =============
    "Toate drepturile rezervate.": {"en": "All rights reserved.", "fr": "Tous droits réservés.", "it": "Tutti i diritti riservati.", "es": "Todos los derechos reservados.", "nl": "Alle rechten voorbehouden.", "de": "Alle Rechte vorbehalten."},
    "Politica de confidențialitate": {"en": "Privacy Policy", "fr": "Politique de confidentialité", "it": "Privacy", "es": "Política de privacidad", "nl": "Privacybeleid", "de": "Datenschutz"},
    "Cookies": {"en": "Cookies", "fr": "Cookies", "it": "Cookie", "es": "Cookies", "nl": "Cookies", "de": "Cookies"},
    "Termeni și condiții": {"en": "Terms & conditions", "fr": "Conditions générales", "it": "Termini e condizioni", "es": "Términos y condiciones", "nl": "Algemene voorwaarden", "de": "AGB"},
    "Sustenabilitate": {"en": "Sustainability", "fr": "Durabilité", "it": "Sostenibilità", "es": "Sostenibilidad", "nl": "Duurzaamheid", "de": "Nachhaltigkeit"},

    # ============= POPULAR PHRASES =============
    "premium": {"en": "premium", "fr": "premium", "it": "premium", "es": "premium", "nl": "premium", "de": "Premium"},
    "Premium": {"en": "Premium", "fr": "Premium", "it": "Premium", "es": "Premium", "nl": "Premium", "de": "Premium"},
    "complet": {"en": "complete", "fr": "complet", "it": "completo", "es": "completo", "nl": "compleet", "de": "vollständig"},
    "completă": {"en": "complete", "fr": "complète", "it": "completa", "es": "completa", "nl": "compleet", "de": "vollständig"},
    "Complet": {"en": "Complete", "fr": "Complet", "it": "Completo", "es": "Completo", "nl": "Compleet", "de": "Vollständig"},
    "Completă": {"en": "Complete", "fr": "Complète", "it": "Completa", "es": "Completa", "nl": "Compleet", "de": "Vollständig"},
    "construcție": {"en": "construction", "fr": "construction", "it": "costruzione", "es": "construcción", "nl": "bouw", "de": "Bau"},
    "construit": {"en": "built", "fr": "construit", "it": "costruito", "es": "construido", "nl": "gebouwd", "de": "gebaut"},
    "Construit": {"en": "Built", "fr": "Construit", "it": "Costruito", "es": "Construido", "nl": "Gebouwd", "de": "Gebaut"},
    "casă": {"en": "house", "fr": "maison", "it": "casa", "es": "casa", "nl": "huis", "de": "Haus"},
    "Casă": {"en": "House", "fr": "Maison", "it": "Casa", "es": "Casa", "nl": "Huis", "de": "Haus"},
    "Casa": {"en": "The House", "fr": "La Maison", "it": "La Casa", "es": "La Casa", "nl": "Het Huis", "de": "Das Haus"},
    "viitor": {"en": "future", "fr": "futur", "it": "futuro", "es": "futuro", "nl": "toekomst", "de": "Zukunft"},
    "Viitor": {"en": "Future", "fr": "Futur", "it": "Futuro", "es": "Futuro", "nl": "Toekomst", "de": "Zukunft"},
    "Bun venit în viitor": {"en": "Welcome to the future", "fr": "Bienvenue dans le futur", "it": "Benvenuto nel futuro", "es": "Bienvenido al futuro", "nl": "Welkom in de toekomst", "de": "Willkommen in der Zukunft"},

    # ============= LEGAL & GLOBAL =============
    "Sistemul ICF care construiește case mai eficiente, mai rapide și mai sustenabile. Fabricat în UE.": {
        "en": "The ICF system that builds homes that are more efficient, faster, and more sustainable. Made in the EU.",
        "fr": "Le système ICF qui construit des maisons plus efficaces, plus rapides et plus durables. Fabriqué en UE.",
        "it": "Il sistema ICF che costruisce case più efficienti, più veloci e più sostenibili. Prodotto in UE.",
        "es": "El sistema ICF que construye casas más eficientes, más rápidas y más sostenibles. Fabricado en la UE.",
        "nl": "Het ICF-systeem dat huizen efficiënter, sneller en duurzamer bouwt. Gemaakt in de EU.",
        "de": "Das ICF-System, das effizientere, schnellere und nachhaltigere Häuser baut. Hergestellt in der EU.",
    },
    "Made with ⚒ in Europe": {"en": "Made with ⚒ in Europe", "fr": "Fabriqué avec ⚒ en Europe", "it": "Realizzato con ⚒ in Europa", "es": "Hecho con ⚒ en Europa", "nl": "Gemaakt met ⚒ in Europa", "de": "Gefertigt mit ⚒ in Europa"},
}


# ============================================================
# Apply translations safely (skip script/style/comments)
# ============================================================

# Matches <script>...</script>, <style>...</style>, <!-- ... -->
SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

def apply_translations(text: str, target_lang: str) -> str:
    """Replace Romanian phrases with target-language equivalents.
    Process only the segments OUTSIDE script/style/comments.
    Longest phrases first. Short single-word entries use word boundaries
    to avoid matching inside other words (e.g. 'an' inside 'lang')."""

    # Sort translations longest-first
    sorted_keys = sorted(T.keys(), key=len, reverse=True)

    # Pre-compile regexes for short words that need word boundaries
    word_re = {}
    for ro in sorted_keys:
        # Only single words shorter than 12 chars without spaces need boundaries
        if " " not in ro and len(ro) < 12:
            # Use Unicode word boundaries (\b doesn't work great with non-ASCII)
            word_re[ro] = re.compile(
                r"(?<![\wÀ-ſ])" + re.escape(ro) + r"(?![\wÀ-ſ])"
            )

    # Split into [non-skip, skip, non-skip, skip, ...] segments
    segments = []
    last_end = 0
    for m in SKIP_REGEX.finditer(text):
        segments.append(("translate", text[last_end:m.start()]))
        segments.append(("skip", m.group(0)))
        last_end = m.end()
    segments.append(("translate", text[last_end:]))

    out = []
    for kind, segment in segments:
        if kind == "skip":
            out.append(segment)
            continue
        for ro in sorted_keys:
            tr = T[ro].get(target_lang)
            if not tr:
                continue
            if ro in word_re:
                # Use regex with word boundary
                segment = word_re[ro].sub(tr, segment)
            else:
                # Long phrase / multi-word — plain replace is safe
                segment = segment.replace(ro, tr)
        out.append(segment)

    return "".join(out)


def update_lang_attr(text: str, target_lang: str) -> str:
    """<html lang="ro"> → <html lang="{target}">"""
    return re.sub(r'<html\s+lang="ro"', f'<html lang="{target_lang}"', text, flags=re.IGNORECASE)


def translate_file(file_path: Path, target_lang: str):
    """Read, translate, write back."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ✗ {file_path.relative_to(ROOT)}: read error: {e}")
        return False

    new = update_lang_attr(content, target_lang)
    new = apply_translations(new, target_lang)

    if new == content:
        print(f"  · {file_path.relative_to(ROOT)}: no changes")
        return True

    file_path.write_text(new, encoding="utf-8")
    print(f"  ✓ {file_path.relative_to(ROOT)}")
    return True


def translate_country(lang: str):
    print(f"\n=== Translating {lang.upper()} ===")
    country_dir = COUNTRIES_DIR / lang
    if not country_dir.exists():
        print(f"  ✗ Country folder not found: {country_dir}")
        return
    html_files = list(country_dir.rglob("*.html"))
    print(f"  Files: {len(html_files)}")
    for f in html_files:
        translate_file(f, lang)


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 translations/translate.py <lang> [lang ...] | all")
        print("Langs: en fr it es nl de")
        sys.exit(1)
    if args == ["all"]:
        args = ["en", "fr", "it", "es", "nl", "de"]
    for lang in args:
        if lang not in {"en", "fr", "it", "es", "nl", "de"}:
            print(f"  Skipping unknown language: {lang}")
            continue
        translate_country(lang)
    print("\n✓ Done.\n")


if __name__ == "__main__":
    main()
