---
type: object
cluster: continut
universe: live
status: verified
verified_at: 2026-09-06
verified_on: main (după fbeb7f6)
entity: shared/images/
---

# Imagini

Două case: `shared/images/` (comune, copiate în fiecare `build/<cod>/images/`) și `countries/<cod>/images/` (doar ale țării; azi doar FR are). Paginile le cer relativ (`images/…`), deci la build ambele ajung în același `images/`.

## De ce are forma asta

Randările celor 48 de modele, produsele, eroul și echipa sunt aceleași în toate limbile — se țin o singură dată. Ce e legat de o limbă (clipurile cu text FR, „presence", „mur") stă la țară.

## Forma

- `shared/images/case/` — 335 fișiere = 48 de modele × ~7 randări, numite `<model>-<incapere>.jpg` (`alba-fatada-strada.jpg`). Numele modelului e cheia: un nume refolosit suprascrie tăcut randările (vezi `model-casa.md`).
- `shared/images/erou/` — `beton.webp` (fundalul eroului), `beton-alb.webp` (același beton, în alb, sub `#livrable` FR), `brick/wall/sip.webp`, `sip.glb`.
- `hero/`, `presence/`, `temoignages/`, `personas/`, `systeme/`, `equipe/`, `construction/`, `polistibrick/`, `polistiwall/`, `polistisip/`, `passive/`, `projets/`, `bundle/`, `icons/`, `usines/`, `montaj|montaje|montaza/`.
- `shared/downloads/<lang>/` + `shared/downloads/shared/` — PDF-uri (Polistiwall, SIP250/300), copiate în `build/<cod>/downloads/` (`build/build.py:576-584`).
- `countries/fr/images/` — `mur/`, `presence/` (multe fișiere de lucru ignorate în git prin `.gitignore`, secțiunea presence), `construction/`, `montage/`.
- Copierea: `build/build.py:571-574` (shared), `:594` (țara, prin `copy_tree`).

## Legat de

- **deținut de:** repo-ul (shared) / `tara.md` (countries/<cod>/images)
- **se leagă cu:** `model-casa.md` (case/), `pagina.md` (referințele relative)
- **seamănă dar nu e:** `media/` (video sursă pentru unelte, nu ajunge pe site); `campanii/media/` (reclame)

## Dacă schimbi asta

- **Mișcă:** shared → toate build-urile; `countries/fr/images` → doar FR. O imagine ștearsă din `case/` lasă un card de catalog fără poză în RO ȘI FR.
- **Nu mișcă:** paginile (căile relative rămân valabile); cache-ul CDN e pe 30 de zile (`_headers`, `build/build.py:429`) — o imagine înlocuită sub același nume poate rămâne veche la vizitatori.

## Suprafețe

| Cine | Rol |
|---|---|
| Claude | adaugă randări (Blender, nu AI — regula patronului), texturi |
| `build/build.py` | copiază |
| Cloudflare | cache 30 de zile |

## Vezi

- Sursa: `shared/images/`, `countries/fr/images/`
