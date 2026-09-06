---
type: object
cluster: site
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: countries/<cod>/
---

# Țară (site de țară)

Un site de țară = folderul `countries/<cod>/` (paginile HTML + `_config.json`) + un proiect Cloudflare Pages din `cloudflare/projects.json`. Patronul spune „site-ul francez", „site-ul românesc".

## De ce are forma asta

O singură sursă pentru toate țările, dar fiecare țară are copia ei de pagini: textul se scrie de mână în limba ei, nu se generează. Build-ul construiește o țară odată și sare țările care au doar `_config.json` (`build/build.py:586-593`).

## Forma

- 9 coduri: `ro` (37 pagini, live pe polisti.ro), `fr` (49 pagini, live pe polistibrick-fr.pages.dev), `en`, `it`, `es`, `nl`, `de`, `ie`, `me` (28 pagini fiecare, seed-uite pe 11.08.2026 din FR-ul de atunci; se construiesc, nu se publică — rezervă).
- FR e șablonul pentru țările noi (`translations/WORKFLOW.md:3`).
- Fiecare țară are `_config.json` (vezi `config-tara.md`), `index.html`, `404.html`, `llms.txt`, folderele de pagini în limba ei (`proiecte/` RO = `projets/` FR).
- FR are în plus `_redirects` (Cloudflare) și 6 articole de presă la rădăcină.
- Domeniul și proiectul Pages: `cloudflare/projects.json` (ro → polistibrick-ro → polisti.ro; fr → polistibrick-fr → polistibrick.fr).

Citări: `build/build.py:586-593`, `cloudflare/projects.json`, `translations/WORKFLOW.md:3`

## Legat de

- **deține:** `pagina.md`, `config-tara.md`, imaginile proprii (`countries/<cod>/images/`, doar FR le are)
- **deținut de:** repo-ul
- **se leagă cu:** `deploy.md` (proiectul Pages), `sablon-partajat.md` (nav/footer intră la build), `traduceri.md` (slugurile)
- **seamănă dar nu e:** `build/<cod>/` — e produsul generat, ignorat în git; nu se editează

## Dacă schimbi asta

- **Mișcă:** `build/<cod>/` la următorul build; sitemap-ul și hreflang-ul țării; RO live la push pe main.
- **Nu mișcă:** celelalte țări. O schimbare de text în RO nu ajunge în FR și invers; cele 7 țări de rezervă au un catalog vechi (28 pagini, fără cele 48 de modele).

## Suprafețe

| Cine | Rol |
|---|---|
| Claude / Cursor | scriu paginile |
| `build/build.py` | citește, transformă, scrie `build/<cod>/` |
| workflow-ul Cloudflare | construiește și publică (RO automat, restul manual) |
| `RO CMR/.claude/launch.json` | servește `build/ro` și `build/fr` pe 4700 / 4710 |

## Vezi

- Sursa: `countries/`
- Fluxul pentru o țară nouă: `translations/WORKFLOW.md`
