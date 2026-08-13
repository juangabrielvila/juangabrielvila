"""Build a single anxiety-journal PDF for design iteration.

Usage:  python3 build_one.py [slug]   (default slug: before_the_test)

Kept separate from build_all.py so we can lock the design on one book before
regenerating the whole line.
"""

from __future__ import annotations

import sys
from pathlib import Path

from build_all import ALL_BOOKS
from template import build_book

DEFAULT_SLUG = "before_the_test"

OUT_DIR = Path(__file__).parent / "out"


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SLUG
    cfg = next((b for b in ALL_BOOKS if b.slug == slug), None)
    if cfg is None:
        available = ", ".join(b.slug for b in ALL_BOOKS)
        raise SystemExit(f"Unknown slug: {slug}. Available: {available}")
    path = build_book(cfg, OUT_DIR)
    print(f"  wrote {path.name}")


if __name__ == "__main__":
    main()
