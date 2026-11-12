# Model graph

A model has two kinds of connection. Fields that name another object (a surface's `zone_name`, a branch's component name) are *references*, tracked by the reference graph. Fields that name an HVAC node are *node connections*, read by `idfkit.hvac`. `idfkit.graph.ModelGraph` joins the two under one vocabulary, so one walk from a coil reaches its schedule, its branch, its inlet and outlet nodes, the components on the other side of them and the loops it sits on. It exports node-link JSON that networkx and d3 read.

The view adds no domain logic and copies no data: each walk asks the reference graph and the cached `HVACTopology` at walk time, so it is always current. Use `idfkit.hvac` directly for connection checks, loop chains and node renames; use `ModelGraph` when one question crosses both kinds of connection, or to hand the model to a graph library.

## When to use

- You want everything within a few steps of an object, whatever the kind of connection.
- You want a bounded, filtered neighbourhood to show to a person or an agent.
- You want to export the model as a graph for networkx, d3 or your own tooling.

## Build the view

```python
--8<-- "agent_references/snippets/model-graph.py:build-view"
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
--8<-- "agent_references/snippets/model-graph.py:neighbourhood"
```

`start` is an `ObjectKey` or a node name (case-insensitive). `hops=0` returns the start alone. The edges returned are those between returned nodes. A `Subgraph` also carries `layers`, `unavailable` and `coverage`, so a reader of the result alone knows what it could not see. `KeyError` if the start is not in the model; `ValueError` for `hops < 0` or `max_nodes < 1`.

## Bound the walk

```python
--8<-- "agent_references/snippets/model-graph.py:bounds"
```

`truncated` is true when either the hop or the node bound cut the walk. `omitted_nodes` counts nodes reached but not returned; it is a lower bound, since the walk stops at the cut. `frontier` lists the returned nodes that have neighbours not returned: restart from one to go further. A `GraphNode` restarts with its `key` (an object) or its `node` (a fluid node).

## Filter the walk

```python
--8<-- "agent_references/snippets/model-graph.py:filters"
```

`node_kinds` and `edge_kinds` restrict what the walk passes through. `categories` keeps only object nodes of those `ComponentCategory` values, plus the start and the fluid nodes on the paths to them, and is applied before `max_nodes`. Unknown kinds in a filter are ignored, not an error.

## Export node-link JSON

```python
--8<-- "agent_references/snippets/model-graph.py:export"
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
--8<-- "agent_references/snippets/model-graph.py:results-layer"
```

Build the `ResultIndex` right after the run (see `result-parsing.md`) and pass it in. Each fact and message joins the object or node it is linked to by a `result_link` edge carrying the link's `confidence` and `rule`. An object can carry well over a hundred facts, so filter by kind or keep `max_nodes` bounded. When the document has changed since the run, `graph.results_state` is `"stale"` and every result node has `stale: True`: the results are still walked, never hidden. For one object's results in full (messages deduplicated by kind, available variables), `index.for_object(key)` is the direct call.
## A standalone script

Everything above in one script that uses only names from `idfkit`, `idfkit.hvac` and `idfkit.graph` `__all__`: list connection findings, trace a node, walk a coil's neighbourhood, export it.

```python
--8<-- "agent_references/snippets/model-graph.py:standalone-script"
```

## Common mistakes

!!! failure "parsing graph node ids to get the object back"

    ```python
    _, obj_type, name = node.id.split(":", 2)  # breaks on types and names with colons, and upper-cases both
    ```

!!! success "read `node.key` (objects) or `node.node` (fluid nodes)"

    ```python
    --8<-- "agent_references/snippets/model-graph.py:bounds"
    ```

!!! failure "treating a bounded walk as the whole neighbourhood"

    ```python
    sub = graph.neighbourhood(coil, hops=3, max_nodes=10)
    print(len(sub.nodes), "components connected")  # silently cut at 10
    ```

!!! success "check `truncated` and continue from the `frontier`"

    ```python
    --8<-- "agent_references/snippets/model-graph.py:bounds"
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
