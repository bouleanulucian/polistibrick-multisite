#!/usr/bin/env python3
"""
Extract JSON translation dicts from agent output .jsonl files
using the description in meta.json to know which language/chunk each is.
"""
import json
import re
from pathlib import Path

SUBAGENTS_DIR = Path("/Users/polistibrick/.claude/projects/-Users-polistibrick-Desktop-RO-CMR--claude-worktrees-relaxed-chebyshev-90082e/20753858-ff94-4a4e-ac24-12b42ec9a988/subagents")
OUT_DIR = Path("/Users/polistibrick/Desktop/polistibrick-multisite/translations")

# Description → (lang, chunk) mapping
CHUNK_RE = re.compile(r"\b(EN|FR|IT|ES|NL|DE)\s+chunk\s+([AB])", re.IGNORECASE)


def extract_json_from_text(text: str) -> dict | None:
    """Find the largest dict JSON object inside text."""
    # Try fenced block first
    for m in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL):
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict) and len(obj) > 20:
                return obj
        except Exception:
            continue
    # Find largest {...} block
    best = None
    start = 0
    while True:
        i = text.find("{", start)
        if i < 0:
            break
        depth = 0
        in_str = False
        esc = False
        for j in range(i, len(text)):
            c = text[j]
            if esc:
                esc = False
                continue
            if c == "\\":
                esc = True
                continue
            if c == '"':
                in_str = not in_str
                continue
            if in_str:
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(text[i:j+1])
                        if isinstance(parsed, dict) and len(parsed) > 20:
                            if best is None or len(parsed) > len(best):
                                best = parsed
                    except Exception:
                        pass
                    break
        start = i + 1
    return best


def collect_text_from_jsonl(p: Path) -> str:
    chunks = []
    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    for line in content.splitlines():
        try:
            event = json.loads(line)
        except Exception:
            continue
        def walk(o):
            if isinstance(o, str):
                if "{" in o:
                    chunks.append(o)
            elif isinstance(o, list):
                for x in o:
                    walk(x)
            elif isinstance(o, dict):
                for v in o.values():
                    walk(v)
        walk(event)
    return "\n".join(chunks)


def main():
    meta_files = sorted(SUBAGENTS_DIR.glob("agent-*.meta.json"))
    print(f"Scanning {len(meta_files)} meta files...")
    found = 0
    for mf in meta_files:
        try:
            meta = json.loads(mf.read_text())
        except Exception:
            continue
        desc = meta.get("description", "")
        m = CHUNK_RE.search(desc)
        if not m:
            continue
        lang = m.group(1).lower()
        chunk = m.group(2).upper()
        out_path = OUT_DIR / f"{lang}_chunk_{chunk}.json"
        if out_path.exists() and out_path.stat().st_size > 5000:
            print(f"  {lang} chunk {chunk}: already saved ({out_path.stat().st_size}B), skip")
            continue
        jsonl_path = SUBAGENTS_DIR / f"{mf.stem.replace('.meta','')}.jsonl"
        text = collect_text_from_jsonl(jsonl_path)
        obj = extract_json_from_text(text)
        if not obj:
            print(f"  {lang} chunk {chunk}: NO JSON FOUND in {jsonl_path.name}")
            continue
        out_path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {lang} chunk {chunk}: {len(obj)} entries → {out_path.name}")
        found += 1
    print(f"\nWrote {found} chunk files.")

    # List all chunk files
    print("\nAll chunk files now on disk:")
    for f in sorted(OUT_DIR.glob("*_chunk_*.json")):
        d = json.loads(f.read_text())
        print(f"  {f.name}: {len(d)} entries")


if __name__ == "__main__":
    main()
