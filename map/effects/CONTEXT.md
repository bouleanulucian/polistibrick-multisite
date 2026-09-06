# effects — dacă schimbi X, deschide Y

Catalog, nu explicație: spune ce fișe să deschizi și ce se mișcă la prima mână. Dacă indexul și o fișă nu se pupă, repară fișa.

## Din interiorul repo-ului

| Dacă schimbi | Deschide | Mișcă | Nu mișcă |
|---|---|---|---|
| un text, o secțiune, un `<style>` inline într-o pagină | `../objects/pagina.md` | pagina aceea a țării aceleia; sitemap-ul | aceeași pagină în cealaltă limbă (o schimbi de mână); nav/footer |
| nav, footer, selectorul de țară (`shared/js/site.js`) | `../objects/sablon-partajat.md` | toate țările la următorul build; hash-ul din URL; verificarea de consistență la build | sursa paginilor |
| `shared/css/site.css` sau un js comun | `../objects/sablon-partajat.md` | toate țările; hash-ul | `<style>`-urile inline |
| o imagine din `shared/images/` | `../objects/imagini.md` | toate build-urile; cache-ul CDN 30 de zile | paginile (căi relative) |
| o imagine din `countries/fr/images/` | `../objects/imagini.md` | doar FR | RO |
| un model, un preț din catalog | `../objects/model-casa.md`, `../processes/model-nou.md` | RO ȘI FR (48 = 48), `case/`, `planuri/`, reclamele | celelalte 7 țări, app-ul de devize |
| `countries/<cod>/_config.json` | `../objects/config-tara.md` | toate paginile țării (placeholders, canonical, hreflang), formularele (cheia), iframe-ul de devize | alte țări |
| `translations/path_maps.py` | `../objects/traduceri.md`, `../objects/sablon-partajat.md` | link-urile nav/footer pe țările non-RO; `PB_SLUGS` trebuie ținut de mână în pas | RO, FR |
| `translations/ui_strings.json` | `../objects/traduceri.md` | etichetele nav/footer per limbă | textele din pagini |
| `build/build.py` | `../processes/build.md` | tot ce se construiește și se publică; `ASSET_VERSIONS` | sursa |
| `.github/workflows/cloudflare-pages.yml`, `cloudflare/projects.json` | `../objects/deploy.md` | ce țară pleacă la push (azi doar RO) și pe ce proiect | localul |
| `scripts/planuri/<model>.py`, `cofraj.py` | `../objects/model-casa.md` | prețurile calculate, planurile | catalogul (se rescrie de mână) |
| `campanii/` | `../objects/model-casa.md` | nimic pe site (neurmărit) | build-ul |
| mutarea/redenumirea `build/`, `build/<cod>` | `../objects/previzualizare-locala.md` | `RO CMR/.claude/launch.json` (alt proiect) | — |
| un fișier din `_archive/` | `_archive/README.md` | nimic (nu e citit de nimeni) | — |

## Din afara repo-ului (pointeri care intră; niciun grep de aici nu îi vede)

| Cine intră | Unde lovește | Ce se rupe dacă muți ținta |
|---|---|---|
| `RO CMR/.claude/launch.json` (site-ro, site-fr, site-fr-varianta) | `build/ro`, `build/fr`, `build/fr-varianta` | previzualizarea locală |
| `RO CMR/.claude/serveste-fara-cache.py` | servește folderele de mai sus | idem |
| skill `~/.claude/skills/reclame-video-case/SKILL.md` | `campanii/reclame-proiecte/<casa>/` | livrarea reclamelor |
| `.cursor/mcp.json` (cale absolută) | `mcp/server.py`, `POLISTIBRICK_ROOT` | MCP-ul lui Cursor |
| memoria Claude (proiectul RO CMR) | `shared/images/`, `scripts/planuri/`, `countries/ro/proiecte/index.html`, `countries/fr`, `build/fr`, `campanii/reclame-proiecte/` | sfaturi vechi; memoria se corectează, nu repo-ul |
| `RO CMR/.claude/settings.local.json` | URL-uri `bouleanulucian.github.io/polistibrick-multisite/…` (gh-pages, rezervă) | nimic viu |
| app-ul de devize (alt repo) | e chemat de site prin `_config.json` → `devis_app.url`, nu invers | iframe-ul de pe `devis/` / `oferta/` |
| GitHub Actions | `build/build.py`, `cloudflare/projects.json` | deployul |
