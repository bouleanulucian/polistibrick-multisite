#!/usr/bin/env python3
"""Third pass: fix remaining visible RO phrases on ME pages."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "countries/me"

EXTRA = [
    ("Construiești više multe stanovi.<br><span class=\"h1-l2\">Sa o singură echipă.</span>", "Gradite više stanova.<br><span class=\"h1-l2\">Sa jednim timom.</span>"),
    ("Polistibrick înlocuiește 5 materiale diferite i 5 echipe de construcție. Un singur proizvod, o singură echipă — i kuća je finalizată.", "Polistibrick zamjenjuje 5 različitih materijala i 5 građevinskih timova. Jedan proizvod, jedan tim — i kuća je završena."),
    ("Primește ponuda ta besplatna →", "Dobijte besplatnu ponudu →"),
    ("Libertate arhitecturală", "Arhitektonska sloboda"),
    ("«&nbsp;Kako construiesc asta?&nbsp;»<br><em>Sa Polistibrick, este posibil.</em>", "«&nbsp;Kako da ovo izgradim?&nbsp;»<br><em>Sa Polistibrick-om, moguće je.</em>"),
    ("Libertate totală la izvođenje, ca i la proiectare.", "Potpuna sloboda u izvođenju, kao i u projektovanju."),
    ("Sistemul Polistibrick se reconfigurează: kuća parter, vila sa etaj, mic bloc colectiv", "Polistibrick sistem se rekonfiguriše: kuća prizemna, vila sa spratom, mali stambeni blok"),
    ("Diferențe", "Razlike"),
    ("Diferența Polistibrick", "Polistibrick razlika"),
    ("O echipă — 3 persoane", "Jedan tim — 3 osobe"),
    ("3 materiale", "3 materijala"),
    ("Oplata Polistibrick • Beton • Oțel", "Oplata Polistibrick • Beton • Čelik"),
    ("Sistem tradițional", "Tradicionalni sistem"),
    ("Ești…? Rješenja pe rol", "Vi ste…? Rješenja po ulozi"),
    ("turnare beton într-un lot de kuće", "betoniranje u stambenom kompleksu"),
    ("Îți imaginezi,<br><em>Polistibrick execută.</em>", "Vi zamislite,<br><em>Polistibrick izvodi.</em>"),
    ("O singură echipă = marja a 5 echipe — până la 50%", "Jedan tim = marža od 5 timova — do 50%"),
    ("Cinci linii mai puțin pe ponuda,<br><em>više premium za tine.</em>", "Pet linija manje na ponudi,<br><em>više premiuma za vas.</em>"),
    ("O kuća. <em>Trei proizvoda.</em>", "Jedna kuća. <em>Tri proizvoda.</em>"),
    ("O kuća completă <em>în 4 etape.</em>", "Kompletna kuća <em>u 4 koraka.</em>"),
    ("Solicită o ponuda personalizată", "Zatražite personalizovanu ponudu"),
    ("Mai multe detalii →", "Više detalja →"),
    ("Toate proiectele →", "Svi projekti →"),
    ("Toate svjedočanstva →", "Sva svjedočanstva →"),
    ("Poveștile clienților", "Priče klijenata"),
    ("De la fundație la<br><em>cheia în mână.</em>", "Od temelja do<br><em>ključa u ruke.</em>"),
    ("Cum a decurs", "Kako je proteklo"),
    ("Filtrare după etapă.", "Filtrirajte po fazi."),
    ("Click pe orice imagine pentru a o vedea la dimensiune completă.", "Kliknite na bilo koju sliku da je vidite u punoj veličini."),
    ("Povestește-ne despre proiectul tău.", "Recite nam o svom projektu."),
    ("Datele tale sunt confidențiale.", "Vaši podaci su povjerljivi."),
    ("Trimite mesajul", "Pošaljite poruku"),
    ("Mesaj trimis ✓", "Poruka poslata ✓"),
    ("Mulțumim! Echipa noastră răspunde în maximum 24 de ore lucrătoare.", "Hvala! Naš tim odgovara u roku od 24 radna sata."),
    ("Accept politica de confidențialitate (GDPR)", "Prihvatam politiku privatnosti (GDPR)"),
    ("Ești", "Vi ste"),
    ("Persoană fizică / Proprietar", "Pojedinac / vlasnik"),
    ("Constructor / Antreprenor", "Građevinac / preduzetnik"),
    ("Dezvoltator / Investitor", "Investitor"),
    ("Altul", "Ostalo"),
    ("Numele tău", "Vaše ime"),
    ("email@exemplu.ro", "email@primjer.me"),
    ("Cum te putem ajuta?", "Kako vam možemo pomoći?"),
    ("PDF · DWG · DXF · JPG · PNG · ZIP — max 10 MB / fișier", "PDF · DWG · DXF · JPG · PNG · ZIP — maks. 10 MB / datoteka"),
    ("Șterge", "Ukloni"),
    ("Bună,", "Zdravo,"),
    ("Mulțumim anticipat.", "Hvala unaprijed."),
    ("Selectează țara", "Odaberite zemlju"),
    ("Sediu", "Sjedište"),
    ("Online", "Online"),
    ("Cerere documentație", "Zahtjev za dokumentaciju"),
    ("Suport produs", "Podrška za proizvod"),
    ("Cerere ponuda", "Zahtjev za ponudu"),
    ("Birou de studii (BET)", "Projektantski biro"),
    ("Specialiști la un click distanță.", "Stručnjaci na klik."),
    ("Scrie-ne direct.", "Pišite nam direktno."),
    ("Contactează-ne", "Kontaktirajte nas"),
    ("Află mai mult", "Saznajte više"),
    ("Citește →", "Pročitaj →"),
    ("Descarcă PDF", "Preuzmite PDF"),
    ("Descarcă fișa tehnică", "Preuzmite tehnički list"),
    ("Documentație completă", "Kompletna dokumentacija"),
    ("Specificații tehnice complete", "Kompletne tehničke specifikacije"),
    ("Certificări CE + ETA", "CE + ETA certifikati"),
    ("Garanție 50+ ani.", "Garancija 50+ godina."),
    ("Zidovi pasivi A+++ dintr-o singură turnare.", "Pasivni zidovi A+++ u jednom betoniranju."),
    ("Spanuri de 9 m fără grinzi", "Rasponi od 9 m bez greda"),
    ("Cum funcționează", "Kako funkcioniše"),
    ("Pornire astăzi", "Počnite danas"),
    ("Adaugă restul kućei.", "Dodajte ostatak kuće."),
    ("Clasa energetică", "Energetska klasa"),
    ("Factură reală electricitate + gaz", "Stvarni račun za struju + gas"),
    ("Cronologie execuție", "Vremenski plan izvođenja"),
    ("Vezi studiul de caz →", "Pogledajte studiju slučaja →"),
    ("Mortar zidărie", "Zidarski malter"),
    ("Mortar tencuială", "Malter za fasadu"),
    ("Cuie fixare", "Tiplovi za fiksiranje"),
    ("Plasă fibră", "Staklena mrežica"),
    ("Adeziv fațadă", "Ljepilo za fasadu"),
    ("Convins de", "Uvjereni u"),
    ("Atașează planuri, schițe sau documente", "Priložite planove, skice ili dokumente"),
    ("Ingineri, arhitecți, designeri și specialiști în construcții pasive.", "Inženjeri, arhitekti, dizajneri i specijalisti za pasivnu gradnju."),
    ("Persoanele care fac sistemul Polistibrick să funcționeze pe trei continente.", "Ljudi koji pokreću Polistibrick sistem na tri kontinenta."),
    ("Inovație patentirana", "Patentirana inovacija"),
    ("Suport tehnic pe șantier", "Tehnička podrška na gradilištu"),
    ("Tarife preferențiale", "Povlašćene cijene"),
    ("Cărămidă clasică", "Klasična cigla"),
    ("Construcție inițială", "Početna gradnja"),
    ("Cursuri certificare", "Kursevi certifikacije"),
    ("Rezistență la foc", "Otpornost na vatru"),
    ("Execuție Polistibrick", "Izvođenje Polistibrick"),
    ("Suprafață construită", "Izgrađena površina"),
    ("Suprafață utilă", "Korisna površina"),
    ("Cost total (cheie în mână)", "Ukupni trošak (ključ u ruke"),
    ("Săptămâna 1", "Sedmica 1"),
    ("Săptămâna 2", "Sedmica 2"),
    ("Săptămâna 3", "Sedmica 3"),
    ("Săptămâna 4", "Sedmica 4"),
]

def main():
    pairs = sorted(EXTRA, key=lambda x: -len(x[0]))
    for html in sorted(ROOT.rglob("*.html")):
        t = html.read_text(encoding="utf-8")
        orig = t
        for ro, cnr in pairs:
            t = t.replace(ro, cnr)
        if t != orig:
            html.write_text(t, encoding="utf-8")
    fr = Path(__file__).resolve().parent / "translations/fr_to_cnr.json"
    data = json.loads(fr.read_text(encoding="utf-8"))
    for ro, cnr in EXTRA:
        data[ro] = cnr
    fr.write_text(json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Third pass: {len(EXTRA)} phrases; fr_to_cnr={len(data)}")

if __name__ == "__main__":
    main()
