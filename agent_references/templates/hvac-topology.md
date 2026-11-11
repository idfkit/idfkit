# HVAC topology

EnergyPlus wires HVAC objects together by *node names*: a coil's `air_outlet_node_name` and the next component's `air_inlet_node_name` hold the same string. Node names are strings, not references, so the reference graph never sees them and a typo passes schema validation. `idfkit.hvac` derives the node graph from the document: every field that names a node, the connection role EnergyPlus gives that field, the flow edges between components, and static checks for broken connections.

## When to use

- You edited a node name, a branch or a loop and want to know whether it still connects.
- You want to know which components a node joins, or what is upstream or downstream of a coil.
- You want to know which plant serves a water coil, or which air loop serves a zone.
- You want to lint a hand-authored loop before spending a simulation on it.

## Build the view

```python
--8<-- "agent_references/snippets/hvac-topology.py:build-view"
```

`HVACTopology.from_document(doc)` is cached on the document and rebuilt after any edit, so call it again after changing the model rather than keeping an old view.

## Core API

| Symbol | Purpose |
|---|---|
| `HVACTopology.from_document(doc)` | The cached view of the document's node graph |
| `topo.nodes()` | Every node name, in the model's spelling |
| `topo.uses(node)` | Every field naming the node, as `NodeUse` (object, field, connection role, stream, fluid) |
| `topo.producers(node)` / `topo.consumers(node)` | The components writing / reading the node |
| `topo.controls(node)` | Setpoint managers, sensors, controllers and EMS uses of the node |
| `topo.ports(obj)` | The node uses of one component |
| `topo.downstream(start, hops=2, categories=None, fluid=None)` | `FlowEdge`s reached going downstream, breadth first |
| `topo.upstream(start, hops=2, categories=None, fluid=None)` | `FlowEdge`s reached going upstream, breadth first |
| `topo.check()` / `check_topology(doc)` | Static connection findings, `TopologyFinding` |
| `topo.coverage` | What the view could not see: `HVACTemplate` systems, EMS programs, unclassified types |
| `category_of(obj_type)` | The `ComponentCategory` of an object type |

Node lookups are case-insensitive and answer in the model's spelling. A name that is not a node raises `KeyError`.

## Trace a node

```python
--8<-- "agent_references/snippets/hvac-topology.py:trace-node"
```

A walk's start can be a component, a `Zone` or `Space` (walked as its `ZoneHVAC:EquipmentConnections`), a node name, or a `NodeList` name. In a `FlowEdge`, a zone appears as `ObjectKey("Zone", name)`, and that key can start a new walk. An object with no node connections raises `KeyError` instead of returning an empty walk.

## List findings

```python
--8<-- "agent_references/snippets/hvac-topology.py:list-findings"
```

| Code | Severity | Meaning |
|---|---|---|
| `T010` | error | A branch lists a node the component does not have |
| `T011` | error | Consecutive branch components do not connect |
| `T030` | warning | An inlet nothing supplies, or a branch outlet nothing takes |
| `T090` | info | Object types the view has no rule for |
| `T091` | info | Unexpanded `HVACTemplate` systems |

A finding that relies on a rule written from a field's name, rather than one EnergyPlus reported, is never an error. On models older than the versions measured, severities can be capped: `capped_from` and `cap_reason` say so.

## Read coverage

```python
--8<-- "agent_references/snippets/hvac-topology.py:read-coverage"
```

An empty findings list means nothing was found *in what was covered*. Expand `HVACTemplate:*` objects (see [hvac-templates.md](hvac-templates.md)) before relying on a clean result.

## Filter a walk

```python
--8<-- "agent_references/snippets/hvac-topology.py:category-filter"
```

## Common mistakes

!!! failure "walking from a coil without a fluid and reading the plant off the result"

    ```python
    topo.upstream(coil, hops=12, categories=[ComponentCategory.BOILER, ComponentCategory.CHILLER])
    # also reaches the chiller: the walk crosses the coil's air stream into the cooling coil's loop
    ```

!!! success "pass `fluid=Fluid.WATER` to stay on the coil's plant loop"

    ```python
    --8<-- "agent_references/snippets/hvac-topology.py:category-filter"
    ```

!!! failure "treating a clean `check()` as simulation-ready"

    ```python
    assert not topo.check()  # says nothing about sizing, controls, schedules or uncovered templates
    ```

!!! success "read `coverage`, then simulate"

    ```python
    --8<-- "agent_references/snippets/hvac-topology.py:read-coverage"
    ```

## Related

- [hvac-loops.md](hvac-loops.md): authoring the loops this view reads.
- [hvac-templates.md](hvac-templates.md): templates are not covered until expanded.
- [reference-tracking.md](reference-tracking.md): object references, which node names are not.
