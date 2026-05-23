#!/usr/bin/env python3
"""
Extract translated HTML from an agent's .jsonl transcript file.
Usage: python3 extract_agent_html.py <agent_id> <output_path>
Looks for a ```html ... ``` fenced code block in the assistant's final replies.
"""
import json
import re
import sys
from pathlib import Path

SUBAGENTS_DIR = Path("/Users/polistibrick/.claude/projects/-Users-polistibrick-Desktop-RO-CMR--claude-worktrees-relaxed-chebyshev-90082e/20753858-ff94-4a4e-ac24-12b42ec9a988/subagents")


def collect_assistant_text(jsonl_path: Path) -> str:
    chunks = []
    for line in jsonl_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            event = json.loads(line)
        except Exception:
            continue
        # Look only at assistant messages
        # Event format: { "type": "assistant", "message": {"content": [{"type":"text","text":...}]} }
        msg = event.get("message", {})
        if event.get("type") != "assistant":
            continue
        content = msg.get("content", [])
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    chunks.append(c.get("text", ""))
        elif isinstance(content, str):
            chunks.append(content)
    return "\n".join(chunks)


def extract_html_block(text: str) -> str | None:
    # Look for ```html ... ``` fenced block first
    m = re.search(r"```html\s*\n(.*?)\n```", text, re.DOTALL)
    if m:
        return m.group(1)
    # Fallback: any ``` ... ``` containing <!DOCTYPE or <html
    m = re.search(r"```\w*\s*\n(<!DOCTYPE.*?</html>)\s*\n?```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    # Fallback: bare HTML if no fences
    m = re.search(r"(<!DOCTYPE.*?</html>)", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 extract_agent_html.py <agent_id> <output_path>")
        sys.exit(1)
    agent_id = sys.argv[1]
    output_path = Path(sys.argv[2])
    jsonl_path = SUBAGENTS_DIR / f"agent-{agent_id}.jsonl"
    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found")
        sys.exit(1)
    text = collect_assistant_text(jsonl_path)
    html = extract_html_block(text)
    if not html:
        print(f"ERROR: no HTML block found in agent {agent_id}")
        sys.exit(2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"OK: wrote {len(html)} bytes to {output_path}")


if __name__ == "__main__":
    main()
