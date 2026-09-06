---
type: process
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
consumes: [tara, config-tara, pagina, sablon-partajat, imagini, traduceri]
produces: [build/<cod>/]
---

# build

Transformă sursa unei țări în site-ul static gata de urcat: `python3 build/build.py <cod>` → `build/<cod>/`.

## Intrare → Mișcare → Ieșire

Citește `countries/<cod>/` + `_config.json`, `shared/`, `translations/path_maps.py` și `ui_strings.json`. Șterge și reface `build/<cod>/`, copiază, injectează, verifică. Scrie `build/<cod>/` (ignorat în git; produsul, nu sursa).

## De ce are forma asta

Build-ul e determinist: același input dă aceleași fișiere, octet cu octet (verificat 06.09.2026: 569 fișiere RO + 610 FR identice înainte și după restructurare). De aceea ce vezi pe local e exact ce urcă workflow-ul.

## Pași (`build_country`, `build/build.py:564-618`)

1. `rm` + `mkdir build/<cod>` (`:567-569`) — serverul local ține inodul vechi, vezi `../objects/previzualizare-locala.md`.
2. `shared/css`, `shared/js` → `assets/` cu transformări (placeholders, rescrierea căilor RO → limbă, `:572-573`); `shared/images` → `images/` (`:574`).
3. `shared/downloads/<lang>` + `shared/downloads/shared` → `downloads/` (`:577-584`).
4. Țara fără pagini (doar `_config.json`) e sărită și `build/<cod>` șters (`:586-593`).
5. `countries/<cod>/` → `build/<cod>/` prin `copy_tree` (`:292-327`): placeholders (`:93`), prerender nav/footer în monturi (`:276-290`), rescrierea căilor pentru țările pe șablon FR (`:315`).
6. `_config.json` scos din output (`:598-601`).
7. SEO: canonical, og:url, hreflang pe domeniul oficial (`inject_seo`, `:340`).
8. Optimizări HTML: fonturi non-blocante, `site.js` amânat (`:168-243`).
9. Consistența footer + nav pe toate paginile (`:491`, `:527`) — oprește build-ul la diferențe.
10. `sitemap.xml` (lastmod din `git log`, `:364-410`), `robots.txt` (`:413`), `_headers` + `.htaccess` (`:429`).

Comenzi: `python3 build/build.py fr` · `python3 build/build.py ro fr` · fără argument = toate cele 9 țări (lent: copiază 529 MB de imagini de 9 ori).

## Dacă schimbi asta

- **Mișcă:** `build/<cod>/` și tot ce publică workflow-ul; `ASSET_VERSIONS` (`:42-51`) dacă atingi lista de fișiere versionate.
- **Nu mișcă:** sursa din `countries/` și `shared/`.

## Suprafețe

| Cine | Rol |
|---|---|
| Claude / Cursor / patronul | rulează local |
| workflow-ul Cloudflare | rulează pe ubuntu, Python 3.12 |
| `mcp/server.py` | poate rula build-ul pentru Cursor |

## Vezi

- Obiecte: `../objects/tara.md`, `../objects/sablon-partajat.md`, `../objects/traduceri.md`
- Sursa: `build/build.py`
