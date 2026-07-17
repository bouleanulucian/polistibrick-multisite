#!/usr/bin/env python3
"""Targeted fixes for remaining RO/FR visible text on priority ME pages."""
from pathlib import Path

FIXES = [
    # vlasnici fears 2-4
    ("« Arhitectul meu nu va cunoaște sistem. »", "« Moj arhitekt neće poznavati sistem. »"),
    ("Imamo o <strong>rețea de arhitekti formați Polistibrick</strong> u toată Rumunija. Ga găsiți pe al vi u secțiunea de više jos. Ako arhitectul actual nu ga cunoaște, <strong>ga formăm besplatno</strong>.",
     "Imamo <strong>mrežu arhitekata obučenih za Polistibrick</strong> u cijeloj Crnoj Gori. Pronaći ćete svog u odjeljku ispod. Ako trenutni arhitekt ne poznaje sistem, <strong>obučavamo ga besplatno</strong>."),
    ("« Računile la energija vor exploda u viitor. »", "« Računi za energiju će u budućnosti eksplodirati. »"),
    ("Exact de aceea Polistibrick je o <strong>asigurare împotriva inflației energetske</strong>. Consumul rămâne la <strong>15 kWh/m²/godina</strong>, indiferent de cijenu energije. Calculați uštedele više jos.",
     "Upravo zato je Polistibrick <strong>osiguranje od energetske inflacije</strong>. Potrošnja ostaje na <strong>15 kWh/m²/godina</strong>, bez obzira na cijenu energije. Izračunajte uštede ispod."),
    ("« Ko va repara kuća mea u 2045? »", "« Ko će popravljati moju kuću 2045. godine? »"),
    ("Polistibrick je o <strong>struktura klasična din beton armat</strong> — orice zidar, instalator ili electrician poate interveni. Izolația EPS nu se degradează, iar struktura nu necesită održavanje specială.",
     "Polistibrick je <strong>klasična armirano-betonska struktura</strong> — bilo koji zidar, instalater ili električar može intervenisati. EPS izolacija se ne degradira, a struktura ne zahtijeva posebno održavanje."),
    # faq hero
    ("Odgovori la cele više frecvente pitanja o sistem Polistibrick — tehničke, comerciale, garanții i punere u operă.",
     "Odgovori na najčešća pitanja o Polistibrick sistemu — tehnička, komercijalna, garancija i izvođenje."),
    ("Cele više frecvente pitanja o sistem Polistibrick — tehničke, comerciale, garanții i punere u operă. Ako nu găsiți răspunsul, scrieți-ne direktan.",
     "Najčešća pitanja o Polistibrick sistemu — tehnička, komercijalna, garancija i izvođenje. Ako ne pronađete odgovor, pišite nam direktno."),
    ("Câți muncitori su necesari za a montira o kuća?", "Koliko radnika je potrebno za montažu kuće?"),
    ("O jedna tim de <strong>3 osobe</strong> montira o kuća parter de 100 m² u <strong>više malo de 3 sedmice</strong>, aproape završena. Gdje o gradnja klasična mobilizează do la 5 timovi diferite (zidari, izolacija exterioară, izolacija interioară, rigipsiști, etanșiori), Polistibrick cere doar una.",
     "Jedan tim od <strong>3 osobe</strong> montira prizemnu kuću od 100 m² za <strong>manje od 3 sedmice</strong>, gotovo završenu. Dok klasična gradnja angažuje do 5 različitih timova (zidari, spoljašnja izolacija, unutrašnja izolacija, gips-karton majstori, zaptivači), Polistibrick zahtijeva samo jedan."),
    ("Câte meserii înživi Polistibrick?", "Koliko zanata Polistibrick zamjenjuje?"),
    ("<strong>Cinci, într-o jedna montare</strong>: zidăria, izolacija exterioară (ETICS), izolacija interioară, obloga / finisarea i etanșeitatea la aer. Un singur proizvod i o jedna tim — u loc de cinci materijali i cinci timovi diferite.",
     "<strong>Pet u jednoj montaži</strong>: zidanje, spoljašnja izolacija (ETICS), unutrašnja izolacija, obloga / završna obrada i zaptivanje vazduha. Jedan proizvod i jedan tim — umjesto pet materijala i pet različitih timova."),
    ("Rețelele se trag <strong>prin oplata</strong> înainte de închidere, exact ca într-un zid de gips-carton. Conductele su integrisane u montaža, nu tratate separat.",
     "Mreže se provlače <strong>kroz oplatu</strong> prije zatvaranja, baš kao u gips-karton zidu. Cjevovodi su integrisani u montažu, ne obrađuju se odvojeno."),
    ("Koliko ću uštedjeti na računima za 25 godina?", "Koliko ću uštedjeti na računima za 25 godina?"),
    # privatnost
    ("Politică de privatnost · GDPR · Polistibrick", "Politika privatnosti · GDPR · Polistibrick"),
    ("Politică de privatnost (GDPR)", "Politika privatnosti (GDPR)"),
    ("Kako colectăm, utilizăm i protejăm datele vi personale conform GDPR. Drepturile vi i kako le puteți exercita.",
     "Kako prikupljamo, koristimo i štitimo vaše lične podatke u skladu sa GDPR-om. Vaša prava i kako ih možete ostvariti."),
    ("Kako colectăm, utilizăm i protejăm datele vi personale. Conform Regulamentului UE 2016/679 (GDPR). Ultima actualizare: 3 iulie 2026.",
     "Kako prikupljamo, koristimo i štitimo vaše lične podatke. U skladu sa Uredbom EU 2016/679 (GDPR). Posljednje ažuriranje: 3. jul 2026."),
    # o-nama
    ("Țări de prezență", "Zemlje prisustva"),
    ("Šta ne deosebește.", "Šta nas izdvaja."),
    ("Credem da performansa superioară nu trebuie rezervată celor sa buget nelimitat. Kuća pasivna Polistibrick costă la fel ca o kuća klasična — sa 30 % više malo nego alternativa pasivna tradicionalna.",
     "Vjerujemo da vrhunske performanse ne treba da budu rezervisane za one sa neograničenim budžetom. Polistibrick pasivna kuća košta isto kao klasična kuća — 30% manje od tradicionalne pasivne alternative."),
    # zidovi-mbk
    ("Un oplata. <em>O kuća întreagă.</em>", "Jedna oplata. <em>Cijela kuća.</em>"),
    ("Cigla klasična are nevoie de više de 10 materijali i 4-5 timovi diferite za un zid finit. MBK le înživi pe sve:",
     "Klasična cigla zahtijeva više od 10 materijala i 4-5 različitih timova za gotov zid. MBK ih sve zamjenjuje:"),
    ("<strong>Oplata:</strong> struktura modulară koji primește betonul", "<strong>Oplata:</strong> modularna struktura koja prima beton"),
    ("<strong>Struktura portantă:</strong> beton armat de 15 cm — rezistență la cutremure i la foc A1",
     "<strong>Noseća struktura:</strong> armirani beton od 15 cm — otpornost na zemljotrese i vatru A1"),
    ("Zatražite la dokumentacija", "Zatražite dokumentaciju"),
    # uslovi title
    ("Uslovi i condiții generale · Polistibrick", "Opšti uslovi · Polistibrick"),
    ("Uslovi i condiții generale", "Opšti uslovi"),
]

TARGETS = [
    "countries/me/za/vlasnici/index.html",
    "countries/me/resursi/faq/index.html",
    "countries/me/legal/privatnost/index.html",
    "countries/me/legal/uslovi/index.html",
    "countries/me/o-nama/index.html",
    "countries/me/proizvodi/zidovi-mbk/index.html",
    "countries/me/proizvodi/podovi-pbk/index.html",
    "countries/me/proizvodi/krov-tbk/index.html",
]

root = Path(__file__).resolve().parent
for rel in TARGETS:
    p = root / rel
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    orig = t
    for a, b in sorted(FIXES, key=lambda x: -len(x[0])):
        t = t.replace(a, b)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print(f"fixed {rel}")
