# Model graph

A model has two kinds of connection. Fields that name another object (a surface's `zone_name`, a branch's component name) are *references*, tracked by the reference graph. Fields that name an HVAC node are *node connections*, read by `idfkit.hvac`. `idfkit.graph.ModelGraph` joins the two under one vocabulary, so one walk from a coil reaches its schedule, its branch, its inlet and outlet nodes, the components on the other side of them and the loops it sits on. It exports node-link JSON that networkx and d3 read.

The view adds no domain logic and copies no data: each walk asks the reference graph and the cached `HVACTopology` at walk time, so it is always current. Use `idfkit.hvac` directly for connection checks, loop chains and node renames; use `ModelGraph` when one question crosses both kinds of connection, or to hand the model to a graph library.

## When to use

- You want everything within a few steps of an object, whatever the kind of connection.
- You want a bounded, filtered neighbourhood to show to a person or an agent.
- You want to export the model as a graph for networkx, d3 or your own tooling.

## Build the view

```python
from idfkit import load_idf
from idfkit.graph import ModelGraph

doc = load_idf("5ZoneAirCooled.idf")
graph = ModelGraph(doc)  # stores the document and returns: nothing is copied or built yet

print(graph.layers)  # ['model', 'topology']
print(graph.unavailable)  # {'results': 'no ResultIndex was passed in'}
if graph.coverage.partial:  # same Coverage as HVACTopology: templates, EMS programs, unclassified types
    print([part.kind for part in graph.coverage.uncovered])
```

`ModelGraph(doc)` has the `model` and `topology` layers. The `results` layer appears only when a run's linked results are passed in with `ModelGraph(doc, results=index)` (see [Results layer](#results-layer)); without them `graph.unavailable` is `{"results": "no ResultIndex was passed in"}` and no `result_fact`, `message` or `result_link` appears.

## Vocabulary

| Kind | Layer | Stands for |
|---|---|---|
| node `object` | `model` | A model object. `key` is its `ObjectKey`; `attrs["category"]` is its `ComponentCategory` value |
| node `node` | `topology` | A fluid node. `node` is its name in the model's spelling; `attrs["fluid"]` is `Air`, `Water`, … |
| edge `reference` | `model` | A field of `source` names the object `target`. `attrs["field"]` names the field |
| edge `flow` | `topology` | A component takes flow from (`node -> object`) or puts flow into (`object -> node`) a node. `attrs`: `field`, `connection_type`, `fluid`, `provenance`, and `via_nodelist` when named through a `NodeList` |
| edge `control` | `topology` | A sensor, actuator or setpoint use of a node (`object -> node`). `attrs`: `field`, `connection_type`, `provenance`; EMS uses add `rule: "ems_key"`, `confidence: "convention"` |
| edge `membership` | `topology` | A component sits on a loop, or zone equipment on its `ZoneHVAC:EquipmentConnections` (`object -> loop`). `attrs`: `loop_kind`, `side`, `branch`, `position` |
| node `result_fact` | `results` | One value a run reported for an object or node. `key` is the owner; `attrs`: `metric`, `value`, `units`, `source`, `where`, `multiplier`, `stale` |
| node `message` | `results` | One warning, severe or fatal message. `attrs`: `severity`, `message_kind`, `text`, `occurrences`, `first_seen`, `stale` |
| edge `result_link` | `results` | A fact or message is linked to an object or node (`result -> object`). `attrs`: `confidence`, `rule` of the link |

Graph node ids are `object:<TYPE>:<NAME>` and `node:<NAME>`, upper-cased (results add `fact:<TYPE>:<NAME>:<where>` and `message:<kind>:<index>`), so equal ids mean equal identity. `graph.node_id(target)` gives the id of an `ObjectKey` or a node name. Edge `key` is unique between the same two endpoints, such as `reference:zone_name` or `flow:air_outlet_node_name`. The vocabulary may grow in a minor release: code that reads kinds must ignore kinds it does not know.

## Core API

| Symbol | Purpose |
|---|---|
| `ModelGraph(doc)` | The view. Stores the document; builds nothing |
| `graph.layers` / `graph.unavailable` | The layers present, and each missing layer with the reason |
| `graph.coverage` | What the view cannot see (the `Coverage` of `HVACTopology`) |
| `graph.node_id(target)` | The graph node id of an `ObjectKey` or a node name. `KeyError` if absent |
| `graph.neighbourhood(start, *, hops=1, node_kinds, edge_kinds, categories, max_nodes=200)` | A bounded `Subgraph` around an object or node, walked breadth first in both directions |
| `graph.to_node_link(*, layers, node_kinds, edge_kinds, start, hops)` | The view as node-link data, a `dict[str, JSONValue]` |
| `write_node_link(graph, ...)` / `save_node_link(graph, path, ...)` | The same, as JSON text or a UTF-8 file |
| `NODE_LINK_FORMAT_VERSION` | The export format version, `1`. Raised only when a key is removed or renamed or a kind changes meaning |
| `GraphNode`, `GraphEdge`, `Subgraph` | Frozen dataclasses the walk returns |
| `NodeKind`, `EdgeKind`, `Layer`, `JSONValue` | The `Literal` vocabularies and the JSON value type |
| `ObjectKey`, `Coverage` | Re-exported from `idfkit.hvac` |

