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
from idfkit import load_idf
from idfkit.hvac import HVACTopology

doc = load_idf("5ZoneAirCooled.idf")
topo = HVACTopology.from_document(doc)  # cached on the document until the next edit
print(len(topo.nodes()), "nodes")
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
# Every field that names a node, with the role EnergyPlus gives it
for use in topo.uses("Main Cooling Coil 1 Outlet Node"):
    print(use.object.object_type, use.object.name, use.field, use.connection, use.fluid)
# Coil:Cooling:Water  Main Cooling Coil 1  air_outlet_node_name  ConnectionType.OUTLET  Fluid.AIR
# Coil:Heating:Water  Main Heating Coil 1  air_inlet_node_name   ConnectionType.INLET   Fluid.AIR
# Branch              Air Loop Main Branch components.component_outlet_node_name ...

# Who writes the node, who reads it, what senses or sets it
writers = topo.producers("Main Cooling Coil 1 Outlet Node")
readers = topo.consumers("Main Cooling Coil 1 Outlet Node")
sensors = topo.controls("Main Cooling Coil 1 Outlet Node")

# The ports of one component, and the edges one step downstream of it
coil = doc["Coil:Cooling:Water"]["Main Cooling Coil 1"]
for use in topo.ports(coil):
    print(use.node, use.connection)
for edge in topo.downstream(coil, hops=1):
    print(edge.source.name, "->", edge.target.name, "via", edge.node, edge.fluid)
```

A walk's start can be a component, a `Zone` or `Space` (walked as its `ZoneHVAC:EquipmentConnections`), a node name, or a `NodeList` name. In a `FlowEdge`, a zone appears as `ObjectKey("Zone", name)`, and that key can start a new walk. An object with no node connections raises `KeyError` instead of returning an empty walk.

## Where a component sits

```python
coil = doc["Coil:Cooling:Water"]["Main Cooling Coil 1"]
for membership in topo.memberships(coil):
    branch = membership.branch.name if membership.branch else None
    print(membership.loop.name, membership.kind, membership.side, branch, membership.position)
# VAV Sys 1           air    supply  VAV Sys 1 Main Branch  1
# Chilled Water Loop  plant  demand  Cooling Coil Branch    0

# Which plant serves this coil? Read the water-side membership, no walk needed.
plants = [m.loop.name for m in topo.memberships(coil) if m.kind in ("plant", "condenser")]

# A terminal's reheat coil is on the air loop's demand path but on no branch of it.
reheat = doc["Coil:Heating:Water"]["SPACE1-1 Zone Coil"]
on_air = [m for m in topo.memberships(reheat) if m.kind == "air"]
assert on_air[0].side == "demand" and on_air[0].branch is None and on_air[0].position is None
```

`LoopMembership.kind` is `"air"`, `"plant"`, `"condenser"` or `"zone_equipment"`, and `side` is `"supply"`, `"demand"` or `None` for zone equipment. A water coil reports both its air loop and the demand side of its water loop, each on its own `stream`. A component listed on a branch reports the branch and its 0-based `position`; a component on an air loop's path but on no branch (an outdoor-air mixer, a terminal unit, the coil inside it, a zone splitter) reports the side with `branch` and `position` set to `None`. Equipment in a zone's equipment list reports `kind="zone_equipment"`, with `loop` naming the `ZoneHVAC:EquipmentConnections`. An object on no loop returns an empty list.

## Walk a loop

```python
for loop in topo.loops():  # air loops first, then plant, then condenser loops
    print(loop.obj_type, loop.name)

air_loop = doc["AirLoopHVAC"]["VAV Sys 1"]
for path in topo.chain(air_loop, "supply"):  # one list per branch, in BranchList order
    print([o.name for o in path])
# ['OA Sys 1', 'Main Cooling Coil 1', 'Main Heating Coil 1', 'Supply Fan 1']

for path in topo.chain(air_loop, "demand"):  # one path per zone from the splitter, then the return paths
    print([o.name for o in path])
# ['Zone Supply Air Splitter 1', 'SPACE1-1 VAV Reheat', 'SPACE1-1 Zone Coil']
# ... one per zone ...
# ['Return-Plenum-1']

print([z.name for z in topo.zones_served(air_loop)])
# ['SPACE1-1', 'SPACE2-1', 'SPACE3-1', 'SPACE4-1', 'SPACE5-1']

chilled_water = doc["PlantLoop"]["Chilled Water Loop"]
demand_branches = topo.chain(chilled_water, "demand")  # one list per demand branch, bypass included
```

`chain(loop, side)` gives one list per branch, in `BranchList` order, for plant and condenser loops and for an air loop's supply side. An air loop's demand side has no branches: it gives one path per zone from the splitter, then the return paths; the zones themselves are not listed. A loop that is not an `AirLoopHVAC`, `PlantLoop` or `CondenserLoop` of the document raises `ValueError`, as does any `side` other than `"supply"` or `"demand"`. `zones_served` takes an air loop only.

## List findings

```python
from idfkit.hvac import check_topology

for finding in check_topology(doc):
    print(finding.code, finding.severity, finding.message)
    if finding.expected is not None:
        print("  the other side says", finding.expected, "but this object says", finding.actual)

errors = [f for f in topo.check() if f.severity == "error"]
if errors:
    raise SystemExit("Fix the connection errors before simulating")
# A clean result does not mean the model simulates: run EnergyPlus to know that.
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
from idfkit.hvac import UncoveredPart

coverage = topo.coverage
if coverage.partial:
    parts: tuple[UncoveredPart, ...] = coverage.uncovered
    for part in parts:
        # hvac_template, ems_program or unclassified_type, with up to 3 examples
        print(part.kind, part.count, part.reason, [k.name for k in part.examples])
