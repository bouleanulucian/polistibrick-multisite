#!/usr/bin/env python3
"""
Polistibrick MCP — faza 1
Unelte: audit site, listare pagini, build, info devis app.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES = ROOT / "countries"
BUILD = ROOT / "build"
DEVIS_APP = ROOT.parent / "polistibrick-devis-app"

mcp = FastMCP("polistibrick")


def _run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
    )
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


@mcp.tool()
def list_countries() -> str:
    """Listează țările disponibile (foldere cu _config.json)."""
    codes = sorted(
        d.name
        for d in COUNTRIES.iterdir()
        if d.is_dir() and (d / "_config.json").exists()
    )
    return json.dumps({"countries": codes}, ensure_ascii=False, indent=2)


@mcp.tool()
def list_pages(country: str = "ro") -> str:
    """Listează paginile HTML sursă pentru o țară."""
    base = COUNTRIES / country.lower()
    if not base.exists():
        return json.dumps({"error": f"Țara '{country}' nu există."})
    pages = sorted(
        str(p.relative_to(base))
        for p in base.rglob("*.html")
        if "images" not in p.parts
    )
    return json.dumps({"country": country.lower(), "pages": pages, "count": len(pages)}, ensure_ascii=False, indent=2)


@mcp.tool()
def audit_site(country: str = "ro") -> str:
    """Rulează audit complet (texte străine, linkuri, SEO) pentru RO."""
    code = country.lower()
    if code != "ro":
        return json.dumps({"error": "Audit complet disponibil doar pentru RO (audit_ro_complete.py)."})
    script = ROOT / "translations" / "audit_ro_complete.py"
    if not script.exists():
        return json.dumps({"error": "Script audit lipsă."})
    rc, out = _run([sys.executable, str(script), code])
    return json.dumps({"exit_code": rc, "output": out}, ensure_ascii=False, indent=2)


@mcp.tool()
def build_country(country: str = "ro") -> str:
    """Build site pentru o țară → build/[country]/"""
    code = country.lower()
    rc, out = _run([sys.executable, str(ROOT / "build" / "build.py"), code])
    return json.dumps({"exit_code": rc, "output": out[-4000:] if len(out) > 4000 else out}, ensure_ascii=False, indent=2)


@mcp.tool()
def get_country_config(country: str = "ro") -> str:
    """Citește _config.json pentru o țară (domain, devis_app, contact)."""
    cfg_path = COUNTRIES / country.lower() / "_config.json"
    if not cfg_path.exists():
        return json.dumps({"error": f"Config lipsă: {cfg_path}"})
    with cfg_path.open(encoding="utf-8") as f:
        cfg = json.load(f)
    safe = {
        k: cfg.get(k)
        for k in ("lang", "country", "domain", "domain_url", "devis_app", "contact", "forms")
    }
    return json.dumps(safe, ensure_ascii=False, indent=2)


@mcp.tool()
def devis_app_status() -> str:
    """Verifică dacă app devis există, build trece, env example."""
    info: dict = {"path": str(DEVIS_APP), "exists": DEVIS_APP.is_dir()}
    if not info["exists"]:
        return json.dumps(info, ensure_ascii=False, indent=2)
    info["has_env_example"] = (DEVIS_APP / ".env.example").exists()
    info["package"] = json.loads((DEVIS_APP / "package.json").read_text())["name"]
    rc, out = _run(["npm", "run", "build"], cwd=DEVIS_APP)
    info["build_exit_code"] = rc
    info["build_ok"] = rc == 0
    if rc != 0:
        info["build_tail"] = out[-2000:]
    return json.dumps(info, ensure_ascii=False, indent=2)


@mcp.tool()
def list_blog_drafts() -> str:
    """Listează draft-urile JSON de articole blog (drafts/blog/)."""
    drafts_dir = ROOT / "drafts" / "blog"
    if not drafts_dir.exists():
        return json.dumps({"drafts": []})
    items = []
    for p in sorted(drafts_dir.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            items.append({"file": p.name, "slug": d.get("slug"), "title": d.get("title")})
        except json.JSONDecodeError:
            items.append({"file": p.name, "error": "invalid json"})
    return json.dumps({"drafts": items}, ensure_ascii=False, indent=2)


@mcp.tool()
def create_blog_draft(
    slug: str,
    title: str,
    meta_desc: str,
    category: str,
    headline: str,
    lead: str,
    content_html: str,
    hero_image: str = "../../../images/blog/blog-hero.png",
    date: str = "",
) -> str:
    """Creează draft JSON articol blog RO în drafts/blog/ (fără publish)."""
    from datetime import date as dt

    draft_dir = ROOT / "drafts" / "blog"
    draft_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "slug": slug,
        "title": title,
        "meta_desc": meta_desc,
        "category": category,
        "date": date or dt.today().isoformat(),
        "read_min": max(3, len(content_html.split()) // 200),
        "headline": headline,
        "lead": lead,
        "hero_image": hero_image,
        "hero_alt": title,
        "content_html": content_html,
    }
    path = draft_dir / f"{slug}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return json.dumps({"ok": True, "path": str(path.relative_to(ROOT))}, ensure_ascii=False, indent=2)


@mcp.tool()
def publish_blog_post(slug: str) -> str:
    """Publică articol din drafts/blog/[slug].json → countries/ro/resurse/blog/[slug]/"""
    draft = ROOT / "drafts" / "blog" / f"{slug}.json"
    if not draft.exists():
        return json.dumps({"error": f"Draft lipsă: {draft.name}"})
    rc, out = _run([sys.executable, str(ROOT / "tools" / "new_blog_post.py"), str(draft), "--publish"])
    return json.dumps({"exit_code": rc, "output": out}, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
