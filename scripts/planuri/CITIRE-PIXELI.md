# Citirea planurilor pe pixeli — stilul de lucru

Validat pe ELVA (proiect 88-77, 18.08.2026), după lecția serii de 17.08
(radiografia întâi, nimic inventat, comparația înainte de „gata").
Sculele: `radiografie.py` (țigle, ziduri, profil goluri, rasterizare,
suprapunere) + modelul per proiect (`elva.py` ca șablon).

## Ordinea fixă

1. **Radiografia întâi.** Planșa de contact a proiectului → poza cu planul →
   `tigla()` 3×3 la 4× → SE CITEȘTE fiecare țiglă. Colțurile ambigue primesc
   zoom dedicat cu **caroiaj metric desenat peste** (nu se ghicește din poza
   mică). Dulapurile cu X nu-s pereți; arcul = ușă; liniile subțiri = mobilă.

2. **Scara din două surse independente.** Masca de ziduri (`ziduri()` —
   deschidere morfologică: cerneala groasă rămâne, mobila/textul dispar,
   componentele lipite de margine se șterg) → caseta ei se împarte la DOUĂ
   cote scrise diferite (lățime/adâncime). Sub 0,5% diferență = etalon bun.
   A treia sursă = ariile scrise, la rezolvare.

3. **Inventarul liniilor.** Măștile se separă pe direcții (element morfologic
   vertical/orizontal ~0,9 m), profilele dau fiecare linie cu poziția și
   întinderea ei. Liniile scurte pot lipsi — se caută la zoom, nu se inventează.

4. **Golurile, numeric.** `profil()` pe fiecare perete (exterior și interior),
   pe întinderea lui reală: golurile >0,4 m = uși/ferestre, cu poziții și
   lățimi măsurate. Ușile interioare ies din aceleași scanări (unde, între ce
   camere). Nicio fereastră „din burtă".

5. **Aria nemarcată se deduce, nu se inventează.** Suma etichetelor vs. totalul
   scris în descriere → diferența e camera fără etichetă (la 88-77: centrala,
   4,2 m²). Intră ca țintă MOALE în rezolvare.

6. **Grila se rezolvă pe DOUĂ surse deodată**: ariile scrise (greutate mare,
   exacte) + pozițiile măsurate ale axelor (greutate mică — „nu fugi de
   pixeli"). Doar ariile NU ajung: mai multe grile dau aceleași arii — asta a
   produs „corect pe cifre, fals vizual" la 80-49. Camerele = celule între
   fețe derivate din axe; ușile se leagă de FEȚELE REZOLVATE, nu de cote brute.

7. **Sistemul nostru de pereți**: 38 exterior (crescut spre exterior — fețele
   interioare rămân pe pozițiile lor), 13 compartimentări. Peretele de 38
   merge pe fundul porticului/teraselor scobite — unde se schimbă temperatura.

8. **Porțile de „gata"** (toate trei, în ordinea asta):
   - ariile: max |eroare| ≤ 0,01 m² pe tot ce e scris; `verifica()` = TRECE;
   - **suprapunerea metrică** (`rasterizeaza()` + ancorare pe fețele
     interioare, FĂRĂ scalare pe casete — casetele pot conține terase!):
     negru = amândoi, roșu = doar eu, gri = doar ei; se citește vizual —
     compartimentările trebuie să fie negre, cu derive doar unde ariile au
     cerut; IoU pe linii subțiri e sensibil la ±1 px, nu e cifra unică;
   - planul meu **lângă** original, la aceeași înălțime (`alaturi()`), privit.

## Capcane deja plătite

- Caseta măștii ≠ casa: cotele scrise pot include terase/stâlpi (17,15 la
  88-77 era CU terasa de est). Ancorarea se face pe fețe, nu pe casete.
- Liniile perpendiculare murdăresc profilele — separă întâi direcțiile.
- O „linie groasă" poate fi perete + mobilă lipită (vanity la 88-77, −25 cm).
- Camerele deschise (bucătărie ↔ living) au nevoie de pasaj nedesenat ca să
  treacă verificarea circulației.
- `verifica()` cere ușa CUPRINSĂ în ambele camere: după rezolvare, ușile se
  recalculează din fețe, cu 8 cm siguranță.
