#!/usr/bin/env python3
"""Rebuild countries/me from EN with safe phrase-only Montenegrin translation."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EN_TO_ME = {
    "products": "proizvodi", "walls-mbk": "zidovi-mbk", "floors-pbk": "podovi-pbk",
    "roof-tbk": "krov-tbk", "for": "za", "homeowners": "vlasnici", "architects": "arhitekti",
    "builders": "gradjevinci", "investors": "investitori", "about": "o-nama",
    "certifications": "sertifikati", "factories": "fabrike", "founder": "osnivac",
    "patent": "patent", "resources": "resursi", "projects": "projekti",
    "house-cluj-napoca": "kuca-cluj-napoca", "lyon-development": "kompleks-lyon",
    "villa-valencia": "vila-valencia", "savings": "ustede", "quote": "ponuda",
    "calculator": "kalkulator", "testimonials": "svjedocanstva",
    "become-a-partner": "postani-partner", "installation": "montaza",
    "privacy": "privatnost", "sustainability": "odrzivost", "terms": "uslovi",
    "cookies": "kolacici", "legal-notice": "pravne-napomene",
    "what-is-a-passive-house": "sta-je-pasivna-kuca", "comparison": "poredjenje",
}

EN_TO_ME_FILES = {
    "index.html": "index.html",
    "polistibrick-mercury-style.html": "polistibrick-mercury-style.html",
    "products/walls-mbk/index.html": "proizvodi/zidovi-mbk/index.html",
    "products/floors-pbk/index.html": "proizvodi/podovi-pbk/index.html",
    "products/roof-tbk/index.html": "proizvodi/krov-tbk/index.html",
    "for/homeowners/index.html": "za/vlasnici/index.html",
    "for/architects/index.html": "za/arhitekti/index.html",
    "for/builders/index.html": "za/gradjevinci/index.html",
    "for/investors/index.html": "za/investitori/index.html",
    "about/index.html": "o-nama/index.html",
    "about/patent/index.html": "o-nama/patent/index.html",
    "about/certifications/index.html": "o-nama/sertifikati/index.html",
    "about/factories/index.html": "o-nama/fabrike/index.html",
    "about/founder/index.html": "o-nama/osnivac/index.html",
    "projects/index.html": "projekti/index.html",
    "projects/house-cluj-napoca/index.html": "projekti/kuca-cluj-napoca/index.html",
    "projects/lyon-development/index.html": "projekti/kompleks-lyon/index.html",
    "projects/villa-valencia/index.html": "projekti/vila-valencia/index.html",
    "testimonials/index.html": "svjedocanstva/index.html",
    "savings/index.html": "ustede/index.html",
    "calculator/index.html": "kalkulator/index.html",
    "quote/index.html": "ponuda/index.html",
    "become-a-partner/index.html": "postani-partner/index.html",
    "installation/index.html": "montaza/index.html",
    "contact/index.html": "contact/index.html",
    "resources/index.html": "resursi/index.html",
    "resources/faq/index.html": "resursi/faq/index.html",
    "resources/blog/index.html": "resursi/blog/index.html",
    "legal/privacy/index.html": "legal/privatnost/index.html",
    "legal/sustainability/index.html": "legal/odrzivost/index.html",
    "legal/terms/index.html": "legal/uslovi/index.html",
    "legal/cookies/index.html": "legal/kolacici/index.html",
    "legal/legal-notice/index.html": "legal/pravne-napomene/index.html",
}

PROTECT_TOKENS = [
    "Polistibrick", "Passivhaus", "Web3Forms", "Cloudflare", "localhost",
    "github.io", "vercel.app", "polistibrick.me", "polistibrick.com",
    "MBK", "PBK", "TBK", "BIM", "ICF", "GDPR", "RGPD", "CE", "ETA", "ISO",
    "PDF", "DWG", "DXF", "JPG", "PNG", "ZIP", "webp", "webm", "woff2",
    "font-weight", "transform", "webkit", "translateY", "translateX",
]

# Build EN→CNR from fr bridge + extras
fr_en = json.loads((ROOT / "translations/fr_to_en.json").read_text(encoding="utf-8"))
fr_cnr = json.loads((ROOT / "translations/fr_to_cnr.json").read_text(encoding="utf-8"))
EN_TO_CNR = {en: fr_cnr[fr] for fr, en in fr_en.items() if fr in fr_cnr and en != fr_cnr[fr]}

EN_TO_CNR.update({
    "For homeowners · A home for life, no bills — Polistibrick": "Za vlasnike · Kuća za cijeli život bez računa — Polistibrick",
    "Build a certified passive house, no high energy bills, guaranteed for 50 years. Cost calculator, transparent comparison, certified architects near you.": "Gradite certificiranu pasivnu kuću, bez visokih računa za energiju, garancija 50 godina. Kalkulator troškova, transparentno poređenje, certificirani arhitekti u vašoj blizini.",
    "One house. One system. No compromise.": "Jedna kuća. Jedan sistem. Bez kompromisa.",
    "One house. One system.": "Jedna kuća. Jedan sistem.",
    "Complete ICF system — walls, floors, roof. A+++ standard. Built in 4 weeks. No compromise, no bills.": "Kompletan ICF sistem — zidovi, podovi, krov. standard A+++. Izgrađeno za 4 sedmice. Bez kompromisa, bez računa.",
    "Complete ICF system for A+++ house. Walls, floors, roof — one premium system.": "Kompletan ICF sistem za kuću A+++. Zidovi, podovi, krov — premium sistem.",
    "Redirecting to": "Preusmjeravanje na",
    "Polistibrick — Smart construction": "Polistibrick — Pametna gradnja",
    "Polistibrick — home": "Polistibrick — početna",
    "Get your free quote →": "Dobijte besplatnu ponudu →",
    "How do I build this?": "Kako da ovo izgradim?",
    "With Polistibrick, it's possible.": "Sa Polistibrick-om, moguće je.",
    "You imagine,": "Vi zamislite,",
    "Polistibrick delivers.": "Polistibrick izvodi.",
    "A technology": "Jedna tehnologija",
    "with 5 advantages": "sa 5 prednosti",
    "Polistibrick replaces 5 different materials and 5 construction teams. One product, one team — and the house is complete.": "Polistibrick zamjenjuje 5 različitih materijala i 5 građevinskih timova. Jedan proizvod, jedan tim — i kuća je završena.",
    "One team - 3 people": "Jedan tim — 3 osobe",
    "One single team = the margin of 5 teams — up to 50%": "Jedan tim = marža od 5 timova — do 50%",
    "Five fewer lines on the quote,": "Pet linija manje na ponudi,",
    "more premium for you.": "više premiuma za vas.",
    "One house.": "Jedna kuća.",
    "Three products.": "Tri proizvoda.",
    "A complete house": "Kompletna kuća",
    "in 4 steps.": "u 4 koraka.",
    "Request a personalised quote": "Zatražite personalizovanu ponudu",
    "We detect you're in": "Detektujemo da ste u",
    "Visit": "Posjećujete",
    "Yes, go": "Da, idi",
    "Stay here": "Ostajem ovdje",
    "Change country": "Promijeni zemlju",
    "Site navigation": "Navigacija sajta",
    "FAQ": "Često postavljana pitanja",
    "Free quote": "Besplatna ponuda",
    "Get a quote": "Zatražite ponudu",
    "About us": "O nama",
    "Legal notice": "Pravne napomene",
    "Legal information": "Pravne informacije",
    "Cookie consent": "Saglasnost za kolačiće",
    "cookie policy": "politiku kolačića",
    "privacy policy": "politiku privatnosti",
    "privacy policy (GDPR)": "politika privatnosti (GDPR)",
    "We use cookies and third-party services to improve the site. See our": "Koristimo kolačiće i usluge trećih strana za poboljšanje sajta. Pogledajte našu",
    "Which country are you": "U kojoj zemlji",
    "building in?": "gradite?",
    "Choose your country": "Odaberite svoju zemlju",
    "🌍 Choose your country": "🌍 Odaberite svoju zemlju",
    "★ Your country": "★ Vaša zemlja",
    "Your country isn't listed? Write to us at": "Vaša zemlja nije na listi? Pišite nam na",
    "We'll redirect you to your country's site with the local team, direct contact and a quote in your language.": "Preusmjeravamo vas na sajt vaše zemlje sa lokalnim timom, direktnim kontaktom i ponudom na vašem jeziku.",
    "© 2026 Polistibrick. All rights reserved. Patented system.": "© 2026 Polistibrick. Sva prava zadržana. Patentirani sistem.",
    "Main navigation": "Glavna navigacija",
    "Open menu": "Otvorite meni",
    "Navigation menu": "Meni navigacije",
    "Products": "Proizvodi", "Solutions": "Rješenja", "Projects": "Projekti",
    "Calculator": "Kalkulator", "Resources": "Resursi", "About": "O nama", "Contact": "Kontakt",
    "MBK Walls": "Zidovi MBK", "PBK Floors": "Podovi PBK", "TBK Roof": "Krov TBK",
    "For owners": "Za vlasnike", "For architects": "Za arhitekte", "For builders": "Za građevince",
    "For investors": "Za investitore", "→ Become a partner": "→ Postanite partner",
    "Houses built": "Izgrađene kuće", "Testimonials (video)": "Svjedočanstva (video)",
    "Cost calculator": "Kalkulator troškova", "Savings calculator": "Kalkulator ušteda",
    "Company": "Kompanija", "Certifications": "Sertifikati", "Our factories": "Naše fabrike",
    "Team": "Tim", "Founder": "Osnivač", "Patent": "Patent",
    "Completed projects": "Realizovani projekti", "Terms": "Uslovi", "Privacy": "Privatnost",
    "Sustainability": "Održivost", "Cookies": "Kolačići", "Quote": "Ponuda",
    "Installation": "Montaža", "Savings": "Uštede", "Testimonials": "Svjedočanstva",
    "Become a partner": "Postanite partner", "Comparison": "Poređenje",
    "Owners": "Vlasnici", "Architects": "Arhitekti", "Builders": "Građevinci", "Investors": "Investitori",
    "Accept": "Prihvati", "Decline": "Odbij", "Close": "Zatvori", "Call": "Pozovite",
    "Learn more": "Saznajte više", "Read →": "Pročitaj →", "Send message": "Pošaljite poruku",
    "How can we help you?": "Kako vam možemo pomoći?",
    "Message sent": "Poruka poslata", "Thank you!": "Hvala!",
    "Our team will reply within 24 business hours.": "Naš tim vam odgovara u roku od 24 radna sata.",
    "Select country": "Odaberite zemlju", "You are": "Vi ste",
    "Individual / Owner": "Pojedinac / vlasnik", "Builder / Contractor": "Građevinac / preduzetnik",
    "Developer / Investor": "Investitor", "Other": "Ostalo", "Your name": "Vaše ime",
    "Name": "Ime", "Phone": "Telefon", "Message": "Poruka", "Subject": "Predmet",
    "Select": "Odaberite", "Remove": "Ukloni",
    "Maximum 10 MB per file.": "Maksimalno 10 MB po datoteci.",
    "The file": "Datoteka", "is too large": "je prevelika",
    "Hello,": "Zdravo,", "Thanks in advance.": "Hvala unaprijed.",
    "Walls · MBK": "Zidovi · MBK", "Floors · PBK": "Podovi · PBK", "Roof · TBK": "Krov · TBK",
    "Quick contact": "Brzi kontakt", "Call Polistibrick": "Pozovite Polistibrick",
    "Send an email": "Pošaljite e-mail", "Specialists one click away.": "Stručnjaci na klik.",
    "Write to us directly.": "Pišite nam direktno.",
    "Insulating formwork for load-bearing walls": "Izolaciona oplata za noseće zidove",
    "Prefab panels with 10.8 h thermal lag": "Prefabrikovani paneli sa faznim pomakom 10,8 h",
    "Passivhaus system from the factory": "Passivhaus sistem iz fabrike",
    "Corners, ends, stairs, windows": "Uglovi, završeci, stepenice, prozori",
    "Passive house without high bills": "Pasivna kuća bez visokih računa",
    "Construction details, BIM, datasheets": "Konstruktivni detalji, BIM, listovi",
    "Installation, certification, partnership": "Montaža, certifikacija, partnerstvo",
    "ROI, execution speed, developments": "ROI, brzina izvođenja, kompleksi",
    "Certified builder application": "Prijava certificiranih građevinaca",
    "Gallery + map of projects": "Galerija + mapa projekata",
    "Owners speak, with real figures": "Vlasnici govore, sa stvarnim brojkama",
    "Estimate panel prices for your house": "Procijenite cijenu panela za vašu kuću",
    "Polistibrick vs brick over 25 years": "Polistibrick naspram cigle za 25 godina",
    "Articles about Passive House, ICF": "Članci o pasivnoj kući, ICF-u",
    "Answers to the most common questions": "Odgovori na najčešća pitanja",
    "Who we are, vision, mission": "Ko smo mi, vizija, misija",
    "Polistibrick Patent": "Polistibrick patent",
    "The patent that makes us unique": "Patent koji nas čini jedinstvenim",
    "CE, ISO, Passivhaus, technical approvals": "CE, ISO, Passivhaus, odobrenja",
    "Valencia (ES) and Craiova (RO)": "Valencija (ES) i Krajova (RO)",
    "Founders and our people": "Osnivači i naši saradnici",
    "The patented ICF system for premium passive houses, with no energy bills. Made in the EU.": "Patentirani ICF sistem za premium pasivne kuće, bez računa za energiju. Proizvedeno u EU.",
    "Polistibrick vs classic system vs other ICF": "Polistibrick naspram klasičnog sistema naspram drugog ICF-a",
    "and": "i",
})

PAIRS = sorted(EN_TO_CNR.items(), key=lambda x: -len(x[0]))


def rewrite_en_paths(text: str) -> str:
    for en, me in sorted(EN_TO_ME.items(), key=lambda x: -len(x[0])):
        text = text.replace(f"/{en}/", f"/{me}/")
        text = text.replace(f'"{en}/', f'"{me}/')
        text = text.replace(f"'{en}/", f"'{me}/")
    return text


def shield(text: str) -> tuple[str, dict[str, str]]:
    vault = {}
    for i, tok in enumerate(PROTECT_TOKENS):
        key = f"\x00§{i}§\x00"
        if tok in text:
            vault[key] = tok
            text = text.replace(tok, key)
    return text, vault


def unshield(text: str, vault: dict[str, str]) -> str:
    for key, tok in vault.items():
        text = text.replace(key, tok)
    return text


def translate_block(text: str) -> str:
    text, vault = shield(text)
    for en, cnr in PAIRS:
        text = text.replace(en, cnr)
    return unshield(text, vault)


def translate_html(text: str) -> str:
    parts = re.split(r"(<script[\s\S]*?</script>|<style[\s\S]*?</style>)", text, flags=re.I)
    return "".join(p if i % 2 else translate_block(p) for i, p in enumerate(parts))


def process_file(en_rel: str, me_rel: str) -> None:
    src = ROOT / "countries/en" / en_rel
    dst = ROOT / "countries/me" / me_rel
    text = src.read_text(encoding="utf-8")
    text = text.replace('lang="en"', 'lang="cnr"')
    text = rewrite_en_paths(text)
    text = translate_html(text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def main():
    for en_rel, me_rel in EN_TO_ME_FILES.items():
        process_file(en_rel, me_rel)
    out = ROOT / "translations/en_to_cnr.json"
    out.write_text(json.dumps(dict(sorted(EN_TO_CNR.items())), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rebuilt {len(EN_TO_ME_FILES)} pages; {len(EN_TO_CNR)} EN→CNR pairs")


if __name__ == "__main__":
    main()
