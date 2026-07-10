#!/usr/bin/env python3
"""Audit complet site IT: texte străine, URL-uri FR, SEO."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IT = ROOT / "countries" / "it"
BUILD = ROOT / "build" / "it"

FR_URL_PARAMS = re.compile(
    r'subject=Demande|doc=Documentation|Dossier\+Technique|Demande\+de\+',
    re.I,
)

FR_VISIBLE = re.compile(
    r'\b(Demander|Demande de|Voir le|pour les|chez vous|notre système|'
    r'votre maison|nous sommes|vous pouvez|Construire une|une maison|'
    r'des factures|témoignages|propriétaires)\b',
    re.I,
)

RO_VISIBLE = re.compile(
    r'\b(despre|pentru|noastre|construiți|Redirecționare)\b',
    re.I,
)

FR_LEFTOVER_META = re.compile(
    r'Sole isolants|Tettoure isolante|Description maison|Demande\+',
    re.I,
)


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

        if 'lang="it"' not in raw[:500]:
            issues.append(f"  ! {rel}: lipsește lang=\"it\"")

        for m in FR_URL_PARAMS.finditer(raw):
            issues.append(f"  ! {rel}: param URL FR: {m.group(0)}")

        for m in FR_LEFTOVER_META.finditer(raw):
            issues.append(f"  ! {rel}: text/meta FR: {m.group(0)}")

        visible = strip_non_visible(raw)
        # Ignore French folder names in href/src paths (intentional URL structure)
        visible_no_urls = re.sub(r'href="[^"]*"', '', visible)
        visible_no_urls = re.sub(r'src="[^"]*"', '', visible_no_urls)
        visible_no_urls = re.sub(r'data-href="[^"]*"', '', visible_no_urls)

        for m in FR_VISIBLE.finditer(visible_no_urls):
            issues.append(f"  ! {rel}: text FR vizibil: {m.group(1)}")

        for m in RO_VISIBLE.finditer(visible_no_urls):
            issues.append(f"  ! {rel}: text RO vizibil: {m.group(0)[:60]}")
            break

    js_dir = base / "assets" / "js"
    if js_dir.exists():
        for js in js_dir.glob("*.js"):
            t = js.read_text(encoding="utf-8")
            if "{{ui." in t or "{{forms." in t or "{{legal." in t:
                issues.append(f"  ! assets/js/{js.name}: placeholder nerezolvat")

    return issues


def main():
    print("=" * 60)
    print("AUDIT COMPLET ITALIANĂ — polistibrick.it")
    print("=" * 60)

    src_issues = audit_dir(IT, "SURSE countries/it")
    build_issues = audit_dir(BUILD, "BUILD build/it") if BUILD.exists() else ["[BUILD] Rulează: python3 build/build.py it"]

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
