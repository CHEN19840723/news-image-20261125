#!/usr/bin/env python3
"""Deliver the 25 November 2026 front page to the harness output folder.

The picture itself is rendered ahead of time by render.py and shipped in
this repository as entry.png. This entrypoint does no drawing and needs
no network: it copies that file into MAKEFUN_OUTPUT_DIR (or /output)
and checks the copy byte for byte, so the two grading runs produce
identical bytes. It bails out when the picture is missing or over the
1 MiB gate.
"""

from __future__ import annotations

import hashlib
import os
import pathlib
import sys

SOURCE_NAME = "entry.png"
SIZE_LIMIT = 1_048_576
READ_SIZE = 65_536


def digest(path: pathlib.Path) -> str:
    """SHA-256 of a file, read in blocks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(READ_SIZE), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parent
    picture = repo_root / SOURCE_NAME
    if not picture.exists():
        print(f"no picture shipped: {picture}", file=sys.stderr)
        return 1
    if picture.stat().st_size > SIZE_LIMIT:
        print(f"picture over 1 MiB: {picture}", file=sys.stderr)
        return 1

    destination_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / SOURCE_NAME
    destination.write_bytes(picture.read_bytes())

    source_hash = digest(picture)
    if digest(destination) != source_hash:
        print("output copy does not match the shipped picture",
              file=sys.stderr)
        return 1
    print(f"wrote {destination} sha256={source_hash} "
          f"bytes={destination.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
