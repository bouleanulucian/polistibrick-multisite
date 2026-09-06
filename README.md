# Polistibrick multisite

Sursa unică a site-urilor Polistibrick pe țări. Un repo → un folder de țară → un build → un proiect Cloudflare Pages.

| | |
|---|---|
| **Live** | polisti.ro (RO) · polistibrick-fr.pages.dev (FR — domeniul polistibrick.fr așteaptă mutarea nameserverelor de la One.com) |
| **În rezervă** | en, it, es, nl, de, ie, me — seed-uite din FR pe 11.08.2026, se construiesc, nu se publică |
| **Harta** | `map/` — ce e fiecare lucru și ce mai mișcă dacă îl schimbi. Agenții intră prin `CLAUDE.md` / `AGENTS.md` |
| **Arhiva** | `_archive/` — ce nu mai e pe drumul principal (`_archive/README.md`) |

## Structura

```
countries/<cod>/        paginile HTML ale țării + _config.json (firmă, contact, formulare, domeniu)
shared/                 css, js (nav + footer în js/site.js), images (case/ = cele 48 de modele), downloads
build/build.py          fabrica: config → placeholders → nav/footer → SEO → sitemap → build/<cod>/
translations/           fluxul de țară nouă (WORKFLOW.md), path_maps.py + ui_strings.json (citite de build)
cloudflare/             projects.json (țară → proiect Pages → domeniu), jurnalul migrării FR
.github/workflows/      deployul: push pe main = doar RO; alte țări prin workflow_dispatch
scripts/planuri/        planul și prețul fiecărui model de casă (un .py pe casă, cofraj.py)
campanii/               reclamele video pe modele (2,4 GB, neurmărit în git)
media/ tools/ mcp/      video sursă, unelte (blog, studio testimoniale), MCP-ul lui Cursor
map/ _archive/          harta sistemului · arhiva
```

## Construiește

```bash
python3 build/build.py fr        # o țară → build/fr/
python3 build/build.py ro fr     # două
python3 build/build.py           # toate cele 9 (lent)
```

Build-ul: citește `countries/<cod>/_config.json`, copiază `shared/` și paginile, umple `{{placeholders}}`, lipește nav-ul și footer-ul din `shared/js/site.js`, rescrie căile RO în limba țării (`translations/path_maps.py`), injectează canonical/hreflang, verifică că nav-ul și footer-ul sunt identice pe toate paginile, scrie `sitemap.xml` (lastmod din git), `robots.txt`, `_headers`. `build/` e ignorat în git.

## Vezi pe local

Serverele stau în proiectul vecin `RO CMR/.claude/launch.json` (`site-ro` 4700, `site-fr` 4710), servite fără cache. După fiecare build, serverul se repornește (build-ul recreează folderul). Detalii: `map/processes/previzualizeaza.md`.

## Publică

- **RO**: `git push origin main` → GitHub Actions construiește și urcă pe Cloudflare Pages automat (`.github/workflows/cloudflare-pages.yml`).
- **FR** (și orice altă țară): `gh workflow run cloudflare-pages.yml --ref main -f country=fr`, apoi `gh run watch`.
- Nimic nu se publică până patronul nu a văzut pe local. Pașii: `map/processes/publica.md`.

Secretele GitHub: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`. Proiectele: `cloudflare/projects.json`.

## Placeholders

Oriunde în HTML: `{{cheie.subcheie}}` din `_config.json` al țării — `{{contact.phone_display}}`, `{{company.address_street}}`, `{{devis_app.url}}`.

## Formulare

Formularele (`/oferta/`, `/contact/`, `/devino-partener/` și echivalentele FR) merg prin Web3Forms cu `forms.access_key` din `_config.json`.

**Unde ajunge mailul decide cheia, nu `form_submit_email`** (câmp documentar). Ca să schimbi destinatarul îți trebuie altă cheie sau alt destinatar în panoul Web3Forms. Lead-urile RO au picat la asociați în primele zile după lansare din exact cauza asta; reparat pe 13.08.2026.

- RO → `contact@polisti.ro` (cheia `91843857…`, cont `contact@polisti.ro`)
- FR → `contact@polistibrick.fr`

## Țară nouă

`translations/WORKFLOW.md` (seed din FR, dicționar, localizarea slugurilor, build). Cele 7 țări de rezervă sunt copii vechi: o relansare = re-seed din FR-ul de azi, nu peticire.

## Stack

HTML/CSS/JS static, un script Python fără dependențe, Cloudflare Pages, GitHub Actions. Restructurat pe metoda ICM pe 06.09.2026 (harta în `map/`).
