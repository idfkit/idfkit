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


# --8<-- [start:verify-loop]
from idfkit.hvac import HVACTopology

topo = HVACTopology.from_document(doc)
# The coil should sit on the air loop's supply branch and on the chilled-water demand side.
for membership in topo.memberships(coil):
    print(membership.loop.name, membership.kind, membership.side, membership.position)
assert any(m.kind == "plant" and m.side == "demand" for m in topo.memberships(coil)), "coil not on a plant loop"

# Each supply branch in BranchList order, its components in listed order
air_loop = doc["AirLoopHVAC"]["AHU-1"]
for path in topo.chain(air_loop, "supply"):
    print([o.name for o in path])
print([z.name for z in topo.zones_served(air_loop)])
# --8<-- [end:verify-loop]


# --8<-- [start:mistake-node-good]
from idfkit.hvac import HVACTopology

# Rewrites the coil, the fan, the Branch, setpoint managers and NodeList entries in one step.
result = doc.rename_node("AHU-1 Cooling Coil Outlet Node", "AHU-1 Coil Out")
print(result.fields_updated, [key.name for key in result.objects])
topo = HVACTopology.from_document(doc)
assert [o.name for o in topo.consumers("AHU-1 Coil Out")] == [fan.name]
# --8<-- [end:mistake-node-good]


# --8<-- [start:mistake-rename-good]
coil.name = "New Coil Name"
# Every Branch.component_name that pointed at "AHU-1 Cooling Coil" updates.
# --8<-- [end:mistake-rename-good]


# --8<-- [start:mistake-walk-good]
from idfkit.hvac import check_topology

findings = check_topology(doc)  # T010/T011 branch mismatches, T001-T004 and T030 one-sided nodes
for finding in findings:
    print(finding.code, finding.severity, finding.message)
assert not [f for f in findings if f.severity == "error"], "broken loop connections"
# --8<-- [end:mistake-walk-good]
