#!/usr/bin/env python3
"""Final visible-text fixes for ME Montenegrin pages."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "countries/me"

FIXES = [
    ("Construiesc singur →", "Gradim sami →"),
    ("Un singur", "Jedan"),
    ("«&nbsp;Kako grade asta&nbsp;?&nbsp;»", "«&nbsp;Kako da ovo izgradim?&nbsp;»"),
    ("Sa Polistibrick, je posibil.", "Sa Polistibrick-om, moguće je."),
    ("Tu proiectezi,<br><em>Polistibrick execută.</em>", "Vi projektujete,<br><em>Polistibrick izvodi.</em>"),
    ("5 echipe — 15 persoane", "5 timova — 15 osoba"),
    ("Blocuri • Mortar • Oplata • Fier • Beton • Izolacija • Placare • Șuruburi • etc.", "Blokovi • Malter • Oplata • Čelik • Beton • Izolacija • Obloga • Vijci • itd."),
    ("Za prva dată, imaginația ta nu više are limite — console generoase i deschideri ample, în calcule Eurocode 2 clasice.", "Prvi put, vašoj mašti više nema granica — velikodušni konzoli i široki otvori, u klasičnim proračunima Eurocode 2."),
    ("cinci proizvodi într-un singur panel", "pet proizvoda u jednom panelu"),
    ("3 proizvodi consolidate intr-o singura sectiune", "3 proizvoda objedinjena u jednoj sekciji"),
    ("Singurul ICF sa ova garancija.", "Jedini ICF sa ovom garancijom."),
    ("De la temelj la cofrajul închis — gata za turnarea betonului. Întregul proces în câteva sedmice, sa doar 2–3 persoane pe gradilište.", "Od temelja do zatvorene oplate — spremno za betoniranje. Cijeli proces za nekoliko sedmica, sa samo 2–3 osobe na gradilištu."),
    ("Oplata închis, gata za turnarea betonului", "Zatvorena oplata, spremna za betoniranje"),
    ("Sve elementele asamblate i verificate. <strong>Smo gata za turnarea betonului.</strong>", "Svi elementi montirani i provjereni. <strong>Spremni smo za betoniranje.</strong>"),
    ("După turnarea betonului, structura devine <strong>monolitică în 24 de ore</strong> — zidovi, podovi, krov, izolate continuu, bez punți termičke.", "Nakon betoniranja, struktura postaje <strong>monolitna za 24 sata</strong> — zidovi, podovi, krov, kontinuirano izolirani, bez termičkih mostova."),
    ("L-am testat pe prvi gradilište i, sincer, <em>e o minune</em>. Peretele se ridică aproape singur — nu ne întoarcem înapoi.", "Testirali smo na prvom gradilištu i, iskreno, <em>to je čudo</em>. Zid se podiže gotovo sam — ne vraćamo se nazad."),
    ("Sa aceeași echipă, grade <em>više više multe kuće</em> pe godina. Planificarea ține în sfârșit.", "Sa istim timom gradim <em>mnogo više kuća</em> godišnje. Planiranje konačno drži."),
    ("Redirecționare către", "Preusmjeravanje na"),
    ("Pentru proprietari", "Za vlasnike"),
    ("Pentru arhitecți", "Za arhitekte"),
    ("Pentru constructori", "Za građevince"),
    ("Pentru investitori", "Za investitore"),
    ("Întrebări frecvente", "Često postavljana pitanja"),
    ("Compania", "Kompanija"),
    ("Brevet", "Patent"),
    ("Certificări", "Sertifikati"),
    ("Fabricile noastre", "Naše fabrike"),
    ("Fondatorul", "Osnivač"),
    ("Devis", "Ponuda"),
    ("Devis gratuit", "Besplatna ponuda"),
    ("Economii", "Uštede"),
    ("Témoignages", "Svjedočanstva"),
    ("Produits", "Proizvodi"),
    ("Solutions", "Rješenja"),
    ("Projets", "Projekti"),
    ("Calculateur", "Kalkulator"),
    ("Ressources", "Resursi"),
    ("À propos", "O nama"),
    ("Pour les propriétaires", "Za vlasnike"),
    ("Pour les architectes", "Za arhitekte"),
    ("Pour les constructeurs", "Za građevince"),
    ("Pour les investisseurs", "Za investitore"),
    ("→ Devenez partenaire", "→ Postanite partner"),
    ("Maisons construites", "Izgrađene kuće"),
    ("Témoignages (vidéo)", "Svjedočanstva (video)"),
    ("Calculateur de coût", "Kalkulator troškova"),
    ("Calculateur d'économies (vs brique)", "Kalkulator ušteda (naspram cigle)"),
    ("Questions fréquentes", "Često postavljana pitanja"),
    ("L'entreprise", "Kompanija"),
    ("Le fondateur", "Osnivač"),
    ("Nos usines", "Naše fabrike"),
    ("Changer de pays", "Promijeni zemlju"),
    ("Navigation du site", "Navigacija sajta"),
    ("Je reste ici", "Ostajem ovdje"),
    ("Da, mergi", "Da, idi"),
    ("Nous détectons que vous êtes en", "Detektujemo da ste u"),
    ("Vizitezi", "Posjećujete"),
]

def main():
    for html in sorted(ROOT.rglob("*.html")):
        t = html.read_text(encoding="utf-8")
        orig = t
        for a, b in sorted(FIXES, key=lambda x: -len(x[0])):
            t = t.replace(a, b)
        if t != orig:
            html.write_text(t, encoding="utf-8")
    fr = Path(__file__).resolve().parent / "translations/fr_to_cnr.json"
    data = json.loads(fr.read_text(encoding="utf-8"))
    data.update(dict(FIXES))
    fr.write_text(json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Final fixes applied ({len(FIXES)} phrases)")

if __name__ == "__main__":
    main()
