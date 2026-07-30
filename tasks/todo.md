# Plan: replicare redesign homepage pe toate țările + publicare live

Pachetul FR validat local (30.07.2026): font unic Inter + titluri bold uppercase mici,
teaser contur roșu + comutare instant, MORPH șters, PASSIF șters, „Pour Qui ?",
texte mărunte șterse (eyebrows/note/paragrafe), titlu CINQ nou, metric arhitect scurt,
video hero 18s (toate țările au deja fișierele).

- [x] Diff FR salvat ca spec (scratchpad/fr-homepage.diff — 15 schimbări)
- [x] Commit FR + css + build.py + hero assets pe main (checkpoint)
- [x] 8 agenți în paralel: de, en, es, ie, it, me, nl, ro — toate au raportat verificări curate
- [x] Verificare independentă pe toate țările — toate curate
- [x] Build toate 9 țările (build.py are acum versionare pe hash de conținut — mai bună decât ?v= manual)
- [x] Commit main: 576b850 (+ 776022a — ro uitat din lista explicită de git add, prins la re-verificare)
- [x] Deploy gh-pages: 9ba94ab (fetch+rebase ok, 325 fișiere)
- [x] Verificare live: toate 9 țările servesc versiunea nouă (morph=0, passif=0, Inter 800, titlu nou) — 31.07.2026

## Review
Redesignul FR replicat pe toate limbile prin 8 agenți paraleli, fiecare cu verificare grep +
re-verificare independentă centrală. de=Elveția, nl=Belgia (francofone → franceza verbatim, corect).
Localizări: For Who? / ¿Para quién? / Per chi? / Za koga? / Pentru cine?
Rămas pe viitor: font unic pe sub-pagini (site.css folosește încă Cormorant) — „după ce terminăm îl faci pe tot".
