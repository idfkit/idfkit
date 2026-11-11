"""The HVAC topology view on real and minimal models: roles, flow, walks and caching.

The second half covers the connection checks (T010, T011, T030, T090, T091).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import IDFDocument, load_idf, new_document
from idfkit.hvac import ComponentCategory, ConnectionType, Fluid, HVACTopology, ObjectKey, check_topology

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


@pytest.fixture
def dual_duct() -> IDFDocument:
    return load_idf(str(LINKED / "DOASDualDuctSchool.idf"))


def test_a_zone_start_walks_from_its_equipment_connections(dual_duct: IDFDocument) -> None:
    topo = HVACTopology.from_document(dual_duct)
    zone = dual_duct["Zone"]["Corridor_Pod_1"]
    down = {(e.source, e.target.object_type) for e in topo.downstream(zone, hops=1)}
    assert down == {
        (ObjectKey("Zone", "Corridor_Pod_1"), "AirLoopHVAC:ZoneMixer"),
        (ObjectKey("Zone", "Corridor_Pod_1"), "OutdoorAir:Mixer"),
    }
    heating = topo.upstream(zone, hops=4, categories={ComponentCategory.HEATING_COIL})
    assert {e.source.name for e in heating} == {"Corridor_Pod_1 Fan Coil Heat Coil", "DOAS_POD_1_OA_HeatC 1"}
    assert {u.field for u in topo.ports(zone)} >= {"zone_air_node_name"}


def test_a_flow_edge_zone_key_is_a_valid_start(dual_duct: IDFDocument) -> None:
    topo = HVACTopology.from_document(dual_duct)
    terminal = dual_duct["AirTerminal:DualDuct:VAV:OutdoorAir"]["Lobby Dual Duct Box Component"]
    (edge,) = [e for e in topo.downstream(terminal, hops=1) if e.kind == "zone"]
    assert edge.target.object_type == "Zone"
    zone = dual_duct["Zone"][edge.target.name]
    assert topo.upstream(zone, hops=1)


def test_an_object_with_no_connections_is_an_error_not_an_empty_walk(dual_duct: IDFDocument) -> None:
    topo = HVACTopology.from_document(dual_duct)
    material = next(iter(dual_duct["Material"]))
    with pytest.raises(KeyError, match="no HVAC connections"):
        topo.downstream(material)
    assert topo.ports(material) == []


def test_a_loop_crossing_is_found_from_the_supply_outlet_node(dual_duct: IDFDocument) -> None:
    topo = HVACTopology.from_document(dual_duct)
    loop = dual_duct["PlantLoop"]["CoolSys1"]
    assert loop.plant_side_outlet_node_name is not None
    (edge,) = topo.downstream(loop.plant_side_outlet_node_name, hops=1)
    assert edge.source == ObjectKey("Pipe:Adiabatic", "CoolSys1 Supply Outlet Pipe")
    assert edge.target == ObjectKey("Pipe:Adiabatic", "CoolSys1 Demand Inlet Pipe")
    assert edge.kind == "component"  # no splitter or mixer between the two pipes


def test_a_nodelist_start_walks_from_every_listed_node(dual_duct: IDFDocument) -> None:
    topo = HVACTopology.from_document(dual_duct)
    loop = dual_duct["AirLoopHVAC"]["DUALDUCT_OTHER"]
    assert loop.supply_side_outlet_node_names is not None
    edges = topo.downstream(loop.supply_side_outlet_node_names, hops=1)
    assert {e.target.name for e in edges} == {
        "DUALDUCT_OTHER Supply Air Splitter",
        "DUALDUCT_OTHER RC Supply Air Splitter",
    }
    with pytest.raises(KeyError, match="No node or NodeList"):
        topo.downstream("No Such Node", hops=1)


def test_branches_and_controls_report_the_fluid_of_the_node_they_sit_on(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    air = {u.object.object_type: u.fluid for u in topo.uses("Main Cooling Coil 1 Outlet Node")}
    assert air["Branch"] is Fluid.AIR  # the Branch rule's commonest observation is water
    for node, fluid in (("VAV Sys 1 Outlet Node", Fluid.AIR), ("HW Supply Outlet Node", Fluid.WATER)):
        (setpoint,) = [u for u in topo.controls(node) if u.object.object_type == "SetpointManager:Scheduled"]
        assert setpoint.fluid is fluid


PLANT_SOURCES = (ComponentCategory.BOILER, ComponentCategory.CHILLER)


def test_a_water_walk_from_a_coil_inlet_reaches_only_its_own_plant(dual_duct: IDFDocument) -> None:
    topo = HVACTopology.from_document(dual_duct)
    coil = dual_duct["Coil:Heating:Water"]["Corner_Class_1_Pod_1 Fan Coil Heat Coil"]
    inlet = coil.water_inlet_node_name
    assert inlet is not None
    edges = topo.upstream(inlet, hops=12, categories=PLANT_SOURCES, fluid=Fluid.WATER)
    assert {e.source.object_type for e in edges} == {"Boiler:HotWater"}
    assert all(e.fluid is Fluid.WATER for e in topo.upstream(inlet, hops=12, fluid=Fluid.WATER))


def test_a_fluid_filter_stops_the_walk_crossing_streams_at_a_coil(dual_duct: IDFDocument) -> None:
    topo = HVACTopology.from_document(dual_duct)
    coil = dual_duct["Coil:Heating:Water"]["Corner_Class_1_Pod_1 Fan Coil Heat Coil"]
    every = {e.source.object_type for e in topo.upstream(coil, hops=30, categories=PLANT_SOURCES)}
    assert "Chiller:Electric:EIR" in every  # the air stream leads to the cooling coil, then its plant
    water = topo.upstream(coil, hops=30, categories=PLANT_SOURCES, fluid=Fluid.WATER)
    assert {e.source.object_type for e in water} == {"Boiler:HotWater"}
    air = topo.upstream(coil, hops=3, fluid=Fluid.AIR)
    assert air and all(e.fluid is Fluid.AIR for e in air)


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
    doc.add("Chiller:Electric:EIR", "Chiller", dict(fields), validate=False)
    (use,) = HVACTopology.from_document(doc).uses("Cond In")
    assert use.connection is expected  # a blank condenser type takes the schema default, WaterCooled


def test_outdoor_air_nodes_are_boundaries(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    roles = {u.connection for u in topo.uses("Outside Air Inlet Node 1")}
    assert ConnectionType.OUTSIDE_AIR in roles


# --------------------------------------------------------------------------------------------- #
# Connection checks (T010, T011, T030, T090, T091)
# --------------------------------------------------------------------------------------------- #


def test_unmodified_model_has_no_connection_error_and_every_finding_names_its_rule(five_zone: IDFDocument) -> None:
    findings = check_topology(five_zone)
    assert [f for f in findings if f.severity == "error"] == []
    assert all(f.code.startswith("T0") for f in findings)


def test_outlet_typo_is_a_branch_mismatch_and_a_one_sided_node(five_zone: IDFDocument) -> None:
    five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"].air_outlet_node_name = "TYPO NODE"
    findings = check_topology(five_zone)

    (t010,) = [f for f in findings if f.code == "T010"]
    assert t010.severity == "error"
    assert t010.objects == (
        ObjectKey("Branch", "VAV Sys 1 Main Branch"),
        ObjectKey("Coil:Cooling:Water", "Main Cooling Coil 1"),
    )
    assert t010.field == "air_outlet_node_name"
    assert t010.expected == "Main Cooling Coil 1 Outlet Node"
    assert t010.actual == "TYPO NODE"
    assert t010.provenance == "eplus_examples"

    (t030,) = [f for f in findings if f.code == "T030" and f.node == "TYPO NODE"]
    assert t030.severity == "warning"
    assert t030.objects == (ObjectKey("Coil:Cooling:Water", "Main Cooling Coil 1"),)


def test_disconnected_consecutive_branch_components_are_t011(five_zone: IDFDocument) -> None:
    branch = five_zone["Branch"]["VAV Sys 1 Main Branch"]
    branch.components[2].component_inlet_node_name = "Somewhere Else"
    (t011,) = [f for f in check_topology(five_zone) if f.code == "T011"]
    assert t011.severity == "error"
    assert t011.objects[0] == ObjectKey("Branch", "VAV Sys 1 Main Branch")
    assert t011.expected == "Main Cooling Coil 1 Outlet Node"
    assert t011.actual == "Somewhere Else"


def test_boundaries_are_not_one_sided_nodes() -> None:
    doc = load_idf(str(LINKED / "5ZoneAirCooled.idf"))
    nodes = {f.node for f in check_topology(doc) if f.code == "T030"}
    # outdoor air inlet, mixer relief outlet and the air-cooled chiller's condenser outlet
    assert {"Outside Air Inlet Node 1", "Relief Air Outlet Node 1", "Central Chiller Condenser Outlet Node"}.isdisjoint(
        nodes
    )


def test_an_exhaust_fan_venting_outdoors_is_not_reported() -> None:
    doc = new_document()
    doc.add(
        "ZoneHVAC:EquipmentConnections",
        zone_name="Office",
        zone_air_exhaust_node_or_nodelist_name="Office Exhaust",
        zone_air_node_name="Office Air",
        validate=False,
    )
    doc.add(
        "Fan:ZoneExhaust",
        "Exhaust Fan",
        air_inlet_node_name="Office Exhaust",
        air_outlet_node_name="Outside",
        validate=False,
    )
    assert [f for f in check_topology(doc) if f.code == "T030"] == []


def test_an_inlet_nothing_supplies_is_t030() -> None:
    doc = new_document()
    doc.add(
        "Coil:Heating:Electric", "Heater", air_inlet_node_name="Nowhere", air_outlet_node_name="Out", validate=False
    )
    (t030,) = [f for f in check_topology(doc) if f.code == "T030"]
    assert t030.node == "Nowhere"
    assert t030.severity == "warning"


def test_templates_give_t091_and_no_missing_node_findings() -> None:
    doc = load_idf(str(LINKED / "HVACTemplate-5ZoneVAVWaterCooled.idf"))
    findings = check_topology(doc)
    assert [f.code for f in findings if f.code == "T091"] == ["T091"]
    assert next(f for f in findings if f.code == "T091").severity == "info"
    assert [f for f in findings if f.code == "T030"] == []


def test_a_type_without_rules_is_t090_info() -> None:
    doc = new_document(version=(8, 9, 0))
    doc.add(
        "AirTerminal:SingleDuct:Uncontrolled",
        "Diffuser",
        zone_supply_air_node_name="Office Inlet",
        validate=False,
    )
    topo = HVACTopology.from_document(doc)
    (t090,) = [f for f in topo.check() if f.code == "T090"]
    assert t090.severity == "info"
    assert t090.objects == (ObjectKey("AirTerminal:SingleDuct:Uncontrolled", "Diffuser"),)
    assert [p.kind for p in topo.coverage.uncovered] == ["unclassified_type"]
    (use,) = topo.uses("Office Inlet")
    assert use.connection is None
    assert use.provenance is None


def test_hand_written_rules_never_yield_an_error() -> None:
    from idfkit.hvac.checks import qualified_severity

    assert qualified_severity("T010", "hand_written") == "warning"
    assert qualified_severity("T010", "eplus_examples") == "error"


def test_the_check_result_is_cached_with_the_view(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    assert topo.check() == topo.check()
    assert check_topology(five_zone) == topo.check()


def test_version_caps_lower_errors_on_measured_earlier_versions(
    five_zone: IDFDocument, monkeypatch: pytest.MonkeyPatch
) -> None:
    import idfkit.hvac.checks as checks
    from idfkit.hvac._rule_types import VersionCap

    monkeypatch.setattr(checks, "MEASURED_VERSIONS", ((9, 6, 0), (23, 2, 0)))
    monkeypatch.setattr(checks, "VERSION_CAPS", (VersionCap("T010", (9, 6, 0), "warning", 400, 3),))
    error = checks.TopologyFinding("T010", "error", (ObjectKey("Branch", "B"),), "m", "eplus_examples")

    capped = checks.cap_severity(error, (9, 6, 0))
    assert (capped.severity, capped.capped_from) == ("warning", "error")
    assert capped.cap_reason is not None and "9.6.0" in capped.cap_reason
    assert checks.cap_severity(error, (8, 9, 0)).severity == "warning"  # older than measured: oldest row
    assert checks.cap_severity(error, (22, 1, 0)).severity == "warning"  # nearest at or below: 9.6
    assert checks.cap_severity(error, (23, 2, 0)) == error  # 23.2 measured clean for T010
    assert checks.cap_severity(error, (26, 2, 0)) == error  # 26.2 is never capped
