#!/usr/bin/env python3
"""Generate translated_chunk_2.json from missing_chunk_2.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MISSING = ROOT / "missing_chunk_2.json"
OUTPUT = ROOT / "translated_chunk_2.json"

# Each entry: (en, fr, it, es, nl, de)
T = {}

def _add(ro, en, fr, it, es, nl, de):
    T[ro] = (en, fr, it, es, nl, de)

# Batch 1 (1-30)
_add(
"Datele dumneavoastră nu sunt vândute. Apelăm la următorii furnizori, strict pentru scopurile indicate:",
"Your data is never sold. We use the following providers strictly for the purposes stated:",
"Vos données ne sont jamais vendues. Nous faisons appel aux fournisseurs suivants, strictement pour les finalités indiquées :",
"I vostri dati non vengono mai venduti. Ci avvaliamo dei seguenti fornitori, esclusivamente per le finalità indicate:",
"Sus datos no se venden. Recurrimos a los siguientes proveedores, estrictamente para los fines indicados:",
"Uw gegevens worden nooit verkocht. Wij maken uitsluitend gebruik van de volgende leveranciers voor de aangegeven doeleinden:",
"Ihre Daten werden nicht verkauft. Wir nutzen die folgenden Anbieter ausschließlich für die angegebenen Zwecke:",
)
_add(
"Încarcă planurile (PDF, DWG, DXF) sau descrie proiectul — primești oferta estimativă în câteva minute.",
"Upload your plans (PDF, DWG, DXF) or describe your project — receive an estimated quote in minutes.",
"Téléchargez vos plans (PDF, DWG, DXF) ou décrivez votre projet — recevez un devis estimatif en quelques minutes.",
"Carica i progetti (PDF, DWG, DXF) o descrivi il progetto — ricevi un preventivo stimato in pochi minuti.",
"Sube los planos (PDF, DWG, DXF) o describe el proyecto — recibe un presupuesto estimado en minutos.",
"Upload de plannen (PDF, DWG, DXF) of beschrijf het project — ontvang binnen enkele minuten een raming.",
"Laden Sie Ihre Pläne (PDF, DWG, DXF) hoch oder beschreiben Sie Ihr Projekt — erhalten Sie in wenigen Minuten ein Kostenvoranschlag.",
)
_add(
"în stocarea locală a browserului). Indispensabile pentru respectarea preferințelor dumneavoastră GDPR.",
"in your browser's local storage). Essential for respecting your GDPR preferences.",
"dans le stockage local de votre navigateur). Indispensables au respect de vos préférences RGPD.",
"nella memoria locale del browser). Indispensabili per rispettare le vostre preferenze GDPR.",
"en el almacenamiento local del navegador). Imprescindibles para respetar sus preferencias RGPD.",
"in de lokale opslag van uw browser). Onmisbaar voor het respecteren van uw AVG-voorkeuren.",
"im lokalen Speicher Ihres Browsers). Unverzichtbar für die Einhaltung Ihrer DSGVO-Einstellungen.",
)
_add(
". Primele familii locuiesc încă în casele lor, cu aceleași performanțe ca în prima zi. Structura este",
". The first families still live in their homes, with the same performance as day one. The structure is",
". Les premières familles vivent encore dans leurs maisons, avec les mêmes performances qu'au premier jour. La structure est",
". Le prime famiglie vivono ancora nelle loro case, con le stesse prestazioni del primo giorno. La struttura è",
". Las primeras familias siguen viviendo en sus casas, con el mismo rendimiento que el primer día. La estructura es",
". De eerste gezinnen wonen nog steeds in hun huizen, met dezelfde prestaties als op dag één. De structuur is",
". Die ersten Familien leben noch immer in ihren Häusern, mit derselben Leistung wie am ersten Tag. Die Struktur ist",
)
_add(
": îl măsurați, îl tăiați, îl fixați — exact ca orice alt sistem de cofraj. Singura regulă pe șantier:",
": measure it, cut it, fix it — just like any other formwork system. The only rule on site:",
" : vous le mesurez, vous le coupez, vous le fixez — exactement comme tout autre système de coffrage. La seule règle sur chantier :",
": lo misurate, lo tagliate, lo fissate — esattamente come qualsiasi altro sistema di cassero. L'unica regola in cantiere:",
": lo mide, lo corta, lo fija — exactamente como cualquier otro sistema de encofrado. La única regla en obra:",
": u meet het, snijdt het, bevestigt het — precies zoals elk ander bekistingssysteem. De enige regel op de werf:",
": Sie messen, schneiden und befestigen es — genau wie bei jedem anderen Schalungssystem. Die einzige Regel auf der Baustelle:",
)
_add(
"Parcurs structurat, dedicat programelor de ansamblu. Șef de proiect alocat de la nivelul 10+ unități.",
"Structured pathway dedicated to development programmes. Project manager assigned from 10+ units.",
"Parcours structuré, dédié aux programmes d'ensemble. Chef de projet assigné à partir de 10+ unités.",
"Percorso strutturato, dedicato ai programmi di complesso. Capo progetto assegnato a partire da 10+ unità.",
"Recorrido estructurado, dedicado a programas de conjunto. Jefe de proyecto asignado a partir de 10+ unidades.",
"Gestructureerd traject, toegewijd aan wooncomplexprogramma's. Projectleider toegewezen vanaf 10+ eenheden.",
"Strukturierter Ablauf für Wohnanlagenprogramme. Projektleiter ab 10+ Einheiten zugewiesen.",
)
_add(
"Selectați țara unde construiți pentru a vedea contactul echipei locale și a-i trimite mesajul direct.",
"Select the country where you are building to see your local team contact and send them a message directly.",
"Sélectionnez le pays où vous construisez pour voir le contact de l'équipe locale et lui envoyer un message directement.",
"Selezionate il paese in cui costruite per vedere il contatto del team locale e inviargli un messaggio direttamente.",
"Seleccione el país donde construye para ver el contacto del equipo local y enviarle un mensaje directamente.",
"Selecteer het land waar u bouwt om het contact van het lokale team te zien en hen direct een bericht te sturen.",
"Wählen Sie das Land, in dem Sie bauen, um den Kontakt des lokalen Teams zu sehen und direkt eine Nachricht zu senden.",
)
_add(
"Vrem să fii sigur că ce îți promitem se verifică în viața reală a celor care au cumpărat înaintea ta.",
"We want you to be confident that what we promise is verified in the real lives of those who bought before you.",
"Nous voulons que vous soyez certain que ce que nous promettons se vérifie dans la vie réelle de ceux qui ont acheté avant vous.",
"Vogliamo che tu sia sicuro che ciò che promettiamo si verifica nella vita reale di chi ha acquistato prima di te.",
"Queremos que estés seguro de que lo que prometemos se verifica en la vida real de quienes compraron antes que tú.",
"We willen dat u er zeker van bent dat wat wij beloven, wordt bevestigd in het echte leven van degenen die vóór u kochten.",
"Wir möchten, dass Sie sicher sein können, dass das, was wir versprechen, im wirklichen Leben derer bestätigt wird, die vor Ihnen gekauft haben.",
)
_add(
"— clienții care ajung pe polistibrick.eu sunt redirecționați către partenerii certificați din regiune",
"— visitors to polistibrick.eu are redirected to certified partners in their region",
"— les visiteurs de polistibrick.eu sont redirigés vers les partenaires certifiés de leur région",
"— i visitatori di polistibrick.eu vengono reindirizzati ai partner certificati della regione",
"— los visitantes de polistibrick.eu son redirigidos a los socios certificados de su región",
"— bezoekers van polistibrick.eu worden doorverwezen naar gecertificeerde partners in hun regio",
"— Besucher von polistibrick.eu werden an zertifizierte Partner in ihrer Region weitergeleitet",
)
_add(
"Costul variază în funcție de regiune, suprafață și nivel de finisaje. În medie în România, calculați",
"Cost varies by region, floor area and finish level. On average in Romania, calculate",
"Le coût varie selon la région, la surface et le niveau de finitions. En moyenne en Roumanie, calculez",
"Il costo varia in base a regione, superficie e livello di finiture. In media in Romania, calcolate",
"El coste varía según la región, la superficie y el nivel de acabados. De media en Rumanía, calcule",
"De kosten variëren per regio, oppervlakte en afwerkingsniveau. Gemiddeld in Roemenië, bereken",
"Die Kosten variieren je nach Region, Fläche und Ausbaustandard. Im Durchschnitt in Rumänien, rechnen Sie mit",
)
_add(
"Electricitate, instalații sanitare, ventilație cu recuperare de căldură. Țiglă ceramică pe acoperiș.",
"Electricity, plumbing, heat recovery ventilation. Ceramic roof tiles.",
"Électricité, installations sanitaires, ventilation avec récupération de chaleur. Tuiles céramiques en toiture.",
"Elettricità, impianti sanitari, ventilazione con recupero di calore. Tegole ceramiche sul tetto.",
"Electricidad, instalaciones sanitarias, ventilación con recuperación de calor. Teja cerámica en cubierta.",
"Elektriciteit, sanitaire installaties, ventilatie met warmteterugwinning. Keramische dakpannen.",
"Elektrizität, Sanitärinstallationen, Lüftung mit Wärmerückgewinnung. Keramische Dachziegel.",
)
_add(
"O echipă mică e suficientă. Mai puțină manoperă, mai puțină coordonare, costuri mai mici de șantier.",
"A small team is enough. Less labour, less coordination, lower site costs.",
"Une petite équipe suffit. Moins de main-d'œuvre, moins de coordination, des coûts de chantier réduits.",
"Basta una squadra piccola. Meno manodopera, meno coordinamento, costi di cantiere inferiori.",
"Basta un equipo pequeño. Menos mano de obra, menos coordinación, menores costes de obra.",
"Een klein team is voldoende. Minder arbeid, minder coördinatie, lagere bouwkosten.",
"Ein kleines Team genügt. Weniger Arbeitsaufwand, weniger Koordination, geringere Baustellenkosten.",
)
_add(
"Sau, dacă preferați, continuați prin formularul de contact — un specialist vă răspunde în 48 de ore.",
"Or, if you prefer, continue via the contact form — a specialist will respond within 48 hours.",
"Ou, si vous préférez, continuez via le formulaire de contact — un spécialiste vous répond sous 48 heures.",
"Oppure, se preferite, proseguite tramite il modulo di contatto — uno specialista vi risponde entro 48 ore.",
"O, si lo prefiere, continúe mediante el formulario de contacto — un especialista le responderá en 48 horas.",
"Of ga, als u dat liever heeft, verder via het contactformulier — een specialist antwoordt binnen 48 uur.",
"Oder fahren Sie, wenn Sie möchten, über das Kontaktformular fort — ein Spezialist antwortet innerhalb von 48 Stunden.",
)
_add(
"Sistem Passivhaus din fabrică. Deschideri de 9 m, U=0,13, doar 22 kg/m². Fără izolație suplimentară.",
"Passivhaus system from the factory. 9 m spans, U=0.13, only 22 kg/m². No additional insulation.",
"Système Passivhaus d'usine. Portées de 9 m, U=0,13, seulement 22 kg/m². Sans isolation supplémentaire.",
"Sistema Passivhaus di fabbrica. Luci di 9 m, U=0,13, solo 22 kg/m². Senza isolamento aggiuntivo.",
"Sistema Passivhaus de fábrica. Luces de 9 m, U=0,13, solo 22 kg/m². Sin aislamiento adicional.",
"Passivhaus-systeem uit de fabriek. Overspanningen van 9 m, U=0,13, slechts 22 kg/m². Geen extra isolatie.",
"Passivhaus-System ab Werk. Spannweiten von 9 m, U=0,13, nur 22 kg/m². Keine zusätzliche Dämmung.",
)
_add(
"Puține deșeuri, puțin praf, toleranțe de fabrică. Un șantier ordonat de la început până la sfârșit.",
"Minimal waste, minimal dust, factory tolerances. An orderly site from start to finish.",
"Peu de déchets, peu de poussière, tolérances d'usine. Un chantier ordonné du début à la fin.",
"Pochi rifiuti, poca polvere, tolleranze di fabbrica. Un cantiere ordinato dall'inizio alla fine.",
"Pocos residuos, poco polvo, tolerancias de fábrica. Una obra ordenada de principio a fin.",
"Weinig afval, weinig stof, fabriekstoleranties. Een geordende werf van begin tot eind.",
"Wenig Abfall, wenig Staub, Werktoleranzen. Eine ordentliche Baustelle von Anfang bis Ende.",
)
_add(
"Vizitați unul dintre centrele de producție pentru a descoperi fabricarea automatizată a sistemelor.",
"Visit one of our production centres to discover the automated manufacturing of our systems.",
"Visitez l'un de nos centres de production pour découvrir la fabrication automatisée de nos systèmes.",
"Visitate uno dei nostri centri di produzione per scoprire la fabbricazione automatizzata dei sistemi.",
"Visite uno de nuestros centros de producción para descubrir la fabricación automatizada de los sistemas.",
"Bezoek een van onze productiecentra om de geautomatiseerde fabricage van onze systemen te ontdekken.",
"Besuchen Sie eines unserer Produktionszentren und entdecken Sie die automatisierte Fertigung unserer Systeme.",
)
_add(
"pentru o casă de 150-200 m² la sol (structură). Panourile, pe toată înălțimea etajului, se montează",
"for a 150–200 m² ground-floor house (structure). Panels, spanning the full storey height, are installed",
"pour une maison de 150-200 m² au sol (structure). Les panneaux, sur toute la hauteur de l'étage, se montent",
"per una casa di 150-200 m² a terra (struttura). I pannelli, per tutta l'altezza del piano, si montano",
"para una casa de 150-200 m² en planta (estructura). Los paneles, a toda la altura de la planta, se montan",
"voor een huis van 150-200 m² op de begane grond (structuur). De panelen, over de volledige verdiepingshoogte, worden gemonteerd",
"für ein Haus mit 150–200 m² Grundfläche (Struktur). Die Paneele, über die gesamte Geschosshöhe, werden montiert",
)
_add(
"« Am crescut pe șantiere. Mi-am petrecut cariera rezolvând ceea ce nimeni altcineva nu rezolvase. »",
'"I grew up on construction sites. I spent my career solving what no one else had solved."',
"« J'ai grandi sur les chantiers. J'ai passé ma carrière à résoudre ce que personne d'autre n'avait résolu. »",
"« Sono cresciuto nei cantieri. Ho passato la mia carriera a risolvere ciò che nessun altro aveva risolto. »",
"« Crecí en obras. Pasé mi carrera resolviendo lo que nadie más había resuelto. »",
"« Ik ben opgewassen op bouwplaatsen. Ik heb mijn carrière besteed aan het oplossen van wat niemand anders had opgelost. »",
'„Ich bin auf Baustellen aufgewachsen. Ich habe meine Karriere damit verbracht, zu lösen, was niemand sonst gelöst hatte."',
)
_add(
"🎬 Video-urile reale vor înlocui aceste placeholder-e pe măsură ce le filmăm cu proprietarii noștri.",
"🎬 Real videos will replace these placeholders as we film them with our homeowners.",
"🎬 Les vidéos réelles remplaceront ces placeholders au fur et à mesure que nous les tournons avec nos propriétaires.",
"🎬 I video reali sostituiranno questi placeholder man mano che li filmiamo con i nostri proprietari.",
"🎬 Los vídeos reales sustituirán estos marcadores de posición a medida que los filmemos con nuestros propietarios.",
"🎬 Echte video's vervangen deze placeholders zodra we ze opnemen met onze huiseigenaren.",
"🎬 Echte Videos ersetzen diese Platzhalter, sobald wir sie mit unseren Hausbesitzern drehen.",
)
_add(
". Băieții au prins metoda în două zile, peretele se ridică aproape singur. Nu ne întoarcem înapoi.",
". The crew picked up the method in two days, the wall goes up almost by itself. We're not going back.",
". L'équipe a maîtrisé la méthode en deux jours, le mur se dresse presque tout seul. On ne revient pas en arrière.",
". La squadra ha imparato il metodo in due giorni, il muro si alza quasi da solo. Non torniamo indietro.",
". El equipo dominó el método en dos días, el muro se levanta casi solo. No volvemos atrás.",
". Het team pakte de methode in twee dagen op, de muur gaat bijna vanzelf omhoog. We gaan niet terug.",
". Das Team hat die Methode in zwei Tagen verstanden, die Wand steht fast von selbst. Wir gehen nicht zurück.",
)
_add(
"Articole despre casa pasivă, ICF, miturile despre EPS, etanșeitatea la aer și multe alte subiecte.",
"Articles on passive houses, ICF, EPS myths, airtightness and many other topics.",
"Articles sur la maison passive, l'ICF, les mythes sur l'EPS, l'étanchéité à l'air et bien d'autres sujets.",
"Articoli su casa passiva, ICF, miti sull'EPS, tenuta all'aria e molti altri argomenti.",
"Artículos sobre casa pasiva, ICF, mitos del EPS, estanqueidad al aire y muchos otros temas.",
"Artikelen over passiefhuis, ICF, EPS-mythen, luchtdichtheid en vele andere onderwerpen.",
"Artikel über Passivhaus, ICF, EPS-Mythen, Luftdichtheit und viele weitere Themen.",
)
_add(
"12 case structurale montate în 8 săptămâni. Echipă de 12 persoane repartizată pe 2 case simultan.",
"12 structural homes assembled in 8 weeks. Team of 12 split across 2 homes simultaneously.",
"12 maisons structurelles montées en 8 semaines. Équipe de 12 personnes répartie sur 2 maisons simultanément.",
"12 case strutturali montate in 8 settimane. Squadra di 12 persone ripartita su 2 case simultaneamente.",
"12 casas estructurales montadas en 8 semanas. Equipo de 12 personas repartido en 2 casas simultáneamente.",
"12 structurele woningen gemonteerd in 8 weken. Team van 12 personen verdeeld over 2 woningen tegelijk.",
"12 Strukturhäuser in 8 Wochen montiert. Team von 12 Personen auf 2 Häuser gleichzeitig verteilt.",
)
_add(
"Completezi formularul. Toate datele rămân confidențiale și sunt verificate de echipa noastră B2B.",
"Fill in the form. All data remains confidential and is verified by our B2B team.",
"Remplissez le formulaire. Toutes les données restent confidentielles et sont vérifiées par notre équipe B2B.",
"Compilate il modulo. Tutti i dati restano riservati e vengono verificati dal nostro team B2B.",
"Complete el formulario. Todos los datos permanecen confidenciales y son verificados por nuestro equipo B2B.",
"Vul het formulier in. Alle gegevens blijven vertrouwelijk en worden gecontroleerd door ons B2B-team.",
"Füllen Sie das Formular aus. Alle Daten bleiben vertraulich und werden von unserem B2B-Team geprüft.",
)
_add(
"De la primul plan la primul Crăciun acasă. Ghid practic cu calendar, bugete și capcane de evitat.",
"From first plan to first Christmas at home. Practical guide with timeline, budgets and pitfalls to avoid.",
"Du premier plan au premier Noël à la maison. Guide pratique avec calendrier, budgets et pièges à éviter.",
"Dal primo progetto al primo Natale a casa. Guida pratica con calendario, budget e insidie da evitare.",
"Del primer plano al primer Navidad en casa. Guía práctica con calendario, presupuestos y trampas a evitar.",
"Van het eerste plan tot de eerste Kerst thuis. Praktische gids met planning, budgetten en valkuilen om te vermijden.",
"Vom ersten Plan bis zum ersten Weihnachten zu Hause. Praktischer Leitfaden mit Zeitplan, Budgets und Fallstricken.",
)
_add(
"Direct pe șantier, în 2–5 zile pentru orice destinație europeană. Intervale de livrare flexibile.",
"Direct to site, in 2–5 days for any European destination. Flexible delivery windows.",
"Livraison directe sur chantier, en 2 à 5 jours pour toute destination européenne. Créneaux de livraison flexibles.",
"Direttamente in cantiere, in 2–5 giorni per qualsiasi destinazione europea. Finestre di consegna flessibili.",
"Directo a obra, en 2–5 días para cualquier destino europeo. Ventanas de entrega flexibles.",
"Rechtstreeks naar de werf, in 2–5 dagen voor elke Europese bestemming. Flexibele leveringsvensters.",
"Direkt auf die Baustelle, in 2–5 Tagen für jedes europäische Ziel. Flexible Lieferfenster.",
)
_add(
"Spune-ne despre proiectul tău. Îți pregătim o ofertă personalizată în 48 de ore — fără obligație.",
"Tell us about your project. We'll prepare a personalized quote within 48 hours — no obligation.",
"Parlez-nous de votre projet. Nous préparons un devis personnalisé sous 48 heures — sans engagement.",
"Raccontaci il tuo progetto. Ti prepariamo un preventivo personalizzato entro 48 ore — senza impegno.",
"Cuéntanos tu proyecto. Te preparamos un presupuesto personalizado en 48 horas — sin compromiso.",
"Vertel ons over uw project. Wij stellen binnen 48 uur een persoonlijke offerte op — vrijblijvend.",
"Erzählen Sie uns von Ihrem Projekt. Wir erstellen innerhalb von 48 Stunden ein individuelles Angebot — unverbindlich.",
)
_add(
"Apel telefonic de 30 min cu șeful de proiect ansamblu. Număr unități, suprafață, calendar țintă.",
"30-minute call with the development project manager. Unit count, floor area, target timeline.",
"Appel téléphonique de 30 min avec le chef de projet ensemble. Nombre d'unités, surface, calendrier cible.",
"Chiamata di 30 min con il capo progetto del complesso. Numero unità, superficie, calendario obiettivo.",
"Llamada de 30 min con el jefe de proyecto del conjunto. Número de unidades, superficie, calendario objetivo.",
"Telefoongesprek van 30 min met de projectleider van het complex. Aantal eenheden, oppervlakte, streefplanning.",
"30-minütiges Gespräch mit dem Projektleiter der Anlage. Anzahl Einheiten, Fläche, Zielzeitplan.",
)
_add(
"Foc A1 + antiseismic Excelent. Structura din lemn nu rezistă nici la foc, nici în zone seismice.",
"A1 fire resistance + Excellent seismic rating. Timber structures fail on both fire and seismic zones.",
"Feu A1 + parasismique Excellent. La structure bois ne résiste ni au feu, ni en zone sismique.",
"Fuoco A1 + antisismico Eccellente. La struttura in legno non resiste né al fuoco, né in zone sismiche.",
"Fuego A1 + antisísmico Excelente. La estructura de madera no resiste ni al fuego ni en zonas sísmicas.",
"Brand A1 + aardbevingsbestendig Uitstekend. Houtstructuren falen zowel bij brand als in seismische zones.",
"Feuer A1 + erdbebensicher Ausgezeichnet. Holzstrukturen versagen sowohl beim Brand als auch in Erdbebengebieten.",
)
_add(
"Sistemul ICF care construiește case mai performante, mai rapide și mai durabile. Fabricat în UE.",
"The ICF system that builds higher-performing, faster and more durable homes. Made in the EU.",
"Le système ICF qui construit des maisons plus performantes, plus rapides et plus durables. Fabriqué dans l'UE.",
"Il sistema ICF che costruisce case più performanti, più rapide e più durature. Prodotto nell'UE.",
"El sistema ICF que construye casas más eficientes, más rápidas y más duraderas. Fabricado en la UE.",
"Het ICF-systeem dat beter presterende, snellere en duurzamere huizen bouwt. Gemaakt in de EU.",
"Das ICF-System, das leistungsfähigere, schnellere und langlebigere Häuser baut. Hergestellt in der EU.",
)
_add(
"— 30 de minute pe șantier, publicare pe rețele sociale inclusă, ofertă pentru următorul proiect.",
"— 30 minutes on site, social media coverage included, quote for your next project.",
"— 30 minutes sur chantier, publication sur les réseaux sociaux incluse, devis pour le prochain projet.",
"— 30 minuti in cantiere, pubblicazione sui social inclusa, preventivo per il prossimo progetto.",
"— 30 minutos en obra, publicación en redes sociales incluida, presupuesto para el próximo proyecto.",
"— 30 minuten op de werf, publicatie op sociale media inbegrepen, offerte voor het volgende project.",
"— 30 Minuten auf der Baustelle, Social-Media-Veröffentlichung inklusive, Angebot für das nächste Projekt.",
)
_add(
"— acolo unde o casă clasică ar necesita plăci diferite pentru fiecare dintre aceste proprietăți.",
"— where a conventional home would require different panels for each of these properties.",
"— là où une maison classique nécessiterait des panneaux différents pour chacune de ces propriétés.",
"— dove una casa classica richiederebbe pannelli diversi per ciascuna di queste proprietà.",
"— donde una casa clásica requeriría paneles diferentes para cada una de estas propiedades.",
"— waar een klassiek huis voor elk van deze eigenschappen verschillende panelen zou vereisen.",
"— wo ein klassisches Haus für jede dieser Eigenschaften unterschiedliche Paneele erfordern würde.",
)
_add(
"Vrei să-ți crești afacerea? Vrei să fii primul din zona ta care oferă case pasive? Aplică acum.",
"Want to grow your business? Want to be the first in your area to offer passive homes? Apply now.",
"Vous voulez développer votre activité ? Vous voulez être le premier dans votre région à proposer des maisons passives ? Postulez maintenant.",
"Vuoi far crescere la tua attività? Vuoi essere il primo nella tua zona a offrire case passive? Candidati ora.",
"¿Quieres hacer crecer tu negocio? ¿Quieres ser el primero en tu zona en ofrecer casas pasivas? Solicita ahora.",
"Wilt u uw bedrijf laten groeien? Wilt u de eerste in uw regio zijn die passieve huizen aanbiedt? Solliciteer nu.",
"Möchten Sie Ihr Geschäft ausbauen? Möchten Sie der Erste in Ihrer Region sein, der Passivhäuser anbietet? Jetzt bewerben.",
)
_add(
"Acord-cadru anual, șef de proiect dedicat, tarife negociate, co-marketing pe canalele noastre.",
"Annual framework agreement, dedicated project manager, negotiated rates, co-marketing on our channels.",
"Accord-cadre annuel, chef de projet dédié, tarifs négociés, co-marketing sur nos canaux.",
"Accordo quadro annuale, capo progetto dedicato, tariffe negoziate, co-marketing sui nostri canali.",
"Acuerdo marco anual, jefe de proyecto dedicado, tarifas negociadas, co-marketing en nuestros canales.",
"Jaarlijks raamcontract, toegewijde projectleider, onderhandelde tarieven, co-marketing op onze kanalen.",
"Jährlicher Rahmenvertrag, dedizierter Projektleiter, verhandelte Tarife, Co-Marketing auf unseren Kanälen.",
)
_add(
"Combinația EPS + fibrocement absoarbe pașii și zgomotul aerian între etaje. Liniște garantată.",
"The EPS + fibre cement combination absorbs footsteps and airborne noise between floors. Guaranteed quiet.",
"La combinaison EPS + fibrociment absorbe les pas et le bruit aérien entre les étages. Tranquillité garantie.",
"La combinazione EPS + fibrocemento assorbe i passi e il rumore aereo tra i piani. Silenzio garantito.",
"La combinación EPS + fibrocemento absorbe los pasos y el ruido aéreo entre plantas. Tranquilidad garantizada.",
"De combinatie EPS + vezelcement absorbeert voetstappen en luchtgeluid tussen verdiepingen. Gegarandeerde rust.",
"Die Kombination EPS + Faserzement absorbiert Tritte und Luftschall zwischen den Geschossen. Garantierte Ruhe.",
)
_add(
"Fiecare lot este verificat dimensional și termic. Loturile cu abatere &gt; 1 mm sunt respinse.",
"Every batch is dimensionally and thermally verified. Batches with deviation &gt; 1 mm are rejected.",
"Chaque lot est vérifié dimensionnellement et thermiquement. Les lots avec écart &gt; 1 mm sont rejetés.",
"Ogni lotto è verificato dimensionalmente e termicamente. I lotti con scostamento &gt; 1 mm vengono respinti.",
"Cada lote se verifica dimensional y térmicamente. Los lotes con desviación &gt; 1 mm se rechazan.",
"Elke partij wordt dimensionaal en thermisch gecontroleerd. Partijen met afwijking &gt; 1 mm worden afgekeurd.",
"Jede Charge wird dimensional und thermisch geprüft. Chargen mit Abweichung &gt; 1 mm werden abgelehnt.",
)
_add(
"Fișe tehnice, CAD, BIM, detalii constructive, rapoarte de încercare. Vă trimitem totul în 24h.",
"Technical datasheets, CAD, BIM, construction details, test reports. We send everything within 24h.",
"Fiches techniques, CAD, BIM, détails constructifs, rapports d'essai. Nous vous envoyons tout sous 24h.",
"Schede tecniche, CAD, BIM, dettagli costruttivi, rapporti di prova. Vi inviamo tutto entro 24h.",
"Fichas técnicas, CAD, BIM, detalles constructivos, informes de ensayo. Le enviamos todo en 24h.",
"Technische fiches, CAD, BIM, constructiedetails, testrapporten. Wij sturen alles binnen 24u.",
"Technische Datenblätter, CAD, BIM, Konstruktionsdetails, Prüfberichte. Wir senden alles innerhalb von 24h.",
)
_add(
"Sunt cu adevărat mulțumit că am descoperit acest sistem. Cu aceeași echipă, construiesc astăzi",
"I am truly glad I discovered this system. With the same crew, I am building today",
"Je suis vraiment content d'avoir découvert ce système. Avec la même équipe, je construis aujourd'hui",
"Sono davvero soddisfatto di aver scoperto questo sistema. Con la stessa squadra, costruisco oggi",
"Estoy realmente satisfecho de haber descubierto este sistema. Con el mismo equipo, construyo hoy",
"Ik ben echt blij dat ik dit systeem heb ontdekt. Met hetzelfde team bouw ik vandaag",
"Ich bin wirklich froh, dieses System entdeckt zu haben. Mit demselben Team baue ich heute",
)
_add(
"Acoperișul Passivhaus care iese din fabrică gata de montaj. Etanș la aer, fără punți termice.",
"The Passivhaus roof that leaves the factory ready to install. Airtight, no thermal bridges.",
"Le toit Passivhaus qui sort d'usine prêt à monter. Étanche à l'air, sans ponts thermiques.",
"Il tetto Passivhaus che esce di fabbrica pronto per il montaggio. A tenuta d'aria, senza ponti termici.",
"El tejado Passivhaus que sale de fábrica listo para montar. Estanco al aire, sin puentes térmicos.",
"Het Passivhaus-dak dat uit de fabriek komt, klaar om te monteren. Luchtdicht, zonder koudebruggen.",
"Das Passivhaus-Dach, das ab Werk montagefertig aus der Fabrik kommt. Luftdicht, ohne Wärmebrücken.",
)
_add(
"O echipă de 4 persoane montează pereții parterului. Casa e mai mare — durează puțin mai mult.",
"A team of 4 installs the ground-floor walls. The house is larger — it takes a little longer.",
"Une équipe de 4 personnes monte les murs du rez-de-chaussée. La maison est plus grande — cela prend un peu plus de temps.",
"Una squadra di 4 persone monta i muri del piano terra. La casa è più grande — ci vuole un po' più di tempo.",
"Un equipo de 4 personas monta los muros de la planta baja. La casa es más grande — tarda un poco más.",
"Een team van 4 personen monteert de muren van de begane grond. Het huis is groter — het duurt iets langer.",
"Ein Team von 4 Personen montiert die Wände des Erdgeschosses. Das Haus ist größer — es dauert etwas länger.",
)
_add(
"Structură 4–6 săptămâni (față de 4–5 luni). Pe un program de 10 unități, câștigați 3–4 luni =",
"Structure in 4–6 weeks (vs 4–5 months). On a 10-unit programme, you gain 3–4 months =",
"Structure en 4–6 semaines (contre 4–5 mois). Sur un programme de 10 unités, vous gagnez 3–4 mois =",
"Struttura in 4–6 settimane (contro 4–5 mesi). Su un programma di 10 unità, guadagnate 3–4 mesi =",
"Estructura en 4–6 semanas (frente a 4–5 meses). En un programa de 10 unidades, gana 3–4 meses =",
"Structuur in 4–6 weken (vs 4–5 maanden). Bij een programma van 10 eenheden wint u 3–4 maanden =",
"Struktur in 4–6 Wochen (vs. 4–5 Monate). Bei einem 10-Einheiten-Programm gewinnen Sie 3–4 Monate =",
)
_add(
"Toate elementele sunt asamblate și verificate. Casa este acum gata pentru turnarea betonului.",
"All elements are assembled and verified. The house is now ready for the concrete pour.",
"Tous les éléments sont assemblés et vérifiés. La maison est maintenant prête pour le coulage du béton.",
"Tutti gli elementi sono assemblati e verificati. La casa è ora pronta per il getto di calcestruzzo.",
"Todos los elementos están ensamblados y verificados. La casa está ahora lista para el hormigonado.",
"Alle elementen zijn gemonteerd en gecontroleerd. Het huis is nu klaar voor het storten van beton.",
"Alle Elemente sind montiert und geprüft. Das Haus ist jetzt bereit für die Betonierung.",
)
_add(
"care au inundat piața fără valoare adăugată reală — în timp ce Polistibrick oferă o adevărată",
"that flooded the market without real added value — while Polistibrick offers a genuine",
"qui ont inondé le marché sans réelle valeur ajoutée — tandis que Polistibrick offre une véritable",
"che hanno invaso il mercato senza reale valore aggiunto — mentre Polistibrick offre una vera",
"que han inundado el mercado sin valor añadido real — mientras Polistibrick ofrece una auténtica",
"die de markt overspoelden zonder echte toegevoegde waarde — terwijl Polistibrick een echte",
"die den Markt ohne echten Mehrwert überschwemmt haben — während Polistibrick ein echtes",
)
_add(
"Cere o ofertă personalizată — calculăm precis pentru proiectul tău, pe baza planurilor tale.",
"Request a personalized quote — we calculate precisely for your project, based on your plans.",
"Demandez un devis personnalisé — nous calculons précisément pour votre projet, sur la base de vos plans.",
"Richiedi un preventivo personalizzato — calcoliamo con precisione per il tuo progetto, in base ai tuoi progetti.",
"Pide un presupuesto personalizado — calculamos con precisión para tu proyecto, según tus planos.",
"Vraag een persoonlijke offerte aan — wij berekenen nauwkeurig voor uw project, op basis van uw plannen.",
"Fordern Sie ein individuelles Angebot an — wir kalkulieren präzise für Ihr Projekt, basierend auf Ihren Plänen.",
)
_add(
"Cere o ofertă personalizată — calculăm exact pentru proiectul tău, pe baza planurilor tale.",
"Request a personalized quote — we calculate exactly for your project, based on your plans.",
"Demandez un devis personnalisé — nous calculons exactement pour votre projet, sur la base de vos plans.",
"Richiedi un preventivo personalizzato — calcoliamo esattamente per il tuo progetto, in base ai tuoi progetti.",
"Pide un presupuesto personalizado — calculamos exactamente para tu proyecto, según tus planos.",
"Vraag een persoonlijke offerte aan — wij berekenen exact voor uw project, op basis van uw plannen.",
"Fordern Sie ein individuelles Angebot an — wir kalkulieren exakt für Ihr Projekt, basierend auf Ihren Plänen.",
)
_add(
"Echilibrul perfect între performanță și cost. Conform casă pasivă în toată Europa Centrală.",
"The perfect balance between performance and cost. Passive house compliant across Central Europe.",
"L'équilibre parfait entre performance et coût. Conforme maison passive dans toute l'Europe centrale.",
"Il perfetto equilibrio tra prestazioni e costo. Conforme casa passiva in tutta l'Europa centrale.",
"El equilibrio perfecto entre rendimiento y coste. Conforme casa pasiva en toda Europa Central.",
"De perfecte balans tussen prestatie en kosten. Passiefhuis-conform in heel Midden-Europa.",
"Die perfekte Balance zwischen Leistung und Kosten. Passivhaus-konform in ganz Mitteleuropa.",
)
_add(
"Panouri PBK 250 montate orizontal — straturi EPS-Grafit + fibrociment gata pentru armătură.",
"PBK 250 panels installed horizontally — EPS-Graphite + fibre cement layers ready for reinforcement.",
"Panneaux PBK 250 montés horizontalement — couches EPS-Graphite + fibrociment prêtes pour l'armature.",
"Pannelli PBK 250 montati orizzontalmente — strati EPS-Grafite + fibrocemento pronti per l'armatura.",
"Paneles PBK 250 montados horizontalmente — capas EPS-Grafito + fibrocemento listas para armadura.",
"PBK 250 panelen horizontaal gemonteerd — EPS-Grafiet + vezelcement lagen klaar voor wapening.",
"PBK 250 Paneele horizontal montiert — EPS-Graphit + Faserzement-Schichten bereit für die Bewehrung.",
)
_add(
"În 7 zile: preț per unitate + total ansamblu + tarif volum aplicabil + planificare livrare.",
"Within 7 days: price per unit + development total + applicable volume rate + delivery schedule.",
"Sous 7 jours : prix par unité + total ensemble + tarif volume applicable + planification livraison.",
"Entro 7 giorni: prezzo per unità + totale complesso + tariffa volume applicabile + pianificazione consegna.",
"En 7 días: precio por unidad + total del conjunto + tarifa por volumen aplicable + planificación de entrega.",
"Binnen 7 dagen: prijs per eenheid + totaal complex + toepasselijk volumetarief + leveringsplanning.",
"Innerhalb von 7 Tagen: Preis pro Einheit + Gesamtsumme + anwendbarer Mengentarif + Lieferplanung.",
)
_add(
"(în funcție de finisaje și autorizație). De 2–3 ori mai rapid decât o construcție clasică.",
"(depending on finishes and permit). 2–3 times faster than conventional construction.",
"(selon finitions et autorisation). 2 à 3 fois plus rapide qu'une construction classique.",
"(a seconda di finiture e autorizzazione). 2–3 volte più veloce di una costruzione classica.",
"(según acabados y licencia). 2–3 veces más rápido que una construcción clásica.",
"(afhankelijk van afwerking en vergunning). 2–3 keer sneller dan klassieke bouw.",
"(je nach Ausbaustandard und Genehmigung). 2–3-mal schneller als klassischer Bau.",
)
_add(
"Deschideri maxime, performanță termică maximă. Pentru locuințe deschise și săli generoase.",
"Maximum spans, maximum thermal performance. For open-plan homes and generous spaces.",
"Portées maximales, performance thermique maximale. Pour des logements ouverts et des espaces généreux.",
"Luci massime, prestazione termica massima. Per abitazioni aperte e spazi generosi.",
"Luces máximas, rendimiento térmico máximo. Para viviendas abiertas y espacios generosos.",
"Maximale overspanningen, maximale thermische prestatie. Voor open woningen en royale ruimtes.",
"Maximale Spannweiten, maximale Wärmeleistung. Für offene Wohnungen und großzügige Räume.",
)
_add(
"O singură turnare pentru tot. Montajul ferestrelor cu triplu geam și al ușilor exterioare.",
"One pour for everything. Installation of triple-glazed windows and exterior doors.",
"Un seul coulage pour tout. Pose des fenêtres triple vitrage et des portes extérieures.",
"Un unico getto per tutto. Montaggio di finestre con triplo vetro e porte esterne.",
"Un solo hormigonado para todo. Montaje de ventanas de triple acristalamiento y puertas exteriores.",
"Eén storting voor alles. Montage van ramen met driedubbel glas en buitendeuren.",
"Ein Guss für alles. Montage von Dreifachverglasungsfenstern und Außentüren.",
)
_add(
"exclusiv în tehnologie — pentru a aduce pe piață doar produse premium, de înaltă calitate.",
"exclusively in technology — to bring to market only premium, high-quality products.",
"exclusivement en technologie — pour n'apporter sur le marché que des produits premium, de haute qualité.",
"esclusivamente in tecnologia — per portare sul mercato solo prodotti premium, di alta qualità.",
"exclusivamente en tecnología — para llevar al mercado solo productos premium, de alta calidad.",
"uitsluitend in technologie — om alleen premium producten van hoge kwaliteit op de markt te brengen.",
"ausschließlich in Technologie — um nur Premium-Produkte von höchster Qualität auf den Markt zu bringen.",
)
_add(
"pentru o casă de 150–200 m² (față de 4–5 luni cu cărămida clasică). În total, vă mutați în",
"for a 150–200 m² house (vs 4–5 months with classic brick). In total, you move in",
"pour une maison de 150–200 m² (contre 4–5 mois avec la brique classique). Au total, vous emménagez en",
"per una casa di 150–200 m² (contro 4–5 mesi con il mattone classico). In totale, vi trasferite in",
"para una casa de 150–200 m² (frente a 4–5 meses con ladrillo clásico). En total, se muda en",
"voor een huis van 150–200 m² (vs 4–5 maanden met klassieke baksteen). In totaal verhuist u in",
"für ein Haus mit 150–200 m² (vs. 4–5 Monate mit klassischem Ziegel). Insgesamt ziehen Sie in",
)
_add(
"Și dacă mâine ar apărea un sistem mai bun și mai performant, tot Polistibrick îl va crea —",
"And if tomorrow a better, higher-performing system emerged, Polistibrick would be the one to create it —",
"Et si demain un système meilleur et plus performant apparaissait, ce serait toujours Polistibrick qui le créerait —",
"E se domani emergesse un sistema migliore e più performante, sarebbe sempre Polistibrick a crearlo —",
"Y si mañana surgiera un sistema mejor y más eficiente, sería Polistibrick quien lo crearía —",
"En als morgen een beter, hoger presterend systeem zou verschijnen, zou Polistibrick het zijn die het zou creëren —",
"Und wenn morgen ein besseres, leistungsfähigeres System entstünde, wäre es Polistibrick, das es entwickeln würde —",
)
_add(
"(structură, izolație, etanșare, acustică și finisaje). Marjele operaționale pot ajunge la",
"(structure, insulation, airtightness, acoustics and finishes). Operating margins can reach",
"(structure, isolation, étanchéité, acoustique et finitions). Les marges opérationnelles peuvent atteindre",
"(struttura, isolamento, tenuta, acustica e finiture). I margini operativi possono raggiungere",
"(estructura, aislamiento, estanqueidad, acústica y acabados). Los márgenes operativos pueden alcanzar",
"(structuur, isolatie, luchtdichtheid, akoestiek en afwerking). Operationele marges kunnen oplopen tot",
"(Struktur, Dämmung, Luftdichtheit, Akustik und Ausbau). Die operativen Margen können erreichen",
)
_add(
"Echipa Polistibrick vă răspunde personal. Consultanță la măsură, răspuns garantat în 48h.",
"The Polistibrick team responds to you personally. Tailored advice, guaranteed response within 48h.",
"L'équipe Polistibrick vous répond personnellement. Conseil sur mesure, réponse garantie sous 48h.",
"Il team Polistibrick vi risponde personalmente. Consulenza su misura, risposta garantita entro 48h.",
"El equipo Polistibrick le responde personalmente. Asesoramiento a medida, respuesta garantizada en 48h.",
"Het Polistibrick-team antwoordt u persoonlijk. Advies op maat, gegarandeerd antwoord binnen 48u.",
"Das Polistibrick-Team antwortet Ihnen persönlich. Maßgeschneiderte Beratung, garantierte Antwort innerhalb von 48h.",
)
_add(
"Pentru orice informație privind prelucrarea datelor dumneavoastră personale, consultați",
"For any information regarding the processing of your personal data, please consult",
"Pour toute information concernant le traitement de vos données personnelles, consultez",
"Per qualsiasi informazione sul trattamento dei vostri dati personali, consultate",
"Para cualquier información sobre el tratamiento de sus datos personales, consulte",
"Voor informatie over de verwerking van uw persoonsgegevens, raadpleeg",
"Für Informationen zur Verarbeitung Ihrer personenbezogenen Daten konsultieren Sie",
)
_add(
"Recepție tehnică validată. Test de consum verificat pe loc — sub pragurile Passivhaus.",
"Technical acceptance validated. On-site consumption test verified — below Passivhaus thresholds.",
"Réception technique validée. Test de consommation vérifié sur place — sous les seuils Passivhaus.",
"Collaudo tecnico convalidato. Test di consumo verificato in loco — sotto le soglie Passivhaus.",
"Recepción técnica validada. Prueba de consumo verificada in situ — por debajo de los umbrales Passivhaus.",
"Technische oplevering gevalideerd. Verbruikstest ter plaatse geverifieerd — onder Passivhaus-drempels.",
"Technische Abnahme bestätigt. Verbrauchstest vor Ort verifiziert — unter Passivhaus-Grenzwerten.",
)
_add(
"Suprafața casei → cost construcție, economii pe 25 de ani, comparație cu alte sisteme.",
"House floor area → construction cost, savings over 25 years, comparison with other systems.",
"Surface de la maison → coût de construction, économies sur 25 ans, comparaison avec d'autres systèmes.",
"Superficie della casa → costo di costruzione, risparmi in 25 anni, confronto con altri sistemi.",
"Superficie de la casa → coste de construcción, ahorros en 25 años, comparación con otros sistemas.",
"Woningoppervlakte → bouwkosten, besparingen over 25 jaar, vergelijking met andere systemen.",
"Hausfläche → Baukosten, Ersparnisse über 25 Jahre, Vergleich mit anderen Systemen.",
)
_add(
"Cele 12 case rămase sunt montate. În paralel, modulele 1+2 intră în faza de finisaje.",
"The remaining 12 homes are assembled. In parallel, modules 1+2 enter the finishing phase.",
"Les 12 maisons restantes sont montées. En parallèle, les modules 1+2 entrent en phase de finitions.",
"Le restanti 12 case sono montate. In parallelo, i moduli 1+2 entrano nella fase di finiture.",
"Las 12 casas restantes están montadas. En paralelo, los módulos 1+2 entran en fase de acabados.",
"De overige 12 woningen zijn gemonteerd. Parallel gaan modules 1+2 de afwerkingsfase in.",
"Die verbleibenden 12 Häuser sind montiert. Parallel treten Module 1+2 in die Ausbau-Phase ein.",
)
_add(
"Cofraj-pierdut cu 3 modele (210/270/300). Pereți pasivi A+++ dintr-o singură turnare.",
"Lost formwork with 3 models (210/270/300). A+++ passive walls from a single pour.",
"Coffrage perdu avec 3 modèles (210/270/300). Murs passifs A+++ en un seul coulage.",
"Cassero perduto con 3 modelli (210/270/300). Pareti passive A+++ in un unico getto.",
"Encofrado perdido con 3 modelos (210/270/300). Muros pasivos A+++ en un solo hormigonado.",
"Verloren bekisting met 3 modellen (210/270/300). A+++ passieve muren uit één storting.",
"Verlorene Schalung mit 3 Modellen (210/270/300). A+++ Passivwände aus einem Guss.",
)
_add(
"Program arhitect: formare 1 zi gratuită, lead-uri transmise, co-branding pe proiecte.",
"Architect programme: 1-day free training, leads forwarded, co-branding on projects.",
"Programme architecte : formation 1 jour gratuite, leads transmis, co-branding sur les projets.",
"Programma architetto: formazione 1 giorno gratuita, lead trasmessi, co-branding sui progetti.",
"Programa arquitecto: formación 1 día gratuita, leads transmitidos, co-branding en proyectos.",
"Architectenprogramma: 1 dag gratis training, leads doorgestuurd, co-branding op projecten.",
"Architektenprogramm: 1 Tag kostenlose Schulung, Leads weitergeleitet, Co-Branding bei Projekten.",
)
_add(
"pe structură — sunt furnizate de firma sau constructorul care pune în operă sistemul.",
"for the structure — supplied by the company or builder installing the system.",
"pour la structure — fournis par l'entreprise ou le constructeur qui met en œuvre le système.",
"per la struttura — forniti dall'azienda o dal costruttore che mette in opera il sistema.",
"para la estructura — suministrados por la empresa o el constructor que ejecuta el sistema.",
"voor de structuur — geleverd door het bedrijf of de bouwer die het systeem plaatst.",
"für die Struktur — geliefert vom Unternehmen oder Bauunternehmer, der das System einbaut.",
)
_add(
", societate cu răspundere limitată, înregistrată la Registrul Comerțului sub numărul",
", limited liability company, registered with the Trade Register under number",
", société à responsabilité limitée, enregistrée au Registre du Commerce sous le numéro",
", società a responsabilità limitata, registrata al Registro delle Imprese con il numero",
", sociedad de responsabilidad limitada, inscrita en el Registro Mercantil con el número",
", besloten vennootschap, ingeschreven in het handelsregister onder nummer",
", Gesellschaft mit beschränkter Haftung, eingetragen im Handelsregister unter der Nummer",
)
_add(
"Recenzia ta a fost trimisă. Va fi publicată pe site după validare de echipa noastră.",
"Your review has been submitted. It will be published on the site after validation by our team.",
"Votre avis a été envoyé. Il sera publié sur le site après validation par notre équipe.",
"La tua recensione è stata inviata. Sarà pubblicata sul sito dopo la validazione del nostro team.",
"Tu reseña ha sido enviada. Se publicará en el sitio tras la validación de nuestro equipo.",
"Uw review is verzonden. Deze wordt op de site gepubliceerd na validatie door ons team.",
"Ihre Bewertung wurde eingereicht. Sie wird nach Prüfung durch unser Team auf der Website veröffentlicht.",
)
_add(
"— interes legitim sau consimțământ acolo unde este necesar (art. 6.1.f / 6.1.a). (3)",
"— legitimate interest or consent where required (Art. 6.1.f / 6.1.a). (3)",
"— intérêt légitime ou consentement lorsque nécessaire (art. 6.1.f / 6.1.a). (3)",
"— interesse legittimo o consenso ove necessario (art. 6.1.f / 6.1.a). (3)",
"— interés legítimo o consentimiento cuando sea necesario (art. 6.1.f / 6.1.a). (3)",
"— gerechtvaardigd belang of toestemming waar nodig (art. 6.1.f / 6.1.a). (3)",
"— berechtigtes Interesse oder Einwilligung, wo erforderlich (Art. 6.1.f / 6.1.a). (3)",
)
_add(
"Cofraj-pierdut cu 3 modele predefinite. Pereți pasivi A+++ dintr-o singură turnare.",
"Lost formwork with 3 predefined models. A+++ passive walls from a single pour.",
"Coffrage perdu avec 3 modèles prédéfinis. Murs passifs A+++ en un seul coulage.",
"Cassero perduto con 3 modelli predefiniti. Pareti passive A+++ in un unico getto.",
"Encofrado perdido con 3 modelos predefinidos. Muros pasivos A+++ en un solo hormigonado.",
"Verloren bekisting met 3 vooraf gedefinieerde modellen. A+++ passieve muren uit één storting.",
"Verlorene Schalung mit 3 vordefinierten Modellen. A+++ Passivwände aus einem Guss.",
)
_add(
"Cofrajul termoizolant care se ridică manual. Izolație integrată, gata pentru beton.",
"Insulating formwork raised by hand. Integrated insulation, ready for concrete.",
"Le coffrage isolant qui se monte à la main. Isolation intégrée, prêt pour le béton.",
"Il cassero isolante che si monta a mano. Isolamento integrato, pronto per il calcestruzzo.",
"El encofrado aislante que se monta a mano. Aislamiento integrado, listo para hormigón.",
"De isolerende bekisting die handmatig wordt opgebouwd. Geïntegreerde isolatie, klaar voor beton.",
"Die wärmedämmende Schalung, die von Hand aufgebaut wird. Integrierte Dämmung, bereit für Beton.",
)
_add(
"Săpătură, fundație continuă, placă de fundație pentru parter. Echipă locală 4 zile.",
"Excavation, continuous foundation, ground-floor slab. Local crew, 4 days.",
"Terrassement, fondation continue, dalle de fondation pour le rez-de-chaussée. Équipe locale, 4 jours.",
"Scavo, fondazione continua, platea di fondazione per il piano terra. Squadra locale, 4 giorni.",
"Excavación, cimentación continua, losa de cimentación para planta baja. Equipo local, 4 días.",
"Graafwerk, doorlopende fundering, funderingsplaat voor begane grond. Lokaal team, 4 dagen.",
"Aushub, Streifenfundament, Bodenplatte für Erdgeschoss. Lokales Team, 4 Tage.",
)
_add(
"TBK este sistemul de acoperiș cu cea mai înaltă performanță termică din clasa lui —",
"TBK is the roof system with the highest thermal performance in its class —",
"TBK est le système de toiture avec la plus haute performance thermique de sa catégorie —",
"TBK è il sistema di copertura con la più alta prestazione termica della sua categoria —",
"TBK es el sistema de cubierta con el mayor rendimiento térmico de su clase —",
"TBK is het dak systeem met de hoogste thermische prestatie in zijn klasse —",
"TBK ist das Dachsystem mit der höchsten Wärmeleistung seiner Klasse —",
)
_add(
"Tot ce ai nevoie ca arhitect, constructor sau client. Disponibil în RO, EN, FR, ES.",
"Everything you need as an architect, builder or client. Available in RO, EN, FR, ES.",
"Tout ce dont vous avez besoin en tant qu'architecte, constructeur ou client. Disponible en RO, EN, FR, ES.",
"Tutto ciò di cui hai bisogno come architetto, costruttore o cliente. Disponibile in RO, EN, FR, ES.",
"Todo lo que necesitas como arquitecto, constructor o cliente. Disponible en RO, EN, FR, ES.",
"Alles wat u nodig heeft als architect, bouwer of klant. Beschikbaar in RO, EN, FR, ES.",
"Alles, was Sie als Architekt, Bauunternehmer oder Kunde brauchen. Verfügbar in RO, EN, FR, ES.",
)
_add(
"Următorii furnizori pot plasa sau primi date în funcție de navigarea dumneavoastră:",
"The following providers may place or receive data depending on your browsing:",
"Les fournisseurs suivants peuvent placer ou recevoir des données selon votre navigation :",
"I seguenti fornitori possono inserire o ricevere dati in base alla vostra navigazione:",
"Los siguientes proveedores pueden colocar o recibir datos según su navegación:",
"De volgende leveranciers kunnen gegevens plaatsen of ontvangen afhankelijk van uw browsen:",
"Die folgenden Anbieter können je nach Ihrer Navigation Daten platzieren oder empfangen:",
)
_add(
"— transmitere securizată a mesajelor din formulare către căsuțele noastre de email.",
"— secure transmission of form messages to our email inboxes.",
"— transmission sécurisée des messages des formulaires vers nos boîtes email.",
"— trasmissione sicura dei messaggi dei moduli alle nostre caselle email.",
"— transmisión segura de los mensajes de los formularios a nuestras bandejas de correo.",
"— beveiligde overdracht van formulierberichten naar onze e-mailboxen.",
"— sichere Übermittlung von Formularnachrichten an unsere E-Mail-Postfächer.",
)
_add(
"Formare practică la calepinaj, etajare și turnare cu formatorii noștri de șantier.",
"Hands-on training in layout, storey planning and pouring with our site trainers.",
"Formation pratique au calepinage, à l'étage et au coulage avec nos formateurs de chantier.",
"Formazione pratica su calepinatura, pianificazione dei piani e getto con i nostri formatori di cantiere.",
"Formación práctica en replanteo, plantas y hormigonado con nuestros formadores de obra.",
"Praktische training in uitzetten, verdiepingsplanning en storten met onze werftrainers.",
"Praxisschulung in Rissplanung, Geschossplanung und Betonierung mit unseren Baustellen-Trainern.",
)
_add(
"Pentru investitori și dezvoltatori · Polistibrick — Ansambluri rezidențiale pasive",
"For investors and developers · Polistibrick — Passive residential developments",
"Pour investisseurs et promoteurs · Polistibrick — Ensembles résidentiels passifs",
"Per investitori e sviluppatori · Polistibrick — Complessi residenziali passivi",
"Para inversores y promotores · Polistibrick — Conjuntos residenciales pasivos",
"Voor investeerders en ontwikkelaars · Polistibrick — Passieve wooncomplexen",
"Für Investoren und Bauträger · Polistibrick — Passive Wohnanlagen",
)
_add(
"Răspuns tehnic în 24h. Punți termice, calcule U-value, îmbinări complexe. Gratuit.",
"Technical response within 24h. Thermal bridges, U-value calculations, complex junctions. Free.",
"Réponse technique sous 24h. Ponts thermiques, calculs U-value, jonctions complexes. Gratuit.",
"Risposta tecnica entro 24h. Ponti termici, calcoli U-value, giunzioni complesse. Gratuito.",
"Respuesta técnica en 24h. Puentes térmicos, cálculos U-value, uniones complejas. Gratuito.",
"Technisch antwoord binnen 24u. Koudbruggen, U-value berekeningen, complexe aansluitingen. Gratis.",
"Technische Antwort innerhalb von 24h. Wärmebrücken, U-Wert-Berechnungen, komplexe Anschlüsse. Kostenlos.",
)
_add(
"Semnare contract ansamblu: prețuri fixate, calendar garantat, condiții plată, SLA.",
"Development contract signing: fixed prices, guaranteed timeline, payment terms, SLA.",
"Signature contrat ensemble : prix fixés, calendrier garanti, conditions de paiement, SLA.",
"Firma contratto complesso: prezzi fissati, calendario garantito, condizioni di pagamento, SLA.",
"Firma de contrato del conjunto: precios fijados, calendario garantizado, condiciones de pago, SLA.",
"Ondertekening complexcontract: vaste prijzen, gegarandeerde planning, betalingsvoorwaarden, SLA.",
"Vertragsunterzeichnung Anlage: Festpreise, garantierter Zeitplan, Zahlungsbedingungen, SLA.",
)
_add(
"Tencuieli, vopsea, parchet, mobilier de bucătărie. Tencuială silicatică pe fațadă.",
"Plaster, paint, parquet, kitchen furniture. Silicate render on the facade.",
"Enduits, peinture, parquet, mobilier de cuisine. Enduit silicaté en façade.",
"Intonaci, vernice, parquet, arredamento cucina. Intonaco silicatico in facciata.",
"Enlucidos, pintura, parquet, mobiliario de cocina. Enlucido silicático en fachada.",
"Stucwerk, verf, parket, keukenmeubilair. Silicaatpleister op de gevel.",
"Putz, Farbe, Parkett, Küchenmöbel. Silikatputz an der Fassade.",
)
_add(
"brevetul european le-a oferit garanția unui sistem unic, nu a unui produs de masă.",
"the European patent gave them the assurance of a unique system, not a mass-market product.",
"le brevet européen leur a offert l'assurance d'un système unique, pas d'un produit de masse.",
"il brevetto europeo ha offerto loro la garanzia di un sistema unico, non di un prodotto di massa.",
"la patente europea les ofreció la garantía de un sistema único, no de un producto de masas.",
"het Europese octrooi bood hen de zekerheid van een uniek systeem, geen massaproduct.",
"das europäische Patent gab ihnen die Gewissheit eines einzigartigen Systems, keines Massenprodukts.",
)
_add(
"— trimitere formulare (fără cookie de marketing; prelucrarea datelor din formular)",
"— form submission (no marketing cookie; form data processing)",
"— envoi de formulaires (sans cookie marketing ; traitement des données du formulaire)",
"— invio moduli (senza cookie di marketing; trattamento dati del modulo)",
"— envío de formularios (sin cookie de marketing; tratamiento de datos del formulario)",
"— formulierverzending (geen marketingcookie; verwerking van formuliergegevens)",
"— Formularübermittlung (ohne Marketing-Cookie; Verarbeitung der Formulardaten)",
)
_add(
": Blocuri • Mortar • Cofraj • Fier • Beton • Izolație • Placare • Șuruburi • etc.",
": Blocks • Mortar • Formwork • Rebar • Concrete • Insulation • Cladding • Screws • etc.",
": Blocs • Mortier • Coffrage • Acier • Béton • Isolation • Bardage • Vis • etc.",
": Blocchi • Malta • Cassero • Ferro • Calcestruzzo • Isolamento • Rivestimento • Viti • ecc.",
": Bloques • Mortero • Encofrado • Acero • Hormigón • Aislamiento • Revestimiento • Tornillos • etc.",
": Blokken • Mortel • Bekisting • Wapening • Beton • Isolatie • Bekleding • Schroeven • etc.",
": Blöcke • Mörtel • Schalung • Bewehrung • Beton • Dämmung • Verkleidung • Schrauben • usw.",
)
_add(
"Calculator ROI Excel, studiu de caz ansamblu, grilă tarife volum. Răspuns în 24h.",
"ROI Excel calculator, development case study, volume pricing grid. Response within 24h.",
"Calculateur ROI Excel, étude de cas ensemble, grille tarifs volume. Réponse sous 24h.",
"Calcolatore ROI Excel, caso studio complesso, griglia tariffe volume. Risposta entro 24h.",
"Calculadora ROI Excel, estudio de caso del conjunto, tabla de tarifas por volumen. Respuesta en 24h.",
"ROI Excel-calculator, casestudy complex, volumetarievenraster. Antwoord binnen 24u.",
"ROI-Excel-Rechner, Anlagen-Fallstudie, Mengenpreisraster. Antwort innerhalb von 24h.",
)
_add(
"Completați formularul rapid de partener. Serviciul tehnic validează competențele.",
"Complete the quick partner form. Our technical team validates your qualifications.",
"Remplissez le formulaire partenaire rapide. Le service technique valide vos compétences.",
"Compilate il modulo partner rapido. Il servizio tecnico convalida le vostre competenze.",
"Complete el formulario rápido de socio. El servicio técnico valida sus competencias.",
"Vul het snelle partnerformulier in. Onze technische dienst valideert uw competenties.",
"Füllen Sie das kurze Partnerformular aus. Unser technischer Service prüft Ihre Qualifikationen.",
)
_add(
"Partener certificat · Bâti-Innov SAS · Auvergne-Rhône-Alpes · 12 proiecte livrate",
"Certified partner · Bâti-Innov SAS · Auvergne-Rhône-Alpes · 12 projects delivered",
"Partenaire certifié · Bâti-Innov SAS · Auvergne-Rhône-Alpes · 12 projets livrés",
"Partner certificato · Bâti-Innov SAS · Auvergne-Rhône-Alpes · 12 progetti consegnati",
"Socio certificado · Bâti-Innov SAS · Auvergne-Rhône-Alpes · 12 proyectos entregados",
"Gecertificeerde partner · Bâti-Innov SAS · Auvergne-Rhône-Alpes · 12 projecten geleverd",
"Zertifizierter Partner · Bâti-Innov SAS · Auvergne-Rhône-Alpes · 12 Projekte geliefert",
)
_add(
"Pentru arhitecți și birouri de proiectare · Polistibrick — Sistem ICF beton armat",
"For architects and design offices · Polistibrick — Reinforced concrete ICF system",
"Pour architectes et bureaux d'études · Polistibrick — Système ICF béton armé",
"Per architetti e studi di progettazione · Polistibrick — Sistema ICF calcestruzzo armato",
"Para arquitectos y despachos de diseño · Polistibrick — Sistema ICF hormigón armado",
"Voor architecten en ontwerpbureaus · Polistibrick — Gewapend beton ICF-systeem",
"Für Architekten und Planungsbüros · Polistibrick — Stahlbeton-ICF-System",
)
_add(
"— detectarea țării din adresa IP (numai dacă acceptați cookie-urile neesențiale).",
"— country detection from IP address (only if you accept non-essential cookies).",
"— détection du pays à partir de l'adresse IP (uniquement si vous acceptez les cookies non essentiels).",
"— rilevamento del paese dall'indirizzo IP (solo se accettate i cookie non essenziali).",
"— detección del país desde la dirección IP (solo si acepta las cookies no esenciales).",
"— landdetectie via IP-adres (alleen als u niet-essentiële cookies accepteert).",
"— Ländererkennung über die IP-Adresse (nur wenn Sie nicht notwendige Cookies akzeptieren).",
)
_add(
"Apel telefonic de 30 min cu șeful de proiect ansamblu. Studiu de preț în 7 zile.",
"30-minute call with the development project manager. Price study within 7 days.",
"Appel téléphonique de 30 min avec le chef de projet ensemble. Étude de prix sous 7 jours.",
"Chiamata di 30 min con il capo progetto del complesso. Studio prezzi entro 7 giorni.",
"Llamada de 30 min con el jefe de proyecto del conjunto. Estudio de precios en 7 días.",
"Telefoongesprek van 30 min met de projectleider van het complex. Prijsstudie binnen 7 dagen.",
"30-minütiges Gespräch mit dem Projektleiter der Anlage. Preisstudie innerhalb von 7 Tagen.",
)
_add(
"Excavație, fundație. Teren stabil — nu a fost necesară stabilizare suplimentară.",
"Excavation, foundation. Stable ground — no additional stabilisation required.",
"Terrassement, fondation. Terrain stable — aucune stabilisation supplémentaire nécessaire.",
"Scavo, fondazione. Terreno stabile — non è stata necessaria stabilizzazione aggiuntiva.",
"Excavación, cimentación. Terreno estable — no fue necesaria estabilización adicional.",
"Graafwerk, fundering. Stabiele grond — geen extra stabilisatie nodig.",
"Aushub, Fundament. Stabiler Boden — keine zusätzliche Stabilisierung erforderlich.",
)
_add(
"Plăcile portante EPS-Graphite + fibrociment, montate orizontal și armate pe loc.",
"Load-bearing EPS-Graphite + fibre cement slabs, installed horizontally and reinforced on site.",
"Dalles portantes EPS-Graphite + fibrociment, montées horizontalement et armées sur place.",
"Lastre portanti EPS-Grafite + fibrocemento, montate orizzontalmente e armate in loco.",
"Losas portantes EPS-Grafito + fibrocemento, montadas horizontalmente y armadas in situ.",
"Dragende EPS-Grafiet + vezelcement platen, horizontaal gemonteerd en ter plaatse gewapend.",
"Tragende EPS-Graphit + Faserzement-Platten, horizontal montiert und vor Ort bewehrt.",
)
_add(
"Scrieți-ne — echipa Polistibrick din țara în care construiți vă răspunde direct.",
"Write to us — the Polistibrick team in the country where you are building responds directly.",
"Écrivez-nous — l'équipe Polistibrick du pays où vous construisez vous répond directement.",
"Scriveteci — il team Polistibrick del paese in cui costruite vi risponde direttamente.",
"Escríbanos — el equipo Polistibrick del país donde construye le responde directamente.",
"Schrijf ons — het Polistibrick-team in het land waar u bouwt antwoordt u rechtstreeks.",
"Schreiben Sie uns — das Polistibrick-Team im Land, in dem Sie bauen, antwortet Ihnen direkt.",
)
_add(
"Și o face mai rapid, cu o echipă mai mică și marje superioare sistemului clasic.",
"And it does so faster, with a smaller team and higher margins than the classic system.",
"Et le fait plus rapidement, avec une équipe plus réduite et des marges supérieures au système classique.",
"E lo fa più rapidamente, con una squadra più piccola e margini superiori al sistema classico.",
"Y lo hace más rápido, con un equipo más pequeño y márgenes superiores al sistema clásico.",
"En dat sneller, met een kleiner team en hogere marges dan het klassieke systeem.",
"Und das schneller, mit einem kleineren Team und höheren Margen als das klassische System.",
)
_add(
"Structură în 4–6 săptămâni vs 4–5 luni cu cărămida. Vă mutați de 3× mai repede.",
"Structure in 4–6 weeks vs 4–5 months with brick. You move in 3× faster.",
"Structure en 4–6 semaines vs 4–5 mois avec la brique. Vous emménagez 3× plus vite.",
"Struttura in 4–6 settimane vs 4–5 mesi con il mattone. Vi trasferite 3× più velocemente.",
"Estructura en 4–6 semanas vs 4–5 meses con ladrillo. Se muda 3× más rápido.",
"Structuur in 4–6 weken vs 4–5 maanden met baksteen. U verhuist 3× sneller.",
"Struktur in 4–6 Wochen vs. 4–5 Monate mit Ziegel. Sie ziehen 3× schneller ein.",
)
_add(
"Testimoniale · Proprietarii Polistibrick vorbesc — facturi reale, povești reale",
"Testimonials · Polistibrick homeowners speak — real bills, real stories",
"Témoignages · Les propriétaires Polistibrick parlent — factures réelles, histoires réelles",
"Testimonianze · I proprietari Polistibrick raccontano — bollette reali, storie reali",
"Testimonios · Los propietarios Polistibrick hablan — facturas reales, historias reales",
"Getuigenissen · Polistibrick-huiseigenaren vertellen — echte rekeningen, echte verhalen",
"Erfahrungsberichte · Polistibrick-Hausbesitzer berichten — echte Rechnungen, echte Geschichten",
)
_add(
"— ideal pentru arhitectura contemporană (acoperișuri plate, volume în consolă).",
"— ideal for contemporary architecture (flat roofs, cantilevered volumes).",
"— idéal pour l'architecture contemporaine (toitures plates, volumes en porte-à-faux).",
"— ideale per l'architettura contemporanea (tetti piani, volumi a sbalzo).",
"— ideal para arquitectura contemporánea (cubiertas planas, volúmenes en voladizo).",
"— ideaal voor hedendaagse architectuur (platte daken, uitkragende volumes).",
"— ideal für zeitgenössische Architektur (Flachdächer, auskragende Volumen).",
)
_add(
"Altele nu rezistă turnărilor în înălțime și impun turnarea în mai multe etape.",
"Others cannot withstand tall pours and require multi-stage casting.",
"D'autres ne résistent pas aux coulages en hauteur et imposent un coulage en plusieurs étapes.",
"Altri non resistono ai getti in altezza e impongono il getto in più fasi.",
"Otros no resisten los hormigonados en altura e imponen el hormigonado en varias fases.",
"Anderen weerstaan geen hoge stortingen en vereisen storten in meerdere fasen.",
"Andere halten hohen Betonierungen nicht stand und erfordern mehrstufiges Betonieren.",
)
_add(
"Blower Door pe fiecare unitate. Toate obțin certificarea Passivhaus din prima.",
"Blower Door test on every unit. All achieve Passivhaus certification on the first attempt.",
"Test Blower Door sur chaque unité. Toutes obtiennent la certification Passivhaus du premier coup.",
"Test Blower Door su ogni unità. Tutte ottengono la certificazione Passivhaus al primo tentativo.",
"Prueba Blower Door en cada unidad. Todas obtienen la certificación Passivhaus a la primera.",
"Blower Door-test op elke eenheid. Alle behalen Passivhaus-certificering in één keer.",
"Blower-Door-Test bei jeder Einheit. Alle erhalten die Passivhaus-Zertifizierung beim ersten Mal.",
)
_add(
"Fără macara. Fără structură interminabilă. Sistemul Polistibrick se asamblează",
"No crane. No endless structure. The Polistibrick system assembles",
"Sans grue. Sans structure interminable. Le système Polistibrick s'assemble",
"Senza gru. Senza struttura interminabile. Il sistema Polistibrick si assembla",
"Sin grúa. Sin estructura interminable. El sistema Polistibrick se ensambla",
"Zonder kraan. Zonder eindeloze structuur. Het Polistibrick-systeem wordt gemonteerd",
"Ohne Kran. Ohne endlose Struktur. Das Polistibrick-System lässt sich montieren",
)
_add(
"Pentru climă temperată. Conformitate casă pasivă în zonele sudice ale Europei.",
"For temperate climate. Passive house compliant in southern European regions.",
"Pour climat tempéré. Conforme maison passive dans les régions sud de l'Europe.",
"Per clima temperato. Conforme casa passiva nelle zone meridionali d'Europa.",
"Para clima templado. Conforme casa pasiva en las zonas meridionales de Europa.",
"Voor gematigd klimaat. Passiefhuis-conform in de zuidelijke regio's van Europa.",
"Für gemäßigtes Klima. Passivhaus-konform in den südlichen Regionen Europas.",
)
_add(
"pentru a afla ce trackere sunt utilizate și pentru a vă gestiona preferințele.",
"to find out which trackers are used and to manage your preferences.",
"pour savoir quels traceurs sont utilisés et pour gérer vos préférences.",
"per scoprire quali tracker sono utilizzati e per gestire le vostre preferenze.",
"para saber qué rastreadores se utilizan y para gestionar sus preferencias.",
"om te zien welke trackers worden gebruikt en om uw voorkeuren te beheren.",
"um zu erfahren, welche Tracker verwendet werden, und um Ihre Einstellungen zu verwalten.",
)
_add(
"Polistibrick este alternativa modernă. Un sistem care produce o locuință care",
"Polistibrick is the modern alternative. A system that produces a home that",
"Polistibrick est l'alternative moderne. Un système qui produit un logement qui",
"Polistibrick è l'alternativa moderna. Un sistema che produce un'abitazione che",
"Polistibrick es la alternativa moderna. Un sistema que produce una vivienda que",
"Polistibrick is het moderne alternatief. Een systeem dat een woning produceert die",
"Polistibrick ist die moderne Alternative. Ein System, das ein Zuhause schafft, das",
)
_add(
". BOM calculat de Polistibrick = fără surprize la cantități. Termene livrare",
". BOM calculated by Polistibrick = no quantity surprises. Delivery deadlines",
". BOM calculé par Polistibrick = pas de surprise sur les quantités. Délais de livraison",
". BOM calcolato da Polistibrick = nessuna sorpresa sulle quantità. Termini di consegna",
". BOM calculado por Polistibrick = sin sorpresas en cantidades. Plazos de entrega",
". BOM berekend door Polistibrick = geen verrassingen bij hoeveelheden. Leveringstermijnen",
". Von Polistibrick berechnete Stückliste = keine Mengenüberraschungen. Lieferfristen",
)
_add(
". Am doar fierul, betonul și cofrajul Polistibrick — e sigur și fără erori.",
". I only have the rebar, concrete and Polistibrick formwork — it's safe and error-free.",
". Je n'ai que l'acier, le béton et le coffrage Polistibrick — c'est sûr et sans erreur.",
". Ho solo il ferro, il calcestruzzo e il cassero Polistibrick — è sicuro e senza errori.",
". Solo tengo el acero, el hormigón y el encofrado Polistibrick — es seguro y sin errores.",
". Ik heb alleen de wapening, het beton en de Polistibrick-bekisting — het is veilig en foutloos.",
". Ich habe nur die Bewehrung, den Beton und die Polistibrick-Schalung — es ist sicher und fehlerfrei.",
)
_add(
"Configurator AI gratuit — ofertă estimativă în câteva minute, PDF pe email.",
"Free AI configurator — estimated quote in minutes, PDF by email.",
"Configurateur IA gratuit — devis estimatif en quelques minutes, PDF par email.",
"Configuratore AI gratuito — preventivo stimato in pochi minuti, PDF via email.",
"Configurador IA gratuito — presupuesto estimado en minutos, PDF por email.",
"Gratis AI-configurator — raming binnen enkele minuten, PDF per e-mail.",
"Kostenloser KI-Konfigurator — Kostenvoranschlag in wenigen Minuten, PDF per E-Mail.",
)
_add(
"Dacă biroul de proiectare tehnică întâmpină întrebări, luăm contact cu ei —",
"If the technical design office has questions, we contact them —",
"Si le bureau d'études techniques a des questions, nous les contactons —",
"Se lo studio di progettazione tecnica ha domande, li contattiamo —",
"Si la oficina de diseño técnico tiene preguntas, nos ponemos en contacto con ellos —",
"Als het technisch ontwerpbureau vragen heeft, nemen wij contact met hen op —",
"Wenn das technische Planungsbüro Fragen hat, nehmen wir Kontakt mit ihnen auf —",
)
_add(
"Panouri fabricate conform planificării. Livrare direct pe șantier, pe faze.",
"Panels manufactured to schedule. Direct delivery to site, in phases.",
"Panneaux fabriqués selon la planification. Livraison directe sur chantier, par phases.",
"Pannelli fabbricati secondo la pianificazione. Consegna diretta in cantiere, a fasi.",
"Paneles fabricados según la planificación. Entrega directa a obra, por fases.",
"Panelen gefabriceerd volgens planning. Rechtstreekse levering op de werf, in fasen.",
"Paneele nach Plan gefertigt. Direktlieferung auf die Baustelle, in Phasen.",
)
_add(
"Rezultatul se actualizează în timp real pe măsură ce completezi formularul.",
"The result updates in real time as you complete the form.",
"Le résultat se met à jour en temps réel au fur et à mesure que vous remplissez le formulaire.",
"Il risultato si aggiorna in tempo reale man mano che compili il modulo.",
"El resultado se actualiza en tiempo real a medida que completa el formulario.",
"Het resultaat wordt in realtime bijgewerkt terwijl u het formulier invult.",
"Das Ergebnis aktualisiert sich in Echtzeit, während Sie das Formular ausfüllen.",
)
_add(
"Săpătură și fundații pentru cele 24 de unități. Echipă locală, 4 săptămâni.",
"Excavation and foundations for all 24 units. Local crew, 4 weeks.",
"Terrassement et fondations pour les 24 unités. Équipe locale, 4 semaines.",
"Scavo e fondazioni per le 24 unità. Squadra locale, 4 settimane.",
"Excavación y cimentaciones para las 24 unidades. Equipo local, 4 semanas.",
"Graafwerk en funderingen voor alle 24 eenheden. Lokaal team, 4 weken.",
"Aushub und Fundamente für alle 24 Einheiten. Lokales Team, 4 Wochen.",
)
_add(
"Șef de proiect prezent până la livrarea ultimei unități. Raport săptămânal.",
"Project manager on site until the last unit is delivered. Weekly report.",
"Chef de projet présent jusqu'à la livraison de la dernière unité. Rapport hebdomadaire.",
"Capo progetto presente fino alla consegna dell'ultima unità. Report settimanale.",
"Jefe de proyecto presente hasta la entrega de la última unidad. Informe semanal.",
"Projectleider aanwezig tot levering van de laatste eenheid. Wekelijks rapport.",
"Projektleiter vor Ort bis zur Lieferung der letzten Einheit. Wöchentlicher Bericht.",
)
_add(
"Calculul include atât încălzirea (iarnă), cât și aerul condiționat (vară).",
"The calculation includes both heating (winter) and air conditioning (summer).",
"Le calcul inclut à la fois le chauffage (hiver) et la climatisation (été).",
"Il calcolo include sia il riscaldamento (inverno) che l'aria condizionata (estate).",
"El cálculo incluye tanto la calefacción (invierno) como el aire acondicionado (verano).",
"De berekening omvat zowel verwarming (winter) als airconditioning (zomer).",
"Die Berechnung umfasst sowohl Heizung (Winter) als auch Klimaanlage (Sommer).",
)
_add(
"Cu cele 2 fabrici de producție, expediem structura completă a unei case în",
"With our 2 production plants, we ship the complete structure of a house in",
"Avec nos 2 usines de production, nous expédions la structure complète d'une maison en",
"Con le nostre 2 fabbriche di produzione, spediamo la struttura completa di una casa in",
"Con nuestras 2 fábricas de producción, enviamos la estructura completa de una casa en",
"Met onze 2 productiefabrieken verzenden we de complete structuur van een huis in",
"Mit unseren 2 Produktionswerken versenden wir die komplette Struktur eines Hauses in",
)
_add(
"Test Blower Door (n50 = 0,48 — sub limita Passivhaus). Recepție și mutare.",
"Blower Door test (n50 = 0.48 — below Passivhaus limit). Acceptance and move-in.",
"Test Blower Door (n50 = 0,48 — sous la limite Passivhaus). Réception et emménagement.",
"Test Blower Door (n50 = 0,48 — sotto il limite Passivhaus). Collaudo e trasloco.",
"Prueba Blower Door (n50 = 0,48 — por debajo del límite Passivhaus). Recepción y mudanza.",
"Blower Door-test (n50 = 0,48 — onder Passivhaus-limiet). Oplevering en verhuizing.",
"Blower-Door-Test (n50 = 0,48 — unter Passivhaus-Grenzwert). Abnahme und Einzug.",
)
_add(
". Am doar fierul, betonul și cofrajul Polistibrick — sigur și fără erori.",
". I only have the rebar, concrete and Polistibrick formwork — safe and error-free.",
". Je n'ai que l'acier, le béton et le coffrage Polistibrick — sûr et sans erreur.",
". Ho solo il ferro, il calcestruzzo e il cassero Polistibrick — sicuro e senza errori.",
". Solo tengo el acero, el hormigón y el encofrado Polistibrick — seguro y sin errores.",
". Ik heb alleen de wapening, het beton en de Polistibrick-bekisting — veilig en foutloos.",
". Ich habe nur die Bewehrung, den Beton und die Polistibrick-Schalung — sicher und fehlerfrei.",
)
_add(
"Am identificat, unul câte unul, limitele fiecărui sistem ICF de pe piață.",
"We identified, one by one, the limits of every ICF system on the market.",
"Nous avons identifié, un par un, les limites de chaque système ICF du marché.",
"Abbiamo identificato, uno per uno, i limiti di ogni sistema ICF sul mercato.",
"Hemos identificado, uno a uno, los límites de cada sistema ICF del mercado.",
"We hebben, één voor één, de grenzen van elk ICF-systeem op de markt geïdentificeerd.",
"Wir haben, eines nach dem anderen, die Grenzen jedes ICF-Systems auf dem Markt identifiziert.",
)
_add(
"Puneți-ne în legătură cu arhitectul care vă proiectează casa. Îi furnizăm",
"Put us in touch with the architect designing your home. We provide them with",
"Mettez-nous en contact avec l'architecte qui conçoit votre maison. Nous lui fournissons",
"Metteteci in contatto con l'architetto che progetta la vostra casa. Gli forniamo",
"Pónganos en contacto con el arquitecto que diseña su casa. Le proporcionamos",
"Breng ons in contact met de architect die uw huis ontwerpt. Wij leveren hem",
"Stellen Sie uns dem Architekten vor, der Ihr Haus plant. Wir stellen ihm",
)
_add(
"Altele nu acceptă armătura din fier-beton — o limită structurală majoră.",
"Others do not accept reinforcing steel — a major structural limitation.",
"D'autres n'acceptent pas l'armature en acier — une limitation structurelle majeure.",
"Altri non accettano l'armatura in ferro — un limite strutturale importante.",
"Otros no aceptan la armadura de acero — una limitación estructural importante.",
"Anderen accepteren geen wapeningsstaal — een belangrijke structurele beperking.",
"Andere akzeptieren keine Bewehrungsstahl — eine wesentliche strukturelle Einschränkung.",
)
_add(
"Devino partener Polistibrick · Constructor certificat în 9 țări europene",
"Become a Polistibrick partner · Certified builder in 9 European countries",
"Devenez partenaire Polistibrick · Constructeur certifié dans 9 pays européens",
"Diventa partner Polistibrick · Costruttore certificato in 9 paesi europei",
"Hazte socio Polistibrick · Constructor certificado en 9 países europeos",
"Word Polistibrick-partner · Gecertificeerde bouwer in 9 Europese landen",
"Partner werden bei Polistibrick · Zertifizierter Bauunternehmer in 9 europäischen Ländern",
)
_add(
"Foc, hidrofug, etanșeitate la aer, izolație pasivă, fonoizolație, fixare",
"Fire resistance, waterproofing, airtightness, passive insulation, sound insulation, fixing",
"Feu, hydrofuge, étanchéité à l'air, isolation passive, phonique, fixation",
"Fuoco, impermeabile, tenuta all'aria, isolamento passivo, fonoisolazione, fissaggio",
"Fuego, impermeable, estanqueidad al aire, aislamiento pasivo, fonoaislamiento, fijación",
"Brand, waterdicht, luchtdichtheid, passieve isolatie, geluidsisolatie, bevestiging",
"Feuer, wasserdicht, Luftdichtheit, Passivdämmung, Schalldämmung, Befestigung",
)
_add(
"Folosește media pentru țara ta (RO ~0,18, FR ~0,25, DE ~0,32, ES ~0,20).",
"Use the average for your country (RO ~0.18, FR ~0.25, DE ~0.32, ES ~0.20).",
"Utilisez la moyenne pour votre pays (RO ~0,18, FR ~0,25, DE ~0,32, ES ~0,20).",
"Usa la media per il tuo paese (RO ~0,18, FR ~0,25, DE ~0,32, ES ~0,20).",
"Usa la media de tu país (RO ~0,18, FR ~0,25, DE ~0,32, ES ~0,20).",
"Gebruik het gemiddelde voor uw land (RO ~0,18, FR ~0,25, DE ~0,32, ES ~0,20).",
"Verwenden Sie den Durchschnitt für Ihr Land (RO ~0,18, FR ~0,25, DE ~0,32, ES ~0,20).",
)
_add(
"Sistem Passivhaus din fabrică. Deschideri de 9 m, U=0,13, doar 22 kg/m².",
"Passivhaus system from the factory. 9 m spans, U=0.13, only 22 kg/m².",
"Système Passivhaus d'usine. Portées de 9 m, U=0,13, seulement 22 kg/m².",
"Sistema Passivhaus di fabbrica. Luci di 9 m, U=0,13, solo 22 kg/m².",
"Sistema Passivhaus de fábrica. Luces de 9 m, U=0,13, solo 22 kg/m².",
"Passivhaus-systeem uit de fabriek. Overspanningen van 9 m, U=0,13, slechts 22 kg/m².",
"Passivhaus-System ab Werk. Spannweiten von 9 m, U=0,13, nur 22 kg/m².",
)
_add(
"pentru a te alătura rețelei, a fi format și a primi șantiere în zona ta.",
"to join the network, get trained and receive projects in your area.",
"pour rejoindre le réseau, être formé et recevoir des chantiers dans votre région.",
"per unirti alla rete, essere formato e ricevere cantieri nella tua zona.",
"para unirte a la red, formarte y recibir obras en tu zona.",
"om u aan te sluiten bij het netwerk, opgeleid te worden en projecten in uw regio te ontvangen.",
"um dem Netzwerk beizutreten, geschult zu werden und Baustellen in Ihrer Region zu erhalten.",
)
_add(
"Începeți lucrările liniștit, cu prezența inginerului nostru de aplicare.",
"Start your build with confidence, with our application engineer on site.",
"Commencez les travaux en toute sérénité, avec la présence de notre ingénieur d'application.",
"Iniziate i lavori con tranquillità, con la presenza del nostro ingegnere di applicazione.",
"Comience las obras con tranquilidad, con la presencia de nuestro ingeniero de aplicación.",
"Begin het werk met vertrouwen, met onze applicatie-ingenieur op de werf.",
"Beginnen Sie die Arbeiten mit Ruhe, in Anwesenheit unseres Anwendungsingenieurs.",
)
_add(
"— încărcarea fonturilor tipografice (cerere către serverele Google; vezi",
"— loading of typography fonts (request to Google servers; see",
"— chargement des polices typographiques (requête vers les serveurs Google ; voir",
"— caricamento dei font tipografici (richiesta ai server Google; vedi",
"— carga de fuentes tipográficas (solicitud a los servidores de Google; ver",
"— laden van typografische lettertypen (verzoek aan Google-servers; zie",
"— Laden der Schriftarten (Anfrage an Google-Server; siehe",
)
_add(
"📝 Articolele complete vor fi publicate aici pe măsură ce sunt redactate.",
"📝 Full articles will be published here as they are written.",
"📝 Les articles complets seront publiés ici au fur et à mesure de leur rédaction.",
"📝 Gli articoli completi saranno pubblicati qui man mano che vengono redatti.",
"📝 Los artículos completos se publicarán aquí a medida que se redacten.",
"📝 Volledige artikelen worden hier gepubliceerd zodra ze zijn geschreven.",
"📝 Vollständige Artikel werden hier veröffentlicht, sobald sie verfasst sind.",
)
_add(
"Deschideri de 9 m fără grinzi, defazaj termic de 10,8 h, doar 65 kg/m².",
"9 m spans without beams, 10.8 h thermal lag, only 65 kg/m².",
"Portées de 9 m sans poutres, déphasage thermique de 10,8 h, seulement 65 kg/m².",
"Luci di 9 m senza travi, sfasamento termico di 10,8 h, solo 65 kg/m².",
"Luces de 9 m sin vigas, desfase térmico de 10,8 h, solo 65 kg/m².",
"Overspanningen van 9 m zonder balken, thermische vertraging van 10,8 u, slechts 65 kg/m².",
"Spannweiten von 9 m ohne Balken, thermische Verzögerung von 10,8 h, nur 65 kg/m².",
)
_add(
"Resurse Polistibrick · Fișe tehnice, BIM, întrebări frecvente, articole",
"Polistibrick Resources · Technical datasheets, BIM, FAQ, articles",
"Ressources Polistibrick · Fiches techniques, BIM, FAQ, articles",
"Risorse Polistibrick · Schede tecniche, BIM, FAQ, articoli",
"Recursos Polistibrick · Fichas técnicas, BIM, FAQ, artículos",
"Polistibrick Bronnen · Technische fiches, BIM, FAQ, artikelen",
"Polistibrick Ressourcen · Technische Datenblätter, BIM, FAQ, Artikel",
)
_add(
"pentru încălzire și răcire. Nu depinde de gadgeturi scumpe — depinde de",
"for heating and cooling. It doesn't depend on expensive gadgets — it depends on",
"pour le chauffage et le refroidissement. Ça ne dépend pas de gadgets coûteux — ça dépend de",
"per riscaldamento e raffreddamento. Non dipende da gadget costosi — dipende da",
"para calefacción y refrigeración. No depende de gadgets caros — depende de",
"voor verwarming en koeling. Het hangt niet af van dure gadgets — het hangt af van",
"für Heizung und Kühlung. Es hängt nicht von teuren Gadgets ab — es hängt ab von",
)
_add(
"Dacă totuși arhitectul refuză să colaboreze în interesul dumneavoastră",
"If the architect still refuses to collaborate in your best interest",
"Si malgré tout l'architecte refuse de collaborer dans votre intérêt",
"Se comunque l'architetto rifiuta di collaborare nel vostro interesse",
"Si a pesar de todo el arquitecto se niega a colaborar en su interés",
"Als de architect desondanks weigert samen te werken in uw belang",
"Wenn der Architekt dennoch weigert, in Ihrem Interesse zusammenzuarbeiten",
)
_add(
"Despre Polistibrick · Sistemul ICF brevetat pentru case pasive premium",
"About Polistibrick · The patented ICF system for premium passive homes",
"À propos de Polistibrick · Le système ICF breveté pour maisons passives haut de gamme",
"Su Polistibrick · Il sistema ICF brevettato per case passive premium",
"Acerca de Polistibrick · El sistema ICF patentado para casas pasivas premium",
"Over Polistibrick · Het gepatenteerde ICF-systeem voor premium passieve huizen",
"Über Polistibrick · Das patentierte ICF-System für Premium-Passivhäuser",
)
_add(
"— două puncte cheie ale RE2020. Testele de etanșeitate trec din prima.",
"— two key points of RE2020. Airtightness tests pass on the first attempt.",
"— deux points clés de la RE2020. Les tests d'étanchéité passent du premier coup.",
"— due punti chiave della RE2020. I test di tenuta all'aria passano al primo tentativo.",
"— dos puntos clave de RE2020. Las pruebas de estanqueidad pasan a la primera.",
"— twee kernpunten van RE2020. Luchtdichtheidstesten slagen in één keer.",
"— zwei Kernpunkte der RE2020. Luftdichtheitstests bestehen beim ersten Mal.",
)
_add(
"— garanția de perfectă finalizare (1 an), biennală (2 ani) și mai ales",
"— the perfect completion guarantee (1 year), biennial (2 years) and especially",
"— la garantie de parfait achèvement (1 an), biennale (2 ans) et surtout",
"— la garanzia di perfetto completamento (1 anno), biennale (2 anni) e soprattutto",
"— la garantía de perfecta terminación (1 año), bienal (2 años) y sobre todo",
"— de garantie van perfecte oplevering (1 jaar), tweejaarlijks (2 jaar) en vooral",
"— die Garantie für mangelfreie Fertigstellung (1 Jahr), zweijährlich (2 Jahre) und vor allem",
)
_add(
"Anumite cofraje cedează sub presiunea betonului în momentul turnării.",
"Some formwork fails under concrete pressure at the moment of pouring.",
"Certains coffrages cèdent sous la pression du béton au moment du coulage.",
"Alcuni casseforme cedono sotto la pressione del calcestruzzo al momento del getto.",
"Algunos encofrados ceden bajo la presión del hormigón en el momento del hormigonado.",
"Sommige bekistingen bezwijken onder de betondruk op het moment van storten.",
"Manche Schalungen geben unter dem Betondruck im Moment des Gießens nach.",
)
_add(
"EPS-ul brut este combustibil — dar izolatorul pe care îl folosim este",
"Raw EPS is combustible — but the insulation we use is",
"L'EPS brut est combustible — mais l'isolant que nous utilisons est",
"L'EPS grezzo è combustibile — ma l'isolante che utilizziamo è",
"El EPS bruto es combustible — pero el aislante que utilizamos es",
"Ruw EPS is brandbaar — maar de isolatie die wij gebruiken is",
"Roh-EPS ist brennbar — aber die Dämmung, die wir verwenden, ist",
)
_add(
"Materiale + livrare estimativă. Fără TVA, fără montaj, fără finisaje.",
"Materials + estimated delivery. Excl. VAT, excl. installation, excl. finishes.",
"Matériaux + livraison estimative. Hors TVA, hors montage, hors finitions.",
"Materiali + consegna stimata. IVA esclusa, montaggio escluso, finiture escluse.",
"Materiales + entrega estimada. IVA no incluido, montaje no incluido, acabados no incluidos.",
"Materialen + geschatte levering. Excl. BTW, excl. montage, excl. afwerking.",
"Material + geschätzte Lieferung. Ohne MwSt., ohne Montage, ohne Ausbau.",
)
_add(
"integrăm armătura pre-poziționată — nu e nevoie să o legi pe șantier;",
"we integrate pre-positioned reinforcement — no need to tie it on site;",
"nous intégrons l'armature pré-positionnée — pas besoin de la ligaturer sur chantier ;",
"integriamo l'armatura pre-posizionata — non serve legarla in cantiere;",
"integramos la armadura pre-posicionada — no hace falta atarla en obra;",
"wij integreren voorgepositioneerde wapening — geen noodzaak om deze op de werf te binden;",
"wir integrieren vorgepositionierte Bewehrung — kein Binden auf der Baustelle nötig;",
)
_add(
"și să nu tăiați panoul cu 5 cm prea scurt. Restul este montaj ghidat.",
"and not to cut the panel 5 cm too short. The rest is guided assembly.",
"et de ne pas couper le panneau 5 cm trop court. Le reste est un montage guidé.",
"e di non tagliare il pannello 5 cm troppo corto. Il resto è montaggio guidato.",
"y no cortar el panelo 5 cm demasiado corto. El resto es montaje guiado.",
"en het paneel niet 5 cm te kort te snijden. De rest is begeleide montage.",
"und das Paneel nicht 5 cm zu kurz zu schneiden. Der Rest ist geführte Montage.",
)
_add(
"(VMMC), nu prin infiltrații ncontrolate. Aer curat, pierderi minime.",
"(MVHR), not through uncontrolled infiltration. Clean air, minimal losses.",
"(VMC double flux), pas par des infiltrations non contrôlées. Air pur, pertes minimales.",
"(VMC a doppio flusso), non tramite infiltrazioni non controllate. Aria pulita, perdite minime.",
"(VMC de doble flujo), no por infiltraciones no controladas. Aire limpio, pérdidas mínimas.",
"(WTW), niet via ongecontroleerde infiltratie. Schone lucht, minimale verliezen.",
"(WRG-Lüftung), nicht durch unkontrollierte Infiltration. Saubere Luft, minimale Verluste.",
)
_add(
"(față de 4–5 luni cu cărămida). Pe un ansamblu de 10 case, câștigați",
"(vs 4–5 months with brick). On a development of 10 homes, you gain",
"(contre 4–5 mois avec la brique). Sur un ensemble de 10 maisons, vous gagnez",
"(contro 4–5 mesi con il mattone). Su un complesso di 10 case, guadagnate",
"(frente a 4–5 meses con ladrillo). En un conjunto de 10 casas, gana",
"(vs 4–5 maanden met baksteen). Bij een complex van 10 woningen wint u",
"(vs. 4–5 Monate mit Ziegel). Bei einer Anlage mit 10 Häusern gewinnen Sie",
)
_add(
"Mulțumim! Echipa noastră B2B te contactează în 48 de ore lucrătoare.",
"Thank you! Our B2B team will contact you within 48 business hours.",
"Merci ! Notre équipe B2B vous contacte sous 48 heures ouvrées.",
"Grazie! Il nostro team B2B ti contatterà entro 48 ore lavorative.",
"¡Gracias! Nuestro equipo B2B le contactará en 48 horas laborables.",
"Bedankt! Ons B2B-team neemt binnen 48 werkuren contact met u op.",
"Vielen Dank! Unser B2B-Team kontaktiert Sie innerhalb von 48 Werktunden.",
)
_add(
"Și cele mai robuste sunt lente și anevoioase de asamblat pe șantier.",
"Even the most robust ones are slow and cumbersome to assemble on site.",
"Même les plus robustes sont lents et pénibles à assembler sur chantier.",
"Anche i più robusti sono lenti e laboriosi da assemblare in cantiere.",
"Incluso los más robustos son lentos y engorrosos de ensamblar en obra.",
"Zelfs de meest robuuste zijn traag en lastig te monteren op de werf.",
"Selbst die robustesten sind langsam und mühsam auf der Baustelle zu montieren.",
)
_add(
". Cu, în plus, un termen de execuție de 5 săptămâni față de 5 luni.",
". Plus, a build time of 5 weeks vs 5 months.",
". Avec, en plus, un délai d'exécution de 5 semaines contre 5 mois.",
". Con, in più, un termine di esecuzione di 5 settimane contro 5 mesi.",
". Además, un plazo de ejecución de 5 semanas frente a 5 meses.",
". Bovendien een uitvoeringstermijn van 5 weken vs 5 maanden.",
". Zudem eine Ausführungszeit von 5 Wochen statt 5 Monaten.",
)
_add(
"Planșee PBK · Panouri prefabricate cu defazaj 10,8 h — Polistibrick",
"PBK Floors · Prefabricated panels with 10.8 h thermal lag — Polistibrick",
"Planchers PBK · Panneaux préfabriqués avec déphasage 10,8 h — Polistibrick",
"Solai PBK · Pannelli prefabbricati con sfasamento 10,8 h — Polistibrick",
"Forjados PBK · Paneles prefabricados con desfase 10,8 h — Polistibrick",
"Vloeren PBK · Geprefabriceerde panelen met 10,8 u thermische vertraging — Polistibrick",
"Decken PBK · Vorgefertigte Paneele mit 10,8 h thermischer Verzögerung — Polistibrick",
)
_add(
"Împărtășește experiența ta cu Polistibrick. Publicat după validare.",
"Share your Polistibrick experience. Published after validation.",
"Partagez votre expérience Polistibrick. Publié après validation.",
"Condividi la tua esperienza con Polistibrick. Pubblicato dopo la validazione.",
"Comparte tu experiencia con Polistibrick. Publicado tras la validación.",
"Deel uw Polistibrick-ervaring. Gepubliceerd na validatie.",
"Teilen Sie Ihre Polistibrick-Erfahrung. Nach Prüfung veröffentlicht.",
)
_add(
"— pereți, planșee și acoperiș izolate continuu, fără punți termice.",
"— walls, floors and roof continuously insulated, no thermal bridges.",
"— murs, planchers et toiture isolés en continu, sans ponts thermiques.",
"— pareti, solai e tetto isolati in continuo, senza ponti termici.",
"— muros, forjados y cubierta aislados de forma continua, sin puentes térmicos.",
"— muren, vloeren en dak continu geïsoleerd, zonder koudebruggen.",
"— Wände, Decken und Dach durchgängig gedämmt, ohne Wärmebrücken.",
)
_add(
"Acoperiș TBK 250 montat — un singur strat, performanță Passivhaus.",
"TBK 250 roof installed — single layer, Passivhaus performance.",
"Toiture TBK 250 montée — une seule couche, performance Passivhaus.",
"Tetto TBK 250 montato — un unico strato, prestazione Passivhaus.",
"Cubierta TBK 250 montada — una sola capa, rendimiento Passivhaus.",
"TBK 250 dak gemonteerd — één laag, Passivhaus-prestatie.",
"TBK 250 Dach montiert — eine Schicht, Passivhaus-Leistung.",
)
_add(
"Calculator economii · Cât economisești cu Polistibrick — 25 de ani",
"Savings calculator · How much you save with Polistibrick — 25 years",
"Calculateur d'économies · Combien vous économisez avec Polistibrick — 25 ans",
"Calcolatore risparmi · Quanto risparmi con Polistibrick — 25 anni",
"Calculadora de ahorros · Cuánto ahorras con Polistibrick — 25 años",
"Besparingscalculator · Hoeveel u bespaart met Polistibrick — 25 jaar",
"Sparrechner · Wie viel Sie mit Polistibrick sparen — 25 Jahre",
)
_add(
"Pereți MBK · Cofraj termoizolant pentru case pasive — Polistibrick",
"MBK Walls · Insulating formwork for passive homes — Polistibrick",
"Murs MBK · Coffrage isolant pour maisons passives — Polistibrick",
"Pareti MBK · Cassero isolante per case passive — Polistibrick",
"Muros MBK · Encofrado aislante para casas pasivas — Polistibrick",
"Muren MBK · Isolerende bekisting voor passieve huizen — Polistibrick",
"Wände MBK · Wärmedämmschalung für Passivhäuser — Polistibrick",
)
_add(
"Un parteneriat axat pe formarea echipelor și accesul la piețe noi.",
"A partnership focused on team training and access to new markets.",
"Un partenariat axé sur la formation des équipes et l'accès à de nouveaux marchés.",
"Una partnership focalizzata sulla formazione dei team e l'accesso a nuovi mercati.",
"Una asociación centrada en la formación de equipos y el acceso a nuevos mercados.",
"Een partnerschap gericht op teamtraining en toegang tot nieuwe markten.",
"Eine Partnerschaft mit Fokus auf Teamtraining und Zugang zu neuen Märkten.",
)
_add(
"— fețele exterioare, rezistență la foc A1 + suport pentru finisaje",
"— exterior faces, A1 fire resistance + support for finishes",
"— faces extérieures, résistance au feu A1 + support pour finitions",
"— facce esterne, resistenza al fuoco A1 + supporto per finiture",
"— caras exteriores, resistencia al fuego A1 + soporte para acabados",
"— buitenzijden, brandweerstand A1 + ondersteuning voor afwerking",
"— Außenseiten, Feuerwiderstand A1 + Unterstützung für Ausbau",
)
_add(
"— pereți, planșee, acoperiș, izolate continuu, fără punți termice.",
"— walls, floors, roof, continuously insulated, no thermal bridges.",
"— murs, planchers, toiture, isolés en continu, sans ponts thermiques.",
"— pareti, solai, tetto, isolati in continuo, senza ponti termici.",
"— muros, forjados, cubierta, aislados de forma continua, sin puentes térmicos.",
"— muren, vloeren, dak, continu geïsoleerd, zonder koudebruggen.",
"— Wände, Decken, Dach, durchgängig gedämmt, ohne Wärmebrücken.",
)
_add(
"Ce este o casă pasivă și cum funcționează · Articole Polistibrick",
"What is a passive house and how does it work · Polistibrick Articles",
"Qu'est-ce qu'une maison passive et comment ça fonctionne · Articles Polistibrick",
"Cos'è una casa passiva e come funziona · Articoli Polistibrick",
"Qué es una casa pasiva y cómo funciona · Artículos Polistibrick",
"Wat is een passiefhuis en hoe werkt het · Polistibrick Artikelen",
"Was ist ein Passivhaus und wie funktioniert es · Polistibrick Artikel",
)
_add(
"Conform RE2020 standard. Ideal pentru rezidențial clasic premium.",
"RE2020 standard compliant. Ideal for premium classic residential.",
"Conforme standard RE2020. Idéal pour le résidentiel classique haut de gamme.",
"Conforme standard RE2020. Ideale per residenziale classico premium.",
"Conforme estándar RE2020. Ideal para residencial clásico premium.",
"RE2020-standaard conform. Ideaal voor premium klassiek residentieel.",
"RE2020-Standard konform. Ideal für klassisches Premium-Wohnbau.",
)
_add(
"EPS continuu, fără punți termice, până la 30 cm grosime (MBK 300)",
"Continuous EPS, no thermal bridges, up to 30 cm thickness (MBK 300)",
"EPS continu, sans ponts thermiques, jusqu'à 30 cm d'épaisseur (MBK 300)",
"EPS continuo, senza ponti termici, fino a 30 cm di spessore (MBK 300)",
"EPS continuo, sin puentes térmicos, hasta 30 cm de espesor (MBK 300)",
"Doorlopend EPS, zonder koudebruggen, tot 30 cm dikte (MBK 300)",
"Durchgängiges EPS, ohne Wärmebrücken, bis 30 cm Dicke (MBK 300)",
)
_add(
"Pentru orice întrebare legată de site sau de conținutul acestuia:",
"For any question about the site or its content:",
"Pour toute question concernant le site ou son contenu :",
"Per qualsiasi domanda sul sito o sul suo contenuto:",
"Para cualquier pregunta sobre el sitio o su contenido:",
"Voor elke vraag over de site of de inhoud:",
"Für Fragen zur Website oder deren Inhalt:",
)
_add(
"față de cărămidă datorită vitezei de execuție și manoperei reduse",
"vs brick thanks to faster execution and reduced labour",
"par rapport à la brique grâce à la rapidité d'exécution et à la main-d'œuvre réduite",
"rispetto al mattone grazie alla velocità di esecuzione e alla manodopera ridotta",
"frente al ladrillo gracias a la velocidad de ejecución y la mano de obra reducida",
"ten opzichte van baksteen dankzij snellere uitvoering en minder arbeid",
"gegenüber Ziegel dank schnellerer Ausführung und geringerem Arbeitsaufwand",
)
_add(
"propunem 3 modele predefinite plus producție la comandă gratuită;",
"we offer 3 predefined models plus free custom production;",
"nous proposons 3 modèles prédéfinis plus une production sur commande gratuite ;",
"proponiamo 3 modelli predefiniti più produzione su ordinazione gratuita;",
"proponemos 3 modelos predefinidos más producción a medida gratuita;",
"wij bieden 3 vooraf gedefinieerde modellen plus gratis productie op maat;",
"wir bieten 3 vordefinierte Modelle plus kostenlose Sonderanfertigung;",
)
_add(
", fără punți termice la rosturi dacă montajul respectă manualul.",
", no thermal bridges at joints if assembly follows the manual.",
", sans ponts thermiques aux joints si le montage respecte le manuel.",
", senza ponti termici ai giunti se il montaggio rispetta il manuale.",
", sin puentes térmicos en las juntas si el montaje respeta el manual.",
", zonder koudebruggen bij voegen als de montage het handboek volgt.",
", ohne Wärmebrücken an Fugen, wenn die Montage dem Handbuch folgt.",
)
_add(
"Acoperiș montat în 2 zile. Tâmplărie cu geam low-e, triplu geam.",
"Roof installed in 2 days. Low-e triple-glazed joinery.",
"Toiture montée en 2 jours. Menuiseries triple vitrage low-e.",
"Tetto montato in 2 giorni. Serramenti con vetro low-e, triplo vetro.",
"Cubierta montada en 2 días. Carpintería con vidrio low-e, triple acristalamiento.",
"Dak gemonteerd in 2 dagen. Schrijnwerk met low-e, driedubbel glas.",
"Dach in 2 Tagen montiert. Schreinerarbeiten mit Low-E-Dreifachverglasung.",
)
_add(
"Ansamblu rezidențial · Lyon, Franța · Studiu de caz Polistibrick",
"Residential development · Lyon, France · Polistibrick case study",
"Ensemble résidentiel · Lyon, France · Étude de cas Polistibrick",
"Complesso residenziale · Lione, Francia · Caso studio Polistibrick",
"Conjunto residencial · Lyon, Francia · Estudio de caso Polistibrick",
"Wooncomplex · Lyon, Frankrijk · Polistibrick casestudy",
"Wohnanlage · Lyon, Frankreich · Polistibrick Fallstudie",
)
_add(
"Montaj Polistibrick · O casă montată manual, în câteva săptămâni",
"Polistibrick Assembly · A home built by hand, in a few weeks",
"Montage Polistibrick · Une maison montée à la main, en quelques semaines",
"Montaggio Polistibrick · Una casa montata a mano, in poche settimane",
"Montaje Polistibrick · Una casa montada a mano, en pocas semanas",
"Polistibrick Montage · Een huis handmatig gemonteerd, in enkele weken",
"Polistibrick Montage · Ein Haus von Hand montiert, in wenigen Wochen",
)
_add(
"care integrează ingenios cele 5 materiale necesare construcției.",
"that ingeniously integrates the 5 materials needed for construction.",
"qui intègre ingénieusement les 5 matériaux nécessaires à la construction.",
"che integra ingegnosamente i 5 materiali necessari alla costruzione.",
"que integra ingeniosamente los 5 materiales necesarios para la construcción.",
"dat op ingenieuze wijze de 5 materialen integreert die nodig zijn voor de bouw.",
"das auf clevere Weise die 5 für den Bau benötigten Materialien integriert.",
)
_add(
", nu +50%. Economiile la energie acoperă diferența în 8–15 ani.",
", not +50%. Energy savings cover the difference in 8–15 years.",
", pas +50 %. Les économies d'énergie couvrent la différence en 8–15 ans.",
", non +50%. I risparmi energetici coprono la differenza in 8–15 anni.",
", no +50%. Los ahorros energéticos cubren la diferencia en 8–15 años.",
", niet +50%. Energiebesparingen dekken het verschil in 8–15 jaar.",
", nicht +50 %. Energieeinsparungen decken die Differenz in 8–15 Jahren.",
)
_add(
"Pentru proprietari · Casa pe viață, fără facturi — Polistibrick",
"For homeowners · A home for life, no bills — Polistibrick",
"Pour propriétaires · Une maison pour la vie, sans factures — Polistibrick",
"Per proprietari · Casa per tutta la vita, senza bollette — Polistibrick",
"Para propietarios · Casa de por vida, sin facturas — Polistibrick",
"Voor huiseigenaren · Huis voor het leven, zonder rekeningen — Polistibrick",
"Für Eigentümer · Haus fürs Leben, ohne Rechnungen — Polistibrick",
)
_add(
"Răspuns în 3 zile lucrătoare. Toate datele rămân confidențiale.",
"Response within 3 business days. All data remains confidential.",
"Réponse sous 3 jours ouvrés. Toutes les données restent confidentielles.",
"Risposta entro 3 giorni lavorativi. Tutti i dati restano riservati.",
"Respuesta en 3 días laborables. Todos los datos permanecen confidenciales.",
"Antwoord binnen 3 werkdagen. Alle gegevens blijven vertrouwelijk.",
"Antwort innerhalb von 3 Werktagen. Alle Daten bleiben vertraulich.",
)
_add(
"Vilă de familie · Valencia, Spania · Studiu de caz Polistibrick",
"Family villa · Valencia, Spain · Polistibrick case study",
"Villa familiale · Valence, Espagne · Étude de cas Polistibrick",
"Villa familiare · Valencia, Spagna · Caso studio Polistibrick",
"Villa familiar · Valencia, España · Estudio de caso Polistibrick",
"Gezinsvilla · Valencia, Spanje · Polistibrick casestudy",
"Familienvilla · Valencia, Spanien · Polistibrick Fallstudie",
)
_add(
", indiferent de prețul energiei. Calculați economiile mai jos.",
", regardless of energy prices. Calculate your savings below.",
", quel que soit le prix de l'énergie. Calculez vos économies ci-dessous.",
", indipendentemente dal prezzo dell'energia. Calcolate i risparmi qui sotto.",
", independientemente del precio de la energía. Calcule sus ahorros a continuación.",
", ongeacht de energieprijs. Bereken uw besparingen hieronder.",
", unabhängig vom Energiepreis. Berechnen Sie Ihre Ersparnisse unten.",
)
_add(
", în calitate de reprezentant legal al {{company.name_short}}.",
", as legal representative of {{company.name_short}}.",
", en qualité de représentant légal de {{company.name_short}}.",
", in qualità di rappresentante legale di {{company.name_short}}.",
", en calidad de representante legal de {{company.name_short}}.",
", als wettelijke vertegenwoordiger van {{company.name_short}}.",
", als gesetzlicher Vertreter von {{company.name_short}}.",
)
_add(
"Articole Polistibrick · Casă pasivă, ICF, eficiență energetică",
"Polistibrick Articles · Passive house, ICF, energy efficiency",
"Articles Polistibrick · Maison passive, ICF, efficacité énergétique",
"Articoli Polistibrick · Casa passiva, ICF, efficienza energetica",
"Artículos Polistibrick · Casa pasiva, ICF, eficiencia energética",
"Polistibrick Artikelen · Passiefhuis, ICF, energie-efficiëntie",
"Polistibrick Artikel · Passivhaus, ICF, Energieeffizienz",
)
_add(
"Pereții parterului montați integral, pregătiți pentru planșeu.",
"Ground-floor walls fully installed, ready for the floor slab.",
"Murs du rez-de-chaussée montés intégralement, prêts pour le plancher.",
"Pareti del piano terra montati integralmente, pronti per il solaio.",
"Muros de la planta baja montados íntegramente, listos para el forjado.",
"Muren van de begane grond volledig gemonteerd, klaar voor de vloerplaat.",
"Erdgeschosswände vollständig montiert, bereit für die Decke.",
)
_add(
". Peretele se ridică aproape singur — nu ne întoarcem înapoi.",
". The wall goes up almost by itself — we're not going back.",
". Le mur se dresse presque tout seul — on ne revient pas en arrière.",
". Il muro si alza quasi da solo — non torniamo indietro.",
". El muro se levanta casi solo — no volvemos atrás.",
". De muur gaat bijna vanzelf omhoog — we gaan niet terug.",
". Die Wand steht fast von selbst — wir gehen nicht zurück.",
)
_add(
"Mulțumim! Echipa noastră vă răspunde în 24 de ore lucrătoare.",
"Thank you! Our team will respond within 24 business hours.",
"Merci ! Notre équipe vous répond sous 24 heures ouvrées.",
"Grazie! Il nostro team vi risponde entro 24 ore lavorative.",
"¡Gracias! Nuestro equipo le responderá en 24 horas laborables.",
"Bedankt! Ons team antwoordt binnen 24 werkuren.",
"Vielen Dank! Unser Team antwortet innerhalb von 24 Werktunden.",
)
_add(
"Pentru deschideri mici și medii. Soluția ușoară și economică.",
"For small and medium spans. The lightweight, cost-effective solution.",
"Pour petites et moyennes portées. La solution légère et économique.",
"Per luci piccole e medie. La soluzione leggera ed economica.",
"Para luces pequeñas y medianas. La solución ligera y económica.",
"Voor kleine en middelgrote overspanningen. De lichte en economische oplossing.",
"Für kleine und mittlere Spannweiten. Die leichte und wirtschaftliche Lösung.",
)
_add(
"Turnarea betonului într-o singură etapă — întreaga structură.",
"Single-stage concrete pour — the entire structure.",
"Coulage du béton en une seule étape — toute la structure.",
"Getto di calcestruzzo in un'unica fase — l'intera struttura.",
"Hormigonado en una sola fase — toda la estructura.",
"Betonstorting in één fase — de volledige structuur.",
"Betonierrung in einem Guss — die gesamte Struktur.",
)
_add(
"este asigurată de sistem în sine, iar izolația este continuă,",
"is ensured by the system itself, and insulation is continuous,",
"est assurée par le système lui-même, et l'isolation est continue,",
"è garantita dal sistema stesso, e l'isolamento è continuo,",
"está asegurada por el propio sistema, y el aislamiento es continuo,",
"wordt door het systeem zelf gewaarborgd, en de isolatie is doorlopend,",
"wird vom System selbst gewährleistet, und die Dämmung ist durchgängig,",
)
_add(
"pentru partenerii certificați + livrare prioritară pe șantier",
"for certified partners + priority delivery to site",
"pour les partenaires certifiés + livraison prioritaire sur chantier",
"per i partner certificati + consegna prioritaria in cantiere",
"para socios certificados + entrega prioritaria en obra",
"voor gecertificeerde partners + prioritaire levering op de werf",
"für zertifizierte Partner + prioritäre Lieferung auf die Baustelle",
)
_add(
"(auto-stingător). Și mai ales, în sistemul Polistibrick este",
"(self-extinguishing). And above all, in the Polistibrick system it is",
"(auto-extincteur). Et surtout, dans le système Polistibrick il est",
"(autoestinguente). E soprattutto, nel sistema Polistibrick è",
"(autoextinguible). Y sobre todo, en el sistema Polistibrick es",
"(zelfdovend). En vooral, in het Polistibrick-systeem is het",
"(selbstlöschend). Und vor allem ist es im Polistibrick-System",
)
_add(
"Detaliu sistem asamblare brevetat — punți termice eliminate.",
"Patented assembly system detail — thermal bridges eliminated.",
"Détail du système d'assemblage breveté — ponts thermiques éliminés.",
"Dettaglio sistema di assemblaggio brevettato — ponti termici eliminati.",
"Detalle del sistema de ensamblaje patentado — puentes térmicos eliminados.",
"Detail gepatenteerd montagesysteem — koudebruggen geëlimineerd.",
"Detail des patentierten Montagesystems — Wärmebrücken eliminiert.",
)
_add(
"— corpul izolant central, defazaj termic de până la 10,8 ore",
"— central insulating core, thermal lag up to 10.8 hours",
"— corps isolant central, déphasage thermique jusqu'à 10,8 heures",
"— corpo isolante centrale, sfasamento termico fino a 10,8 ore",
"— núcleo aislante central, desfase térmico de hasta 10,8 horas",
"— centraal isolerend kern, thermische vertraging tot 10,8 uur",
"— zentraler Dämmkern, thermische Verzögerung bis zu 10,8 Stunden",
)
_add(
"Acoperiș TBK · Sistem Passivhaus din fabrică — Polistibrick",
"TBK Roof · Passivhaus system from the factory — Polistibrick",
"Toiture TBK · Système Passivhaus d'usine — Polistibrick",
"Tetto TBK · Sistema Passivhaus di fabbrica — Polistibrick",
"Tejado TBK · Sistema Passivhaus de fábrica — Polistibrick",
"Dak TBK · Passivhaus-systeem uit de fabriek — Polistibrick",
"Dach TBK · Passivhaus-System ab Werk — Polistibrick",
)
_add(
"Casă individuală · Cluj-Napoca · Studiu de caz Polistibrick",
"Single-family home · Cluj-Napoca · Polistibrick case study",
"Maison individuelle · Cluj-Napoca · Étude de cas Polistibrick",
"Casa unifamiliare · Cluj-Napoca · Caso studio Polistibrick",
"Casa unifamiliar · Cluj-Napoca · Estudio de caso Polistibrick",
"Eengezinswoning · Cluj-Napoca · Polistibrick casestudy",
"Einfamilienhaus · Cluj-Napoca · Polistibrick Fallstudie",
)
_add(
"Dacă ai planuri sau doar o idee de suprafață, poți obține o",
"If you have plans or just a floor area idea, you can get a",
"Si vous avez des plans ou juste une idée de surface, vous pouvez obtenir un",
"Se hai progetti o solo un'idea di superficie, puoi ottenere un",
"Si tienes planos o solo una idea de superficie, puedes obtener un",
"Als u plannen heeft of alleen een idee van oppervlakte, kunt u een",
"Wenn Sie Pläne haben oder nur eine Flächenvorstellung, können Sie ein",
)
_add(
"Specialiștii noștri vă răspund direct în maximum 24 de ore.",
"Our specialists respond to you directly within 24 hours.",
"Nos spécialistes vous répondent directement sous 24 heures maximum.",
"I nostri specialisti vi rispondono direttamente entro massimo 24 ore.",
"Nuestros especialistas le responden directamente en un máximo de 24 horas.",
"Onze specialisten antwoorden u rechtstreeks binnen maximaal 24 uur.",
"Unsere Spezialisten antworten Ihnen direkt innerhalb von maximal 24 Stunden.",
)
_add(
"al fiecărui criteriu (explicații tehnice, norme, exemple) →",
"for each criterion (technical explanations, standards, examples) →",
"pour chaque critère (explications techniques, normes, exemples) →",
"per ogni criterio (spiegazioni tecniche, norme, esempi) →",
"para cada criterio (explicaciones técnicas, normas, ejemplos) →",
"per criterium (technische uitleg, normen, voorbeelden) →",
"für jedes Kriterium (technische Erklärungen, Normen, Beispiele) →",
)
_add(
"beton armat de 15 cm — rezistență la cutremure și la foc A1",
"15 cm reinforced concrete — earthquake and A1 fire resistance",
"béton armé de 15 cm — résistance aux séismes et au feu A1",
"calcestruzzo armato di 15 cm — resistenza ai terremoti e al fuoco A1",
"hormigón armado de 15 cm — resistencia a terremotos y fuego A1",
"15 cm gewapend beton — aardbevings- en brandweerstand A1",
"15 cm Stahlbeton — Erdbeben- und Feuerwiderstand A1",
)
_add(
"« Dacă apare o problemă, rămân singur față de beneficiar. »",
'"If a problem arises, I am left alone facing the client."',
"« Si un problème survient, je reste seul face au client. »",
"« Se sorge un problema, resto solo di fronte al committente. »",
"« Si surge un problema, me quedo solo frente al cliente. »",
"« Als er een probleem ontstaat, sta ik alleen tegenover de opdrachtgever. »",
'„Wenn ein Problem auftritt, stehe ich allein dem Auftraggeber gegenüber."',
)
_add(
", cea mai bună clasă de reacție la foc. Rezultat: sistemul",
", the highest fire reaction class. Result: the system",
", la meilleure classe de réaction au feu. Résultat : le système",
", la migliore classe di reazione al fuoco. Risultato: il sistema",
", la mejor clase de reacción al fuego. Resultado: el sistema",
", de hoogste brandreactieklasse. Resultaat: het systeem",
", die beste Brandreaktionsklasse. Ergebnis: das System",
)
_add(
"Calculator cost · Estimează prețul casei tale Polistibrick",
"Cost calculator · Estimate the price of your Polistibrick home",
"Calculateur de coût · Estimez le prix de votre maison Polistibrick",
"Calcolatore costi · Stima il prezzo della tua casa Polistibrick",
"Calculadora de costes · Estima el precio de tu casa Polistibrick",
"Kostencalculator · Schat de prijs van uw Polistibrick-huis",
"Kostenrechner · Schätzen Sie den Preis Ihres Polistibrick-Hauses",
)
_add(
"Factură electricitate ianuarie 2025: 41 €. Iarnă la −8 °C.",
"Electricity bill January 2025: €41. Winter at −8 °C.",
"Facture électricité janvier 2025 : 41 €. Hiver à −8 °C.",
"Bolletta elettricità gennaio 2025: 41 €. Inverno a −8 °C.",
"Factura electricidad enero 2025: 41 €. Invierno a −8 °C.",
"Elektriciteitsrekening januari 2025: €41. Winter bij −8 °C.",
"Stromrechnung Januar 2025: 41 €. Winter bei −8 °C.",
)
_add(
"O scurtă formare este suficientă pentru a prelua sistemul.",
"A short training is enough to take on the system.",
"Une courte formation suffit pour prendre en main le système.",
"Una breve formazione è sufficiente per prendere in mano il sistema.",
"Una breve formación es suficiente para asumir el sistema.",
"Een korte training is voldoende om het systeem over te nemen.",
"Eine kurze Schulung genügt, um das System zu übernehmen.",
)
_add(
"Un partener Polistibrick construiește 10–50 de case pe an.",
"A Polistibrick partner builds 10–50 homes per year.",
"Un partenaire Polistibrick construit 10 à 50 maisons par an.",
"Un partner Polistibrick costruisce 10–50 case all'anno.",
"Un socio Polistibrick construye 10–50 casas al año.",
"Een Polistibrick-partner bouwt 10–50 huizen per jaar.",
"Ein Polistibrick-Partner baut 10–50 Häuser pro Jahr.",
)
_add(
"« Întârzierile de livrare pe șantier mă vor costa scump. »",
'"Delivery delays on site will cost me dearly."',
"« Les retards de livraison sur chantier me coûteront cher. »",
"« I ritardi di consegna in cantiere mi costeranno caro. »",
"« Los retrasos de entrega en obra me costarán caro. »",
"« Leveringsvertragingen op de werf kosten me veel geld. »",
'„Lieferverzögerungen auf der Baustelle werden mich teuer zu stehen kommen."',
)
_add(
"Da, fără nicio dificultate. Structural, Polistibrick este",
"Yes, without any difficulty. Structurally, Polistibrick is",
"Oui, sans aucune difficulté. Structurellement, Polistibrick est",
"Sì, senza alcuna difficoltà. Strutturalmente, Polistibrick è",
"Sí, sin ninguna dificultad. Estructuralmente, Polistibrick es",
"Ja, zonder enige moeite. Structureel is Polistibrick",
"Ja, ohne jede Schwierigkeit. Strukturell ist Polistibrick",
)
_add(
"Modulele 3+4 pornesc în paralel cu finisajele pe primele.",
"Modules 3+4 start in parallel with finishes on the first ones.",
"Les modules 3+4 démarrent en parallèle des finitions sur les premiers.",
"I moduli 3+4 partono in parallelo alle finiture sui primi.",
"Los módulos 3+4 arrancan en paralelo con los acabados en los primeros.",
"Modules 3+4 starten parallel met de afwerking op de eerste.",
"Module 3+4 starten parallel zur Ausführung der Ausbauarbeiten an den ersten.",
)
_add(
"Pregătire turnare beton (cantitate optimă pre-calculată).",
"Concrete pour preparation (optimal quantity pre-calculated).",
"Préparation coulage béton (quantité optimale pré-calculée).",
"Preparazione getto calcestruzzo (quantità ottimale pre-calcolata).",
"Preparación hormigonado (cantidad óptima precalculada).",
"Voorbereiding betonstorting (optimale hoeveelheid vooraf berekend).",
"Vorbereitung Betonierung (optimale Menge vorberechnet).",
)
_add(
"de la 5 unități, acord-cadru dedicat pentru programe 25+.",
"from 5 units, dedicated framework agreement for 25+ programmes.",
"à partir de 5 unités, accord-cadre dédié pour les programmes 25+.",
"a partire da 5 unità, accordo quadro dedicato per programmi 25+.",
"a partir de 5 unidades, acuerdo marco dedicado para programas 25+.",
"vanaf 5 eenheden, toegewijd raamcontract voor programma's van 25+.",
"ab 5 Einheiten, dedizierter Rahmenvertrag für Programme ab 25+.",
)
_add(
"este o locuință construită astfel încât să aibă nevoie de",
"is a home built so that it needs",
"est un logement construit de sorte à avoir besoin de",
"è un'abitazione costruita in modo da aver bisogno di",
"es una vivienda construida de forma que necesita",
"is een woning gebouwd zodat deze behoefte heeft aan",
"ist ein Zuhause, das so gebaut ist, dass es",
)
_add(
"reducere sonoră premium prin combinația EPS + beton armat",
"premium sound reduction through the EPS + reinforced concrete combination",
"réduction sonore premium par la combinaison EPS + béton armé",
"riduzione sonora premium tramite la combinazione EPS + calcestruzzo armato",
"reducción sonora premium mediante la combinación EPS + hormigón armado",
"premium geluidsreductie door de combinatie EPS + gewapend beton",
"Premium-Schalldämmung durch die Kombination EPS + Stahlbeton",
)
_add(
"respiră prin ventilație mecanică cu recuperare de căldură",
"breathes through mechanical ventilation with heat recovery",
"respire par ventilation mécanique avec récupération de chaleur",
"respira tramite ventilazione meccanica con recupero di calore",
"respira mediante ventilación mecánica con recuperación de calor",
"ademt via mechanische ventilatie met warmteterugwinning",
"atmet über mechanische Lüftung mit Wärmerückgewinnung",
)
_add(
"— asigurare daune-opere și garanție decenală incluse — la",
"— construction insurance and ten-year warranty included — at",
"— assurance dommages-ouvrage et garantie décennale incluses — à",
"— assicurazione danni-opera e garanzia decennale incluse — a",
"— seguro de daños en la obra y garantía decenal incluidos — a",
"— bouwverzekering en tienjarige garantie inbegrepen — tegen",
"— Bauversicherung und Zehnjahresgarantie inklusive — zu",
)
_add(
"✓ Cost de construcție (panouri + manoperă, fără finisaje)",
"✓ Construction cost (panels + labour, excl. finishes)",
"✓ Coût de construction (panneaux + main-d'œuvre, hors finitions)",
"✓ Costo di costruzione (pannelli + manodopera, finiture escluse)",
"✓ Coste de construcción (paneles + mano de obra, sin acabados)",
"✓ Bouwkosten (panelen + arbeid, excl. afwerking)",
"✓ Baukosten (Paneele + Arbeitskosten, ohne Ausbau)",
)
_add(
"Fațadă principală finisată cu tencuială silicatică crem.",
"Main facade finished with cream silicate render.",
"Façade principale finie avec enduit silicaté crème.",
"Facciata principale finita con intonaco silicatico crema.",
"Fachada principal acabada con enlucido silicático crema.",
"Hoofdgevel afgewerkt met crèmekleurig silicaatpleister.",
"Hauptfassade mit cremefarbenem Silikatputz fertiggestellt.",
)
_add(
"Mesajul dvs. ajunge direct la echipa din țara selectată.",
"Your message goes directly to the team in the selected country.",
"Votre message arrive directement à l'équipe du pays sélectionné.",
"Il vostro messaggio arriva direttamente al team del paese selezionato.",
"Su mensaje llega directamente al equipo del país seleccionado.",
"Uw bericht komt rechtstreeks bij het team in het geselecteerde land.",
"Ihre Nachricht erreicht direkt das Team im ausgewählten Land.",
)
_add(
"pe proiect, recuperând valoarea anterior subcontractată.",
"per project, recovering value previously subcontracted.",
"par projet, récupérant la valeur précédemment sous-traitée.",
"per progetto, recuperando il valore precedentemente subappaltato.",
"por proyecto, recuperando el valor anteriormente subcontratado.",
"per project, waarde terugwinnend die eerder werd uitbesteed.",
"pro Projekt, wiedergewinnend, was zuvor ausgelagert wurde.",
)
_add(
"— până la cofraj închis, gata pentru turnarea betonului.",
"— up to closed formwork, ready for the concrete pour.",
"— jusqu'au coffrage fermé, prêt pour le coulage du béton.",
"— fino al cassero chiuso, pronto per il getto di calcestruzzo.",
"— hasta encofrado cerrado, listo para el hormigonado.",
"— tot gesloten bekisting, klaar voor het storten van beton.",
"— bis zur geschlossenen Schalung, bereit für die Betonierung.",
)
_add(
"— un inginer Polistibrick te însoțește la primul proiect",
"— a Polistibrick engineer accompanies you on your first project",
"— un ingénieur Polistibrick vous accompagne sur votre premier projet",
"— un ingegnere Polistibrick ti accompagna nel primo progetto",
"— un ingeniero Polistibrick te acompaña en tu primer proyecto",
"— een Polistibrick-ingenieur begeleidt u bij uw eerste project",
"— ein Polistibrick-Ingenieur begleitet Sie beim ersten Projekt",
)
_add(
"— λ = 0,031 W/mK, performanță Passivhaus din construcție",
"— λ = 0.031 W/mK, Passivhaus performance built in",
"— λ = 0,031 W/mK, performance Passivhaus dès la construction",
"— λ = 0,031 W/mK, prestazione Passivhaus dalla costruzione",
"— λ = 0,031 W/mK, rendimiento Passivhaus desde la construcción",
"— λ = 0,031 W/mK, Passivhaus-prestatie ingebouwd",
"— λ = 0,031 W/mK, Passivhaus-Leistung ab der Konstruktion",
)
_add(
". Polistibrick este același beton armat, turnat într-un",
". Polistibrick is the same reinforced concrete, poured into a",
". Polistibrick, c'est le même béton armé, coulé dans un",
". Polistibrick è lo stesso calcestruzzo armato, gettato in un",
". Polistibrick es el mismo hormigón armado, vertido en un",
". Polistibrick is hetzelfde gewapend beton, gestort in een",
". Polistibrick ist derselbe Stahlbeton, gegossen in eine",
)
_add(
"Ce se întâmplă dacă vreau să modific casa peste 10 ani?",
"What happens if I want to modify the house in 10 years?",
"Que se passe-t-il si je veux modifier la maison dans 10 ans ?",
"Cosa succede se voglio modificare la casa tra 10 anni?",
"¿Qué pasa si quiero modificar la casa dentro de 10 años?",
"Wat gebeurt er als ik het huis over 10 jaar wil aanpassen?",
"Was passiert, wenn ich das Haus in 10 Jahren umbauen möchte?",
)
_add(
"Pereții etajului 1 montați și armătură pre-poziționată.",
"First-floor walls installed and pre-positioned reinforcement.",
"Murs du 1er étage montés et armature pré-positionnée.",
"Pareti del piano 1 montati e armatura pre-posizionata.",
"Muros de la planta 1 montados y armadura pre-posicionada.",
"Muren van verdieping 1 gemonteerd en voorgepositioneerde wapening.",
"Wände des 1. Geschosses montiert und vorgepositionierte Bewehrung.",
)
_add(
"Turnare beton într-o singură etapă pentru toți pereții.",
"Single-stage concrete pour for all walls.",
"Coulage béton en une seule étape pour tous les murs.",
"Getto calcestruzzo in un'unica fase per tutti i muri.",
"Hormigonado en una sola fase para todos los muros.",
"Betonstorting in één fase voor alle muren.",
"Betonierrung in einem Guss für alle Wände.",
)
_add(
"identic cu tehnologia clasică a zidului din beton armat",
"identical to classic reinforced concrete wall technology",
"identique à la technologie classique du mur en béton armé",
"identico alla tecnologia classica del muro in calcestruzzo armato",
"idéntico a la tecnología clásica del muro de hormigón armado",
"identiek aan klassieke gewapend-betonwandtechnologie",
"identisch mit klassischer Stahlbetonwand-Technologie",
)
_add(
"nu mai are nevoie să consume energie pentru a funcționa",
"no longer needs to consume energy to function",
"n'a plus besoin de consommer d'énergie pour fonctionner",
"non ha più bisogno di consumare energia per funzionare",
"ya no necesita consumir energía para funcionar",
"hoeft geen energie meer te verbruiken om te functioneren",
"muss keine Energie mehr verbrauchen, um zu funktionieren",
)
_add(
"« Documentația tehnică este împrăștiată sau lipsește. »",
'"Technical documentation is scattered or missing."',
"« La documentation technique est dispersée ou manquante. »",
"« La documentazione tecnica è sparsa o mancante. »",
"« La documentación técnica está dispersa o falta. »",
"« Technische documentatie is verspreid of ontbreekt. »",
'„Die technische Dokumentation ist verstreut oder fehlt."',
)
_add(
"« Nu creez o companie. Creez un sistem pentru viitor. »",
'"I am not building a company. I am building a system for the future."',
"« Je ne crée pas une entreprise. Je crée un système pour l'avenir. »",
"« Non creo un'azienda. Creo un sistema per il futuro. »",
"« No creo una empresa. Creo un sistema para el futuro. »",
"« Ik bouw geen bedrijf. Ik bouw een systeem voor de toekomst. »",
'„Ich gründe kein Unternehmen. Ich schaffe ein System für die Zukunft."',
)
_add(
"Îmbinări perete-perete, perete-planșeu, perete-acoperiș",
"Wall-to-wall, wall-to-floor, wall-to-roof junctions",
"Jonctions mur-mur, mur-plancher, mur-toiture",
"Giunzioni parete-parete, parete-solaio, parete-tetto",
"Uniones muro-muro, muro-forjado, muro-cubierta",
"Muur-muur, muur-vloer, muur-dak aansluitingen",
"Wand-Wand-, Wand-Decke-, Wand-Dach-Anschlüsse",
)
_add(
"— răcoare vara, cald iarna, fără izolație suplimentară.",
"— cool in summer, warm in winter, no additional insulation.",
"— frais en été, chaud en hiver, sans isolation supplémentaire.",
"— fresco in estate, caldo in inverno, senza isolamento aggiuntivo.",
"— fresco en verano, cálido en invierno, sin aislamiento adicional.",
"— koel in de zomer, warm in de winter, zonder extra isolatie.",
"— kühl im Sommer, warm im Winter, ohne zusätzliche Dämmung.",
)
_add(
"Depășește larg RE2020. Standard Passivhaus certificat.",
"Far exceeds RE2020. Certified Passivhaus standard.",
"Dépasse largement la RE2020. Standard Passivhaus certifié.",
"Supera ampiamente la RE2020. Standard Passivhaus certificato.",
"Supera con creces RE2020. Estándar Passivhaus certificado.",
"Overtreft ruimschoots RE2020. Gecertificeerde Passivhaus-standaard.",
"Übertrifft RE2020 deutlich. Zertifizierter Passivhaus-Standard.",
)
_add(
"față de o casă tradițională din cărămidă neoptimizată.",
"vs an unoptimised traditional brick home.",
"par rapport à une maison traditionnelle en brique non optimisée.",
"rispetto a una casa tradizionale in mattone non ottimizzata.",
"frente a una casa tradicional de ladrillo no optimizada.",
"ten opzichte van een niet-geoptimaliseerd traditioneel bakstenen huis.",
"gegenüber einem nicht optimierten traditionellen Ziegelhaus.",
)
_add(
"🔒 Verificat și publicat de Polistibrick după validare.",
"🔒 Verified and published by Polistibrick after validation.",
"🔒 Vérifié et publié par Polistibrick après validation.",
"🔒 Verificato e pubblicato da Polistibrick dopo la validazione.",
"🔒 Verificado y publicado por Polistibrick tras la validación.",
"🔒 Geverifieerd en gepubliceerd door Polistibrick na validatie.",
"🔒 Von Polistibrick geprüft und nach Validierung veröffentlicht.",
)
_add(
"Aveți nevoie de un dosar tehnic de inginerie complet?",
"Do you need a complete engineering technical file?",
"Avez-vous besoin d'un dossier technique d'ingénierie complet ?",
"Avete bisogno di un fascicolo tecnico di ingegneria completo?",
"¿Necesita un expediente técnico de ingeniería completo?",
"Heeft u een volledig technisch engineeringdossier nodig?",
"Benötigen Sie eine vollständige technische Ingenieurmappe?",
)
_add(
"VMC (ventilație mecanică controlată) este obligatorie",
"MVHR (mechanical ventilation with heat recovery) is mandatory",
"La VMC (ventilation mécanique contrôlée) est obligatoire",
"La VMC (ventilazione meccanica controllata) è obbligatoria",
"La VMC (ventilación mecánica controlada) es obligatoria",
"WTW (mechanische ventilatie met warmteterugwinning) is verplicht",
"Die WRG-Lüftung (mechanische Lüftung mit Wärmerückgewinnung) ist obligatorisch",
)
_add(
"deținem un brevet european, deci este un sistem unic.",
"we hold a European patent, so it is a unique system.",
"nous détenons un brevet européen, c'est donc un système unique.",
"possediamo un brevetto europeo, quindi è un sistema unico.",
"poseemos una patente europea, por lo que es un sistema único.",
"wij bezitten een Europees octrooi, het is dus een uniek systeem.",
"wir besitzen ein europäisches Patent, es ist also ein einzigartiges System.",
)
_add(
"« Ce se întâmplă dacă regret alegerea peste 10 ani? »",
'"What if I regret my choice in 10 years?"',
"« Que se passe-t-il si je regrette mon choix dans 10 ans ? »",
"« Cosa succede se mi pentirò della scelta tra 10 anni? »",
"« ¿Qué pasa si me arrepiento de la elección dentro de 10 años? »",
"« Wat als ik over 10 jaar spijt heb van mijn keuze? »",
'„Was, wenn ich meine Wahl in 10 Jahren bereue?"',
)
_add(
"și te alături rețelei de parteneri fixi Polistibrick.",
"and join the Polistibrick fixed partner network.",
"et rejoignez le réseau de partenaires fixes Polistibrick.",
"e ti unisci alla rete di partner fissi Polistibrick.",
"y te unes a la red de socios fijos Polistibrick.",
"en sluit u aan bij het vaste Polistibrick-partnernetwerk.",
"und treten Sie dem festen Polistibrick-Partnernetzwerk bei.",
)
_add(
"Pentru prelucrarea generală a datelor dumneavoastră:",
"For the general processing of your data:",
"Pour le traitement général de vos données :",
"Per il trattamento generale dei vostri dati:",
"Para el tratamiento general de sus datos:",
"Voor de algemene verwerking van uw gegevens:",
"Für die allgemeine Verarbeitung Ihrer Daten:",
)
_add(
"Sistemul se adaptează unei arhitecturi tradiționale?",
"Does the system adapt to traditional architecture?",
"Le système s'adapte-t-il à une architecture traditionnelle ?",
"Il sistema si adatta a un'architettura tradizionale?",
"¿El sistema se adapta a una arquitectura tradicional?",
"Past het systeem bij traditionele architectuur?",
"Passt sich das System an traditionelle Architektur an?",
)
_add(
"Vedere aeriană a șantierului la jumătatea execuției.",
"Aerial view of the site at mid-construction.",
"Vue aérienne du chantier à mi-parcours.",
"Vista aerea del cantiere a metà esecuzione.",
"Vista aérea de la obra a mitad de ejecución.",
"Luchtfoto van de werf halverwege de uitvoering.",
"Luftaufnahme der Baustelle zur Hälfte der Ausführung.",
)
_add(
"« Nu există bibliotecă BIM sau fișiere CAD curate. »",
'"There is no BIM library or clean CAD files."',
"« Il n'existe pas de bibliothèque BIM ni de fichiers CAD propres. »",
"« Non esiste una libreria BIM o file CAD puliti. »",
"« No hay biblioteca BIM ni archivos CAD limpios. »",
"« Er is geen BIM-bibliotheek of schone CAD-bestanden. »",
'„Es gibt keine BIM-Bibliothek oder saubere CAD-Dateien."',
)
_add(
"« Voi trebui să învăț o metodă de calcul specială. »",
'"I will have to learn a special calculation method."',
"« Je vais devoir apprendre une méthode de calcul spéciale. »",
"« Dovrò imparare un metodo di calcolo speciale. »",
"« Tendré que aprender un método de cálculo especial. »",
"« Ik zal een speciale rekenmethode moeten leren. »",
'„Ich werde eine spezielle Berechnungsmethode lernen müssen."',
)
_add(
"(de 3–4 ori mai puțin decât o casă nouă obișnuită);",
"(3–4 times less than a typical new home);",
"(3 à 4 fois moins qu'une maison neuve classique) ;",
"(3–4 volte meno di una casa nuova tradizionale);",
"(3–4 veces menos que una casa nueva habitual);",
"(3–4 keer minder dan een gewone nieuwbouwwoning);",
"(3–4-mal weniger als ein übliches Neubauhaus);",
)
_add(
"Cum obțin finanțarea pentru acest cost suplimentar?",
"How do I obtain financing for this additional cost?",
"Comment obtenir le financement pour ce coût supplémentaire ?",
"Come ottengo il finanziamento per questo costo aggiuntivo?",
"¿Cómo obtengo la financiación para este coste adicional?",
"Hoe verkrijg ik financiering voor deze extra kosten?",
"Wie erhalte ich die Finanzierung für diese Mehrkosten?",
)
_add(
"Câți muncitori sunt necesari pentru a monta o casă?",
"How many workers are needed to assemble a home?",
"Combien d'ouvriers sont nécessaires pour monter une maison ?",
"Quanti operai servono per montare una casa?",
"¿Cuántos trabajadores se necesitan para montar una casa?",
"Hoeveel arbeiders zijn nodig om een huis te monteren?",
"Wie viele Arbeiter werden benötigt, um ein Haus zu montieren?",
)
_add(
"Fotografiile de șantier vor fi publicate în curând.",
"Site photos will be published soon.",
"Les photos de chantier seront publiées prochainement.",
"Le foto di cantiere saranno pubblicate a breve.",
"Las fotos de obra se publicarán pronto.",
"Werfoto's worden binnenkort gepubliceerd.",
"Baustellenfotos werden in Kürze veröffentlicht.",
)
_add(
"Pentru constructori · Program partener Polistibrick",
"For builders · Polistibrick partner programme",
"Pour constructeurs · Programme partenaire Polistibrick",
"Per costruttori · Programma partner Polistibrick",
"Para constructores · Programa socio Polistibrick",
"Voor bouwers · Polistibrick partnerprogramma",
"Für Bauunternehmer · Polistibrick Partnerprogramm",
)
_add(
"Polistibrick te formează direct pe propriul șantier",
"Polistibrick trains you directly on your own site",
"Polistibrick vous forme directement sur votre propre chantier",
"Polistibrick ti forma direttamente sul tuo cantiere",
"Polistibrick te forma directamente en tu propia obra",
"Polistibrick leidt u rechtstreeks op op uw eigen werf",
"Polistibrick schult Sie direkt auf Ihrer eigenen Baustelle",
)
_add(
"Videoclipul tău testimonial — cel mai convingător ⭐",
"Your testimonial video — the most convincing ⭐",
"Votre vidéo témoignage — la plus convaincante ⭐",
"Il tuo video testimonianza — il più convincente ⭐",
"Tu vídeo testimonial — el más convincente ⭐",
"Uw testimonialvideo — de meest overtuigende ⭐",
"Ihr Erfahrungsvideo — das überzeugendste ⭐",
)
_add(
"pe lot — mai puține dobânzi, monetizare mai rapidă.",
"per lot — less interest, faster monetisation.",
"par lot — moins d'intérêts, monétisation plus rapide.",
"per lotto — meno interessi, monetizzazione più rapida.",
"por parcela — menos intereses, monetización más rápida.",
"per perceel — minder rente, snellere verzilvering.",
"pro Los — weniger Zinsen, schnellere Verwertung.",
)
_add(
"pentru că construcția este aerul pe care îl respir.",
"because construction is the air I breathe.",
"parce que la construction est l'air que je respire.",
"perché la costruzione è l'aria che respiro.",
"porque la construcción es el aire que respiro.",
"omdat bouwen de lucht is die ik adem.",
"weil Bauen die Luft ist, die ich atme.",
)
_add(
"(abia 5% peste cărămidă, dar cu performanță A+++),",
"(only 5% above brick, but with A+++ performance),",
"(à peine 5 % au-dessus de la brique, mais avec performance A+++),",
"(appena il 5% sopra il mattone, ma con prestazioni A+++),",
"(apenas un 5% por encima del ladrillo, pero con rendimiento A+++),",
"(slechts 5% boven baksteen, maar met A+++ prestatie),",
"(nur 5 % über Ziegel, aber mit A+++-Leistung),",
)
_add(
", ca producător, acoperă conformitatea cu marcajul",
", as manufacturer, covers compliance with marking",
", en tant que fabricant, couvre la conformité au marquage",
", come produttore, copre la conformità al marchio",
", como fabricante, cubre la conformidad con el marcado",
", als producent, dekt conformiteit met de markering",
", als Hersteller, deckt die Konformität mit der Kennzeichnung",
)
_add(
"Fabricat cu ⚒ în Europa • ISO 9001 / 14001 / 45001",
"Made with ⚒ in Europe • ISO 9001 / 14001 / 45001",
"Fabriqué avec ⚒ en Europe • ISO 9001 / 14001 / 45001",
"Prodotto con ⚒ in Europa • ISO 9001 / 14001 / 45001",
"Fabricado con ⚒ en Europa • ISO 9001 / 14001 / 45001",
"Gemaakt met ⚒ in Europa • ISO 9001 / 14001 / 45001",
"Hergestellt mit ⚒ in Europa • ISO 9001 / 14001 / 45001",
)
_add(
"Libertate totală la execuție, ca și la proiectare.",
"Total freedom in execution, as in design.",
"Liberté totale à l'exécution, comme à la conception.",
"Libertà totale in esecuzione, come in progettazione.",
"Libertad total en ejecución, como en diseño.",
"Totale vrijheid in uitvoering, net als in ontwerp.",
"Volle Freiheit in der Ausführung, wie in der Planung.",
)
_add(
"MBK 210 era optimizat pentru climat temperat-cald;",
"MBK 210 was optimised for temperate-warm climate;",
"MBK 210 était optimisé pour le climat tempéré-chaud ;",
"MBK 210 era ottimizzato per clima temperato-caldo;",
"MBK 210 estaba optimizado para clima templado-cálido;",
"MBK 210 was geoptimaliseerd voor gematigd-warm klimaat;",
"MBK 210 war für gemäßigt-warmes Klima optimiert;",
)
_add(
"Montaj tâmplărie cu triplu geam — ferestre și uși.",
"Triple-glazed joinery installation — windows and doors.",
"Pose menuiseries triple vitrage — fenêtres et portes.",
"Montaggio serramenti con triplo vetro — finestre e porte.",
"Montaje de carpintería con triple acristalamiento — ventanas y puertas.",
"Montage schrijnwerk met driedubbel glas — ramen en deuren.",
"Montage von Dreifachverglasungs-Schreinerarbeiten — Fenster und Türen.",
)
_add(
"confort termic uniform, fără punți termice majore.",
"uniform thermal comfort, no major thermal bridges.",
"confort thermique uniforme, sans ponts thermiques majeurs.",
"comfort termico uniforme, senza ponti termici importanti.",
"confort térmico uniforme, sin puentes térmicos importantes.",
"uniform thermisch comfort, zonder grote koudebruggen.",
"gleichmäßiger thermischer Komfort, ohne größere Wärmebrücken.",
)
_add(
"« Dacă RE2030 apare în 5 ani și obligă renovări? »",
'"What if RE2030 comes in 5 years and mandates renovations?"',
"« Et si RE2030 arrive dans 5 ans et impose des rénovations ? »",
"« E se RE2030 arriva tra 5 anni e impone ristrutturazioni? »",
"« ¿Y si RE2030 llega en 5 años y obliga a renovaciones? »",
"« Wat als RE2030 over 5 jaar komt en renovaties verplicht? »",
'„Was, wenn RE2030 in 5 Jahren kommt und Renovierungen vorschreibt?"',
)
_add(
"« Nu am interlocutor tehnic când am o întrebare. »",
'"I have no technical contact when I have a question."',
"« Je n'ai pas d'interlocuteur technique quand j'ai une question. »",
"« Non ho un referente tecnico quando ho una domanda. »",
"« No tengo interlocutor técnico cuando tengo una pregunta. »",
"« Ik heb geen technisch aanspreekpunt als ik een vraag heb. »",
'„Ich habe keinen technischen Ansprechpartner, wenn ich eine Frage habe."',
)
_add(
"Care este diferența față de un sistem ICF clasic?",
"What is the difference from a classic ICF system?",
"Quelle est la différence avec un système ICF classique ?",
"Qual è la differenza rispetto a un sistema ICF classico?",
"¿Cuál es la diferencia respecto a un sistema ICF clásico?",
"Wat is het verschil met een klassiek ICF-systeem?",
"Was ist der Unterschied zu einem klassischen ICF-System?",
)
_add(
"Cum trec electricitatea și instalațiile sanitare?",
"How do electricity and plumbing run through?",
"Comment passent l'électricité et les installations sanitaires ?",
"Come passano l'elettricità e gli impianti sanitari?",
"¿Cómo pasan la electricidad y las instalaciones sanitarias?",
"Hoe lopen elektriciteit en sanitaire installaties?",
"Wie verlaufen Elektrizität und Sanitärinstallationen?",
)
_add(
"O singură echipă = marja a 5 echipe — până la 50%",
"One team = the margin of 5 teams — up to 50%",
"Une seule équipe = la marge de 5 équipes — jusqu'à 50 %",
"Una sola squadra = il margine di 5 squadre — fino al 50%",
"Un solo equipo = el margen de 5 equipos — hasta un 50%",
"Eén team = de marge van 5 teams — tot 50%",
"Ein Team = die Marge von 5 Teams — bis zu 50 %",
)
_add(
"Polistibrick — O casă. Un sistem. Fără compromis.",
"Polistibrick — One house. One system. No compromise.",
"Polistibrick — Une maison. Un système. Sans compromis.",
"Polistibrick — Una casa. Un sistema. Senza compromessi.",
"Polistibrick — Una casa. Un sistema. Sin compromisos.",
"Polistibrick — Eén huis. Eén systeem. Geen compromis.",
"Polistibrick — Ein Haus. Ein System. Kein Kompromiss.",
)
_add(
"fabrica din Valencia permitea livrarea în 3 zile;",
"the Valencia plant enabled delivery in 3 days;",
"l'usine de Valence permettait une livraison en 3 jours ;",
"la fabbrica di Valencia consentiva la consegna in 3 giorni;",
"la fábrica de Valencia permitía la entrega en 3 días;",
"de fabriek in Valencia maakte levering in 3 dagen mogelijk;",
"das Werk in Valencia ermöglichte Lieferung in 3 Tagen;",
)
_add(
". Echipa este productivă din prima zi de montaj.",
". The team is productive from day one of assembly.",
". L'équipe est productive dès le premier jour de montage.",
". La squadra è produttiva dal primo giorno di montaggio.",
". El equipo es productivo desde el primer día de montaje.",
". Het team is productief vanaf de eerste montagedag.",
". Das Team ist ab dem ersten Montagetag produktiv.",
)
_add(
". Termenele sunt ferme și garantate contractual.",
". Deadlines are firm and contractually guaranteed.",
". Les délais sont fermes et garantis contractuellement.",
". I termini sono fermi e garantiti contrattualmente.",
". Los plazos son firmes y garantizados contractualmente.",
". Termijnen zijn vast en contractueel gegarandeerd.",
". Fristen sind fest und vertraglich garantiert.",
)
_add(
"Certificat Passivhaus pentru cele 24 de unități.",
"Passivhaus certified for all 24 units.",
"Certifié Passivhaus pour les 24 unités.",
"Certificato Passivhaus per le 24 unità.",
"Certificado Passivhaus para las 24 unidades.",
"Passivhaus-gecertificeerd voor alle 24 eenheden.",
"Passivhaus-zertifiziert für alle 24 Einheiten.",
)
_add(
"Cluj-Napoca, RO · Casă 180 m² · Locuită din 2024",
"Cluj-Napoca, RO · 180 m² home · Occupied since 2024",
"Cluj-Napoca, RO · Maison 180 m² · Habitée depuis 2024",
"Cluj-Napoca, RO · Casa 180 m² · Abitata dal 2024",
"Cluj-Napoca, RO · Casa 180 m² · Habitada desde 2024",
"Cluj-Napoca, RO · Woning 180 m² · Bewoond sinds 2024",
"Cluj-Napoca, RO · Haus 180 m² · Bewohnt seit 2024",
)
_add(
"Depășește RE2020. Atinge standardul casă pasivă.",
"Exceeds RE2020. Meets passive house standard.",
"Dépasse la RE2020. Atteint le standard maison passive.",
"Supera la RE2020. Raggiunge lo standard casa passiva.",
"Supera RE2020. Alcanza el estándar casa pasiva.",
"Overtreft RE2020. Bereikt passiefhuis-standaard.",
"Übertrifft RE2020. Erreicht Passivhaus-Standard.",
)
_add(
"Instalații de ventilație pentru toate unitățile.",
"Ventilation systems for all units.",
"Installations de ventilation pour toutes les unités.",
"Impianti di ventilazione per tutte le unità.",
"Instalaciones de ventilación para todas las unidades.",
"Ventilatie-installaties voor alle eenheden.",
"Lüftungsanlagen für alle Einheiten.",
)
_add(
"bibliotecă completă Revit + ArchiCAD + IFC + DWG",
"complete Revit + ArchiCAD + IFC + DWG library",
"bibliothèque complète Revit + ArchiCAD + IFC + DWG",
"libreria completa Revit + ArchiCAD + IFC + DWG",
"biblioteca completa Revit + ArchiCAD + IFC + DWG",
"volledige Revit + ArchiCAD + IFC + DWG bibliotheek",
"vollständige Revit + ArchiCAD + IFC + DWG Bibliothek",
)
_add(
"« Cum conving clienții și găsesc proiecte noi? »",
'"How do I convince clients and find new projects?"',
"« Comment convaincre les clients et trouver de nouveaux projets ? »",
"« Come convinco i clienti e trovo nuovi progetti? »",
"« ¿Cómo convenzo a los clientes y encuentro proyectos nuevos? »",
"« Hoe overtuig ik klanten en vind ik nieuwe projecten? »",
'„Wie überzeuge ich Kunden und finde neue Projekte?"',
)
_add(
"« Mi-e teamă să pierd bani până învață echipa. »",
'"I am afraid of losing money while the team learns."',
"« J'ai peur de perdre de l'argent pendant que l'équipe apprend. »",
"« Ho paura di perdere soldi finché la squadra impara. »",
"« Me da miedo perder dinero mientras el equipo aprende. »",
"« Ik ben bang geld te verliezen terwijl het team leert. »",
'„Ich habe Angst, Geld zu verlieren, bis das Team gelernt hat."',
)
_add(
"+ monetizare accelerată a capitalului investit.",
"+ accelerated monetisation of invested capital.",
"+ monétisation accélérée du capital investi.",
"+ monetizzazione accelerata del capitale investito.",
"+ monetización acelerada del capital invertido.",
"+ versnelde verzilvering van geïnvesteerd kapitaal.",
"+ beschleunigte Verwertung des investierten Kapitals.",
)
_add(
"+15–25% la revânzare, structura de 2× mai rapid",
"+15–25% on resale, structure 2× faster",
"+15–25 % à la revente, structure 2× plus rapide",
"+15–25% alla rivendita, struttura 2× più veloce",
"+15–25% en reventa, estructura 2× más rápida",
"+15–25% bij doorverkoop, structuur 2× sneller",
"+15–25 % beim Weiterverkauf, Struktur 2× schneller",
)
_add(
"Accept ca datele mele să fie prelucrate conform",
"I accept that my data will be processed in accordance with",
"J'accepte que mes données soient traitées conformément à",
"Accetto che i miei dati siano trattati conformemente a",
"Acepto que mis datos sean tratados conforme a",
"Ik accepteer dat mijn gegevens worden verwerkt conform",
"Ich akzeptiere, dass meine Daten verarbeitet werden gemäß",
)
_add(
"Notă metodă — Polistibrick ca cofraj Eurocode 2",
"Method note — Polistibrick as formwork per Eurocode 2",
"Note méthode — Polistibrick comme coffrage selon Eurocode 2",
"Nota metodo — Polistibrick come cassero secondo Eurocode 2",
"Nota metodológica — Polistibrick como encofrado según Eurocode 2",
"Methode-notitie — Polistibrick als bekisting volgens Eurocode 2",
"Methodenhinweis — Polistibrick als Schalung nach Eurocode 2",
)

def main():
    with open(MISSING, encoding="utf-8") as f:
        missing = json.load(f)
    missing_keys = [k for k in missing if k not in T]
    if missing_keys:
        print(f"ERROR: {len(missing_keys)} keys still untranslated:")
        for k in missing_keys[:20]:
            print(f"  - {k[:100]}...")
        raise SystemExit(1)
    out = {ro: {"en": en, "fr": fr, "it": it, "es": es, "nl": nl, "de": de}
           for ro, (en, fr, it, es, nl, de) in T.items()}
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(out)} translations to {OUTPUT.name}")

if __name__ == "__main__":
    main()
