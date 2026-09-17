# polisti.ro citibil de AI — design (varianta B)

Data: 17.09.2026 · Ramură: `ai-citibil-ro` · Țară: RO (instalația în `build/`, ca FR să moștenească)

## Scop

Când cineva întreabă un asistent AI (ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini)
o întrebare la care o pagină polisti.ro răspunde, AI-ul să găsească pagina, să extragă pasajul,
să aibă încredere în entitate și să citeze polisti.ro.

Criteriu de reușită, măsurabil: pe cele 13 pagini-țintă, testul „10 întrebări de cumpărător"
(rulat pe HTML-ul construit, apoi pe site-ul viu) răspunde cu cifră + sursă la fiecare întrebare
pe care pagina o vizează; zero neconcordanțe de fapte între llms.txt, JSON-LD, subsol și text.

## Ce a găsit auditul (17.09)

- `llms.txt` e scris de mână (12.08): zice 11 modele de case, site-ul are 24; „august 2026".
- Organization în JSON-LD are 3 variante: completă doar pe `/` și `/contact/`; pe 31 de pagini
  e golită (fără telefon, email, vatID, legalName, sameAs).
- `og:locale` există în `_config.json` (ro_RO) dar nu ajunge în pagină.
- Prețul pieței „la cheie" apare în 4 variante pe 4 pagini (900–1 350 / 900–1 300 / 900–1 650 /
  ~1 300). Cifra Polistibrick (950–1 280) e consecventă.
- Din 13 pagini-țintă, 3 deschid deja „răspuns-întâi" (casa-pasiva, nzeb, cat-costa-o-casa);
  10 deschid cu definiție sau cu text de broșură, fără cifră în prima frază.
- Emailul e doar în JSON-LD, nu în text; U-ul nu apare pe prima pagină.
- `dateModified` pe articole e scris de mână (2026-08-12) → rămâne în urmă la orice editare.
- Rețele sociale RO verificate: youtube.com/@Polistibrick, instagram.com/polistibrick.ro,
  facebook.com/polistibrik. TikTok-ul e cont personal — nu intră în sameAs.

## Piesele

### 1. `build/fapte.py` — o singură sursă de adevăr
Un modul citit de build. Faptele care NU se schimbă cu pagina: brevet, mărci, certificări,
U-uri pe sistem, grila de preț (interval + luna), intervalul canonic al pieței „la cheie"
(900–1 350 €/m², cu sursele numite) și „la gri", energie €/kWh cu sursa. Restul (firmă,
telefon, email, adresă, rețele) vine din `_config.json` — acolo se completează `contact.social`
cu cele 3 URL-uri verificate. Nimic nou nu se inventează: faptele se copiază din paginile
existente, iar acolo unde paginile diferă se alege una și se aliniază celelalte.

### 2. Generatorul `llms.txt` + `llms-full.txt` (în `build/build.py`, după sitemap)
- `llms.txt`: antet din fapte + config; lista paginilor indexabile din sitemap, fiecare cu
  `<title>` și `meta description` ale ei; numărul de modele NUMĂRAT din `/proiecte/`.
- `llms-full.txt`: pentru fiecare pagină din sitemap, `## Titlu` + URL + textul principal
  (fără nav/footer/script) convertit în text simplu, în ordinea sitemap-ului.
- Fișierul static `countries/ro/llms.txt` se șterge (altfel îl suprascrie pe cel generat sau
  invers — un singur drum).

### 3. Organization canonic injectat la build
Un singur obiect Organization (`@id` `…/#organizatie`), construit din config + fapte, cu
`legalName`, `vatID`, `telephone`, `email`, `PostalAddress`, `logo`, `sameAs` (Espacenet,
EUIPO ×2, YouTube, Instagram, Facebook). La build, orice Organization inline cu același `@id`
e ÎNLOCUIT cu cel canonic; paginile fără el îl primesc. `WebPage`/`Article` primesc
`dateModified` din git (aceeași funcție ca sitemap-ul), `inLanguage` din config.
`og:locale` se emite în `inject_seo`.

### 4. „Răspuns-întâi" pe 13 pagini (conținut, `countries/ro/`)
Sub H1, înaintea textului existent, un bloc `<section class="raspuns">`: H2 = întrebarea
exact cum o pune omul; 2–3 fraze cu cifra în prima frază și sursa numită lângă cifră;
rând „Actualizat: <lună an>". Textul existent rămâne neatins dedesubt. Paginile care deschid
deja corect (casa-pasiva, nzeb) primesc doar sursa/data dacă lipsesc. FAQPage-ul paginii
primește întrebarea nouă doar dacă răspunsul e identic cu textul vizibil.
Stil: regulile din `scriitura-lucian` (cifre, nu adjective; fără liste negre).

### 5. Faptele în text vizibil
Subsolul comun (`shared/js/site.js`, `FOOTER_HTML`): rând cu firma, CUI, J, adresa, telefon,
email — textul, nu doar schema. Prima pagină: U-ul peretelui în text. Aliniere: cele 3 pagini
cu prețul pieței divergent trec pe intervalul canonic + sursele numite.

### 6. Verificări la build (blochează build-ul)
- `check_fapte`: fiecare cifră din `llms.txt` există în textul paginii spre care trimite.
- `check_organization`: exact o variantă de Organization pe tot site-ul.
- JSON-LD parsabil pe toate paginile (există deja implicit; se face explicit).
- Testul „10 întrebări" ca script separat (`scripts/test-citibil.py`): pentru fiecare pagină-țintă,
  extrage H1, primul paragraf, cifre, surse, JSON-LD; raport înainte/după.

## Ce NU intră
- Pagini noi (varianta C). Grila de preț a firmei (decizia patronului). FR (moștenește
  instalația; conținutul FR, separat). Prezența în afara site-ului (GBP, LinkedIn firmă,
  Wikidata, directoare) — listă separată pentru patron.

## Riscuri și cum le țin
- Build-ul are `check_footer_consistency`/`check_nav_consistency` care compară toate paginile:
  orice schimbare în subsol trece prin ele. Lucrez pe ramură; nimic nu se publică fără comandă.
- Înlocuirea Organization poate schimba `@id`-uri referite de `author`/`publisher` → păstrez
  `@id` identic (`…/#organizatie`).
- `llms-full.txt` mare (~500 KB) → e text, se servește cu cache; nu intră în sitemap.
