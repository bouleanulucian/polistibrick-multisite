# _archive — ce nu mai e pe drumul principal

Mutat pe 06.09.2026 (restructurare ICM). Tot ce e aici se citește, nu se editează. Nimic din repo, din workflow, din `launch.json`, din skill-uri sau din MCP-ul lui Cursor nu mai pomenește aceste fișiere (verificat înainte de mutare; build-ul RO și FR a ieșit identic, fișier cu fișier, înainte și după).

| Folder | Ce e | De unde vine | Când a fost viu |
|---|---|---|---|
| `traduceri/` | cele 12 scripturi de pasaj ES/ME care stăteau ascunse în rădăcină (`.translate_*`, `.rebuild_me_*`, `.fix_me_priority`), `tmp_ro_fr_map.json`, auditul de traduceri din 31.07 și `lang-errors.json` (fost `tasks/`) | rădăcină, `tasks/` | iulie–august 2026 |
| `traduceri/translations/` | 136 de fișiere de lucru: chunk-uri, batch-uri, `remaining_*`, `still_missing_*`, `extra_*`, scripturile `apply_*`/`complete_*`/`sync_*`/`extract_*`/`merge_*` de o singură folosință, `leftovers_100/`, `chunks/` | `translations/` | iulie–august 2026 |
| `mercury-hero-iulie/scripts/` | patch-urile homepage-ului „mercury" și ale video-ului hero vechi (`patch-mercury-*`, `patch-hero-webm`, `optimize-*-media.sh`, `encode-hero-from-master.sh`, `extract-mercury-css.py`) | `scripts/` | 5 iulie 2026 |
| `muntenegru-august/` | `reface-me-din-fr.py`, `repara-me-cod.py`, `texte-me.py` — refacerea site-ului ME | `scripts/` | 10 august 2026 |
| `pre-multisite/` | `fr/` (o imagine rămasă de la site-ul FR de dinainte de multisite), `landing/index.html`, `apps/README.md` (descrierea legăturii cu app-ul de devize) | rădăcină | iunie–iulie 2026 |
| `_neurmarite/` | ignorat în git: `masters/` (video 4K sursă pentru hero, 99 MB), `tmp-hero-web/` (fost `.tmp/`), `referinte-ig/` (planșe Instagram descărcate pentru planuri), `graphify-out/` (harta graphify din 1 august) | rădăcină | iulie–august 2026 |

Ce a RĂMAS viu în `translations/`: `WORKFLOW.md`, `BRIEF.md`, `BRIEF-FR.md`, `GLOSSARY.md`, `path_maps.py` și `ui_strings.json` (citite de `build/build.py`), dicționarele `{lang}.json`, `fr_to_*.json`, `*_to_cnr.json`, și scripturile numite în `WORKFLOW.md` (`seed_from_fr`, `extract_fr_phrases`, `apply_lang`, `localize_country_paths`, `audit*`, `merge_chunks`, `rename*`, `patch_site_js`, `translate`).

Dacă ai nevoie de ceva de aici înapoi: `git mv` la loc și adaugă fișa în `map/`.
