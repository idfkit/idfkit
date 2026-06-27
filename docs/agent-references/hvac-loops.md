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
--8<-- "docs/snippets/agent_references/hvac-loops.py:lint-before-simulate"
```

`validate_document` with `check_references=True` (the default) reports every dangling node-name reference as an `E004` error. That's the single most useful smoke test before kicking off a simulation.

## Tracing a loop with `get_referencing`

```python
--8<-- "docs/snippets/agent_references/hvac-loops.py:trace-referencing"
```

If a branch or controller you expect to see isn't there, the wiring is wrong — fix it before simulating, not after.

## Safe renames

```python
--8<-- "docs/snippets/agent_references/hvac-loops.py:safe-rename"
```

This is the central reason idfkit is safer than text-editing IDFs: a rename through the reference graph is atomic and complete. Renaming via raw string substitution (e.g. `sed`) inevitably misses one of the dozens of fields that mention the name.

See [reference-tracking.md](reference-tracking.md) for the full rename machinery.

## Branch + BranchList walkthrough

The branch/branch-list graph is what most loop authoring boils down to. Use the reference graph to verify it.

```python
--8<-- "docs/snippets/agent_references/hvac-loops.py:branch-branchlist"
```

A loop with a missing branch-list entry simulates and produces silently wrong results. The reference-graph walk above catches it in seconds.

## Connector:Splitter / Connector:Mixer

Splitter/mixer pairs define the parallel paths in an air or water loop. Each names branches via extensible fields:

```python
--8<-- "docs/snippets/agent_references/hvac-loops.py:splitter-mixer"
```

Validation checks that every branch name in the splitter/mixer exists as a `Branch` object — typos surface as `E004`.

## Pattern: link by node names

EnergyPlus loops are wired by string-typed *node names*, not by object references. A coil declares `air_inlet_node_name` and `air_outlet_node_name`; the adjacent branch component declares the same node names on its own side. **idfkit's schema-driven validation enforces that node names are real strings, not that two objects share the right one.**

The safety net is `get_referencing` plus a final `validate_document` call. There's no idfkit feature that "wires" two nodes for you — that's still your responsibility.

```python
--8<-- "docs/snippets/agent_references/hvac-loops.py:link-node-names"
```

If the strings don't match exactly (case-sensitive), the loop is broken. EnergyPlus will only tell you at simulation time. **Always lint with `validate_document` and a `get_referencing` spot-check before simulating.**

## Common mistakes

!!! failure "editing a node-name string by hand"

    ```python
    coil._data["air_outlet_node_name"] = "AHU-1 Coil Out"
    # fan.air_inlet_node_name still says "AHU-1 Cooling Coil Outlet Node" — broken
    ```

!!! success "set both ends, or rename the coil"

    ```python
    --8<-- "docs/snippets/agent_references/hvac-loops.py:mistake-node-good"
    ```

!!! failure "renaming a coil via `_data["name"]`"

    ```python
    coil._data["name"] = "New Coil Name"
    # Branch component still names "AHU-1 Cooling Coil" — broken
    ```

!!! success "set `.name`"

    ```python
    --8<-- "docs/snippets/agent_references/hvac-loops.py:mistake-rename-good"
    ```

!!! failure "assuming `validate_document` catches mismatched node-name strings"

    ```python
    # Node names are strings, not references — the schema validates type but not consistency.
    # A typo in a node name passes validation but breaks the loop.
    ```

!!! success "also walk the graph manually for critical loops"

    ```python
    --8<-- "docs/snippets/agent_references/hvac-loops.py:mistake-walk-good"
    ```

## Diagram an HVAC system

Once a loop graph exists, `idfkit.visualization.build_hvac_graph` reconstructs its
topology — air, plant, and condenser loops, their supply/demand sides, branches,
splitters/mixers, zone equipment — directly from the IDF objects, with no
simulation run. It is the IDF-native analogue of the EnergyPlus HVAC-Diagram
utility (which reads the post-run `eplusout.bnd` file). Render the result to a
Mermaid flowchart, Graphviz DOT, or a JSON-serializable dict.

The document must be **expanded** first: `build_hvac_graph` raises
`HVACDiagramError` if `HVACTemplate:*` objects remain (pass `expand=True` to run
`ExpandObjects` first). Building never raises on odd topology — it records
`HVACWarning`s (dangling nodes, unconnected components) on the returned graph.

```python
--8<-- "docs/snippets/agent_references/hvac-loops.py:diagram"
```

Connectivity follows the same rule EnergyPlus uses: a component whose *outlet* is
node N feeds the component whose *inlet* is node N. A water coil that sits on both
an air supply branch and a plant demand branch becomes a single graph vertex with
both loop memberships.

Compound units are expanded rather than drawn as opaque boxes. An
`AirLoopHVAC:UnitarySystem` and a zone forced-air unit (`ZoneHVAC:FourPipeFanCoil`,
`ZoneHVAC:PackagedTerminalAirConditioner`, `ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`,
…) are each replaced by their internal OA-mixer/fan/coil train, so a packaged unit
reads as its sequence of components. Zone equipment groups under the zone it serves
instead of a flat "Other equipment" bin, and a VRF outdoor unit is linked to its
terminal units through the refrigerant network (`graph.refrigerant_edges`, drawn as
dashed `refrigerant` edges) since that coupling is a named terminal-unit list, not a
node connection. The expandable-container set is driven by the schema object group
(`"Zone HVAC Forced Air Units"`), so new zone unit types are picked up automatically.

## Related

- [hvac-templates.md](hvac-templates.md) — start here unless you really need hand-authored loops.
- [reference-tracking.md](reference-tracking.md) — the workhorse for navigating and renaming loop graphs.
- [schema-and-validation.md](schema-and-validation.md) — `E004` errors are dangling node-name references.
- I/O Reference (via `idfkit-mcp` search_docs or the docs site): `AirLoopHVAC`, `PlantLoop`, `CondenserLoop`, `Branch`, `BranchList`, `Connector:Splitter`, `Connector:Mixer`, setpoint managers, controllers.
