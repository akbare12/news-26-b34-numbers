"""news-26-b34-numbers — grader entry point (STDLIB ONLY).

The grader runs this file with nothing installed beyond the standard
library, from an arbitrary working directory, with MAKEFUN_OUTPUT_DIR
pointing at an empty output directory and the repo mounted read-only.

This file therefore does exactly one thing: copy the pre-rendered
``entry.png`` (produced at build time by ``gen.py`` with Pillow) into
``$MAKEFUN_OUTPUT_DIR/entry.png``. No image work happens here, no
third-party imports, no writes next to this file.

Layout: V32 ALSO-first — masthead + DATE CHECK (2 lines), then the ALSO
band (37 stories, 3 columns) FIRST, then 3 heroes side by side, then
10 cards (2x5), a world-map strip, a timeline strip and a footer.
50 stories total: 3 heroes + 10 cards + 37 ALSO items.

Date: Thursday 26 November 2026. All facts verified against the
26 Nov 2026 canon; items from 25 Nov are marked [CL] with the date.
"""
import hashlib
import os
import shutil
import sys


def _here():
    """Directory that holds this file (and entry.png)."""
    return os.path.dirname(os.path.abspath(__file__))


def _find_entry():
    """Locate entry.png: next to this file, else in the cwd."""
    here = _here()
    cand = os.path.join(here, "entry.png")
    if os.path.isfile(cand):
        return cand
    cand = os.path.join(os.getcwd(), "entry.png")
    if os.path.isfile(cand):
        return cand
    raise FileNotFoundError(
        "entry.png not found next to main.py (%s) or in cwd (%s)"
        % (here, os.getcwd()))


def _sha256(path):
    """SHA-256 of a file, read in 1 MiB chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    """Copy entry.png into MAKEFUN_OUTPUT_DIR and verify the copy."""
    src = _find_entry()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if src_size != dst_size:
        raise RuntimeError("size mismatch after copy: %d != %d"
                           % (src_size, dst_size))
    src_hash = _sha256(src)
    dst_hash = _sha256(dst)
    if src_hash != dst_hash:
        raise RuntimeError("sha256 mismatch after copy")
    print("entry.png -> %s (%d bytes, sha256 %s)"
          % (dst, dst_size, dst_hash), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
