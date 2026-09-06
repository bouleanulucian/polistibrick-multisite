---
type: object
cluster: sablon
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: shared/js/site.js
---

# Șablonul partajat (nav, footer, css, js comun)

Tot ce apare la fel pe toate paginile trăiește în `shared/` și e lipit în pagini la build. Nav-ul și footer-ul sunt două șiruri în `shared/js/site.js`: `NAV_HTML` (`:27`) și `FOOTER_HTML` (`:113`).

## De ce are forma asta

Un singur loc pentru meniu și footer, dar paginile trebuie să iasă complete în HTML (SEO, fără flash la încărcare): build-ul extrage cele două șabloane din `site.js` (`build/build.py:258-274`) și le prerandează în monturile `data-include` (`:276-290`). Apoi verifică că toate paginile țării au același footer și același nav (`check_footer_consistency` `:491`, `check_nav_consistency` `:527`) — o pagină cu nav diferit oprește build-ul cu un mesaj.

## Forma

- `shared/js/site.js`: `NAV_HTML`, `FOOTER_HTML`, selectorul de țară, `PB_SLUGS` (`:247`) — harta sluguri RO → limbă, inline; comentariul zice „generată din `translations/path_maps.py`", dar nu există script care să o regenereze (fantomă) — se editează de mână odată cu `path_maps.py`.
- Căile RO din `site.js` sunt rescrise per țară la build din `PATH_REWRITES` (`build/build.py:100-110`, din `translations/path_maps.py`).
- Etichetele nav/footer per limbă: `translations/ui_strings.json` (`build/build.py:30`).
- CSS: `shared/css/site.css` (comun); `shared/css/mercury-home.css` (stilul vechi al homepage-ului; încă versionat, `build/build.py:45` — rezervă, verifică cu `grep -l mercury-home countries/*/index.html` înainte de a-l scoate).
- JS: `forms.js` (Web3Forms), `cookies.js`, `devis-embed.js` (iframe-ul de devize), `vizualizator-3d.js`, `mercury-perf.js`.
- Hash-uri de cache-busting pe fiecare fișier: `ASSET_VERSIONS` (`build/build.py:42-51`) — orice octet schimbat în `site.js` schimbă URL-ul lui în toate paginile.

Citări: `shared/js/site.js:27,113,247`; `build/build.py:30,42-51,100-110,258-290,491,527`

## Legat de

- **deținut de:** repo-ul (comun tuturor țărilor)
- **se leagă cu:** `traduceri.md` (`path_maps.py`, `ui_strings.json`), `pagina.md` (monturile), `tara.md`
- **seamănă dar nu e:** `<style>`-urile inline din pagini (specifice unei secțiuni; nu sunt partajate)

## Dacă schimbi asta

- **Mișcă:** TOATE țările la următorul lor build (RO live la push; FR după `workflow_dispatch`); hash-ul din URL-ul fișierului; consistența nav/footer verificată la build.
- **Nu mișcă:** sursa paginilor (rămân neschimbate; efectul se vede doar după build); cele 7 țări de rezervă până nu le construiește cineva.

## Suprafețe

| Cine | Rol |
|---|---|
| Claude / Cursor | editează |
| `build/build.py` | extrage, rescrie căile, prerandează, verifică |
| browserul | încarcă `assets/js/site.js?v=<hash>` |

## Vezi

- Sursa: `shared/js/site.js`, `shared/css/site.css`
