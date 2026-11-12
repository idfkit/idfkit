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
# Every object that names "AHU-1 Cooling Coil" in a reference field
for obj in doc.get_referencing("AHU-1 Cooling Coil"):
    print(obj.obj_type, obj.name)
# Branch 'AHU-1 Cooling Branch'
# Controller:WaterCoil 'AHU-1 Cooling Coil Controller'
# Setpoint managers name nodes, not coils, so they are not listed here.
# --8<-- [end:trace-referencing]


# --8<-- [start:safe-rename]
# Rename a coil. Every branch component and controller that pointed at
# "AHU-1 Cooling Coil" now points at "AHU-1 Cooling Coil A". Node names are unchanged.
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
# Node names are plain strings: validate_document and get_referencing do not see them.
# Check that every air node a coil names also appears in another object, in any field,
# including Branch components, OutdoorAir:Mixer streams and NodeLists.
from collections.abc import Iterator
from typing import Any


def strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value.upper()
    elif isinstance(value, dict):
        for item in value.values():  # pyright: ignore[reportUnknownVariableType]
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:  # pyright: ignore[reportUnknownVariableType]
            yield from strings(item)


mentions: dict[str, list[IDFObject]] = {}
for obj in doc.all_objects:
    for text in set(strings(obj.to_dict())):
        mentions.setdefault(text, []).append(obj)

for coil in doc.get_collection("Coil:Cooling:Water"):
    for node in (coil.air_inlet_node_name, coil.air_outlet_node_name):
        others = [o for o in mentions.get(str(node).upper(), []) if o is not coil]
        assert others, f"Coil {coil.name}: no other object names node {node!r}"
# --8<-- [end:mistake-walk-good]
