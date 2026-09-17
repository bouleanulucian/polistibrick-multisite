#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prețurile pieței FRANCEZE pe countries/fr/ — 11.09.2026.

De ce: site-ul francez publica prețurile pieței din ROMÂNIA, traduse, de cele mai
multe ori fără să scrie că sunt românești. Un client francez citea «maison clé en
main 900–1 350 €/m²» și credea că poate construi în Franța la prețul ăsta. Media
oficială franceză e aproape dublă.

CIFRELE FRANCEZE (TTC, pe m² construit, fără teren) — aceleași ca pe fișele client:
  gros œuvre                700–1 100 €/m²   Renovbox 2026, prix-travaux-m2
  hors d'eau hors d'air   1 000–1 400 €/m²   Renovbox 2026 + regula «gros œuvre = 45–55 %»
  clé en main standard    1 700–2 200 €/m²   EPTB/SDES: media oficială 1 914 €/m² (2024)
  clé en main premium     2 300–3 000 €/m²   Constructeur-maison 2026
  perete clasic francez     329 €/m² de mur  = enduit int. 32 + parpaing posé 126
                                               + chaînages 16 + enduit ext. 25 + ITE 130
  peretele nostru           182 / 125 / 86 €/m² de mur  (Brick / Wall / SIP)
  zidărie pusă în operă     parpaing 96–156 · brique 120–190 · béton cellulaire 100–160 €/m² TTC
                            (Kelyseo 2026; Travaux.com 2026 pentru béton cellulaire)
  electricitate             0,29 €/kWh       Eurostat, semestrul 2 2025

CE NU SE ATINGE:
  · grila noastră de preț (205–280 / 157–205 / 229–287 €/m²) — e decizia patronului;
  · fabrica din Balș, presa românească, proiectele construite în România — sunt adevărate;
  · exemplele de șantier 1 223 / 1 039 / 1 100 €/m² — rămân, dar scrie lângă ele că sunt
    șantiere ROMÂNEȘTI cu manoperă românească, și se pune alături reperul francez.

