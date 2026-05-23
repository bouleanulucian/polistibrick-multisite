#!/usr/bin/env python3
"""One-time patch: replace hardcoded RO strings in shared/js/site.js with {{ui.*}} placeholders."""
from pathlib import Path

p = Path("/Users/polistibrick/Desktop/polistibrick-multisite/shared/js/site.js")
text = p.read_text(encoding="utf-8")

# Order matters: longer/more specific first
REPL = [
    # Nav
    ('aria-label="Polistibrick — acasă"', 'aria-label="{{ui.home_aria}}"'),
    ('aria-label="Navigare principală"', 'aria-label="{{ui.nav_aria}}"'),
    # Nav buttons (text inside <button class="nav-link">)
    ('>\n            Produse\n            <svg', '>\n            {{ui.produse}}\n            <svg'),
    ('>\n            Soluții\n            <svg', '>\n            {{ui.solutii}}\n            <svg'),
    ('>\n            Proiecte\n            <svg', '>\n            {{ui.proiecte}}\n            <svg'),
    ('>\n            Calculator\n            <svg', '>\n            {{ui.calculator}}\n            <svg'),
    ('>\n            Resurse\n            <svg', '>\n            {{ui.resurse}}\n            <svg'),
    ('>\n            Despre\n            <svg', '>\n            {{ui.despre}}\n            <svg'),
    # Nav dropdown items (full anchor lines)
    ('href="${BASE}produse/pereti-mbk/">Pereți MBK<span class="nav-dropdown-item-sub">Cofraj-pierdut pentru pereți portanți</span>',
     'href="${BASE}produse/pereti-mbk/">{{ui.pereti_mbk}}<span class="nav-dropdown-item-sub">{{ui.pereti_mbk_sub}}</span>'),
    ('href="${BASE}produse/planseu-pbk/">Planșee PBK<span class="nav-dropdown-item-sub">Panouri prefabricate cu defazaj 10,8 h</span>',
     'href="${BASE}produse/planseu-pbk/">{{ui.planseu_pbk}}<span class="nav-dropdown-item-sub">{{ui.planseu_pbk_sub}}</span>'),
    ('href="${BASE}produse/acoperis-tbk/">Acoperiș TBK<span class="nav-dropdown-item-sub">Sistem Passivhaus din fabrică</span>',
     'href="${BASE}produse/acoperis-tbk/">{{ui.acoperis_tbk}}<span class="nav-dropdown-item-sub">{{ui.acoperis_tbk_sub}}</span>'),
    ('href="${BASE}produse/accesorii/">Accesorii<span class="nav-dropdown-item-sub">Colțare, capete, scări, ferestre</span>',
     'href="${BASE}produse/accesorii/">{{ui.accesorii}}<span class="nav-dropdown-item-sub">{{ui.accesorii_sub}}</span>'),
    ('href="${BASE}pentru/proprietari/">Pentru proprietari<span class="nav-dropdown-item-sub">Casă pasivă fără facturi mari</span>',
     'href="${BASE}pentru/proprietari/">{{ui.pentru_proprietari}}<span class="nav-dropdown-item-sub">{{ui.pentru_proprietari_sub}}</span>'),
    ('href="${BASE}pentru/arhitecti/">Pentru arhitecți<span class="nav-dropdown-item-sub">Detalii constructive, BIM, fișe</span>',
     'href="${BASE}pentru/arhitecti/">{{ui.pentru_arhitecti}}<span class="nav-dropdown-item-sub">{{ui.pentru_arhitecti_sub}}</span>'),
    ('href="${BASE}pentru/constructori/">Pentru constructori<span class="nav-dropdown-item-sub">Montaj, certificare, parteneriat</span>',
     'href="${BASE}pentru/constructori/">{{ui.pentru_constructori}}<span class="nav-dropdown-item-sub">{{ui.pentru_constructori_sub}}</span>'),
    ('href="${BASE}pentru/investitori/">Pentru investitori<span class="nav-dropdown-item-sub">ROI, viteză execuție, ansambluri</span>',
     'href="${BASE}pentru/investitori/">{{ui.pentru_investitori}}<span class="nav-dropdown-item-sub">{{ui.pentru_investitori_sub}}</span>'),
    ('href="${BASE}devino-partener/" style="color:var(--red);font-weight:600;">→ Devino partener<span class="nav-dropdown-item-sub" style="color:rgba(200,16,46,0.7);">Aplicație constructori certificați</span>',
     'href="${BASE}devino-partener/" style="color:var(--red);font-weight:600;">{{ui.devino_partener}}<span class="nav-dropdown-item-sub" style="color:rgba(200,16,46,0.7);">{{ui.devino_partener_sub}}</span>'),
    ('href="${BASE}proiecte/">Case construite<span class="nav-dropdown-item-sub">Galerie + hartă cu proiecte</span>',
     'href="${BASE}proiecte/">{{ui.case_construite}}<span class="nav-dropdown-item-sub">{{ui.case_construite_sub}}</span>'),
    ('href="${BASE}testimoniale/">Testimoniale (video)<span class="nav-dropdown-item-sub">Proprietarii vorbesc, cu cifre reale</span>',
     'href="${BASE}testimoniale/">{{ui.testimoniale}}<span class="nav-dropdown-item-sub">{{ui.testimoniale_sub}}</span>'),
    ('href="${BASE}calculator/">Calculator cost<span class="nav-dropdown-item-sub">Estimează prețul panourilor casei tale</span>',
     'href="${BASE}calculator/">{{ui.calc_cost}}<span class="nav-dropdown-item-sub">{{ui.calc_cost_sub}}</span>'),
    ('href="${BASE}economii/">Calculator economii<span class="nav-dropdown-item-sub">Polistibrick vs cărămidă pe 25 de ani</span>',
     'href="${BASE}economii/">{{ui.calc_econ}}<span class="nav-dropdown-item-sub">{{ui.calc_econ_sub}}</span>'),
    ('href="${BASE}resurse/blog/">Blog<span class="nav-dropdown-item-sub">Articole despre Casa Pasivă, ICF</span>',
     'href="${BASE}resurse/blog/">{{ui.blog}}<span class="nav-dropdown-item-sub">{{ui.blog_sub}}</span>'),
    ('href="${BASE}resurse/faq/">Întrebări frecvente<span class="nav-dropdown-item-sub">Răspunsuri la cele mai comune întrebări</span>',
     'href="${BASE}resurse/faq/">{{ui.faq}}<span class="nav-dropdown-item-sub">{{ui.faq_sub}}</span>'),
    ('href="${BASE}despre/">Compania<span class="nav-dropdown-item-sub">Cine suntem, viziune, misiune</span>',
     'href="${BASE}despre/">{{ui.compania}}<span class="nav-dropdown-item-sub">{{ui.compania_sub}}</span>'),
    ('href="${BASE}despre/patent/">Patentul Polistibrick<span class="nav-dropdown-item-sub">Brevetul care ne face unici</span>',
     'href="${BASE}despre/patent/">{{ui.patent}}<span class="nav-dropdown-item-sub">{{ui.patent_sub}}</span>'),
    ('href="${BASE}despre/certificari/">Certificări<span class="nav-dropdown-item-sub">CE, ISO, Passivhaus, agremente</span>',
     'href="${BASE}despre/certificari/">{{ui.certificari}}<span class="nav-dropdown-item-sub">{{ui.certificari_sub}}</span>'),
    ('href="${BASE}despre/fabrici/">Fabricile noastre<span class="nav-dropdown-item-sub">Valencia (ES) și Craiova (RO)</span>',
     'href="${BASE}despre/fabrici/">{{ui.fabrici}}<span class="nav-dropdown-item-sub">{{ui.fabrici_sub}}</span>'),
    ('href="${BASE}despre/echipa/">Echipa<span class="nav-dropdown-item-sub">Fondatori și oamenii noștri</span>',
     'href="${BASE}despre/echipa/">{{ui.echipa}}<span class="nav-dropdown-item-sub">{{ui.echipa_sub}}</span>'),
    # Nav CTA
    ('class="btn btn-ghost">Contact</a>', 'class="btn btn-ghost">{{ui.contact}}</a>'),
    ('class="btn btn-primary btn-arrow">Cere ofertă</a>', 'class="btn btn-primary btn-arrow">{{ui.cere_oferta}}</a>'),
    # Footer
    ('<p class="footer-brand-tagline">Sistemul ICF brevetat pentru case pasive premium, fără facturi de energie. Fabricat în UE.</p>',
     '<p class="footer-brand-tagline">{{ui.footer_tagline}}</p>'),
    ('<h5>Produse</h5>', '<h5>{{ui.footer_h_produse}}</h5>'),
    ('<h5>Soluții</h5>', '<h5>{{ui.footer_h_solutii}}</h5>'),
    ('<h5>Resurse</h5>', '<h5>{{ui.footer_h_resurse}}</h5>'),
    ('<h5>Companie</h5>', '<h5>{{ui.footer_h_companie}}</h5>'),
    ('<li><a href="${BASE}produse/pereti-mbk/">Pereți MBK</a></li>', '<li><a href="${BASE}produse/pereti-mbk/">{{ui.pereti_mbk}}</a></li>'),
    ('<li><a href="${BASE}produse/planseu-pbk/">Planșee PBK</a></li>', '<li><a href="${BASE}produse/planseu-pbk/">{{ui.planseu_pbk}}</a></li>'),
    ('<li><a href="${BASE}produse/acoperis-tbk/">Acoperiș TBK</a></li>', '<li><a href="${BASE}produse/acoperis-tbk/">{{ui.acoperis_tbk}}</a></li>'),
    ('<li><a href="${BASE}produse/accesorii/">Accesorii</a></li>', '<li><a href="${BASE}produse/accesorii/">{{ui.accesorii}}</a></li>'),
    ('<li><a href="${BASE}pentru/proprietari/">Proprietari</a></li>', '<li><a href="${BASE}pentru/proprietari/">{{ui.footer_proprietari}}</a></li>'),
    ('<li><a href="${BASE}pentru/arhitecti/">Arhitecți</a></li>', '<li><a href="${BASE}pentru/arhitecti/">{{ui.footer_arhitecti}}</a></li>'),
    ('<li><a href="${BASE}pentru/constructori/">Constructori</a></li>', '<li><a href="${BASE}pentru/constructori/">{{ui.footer_constructori}}</a></li>'),
    ('<li><a href="${BASE}pentru/investitori/">Investitori</a></li>', '<li><a href="${BASE}pentru/investitori/">{{ui.footer_investitori}}</a></li>'),
    ('<li><a href="${BASE}proiecte/">Proiecte realizate</a></li>', '<li><a href="${BASE}proiecte/">{{ui.footer_proiecte_realizate}}</a></li>'),
    ('<li><a href="${BASE}resurse/blog/">Blog</a></li>', '<li><a href="${BASE}resurse/blog/">{{ui.blog}}</a></li>'),
    ('<li><a href="${BASE}resurse/faq/">Întrebări frecvente</a></li>', '<li><a href="${BASE}resurse/faq/">{{ui.faq}}</a></li>'),
    ('<li><a href="${BASE}calculator/">Calculator cost</a></li>', '<li><a href="${BASE}calculator/">{{ui.calc_cost}}</a></li>'),
    ('<li><a href="${BASE}despre/">Despre noi</a></li>', '<li><a href="${BASE}despre/">{{ui.footer_despre_noi}}</a></li>'),
    ('<li><a href="${BASE}despre/patent/">Patent</a></li>', '<li><a href="${BASE}despre/patent/">{{ui.patent}}</a></li>'),
    ('<li><a href="${BASE}despre/certificari/">Certificări</a></li>', '<li><a href="${BASE}despre/certificari/">{{ui.certificari}}</a></li>'),
    ('<li><a href="${BASE}despre/fabrici/">Fabrici</a></li>', '<li><a href="${BASE}despre/fabrici/">{{ui.fabrici}}</a></li>'),
    ('<li><a href="${BASE}contact/">Contact</a></li>', '<li><a href="${BASE}contact/">{{ui.contact}}</a></li>'),
    ('<span>© 2026 Polistibrick. Toate drepturile rezervate. Sistem brevetat.</span>', '<span>{{ui.footer_copyright}}</span>'),
    ('<a href="${BASE}legal/termeni/">Termeni</a>', '<a href="${BASE}legal/termeni/">{{ui.footer_termeni}}</a>'),
    ('<a href="${BASE}legal/confidentialitate/">Confidențialitate</a>', '<a href="${BASE}legal/confidentialitate/">{{ui.footer_confidentialitate}}</a>'),
    ('<a href="${BASE}legal/cookies/">Cookies</a>', '<a href="${BASE}legal/cookies/">{{ui.footer_cookies}}</a>'),
    ('<a href="${BASE}legal/sustenabilitate/">Sustenabilitate</a>', '<a href="${BASE}legal/sustenabilitate/">{{ui.footer_sustenabilitate}}</a>'),
    # Country names in picker (we keep them in local language for UX)
    ("RO: { name: 'România',", "RO: { name: 'România',"),  # noop, keep RO
    ("ES: { name: 'Spania',", "ES: { name: 'España',"),
    ("FR: { name: 'Franța',", "FR: { name: 'France',"),
    ("BE: { name: 'Belgia',", "BE: { name: 'Belgique',"),
    ("IT: { name: 'Italia',", "IT: { name: 'Italia',"),  # already correct
    ("AT: { name: 'Austria',", "AT: { name: 'Österreich',"),
    ("IE: { name: 'Irlanda',", "IE: { name: 'Ireland',"),
    ("ME: { name: 'Muntenegru',", "ME: { name: 'Crna Gora',"),
    # Country picker modal
    ("setAttribute('aria-label', 'Alege țara');", "setAttribute('aria-label', '{{ui.cp_label}}');"),
    ('<button class="country-picker-close" aria-label="Închide">×</button>',
     '<button class="country-picker-close" aria-label="{{ui.cp_close}}">×</button>'),
    ('<span class="country-picker-eyebrow">🌍 Alege țara ta</span>',
     '<span class="country-picker-eyebrow">{{ui.cp_eyebrow}}</span>'),
    ('<h2 class="country-picker-title">În ce țară <em>construiești?</em></h2>',
     '<h2 class="country-picker-title">{{ui.cp_title}} <em>{{ui.cp_title_em}}</em></h2>'),
    ('<p class="country-picker-sub">Te redirecționăm la site-ul țării tale cu echipă locală, contact direct și ofertă în limba ta.</p>',
     '<p class="country-picker-sub">{{ui.cp_sub}}</p>'),
    ("'<span class=\"country-picker-tag\">★ Țara ta</span>'",
     "'<span class=\"country-picker-tag\">{{ui.cp_your_country}}</span>'"),
    ('<p class="country-picker-foot">Țara ta nu e listată? Scrie-ne la <a href="mailto:info@polistibrick.eu">info@polistibrick.eu</a></p>',
     '<p class="country-picker-foot">{{ui.cp_foot}} <a href="mailto:info@polistibrick.eu">info@polistibrick.eu</a></p>'),
]

changes = 0
for old, new in REPL:
    if old == new:
        continue
    if old in text:
        text = text.replace(old, new)
        changes += 1
    else:
        print(f"  ⚠ not found: {old[:80]}")

p.write_text(text, encoding="utf-8")
print(f"Applied {changes} replacements to site.js")
