from __future__ import annotations

from idfkit import IDFDocument
from idfkit.graph import GraphEdge, GraphNode, ModelGraph, Subgraph

doc: IDFDocument = ...  # type: ignore[assignment]
graph: ModelGraph = ...  # type: ignore[assignment]
sub: Subgraph = ...  # type: ignore[assignment]
node: GraphNode = ...  # type: ignore[assignment]
edge: GraphEdge = ...  # type: ignore[assignment]

# --8<-- [start:build-view]
from idfkit import load_idf
from idfkit.graph import ModelGraph

doc = load_idf("5ZoneAirCooled.idf")
graph = ModelGraph(doc)  # stores the document and returns: nothing is copied or built yet

print(graph.layers)  # ['model', 'topology']
print(graph.unavailable)  # {'results': 'no ResultIndex was passed in'}
if graph.coverage.partial:  # same Coverage as HVACTopology: templates, EMS programs, unclassified types
    print([part.kind for part in graph.coverage.uncovered])
# --8<-- [end:build-view]


# --8<-- [start:results-layer]
from idfkit.graph import ModelGraph, ObjectKey
from idfkit.simulation import ResultIndex, SimulationResult

result = SimulationResult.from_directory("run")  # a finished run with Output:SQLite, or simulate(doc, weather)
index = ResultIndex.build(doc, result, run_revision=doc.revision, run_model_hash="")
graph = ModelGraph(doc, results=index)
print(graph.layers, graph.results_state)  # ['model', 'topology', 'results'] fresh

air_loop = ObjectKey("AirLoopHVAC", "VAV Sys 1")
sub = graph.neighbourhood(air_loop, hops=1, node_kinds=["object", "result_fact", "message"])
for node in sub.nodes:
    if node.kind == "message":
        print(node.id, "|", node.label)  # message:sizing.system_flow_ratio:0 | warning sizing.system_flow_ratio
facts = [node for node in sub.nodes if node.kind == "result_fact"]
print(facts[0].id)  # fact:AIRLOOPHVAC:VAV SYS 1:ComponentSizes#66
for edge in sub.edges:
    if edge.kind == "result_link" and edge.source == facts[0].id:
        print(edge.target, dict(edge.attrs))  # object:AIRLOOPHVAC:VAV SYS 1 {'confidence': 'exact', 'rule': 'exact'}
graph = ModelGraph(doc)  # the sections below use the model and topology layers only
# --8<-- [end:results-layer]


# --8<-- [start:neighbourhood]
from idfkit.graph import ModelGraph, ObjectKey

coil = ObjectKey("Coil:Cooling:Water", "OA Cooling Coil 1")
print(graph.node_id(coil))  # object:COIL:COOLING:WATER:OA COOLING COIL 1

sub = graph.neighbourhood(coil, hops=1)  # both directions, breadth first; max_nodes=200 by default
for node in sub.nodes:  # sub.nodes[0] is the start
    print(node.kind, node.label, dict(node.attrs))
# object  Coil:Cooling:Water "OA Cooling Coil 1"          {'category': 'cooling_coil'}
# object  Schedule:Compact "CoolingCoilAvailSched"        {'category': 'other'}
# object  Branch "OA Cooling Coil Branch"                 {'category': 'other'}
# node    Node "OA Heating Coil 1 Air Outlet Node"        {'fluid': 'Air'}
# node    Node "OA Cooling Coil 1 Water Inlet Node"       {'fluid': 'Water'}
# object  PlantLoop "Chilled Water Loop"                  {'category': 'other'}
# ...

for edge in sub.edges:
    print(edge.kind, edge.source, "->", edge.target, edge.key)
# reference   object:COIL:COOLING:WATER:OA COOLING COIL 1 -> object:SCHEDULE:COMPACT:COOLINGCOILAVAILSCHED
# reference   object:BRANCH:OA COOLING COIL BRANCH -> object:COIL:COOLING:WATER:OA COOLING COIL 1
# flow        node:OA HEATING COIL 1 AIR OUTLET NODE -> object:COIL:COOLING:WATER:OA COOLING COIL 1
# flow        object:COIL:COOLING:WATER:OA COOLING COIL 1 -> node:OA MIXING BOX 1 INLET NODE
# membership  object:COIL:COOLING:WATER:OA COOLING COIL 1 -> object:PLANTLOOP:CHILLED WATER LOOP

# A fluid node starts a walk by name, case-insensitively.
around_node = graph.neighbourhood("Mixed Air Node 1", hops=1)
# --8<-- [end:neighbourhood]


# --8<-- [start:bounds]
sub = graph.neighbourhood(coil, hops=3, max_nodes=10)
if sub.truncated:  # the hop or node bound cut the walk
    print(sub.omitted_nodes, "nodes reached but not returned (a lower bound)")
    # Continue from the frontier: returned nodes with neighbours that were not returned.
    frontier = set(sub.frontier)
    for node in sub.nodes:
        if node.id not in frontier:
            continue
        restart = node.key if node.key is not None else node.node  # ObjectKey, or a fluid node name
        if restart is not None:
            more = graph.neighbourhood(restart, hops=1, max_nodes=10)
