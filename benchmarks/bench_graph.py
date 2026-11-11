"""Benchmark the model knowledge graph on the reference model (research R-21, task T117).

Prints the figures the performance contract budgets: ``ModelGraph(doc)`` construction, a 3-hop
neighbourhood of up to 200 nodes from a zone and from a water heating coil with the topology
cached, and ``to_node_link()`` of the ``model`` and ``topology`` layers, timed and, in a separate
run, measured for peak memory. Needs no EnergyPlus installation.

Usage::

    uv run python benchmarks/bench_graph.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmarks._timing import best_of, peak_memory, reference_model_path
from idfkit import load_idf
from idfkit.graph import Layer, ModelGraph, ObjectKey
from idfkit.hvac import HVACTopology

LAYERS: list[Layer] = ["model", "topology"]


def main() -> None:
    """Time each operation as the best of several runs and print a Markdown table."""
    path = str(reference_model_path())
    doc = load_idf(path)
    HVACTopology.from_document(doc)
    construct = best_of(lambda: ModelGraph(doc), 5)
    graph = ModelGraph(doc)
    rows = [("ModelGraph(doc)", f"{construct * 1e6:.2f} us")]
    for obj in (next(iter(doc["Zone"])), next(iter(doc["Coil:Heating:Water"]))):
        start = ObjectKey(obj.obj_type, obj.name)
        sub = graph.neighbourhood(start, hops=3, max_nodes=200)
        walk = best_of(lambda start=start: graph.neighbourhood(start, hops=3, max_nodes=200), 5)
        label = f"neighbourhood({obj.obj_type} {obj.name}, 3 hops, 200 nodes), {len(sub.nodes)} nodes"
        rows.append((label + (", truncated" if sub.truncated else ""), f"{walk * 1000:.2f} ms"))
    export = best_of(lambda: graph.to_node_link(layers=LAYERS), 3)
    data = graph.to_node_link(layers=LAYERS)
    fresh = ModelGraph(load_idf(path))
    _, peak = peak_memory(lambda: fresh.to_node_link(layers=LAYERS))
    _, peak_cached = peak_memory(lambda: graph.to_node_link(layers=LAYERS))
    nodes = data["nodes"]
    links = data["links"] if "links" in data else data.get("edges")
    rows += [
        ("to_node_link(model, topology), topology cached", f"{export * 1000:.0f} ms"),
        ("peak memory, export with topology build / cached", f"{peak / 1e6:.1f} MB / {peak_cached / 1e6:.1f} MB"),
        (
            "exported nodes / links",
            f"{len(nodes) if isinstance(nodes, list) else '?'} / {len(links) if isinstance(links, list) else '?'}",
        ),
    ]
    print("| Operation (HospitalLowEnergy) | Measured |")
    print("|---|---|")
    for name, value in rows:
        print(f"| {name} | {value} |")


if __name__ == "__main__":
    main()
