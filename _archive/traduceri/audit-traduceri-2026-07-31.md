# Audit final de traduceri — toate modificările din 31.07.2026, pe 9 țări

## Ce s-a schimbat azi (16 commit-uri, ~54 fișiere/țară)
1. **Homepage** — font unic Inter, MORPH + PASSIF șterse, „Pour Qui ?", texte mărunte curățate,
   carduri slider pe 1 rând, titlu Cinq nou, buton hero → `#pour`, opțiune „Auto-constructeur" ștearsă
2. **Pagina proprietari** — eyebrow „cei care comandă" (nu „construiesc singuri"), calculatorul refăcut
   (valori per țară, etichete, unități, notă cu surse), buton → `#calculator`, textul „economisiți X%"
3. **FAQ** — răspunsul „am nevoie de constructor specializat" rescris (fără scara „devii montator agreat")
4. **Produse MBK/PBK/TBK** — scara de verde, Premium/Pasiv/Pasiv Plus, greutăți cofraj 25/27/29,
   beton 12-25 cm + nota „grosimi pentru beton de 15 cm", eticheta „Greutate cofraj"
5. **Certificări** — CSTB scos peste tot, titlu în limba țării, descriere fără organism/țară
6. **Arhitecți** — „Certificat technique" (fără CSTB), enumerarea rapoartelor
7. **Deviz** — configuratorul doar la clic, `#generator` eliminat

## Riscul de acoperit
Multe texte au fost scrise/rescrise de agenți în 6 limbi. Sesiunea a scos deja la iveală
titluri rămase în FR pe EN/IE, texte IT pe ES, română pe ME. Trebuie o trecere finală,
țară cu țară, care verifică LIMBA și SENSUL, nu doar prezența stringurilor.

## Plan
- [ ] Echipa A (9 agenți, unul per țară): audit + reparare pe toate cele 7 zone de mai sus
- [ ] Echipa B (9 verificatori): relectură adversarială, de pe disc, fără să creadă raportul A
- [ ] Verificare centrală (eu): grep pe tipare de limbă greșită + build
- [ ] Build 9 țări + publicare main + gh-pages
- [ ] Verificare live per țară

## Referință limbi
| cod | piață | limba corectă |
|---|---|---|
| fr | Franța | franceză |
| de | **Elveția** | franceză (netradus — franceza E corectă) |
| nl | **Belgia** | franceză (netradus — franceza E corectă) |
| en | **Marea Britanie** | engleză |
| ie | Irlanda | engleză |
| es | Spania | spaniolă |
| it | Italia | italiană |
| ro | România | română |
| me | Muntenegru | muntenegreană (alfabet latin) |
