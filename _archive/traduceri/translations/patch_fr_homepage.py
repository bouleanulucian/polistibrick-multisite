#!/usr/bin/env python3
"""Brute-force patch for FR homepage — all RO remnants in static nav + content."""
from pathlib import Path

p = Path("/Users/polistibrick/Desktop/polistibrick-multisite/countries/fr/polistibrick-mercury-style.html")
text = p.read_text(encoding="utf-8")

REPL = [
    # Static main nav (lines 3057-3114)
    ('class="nav-menu-link">Produse <span', 'class="nav-menu-link">Produits <span'),
    ('class="nav-menu-link">Soluții <span', 'class="nav-menu-link">Solutions <span'),
    ('class="nav-menu-link">Proiecte <span', 'class="nav-menu-link">Projets <span'),
    ('class="nav-menu-link">Calculator <span', 'class="nav-menu-link">Calculateur <span'),
    ('class="nav-menu-link">Resurse <span', 'class="nav-menu-link">Ressources <span'),
    ('class="nav-menu-link">Despre <span', 'class="nav-menu-link">À propos <span'),
    # Dropdown items
    ('<a href="produse/accesorii/">Accesorii</a>', '<a href="produse/accesorii/">Accessoires</a>'),
    ('<a href="pentru/proprietari/">Pour proprietari</a>', '<a href="pentru/proprietari/">Pour les propriétaires</a>'),
    ('<a href="pentru/constructori/">Pour constructori</a>', '<a href="pentru/constructori/">Pour les constructeurs</a>'),
    ('<a href="pentru/investitori/">Pour investitori</a>', '<a href="pentru/investitori/">Pour les investisseurs</a>'),
    ('">→ Devino partener</a>', '">→ Devenez partenaire</a>'),
    ('<a href="proiecte/">Case construite</a>', '<a href="proiecte/">Maisons construites</a>'),
    ('<a href="testimoniale/">Testimoniale (video)</a>', '<a href="testimoniale/">Témoignages (vidéo)</a>'),
    ('<a href="calculator/">Calculator cost</a>', '<a href="calculator/">Calculateur de coût</a>'),
    ('<a href="despre/">Compania</a>', '<a href="despre/">L\'entreprise</a>'),
    ('<a href="despre/patent/">Patent</a>', '<a href="despre/patent/">Brevet</a>'),
    ('<a href="despre/fabrici/">Fabrici</a>', '<a href="despre/fabrici/">Nos usines</a>'),
    ('<a href="despre/echipa/">Echipa</a>', '<a href="despre/echipa/">L\'équipe</a>'),
    ('aria-label="Schimbă țara"', 'aria-label="Changer de pays"'),
    ('aria-label="Navigare site"', 'aria-label="Navigation du site"'),
    # Nav drawer (mobile)
    ('<div class="nav-drawer-title">Produse</div>', '<div class="nav-drawer-title">Produits</div>'),
    ('<div class="nav-drawer-title">Soluții</div>', '<div class="nav-drawer-title">Solutions</div>'),
    ('<div class="nav-drawer-title">Proiecte</div>', '<div class="nav-drawer-title">Projets</div>'),
    ('<div class="nav-drawer-title">Calculator</div>', '<div class="nav-drawer-title">Calculateur</div>'),
    ('<div class="nav-drawer-title">Resurse</div>', '<div class="nav-drawer-title">Ressources</div>'),
    ('<div class="nav-drawer-title">Despre</div>', '<div class="nav-drawer-title">À propos</div>'),
    ('<a href="pentru/proprietari/">Pour proprietari</a>\n    <a href="pentru/arhitecti/">Pour les architectes</a>\n    <a href="pentru/constructori/">Pour constructori</a>\n    <a href="pentru/investitori/">Pour investitori</a>',
     '<a href="pentru/proprietari/">Pour les propriétaires</a>\n    <a href="pentru/arhitecti/">Pour les architectes</a>\n    <a href="pentru/constructori/">Pour les constructeurs</a>\n    <a href="pentru/investitori/">Pour les investisseurs</a>'),
    ('<a href="devino-partener/" class="partner-link">→ Devino partener</a>',
     '<a href="devino-partener/" class="partner-link">→ Devenez partenaire</a>'),
    ('<a href="proiecte/">Case construite</a>\n    <a href="testimoniale/">Testimoniale video</a>',
     '<a href="proiecte/">Maisons construites</a>\n    <a href="testimoniale/">Témoignages vidéo</a>'),
    ('<a href="despre/">Compania</a>\n    <a href="despre/patent/">Patent</a>',
     '<a href="despre/">L\'entreprise</a>\n    <a href="despre/patent/">Brevet</a>'),
    ('<a href="despre/fabrici/">Fabrici</a>\n    <a href="despre/echipa/">Echipa</a>',
     '<a href="despre/fabrici/">Nos usines</a>\n    <a href="despre/echipa/">L\'équipe</a>'),
    # Stats + watermarks
    ('<div class="stat-num">Facturi <span>−90%</span></div>', '<div class="stat-num">Factures <span>−90%</span></div>'),
    ('<strong>−95%</strong><span>Facturi</span>', '<strong>−95%</strong><span>Factures</span>'),
    ('<h4>Facturi reale, <em>pas des promesses.</em></h4>', '<h4>Factures réelles, <em>pas des promesses.</em></h4>'),
    ('<span class="wm-half wm-top">5-în-1</span>\n        <span class="wm-half wm-bottom">5-în-1</span>',
     '<span class="wm-half wm-top">5-en-1</span>\n        <span class="wm-half wm-bottom">5-en-1</span>'),
    ('<h3>Perete finit <em>5 în 1.</em></h3>', '<h3>Mur fini <em>5 en 1.</em></h3>'),
    ('<h2 class="ct-headline"><strong>3 materiale.</strong> <strong>1 équipe.</strong> <strong>1 lună.</strong></h2>',
     '<h2 class="ct-headline"><strong>3 matériaux.</strong> <strong>1 équipe.</strong> <strong>1 mois.</strong></h2>'),
    # Wm-half "Fabrici" → "Usines"
    ('<span class="wm-half wm-top">Fabrici</span>\n        <span class="wm-half wm-bottom">Fabrici</span>',
     '<span class="wm-half wm-top">Usines</span>\n        <span class="wm-half wm-bottom">Usines</span>'),
    ('<span class="fabrici-stat"><strong>2</strong> <span class="fabrici-stat-emoji">🏭</span> Fabrici</span>',
     '<span class="fabrici-stat"><strong>2</strong> <span class="fabrici-stat-emoji">🏭</span> Usines</span>'),
    # Footer link
    ('<li><a href="proiecte/">Proiecte</a></li>', '<li><a href="proiecte/">Projets</a></li>'),
    # Misc visible
    ('<span class="passive-photo-label">Proiecte reale Polistibrick</span>',
     '<span class="passive-photo-label">Projets réels Polistibrick</span>'),
    # Comments (cosmetic but cleaner)
    ('Two-stat row beneath the CTA: 2 🏭 Fabrici · 9 🌍 Țări de prezență',
     'Two-stat row beneath the CTA: 2 🏭 Usines · 9 🌍 Pays de présence'),
    ('Card wrap — same pattern as Fabrici', 'Card wrap — same pattern as Usines'),
]

changes = 0
missing = []
for old, new in REPL:
    if old in text:
        text = text.replace(old, new)
        changes += 1
    else:
        missing.append(old[:80])

p.write_text(text, encoding="utf-8")
print(f"Applied {changes}/{len(REPL)} replacements")
if missing:
    print(f"\n⚠ {len(missing)} not found:")
    for m in missing[:5]:
        print(f"  - {m}")
