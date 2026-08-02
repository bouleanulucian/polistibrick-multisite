#!/usr/bin/env python3
"""
Studio Testimoniale — Polistibrick
===================================
Unealtă locală pentru încărcat testimoniale (video sau text) pe site.

Pornire:   python3 tools/testimonial-studio/server.py
Se deschide singură în browser pe http://localhost:4800

Ce face:
  1. Primești formularul, alegi VIDEO sau TEXT
  2. La video: îl încarci, îl comprimă pentru web, îi normalizează sunetul,
     scoate un poster și transcrie automat ce se vorbește (whisper local)
  3. Completezi datele (nume, firmă, citat, cifre) și traducerile
  4. ALEGI ȚĂRILE — nimic nu se publică fără asta
  5. Vezi o previzualizare exactă
  6. Confirmi, și abia atunci scrie în paginile alese

Nu publică pe internet. Scrie doar în countries/ pe calculatorul tău.
Publicarea pe live rămâne un pas separat (build + git).
"""

import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
UPLOADS = HERE / "uploads"
UPLOADS.mkdir(exist_ok=True)
PORT = 4800

# ── Cele nouă piețe: folderul, limba subtitrării, numele paginii, folderul de imagini ──
MARKETS = {
    "fr": dict(name="Franța",        lang="fr", page="temoignages",    img="temoignages"),
    "de": dict(name="Elveția",       lang="fr", page="temoignages",    img="temoignages"),
    "nl": dict(name="Belgia",        lang="fr", page="temoignages",    img="temoignages"),
    "en": dict(name="Marea Britanie",lang="en", page="testimonials",   img="testimonials"),
    "ie": dict(name="Irlanda",       lang="en", page="testimonials",   img="testimonials"),
    "es": dict(name="Spania",        lang="es", page="testimonios",    img="testimonios"),
    "it": dict(name="Italia",        lang="it", page="testimonianze",  img="testimonianze"),
    "ro": dict(name="România",       lang="ro", page="testimoniale",   img="testimoniale"),
    "me": dict(name="Muntenegru",    lang="me", page="svjedocanstva",  img="svjedocanstva"),
}

# Etichetele care apar pe card, în limba fiecărei piețe
LABELS = {
    "fr": dict(subs="Sous-titres en français", watch="Voir le témoignage"),
    "en": dict(subs="English subtitles",       watch="Watch the testimonial"),
    "es": dict(subs="Subtítulos en español",   watch="Ver el testimonio"),
    "it": dict(subs="Sottotitoli in italiano", watch="Guarda la testimonianza"),
    "ro": dict(subs="Subtitrare în română",    watch="Vezi testimonialul"),
    "me": dict(subs="Titlovi na crnogorskom",  watch="Pogledajte svjedočanstvo"),
}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", s) or "temoignage"


# ─────────────────────────────── PRELUCRARE VIDEO ───────────────────────────────

def process_video(src: Path, slug: str):
    """Comprimă pentru web, normalizează sunetul, scoate poster. Întoarce căile."""
    out_mp4 = UPLOADS / f"{slug}.mp4"
    out_jpg = UPLOADS / f"{slug}-poster.jpg"

    probe = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)])
    w, h = (probe.stdout.strip().split(",") + ["0", "0"])[:2]
    w, h = int(w or 0), int(h or 0)
    vertical = h > w

    # verticalul rămâne vertical (e filmare de telefon, aşa e cinstit);
    # doar limităm rezoluţia ca fişierul să nu fie uriaş
    scale = "scale=-2:1280" if vertical else "scale=1280:-2"

    run(["ffmpeg", "-y", "-i", str(src),
         "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
         "-vf", scale,
         "-c:a", "aac", "-b:a", "128k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-movflags", "+faststart", str(out_mp4)])

    dur = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(out_mp4)]).stdout.strip()
    dur = float(dur or 0)
    run(["ffmpeg", "-y", "-ss", str(min(3, dur / 3)), "-i", str(out_mp4),
         "-frames:v", "1", "-q:v", "3", str(out_jpg)])

    return dict(mp4=out_mp4, poster=out_jpg, vertical=vertical,
                duration=round(dur, 1), size_mb=round(out_mp4.stat().st_size / 1e6, 1))


def transcribe(video: Path):
    """Transcrie ce se vorbeşte. Întoarce limba, textul şi segmentele cu timpi."""
    wav = UPLOADS / "_audio.wav"
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-acodec", "pcm_s16le",
         "-ar", "16000", "-ac", "1", str(wav)])
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return dict(ok=False, error="faster-whisper nu e instalat (pip install faster-whisper)")
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, info = model.transcribe(str(wav), beam_size=5, vad_filter=True)
    cues = [dict(start=round(s.start, 2), end=round(s.end, 2), text=s.text.strip()) for s in segs]
    wav.unlink(missing_ok=True)
    return dict(ok=True, language=info.language, confidence=round(info.language_probability, 2),
                cues=cues, text=" ".join(c["text"] for c in cues))


