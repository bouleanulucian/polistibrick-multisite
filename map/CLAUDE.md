# map — harta sistemului polistibrick-multisite

Ce e fiecare lucru din repo, cum se mișcă, și ce mai mișcă dacă îl schimbi. Repo-ul rămâne sursa adevărului; harta îl citează, nu îl rescrie.

## Cum se citește

1. Ai o întrebare „ce e X?" → `objects/_index.md` → fișa lui X (un fișier, citează sursa).
2. Ai o întrebare „cum fac Y?" → `processes/<verb>.md`.
3. Ai o întrebare „dacă schimb X, ce se rupe?" → `effects/CONTEXT.md`.
4. Nu deschide tot folderul `objects/`: catalogul există ca să nu fie nevoie.

## Numele care se ciocnesc (cuvântul patronului = fișierul)

| Se spune | În fișiere |
|---|---|
| acasă, prima pagină | `countries/<cod>/index.html` |
| erou, robotul cu cele 3 produse | secțiunea `.h4` `#heroSection` (stilul are id-ul `hero4`) |
| „un singur cofraj", pagina care creează lumină | `#livrable` (doar FR, între erou și video) |
| video cu peretele, „Dans le mur", replica roșie | `#cinq` / `#cinqVideo` / `#cinqReplica` |
| catalog, proiecte, modele, case | `proiecte/` (RO) = `projets/` (FR); 48 de modele; `shared/images/case/` |
| ofertă, devis | `oferta/` (RO) = `devis/` (FR): iframe spre app-ul de devize, alt repo |
| presence | imaginile și clipurile fabricii (`images/presence/`) |
| mercury | stilul vechi al homepage-ului; `shared/css/mercury-home.css` încă versionat de build |
| ME, cnr | Muntenegru, muntenegreană |
| „publică" | RO automat la push pe main; FR manual prin workflow |

## Universuri

- **viu**: RO, FR, `build.py`, workflow-ul, `path_maps.py`, `ui_strings.json`, `scripts/planuri/`.
- **rezervă**: cele 7 țări seed-uite (en, it, es, nl, de, ie, me — 28 pagini, design de dinainte de 24.08, nepublicate), previzualizarea gh-pages, `mercury-home.css`, `DEPLOY.md`.
- **fantomă**: `docs/` promis de README-ul vechi, `translations/phrases_fr_source.json` numit în `WORKFLOW.md` dar inexistent, orice script care „regenerează" `PB_SLUGS` din `site.js` (nu există; harta e inline).

## Unde e ce

| Folder | Ține |
|---|---|
| `objects/` | fișele substantivelor + `_index.md` |
| `processes/` | fișele verbelor: build, publică, previzualizează, model nou, țară nouă, verifică |
| `effects/CONTEXT.md` | indexul „dacă schimbi X, deschide Y" + ce intră din afara repo-ului |
| `_meta/schema.md` | tipurile de fișe și etichetele lor |
| `_templates/` | fișă goală de obiect și de proces |
| `_scripts/regenereaza.sh` | reface `_index.md` din antete și gemenii `AGENTS.md`/`routing.md` |

`AGENTS.md` și `routing.md` din acest folder sunt copii generate ale acestui fișier. Nu se editează de mână.
