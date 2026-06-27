from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
branch: IDFObject = ...  # type: ignore[assignment]
comp: IDFObject = ...  # type: ignore[assignment]
bl: IDFObject = ...  # type: ignore[assignment]
branch_name: str = ...  # type: ignore[assignment]
splitter: IDFObject = ...  # type: ignore[assignment]
mixer: IDFObject = ...  # type: ignore[assignment]
coil: IDFObject = ...  # type: ignore[assignment]
fan: IDFObject = ...  # type: ignore[assignment]

# --8<-- [start:lint-before-simulate]
from idfkit import load_idf, validate_document

doc = load_idf("custom_loop.idf")
result = validate_document(doc)
if not result.is_valid:
    for err in result.errors:
        print(err)
    raise SystemExit("Refusing to simulate an invalid loop graph")
# --8<-- [end:lint-before-simulate]


# --8<-- [start:trace-referencing]
# Every object that mentions "AHU-1 Cooling Coil"
for obj in doc.get_referencing("AHU-1 Cooling Coil"):
    print(obj.obj_type, obj.name)
# Branch 'AHU-1 Cooling Branch'
# Controller:WaterCoil 'AHU-1 Cooling Coil Controller'
# SetpointManager:Scheduled 'AHU-1 Cooling Coil Setpoint'
# ...
# --8<-- [end:trace-referencing]


# --8<-- [start:safe-rename]
# Rename a coil. Every branch component, controller, setpoint manager
# that pointed at "AHU-1 Cooling Coil" now points at "AHU-1 Cooling Coil A".
doc["Coil:Cooling:Water"]["AHU-1 Cooling Coil"].name = "AHU-1 Cooling Coil A"
# --8<-- [end:safe-rename]


# --8<-- [start:branch-branchlist]
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
# --8<-- [end:branch-branchlist]


# --8<-- [start:splitter-mixer]
splitter = doc.add("Connector:Splitter", "CHW Loop Splitter")
splitter.inlet_branch_name = "CHW Loop Supply Inlet Branch"
splitter.branches.append(outlet_branch_name="Chiller 1 Branch")
splitter.branches.append(outlet_branch_name="Chiller 2 Branch")

mixer = doc.add("Connector:Mixer", "CHW Loop Mixer")
mixer.outlet_branch_name = "CHW Loop Supply Outlet Branch"
mixer.branches.append(inlet_branch_name="Chiller 1 Branch")
mixer.branches.append(inlet_branch_name="Chiller 2 Branch")
# --8<-- [end:splitter-mixer]


# --8<-- [start:link-node-names]
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
# --8<-- [end:link-node-names]


# --8<-- [start:mistake-node-good]
coil.air_outlet_node_name = "AHU-1 Coil Out"
fan.air_inlet_node_name = "AHU-1 Coil Out"
# Note: node names are strings, not references — both must be updated.
# --8<-- [end:mistake-node-good]


# --8<-- [start:mistake-rename-good]
coil.name = "New Coil Name"
# Every Branch.component_name that pointed at "AHU-1 Cooling Coil" updates.
# --8<-- [end:mistake-rename-good]


# --8<-- [start:mistake-walk-good]
# Sanity-check that every coil has a paired adjacent branch component
for coil in doc.get_collection("Coil:Cooling:Water"):
    inlet = coil.air_inlet_node_name
    outlet = coil.air_outlet_node_name
    upstream = [o for o in doc.all_objects if getattr(o, "air_outlet_node_name", None) == inlet]
    downstream = [o for o in doc.all_objects if getattr(o, "air_inlet_node_name", None) == outlet]
    assert upstream and downstream, f"Coil {coil.name} has dangling air nodes"
# --8<-- [end:mistake-walk-good]


# --8<-- [start:diagram]
from idfkit.visualization import HVACDiagramConfig, build_hvac_graph, hvac_to_mermaid

# Build a topology graph from an *expanded* document (no HVACTemplate:* objects).
# Raises HVACDiagramError if templates remain; pass expand=True to run
# ExpandObjects first (needs an EnergyPlus install).
graph = build_hvac_graph(doc)
print(f"{len(graph.loops)} loops, {len(graph.vertices)} components, {len(graph.edges)} links")
for warning in graph.warnings:
    print(warning.kind, warning.message)

# Render to Mermaid (paste into mermaid.live or a Markdown file), Graphviz DOT,
# or a plain JSON-serializable dict.
mermaid = graph.to_mermaid(HVACDiagramConfig(direction="LR"))
dot = graph.to_dot()
data = graph.to_dict()

# Convenience: go straight from a document, skipping the explicit graph.
mermaid = hvac_to_mermaid(doc)

# Large models (hundreds of components): filter to one loop, or collapse the
# whole building to a one-node-per-loop/zone overview.
one_loop = graph.subset(loop_names=["VAV_1"]).to_mermaid()
overview = graph.overview_mermaid()

# Zone equipment (fan coils, PTACs, VRF terminal units) is expanded into its
# internal OA-mixer/fan/coil train and grouped under the zone it serves — not
# dumped into a flat "Other equipment" box. A water coil shared with a plant loop
# keeps its plant membership; the air-only fan and mixer cluster with the zone.
for vertex in graph.vertices:
    if vertex.zone is not None:
        print(f"{vertex.obj_type} serves zone {vertex.zone}")

# Variable-refrigerant-flow systems couple their outdoor unit to each terminal
# unit through a refrigerant network (a named ZoneTerminalUnitList), not through
# air/water nodes — so those links are tracked separately and drawn dashed.
for ref in graph.refrigerant_edges:
    print(f"{ref.master_key} -> {ref.terminal_key}")
# --8<-- [end:diagram]
