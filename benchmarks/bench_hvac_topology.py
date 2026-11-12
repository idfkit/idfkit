"""Benchmark the HVAC topology view on the reference model (research R-21, task T051).

Prints the table each slice's pull request reports: model load, the topology build with all checks,
the cached view, a few queries, loop memberships and chains (first call on a fresh view, which builds
the memoised answer, and cached), and peak memory. Needs no EnergyPlus installation.

Usage::

    uv run python benchmarks/bench_hvac_topology.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from collections.abc import Callable
from typing import Literal

from benchmarks._timing import best_of, peak_memory, reference_model_path
from idfkit import IDFDocument, load_idf
from idfkit.hvac import HVACTopology

SIDES: tuple[Literal["supply", "demand"], ...] = ("supply", "demand")


def first_call(doc: IDFDocument, query: Callable[[HVACTopology], object]) -> float:
    """Best of five first calls of *query*, each on a view built (untimed) for it alone."""
    views = iter([HVACTopology(doc) for _ in range(5)])
    return best_of(lambda: query(next(views)), 5)


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
    coil = max(
        (o for t in doc.collections if t.startswith("Coil:") and ":Water" in t for o in doc.get_collection(t)),
        key=lambda c: len({m.kind for m in topo.memberships(c)}),
    )
    memb_first = first_call(doc, lambda view: view.memberships(coil))
    memb_cached = best_of(lambda: topo.memberships(coil), 5)
    loop, side = max(((lp, sd) for lp in topo.loops() for sd in SIDES), key=lambda s: len(topo.chain(*s)))
    chain_first = first_call(doc, lambda view: view.chain(loop, side))
    chain_cached = best_of(lambda: topo.chain(loop, side), 5)
    fresh = load_idf(path)
    _, peak = peak_memory(lambda: HVACTopology.from_document(fresh).check())
    rows = [
        ("load_idf", f"{load * 1000:.0f} ms"),
        ("from_document + check()", f"{build * 1000:.1f} ms ({build / load:.0%} of load)"),
        ("from_document, cached", f"{cached * 1e6:.1f} us"),
        ("downstream, 3 hops", f"{walk * 1e6:.0f} us"),
        ("uses(node)", f"{uses * 1e6:.0f} us"),
        (f"memberships({coil.name}), first / cached", f"{memb_first * 1000:.2f} ms / {memb_cached * 1e6:.1f} us"),
        (
            f"chain({loop.name}, {side}), {len(topo.chain(loop, side))} branches, first / cached",
            f"{chain_first * 1000:.2f} ms / {chain_cached * 1e6:.1f} us",
        ),
        ("peak memory, build + checks", f"{peak / 1e6:.1f} MB"),
        ("nodes / findings", f"{len(topo.nodes())} / {len(topo.check())}"),
    ]
    print("| Operation (HospitalLowEnergy) | Measured |")
    print("|---|---|")
    for name, value in rows:
        print(f"| {name} | {value} |")


if __name__ == "__main__":
    main()
