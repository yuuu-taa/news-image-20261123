#!/usr/bin/env python3
"""Copy the bundled entry image to /output/entry.png.

The image (entry.png, kept beside this file) is a newspaper-style
collage summing up the world news of Monday 23 November 2026.
This program uses only the Python standard library, never touches
the network, and produces byte-identical output on every run.
"""

import hashlib
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT = Path("/output/entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Read the width and height from a PNG file's IHDR chunk."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png is not a PNG file")
    # After the 8-byte signature comes the IHDR chunk: a 4-byte length,
    # the 4 bytes "IHDR", then width and height as big-endian uint32.
    width, height = struct.unpack(">II", data[16:24])
    return width, height


MAX_BYTES = 1024 * 1024  # the bounty caps the image at 1 MiB
MAX_SIDE = 1024  # ... and at 1024 x 1024 pixels


def main() -> int:
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    width, height = png_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the 1024x1024 cap")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {OUTPUT}: {len(data)} bytes, {width}x{height}, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
