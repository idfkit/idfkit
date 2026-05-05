#!/usr/bin/env python
"""Pyinstrument profile of common field-access patterns.

Profiles the three most-called read/write paths on a realistic 1700-object
model:

* read     — ``zone.x_origin`` (every model-walking workflow)
* read-str — ``zone.name``   (separate path: name is special-cased)
* write    — ``zone.x_origin = 5.0``
* iterate  — ``for z in coll: _ = z.x_origin``

Each pattern is exercised in a tight loop; loop overhead is reported as
``[self]`` in the profile so it's easy to subtract out.

Usage:
    uv run --group benchmark python benchmarks/profile_field_access.py
    uv run --group benchmark python benchmarks/profile_field_access.py read --iterations 2_000_000 -o read.html
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
from typing import Any

from pyinstrument import Profiler

sys.path.insert(0, str(Path(__file__).parent))
import bench

_HERE = Path(__file__).parent


def _build_model() -> Any:
    from idfkit import load_idf

    idf_str = bench.generate_test_idf()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".idf", delete=False) as fh:
        fh.write(idf_str)
        idf_path = Path(fh.name)
    return load_idf(str(idf_path))


def _profile(label: str, iterations: int, fn) -> Profiler:
    print(f"\nProfiling {iterations:,} x {label}...")
    profiler = Profiler(interval=0.0001)
    profiler.start()
    fn(iterations)
    profiler.stop()
    return profiler


def main() -> None:  # noqa: C901
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "pattern",
        nargs="?",
        choices=("read", "read-name", "write", "iterate", "all"),
        default="all",
        help="Which access pattern to profile (default: all)",
    )
    parser.add_argument("-n", "--iterations", type=int, default=1_000_000)
    parser.add_argument("-o", "--out", type=Path, default=None, help="Write HTML profile output here")
    args = parser.parse_args()

    print("Building 1700-object model...")
    model = _build_model()
    zone = model["Zone"]["Zone_250"]
    coll = model["Zone"]

    # Warm up every path we might profile.
    for _ in range(1000):
        _ = zone.x_origin
        _ = zone.name
        zone.x_origin = 5.0
    for _ in range(10):
        for z in coll:
            _ = z.x_origin

    def run_read(n: int) -> None:
        for _ in range(n):
            _ = zone.x_origin

    def run_read_name(n: int) -> None:
        for _ in range(n):
            _ = zone.name

    def run_write(n: int) -> None:
        for i in range(n):
            zone.x_origin = i

    def run_iterate(n: int) -> None:
        # Each pass over the collection is ``len(coll)`` field reads; we
        # divide *n* by that so the total work matches the others.
        passes = max(1, n // len(coll))
        for _ in range(passes):
            for z in coll:
                _ = z.x_origin

    patterns = {
        "read": ("zone.x_origin", run_read),
        "read-name": ("zone.name", run_read_name),
        "write": ("zone.x_origin = i", run_write),
        "iterate": ("for z in coll: z.x_origin", run_iterate),
    }
    selected = list(patterns) if args.pattern == "all" else [args.pattern]

    profilers: dict[str, Profiler] = {}
    for name in selected:
        label, fn = patterns[name]
        profilers[name] = _profile(label, args.iterations, fn)

    if args.out is not None:
        # When writing HTML, concatenate per-pattern profiles into one file.
        html_parts: list[str] = []
        for name, prof in profilers.items():
            html_parts.append(f"<h2>{name}: {patterns[name][0]}</h2>")
            html_parts.append(prof.output_html())
        args.out.write_text("\n".join(html_parts))
        print(f"\nHTML profile written to {args.out}")
    else:
        for name, prof in profilers.items():
            print(f"\n--- {name}: {patterns[name][0]} ---")
            print(prof.output_text(unicode=True, color=False, show_all=False))


if __name__ == "__main__":
    main()
