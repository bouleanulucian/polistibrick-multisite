#!/usr/bin/env python3
"""Translate countries/fr/polistibrick-mercury-style.html → countries/it/ (FR → IT)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "countries/fr/polistibrick-mercury-style.html"
TARGET = ROOT / "countries/it/polistibrick-mercury-style.html"

SKIP_REGEX = re.compile(
    r"(<script\b[^>]*>.*?</script>)"
    r"|(<style\b[^>]*>.*?</style>)"
    r"|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)

TRANSLATIONS = {
    # Meta
    "Polistibrick — Une maison. Un système. Sans compromis.": "Polistibrick — Una casa. Un sistema. Senza compromessi.",
    'content="Système ICF complet — murs, planchers, toit. standard A+++. Construit en 4 semaines. Sans compromis, sans factures."':
    'content="Sistema ICF completo — pareti, solai, tetto. Standard A+++. Costruito in 4 settimane. Senza compromessi, senza bollette."',
    'content="Polistibrick — Une maison. Un système."': 'content="Polistibrick — Una casa. Un sistema."',
    'content="Système ICF complet pour maison A+++. Murs, planchers, toit — un système premium."':
    'content="Sistema ICF completo per casa A+++. Pareti, solai, tetto — un sistema premium."',

    # Country banner (fix FR/RO leftovers → IT defaults)
    "Nous détectons que vous êtes en": "Rileviamo che sei in",
    "Nous avons détecté que vous êtes en": "Abbiamo rilevato che sei in",
    "Vizitezi": "Visiti",
    "Da, mergi": "Sì, vai",
    "Je reste ici": "Resto qui",

    # Nav
    'aria-label="Navigation du site"': 'aria-label="Navigazione principale"',
    "Produits": "Prodotti",
    "Solutions": "Soluzioni",
    "Pour les propriétaires": "Per i proprietari",
    "Pour les architectes": "Per gli architetti",
    "Pour les constructeurs": "Per i costruttori",
    "Pour les investisseurs": "Per gli investitori",
    "→ Devenez partenaire": "→ Diventa partner",
    "Projets": "Progetti",
    "Maisons construites": "Case costruite",
    "Témoignages (vidéo)": "Testimonianze (video)",
    "Témoignages vidéo": "Testimonianze video",
    "Calculateur d'économies (vs brique)": "Calcolatore risparmi (vs mattone)",
    "Calculateur d'économies": "Calcolatore risparmi",
    "Calculateur de coût": "Calcolatore costi",
    "Calculateur": "Calcolatore",
    "Ressources": "Risorse",
    "Questions fréquentes": "Domande frequenti",
    "À propos": "Chi siamo",
    "L'entreprise": "L'azienda",
    "Certifications": "Certificazioni",
    "Nos usines": "Le nostre fabbriche",
    "Le fondateur": "Il fondatore",
    'aria-label="Changer de pays"': 'aria-label="Scegli il tuo paese"',
    "Choisir le pays": "Scegli il tuo paese",
    'class="btn btn-primary nav-cta-devis">Devis</a>': 'class="btn btn-primary nav-cta-devis">Preventivo</a>',
    "Demander un devis →": "Richiedi un preventivo →",
    'aria-label="Deschide meniul"': 'aria-label="Apri il menu"',
    'aria-label="Fermer le menu"': 'aria-label="Chiudi il menu"',
    'aria-label="Fermer"': 'aria-label="Chiudi"',

    # Hero
    "Une technologie": "Una tecnologia",
    "avec 5 avantages": "con 5 vantaggi",
    "Construisez plus de logements.": "Costruisci più abitazioni.",
    "Avec une seule équipe.": "Con un solo team.",
    "Polistibrick remplace 5 matériaux différents et 5 équipes de construction. Un seul produit, une seule équipe — et la maison est achevée. <strong>Innovation brevetée.</strong>":
    "Polistibrick sostituisce 5 materiali diversi e 5 squadre di cantiere. Un solo prodotto, un solo team — e la casa è completata. <strong>Innovazione brevettata.</strong>",
    "Recevez votre devis gratuit →": "Ricevi il tuo preventivo gratuito →",
    "Je construis moi-même →": "Costruisco da solo →",
    'alt="Polistibrick — Construction intelligente"': 'alt="Polistibrick — Costruzione intelligente"',

    # Morph
    "Un seul": "Un solo",
    '<div class="mw-line2">Système</div>': '<div class="mw-line2">Sistema</div>',
    "Liberté architecturale": "Libertà architettonica",
    "«&nbsp;Comment je construis ça&nbsp;?&nbsp;»": "«&nbsp;Come costruisco questo?&nbsp;»",
    "<em>Avec Polistibrick, c'est possible.</em>": "<em>Con Polistibrick, è possibile.</em>",
    "Liberté totale à l'exécution, comme à la conception.": "Libertà totale in cantiere, come in progettazione.",
    "Devis gratuit →": "Preventivo gratuito →",
    'aria-label="Le système Polistibrick se reconfigure : maison de plain-pied, villa à étage, petit immeuble collectif"':
    'aria-label="Il sistema Polistibrick si riconfigura: casa su un piano, villa a due piani, piccolo condominio"',

    # Differences
    "Différences": "Differenze",
    'aria-label="La différence Polistibrick"': 'aria-label="La differenza Polistibrick"',
    "Polistibrick vs classique": "Polistibrick vs classico",
    "Classique": "Classico",
    "Système Polistibrick": "Sistema Polistibrick",
    "👤 Une équipe - 3 personnes": "👤 Un team — 3 persone",
    "3 Matériaux": "3 materiali",
    ": Coffrage Polistibrick • Béton • Acier": ": Cassero Polistibrick • Calcestruzzo • Acciaio",
    "Système Traditionnel": "Sistema tradizionale",
    "👤👤👤👤👤 5 équipes - 15 personnes": "👤👤👤👤👤 5 team — 15 persone",
    "9 Matériaux": "9 materiali",
    ": Blocs • Mortier • Coffrage • Fer • Béton • Isolation • Doublage • Vis • etc.":
    ": Blocchi • Malta • Cassero • Ferro • Calcestruzzo • Isolamento • Controsoffitto • Viti • ecc.",

    # Personas
    "Pour Vous": "Per voi",
    'aria-label="Vous êtes... ? Solutions par rôle"': 'aria-label="Chi sei? Soluzioni per ruolo"',
    'alt="Chantier Polistibrick : coulage du béton dans un lotissement de maisons"':
    'alt="Cantiere Polistibrick: getto di calcestruzzo in un lotto di case"',
    "Vous êtes… Constructeur ?": "Sei… un costruttore?",
    "2× plus rapide. <em>Marges protégées.</em>": "2× più veloce. <em>Margini protetti.</em>",
    "Une seule équipe = la marge de 5 équipes — jusqu'à 50%": "Un solo team = il margine di 5 team — fino al 50%",
    "Voir pour constructeurs →": "Scopri per i costruttori →",
    'alt="Maison d\'architecte contemporaine avec porte-à-faux, réalisée avec Polistibrick"':
    'alt="Casa d\'architetto contemporanea con sbalzi, realizzata con Polistibrick"',
    "Vous êtes… Architecte · Ingénieur ?": "Sei… architetto · ingegnere?",
    "Vous imaginez,": "Immagini,",
    "<em>Polistibrick exécute.</em>": "<em>Polistibrick realizza.</em>",
    "Pour la première fois, votre imagination n'a plus de limite — grands porte-à-faux et portées généreuses, en calculs Eurocode 2 classiques.":
    "Per la prima volta, la tua immaginazione non ha più limiti — grandi sbalzi e luci generose, con calcoli Eurocode 2 classici.",
    "Voir pour architectes →": "Scopri per gli architetti →",
    'alt="Couple profitant de la terrasse d\'une maison Polistibrick au coucher du soleil"':
    'alt="Coppia sulla terrazza di una casa Polistibrick al tramonto"',
    "Vous êtes… Propriétaire ?": "Sei… un proprietario?",
    "Maison premium, <em>sans factures.</em>": "Casa premium, <em>senza bollette.</em>",
    "−90% sur les factures d'énergie, pour la vie": "−90% sulle bollette energetiche, per tutta la vita",
    "Voir pour propriétaires →": "Scopri per i proprietari →",
    "Vous êtes… Promoteur ?": "Sei… un promotore?",
    "ROI maximum. <em>Risque minimum.</em>": "ROI massimo. <em>Rischio minimo.</em>",
    "+15 à 25% à la revente, gros œuvre 2× plus vite": "+15–25% alla rivendita, struttura 2× più veloce",
    "Voir pour promoteurs →": "Scopri per gli investitori →",
    'aria-label="Choisir le rôle"': 'aria-label="Scegli il ruolo"',
    "Constructeur": "Costruttore",
    "Architecte": "Architetto",
    "Propriétaire": "Proprietario",
    "Promoteur": "Promotore",

    # Passif
    "Passif": "Passivo",
    'aria-label="Le standard Maison Passive"': 'aria-label="Lo standard Casa Passiva"',
    "Votre meilleur argument de vente": "Il tuo miglior argomento di vendita",
    "Offrez le passif à vos clients,": "Offri il passivo ai tuoi clienti,",
    "<em>au prix du classique.</em>": "<em>al prezzo del classico.</em>",
    "Classe A+++": "Classe A+++",
    "−90% de factures": "−90% bollette",
    'aria-label="Maison Polistibrick en hiver : confort constant à l\'intérieur"':
    'aria-label="Casa Polistibrick in inverno: comfort costante all\'interno"',
    'alt="Vue depuis le salon en hiver — confort constant"': 'alt="Vista dal soggiorno in inverno — comfort costante"',

    # Cinq-en-un
    "De Série": "Di serie",
    'aria-label="La différence Polistibrick : cinq produits en un seul panneau"':
    'aria-label="La differenza Polistibrick: cinque prodotti in un solo pannello"',
    "La différence Polistibrick": "La differenza Polistibrick",
    "Cinq lignes en moins sur le devis,": "Cinque righe in meno sul preventivo,",
    "<em>du premium en plus pour vous.</em>": "<em>più premium per te.</em>",
    "<strong>Feu, hydrofuge, étanchéité à l'air, isolation passive, insonorisation, fixation</strong> : ailleurs, on les chiffre, on les transporte et on les pose selon des normes strictes — au prix fort. Polistibrick les intègre d'usine, les avantages les plus convoités de 2026. Votre client les obtient sans surcoût — une maison que peu possèdent.":
    "<strong>Fuoco, idrorepellenza, tenuta all'aria, isolamento passivo, insonorizzazione, fissaggio</strong>: altrove li si quantificano, si trasportano e si posano secondo norme rigorose — a prezzo elevato. Polistibrick li integra in fabbrica, i vantaggi più ambiti del 2026. Il tuo cliente li ottiene senza sovrapprezzo — una casa che pochi possiedono.",
    'aria-label="Le panneau Polistibrick testé : assemblage, feu, eau, impact, gel, bruit — intact à chaque épreuve"':
    'aria-label="Pannello Polistibrick testato: assemblaggio, fuoco, acqua, impatto, gelo, rumore — intatto a ogni prova"',
    "Sécurité feu intégrale": "Sicurezza antincendio integrata",
    "Fibrociment A1 + béton armé.": "Fibrocemento A1 + calcestruzzo armato.",
    "Étanche partout": "Stagno ovunque",
    "Hydrofuge à 100%, sans plaques vertes.": "Idrorepellente al 100%, senza lastre verdi.",
    "Silence de série": "Silenzio di serie",
    "Insonorisation ≥ 65 dB de série.": "Insonorizzazione ≥ 65 dB di serie.",
    "Structure antisismique": "Struttura antisismica",
    "Béton armé monolithique durable à vie.": "Calcestruzzo armato monolitico durevole a vita.",
    "Fixation directe": "Fissaggio diretto",
    "Vissez directement, sans perceuse.": "Avvita direttamente, senza trapano.",

    # Présence
    "Présence": "Presenza",
    'aria-label="Présence : deux usines, neuf pays"': 'aria-label="Presenza: due fabbriche, nove paesi"',
    'aria-label="Usine Polistibrick : chargement des panneaux Polistibrick sur un camion"':
    'aria-label="Fabbrica Polistibrick: carico dei pannelli Polistibrick su un camion"',
    "Production · Polistibrick": "Produzione · Polistibrick",
    "Capacité industrielle <em>& Logistique.</em>": "Capacità industriale <em>e logistica.</em>",
    "2 usines en propre": "2 fabbriche proprie",
    "9 pays livrés": "9 paesi serviti",
    "directement sur chantier": "direttamente in cantiere",
    'aria-label="Carte de l\'Europe : les pays de présence Polistibrick"':
    'aria-label="Mappa d\'Europa: i paesi di presenza Polistibrick"',
    "Irlande": "Irlanda",
    "Belgique": "Belgio",
    "Autriche": "Austria",
    "Italie": "Italia",
    "Roumanie": "Romania",
    "Monténégro": "Montenegro",
    "Usine · Espagne": "Fabbrica · Spagna",
    "Usine · Roumanie": "Fabbrica · Romania",
    "Usines": "Fabbriche",
    "Pays de présence": "Paesi di presenza",

    # Système products
    '<span class="wm-half wm-top">Système</span>': '<span class="wm-half wm-top">Sistema</span>',
    '<span class="wm-half wm-bottom">Système</span>': '<span class="wm-half wm-bottom">Sistema</span>',
    "Une maison. <em>Trois produits.</em>": "Una casa. <em>Tre prodotti.</em>",
    'alt="Polistibrick MBK — mur premium"': 'alt="Polistibrick MBK — parete premium"',
    "Murs · MBK": "Pareti · MBK",
    "Fini <em>5 en 1.</em>": "Finito <em>5 in 1.</em>",
    "3 modèles haut de gamme (210/270/300) plus production sur commande sans coût supplémentaire. Le seul ICF avec cette garantie.":
    "3 modelli premium (210/270/300) più produzione su ordinazione senza costi aggiuntivi. L'unico ICF con questa garanzia.",
    "W/m²K · Feu A1 · Antisismique": "W/m²K · Fuoco A1 · Antisismico",
    'alt="Polistibrick PBK — plancher premium"': 'alt="Polistibrick PBK — solaio premium"',
    "Planchers · PBK": "Solai · PBK",
    "Portées <em>jusqu'à 9 m.</em>": "Luci <em>fino a 9 m.</em>",
    "Système préfabriqué léger et ultra-résistant : polystyrène + fibrociment + béton armé. Déphasage thermique 10,8 h.":
    "Sistema prefabbricato leggero e ultra-resistente: polistirene + fibrocemento + calcestruzzo armato. Sfasamento termico 10,8 h.",
    "de portée · 65 kg/m² · Acoustique ≥ 52 dB": "di luce · 65 kg/m² · Acustica ≥ 52 dB",
    'alt="Polistibrick TBK — toit Passivhaus"': 'alt="Polistibrick TBK — tetto Passivhaus"',
    "Toit · TBK": "Tetto · TBK",
    "Passivhaus <em>sortie d'usine.</em>": "Passivhaus <em>dalla fabbrica.</em>",
    "U=0,13 W/m²K, épaisseur 25 cm, seulement 22 kg/m². Le toit le plus performant de sa catégorie. Sans isolation additionnelle.":
    "U=0,13 W/m²K, spessore 25 cm, solo 22 kg/m². Il tetto più performante della sua categoria. Senza isolamento aggiuntivo.",
    'alt="Maison Polistibrick en vue éclatée : toit TBK, plancher PBK, murs MBK"':
    'alt="Casa Polistibrick in vista esplosa: tetto TBK, solaio PBK, pareti MBK"',

    # Montaj
    "Montage": "Montaggio",
    "Étapes de pose": "Fasi di posa",
    "Une maison complète <em>en 4 étapes.</em>": "Una casa completa <em>in 4 fasi.</em>",
    "De la fondation au coffrage fermé — prêt pour le coulage du béton. L'ensemble du processus en quelques semaines avec seulement 2 à 3 personnes sur le chantier.":
    "Dalle fondazioni al cassero chiuso — pronto per il getto di calcestruzzo. L'intero processo in poche settimane con solo 2–3 persone in cantiere.",
    'alt="Coffrage assemblé avec étaiement latéral"': 'alt="Cassero assemblato con puntellatura laterale"',
    "Coffrage": "Cassero",
    "Murs EPS dressés et fixés avec étaiement latéral en bois sur la fondation. Sans mortier, sans perte d'isolation.":
    "Pareti EPS erette e fissate con puntellatura laterale in legno sulla fondazione. Senza malta, senza perdite di isolamento.",
    'alt="Plancher PBK monté"': 'alt="Solaio PBK montato"',
    "Plancher": "Solaio",
    "Panneaux PBK 250 montés horizontalement — couches EPS-Graphite + fibrociment prêtes à recevoir l'armature.":
    "Pannelli PBK 250 montati orizzontalmente — strati EPS-Grafite + fibrocemento pronti per l'armatura.",
    'alt="Armature acier-béton sur plancher"': 'alt="Armatura acciaio-calcestruzzo sul solaio"',
    "Armature": "Armatura",
    "Les treillis d'acier d'armature se placent entre les nervures EPS-Graphite. Liaison monolithique entre les murs et le plancher.":
    "Le reti d'armatura in acciaio si posano tra le nervature EPS-Grafite. Collegamento monolitico tra pareti e solaio.",
    'alt="Coffrage fermé, prêt pour le coulage du béton"': 'alt="Cassero chiuso, pronto per il getto di calcestruzzo"',
    "Fermeture du coffrage": "Chiusura del cassero",
    "Tous les éléments assemblés et vérifiés. <strong>Nous sommes maintenant prêts pour le coulage du béton.</strong>":
    "Tutti gli elementi assemblati e verificati. <strong>Siamo pronti per il getto di calcestruzzo.</strong>",
    "Après le coulage du béton, la structure devient <strong>monolithique en 24 heures</strong> — murs, planchers, toit, isolés en continu, sans ponts thermiques.":
    "Dopo il getto di calcestruzzo, la struttura diventa <strong>monolitica in 24 ore</strong> — pareti, solai, tetto, isolati in continuo, senza ponti termici.",
    "Voir tout le montage": "Vedi tutto il montaggio",
    "Demandez un devis personnalisé": "Richiedi un preventivo personalizzato",

    # Confiance
    "Confiance": "Fiducia",
    'aria-label="Avis et témoignages de constructeurs"': 'aria-label="Recensioni e testimonianze dei costruttori"',
    "Avis vérifiés · Constructeurs": "Recensioni verificate · Costruttori",
    "Ils ont bâti avec Polistibrick — <em>ils en parlent.</em>": "Hanno costruito con Polistibrick — <em>ne parlano.</em>",
    "Témoignage vidéo": "Testimonianza video",
    'aria-label="Lire la vidéo"': 'aria-label="Riproduci il video"',
    'aria-label="5 sur 5"': 'aria-label="5 su 5"',
    "On l'a testé sur un premier chantier et, franchement, <em>c'est une merveille</em>. Le mur monte presque tout seul — on ne revient pas en arrière.":
    "L'abbiamo testato sul primo cantiere e, francamente, <em>è una meraviglia</em>. Il muro si alza quasi da solo — non torniamo indietro.",
    "Entreprise générale · Aix-en-Provence": "Impresa generale · Aix-en-Provence",
    "✓ Constructeur vérifié": "✓ Costruttore verificato",
    "Avec la même équipe, je construis <em>beaucoup plus de maisons</em> dans l'année. Le planning tient enfin.":
    "Con lo stesso team, costruisco <em>molte più case</em> all'anno. Il planning finalmente regge.",
    "Constructeur de maisons · Nantes": "Costruttore di case · Nantes",
    "Avis vérifié": "Recensione verificata",
    "Ma plus grande satisfaction&nbsp;? Boucler <em>un devis en 5 minutes</em>. Je n'ai que le fer, le béton et le coffrage Polistibrick — sûr, et sans erreurs.":
    "La mia più grande soddisfazione&nbsp;? Chiudere <em>un preventivo in 5 minuti</em>. Ho solo ferro, calcestruzzo e cassero Polistibrick — sicuro e senza errori.",
    "Entreprise de construction · Annecy": "Impresa edile · Annecy",
    "Le confort des maisons impressionne à la livraison — <em>charges quasi nulles</em>. Mes clients sont conquis.":
    "Il comfort delle case colpisce alla consegna — <em>consumi quasi nulli</em>. I miei clienti sono conquistati.",
    "Maison individuelle · Bordeaux": "Casa unifamiliare · Bordeaux",
    "✓ Client vérifié": "✓ Cliente verificato",
    "Laisser un avis →": "Lascia una recensione →",
    "Voir tous les avis →": "Vedi tutte le recensioni →",
    "Vidéo ou message + photos · publié après validation": "Video o messaggio + foto · pubblicato dopo validazione",
    'aria-label="Avis précédent"': 'aria-label="Recensione precedente"',
    'aria-label="Avis suivant"': 'aria-label="Recensione successiva"',
    'aria-label="Avis ': 'aria-label="Recensione ',

    # Histoires (hidden section)
    'alt="Maison construite par une entreprise avec le système Polistibrick"':
    'alt="Casa costruita da un\'impresa con il sistema Polistibrick"',
    "il y a 3 mois": "3 mesi fa",
    ". Les gars ont pris le coup de main en deux jours, le mur monte presque tout seul. On ne revient pas en arrière.":
    ". I ragazzi hanno preso la mano in due giorni, il muro si alza quasi da solo. Non torniamo indietro.",
    'alt="Maison réalisée par un constructeur avec le système Polistibrick"':
    'alt="Casa realizzata da un costruttore con il sistema Polistibrick"',
    "il y a 5 mois": "5 mesi fa",
    "Je suis vraiment content d'avoir découvert ce système. Avec la même équipe, je construis aujourd'hui <em>beaucoup plus de maisons</em> dans l'année.":
    "Sono davvero contento di aver scoperto questo sistema. Con lo stesso team, oggi costruisco <em>molte più case</em> all'anno.",
    'alt="Programme de maisons réalisé par une entreprise avec le système Polistibrick"':
    'alt="Programma di case realizzato da un\'impresa con il sistema Polistibrick"',
    "il y a 2 mois": "2 mesi fa",
    ". Je n'ai que le fer, le béton et le coffrage Polistibrick — c'est sûr, et sans erreurs.":
    ". Ho solo ferro, calcestruzzo e cassero Polistibrick — è sicuro e senza errori.",
    'aria-label="Témoignage précédent"': 'aria-label="Testimonianza precedente"',
    'aria-label="Témoignage suivant"': 'aria-label="Testimonianza successiva"',
    'aria-label="Témoignage 1"': 'aria-label="Testimonianza 1"',
    'aria-label="Témoignage 2"': 'aria-label="Testimonianza 2"',
    'aria-label="Témoignage 3"': 'aria-label="Testimonianza 3"',

    # CTA
    "CONSTRUISEZ AVEC NOUS": "COSTRUISCI CON NOI",
    "Construisons ensemble<br><em>votre maison du futur.</em>": "Costruiamo insieme<br><em>la tua casa del futuro.</em>",
    "Parlez-nous de votre projet. Nous vous préparons un devis personnalisé sous 48 heures — sans engagement.":
    "Raccontaci il tuo progetto. Ti prepariamo un preventivo personalizzato entro 48 ore — senza impegno.",

    # Footer
    "Certifié et reconnu internationalement": "Certificato e riconosciuto a livello internazionale",
    "Brevet European": "Brevetto europeo",
    "Agrement Tehnic": "Approvazione tecnica",
    "Standard European": "Standard europeo",
    "Maison Passive": "Casa Passiva",
    "Le système ICF qui construit des maisons plus performantes, plus rapides et plus durables. Fabriqué en UE.":
    "Il sistema ICF brevettato per case passive premium, senza bollette energetiche. Fabbricato nell'UE.",
    "Système": "Sistema",
    "Murs MBK": "Pareti MBK",
    "Planchers PBK": "Solai PBK",
    "Toit TBK": "Tetto TBK",
    "Comment ça fonctionne": "Come funziona",
    "Entreprise": "Azienda",
    "Légal": "Note legali",
    "Mentions légales": "Note legali",
    "Politique de confidentialité": "Privacy",
    "Conditions générales": "Termini e condizioni",
    "Politique de cookies": "Cookie",
    "Durabilité": "Sostenibilità",
    "© 2026 Polistibrick. Tous droits réservés.": "© 2026 Polistibrick. Tutti i diritti riservati. Sistema brevettato.",
    "Fabriqué avec ⚒ en Europe • ISO 9001 / 14001 / 45001": "Realizzato con ⚒ in Europa • ISO 9001 / 14001 / 45001",

    # Banner JS texts for IT locale
    "it: { msg: 'Hai notato che sei in', visit: 'Vai a', yes: 'Sì, vai', no: 'Resta qui' }":
    "it: { msg: 'Abbiamo rilevato che sei in', visit: 'Visita', yes: 'Sì, vai', no: 'Resto qui' }",

    # Avis modal
    "Laisser un avis": "Lascia una recensione",
    "Partagez votre expérience avec Polistibrick. Publié après validation.":
    "Condividi la tua esperienza con Polistibrick. Pubblicato dopo validazione.",
    "Votre note": "La tua valutazione",
    'aria-label="Note"': 'aria-label="Valutazione"',
    'aria-label="1 étoile"': 'aria-label="1 stella"',
    'aria-label="2 étoiles"': 'aria-label="2 stelle"',
    'aria-label="3 étoiles"': 'aria-label="3 stelle"',
    'aria-label="4 étoiles"': 'aria-label="4 stelle"',
    'aria-label="5 étoiles"': 'aria-label="5 stelle"',
    "Nom / Entreprise": "Nome / Azienda",
    "Vous êtes": "Sei",
    "Choisir…": "Scegli…",
    "Auto-constructeur": "Auto-costruttore",
    "Architecte · Ingénieur": "Architetto · Ingegnere",
    "Localité (ville / région)": "Località (città / regione)",
    "Type d'avis": "Tipo di recensione",
    "✍️ Texte + photos": "✍️ Testo + foto",
    "🎥 Vidéo": "🎥 Video",
    "Votre avis": "La tua recensione",
    "Décrivez votre projet et votre expérience…": "Descrivi il tuo progetto e la tua esperienza…",
    "Votre vidéo de témoignage — le plus convaincant ⭐": "Il tuo video testimonianza — il più convincente ⭐",
    "🎥 Ajouter ou filmer votre vidéo de témoignage": "🎥 Aggiungi o registra il tuo video testimonianza",
    "Photos du projet (optionnel)": "Foto del progetto (opzionale)",
    "📷 Ajouter des photos de votre chantier / maison": "📷 Aggiungi foto del tuo cantiere / casa",
    "Logo de votre entreprise (optionnel)": "Logo della tua azienda (opzionale)",
    "Ajouter votre logo": "Aggiungi il tuo logo",
    "Merci de remplir au moins : note, nom et avis.": "Compila almeno: valutazione, nome e recensione.",
    "J'accepte que mes données soient traitées conformément à la":
    "Accetto che i miei dati siano trattati conformemente alla",
    "politique de confidentialité (RGPD)": "informativa sulla privacy (GDPR)",
    "Envoyer mon avis →": "Invia la mia recensione →",
    "🔒 Vérifié et publié par Polistibrick après validation.":
    "🔒 Verificato e pubblicato da Polistibrick dopo validazione.",
    "Merci !": "Grazie!",
    "Votre avis a bien été envoyé. Il sera publié sur le site après validation par notre équipe.":
    "La tua recensione è stata inviata. Sarà pubblicata sul sito dopo la validazione del nostro team.",
    "Votre avis (optionnel)": "La tua recensione (opzionale)",
    'aria-label="Retirer"': 'aria-label="Rimuovi"',
    "Retirer la vidéo": "Rimuovi il video",

    # Mobile contact bar
    'aria-label="Contact rapide"': 'aria-label="Contatto rapido"',
    'aria-label="Appeler Polistibrick"': 'aria-label="Chiama Polistibrick"',
    "Appeler": "Chiama",
    'aria-label="Envoyer un email"': 'aria-label="Invia email"',

    # Remaining nav product labels
    "Brevet": "Brevetto",
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
            it = translations[fr]
            if fr in segment:
                segment = segment.replace(fr, it)
        out.append(segment)
    return "".join(out)


def main():
    content = SOURCE.read_text(encoding="utf-8")
    content = content.replace('<html lang="fr">', '<html lang="it">')
    content = apply_translations(content, TRANSLATIONS)
    TARGET.write_text(content, encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
