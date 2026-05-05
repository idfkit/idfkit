#!/usr/bin/env python
"""Aggregate per-run benchmark JSON outputs into a single results.json.

Each matrix job in the benchmark workflow uploads its own ``results.json``.
This script walks an input directory, takes the *median of the per-run
minimums* (and means) for every tool/operation pair, writes the consolidated
file at ``benchmarks/results.json``, then reuses ``bench.py``'s chart and
README-patch helpers so the docs reflect the aggregated numbers.

Usage:
    uv run --group benchmark python benchmarks/aggregate.py <input_dir>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import median
from typing import Any

import bench

_HERE = Path(__file__).parent


def _load_runs(input_dir: Path) -> list[dict[str, Any]]:
    """Walk *input_dir* recursively for any results.json files."""
    files = sorted(input_dir.rglob("results.json"))
    if not files:
        msg = f"No results.json files found under {input_dir}"
        raise SystemExit(msg)
    runs: list[dict[str, Any]] = []
    for f in files:
        with f.open() as fh:
            runs.append(json.load(fh))
    print(f"Loaded {len(runs)} run(s) from {input_dir}")
    return runs


def _aggregate(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Median per (tool, op, metric) across all runs.

    Metadata is taken from the first run plus a ``runs_aggregated`` count.
    """
    base_meta: dict[str, Any] = dict(runs[0]["metadata"])
    base_meta["runs_aggregated"] = len(runs)

    out: dict[str, Any] = {"metadata": base_meta}

    # Tool names are dict keys other than 'metadata'; preserve order from the first run.
    tool_names = [k for k in runs[0] if k != "metadata"]

    for tool in tool_names:
        per_op: dict[str, dict[str, float]] = {}
        op_names = list(runs[0][tool])  # operations present in the first run
        for op in op_names:
            mins: list[float] = [float(r[tool][op]["min"]) for r in runs if tool in r and op in r[tool]]
            means: list[float] = [float(r[tool][op]["mean"]) for r in runs if tool in r and op in r[tool]]
            per_op[op] = {"min": median(mins), "mean": median(means)}
        out[tool] = per_op
    return out


def _fmt(seconds: float) -> str:
    if seconds < 1e-6:
        return f"{seconds * 1e9:.0f}ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.1f}µs"
    if seconds < 1:
        return f"{seconds * 1e3:.1f}ms"
    return f"{seconds:.2f}s"


def _print_summary(consolidated: dict[str, Any]) -> None:
    op = bench.HERO_OPERATION
    idfkit_t = float(consolidated[bench.TOOL_IDFKIT][op]["min"])
    print(f"\nMedian-of-runs summary on '{op}':")
    print(f"  idfkit  {_fmt(idfkit_t)}")
    for tool, results in consolidated.items():
        if tool in ("metadata", bench.TOOL_IDFKIT) or op not in results:
            continue
        t = float(results[op]["min"])
        ratio = t / idfkit_t if idfkit_t > 0 else float("inf")
        print(f"  {tool!r:35s} {_fmt(t)}  ({ratio:.0f}x)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory containing per-run results.json files")
    parser.add_argument(
        "--out",
        type=Path,
        default=_HERE / "results.json",
        help="Where to write the consolidated results.json",
    )
    parser.add_argument(
        "--render",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Also regenerate SVGs and patch README/docs (default: yes)",
    )
    args = parser.parse_args()

    runs = _load_runs(args.input_dir)
    consolidated = _aggregate(runs)

    args.out.write_text(json.dumps(consolidated, indent=2))
    print(f"Wrote consolidated results to {args.out}")
    _print_summary(consolidated)

    if args.render:
        # Strip metadata for the chart generators (they expect tool->op->{min,mean}).
        all_results: dict[str, dict[str, dict[str, float]]] = {k: v for k, v in consolidated.items() if k != "metadata"}
        assets_dir = _HERE.parent / "docs" / "assets"
        bench.generate_hero_chart(all_results, assets_dir / "benchmark.svg")
        print("Per-operation charts:")
        bench.generate_operation_charts(all_results, assets_dir)
        # update_readme reads from the given path and patches README + docs/benchmarks.md.
        bench.update_readme(results_path=args.out)


if __name__ == "__main__":
    sys.path.insert(0, str(_HERE))
    main()
