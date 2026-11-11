# HVAC loops

When `HVACTemplate:*` isn't enough — custom controls, unusual topology, plant interactions templates can't express — you author `AirLoopHVAC`, `PlantLoop`, and `CondenserLoop` by hand. This is dozens of interconnected objects (branches, splitters, mixers, coils, fans, pumps, setpoint managers) wired by node names. **This reference is scoped to idfkit-specific machinery for surviving that complexity**, not to EnergyPlus engineering — see the EnergyPlus I/O Reference for what each object does.

## When to use

- HVACTemplate can't represent what you need (e.g. ground-source heat pump with a custom storage tank).
- You're retrofitting a model that already has hand-authored loops.
- You need to lint an existing loop graph before simulating.

If templates work, use them. They're simpler, faster to author, and idfkit has more support for them. See [hvac-templates.md](hvac-templates.md).

## Where idfkit helps

idfkit doesn't provide higher-level "build me an air loop" helpers — you author each `AirLoopHVAC`, `Branch`, `BranchList`, `Connector:Splitter`, `Connector:Mixer`, `Coil:Cooling:Water`, etc. through `doc.add()`. But once you've done that, idfkit gives you three things EnergyPlus alone doesn't:

1. **Schema validation catches node-name typos**. EnergyPlus only catches them at runtime, deep in the `.err` file.
2. **The reference graph tells you what wires to what**. `doc.get_referencing("AHU-1 Cooling Coil")` returns every object that mentions that coil — branches, controllers, setpoint managers, etc.
3. **Cascading renames work across the loop graph**. Rename a coil and every branch, controller, and node specification updates.

## Canonical pattern: lint before simulate

```python
from idfkit import load_idf, validate_document

doc = load_idf("custom_loop.idf")
result = validate_document(doc)
if not result.is_valid:
    for err in result.errors:
        print(err)
    raise SystemExit("Refusing to simulate an invalid loop graph")
```

`validate_document` with `check_references=True` (the default) reports every dangling node-name reference as an `E004` error. That's the single most useful smoke test before kicking off a simulation.

## Tracing a loop with `get_referencing`

```python
# Every object that mentions "AHU-1 Cooling Coil"
for obj in doc.get_referencing("AHU-1 Cooling Coil"):
    print(obj.obj_type, obj.name)
# Branch 'AHU-1 Cooling Branch'
# Controller:WaterCoil 'AHU-1 Cooling Coil Controller'
# SetpointManager:Scheduled 'AHU-1 Cooling Coil Setpoint'
# ...
```

If a branch or controller you expect to see isn't there, the wiring is wrong — fix it before simulating, not after.

## Safe renames

```python
# Rename a coil. Every branch component, controller, setpoint manager
# that pointed at "AHU-1 Cooling Coil" now points at "AHU-1 Cooling Coil A".
doc["Coil:Cooling:Water"]["AHU-1 Cooling Coil"].name = "AHU-1 Cooling Coil A"
```

This is the central reason idfkit is safer than text-editing IDFs: a rename through the reference graph is atomic and complete. Renaming via raw string substitution (e.g. `sed`) inevitably misses one of the dozens of fields that mention the name.

See [reference-tracking.md](reference-tracking.md) for the full rename machinery.

## Branch + BranchList walkthrough

The branch/branch-list graph is what most loop authoring boils down to. Use the reference graph to verify it.

```python
# All branches in the model
for branch in doc.get_collection("Branch"):
    print(branch.name)
    # Each Branch has an extensible list of components
    for comp in branch.components:
        print("  ", comp.component_object_type, comp.component_name)

# All BranchLists, and which branches they reference
for bl in doc.get_collection("BranchList"):
    print(bl.name)
    for branch_name in doc.get_references(bl):
        print("  branch:", branch_name)
```

A loop with a missing branch-list entry simulates and produces silently wrong results. The reference-graph walk above catches it in seconds.

## Connector:Splitter / Connector:Mixer

Splitter/mixer pairs define the parallel paths in an air or water loop. Each names branches via extensible fields:

```python
splitter = doc.add("Connector:Splitter", "CHW Loop Splitter")
splitter.inlet_branch_name = "CHW Loop Supply Inlet Branch"
splitter.branches.append(outlet_branch_name="Chiller 1 Branch")
splitter.branches.append(outlet_branch_name="Chiller 2 Branch")

mixer = doc.add("Connector:Mixer", "CHW Loop Mixer")
mixer.outlet_branch_name = "CHW Loop Supply Outlet Branch"
mixer.branches.append(inlet_branch_name="Chiller 1 Branch")
mixer.branches.append(inlet_branch_name="Chiller 2 Branch")
```

