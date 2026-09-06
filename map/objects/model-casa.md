---
type: object
cluster: continut
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: countries/ro/proiecte/index.html
---

# Model de casă (proiect, casă din catalog)

Un model (Alba, Aria, Elva… 48 în total) trăiește în patru locuri, legate doar prin nume. Patronul spune „proiect", „casă", „model"; pe site e „proiecte" (RO) / „projets" (FR).

## De ce are forma asta

Catalogul e scris de mână în RO și FR (prețuri la cost Franța pe FR), randările sunt comune, planul și prețul se calculează local, reclamele se produc separat. Nu există o bază de date: **numele modelului e cheia** peste toate patru.

## Forma

1. Catalog: `countries/ro/proiecte/index.html` + `countries/fr/projets/index.html` — 48 de carduri `.case-photo` (`projets/index.html:374`), fișa `#detail-N` (`:389`) cu prețul pe cele trei sisteme, pilula `.var-nota` „prețul e al sistemului, nu al casei" (`:385`) și popupul `#notaModal`.
2. Randări: `shared/images/case/<model>-<incapere>.jpg` (≈7 pe model; 335 fișiere).
3. Plan + preț: `scripts/planuri/<model>.py` (46 de modele au script), `cofraj.py` (prețul cofrajului în trei sisteme, `scripts/planuri/cofraj.py:3`), `coteaza.py`, `radiografie.py`; metoda în `scripts/planuri/CITIRE-PIXELI.md` (radiografia întâi, nimic inventat).
4. Reclame: `campanii/reclame-proiecte/<model>/` (neurmărit în git; skill-ul `reclame-video-case` livrează aici).

Regulile de coerență (skill `case-polistibrick`): planul, randările și textul descriu aceeași casă; prețurile afișate = cofrajul, nu casa finită.

## Legat de

- **deținut de:** `pagina.md` (catalogul), `imagini.md` (case/)
- **se leagă cu:** `scripts/planuri/`, `campanii/`, app-ul de devize (alt repo, folosește aceleași prețuri de cofraj)
- **seamănă dar nu e:** catalogul celor 7 țări de rezervă (28 de pagini vechi; nu are cele 48 de modele)

## Dacă schimbi asta

- **Mișcă:** RO ȘI FR împreună (48 = 48, aceleași modele, aceeași ordine); `case/` dacă schimbi numele; `planuri/<model>.py` dacă schimbi planul; reclamele existente devin vechi dacă schimbi prețul.
- **Nu mișcă:** celelalte 7 țări; `shared/js/site.js`; app-ul de devize (nu citește catalogul).

## Suprafețe

| Cine | Rol |
|---|---|
| Claude | scrie cardurile, randează (Blender), calculează prețul |
| patronul | validează pe local; decide prețul |
| vizitatorul | catalog + popup + „Vezi tot proiectul" |

## Vezi

- Sursa: `countries/fr/projets/index.html`, `scripts/planuri/CITIRE-PIXELI.md`
- Procesul: `../processes/model-nou.md`
