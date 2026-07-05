#!/usr/bin/env python3
"""
Polistibrick Multi-site Build Script
-------------------------------------
Reads countries/[code]/_config.json and country HTML files,
copies shared assets, replaces {{placeholders}}, outputs to build/[code]/.

Usage:
    python3 build/build.py              # build all countries
    python3 build/build.py ro           # build only RO
    python3 build/build.py ro en fr     # build specific countries
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = ROOT / "countries"
SHARED_DIR = ROOT / "shared"
BUILD_DIR = ROOT / "build"
FALLBACK_COUNTRY = "ro"   # used when a country has only _config.json

PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")


UI_STRINGS_PATH = ROOT / "translations" / "ui_strings.json"


def load_config(country_code: str) -> dict:
    cfg_path = COUNTRIES_DIR / country_code / "_config.json"
    if not cfg_path.exists():
        raise SystemExit(f"[ERROR] Missing config: {cfg_path}")
    with cfg_path.open(encoding="utf-8") as f:
        cfg = json.load(f)
    # Inject UI strings for the country's language (used by site.js placeholders)
    if UI_STRINGS_PATH.exists() and "ui" not in cfg:
        with UI_STRINGS_PATH.open(encoding="utf-8") as f:
            ui_all = json.load(f)
        lang = cfg.get("lang", "ro")
        if country_code == "ie":  # ie falls back to RO template; UI should be EN
            lang = "en"
        cfg["ui"] = ui_all.get(lang, ui_all.get("ro", {}))
    return cfg


def resolve_placeholder(key: str, config: dict) -> str:
    """Walk dotted path like 'contact.email_general' through config."""
    value = config
    for part in key.split("."):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return "{{" + key + "}}"  # leave un-resolved
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def apply_placeholders(text: str, config: dict) -> str:
    return PLACEHOLDER_RE.sub(lambda m: resolve_placeholder(m.group(1), config), text)


# Per-language URL path rewriting (RO → target lang folder names)
PATH_REWRITES = {
    "fr": {
        "produse": "produits", "pentru": "pour", "despre": "a-propos",
        "resurse": "ressources", "proiecte": "projets", "economii": "economies",
        "oferta": "devis", "comparatie": "comparaison", "calculator": "calculateur",
        "testimoniale": "temoignages", "devino-partener": "devenir-partenaire",
        "pereti-mbk": "murs-mbk", "planseu-pbk": "planchers-pbk",
        "acoperis-tbk": "toit-tbk", "accesorii": "accessoires",
        "proprietari": "proprietaires", "arhitecti": "architectes",
        "constructori": "constructeurs", "investitori": "investisseurs",
        "certificari": "certifications", "fabrici": "usines",
        "echipa": "fondateur", "patent": "brevet",
        "casa-cluj-napoca": "maison-cluj-napoca", "ansamblu-lyon": "ensemble-lyon",
        "confidentialitate": "confidentialite", "sustenabilitate": "durabilite",
        "termeni": "conditions",
        "mentiuni-legale": "mentions-legales",
    },
}


def rewrite_paths(text: str, lang: str) -> str:
    """Rewrite RO folder names to target language paths in href/src attributes."""
    rewrites = PATH_REWRITES.get(lang)
    if not rewrites:
        return text
    for old, new in sorted(rewrites.items(), key=lambda x: -len(x[0])):
        if old == new:
            continue
        # Match in href="..." / src="..." / template literals ${BASE}old/
        text = re.sub(r'(["\'/$\}])' + re.escape(old) + r'(/)', r'\1' + new + r'\2', text)
    return text


# Dev/staging files under */presence/ — not referenced on the live site
PRESENCE_KEEP_FILES = {
    "presence-factory.jpg",
    "presence-factory-film.mp4",
}


# Unused / dev assets — never linked from live HTML
SHARED_SKIP_NAMES = {
    "house-comparison.png",
    "house-comparison-pbk.png",
    "wall.mp4",
    "wall_original.mp4",
    "wall_uncrop.mp4",
    "mbk-wall-old.png",
    "stage3.png",
    "passive-seasons.mp4",
    "passive-seasons-mobile.mp4",
    "hero-houses-reel.mp4",
    "hero-houses-reel-desktop.webm",
    "hero-houses-reel-mobile.webm",
}


def should_skip_asset(rel: Path) -> bool:
    if rel.name in SHARED_SKIP_NAMES:
        return True
    if "presence" in rel.parts:
        return rel.name not in PRESENCE_KEEP_FILES
    return False


def optimize_html(text: str) -> str:
    """Non-blocking fonts, lighter weights, deferred shared JS."""
    if "fonts.googleapis.com" in text and "preconnect" not in text:
        text = text.replace(
            "</head>",
            '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n</head>',
            1,
        )
    text = text.replace(
        "Inter:wght@400;500;600;700;800",
        "Inter:wght@400;500;600;700",
    )
    text = text.replace(
        "Inter:wght@300;400;500;600;700;800",
        "Inter:wght@400;500;600;700",
    )
    text = re.sub(
        r'<link\s+href="(https://fonts\.googleapis\.com/css[^"]+)"\s+rel="stylesheet">',
        lambda m: (
            f'<link rel="preload" as="style" href="{m.group(1)}" '
            f'onload="this.onload=null;this.rel=\'stylesheet\'">\n'
            f'  <noscript><link rel="stylesheet" href="{m.group(1)}"></noscript>'
        ),
        text,
    )
    text = re.sub(
        r'(<script\s+src=")([^"]*site\.js)(?:\?[^"]*)?(")(\s*defer)?>',
        r'\1\2?v=2\3 defer>',
        text,
    )
    text = re.sub(
        r'(<script\s+src=")([^"]*mercury-perf\.js)(?:\?[^"]*)?(")(\s*defer)?>',
        r'\1\2?v=10\3 defer>',
        text,
    )
    text = re.sub(
        r'(<link rel="stylesheet" href="assets/css/mercury-home\.css)\?v=[^"]*(">)',
        r'\1?v=3\2',
        text,
    )
    text = re.sub(
        r'(<script\s+src="[^"]*forms\.js")(?!\s+defer)>',
        r"\1 defer>",
        text,
    )
    text = re.sub(
        r'(<script\s+src="[^"]*cookies\.js")(?!\s+defer)>',
        r"\1 defer>",
        text,
    )
    return text


def optimize_html_files(out_dir: Path):
    for html in out_dir.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        optimized = optimize_html(text)
        if optimized != text:
            html.write_text(optimized, encoding="utf-8")


def path_rewrite_lang(country_code: str, lang: str) -> str | None:
    """Countries seeded from the FR template use French URL slugs."""
    if country_code == "ro" or lang == "ro":
        return None
    return "fr"


def copy_tree(src: Path, dst: Path, transform: bool, config: dict, country_code: str = ""):
    """Copy src→dst. If transform=True, replace placeholders in .html/.css/.js."""
    if not src.exists():
        return
    lang = config.get("lang", "ro")
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        if should_skip_asset(rel):
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if transform and item.suffix.lower() in {".html", ".css", ".js", ".xml", ".txt", ".json"}:
            try:
                content = item.read_text(encoding="utf-8")
                content = apply_placeholders(content, config)
                # Rewrite RO folder names in shared site.js → French paths (FR template countries)
                if item.suffix.lower() in {".js", ".html"}:
                    rewrite = path_rewrite_lang(country_code, lang)
                    if rewrite:
                        content = rewrite_paths(content, rewrite)
                if item.suffix.lower() == ".html":
                    content = optimize_html(content)
                target.write_text(content, encoding="utf-8")
                continue
            except UnicodeDecodeError:
                pass  # fall through to binary copy
        shutil.copy2(item, target)


def page_canonical(rel_path: str, base: str) -> str:
    """Map a built HTML file's relative path to its public canonical URL.
    The homepage (both the index.html redirect and the actual homepage file)
    canonicalizes to the site root, not to /polistibrick-mercury-style.html."""
    if rel_path in ("index.html", "polistibrick-mercury-style.html"):
        rel_path = ""
    elif rel_path.endswith("/index.html"):
        rel_path = rel_path[:-len("index.html")]
    return f"{base}/{rel_path}"


def inject_seo(out_dir: Path, config: dict):
    """Insert canonical + og:url + hreflang into every page that lacks them.
    Canonical always points to the official domain (domain_url), never the
    staging host (e.g. GitHub Pages)."""
    base = config.get("domain_url", "").rstrip("/")
    if not base:
        return
    hreflang = config.get("metadata", {}).get("hreflang") or config.get("lang", "")
    for html in out_dir.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        if 'rel="canonical"' in text or "</head>" not in text:
            continue
        rel = html.relative_to(out_dir).as_posix()
        url = page_canonical(rel, base)
        tags = (
            f'<link rel="canonical" href="{url}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<link rel="alternate" hreflang="{hreflang}" href="{url}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{url}">\n'
        )
        text = text.replace("</head>", tags + "</head>", 1)
        html.write_text(text, encoding="utf-8")


def generate_sitemap(out_dir: Path, config: dict):
    base = config.get("domain_url", "").rstrip("/")
    skip_files = {"polistibrick-mercury-style.html"}  # homepage canonical = /
    urls = []
    for html in out_dir.rglob("*.html"):
        rel = html.relative_to(out_dir).as_posix()
        if rel in skip_files:
            continue
        if rel.endswith("/index.html"):
            rel = rel[:-10]
        elif rel == "index.html":
            rel = ""
        urls.append(f"{base}/{rel}")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(set(urls)):
        lines.append(f"  <url><loc>{u}</loc></url>")
    lines.append("</urlset>")
    (out_dir / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def generate_robots(out_dir: Path, config: dict):
    base = config.get("domain_url", "").rstrip("/")
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )
    (out_dir / "robots.txt").write_text(content, encoding="utf-8")


def generate_cache_headers(out_dir: Path):
    """Cache-Control for Cloudflare CDN / Pages + Apache origins behind Cloudflare."""
    headers = """# Auto-generated — Cloudflare Pages / Netlify cache rules
