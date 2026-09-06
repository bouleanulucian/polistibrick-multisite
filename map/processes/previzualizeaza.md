---
type: process
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
consumes: [tara, previzualizare-locala]
produces: [captură pentru patron]
---

# previzualizează

Arată patronului o schimbare pe local, pe 4700 (RO) sau 4710 (FR), cu o captură care chiar arată pagina desenată.

## Intrare → Mișcare → Ieșire

Intră o schimbare în `countries/` sau `shared/`. Se construiește țara, se repornește serverul, se confirmă că livrează noul, se face captura cu scroll real. Iese captura trimisă patronului și decizia lui.

## De ce are forma asta

De trei ori patronul a spus „nu văd nimic" / „nu merge local": o dată Chrome ținea pagina din cache, de două ori serverul ținea folderul șters de build. Și capturile din panou arătau pagina nedesenată. Fiecare pas de mai jos închide una din aceste capcane.

## Pași

1. `python3 build/build.py <cod>` (`build.md`).
2. Serverul: `preview_list` → `preview_stop <serverId al site-<cod>>` → `preview_start {name: "site-<cod>"}` (definițiile în `RO CMR/.claude/launch.json`; serverul e `serveste-fara-cache.py`, `Cache-Control: no-store`).
3. Confirmă că serverul livrează versiunea nouă, nu cea veche: `curl -s http://localhost:4710/ | grep -c '<marcaj din schimbare>'` (și imaginile noi: `curl -s -o /dev/null -w "%{http_code} %{size_download}" http://localhost:4710/images/…`).
4. Captura: Playwright `browser_run_code_unsafe` — `page.setViewportSize`, `page.goto('http://localhost:4710/?v=' + Date.now())`, apoi `page.mouse.wheel(0, 400)` în buclă până ținta e în ecran, `waitForTimeout`, `page.screenshot({path: 'RO CMR/.playwright-mcp/<nume>.png'})`. Nu `scrollTo`, nu `scrollIntoView` (eroul le resetează).
5. Uită-te la captură tu întâi (Read pe PNG); dacă nu arată ce ai vrut, repară înainte s-o trimiți.
6. Trimite captura patronului (`SendUserFile`) cu o legendă de un rând și spune-i „dă refresh la localhost:4710".
7. Nimic nu se comite ca „publicat" până nu spune el da. Commit local e în regulă; push nu.

## Dacă schimbi asta

- **Mișcă:** portul sau numele serverului → `launch.json` din `RO CMR` (alt proiect).
- **Nu mișcă:** live-ul.

## Suprafețe

| Cine | Rol |
|---|---|
| Claude | rulează |
| patronul | vede în Chrome, decide |

## Vezi

- Obiecte: `../objects/previzualizare-locala.md`
- Sursa: `RO CMR/.claude/launch.json`
