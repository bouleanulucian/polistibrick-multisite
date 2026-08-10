#!/usr/bin/env python3
"""
Publică build-ul pe gh-pages cu media o singură dată.

Reguli:
  • Media (poze, video, 3D) stă o singură dată, în /images/ la rădăcina site-ului.
  • Pe fiecare ţară rămân doar HTML, assets/ şi downloads/.
  • Se rescrie DOAR prefixul căii către media. Restul căii — inclusiv numele de
    foldere traduse (montaj, montage, montaggio…) — rămâne neatins. Traducerea
    numelor s-a făcut deja la build; aplicată a doua oară strică fişierele
    (montaj→montaggio, presence→presenšta, mercury→mersary).
  • Sursa şi build.py nu se modifică, ca deploy-ul pe Cloudflare şi Apache să
    meargă mai departe cu structura per ţară.

Rulare:  python3 scripts/publica-preview.py [--fara-verificare]
"""
import re, shutil, subprocess, sys
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent
BUILD    = RADACINA / "build"
WORKTREE = RADACINA / ".gh-pages-worktree"
TARI     = ["ro", "fr", "de", "en", "es", "it", "me", "nl", "ie"]
PREFIX   = "/polistibrick-multisite/"        # site-ul stă sub numele repo-ului pe GitHub Pages
MEDIA    = PREFIX + "images/"

# ── verificări înainte ──────────────────────────────────────────────────────
lipsa = [c for c in TARI if not (BUILD / c / "index.html").exists()]
if lipsa:
    sys.exit("! lipsesc build-uri: %s — rulează întâi build/build.py" % ", ".join(lipsa))
if not (WORKTREE / ".git").exists():
    sys.exit("! %s nu e worktree git" % WORKTREE)

# ── 1. golesc ce publicăm, păstrez ce e la rădăcină (index.html, preview.html) ──
for d in [WORKTREE / c for c in TARI] + [WORKTREE / "images"]:
    if d.exists(): shutil.rmtree(d)

# ── 2. media, o singură dată ────────────────────────────────────────────────
# Toate ţările au acelaşi shared/images în build; iau unirea lor, ca să prind şi
# imaginile pe care şi le adaugă o ţară anume.
comun = WORKTREE / "images"
for c in TARI:
    src = BUILD / c / "images"
    if src.exists():
        subprocess.run(["rsync", "-a", "%s/" % src, "%s/" % comun], check=True)

# ── 3. fiecare ţară: tot, mai puţin media ───────────────────────────────────
for c in TARI:
    subprocess.run(["rsync", "-a", "--exclude", "images/",
                    "%s/" % (BUILD / c), "%s/" % (WORKTREE / c)], check=True)

# ── 4. rescriu doar prefixul către media ────────────────────────────────────
# `../../images/x`, `../images/x`, `images/x` → `/polistibrick-multisite/images/x`
# Ancorat pe ghilimea sau paranteză din faţă, ca să nu prind `assets/images` sau
# text obişnuit. Prinde şi JSON-ul din interiorul unui atribut cu ghilimele simple.
RE_CALE = re.compile(r'(?<=[\'"(])(?:\.\./)*images/')
# site.js construieşte calea cu o variabilă de bază; o înlocuiesc cu prefixul fix
RE_VAR  = re.compile(r'\$\{(?:BASE|IMG)\}(?:\.\./)*images/')

def rescrie(f: Path) -> bool:
    try: t = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError): return False
    nou = RE_VAR.sub(MEDIA, RE_CALE.sub(MEDIA, t))
    if nou == t: return False
    f.write_text(nou, encoding="utf-8")
    return True

atinse = 0
for c in TARI:
    for ext in ("*.html", "*.js", "*.css", "*.xml", "*.json"):
        for f in (WORKTREE / c).rglob(ext):
            atinse += rescrie(f)
print("  prefix rescris în %d fişiere" % atinse)

# ── 5. control ──────────────────────────────────────────────────────────────
def mb(p: Path) -> float:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) / 1048576

probleme = []
for c in TARI:
    if (WORKTREE / c / "images").exists():
        probleme.append("a rămas %s/images" % c)
    ramase = 0
    for f in (WORKTREE / c).rglob("*.html"):
        t = f.read_text(encoding="utf-8", errors="replace")
        ramase += len(RE_CALE.findall(t)) + len(RE_VAR.findall(t))
    if ramase:
        probleme.append("%s: %d căi de media încă relative" % (c, ramase))

print("  media comună : %6.0f MB, %d fişiere" % (mb(comun), sum(1 for _ in comun.rglob("*") if _.is_file())))
total = sum(mb(WORKTREE / c) for c in TARI) + mb(comun)
print("  ţări         : %6.0f MB" % sum(mb(WORKTREE / c) for c in TARI))
print("  TOTAL        : %6.0f MB" % total)

if probleme:
    print("\n! probleme:"); [print("   -", p) for p in probleme]; sys.exit(1)
if total > 700:
    sys.exit("! %d MB — media s-a duplicat, nu public" % total)
print("  ✓ media o singură dată, toate căile absolute")
