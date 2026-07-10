# Translation workflow (FR template → other countries)

France (`countries/fr/`) is the **reference site** (32 pages). Other countries start from `_config.json` only until seeded.

## Quick start — new country (e.g. EN)

```bash
# 1. Ensure countries/en/_config.json exists (domain, contact, lang, forms)

# 2. Copy FR structure + pages (keeps EN config)
python3 translations/seed_from_fr.py en

# 3. Extract French phrases to translate
python3 translations/extract_fr_phrases.py --out translations/phrases_fr_source.json

# 4. Fill translations/en.json — keys = French phrases, values = English text
#    (see BRIEF.md + GLOSSARY.md for tone and terminology)

# 5. Apply translations + build
python3 translations/apply_lang.py en
python3 build/build.py en
```

Preview: `python3 -m http.server 8080` → `http://localhost:8080/build/en/`

## What gets translated automatically

| Layer | File | How |
|-------|------|-----|
| Nav / footer / country picker | `translations/ui_strings.json` | `build.py` injects per `lang` in `_config.json` |
| Page body | `translations/{lang}.json` | `apply_lang.py` string replace (skips `<script>`, `<style>`, comments) |
| Contact, legal, forms | `countries/{code}/_config.json` | Edit manually per country |

## URL paths

Each country uses **URL slugs in its own language** (SEO local).

| Country | Example paths |
|---------|----------------|
| RO | `/pentru/proprietari/`, `/oferta/`, `/despre/` |
| FR | `/pour/proprietaires/`, `/devis/`, `/a-propos/` |
| IT | `/per/proprietari/`, `/preventivo/`, `/chi-siamo/` |
| EN | `/for/homeowners/`, `/quote/`, `/about/` |
| ES | `/para/propietarios/`, `/presupuesto/`, `/sobre-nosotros/` |

After seeding from FR, localize folders:

```bash
python3 translations/localize_country_paths.py it   # one country
python3 translations/localize_country_paths.py all  # it en es nl de ie
```

Maps live in `translations/path_maps.py`. `build.py` rewrites shared `site.js` (RO paths) → local paths per lang.

## Forms (live email)

Add Web3Forms key in each country's `_config.json`:

```json
"forms": { "access_key": "YOUR_KEY", "subjects": { ... } }
```

## Existing tools

- `translations/BRIEF.md` — brand voice, what to translate
- `translations/GLOSSARY.md` — MBK/PBK/TBK, Passivhaus, etc.
- `translations/audit.py` — find untranslated RO/FR leftovers
- `translations/merge_chunks.py` — merge chunked translation JSON files
