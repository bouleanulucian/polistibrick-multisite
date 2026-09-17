# polisti.ro citibil de AI — plan (17.09.2026, ramura `ai-citibil-ro`)

Spec: `docs/superpowers/specs/2026-09-17-ai-citibil-ro-design.md`

## Audit
- [x] Build-ul: canonical/hreflang injectate, sitemap cu lastmod din git, robots cu boți AI — există
- [x] JSON-LD: inline pe 36 pagini; Organization în 3 variante (31 golite)
- [x] llms.txt static, rămas în urmă (zicea 11 modele; site-ul are 48)
- [x] 13 pagini-țintă: 3 deschideau răspuns-întâi, 10 nu
- [x] Prețul pieței „la cheie": 4 variante → canonic 900–1 350 + surse numite
- [x] Rapoartele agenților: schema (narrow) integrat; GEO și tehnic au expirat înainte de raport (limită de pași) — auditul făcut de mână

## Instalație (build/)
- [x] `build/fapte.py` — faptele + social în `_config.json` (3 URL-uri verificate)
- [x] Organization canonic injectat + `dateModified` din git + `inLanguage` + `og:locale` + WebPage minim unde lipsea
- [x] Generator `llms.txt` + `llms-full.txt`; ștergere `countries/ro/llms.txt`
- [x] `check_fapte` + `check_organization` în build (au prins 2 probleme reale la prima rulare)
- [x] `scripts/test-citibil.py` — testul „10 întrebări", ÎNAINTE/DUPĂ
- [x] `.gitignore`: excepții pentru `build/citibil.py` și `build/fapte.py` (altfel CI nu le-ar fi avut)

## Conținut (countries/ro/)
- [x] Bloc răspuns-întâi pe 11 pagini; dată + sursă pe 2 (`scripts/raspuns-intai-ro.py`, cu plasă: orice cifră trebuie să existe deja pe site)
- [x] Alinierea celor 3 pagini cu prețul pieței divergent
- [x] Subsol: firmă, CUI, J, adresă, telefon în text (șablon comun + prima pagină); U pe cardul Polistibrick de pe prima pagină
- [ ] Emailul în text — lăsat ASCUNS intenționat (site-ul îl codifică b64 contra spam); e în JSON-LD și llms.txt — decizia patronului

## Verificare
- [x] Build verde (toate check-urile), 43 blocuri JSON-LD parsabile
- [x] Testul „10 întrebări": citabile 2 → 13 din 14; Organization complet 1 → 14; dateModified 7 → 14
- [x] Previzualizare locală: blocul (poziție, stil), subsolul, cardul, llms.txt 200 text/plain, fără erori în consolă
- [x] Diff citit; nimic publicat (ramură locală, necomisă încă)

## Review — ce s-a adăugat (pentru patron)
- 2 module de build, 2 scripturi, 1 stil `.raspuns`, 1 rând în subsol, 11 blocuri de text, 2 date, 3 alinieri de cifre, 1 U pe prima pagină
- Rămân la patron: emailul în clar da/nu · `priceValidUntil` la prețuri · răspunsul dublat în FAQ-ul de pe /preturi/ · prezența în afara site-ului (GBP, LinkedIn firmă, Wikidata)
