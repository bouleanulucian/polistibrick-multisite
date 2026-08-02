# Studio Testimoniale

Unealtă locală pentru pus testimoniale pe site — video sau text — fără să atingi cod.

## Pornire

```bash
python3 tools/testimonial-studio/server.py
```

Se deschide singură în browser, pe http://localhost:4800

## Cum merge

1. **Alegi tipul** — video sau doar text
2. **Tragi videoclipul** în casetă. Unealta îl comprimă pentru web (dintr-un fișier
   de 19 MB face ~6), îi normalizează sunetul (înregistrările de pe șantier sunt slabe),
   scoate un poster și **transcrie automat ce se vorbește**
3. **Corectezi transcrierea** — recunoașterea greșește constant numele de firme și „Polistibrick"
4. **Completezi datele** — nume, firmă, citatul de pe card, trei cifre care conving
5. **ALEGI ȚĂRILE** — fără asta butonul de publicare rămâne blocat. Îți scrie negru pe alb
   pe ce piețe se va publica, înainte să apeși
6. **Completezi textele pe fiecare limbă** — apar doar limbile țărilor alese.
   Dacă nu vrei să traduci manual, un buton îți copiază cererea gata scrisă pentru Claude
7. **Publici** — o confirmare finală îți listează țările, apoi scrie în paginile lor

## Ce NU face

Nu publică pe internet. Scrie doar în `countries/` pe calculatorul tău.
Ca să ajungă pe live, rămâne pasul obișnuit:

```bash
python3 build/build.py fr ro
```

apoi publicarea pe git.

## Ce-i trebuie

- `ffmpeg` (îl ai)
- `faster-whisper` pentru transcriere automată (îl ai). Fără el, restul merge,
  doar transcrierea nu — scrii subtitrarea de mână.

## Unde ajung fișierele

- video + poster + subtitrări → `countries/<țară>/images/<pagina-testimoniale>/`
- cardul → primul din grila de pe pagina de testimoniale a fiecărei țări alese

Fiecare testimonial are un identificator. Dacă publici din nou același, îl înlocuiește
pe cel vechi în loc să-l dubleze.

## Poze de șantier

Merg în trei feluri:

- **doar poze** (testimonial text, fără video) — prima poză devine imaginea mare a cardului,
  restul apar ca miniaturi sub citat
- **video + poze** — videoclipul sus, pozele ca miniaturi dedesubt
- **doar video** — cum era

Le tragi în caseta a doua, poți alege mai multe deodată, și le scoți cu × dacă te răzgândești.
Sunt redimensionate automat pentru web (max 1400 px lățime).
