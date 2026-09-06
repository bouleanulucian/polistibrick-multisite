#!/usr/bin/env python3
"""Extract JSON from agent reply + apply translations to FR homepage."""
import json, re
from pathlib import Path

JSONL = Path("/Users/polistibrick/.claude/projects/-Users-polistibrick-Desktop-RO-CMR--claude-worktrees-relaxed-chebyshev-90082e/20753858-ff94-4a4e-ac24-12b42ec9a988/subagents/agent-af95cfe2ba9391bcd.jsonl")

# Get assistant text
chunks = []
for line in JSONL.read_text(encoding="utf-8", errors="ignore").splitlines():
    try:
        ev = json.loads(line)
    except Exception:
        continue
    if ev.get("type") != "assistant":
        continue
    content = ev.get("message", {}).get("content", [])
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                chunks.append(c.get("text", ""))
text = "\n".join(chunks)

# Find fenced JSON
m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
if not m:
    m = re.search(r"(\{[\s\S]+\})", text)
raw = m.group(1)
data = json.loads(raw)

# Strip extra wrapping quotes from keys (agent included them from the list)
clean = {}
for k, v in data.items():
    ck = k.strip().strip('"').strip("\\\"")
    # also handle case where key starts/ends with literal escaped quote
    if ck.startswith('\\"'): ck = ck[2:]
    if ck.endswith('\\"'): ck = ck[:-2]
    clean[ck] = v

print(f"Got {len(clean)} translations")
print("Sample keys:")
for k in list(clean.keys())[:5]:
    print(f"  - {k[:80]}")

# Apply to homepage
SKIP = re.compile(r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)", re.DOTALL|re.IGNORECASE)
src = Path("countries/fr/polistibrick-mercury-style.html")
content_text = src.read_text(encoding="utf-8")
sorted_keys = sorted(clean.keys(), key=len, reverse=True)
segments = []
last = 0
for m in SKIP.finditer(content_text):
    segments.append(("t", content_text[last:m.start()]))
    segments.append(("s", m.group(0)))
    last = m.end()
segments.append(("t", content_text[last:]))
out = []
for kind, seg in segments:
    if kind == "s":
        out.append(seg); continue
    for ro in sorted_keys:
        tr = clean[ro]
        if tr:
            seg = seg.replace(ro, tr)
    out.append(seg)
src.write_text("".join(out), encoding="utf-8")
print(f"Applied to {src}")
