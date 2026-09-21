"""Faptele care nu se schimbă de la o pagină la alta — o singură sursă de adevăr.

De ce există: la auditul din 17.09.2026, llms.txt (scris de mână) zicea 11 modele de case
când site-ul avea 24, iar prețul pieței „la cheie" apărea în 4 variante pe 4 pagini.
Un AI care citește site-ul vede 4 răspunsuri la aceeași întrebare și nu citează niciunul.

Regula: aici intră DOAR cifre care există deja pe o pagină publicată a site-ului, cu pagina
sursă notată. Nimic nu se inventează aici; dacă o cifră se schimbă, se schimbă întâi pagina,
apoi rândul de aici, apoi build-ul verifică (check_fapte) că cele două spun același lucru.

Ce vine din _config.json, NU de aici: firma, CUI, J, adresa, telefon, email, rețele.
"""

FAPTE = {
    "ro": {
        # ── entitatea: ce avea deja blocul Organization de pe prima pagină (12.08) ──────
        "organization": {
            "alternateName": ["Grup Polistibrick", "Polistibrick", "Polisti"],
            "description": ("Grup Polistibrick este producătorul românesc care fabrică, lângă Balș (jud. Olt), "
                            "cele trei sisteme constructive: Polistibrick (cofraj izolant din beton armat, "
                            "brevet EP 4372168 B1), Polistiwall și PolistiSIP (structură din lemn)."),
        },

        # ── proprietate intelectuală ──────────────────────────────────── /despre/patent/
        "brevet": {
            "numar": "EP 4372168 B1",
            "acordat": "2025-10-15",
            "titular": "Lucian-Cristian Bouleanu",
            "url": "https://worldwide.espacenet.com/patent/search?q=pn%3DEP4372168",
            "pagina": "despre/patent/",
        },
        "marci": [
            {"numar": "018936693", "clase": "19",
             "url": "https://euipo.europa.eu/eSearch/#details/trademarks/018936693"},
            {"numar": "019311167", "clase": "35, 37",
             "url": "https://euipo.europa.eu/eSearch/#details/trademarks/019311167"},
        ],

        # ── certificări: exact ce afirmă pagina ─────────────────────── /despre/certificari/
        # (ISO 14001 și 45001 puse pe pagină la cererea patronului, 17.09.2026)
        "certificari": [
            "Marcaj CE — declarație de conformitate CPR 305/2011/UE",
            "Evaluare Tehnică Europeană (ETA), referință EAD 040287-00-1201, EOTA",
            "ISO 9001:2015 — managementul calității în producție",
            "ISO 14001:2015 — management de mediu",
            "ISO 45001:2018 — securitate și sănătate în muncă",
            "Standard Passivhaus — validare de componentă, U 0,10–0,13 W/m²K",
            "Reacție la foc Euroclasa A1 (EN 13501-1) — placare din fibrociment",
        ],

        # ── sistemele: U și compoziția, din paginile de produs ───────────────────────
        "sisteme": {
            "Polistibrick": {"U": "0,10–0,14", "perete_cm": "38–47",
                             "compozitie": "fibrociment pe ambele fețe, EPS grafitat, beton armat turnat în cofraj",
                             "pagina": "produse/polistibrick/"},
            # două grosimi, două U-uri: pagina le scrie separat, nu ca interval → U_text pentru afișare,
            # U rămâne pentru verificare (check_fapte cere fiecare capăt pe pagină)
            "Polistiwall":  {"U": "0,12–0,15", "U_text": "0,15 (Wall 200) / 0,12 (Wall 250)", "perete_cm": "35–40",
                             "compozitie": "izolație EPS 20 sau 25 cm doar la exterior, fața interioară rămâne beton",
                             "pagina": "produse/polistiwall/"},
            "PolistiSIP":   {"U": "0,11", "perete_cm": "30",
                             "compozitie": "panou sandwich OSB/3 + EPS grafitat 27 cm + I-Joist STEICO, fără beton turnat",
                             "pagina": "produse/polistisip/"},
        },

        # ── prețuri publicate, august 2026, fără TVA ──────────────────────── /preturi/
        "preturi": {
            "luna": "august 2026",
            "cofraj": {"Polistibrick": "197–281", "Polistiwall": "153–204", "PolistiSIP": "201–242"},
            "la_gri": {"Polistibrick": "690–810", "Polistiwall": "640–720", "PolistiSIP": "590–640"},
            "la_cheie_polistibrick": "950–1.280",   # case reale, șantiere Polistibrick
            "pagina": "preturi/",
        },

        # ── piața românească, la cheie, casă clasică: UN singur interval pe tot site-ul
        # Canonic = pagina dedicată costurilor. Ghidurile publice 2026 (Brig.ro, Wolf
        # Construct) dau 1.250–1.650 pentru standard: se citează ca plafonul prudent.
        "piata": {
            "la_cheie": "900–1.350",
            "la_cheie_prudent": "1.250–1.650",
            "la_rosu": "450–700",
            "surse": [
                {"nume": "Brig.ro — ghid prețuri case la cheie 2026",
                 "url": "https://brig.ro/blog/ghid-complet-2026-cat-costa-constructia-unei-case-la-cheie-in-romania"},
                {"nume": "Wolf Construct — cât costă să construiești o casă în 2026",
                 "url": "https://wolfconstruct.ro/blogs/constructii-case-structura-metalica-proiecte-case/cat-costa-sa-construiesti-o-casa-in-2026"},
            ],
            "pagina": "resurse/cat-costa-o-casa/",
        },

        # ── consum: cifrele folosite pe /economii/ și în ghiduri ─────────────────────
        "consum_kwh": {"polistibrick": "25–45", "caramida_neizolata": "100–180", "pasiv_max": "15"},
    }
}


