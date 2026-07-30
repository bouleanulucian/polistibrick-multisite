# Plan: replicare redesign homepage pe toate țările + publicare live

Pachetul FR validat local (30.07.2026): font unic Inter + titluri bold uppercase mici,
teaser contur roșu + comutare instant, MORPH șters, PASSIF șters, „Pour Qui ?",
texte mărunte șterse (eyebrows/note/paragrafe), titlu CINQ nou, metric arhitect scurt,
video hero 18s (toate țările au deja fișierele).

- [x] Diff FR salvat ca spec (scratchpad/fr-homepage.diff — 15 schimbări)
- [x] Commit FR + css + build.py + hero assets pe main (checkpoint)
- [ ] 8 agenți în paralel: de, en, es, ie, it, me, nl, ro — aceleași schimbări in-place,
      text tradus în limba țării (de/nl = încă placeholder FR → copiază franceza verbatim)
- [ ] Verificare markere pe toate țările (morph=0, passif=0, eyebrows=0, Inter 800, p>0.06)
- [ ] Build toate țările (explicit: de en es fr ie it me nl ro — NU „fr 2")
- [ ] Commit main (toate țările)
- [ ] Deploy: .gh-pages-worktree (fetch+rebase, fără force) → push gh-pages
- [ ] Verificare live per țară (curl: titlu CINQ nou, absență passif/morph)
