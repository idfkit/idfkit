from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.hvac import FlowEdge, HVACTopology, NodeUse, TopologyFinding

doc: IDFDocument = ...  # type: ignore[assignment]
coil: IDFObject = ...  # type: ignore[assignment]
topo: HVACTopology = ...  # type: ignore[assignment]
use: NodeUse = ...  # type: ignore[assignment]
edge: FlowEdge = ...  # type: ignore[assignment]
finding: TopologyFinding = ...  # type: ignore[assignment]

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
coverage = topo.coverage
if coverage.partial:
    for part in coverage.uncovered:
        # hvac_template, ems_program or unclassified_type, with up to 3 examples
        print(part.kind, part.count, part.reason, [k.name for k in part.examples])
# --8<-- [end:read-coverage]


# --8<-- [start:category-filter]
from idfkit.hvac import ComponentCategory, Fluid

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
