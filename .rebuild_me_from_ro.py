#!/usr/bin/env python3
"""Rebuild countries/me from RO — phrase-only Montenegrin translation (safe)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

RO_TO_ME = {
    "produse": "proizvodi", "pereti-mbk": "zidovi-mbk", "planseu-pbk": "podovi-pbk",
    "acoperis-tbk": "krov-tbk", "pentru": "za", "proprietari": "vlasnici",
    "arhitecti": "arhitekti", "constructori": "gradjevinci", "investitori": "investitori",
    "despre": "o-nama", "certificari": "sertifikati", "fabrici": "fabrike",
    "echipa": "osnivac", "patent": "patent", "proiecte": "projekti",
    "casa-cluj-napoca": "kuca-cluj-napoca", "ansamblu-lyon": "kompleks-lyon",
    "villa-valencia": "vila-valencia", "economii": "ustede", "oferta": "ponuda",
    "calculator": "kalkulator", "testimoniale": "svjedocanstva",
    "devino-partener": "postani-partner", "montaj": "montaza", "resurse": "resursi",
    "confidentialitate": "privatnost", "sustenabilitate": "odrzivost",
    "termeni": "uslovi", "mentiuni-legale": "pravne-napomene", "cookies": "kolacici",
    "ce-este-casa-passiva": "sta-je-pasivna-kuca", "comparatie": "poredjenje",
    "accesorii": "pribor",
}

RO_TO_ME_FILES = {
    "index.html": "index.html",
    "polistibrick-mercury-style.html": "polistibrick-mercury-style.html",
    "produse/pereti-mbk/index.html": "proizvodi/zidovi-mbk/index.html",
    "produse/planseu-pbk/index.html": "proizvodi/podovi-pbk/index.html",
    "produse/acoperis-tbk/index.html": "proizvodi/krov-tbk/index.html",
    "pentru/proprietari/index.html": "za/vlasnici/index.html",
    "pentru/arhitecti/index.html": "za/arhitekti/index.html",
    "pentru/constructori/index.html": "za/gradjevinci/index.html",
    "pentru/investitori/index.html": "za/investitori/index.html",
    "despre/index.html": "o-nama/index.html",
    "despre/patent/index.html": "o-nama/patent/index.html",
    "despre/certificari/index.html": "o-nama/sertifikati/index.html",
    "despre/fabrici/index.html": "o-nama/fabrike/index.html",
    "despre/echipa/index.html": "o-nama/osnivac/index.html",
    "proiecte/index.html": "projekti/index.html",
    "proiecte/casa-cluj-napoca/index.html": "projekti/kuca-cluj-napoca/index.html",
    "proiecte/ansamblu-lyon/index.html": "projekti/kompleks-lyon/index.html",
    "proiecte/villa-valencia/index.html": "projekti/vila-valencia/index.html",
    "testimoniale/index.html": "svjedocanstva/index.html",
    "economii/index.html": "ustede/index.html",
    "calculator/index.html": "kalkulator/index.html",
    "oferta/index.html": "ponuda/index.html",
    "devino-partener/index.html": "postani-partner/index.html",
    "montaj/index.html": "montaza/index.html",
    "contact/index.html": "contact/index.html",
    "resurse/index.html": "resursi/index.html",
    "resurse/faq/index.html": "resursi/faq/index.html",
    "resurse/blog/index.html": "resursi/blog/index.html",
    "legal/confidentialitate/index.html": "legal/privatnost/index.html",
    "legal/sustenabilitate/index.html": "legal/odrzivost/index.html",
    "legal/termeni/index.html": "legal/uslovi/index.html",
    "legal/cookies/index.html": "legal/kolacici/index.html",
    "legal/mentiuni-legale/index.html": "legal/pravne-napomene/index.html",
}

# ui_strings ro→cnr (full nav/footer strings)
ui = json.loads((ROOT / "translations/ui_strings.json").read_text(encoding="utf-8"))
PHRASES = {v: ui["cnr"][k] for k, v in ui["ro"].items() if k in ui["cnr"] and v != ui["cnr"][k]}

# Page-level RO→CNR phrases (multi-word only — safe)
PHRASES.update({
    "Pentru proprietari · Casa pe viață, fără facturi — Polistibrick": "Za vlasnike · Kuća za cijeli život bez računa — Polistibrick",
    "Construiți o casă pasivă certificată, fără facturi mari la energie, garanție 50 de ani. Calculator de economii, comparație transparentă, arhitecți certificați Polistibrick în apropiere.": "Gradite certificiranu pasivnu kuću, bez visokih računa za energiju, garancija 50 godina. Kalkulator ušteda, transparentno poređenje, certificirani arhitekti Polistibrick u vašoj blizini.",
    "O casă. Un sistem. Fără compromis.": "Jedna kuća. Jedan sistem. Bez kompromisa.",
    "O casă. Un sistem.": "Jedna kuća. Jedan sistem.",
    "Sistem ICF complet — pereți, planșee, acoperiș. standard A+++. Construit în 4 săptămâni. Fără compromis, fără facturi.": "Kompletan ICF sistem — zidovi, podovi, krov. standard A+++. Izgrađeno za 4 sedmice. Bez kompromisa, bez računa.",
    "Sistem ICF complet pentru casă A+++. Pereți, planșee, acoperiș — un sistem premium.": "Kompletan ICF sistem za kuću A+++. Zidovi, podovi, krov — premium sistem.",
    "Redirecționare către": "Preusmjeravanje na",
    "Detectăm că ești în": "Detektujemo da ste u",
    "Vizitezi": "Posjećujete",
    "Da, mergi": "Da, idi",
    "Rămân aici": "Ostajem ovdje",
    "Schimbă țara": "Promijeni zemlju",
    "Navigare site": "Navigacija sajta",
    "Cofraj-pierdut pentru pereți portanți": "Izolaciona oplata za noseće zidove",
    "Panouri prefabricate cu defazaj 10,8 h": "Prefabrikovani paneli sa faznim pomakom 10,8 h",
    "Sistem Passivhaus din fabrică": "Passivhaus sistem iz fabrike",
    "Colțare, capete, scări, ferestre": "Uglovi, završeci, stepenice, prozori",
    "Casă pasivă fără facturi mari": "Pasivna kuća bez visokih računa",
    "Detalii constructive, BIM, fișe": "Konstruktivni detalji, BIM, listovi",
    "Montaj, certificare, parteneriat": "Montaža, certifikacija, partnerstvo",
    "ROI, viteză execuție, ansambluri": "ROI, brzina izvođenja, kompleksi",
    "→ Devino partener": "→ Postanite partner",
    "Aplicație constructori certificați": "Prijava certificiranih građevinaca",
    "Case construite": "Izgrađene kuće",
    "Galerie + hartă cu proiecte": "Galerija + mapa projekata",
    "Testimoniale (video)": "Svjedočanstva (video)",
    "Proprietarii vorbesc, cu cifre reale": "Vlasnici govore, sa stvarnim brojkama",
    "Calculator cost": "Kalkulator troškova",
    "Estimează prețul panourilor casei tale": "Procijenite cijenu panela za vašu kuću",
    "Calculator economii": "Kalkulator ušteda",
    "Polistibrick vs cărămidă pe 25 de ani": "Polistibrick naspram cigle za 25 godina",
    "Articole despre Casa Pasivă, ICF": "Članci o pasivnoj kući, ICF-u",
    "Întrebări frecvente": "Često postavljana pitanja",
    "Răspunsuri la cele mai comune întrebări": "Odgovori na najčešća pitanja",
    "Cine suntem, viziune, misiune": "Ko smo mi, vizija, misija",
    "Patentul Polistibrick": "Polistibrick patent",
    "Brevetul care ne face unici": "Patent koji nas čini jedinstvenim",
    "CE, ISO, Passivhaus, agremente": "CE, ISO, Passivhaus, odobrenja",
    "Valencia (ES) și Craiova (RO)": "Valencija (ES) i Krajova (RO)",
    "Fondatori și oamenii noștri": "Osnivači i naši saradnici",
    "Sistemul ICF brevetat pentru case pasive premium, fără facturi de energie. Fabricat în UE.": "Patentirani ICF sistem za premium pasivne kuće, bez računa za energiju. Proizvedeno u EU.",
    "Proiecte realizate": "Realizovani projekti",
    "Despre noi": "O nama",
    "Mențiuni legale": "Pravne napomene",
    "Politică cookies": "Politika kolačića",
    "Informații legale": "Pravne informacije",
    "© 2026 Polistibrick. Toate drepturile rezervate. Sistem brevetat.": "© 2026 Polistibrick. Sva prava zadržana. Patentirani sistem.",
    "Alege țara": "Odaberite svoju zemlju",
    "🌍 Alege țara ta": "🌍 Odaberite svoju zemlju",
    "În ce țară": "U kojoj zemlji",
    "construiești?": "gradite?",
    "Te redirecționăm la site-ul țării tale cu echipă locală, contact direct și ofertă în limba ta.": "Preusmjeravamo vas na sajt vaše zemlje sa lokalnim timom, direktnim kontaktom i ponudom na vašem jeziku.",
    "★ Țara ta": "★ Vaša zemlja",
    "Țara ta nu e listată? Scrie-ne la": "Vaša zemlja nije na listi? Pišite nam na",
    "Polistibrick — Construcție inteligentă": "Polistibrick — Pametna gradnja",
    "Polistibrick vs sistem clasic vs alt ICF": "Polistibrick naspram klasičnog sistema naspram drugog ICF-a",
    "Ofertă gratuită": "Besplatna ponuda",
    "Folosim cookie-uri și servicii terțe pentru a îmbunătăți site-ul. Consultați": "Koristimo kolačiće i usluge trećih strana za poboljšanje sajta. Pogledajte",
    "politica de cookies": "politiku kolačića",
    "politica de confidențialitate": "politiku privatnosti",
    "Consimțământ cookies": "Saglasnost za kolačiće",
    "Contact rapid": "Brzi kontakt",
    "Sună Polistibrick": "Pozovite Polistibrick",
    "Trimite e-mail": "Pošaljite e-mail",
    "Cum vă putem ajuta?": "Kako vam možemo pomoći?",
    "Mesaj trimis": "Poruka poslata",
    "Echipa noastră vă răspunde în maximum 24 de ore lucrătoare.": "Naš tim vam odgovara u roku od 24 radna sata.",
    "Specialiști la un click distanță.": "Stručnjaci na klik.",
    "Scrie-ne direct.": "Pišite nam direktno.",
    "Maximum 10 MB per fișier.": "Maksimalno 10 MB po datoteci.",
    "Pentru arhitecți": "Za arhitekte",
    "Pentru constructori": "Za građevince",
    "Pentru investitori": "Za investitore",
    "Pentru proprietari": "Za vlasnike",
    "Cere ofertă": "Zatražite ponudu",
    "Devino partener": "Postanite partner",
    "Navigare principală": "Glavna navigacija",
    "Deschide meniul": "Otvorite meni",
    "Meniu navigare": "Meni navigacije",
    "Polistibrick — acasă": "Polistibrick — početna",
    "Acceptați politica de confidențialitate pentru a continua.": "Prihvatite politiku privatnosti da biste nastavili.",
    "Se trimite…": "Šalje se…",
    "Formular indisponibil. Contact:": "Formular nije dostupan. Kontakt:",
})

# Full ro_to_cnr phrase dictionary
ro_cnr = json.loads((ROOT / "translations/ro_to_cnr.json").read_text(encoding="utf-8"))
PHRASES.update({k: v for k, v in ro_cnr.items() if k != v})

PAIRS = sorted({k: v for k, v in PHRASES.items() if k != v and (len(k) >= 6 or " " in k)}.items(), key=lambda x: -len(x[0]))


def rewrite_ro_paths(text: str) -> str:
    for ro, me in sorted(RO_TO_ME.items(), key=lambda x: -len(x[0])):
        text = text.replace(f"/{ro}/", f"/{me}/")
        text = text.replace(f'"{ro}/', f'"{me}/')
        text = text.replace(f"'{ro}/", f"'{me}/")
    return text


def translate_block(text: str) -> str:
    for ro, cnr in PAIRS:
        text = text.replace(ro, cnr)
    return text


def translate_html(text: str) -> str:
    parts = re.split(r"(<script[\s\S]*?</script>|<style[\s\S]*?</style>)", text, flags=re.I)
    return "".join(p if i % 2 else translate_block(p) for i, p in enumerate(parts))


def process_file(ro_rel: str, me_rel: str) -> None:
    src = ROOT / "countries/ro" / ro_rel
    dst = ROOT / "countries/me" / me_rel
    text = src.read_text(encoding="utf-8")
    text = text.replace('lang="ro"', 'lang="cnr"')
    text = rewrite_ro_paths(text)
    text = translate_html(text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def main():
    for ro_rel, me_rel in RO_TO_ME_FILES.items():
        process_file(ro_rel, me_rel)
    print(f"Phrase-safe rebuilt {len(RO_TO_ME_FILES)} pages ({len(PAIRS)} phrases)")


if __name__ == "__main__":
    main()
