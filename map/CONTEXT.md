# map — cum se umblă prin hartă

Fluxul într-o linie: întrebarea alege raftul; deschizi o fișă, nu un folder.

| Raft | Job | Intrare | Ieșire | Ce verifică omul |
|---|---|---|---|---|
| `objects/` | spune ce e un lucru și ce mai mișcă dacă îl schimbi | întrebarea „ce e X?" | o fișă cu citări `cale:linie` | citarea duce la sursă, nu la un eseu |
| `processes/` | spune cum se face o mișcare care se repetă | întrebarea „cum fac Y?" | pași numerotați cu citări | pașii pot fi rulați fără să întrebi pe nimeni |
| `effects/` | spune ce se rupe | o schimbare plănuită | lista de fișe de deschis | „nu mișcă" numește vecinul greșit |

Fabrica (stabil): `_meta/schema.md`, `_templates/`.
Produs (se schimbă cu repo-ul): fișele din `objects/` și `processes/`, `effects/CONTEXT.md`.

## Reguli

- O fișă e `verified` doar cu dată, commit și citări. Altfel e `stub` sau `stale`. O dată sigură și greșită e mai rea decât lipsa ei.
- Codul bate comentariul; dacă nu se pupă, fișa spune asta și citează codul.
- Un fapt are o singură casă. Dacă îl găsești în două fișe, una devine link.
- Fișele nu copiază comportamentul „as-built" din cod; arată spre fișierul care îl deține.
- Testul rece: un agent fără memorie deschide `CLAUDE.md` de la rădăcină, apoi `map/CLAUDE.md`, apoi o fișă, și poate spune ce e X și ce mișcă X. Dacă nu poate, se mută sau se sparge un fișier, nu se scrie o explicație în plus.
- Bugetul: rădăcină + `map/CLAUDE.md` + o fișă ≈ 2 000–8 000 de tokeni.
