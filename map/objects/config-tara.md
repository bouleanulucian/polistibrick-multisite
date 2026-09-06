---
type: object
cluster: site
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: countries/<cod>/_config.json
---

# Config de țară

`countries/<cod>/_config.json`: datele care diferă de la o țară la alta și intră în pagini prin placeholders `{{cheie.subcheie}}`.

## De ce are forma asta

Paginile sunt scrise de mână, dar telefonul, adresa, moneda, cheia de formular și URL-ul app-ului de devize nu trebuie căutate prin 49 de fișiere. Build-ul le injectează (`build/build.py:55-110`) și scoate fișierul din output (`build/build.py:598-601`).

## Forma

- `lang`, `country`, `country_name`, `domain`, `domain_url` — și baza canonicului/hreflang (`metadata.hreflang`, `countries/fr/_config.json:79`).
- `company.*` (nume legal, TVA, adresă), `contact.*` (telefon, emailuri, program, social), `team[]`.
- `currency`, `currency_symbol`, `vat_rate`.
- `forms.access_key` (`countries/fr/_config.json:55-56`) — cheia Web3Forms. **Cutia în care ajunge mailul o decide cheia, nu `form_submit_email`** (documentar). Lecția din 13.08.2026 e în `README.md`, secțiunea formulare.
- `legal.*` (director publicație, găzduire, contact confidențialitate), `factory.*`.
- `devis_app.url` / `preview_url` / `pays` (`:81`) — iframe-ul de pe `devis/` / `oferta/`.

## Legat de

- **deținut de:** `tara.md`
- **se leagă cu:** `pagina.md` (placeholders), `deploy.md` (domeniul), app-ul de devize (alt repo, prin `devis_app.url`)

## Dacă schimbi asta

- **Mișcă:** toate paginile țării la următorul build (placeholders, canonical, hreflang, sitemap, robots); formularele (dacă schimbi cheia); iframe-ul de devize.
- **Nu mișcă:** celelalte țări; textul scris de mână în pagini.

## Suprafețe

| Cine | Rol |
|---|---|
| `build/build.py` | citește (`load_config`, `:55`) |
| Claude | editează la cererea patronului |
| Web3Forms | decide destinația mailului după cheie |

## Vezi

- Sursa: `countries/fr/_config.json`, `countries/ro/_config.json`
