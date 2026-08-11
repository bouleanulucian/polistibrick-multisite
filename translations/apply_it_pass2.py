#!/usr/bin/env python3
"""Aggressive second-pass FR→IT for priority IT pages."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IT_DIR = ROOT / "countries" / "it"
FR_DIR = ROOT / "countries" / "fr"
TRANS = ROOT / "translations"

sys.path.insert(0, str(ROOT))
from translations.sync_fr_to_es import apply_dict, filter_mapping  # noqa: E402
from translations.path_maps import FR_TO_IT  # noqa: E402

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

IT_TO_FR = {it: fr for fr, it in FR_TO_IT.items()}

PRIORITY = [
    "progetti/index.html",
    "per/proprietari/index.html",
    "per/architetti/index.html",
    "per/costruttori/index.html",
    "per/investitori/index.html",
    "risorse/faq/index.html",
    "prodotti/polistibrick/index.html",
    "prodotti/polistiwall/index.html",
    "prodotti/polistisip/index.html",
    "prodotti/index.html",
    "chi-siamo/index.html",
    "chi-siamo/fondatore/index.html",
    "chi-siamo/fabbriche/index.html",
    "chi-siamo/brevetto/index.html",
    "chi-siamo/certificazioni/index.html",
    "diventa-partner/index.html",
    "contact/index.html",
    "testimonianze/index.html",
    "risparmi/index.html",
    "legal/privacy/index.html",
    "legal/condizioni/index.html",
    "legal/note-legali/index.html",
    "legal/sostenibilita/index.html",
    "legal/cookie/index.html",
    "montaggio/index.html",
]

# Complete FR→IT for projects page + pass-2 blocks
PASS2: dict[str, str] = {
    # --- projects: all model paragraphs ---
    "Projects Polistibrick · modèles de maisons, une maison en trois systèmes": "Progetti Polistibrick · modelli di case, una casa in tre sistemi",
    "Progetti Polistibrick · modèles de maisons, une maison en trois systèmes": "Progetti Polistibrick · modelli di case, una casa in tre sistemi",
    "Models de maisons Polistibrick · une maison, 3 systèmes constructifs": "Modelli di case Polistibrick · una casa, 3 sistemi costruttivi",
    "Modèles de maisons Polistibrick · une maison, 3 systèmes constructifs": "Modelli di case Polistibrick · una casa, 3 sistemi costruttivi",
    "Vous choisissez d'abord la maison, pas le budget. Le même plan se construit en trois systèmes, et le prix change selon la structure.": "Scegli prima la casa, non il budget. Lo stesso progetto si costruisce in tre sistemi e il prezzo cambia in base alla struttura.",
    "plain-pied": "su un piano",
    "terrasse": "terrazza",
    "petit terrain": "terreno piccolo",
    "garage double": "garage doppio",
    "81 m² au sol": "81 m² di impronta",
    "90 m² au sol": "90 m² di impronta",
    "garage en option": "garage opzionale",
    "jardin": "giardino",
    "sans garage": "senza garage",
    "deux niveaux": "due livelli",
    "séjour + cuisine": "soggiorno + cucina",
    "séjour": "soggiorno",
    "surface utile": "superficie utile",
    "surface construite": "superficie costruita",
    "chambres": "camere",
    "terrasse couverte": "terrazza coperta",
    "chambre principale": "camera principale",
    "salle de bains": "bagno",
    "emprise au sol": "impronta a terra",
    "chaque chambre": "ogni camera",
    "salles de bains": "bagni",
    "bureau": "studio",
    "emprise sans garage": "impronta senza garage",
    "buanderie": "lavanderia",
    "sans escalier": "senza scale",
    "Façade côté rue": "Facciata lato strada",
    "Façade côté jardin": "Facciata lato giardino",
    "Séjour · cuisine · salle à manger": "Soggiorno · cucina · sala da pranzo",
    "La cuisine": "La cucina",
    "La chambre principale": "La camera principale",
    "La chambre parentale": "La suite genitori",
    "La salle de bains parentale": "Il bagno della suite genitori",
    "La salle de bains": "Il bagno",
    "La salle de bains de l'étage": "Il bagno al piano superiore",
    "La chambre du rez-de-chaussée": "La camera al piano terra",
    "Chambre à l'étage": "Camera al piano superiore",
    "Une chambre": "Una camera",
    "Le séjour": "Il soggiorno",
    "La cuisine fermée": "La cucina chiusa",
    "Le plan du rez-de-chaussée": "Planimetria piano terra",
    "Le plan du rez-de-chaussée et de l'étage": "Planimetria piano terra e primo piano",
    "Mur extérieur de 38 cm, U = 0,14 W/m²K — se chauffe avec une petite chaudière": "Parete esterna da 38 cm, U = 0,14 W/m²K — si riscalda con una piccola caldaia",
    "Mur extérieur de 38 cm, U = 0,14 W/m²K — se chauffe avec une petite chaudière": "Parete esterna da 38 cm, U = 0,14 W/m²K — si riscalda con una piccola caldaia",
    "Mur coupe-feu en béton de 15 cm entre le garage et la maison": "Parete tagliafuoco in calcestruzzo da 15 cm tra garage e casa",
    "Mur coupe-feu en calcestruzzo de 15 cm entre le garage et la maison": "Parete tagliafuoco in calcestruzzo da 15 cm tra garage e casa",
    "Mur coupe-feu en béton de 15 cm entre le garage et la maison": "Parete tagliafuoco in calcestruzzo da 15 cm tra garage e casa",
    "Plancher en panneaux PBK avec dalle de compression, portée libre jusqu'à 9 m": "Solaio in pannelli PBK con soletta di compressione, luce libera fino a 9 m",
    "Floor en panneaux PBK avec dalle de compression, portée libre jusqu'à 9 m": "Solaio in pannelli PBK con soletta di compressione, luce libera fino a 9 m",
    "Structure béton, isolation, finitions": "Struttura in calcestruzzo, isolamento, finiture",
    "Structure béton, isolation": "Struttura in calcestruzzo, isolamento",
    "Structure bois, isolation": "Struttura in legno, isolamento",
    "Maison compacte de plain-pied, toit-terrasse, 3 chambres · 131 m² utiles": "Casa compatta su un piano, tetto-terrazza, 3 camere · 131 m² utili",
    "Maison compacte de plain-pied, roof-terrasse, 3 chambres · 131 m² utiles": "Casa compatta su un piano, tetto-terrazza, 3 camere · 131 m² utili",
    "Pura est la maison la plus ramassée du catalogue : 156 m² d'emprise pour trois chambres. Volume presque carré, avec toit-terrasse — sans charpente, sans combles.": "Pura è la casa più compatta del catalogo: 156 m² di impronta per tre camere. Volume quasi quadrato, con tetto-terrazza — senza capriate, senza sottotetto.",
    "Pura est la maison la plus ramassée du catalogue : 156 m² d'emprise pour trois chambres. Volume presque carré, avec roof-terrasse — sans charpente, sans combles.": "Pura è la casa più compatta del catalogo: 156 m² di impronta per tre camere. Volume quasi quadrato, con tetto-terrazza — senza capriate, senza sottotetto.",
    "L'espace de vie est une seule pièce de 50 m², orientée vers la terrasse en béton. La cuisine a sa propre fenêtre au-dessus du plan de travail, ce qui compte quand on cuisine dos au séjour.": "La zona giorno è un'unica stanza di 50 m², orientata verso la terrazza in calcestruzzo. La cucina ha la propria finestra sopra il piano di lavoro, importante quando si cucina di spalle al soggiorno.",
    "L'espace de vie est une seule pièce de 50 m², orientée vers la terrasse en calcestruzzo. La cuisine a sa propre fenêtre au-dessus du plan de travail, ce qui compte quand on cuisine dos au séjour.": "La zona giorno è un'unica stanza di 50 m², orientata verso la terrazza in calcestruzzo. La cucina ha la propria finestra sopra il piano di lavoro, importante quando si cucina di spalle al soggiorno.",
    "Chambre principale de 16,1 m², la plus grande du catalogue": "Camera principale da 16,1 m², la più grande del catalogo",
    "Toit-terrasse — pas de charpente à entretenir": "Tetto-terrazza — nessuna capriata da mantenere",
    "Roof-terrasse — pas de charpente à entretenir": "Tetto-terrazza — nessuna capriata da mantenere",
    "Maison premium de plain-pied, avec suite parentale et garage double · 161 m² utiles": "Casa premium su un piano, con suite genitori e garage doppio · 161 m² utili",
    "Premium home de plain-pied, avec suite parentale et garage double · 161 m² utiles": "Casa premium su un piano, con suite genitori e garage doppio · 161 m² utili",
    "La chambre parentale de 17,5 m² a son propre dressing et sa propre salle de bains, regroupés en suite au bout de la maison. Les deux autres chambres ont leur salle de bains, de l'autre côté du couloir — pas de file d'attente le matin.": "La suite genitori da 17,5 m² ha il proprio dressing e il proprio bagno, raggruppati in suite all'estremità della casa. Le altre due camere condividono un bagno dall'altra parte del corridoio — nessuna coda al mattino.",
    "Le bureau de 10,4 m² est près de l'espace de vie, pas entre les chambres. On peut travailler ou recevoir un client sans traverser la chambre de personne. Le garage double communique avec la maison par un cellier technique, pas directement par le séjour.": "Lo studio da 10,4 m² è vicino alla zona giorno, non tra le camere. Si può lavorare o ricevere un cliente senza attraversare la camera di nessuno. Il garage doppio comunica con la casa tramite un locale tecnico, non direttamente dal soggiorno.",
    "Suite parentale : chambre de 17,5 m² + dressing + salle de bains privative": "Suite genitori: camera da 17,5 m² + dressing + bagno privato",
    "Garage double de 36,5 m², avec mur coupe-feu en béton côté maison": "Garage doppio da 36,5 m², con parete tagliafuoco in calcestruzzo lato casa",
    "Garage double de 36,5 m², avec mur coupe-feu en calcestruzzo côté maison": "Garage doppio da 36,5 m², con parete tagliafuoco in calcestruzzo lato casa",
    "Le rez-de-chaussée est une seule pièce : séjour, cuisine et salle à manger, 43 m², avec une baie coulissante vers la terrasse. L'escalier monte près de l'entrée, sans couper l'espace. En bas, il ne reste qu'un WC et le local technique.": "Il piano terra è un'unica stanza: soggiorno, cucina e sala da pranzo, 43 m², con una porta scorrevole verso la terrazza. Le scale salgono vicino all'ingresso, senza tagliare lo spazio. Al piano terra restano solo un WC e il locale tecnico.",
    "Les trois chambres sont à l'étage, avec la salle de bains de 11 m². La séparation entre jour et nuit, c'est le plancher qui la fait, pas une cloison — le meilleur isolant phonique d'une maison.": "Le tre camere sono al piano superiore, con il bagno da 11 m². La separazione tra giorno e notte la fa il solaio, non un tramezzo — il miglior isolamento acustico di una casa.",
    "Le rez-de-chaussée est un seul volume de 48 m² — séjour, cuisine et salle à manger — avec une baie coulissante vers la terrasse. L'escalier monte près de l'entrée. En bas aussi, un WC et un cellier, pour ne pas monter à l'étage pour chaque petite chose.": "Il piano terra è un unico volume di 48 m² — soggiorno, cucina e sala da pranzo — con una porta scorrevole verso la terrazza. Le scale salgono vicino all'ingresso. Al piano terra anche un WC e una dispensa, per non salire al piano superiore per ogni piccola cosa.",
    "En haut, trois chambres presque égales : 15,8 · 15,9 · 16,2 m². Pas de petite chambre pour laquelle les enfants se disputent. La salle de bains de 9,4 m² dessert les trois.": "Sopra, tre camere quasi uguali: 15,8 · 15,9 · 16,2 m². Nessuna cameretta per cui litigare. Il bagno da 9,4 m² serve tutte e tre.",
    "Trois chambres entre 15,8 et 16,2 m² — aucune n'est « la petite chambre »": "Tre camere tra 15,8 e 16,2 m² — nessuna è « la cameretta »",
    "La chambre de 17,8 m² est au rez-de-chaussée, près de la salle de bains et de la buanderie. Elle peut être la chambre des grands-parents, le bureau ou la chambre d'amis — personne ne monte d'escalier s'il ne veut pas. Les trois autres sont en haut, avec deux salles de bains entre elles.": "La camera da 17,8 m² è al piano terra, vicino al bagno e alla lavanderia. Può essere la camera dei nonni, lo studio o la camera degli ospiti — nessuno sale le scale se non vuole. Le altre tre sono sopra, con due bagni tra loro.",
    "Le rez-de-chaussée a le séjour ouvert de 41 m², une buanderie séparée et une salle de bains complète. Le garage peut se construire ou non : il est dessiné en trait interrompu, et le mur entre lui et la maison reste de toute façon, comme mur extérieur.": "Il piano terra ha il soggiorno aperto da 41 m², una lavanderia separata e un bagno completo. Il garage può essere costruito o meno: è disegnato a tratto interrotto, e il muro tra garage e casa resta comunque come parete esterna.",
    "Trois salles de bains pour quatre chambres — une en bas, deux en haut": "Tre bagni per quattro camere — uno al piano terra, due sopra",
    "Buanderie séparée de la salle de bains, au rez-de-chaussée": "Lavanderia separata dal bagno, al piano terra",
    "Le séjour de 30 m² s'ouvre sur le jardin, et la cuisine a son propre cellier de 6,8 m² — rare pour une maison de cette taille, mais ça fait la différence quand on n'a nulle part où ranger.": "Il soggiorno da 30 m² si apre sul giardino, e la cucina ha la propria dispensa da 6,8 m² — raro per una casa di queste dimensioni, ma fa la differenza quando non c'è dove riporre.",
    "La grande chambre fait 15,6 m², la deuxième 12,3. La salle de bains de 7 m² est complète, avec baignoire et douche. Le garage peut se construire ou non : il est dessiné en pointillé, et sans lui l'emprise passe de 113 à 97 m².": "La camera grande è di 15,6 m², la seconda 12,3. Il bagno da 7 m² è completo, con vasca e doccia. Il garage può essere costruito o meno: è disegnato a puntini, e senza di esso l'impronta scende da 113 a 97 m².",
    "La plus petite surface utile du catalogue — le plus petit coût de construction": "La più piccola superficie utile del catalogo — il costo di costruzione più basso",
    "La plus petite surface utile du catalogue — le plus petit cost de construction": "La più piccola superficie utile del catalogo — il costo di costruzione più basso",
    "Cellier de 6,8 m², inhabituel pour une maison de 80 m²": "Dispensa da 6,8 m², insolita per una casa da 80 m²",
    "Tout sur un niveau, sans escalier": "Tutto su un livello, senza scale",
    "Les quatre chambres sont presque identiques : entre 13,6 et 14,2 m², deux de chaque côté du palier. Dans une maison avec quatre enfants, ou avec enfants et bureau, cela veut dire que personne ne se sent lésé.": "Le quattro camere sono quasi identiche: tra 13,6 e 14,2 m², due per lato del pianerottolo. In una casa con quattro figli, o con figli e studio, significa che nessuno si sente penalizzato.",
    "La cuisine est une pièce séparée, pas ouverte sur le séjour. On perd l'effet d'espace, on gagne le calme et l'absence d'odeurs — certains la veulent, d'autres non, mais il est bon que cette variante existe aussi au catalogue.": "La cucina è una stanza separata, non aperta sul soggiorno. Si perde l'effetto spazio, si guadagnano calma e assenza di odori — alcuni la vogliono, altri no, ma è bene che anche questa variante esista nel catalogo.",
    "Quatre chambres sur une emprise de seulement 90 m²": "Quattro camere su un'impronta di soli 90 m²",
    "Des chambres presque égales, entre 13,6 et 14,2 m²": "Camere quasi uguali, tra 13,6 e 14,2 m²",
    "Buanderie à l'étage, près de la salle de bains": "Lavanderia al piano superiore, vicino al bagno",
    "Au-dessus du garage, une chambre : le plancher PBK arrive déjà isolé, sans pont thermique": "Sopra il garage, una camera: il solaio PBK arriva già isolato, senza ponte termico",
    "Les trois chambres et la salle de bains sont regroupées de façon compacte dans la moitié est, reliées par un couloir court. Rien ne se perd en couloirs — c'est pourquoi il en reste autant pour l'espace de vie.": "Le tre camere e il bagno sono raggruppati in modo compatto nella metà est, collegati da un corridoio corto. Nulla si perde nei corridoi — ecco perché ne resta tanto per la zona giorno.",
    "Sans garage et sans découpes dans le plan : un rectangle net de 13 sur 8,6 mètres. C'est la plus simple et la moins chère à monter du catalogue, à qualité de mur égale.": "Senza garage e senza tagli nel progetto: un rettangolo netto di 13 per 8,6 metri. La più semplice e la meno costosa da montare del catalogo, a parità di qualità delle pareti.",
    "Le plus grand séjour du catalogue rapporté à la surface — 42 sur 92 m²": "Il soggiorno più grande del catalogo rispetto alla superficie — 42 su 92 m²",
    "Volume rectangulaire simple, sans découpes — le moins cher à monter": "Volume rettangolare semplice, senza tagli — il meno costoso da montare",
    "Salle de bains de 8,6 m², généreuse pour une maison de 92 m²": "Bagno da 8,6 m², generoso per una casa da 92 m²",
    "Sans garage — le stationnement reste sur l'allée": "Senza garage — il parcheggio resta sul vialetto",
    "Cela la rend adaptée à deux situations que le reste du catalogue ne couvre pas : la grande famille avec de jeunes enfants, où l'escalier est un souci de plus, et deux générations sous le même toit, où les grands-parents ne peuvent pas monter.": "La rende adatta a due situazioni che il resto del catalogo non copre: la famiglia numerosa con bambini piccoli, dove le scale sono un problema in più, e due generazioni sotto lo stesso tetto, dove i nonni non possono salire.",
    "Les quatre chambres sont groupées deux par deux de part et d'autre d'un couloir court, avec la salle de bains au bout. L'espace de vie reste séparé, à l'autre bout de la maison, près du cellier et du garage.": "Le quattro camere sono raggruppate due per due ai lati di un corridoio corto, con il bagno alla fine. La zona giorno resta separata, all'altra estremità della casa, vicino a dispensa e garage.",
    "La seule du catalogue avec quatre chambres sans étage": "L'unica del catalogo con quattro camere senza piano superiore",
    "Garage en option de 28 m², le plus grand du catalogue après Aura": "Garage opzionale da 28 m², il più grande del catalogo dopo Aura",
    "La structure en bois du PolistiSIP utilise une ressource qui se renouvelle et demande moins de béton ; nous publierons les chiffres exacts d'empreinte quand l'analyse complète sera prête.": "La struttura in legno del PolistiSIP utilizza una risorsa rinnovabile e richiede meno calcestruzzo; pubblicheremo i dati esatti sull'impronta quando l'analisi completa sarà pronta.",
    "Transfert thermique U": "Trasmittanza termica U",
    "Poids du mur": "Peso della parete",
    "Structure béton · isolation · <strong>finitions</strong>": "Struttura calcestruzzo · isolamento · <strong>finiture</strong>",
    "Livré avec la plaque de fibrociment sur les deux faces. On enduit directement, sans couche d'égalisation.": "Consegnato con la lastra in fibrocemento su entrambe le facce. Si intonaca direttamente, senza strato di livellamento.",
    "Le coffrage seul": "Solo il cassero",
    "Les panneaux seuls": "Solo i pannelli",
    "Les prix sont estimatifs et se confirment après examen du terrain et du projet. Le coffrage, c'est le matériau livré ; le gros œuvre, c'est la fondation, la structure et la toiture, montées par nous. Les données thermiques viennent des fiches Ubakus du mur.": "I prezzi sono indicativi e si confermano dopo l'analisi del terreno e del progetto. Il cassero è il materiale consegnato; la struttura comprende fondazioni, struttura e copertura, montate da noi. I dati termici provengono dalle schede Ubakus della parete.",
    "Maison compacte de plain-pied, 2 chambres, garage en option · 80 m² utiles": "Casa compatta su un piano, 2 camere, garage opzionale · 80 m² utili",
    "Maison sur un niveau, 3 chambres, séjour ouvert de 42 m² · 92 m² utiles": "Casa su un livello, 3 camere, soggiorno aperto da 42 m² · 92 m² utili",
    "Maison sur un niveau avec 4 chambres, garage en option · 97 m² utiles": "Casa su un livello con 4 camere, garage opzionale · 97 m² utili",
    "Maison à étage, 4 chambres, cuisine fermée · 119 m² utiles sur 90 m² de terrain": "Casa a due piani, 4 camere, cucina chiusa · 119 m² utili su 90 m² di terreno",
    "Maison familiale à étage, 4 chambres et 3 salles de bains · 144 m² utiles": "Casa familiare a due piani, 4 camere e 3 bagni · 144 m² utili",
    "Maison à étage avec garage, 3 chambres · 147 m² utiles": "Casa a deux piani con garage, 3 camere · 147 m² utili",
    "Maison compacte à étage, 3 chambres · 131 m² utiles sur seulement 81 m² de terrain": "Casa compatta a due piani, 3 camere · 131 m² utili su soli 81 m² di terreno",
    "Quatre chambres, dont une au rez-de-chaussée — pour les grands-parents, le bureau ou les invités, sans escalier": "Quattro camere, di cui una al piano terra — per nonni, studio o ospiti, senza scale",
    "Garage en option de 20 m² — qu'on le construise ou non, le plan reste le même": "Garage opzionale da 20 m² — che venga costruito o meno, il progetto resta lo stesso",
    "Garage en option de 13 m² — sans lui, l'emprise descend à 97 m²": "Garage opzionale da 13 m² — senza di esso, l'impronta scende a 97 m²",
    "Cuisine fermée, la seule du catalogue — pas d'odeurs dans l'espace de vie": "Cucina chiusa, l'unica del catalogo — nessun odore nella zona giorno",
    "50 m² séjour + cuisine": "50 m² soggiorno + cucina",
    "43 m² séjour + cuisine": "43 m² soggiorno + cucina",
    "41 m² séjour + cuisine": "41 m² soggiorno + cucina",
    "35 m² séjour + cuisine": "35 m² soggiorno + cucina",
    "30 m² séjour + cuisine": "30 m² soggiorno + cucina",
    "42 m² séjour + cuisine": "42 m² soggiorno + cucina",
    "28 m² séjour": "28 m² soggiorno",
    "rez-de-chaussée": "piano terra",
    "étage": "piano superiore",
    "toit-terrasse": "tetto-terrazza",
    "roof-terrasse": "tetto-terrazza",
    "Maison de plain-pied": "Casa su un piano",
    "maison de plain-pied": "casa su un piano",
    "Maison en L de plain-pied": "Casa a L su un piano",
    "maison en L de plain-pied": "casa a L su un piano",
    "Maison cubique de plain-pied": "Casa cubica su un piano",
    "maison cubique de plain-pied": "casa cubica su un piano",
    "Maison longue, sur un seul niveau": "Casa allungata, su un solo livello",
    "maison longue, sur un seul niveau": "casa allungata, su un solo livello",
    "vue depuis la rue": "vista dalla strada",
    "avec terrasse abritée": "con terrazza riparata",
    "avec tetto-terrasse": "con tetto-terrazza",
    "avec toit-terrasse": "con tetto-terrazza",
    "MODÈLE": "MODELLO",
    "Modèle": "Modello",
    "modèle": "modello",
    "catalogue": "catalogo",
    "Catalogue": "Catalogo",
    "fondation": "fondazioni",
    "Fondation": "Fondazioni",
    "charpente": "capriata",
    "combles": "sottotetto",
    "baie coulissante": "porta scorrevole",
    "cellier": "dispensa",
    "Cellier": "Dispensa",
    "vestibule": "vestibolo",
    "couloir": "corridoio",
    "Couloir": "Corridoio",
    "invités": "ospiti",
    "grands-parents": "nonni",
    "enfants": "bambini",
    "famille": "famiglia",
    "Famille": "Famiglia",
    "terrain étroit": "terreno stretto",
    "terrain ordinaire": "terreno ordinario",
    "emprise": "impronta",
    "niveau": "livello",
    "Niveau": "Livello",
    "volume": "volume",
    "Volume": "Volume",
    "pièce": "stanza",
    "pièces": "stanze",
    "Pièce": "Stanza",
    "cuisine": "cucina",
    "Cuisine": "Cucina",
    "salle à manger": "sala da pranzo",
    "espace de vie": "zona giorno",
    "Espace de vie": "Zona giorno",
    "zone de nuit": "zona notte",
    "zone où l'on dort": "zona notte",
    "mur extérieur": "parete esterna",
    "Mur extérieur": "Parete esterna",
    "mur coupe-feu": "parete tagliafuoco",
    "gros œuvre": "struttura",
    "Gros œuvre": "Struttura",
    "finitions": "finiture",
    "Finitions": "Finiture",
    "main-d'œuvre": "manodopera",
    "prix de structure": "prezzo strutturale",
    "prix de vente": "prezzo di vendita",
    "grille": "griglia",
    "distribution": "distribuzione",
    "Variante": "Variante",
    "variante": "variante",
    "PolistiSIP": "PolistiSIP",
    "Polistiwall": "Polistiwall",
    "Polistibrick": "Polistibrick",
    # --- per/proprietari ---
    "Per i proprietari · La maison à vie senza bollette — Polistibrick": "Per i proprietari · La casa per tutta la vita senza bollette — Polistibrick",
    "Facture d'énergie &lt; 50 €/mois": "Bolletta energetica &lt; 50 €/mese",
    "Facture d'énergie < 50 €/mois": "Bolletta energetica < 50 €/mese",
    "Polistibrick consomme 15 kWh/m²/an, contre 104 pour une maison existante qui a aussi la climatisation. Vous économisez environ 86 % sur vos factures, pour la vie.": "Polistibrick consuma 15 kWh/m²/anno, contro 104 per una casa esistente con anche la climatizzazione. Risparmiate circa l'86% sulle bollette, per tutta la vita.",
    "Polistibrick consomme 15 kWh/m²/an, contre 104 pour une maison existante qui a aussi la climatisation. Vous économisez environ 86 % sur vos bollette, pour la vie.": "Polistibrick consuma 15 kWh/m²/anno, contro 104 per una casa esistente con anche la climatizzazione. Risparmiate circa l'86% sulle bollette, per tutta la vita.",
    "La maison à 80 % en 4 à 6 settimane": "La casa all'80% in 4–6 settimane",
    "La structure se monte 3 fois plus vite que la maçonnerie classique. Vous emménagez en quelques mois, pas en quelques années. Moins de stress, moins de retards.": "La struttura si monta 3 volte più velocemente della muratura classica. Traslocate in pochi mesi, non in anni. Meno stress, meno ritardi.",
    "Calme, sécurité, sérénité": "Calma, sicurezza, serenità",
    "52 dB d'isolamento acustico, A1 anti-feu, antisismique Eurocode 8. Votre maison protège votre famille de tout — le bruit, le feu, la terre qui tremble.": "52 dB di isolamento acustico, A1 antincendio, antisismico Eurocode 8. La vostra casa protegge la famiglia da tutto — rumore, fuoco, terremoti.",
    "Jamais de moisissures": "Mai muffe",
    "L'EPS à cellules fermées n'absorbe pas l'eau. Vos murs restent secs, vos enfants respirent un air sain, pas de problèmes d'humidité dans 10 ans.": "L'EPS a celle chiuse non assorbe acqua. I muri restano asciutti, i bambini respirano aria sana, nessun problema di umidità tra 10 anni.",
    "L'EPS à cellules fermées n'absorbe pas l'eau. Vos pareti restent secs, vos enfants respirent un air sain, pas de problèmes d'humidité dans 10 ans.": "L'EPS a celle chiuse non assorbe acqua. Le pareti restano asciutte, i bambini respirano aria sana, nessun problema di umidità tra 10 anni.",
    "Une casa passiva certifiée RE2020 se revend 15 à 25 % plus cher qu'une maison classique. Polistibrick = investissement qui se valorise dans le temps.": "Una casa passiva certificata RE2020 si rivende il 15–25% in più rispetto a una casa classica. Polistibrick = investimento che si valorizza nel tempo.",
    "Unea casa passiva certifiée RE2020 se revend 15 à 25 % plus cher qu'une maison classique. Polistibrick = investissement qui se valorise dans le temps.": "Una casa passiva certificata RE2020 si rivende il 15–25% in più rispetto a una casa classica. Polistibrick = investimento che si valorizza nel tempo.",
    "Toujours 21 °C, sans effort": "Sempre 21 °C, senza sforzo",
    "L'inertie thermique du béton + l'EPS maintiennent une température constante. Pas de coup de froid en hiver, pas de canicule en été. Confort total.": "L'inerzia termica del calcestruzzo + l'EPS mantengono una temperatura costante. Niente colpi di freddo in inverno, niente ondate di caldo in estate. Comfort totale.",
    "L'inertie thermique du calcestruzzo + l'EPS maintiennent une température constante. Pas de coup de froid en inverno, pas de canicule en été. Confort total.": "L'inerzia termica del calcestruzzo + l'EPS mantengono una temperatura costante. Niente colpi di freddo in inverno, niente ondate di caldo in estate. Comfort totale.",
    "Combien votre maison <em style=\"font-style:italic;color:var(--red);font-weight:400;\">vous fera économiser ?</em>": "Quanto vi farà risparmiare la vostra casa <em style=\"font-style:italic;color:var(--red);font-weight:400;\">?</em>",
    "Indiquez la surface de votre future maison. Nous calculons la facture annuelle de chauffage avec Polistibrick MBK 300 face à une maison existante moyenne.": "Indicate la superficie della vostra futura casa. Calcoliamo la bolletta annuale di riscaldamento con Polistibrick MBK 300 rispetto a una casa esistente media.",
    "Indiquez la surface de votre future maison. Nous calculons la bolletta annuelle de riscaldamento avec Polistibrick MBK 300 face à une maison existante moyenne.": "Indicate la superficie della vostra futura casa. Calcoliamo la bolletta annuale di riscaldamento con Polistibrick MBK 300 rispetto a una casa esistente media.",
    "Surface habitable de votre maison :": "Superficie abitabile della vostra casa:",
    "Avec une maison existante": "Con una casa esistente",
    "maison existante": "casa esistente",
    "Nous avons un <strong>réseau d'architectes formés Polistibrick</strong> partout en France.": "Abbiamo una <strong>rete di architetti formati Polistibrick</strong> in tutta Europa.",
    "Nous avons un <strong>réseau d'architectes formés Polistibrick</strong> partout en Francia.": "Abbiamo una <strong>rete di architetti formati Polistibrick</strong> in tutta Europa.",
    "Polistibrick est <strong>une structure en béton armé classique</strong> — n'importe quel maçon, plombier ou électricien peut intervenir.": "Polistibrick è <strong>una struttura in calcestruzzo armato classica</strong> — qualsiasi muratore, idraulico o elettricista può intervenire.",
    "Polistibrick est <strong>une structure en calcestruzzo armé classique</strong> — n'importe quel maçon, plombier ou électricien peut intervenir.": "Polistibrick è <strong>una struttura in calcestruzzo armato classica</strong> — qualsiasi muratore, idraulico o elettricista può intervenire.",
    # --- chi-siamo ---
    "Tout commence  sur le chantier.": "Tutto inizia in cantiere.",
    "Nous construisons aujourd'hui  le case di domani.": "Costruiamo oggi le case di domani.",
    "Des spécialistes  a un click di distanza.": "Specialisti a un clic di distanza.",
    "Les usines Polistibrick de  Valencia (Espagne)  et de  Craiova (Romania)  produisent les panneaux MBK, PBK et TBK selon les standards": "Le fabbriche Polistibrick di Valencia (Spagna) e Craiova (Romania) producono i pannelli MBK, PBK e TBK secondo gli standard",
    "Les usines Polistibrick de  Valencia (Espagne)  et de  Craiova (Romania)  produisent i pannelli MBK, PBK e TBK secondo gli standard": "Le fabbriche Polistibrick di Valencia (Spagna) e Craiova (Romania) producono i pannelli MBK, PBK e TBK secondo gli standard",
    "Polistibrick détient le brevet européen du système de construction ICF intégré — le seul à réunir dans un même produit préfabriqué le coffrage, l'isolation continue, la structure porteuse et le support pour finitions.": "Polistibrick detiene il brevetto europeo del sistema di costruzione ICF integrato — l'unico a riunire in un unico prodotto prefabbricato il cassero, l'isolamento continuo, la struttura portante e il supporto per le finiture.",
    "Polistibrick détient le sistema brevettato europeo du système de construction ICF intégré — le seul à réunir dans un même produit préfabriqué le cassero, l'isolamento continue, la structure porteuse et le support pour finitions.": "Polistibrick detiene il brevetto europeo del sistema di costruzione ICF integrato — l'unico a riunire in un unico prodotto prefabbricato il cassero, l'isolamento continuo, la struttura portante e il supporto per le finiture.",
    "Fondateur &amp; CEO · Inventeur du système Polistibrick": "Fondatore &amp; CEO · Inventore del sistema Polistibrick",
    "Il fondatore de Polistibrick · Lucian Bouleanu": "Il fondatore di Polistibrick · Lucian Bouleanu",
    # --- contact / partner ---
    "Votre message arrive directement à l'équipe du pays sélectionné.": "Il vostro messaggio arriva direttamente al team del paese selezionato.",
    "Écrivez-nous directement.": "Scriveteci direttamente.",
    "Un cliente diretto costruisce una casa.  Un partenaire Polistibrick construit 10 à 50 maisons par an.": "Un cliente diretto costruisce una casa. Un partner Polistibrick costruisce 10–50 case all'anno.",
    "Candidati per diventare partner certificato. Sous 3 jours ouvrés, nous vous contactons pour fixer la date du cours de certification.": "Candidati per diventare partner certificato. Entro 3 giorni lavorativi ti contattiamo per fissare la data del corso di certificazione.",
    "Sous 3 jours ouvrés, nous vous contactons pour fixer la date du cours de certification.": "Entro 3 giorni lavorativi ti contattiamo per fissare la data del corso di certificazione.",
    # --- testimonianze ---
    "Après 2 hivers dans la maison Polistibrick, je n'ai plus jamais rallumé la chaudière.": "Dopo 2 inverni nella casa Polistibrick, non ho più mai riacceso la caldaia.",
    "Pago 38 €/mese, mentre i vicini con il mattone pagano 300+.": "Pago 38 €/mese, mentre i vicini con il mattone pagano oltre 300.",
    "2 ans après l'emménagement, la maison est silencieuse, chaude, et je peux dormir sans me réveiller avec les radiateurs.": "2 anni dopo il trasloco, la casa è silenziosa, calda, e posso dormire senza svegliarmi per i radiatori.",
    "Je me disais : « Ce sera l'humidité, la moisissure, la catastrophe. » Après 3 ans — rien. Les murs sont secs, la maison respire, je n'ai jamais traversé une saison difficile.": "Mi dicevo: « Sarà umidità, muffa, catastrofe. » Dopo 3 anni — nulla. I muri sono asciutti, la casa respira, non ho mai attraversato una stagione difficile.",
    "Je me disais : « Ce sera l'humidité, la moisissure, la catastrophe. » Après 3 ans — rien. Les pareti sont secs, la maison respire, je n'ai jamais traversé une saison difficile.": "Mi dicevo: « Sarà umidità, muffa, catastrofe. » Dopo 3 anni — nulla. Le pareti sono asciutte, la casa respira, non ho mai attraversato una stagione difficile.",
    "Per gli architetti, Polistibrick est un cadeau. Des portées de 9 m sans charpente, sans ponts thermiques à calculer. Je valide le PHPP du premier coup, sans ajustements. Et les clients adorent le prix.": "Per gli architetti, Polistibrick è un regalo. Luci di 9 m senza capriate, senza ponti termici da calcolare. Valido il PHPP al primo colpo, senza aggiustamenti. E i clienti adorano il prezzo.",
    "De courtes vidéos avec des factures réelles, des changements réels, des leçons réelles.": "Brevi video con bollette reali, cambiamenti reali, lezioni reali.",
    "De courtes vidéos avec des bollette réelles, des changements réels, des leçons réelles.": "Brevi video con bollette reali, cambiamenti reali, lezioni reali.",
    # --- risparmi ---
    "Le calcul inclut à la fois le chauffage (hiver) et la climatisation (été).": "Il calcolo include sia il riscaldamento (inverno) sia la climatizzazione (estate).",
    "Le calcul inclut à la fois le riscaldamento (inverno) et la climatisation (été).": "Il calcolo include sia il riscaldamento (inverno) sia la climatizzazione (estate).",
    "💡 Le calcul inclut :": "💡 Il calcolo include:",
    "Mattone : ~1 000 €/m² en standard non conforme. Polistibrick : ~1 050 €/m² (+5 %) pour une casa passiva A+++. Inclut les matériaux et la main-d'œuvre, hors finitions intérieures ou extérieures.": "Mattone: ~1.000 €/m² in standard non conforme. Polistibrick: ~1.050 €/m² (+5%) per una casa passiva A+++. Include materiali e manodopera, escluse finiture interne o esterne.",
    "Basé sur la consommation typique par climat : la brique consomme en moyenne 100-180 kWh/m²/an pour le chauffage et la climatisation. Polistibrick (passive) consomme 25-45 kWh/m²/an. Réduction moyenne de 70 %.": "Basato sul consumo tipico per clima: il mattone consuma in media 100-180 kWh/m²/anno per riscaldamento e climatizzazione. Polistibrick (passiva) consuma 25-45 kWh/m²/anno. Riduzione media del 70%.",
    "Basé sur la consommation typique par climat : la mattone consomme en moyenne 100-180 kWh/m²/an pour le riscaldamento et la climatisation. Polistibrick (passiva) consuma 25-45 kWh/m²/anno. Réduction moyenne de 70 %.": "Basato sul consumo tipico per clima: il mattone consuma in media 100-180 kWh/m²/anno per riscaldamento e climatizzazione. Polistibrick (passiva) consuma 25-45 kWh/m²/anno. Riduzione media del 70%.",
    "Nous pensons que la performance supérieure ne doit pas être réservée à ceux qui ont un budget illimité. La Casa Passiva Polistibrick coûte autant qu'une maison classique — soit 30 % de moins que l'alternative passive traditionnelle.": "Crediamo che le prestazioni superiori non debbano essere riservate a chi ha un budget illimitato. La Casa Passiva Polistibrick costa quanto una casa classica — cioè il 30% in meno dell'alternativa passiva tradizionale.",
    # --- legal privacy ---
    "Le responsable du traitement est la société": "Il titolare del trattamento è la società",
    "Via nos formulaires : identité (nom, email, téléphone), informations projet (localisation, surface, type de construction), pièces jointes que vous choisissez d'envoyer.": "Tramite i nostri moduli: identità (nome, email, telefono), informazioni progetto (località, superficie, tipo di costruzione), allegati che scegliete di inviare.",
    "Vos données ne sont pas vendues.": "I vostri dati non vengono venduti.",
    "Nous faisons appel aux prestataires suivants, strictement pour les finalités indiquées :": "Ci avvaliamo dei seguenti fornitori, rigorosamente per le finalità indicate:",
    "Nous partageons également vos données avec les partenaires constructeurs certifiés lorsque cela est nécessaire à l'exécution de votre projet, et uniquement avec votre accord explicite.": "Condividiamo anche i vostri dati con i partner costruttori certificati quando necessario per l'esecuzione del vostro progetto, e solo con il vostro consenso esplicito.",
    "Demandes via formulaire : 5 ans pour les clients, 12 mois pour les prospects non convertis.": "Richieste via modulo: 5 anni per i clienti, 12 mesi per i prospect non convertiti.",
    "Vous pouvez introduire une réclamation auprès de la": "Potete presentare un reclamo presso la",
    # --- montaggio leftovers ---
    "Les panneaux EPS sont dressés et fixés sur la fondation avec un étaiement latéral en bois. Assemblage à sec : sans mortier, sans perte d'isolation.": "I pannelli EPS sono eretti e fissati sulla fondazione con puntellatura laterale in legno. Assemblaggio a secco: senza malta, senza perdite di isolamento.",
    "Les pareti EPS sont dressés et fixés sur la fondation avec un étaiement latéral en bois. Assemblage à sec : sans mortier, sans perte d'isolamento.": "Le pareti EPS sono erette e fissate sulla fondazione con puntellatura laterale in legno. Assemblaggio a secco: senza malta, senza perdite di isolamento.",
    "Les treillis d'acier se placent entre les nervures EPS-Graphite. C'est ce qui crée la liaison monolithique entre les murs et le plancher.": "Le reti d'armatura in acciaio si posano tra le nervature EPS-Grafite. Questo crea il collegamento monolitico tra pareti e solaio.",
    "Les treillis d'acier se placent entre les nervatures EPS-Graphite. C'est ce qui crée la liaison monolithique entre les pareti et le plancher.": "Le reti d'armatura in acciaio si posano tra le nervature EPS-Grafite. Questo crea il collegamento monolitico tra pareti e solaio.",
    "Tous les éléments sont assemblés et vérifiés. La maison est désormais prête pour le coulage du béton.": "Tutti gli elementi sono assemblati e verificati. La casa è ora pronta per il getto di calcestruzzo.",
    "Tous les éléments sont assemblés et vérifiés. La maison est désormais prête pour le coulage du calcestruzzo.": "Tutti gli elementi sono assemblati e verificati. La casa è ora pronta per il getto di calcestruzzo.",
    "Le gros œuvre fermé en semaines au lieu de mois. Vous emménagez plus tôt et payez moins d'intérêts de chantier.": "Struttura chiusa in settimane invece che in mesi. Traslocate prima e pagate meno interessi di cantiere.",
    "Quelques semaines": "Poche settimane",
    "Quelques settimane": "Poche settimane",
    "Le cassero isolant qui se dresse à la main. Isolation intégrée, prêt pour le béton.": "Il cassero isolante che si erige a mano. Isolamento integrato, pronto per il calcestruzzo.",
    "Les dalles porteuses EPS-Graphite + fibrociment, posées horizontalement et armées sur place.": "Le sole in EPS-Grafite + fibrocemento, posate orizzontalmente e armate in cantiere.",
    "La toiture Passivhaus qui sort d'usine prête à poser. Étanchéité à l'air, sans pont thermique.": "La copertura Passivhaus che esce di fabbrica pronta da posare. Tenuta all'aria, senza ponte termico.",
    "La tettoure Passivhaus qui sort d'usine prête à poser. Étanchéité à l'air, sans pont thermique.": "La copertura Passivhaus che esce di fabbrica pronta da posare. Tenuta all'aria, senza ponte termico.",
    # --- prodotti technical ---
    "De l'intérieur vers l'extérieur. Feu&nbsp;: B-s1, d0 . Entre chaque panneau&nbsp;: poutre I-Joist .": "Dall'interno verso l'esterno. Fuoco&nbsp;: B-s1, d0. Tra ogni pannello&nbsp;: trave I-Joist.",
    "Portée max. 6 m 7,5 m 9 m": "Luce max. 6 m 7,5 m 9 m",
    "Déphasage confort d'été 7,3 h": "Sfasamento comfort estivo 7,3 h",
    "Épaisseur totale 25 cm": "Spessore totale 25 cm",
    "OSB + EPS graphité + I-Joist STEICO": "OSB + EPS grafite + I-Joist STEICO",
    "OSB/3 intérieur 15 mm": "OSB/3 interno 15 mm",
    "OSB/3 extérieur 15 mm": "OSB/3 esterno 15 mm",
    "Isolant PSE graphité (λ 0,031) 220 mm": "Isolante EPS grafite (λ 0,031) 220 mm",
    "Après coulage": "Dopo il getto",
    "Six équipes. Sept postes.": "Sei squadre. Sette posti.",
    "1. Maçonnerie": "1. Muratura",
    "3. Étanchéité à l'air": "3. Tenuta all'aria",
    "3. Étanchéité à l'air": "3. Tenuta all'aria",
    "Sans erreurs d'exécution": "Senza errori di esecuzione",
    "→ Vous finissez l'intérieur": "→ Completate l'interno",
    "→ Vous finissez l'intérieur": "→ Completate l'interno",
    "Comme Brick, sans intérieur": "Come Mattone, senza interni",
    "25 ans (recommandé)": "25 anni (consigliato)",
    "Tempéré (Europe centrale — 8-14 °C en moyenne)": "Temperato (Europa centrale — 8-14 °C in media)",
    "100 % Certifiés Passivhaus": "100% certificati Passivhaus",
    "9m Portées max.": "9 m luci max.",
    "−72 % Énergie vs voisin": "−72% energia vs vicino",
    "Jean-François Roux": "Jean-François Roux",
    "Architecte partenaire · 12 projets Polistibrick livrés": "Architetto partner · 12 progetti Polistibrick consegnati",
    "Co-branding régional": "Co-branding regionale",
    "Formation pratique au calepinage, à l'étaiement et au coulage avec nos formateurs chantier.": "Formazione pratica al calepinaggio, al puntellamento e al getto con i nostri formatori di cantiere.",
    "Démarrez vos travaux l'esprit tranquille, avec la présence de notre ingénieur d'application.": "Iniziate i lavori con tranquillità, con la presenza del nostro ingegnere applicativo.",
    "2 à 3 jours intensifs dans nos usines. Pratique réelle de montage et de découpe des panneaux. Certification officielle constructeur.": "2–3 giorni intensivi nelle nostre fabbriche. Pratica reale di montaggio e taglio dei pannelli. Certificazione ufficiale costruttore.",
    "Mise en avant de vos chantiers sur nos supports nationaux pour consolider votre réputation de constructeur passif premium.": "Valorizzazione dei vostri cantieri sui nostri canali nazionali per consolidare la reputazione di costruttore passivo premium.",
    "Les commandes usine sont traitées en priorité pour une livraison selon le planning exact du chantier.": "Gli ordini di fabbrica sono trattati prioritariamente per una consegna secondo il planning esatto del cantiere.",
}


def it_rel_to_fr_rel(rel: str) -> str:
    parts = rel.split("/")
    out = []
    for p in parts:
        out.append(IT_TO_FR.get(p, p))
    return "/".join(out)


def load_mercury_py() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location(
        "tm", TRANS / "translate_mercury_it.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TRANSLATIONS


def build_mapping() -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in (
        "fr_to_it.json",
        "mercury_fr_to_it.json",
        "extra_fr_to_it.json",
        "remaining_fr_it.json",
        "pass3_fr_to_it.json",
        "it_chunk_A.json",
        "it_chunk_B.json",
    ):
        p = TRANS / name
        if p.exists():
            for k, v in json.loads(p.read_text(encoding="utf-8")).items():
                if k and v:
                    merged[k] = v
    for k, v in load_mercury_py().items():
        if k and v:
            merged[k] = v
    merged.update(PASS2)
    return filter_mapping(merged)


def count_replacements(before: str, after: str, mapping: dict[str, str]) -> int:
    n = 0
    for k in mapping:
        if k in before and k not in after:
            n += before.count(k)
    return n


def main() -> None:
    mapping = build_mapping()
    # persist pass2 into remaining_fr_it + extra
    remaining = json.loads((TRANS / "remaining_fr_it.json").read_text(encoding="utf-8"))
    extra = json.loads((TRANS / "extra_fr_to_it.json").read_text(encoding="utf-8"))
    for k, v in PASS2.items():
        if k and v:
            remaining[k] = v
            extra[k] = v
    (TRANS / "remaining_fr_it.json").write_text(
        json.dumps(remaining, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (TRANS / "extra_fr_to_it.json").write_text(
        json.dumps(extra, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    targets = [IT_DIR / p for p in PRIORITY if (IT_DIR / p).exists()]
    # also all IT html
    all_files = sorted(set(IT_DIR.rglob("*.html")) | set(targets))

    total_repl = 0
    changed: list[str] = []
    for path in sorted(all_files):
        orig = path.read_text(encoding="utf-8")
        text = orig
        for _ in range(8):
            text = apply_dict(text, mapping)
        if text != orig:
            total_repl += count_replacements(orig, text, mapping)
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(IT_DIR).as_posix())
            print(f"  ✓ {path.relative_to(IT_DIR)}")

    print(f"\nPass 2: {len(mapping)} keys, {len(changed)} files, ~{total_repl} replacements")


if __name__ == "__main__":
    main()
