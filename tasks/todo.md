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
- [x] Diff citit; PUBLICAT 17.09.2026, commit a64c6b8, verificat live (llms.txt 48 modele, blocuri, Organization, ISO)

## Review — ce s-a adăugat (pentru patron)
- 2 module de build, 2 scripturi, 1 stil `.raspuns`, 1 rând în subsol, 11 blocuri de text, 2 date, 3 alinieri de cifre, 1 U pe prima pagină
- Rămân la patron: emailul în clar da/nu · `priceValidUntil` la prețuri · răspunsul dublat în FAQ-ul de pe /preturi/ · prezența în afara site-ului (GBP, LinkedIn firmă, Wikidata)

# polistibrick.fr B2B — plan (21.09.2026, ramura `site-fr-b2b`, NEPUBLICAT)

Spec: `docs/superpowers/specs/2026-09-21-site-fr-b2b-design.md` · Plan: `docs/superpowers/plans/2026-09-21-site-fr-b2b.md`

- [x] T1 plase: `scripts/amprente.sh` (amprenta celor 8 țări), `scripts/verif-fr.py` (cuvinte interzise, 48 URL-uri vechi, placeholder-e)
- [x] T2 build: meniu/subsol pe țară (`countries/<cod>/_nav.html`, `_footer.html`), activ doar dacă fișierul există
- [x] T3 meniu FR: Le système · Prix · Chantier · Votre assureur · Références · Partenaire · Contact + «Chiffrer mon plan»
- [x] T4 `build/fapte.py` FR, llms.txt în franceză, testul de citibilitate pe FR, ISO 14001/45001 pe certificări
- [x] T5 structură: 5 mutări, 16 ștergeri, 21 redirecturi 301; 35 pagini în loc de 49
- [x] T6 acasă: aceeași grafică, vocea firmei care pune (73 înlocuiri de text)
- [x] T7 `/systeme/` + 3 fișe produs cu răspuns-întâi
- [x] T8 `/prix/` (răspuns-întâi, reperul EPTB), `/projets/` (48 case, carduri pe un rând)
- [x] T9 `/chantier/`: livrare, echipă, 4 pași, gaine, formarea 2–3 zile
- [x] T10 `/assureur/`: dosarul, fără ATEx/Avis Technique/technique courante
- [x] T11 `/references/`: MBK, CS BTP, Sainte-Hilaire — video + citate din transcrieri
- [x] T12 partener (condițiile §5, mărturia falsă ștearsă), contact, devis, `/vous-faites-construire/`
- [x] T13 ressources doar pro (ICF → bloc coffrant isolant, FAQ 20→17), à propos
- [x] T14 verificare: build verde · verif-fr ✓ · 10/13 citabile · amprente identice (RO byte-identic cu main) · JSON-LD parsabil · previzualizare 1440/390

## Review
- Nepublicat: la «publică» → merge `site-fr-b2b` în `main`, push (publică doar ro, neschimbat), apoi `gh workflow run cloudflare-pages.yml --ref main -f country=fr`.
- Rămân la patron: condițiile de partener FR (propunere PDG), prețurile din `/projets/` vs grila `/prix/`, certificatul Passivhaus / ETE când există.

## Validat de patron, 21.09.2026 seara — «bun, gata, asta așa rămâne»
- Meniu: Le système · Produits ▸ (3 fișe) · Références · Le brevet · Certifications · Les usines · Partenaire · Prix · Chantier · Votre assureur · Questions fréquentes · Le fondateur · Contact
- Subsol: 4 coloane complete (+ Toit TBK, Chiffrer mon plan, Vous faites construire ?, Le fondateur)
- Acasă: cardurile Maçonnerie/ITE și bilanțul în vocea firmei; «5 avantages premium, directement de l'usine»; carusel 6,5 s; «Deux usines en Europe. Livré sur chantier.»; adresa 4 Rue Hans List; buton Contactez-nous
- Contact: Franța prima, fără detecție IP · /systeme/ și /prix/ fără dubluri · /references/ video portret
- Deschis: /chantier/ (cifrele patronului) · publicarea (la comanda lui)
