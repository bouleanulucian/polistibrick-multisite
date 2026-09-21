# polistibrick.fr — site B2B pentru firma care execută (design, 21.09.2026)

Decis cu patronul pe 21.09.2026 (memorie: `decizii-site-fr-b2b`, cercetarea: `franta-piata-b2b-2026`).
Mandat: „ești PDG Polistibrick France; site-ul vorbește strict cu clientul tău, nu amestecat."

## 1. Clientul (unul)

**Firma de construcții care execută cu echipa ei** — maçonnerie, gros œuvre, entreprise générale;
3–20 oameni; 5–30 de case pe an; lucrează pentru particulari cu arhitect și ca subcontractant al
unui CMI regional. Ea decide sistemul de perete, ea cumpără, ea montează.
Durerea ei, măsurată: >80 000 posturi neocupate în BTP (FFB), zidarii cei mai greu de găsit, 87 %
din firme cu întârzieri pe șantier. Cei trei clienți francezi filmați sunt exact ea: MBK (Montesson,
al 3-lea șantier, „je manque de main-d'œuvre"), CS BTP (prima casă, „avec ou sans expérience"),
Sainte-Hilaire (casă în Paris, „hors d'eau hors d'air en un temps record").

**Nu vorbim cu:** particularul (o singură pagină de predare, în afara meniului), promotorul, CMI-ul
național, autoconstructorul. Arhitectul primește documentele pe pagina „dossier", nu o pagină a lui.

## 2. Promisiunea (ce spunem, o singură dată, peste tot la fel)

| Ce | Cifra | De unde |
|---|---|---|
| Echipa | **3 oameni** montează și toarnă pereții și planșeele unei case de 100 m² **în 3 săptămâni**, fără macara | patronul (100 m² parter, <3 săptămâni); Sainte-Hilaire, MBK |
| Prețul | **grilă publică HT, livrare inclusă**: Polistibrick 205–280 €/m², Polistiwall 157–205, PolistiSIP 229–287 (după suprafață) | `/prix/` FR, deja publicat |
| Peretele | fibrociment pe ambele fețe, EPS grafitat, beton armat; **U 0,10–0,14**; **182 €/m² de mur** contre **329 €/m²** parpaing + ITE + enduits, main-d'œuvre comprise | fișele client FR (Kelyseo, Renovscore 2026) |
| Livrarea | **30 à 45 jours** après commande confirmée, 1–2 camions | patronul, 21.09 |
| Formarea | **2 à 3 jours sur votre premier chantier**, avec un spécialiste Polistibrick | patronul, 04.09 / 09.09 |
| Răspunsul | **24 h**; două căi: are proiect → devis; n-are → proiectul întâi, apoi devis | decizia din 20.09 (RO), aplicată FR |
| Devizul | **chiffrage sur votre plan**, PDF, aplicația (`polistibrick-configurator.vercel.app?pays=FR`) | live din 30.08 |
| Dosarul pentru asigurator | brevet EP 4372168 B1, marcaj CE, ISO 9001/14001/45001, fișe tehnice, DoP, DWG/DXF/Revit | ce există azi |

**Interzise pe site:** ATEx, Avis Technique, DTA, „technique courante" (decizia patronului); „ICF"
(termenul francez e **bloc coffrant isolant / BCI**); „5-en-1" ca slogan (e al lui Isolabloc — spunem
cu cifre ce lots dispar); „formation à l'usine", „visite d'usine"; „délais fermes garantis" fără cifră;
„zéro sinistre"; marje procentuale promise; „polistibrick.eu"; „révolution", „maison de rêve",
„devis gratuit", „pas cher". Certificatul Passivhaus și ETE-ul intră **în ziua în care există**.

## 3. Structura (12 pagini în meniu + 1 în afara lui + ressources pro + legal)

Meniu, în ordinea întrebărilor constructorului: **Le système · Prix · Chantier · Votre assureur ·
Références · Partenaire · Contact** (+ butonul „Chiffrer mon plan").

| URL | Rol | Sursa / soarta |
|---|---|---|
| `/` | Accueil: 1) hero — durerea + promisiunea + 3 cifre (205 €/m² HT livré · 30–45 jours · 2–3 jours sur votre chantier), CTA „Chiffrer mon plan" + „Appeler Pierre Dumont"; 2) cei 3 constructori francezi, video + nume + o frază; 3) „Ce que vous ne faites plus": tabelul lots (maçonnerie, ITE, doublage, étanchéité, saignées) cu 329 vs 182 €/m² de mur; 4) peretele (compoziție, fibrociment, U); 5) șantierul (3/3/sans grue, 30–45 j, formare); 6) dosarul pentru asigurator; 7) partener (leads du département, sans frais); 8) CTA final | rescrisă integral |
| `/systeme/` | Le bloc coffrant isolant à parement fibre-ciment: ce e, compoziția, U, de ce fără tencuială pe EPS, cele trei variante (Polistibrick / Polistiwall / PolistiSIP) cu când se alege fiecare; DWG/DXF/Revit | nouă; absoarbe `/produits/` și cele 3 pagini de produs (rămân ca sub-pagini, rescrise pe voce B2B) |
| `/prix/` | grila HT + ce cuprinde + „Chiffrer mon plan" (app) + „48 maisons chiffrées" (link spre `/projets/`) | există; introducerea rescrisă pe voce B2B, „prix TTC"/particular scos |
| `/chantier/` | cadența, montajul pas cu pas, formarea 2–3 zile pe primul șantier, livrarea 30–45 j, 1–2 camioane, instalațiile prin perete, ce echipament trebuie | din `/montage/` (301 → `/chantier/`) |
| `/assureur/` | „Le dossier pour votre assureur": ce documente dăm (listă + descărcare la cerere), cine răspunde tehnic în 24 h, cum decurge pe primul șantier. Zero ATEx/AT | nouă; `ressources/bloc-coffrant-decennale-avis-technique/` → 301 aici |
| `/references/` | 3 studii de caz: Montesson, CS BTP, Paris — video, cine, ce, cât a durat, ce a spus | nouă (materialul există) |
| `/devenir-partenaire/` | condițiile FR (vezi §5), formularul | există; rescrisă |
| `/contact/` + `/devis/` | 24 h, cele două căi, biroul Croissy, Pierre Dumont, +33 1 61 30 40 09 | există; texte rescrise |
| `/vous-faites-construire/` | pagina de predare pentru particular: „Donnez ce site à votre entreprise. On lui livre le kit, on forme son équipe, on chiffre votre plan." + formular care ajunge la partenerul din departament. **În afara meniului** | din `pour/proprietaires/` (301) |
| `/ressources/` | doar pentru profesioniști: re2020 (pentru BET), electricite-plomberie, enduit-bardage, incendie, prix-bloc-coffrant-isolant, bloc-coffrant-isolant (fost coffrage-isolant), polistibrick-vs-bloc-coffrant-classique (fost vs-icf), faq (rescris pentru firme) | 4 pagini B2C șterse cu 301 (combien-coute-une-maison, maison-passive, beton-cellulaire-ou-brique, maison-polystyrene-avis → `/ressources/`) |
| `/a-propos/` (+ brevet, certifications, usines, fondateur) | păstrate, scurtate pe voce B2B | presa (index + 6 comunicate) ștearsă, 301 → `/a-propos/` |
| `/projets/` | „48 maisons chiffrées" — dovada prețului public; intro rescris pentru firme; carduri pe un rând ca la RO | există |
| legal (5) | neschimbate | |
| **șterse cu 301:** `pour/constructeurs` → `/` · `pour/architectes` → `/assureur/` · `pour/investisseurs` → `/devenir-partenaire/` · `economies` → `/prix/` · presa · cele 4 ressources B2C | |

