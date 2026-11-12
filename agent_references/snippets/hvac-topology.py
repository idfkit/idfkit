from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.hvac import FlowEdge, HVACTopology, LoopMembership, NodeUse, TopologyFinding

doc: IDFDocument = ...  # type: ignore[assignment]
coil: IDFObject = ...  # type: ignore[assignment]
topo: HVACTopology = ...  # type: ignore[assignment]
use: NodeUse = ...  # type: ignore[assignment]
edge: FlowEdge = ...  # type: ignore[assignment]
finding: TopologyFinding = ...  # type: ignore[assignment]
membership: LoopMembership = ...  # type: ignore[assignment]
loop: IDFObject = ...  # type: ignore[assignment]
path: list[IDFObject] = ...  # type: ignore[assignment]

# --8<-- [start:build-view]
from idfkit import load_idf
from idfkit.hvac import HVACTopology

doc = load_idf("5ZoneAirCooled.idf")
topo = HVACTopology.from_document(doc)  # cached on the document until the next edit
print(len(topo.nodes()), "nodes")
# --8<-- [end:build-view]


# --8<-- [start:trace-node]
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
# --8<-- [end:trace-node]


# --8<-- [start:list-findings]
from idfkit.hvac import check_topology

for finding in check_topology(doc):
    print(finding.code, finding.severity, finding.message)
    if finding.expected is not None:
        print("  the other side says", finding.expected, "but this object says", finding.actual)

errors = [f for f in topo.check() if f.severity == "error"]
if errors:
    raise SystemExit("Fix the connection errors before simulating")
# A clean result does not mean the model simulates: run EnergyPlus to know that.
# --8<-- [end:list-findings]


# --8<-- [start:read-coverage]
from idfkit.hvac import UncoveredPart

coverage = topo.coverage
if coverage.partial:
    parts: tuple[UncoveredPart, ...] = coverage.uncovered
    for part in parts:
        # hvac_template, ems_program or unclassified_type, with up to 3 examples
        print(part.kind, part.count, part.reason, [k.name for k in part.examples])
# --8<-- [end:read-coverage]


# --8<-- [start:category-filter]
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
# --8<-- [end:category-filter]


# --8<-- [start:memberships]
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
# --8<-- [end:memberships]


# --8<-- [start:chain]
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
# --8<-- [end:chain]


# --8<-- [start:rename-node]
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
# --8<-- [end:rename-node]
