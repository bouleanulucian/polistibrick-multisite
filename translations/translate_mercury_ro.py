#!/usr/bin/env python3
"""Translate countries/ro/polistibrick-mercury-style.html FR → RO (HTML only)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "countries/ro/polistibrick-mercury-style.html"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

# Longest keys first when applying
TRANSLATIONS = {
    # Meta
    "Polistibrick — Une maison. Un système. Sans compromis.": "Polistibrick — O casă. Un sistem. Fără compromis.",
    'content="Système ICF complet — murs, planchers, toit. Standard A+++. Construit en 4 semaines. Sans compromis, sans factures."':
    'content="Sistem ICF complet — pereți, planșee, acoperiș. Standard A+++. Construit în 4 săptămâni. Fără compromis, fără facturi."',
    'content="Polistibrick — Une maison. Un système."': 'content="Polistibrick — O casă. Un sistem."',
    'content="Système ICF complet pour maison A+++. Murs, planchers, toit — un système premium."':
    'content="Sistem ICF complet pentru casă A+++. Pereți, planșee, acoperiș — un sistem premium."',

    # Country banner
    "Nous détectons que vous êtes en": "Detectăm că ești în",

    # Nav
    'aria-label="Navigation du site"': 'aria-label="Navigare principală"',
    "Produits": "Produse",
    "Solutions": "Soluții",
    "Pour les propriétaires": "Pentru proprietari",
    "Pour les architectes": "Pentru arhitecți",
    "Pour les constructeurs": "Pentru constructori",
    "Pour les investisseurs": "Pentru investitori",
    "→ Devenez partenaire": "→ Devino partener",
    "Projets": "Proiecte",
    "Maisons construites": "Case construite",
    "Témoignages (vidéo)": "Testimoniale (video)",
    "Témoignages vidéo": "Testimoniale video",
    "Calculateur d'économies (vs brique)": "Calculator economii (vs cărămidă)",
    "Calculateur d'économies": "Calculator economii",
    "Calculateur de coût": "Calculator cost",
    "Calculateur": "Calculator",
    "Ressources": "Resurse",
    "Questions fréquentes": "Întrebări frecvente",
    "À propos": "Despre",
    "L'entreprise": "Compania",
    "Certifications": "Certificări",
    "Nos usines": "Fabricile noastre",
    "Le fondateur": "Fondatorul",
    "Choisir le pays": "Alege țara",
    "Devis →": "Ofertă →",
    "Demander un devis →": "Cere o ofertă →",
    'aria-label="Fermer le menu"': 'aria-label="Închide meniul"',
    'aria-label="Fermer"': 'aria-label="Închide"',

    # Hero
    "Système constructif breveté · RE2020": "Sistem constructiv brevetat · RE2020",
    "Construisez plus de maisons.": "Construiești mai multe case.",
    "Avec moins de main-d'œuvre.": "Cu mai puțină manoperă.",
    "Polistibrick remplace 5 matériaux différents et 5 équipes de construction. Un seul produit, une seule équipe — et la maison est achevée. <strong>Innovation brevetée.</strong>":
    "Polistibrick înlocuiește 5 materiale diferite și 5 echipe de construcție. Un singur produs, o singură echipă — și casa este finalizată. <strong>Inovație brevetată.</strong>",
    "Recevez votre devis gratuit →": "Primește oferta ta gratuită →",
    "Je construis moi-même →": "Construiesc singur →",

    # Morph
    "Liberté architecturale": "Libertate arhitecturală",
    "«&nbsp;Comment je construis ça&nbsp;?&nbsp;»": "«&nbsp;Cum construiesc asta&nbsp;?&nbsp;»",
    "<em>Avec Polistibrick, c'est possible.</em>": "<em>Cu Polistibrick, este posibil.</em>",
    "Liberté totale à l'exécution, comme à la conception.": "Libertate totală la execuție, ca și la proiectare.",
    'aria-label="Le système Polistibrick se reconfigure : maison de plain-pied, villa à étage, petit immeuble collectif"':
    'aria-label="Sistemul Polistibrick se reconfigurează: casă parter, vilă cu etaj, mic bloc colectiv"',
    '<div class="mw-line2">Système</div>': '<div class="mw-line2">Sistem</div>',

    # Differences
    "Différences": "Diferențe",
    'aria-label="La différence Polistibrick"': 'aria-label="Diferența Polistibrick"',
    "Polistibrick vs classique": "Polistibrick vs clasic",
    "Classique": "Clasic",
    "Système Polistibrick": "Sistem Polistibrick",
    "👤 Une équipe - 3 personnes": "👤 O echipă — 3 persoane",
    "3 Matériaux": "3 materiale",
    ": Coffrage Polistibrick • Béton • Acier": ": Cofraj Polistibrick • Beton • Oțel",
    "Système Traditionnel": "Sistem tradițional",
    "👤👤👤👤👤 5 équipes - 15 personnes": "👤👤👤👤👤 5 echipe — 15 persoane",
    "9 Matériaux": "9 materiale",
    ": Blocs • Mortier • Coffrage • Fer • Béton • Isolation • Doublage • Vis • etc.":
    ": Blocuri • Mortar • Cofraj • Fier • Beton • Izolație • Placaj • Șuruburi • etc.",

    # Personas
    "Pour Vous": "Pentru tine",
    'aria-label="Vous êtes... ? Solutions par rôle"': 'aria-label="Ești…? Soluții pe rol"',
    'alt="Chantier Polistibrick : coulage du béton dans un lotissement de maisons"':
    'alt="Șantier Polistibrick: turnare beton într-un lot de case"',
    "Vous êtes… Constructeur ?": "Ești… Constructor?",
    "2× plus rapide. <em>Marges protégées.</em>": "De 2× mai rapid. <em>Marje protejate.</em>",
    "Une seule équipe = la marge de 5 équipes — jusqu'à 50%": "O singură echipă = marja a 5 echipe — până la 50%",
    "Voir pour constructeurs →": "Vezi pentru constructori →",
    'alt="Maison d\'architecte contemporaine avec porte-à-faux, réalisée avec Polistibrick"':
    'alt="Casă de arhitect contemporană cu console, realizată cu Polistibrick"',
    "Vous êtes… Architecte · Ingénieur ?": "Ești… Arhitect · Inginer?",
    "Vous imaginez,": "Tu proiectezi,",
    "<em>Polistibrick exécute.</em>": "<em>Polistibrick execută.</em>",
    "Pour la première fois, votre imagination n'a plus de limite — grands porte-à-faux et portées généreuses, en calculs Eurocode 2 classiques.":
    "Pentru prima dată, imaginația ta nu mai are limite — console generoase și deschideri ample, în calcule Eurocode 2 clasice.",
    "Voir pour architectes →": "Vezi pentru arhitecți →",
    'alt="Couple profitant de la terrasse d\'une maison Polistibrick au coucher du soleil"':
    'alt="Cuplu pe terasa unei case Polistibrick la apus"',
    "Vous êtes… Propriétaire ?": "Ești… Proprietar?",
    "Maison premium, <em>sans factures.</em>": "Casă premium, <em>fără facturi.</em>",
    "−90% sur les factures d'énergie, pour la vie": "−90% la facturile de energie, pe viață",
    "Voir pour propriétaires →": "Vezi pentru proprietari →",
    "Vous êtes… Promoteur ?": "Ești… Dezvoltator?",
    "ROI maximum. <em>Risque minimum.</em>": "ROI maxim. <em>Risc minim.</em>",
    "+15 à 25% à la revente, gros œuvre 2× plus vite": "+15–25% la revânzare, structura de 2× mai rapid",
    "Voir pour promoteurs →": "Vezi pentru investitori →",
    'aria-label="Choisir le rôle"': 'aria-label="Alege rolul"',
    "Constructeur": "Constructor",
    "Architecte": "Arhitect",
    "Propriétaire": "Proprietar",
    "Promoteur": "Dezvoltator",

    # Passif
    'aria-label="Le standard Maison Passive"': 'aria-label="Standardul casă pasivă"',
    "Votre meilleur argument de vente": "Cel mai bun argument de vânzare",
    "Offrez le passif à vos clients,": "Oferă pasiv clienților tăi,",
    "<em>au prix du classique.</em>": "<em>la prețul celui clasic.</em>",
    "−90% de factures": "−90% facturi",
    "Devis gratuit →": "Ofertă gratuită →",
    'aria-label="La même maison Polistibrick à travers les quatre saisons : dehors tout change, dedans le confort reste constant"':
    'aria-label="Aceeași casă Polistibrick în cele patru anotimpuri: afară totul se schimbă, înăuntru confortul rămâne constant"',
    'alt="La vue depuis le salon au printemps"': 'alt="Vederea din living primăvara"',

    # Cinq-en-un
    "De Série": "De serie",
    'aria-label="La différence Polistibrick : cinq produits en un seul panneau"':
    'aria-label="Diferența Polistibrick: cinci produse într-un singur panou"',
    "La différence Polistibrick": "Diferența Polistibrick",
    "Cinq lignes en moins sur le devis,": "Cinci linii în minus pe ofertă,",
    "<em>du premium en plus pour vous.</em>": "<em>premium în plus pentru tine.</em>",
    "<strong>Feu, hydrofuge, étanchéité à l'air, isolation passive, insonorisation, fixation</strong> : ailleurs, on les chiffre, on les transporte et on les pose selon des normes strictes — au prix fort. Polistibrick les intègre d'usine, les avantages les plus convoités de 2026. Votre client les obtient sans surcoût — une maison que peu possèdent.":
    "<strong>Foc, hidrofug, etanșeitate la aer, izolație pasivă, fonoizolație, fixare</strong>: în altă parte, le calculezi, le transporti și le montezi conform unor norme stricte — la preț mare. Polistibrick le integrează din fabrică, avantajele cele mai dorite din 2026. Clientul tău le primește fără cost suplimentar — o casă pe care puțini o au.",
    'aria-label="Le panneau Polistibrick testé : assemblage, feu, eau, impact, gel, bruit — intact à chaque épreuve"':
    'aria-label="Panoul Polistibrick testat: asamblare, foc, apă, impact, îngheț, zgomot — intact la fiecare probă"',
    "Sécurité feu intégrale": "Securitate la foc integrată",
    "Fibrociment A1 + béton armé.": "Fibrociment A1 + beton armat.",
    "Étanche partout": "Etanș peste tot",
    "Hydrofuge à 100%, sans plaques vertes.": "Hidrofug 100%, fără plăci verzi.",
    "Silence de série": "Silence de serie",
    "Insonorisation ≥ 65 dB de série.": "Fonoizolație ≥ 65 dB de serie.",
    "Structure antisismique": "Structură antiseismică",
    "Béton armé monolithique durable à vie.": "Beton armat monolitic durabil pe viață.",
    "Fixation directe": "Fixare directă",
    "Vissez directement, sans perceuse.": "Șurubui direct, fără burghiu.",

    # Présence
    "Présence": "Prezență",
    'aria-label="Présence : deux usines, neuf pays"': 'aria-label="Prezență: două fabrici, nouă țări"',
    'aria-label="Usine Polistibrick : chargement des panneaux Polistibrick sur un camion"':
    'aria-label="Fabrică Polistibrick: încărcarea panourilor Polistibrick pe camion"',
    "Capacité industrielle <em>& Logistique.</em>": "Capacitate industrială <em>& logistică.</em>",
    "2 usines en propre": "2 fabrici proprii",
    "9 pays livrés": "9 țări livrate",
    "directement sur chantier": "direct pe șantier",
    'aria-label="Carte de l\'Europe : les pays de présence Polistibrick"':
    'aria-label="Harta Europei: țările de prezență Polistibrick"',
    "Irlande": "Irlanda",
    "Belgique": "Belgia",
    "Autriche": "Austria",
    "Italie": "Italia",
    "Roumanie": "România",
    "Monténégro": "Muntenegru",
    "Usine · Espagne": "Fabrică · Spania",
    "Usine · Roumanie": "Fabrică · România",
    "Usines": "Fabrici",
    "Pays de présence": "Țări de prezență",

    # Système products
    '<span class="wm-half wm-top">Système</span>': '<span class="wm-half wm-top">Sistem</span>',
    '<span class="wm-half wm-bottom">Système</span>': '<span class="wm-half wm-bottom">Sistem</span>',
    "Une maison. <em>Trois produits.</em>": "O casă. <em>Trei produse.</em>",
    'alt="Polistibrick MBK — mur premium"': 'alt="Polistibrick MBK — perete premium"',
    "Murs · MBK": "Pereți · MBK",
    "Fini <em>5 en 1.</em>": "Gata <em>5-în-1.</em>",
    "3 modèles haut de gamme (210/270/300) plus production sur commande sans coût supplémentaire. Le seul ICF avec cette garantie.":
    "3 modele premium (210/270/300) plus producție la comandă fără cost suplimentar. Singurul ICF cu această garanție.",
    "W/m²K · Feu A1 · Antisismique": "W/m²K · Foc A1 · Antiseismic",
    'alt="Polistibrick PBK — plancher premium"': 'alt="Polistibrick PBK — planșeu premium"',
    "Planchers · PBK": "Planșee · PBK",
    "Portées <em>jusqu'à 9 m.</em>": "Deschideri <em>până la 9 m.</em>",
    "Système préfabriqué léger et ultra-résistant : polystyrène + fibrociment + béton armé. Déphasage thermique 10,8 h.":
    "Sistem prefabricat ușor și ultra-rezistent: polistiren + fibrociment + beton armat. Defazaj termic 10,8 h.",
    "de portée · 65 kg/m² · Acoustique ≥ 52 dB": "deschidere · 65 kg/m² · Acustic ≥ 52 dB",
    'alt="Polistibrick TBK — toit Passivhaus"': 'alt="Polistibrick TBK — acoperiș Passivhaus"',
    "Toit · TBK": "Acoperiș · TBK",
    "Passivhaus <em>sortie d'usine.</em>": "Passivhaus <em>din fabrică.</em>",
    "U=0,13 W/m²K, épaisseur 25 cm, seulement 22 kg/m². Le toit le plus performant de sa catégorie. Sans isolation additionnelle.":
    "U=0,13 W/m²K, grosime 25 cm, doar 22 kg/m². Cel mai performant acoperiș din categoria sa. Fără izolație suplimentară.",
    'alt="Maison Polistibrick en vue éclatée : toit TBK, plancher PBK, murs MBK"':
    'alt="Casă Polistibrick în vedere explodată: acoperiș TBK, planșeu PBK, pereți MBK"',

    # Montaj
    "Montage": "Montaj",
    "Étapes de pose": "Etape de montaj",
    "Une maison complète <em>en 4 étapes.</em>": "O casă completă <em>în 4 etape.</em>",
    "De la fondation au coffrage fermé — prêt pour le coulage du béton. L'ensemble du processus en quelques semaines avec seulement 2 à 3 personnes sur le chantier.":
    "De la fundație la cofrajul închis — gata pentru turnarea betonului. Întregul proces în câteva săptămâni, cu doar 2–3 persoane pe șantier.",
    'alt="Coffrage assemblé avec étaiement latéral"': 'alt="Cofraj asamblat cu sprijin lateral"',
    "Coffrage": "Cofraj",
    "Murs EPS dressés et fixés avec étaiement latéral en bois sur la fondation. Sans mortier, sans perte d'isolation.":
    "Pereți EPS ridicați și fixați cu sprijin lateral de lemn pe fundație. Fără mortar, fără pierderi de izolație.",
    'alt="Plancher PBK monté"': 'alt="Planșeu PBK montat"',
    "Plancher": "Planșeu",
    "Panneaux PBK 250 montés horizontalement — couches EPS-Graphite + fibrociment prêtes à recevoir l'armature.":
    "Panouri PBK 250 montate orizontal — straturi EPS-Grafit + fibrociment gata pentru armătură.",
    'alt="Armature acier-béton sur plancher"': 'alt="Armătură oțel-beton pe planșeu"',
    "Armature": "Armătură",
    "Les treillis d'acier d'armature se placent entre les nervures EPS-Graphite. Liaison monolithique entre les murs et le plancher.":
    "Plasele de oțel-beton se așază între nervurile EPS-Grafit. Legătură monolitică între pereți și planșeu.",
    'alt="Coffrage fermé, prêt pour le coulage du béton"': 'alt="Cofraj închis, gata pentru turnarea betonului"',
    "Fermeture du coffrage": "Închiderea cofrajului",
    "Tous les éléments assemblés et vérifiés. <strong>Nous sommes maintenant prêts pour le coulage du béton.</strong>":
    "Toate elementele asamblate și verificate. <strong>Suntem gata pentru turnarea betonului.</strong>",
    "Après le coulage du béton, la structure devient <strong>monolithique en 24 heures</strong> — murs, planchers, toit, isolés en continu, sans ponts thermiques.":
    "După turnarea betonului, structura devine <strong>monolitică în 24 de ore</strong> — pereți, planșee, acoperiș, izolate continuu, fără punți termice.",
    "Voir tout le montage": "Vezi tot montajul",
    "Demandez un devis personnalisé": "Cere o ofertă personalizată",

    # Confiance / testimonials
    "Confiance": "Încredere",
    'aria-label="Avis et témoignages de constructeurs"': 'aria-label="Recenzii și testimoniale de la constructori"',
    "Avis vérifiés · Constructeurs": "Recenzii verificate · Constructori",
    "Ils ont bâti avec Polistibrick — <em>ils en parlent.</em>": "Au construit cu Polistibrick — <em>vorbesc despre asta.</em>",
    "Témoignage vidéo": "Testimonial video",
    'aria-label="Lire la vidéo"': 'aria-label="Redă videoclipul"',
    'aria-label="5 sur 5"': 'aria-label="5 din 5"',
    "On l'a testé sur un premier chantier et, franchement, <em>c'est une merveille</em>. Le mur monte presque tout seul — on ne revient pas en arrière.":
    "L-am testat pe primul șantier și, sincer, <em>e o minune</em>. Peretele se ridică aproape singur — nu ne întoarcem înapoi.",
    "Entreprise générale · Aix-en-Provence": "Firmă generală · Aix-en-Provence",
    "✓ Constructeur vérifié": "✓ Constructor verificat",
    "Avec la même équipe, je construis <em>beaucoup plus de maisons</em> dans l'année. Le planning tient enfin.":
    "Cu aceeași echipă, construiesc <em>mult mai multe case</em> pe an. Planificarea ține în sfârșit.",
    "Constructeur de maisons · Nantes": "Constructor de case · Nantes",
    "Avis vérifié": "Recenzie verificată",
    "Ma plus grande satisfaction&nbsp;? Boucler <em>un devis en 5 minutes</em>. Je n'ai que le fer, le béton et le coffrage Polistibrick — sûr, et sans erreurs.":
    "Cea mai mare satisfacție&nbsp;? Finalizez <em>o ofertă în 5 minute</em>. Am doar fierul, betonul și cofrajul Polistibrick — sigur și fără erori.",
    "Entreprise de construction · Annecy": "Firmă de construcții · Annecy",
    "Le confort des maisons impressionne à la livraison — <em>charges quasi nulles</em>. Mes clients sont conquis.":
    "Confortul caselor impresionează la predare — <em>consum aproape zero</em>. Clienții mei sunt cuceriți.",
    "Maison individuelle · Bordeaux": "Casă individuală · Bordeaux",
    "✓ Client vérifié": "✓ Client verificat",
    "Laisser un avis →": "Lasă o recenzie →",
    "Voir tous les avis →": "Vezi toate recenziile →",
    "Vidéo ou message + photos · publié après validation": "Video sau mesaj + poze · publicat după validare",

    # Histoires carousel (duplicate quotes)
    ". Les gars ont pris le coup de main en deux jours, le mur monte presque tout seul. On ne revient pas en arrière.":
    ". Băieții au prins metoda în două zile, peretele se ridică aproape singur. Nu ne întoarcem înapoi.",
    "Je suis vraiment content d'avoir découvert ce système. Avec la même équipe, je construis aujourd'hui <em>beaucoup plus de maisons</em> dans l'année.":
    "Sunt cu adevărat mulțumit că am descoperit acest sistem. Cu aceeași echipă, construiesc astăzi <em>mult mai multe case</em> pe an.",
    ". Je n'ai que le fer, le béton et le coffrage Polistibrick — c'est sûr, et sans erreurs.":
    ". Am doar fierul, betonul și cofrajul Polistibrick — e sigur și fără erori.",

    # CTA
    "CONSTRUISEZ AVEC NOUS": "CONSTRUIEȘTE CU NOI",
    "Construisons ensemble<br><em>votre maison du futur.</em>": "Construim împreună<br><em>casa ta din viitor.</em>",
    "Parlez-nous de votre projet. Nous vous préparons un devis personnalisé sous 48 heures — sans engagement.":
    "Spune-ne despre proiectul tău. Îți pregătim o ofertă personalizată în 48 de ore — fără obligație.",
    'alt="Polistibrick — Construction intelligente"': 'alt="Polistibrick — Construcție inteligentă"',

    # Footer
    "Certifié et reconnu internationalement": "Certificat și recunoscut internațional",
    "Brevet European": "Brevet european",
    "Maison Passive": "Casă pasivă",
    "Standard European": "Standard european",
    "Le système ICF qui construit des maisons plus performantes, plus rapides et plus durables. Fabriqué en UE.":
    "Sistemul ICF care construiește case mai performante, mai rapide și mai durabile. Fabricat în UE.",
    "Système": "Sistem",
    "Murs MBK": "Pereți MBK",
    "Planchers PBK": "Planșee PBK",
    "Toit TBK": "Acoperiș TBK",
    "Comment ça fonctionne": "Cum funcționează",
    "Entreprise": "Companie",
    "Légal": "Legal",
    "Mentions légales": "Mențiuni legale",
    "Politique de confidentialité": "Politica de confidențialitate",
    "Conditions générales": "Termeni și condiții",
    "Politique de cookies": "Politica de cookies",
    "Durabilité": "Sustenabilitate",
    "© 2026 Polistibrick. Tous droits réservés.": "© 2026 Polistibrick. Toate drepturile rezervate.",
    "Fabriqué avec ⚒ en Europe • ISO 9001 / 14001 / 45001": "Fabricat cu ⚒ în Europa • ISO 9001 / 14001 / 45001",

    # Avis modal
    "Laisser un avis": "Lasă o recenzie",
    "Partagez votre expérience avec Polistibrick. Publié après validation.":
    "Împărtășește experiența ta cu Polistibrick. Publicat după validare.",
    "Votre note": "Nota ta",
    'aria-label="Note"': 'aria-label="Notă"',
    'aria-label="1 étoile"': 'aria-label="1 stea"',
    'aria-label="2 étoiles"': 'aria-label="2 stele"',
    'aria-label="3 étoiles"': 'aria-label="3 stele"',
    'aria-label="4 étoiles"': 'aria-label="4 stele"',
    'aria-label="5 étoiles"': 'aria-label="5 stele"',
    "Nom / Entreprise": "Nume / Firmă",
    "Vous êtes": "Ești",
    "Choisir…": "Alege…",
    "Auto-constructeur": "Auto-constructor",
    "Architecte · Ingénieur": "Arhitect · Inginer",
    "Localité (ville / région)": "Localitate (oraș / regiune)",
    'placeholder="ex. Aix-en-Provence"': 'placeholder="ex. Cluj-Napoca"',
    "Type d'avis": "Tip recenzie",
    "🎥 Vidéo": "🎥 Video",
    "Votre avis": "Recenzia ta",
    "Votre vidéo de témoignage — le plus convaincant ⭐": "Videoclipul tău testimonial — cel mai convingător ⭐",
    "🎥 Ajouter ou filmer votre vidéo de témoignage": "🎥 Adaugă sau filmează videoclipul testimonial",
    "Photos du projet (optionnel)": "Poze de pe proiect (opțional)",
    "📷 Ajouter des photos de votre chantier / maison": "📷 Adaugă poze de pe șantier / casă",
    "Logo de votre entreprise (optionnel)": "Logo-ul firmei tale (opțional)",
    "Ajouter votre logo": "Adaugă logo-ul tău",
    "Merci de remplir au moins : note, nom et avis.": "Completează cel puțin: notă, nume și recenzie.",
    "J'accepte que mes données soient traitées conformément à la":
    "Accept că datele mele sunt prelucrate conform",
    "politique de confidentialité (RGPD)": "politicii de confidențialitate (GDPR)",
    "Envoyer mon avis →": "Trimite recenzia →",
    "🔒 Vérifié et publié par Polistibrick après validation.":
    "🔒 Verificat și publicat de Polistibrick după validare.",
    "Merci !": "Mulțumim!",
    "Votre avis a bien été envoyé. Il sera publié sur le site après validation par notre équipe.":
    "Recenzia ta a fost trimisă. Va fi publicată pe site după validare de echipa noastră.",

    # Remaining product labels in nav
    "Murs MBK": "Pereți MBK",
    "Planchers PBK": "Planșee PBK",
    "Toit TBK": "Acoperiș TBK",
    "Brevet": "Patent",
}


def apply_translations(text: str, translations: dict) -> str:
    sorted_keys = sorted(translations.keys(), key=len, reverse=True)
    segments = []
    last_end = 0
    for m in SKIP_REGEX.finditer(text):
        segments.append(("translate", text[last_end:m.start()]))
        segments.append(("skip", m.group(0)))
        last_end = m.end()
    segments.append(("translate", text[last_end:]))

    out = []
    for kind, segment in segments:
        if kind == "skip":
            out.append(segment)
            continue
        for fr in sorted_keys:
            ro = translations[fr]
            if fr in segment:
                segment = segment.replace(fr, ro)
        out.append(segment)
    return "".join(out)


def main():
    # Merge inverted fr.json for any overlapping strings
    fr_json = json.loads((ROOT / "translations/fr.json").read_text(encoding="utf-8"))
    inv = {fr: ro for ro, fr in fr_json.items() if fr and ro and fr != ro}
    merged = {**inv, **TRANSLATIONS}  # explicit TRANSLATIONS win

    original = TARGET.read_text(encoding="utf-8")
    new = apply_translations(original, merged)
    if new != original:
        TARGET.write_text(new, encoding="utf-8")
        print(f"Updated {TARGET.relative_to(ROOT)}")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
