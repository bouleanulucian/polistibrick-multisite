---
type: process
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
consumes: [tara, sablon-partajat, deploy]
produces: [dovezi: numere, capturi, coduri HTTP]
---

# verifică

Dovedește că o schimbare e acolo unde trebuie: în sursă, în build, pe local, pe live. Măsoară, nu privi.

## Intrare → Mișcare → Ieșire

Intră o schimbare declarată „gata". Se numără în fișierele construite, se cere serverului, se face captura cu scroll real, se face `curl` pe live. Ies numere și capturi, nu impresii.

## De ce are forma asta

Lecțiile din repo: capturile din panou arată pagina nedesenată; Chrome livrează din cache; serverul ține folderul șters; „am copiat tot" era tăiat la 100 pe lot. Fiecare verificare de mai jos e un răspuns la una din ele.

## Pași

1. În sursă: `grep -c '<marcaj>' countries/<cod>/<pagina>/index.html` — și în cealaltă limbă, dacă schimbarea trebuia să fie în amândouă (RO ≠ FR automat).
2. În build: `python3 build/build.py <cod>` trece fără „nav/footer inconsistent"; `grep -c '<marcaj>' build/<cod>/<pagina>/index.html`.
3. Pe local: `curl -s http://localhost:4710/<pagina>/ | grep -c '<marcaj>'` după repornirea serverului; imaginile: cod HTTP 200 și mărimea în octeți.
4. Vizual: Playwright cu `page.mouse.wheel` (`previzualizeaza.md`, pasul 4); pentru WebGL (vizualizatorul 3D) Chrome headless cu `--use-gl=angle --use-angle=swiftshader`.
5. Pe live: `curl -s "https://<domeniu>/<pagina>/?v=$(date +%s)" | grep -c '<marcaj>'`; rulările: `gh run list --limit 3` toate `success`.
6. Texte străine rămase într-o țară: `python3 translations/audit.py` (leftovers RO/FR); RO complet: `python3 translations/audit_ro_complete.py ro` (și prin `mcp/server.py`, `audit_site`).
7. Paritate după o restructurare: amprentă `find build/<cod> -type f -print0 | sort -z | xargs -0 shasum -a 256` înainte și după, `diff` gol.

Rezervă (gh-pages, nu se mai folosesc): `scripts/verifica-publicarea.py`, `scripts/publica-preview.py`, `scripts/deploy-preview.sh`.

## Dacă schimbi asta

- **Mișcă:** nimic în repo; e o listă de control.
- **Nu mișcă:** —

## Suprafețe

| Cine | Rol |
|---|---|
| Claude | rulează, raportează numerele |
| patronul | primește captura și linkul |

## Vezi

- Obiecte: `../objects/previzualizare-locala.md`, `../objects/deploy.md`
- Sursa: `translations/audit.py`, `build/build.py:491-560`
