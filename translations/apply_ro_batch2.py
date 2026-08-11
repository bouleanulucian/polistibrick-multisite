#!/usr/bin/env python3
"""Apply batch2 FR→RO translations to countries/ro/ HTML and merge into extra_fr_to_ro.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANS = ROOT / "translations"
RO_DIR = ROOT / "countries" / "ro"

SKIP = re.compile(
    r"(<script\b[^>]*>.*?</script>)|(<style\b[^>]*>.*?</style>)|(<!--.*?-->)",
    re.DOTALL | re.IGNORECASE,
)


def apply_dict(text: str, mapping: dict[str, str], passes: int = 3) -> str:
    keys = sorted(mapping.keys(), key=len, reverse=True)
    segments = []
    last_end = 0
    for m in SKIP.finditer(text):
        segments.append(("t", text[last_end : m.start()]))
        segments.append(("s", m.group(0)))
        last_end = m.end()
    segments.append(("t", text[last_end:]))
    out = []
    for kind, seg in segments:
        if kind == "s":
            out.append(seg)
            continue
        for _ in range(passes):
            for fr in keys:
                tr = mapping[fr]
                if fr in seg:
                    seg = seg.replace(fr, tr)
        out.append(seg)
    return "".join(out)


def main() -> None:
    extra_path = TRANS / "extra_fr_to_ro.json"
    batch_path = TRANS / "batch2_fr_to_ro.json"

    merged: dict[str, str] = {}
    if extra_path.exists():
        merged.update(json.loads(extra_path.read_text(encoding="utf-8")))
    if batch_path.exists():
        merged.update(json.loads(batch_path.read_text(encoding="utf-8")))

    changed = 0
    for f in sorted(RO_DIR.rglob("*.html")):
        original = f.read_text(encoding="utf-8")
        new = apply_dict(original, merged)
        if new != original:
            f.write_text(new, encoding="utf-8")
            changed += 1

    extra_path.write_text(
        json.dumps(dict(sorted(merged.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"apply_ro_batch2: {len(merged)} keys, {changed} files updated")


if __name__ == "__main__":
    main()
