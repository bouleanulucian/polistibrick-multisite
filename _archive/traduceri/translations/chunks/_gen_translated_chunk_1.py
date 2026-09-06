#!/usr/bin/env python3
"""Generate translated_chunk_1.json from missing_chunk_1.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MISSING = ROOT / "missing_chunk_1.json"
OUTPUT = ROOT / "translated_chunk_1.json"

# Each entry: (en, fr, it, es, nl, de)
T = {
": un perete nu lasă aerul să intre. Concret, pereții Polistibrick gestionează vaporii de apă controlat (μ = 30-70), suficient pentru a evita condensul fără a pierde căldura. EPS-ul nu absoarbe apă (celule închise) — deci nici o problemă de umiditate sau mucegai, și o durată de viață estimată la peste 50 de ani. De reținut: instalarea unei": (
": a wall that keeps air out. Specifically, Polistibrick walls manage water vapour in a controlled way (μ = 30-70), enough to prevent condensation without losing heat. EPS does not absorb water (closed cells) — so no humidity or mould issues, and an estimated lifespan of over 50 years. Please note: installing a",
": un mur qui ne laisse pas entrer l'air. Concrètement, les murs Polistibrick gèrent la vapeur d'eau de façon contrôlée (μ = 30-70), suffisamment pour éviter la condensation sans perdre la chaleur. L'EPS n'absorbe pas l'eau (cellules fermées) — donc aucun problème d'humidité ou de moisissure, et une durée de vie estimée à plus de 50 ans. À noter : l'installation d'une",
": un muro che non lascia entrare l'aria. In concreto, i muri Polistibrick gestiscono il vapore acqueo in modo controllato (μ = 30-70), sufficiente per evitare la condensa senza perdere calore. L'EPS non assorbe acqua (celle chiuse) — quindi nessun problema di umidità o muffa, e una durata di vita stimata oltre 50 anni. Da ricordare: l'installazione di una",
": un muro que no deja entrar el aire. En concreto, los muros Polistibrick gestionan el vapor de agua de forma controlada (μ = 30-70), suficiente para evitar la condensación sin perder calor. El EPS no absorbe agua (células cerradas) — por lo tanto, ningún problema de humedad o moho, y una vida útil estimada de más de 50 años. A tener en cuenta: la instalación de una",
": een muur die geen lucht binnenlaat. Concreet beheren Polistibrick-muren waterdamp gecontroleerd (μ = 30-70), genoeg om condensatie te voorkomen zonder warmte te verliezen. EPS absorbeert geen water (gesloten cellen) — dus geen vocht- of schimmelproblemen, en een geschatte levensduur van meer dan 50 jaar. Let op: het installeren van een",
": eine Wand, die keine Luft eindringen lässt. Konkret steuern Polistibrick-Wände Wasserdampf kontrolliert (μ = 30-70), ausreichend, um Kondensation zu vermeiden, ohne Wärme zu verlieren. EPS absorbiert kein Wasser (geschlossene Zellen) — also keine Feuchtigkeits- oder Schimmelprobleme, und eine geschätzte Lebensdauer von über 50 Jahren. Zu beachten: die Installation einer",
),
"La Valencia, vara durează 5 luni cu temperaturi ce depășesc 35 °C. Aerul condiționat merge non-stop în casele clasice — facturi de peste 400 €/lună vara. Familia [Nume] a construit cu Polistibrick MBK 210 (versiune pentru climat temperat-cald) și TBK 250. După 18 luni de ocupare, aerul condiționat nu a fost pornit niciodată.": (
"In Valencia, summer lasts 5 months with temperatures exceeding 35 °C. Air conditioning runs non-stop in conventional homes — bills of over €400/month in summer. The [Nume] family built with Polistibrick MBK 210 (temperate-warm climate version) and TBK 250. After 18 months of occupancy, the air conditioning was never turned on.",
"À Valence, l'été dure 5 mois avec des températures dépassant 35 °C. La climatisation tourne en permanence dans les maisons classiques — factures de plus de 400 €/mois en été. La famille [Nume] a construit avec Polistibrick MBK 210 (version climat tempéré-chaud) et TBK 250. Après 18 mois d'occupation, la climatisation n'a jamais été allumée.",
"A Valencia, l'estate dura 5 mesi con temperature superiori a 35 °C. L'aria condizionata funziona ininterrottamente nelle case tradizionali — bollette oltre 400 €/mese in estate. La famiglia [Nume] ha costruito con Polistibrick MBK 210 (versione clima temperato-caldo) e TBK 250. Dopo 18 mesi di occupazione, l'aria condizionata non è mai stata accesa.",
"En Valencia, el verano dura 5 meses con temperaturas que superan los 35 °C. El aire acondicionado funciona sin parar en las casas clásicas — facturas de más de 400 €/mes en verano. La familia [Nume] construyó con Polistibrick MBK 210 (versión clima templado-cálido) y TBK 250. Tras 18 meses de ocupación, el aire acondicionado nunca se encendió.",
"In Valencia duurt de zomer 5 maanden met temperaturen boven 35 °C. Airconditioning draait non-stop in klassieke woningen — rekeningen van meer dan €400/maand in de zomer. Familie [Nume] bouwde met Polistibrick MBK 210 (temperaat-warm klimaatversie) en TBK 250. Na 18 maanden bewoning is de airconditioning nooit aangezet.",
"In Valencia dauert der Sommer 5 Monate mit Temperaturen über 35 °C. Die Klimaanlage läuft in klassischen Häusern nonstop — Rechnungen von über 400 €/Monat im Sommer. Familie [Nume] baute mit Polistibrick MBK 210 (Version für gemäßigt-warmes Klima) und TBK 250. Nach 18 Monaten Nutzung wurde die Klimaanlage nie eingeschaltet.",
),
"Dezvoltatorul [Numele companiei] căuta un sistem care combină viteza, performanța Passivhaus și marja de profit. A ales Polistibrick MBK 270 pentru cele 24 de unități. Cele 24 de case au fost livrate în 6 luni în total. Toate certificate Passivhaus din prima. Vândute în 4 săptămâni cu o primă de 18% peste media sectorului.": (
"Developer [Numele companiei] was looking for a system combining speed, Passivhaus performance and profit margin. They chose Polistibrick MBK 270 for all 24 units. All 24 homes were delivered in 6 months total. All Passivhaus certified on the first attempt. Sold in 4 weeks at an 18% premium above the sector average.",
"Le promoteur [Numele companiei] cherchait un système combinant rapidité, performance Passivhaus et marge bénéficiaire. Il a choisi Polistibrick MBK 270 pour les 24 unités. Les 24 maisons ont été livrées en 6 mois au total. Toutes certifiées Passivhaus du premier coup. Vendues en 4 semaines avec une prime de 18 % au-dessus de la moyenne du secteur.",
"Lo sviluppatore [Numele companiei] cercava un sistema che combinasse velocità, prestazioni Passivhaus e margine di profitto. Ha scelto Polistibrick MBK 270 per le 24 unità. Le 24 case sono state consegnate in 6 mesi in totale. Tutte certificate Passivhaus al primo tentativo. Vendute in 4 settimane con un premio del 18% sopra la media del settore.",
"El promotor [Numele companiei] buscaba un sistema que combinara velocidad, rendimiento Passivhaus y margen de beneficio. Eligió Polistibrick MBK 270 para las 24 unidades. Las 24 casas se entregaron en 6 meses en total. Todas certificadas Passivhaus a la primera. Vendidas en 4 semanas con una prima del 18% sobre la media del sector.",
"Ontwikkelaar [Numele companiei] zocht een systeem dat snelheid, Passivhaus-prestaties en winstmarge combineert. Koos Polistibrick MBK 270 voor de 24 eenheden. Alle 24 woningen geleverd in totaal 6 maanden. Alle Passivhaus-gecertificeerd in één keer. Verkocht in 4 weken met een premie van 18% boven het sectorsgemiddelde.",
"Der Bauträger [Numele companiei] suchte ein System, das Geschwindigkeit, Passivhaus-Leistung und Gewinnmarge vereint. Er wählte Polistibrick MBK 270 für alle 24 Einheiten. Alle 24 Häuser in insgesamt 6 Monaten geliefert. Alle beim ersten Mal Passivhaus-zertifiziert. In 4 Wochen verkauft mit 18 % Aufschlag über dem Branchendurchschnitt.",
),
"Era prima dată când construiam un ansamblu Passivhaus. Termenul nostru era de 12 luni. Cu Polistibrick, am livrat în 6 luni — am avut 6 luni în plus pentru comercializarea proiectului. Și cum întregul proiect a obținut certificarea de la prima vizită PHPP, am putut vinde la +18% peste piață. Un ROI de alt nivel.": (
"It was our first time building a Passivhaus development. Our deadline was 12 months. With Polistibrick, we delivered in 6 months — giving us 6 extra months to market the project. And since the entire project achieved certification on the first PHPP visit, we could sell at +18% above market. A ROI on another level.",
"C'était la première fois que nous construisions un ensemble Passivhaus. Notre délai était de 12 mois. Avec Polistibrick, nous avons livré en 6 mois — 6 mois de plus pour commercialiser le projet. Et comme l'ensemble du projet a obtenu la certification dès la première visite PHPP, nous avons pu vendre à +18 % au-dessus du marché. Un ROI d'un autre niveau.",
"Era la prima volta che costruivamo un complesso Passivhaus. La nostra scadenza era di 12 mesi. Con Polistibrick, abbiamo consegnato in 6 mesi — 6 mesi in più per commercializzare il progetto. E poiché l'intero progetto ha ottenuto la certificazione alla prima visita PHPP, abbiamo potuto vendere a +18% sopra il mercato. Un ROI di altro livello.",
"Era la primera vez que construíamos un conjunto Passivhaus. Nuestro plazo era de 12 meses. Con Polistibrick, entregamos en 6 meses — 6 meses extra para comercializar el proyecto. Y como todo el proyecto obtuvo la certificación en la primera visita PHPP, pudimos vender a +18% sobre el mercado. Un ROI de otro nivel.",
"Het was onze eerste keer dat we een Passivhaus-complex bouwden. Onze deadline was 12 maanden. Met Polistibrick leverden we in 6 maanden — 6 maanden extra om het project te commercialiseren. En omdat het hele project bij het eerste PHPP-bezoek certificatie kreeg, konden we verkopen tegen +18% boven markt. Een ROI van een ander niveau.",
"Es war das erste Mal, dass wir eine Passivhaus-Anlage bauten. Unsere Frist war 12 Monate. Mit Polistibrick lieferten wir in 6 Monaten — 6 Monate mehr für die Vermarktung. Und da das gesamte Projekt beim ersten PHPP-Besuch zertifiziert wurde, konnten wir mit +18 % über Markt verkaufen. Ein ROI auf einem anderen Niveau.",
),
"Polistibrick este un sistem ICF (Insulated Concrete Forms) brevetat european. Concret, sunt cofraje prefabricate din polistiren expandat (EPS) care se asamblează ca LEGO și se umplu cu beton armat. Rezultatul este un perete monolitic, termoizolat și fonoizolat, gata să primească finisajele.": (
"Polistibrick is a patented European ICF (Insulated Concrete Forms) system. Specifically, prefabricated formwork made of expanded polystyrene (EPS) that assembles like LEGO and is filled with reinforced concrete. The result is a monolithic, thermally and acoustically insulated wall, ready for finishes.",
"Polistibrick est un système ICF (Insulated Concrete Forms) breveté européen. Concrètement, des coffrages préfabriqués en polystyrène expansé (EPS) qui s'assemblent comme des LEGO et se remplissent de béton armé. Le résultat est un mur monolithique, thermo-isolé et phoniquement isolé, prêt à recevoir les finitions.",
"Polistibrick è un sistema ICF (Insulated Concrete Forms) brevettato europeo. In concreto, casseforme prefabbricate in polistirene espanso (EPS) che si assemblano come LEGO e si riempiono di calcestruzzo armato. Il risultato è un muro monolitico, termoisolato e fonoisolato, pronto per le finiture.",
"Polistibrick es un sistema ICF (Insulated Concrete Forms) patentado europeo. En concreto, encofrados prefabricados de poliestireno expandido (EPS) que se ensamblan como LEGO y se rellenan con hormigón armado. El resultado es un muro monolítico, termoaislado y fonoaislado, listo para recibir los acabados.",
"Polistibrick is een gepatenteerd Europees ICF-systeem (Insulated Concrete Forms). Concreet: geprefabriceerde bekistingen van geëxpandeerd polystyreen (EPS) die als LEGO in elkaar worden gezet en met gewapend beton worden gevuld. Het resultaat is een monolithische, thermisch en akoestisch geïsoleerde muur, klaar voor afwerking.",
"Polistibrick ist ein patentiertes europäisches ICF-System (Insulated Concrete Forms). Konkret handelt es sich um vorgefertigte Schalungen aus expandiertem Polystyrol (EPS), die sich wie LEGO zusammenfügen und mit Stahlbeton verfüllt werden. Das Ergebnis ist eine monolithische, wärme- und schalldämmende Wand, bereit für den Ausbau.",
),
"Întregul conținut al site-ului (texte, imagini, videoclipuri, logo-uri, mărci, brevete) este proprietatea exclusivă a {{company.name_legal}} sau a partenerilor săi. Orice reproducere, reprezentare sau difuzare, totală sau parțială, fără autorizație scrisă prealabilă este interzisă.": (
"All site content (text, images, videos, logos, trademarks, patents) is the exclusive property of {{company.name_legal}} or its partners. Any reproduction, representation or distribution, in whole or in part, without prior written authorisation is prohibited.",
"L'ensemble du contenu du site (textes, images, vidéos, logos, marques, brevets) est la propriété exclusive de {{company.name_legal}} ou de ses partenaires. Toute reproduction, représentation ou diffusion, totale ou partielle, sans autorisation écrite préalable est interdite.",
"L'intero contenuto del sito (testi, immagini, video, loghi, marchi, brevetti) è di esclusiva proprietà di {{company.name_legal}} o dei suoi partner. Qualsiasi riproduzione, rappresentazione o diffusione, totale o parziale, senza autorizzazione scritta preventiva è vietata.",
"Todo el contenido del sitio (textos, imágenes, vídeos, logotipos, marcas, patentes) es propiedad exclusiva de {{company.name_legal}} o de sus socios. Queda prohibida cualquier reproducción, representación o difusión, total o parcial, sin autorización escrita previa.",
"Alle site-inhoud (teksten, afbeeldingen, video's, logo's, merken, patenten) is exclusief eigendom van {{company.name_legal}} of zijn partners. Elke reproductie, weergave of verspreiding, geheel of gedeeltelijk, zonder voorafgaande schriftelijke toestemming is verboden.",
"Der gesamte Website-Inhalt (Texte, Bilder, Videos, Logos, Marken, Patente) ist ausschließliches Eigentum von {{company.name_legal}} oder seiner Partner. Jede Vervielfältigung, Darstellung oder Verbreitung, ganz oder teilweise, ohne vorherige schriftliche Genehmigung ist untersagt.",
),
"Construirea unei case — mai ales a unei case premium — este cea mai importantă decizie din viața dumneavoastră. Polistibrick vă oferă liniștea unei case pasive certificate: silențioasă, rezistentă la foc, antiseismică și care durează generații, fără întreținere specială.": (
"Building a home — especially a premium home — is the most important decision of your life. Polistibrick gives you the peace of mind of a certified passive house: quiet, fire-resistant, seismic-resistant and built to last generations, with no special maintenance.",
"Construire une maison — surtout une maison haut de gamme — est la décision la plus importante de votre vie. Polistibrick vous offre la sérénité d'une maison passive certifiée : silencieuse, résistante au feu, parasismique et conçue pour durer des générations, sans entretien particulier.",
"Costruire una casa — soprattutto una casa premium — è la decisione più importante della vostra vita. Polistibrick vi offre la tranquillità di una casa passiva certificata: silenziosa, resistente al fuoco, antisismica e pensata per durare generazioni, senza manutenzione speciale.",
"Construir una casa — especialmente una casa premium — es la decisión más importante de su vida. Polistibrick le ofrece la tranquilidad de una casa pasiva certificada: silenciosa, resistente al fuego, antisísmica y diseñada para durar generaciones, sin mantenimiento especial.",
"Een huis bouwen — vooral een premium huis — is de belangrijkste beslissing van uw leven. Polistibrick biedt u de gemoedsrust van een gecertificeerd passiefhuis: stil, brandwerend, aardbevingsbestendig en gebouwd om generaties mee te gaan, zonder speciaal onderhoud.",
"Ein Haus zu bauen — besonders ein Premium-Haus — ist die wichtigste Entscheidung Ihres Lebens. Polistibrick bietet Ihnen die Sicherheit eines zertifizierten Passivhauses: leise, feuerbeständig, erdbebensicher und für Generationen gebaut, ohne besondere Wartung.",
),
"Familia Mureșan dorea o casă pasivă A+++ fără să plătească prețul cărămizii. A ales Polistibrick pentru cele 5% în plus față de cărămida clasică și o casă livrată în 5 săptămâni în loc de 5 luni. La doi ani după mutare, factura medie de electricitate este de 38 €/lună.": (
"The Mureșan family wanted an A+++ passive house without paying brick prices. They chose Polistibrick for the 5% premium over classic brick and a home delivered in 5 weeks instead of 5 months. Two years after moving in, their average electricity bill is €38/month.",
"La famille Mureșan souhaitait une maison passive A+++ sans payer le prix de la brique. Elle a choisi Polistibrick pour les 5 % de plus par rapport à la brique classique et une maison livrée en 5 semaines au lieu de 5 mois. Deux ans après l'emménagement, la facture moyenne d'électricité est de 38 €/mois.",
"La famiglia Mureșan desiderava una casa passiva A+++ senza pagare il prezzo del mattone. Ha scelto Polistibrick per il 5% in più rispetto al mattone classico e una casa consegnata in 5 settimane invece di 5 mesi. Due anni dopo il trasloco, la bolletta media di elettricità è di 38 €/mese.",
"La familia Mureșan quería una casa pasiva A+++ sin pagar el precio del ladrillo. Eligió Polistibrick por el 5% adicional respecto al ladrillo clásico y una casa entregada en 5 semanas en lugar de 5 meses. Dos años después de mudarse, la factura media de electricidad es de 38 €/mes.",
"Familie Mureșan wilde een A+++ passiefhuis zonder baksteenprijzen te betalen. Koos Polistibrick voor de 5% meer ten opzichte van klassieke baksteen en een huis geleverd in 5 weken in plaats van 5 maanden. Twee jaar na verhuizing bedraagt de gemiddelde elektriciteitsrekening €38/maand.",
"Die Familie Mureșan wollte ein A+++ Passivhaus, ohne Ziegelpreise zu zahlen. Sie wählte Polistibrick für die 5 % Aufpreis gegenüber klassischem Ziegel und ein Haus, das in 5 Wochen statt 5 Monaten geliefert wurde. Zwei Jahre nach dem Einzug beträgt die durchschnittliche Stromrechnung 38 €/Monat.",
),
"Suntem singurul sistem ICF din Europa care produce la comandă, fără cost suplimentar. Singurul cu 3 modele predefinite plus personalizare totală. Și suntem primii care credem că o casă pasivă premium ar trebui să coste la fel ca o casă clasică — nu cu 35 % în plus.": (
"We are the only ICF system in Europe that produces to order, at no extra cost. The only one with 3 predefined models plus full customisation. And we are the first to believe that a premium passive house should cost the same as a conventional home — not 35% more.",
"Nous sommes le seul système ICF en Europe à produire sur commande, sans surcoût. Le seul avec 3 modèles prédéfinis plus une personnalisation totale. Et nous sommes les premiers à penser qu'une maison passive haut de gamme devrait coûter autant qu'une maison classique — pas 35 % de plus.",
"Siamo l'unico sistema ICF in Europa che produce su ordinazione, senza costi aggiuntivi. L'unico con 3 modelli predefiniti più personalizzazione totale. E siamo i primi a credere che una casa passiva premium debba costare quanto una casa classica — non il 35% in più.",
"Somos el único sistema ICF en Europa que produce bajo pedido, sin coste adicional. El único con 3 modelos predefinidos más personalización total. Y somos los primeros en creer que una casa pasiva premium debería costar lo mismo que una casa clásica — no un 35% más.",
"Wij zijn het enige ICF-systeem in Europa dat op maat produceert, zonder meerprijs. Het enige met 3 voorgedefinieerde modellen plus volledige personalisatie. En wij zijn de eersten die geloven dat een premium passiefhuis evenveel moet kosten als een klassiek huis — niet 35% meer.",
"Wir sind das einzige ICF-System in Europa, das auf Bestellung produziert, ohne Aufpreis. Das einzige mit 3 vordefinierten Modellen plus vollständiger Anpassung. Und wir sind die Ersten, die glauben, dass ein Premium-Passivhaus genauso viel kosten sollte wie ein klassisches Haus — nicht 35 % mehr.",
),
"Construcția s-a desfășurat între aprilie și mai 2024. Echipa de 3 persoane a constructorului partener a montat pereții MBK 270 în 9 zile, planșeele PBK în 2 zile, acoperișul TBK în 3 zile. Turnarea betonului: o singură zi. Finisaje și instalații: 4 săptămâni.": (
"Construction took place between April and May 2024. The partner builder's 3-person team installed MBK 270 walls in 9 days, PBK floors in 2 days, TBK roof in 3 days. Concrete pour: one day. Finishes and services: 4 weeks.",
"La construction s'est déroulée entre avril et mai 2024. L'équipe de 3 personnes du constructeur partenaire a monté les murs MBK 270 en 9 jours, les planchers PBK en 2 jours, la toiture TBK en 3 jours. Coulée du béton : une seule journée. Finitions et installations : 4 semaines.",
"La costruzione si è svolta tra aprile e maggio 2024. Il team di 3 persone del costruttore partner ha montato i muri MBK 270 in 9 giorni, i solai PBK in 2 giorni, il tetto TBK in 3 giorni. Getto del calcestruzzo: un solo giorno. Finiture e impianti: 4 settimane.",
"La construcción se desarrolló entre abril y mayo de 2024. El equipo de 3 personas del constructor asociado montó los muros MBK 270 en 9 días, los forjados PBK en 2 días, la cubierta TBK en 3 días. Vertido de hormigón: un solo día. Acabados e instalaciones: 4 semanas.",
"De bouw vond plaats tussen april en mei 2024. Het team van 3 personen van de partner-bouwer monteerde MBK 270-muren in 9 dagen, PBK-vloeren in 2 dagen, TBK-dak in 3 dagen. Betonstort: één dag. Afwerking en installaties: 4 weken.",
"Der Bau fand zwischen April und Mai 2024 statt. Das 3-köpfige Team des Partner-Bauunternehmers montierte MBK 270-Wände in 9 Tagen, PBK-Decken in 2 Tagen, TBK-Dach in 3 Tagen. Betonierung: ein Tag. Ausbau und Installationen: 4 Wochen.",
),
}

def _load_remaining():
    """Load remaining translations from companion modules into T dict."""
    from importlib import import_module
    for mod_name, attr in (
        ("_translations_chunk_1_rest", "REST"),
        ("_translations_chunk_1_rest2", "REST2"),
        ("_translations_chunk_1_rest3", "REST3"),
    ):
        mod = import_module(mod_name)
        T.update(getattr(mod, attr))


def main():
    _load_remaining()
    with open(MISSING, encoding="utf-8") as f:
        missing = json.load(f)
    missing_keys = [k for k in missing if k not in T]
    if missing_keys:
        print(f"ERROR: {len(missing_keys)} keys still untranslated:")
        for k in missing_keys[:10]:
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