def process_photo(src: Path, slug: str, idx: int):
    """Redimensionează poza de şantier pentru web şi scoate o miniatură."""
    out = UPLOADS / f"{slug}-photo{idx}.jpg"
    run(["ffmpeg", "-y", "-i", str(src),
         "-vf", "scale='min(1400,iw)':-2",
         "-q:v", "4", str(out)])
    return out


def write_vtt(cues, path: Path):
    def ts(x):
        h, r = divmod(x, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"
    out = ["WEBVTT", ""]
    for c in cues:
        out += [f"{ts(c['start'])} --> {ts(c['end'])}", c["text"], ""]
    path.write_text("\n".join(out), encoding="utf-8")


# ─────────────────────────────── GENERARE CARD ───────────────────────────────

def build_card(data, market_code, has_video, slug):
    m = MARKETS[market_code]
    lab = LABELS[m["lang"]]
    t = data["perCountry"].get(market_code, {})
    quote = (t.get("quote") or data.get("quote") or "").strip()
    name = data.get("name", "").strip()
    meta = (t.get("meta") or data.get("meta") or "").strip()
    stats = t.get("stats") or data.get("stats") or []

    photos = data.get("photos") or []
    stats_html = ""
    for s in stats[:3]:
        if not (s.get("num") or s.get("label")):
            continue
        stats_html += (f'\n<div class="video-stat"><span class="video-stat-num">{s.get("num","")}</span>'
                       f'<span class="video-stat-label">{s.get("label","")}</span></div>')

    if has_video:
        media = (f'<div class="video-thumb video-thumb--player">\n'
                 f'<video class="testi-video" controls preload="none" playsinline\n'
                 f'       poster="../images/{m["img"]}/{slug}-poster.jpg"\n'
                 f'       aria-label="{lab["watch"]} — {name}">\n'
                 f'  <source src="../images/{m["img"]}/{slug}.mp4" type="video/mp4">\n'
                 f'  <track kind="subtitles" src="../images/{m["img"]}/{slug}.{m["lang"]}.vtt" '
                 f'srclang="{m["lang"]}" label="{lab["subs"]}" default>\n'
                 f'</video>\n</div>')
        klass = "video-card video-card--real"
    elif photos:
        media = (f'<div class="video-thumb video-thumb--shot">\n'
                 f'<img src="../images/{m["img"]}/{photos[0]}" alt="" loading="lazy">\n</div>')
        klass = "video-card video-card--real video-card--photos"
        gallery = ('\n<div class="testi-shots">' + "".join(
            f'\n<img src="../images/{m["img"]}/{p}" alt="" loading="lazy">' for p in photos[1:]
        ) + '\n</div>') if len(photos) > 1 else ""
    else:
        media = ""
        klass = "video-card video-card--real video-card--text"

    return f'''
<article class="{klass}" data-testimonial="{slug}">
{media}
<div class="video-meta">
<p class="video-quote">{quote}</p>{gallery}
<div class="video-author">
<div class="video-author-info">
<strong>{name}</strong>
<span>{meta}</span>
</div>
</div>
<div class="video-stats">{stats_html}
</div>
</div>
</article>
'''


CARD_CSS = """
    .video-thumb--player { padding-top: 0; height: auto; background: #000; }
    .video-thumb--player .testi-video { width: 100%; max-height: 460px; display: block; background: #000; object-fit: contain; }
    .video-card--real { border-color: rgba(200,16,46,0.28); }
    .video-card--text .video-meta { padding-top: 28px; }
    .video-thumb--shot { padding-top: 0; height: auto; }
    .video-thumb--shot img { width: 100%; display: block; max-height: 340px; object-fit: cover; }
    .testi-shots { display: grid; grid-template-columns: repeat(auto-fill, minmax(78px, 1fr)); gap: 6px; margin: 14px 0 4px; }
    .testi-shots img { width: 100%; aspect-ratio: 4/3; object-fit: cover; border-radius: 7px; display: block; }
"""


def publish(data):
    """Scrie în paginile ţărilor alese. Întoarce ce s-a scris."""
    slug = data["slug"]
    has_video = data.get("hasVideo", False)
    written = []

    for code in data["countries"]:
        m = MARKETS[code]
        page = ROOT / "countries" / code / m["page"] / "index.html"
        if not page.exists():
            written.append(dict(country=code, ok=False, error=f"pagina {page} nu există"))
            continue

        # 1) fişierele media
        if has_video:
            imgdir = ROOT / "countries" / code / "images" / m["img"]
            imgdir.mkdir(parents=True, exist_ok=True)
            shutil.copy(UPLOADS / f"{slug}.mp4", imgdir / f"{slug}.mp4")
            shutil.copy(UPLOADS / f"{slug}-poster.jpg", imgdir / f"{slug}-poster.jpg")
            cues = data["perCountry"].get(code, {}).get("cues") or data.get("cues") or []
            if cues:
                write_vtt(cues, imgdir / f"{slug}.{m['lang']}.vtt")

        for ph in (data.get("photos") or []):
            imgdir = ROOT / "countries" / code / "images" / m["img"]
            imgdir.mkdir(parents=True, exist_ok=True)
            src = UPLOADS / ph
            if src.exists():
                shutil.copy(src, imgdir / ph)

        # 2) cardul în grilă
        s = page.read_text(encoding="utf-8")
        if f'data-testimonial="{slug}"' in s:
            s = re.sub(rf'\n<article class="[^"]*" data-testimonial="{slug}">.*?</article>\n', '\n', s, flags=re.S)
        if ".video-thumb--player" not in s:
            s = s.replace("    .video-meta {", CARD_CSS + "    .video-meta {", 1)
        card = build_card(data, code, has_video, slug)
        if '<div class="video-grid">' not in s:
            written.append(dict(country=code, ok=False, error="grila video-grid nu a fost găsită"))
            continue
        s = s.replace('<div class="video-grid">', '<div class="video-grid">' + card, 1)
        page.write_text(s, encoding="utf-8")
        written.append(dict(country=code, ok=True, page=str(page.relative_to(ROOT))))

    return written


# ─────────────────────────────── SERVER ───────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, (HERE / "ui.html").read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/markets":
            return self._send(200, dict(markets=MARKETS))
        if self.path.startswith("/uploads/"):
            f = UPLOADS / Path(self.path).name
            if f.exists():
                ct = mimetypes.guess_type(str(f))[0] or "application/octet-stream"
                return self._send(200, f.read_bytes(), ct)
        return self._send(404, dict(error="not found"))

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n)

        if self.path == "/api/upload":
            ctype = self.headers.get("Content-Type", "")
            boundary = ctype.split("boundary=")[-1].encode()
            parts = raw.split(b"--" + boundary)
            name, blob = "video.mp4", None
            for p in parts:
                if b"filename=" in p:
                    m = re.search(rb'filename="([^"]*)"', p)
                    if m and m.group(1):
                        name = m.group(1).decode()
                    blob = p.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0]
                    break
            if not blob:
                return self._send(400, dict(error="niciun fişier primit"))
            slug = slugify(Path(name).stem)
            src = UPLOADS / f"_src_{slug}{Path(name).suffix}"
            src.write_bytes(blob)
            info = process_video(src, slug)
            tr = transcribe(info["mp4"])
            src.unlink(missing_ok=True)
            return self._send(200, dict(ok=True, slug=slug, duration=info["duration"],
                                        sizeMb=info["size_mb"], vertical=info["vertical"],
                                        previewUrl=f"/uploads/{slug}.mp4",
                                        posterUrl=f"/uploads/{slug}-poster.jpg",
                                        transcript=tr))

        if self.path == "/api/photos":
            ctype = self.headers.get("Content-Type", "")
            boundary = ctype.split("boundary=")[-1].encode()
            slug = "shot"
            saved = []
            for i, p in enumerate(raw.split(b"--" + boundary)):
                if b"filename=" not in p:
                    if b'name="slug"' in p:
                        slug = p.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0].decode() or "shot"
                    continue
                m = re.search(rb'filename="([^"]*)"', p)
                if not (m and m.group(1)):
                    continue
                blob = p.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0]
                tmp = UPLOADS / f"_ph_{i}{Path(m.group(1).decode()).suffix}"
                tmp.write_bytes(blob)
                out = process_photo(tmp, slug, len(saved) + 1)
                tmp.unlink(missing_ok=True)
                if out.exists():
                    saved.append(out.name)
            return self._send(200, dict(ok=True, photos=saved,
                                        urls=[f"/uploads/{n}" for n in saved]))

        if self.path == "/api/preview":
            d = json.loads(raw)
            code = d["countries"][0] if d.get("countries") else "fr"
            return self._send(200, dict(html=build_card(d, code, d.get("hasVideo", False), d["slug"])))

        if self.path == "/api/publish":
            d = json.loads(raw)
            if not d.get("countries"):
                return self._send(400, dict(error="Nu ai ales nicio ţară."))
            return self._send(200, dict(ok=True, written=publish(d)))

        return self._send(404, dict(error="not found"))


def main():
    if not shutil.which("ffmpeg"):
        print("✗ ffmpeg lipseşte. Instalează-l: brew install ffmpeg")
        sys.exit(1)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"\n  Studio Testimoniale Polistibrick")
    print(f"  → {url}\n")
    print(f"  Scrie în: {ROOT / 'countries'}")
    print(f"  Nu publică pe internet — publicarea rămâne pas separat.\n")
    print(f"  Oprire: Ctrl+C\n")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  oprit\n")


if __name__ == "__main__":
    main()
