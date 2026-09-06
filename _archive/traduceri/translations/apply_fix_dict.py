#!/usr/bin/env python3
"""Apply fr_fix_dict.json to ALL countries/fr/*.html (HTML-aware: skip script/style/comments).
Usage: python3 apply_fix_dict.py fr"""
import json, re, sys
from pathlib import Path

ROOT = Path("/Users/polistibrick/Desktop/polistibrick-multisite")
SKIP = re.compile(r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)", re.DOTALL|re.IGNORECASE)

lang = sys.argv[1] if len(sys.argv) > 1 else "fr"
dict_path = ROOT / "translations" / f"{lang}_fix_dict.json"
country = ROOT / "countries" / lang

d = json.loads(dict_path.read_text(encoding="utf-8"))
# Strip _doc and similar
d = {k: v for k, v in d.items() if not k.startswith("_")}
keys = sorted(d.keys(), key=len, reverse=True)

total_subs = 0
files_changed = 0
for f in sorted(country.rglob("*.html")):
    txt = f.read_text(encoding="utf-8")
    segments = []
    last = 0
    for m in SKIP.finditer(txt):
        segments.append(("t", txt[last:m.start()]))
        segments.append(("s", m.group(0)))
        last = m.end()
    segments.append(("t", txt[last:]))
    out = []
    file_subs = 0
    for kind, seg in segments:
        if kind == "s":
            out.append(seg); continue
        for k in keys:
            v = d[k]
            count = seg.count(k)
            if count:
                seg = seg.replace(k, v)
                file_subs += count
        out.append(seg)
    new_txt = "".join(out)
    if new_txt != txt:
        f.write_text(new_txt, encoding="utf-8")
        files_changed += 1
        total_subs += file_subs

print(f"  {lang}: {total_subs} substitutions in {files_changed} files")
