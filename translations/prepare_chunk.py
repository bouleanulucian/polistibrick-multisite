#!/usr/bin/env python3
"""Prepare top-N phrases as a simple list for translation agents."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
phrases_file = ROOT / "translations" / "phrases_to_translate.json"
data = json.loads(phrases_file.read_text(encoding="utf-8"))

# Sort by count descending, take top N
sorted_items = sorted(data.items(), key=lambda x: -x[1]["count"])

# Output as plain numbered list for agent
TOP_N = 400
print(f"# Top {TOP_N} Romanian phrases to translate (numbered)")
print(f"# Total unique: {len(data)}")
print(f"# Coverage: top {TOP_N} = {sum(c['count'] for _, c in sorted_items[:TOP_N])} of {sum(c['count'] for _, c in sorted_items)} occurrences")
print("")
for i, (phrase, meta) in enumerate(sorted_items[:TOP_N], 1):
    # Escape any " in phrase for clean output
    p = phrase.replace('"', '\\"')
    print(f'{i}. "{p}"')
