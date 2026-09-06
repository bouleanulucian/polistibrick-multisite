# Schema hărții

Setul închis de tipuri de fișe, etichetele lor și numirea. Când practica și acest fișier nu se pupă, se împacă în aceeași zi.

## Tipuri

| `type:` | Stă la | Poartă |
|---|---|---|
| object | `objects/<slug>.md` | o propoziție, de ce are forma asta, forma (cu citări), legături, „dacă schimbi asta" (mișcă / nu mișcă), suprafețe, sursa |
| process | `processes/<slug>.md` | intrare → mișcare → ieșire, pași numerotați cu citări, consumă / produce (link-uri la obiecte), mișcă / nu mișcă |
| effects | `effects/CONTEXT.md` | catalog „dacă schimbi X, deschide Y" + ce intră din afara repo-ului |

## Etichete (antet YAML)

- `type`: object | process
- `cluster`: site | continut | sablon | date | livrare (doar la object)
- `universe`: live | leftover | ghost
- `status`: stub | verified | stale — `verified` cere `verified_at` (dată) și `verified_on` (commit sau ramură)
- `entity`: calea fișierului care deține adevărul (la object)
- `consumes` / `produces`: liste de slug-uri de obiecte (la process)

## Numire

- Slug-uri kebab-case, în română, fără diacritice în numele fișierelor (`sablon-partajat.md`, `model-casa.md`).
- Citările sunt `cale/relativa/la/rădăcina/repo-ului:linie`. Liniile se re-verifică la fiecare `verified`.
- `_index.md` din `objects/` e generat de `_scripts/regenereaza.sh` din antete. Nu se editează de mână.
- `AGENTS.md` și `routing.md` sunt copii byte-cu-byte ale `CLAUDE.md` din același folder, generate de același script.