```

An empty findings list means nothing was found *in what was covered*. Expand `HVACTemplate:*` objects (see [hvac-templates.md](hvac-templates.md)) before relying on a clean result.

## Rename a node

```python
old, new = "Main Cooling Coil 1 Outlet Node", "AHU Cooling Coil Outlet"
from idfkit.hvac import NodeRenameResult

result: NodeRenameResult = doc.rename_node(old, new)
print(result.fields_updated)  # 6: both coils, two Branch fields, the controller sensor, a NodeList entry
print([key.name for key in result.objects])

# Output:Variable key values are free text, not node fields: rename_node leaves them alone.
for var in doc["Output:Variable"]:
    if var.key_value.upper() == old.upper():
        var.key_value = new

topo = HVACTopology.from_document(doc)  # the edit made the old view stale
assert [o.name for o in topo.consumers(new)] == ["Main Heating Coil 1"]
```

`doc.rename_node(old, new)` rewrites every field that names the node, including fields with no connection rule, and every `NodeList` entry; a field that names a `NodeList` keeps naming the list. It is atomic: if one write fails, the writes already made are undone. `old` is matched case-insensitively and must be a node (`KeyError` otherwise). `new` must be non-empty, differ from `old`, and not already be a node (`ValueError`): two nodes are never merged. `Output:Variable` key values and other free text are not node fields and are left alone.

## Filter a walk

```python
from idfkit.hvac import ComponentCategory, Fluid, category_of

# The category comes from the object type alone, so it needs no model.
print(category_of("Coil:Cooling:Water"))  # ComponentCategory.COOLING_COIL
print(category_of("Schedule:Compact"))  # ComponentCategory.OTHER

# Which plant supplies this coil? Stay on the water stream, keep only plant sources.
sources = topo.upstream(
    coil,
    hops=12,
    categories=[ComponentCategory.CHILLER, ComponentCategory.BOILER],
    fluid=Fluid.WATER,
)
print({e.source.name for e in sources})

# Without a fluid the walk follows every stream: from a coil's air side it can reach
# another coil and then that coil's plant. A category filter keeps edges, never stops the walk.
fans_downstream = topo.downstream(coil, hops=4, categories=[ComponentCategory.FAN])

# A walk can start from a component, a Zone or Space, a node name, or a NodeList name.
from_zone = topo.upstream(doc["Zone"]["SPACE1-1"], hops=2)
```

## Common mistakes

!!! failure "walking from a coil without a fluid and reading the plant off the result"

    ```python
    topo.upstream(coil, hops=12, categories=[ComponentCategory.BOILER, ComponentCategory.CHILLER])
    # also reaches the chiller: the walk crosses the coil's air stream into the cooling coil's loop
    ```

!!! success "pass `fluid=Fluid.WATER` to stay on the coil's plant loop"

    ```python
    from idfkit.hvac import ComponentCategory, Fluid, category_of

    # The category comes from the object type alone, so it needs no model.
    print(category_of("Coil:Cooling:Water"))  # ComponentCategory.COOLING_COIL
    print(category_of("Schedule:Compact"))  # ComponentCategory.OTHER

    # Which plant supplies this coil? Stay on the water stream, keep only plant sources.
    sources = topo.upstream(
        coil,
        hops=12,
        categories=[ComponentCategory.CHILLER, ComponentCategory.BOILER],
        fluid=Fluid.WATER,
    )
    print({e.source.name for e in sources})

    # Without a fluid the walk follows every stream: from a coil's air side it can reach
    # another coil and then that coil's plant. A category filter keeps edges, never stops the walk.
    fans_downstream = topo.downstream(coil, hops=4, categories=[ComponentCategory.FAN])

    # A walk can start from a component, a Zone or Space, a node name, or a NodeList name.
    from_zone = topo.upstream(doc["Zone"]["SPACE1-1"], hops=2)
    ```

!!! failure "renaming a node by editing one field"

    ```python
    coil.air_outlet_node_name = "AHU Cooling Coil Outlet"
    # the heating coil, the Branch, the controller and the NodeList still say the old name
    ```

!!! success "rename it everywhere with `doc.rename_node`"

    ```python
    old, new = "Main Cooling Coil 1 Outlet Node", "AHU Cooling Coil Outlet"
    from idfkit.hvac import NodeRenameResult

    result: NodeRenameResult = doc.rename_node(old, new)
    print(result.fields_updated)  # 6: both coils, two Branch fields, the controller sensor, a NodeList entry
    print([key.name for key in result.objects])

    # Output:Variable key values are free text, not node fields: rename_node leaves them alone.
    for var in doc["Output:Variable"]:
        if var.key_value.upper() == old.upper():
            var.key_value = new

    topo = HVACTopology.from_document(doc)  # the edit made the old view stale
    assert [o.name for o in topo.consumers(new)] == ["Main Heating Coil 1"]
    ```

!!! failure "treating a clean `check()` as simulation-ready"

    ```python
    assert not topo.check()  # says nothing about sizing, controls, schedules or uncovered templates
    ```

!!! success "read `coverage`, then simulate"

    ```python
    from idfkit.hvac import UncoveredPart

    coverage = topo.coverage
    if coverage.partial:
        parts: tuple[UncoveredPart, ...] = coverage.uncovered
        for part in parts:
            # hvac_template, ems_program or unclassified_type, with up to 3 examples
            print(part.kind, part.count, part.reason, [k.name for k in part.examples])
    ```

## Related

- [hvac-loops.md](hvac-loops.md): authoring the loops this view reads.
- [hvac-templates.md](hvac-templates.md): templates are not covered until expanded.
- [reference-tracking.md](reference-tracking.md): object references, which node names are not; `doc.rename()` never reaches a node.
