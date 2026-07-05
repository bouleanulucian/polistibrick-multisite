#!/usr/bin/env python3
"""Build remaining translation entries with exact keys from missing_chunk_1.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MISSING = ROOT / "missing_chunk_1.json"
REST1 = ROOT / "_translations_chunk_1_rest.py"
OUT = ROOT / "_translations_chunk_1_rest2.py"

# (en, fr, it, es, nl, de) — keyed by exact RO phrase from missing_chunk_1.json
EXTRA = {
"cookie-urile neesențiale. Alegerea este înregistrată 13 luni. Pentru a o modifica, ștergeți datele site-ului din setările browserului — bannerul va reapărea.": (
"non-essential cookies. The choice is stored for 13 months. To change it, delete site data from your browser settings — the banner will reappear.",
"les cookies non essentiels. Le choix est enregistré 13 mois. Pour le modifier, supprimez les données du site dans les paramètres du navigateur — la bannière réapparaîtra.",
"i cookie non essenziali. La scelta è registrata per 13 mesi. Per modificarla, cancellate i dati del sito dalle impostazioni del browser — il banner riapparirà.",
"las cookies no esenciales. La elección se registra 13 meses. Para modificarla, elimine los datos del sitio en la configuración del navegador — el banner volverá a aparecer.",
"niet-essentiële cookies. De keuze wordt 13 maanden bewaard. Om te wijzigen, verwijdert u sitegegevens uit de browserinstellingen — de banner verschijnt opnieuw.",
"nicht notwendige Cookies. Die Wahl wird 13 Monate gespeichert. Zum Ändern löschen Sie Website-Daten in den Browser-Einstellungen — das Banner erscheint erneut.",
),
"TBK îmbină OSB de înaltă densitate la exterior cu polistiren EPS-Grafit la interior. Rezultatul: cel mai performant acoperiș pasiv prefabricat de pe piață.": (
"TBK combines high-density OSB on the exterior with graphite EPS polystyrene on the interior. The result: the most performant prefabricated passive roof on the market.",
"TBK combine de l'OSB haute densité à l'extérieur avec du polystyrène EPS-Graphite à l'intérieur. Le résultat : la toiture passive préfabriquée la plus performante du marché.",
"TBK combina OSB ad alta densità all'esterno con polistirene EPS-Grafit all'interno. Il risultato: il tetto passivo prefabbricato più performante sul mercato.",
"TBK combina OSB de alta densidad en el exterior con poliestireno EPS-Grafit en el interior. El resultado: la cubierta pasiva prefabricada más performante del mercado.",
"TBK combineert OSB met hoge dichtheid aan de buitenkant met grafiet-EPS aan de binnenkant. Het resultaat: het best presterende geprefabriceerde passieve dak op de markt.",
"TBK verbindet hochdichtes OSB außen mit Graphit-EPS innen. Das Ergebnis: das leistungsfähigste vorgefertigte Passivdach auf dem Markt.",
),
"În România, factura la energie a devenit un criteriu la fel de important ca prețul casei. O casă pasivă bien construită poate reduce costul de încălzire cu": (
"In Romania, the energy bill has become as important a criterion as the price of the home. A well-built passive house can reduce heating costs by",
"En Roumanie, la facture d'énergie est devenue un critère aussi important que le prix de la maison. Une maison passive bien construite peut réduire le coût de chauffage de",
"In Romania, la bolletta energetica è diventata un criterio importante quanto il prezzo della casa. Una casa passiva ben costruita può ridurre il costo del riscaldamento del",
"En Rumanía, la factura energética se ha convertido en un criterio tan importante como el precio de la casa. Una casa pasiva bien construida puede reducir el coste de calefacción en",
"In Roemenië is de energierekening een criterium geworden dat even belangrijk is als de huisprijs. Een goed gebouwd passiefhuis kan de verwarmingskosten verlagen met",
"In Rumänien ist die Energierechnung ein Kriterium geworden, das genauso wichtig ist wie der Hauspreis. Ein gut gebautes Passivhaus kann die Heizkosten senken um",
),
"Cele mai frecvente întrebări despre sistemul Polistibrick — tehnice, comerciale, garanții și punere în operă. Dacă nu găsiți răspunsul, scrieți-ne direct.": (
"The most frequent questions about the Polistibrick system — technical, commercial, warranties and installation. If you don't find the answer, write to us directly.",
"Les questions les plus fréquentes sur le système Polistibrick — techniques, commerciales, garanties et mise en œuvre. Si vous ne trouvez pas la réponse, écrivez-nous directement.",
"Le domande più frequenti sul sistema Polistibrick — tecniche, commerciali, garanzie e posa in opera. Se non trovate la risposta, scriveteci direttamente.",
"Las preguntas más frecuentes sobre el sistema Polistibrick — técnicas, comerciales, garantías y puesta en obra. Si no encuentra la respuesta, escríbanos directamente.",
"De meest gestelde vragen over het Polistibrick-systeem — technisch, commercieel, garanties en installatie. Als u het antwoord niet vindt, schrijf ons direct.",
"Die häufigsten Fragen zum Polistibrick-System — technisch, kommerziell, Garantien und Einbau. Wenn Sie die Antwort nicht finden, schreiben Sie uns direkt.",
),
"Pentru proiecte care vizează performanță energetică premium. Compatibil certificare Passivhaus Institut. Foarte puțină încălzire necesară (~25 kWh/m²/an).": (
"For projects targeting premium energy performance. Compatible with Passivhaus Institut certification. Very little heating required (~25 kWh/m²/year).",
"Pour les projets visant une performance énergétique premium. Compatible certification Passivhaus Institut. Très peu de chauffage nécessaire (~25 kWh/m²/an).",
"Per progetti che mirano a prestazioni energetiche premium. Compatibile certificazione Passivhaus Institut. Poco riscaldamento necessario (~25 kWh/m²/anno).",
"Para proyectos que buscan rendimiento energético premium. Compatible con certificación Passivhaus Institut. Muy poca calefacción necesaria (~25 kWh/m²/año).",
"Voor projecten met premium energieprestaties. Compatibel met Passivhaus Institut-certificering. Zeer weinig verwarming nodig (~25 kWh/m²/jaar).",
"Für Projekte mit Premium-Energieleistung. Kompatibel mit Passivhaus Institut-Zertifizierung. Sehr wenig Heizung erforderlich (~25 kWh/m²/Jahr).",
),
", cu sediul social la {{company.address_street}}, {{company.address_zip}} {{company.address_city}}, {{company.address_country}}, înregistrată sub numărul": (
", with registered office at {{company.address_street}}, {{company.address_zip}} {{company.address_city}}, {{company.address_country}}, registered under number",
", dont le siège social est situé {{company.address_street}}, {{company.address_zip}} {{company.address_city}}, {{company.address_country}}, enregistrée sous le numéro",
", con sede legale in {{company.address_street}}, {{company.address_zip}} {{company.address_city}}, {{company.address_country}}, registrata con il numero",
", con domicilio social en {{company.address_street}}, {{company.address_zip}} {{company.address_city}}, {{company.address_country}}, registrada con el número",
", met statutaire zetel te {{company.address_street}}, {{company.address_zip}} {{company.address_city}}, {{company.address_country}}, ingeschreven onder nummer",
", mit Sitz in {{company.address_street}}, {{company.address_zip}} {{company.address_city}}, {{company.address_country}}, eingetragen unter der Nummer",
),
"Condițiile care reglementează utilizarea site-ului Polistibrick și relația contractuală dintre noi și clienții noștri. Ultima actualizare: 19 iunie 2026.": (
"The terms governing use of the Polistibrick website and the contractual relationship between us and our clients. Last updated: 19 June 2026.",
"Les conditions régissant l'utilisation du site Polistibrick et la relation contractuelle entre nous et nos clients. Dernière mise à jour : 19 juin 2026.",
"I termini che regolano l'utilizzo del sito Polistibrick e il rapporto contrattuale tra noi e i nostri clienti. Ultimo aggiornamento: 19 giugno 2026.",
"Las condiciones que regulan el uso del sitio Polistibrick y la relación contractual entre nosotros y nuestros clientes. Última actualización: 19 de junio de 2026.",
"De voorwaarden voor het gebruik van de Polistibrick-website en de contractuele relatie tussen ons en onze klanten. Laatst bijgewerkt: 19 juni 2026.",
"Die Bedingungen für die Nutzung der Polistibrick-Website und das Vertragsverhältnis zwischen uns und unseren Kunden. Zuletzt aktualisiert: 19. Juni 2026.",
),
"Vin dintr-o familie de zidari. Am pus piciorul în această lume la opt ani. La doisprezece, îmi petreceam deja verile pe șantiere, alături de bunicul meu,": (
"I come from a family of masons. I set foot in this world at eight. By twelve, I was already spending summers on building sites, alongside my grandfather,",
"Je viens d'une famille de maçons. J'ai mis le pied dans ce monde à huit ans. À douze ans, je passais déjà mes étés sur les chantiers, aux côtés de mon grand-père,",
"Vengo da una famiglia di muratori. Ho messo piede in questo mondo a otto anni. A dodici, passavo già le estati nei cantieri, accanto a mio nonno,",
"Vengo de una familia de albañiles. Puse pie en este mundo a los ocho años. A los doce, ya pasaba los veranos en obras, junto a mi abuelo,",
"Ik kom uit een metselaarsfamilie. Ik zette voet in deze wereld op achtjarige leeftijd. Op mijn twaalfde bracht ik al zomers door op bouwplaatsen, naast mijn grootvader,",
"Ich stamme aus einer Maurerfamilie. Mit acht trat ich in diese Welt. Mit zwölf verbrachte ich bereits Sommer auf Baustellen, an der Seite meines Großvaters,",
),
"Calculele Eurocode 2 rămân identice. Nicio metodă specială de învățat. Nicio surpriză pe șantier. Lucrați exact ca la un proiect tradițional din beton.": (
"Eurocode 2 calculations remain identical. No special method to learn. No surprises on site. You work exactly as on a traditional concrete project.",
"Les calculs Eurocode 2 restent identiques. Aucune méthode spéciale à apprendre. Aucune surprise sur le chantier. Vous travaillez exactement comme sur un projet béton traditionnel.",
"I calcoli Eurocode 2 restano identici. Nessun metodo speciale da imparare. Nessuna sorpresa in cantiere. Lavorate esattamente come in un progetto tradizionale in calcestruzzo.",
"Los cálculos Eurocode 2 permanecen idénticos. Ningún método especial que aprender. Ninguna sorpresa en obra. Trabaja exactamente como en un proyecto tradicional de hormigón.",
"Eurocode 2-berekeningen blijven identiek. Geen speciale methode te leren. Geen verrassingen op de werf. U werkt precies als bij een traditioneel betonproject.",
"Eurocode-2-Berechnungen bleiben identisch. Keine spezielle Methode zu erlernen. Keine Überraschungen auf der Baustelle. Sie arbeiten genau wie bei einem traditionellen Betonprojekt.",
),
"sistem de construcție ICF integrat — cofraj, izolație continuă, structură portantă și suport pentru finisaje reunite într-un singur produs prefabricat.": (
"integrated ICF construction system — formwork, continuous insulation, load-bearing structure and finish support combined in a single prefabricated product.",
"système de construction ICF intégré — coffrage, isolation continue, structure portante et support de finitions réunis en un seul produit préfabriqué.",
"sistema di costruzione ICF integrato — cassero, isolamento continuo, struttura portante e supporto finiture riuniti in un unico prodotto prefabbricato.",
"sistema de construcción ICF integrado — encofrado, aislamiento continuo, estructura portante y soporte de acabados reunidos en un solo producto prefabricado.",
"geïntegreerd ICF-bouwsysteem — bekisting, continue isolatie, draagstructuur en afwerkingsondersteuning verenigd in één geprefabriceerd product.",
"integriertes ICF-Bausystem — Schalung, durchgängige Dämmung, tragende Struktur und Ausbauunterstützung in einem vorgefertigten Produkt vereint.",
),
"Brevetul european care protejează combinația unică EPS + beton armat + sistem de asamblare brevetat. Un sistem pe care nimeni altcineva nu îl fabrică.": (
"The European patent protecting the unique combination of EPS + reinforced concrete + patented assembly system. A system no one else manufactures.",
"Le brevet européen qui protège la combinaison unique EPS + béton armé + système d'assemblage breveté. Un système que personne d'autre ne fabrique.",
"Il brevetto europeo che protegge la combinazione unica EPS + calcestruzzo armato + sistema di assemblaggio brevettato. Un sistema che nessun altro produce.",
"La patente europea que protege la combinación única EPS + hormigón armado + sistema de ensamblaje patentado. Un sistema que nadie más fabrica.",
"Het Europese octrooi dat de unieke combinatie EPS + gewapend beton + gepatenteerd montagesysteem beschermt. Een systeem dat niemand anders produceert.",
"Das europäische Patent, das die einzigartige Kombination EPS + Stahlbeton + patentiertes Montagesystem schützt. Ein System, das niemand sonst herstellt.",
),
"După calcule, a descoperit că diferența de cost între o casă pasivă tradițională (cărămidă + izolație suplimentară) și Polistibrick ajungea la aproape": (
"After calculations, they discovered the cost difference between a traditional passive house (brick + extra insulation) and Polistibrick came to almost",
"Après calculs, il a découvert que la différence de coût entre une maison passive traditionnelle (brique + isolation supplémentaire) et Polistibrick atteignait presque",
"Dopo i calcoli, ha scoperto che la differenza di costo tra una casa passiva tradizionale (mattone + isolamento aggiuntivo) e Polistibrick arrivava a quasi",
"Tras los cálculos, descubrió que la diferencia de coste entre una casa pasiva tradicional (ladrillo + aislamiento extra) y Polistibrick llegaba a casi",
"Na berekeningen ontdekte hij dat het kostenverschil tussen een traditioneel passiefhuis (baksteen + extra isolatie) en Polistibrick bijna",
"Nach Berechnungen stellte er fest, dass die KostenDifferenz zwischen einem traditionellen Passivhaus (Ziegel + Zusatzdämmung) und Polistibrick fast",
),
"Litigiile se soluționează pe cale amiabilă, în primă instanță. În caz contrar, instanțele de la sediul social al Polistibrick România sunt competente.": (
"Disputes are resolved amicably in the first instance. Otherwise, the courts at the registered office of Polistibrick Romania have jurisdiction.",
"Les litiges se règlent à l'amiable, en première instance. À défaut, les tribunaux du siège social de Polistibrick Roumanie sont compétents.",
"Le controversie si risolvono bonariamente, in prima istanza. In caso contrario, sono competenti i tribunali della sede legale di Polistibrick Romania.",
"Las disputas se resuelven amistosamente, en primera instancia. En caso contrario, son competentes los tribunales de la sede social de Polistibrick Rumanía.",
"Geschillen worden in eerste instantie minnelijk opgelost. Anders zijn de rechtbanken bij de statutaire zetel van Polistibrick Roemenië bevoegd.",
"Streitigkeiten werden zunächst gütlich beigelegt. Andernfalls sind die Gerichte am Sitz von Polistibrick Rumänien zuständig.",
),
"Toate sistemele clasice de acoperiș cer +10-15 cm de vată minerală pentru a deveni pasive. TBK e gata din fabrică — un singur panou, un singur produs.": (
"All classic roof systems require +10-15 cm of mineral wool to become passive. TBK is ready from the factory — one panel, one product.",
"Tous les systèmes de toiture classiques exigent +10-15 cm de laine minérale pour devenir passifs. TBK est prêt en usine — un seul panneau, un seul produit.",
"Tutti i sistemi di copertura classici richiedono +10-15 cm di lana minerale per diventare passivi. TBK è pronto in fabbrica — un solo pannello, un solo prodotto.",
"Todos los sistemas de cubierta clásicos requieren +10-15 cm de lana mineral para ser pasivos. TBK está listo de fábrica — un solo panel, un solo producto.",
"Alle klassieke daksystemen vereisen +10-15 cm steenwol om passief te worden. TBK is klaar uit de fabriek — één paneel, één product.",
"Alle klassischen Dachsysteme erfordern +10-15 cm Mineralfaser, um passiv zu werden. TBK ist ab Werk fertig — ein Paneel, ein Produkt.",
),
"care a redefinit ce înseamnă o casă premium: pasivă din concepție, fără facturi de încălzire sau aer condiționat, construită în săptămâni, nu în ani.": (
"that redefined what a premium home means: passive by design, no heating or air conditioning bills, built in weeks, not years.",
"qui a redéfini ce qu'est une maison haut de gamme : passive dès la conception, sans factures de chauffage ou de climatisation, construite en semaines, pas en années.",
"che ha ridefinito cosa significa casa premium: passiva fin dalla concezione, senza bollette di riscaldamento o aria condizionata, costruita in settimane, non anni.",
"que redefinió qué significa una casa premium: pasiva desde el diseño, sin facturas de calefacción o aire acondicionado, construida en semanas, no años.",
"dat herdefinieerde wat een premium huis betekent: passief by design, geen verwarmings- of airconditioningrekeningen, gebouwd in weken, niet jaren.",
"das neu definierte, was ein Premium-Haus bedeutet: passiv von Anfang an, keine Heiz- oder Klimarechnungen, in Wochen gebaut, nicht Jahren.",
),
"Structura se montează de 3 ori mai repede decât zidăria clasică. Vă mutați în câteva luni, nu în câțiva ani. Mai puțin stres, mai puține întârzieri.": (
"The structure installs 3 times faster than classic masonry. You move in within months, not years. Less stress, fewer delays.",
"La structure se monte 3 fois plus vite que la maçonnerie classique. Vous emménagez en quelques mois, pas en quelques années. Moins de stress, moins de retards.",
"La struttura si monta 3 volte più velocemente della muratura classica. Vi trasferite in pochi mesi, non anni. Meno stress, meno ritardi.",
"La estructura se monta 3 veces más rápido que la mampostería clásica. Se muda en meses, no años. Menos estrés, menos retrasos.",
"De structuur monteert 3× sneller dan klassiek metselwerk. U verhuist binnen maanden, niet jaren. Minder stress, minder vertragingen.",
"Die Struktur montiert sich 3× schneller als klassisches Mauerwerk. Sie ziehen in Monaten ein, nicht Jahren. Weniger Stress, weniger Verzögerungen.",
),
"Cum contribuie Polistibrick la o construcție mai durabilă. Date concrete despre emisii, ciclul de viață și impactul real al unei case Polistibrick.": (
"How Polistibrick contributes to more sustainable construction. Concrete data on emissions, life cycle and the real impact of a Polistibrick home.",
"Comment Polistibrick contribue à une construction plus durable. Données concrètes sur les émissions, le cycle de vie et l'impact réel d'une maison Polistibrick.",
"Come Polistibrick contribuisce a una costruzione più sostenibile. Dati concreti su emissioni, ciclo di vita e impatto reale di una casa Polistibrick.",
"Cómo Polistibrick contribuye a una construcción más sostenible. Datos concretos sobre emisiones, ciclo de vida e impacto real de una casa Polistibrick.",
"Hoe Polistibrick bijdraagt aan duurzamer bouwen. Concrete gegevens over emissies, levenscyclus en de werkelijke impact van een Polistibrick-huis.",
"Wie Polistibrick zu nachhaltigerem Bau beiträgt. Konkrete Daten zu Emissionen, Lebenszyklus und der tatsächlichen Wirkung eines Polistibrick-Hauses.",
),
". Păstrați calculele Eurocode 2 obișnuite. Descărcare de sarcină, dimensionare armături, verificări ELU/ELS — exact ca la orice proiect din beton.": (
". Keep your usual Eurocode 2 calculations. Load transfer, rebar sizing, ULS/SLS checks — exactly as on any concrete project.",
". Conservez vos calculs Eurocode 2 habituels. Descente de charges, dimensionnement armatures, vérifications ELU/ELS — exactement comme sur tout projet béton.",
". Mantenete i calcoli Eurocode 2 usuali. Scarico carichi, dimensionamento armature, verifiche SLU/SLE — esattamente come in qualsiasi progetto in calcestruzzo.",
". Mantenga sus cálculos Eurocode 2 habituales. Descarga de cargas, dimensionado de armaduras, comprobaciones ELU/ELS — exactamente como en cualquier proyecto de hormigón.",
". Behoud uw gebruikelijke Eurocode 2-berekeningen. Belastingoverdracht, wapening dimensioneren, UGT/BGT-controles — precies als bij elk betonproject.",
". Behalten Sie Ihre üblichen Eurocode-2-Berechnungen. Lastabtragung, Bewehrungsbemessung, Grenzzustände — genau wie bei jedem Betonprojekt.",
),
"Beton monolitic turnat într-o singură etapă — fără rosturi, fără puncte slabe. Trece testul Blower Door (n50 &lt; 0,6) fără membrane suplimentare.": (
"Monolithic concrete poured in a single stage — no joints, no weak points. Passes the Blower Door test (n50 &lt; 0.6) without additional membranes.",
"Béton monolithique coulé en une seule étape — sans joints, sans points faibles. Passe le test Blower Door (n50 &lt; 0,6) sans membranes supplémentaires.",
"Calcestruzzo monolitico gettato in un'unica fase — senza giunti, senza punti deboli. Supera il test Blower Door (n50 &lt; 0,6) senza membrane aggiuntive.",
"Hormigón monolítico vertido en una sola fase — sin juntas, sin puntos débiles. Supera la prueba Blower Door (n50 &lt; 0,6) sin membranas adicionales.",
"Monolithisch beton in één fase gestort — geen voegen, geen zwakke punten. Slaagt voor de Blower Door-test (n50 &lt; 0,6) zonder extra membranen.",
"Monolithischer Beton in einer Phase gegossen — ohne Fugen, ohne Schwachstellen. Besteht den Blower-Door-Test (n50 &lt; 0,6) ohne zusätzliche Membranen.",
),
". Pereți cu izolație integrată, planșee cu defazaj termic, acoperișe Passivhaus livrate din fabrică. Trei elemente prefabricate, o casă întreagă.": (
". Walls with integrated insulation, floors with thermal lag, Passivhaus roofs delivered from the factory. Three prefabricated elements, one complete home.",
". Murs à isolation intégrée, planchers à déphasage thermique, toitures Passivhaus livrées en usine. Trois éléments préfabriqués, une maison entière.",
". Pareti con isolamento integrato, solai con sfasamento termico, tetti Passivhaus consegnati in fabbrica. Tre elementi prefabbricati, un'intera casa.",
". Muros con aislamiento integrado, forjados con desfase térmico, cubiertas Passivhaus entregadas de fábrica. Tres elementos prefabricados, una casa entera.",
". Muren met geïntegreerde isolatie, vloeren met thermische vertraging, Passivhaus-daken uit de fabriek. Drie geprefabriceerde elementen, één compleet huis.",
". Wände mit integrierter Dämmung, Decken mit thermischer Phasenverschiebung, Passivhaus-Dächer ab Werk. Drei vorgefertigte Elemente, ein ganzes Haus.",
),
"De la fundație la cofraj închis. Întregul proces în câteva săptămâni, cu doar 2–3 persoane pe șantier — fără mortar și fără pierderi de izolație.": (
"From foundation to closed formwork. The entire process in a few weeks, with just 2–3 people on site — no mortar and no insulation losses.",
"De la fondation au coffrage fermé. L'ensemble du processus en quelques semaines, avec seulement 2–3 personnes sur le chantier — sans mortier ni pertes d'isolation.",
"Dalla fondazione al cassero chiuso. L'intero processo in poche settimane, con solo 2–3 persone in cantiere — senza malta e senza perdite di isolamento.",
"Desde cimentación hasta encofrado cerrado. Todo el proceso en pocas semanas, con solo 2–3 personas en obra — sin mortero ni pérdidas de aislamiento.",
"Van fundering tot gesloten bekisting. Het hele proces in enkele weken, met slechts 2–3 personen op de werf — zonder mortel en zonder isolatieverlies.",
"Von der Fundament bis zum geschlossenen Schalung. Der gesamte Prozess in wenigen Wochen, mit nur 2–3 Personen auf der Baustelle — ohne Mörtel und ohne Dämmverluste.",
),
"Electricitate, instalații sanitare, încălzire, VMC cu recuperare de căldură. Buget mediu 80–150 €/m² casă, în funcție de nivelul tehnologic ales.": (
"Electricity, plumbing, heating, MVHR with heat recovery. Average budget €80–150/m² of house, depending on technology level chosen.",
"Électricité, installations sanitaires, chauffage, VMC avec récupération de chaleur. Budget moyen 80–150 €/m² maison, selon le niveau technologique choisi.",
"Elettricità, impianti sanitari, riscaldamento, VMC con recupero calore. Budget medio 80–150 €/m² casa, in base al livello tecnologico scelto.",
"Electricidad, instalaciones sanitarias, calefacción, VMC con recuperación de calor. Presupuesto medio 80–150 €/m² casa, según nivel tecnológico elegido.",
"Elektriciteit, sanitaire installaties, verwarming, WTW met warmteterugwinning. Gemiddeld budget €80–150/m² huis, afhankelijk van gekozen technologieniveau.",
"Strom, Sanitär, Heizung, Lüftung mit Wärmerückgewinnung. Durchschnittsbudget 80–150 €/m² Haus, je nach gewähltem Technologieniveau.",
),
"Integrați în structura proprie valoarea adăugată a izolației exterioare, finisajelor și acusticii. Maximizați câștigul pe metru pătrat construit.": (
"Integrate into your own structure the added value of external insulation, finishes and acoustics. Maximise gain per square metre built.",
"Intégrez dans votre propre structure la valeur ajoutée de l'isolation extérieure, des finitions et de l'acoustique. Maximisez le gain au mètre carré construit.",
"Integrate nella vostra struttura il valore aggiunto dell'isolamento esterno, finiture e acustica. Massimizzate il guadagno per metro quadrato costruito.",
"Integre en su propia estructura el valor añadido del aislamiento exterior, acabados y acústica. Maximice la ganancia por metro cuadrado construido.",
"Integreer in uw eigen structuur de meerwaarde van buitenisolatie, afwerking en akoestiek. Maximaliseer winst per vierkante meter gebouwd.",
"Integrieren Sie in Ihre eigene Struktur den Mehrwert von Außendämmung, Ausbau und Akustik. Maximieren Sie den Gewinn pro Quadratmeter gebaut.",
),
"Reducerea consumului de energie cu 70 % înseamnă mai puține emisii pe durata de viață a casei. Construim case care nu mai poluează odată locuite.": (
"Reducing energy consumption by 70% means fewer emissions over the home's lifetime. We build homes that stop polluting once occupied.",
"La réduction de la consommation d'énergie de 70 % signifie moins d'émissions sur la durée de vie de la maison. Nous construisons des maisons qui ne polluent plus une fois habitées.",
"Ridurre il consumo energetico del 70% significa meno emissioni per tutta la vita della casa. Costruiamo case che smettono di inquinare una volta abitate.",
"Reducir el consumo energético un 70% significa menos emisiones durante la vida útil de la casa. Construimos casas que dejan de contaminar una vez habitadas.",
"Energieverbruik met 70% verminderen betekent minder emissies over de levensduur van het huis. Wij bouwen huizen die stoppen met vervuilen zodra ze bewoond zijn.",
"Energieverbrauch um 70 % zu senken bedeutet weniger Emissionen über die Lebensdauer des Hauses. Wir bauen Häuser, die nach dem Bezug nicht mehr verschmutzen.",
),
"Sistemul a fost validat de Oficiul European al Brevetelor — am demonstrat că tehnologia este nouă, inventivă și aplicabilă la scară industrială.": (
"The system was validated by the European Patent Office — we demonstrated the technology is new, inventive and applicable at industrial scale.",
"Le système a été validé par l'Office Européen des Brevets — nous avons démontré que la technologie est nouvelle, inventive et applicable à l'échelle industrielle.",
"Il sistema è stato convalidato dall'Ufficio Europeo dei Brevetti — abbiamo dimostrato che la tecnologia è nuova, inventiva e applicabile su scala industriale.",
"El sistema fue validado por la Oficina Europea de Patentes — demostramos que la tecnología es nueva, inventiva y aplicable a escala industrial.",
"Het systeem werd gevalideerd door het Europees Octrooibureau — wij toonden aan dat de technologie nieuw, inventief en toepasbaar op industriële schaal is.",
"Das System wurde vom Europäischen Patentamt validiert — wir haben nachgewiesen, dass die Technologie neu, erfinderisch und industriell anwendbar ist.",
),
"Clasa de reacție la foc cea mai înaltă — necombustibil. Plăcile din fibrocement A1 nu contribuie la incendiu și frânează propagarea flăcărilor.": (
"The highest fire reaction class — non-combustible. A1 fibre-cement panels do not contribute to fire and slow flame propagation.",
"La classe de réaction au feu la plus élevée — non combustible. Les plaques en fibro-ciment A1 ne contribuent pas à l'incendie et freinent la propagation des flammes.",
"La classe di reazione al fuoco più alta — non combustibile. Le lastre in fibrocemento A1 non contribuiscono all'incendio e frenano la propagazione delle fiamme.",
"La clase de reacción al fuego más alta — no combustible. Las placas de fibrocemento A1 no contribuyen al incendio y frenan la propagación de las llamas.",
"De hoogste brandreactieklasse — onbrandbaar. A1 vezelcementplaten dragen niet bij aan brand en remmen vlammenspreiding.",
"Die höchste Brandreaktionsklasse — nicht brennbar. A1-Faserzementplatten tragen nicht zur Brandentstehung bei und bremsen Flammenausbreitung.",
),
"Cum colectăm, utilizăm și protejăm datele dumneavoastră personale. Conform Regulamentului UE 2016/679 (GDPR). Ultima actualizare: 3 iulie 2026.": (
"How we collect, use and protect your personal data. In accordance with EU Regulation 2016/679 (GDPR). Last updated: 3 July 2026.",
"Comment nous collectons, utilisons et protégeons vos données personnelles. Conformément au Règlement UE 2016/679 (RGPD). Dernière mise à jour : 3 juillet 2026.",
"Come raccogliamo, utilizziamo e proteggiamo i vostri dati personali. Conforme al Regolamento UE 2016/679 (GDPR). Ultimo aggiornamento: 3 luglio 2026.",
"Cómo recopilamos, utilizamos y protegemos sus datos personales. Conforme al Reglamento UE 2016/679 (RGPD). Última actualización: 3 de julio de 2026.",
"Hoe wij uw persoonsgegevens verzamelen, gebruiken en beschermen. Conform EU-Verordening 2016/679 (AVG). Laatst bijgewerkt: 3 juli 2026.",
"Wie wir Ihre personenbezogenen Daten erheben, nutzen und schützen. Gemäß EU-Verordnung 2016/679 (DSGVO). Zuletzt aktualisiert: 3. Juli 2026.",
),
"Din familie de zidari la invenția sistemului 5-în-1. Omul din spatele Polistibrick, povestea și promisiunea sa: să schimbe modul de a construi.": (
"From a mason's family to the invention of the 5-in-1 system. The man behind Polistibrick, his story and his promise: to change the way we build.",
"D'une famille de maçons à l'invention du système 5-en-1. L'homme derrière Polistibrick, son histoire et sa promesse : changer la façon de construire.",
"Da famiglia di muratori all'invenzione del sistema 5-in-1. L'uomo dietro Polistibrick, la sua storia e la sua promessa: cambiare il modo di costruire.",
"De familia de albañiles a la invención del sistema 5-en-1. El hombre detrás de Polistibrick, su historia y su promesa: cambiar la forma de construir.",
"Van metselaarsfamilie tot de uitvinding van het 5-in-1-systeem. De man achter Polistibrick, zijn verhaal en zijn belofte: de manier van bouwen veranderen.",
"Von einer Maurerfamilie zur Erfindung des 5-in-1-Systems. Der Mann hinter Polistibrick, seine Geschichte und sein Versprechen: die Art zu bauen verändern.",
),
"Medie pe 24 de luni, iarnă la −15 °C inclusă. Casă de 180 m² cu 4 persoane, mașină electrică încărcată acasă, 2 calculatoare pornite permanent.": (
"Average over 24 months, winter at −15 °C included. 180 m² home with 4 people, electric car charged at home, 2 computers running permanently.",
"Moyenne sur 24 mois, hiver à −15 °C inclus. Maison de 180 m² avec 4 personnes, voiture électrique chargée à domicile, 2 ordinateurs allumés en permanence.",
"Media su 24 mesi, inverno a −15 °C incluso. Casa di 180 m² con 4 persone, auto elettrica caricata a casa, 2 computer accesi permanentemente.",
"Media de 24 meses, invierno a −15 °C incluido. Casa de 180 m² con 4 personas, coche eléctrico cargado en casa, 2 ordenadores encendidos permanentemente.",
"Gemiddelde over 24 maanden, winter bij −15 °C inbegrepen. Huis van 180 m² met 4 personen, elektrische auto thuis geladen, 2 computers permanent aan.",
"Durchschnitt über 24 Monate, Winter bei −15 °C inbegriffen. 180 m² Haus mit 4 Personen, Elektroauto zu Hause geladen, 2 Computer dauerhaft eingeschaltet.",
),
"(adresă IP) pentru preselectarea celui mai apropiat birou Polistibrick. Activat numai dacă faceți clic pe «Acceptă» în bannerul de cookie-uri.": (
"(IP address) for preselecting the nearest Polistibrick office. Activated only if you click «Accept» in the cookie banner.",
"(adresse IP) pour présélectionner le bureau Polistibrick le plus proche. Activé uniquement si vous cliquez sur « Accepter » dans la bannière cookies.",
"(indirizzo IP) per preselezionare l'ufficio Polistibrick più vicino. Attivato solo se cliccate « Accetta » nel banner cookie.",
"(dirección IP) para preseleccionar la oficina Polistibrick más cercana. Activado solo si hace clic en « Aceptar » en el banner de cookies.",
"(IP-adres) voor het voorselecteren van het dichtstbijzijnde Polistibrick-kantoor. Alleen geactiveerd als u op « Accepteren » klikt in de cookiebanner.",
"(IP-Adresse) zur Vorauswahl des nächsten Polistibrick-Büros. Nur aktiviert, wenn Sie im Cookie-Banner auf « Akzeptieren » klicken.",
),
"Tehnologie solidă de beton armat turnat în cofraj izolant calibrat din fabrică. Riscurile de tăiere greșită și defecte termice sunt eliminate.": (
"Solid reinforced concrete technology poured in factory-calibrated insulating formwork. Risks of incorrect cutting and thermal defects are eliminated.",
"Technologie solide de béton armé coulé dans un coffrage isolant calibré en usine. Les risques de mauvaise découpe et de défauts thermiques sont éliminés.",
"Tecnologia solida di calcestruzzo armato gettato in cassero isolante calibrato in fabbrica. I rischi di taglio errato e difetti termici sono eliminati.",
"Tecnología sólida de hormigón armado vertido en encofrado aislante calibrado en fábrica. Se eliminan los riesgos de corte incorrecto y defectos térmicos.",
"Solide gewapend-betontechnologie gestort in fabriek-gekalibreerde isolerende bekisting. Risico's op verkeerd snijden en thermische defecten zijn geëlimineerd.",
"Solide Stahlbetontechnologie gegossen in werkskalibrierter Wärmedämmschalung. Risiken falscher Schnitte und thermischer Mängel sind eliminiert.",
),
"Pentru proiecte care vizează conformitatea reglementară RE2020. Toate avantajele Polistibrick (A1 foc, acustic 52 dB, hidrofug, antiseismic).": (
"For projects targeting RE2020 regulatory compliance. All Polistibrick advantages (A1 fire, 52 dB acoustic, waterproof, seismic-resistant).",
"Pour les projets visant la conformité réglementaire RE2020. Tous les avantages Polistibrick (A1 feu, acoustique 52 dB, hydrofuge, parasismique).",
"Per progetti che mirano alla conformità regolamentare RE2020. Tutti i vantaggi Polistibrick (A1 fuoco, acustico 52 dB, impermeabile, antisismico).",
"Para proyectos que buscan conformidad normativa RE2020. Todas las ventajas Polistibrick (A1 fuego, acústico 52 dB, impermeable, antisísmico).",
"Voor projecten met RE2020-regelgevingsconformiteit. Alle Polistibrick-voordelen (A1 brand, 52 dB akoestisch, waterdicht, aardbevingsbestendig).",
"Für Projekte mit RE2020-Regelkonformität. Alle Polistibrick-Vorteile (A1 Feuer, 52 dB Akustik, wasserdicht, erdbebensicher).",
),
"Redirecționăm cererile de ofertă geolocalizate de la proprietari și dezvoltatori din regiunea dumneavoastră direct către firma dumneavoastră.": (
"We redirect geolocated quote requests from owners and developers in your region directly to your company.",
"Nous redirigeons les demandes de devis géolocalisées des propriétaires et promoteurs de votre région directement vers votre entreprise.",
"Reindirizziamo le richieste di preventivo geolocalizzate da proprietari e sviluppatori della vostra regione direttamente alla vostra azienda.",
"Redirigimos las solicitudes de presupuesto geolocalizadas de propietarios y promotores de su región directamente a su empresa.",
"Wij sturen geolokaliseerde offerteaanvragen van eigenaren en ontwikkelaars in uw regio rechtstreeks door naar uw bedrijf.",
"Wir leiten geolokalisierte Angebotsanfragen von Eigentümern und Bauträgern in Ihrer Region direkt an Ihr Unternehmen weiter.",
),
"Construcția a început în martie 2023. Tâmplăria a sosit cu o săptămână întârziere, dar restul a decurs conform planului. Mutare: 1 mai 2023.": (
"Construction started in March 2023. Joinery arrived a week late, but the rest proceeded according to plan. Move-in: 1 May 2023.",
"La construction a commencé en mars 2023. La menuiserie est arrivée avec une semaine de retard, mais le reste s'est déroulé selon le plan. Emménagement : 1er mai 2023.",
"La costruzione è iniziata a marzo 2023. Serramenti arrivati con una settimana di ritardo, ma il resto è proceduto secondo piano. Trasloco: 1 maggio 2023.",
"La construcción comenzó en marzo de 2023. La carpintería llegó con una semana de retraso, pero el resto siguió el plan. Mudanza: 1 de mayo de 2023.",
"De bouw startte in maart 2023. Timmerwerk kwam een week te laat, maar de rest verliep volgens plan. Verhuizing: 1 mei 2023.",
"Der Bau begann im März 2023. Die Tischlerarbeiten kamen eine Woche zu spät, der Rest verlief planmäßig. Einzug: 1. Mai 2023.",
),
"Informații de reglementare despre editorul și gazda web a site-ului polistibrick.ro, conform Legii nr. 365/2002 privind comerțul electronic.": (
"Regulatory information about the publisher and web host of polistibrick.ro, pursuant to Law no. 365/2002 on electronic commerce.",
"Informations réglementaires sur l'éditeur et l'hébergeur web du site polistibrick.ro, conformément à la Loi n° 365/2002 sur le commerce électronique.",
"Informazioni regolamentari sull'editore e l'host web del sito polistibrick.ro, conforme alla Legge n. 365/2002 sul commercio elettronico.",
"Información regulatoria sobre el editor y el host web del sitio polistibrick.ro, conforme a la Ley n.º 365/2002 sobre comercio electrónico.",
"Regelgevende informatie over de uitgever en webhost van polistibrick.ro, conform Wet nr. 365/2002 betreffende elektronische handel.",
"Regulatorische Informationen über Herausgeber und Webhost von polistibrick.ro gemäß Gesetz Nr. 365/2002 über den elektronischen Handel.",
),
"Medie electricitate pe 18 luni (vară inclusă). Casă de 280 m² cu 3 persoane. Aer condiționat niciodată pornit. Apă caldă din panouri solare.": (
"Average electricity over 18 months (summer included). 280 m² home with 3 people. Air conditioning never turned on. Hot water from solar panels.",
"Moyenne électricité sur 18 mois (été inclus). Maison de 280 m² avec 3 personnes. Climatisation jamais allumée. Eau chaude via panneaux solaires.",
"Media elettricità su 18 mesi (estate inclusa). Casa di 280 m² con 3 persone. Aria condizionata mai accesa. Acqua calda da pannelli solari.",
"Media de electricidad en 18 meses (verano incluido). Casa de 280 m² con 3 personas. Aire acondicionado nunca encendido. Agua caliente de paneles solares.",
"Gemiddeld stroomverbruik over 18 maanden (zomer inbegrepen). Huis van 280 m² met 3 personen. Airconditioning nooit aangezet. Warm water via zonnepanelen.",
"Durchschnittlicher Stromverbrauch über 18 Monate (Sommer inbegriffen). 280 m² Haus mit 3 Personen. Klimaanlage nie eingeschaltet. Warmwasser über Solarpanels.",
),
"Pentru fiecare proiect, planuri de montaj detaliate — fiecare panou numerotat și marcat, pentru o asamblare rapidă și fără erori pe șantier.": (
"For each project, detailed installation plans — each panel numbered and marked, for fast, error-free assembly on site.",
"Pour chaque projet, plans de montage détaillés — chaque panneau numéroté et marqué, pour un assemblage rapide et sans erreur sur le chantier.",
"Per ogni progetto, piani di montaggio dettagliati — ogni pannello numerato e marcato, per un assemblaggio rapido e senza errori in cantiere.",
"Para cada proyecto, planos de montaje detallados — cada panel numerado y marcado, para un montaje rápido y sin errores en obra.",
"Voor elk project gedetailleerde montageplannen — elk paneel genummerd en gemarkeerd, voor snelle foutloze montage op de werf.",
"Für jedes Projekt detaillierte Montagepläne — jedes Paneel nummeriert und markiert, für schnelle fehlerfreie Montage auf der Baustelle.",
),
"Pereții EPS sunt ridicați și fixați pe fundație cu sprijiniri laterale din lemn. Asamblare la uscat: fără mortar, fără pierderi de izolație.": (
"EPS walls are raised and fixed to the foundation with lateral wooden supports. Dry assembly: no mortar, no insulation losses.",
"Les murs EPS sont levés et fixés sur la fondation avec des supports latéraux en bois. Assemblage à sec : sans mortier, sans pertes d'isolation.",
"I muri EPS sono sollevati e fissati sulla fondazione con supporti laterali in legno. Assemblaggio a secco: senza malta, senza perdite di isolamento.",
"Los muros EPS se levantan y fijan a la cimentación con apoyos laterales de madera. Montaje en seco: sin mortero, sin pérdidas de aislamiento.",
"EPS-muren worden opgetrokken en op de fundering bevestigd met houten steunen. Droge montage: geen mortel, geen isolatieverlies.",
"EPS-Wände werden auf die Fundament gehoben und mit seitlichen Holzstützen befestigt. Trockenmontage: kein Mörtel, kein Dämmverlust.",
),
}


def py_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def format_entry(key: str, vals: tuple) -> str:
    lines = [f"{py_str(key)}: ("]
    for v in vals:
        lines.append(f"{py_str(v)},")
    lines.append("),")
    return "\n".join(lines)


def main():
    missing = json.loads(MISSING.read_text(encoding="utf-8"))
    ns = {}
    exec(REST1.read_text(encoding="utf-8"), ns)
    done = set(list(missing.keys())[:10]) | set(ns["REST"].keys())
    remaining = [k for k in missing if k not in done]
    missing_extra = [k for k in remaining if k not in EXTRA]
    if missing_extra:
        print(f"WARNING: {len(missing_extra)} keys not in EXTRA yet")
        for k in missing_extra[:5]:
            print(" ", k[:80])
    body = ["REST2 = {"]
    for k in remaining:
        if k in EXTRA:
            body.append(format_entry(k, EXTRA[k]))
    body.append("}")
    OUT.write_text("\n".join(body) + "\n", encoding="utf-8")
    print(f"Wrote {sum(1 for k in remaining if k in EXTRA)} entries to {OUT.name}")


if __name__ == "__main__":
    main()
