#!/usr/bin/env python3
"""Translate FR comparison page → RO. Replace all visible French text with Romanian."""
import re
from pathlib import Path

p = Path("/Users/polistibrick/Desktop/polistibrick-multisite/countries/ro/comparatie/index.html")
txt = p.read_text(encoding="utf-8")

# Order: longest/most specific FIRST to avoid partial replacements
REPL = [
    # HTML lang attribute
    ('<html lang="fr">', '<html lang="ro">'),

    # META
    ('Comparaison · Polistibrick — la seule technologie qui réunit 5 matériaux premium dans un seul système de construction',
     'Comparație · Polistibrick — singura tehnologie care reunește 5 materiale premium într-un singur sistem de construcție'),
    ('Polistibrick est la seule technologie qui réunit 5 matériaux premium (isolation, feu A1, antisismique, hydrofuge, acoustique) dans un seul système de construction. Comparé aux autres ICF, au système classique et au système classique transformé en passif.',
     'Polistibrick este singura tehnologie care reunește 5 materiale premium (izolație, foc A1, antiseismic, hidrofug, acustic) într-un singur sistem de construcție. Comparat cu alte ICF, sistemul clasic și sistemul clasic transformat în pasiv.'),

    # CSS path (RO version uses ../assets/css/site.css too — already correct)

    # HERO
    ('★ La seule technologie premium intégrée', '★ Singura tehnologie premium integrată'),
    ('Polistibrick — la seule technologie qui <em>réunit 5 matériaux premium</em> dans un seul système de construction.',
     'Polistibrick — singura tehnologie care <em>reunește 5 materiale premium</em> într-un singur sistem de construcție.'),
    ('🌡️ Isolation · 🔥 Résistance au feu A1 · 🛡️ Antisismique · 💧 Hydrofuge · 🔇 Acoustique — tout intégré dans un panneau préfabriqué unique. Aucune autre technologie de construction n\'offre cette intégration. Comparé aux autres ICF, au système classique et au système classique transformé en passif.',
     '🌡️ Izolație · 🔥 Rezistență la foc A1 · 🛡️ Antiseismic · 💧 Hidrofug · 🔇 Acustic — totul integrat într-un panou prefabricat unic. Nicio altă tehnologie de construcție nu oferă această integrare. Comparat cu alte ICF, cu sistemul clasic și cu sistemul clasic transformat în pasiv.'),

    # Hero system tags
    ('★ Premium 5-en-1', '★ Premium 5-în-1'),
    ('ICF basique', 'ICF bazic'),
    ('Conventionnel', 'Convențional'),
    ('Passive par ajouts', 'Pasiv prin adaosuri'),
    ('Autre système ICF', 'Alt sistem ICF'),
    ('Système classique → passif', 'Sistem clasic → pasiv'),
    ('Système classique', 'Sistem clasic'),

    # CRITÈRE 01 — 5-EN-1
    ('Critère 01 · ⚡ Système 5-en-1', 'Criteriul 01 · ⚡ Sistem 5-în-1'),
    ('5 fonctions dans <em>un seul panneau.</em>', '5 funcții într-<em>un singur panou.</em>'),
    ('Polistibrick intègre 5 fonctions premium dans un seul panneau préfabriqué — moulées ensemble en usine, livrées prêtes à monter :',
     'Polistibrick integrează 5 funcții premium într-un singur panou prefabricat — turnate împreună în fabrică, livrate gata de montaj:'),
    ('<strong>Isolation thermique</strong> · EPS premium continu jusqu\'à 30 cm',
     '<strong>Izolație termică</strong> · EPS premium continuu până la 30 cm'),
    ('<strong>Résistance au feu A1</strong> · incombustible, REI 240',
     '<strong>Rezistență la foc A1</strong> · necombustibil, REI 240'),
    ('<strong>Antisismique</strong> · béton armé 15 cm avec plan d\'armature',
     '<strong>Antiseismic</strong> · beton armat 15 cm cu plan de armare'),
    ('<strong>Hydrofuge</strong> · EPS à cellules fermées, ni eau ni moisissure',
     '<strong>Hidrofug</strong> · EPS cu celule închise, fără apă, fără mucegai'),
    ('<strong>Isolation acoustique</strong> · combinaison EPS + béton armé',
     '<strong>Izolație acustică</strong> · combinație EPS + beton armat'),
    ('<strong>5 fonctions premium dans 1 panneau.</strong> Les autres ICF n\'intègrent que l\'isolation — il faut tout le reste à part.',
     '<strong>5 funcții premium într-un panou.</strong> Alte ICF integrează doar izolația — restul trebuie adăugat separat.'),
    ('🌡️ + 🔥 + 🛡️ + 💧 + 🔇 — tout-en-un, moulé en usine.',
     '🌡️ + 🔥 + 🛡️ + 💧 + 🔇 — totul-într-unul, turnat în fabrică.'),
    ('5-EN-1', '5-ÎN-1'),
    ('🌡️ seulement. Feu / antisismique / hydrofuge / acoustique = à ajouter.',
     '🌡️ doar atât. Foc / antiseismic / hidrofug / acustic = de adăugat.'),
    ('1 sur 5', '1 din 5'),
    ('0 fonction premium intégrée. Tout à ajouter séparément.',
     '0 funcții premium integrate. Totul de adăugat separat.'),
    ('0 sur 5', '0 din 5'),
    ('Brique + 11 couches ajoutées pour atteindre les 5 fonctions.',
     'Cărămidă + 11 straturi adăugate pentru a atinge cele 5 funcții.'),
    ('Empilé', 'Stratificat'),

    # CRITÈRE 02 — Plan d'armature
    ('Critère 02 · 🛠️ Plan d\'armature', 'Criteriul 02 · 🛠️ Plan de armare'),
    ('Le seul ICF qui respecte <em>un vrai plan d\'armature.</em>', 'Singurul ICF care respectă <em>un plan de armare real.</em>'),
    ('Polistibrick a des logements brevetés pré-positionnés pour les barres d\'acier — l\'ingénieur structure peut concevoir un plan d\'armature comme pour le béton armé classique. Les autres ICF sont des systèmes "LEGO" basiques : pas de plan d\'armature possible, pas de calculs structurels avancés.',
     'Polistibrick are locașuri brevetate pre-poziționate pentru bare de oțel — inginerul de structură poate concepe un plan de armare ca pentru betonul armat clasic. Alte ICF sunt sisteme "LEGO" bazice: fără plan de armare posibil, fără calcule structurale avansate.'),
    ('<strong>Plan d\'armature ingénieur = sécurité structurelle.</strong> Indispensable pour les bâtiments multi-étages, zones sismiques, charges lourdes.',
     '<strong>Plan de armare inginer = siguranță structurală.</strong> Indispensabil pentru clădirile multi-etajate, zone seismice, sarcini grele.'),
    ('Logements brevetés pour barres d\'acier — plan d\'armature respecté', 'Locașuri brevetate pentru bare de oțel — plan de armare respectat'),
    ('Complet', 'Complet'),
    ('Système LEGO basique — pas de plan d\'armature possible', 'Sistem LEGO bazic — fără plan de armare posibil'),
    ('Incomplet', 'Incomplet'),
    ('Renforcement standard possible', 'Întărire standard posibilă'),
    ('Basique', 'Bazic'),
    ('Identique à la brique classique', 'Identic cu cărămida clasică'),
    ('Compliqué', 'Complicat'),

    # CRITÈRE 03 — Zones sismiques
    ('Critère 03 · 🏔️ Zones sismiques', 'Criteriul 03 · 🏔️ Zone seismice'),
    ('Conçu pour résister <em>aux séismes.</em>', 'Conceput să reziste <em>la seisme.</em>'),
    ('Grâce au plan d\'armature respecté et à la structure monolithique en béton armé, Polistibrick est certifié pour les zones sismiques et les terrains avec mouvements. Les autres ICF (sans plan d\'armature) ne peuvent pas être utilisés dans ces zones — c\'est une limitation structurelle majeure.',
     'Datorită planului de armare respectat și structurii monolitice în beton armat, Polistibrick este certificat pentru zonele seismice și terenurile cu mișcări. Alte ICF (fără plan de armare) nu pot fi folosite în aceste zone — este o limitare structurală majoră.'),
    ('<strong>Construisez en sécurité partout en Europe</strong>, y compris dans les régions sismiques (Italie, Roumanie, Grèce, Balkans).',
     '<strong>Construiți în siguranță oriunde în Europa</strong>, inclusiv în regiunile seismice (Italia, România, Grecia, Balcani).'),
    ('Certifié zones sismiques · béton armé monolithique', 'Certificat zone seismice · beton armat monolitic'),
    ('Oui', 'Da'),
    ('Non adapté — pas de plan d\'armature, structure fragile', 'Neadaptat — fără plan de armare, structură fragilă'),
    ('Non', 'Nu'),
    ('Possible avec renforcement structurel', 'Posibil cu întărire structurală'),
    ('Possible', 'Posibil'),
    ('Identique au système classique', 'Identic cu sistemul clasic'),

    # CRITÈRE 04 — Équipes
    ('Critère 04 · 👷 Équipes', 'Criteriul 04 · 👷 Echipe'),
    ('Une seule équipe <em>fait tout.</em>', 'O singură echipă <em>face tot.</em>'),
    ('Polistibrick est livré prêt à monter : une équipe certifiée fait murs, planchers, toit. Les autres ICF ne font que les murs isolés — il faut quand même appeler maçons, charpentiers, façadiers comme avec la brique classique.',
     'Polistibrick este livrat gata de montaj: o singură echipă certificată face pereți, planșee, acoperiș. Alte ICF fac doar pereți izolați — tot trebuie să chemi zidari, dulgheri, fațadiști ca la cărămida clasică.'),
    ('<strong>1 seul interlocuteur, 1 seul calendrier.</strong> Avec les autres ICF, vous gérez autant d\'équipes qu\'avec la brique.',
     '<strong>1 singur interlocutor, 1 singur calendar.</strong> Cu alte ICF, gestionezi tot atâtea echipe ca la cărămidă.'),
    ('Une seule équipe certifiée (2-3 personnes)', 'O singură echipă certificată (2-3 persoane)'),
    ('1 équipe', '1 echipă'),
    ('Plusieurs équipes (comme la brique)', 'Mai multe echipe (ca la cărămidă)'),
    ('Plusieurs', 'Mai multe'),
    ('Maçons + isolateurs + façadiers...', 'Zidari + izolatori + fațadiști...'),
    ('Encore plus d\'étapes spécialisées', 'Și mai multe etape specializate'),
    ('Encore +', 'Și mai +'),

    # CRITÈRE 05 — Temps
    ('Critère 05 · ⏱️ Temps d\'exécution', 'Criteriul 05 · ⏱️ Timp de execuție'),
    ('Vous emménagez <em>en quelques semaines.</em>', 'Vă mutați <em>în câteva săptămâni.</em>'),
    ('Les panneaux Polistibrick s\'assemblent comme des LEGO et intègrent tout — c\'est ce qui fait la rapidité. Les autres ICF, même s\'ils sont en blocs, doivent être complétés par tout le reste (façade, finitions, étanchéité) — le chantier dure aussi longtemps que pour la brique classique.',
     'Panourile Polistibrick se asamblează ca LEGO și integrează tot — asta face rapiditatea. Alte ICF, chiar dacă sunt în blocuri, trebuie completate cu tot restul (fațadă, finisaje, hidroizolație) — șantierul durează la fel cât la cărămidă.'),
    ('<strong>Le seul ICF qui réduit vraiment le temps de chantier.</strong> Les autres prennent le même temps que la brique.',
     '<strong>Singurul ICF care reduce cu adevărat timpul de șantier.</strong> Altele durează la fel ca la cărămidă.'),
    ('Quelques semaines pour le gros œuvre fini', 'Câteva săptămâni pentru structura finită'),
    ('Le plus rapide', 'Cel mai rapid'),
    ('Même temps que la brique (mêmes étapes complémentaires)', 'Același timp ca la cărămidă (aceleași etape complementare)'),
    ('≈ Brique', '≈ Cărămidă'),
    ('Plusieurs mois sur chantier', 'Mai multe luni pe șantier'),
    ('Plusieurs mois', 'Mai multe luni'),
    ('Encore plus long (couches passives ajoutées)', 'Și mai lung (straturi pasive adăugate)'),

    # CRITÈRE 06 — Isolation continue
    ('Critère 06 · 🌡️ Isolation continue', 'Criteriul 06 · 🌡️ Izolație continuă'),
    ('Isolation <em>moulée dans le panneau.</em>', 'Izolație <em>turnată în panou.</em>'),
    ('Chez Polistibrick, l\'EPS premium est moulé dans le panneau avec le béton — continuité parfaite, zéro pont thermique. Les autres ICF ont une isolation intégrée, mais sans la même qualité d\'intégration ni performance Passivhaus par défaut.',
     'La Polistibrick, EPS-ul premium este turnat în panou împreună cu betonul — continuitate perfectă, zero punți termice. Alte ICF au izolație integrată, dar fără aceeași calitate de integrare și fără performanță Passivhaus implicit.'),
    ('<strong>Performance Passivhaus dès la conception.</strong> Pas un accessoire — c\'est la structure elle-même.',
     '<strong>Performanță Passivhaus de la proiectare.</strong> Nu un accesoriu — este chiar structura.'),
    ('Intégrée + continue', 'Integrată + continuă'),
    ('EPS premium', 'EPS premium'),
    ('Béton armé', 'Beton armat'),
    ('EPS', 'EPS'),
    ('Intégrée mais basique', 'Integrată dar bazică'),
    ('EPS léger', 'EPS ușor'),
    ('Béton', 'Beton'),
    ('Collée après coup', 'Lipită după turnare'),
    ('Brique', 'Cărămidă'),
    ('+ EPS', '+ EPS'),
    ('Enduit', 'Tencuială'),
    ('Plus d\'EPS collé', 'Mai mult EPS lipit'),
    ('+ EPS épais', '+ EPS gros'),

    # CRITÈRE 07 — Sécurité feu
    ('Critère 07 · 🔥 Résistance au feu', 'Criteriul 07 · 🔥 Rezistență la foc'),
    ('Classe A1 — <em>non-combustible.</em>', 'Clasa A1 — <em>necombustibil.</em>'),
    ('Les quatre systèmes atteignent la classe A1 (incombustible — la plus élevée en Europe). La différence est dans la structure : seul Polistibrick offre du béton armé continu avec plan d\'armature respecté, pour la meilleure intégrité face au feu.',
     'Toate cele patru sisteme ating clasa A1 (necombustibil — cea mai ridicată în Europa). Diferența este în structură: doar Polistibrick oferă beton armat continuu cu plan de armare respectat, pentru cea mai bună integritate în fața focului.'),
    ('<strong>A1 + structure monolithique en béton armé.</strong> La sécurité d\'une structure conçue par un ingénieur.',
     '<strong>A1 + structură monolitică din beton armat.</strong> Siguranța unei structuri proiectate de inginer.'),
    ('A1 + structure monolithique en béton armé', 'A1 + structură monolitică din beton armat'),
    ('A1 si correctement installé', 'A1 dacă este instalat corect'),
    ('A1 · maçonnerie traditionnelle', 'A1 · zidărie tradițională'),
    ('A1 · brique + couches isolantes', 'A1 · cărămidă + straturi izolante'),

    # CRITÈRE 08 — Hydrofuge
    ('Critère 08 · 💧 Hydrofuge', 'Criteriul 08 · 💧 Hidrofug'),
    ('Aucune eau. <em>Aucune moisissure.</em>', 'Fără apă. <em>Fără mucegai.</em>'),
    ('L\'EPS de Polistibrick est à cellules fermées — il n\'absorbe pas l\'eau. Combiné au béton armé monolithique, vous avez une structure totalement étanche, sans risque d\'humidité, de moisissure ou de pourriture. La brique, elle, absorbe naturellement l\'humidité — d\'où les problèmes de murs humides et d\'enduit qui s\'écaille.',
     'EPS-ul Polistibrick este cu celule închise — nu absoarbe apa. Combinat cu betonul armat monolitic, ai o structură complet etanșă, fără risc de umiditate, mucegai sau putrezire. Cărămida, în schimb, absoarbe natural umiditatea — de aici problemele cu pereți umezi și tencuială care se cojește.'),
    ('<strong>Murs étanches à vie.</strong> Aucun problème d\'humidité, garantie 50+ ans.',
     '<strong>Pereți etanși pe viață.</strong> Fără probleme de umiditate, garanție 50+ ani.'),
    ('EPS cellules fermées + béton armé monolithique', 'EPS celule închise + beton armat monolitic'),
    ('Totalement', 'Total'),
    ('EPS basique + jonctions = points d\'infiltration', 'EPS bazic + îmbinări = puncte de infiltrare'),
    ('Partiellement', 'Parțial'),
    ('Brique absorbe l\'humidité — risque de moisissure', 'Cărămida absoarbe umiditatea — risc de mucegai'),
    ('Membranes ajoutées, mais brique reste absorbante', 'Membrane adăugate, dar cărămida rămâne absorbantă'),

    # CRITÈRE 09 — Acoustique
    ('Critère 09 · 🔇 Isolation acoustique', 'Criteriul 09 · 🔇 Izolație acustică'),
    ('Silence <em>de chambre forte.</em>', 'Liniște <em>ca într-o cameră blindată.</em>'),
    ('La combinaison EPS premium + béton armé de Polistibrick offre une isolation acoustique professionnelle (&gt; 50 dB) sans aucune couche ajoutée. La brique seule est acoustiquement faible — il faut des panneaux acoustiques séparés pour atteindre le même résultat.',
     'Combinația EPS premium + beton armat Polistibrick oferă o izolație acustică profesională (&gt; 50 dB) fără niciun strat adăugat. Cărămida singură este slabă acustic — sunt necesare panouri acustice separate pentru același rezultat.'),
    ('<strong>Silence total dès la conception.</strong> Vous n\'entendez plus les voisins, ni la rue.',
     '<strong>Liniște totală de la proiectare.</strong> Nu mai auzi vecinii, nici strada.'),
    ('EPS + béton armé = &gt; 50 dB sans ajouts', 'EPS + beton armat = &gt; 50 dB fără adăugiri'),
    ('Premium', 'Premium'),
    ('Performance basique, panneaux acoustiques à ajouter', 'Performanță bazică, panouri acustice de adăugat'),
    ('Brique = isolation acoustique faible', 'Cărămida = izolație acustică slabă'),
    ('Faible', 'Slabă'),
    ('Panneaux acoustiques ajoutés séparément', 'Panouri acustice adăugate separat'),
    ('Avec ajouts', 'Cu adaosuri'),

    # CRITÈRE 10 — Classe énergétique
    ('Critère 10 · 🔋 Classe énergétique', 'Criteriul 10 · 🔋 Clasă energetică'),
    ('A+++ <em>par défaut.</em>', 'A+++ <em>implicit.</em>'),
    ('Polistibrick livre A+++ dès la conception. Les autres ICF atteignent une performance moyenne (B/C) — ils isolent mais pas au niveau Passivhaus complet. La brique classique reste E/F. La brique passive atteint A+++ par couches ajoutées.',
     'Polistibrick livrează A+++ de la proiectare. Alte ICF ating o performanță medie (B/C) — izolează dar nu la nivelul Passivhaus complet. Cărămida clasică rămâne E/F. Cărămida pasivă atinge A+++ prin straturi adăugate.'),
    ('<strong>A+++ inclus — pas en option.</strong> Le seul ICF qui livre Passivhaus dès la conception.',
     '<strong>A+++ inclus — nu opțional.</strong> Singurul ICF care livrează Passivhaus de la proiectare.'),
    ('A+++ par défaut, sans ajouts', 'A+++ implicit, fără adăugiri'),
    ('Performance intermédiaire (isolation seule)', 'Performanță intermediară (doar izolație)'),
    ('Standard énergivore', 'Standard mare consumator de energie'),
    ('A+++ atteint par couches ajoutées', 'A+++ atins prin straturi adăugate'),

    # CRITÈRE 11 — Prix
    ('Critère 11 · 💶 Prix accessible', 'Criteriul 11 · 💶 Preț accesibil'),
    ('Le passif au prix <em>du conventionnel.</em>', 'Pasivul la prețul <em>convenționalului.</em>'),
    ('Polistibrick coûte à peine plus que la brique classique — pour une performance A+++ premium intégrée. Les autres ICF coûtent plus cher que la brique sans donner la performance complète. La brique passive traditionnelle est sensiblement plus chère.',
     'Polistibrick costă cu foarte puțin mai mult decât cărămida clasică — pentru o performanță A+++ premium integrată. Alte ICF costă mai mult decât cărămida fără să ofere performanța completă. Cărămida pasivă tradițională este semnificativ mai scumpă.'),
    ('<strong>Polistibrick rend le premium accessible.</strong> Le meilleur rapport performance/prix du marché.',
     '<strong>Polistibrick face premium-ul accesibil.</strong> Cel mai bun raport performanță/preț de pe piață.'),
    ('Quasi-égal au conventionnel — pour A+++ premium', 'Aproape egal cu convenționalul — pentru A+++ premium'),
    ('Excellent', 'Excelent'),
    ('Plus cher sans la performance complète', 'Mai scump fără performanța completă'),
    ('Médiocre', 'Mediocru'),
    ('Standard du marché — sans le passif', 'Standardul pieței — fără pasiv'),
    ('Standard', 'Standard'),
    ('Sensiblement plus chère', 'Semnificativ mai scumpă'),
    ('Cher', 'Scump'),

    # CRITÈRE 12 — Économies
    ('Critère 12 · 📉 Économies à vie', 'Criteriul 12 · 📉 Economii pe viață'),
    ('Vous économisez <em>chaque mois.</em>', 'Economisiți <em>în fiecare lună.</em>'),
    ('La performance Passivhaus de Polistibrick fait fondre vos factures d\'énergie dès la première année. Sur 25 ans, l\'économie cumulée compense — et dépasse — le léger surcoût initial. C\'est la vraie économie : pas à la construction, mais à vie.',
     'Performanța Passivhaus a Polistibrick face să se topească facturile de energie din primul an. Pe 25 de ani, economia cumulată compensează — și depășește — surplusul inițial mic. Aceasta este adevărata economie: nu la construcție, ci pe viață.'),
    ('<strong>Investissement qui se rentabilise chaque hiver.</strong> Chaque facture impayée vous rend votre investissement.',
     '<strong>Investiție care se amortizează în fiecare iarnă.</strong> Fiecare factură neplătită îți recuperează investiția.'),
    ('👑 Économies Polistibrick', '👑 Economii Polistibrick'),
    ('économisés sur <strong>25 ans</strong>,<br>pour une maison de <strong>150 m²</strong>.',
     'economisiți pe <strong>25 de ani</strong>,<br>pentru o casă de <strong>150 m²</strong>.'),
    ('vs construction en brique classique<br>(énergie + entretien cumulés)',
     'vs construcție în cărămidă clasică<br>(energie + întreținere cumulate)'),

    # FINAL VERDICT
    ('👑 Le verdict', '👑 Verdictul'),
    ('Polistibrick — la seule technologie qui <em>réunit 5 matériaux premium</em> dans un seul système.',
     'Polistibrick — singura tehnologie care <em>reunește 5 materiale premium</em> într-un singur sistem.'),
    ('🌡️ Isolation thermique · 🔥 Résistance au feu A1 · 🛡️ Antisismique · 💧 Hydrofuge · 🔇 Acoustique. <strong>Aucun autre système — ni les ICF concurrents, ni la brique classique, ni la brique passive traditionnelle — n\'offre cette intégration premium dans un seul panneau préfabriqué.</strong> Livré par une seule équipe. Au prix du conventionnel.',
     '🌡️ Izolație termică · 🔥 Rezistență la foc A1 · 🛡️ Antiseismic · 💧 Hidrofug · 🔇 Acustic. <strong>Niciun alt sistem — nici ICF-urile concurente, nici cărămida clasică, nici cărămida pasivă tradițională — nu oferă această integrare premium într-un singur panou prefabricat.</strong> Livrat de o singură echipă. La prețul convenționalului.'),
    ('Demander un devis', 'Cere o ofertă'),
    ('Calculer le coût', 'Calculează costul'),

    # CTA paths (RO uses original folder names)
    ('href="../devis/"', 'href="../oferta/"'),
    ('href="../calculateur/"', 'href="../calculator/"'),
]

n = 0
not_found = []
for old, new in REPL:
    if old in txt:
        txt = txt.replace(old, new)
        n += 1
    else:
        not_found.append(old[:80])

p.write_text(txt, encoding="utf-8")
print(f"Applied {n}/{len(REPL)} replacements")
if not_found:
    print(f"\n⚠ {len(not_found)} not found (preview):")
    for nf in not_found[:8]:
        print(f"  - {nf}")
