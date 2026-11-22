"""Entrypoint: paint the front page and write it to /output/entry.png.

Runs with no network and no clock. The output path comes from
MAKEFUN_OUTPUT_DIR when set, else /output, else ./out. The image is
always 1024x1024 and written as a PNG.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import render


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else "out"
    os.makedirs(out_dir, exist_ok=True)
    img = render()
    # PNG, deterministic: render() uses no clock, no randomness, no
    # timestamps, so two runs write identical bytes.
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
