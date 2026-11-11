"""The HVAC topology view on real and minimal models: roles, flow, walks and caching.

Connection-check findings (T010, T011, T030, T090, T091) are tested with ``idfkit.hvac.checks``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import IDFDocument, load_idf, new_document
from idfkit.hvac import ComponentCategory, ConnectionType, Fluid, HVACTopology, ObjectKey

LINKED = Path(__file__).parent / "fixtures" / "simulation" / "linked"


@pytest.fixture
def five_zone() -> IDFDocument:
    return load_idf(str(LINKED / "5ZoneAirCooled.idf"))


def test_ports_carry_energyplus_roles_streams_and_fluids(five_zone: IDFDocument) -> None:
    coil = five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"]
    ports = HVACTopology.from_document(five_zone).ports(coil)
    roles = {(u.field, u.connection, u.stream, u.fluid) for u in ports}
    assert roles == {
        ("air_inlet_node_name", ConnectionType.INLET, 1, Fluid.AIR),
        ("air_outlet_node_name", ConnectionType.OUTLET, 1, Fluid.AIR),
        ("water_inlet_node_name", ConnectionType.INLET, 2, Fluid.WATER),
        ("water_outlet_node_name", ConnectionType.OUTLET, 2, Fluid.WATER),
    }
    assert [u.stream for u in ports] == sorted(u.stream for u in ports)
    assert {u.provenance for u in ports} == {"eplus_examples"}
    assert {u.category for u in ports} == {ComponentCategory.COOLING_COIL}


def test_node_lookup_is_case_insensitive_and_keeps_the_model_spelling(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    uses = topo.uses("mixed air node 1")
    assert uses
    assert {u.node for u in uses} == {"Mixed Air Node 1"}


def test_unknown_node_raises_key_error(five_zone: IDFDocument) -> None:
    with pytest.raises(KeyError, match="No node named"):
        HVACTopology.from_document(five_zone).uses("No Such Node")


def test_producers_and_consumers_skip_parent_uses(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    # The VAV terminal is a parent for its outlet: it repeats its reheat coil's outlet.
    assert [o.name for o in topo.producers("SPACE3-1 In Node")] == ["SPACE3-1 Zone Coil"]
    assert [o.obj_type for o in topo.consumers("SPACE3-1 In Node")] == ["ZoneHVAC:EquipmentConnections"]
    parents = [u for u in topo.uses("SPACE3-1 In Node") if u.is_parent]
    assert {u.object.object_type for u in parents} >= {"AirTerminal:SingleDuct:VAV:Reheat"}


def test_controls_are_sensor_setpoint_and_actuator_uses(five_zone: IDFDocument) -> None:
    controls = HVACTopology.from_document(five_zone).controls("VAV Sys 1 Outlet Node")
    assert {u.connection for u in controls} <= {ConnectionType.SENSOR, ConnectionType.SETPOINT, ConnectionType.ACTUATOR}
    assert ObjectKey("SetpointManager:Scheduled", "Supply Air Temp Manager 1") in {u.object for u in controls}


def test_downstream_follows_flow_through_coils_and_loop_crossings(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    coil = five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"]
    one_hop = topo.downstream(coil, hops=1)
    assert {(e.target.name, e.node) for e in one_hop} == {
        ("Main Heating Coil 1", "Main Cooling Coil 1 Outlet Node"),
        ("CW Demand Mixer", "Main Cooling Coil 1 Water Outlet Node"),
    }
    targets = {e.target.name for e in topo.downstream(coil, hops=3)}
    assert "Zone Supply Air Splitter 1" in targets  # through the air loop's supply-to-demand crossing


def test_upstream_reaches_zones_through_the_return_plenum(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    plenum = five_zone["AirLoopHVAC:ReturnPlenum"]["Return-Plenum-1"]
    zone_edges = [e for e in topo.upstream(plenum, hops=1) if e.kind == "zone"]
    assert {e.source for e in zone_edges} == {ObjectKey("Zone", f"SPACE{i}-1") for i in range(1, 6)}


def test_category_filter_keeps_matching_edges_but_walks_through_others(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    edges = topo.upstream("SPACE3-1 In Node", hops=6, categories={ComponentCategory.HEATING_COIL})
    assert {e.source.name for e in edges} == {"SPACE3-1 Zone Coil", "Main Heating Coil 1"}


def test_hops_bound_the_walk(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    coil = five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"]
    assert topo.downstream(coil, hops=0) == []
    assert len(topo.downstream(coil, hops=1)) < len(topo.downstream(coil, hops=2))
    with pytest.raises(ValueError, match="hops"):
        topo.downstream(coil, hops=-1)


def test_a_node_start_walks_the_edges_through_that_node(five_zone: IDFDocument) -> None:
    edges = HVACTopology.from_document(five_zone).downstream("Mixed Air Node 1", hops=1)
    assert {(e.source.name, e.target.name) for e in edges} == {("OA Mixing Box 1", "Main Cooling Coil 1")}


def test_an_outlet_typo_leaves_a_one_sided_node(five_zone: IDFDocument) -> None:
    coil = five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"]
    coil.air_outlet_node_name = "TYPO NODE"
    topo = HVACTopology.from_document(five_zone)
    assert [o.name for o in topo.producers("TYPO NODE")] == ["Main Cooling Coil 1"]
    assert topo.consumers("TYPO NODE") == []
    assert "Main Heating Coil 1" not in {e.target.name for e in topo.downstream(coil, hops=1)}


def test_the_view_is_cached_per_revision(five_zone: IDFDocument) -> None:
    first = HVACTopology.from_document(five_zone)
    assert HVACTopology.from_document(five_zone) is first
    five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"].air_outlet_node_name = "Renamed Outlet"
    second = HVACTopology.from_document(five_zone)
    assert second is not first
    assert "Renamed Outlet" in second.nodes()


def test_a_nodelist_field_resolves_to_the_list_first() -> None:
    doc = new_document()
    doc.add("NodeList", "Zone Inlets", nodes=[{"node_name": "Inlet A"}, {"node_name": "Inlet B"}], validate=False)
    doc.add(
        "ZoneHVAC:EquipmentConnections",
        zone_name="Office",
        zone_air_inlet_node_or_nodelist_name="Zone Inlets",
        zone_air_node_name="Office Air",
        validate=False,
    )
    topo = HVACTopology.from_document(doc)
    (use,) = topo.uses("Inlet B")
    assert use.connection is ConnectionType.ZONE_INLET
    assert use.via_nodelist == "Zone Inlets"
    assert use.object == ObjectKey("ZoneHVAC:EquipmentConnections", "Office")
    assert "Zone Inlets" not in topo.nodes()


@pytest.mark.parametrize(
    ("condenser_type", "expected"),
    [("AirCooled", ConnectionType.OUTSIDE_AIR), ("WaterCooled", ConnectionType.INLET), (None, ConnectionType.INLET)],
)
def test_value_predicates_choose_the_role(condenser_type: str | None, expected: ConnectionType) -> None:
    doc = new_document()
    fields: dict[str, str] = {"condenser_inlet_node_name": "Cond In", "condenser_outlet_node_name": "Cond Out"}
    if condenser_type is not None:
        fields["condenser_type"] = condenser_type
    doc.add("Chiller:Electric:EIR", "Chiller", validate=False, **fields)
    (use,) = HVACTopology.from_document(doc).uses("Cond In")
    assert use.connection is expected  # a blank condenser type takes the schema default, WaterCooled


def test_outdoor_air_nodes_are_boundaries(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    roles = {u.connection for u in topo.uses("Outside Air Inlet Node 1")}
    assert ConnectionType.OUTSIDE_AIR in roles