# More specific paths first; first match wins.

/assets/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/images/*
  Cache-Control: public, max-age=2592000, stale-while-revalidate=604800

/downloads/*
  Cache-Control: public, max-age=2592000

/sitemap.xml
  Cache-Control: public, max-age=86400

/robots.txt
  Cache-Control: public, max-age=86400

/*
  Cache-Control: public, max-age=3600, must-revalidate
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
"""
    (out_dir / "_headers").write_text(headers, encoding="utf-8")

    htaccess = """# Auto-generated — Apache cache headers (Cloudflare CDN respects these)
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>

<IfModule mod_headers.c>
  <FilesMatch "\\.(css|js)$">
    Header set Cache-Control "public, max-age=604800, stale-while-revalidate=86400"
  </FilesMatch>
  <FilesMatch "\\.(jpg|jpeg|png|gif|webp|svg|ico|mp4|webm|woff2?)$">
    Header set Cache-Control "public, max-age=2592000, stale-while-revalidate=604800"
  </FilesMatch>
  <FilesMatch "\\.(html)$">
    Header set Cache-Control "public, max-age=3600, must-revalidate"
  </FilesMatch>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 7 days"
  ExpiresByType application/javascript "access plus 7 days"
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/webp "access plus 30 days"
  ExpiresByType video/mp4 "access plus 30 days"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>
"""
    (out_dir / ".htaccess").write_text(htaccess, encoding="utf-8")


def build_country(code: str):
    config = load_config(code)
    out_dir = BUILD_DIR / code
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) shared assets → build/[code]/assets/ + images/
    copy_tree(SHARED_DIR / "css", out_dir / "assets" / "css", transform=True, config=config, country_code=code)
    copy_tree(SHARED_DIR / "js",  out_dir / "assets" / "js",  transform=True, config=config, country_code=code)
    copy_tree(SHARED_DIR / "images", out_dir / "images", transform=False, config=config)

    # 1b) shared downloads (PDF, CAD, BIM, etc) per language → build/[code]/downloads/
    lang_code = config.get("lang", "ro")
    downloads_src = SHARED_DIR / "downloads" / lang_code
    if downloads_src.exists():
        copy_tree(downloads_src, out_dir / "downloads", transform=False, config=config)
    # Also copy shared multilingual downloads (logos, brochures)
    shared_downloads = SHARED_DIR / "downloads" / "shared"
    if shared_downloads.exists():
        copy_tree(shared_downloads, out_dir / "downloads", transform=False, config=config)

    # 2) Country HTML — empty countries (only _config.json) are SKIPPED (not built)
    country_src = COUNTRIES_DIR / code
    html_files = [p for p in country_src.iterdir() if p.is_file() and p.suffix == ".html"]
    subfolders = [p for p in country_src.iterdir() if p.is_dir() and p.name not in ('_config.json',)]
    if not html_files and not subfolders:
        print(f"  [skip] {code} is empty (only _config.json) — not deployed")
        shutil.rmtree(out_dir)
        return
    copy_tree(country_src, out_dir, transform=True, config=config, country_code=code)

    # Strip _config.json from output (not needed publicly)
    cfg_out = out_dir / "_config.json"
    if cfg_out.exists():
        cfg_out.unlink()

    # 3) SEO tags (canonical, og:url, hreflang) — always on the official domain
    inject_seo(out_dir, config)

    # 3b) Performance — async fonts, defer site.js (pages that skipped transform)
    optimize_html_files(out_dir)

    # 4) sitemap + robots + CDN cache headers
    generate_sitemap(out_dir, config)
    generate_robots(out_dir, config)
    generate_cache_headers(out_dir)

    pages = sum(1 for _ in out_dir.rglob("*.html"))
    print(f"✓ {code:3} ({config.get('country_name','?')}) → {out_dir.relative_to(ROOT)} ({pages} pages)")


def main():
    codes = sys.argv[1:] or sorted(p.name for p in COUNTRIES_DIR.iterdir() if p.is_dir())
    print(f"\n→ Building {len(codes)} countries: {', '.join(codes)}\n")
    BUILD_DIR.mkdir(exist_ok=True)
    for code in codes:
        try:
            build_country(code)
        except SystemExit as e:
            print(e)
    print(f"\n✓ Done. Output: {BUILD_DIR.relative_to(ROOT)}/\n")


if __name__ == "__main__":
    main()
