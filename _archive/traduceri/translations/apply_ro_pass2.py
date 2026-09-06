#!/usr/bin/env python3
"""Pass 2: apply extra_fr_to_ro + batch4 to all countries/ro HTML."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
RO_DIR = ROOT / "countries" / "ro"

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

# Pass-2 additions — focus files + technical specs
BATCH4: dict[str, str] = {
    # === MONTAJ ===
    "Le montage Polistibrick · Une casă montée à la main, en quelques săptămâni": "Montajul Polistibrick · O casă ridicată manual, în câteva săptămâni",
    "Comment se monte une casă Polistibrick : assemblage à sec, sani grue, par 2 à 3 personnes. De la fondation au cofraj fermé en quelques săptămâni, monolithique en 24 h après le coulage.": "Cum se montează o casă Polistibrick: asamblare uscată, fără macara, cu 2–3 persoane. De la fundație la cofraj închis în câteva săptămâni, monolitică în 24 h după turnare.",
    "Montée à la main, <em>en quelques săptămâni.</em>": "Ridicată manual, <em>în câteva săptămâni.</em>",
    "Pas de grue. Pas de gros œuvre interminable. Le système Polistibrick s'assemble <strong>à sec</strong>, élément par élément, par une équipe de <strong>2 à 3 personnes</strong> — jusqu'au cofraj fermé, prêt pour le coulage du beton.": "Fără macara. Fără structură interminabilă. Sistemul Polistibrick se asamblează <strong>uscat</strong>, element cu element, de o echipă de <strong>2–3 persoane</strong> — până la cofrajul închis, gata pentru turnarea betonului.",
    "Montaj des pereți Polistibrick sur le chantier": "Montaj pereți Polistibrick pe șantier",
    "Vidéo du montage — bientôt disponible": "Videoclip montaj — în curând",
    "Le montage en vidéo<span>Bientôt disponible</span>": "Montajul în video<span>În curând</span>",
    "Le montage complet, du sol au cofraj fermé.": "Montajul complet, de la sol la cofrajul închis.",
    "O casa completa <em>în 4 pași.</em>": "O casă completă <em>în 4 pași.</em>",
    "De la fondation au cofraj fermé. L'ensemble du processus en quelques săptămâni, avec seulement 2 à 3 personnes sur le chantier — sani mortier et sani perte d'izolație.": "De la fundație la cofrajul închis. Întregul proces în câteva săptămâni, cu doar 2–3 persoane pe șantier — fără mortar și fără pierderi de izolație.",
    "Cofraj : pereți EPS dressés avec étaiement": "Cofraj: pereți EPS ridicați cu sprijiniri",
    "Les pereți EPS sunt dressés et fixés sur la fondation avec un étaiement latéral en lemn. Assemblage à sec : sani mortier, sani perte d'izolație.": "Panourile EPS sunt ridicate și fixate pe fundație cu sprijiniri laterale din lemn. Asamblare uscată: fără mortar, fără pierderi de izolație.",
    "Planșeu PBK posé": "Planșeu PBK montat",
    "Les panneaux PBK 250 sont posés horizontalement — couches EPS-Graphite + fibrociment, prêtes à recevoir l'armature.": "Panourile PBK 250 sunt așezate orizontal — straturi EPS-Grafit + fibrociment, gata să primească armătura.",
    "Fier-beton entre les nervures": "Fier-beton între nervuri",
    "Les treillis d'acier se placent entre les nervures EPS-Graphite. C'est ce qui crée la liaison monolithique entre les pereți et le plancher.": "Plasele de oțel se așază între nervurile EPS-Grafit. Aceasta creează legătura monolitică între pereți și planșeu.",
    "Cofraj fermé, prêt pour le coulage": "Cofraj închis, gata pentru turnare",
    "Tous les éléments sont assemblés et vérifiés. La casă est désormais prête pour le coulage du beton.": "Toate elementele sunt asamblate și verificate. Casa este acum gata pentru turnarea betonului.",
    "Après le coulage, la structure devient <strong>monolitică în 24 hours</strong> — pereți, planșee et acoperiș isolés en continu, sani ponts thermiques.": "După turnare, structura devine <strong>monolitică în 24 de ore</strong> — pereți, planșee și acoperiș izolate continuu, fără punți termice.",
    "Un chantier <em>plus simple, plus rapide, plus propre.</em>": "Un șantier <em>mai simplu, mai rapid, mai curat.</em>",
    "Sani grue": "Fără macara",
    "Les éléments sont légers et se manipulent à la main. Aucun engin de levage lourd, aucun accès spécial requis sur le terrain.": "Elementele sunt ușoare și se manipulează manual. Niciun utilaj greu de ridicat, niciun acces special pe teren.",
    "Une petite équipe suffit. Moins de main-d'œuvre, moins de coordination, moins de coûts de chantier.": "O echipă mică e suficientă. Mai puțină manoperă, mai puțină coordonare, costuri mai mici de șantier.",
    "À sec, sani mortier": "Uscat, fără mortar",
    "L'assemblage est mécanique et à sec. Pas de temps de séchage entre les étapes, pas de mvarao qui bloque le chantier.": "Asamblarea e mecanică și uscată. Fără timp de uscare între etape, fără vreme care blochează șantierul.",
    "Structura fermé en săptămâni au lieu de lună. Vous emménagez plus tôt et payez moins d'intérêts de chantier.": "Structura se închide în săptămâni, nu luni. Te muți mai repede și plătești mai puține dobânzi de șantier.",
    "Après le coulage, beton et izolație ne font plus qu'un. Une coquille continue, sani joints ni ponts thermiques.": "După turnare, betonul și izolația devin unul singur. O cochilie continuă, fără rosturi sau punți termice.",
    "Peu de déchets, peu de poussière, des tolérances d'usine. Un chantier net du début à la fin.": "Puține deșeuri, puțin praf, toleranțe de fabrică. Un șantier curat de la început până la sfârșit.",
    "Le chantier, <em>réduit à l'essentiel.</em>": "Șantierul, <em>redus la esențial.</em>",
    "Gros œuvre fermé (vs 4–5 lună)": "Structură închisă (vs 4–5 luni)",
    "Personnes sur le chantier": "Persoane pe șantier",
    "Grue ou engin de levage lourd": "Macara sau utilaj greu de ridicat",
    "Trois éléments, <em>une seule coquille.</em>": "Trei elemente, <em>o singură cochilie.</em>",
    "Le cofraj isolant qui se dresse à la main. Izolație intégrée, prêt pour le beton.": "Cofrajul izolant ridicat manual. Izolație integrată, gata pentru beton.",
    "Voir les pereți MBK →": "Vezi pereții MBK →",
    "Les dalles porteuses EPS-Graphite + fibrociment, posées horizontalement et armées sur fața locului.": "Plăcile portante EPS-Grafit + fibrociment, așezate orizontal și armate pe fața locului.",
    "Voir les planșee PBK →": "Vezi planșeele PBK →",
    "La acoperișure Passivhaus qui sort d'usine prête à poser. Étanche à l'air, sani pont thermique.": "Acoperișul Passivhaus care iese din fabrică gata de montaj. Etanș la aer, fără pod termic.",
    "Voir le acoperiș TBK →": "Vezi acoperișul TBK →",
    "Manuels de montage détaillés, vidéos par élément (pereți, planșee, acoperiș) et fiches techniques sont disponibles dani l'espace professionnel.": "Manuale de montaj detaliate, videoclipuri pe element (pereți, planșee, acoperiș) și fișe tehnice sunt disponibile în spațiul profesional.",
    "Espace constructeurs": "Spațiu constructori",
    "Prêt à voir votre casă <em>sortir de terre ?</em>": "Gata să vezi casa ta <em>ridicându-se?</em>",

    # === ECONOMII ===
    "Calculator economii · Cât economisești cu Polistibrick — 25 years": "Calculator economii · Cât economisești cu Polistibrick — 25 de ani",
    "Calculator dynamique qui montre combien vous économisez avec Polistibrick par rapport à la cărămidă classique sur 25 ani. Saisissez les m², le climat, le prix de l'énergie et visualisez la différence réelle.": "Calculator dinamic care arată cât economisești cu Polistibrick față de cărămida clasică pe 25 de ani. Introdu m², clima, prețul energiei și vezi diferența reală.",
    "Polistibrick vs cărămidă : <em>vos chiffres.</em>": "Polistibrick vs cărămidă: <em>cifrele tale.</em>",
    "Calculator dynamique qui vous montre EXACTEMENT combien vous économisez sur l'énergie, l'entretien et les coûts totaux sur 25 ani, pour la casă que vous souhaitez construire. Saisissez vos chiffres, visualisez le résultat en temps réel.": "Calculator dinamic care îți arată EXACT cât economisești la energie, întreținere și costuri totale pe 25 de ani, pentru casa pe care vrei să o construiești. Introdu cifrele, vezi rezultatul în timp real.",
    "Les données de votre casă.": "Datele casei tale.",
    "Surface de la casă (m²)": "Suprafața casei (m²)",
    "25 ani (recommandé)": "25 ani (recomandat)",
    "Froid (zones montagneuses, nord — &lt; 8 °C en moyenne)": "Rece (zone montane, nord — &lt; 8 °C în medie)",
    "Tempéré (Europe centrale — 8-14 °C en moyenne)": "Temperat (Europa Centrală — 8–14 °C în medie)",
    "Chaud (sud, méditerranéen — &gt; 14 °C en moyenne)": "Cald (sud, mediteranean — &gt; 14 °C în medie)",
    "Le calcul inclut à la fois le încălzire (iarna) et la climatisation (vara).": "Calculul include atât încălzirea (iarna) cât și climatizarea (vara).",
    "0 % — prix constant (optimiste)": "0 % — preț constant (optimist)",
    "2 % — inflation stable": "2 % — inflație stabilă",
    "4 % — réaliste (moyenne UE 2010-2024)": "4 % — realist (media UE 2010–2024)",
    "6 % — pessimiste (crise énergétique)": "6 % — pesimist (criză energetică)",
    "💡 Le calcul inclut :": "💡 Calculul include:",
    "Coût de construcție (panneaux + main-d'œuvre, hors finitions)": "Cost de construcție (panouri + manoperă, fără finisaje)",
    "Coût de l'énergie sur les années sélectionnées": "Costul energiei pe anii selectați",
    "Coût d'entretien estimé": "Cost de întreținere estimat",
    "Le tout projeté avec l'inflation choisie": "Totul proiectat cu inflația aleasă",
    "sur <span id=\"yearsLabel\">25</span> de years, pentru o house de <span id=\"surfaceLabel\">150</span> m²": "pe <span id=\"yearsLabel\">25</span> de ani, pentru o casă de <span id=\"surfaceLabel\">150</span> m²",
    "Économies totales avec Polistibrick": "Economii totale cu Polistibrick",
    "Entretien sur 25 ani": "Întreținere pe 25 de ani",
    "Énergie (cumulé)": "Energie (cumulată)",
    "€ Énergie (cumulé)": "€ Energie (cumulată)",
    "Basé sur la consommation typique par climat": "Bazat pe consumul tipic pe climă",
    "consomme en moyenne": "consumă în medie",

    # === PATENT ===
    "Un système protégé à l'échelle européenne.": "Un sistem protejat la nivel european.",
    "Polistibrick détient le brevet européen du système de construcție ICF intégré — le seul à réunir dani un même produit préfabriqué": "Polistibrick deține brevetul european al sistemului ICF integrat — singurul care reunește într-un singur produs prefabricat",
    "Protégé · Franța &amp; Europe": "Protejat · Franța &amp; Europa",
    "Le système breveté Polistibrick.": "Sistemul brevetat Polistibrick.",
    "Objet : système de construcție ICF intégré — cofraj, izolație continue, structure porteuse et support de finitions réunis dani un": "Obiect: sistem constructiv ICF integrat — cofraj, izolație continuă, structură portantă și suport de finisaje reunite într-un",
    "Statut : Patent délivré et actif": "Status: brevet eliberat și activ",
    "Ce qu'un brevet européen change pentru tine.": "Ce schimbă un brevet european pentru tine.",
    "Le système a vara validé par l'Office européen des brevets — nous avons démontré que la technologie est nouvelle, inventive et app": "Sistemul a fost validat de Oficiul European al Brevetelor — am demonstrat că tehnologia e nouă, inventivă și aplicabilă",
    "Investiție sigură Le brevet ne fait pas que protéger": "Investiție sigură Brevetul nu doar protejează",
    "il confirme que votre casă repose sur une technologie unique": "confirmă că casa ta se bazează pe o tehnologie unică",

    # === CERTIFICARI ===
    "Certificări & Conformité · Polistibrick": "Certificări & conformitate · Polistibrick",
    "Le système constructif Polistibrick fait l'objet d'un encadrement technique rigoureux et d'essais structurels continus au niveau e": "Sistemul constructiv Polistibrick face obiectul unui cadru tehnic riguros și al unor teste structurale continue la nivel european",
    "For că la solidité et l'izolație de votre bâti ne souffrent aucun compromis, chaque composant Polistibrick est certifié conforme a": "Pentru că soliditatea și izolația construcției tale nu suportă compromisuri, fiecare componentă Polistibrick este certificată conform",
    "Déclaration de conformité aux exigences réglementaires du Règlement des Produse de Construcție (RPC) 305/2011/UE, attestant des pe": "Declarație de conformitate cu cerințele Regulamentului Produselor de Construcție (CPR) 305/2011/UE, atestând performanțele",
    "Eliberat de: Organisme Notifié Européen": "Eliberat de: Organism Notificat European",
    "Portée : Règlement RPC 305/2011/UE": "Domeniu: Regulament CPR 305/2011/UE",
    "Évaluation Technique Européenne certifiant les caractéristiques du système constructif en termes de capacité portante, d'izolație": "Evaluare Tehnică Europeană care certifică caracteristicile sistemului constructiv în termeni de capacitate portantă, izolație",
    "Management rigoureux de la qualité sur nos lignes de production. Contrôles automatiques réguliers sur la densité de l'EPS, le cala": "Management riguros al calității pe liniile noastre de producție. Controale automate regulate ale densității EPS, calibrării",
    "Suivi : Audit annuel par organisme certifié": "Urmărire: audit anual de organism certificat",
    "Validation des performances thermiques. Assure une étanchéité à l'air optimale et l'élimination des ponts thermiques, validant l'u": "Validarea performanțelor termice. Asigură etanșeitate la aer optimă și eliminarea punților termice, validând valoarea",
    "Valeur U validée : 0,10 à 0,13 W/m²K": "Valoare U validată: 0,10–0,13 W/m²K",
    "Nos ingénieurs fournissent les notes d'équivalence technique (ETA/CE) requises par les bureaux de co": "Inginerii noștri furnizează notele de echivalență tehnică (ETA/CE) cerute de birourile de",
    "Essais de réaction au feu EN 13501-1. Les parements extérieurs en fibre-ciment garantissent une inco": "Teste de reacție la foc EN 13501-1. Finisajele exterioare din fibrociment garantesc necombustibilitatea",
    "Besoin d'un dossier technique d'ingénierie complet ?": "Ai nevoie de un dosar tehnic de inginerie complet?",
    "Fondateur &amp; CEO · Inventeur du système Polistibrick": "Fondator &amp; CEO · Inventatorul sistemului Polistibrick",

    # === TECHNICAL SPECS (all product pages) ===
    "Déphasage": "Defazaj",
    "Après coulage": "După turnare",
    "Avant coulage": "Înainte de turnare",
    "Isolant PSE": "Izolație PSE",
    "Isolant PSE graphité": "Izolație PSE grafit",
    "Portée max.": "Deschidere max.",
    "Portée max": "Deschidere max",
    "Portée maximale": "Deschidere maximă",
    "Épaisseur totale": "Grosime totală",
    "Poids hourdis": "Greutate plăci",
    "Poids panneau": "Greutate panou",
    "Poids panneau extérieur": "Greutate panou exterior",
    "Poids panneau intérieur": "Greutate panou interior",
    "Largeur panneau": "Lățime panou",
    "Le mur, couche par couche.": "Peretele, strat cu strat.",
    "De l'intérieur vers l'extérieur. Feu&nbsp;: B-s1, d0 . Entre chaque panneau&nbsp;: poutre I-Joist .": "Din interior spre exterior. Foc&nbsp;: B-s1, d0 . Între fiecare panou&nbsp;: grindă I-Joist .",
    "De l'intérieur (sous-face) vers le haut. Feu&nbsp;: A1 . Poids hourdis = fibrociment 8&nbsp;mm + polistiren (avant coulage).": "Din interior (fața inferioară) spre sus. Foc&nbsp;: A1 . Greutate plăci = fibrociment 8&nbsp;mm + polistiren (înainte de turnare).",
    "Beton armé (après coulage) ≈ 10 cm + nervures ≈ 10 cm + nervures ≈ 10 cm + nervures": "Beton armat (după turnare) ≈ 10 cm + nervuri ≈ 10 cm + nervuri ≈ 10 cm + nervuri",
    "OSB/3 intérieur 15 mm": "OSB/3 interior 15 mm",
    "OSB/3 extérieur 15 mm": "OSB/3 exterior 15 mm",
    "Isolant PSE graphité (λ 0,031) 220 mm": "Izolație PSE grafit (λ 0,031) 220 mm",
    "Fiche PBK 200 PDF sur demande →": "Fișă PBK 200 PDF la cerere →",
    "Fiche PBK 250 PDF sur demande →": "Fișă PBK 250 PDF la cerere →",
    "Fiche PBK 300 PDF sur demande →": "Fișă PBK 300 PDF la cerere →",
    "Là où le plancher rencontre le mur, la différence se voit&nbsp;: le beton chauffé par l'intérieur est en rouge.": "Acolo unde planșeul întâlnește peretele, diferența se vede&nbsp;: betonul încălzit din interior e marcat cu roșu.",
    "entre appuis": "între reazeme",
    "Capacité portante": "Capacitate portantă",
    "Cisaillement acoperișure": "Forță tăietoare acoperiș",
    "Dimensions & poids": "Dimensiuni & greutate",
    "Glissez pour tourner": "Glisați pentru rotire",
    "Contreplaqué 1,5": "Contraplacaj 1,5",
    "Isolant 20–25": "Izolație 20–25",
    "PDF sur demande": "PDF la cerere",
    "Page technique + PDF": "Pagină tehnică + PDF",
    "Fiche acoperișure TBK · SIP250": "Fișă acoperiș TBK · SIP250",

    # === POLISTISIP ===
    "On construit auzid'aujourd'hui casele de mâine.": "Construim astăzi casele de mâine.",
    "PolistiSIP n'est pas un cofraj beton. C'est un système de casăs en panneaux sandwich lemn (SIP) avec âme isolante et structure I-J": "PolistiSIP nu e cofraj de beton. E un sistem de case din panouri sandwich lemn (SIP) cu miez izolant și structură I-J",
    "Pentruquoi les casăs perdent de la chaleur ?": "De ce casele pierd căldură?",
    "Pentruquoi les casăs perdent de la chaleur&nbsp;?": "De ce casele pierd căldură&nbsp;?",
    "La plupart perdent de l'énergie par les ponts thermiques — là où le lemn massif traverse l'izolație. PolistiSIP corrige ce point f": "Majoritatea pierd energie prin punți termice — acolo unde lemnul masiv traversează izolația. PolistiSIP corectează acest punct",
    "pas de beton coulé dani le mur": "fără beton turnat în perete",
    "Mur SIP300 — 30 cm, U=0,11, déphasage 11,3 h, 23 kg/m²": "Perete SIP300 — 30 cm, U=0,11, defazaj 11,3 h, 23 kg/m²",
    "Ce n'est pas Polistibrick. Si vous voulez du beton armé → Polistibrick ou Polistiwall .": "Nu e Polistibrick. Dacă vrei beton armat → Polistibrick sau Polistiwall.",
    "Précision d'usine. Vitesse chantier.": "Precizie de fabrică. Viteză pe șantier.",
    "Panneaux pré-découpés, kit complet, structure montée en zile — pas en lună.": "Panouri predecupate, kit complet, structură montată în zile — nu în luni.",

    # === POLISTIBRICK ===
    "Polistibrick : cofraj isolant avec les deux faces en fibrociment . Extérieur prêt pour l'enduit, intérieur prêt à peindre. On mont": "Polistibrick: cofraj izolant cu ambele fețe din fibrociment. Exterior gata de tencuială, interior gata de vopsit. Se montează",
    "Portée jusqu'à 9&nbsp;m": "Deschidere până la 9&nbsp;m",
    "Ou acoperișure classique si vous préférez": "Sau acoperiș clasic dacă preferați",
    "En maçonnerie classique, la chaleur fuit aux ponts thermiques — joints, liaisons, chaque rupture d'izolație. Polistibrick învelopp": "În zidăria clasică, căldura fuge prin punți termice — rosturi, legături, fiecare ruptură de izolație. Polistibrick învelește",
    "Izolație continue deux faces — le beton n'est jamais exposé": "Izolație continuă pe ambele fețe — betonul nu e niciodată expus",
    "Emboîtement MBK — joints sani pont thermique": "Îmbinare MBK — rosturi fără pod termic",

    # === POLISTIWALL ===
    "Polistiwall · Cofraj isolant sani face intérieure | Casă pasivă": "Polistiwall · Cofraj izolant fără față interioară | Casă pasivă",
    "Cofraj isolant sani face intérieure. Casă pasivă.": "Cofraj izolant fără față interioară. Casă pasivă.",
    "Polistiwall : comme Polistibrick, sani panneau intérieur . Vous montez le cofraj extérieur isolant, vous coulez le beton armé ( 15": "Polistiwall: ca Polistibrick, fără panou interior. Montezi cofrajul exterior izolant, torni betonul armat (15",
    "Planșeu au choix : plancher isolant PBK, ou plancher classique": "Planșeu la alegere: planșeu izolant PBK sau planșeu clasic",
    "Face intérieure = beton. Feu A1": "Față interioară = beton. Foc A1",
    "0 Panneau intérieur": "0 Panou interior",
    "20–25 cm PSE extérieur": "20–25 cm PSE exterior",
    "15–25 cm Beton armé": "15–25 cm Beton armat",

    # === MERCURY testimonials ===
    "Une seule équipe = la marge de 5 équipes — jusqu'à 50 %": "O singură echipă = marja a 5 echipe — până la 50%",
    "Imagination sani limite — grands porte-à-faux, calculs Eurocode 2 classiques.": "Imaginație fără limite — console generoase, calcule Eurocode 2 clasice.",
    "−80 % sur les factures d'énergie, pour la vie": "−80% la facturile de energie, pe viață",
    "5 avantages inclus de série. Premium direct d'usine.": "5 avantaje incluse de serie. Premium direct din fabrică.",
    "Ma plus grande satisfaction&nbsp;? Boucler <em>o ofertă în 5 minute</em>. Am doar fierul, betonul și cofrajul Polistibrick — sigur și fără erori.": "Cea mai mare satisfacție&nbsp;? Finalizez <em>o ofertă în 5 minute</em>. Am doar fierul, betonul și cofrajul Polistibrick — sigur și fără erori.",
    "On l'a testé sur un premier șantier": "L-am testat pe primul șantier",
    "il y a 5 lună": "acum 5 luni",
    "il y a 3 lună": "acum 3 luni",
    "Témoignage précédent": "Testimonial anterior",
    "Témoignage suivant": "Testimonial următor",

    # === TESTIMONIALE ===
    "Arhitect partenaire · 12 projets Polistibrick livrés": "Arhitect partener · 12 proiecte Polistibrick livrate",
    "Certifiés Passivhaus": "Certificate Passivhaus",
    "Proiecte livrés": "Proiecte livrate",
    "Locuiești într-o house Polistibrick? Hai să-ți filmăm povestea — 30 minutes sur le chantier, publications sur les réseaux sociaux offertes, offre pour votre prochain projet.": "Locuiești într-o casă Polistibrick? Hai să-ți filmăm povestea — 30 de minute pe șantier, postări pe rețelele sociale incluse, ofertă pentru următorul proiect.",
    "Parce qu'<em>on ne ment pas avec ses yeux.</em>": "Pentru că <em>nu minți cu ochii.</em>",
    "Pe internet, oricine poate scrie orice. Mais on ne peut pas falsifier une factură de 38 €/lună affichée à l'écran d'un téléphone, le visage d'une personne qui en a assez de payer le gaz, ou la joie d'une famille qui a construit sani stress.": "Pe internet, oricine poate scrie orice. Dar nu poți falsifica o factură de 38 €/lună afișată pe ecranul unui telefon, fața unei persoane obosită să plătească gazul, sau bucuria unei familii care a construit fără stres.",
    "Nous voulons que vous soyez certain que ce que nous vous promettons se vérifie dani la vie réelle de celles et ceux qui ont acheté avant vous.": "Vrem să fii sigur că ce îți promitem se verifică în viața reală a celor care au cumpărat înaintea ta.",
    "Vous voulez <em>vous aussi</em> apparaître dani une vidéo comme celle-ci ?": "Vrei <em>și tu</em> să apari într-un videoclip ca acesta?",
    "construisez avec Polistibrick, et dani 2 ani votre histoire sera ici pour inspirer d'autres personnes.": "construiește cu Polistibrick, și peste 2 ani povestea ta va fi aici pentru a inspira alți oameni.",
    "Calculer les économies": "Calculează economiile",
    "Proprietar montrant sa factură réelle": "Proprietar arătând factura reală",

    # === FAQ ===
    "Câți muncitori sunt necesari pentru montaj une casă ?": "Câți muncitori sunt necesari pentru montajul unei case?",
    "O singură echipă de 3 persoane monte une casă de 100 m² de plain-pied en moins de 3 săptămâni , quasi finie. Là où une construcție": "O singură echipă de 3 persoane montează o casă de 100 m² parter în mai puțin de 3 săptămâni, aproape finalizată. Unde o construcție",
    "Polistibrick remplace combien de corps de métier ?": "Polistibrick înlocuiește câte meserii?",
    "Cinq, en une seule pose : la maçonnerie, l'izolație extérieure (ITE), l'izolație intérieure, le doublage / la finition et l'étanch": "Cinci, dintr-o singură montare: zidăria, izolația exterioară (ETI), izolația interioară, placajul / finisajul și etanșeitatea",
    "La plaque de finition, est-ce du placo ?": "Placa de finisaj, e gips-carton?",
    "Non : c'est du fibre-ciment . Dani un seul produit, il résiste au feu, à l'eau et au bruit — là où une casă classique exigerait de": "Nu: e fibrociment. Într-un singur produs, rezistă la foc, apă și zgomot — unde o casă clasică ar cere",
    "Comment passent l'électricité et la plomberie ?": "Cum trec electricitatea și instalațiile sanitare?",
    "Quelle épaisseur de beton dani le mur MBK ?": "Ce grosime de beton are peretul MBK?",
    "Quelle portée pour les planșee PBK ?": "Ce deschidere au planșeele PBK?",
    "Quel modèle choisir : Wall 200 ou Wall 250 ?": "Ce model alegi: Wall 200 sau Wall 250?",

    # === GLOBAL fixes (phrase-level only) ===
    "main-d'œuvre": "manoperă",
    "gros œuvre": "structură",
    "Gros œuvre": "Structură",
    "étanchéité à l'air": "etanșeitate la aer",
    "Étanchéité à l'air": "Etanșeitate la aer",
    "coulé sur chantier": "turnat pe șantier",
    "sani pont thermique": "fără pod termic",
    "sani ponts thermiques": "fără punți termice",
    "sani face intérieure": "fără față interioară",
    "sani panneau intérieur": "fără panou interior",
    "element par élément": "element cu element",
    "en quelques săptămâni": "în câteva săptămâni",
    "Personnes sur le chantier": "Persoane pe șantier",
    "Le montage en vidéo": "Montajul în video",
    "Bientôt disponible": "În curând",
}


def apply_dict(text: str, mapping: dict[str, str], passes: int = 4) -> str:
    keys = sorted(mapping.keys(), key=len, reverse=True)
    segments = []
    last_end = 0
    for m in SKIP.finditer(text):
        segments.append(("t", text[last_end : m.start()]))
        segments.append(("s", m.group(0)))
        last_end = m.end()
    segments.append(("t", text[last_end:]))
    out = []
    for kind, seg in segments:
        if kind == "s":
            out.append(seg)
            continue
        for _ in range(passes):
            for fr in keys:
                tr = mapping[fr]
                if fr in seg:
                    seg = seg.replace(fr, tr)
        out.append(seg)
    return "".join(out)


def main() -> None:
    extra_path = TRANS / "extra_fr_to_ro.json"
    merged: dict[str, str] = {}
    if extra_path.exists():
        merged.update(json.loads(extra_path.read_text(encoding="utf-8")))
    batch4_path = TRANS / "batch4_fr_to_ro.json"
    batch4_path.write_text(
        json.dumps(dict(sorted(BATCH4.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    merged.update(BATCH4)
    extra_path.write_text(
        json.dumps(dict(sorted(merged.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    changed = 0
    for f in sorted(RO_DIR.rglob("*.html")):
        original = f.read_text(encoding="utf-8")
        new = apply_dict(original, merged)
        if new != original:
            f.write_text(new, encoding="utf-8")
            changed += 1
    print(f"pass2: {len(merged)} keys total, {changed} files updated")


if __name__ == "__main__":
    main()
