---
type: object
cluster: livrare
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: /Users/polistibrick/Desktop/Aplicatii site web/RO CMR/.claude/launch.json
---

# Previzualizarea locală (serverele pe 4700 / 4710)

Patronul vede orice schimbare pe local înainte să se publice. Serverele NU stau în acest repo: sunt definite în **alt proiect**, `RO CMR/.claude/launch.json`, și servesc `build/ro` și `build/fr` de aici.

## De ce are forma asta

Sesiunile Claude pornesc din `RO CMR` (proiectul-mamă), cu `polistibrick-multisite` ca folder de lucru adițional; `launch.json` al panoului de previzualizare stă acolo. Serverul e un script propriu, `RO CMR/.claude/serveste-fara-cache.py`, cu `Cache-Control: no-store`, pentru că Chrome ținea pagina veche și patronul vedea „nu s-a schimbat nimic".

## Forma

- `site-ro` → port 4700 → `polistibrick-multisite/build/ro`
- `site-fr` → port 4710 → `polistibrick-multisite/build/fr`
- `site-fr-varianta` → port 4711 → `build/fr-varianta` (folder de experimente, poate lipsi)
- Build-ul șterge și recreează `build/<cod>` (`build/build.py:566-569`) → procesul de server ține inodul vechi și livrează gol sau vechi. **După fiecare build: `preview_stop` pe server, apoi `preview_start`.**
- Confirmare că serverul livrează noul: `curl -s localhost:4710/ | grep -c '<un marcaj din schimbare>'`.
- Captura de ecran: Playwright (`browser_run_code_unsafe`) cu `page.mouse.wheel` în buclă până secțiunea intră în ecran — eroul face scroll-jacking, `scrollTo`/`scrollIntoView` se resetează la 0; capturile din panou sau din Chrome headless prind pagina nedesenată. Fișierele în `RO CMR/.playwright-mcp/`.

## Legat de

- **se leagă cu:** `tara.md` (`build/<cod>`), `../processes/previzualizeaza.md`
- **seamănă dar nu e:** `scripts/dev-local.sh` (server vechi pe 8080, cu app-ul de devize pe 3100) — rezervă

## Dacă schimbi asta

- **Mișcă:** dacă redenumești `build/` sau `build/<cod>`, `launch.json` din `RO CMR` se rupe (pointer extern, nu îl vede niciun grep din acest repo).
- **Nu mișcă:** nimic din repo.

## Suprafețe

| Cine | Rol |
|---|---|
| panoul de previzualizare (Claude) | `preview_start {name: "site-fr"}` |
| patronul | deschide localhost:4710 în Chrome |
| Playwright | capturi cu scroll real |

## Vezi

- Sursa: `RO CMR/.claude/launch.json`, `RO CMR/.claude/serveste-fara-cache.py` (alt proiect — se citesc, nu se editează de aici)