## Walk a neighbourhood

```python
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
```

`start` is an `ObjectKey` or a node name (case-insensitive). `hops=0` returns the start alone. The edges returned are those between returned nodes. A `Subgraph` also carries `layers`, `unavailable` and `coverage`, so a reader of the result alone knows what it could not see. `KeyError` if the start is not in the model; `ValueError` for `hops < 0` or `max_nodes < 1`.

## Bound the walk

```python
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
```

`truncated` is true when either the hop or the node bound cut the walk. `omitted_nodes` counts nodes reached but not returned; it is a lower bound, since the walk stops at the cut. `frontier` lists the returned nodes that have neighbours not returned: restart from one to go further. A `GraphNode` restarts with its `key` (an object) or its `node` (a fluid node).

## Filter the walk

```python
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
```

`node_kinds` and `edge_kinds` restrict what the walk passes through. `categories` keeps only object nodes of those `ComponentCategory` values, plus the start and the fluid nodes on the paths to them, and is applied before `max_nodes`. Unknown kinds in a filter are ignored, not an error.

## Export node-link JSON

```python
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
```

The top level is `directed: true`, `multigraph: true`, `graph`, `nodes` and `edges`. `graph` carries `format` (`"idfkit-model-graph"`), `format_version`, `idfkit_version`, `energyplus_version`, `layers`, `unavailable`, `coverage`, `scope` (the `start`, `hops` and kind filters used) and `results_state` (`"fresh"` or `"stale"` with a results layer, else `None`). Each node and edge flattens its `attrs`; an object node's key is split into `object_type` and `name`. With no `start`, the export is the whole model; `start` and `hops` must be given together (`ValueError` otherwise) and export the neighbourhood with no node bound.

The edge list is under `"edges"`, not `"links"`:

- **networkx 3.6 or later** reads it unchanged: `networkx.node_link_graph(data)`.
- **networkx 3.4 and 3.5** need the key named: `networkx.node_link_graph(data, edges="edges")`.
- **d3-force** expects `links`: rename the key with `data["links"] = data.pop("edges")`.

```python
import json
import networkx as nx  # not an idfkit dependency: install it yourself

data = json.loads(write_node_link(ModelGraph(doc)))
g = nx.node_link_graph(data)  # networkx >= 3.6; on 3.4 / 3.5 add edges="edges"
assert g.is_directed() and g.is_multigraph()
assert g.number_of_nodes() == len(data["nodes"]) and g.number_of_edges() == len(data["edges"])
```


## Results layer

```python
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
```

Build the `ResultIndex` right after the run (see `result-parsing.md`) and pass it in. Each fact and message joins the object or node it is linked to by a `result_link` edge carrying the link's `confidence` and `rule`. An object can carry well over a hundred facts, so filter by kind or keep `max_nodes` bounded. When the document has changed since the run, `graph.results_state` is `"stale"` and every result node has `stale: True`: the results are still walked, never hidden. For one object's results in full (messages deduplicated by kind, available variables), `index.for_object(key)` is the direct call.
## A standalone script

Everything above in one script that uses only names from `idfkit`, `idfkit.hvac` and `idfkit.graph` `__all__`: list connection findings, trace a node, walk a coil's neighbourhood, export it.

```python
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
```

## Common mistakes

!!! failure "parsing graph node ids to get the object back"

    ```python
    _, obj_type, name = node.id.split(":", 2)  # breaks on types and names with colons, and upper-cases both
    ```

!!! success "read `node.key` (objects) or `node.node` (fluid nodes)"

    ```python
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
    ```

!!! failure "treating a bounded walk as the whole neighbourhood"

    ```python
    sub = graph.neighbourhood(coil, hops=3, max_nodes=10)
    print(len(sub.nodes), "components connected")  # silently cut at 10
    ```

!!! success "check `truncated` and continue from the `frontier`"

    ```python
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
    ```

!!! failure "matching on every kind the vocabulary has today"

    ```python
    assert edge.kind in ("reference", "flow", "control", "membership")  # fails once a kind is added
    ```

!!! success "handle the kinds you need and skip the rest"

    ```python
    flows = [e for e in sub.edges if e.kind == "flow"]
    ```

## Related

- [reference-tracking.md](reference-tracking.md): the `model` layer on its own, with renames and dangling references.
- [hvac-topology.md](hvac-topology.md): the `topology` layer on its own, with connection checks, loop chains and `rename_node`.
- [hvac-templates.md](hvac-templates.md): `HVACTemplate:*` systems are not in the topology layer until expanded; `coverage` says so.