Redirecturile se scriu în `countries/fr/_redirects` (Cloudflare Pages). Nicio pagină indexată nu
dă 404.

## 4. Vocea

Regulile din `scriitura-lucian`, aplicate în franceză B2B: **vous** către firmă („on" în citate și
în frazele scurte), propoziții scurte, cifra înaintea adjectivului, fără liniuță lungă, fără
triplete, prima frază oprește cititorul, ultima cere ceva. Vocabularul profesionistului: gros œuvre,
hors d'eau hors d'air, lots, chiffrage, cadence, main-d'œuvre, DPGF, BET structure, Up, parement
fibre-ciment. Fiecare pagină deschide cu întrebarea firmei și răspunsul cu cifra (blocul
«răspuns-întâi» de la RO, în franceză). Mărturiile: **doar cele trei reale**, cu numele firmei.

## 5. Partener — condițiile pentru Franța (propunere PDG, de confirmat de patron)

Fără taxă, fără angajament de volum. Firmă cu SIRET, décennale la zi, minimum 3 oameni.
Primește: grila publică, formarea pe primul șantier, cererile particularilor din departamentul lui
(pagina de predare), materialele. Dă: un video pe săptămână de pe șantier, cifrele lui de €/m² pentru
pagina lui. Exclusivitate pe departament după primele 3 șantiere (nu de la început).
(Foaia românească e strict RO; asta e prima formulare FR — patronul o poate schimba.)

## 6. Instalația (nimic nou de inventat)

Același build: `fapte.py` primește intrarea **`fr`** (brevet, mărci, certificări așa cum sunt pe
pagina FR, U, grila HT, livrare 30–45 j, formare 2–3 j, reperul pieței 1 700–2 200 €/m² clé en main
cu sursele EPTB/Renovbox), deci `llms.txt`/`llms-full.txt` FR se generează, Organization = SARL +
CM2C + LinkedIn, `check_fapte` blochează cifre neconcordante. `scripts/test-citibil.py fr` cu lista
de pagini FR. Butonul „Chiffrer mon plan" → aplicația cu `?pays=FR`.

## 7. Verificare (înainte de a spune «gata»)

1. Build verde (toate check-urile, JSON-LD valid, subsol/nav consecvente).
2. Zero cuvinte interzise (§2) pe tot site-ul — script.
3. Fiecare URL vechi indexat răspunde 200 sau 301 — script pe sitemap-ul de azi.
4. Testul «ce vede un AI» pe cele 12 pagini: cifră + sursă în primul pasaj, Organization complet.
5. Citit cu voce tare: prima și ultima frază de pe fiecare pagină trec testul din `scriitura-lucian`.
6. Previzualizare locală: prima pagină, prix, chantier, assureur, references pe 1440 și 390 px.
7. Publicarea FR rămâne manuală (`gh workflow run cloudflare-pages.yml -f country=fr`) și doar la
   comanda patronului; domeniul arată încă spre WordPress-ul vechi până la mutarea One.com.

## 8. Cum știm că a mers (6 luni de la publicare)

10 firme franceze intrate în discuție prin „Chiffrer mon plan" sau formular; 3 prime șantiere.
Se citește în aplicația de devize, în cutia `devis@polistibrick.fr` și în Cloudflare Analytics.

## 9. În afara acestui design (lucrări separate, notate în restanțe)

Asigurarea de fabricant (broker FR) · mutarea domeniului (One.com) · cele 8 înregistrări DNS ·
certificatul Passivhaus și ETE-ul (se pun când există) · LinkedIn/GBP pentru Franța.
