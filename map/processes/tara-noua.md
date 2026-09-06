---
type: process
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
consumes: [tara, config-tara, traduceri, deploy]
produces: [countries/<cod>/, build/<cod>/, proiect Cloudflare]
---

# țară nouă (sau relansarea uneia de rezervă)

Pornește un site de țară din șablonul FR, cu URL-uri în limba ei, și îl publică manual când e gata.

## Intrare → Mișcare → Ieșire

Intră un `_config.json` al țării și dicționarul ei. Se seed-uiește din FR, se traduc frazele, se localizează folderele, se construiește. Iese `build/<cod>/`, apoi un proiect Cloudflare Pages când patronul spune.

## De ce are forma asta

FR e referința (`translations/WORKFLOW.md:3`); cele 7 țări de rezervă (en, it, es, nl, de, ie, me) au fost seed-uite pe 11.08.2026 din FR-ul de atunci și au rămas la designul vechi (28 de pagini, fără cele 48 de modele, fără eroul din 24.08). **O relansare înseamnă re-seed din FR-ul de azi, nu peticirea copiei vechi.**

## Pași (detaliile în `translations/WORKFLOW.md`)

1. `countries/<cod>/_config.json` complet: `lang`, `domain_url`, firmă, contact, `forms.access_key` (cheia Web3Forms decide cutia), `devis_app`.
2. `python3 translations/seed_from_fr.py <cod>` (`WORKFLOW.md:10-11`).
3. `python3 translations/extract_fr_phrases.py --out translations/phrases_fr_source.json`, apoi umple `translations/<cod>.json` după `BRIEF.md` și `GLOSSARY.md` (terminologia e obligatorie).
4. `python3 translations/apply_lang.py <cod>`; `python3 translations/localize_country_paths.py <cod>` (slugurile din `path_maps.py`); adaugă limba în `PB_SLUGS` din `shared/js/site.js:247` și în `ui_strings.json`.
5. `python3 build/build.py <cod>` → server local → patronul vede.
6. Intrarea în `cloudflare/projects.json` există pentru toate cele 9; publicarea: `gh workflow run cloudflare-pages.yml --ref main -f country=<cod>` (`publica.md`); domeniul: Cloudflare Pages → Custom domains, și nameserverele la Cloudflare.

## Dacă schimbi asta

- **Mișcă:** `countries/<cod>/`, `build/<cod>/`, `PB_SLUGS`, `ui_strings.json`, `path_maps.py`.
- **Nu mișcă:** RO, FR; live-ul, până la `workflow_dispatch`.

## Suprafețe

| Cine | Rol |
|---|---|
| Claude | rulează fluxul |
| patronul | decide când o țară se publică și pe ce domeniu |

## Vezi

- Obiecte: `../objects/tara.md`, `../objects/traduceri.md`, `../objects/deploy.md`
- Sursa: `translations/WORKFLOW.md`
