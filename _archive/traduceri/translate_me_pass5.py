#!/usr/bin/env python3
"""Pass 5: safe phrase-only RO→CNR for countries/me (no short word-boundary swaps)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ME = ROOT / "countries/me"

# Phrase-level only — longest first, safe substring replace
EXTENDED = [
    ("Pentru cei care își construiesc casa", "Za one koji grade svoju kuću"),
    ("Casa pe viață, <em>fără facturi mari.</em>", "Kuća za cijeli život, <em>bez visokih računa.</em>"),
    ("Construirea unei case — mai ales a unei case premium — este cea mai importantă decizie din viața dumneavoastră. Polistibrick vă oferă liniștea unei case pasive certificate: silențioasă, rezistentă la foc, antiseismică și care durează generații, fără întreținere specială.", "Gradnja kuće — posebno premium kuće — najvažnija je odluka u vašem životu. Polistibrick vam nudi mir certificirane pasivne kuće: tiha je, otporna na vatru, antiseismička i traje generacijama, bez posebnog održavanja."),
    ("Calculează economiile mele", "Izračunajte moje uštede"),
    ("Cere o ofertă", "Zatražite ponudu"),
    ("București · livrare 2025", "Podgorica · isporuka 2025"),
    ("Adevăratele dumneavoastră îngrijorări", "Vaše stvarne brige"),
    ("Știm ce vă <em style=\"font-style:italic;color:var(--red);font-weight:400;\">preocupă cu adevărat.</em>", "Znamo šta vas <em style=\"font-style:italic;color:var(--red);font-weight:400;\">zaista brine.</em>"),
    ("Construirea unei case premium este un angajament pe viață. Iată cele 4 întrebări reale pe care și le pun cumpărătorii ca dumneavoastră — și răspunsurile noastre oneste.", "Gradnja premium kuće je obaveza za cijeli život. Evo 4 stvarna pitanja koja kupci poput vas postavljaju — i naših iskrenih odgovora."),
    ("« Ce se întâmplă dacă regret alegerea peste 10 ani? »", "« Šta ako zažalim zbog izbora za 10 godina? »"),
    ("Polistibrick a fost utilizat pentru <strong>mii de case în Europa, de 15 ani</strong>. Primele familii locuiesc încă în casele lor, cu aceleași performanțe ca în prima zi. Structura este <strong>garantată 50 de ani</strong>.", "Polistibrick se koristi za <strong>hiljade kuća u Evropi, 15 godina</strong>. Prve porodice i dalje žive u svojim kućama, sa istim performansama kao prvog dana. Struktura je <strong>garantovana 50 godina</strong>."),
    ("« Arhitectul meu nu va cunoaște sistemul. »", "« Moj arhitekt neće poznavati sistem. »"),
    ("Avem o <strong>rețea de arhitecți formați Polistibrick</strong> în toată România. Îl găsiți pe al dumneavoastră în secțiunea de mai jos. Dacă arhitectul actual nu îl cunoaște, <strong>îl formăm gratuit</strong>.", "Imamo <strong>mrežu arhitekata obučenih za Polistibrick</strong> u cijeloj Crnoj Gori. Pronaći ćete svog u odjeljku ispod. Ako trenutni arhitekt ne poznaje sistem, <strong>obučavamo ga besplatno</strong>."),
    ("« Facturile la energie vor exploda în viitor. »", "« Računi za energiju će u budućnosti eksplodirati. »"),
    ("Exact de aceea Polistibrick este o <strong>asigurare împotriva inflației energetice</strong>. Consumul rămâne la <strong>15 kWh/m²/an</strong>, indiferent de prețul energiei. Calculați economiile mai jos.", "Upravo zato je Polistibrick <strong>osiguranje od energetske inflacije</strong>. Potrošnja ostaje na <strong>15 kWh/m²/godina</strong>, bez obzira na cijenu energije. Izračunajte uštede ispod."),
    ("« Cine va repara casa mea în 2045? »", "« Ko će popravljati moju kuću 2045. godine? »"),
    ("Polistibrick este o <strong>structură clasică din beton armat</strong> — orice zidar, instalator sau electrician poate interveni. Izolația EPS nu se degradează, iar structura nu necesită întreținere specială.", "Polistibrick je <strong>klasična armirano-betonska struktura</strong> — bilo koji zidar, instalater ili električar može intervenisati. EPS izolacija se ne degradira, a struktura ne zahtijeva posebno održavanje."),
    ("Ce schimbă pentru dumneavoastră", "Šta se mijenja za vas"),
    ("Concret, <em>zi de zi.</em>", "Konkretno, <em>dan za danom.</em>"),
    ("Factură la energie &lt; 50 €/lună", "Račun za energiju &lt; 50 €/mjesec"),
    ("Polistibrick consumă 15 kWh/m²/an pentru încălzire (față de 55 pentru o casă RE2020 standard). Economisiți 80% din facturi, pe viață.", "Polistibrick troši 15 kWh/m²/godina za grijanje (naspram 55 za standardnu RE2020 kuću). Uštedite 80% na računima, doživotno."),
    ("Construită în 4–6 săptămâni", "Izgrađena za 4–6 sedmica"),
    ("Structura se montează de 3 ori mai repede decât zidăria clasică. Vă mutați în câteva luni, nu în câțiva ani. Mai puțin stres, mai puține întârzieri.", "Struktura se montira 3 puta brže od klasičnog zidanja. Usеljavate se za nekoliko mjeseci, ne za nekoliko godina. Manje stresa, manje kašnjenja."),
    ("Liniște, siguranță, serenitate", "Mir, sigurnost, spokojstvo"),
    ("52 dB izolare acustică, A1 antincendiu, antiseismic Eurocode 8. Casa vă protejează familia de tot — zgomot, foc, cutremure.", "52 dB akustična izolacija, A1 protivpožarna zaštita, antiseismičnost Eurocode 8. Kuća štiti vašu porodicu od svega — buke, vatre, zemljotresa."),
    ("Bez mucegai, niciodată", "Bez plijesni, nikada"),
    ("EPS cu celule închise nu absoarbe apa. Pereții rămân uscați, copiii respiră aer curat, fără probleme de umiditate peste 10 ani.", "EPS sa zatvorenim ćelijama ne upija vodu. Zidovi ostaju suhi, djeca udišu čist zrak, bez problema s vlagom i poslije 10 godina."),
    ("O casă pasivă certificată RE2020 se vinde cu 15–25% mai scump decât una clasică. Polistibrick = investiție care se valorifică în timp.", "Certificirana pasivna RE2020 kuća prodaje se 15–25% skuplje od klasične. Polistibrick = investicija koja se vremenom povećava."),
    ("Întotdeauna 21°C, fără efort", "Uvijek 21°C, bez napora"),
    ("Inerția termică a betonului + EPS mențin temperatura constantă. Fără frig brusc iarna, fără caniculă vara. Confort total.", "Termička inercija betona + EPS održavaju stalnu temperaturu. Bez naglog hladnoće zimi, bez vrućine ljeti. Potpuna udobnost."),
    ("Cât vă va face casa să <em style=\"font-style:italic;color:var(--red);font-weight:400;\">economisiți?</em>", "Koliko će vam kuća omogućiti da <em style=\"font-style:italic;color:var(--red);font-weight:400;\">uštedite?</em>"),
    ("Indicați suprafața viitoarei case. Calculăm factura anuală de încălzire cu Polistibrick MBK 300 față de o casă clasică RE2020.", "Navedite površinu buduće kuće. Računamo godišnji račun za grijanje sa Polistibrick MBK 300 naspram klasične RE2020 kuće."),
    ("Suprafața utilă a casei:", "Korisna površina kuće:"),
    ("Economisiți <strong id=\"yearly-savings\">900 €</strong> în fiecare an", "Uštedite <strong id=\"yearly-savings\">900 €</strong> svake godine"),
    ("Când este Polistibrick <em>alegerea potrivită pentru dumneavoastră?</em>", "Kada je Polistibrick <em>pravi izbor za vas?</em>"),
    ("Față de cărămida clasică, pasivul clasic și structura din lemn — iată cele 3 criterii unde Polistibrick face diferența.", "Naspram klasične cigle, klasičnog pasiva i drvene strukture — evo 3 kriterija gdje Polistibrick pravi razliku."),
    ("Siguranță totală", "Potpuna sigurnost"),
    ("Foc A1 + antiseismic Excelent. Structura din lemn nu rezistă nici la foc, nici în zone seismice.", "Vatra A1 + antiseismičnost odlična. Drvena struktura ne izdržava ni vatru ni u seizmičkim zonama."),
    ("Structură în 4–6 săptămâni vs 4–5 luni cu cărămida. Vă mutați de 3× mai repede.", "Struktura za 4–6 sedmica naspram 4–5 mjeseci sa ciglom. Usеljavate se 3× brže."),
    ("Vedeți comparația completă pe 12 criterii", "Pogledajte kompletno poređenje po 12 kriterija"),
    ("Ascundeți comparația", "Sakrij poređenje"),
    ("Răspunsuri <em>la întrebările dumneavoastră.</em>", "Odgovori <em>na vaša pitanja.</em>"),
    ("Cele mai frecvente întrebări despre sistemul Polistibrick — tehnice, comerciale, garanții și punere în operă. Dacă nu găsiți răspunsul, scrieți-ne direct.", "Najčešća pitanja o Polistibrick sistemu — tehnička, komercijalna, garancija i izvođenje. Ako ne pronađete odgovor, pišite nam direktno."),
    ("Pentru constructori și profesioniști", "Za građevince i profesionalce"),
    ("Câți muncitori sunt necesari pentru a monta o casă?", "Koliko radnika je potrebno za montažu kuće?"),
    ("Câte meserii înlocuiește Polistibrick?", "Koliko zanata Polistibrick zamjenjuje?"),
    ("Placa de finisare este gips-carton?", "Da li je završna ploča gips-karton?"),
    ("Cum trec electricitatea și instalațiile sanitare?", "Kako se provode elektrika i vodovod?"),
    ("Este antiseismic? Permite console mari?", "Da li je antiseismičan? Dozvoljava velike konzole?"),
    ("Cum devii constructor partener Polistibrick?", "Kako postati Polistibrick partnerski građevinac?"),
    ("Despre sistem", "O sistemu"),
    ("Ce este Polistibrick exact?", "Šta je tačno Polistibrick?"),
    ("Care este diferența față de un sistem ICF clasic?", "Koja je razlika u odnosu na klasični ICF sistem?"),
    ("Pereții respiră? Nu va fi umiditate?", "Da li zidovi dišu? Hoće li biti vlage?"),
    ("Despre cost", "O troškovima"),
    ("Cât costă Polistibrick comparativ cu cărămida?", "Koliko košta Polistibrick u poređenju sa ciglom?"),
    ("Cât voi economisi la facturi în 25 de ani?", "Koliko ću uštedjeti na računima za 25 godina?"),
    ("Există ajutoare fiscale sau subvenții?", "Postoje li porezne olakšice ili subvencije?"),
    ("Despre punerea în operă", "O izvođenju"),
    ("Cât durează construcția cu Polistibrick?", "Koliko traje gradnja sa Polistibrick-om?"),
    ("Am nevoie de un constructor specializat?", "Da li mi treba specijalizovani građevinac?"),
    ("Polistibrick este compatibil cu arhitectura tradițională?", "Da li je Polistibrick kompatibilan sa tradicionalnom arhitekturom?"),
    ("Politică de confidențialitate (GDPR)", "Politika privatnosti (GDPR)"),
    ("Cum colectăm, utilizăm și protejăm datele dumneavoastră personale. Conform Regulamentului UE 2016/679 (GDPR). Ultima actualizare: 3 iulie 2026.", "Kako prikupljamo, koristimo i štitimo vaše lične podatke. U skladu sa Uredbom EU 2016/679 (GDPR). Posljednje ažuriranje: 3. jul 2026."),
    ("Operator de date", "Rukovalac podacima"),
    ("Date colectate", "Prikupljeni podaci"),
    ("Scopuri și temeiuri legale", "Svrhe i pravni osnovi"),
    ("Împuterniciți și destinatari", "Ovlašćeni obrađivači i primaoci"),
    ("Transferuri în afara UE", "Prenosi izvan EU"),
    ("Durata de păstrare", "Period čuvanja"),
    ("Drepturile dumneavoastră", "Vaša prava"),
    ("Reclamații", "Žalbe"),
    ("Termeni și condiții generale", "Opšti uslovi"),
    ("Condițiile care reglementează utilizarea site-ului Polistibrick și relația contractuală dintre noi și clienții noștri. Ultima actualizare: 19 iunie 2026.", "Uslovi koji regulišu korišćenje Polistibrick sajta i ugovorni odnos između nas i naših klijenata. Posljednje ažuriranje: 19. jun 2026."),
    ("Valorile noastre", "Naše vrijednosti"),
    ("Ce ne deosebește.", "Šta nas izdvaja."),
    ("Haut de gamme accessible", "Pristupačan premium"),
    ("Premium accesibil", "Pristupačan premium"),
    ("Credem că performanța superioară nu trebuie rezervată celor cu buget nelimitat. Casa pasivă Polistibrick costă la fel ca o casă clasică — cu 30 % mai puțin decât alternativa pasivă tradițională.", "Vjerujemo da vrhunske performanse ne treba da budu rezervisane za one sa neograničenim budžetom. Polistibrick pasivna kuća košta isto kao klasična kuća — 30% manje od tradicionalne pasivne alternative."),
    ("Inovație patentată", "Patentirana inovacija"),
    ("Deținem brevetul european pentru sistemul nostru ICF integrat. Singurul sistem din categoria sa care combină cofraj + izolație + suport de finisaje într-un singur produs prefabricat.", "Posjedujemo evropski patent za naš integrisani ICF sistem. Jedini sistem u svojoj kategoriji koji kombinuje oplatu + izolaciju + potporu za završnu obradu u jednom prefabrikovanom proizvodu."),
    ("Personalizare totală", "Potpuna personalizacija"),
    ("3 modele predefinite plus producție la comandă fără supliment de preț. Fiecare proiect este unic — sistemul nostru se adaptează, nu invers.", "3 predefinisana modela plus proizvodnja po narudžbi bez dodatnog troška. Svaki projekat je jedinstven — naš sistem se prilagođava, ne obrnuto."),
    ("Producție europeană", "Evropska proizvodnja"),
    ("Fabricile noastre din Valencia (Spania) și Craiova (România) operează conform standardelor CE și ISO. Calitate europeană, livrare europeană, garanție europeană.", "Naše fabrike u Valenciji (Španija) i Krajovi (Rumunija) rade po CE i ISO standardima. Evropski kvalitet, evropska isporuka, evropska garancija."),
    ("Construcție rapidă", "Brza gradnja"),
    ("O casă întreagă în 1 lună față de 4–5 luni cu sistemul clasic. Mai puține echipe, mai puține materiale, mai puține întârzieri. Mai puțin stres pentru proprietar.", "Cijela kuća za 1 mjesec naspram 4–5 mjeseci sa klasičnim sistemom. Manje timova, manje materijala, manje kašnjenja. Manje stresa za vlasnika."),
    ("Dezvoltare durabilă", "Održivi razvoj"),
    ("Reducerea consumului de energie cu 70% înseamnă mai puține emisii pe durata de viață a casei. Construim case care încetează să polueze odată ocupate.", "Smanjenje potrošnje energije za 70% znači manje emisija tokom životnog vijeka kuće. Gradimo kuće koje prestaju da zagađuju kada se usele."),
    ("Explorează", "Istražite"),
    ("Descoperă <em>tot ce ne face unici.</em>", "Otkrijte <em>sve što nas čini jedinstvenim.</em>"),
    ("Vezi brevetul →", "Pogledajte patent →"),
    ("Vezi certificările →", "Pogledajte sertifikate →"),
    ("Vezi fabricile →", "Pogledajte fabrike →"),
    ("Descoperă fondatorul →", "Upoznajte osnivača →"),
    ("Casa dumneavoastră, <em>de la prima schiță.</em>", "Vaša kuća, <em>od prvog nacrta.</em>"),
    ("Vorbește cu noi", "Razgovarajte sa nama"),
    ("Combien vi écoimeisez over 25 years", "Koliko štedite za 25 godina"),
    ("Combien vi écoimeisez with Polistibrick — 25 years", "Koliko štedite sa Polistibrick-om — 25 godina"),
    ("Votre avis (optionnel)", "Vaše mišljenje (opciono)"),
    ("Votre avis", "Vaše mišljenje"),
    ("Nos valeurs", "Naše vrijednosti"),
    ("What sets us apart.", "Šta nas izdvaja."),
    ("Commencez aujourd'hui", "Počnite danas"),
    ("5 functions in a single product", "5 funkcija u jednom proizvodu"),
    ("Un formwork. <em>A whole house.</em>", "Jedna oplata. <em>Cijela kuća.</em>"),
    ("Formwork :", "Oplata:"),
    ("the modular structure that receives the concrete", "modularna struktura koja prima beton"),
    ("Acoustic insulation:", "Akustička izolacija:"),
    ("premium sound reduction through the EPS + reinforced concrete combination", "vrhunsko smanjenje buke kroz kombinaciju EPS-a i armiranog betona"),
    ("Support de finition :", "Potpora za završnu obradu:"),
    ("flat wall, ready to plaster or paint directly", "ravan zid, spreman za direktno malterisanje ili bojenje"),
    ("Do you have a project? <em>Let's build it together.</em>", "Imate projekat? <em>Gradimo ga zajedno.</em>"),
    ("Send us your plan and receive a personalised quote within 48 hours, with a transparent breakdown of materials, delivery and installation.", "Pošaljite nam plan i primite personalizovanu ponudu u roku od 48 sati, sa transparentnom razradom materijala, isporuke i montaže."),
    ("Talk to a specialist", "Razgovarajte sa stručnjakom"),
    ("Premium acoustic insulation", "Vrhunska akustična izolacija"),
    ("The combination of high-density EPS + reinforced concrete delivers sound reduction of over 50 dB — guaranteed quiet in any environment.", "Kombinacija visokogustinske EPS + armiranog betona daje smanjenje buke preko 50 dB — garantovan mir u bilo kom okruženju."),
    ("Monolithic concrete poured in a single stage — no joints, no weak points.", "Monolitni beton ulijevan u jednoj fazi — bez spojeva, bez slabih tačaka."),
    ("A1 fire resistance", "Otpornost na vatru A1"),
    ("The highest fire reaction class — non-combustible.", "Najviša klasa reakcije na vatru — negorivo."),
    ("Your home, <em>from the first sketch.</em>", "Vaša kuća, <em>od prvog nacrta.</em>"),
    ("Send us your plans and receive a personalised quote within 48 hours. No obligation, no hidden costs.", "Pošaljite nam planove i primite personalizovanu ponudu u roku od 48 sati. Bez obaveza, bez skrivenih troškova."),
    ("Talk to us", "Razgovarajte sa nama"),
    ("We believe superior performance should not be reserved for those with unlimited budgets.", "Vjerujemo da vrhunske performanse ne treba da budu rezervisane za one sa neograničenim budžetom."),
    ("Patented innovation", "Patentirana inovacija"),
    ("Total customisation", "Potpuna personalizacija"),
    ("European production", "Evropska proizvodnja"),
    ("Rapid construction", "Brza gradnja"),
    ("Sustainable development", "Održivi razvoj"),
    ("Discover <em>everything that makes us unique.</em>", "Otkrijte <em>sve što nas čini jedinstvenim.</em>"),
    ("How much will I save on bills over 25 years?", "Koliko ću uštedjeti na računima za 25 godina?"),
    ("Combien j'économise sur les factures en 25 ans ?", "Koliko uštedim na računima za 25 godina?"),
    ("Les réseaux se tirent <strong>à travers le coffrage</strong> avant fermeture, exactement comme dans une cloison de plâtre.", "Mreže se provlače <strong>kroz oplatu</strong> prije zatvaranja, baš kao u gips-karton zidu."),
    ("Rețelele se trag <strong>prin cofraj</strong> înainte de închidere, exact ca într-un perete de gips-carton.", "Mreže se provlače <strong>kroz oplatu</strong> prije zatvaranja, baš kao u gips-karton zidu."),
    ("Conductele sunt integrate în montaj, nu tratate separat.", "Cjevovodi su integrisani u montažu, ne obrađuju se odvojeno."),
    ("La maison traditionnelle a été pensée il y a 200 ans.", "Tradicionalna kuća je osmišljena prije 200 godina."),
    ("Elle fonctionne grâce aux factures : gaz, bois, électricité, climatisation — un entretien coûteux et sans fin.", "Funkcioniše zahvaljujući računima: gas, drvo, struja, klimatizacija — skupog i beskrajnog održavanja."),
    ("Aujourd'hui la maison n'est plus un investissement ; c'est une obligation.", "Danas kuća više nije investicija; to je obaveza."),
    ("Polistibrick est l'alternative moderne.", "Polistibrick je moderna alternativa."),
    ("Votre vision, <em>dès la première esquisse.</em>", "Vaša vizija, <em>od prvog nacrta.</em>"),
    ("Envoyez-nous votre plan et recevez un devis personnalisé sous 48 heures.", "Pošaljite nam plan i primite personalizovanu ponudu u roku od 48 sati."),
    ("Sans engagement, sans frais cachés.", "Bez obaveza, bez skrivenih troškova."),
    ("Demander un devis", "Zatražite ponudu"),
    ("Pour afficher la photo et le nom du responsable d'un pays", "Za prikaz fotografije i imena odgovornog lica za zemlju"),
    ("Kontaktez l'équipe Polistibrick de votre pays.", "Kontaktirajte Polistibrick tim u vašoj zemlji."),
    ("Odaberite le drapeau du pays où vous construisez et recevez le contact de l'équipe locale.", "Odaberite zastavu zemlje u kojoj gradite i dobijte kontakt lokalnog tima."),
    ("Combien coûte <em>votre maison Polistibrick ?</em>", "Koliko košta <em>vaša Polistibrick kuća?</em>"),
    ("Votre maison Polistibrick", "Vaša Polistibrick kuća"),
    ("Terrasse supérieure pour le dîner.", "Gornja terasa za večeru."),
    ("5 funcții într-un singur proizvod", "5 funkcija u jednom proizvodu"),
    ("Un oplata. <em>O casă întreagă.</em>", "Jedna oplata. <em>Cijela kuća.</em>"),
    ("Izolacija akustika:", "Akustička izolacija:"),
    ("smanjenje sonoră premium prin combinația EPS + beton armat", "vrhunsko smanjenje buke kroz kombinaciju EPS-a i armiranog betona"),
    ("struktura modulară care primește betonul", "modularna struktura koja prima beton"),
    ("zid plan, gata de tencuit sau vopsit direct", "ravan zid, spreman za direktno malterisanje ili bojenje"),
    ("Počnite danas", "Počnite danas"),
    ("Zatražite la dokumentacija", "Zatražite dokumentaciju"),
    ("Zatražite la dokumentacija", "Zatražite dokumentaciju"),
]

ro_cnr = json.loads((ROOT / "translations/ro_to_cnr.json").read_text(encoding="utf-8"))
pairs_dict = dict(EXTENDED)
pairs_dict.update({k: v for k, v in ro_cnr.items() if k != v and (len(k) >= 6 or " " in k)})
PAIRS = sorted(pairs_dict.items(), key=lambda x: -len(x[0]))


def translate_block(text: str) -> str:
    for old, new in PAIRS:
        text = text.replace(old, new)
    return text


def process_html(text: str) -> str:
    parts = re.split(r"(<script[\s\S]*?</script>|<style[\s\S]*?</style>)", text, flags=re.I)
    return "".join(p if i % 2 else translate_block(p) for i, p in enumerate(parts))


def main():
    changed = 0
    for html in sorted(ME.rglob("*.html")):
        t = html.read_text(encoding="utf-8")
        n = process_html(t)
        if n != t:
            html.write_text(n, encoding="utf-8")
            changed += 1
    print(f"Pass5 safe: updated {changed} files ({len(PAIRS)} phrases)")


if __name__ == "__main__":
    main()
