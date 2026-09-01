# BRIEF — Traducerea site-ului RO → FR (polistibrick.fr)

Misiune: pagina RO (design nou) devine pagina FR, identică la structură, exemplară la limbă.
Publicul francez: în principal FIRME DE CONSTRUCȚII (constructeurs), apoi arhitecți și particulari.

## Reguli absolute
1. NU modifici structura HTML: aceleași taguri, clase, id-uri, atribute, ordinea secțiunilor.
2. Traduci TOT ce e citibil de om: text, `<title>`, meta description, og:title/description,
   alt, aria-label, title=, placeholder, `<option>`, JSON-LD (schema.org), textul din butoane.
   Comentariile HTML se traduc și ele. NIMIC omis.
3. NU traduci și NU atingi: `{{placeholder}}`-urile (ex. {{contact.phone_display}}), `${BASE}`,
   `data-include`, codul JS/CSS (doar string-urile de text vizibil din JS se traduc),
   numele de fișiere/imagini, numerele și prețurile (rămân identice).
4. `lang="ro"` → `lang="fr"` · `og:locale` → `fr_FR` · `ro_RO` nicăieri.
5. Linkurile interne se mapează pe slugurile FR (tabelul de mai jos). Linkurile care încep cu
   `images/`, `assets/`, `downloads/`, `http`, `#`, `mailto:`, `tel:` rămân neatinse.
6. Vouvoiement peste tot: „vous", niciodată „tu". Site-ul RO tutuiește; în Franța nu.
7. Ghilimele franceze « … » cu spații; fără liniuță lungă (—) în text; propoziții scurte,
   ton uman, zero superlative goale (stilul casei).
8. Cifrele NU se schimbă și NU se inventează. Dacă o afirmație e specific românească
   (lege RO, ANPC, nZEB, lei, prețuri de manoperă RO), o ADAPTEZI cinstit:
   nZEB → RE2020 (standardul francez); ANPC/SAL → médiation de la consommation;
   OG 21/1992 → Code de la consommation. Dacă nu ești sigur, traduci fidel și RAPORTEZI.
9. Capcana A1: doar PLACA de fibrociment e clasa A1 (incombustibilă), NU peretele/sistemul.
   Formularea sigură: « la plaque extérieure est en fibres-ciment, classe A1, incombustible ».
10. NICIODATĂ autoconstrucție: nu sugera că clientul construiește singur. Montajul îl face
    un constructeur / o entreprise.

## Glosar (obligatoriu, consecvent)
cofraj → coffrage · cofraj izolant → coffrage isolant · cofraj pierdut → coffrage perdu
perete → mur · planșeu → plancher · acoperiș → toiture · fundație → fondations
construcția la gri → hors d'eau hors d'air (mise hors d'eau hors d'air)
la cheie → clé en main · finisaje → finitions · manoperă → main-d'œuvre
șantier → chantier · beton armat → béton armé · fier/armătură → ferraillage
polistiren grafitat → PSE graphité · placă de fibrociment → plaque de fibres-ciment
placa interioară de finisaj → doublage · gips-carton → placo / plaque de plâtre
punte termică → pont thermique · etanșeitate la aer → étanchéité à l'air
defazaj termic → déphasage thermique · casă pasivă → maison passive
zidărie → maçonnerie · cărămidă → brique · BCA → béton cellulaire
deviz/ofertă → devis · cerere de ofertă → demande de devis · preț → prix
constructor → constructeur · dezvoltator → promoteur · proprietar → propriétaire (particulier)
brevet european → brevet européen · agrement tehnic → avis technique
casă la gri cu trei oameni → hors d'eau hors d'air à trois personnes (adaptare naturală)
NUME PROPRII neatinse: Polistibrick, Polistiwall, PolistiSIP, MBK/PBK/TBK + cifre,
SIP250/SIP300, numele modelelor de case (Doina, Luna, Nera, Vega…), STEICO, Eurocode.

## Harta slugurilor (linkuri interne)
| RO | FR |
| accesorii/ | accessoires/ |
| acoperis-tbk/ | toit-tbk/ |
| acoperis-tbk-sip250/ | toit-tbk-sip250/ |
| ansamblu-lyon/ | ensemble-lyon/ |
| arhitecti/ | architectes/ |
| bca-sau-caramida/ | beton-cellulaire-ou-brique/ |
| calculator/ | calculateur/ |
| casa-cluj-napoca/ | maison-cluj-napoca/ |
| casa-din-polistiren-pareri/ | maison-polystyrene-avis/ |
| casa-pasiva/ | maison-passive/ |
| cat-costa-o-casa/ | combien-coute-une-maison/ |
| certificari/ | certifications/ |
| cofraj-izolant/ | coffrage-isolant/ |
| comparatie/ | comparaison/ |
| confidentialitate/ | confidentialite/ |
| constructori/ | constructeurs/ |
| despre/ | a-propos/ |
| devino-partener/ | devenir-partenaire/ |
| echipa/ | fondateur/ |
| economii/ | economies/ |
| fabrici/ | usines/ |
| investitori/ | investisseurs/ |
| mentiuni-legale/ | mentions-legales/ |
| montaj/ | montage/ |
| nzeb/ | re2020/ |
| oferta/ | devis/ |
| patent/ | brevet/ |
| pentru/ | pour/ |
| pereti-mbk/ | murs-mbk/ |
| planseu-pbk/ | planchers-pbk/ |
| polistibrick/ | polistibrick/ |
| polistibrick-vs-icf-clasic/ | polistibrick-vs-icf-classique/ |
| polistisip/ | polistisip/ |
| polistiwall/ | polistiwall/ |
| preturi/ | prix/ |
| produse/ | produits/ |
| proiecte/ | projets/ |
| proprietari/ | proprietaires/ |
| resurse/ | ressources/ |
| sustenabilitate/ | durabilite/ |
| termeni/ | conditions/ |
| testimoniale/ | temoignages/ |

Pagina `parteneri/` NU se traduce (hartă cu județele României, doar RO).

## Raport la final (obligatoriu)
Întorci JSON: {"pagina": "<țintă>", "status": "ok", "adaptari": ["..."], "incert": ["..."]}
— în `adaptari` scrii ce ai adaptat (legal RO→FR, nZEB→RE2020 etc.),
— în `incert` orice formulare/cifră care cere ochiul patronului. Gol dacă nimic.
