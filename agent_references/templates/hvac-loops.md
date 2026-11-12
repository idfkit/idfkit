# HVAC loops

When `HVACTemplate:*` isn't enough — custom controls, unusual topology, plant interactions templates can't express — you author `AirLoopHVAC`, `PlantLoop`, and `CondenserLoop` by hand. This is dozens of interconnected objects (branches, splitters, mixers, coils, fans, pumps, setpoint managers) wired by node names. **This reference is scoped to idfkit-specific machinery for surviving that complexity**, not to EnergyPlus engineering — see the EnergyPlus I/O Reference for what each object does.

## When to use

- HVACTemplate can't represent what you need (e.g. ground-source heat pump with a custom storage tank).
- You're retrofitting a model that already has hand-authored loops.
- You need to lint an existing loop graph before simulating.

If templates work, use them. They're simpler, faster to author, and idfkit has more support for them. See [hvac-templates.md](hvac-templates.md).

## Where idfkit helps

idfkit doesn't provide higher-level "build me an air loop" helpers — you author each `AirLoopHVAC`, `Branch`, `BranchList`, `Connector:Splitter`, `Connector:Mixer`, `Coil:Cooling:Water`, etc. through `doc.add()`. But once you've done that, idfkit gives you three things EnergyPlus alone doesn't:

1. **Schema validation catches object-name typos**. A branch, branch list or controller that names an object no one declares is an `E009` error before EnergyPlus runs. Node-name typos are not caught: node names are plain strings, not references (see [Pattern: link by node names](#pattern-link-by-node-names)).
2. **The reference graph tells you what names what**. `doc.get_referencing("AHU-1 Cooling Coil")` returns every object that names that coil in a reference field, such as branches and controllers. Setpoint managers name nodes, not coils, so they are not in it.
3. **Cascading renames work across the reference graph**. Rename a coil and every branch and controller that names it updates. Node names are not renamed with it.

## Canonical pattern: lint before simulate

```python
--8<-- "agent_references/snippets/hvac-loops.py:lint-before-simulate"
```

`validate_document` with `check_references=True` (the default) reports every dangling object-name reference, such as a branch naming a missing coil, as an `E009` error. It does not check node names: two objects that should share a node but spell it differently both pass. Run it before every simulation, and check node names separately (see [Common mistakes](#common-mistakes)).

## Tracing a loop with `get_referencing`

```python
--8<-- "agent_references/snippets/hvac-loops.py:trace-referencing"
```

If a branch or controller you expect to see isn't there, the wiring is wrong — fix it before simulating, not after.

## Safe renames

```python
--8<-- "agent_references/snippets/hvac-loops.py:safe-rename"
```

This is the central reason idfkit is safer than text-editing IDFs: a rename through the reference graph is atomic and complete. Renaming via raw string substitution (e.g. `sed`) inevitably misses one of the dozens of fields that mention the name.

See [reference-tracking.md](reference-tracking.md) for the full rename machinery.

## Branch + BranchList walkthrough

The branch/branch-list graph is what most loop authoring boils down to. Use the reference graph to verify it.

```python
--8<-- "agent_references/snippets/hvac-loops.py:branch-branchlist"
```

A loop with a missing branch-list entry simulates and produces silently wrong results. The reference-graph walk above catches it in seconds.

## Connector:Splitter / Connector:Mixer

Splitter/mixer pairs define the parallel paths in an air or water loop. Each names branches via extensible fields:

```python
--8<-- "agent_references/snippets/hvac-loops.py:splitter-mixer"
```

Validation checks that every branch name in the splitter/mixer exists as a `Branch` object — typos surface as `E009`.

## Pattern: link by node names

EnergyPlus loops are wired by string-typed *node names*, not by object references. A coil declares `air_inlet_node_name` and `air_outlet_node_name`; the adjacent branch component declares the same node names on its own side. **idfkit's schema-driven validation enforces that node names are real strings, not that two objects share the right one.**

Neither `validate_document` nor `get_referencing` sees node names, so neither is a safety net for node wiring: `validate_document` reports dangling object-name references (`E009`) only. There's no idfkit feature that "wires" two nodes for you — that's still your responsibility. Check node names with the node-mention walk in [Common mistakes](#common-mistakes).

```python
--8<-- "agent_references/snippets/hvac-loops.py:link-node-names"
```

EnergyPlus matches node names case-insensitively, but any other difference in spelling breaks the loop, and EnergyPlus will only tell you at simulation time. **Before simulating, run `validate_document` for object-name references and the node-mention walk in [Common mistakes](#common-mistakes) for node names.**

## Common mistakes

!!! failure "editing a node-name string by hand"

    ```python
    coil._data["air_outlet_node_name"] = "AHU-1 Coil Out"
    # fan.air_inlet_node_name still says "AHU-1 Cooling Coil Outlet Node" — broken
    ```

!!! success "set both ends"

    ```python
    --8<-- "agent_references/snippets/hvac-loops.py:mistake-node-good"
    ```

!!! failure "renaming a coil via `_data["name"]`"

    ```python
    coil._data["name"] = "New Coil Name"
    # Branch component still names "AHU-1 Cooling Coil" — broken
    ```

!!! success "set `.name`"

    ```python
    --8<-- "agent_references/snippets/hvac-loops.py:mistake-rename-good"
    ```

!!! failure "assuming `validate_document` catches mismatched node-name strings"

    ```python
    # Node names are strings, not references — the schema validates type but not consistency.
    # A typo in a node name passes validation but breaks the loop.
    ```

!!! success "also walk the graph manually for critical loops"

    ```python
    --8<-- "agent_references/snippets/hvac-loops.py:mistake-walk-good"
    ```

## Related

- [hvac-templates.md](hvac-templates.md) — start here unless you really need hand-authored loops.
- [reference-tracking.md](reference-tracking.md) — the workhorse for navigating and renaming loop graphs.
- [schema-and-validation.md](schema-and-validation.md) — `E009` errors are dangling object-name references; node-name typos produce none.
- I/O Reference (via `idfkit-mcp` search_docs or the docs site): `AirLoopHVAC`, `PlantLoop`, `CondenserLoop`, `Branch`, `BranchList`, `Connector:Splitter`, `Connector:Mixer`, setpoint managers, controllers.
