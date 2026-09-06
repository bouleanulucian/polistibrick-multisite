---
type: process
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
consumes: [tara, deploy]
produces: [site live]
---

# publică

Urcă pe live ce a văzut deja patronul pe local. RO pleacă automat la push pe `main`; FR se pornește de mână.

## Intrare → Mișcare → Ieșire

Intră `main` local, curat, cu build-ul văzut pe 4700/4710. Se împinge pe GitHub, workflow-ul construiește și urcă pe Cloudflare Pages. Iese site-ul live, confirmat cu `curl`.

## De ce are forma asta

Push-ul publică România chiar dacă ai lucrat numai la Franța (workflow `:3-11`, `:28`). De aceea pasul 2 e obligatoriu: uită-te ce pleacă pe RO înainte să apeși.

## Pași

1. Patronul a spus „publică" pentru schimbarea asta, după ce a văzut-o pe local (`previzualizeaza.md`). Fără OK, nimic.
2. Ce pleacă: `git status --short` (curat) și `git diff origin/main..main --stat`; pe RO: `git diff origin/main..main -- countries/ro/ shared/ | grep '^[+-][^+-]'`. Dacă apare ceva neașteptat pe RO, oprește-te și întreabă.
3. `git push origin main` (→ RO se publică singur; `.github/workflows/cloudflare-pages.yml:28`). Apoi `git push -f origin main:lansare-fr` (ramura ținută egală).
4. FR: `gh workflow run cloudflare-pages.yml --ref main -f country=fr` (`:12-17`).
5. Așteaptă: `gh run list --limit 3` → `gh run watch <id> --exit-status` pentru fiecare rulare (RO ~2 min, FR ~2 min).
6. Confirmă pe live cu un marcaj din schimbare, cu cache-buster: `curl -s "https://polistibrick-fr.pages.dev/?v=$(date +%s)" | grep -c '<marcaj>'`; RO: `curl -s "https://polisti.ro/?v=$(date +%s)" | grep -c '<marcaj>'`. Imagini noi: `curl -s -o /dev/null -w "%{http_code}" <url>`.
7. Spune patronului ce e live, cu linkurile: polisti.ro; polistibrick-fr.pages.dev (polistibrick.fr rămâne pe One.com până mută nameserverele).

## Dacă schimbi asta

- **Mișcă:** orice push pe `main` cu `countries/**`, `shared/**`, `build/**`, `translations/**`, `cloudflare/**` → RO live.
- **Nu mișcă:** FR sau alte țări fără `workflow_dispatch`; domeniul polistibrick.fr.

## Suprafețe

| Cine | Rol |
|---|---|
| Claude | rulează pașii, doar la comanda patronului |
| GitHub Actions + Cloudflare | construiesc și urcă |
| patronul | dă OK-ul; vede live |

## Vezi

- Obiecte: `../objects/deploy.md`, `../objects/tara.md`
- Sursa: `.github/workflows/cloudflare-pages.yml`, `cloudflare/projects.json`
