# HVAC topology

EnergyPlus wires HVAC objects together by *node names*: a coil's `air_outlet_node_name` and the next component's `air_inlet_node_name` hold the same string. Node names are strings, not references, so the reference graph never sees them and a typo passes schema validation. `idfkit.hvac` derives the node graph from the document: every field that names a node, the connection role EnergyPlus gives that field, the flow edges between components, and static checks for broken connections.

## When to use

- You edited a node name, a branch or a loop and want to know whether it still connects.
- You want to know which components a node joins, or what is upstream or downstream of a coil.
- You want to know which loops a component sits on, which plant serves a water coil, or which zones an air loop serves.
- You want to rename a node everywhere it is used.
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
| `topo.memberships(obj)` | Every loop the object sits on, as `LoopMembership` (loop, kind, side, branch, position, stream) |
| `topo.loops()` | Every `AirLoopHVAC`, `PlantLoop` and `CondenserLoop`, air loops first |
| `topo.chain(loop, side)` | One side of a loop in flow order: a list of components per branch or path |
| `topo.zones_served(air_loop)` | The `Zone` (or `Space`) objects an air loop's demand side reaches |
| `doc.rename_node(old, new)` | Rename a node in every field and `NodeList` entry that names it, as `NodeRenameResult` |
| `topo.check()` / `check_topology(doc)` | Static connection findings, `TopologyFinding` |
| `topo.coverage` | What the view could not see: `HVACTemplate` systems, EMS programs, unclassified types |
| `category_of(obj_type)` | The `ComponentCategory` of an object type |

Node lookups are case-insensitive and answer in the model's spelling. A name that is not a node raises `KeyError`.

## Trace a node

```python
--8<-- "agent_references/snippets/hvac-topology.py:trace-node"
```

A walk's start can be a component, a `Zone` or `Space` (walked as its `ZoneHVAC:EquipmentConnections`), a node name, or a `NodeList` name. In a `FlowEdge`, a zone appears as `ObjectKey("Zone", name)`, and that key can start a new walk. An object with no node connections raises `KeyError` instead of returning an empty walk.

## Where a component sits

```python
--8<-- "agent_references/snippets/hvac-topology.py:memberships"
```

`LoopMembership.kind` is `"air"`, `"plant"`, `"condenser"` or `"zone_equipment"`, and `side` is `"supply"`, `"demand"` or `None` for zone equipment. A water coil reports both its air loop and the demand side of its water loop, each on its own `stream`. A component listed on a branch reports the branch and its 0-based `position`; a component on an air loop's path but on no branch (an outdoor-air mixer, a terminal unit, the coil inside it, a zone splitter) reports the side with `branch` and `position` set to `None`. Equipment in a zone's equipment list reports `kind="zone_equipment"`, with `loop` naming the `ZoneHVAC:EquipmentConnections`. An object on no loop returns an empty list.

## Walk a loop

```python
--8<-- "agent_references/snippets/hvac-topology.py:chain"
```

`chain(loop, side)` gives one list per branch, in `BranchList` order, for plant and condenser loops and for an air loop's supply side. An air loop's demand side has no branches: it gives one path per zone from the splitter, then the return paths; the zones themselves are not listed. A loop that is not an `AirLoopHVAC`, `PlantLoop` or `CondenserLoop` of the document raises `ValueError`, as does any `side` other than `"supply"` or `"demand"`. `zones_served` takes an air loop only.

## List findings

```python
--8<-- "agent_references/snippets/hvac-topology.py:list-findings"
```

| Code | Severity | Meaning |
|---|---|---|
| `T010` | error | A branch lists a node the component does not have |
| `T011` | error | Consecutive branch components do not connect |
| `T001` | warning | A component inlet nothing supplies, that is neither a loop inlet nor outdoor air |
| `T002` | warning | A zone inlet nothing supplies |
| `T003` | warning | A zone exhaust nothing draws from |
| `T004` | warning | A node only setpoint managers, sensors, controllers or actuators name |
| `T030` | warning | An outlet a branch carries that nothing takes |
| `T090` | info | Object types the view has no rule for |
| `T091` | info | Unexpanded `HVACTemplate` systems |

Each node gets at most one of `T001` to `T004` and `T030`, the most specific. These checks are skipped while unexpanded `HVACTemplate:*` objects are present (`T091` says so). An outlet off a branch that nothing takes is legal (exhaust fans, air-cooled condensers and relief streams vent outdoors), so it is not reported. A finding that relies on a rule written from a field's name, rather than one EnergyPlus reported, is never an error. On models older than the versions measured, severities can be capped: `capped_from` and `cap_reason` say so.

## Read coverage

```python
--8<-- "agent_references/snippets/hvac-topology.py:read-coverage"
```

An empty findings list means nothing was found *in what was covered*. Expand `HVACTemplate:*` objects (see [hvac-templates.md](hvac-templates.md)) before relying on a clean result.

## Rename a node

```python
--8<-- "agent_references/snippets/hvac-topology.py:rename-node"
```

`doc.rename_node(old, new)` rewrites every field that names the node, including fields with no connection rule, and every `NodeList` entry; a field that names a `NodeList` keeps naming the list. It is atomic: if one write fails, the writes already made are undone. `old` is matched case-insensitively and must be a node (`KeyError` otherwise). `new` must be non-empty, differ from `old`, and not already be a node (`ValueError`): two nodes are never merged. `Output:Variable` key values and other free text are not node fields and are left alone.

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

!!! failure "renaming a node by editing one field"

    ```python
    coil.air_outlet_node_name = "AHU Cooling Coil Outlet"
    # the heating coil, the Branch, the controller and the NodeList still say the old name
    ```

!!! success "rename it everywhere with `doc.rename_node`"

    ```python
    --8<-- "agent_references/snippets/hvac-topology.py:rename-node"
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
- [reference-tracking.md](reference-tracking.md): object references, which node names are not; `doc.rename()` never reaches a node.