ATENȚIE: pagina combien-coute-une-maison scrie cifrele cu PUNCT («1.350»), restul cu
spațiu fin («1 280»). Ambele variante sunt în listă.
"""
import pathlib, sys, re

RADACINA = pathlib.Path(__file__).resolve().parent.parent / 'countries' / 'fr'

MODIF = {

# ─────────────────────────────────────────────────────────── RE2020 ────────────
'ressources/re2020/index.html': [
 ("Le coffrage Polistibrick coûte 205–280 €/m² selon la surface, et la mise hors d'eau "
  "hors d'air revient à 690–810 €/m².",
  "Le coffrage Polistibrick coûte 205–280 €/m² selon la surface. En France, la mise hors "
  "d'eau hors d'air d'une maison revient à 1 000–1 400 €/m², et le clé en main à "
  "1 700–2 200 €/m² — la moyenne officielle est de 1 914 €/m² (enquête EPTB 2024 du "
  "ministère de la Transition écologique, hors terrain)."),
],

# ──────────────────────────────────────────────── proprietaires (FAQ prix) ─────
'pour/proprietaires/index.html': [
 ("Sur le marché roumain, chez les constructeurs classiques, le gros œuvre démarre autour "
  "de <strong>900 €/m² TTC</strong>, et le clé en main atteint environ "
  "<strong>1 300 €/m² TTC</strong>.",
  "En France, chez les constructeurs classiques, le gros œuvre se situe entre "
  "<strong>700 et 1 100 €/m² TTC</strong> et le clé en main entre "
  "<strong>1 700 et 2 200 €/m² TTC</strong> — moyenne officielle 1 914 €/m² "
  "(enquête EPTB 2024 du ministère, hors terrain)."),
 ("À titre de repère, notre maison d'Oltenița est revenue à 1 100 €/m².",
  "À titre de repère, notre maison d'Oltenița, en Roumanie, est revenue à 1 100 €/m² : "
  "un chantier réel, mais avec des coûts de main-d'œuvre roumains. En France, c'est le mur "
  "qui change le calcul — 182 €/m² de mur contre 329 €/m² pour la maçonnerie isolée par "
  "l'extérieur."),
],

# ───────────────────────────────────────────────────── calculateur économies ───
'economies/index.html': [
 ("Brique : ~1 000 €/m² en standard non conforme RE2020. Polistibrick : ~1 050 €/m² (+5 %) "
  "pour une maison passive A+++. Matériaux et main-d'œuvre compris, hors finitions "
  "intérieures et extérieures.",
  "Marché français : 1 914 €/m² en moyenne pour une maison individuelle neuve clé en main "
  "(enquête EPTB 2024 du ministère, hors terrain). Nous retenons le même coût de "
  "construction pour les deux : en France, le mur Polistibrick revient à 182 €/m² de mur "
  "contre 329 €/m² pour la maçonnerie isolée par l'extérieur, donc l'hypothèse est prudente. "
  "L'écart calculé ici ne vient que de l'énergie."),
 ("const brickBuildPerSqm = 1000;", "const brickBuildPerSqm = 1914;"),
 ("const poliBuildPerSqm = 1050;", "const poliBuildPerSqm = 1914;"),
 ('id="cEnergyPrice" value="0.22"', 'id="cEnergyPrice" value="0.29"'),
 ("parseFloat(f.energyPrice.value) || 0.20", "parseFloat(f.energyPrice.value) || 0.29"),
 ("Utilisez la moyenne de votre pays (FR ~0.25, DE ~0.32, ES ~0.20, RO ~0.18).",
  "Moyenne française : 0,29 €/kWh (Eurostat, 2e semestre 2025). Remplacez-la par le tarif "
  "de votre contrat."),
 ("<strong>Exemple calculé</strong>, à 0,20 €/kWh : une maison de 120 m² en brique "
  "(100–180 kWh/m²/an) paie 2 400–4 320 € par an en chauffage et climatisation. La même "
  "maison en Polistibrick (25–45 kWh/m²/an) paie 600–1 080 €. Sur 25 ans, au milieu des "
  "fourchettes, la différence dépasse 60 000 € sans aucune hausse de prix, et 100 000 € "
  "avec la hausse historique de l'énergie d'environ 4 % par an.",
  "<strong>Exemple calculé</strong>, à 0,29 €/kWh (moyenne française, Eurostat) : une "
  "maison de 120 m² en brique (100–180 kWh/m²/an) paie 3 480–6 260 € par an en chauffage "
  "et climatisation. La même maison en Polistibrick (25–45 kWh/m²/an) paie 870–1 570 €. "
  "Sur 25 ans, au milieu des fourchettes, la différence dépasse 90 000 € sans aucune "
  "hausse de prix, et 150 000 € avec la hausse historique de l'énergie d'environ 4 % par an."),
],

# ────────────────────────────────────────────── béton cellulaire ou brique ─────
'ressources/beton-cellulaire-ou-brique/index.html': [
 ("Prix du mur fini, main-d'œuvre comprise, à titre indicatif pour 2026 sur le marché "
  "roumain : béton cellulaire 240–300 lei/m² de mur, brique 320–390 lei/m².",
  "Prix du mur fini, main-d'œuvre comprise, à titre indicatif pour 2026 sur le marché "
  "français : béton cellulaire 100–160 €/m² de mur, brique 120–190 €/m², hors isolation "
  "extérieure."),
 ("Le marché de 2026 demande 500–800 €/m² construit pour la mise hors d'eau hors d'air, "
  "et 900–1 300 €/m² en clé en main ; les calculs plus prudents montent à 1 250–1 650 €/m².",
  "Le marché français de 2026 demande 1 000–1 400 €/m² construit pour la mise hors d'eau "
  "hors d'air, et 1 700–2 200 €/m² en clé en main ; en haut de gamme, on monte à "
  "2 300–3 000 €/m²."),
 ("Mur 240–300 lei/m², hors isolation", "Mur 100–160 €/m², hors isolation"),
 ("Mur 320–390 lei/m², hors isolation", "Mur 120–190 €/m², hors isolation"),
 ("En clé en main, les maisons Polistibrick sortent à 950–1 280 €/m². Un exemple réel : "
  "une maison de plain-pied de 140 m² avec finitions haut de gamme, à 1 223 €/m².",
  "Un exemple réel, sur un chantier réalisé en Roumanie avec les coûts locaux : une maison "
  "de plain-pied de 140 m² avec finitions haut de gamme, à 1 223 €/m² clé en main. En "
  "France, la main-d'œuvre est plus chère et le clé en main se situe entre 1 700 et "
  "2 200 €/m² quel que soit le système ; ce que Polistibrick change, c'est le mur — "
  "182 €/m² de mur contre 329 €/m² pour la maçonnerie isolée par l'extérieur."),
 ("Oui. À titre indicatif pour 2026, sur le marché roumain : 240–300 lei/m² de mur fini, "
  "main-d'œuvre comprise, pour le béton cellulaire, contre 320–390 lei/m² pour la brique.",
  "Oui. À titre indicatif pour 2026, sur le marché français : 100–160 €/m² de mur fini, "
  "main-d'œuvre comprise, pour le béton cellulaire, contre 120–190 €/m² pour la brique."),
],

# ──────────────────────────────────────────────────── maison polystyrène ───────
'ressources/maison-polystyrene-avis/index.html': [
 ("coffrage à partir de 205 €/m², clé en main 950–1 280 €/m², avec des exemples réels de "
  "maisons terminées.",
  "coffrage à partir de 205 €/m², et le repère du marché français pour une maison clé en "
  "main, 1 700–2 200 €/m², avec des exemples réels de maisons terminées."),
 ("À titre de repère, sur les chantiers roumains du système, une maison de plain-pied de "
  "140 m² avec finitions premium est revenue à 1 223 €/m² clé en main.",
  "À titre de repère, sur les chantiers roumains du système, une maison de plain-pied de "
  "140 m² avec finitions premium est revenue à 1 223 €/m² clé en main — avec des coûts de "
  "main-d'œuvre roumains. En France, comptez 1 700–2 200 €/m² clé en main, quel que soit "
  "le système."),
],

# ───────────────────────────────────────────────────────── maison passive ──────
'ressources/maison-passive/index.html': [
 ("Une maison ordinaire se construit en 2026 pour 450–700 €/m² en gros œuvre et "
  "900–1 350 €/m² clé en main, selon la région et les finitions ; ce sont les chiffres du "
  "marché roumain, celui où les prix Polistibrick sont publics.",
  "En France, une maison ordinaire se construit en 2026 pour 700–1 100 €/m² en gros œuvre "
  "et 1 700–2 200 €/m² clé en main, selon la région et les finitions ; la moyenne "
  "officielle est de 1 914 €/m² (enquête EPTB 2024 du ministère, hors terrain)."),
 ("En clé en main, vous arrivez à 1 000–1 600 €/m².",
  "En clé en main, vous arrivez à 1 900–2 600 €/m²."),
 ("À titre de repère, sur les chantiers roumains du système, les maisons sont sorties entre "
  "950 et 1 280 €/m² clé en main, la fourchette d'une maison ordinaire du marché.",
  "À titre de repère, sur les chantiers roumains du système, les maisons sont sorties entre "
  "950 et 1 280 €/m² clé en main — avec des coûts de main-d'œuvre roumains. En France, le "
  "repère est 1 700–2 200 €/m², la fourchette d'une maison ordinaire du marché."),
 ("l'enveloppe à U 0,10–0,14 revient à 690–810 €/m² hors d'eau hors d'air, le prix d'une "
  "maison ordinaire,",
  "l'enveloppe à U 0,10–0,14 entre dans une mise hors d'eau hors d'air à 1 000–1 400 €/m², "
  "le prix d'une maison ordinaire,"),
 ("En maçonnerie classique, 10 à 20 % de plus : de 900–1 350 €/m² clé en main, vous passez "
  "à 1 000–1 600 €/m².",
  "En maçonnerie classique, 10 à 20 % de plus : de 1 700–2 200 €/m² clé en main, vous "
  "passez à 1 900–2 600 €/m²."),
],

# ───────────────────────────────────────────────────────── coffrage isolant ────
'ressources/coffrage-isolant/index.html': [
 ("Le marché général demande en clé en main 900–1 650 €/m², selon le niveau de finitions "
  "(indicatif).",
  "Le marché français demande en clé en main 1 700–2 200 €/m², et 2 300–3 000 €/m² en haut "
  "de gamme (moyenne officielle 1 914 €/m², enquête EPTB 2024)."),
 ("Deux maisons réelles, pas des simulations : une maison de plain-pied de 140 m² avec des "
  "finitions haut de gamme est sortie à 1 223 €/m², une maison à étage à 1 039 €/m².",
  "Deux maisons réelles, pas des simulations, sur des chantiers réalisés en Roumanie avec "
  "les coûts locaux : une maison de plain-pied de 140 m² avec des finitions haut de gamme "
  "est sortie à 1 223 €/m², une maison à étage à 1 039 €/m². En France, le clé en main se "
  "situe entre 1 700 et 2 200 €/m² quel que soit le système."),
],

# ──────────────────────────────────────────────────────── vs ICF classique ─────
'ressources/polistibrick-vs-icf-classique/index.html': [
 ("Repère de marché : en 2026, une maison classique coûte 450–600 €/m² au stade du gros "
  "œuvre.",
  "Repère de marché : en 2026, en France, une maison classique coûte 700–1 100 €/m² au "
  "stade du gros œuvre et 1 700–2 200 €/m² clé en main."),
 ("Deux repères facturés, pas simulés, sur les chantiers roumains du système : une maison "
  "de plain-pied de 140 m² avec des finitions haut de gamme est revenue à 1 223 €/m² clé "
  "en main, une maison à étage à 1 039 €/m².",
  "Deux repères facturés, pas simulés, sur les chantiers roumains du système — avec des "
  "coûts de main-d'œuvre roumains : une maison de plain-pied de 140 m² avec des finitions "
  "haut de gamme est revenue à 1 223 €/m² clé en main, une maison à étage à 1 039 €/m². "
  "En France, comptez 1 700–2 200 €/m² clé en main."),
 ("À titre de repère, sur les chantiers roumains du système, une maison de plain-pied de "
  "140 m² avec des finitions haut de gamme est revenue à 1 223 €/m² clé en main, une maison "
  "à étage à 1 039 €/m².",
  "À titre de repère, sur les chantiers roumains du système — coûts de main-d'œuvre "
  "roumains — une maison de plain-pied de 140 m² avec des finitions haut de gamme est "
  "revenue à 1 223 €/m² clé en main, une maison à étage à 1 039 €/m². En France, le repère "
  "est 1 700–2 200 €/m²."),
],

# ────────────────────────────────────────────── prix bloc coffrant isolant ─────
'ressources/prix-bloc-coffrant-isolant/index.html': [
 ("Un repère existe : sur les chantiers roumains du système, des maisons sont sorties entre "
  "950 et 1 280 €/m² clé en main. Ce chiffre décrit des chantiers réalisés en Roumanie, "
  "avec les coûts locaux. Ce n'est pas une offre clé en main en France : ici, Polistibrick "
  "livre le coffrage et votre constructeur bâtit.",
  "Un repère existe : sur les chantiers roumains du système, des maisons sont sorties entre "
  "950 et 1 280 €/m² clé en main. Ce chiffre décrit des chantiers réalisés en Roumanie, "
  "avec les coûts locaux. Ce n'est pas une offre clé en main en France : ici, Polistibrick "
  "livre le coffrage et votre constructeur bâtit, et le marché français se situe entre "
  "1 700 et 2 200 €/m² clé en main."),
],

# ─────────────────────────────────────────── combien coûte une maison ──────────
'ressources/combien-coute-une-maison/index.html': [
 ("En 2026, une maison clé en main coûte entre 900 et 1.350 € par mètre carré construit, "
  "sur le marché roumain, là où le fabricant Polistibrick réalise ses chantiers. Hors "
  "d'eau, entre 450 et 700 €/m². Pour une maison de 100 m², cela représente 90.000–135.000 € "
  "pour la seule construction. Sans le terrain, sans les raccordements, sans les "
  "autorisations.",
  "En 2026, en France, une maison clé en main coûte entre 1 700 et 2 200 € par mètre carré "
  "construit — la moyenne officielle est de 1 914 €/m² (enquête EPTB 2024 du ministère). "
  "Au gros œuvre, entre 700 et 1 100 €/m². Pour une maison de 100 m², cela représente "
  "170 000–220 000 € pour la seule construction. Sans le terrain, sans les raccordements, "
  "sans les autorisations."),
 ("le même projet coûte 10–20 % de moins en zone rurale que dans la région Bucarest-Ilfov,",
  "le même projet coûte 10–20 % de moins en province que dans la région parisienne,"),
 ("Les fourchettes du marché roumain en 2026",
  "Les fourchettes du marché français en 2026"),
 ("Les chiffres ci-dessous viennent des guides de coûts publiés par les entreprises de "
  "construction pour 2026, sur le marché roumain, celui où le fabricant construit. La "
  "région Bucarest-Ilfov se situe en haut de chaque fourchette. Les zones rurales "
  "descendent de 10–20 %,",
  "Les chiffres ci-dessous viennent de l'enquête EPTB 2024 du ministère de la Transition "
  "écologique (moyenne nationale 1 914 €/m²) et des guides de coûts publiés par les "
  "constructeurs pour 2026. L'Île-de-France se situe en haut de chaque fourchette. La "
  "province descend de 10–20 %,"),
 ("<td style=\"padding:8px;border-bottom:1px solid #eee\">Hors d'eau</td>"
  "<td style=\"padding:8px;border-bottom:1px solid #eee\">450–700 €/m²</td>",
  "<td style=\"padding:8px;border-bottom:1px solid #eee\">Gros œuvre</td>"
  "<td style=\"padding:8px;border-bottom:1px solid #eee\">700–1 100 €/m²</td>"),
 ("<td style=\"padding:8px;border-bottom:1px solid #eee\">650–850 €/m²</td>",
  "<td style=\"padding:8px;border-bottom:1px solid #eee\">1 000–1 400 €/m²</td>"),
 # descrierea rândului trebuie să urmeze eticheta schimbată (era «Hors d'eau»)
 ("<td style=\"padding:8px;border-bottom:1px solid #eee\">gros œuvre, charpente, couverture</td>",
  "<td style=\"padding:8px;border-bottom:1px solid #eee\">fondations, murs porteurs, planchers, charpente, couverture</td>"),
 ("<td style=\"padding:8px;border-bottom:1px solid #eee\">900–1.350 €/m²</td>",
  "<td style=\"padding:8px;border-bottom:1px solid #eee\">1 700–2 200 €/m²</td>"),
 ("<td style=\"padding:8px;border-bottom:1px solid #eee\">plus de 1.500 €/m²</td>",
  "<td style=\"padding:8px;border-bottom:1px solid #eee\">2 300–3 000 €/m²</td>"),
 ("À titre de repère, sur les chantiers roumains du système, les maisons sont sorties entre "
  "950 et 1 280 €/m² clé en main.</li>",
  "À titre de repère, sur les chantiers roumains du système — avec des coûts de main-d'œuvre "
  "roumains — les maisons sont sorties entre 950 et 1 280 €/m² clé en main. En France, le "
  "clé en main se situe entre 1 700 et 2 200 €/m², quel que soit le système.</li>"),
 ("Mettez ces chiffres à côté du marché. En clé en main, la fourchette générale est de "
  "900–1.350 €/m², et Polistibrick sort à 950–1.280. Vous payez la construction au prix que "
  "tout le monde paie.",
  "Mettez ces chiffres à côté du marché. En France, le clé en main se situe entre 1 700 et "
  "2 200 €/m², quel que soit le système constructif : les lots techniques et les finitions "
  "pèsent pareil. Ce que le coffrage change, c'est le mur — 182 €/m² de mur contre "
  "329 €/m² pour la maçonnerie isolée par l'extérieur."),
 # (regula pe fragmentul scurt a fost înlocuită de cea completă, mai jos)
 ("Sur le marché roumain, où le fabricant construit, une maison de 100–120 m² clé en main "
  "demande 8–12 mois",
  "En France, une maison de 100–120 m² clé en main demande 8–12 mois"),
 ("à titre de repère, sur les chantiers roumains du système, les maisons sont sorties entre "
  "950 et 1 280 €/m² clé en main. Les prix du coffrage sont publiés",
  "à titre de repère, sur les chantiers roumains du système — coûts locaux — les maisons "
  "sont sorties entre 950 et 1 280 €/m² clé en main ; en France, comptez 1 700–2 200 €/m². "
  "Les prix du coffrage sont publiés"),

 # ── sumele absolute, verificarea pe piață și anexele (și în JSON-LD) ─────────
 # gros œuvre 700–1 100 · HEHA 1 000–1 400 · clé en main 1 700–2 200 €/m²
 # viabilisation 5 000–15 000 € · permis + taxe 2 500–6 000 € (surse 2026)

 # ── tabelul în euro absoluți: capetele de rând + cele 6 celule ────────────────
 ('<td style="padding:8px;border-bottom:1px solid #eee">Hors d\'eau</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">45.000–70.000 €</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">67.500–105.000 €</td>',
  '<td style="padding:8px;border-bottom:1px solid #eee">Gros œuvre</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">70 000–110 000 €</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">105 000–165 000 €</td>'),
 ('<td style="padding:8px;border-bottom:1px solid #eee">65.000–85.000 €</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">97.500–127.500 €</td>',
  '<td style="padding:8px;border-bottom:1px solid #eee">100 000–140 000 €</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">150 000–210 000 €</td>'),
 ('<td style="padding:8px;border-bottom:1px solid #eee">90.000–135.000 €</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">135.000–202.500 €</td>',
  '<td style="padding:8px;border-bottom:1px solid #eee">170 000–220 000 €</td>'
  '<td style="padding:8px;border-bottom:1px solid #eee">255 000–330 000 €</td>'),

 # ── verificarea pe piață ─────────────────────────────────────────────────────
 ("Vérification sur le marché : pour 100 m² clé en main standard, les guides des entreprises "
  "de construction annoncent des budgets de 95.000–125.000 €, et pour 150 m², entre 140.000 "
  "et 185.000 €. Le calcul ci-dessus recoupe les offres publiées.",
  "Vérification sur le marché : l'enquête EPTB du ministère donne un coût moyen de "
  "225 500 € pour une maison individuelle neuve de 118 m² en 2024, soit 1 914 €/m². "
  "Le calcul ci-dessus recoupe cette moyenne."),

 # ── întrebarea «100 m²» (apare și în textul vizibil, și în JSON-LD) ───────────
 ("Entre 90.000 et 135.000 € clé en main, pour la seule construction, aux prix 2026 du "
  "marché roumain, où le fabricant réalise ses chantiers. Hors d'eau, 45.000–70.000 €. "
  "Ajoutez les raccordements aux réseaux (8.000–25.000 €), la conception avec les "
  "autorisations (8.000–15.000 €) et une réserve de 10–15 % pour les imprévus.",
  "Entre 170 000 et 220 000 € clé en main, pour la seule construction, aux prix 2026 du "
  "marché français. Au gros œuvre, 70 000–110 000 €. Ajoutez la viabilisation du terrain "
  "(5 000–15 000 €), le dossier de permis et la taxe d'aménagement (2 500–6 000 €) et une "
  "réserve de 10–15 % pour les imprévus."),

 # ── întrebarea «am terenul» ──────────────────────────────────────────────────
 ("Pour une maison de 100 m² clé en main, budgétez 90.000–135.000 € pour la construction, "
  "plus 16.000–40.000 € pour les raccordements, la conception, les autorisations et les "
  "aménagements extérieurs. Un total réaliste démarre à 110.000 €.",
  "Pour une maison de 100 m² clé en main, budgétez 170 000–220 000 € pour la construction, "
  "plus 10 000–25 000 € pour la viabilisation, le dossier de permis, la taxe d'aménagement "
  "et les aménagements extérieurs. Un total réaliste démarre à 180 000 €."),
],
}

total = 0
ratate = []
for rel, reguli in MODIF.items():
    p = RADACINA / rel
    h = p.read_text(encoding='utf-8')
    n = 0
    for a, b in reguli:
        k = h.count(a)
        # pe un fișier deja trecut o dată, vechiul text nu mai există: e normal,
        # atâta timp cât noul text e acolo. Raportăm doar ce chiar lipsește.
        if k == 0 and b not in h:
            ratate.append(f'{rel} :: {a[:70]}…')
        n += k
        h = h.replace(a, b)
    p.write_text(h, encoding='utf-8')
    total += n
    print(f'{rel}: {n} înlocuiri')

print(f'\nTOTAL: {total}')
if ratate:
    print('\nNEGĂSITE (verifică-le de mână):')
    for r in ratate: print('  ✗', r)
sys.exit(1 if ratate else 0)
