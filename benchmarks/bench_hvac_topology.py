"""Benchmark the HVAC topology view on the reference model (research R-21, task T051).

Prints the table each slice's pull request reports: model load, the topology build with all checks,
the cached view, a few queries, and peak memory. Needs no EnergyPlus installation.

Usage::

    uv run python benchmarks/bench_hvac_topology.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmarks._timing import best_of, peak_memory, reference_model_path
from idfkit import load_idf
from idfkit.hvac import HVACTopology


def main() -> None:
    """Time each operation as the best of five runs and print a Markdown table."""
    path = str(reference_model_path())
    load = best_of(lambda: load_idf(path), 5)
    docs = iter([load_idf(path) for _ in range(5)])
    build = best_of(lambda: HVACTopology.from_document(next(docs)).check(), 5)
    doc = load_idf(path)
    topo = HVACTopology.from_document(doc)
    topo.check()
    cached = best_of(lambda: HVACTopology.from_document(doc), 5)
    node = max(topo.nodes(), key=lambda n: len(topo.uses(n)))
    walk = best_of(lambda: topo.downstream(node, hops=3), 5)
    uses = best_of(lambda: topo.uses(node), 5)
    fresh = load_idf(path)
    _, peak = peak_memory(lambda: HVACTopology.from_document(fresh).check())
    rows = [
        ("load_idf", f"{load * 1000:.0f} ms"),
        ("from_document + check()", f"{build * 1000:.1f} ms ({build / load:.0%} of load)"),
        ("from_document, cached", f"{cached * 1e6:.1f} us"),
        ("downstream, 3 hops", f"{walk * 1e6:.0f} us"),
        ("uses(node)", f"{uses * 1e6:.0f} us"),
        ("peak memory, build + checks", f"{peak / 1e6:.1f} MB"),
        ("nodes / findings", f"{len(topo.nodes())} / {len(topo.check())}"),
    ]
    print("| Operation (HospitalLowEnergy) | Measured |")
    print("|---|---|")
    for name, value in rows:
        print(f"| {name} | {value} |")


if __name__ == "__main__":
    main()
