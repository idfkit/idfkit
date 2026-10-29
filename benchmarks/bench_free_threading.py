#!/usr/bin/env python
"""Measure what free-threaded CPython buys idfkit: CPU-bound work spread across threads.

Each workload is a fixed batch of independent jobs (one model each, nothing shared between jobs
but the schema), run on a thread pool of 1, 2, 4 ... workers. On a GIL build the pool can only
interleave the jobs, so the wall time stays flat; on a free-threaded build with the GIL off the
jobs run truly in parallel, and the wall time should fall with the worker count.

Run it once per interpreter and compare::

    uv run --python 3.14 python benchmarks/bench_free_threading.py --json ft-off.json
    PYTHON_GIL=0 uv run --python 3.14t python benchmarks/bench_free_threading.py --json ft-on.json
    python benchmarks/bench_free_threading.py --report ft-off.json ft-on.json

``--report`` prints, per workload, the single-thread time on each interpreter (the cost
free-threading charges a program that never starts a thread) and the speedup at each worker
count, both against the GIL build's single-thread time and against the same build's own.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import sysconfig
import tempfile
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

JOBS = 16
REPEATS = 3
ESO_FIXTURE = Path(__file__).parent.parent / "tests" / "fixtures" / "simulation" / "sample.eso"
COMPACT_FIELDS = [
    "Fraction",
    "Through: 6/30",
    "For: Weekdays",
    "Until: 08:00",
    "0.1",
    "Until: 18:00",
    "0.9",
    "Until: 24:00",
    "0.2",
    "For: AllOtherDays",
    "Until: 24:00",
    "0.0",
    "Through: 12/31",
    "For: AllDays",
    "Until: 24:00",
    "0.5",
]


def _workloads(idf_path: str) -> dict[str, Callable[[], object]]:
    # Imported here so --report runs on any interpreter, idfkit installed or not.
    from bench import ENERGYPLUS_VERSION

    from idfkit import load_idf, write_idf
    from idfkit.geometry import calculate_surface_area, calculate_surface_azimuth, calculate_surface_tilt
    from idfkit.schedules.evaluate import values
    from idfkit.simulation.parsers.eso import ESOResult
    from idfkit.validation import validate_document

    model = load_idf(idf_path, version=ENERGYPLUS_VERSION)
    eso_bytes = ESO_FIXTURE.read_bytes()

    def parse() -> object:
        return load_idf(idf_path, version=ENERGYPLUS_VERSION)

    def validate() -> object:
        # A private copy per job: the contract allows shared reads, but a job here stands for
        # independent work on independent models.
        return validate_document(model.copy())

    def write() -> object:
        return write_idf(model.copy())

    def geometry() -> object:
        own = model.copy()
        return [
            (calculate_surface_area(s), calculate_surface_tilt(s), calculate_surface_azimuth(s))
            for s in own["BuildingSurface:Detailed"]
        ]

    def schedule() -> object:
        own = model.copy()
        own.add("Schedule:Compact", "Occ", validate=False, data=[{"field": f} for f in COMPACT_FIELDS])
        return values(own["Schedule:Compact"]["Occ"], timestep=4)

    def eso() -> object:
        return ESOResult.from_bytes(eso_bytes, eager=True)

    return {
        "parse (load_idf)": parse,
        "validate": validate,
        "write_idf": write,
        "geometry": geometry,
        "schedule (8760x4)": schedule,
        "eso (eager)": eso,
    }


def _time_batch(job: Callable[[], object], workers: int) -> float:
    best = float("inf")
    for _ in range(REPEATS):
        with ThreadPoolExecutor(max_workers=workers) as pool:
            t0 = time.perf_counter()
            list(pool.map(lambda _: job(), range(JOBS)))
            best = min(best, time.perf_counter() - t0)
    return best


def run(json_path: Path | None) -> None:
    gil_enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    free_threaded = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
    label = f"{sys.version.split()[0]}{'t' if free_threaded else ''} (GIL {'on' if gil_enabled else 'off'})"
    cpus = os.cpu_count() or 1
    worker_counts = [w for w in (1, 2, 4, 8, 16) if w <= max(cpus, 1)]
    print(f"{label}, {cpus} CPUs, {JOBS} jobs per batch, best of {REPEATS}")

    with tempfile.TemporaryDirectory() as tmp:
        idf_path = os.path.join(tmp, "model.idf")
        from bench import generate_test_idf

        Path(idf_path).write_text(generate_test_idf(200, 50, 400))
        results: dict[str, dict[str, float]] = {}
        for name, job in _workloads(idf_path).items():
            job()  # warm the schema and the lazily built caches
            results[name] = {str(w): _time_batch(job, w) for w in worker_counts}
            row = "  ".join(
                f"{w}w {t:6.3f}s ({results[name]['1'] / t:4.2f}x)"
                for w, t in zip(worker_counts, results[name].values())
            )
            print(f"  {name:<20} {row}")

    if json_path is not None:
        json_path.write_text(json.dumps({"label": label, "cpus": cpus, "jobs": JOBS, "results": results}, indent=2))


def report(gil_path: Path, ft_path: Path) -> None:
    gil = json.loads(gil_path.read_text())
    ft = json.loads(ft_path.read_text())
    workers = list(next(iter(ft["results"].values())))
    print(f"baseline: {gil['label']}    free-threaded: {ft['label']}    {ft['cpus']} CPUs, {ft['jobs']} jobs")
    head = " | ".join(f"{w}w" for w in workers)
    print(f"| workload | 1-thread cost of FT | FT speedup vs GIL 1w: {head} |")
    print("|---|---|" + "---|" * len(workers))
    for name, g in gil["results"].items():
        f = ft["results"][name]
        cost = f["1"] / g["1"] - 1
        speedups = " | ".join(f"{g['1'] / f[w]:.2f}x" for w in workers)
        print(f"| {name} | {cost:+.0%} | {speedups} |")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", type=Path, help="write this interpreter's timings here")
    parser.add_argument("--report", nargs=2, type=Path, metavar=("GIL_JSON", "FT_JSON"), help="compare two runs")
    args = parser.parse_args()
    if args.report:
        report(*args.report)
    else:
        run(args.json)


if __name__ == "__main__":
    main()
