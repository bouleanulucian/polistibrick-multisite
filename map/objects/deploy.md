---
type: object
cluster: livrare
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: .github/workflows/cloudflare-pages.yml
---

# Deploy (Cloudflare Pages, domenii)

Un workflow GitHub construiește o țară și o urcă pe proiectul ei Cloudflare Pages. Push pe `main` publică **doar România**; orice altă țară se publică manual, una câte una.

## De ce are forma asta

Decizia din 11.08.2026 (comentariul din workflow, `:25-27`): țările se lansează când sunt gata, nu toate odată la fiecare push. Sitemap-ul ia `lastmod` din `git log` (`build/build.py:364`), de aceea checkout-ul e cu istoric complet (`fetch-depth: 0`, `filter: blob:none`, workflow `:35-44`).

## Forma

- Declanșare: `push` pe `main`/`master` cu schimbări în `countries/**`, `shared/**`, `build/**`, `translations/**`, `cloudflare/**` sau workflow (`:3-11`); `workflow_dispatch` cu input `country` (`:12-17`).
- Matricea: `["ro"]` la push, `[<country>]` la dispatch (`:28`).
- Pași: checkout → Python 3.12 → `python3 build/build.py $COUNTRY` → citește `cloudflare/projects.json` → `wrangler pages project create … || true` → `wrangler pages deploy build/$COUNTRY --project-name=… --branch=main` (`:50-70`).
- Secrete GitHub: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`.
- Proiecte și domenii: `cloudflare/projects.json` — ro → `polistibrick-ro` → polisti.ro; fr → `polistibrick-fr` → polistibrick.fr; en → `polistibrick-uk` → polistibrick.uk; de → `polistibrick-ch` → polistibrick.com; nl → `polistibrick-be` → polistibrick.be; it, es, ie, me.
- Starea domeniilor: **polisti.ro live**; **polistibrick.fr încă pe nameserverele One.com** (ns01/ns02.one.com) — site-ul FR se vede doar pe `polistibrick-fr.pages.dev`; jurnalul în `cloudflare/migrare-fr/STARE-MIGRARE.md` + `dns-snapshot-inainte.txt`.
- Ramura `lansare-fr` e ținută egală cu `main` (`git push -f origin main:lansare-fr`) — istoric, nu mai contează pentru deploy.
- Rezervă: previzualizarea GitHub Pages din august (ramura `gh-pages`, `.gh-pages-worktree/`, `scripts/gh-pages/`, `scripts/deploy-preview.sh`, `scripts/publica-preview.py`, `scripts/verifica-publicarea.py`) pe bouleanulucian.github.io — nu se mai folosește; nu e ștearsă.

Citări: `.github/workflows/cloudflare-pages.yml:3-17,25-28,35-44,50-70`; `cloudflare/projects.json`; `build/build.py:364`

## Legat de

- **se leagă cu:** `tara.md`, `config-tara.md` (`domain_url` din config trebuie să fie același cu domeniul din `projects.json`)
- **seamănă dar nu e:** `scripts/dev-local.sh` (server local vechi, port 8080) — nu e deploy

## Dacă schimbi asta

- **Mișcă:** un push pe `main` cu orice din căile de mai sus → RO live în ~2 minute, chiar dacă ai lucrat la FR. `projects.json` greșit → deploy pe alt proiect.
- **Nu mișcă:** FR și celelalte țări (doar `workflow_dispatch`); polistibrick.fr (DNS la One.com).

## Suprafețe

| Cine | Rol |
|---|---|
| GitHub Actions | rulează |
| `gh` CLI (Claude) | `gh workflow run cloudflare-pages.yml --ref main -f country=fr`, `gh run watch` |
| Cloudflare (cont bouleanu.lc@gmail.com) | găzduiește |
| One.com (doar .fr) | ține încă DNS-ul; patronul trebuie să mute nameserverele |

## Vezi

- Sursa: `.github/workflows/cloudflare-pages.yml`
- Procesul: `../processes/publica.md`