# --8<-- [end:bounds]


# --8<-- [start:filters]
from idfkit.graph import EdgeKind, Layer, NodeKind
from idfkit.hvac import ComponentCategory

# Kinds and layers are string literals; these aliases type them.
present: list[Layer] = list(graph.layers)  # ['model', 'topology'], plus 'results' with a ResultIndex
objects_only: list[NodeKind] = ["object"]
fluid_edges: list[EdgeKind] = ["flow", "control"]

# Only the fluid connections: no schedules, branches or loops pulled in by reference edges.
flow_only = graph.neighbourhood(coil, hops=3, edge_kinds=["flow"])

# Keep only fans (plus the start and the fluid nodes on the paths to them).
# The filter is applied before max_nodes, so the bound counts only what you asked for.
fans = graph.neighbourhood(coil, hops=4, categories=[ComponentCategory.FAN])
print([n.label for n in fans.nodes if n.kind == "object"])
# ['Coil:Cooling:Water "OA Cooling Coil 1"', 'Fan:VariableVolume "Supply Fan 1"']

# Objects and references only: the reference graph, walkable with the same call.
references_only = graph.neighbourhood(coil, hops=2, node_kinds=objects_only, edge_kinds=["reference"])
controls = graph.neighbourhood(coil, hops=2, edge_kinds=fluid_edges)
# --8<-- [end:filters]


# --8<-- [start:export]
import json

from idfkit.graph import NODE_LINK_FORMAT_VERSION, JSONValue, save_node_link, write_node_link

save_node_link(graph, "model-graph.json")  # the whole model and topology, UTF-8

text = write_node_link(graph, start=coil, hops=2)  # one neighbourhood; start and hops go together
data = json.loads(text)
assert data["graph"]["format"] == "idfkit-model-graph"
layers: JSONValue = data["graph"]["layers"]  # every value in the export is plain JSON
assert data["graph"]["format_version"] == NODE_LINK_FORMAT_VERSION
print(data["graph"]["layers"], data["graph"]["unavailable"])
# ['model', 'topology'] {'results': 'no ResultIndex was passed in'}: a missing layer is listed, never an error
print(len(data["nodes"]), len(data["edges"]))  # edges are under "edges", not "links"

# Narrow the export: only the model layer (objects and references), or only some kinds.
references = json.loads(write_node_link(graph, layers=["model"]))
fluid_network = json.loads(write_node_link(graph, edge_kinds=["flow", "control"]))

# A d3-force layout expects "links": rename the key in one line.
data["links"] = data.pop("edges")
# --8<-- [end:export]


# --8<-- [start:standalone-script]
"""List connection findings, trace a node, walk a coil's neighbourhood and export the graph.

Usage: python model_graph.py 5ZoneAirCooled.idf
"""

import sys
from pathlib import Path

from idfkit import load_idf
from idfkit.graph import ModelGraph, ObjectKey, save_node_link
from idfkit.hvac import ComponentCategory, HVACTopology, check_topology


def main(path: str) -> None:
    doc = load_idf(path)

    # 1. Connection findings: an empty list means nothing was found in what was covered.
    for finding in check_topology(doc):
        print(finding.code, finding.severity, finding.message)

    # 2. Trace a node: every field that names it, then the components one step downstream.
    topo = HVACTopology.from_document(doc)
    node_name = "Mixed Air Node 1"
    for use in topo.uses(node_name):
        print(use.object.object_type, use.object.name, use.field, use.connection.value)
    for flow in topo.downstream(node_name, hops=1):
        print(flow.source.name, "->", flow.target.name, "via", flow.node)

    # 3. Walk a coil's neighbourhood: references, fluid nodes and loop memberships together.
    graph = ModelGraph(doc)
    coil = ObjectKey("Coil:Cooling:Water", "Main Cooling Coil 1")
    sub = graph.neighbourhood(coil, hops=2, max_nodes=25)
    print(len(sub.nodes), "nodes,", len(sub.edges), "edges; truncated:", sub.truncated)
    for edge in sub.edges:
        if edge.kind in ("flow", "membership") and sub.start in (edge.source, edge.target):
            print(" ", edge.kind, edge.source, "->", edge.target)
    fans = graph.neighbourhood(coil, hops=4, edge_kinds=["flow"], categories=[ComponentCategory.FAN])
    print("fans within 4 hops:", [n.label for n in fans.nodes if n.kind == "object" and n.id != sub.start])
    print("missing layers:", sub.unavailable)

    # 4. Export the coil's neighbourhood as node-link JSON, next to the model.
    out = Path(path).with_suffix(".graph.json")
    save_node_link(graph, out, start=coil, hops=2)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "5ZoneAirCooled.idf")
# --8<-- [end:standalone-script]
