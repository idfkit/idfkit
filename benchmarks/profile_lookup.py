#!/usr/bin/env python
"""Pyinstrument profile of the hot lookup path: ``model[Type][name]``.

The hero benchmark op clocks at ~1 µs per call, well below pyinstrument's
default sampling resolution. We loop the lookup ~1M times so the sampler
sees enough slices to attribute time to call sites. Useful for diffing
HEAD against an earlier commit when the headline ratio shifts.

Usage:
    uv run --group benchmark python benchmarks/profile_lookup.py
    uv run --group benchmark python benchmarks/profile_lookup.py -n 2_000_000 -o profile.html

Then ``git switch <ref>`` and rerun to compare against another commit.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pyinstrument import Profiler

# Reuse the same IDF generator the benchmark uses so we profile a realistic model.
sys.path.insert(0, str(Path(__file__).parent))
import bench

_HERE = Path(__file__).parent


def _build_model() -> object:
    """Generate the same 1700-object IDF the benchmark uses, parse it with idfkit."""
    import tempfile

    from idfkit import load_idf

    idf_str = bench.generate_test_idf()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".idf", delete=False) as fh:
        fh.write(idf_str)
        idf_path = Path(fh.name)
    return load_idf(str(idf_path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-n",
        "--iterations",
        type=int,
        default=1_000_000,
        help="Number of lookups to perform under the profiler (default: 1,000,000)",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="Write HTML profile output to this path (default: print text to stdout)",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="Zone_250",
        help="Object name to look up each iteration (default: Zone_250)",
    )
    parser.add_argument(
        "--type",
        dest="obj_type",
        type=str,
        default="Zone",
        help="Object type to look up each iteration (default: Zone)",
    )
    args = parser.parse_args()

    print("Building 1700-object model and warming up...")
    model = _build_model()
    # Warm-up: ensure the collection cache and any lazy attribute resolution is primed.
    for _ in range(1000):
        _ = model[args.obj_type][args.target]  # type: ignore[index]

    print(f"Profiling {args.iterations:,} lookups of model[{args.obj_type!r}][{args.target!r}]...")
    profiler = Profiler(interval=0.0001)  # 100 µs sampling — finer than default 1 ms
    profiler.start()
    for _ in range(args.iterations):
        _ = model[args.obj_type][args.target]  # type: ignore[index]
    profiler.stop()

    if args.out is not None:
        args.out.write_text(profiler.output_html())
        print(f"HTML profile written to {args.out}")
    else:
        print(profiler.output_text(unicode=True, color=True, show_all=False))


if __name__ == "__main__":
    main()
