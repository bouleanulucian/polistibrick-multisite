#!/usr/bin/env python3
"""Audit complet site RO: texte străine, URL-uri FR/EN, SEO."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RO = ROOT / "countries" / "ro"
BUILD = ROOT / "build" / "ro"

FR_PATH_SEGMENTS = re.compile(
    r"/(produits|devis|a-propos|ressources|projets|economies|pour|confidentialite|"
    r"mentions-legales|conditions|durabilite|devenir-partenaire|temoignages|montage|"
    r"calculateur|architectes|constructeurs|proprietaires|investisseurs|murs-mbk|"
    r"planchers-pbk|toit-tbk|accessoires)/",
    re.I,
)

FR_QUERY = re.compile(
    r"[?&](subject|role|doc|type)=([^\"'&\s]+)",
    re.I,
)

FR_ENGLISH_UI = re.compile(
    r">\s*(Legal|Cookies|Blog|FAQ|Menu|Email \*|Call de|Voir le|Demander|Envoyer|"
    r"United Kingdom|Ireland|Schweiz|België|España|France)\s*<",
    re.I,
)

FR_URL_PARAMS = re.compile(
    r'href=["\'][^"\']*[?&](subject|role|doc|type)=|'
    r'role=(promoteur|architecte|constructeur|particulier|autre)|'
    r'subject=(Demande|Documentation)|Demande\+|Fiche\+technique',
    re.I,
)

ALLOWED_FOREIGN = {
    "Passivhaus", "PHPP", "ICF", "MBK", "PBK", "TBK", "ROI", "BET", "BIM", "CAD",
    "DWG", "IFC", "ISO", "CE", "ETA", "CSTB", "RE2020", "GDPR", "AC ", "UK",
    "Contact", "Calculator", "TikTok", "Facebook", "Instagram", "LinkedIn",
}


def strip_non_visible(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<script\b.*?</script>", "", text, flags=re.I | re.S)
    text = re.sub(r"<style\b.*?</style>", "", text, flags=re.I | re.S)
    return text


def audit_dir(base: Path, label: str) -> list[str]:
    issues = []
    if not base.exists():
        issues.append(f"[{label}] Lipsește: {base}")
        return issues

    html_files = list(base.rglob("*.html"))
    issues.append(f"[{label}] Pagini HTML: {len(html_files)}")

    for f in sorted(html_files):
        raw = f.read_text(encoding="utf-8")
        rel = f.relative_to(base).as_posix()

        if 'lang="ro"' not in raw[:500]:
            issues.append(f"  ! {rel}: lipsește lang=\"ro\"")

        for m in FR_PATH_SEGMENTS.finditer(raw):
            issues.append(f"  ! {rel}: segment URL FR: {m.group(1)}")

        for m in FR_URL_PARAMS.finditer(raw):
            snippet = raw[max(0, m.start() - 20) : m.end() + 40].replace("\n", " ")
            issues.append(f"  ! {rel}: param URL străin: ...{snippet[:90]}...")

        visible = strip_non_visible(raw)
        for m in FR_ENGLISH_UI.finditer(visible):
            issues.append(f"  ! {rel}: text UI străin: {m.group(1)}")

        if "polistibrick.fr" in raw and "data-domain" not in raw[max(0, raw.find("polistibrick.fr") - 80): raw.find("polistibrick.fr")]:
            if rel != "polistibrick-mercury-style.html":
                pass  # country switcher OK

    js_dir = base / "assets" / "js"
    if js_dir.exists():
        for js in js_dir.glob("*.js"):
            t = js.read_text(encoding="utf-8")
            # Doar stringuri vizibile utilizatorului (nu fallback-uri după resolved)
            if re.search(r"showError\(form, 'Merci", t):
                issues.append(f"  ! assets/js/{js.name}: mesaj eroare FR hardcodat")
            if re.search(r"setAttribute\('aria-label', 'Contact rapide'\)", t):
                issues.append(f"  ! assets/js/{js.name}: bară contact FR")
            if "'politique de confidentialité'" in t and "politica de confidențialitate" not in t:
                issues.append(f"  ! assets/js/{js.name}: cookies banner FR")

    sitemap = base / "sitemap.xml"
    if sitemap.exists():
        sm = sitemap.read_text(encoding="utf-8")
        if "polistibrick-mercury-style.html" in sm:
            issues.append("  ! sitemap.xml: conține URL duplicat mercury-style (SEO)")
        if not sm.startswith("<?xml"):
            issues.append("  ! sitemap.xml: invalid")

    return issues


def main():
    code = sys.argv[1] if len(sys.argv) > 1 else "ro"
    print("=" * 60)
    print("AUDIT COMPLET ROMÂNĂ — polistibrick.ro")
    print("=" * 60)

    src_issues = audit_dir(RO, "SURSE countries/ro")
    build_issues = audit_dir(BUILD, "BUILD build/ro") if BUILD.exists() else ["[BUILD] Rulează: python3 build/build.py ro"]

    all_issues = [i for i in src_issues + build_issues if i.startswith("  !")]

    for line in src_issues + build_issues:
        print(line)

    print("=" * 60)
    if all_issues:
        print(f"REZULTAT: {len(all_issues)} problem(e) găsite")
        return 1
    print("REZULTAT: OK — 0 probleme (text + linkuri + SEO)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