Validation checks that every branch name in the splitter/mixer exists as a `Branch` object — typos surface as `E004`.

## Pattern: link by node names

EnergyPlus loops are wired by string-typed *node names*, not by object references. A coil declares `air_inlet_node_name` and `air_outlet_node_name`; the adjacent branch component declares the same node names on its own side. **idfkit's schema-driven validation enforces that node names are real strings, not that two objects share the right one.**

Nothing wires two nodes for you, but `idfkit.hvac` checks them: `HVACTopology` reads every node field with the role EnergyPlus gives it, and `check_topology(doc)` reports a branch listing a node its component does not have (`T010`), consecutive branch components that do not connect (`T011`) and inlets nothing supplies (`T030`). See [hvac-topology.md](hvac-topology.md).

```python
# Coil names node A and node B
coil = doc.add(
    "Coil:Cooling:Water",
    "AHU-1 Cooling Coil",
    availability_schedule_name="Always On",
    water_inlet_node_name="CHW Inlet Node",
    water_outlet_node_name="CHW Outlet Node",
    air_inlet_node_name="AHU-1 Mixed Air Node",
    air_outlet_node_name="AHU-1 Cooling Coil Outlet Node",
    # ...
)
# Adjacent component must declare the same air outlet name as its inlet
fan = doc.add(
    "Fan:VariableVolume",
    "AHU-1 Fan",
    air_inlet_node_name="AHU-1 Cooling Coil Outlet Node",  # MATCHES coil.air_outlet_node_name
    air_outlet_node_name="AHU-1 Supply Outlet Node",
    # ...
)
```

If the strings don't match, the loop is broken, and schema validation will not tell you. **Run `validate_document` and `check_topology` before simulating.**

## Common mistakes

!!! failure "editing a node-name string by hand"

    ```python
    coil._data["air_outlet_node_name"] = "AHU-1 Coil Out"
    # fan.air_inlet_node_name still says "AHU-1 Cooling Coil Outlet Node" — broken
    ```

!!! success "set both ends, then check the connection"

    ```python
    from idfkit.hvac import HVACTopology

    coil.air_outlet_node_name = "AHU-1 Coil Out"
    fan.air_inlet_node_name = "AHU-1 Coil Out"
    # Node names are strings, not references: both ends must change. Then confirm they meet:
    topo = HVACTopology.from_document(doc)
    assert [o.name for o in topo.consumers("AHU-1 Coil Out")] == [fan.name]
    ```

!!! failure "renaming a coil via `_data["name"]`"

    ```python
    coil._data["name"] = "New Coil Name"
    # Branch component still names "AHU-1 Cooling Coil" — broken
    ```

!!! success "set `.name`"

    ```python
    coil.name = "New Coil Name"
    # Every Branch.component_name that pointed at "AHU-1 Cooling Coil" updates.
    ```

!!! failure "assuming `validate_document` catches mismatched node-name strings"

    ```python
    # Node names are strings, not references — the schema validates type but not consistency.
    # A typo in a node name passes validation but breaks the loop.
    ```

!!! success "run the topology checks"

    ```python
    from idfkit.hvac import check_topology

    findings = check_topology(doc)  # T010/T011 branch mismatches, T030 inlets nothing supplies
    for finding in findings:
        print(finding.code, finding.severity, finding.message)
    assert not [f for f in findings if f.severity == "error"], "broken loop connections"
    ```

## Related

- [hvac-templates.md](hvac-templates.md) — start here unless you really need hand-authored loops.
- [hvac-topology.md](hvac-topology.md) — the node graph: who connects to a node, flow walks, connection checks.
- [reference-tracking.md](reference-tracking.md) — navigating and renaming the objects a loop references.
- [schema-and-validation.md](schema-and-validation.md) — `E004` errors are dangling node-name references.
- I/O Reference (via `idfkit-mcp` search_docs or the docs site): `AirLoopHVAC`, `PlantLoop`, `CondenserLoop`, `Branch`, `BranchList`, `Connector:Splitter`, `Connector:Mixer`, setpoint managers, controllers.
