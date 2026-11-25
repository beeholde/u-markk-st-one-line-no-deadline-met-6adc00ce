#!/usr/bin/env python3
"""One Line, No Deadline Met — v2 entry.

Writes one single-line joke giving an excuse for a missed deadline to
/output/entry.txt. Python 3 standard library only; no network, no input
files. The line is a constant: the program's whole job is to deliver it
exactly, and to refuse loudly if it ever stops matching the house gate.
"""

import os
import sys
from pathlib import Path

# The entry: an eight-dollar lottery win treated like a retirement
# plan. The contrast between the tiny prize and the grand evening is
# the turn; the deadline retiring first is the punch.
LINE = (
    "I won eight dollars on a lottery ticket and spent the evening "
    "planning my retirement, so the deadline retired first."
)


def check_line(line: str) -> None:
    """Enforce the house gate: 1-200 chars, one line, not blank, UTF-8."""
    encoded = line.encode("utf-8")  # raises if the line is not valid UTF-8
    if not 1 <= len(line) <= 200:
        raise SystemExit(
            f"line is {len(line)} chars / {len(encoded)} bytes, "
            "gate needs 1-200 chars"
        )
    if "\n" in line or "\r" in line:
        raise SystemExit("line must be a single line")
    if not line.strip():
        raise SystemExit("line must not be only whitespace")
    if line != line.strip():
        raise SystemExit("line must not start or end with whitespace")


def main() -> None:
    check_line(LINE)
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(LINE.encode("utf-8"))
    os.chmod(target, 0o644)
    # Round-trip self-check: the file on disk must be the line, byte for
    # byte — a partial write or an encoding slip fails loudly instead of
    # shipping a truncated entry to the gate.
    if target.read_bytes() != LINE.encode("utf-8"):
        raise SystemExit("written entry does not match the line")


if __name__ == "__main__":
    main()
    sys.exit(0)
