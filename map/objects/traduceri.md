---
type: object
cluster: date
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: translations/
---

# Traduceri (sluguri, etichete, dicționare, fluxul de țară nouă)

`translations/` ține ce e citit de build (`path_maps.py`, `ui_strings.json`), dicționarele pe limbă și scripturile fluxului „țară nouă din FR". RO și FR NU trec prin traduceri: paginile lor sunt scrise de mână.

## De ce are forma asta

URL-urile fiecărei țări sunt în limba ei (SEO local). Build-ul rescrie căile RO din `site.js` per țară (`build/build.py:100-110`) și etichetele nav/footer (`:30`). Dicționarele au fost unealta cu care s-au seed-uit cele 7 țări de rezervă în iulie–august; fluxul e documentat în `WORKFLOW.md` ca să poată fi repetat.

## Forma

- `path_maps.py` — `FR_TO_<LANG>` și `RO_TO_LANG`: slug RO/FR → slug local. Importat de build prin `sys.path` (`build/build.py:103-108`); **dacă lipsește, build-ul cade tăcut pe `{}` și link-urile rămân în română** — nu îl muta.
- `ui_strings.json` — etichetele nav/footer/selector pe `ro, en, fr, it, es, …`.
- Dicționare: `{lang}.json` (frază FR → frază locală) pentru de/en/es/fr/ie/it/nl; `fr_to_{de,en,es,it,nl}.json`; `fr_to_cnr.json`, `ro_to_cnr.json`, `en_to_cnr.json` (ME = muntenegreană).
- Scripturile fluxului (`WORKFLOW.md`): `seed_from_fr.py`, `extract_fr_phrases.py`, `apply_lang.py`, `localize_country_paths.py` (importă `path_maps`), `audit.py`, `audit_ro_complete.py` (apelat de `mcp/server.py:65`), `audit_lang_complete.py`, `merge_chunks.py`, `rename_paths.py`, `rename_fr_paths.py`, `localize_ro_paths.py`, `patch_site_js.py`, `apply_fr_to_lang.py`, `seed_from_ro.py`, `translate.py`.
- Documente: `WORKFLOW.md` (pașii), `BRIEF.md` / `BRIEF-FR.md` (vocea, ce se traduce), `GLOSSARY.md` (terminologia obligatorie: MBK/PBK/TBK, Passivhaus…).
- Fantomă: `phrases_fr_source.json` numit în `WORKFLOW.md:14` nu există (se generează la pasul 3).
- Restul (136 de fișiere de lucru din iulie–august) e în `_archive/traduceri/translations/`.

## Legat de

- **se leagă cu:** `sablon-partajat.md` (`PB_SLUGS` din `site.js` trebuie ținut de mână în pas cu `path_maps.py`), `tara.md`
- **seamănă dar nu e:** `countries/<cod>/` — paginile traduse sunt acolo, nu aici

## Dacă schimbi asta

- **Mișcă:** `path_maps.py` → link-urile nav/footer pe toate țările non-RO la build; `ui_strings.json` → etichetele nav/footer; dicționarele → doar la o rulare nouă a `apply_lang.py` (nimic automat).
- **Nu mișcă:** RO și FR (texte de mână); `PB_SLUGS` din `site.js` (inline, separat).

## Suprafețe

| Cine | Rol |
|---|---|
| `build/build.py` | citește `path_maps.py`, `ui_strings.json` |
| `mcp/server.py` | rulează `audit_ro_complete.py` |
| Claude | rulează fluxul la o țară nouă |

## Vezi

- Sursa: `translations/WORKFLOW.md`, `translations/path_maps.py`