FAPTE["fr"] = {
    # ── Franța, site B2B (21.09.2026). Aceleași reguli: doar cifre care există pe pagina numită.
    "organization": {
        "alternateName": ["Polistibrick", "Polistibrick France"],
        "description": ("Polistibrick fabrique un bloc coffrant isolant à parement fibre-ciment (EPS graphité, "
                        "béton armé coulé sur chantier), livré en kit sur le plan de la maison, pour les entreprises "
                        "de construction. Brevet européen EP 4372168 B1."),
    },
    "brevet": {"numar": "EP 4372168 B1", "acordat": "2025-10-15", "titular": "Lucian-Cristian Bouleanu",
               "url": "https://worldwide.espacenet.com/patent/search?q=pn%3DEP4372168", "pagina": "a-propos/brevet/"},
    "marci": [
        {"numar": "018936693", "clase": "19", "url": "https://euipo.europa.eu/eSearch/#details/trademarks/018936693"},
        {"numar": "019311167", "clase": "35, 37", "url": "https://euipo.europa.eu/eSearch/#details/trademarks/019311167"},
    ],
    # exact ce afirmă /a-propos/certifications/ (ISO 14001/45001 puse pe pagină la cererea patronului)
    "certificari": ["Marquage CE", "ISO 9001", "ISO 14001", "ISO 45001",
                    "Réaction au feu Euroclasse A1 (EN 13501-1) du parement fibre-ciment"],
    "sisteme": {
        "Polistibrick": {"U": "0,10–0,14", "perete_cm": "38–47",
                         "compozitie": "parement fibre-ciment sur les deux faces, EPS graphité, béton armé coulé dans le coffrage",
                         "pagina": "produits/polistibrick/"},
        "Polistiwall":  {"U": "0,12–0,15", "U_text": "0,15 (Wall 200) / 0,12 (Wall 250)", "perete_cm": "35–40",
                         "compozitie": "isolation EPS de 20 ou 25 cm à l'extérieur seulement, face intérieure béton",
                         "pagina": "produits/polistiwall/"},
        "PolistiSIP":   {"U": "0,11", "perete_cm": "30",
                         "compozitie": "panneau sandwich OSB/3 + EPS graphité + I-Joist STEICO, sans béton coulé",
                         "pagina": "produits/polistisip/"},
    },
    "preturi": {"luna": "août 2026",
                "cofraj": {"Polistibrick": "205–280", "Polistiwall": "157–205", "PolistiSIP": "229–287"},
                "la_gri": {}, "la_cheie_polistibrick": "", "pagina": "prix/"},
    "livrare": "30 à 45 jours après commande confirmée",
    "formare": "2 à 3 jours sur votre premier chantier, avec un spécialiste Polistibrick",
    # reperul pieței franceze: clé en main 1 700–2 200 (EPTB 2024: 1 914 €/m²), hors d'eau hors d'air 1 000–1 400
    "piata": {"la_cheie": "1 700–2 200", "la_cheie_prudent": "", "la_rosu": "1 000–1 400",
              "surse": [{"nume": "EPTB/SDES 2024, ministère de la Transition écologique — 1 914 €/m² en moyenne",
                         "url": "https://www.statistiques.developpement-durable.gouv.fr/le-prix-des-terrains-et-du-bati-pour-les-maisons-individuelles-en-2024"},
                        {"nume": "Renovbox 2026, hors d'eau hors d'air",
                         "url": "https://renovbox.fr/prix/construction-maison/hors-d-eau-hors-d-air/"}],
              "pagina": "ressources/re2020/"},
    "consum_kwh": {"polistibrick": "25–45", "caramida_neizolata": "100–180", "pasiv_max": "15"},
}


def fapte(tara: str) -> dict:
    """Faptele unei țări; țările fără intrare proprie nu primesc nimic (nu se moștenește:
    prețurile și piața diferă de la o țară la alta)."""
    return FAPTE.get(tara, {})
