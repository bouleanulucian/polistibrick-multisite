#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificările site-ului FR B2B (spec 2026-09-21 §2 și §7):
cuvinte interzise pe site, URL-uri vechi fără pagină și fără 301, placeholder-e rămase.

Rulare: python3 build/build.py fr && python3 scripts/verif-fr.py
Iese cu 1 la prima problemă; le listează pe toate.
"""
import re, sys, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'build' / 'fr'

# decizia patronului (21.09): zero ATEx / Avis Technique; termenul francez e «bloc coffrant isolant», nu «ICF»;
# «5-en-1» e sloganul lui Isolabloc; formarea e pe șantier, nu la fabrică; fără promisiuni fără cifră.
INTERZISE = ['ATEx', 'Avis Technique', 'DTA', 'technique courante', 'ICF', '5-en-1', '5 en 1',
             "formation à l'usine", "visite d'usine", 'dans nos usines', 'délais fermes', 'zéro sinistre',
             'polistibrick.eu', 'révolution', 'maison de rêve', 'devis gratuit', 'pas cher', '48 heures',
             '3 jours ouvrés', 'Anghel', '10× plus', "jusqu'à 50 %", '+15-25 %', 'nZEB']

# URL-urile FR indexate înainte de refacere (sitemap-ul din 21.09.2026): fiecare există sau are 301
VECHI = """/ /a-propos/ /a-propos/brevet/ /a-propos/certifications/ /a-propos/fondateur/ /a-propos/presse/ /a-propos/usines/
/contact/ /devenir-partenaire/ /devis/ /economies/ /montage/ /pour/architectes/ /pour/constructeurs/ /pour/investisseurs/
/pour/proprietaires/ /prix/ /produits/ /produits/polistibrick/ /produits/polistisip/ /produits/polistiwall/ /produits/toit-tbk-sip250/
/projets/ /ressources/ /ressources/beton-cellulaire-ou-brique/ /ressources/bloc-coffrant-decennale-avis-technique/
/ressources/coffrage-isolant/ /ressources/coffrage-isolant-incendie/ /ressources/combien-coute-une-maison/
/ressources/electricite-plomberie-coffrage-isolant/ /ressources/enduit-bardage-coffrage-isolant/ /ressources/faq/
/ressources/maison-passive/ /ressources/maison-polystyrene-avis/ /ressources/polistibrick-vs-icf-classique/
/ressources/prix-bloc-coffrant-isolant/ /ressources/re2020/ /legal/conditions/ /legal/confidentialite/ /legal/cookies/
/legal/durabilite/ /legal/mentions-legales/
/polistibrick-conquiert-madrid-le-futur-de-la-construction-est-arrive/ /polistibrick-innovation-et-durabilite-a-paris-batimat-2025/
/polistibrick-innovation-et-efficacite-au-ideal-home-show-irlande-edition-2025/
/polistibrick-participation-au-construct-ambient-expo-2024-le-debut-dune-vision-constructive/
/polistibrick-presente-a-imperiul-leilor-la-technologie-roumaine-primee-qui-redefinit-la-construction-durable/
/polistibrick-validation-et-innovation-au-construct-ambient-expo-edition-2025/""".split()


def text(h: str) -> str:
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ',
                        re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I))))


def main():
    if not B.exists():
        sys.exit('rulează întâi python3 build/build.py fr')
    erori = []
    redir = {}
    for line in (ROOT / 'countries' / 'fr' / '_redirects').read_text(encoding='utf-8').splitlines():
        p = line.split()
        if len(p) >= 3 and not line.startswith('#'):
            redir[p[0]] = p[1]
    for f in sorted(B.rglob('*.html')):
        h = f.read_text(encoding='utf-8'); t = text(h)
        for w in INTERZISE:
            # fără majuscule/minuscule («Devis gratuit» = «devis gratuit»), dar pe cuvânt întreg («ICF» nu prinde «spécificf»)
            n = len(re.findall(r'(?<!\w)' + re.escape(w) + r'(?!\w)', t, flags=re.I))
            if n:
                erori.append(f'{f.relative_to(B).as_posix():62} «{w}» ×{n}')
        if '{{' in h:
            erori.append(f'{f.relative_to(B).as_posix():62} placeholder {{{{ rămas')
    for u in VECHI:
        f = B / 'index.html' if u == '/' else B / u.strip('/') / 'index.html'
        if not f.exists() and u not in redir:
            erori.append(f'URL vechi fără pagină și fără 301: {u}')
    for src, dst in redir.items():
        if dst.startswith('/') and dst != '/' and not (B / dst.strip('/') / 'index.html').exists():
            erori.append(f'301 spre o pagină care nu există: {src} → {dst}')
    if erori:
        print(f'✗ verif-fr: {len(erori)} probleme')
        for e in erori:
            print('   ', e)
        sys.exit(1)
    print(f'✓ verif-fr: zero cuvinte interzise, {len(VECHI)} URL-uri vechi acoperite, zero placeholder-e')


if __name__ == '__main__':
    main()
