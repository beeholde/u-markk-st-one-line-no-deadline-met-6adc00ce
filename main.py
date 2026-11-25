#!/usr/bin/env python3
"""One Line, No Deadline Met — v1 entry.

Writes one single-line joke giving an excuse for a missed deadline to
/output/entry.txt. Python 3 standard library only; no network, no input
files. The line is a constant: the program's whole job is to deliver it
exactly, and to refuse loudly if it ever stops matching the house gate.
"""

import os
import sys
from pathlib import Path

# The entry: a goldfish funeral with full honours. The miss is the
# narrator's own choice — reverence, not bad luck — which is the turn.
LINE = (
    "My goldfish died the morning the report was due, so I gave it a "
    "funeral with full honours and missed the deadline out of respect."
)


def check_line(line: str) -> None:
    """Enforce the house gate: 1-200 chars, one line, not blank, UTF-8."""
    size = len(line.encode("utf-8"))
    if not 1 <= len(line) <= 200:
        raise SystemExit(
            f"line is {len(line)} chars / {size} bytes, gate needs 1-200 chars"
        )
    if "\n" in line or "\r" in line:
        raise SystemExit("line must be a single line")
    if not line.strip():
        raise SystemExit("line must not be only whitespace")
    line.encode("utf-8")  # raises if the line is not valid UTF-8


def main() -> None:
    check_line(LINE)
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    os.chmod(target, 0o644)
    # Round-trip self-check: the file on disk must be the line, byte for
    # byte — a partial write or an encoding slip fails loudly instead of
    # shipping a truncated entry to the gate.
    if target.read_bytes() != LINE.encode("utf-8"):
        raise SystemExit("written entry does not match the line")


if __name__ == "__main__":
    main()
    sys.exit(0)
