---
type: process
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
consumes: [model-casa, imagini, pagina]
produces: [card în catalogul RO și FR, randări, plan, (reclame)]
---

# model nou (sau modificarea unui model)

Adaugă o casă în catalog în toate cele patru locuri în care trăiește un model, sub același nume.

## Intrare → Mișcare → Ieșire

Intră un plan (PDF sau poză) și numele. Se citește planul pe pixeli, se calculează prețul cofrajului, se randează, se scrie cardul în RO și FR. Iese catalogul cu 49 de modele în ambele limbi și, dacă se cere, reclamele.

## De ce are forma asta

Nu există bază de date: numele leagă catalogul, randările, planul și reclamele. Un nume deja folosit suprascrie tăcut cele ~7 randări ale altei case. Iar RO și FR sunt copii separate: 48 = 48 se ține de mână.

## Pași

1. Numele: `grep -c "<Nume>" countries/ro/proiecte/index.html countries/fr/projets/index.html` și `ls shared/images/case | grep -i <nume>` — ambele zero, altfel alt nume.
2. Planul: `scripts/planuri/<nume>.py` după `scripts/planuri/CITIRE-PIXELI.md` (radiografia întâi cu `radiografie.py`, nimic inventat, comparația înainte de „gata"); `elva.py` e șablonul.
3. Prețul: `scripts/planuri/cofraj.py` (prețul cofrajului în trei sisteme, `:3`); pe FR prețurile sunt la cost Franța (×1,19–1,23 față de RO — vezi memoria `lansare-fr-traducere`).
4. Randările: Blender headless pe Cycles, nu AI (regula patronului); `shared/images/case/<nume>-<incapere>.jpg`; skill-ul `case-polistibrick`: planul, randările și textul descriu aceeași casă.
5. Cardul: copiază un card existent din `countries/ro/proiecte/index.html` (`.case-photo` + `#detail-N`) și pune-l în aceeași poziție în `countries/fr/projets/index.html`; numerotarea `detail-N` continuă.
6. `python3 build/build.py ro fr` → `previzualizeaza.md` pentru amândouă → patronul validează.
7. `publica.md`.
8. Opțional, la cerere: reclamele cu skill-ul `reclame-video-case` → `campanii/reclame-proiecte/<nume>/`.

## Dacă schimbi asta

- **Mișcă:** RO și FR împreună; `case/`; `planuri/`; reclamele vechi ale modelului (prețul rostit).
- **Nu mișcă:** celelalte 7 țări; `site.js`; app-ul de devize.

## Suprafețe

| Cine | Rol |
|---|---|
| Claude | citește planul, calculează, randează, scrie cardurile |
| patronul | dă numele și validează prețul |

## Vezi

- Obiecte: `../objects/model-casa.md`, `../objects/imagini.md`
- Sursa: `scripts/planuri/CITIRE-PIXELI.md`, `countries/fr/projets/index.html`
