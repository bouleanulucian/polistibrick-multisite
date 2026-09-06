# polistibrick-multisite

Sursa unică a site-urilor Polistibrick pe țări: `countries/<cod>/` + `shared/` → `python3 build/build.py <cod>` → `build/<cod>/` → Cloudflare Pages. Live: **polisti.ro** (RO) și **polistibrick-fr.pages.dev** (FR; domeniul polistibrick.fr așteaptă nameserverele de la One.com).

Construit pe ICM: folderele poartă ordinea, ierarhia poartă contextul, fișierele poartă starea. Dacă ceva trebuie explicat, explicația stă într-o fișă din `map/`, nu în capul cuiva. Acest fișier doar rutează.

## Unde stă fiecare lucru

| Folder | Ce ține |
|---|---|
| `countries/<cod>/` | paginile HTML ale unei țări + `_config.json` (firmă, contact, formulare, domeniu) |
| `shared/` | ce e comun: css, js (nav + footer trăiesc în `js/site.js`), imagini (`images/case/` = cele 48 de modele), downloads |
| `build/build.py` | fabrica: config → placeholders → nav/footer → SEO → sitemap → `build/<cod>/` (ignorat în git) |
| `translations/` | fluxul pentru o țară nouă (`WORKFLOW.md`), `path_maps.py` + `ui_strings.json` (citite de build), dicționarele |
| `cloudflare/` + `.github/workflows/` | proiectele Pages și deployul: push pe main = doar RO; FR manual |
| `scripts/planuri/` | planul și prețul fiecărui model (un `.py` pe casă, `cofraj.py` = prețul cofrajului) |
| `campanii/` | reclamele video pe modele (neurmărit în git, 2,4 GB; skill-ul reclame-video-case livrează aici) |
| `media/`, `tools/`, `mcp/`, `drafts/` | video sursă, unelte (blog, studio testimoniale), MCP-ul lui Cursor, ciorne blog |
| `map/` | harta sistemului: ce e fiecare lucru și ce mai mișcă dacă îl schimbi |
| `_archive/` | ce nu mai e pe drumul principal; `_archive/README.md` spune ce și de ce |

## Du-te după ce ai de făcut

| Dacă | Mergi la | Oprește-te la |
|---|---|---|
| schimbi un text sau o secțiune pe o pagină | `map/objects/pagina.md` → `countries/<cod>/…` | omul vede pe local (`map/processes/previzualizeaza.md`) |
| schimbi nav, footer, css sau js comun | `map/objects/sablon-partajat.md` | build + verificare pe RO și FR |
| adaugi sau modifici un model de casă | `map/processes/model-nou.md` | catalogul RO și FR arată la fel (48 = 48) |
| publici | `map/processes/publica.md` | `curl` pe live confirmă schimbarea |
| pornești o țară nouă | `translations/WORKFLOW.md` | `build/<cod>/` există și arată bine |
| nu știi ce mișcă o schimbare | `map/effects/CONTEXT.md` | fișele numite acolo |
| cauți un script sau un fișier vechi | `_archive/README.md` | citești, nu editezi |

## Regulile care nu se negociază

- Nimic nu se publică până patronul nu a văzut pe local (build + serverul fără cache din `RO CMR/.claude/launch.json`: 4700 RO, 4710 FR).
- Push pe `main` publică **automat România**. Franța doar cu `gh workflow run cloudflare-pages.yml --ref main -f country=fr`.
- Verificarea vizuală se face cu Playwright și rotița de mouse (eroul face scroll-jacking); capturile din panou mint.
- RO și FR au fiecare copia lor de pagini: o schimbare de text într-una NU ajunge în cealaltă.
- `AGENTS.md` e geamănul generat al acestui fișier (`map/_scripts/regenereaza.sh`); nu se editează de mână.
