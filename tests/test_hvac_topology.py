"""The HVAC topology view on real and minimal models: roles, flow, walks and caching.

The second half covers the connection checks (T001-T004, T010-T013, T030, T090, T091) and the loop
queries (memberships, chain, zones served).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import IDFDocument, IDFObject, load_idf, new_document
from idfkit.hvac import (
    ComponentCategory,
    ConnectionType,
    Fluid,
    HVACTopology,
    LoopMembership,
    ObjectKey,
    check_topology,
)

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
# Connection checks (T001-T004, T010, T011, T030, T090, T091)
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


def test_templates_give_t091_and_no_missing_node_findings() -> None:
    doc = load_idf(str(LINKED / "HVACTemplate-5ZoneVAVWaterCooled.idf"))
    findings = check_topology(doc)
    assert [f.code for f in findings if f.code == "T091"] == ["T091"]
    assert next(f for f in findings if f.code == "T091").severity == "info"
    assert [f for f in findings if f.code in {"T001", "T002", "T003", "T004", "T030"}] == []


def _without(obj: IDFObject, wrapper: str, key: str, name: str) -> list[dict[str, object]]:
    return [dict(i) for i in obj.extensible_items(wrapper) if str(i.get(key, "")).upper() != name.upper()]


def test_unmodified_model_has_no_branch_list_or_plant_side_finding(five_zone: IDFDocument) -> None:
    assert [f for f in check_topology(five_zone) if f.code in {"T012", "T013"}] == []


def test_branch_a_splitter_names_but_the_branch_list_omits_is_t012(five_zone: IDFDocument) -> None:
    branch_list = five_zone["BranchList"]["Heating Demand Side Branches"]
    branch_list["branches"] = _without(branch_list, "branches", "branch_name", "SPACE1-1 Reheat Branch")
    (t012,) = [f for f in check_topology(five_zone) if f.code == "T012"]
    assert t012.severity == "warning"
    assert t012.expected == "SPACE1-1 Reheat Branch"
    assert ObjectKey("BranchList", "Heating Demand Side Branches") in t012.objects
    assert ObjectKey("Branch", "SPACE1-1 Reheat Branch") in t012.objects
    assert "Heating Demand Splitter" in t012.message


def test_listed_branch_no_splitter_feeds_is_t012(five_zone: IDFDocument) -> None:
    splitter = five_zone["Connector:Splitter"]["Heating Demand Splitter"]
    mixer = five_zone["Connector:Mixer"]["Heating Demand Mixer"]
    splitter["branches"] = _without(splitter, "branches", "outlet_branch_name", "SPACE2-1 Reheat Branch")
    mixer["branches"] = _without(mixer, "branches", "inlet_branch_name", "SPACE2-1 Reheat Branch")
    (t012,) = [f for f in check_topology(five_zone) if f.code == "T012"]
    assert t012.actual == "SPACE2-1 Reheat Branch"
    assert "no splitter on that side feeds it" in t012.message


def test_water_coil_on_the_plant_supply_side_is_t013(five_zone: IDFDocument) -> None:
    branch = "Cooling Coil Branch"
    d_list = five_zone["BranchList"]["Cooling Demand Side Branches"]
    s_list = five_zone["BranchList"]["Cooling Supply Side Branches"]
    d_list["branches"] = _without(d_list, "branches", "branch_name", branch)
    s_items = [dict(i) for i in s_list.extensible_items("branches")]
    s_list["branches"] = [*s_items[:-1], {"branch_name": branch}, s_items[-1]]
    t013 = [f for f in check_topology(five_zone) if f.code == "T013"]
    assert [(f.objects[0], f.actual, f.expected, f.severity) for f in t013] == [
        (ObjectKey("Coil:Cooling:Water", "Main Cooling Coil 1"), "supply", "demand", "warning")
    ]


def test_boiler_on_the_plant_demand_side_is_t013(five_zone: IDFDocument) -> None:
    branch = "Central Boiler Branch"
    s_list = five_zone["BranchList"]["Heating Supply Side Branches"]
    d_list = five_zone["BranchList"]["Heating Demand Side Branches"]
    s_list["branches"] = _without(s_list, "branches", "branch_name", branch)
    d_items = [dict(i) for i in d_list.extensible_items("branches")]
    d_list["branches"] = [*d_items[:-1], {"branch_name": branch}, d_items[-1]]
    t013 = [f for f in check_topology(five_zone) if f.code == "T013"]
    assert [(f.objects[0].object_type, f.actual, f.expected) for f in t013] == [("Boiler:HotWater", "demand", "supply")]


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


def test_a_held_view_refuses_to_check_a_document_that_changed(five_zone: IDFDocument) -> None:
    checked = HVACTopology.from_document(five_zone)
    findings = checked.check()
    held = HVACTopology(five_zone)
    five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"].air_outlet_node_name = "TYPO NODE"
    with pytest.raises(RuntimeError, match="from_document"):
        held.check()
    assert checked.check() == findings  # computed before the edit: one revision, still returned
    assert any(f.code == "T010" for f in HVACTopology.from_document(five_zone).check())


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


# --------------------------------------------------------------------------------------------- #
# Loop membership, loops, chains and zones served
# --------------------------------------------------------------------------------------------- #


def test_a_water_coil_sits_on_its_air_loop_supply_and_its_plant_demand(five_zone: IDFDocument) -> None:
    coil = five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"]
    assert HVACTopology.from_document(five_zone).memberships(coil) == [
        LoopMembership(
            loop=ObjectKey("AirLoopHVAC", "VAV Sys 1"),
            kind="air",
            side="supply",
            branch=ObjectKey("Branch", "VAV Sys 1 Main Branch"),
            position=1,
            stream=1,
        ),
        LoopMembership(
            loop=ObjectKey("PlantLoop", "Chilled Water Loop"),
            kind="plant",
            side="demand",
            branch=ObjectKey("Branch", "Cooling Coil Branch"),
            position=0,
            stream=2,
        ),
    ]


def test_a_reheat_coil_sits_on_the_air_loop_demand_side_off_any_branch(five_zone: IDFDocument) -> None:
    coil = five_zone["Coil:Heating:Water"]["SPACE1-1 Zone Coil"]
    assert HVACTopology.from_document(five_zone).memberships(coil) == [
        LoopMembership(ObjectKey("AirLoopHVAC", "VAV Sys 1"), "air", "demand", None, None, 1),
        LoopMembership(
            ObjectKey("PlantLoop", "Hot Water Loop"),
            "plant",
            "demand",
            ObjectKey("Branch", "SPACE1-1 Reheat Branch"),
            0,
            2,
        ),
    ]


def test_an_air_cooled_chiller_sits_only_on_its_chilled_water_supply(five_zone: IDFDocument) -> None:
    chiller = five_zone["Chiller:Electric"]["Central Chiller"]
    assert HVACTopology.from_document(five_zone).memberships(chiller) == [
        LoopMembership(
            ObjectKey("PlantLoop", "Chilled Water Loop"),
            "plant",
            "supply",
            ObjectKey("Branch", "Central Chiller Branch"),
            0,
            1,
        ),
    ]


def test_air_loop_demand_components_have_no_branch(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    demand = LoopMembership(ObjectKey("AirLoopHVAC", "VAV Sys 1"), "air", "demand", None, None, 1)
    for obj in (
        five_zone["AirLoopHVAC:ZoneSplitter"]["Zone Supply Air Splitter 1"],
        five_zone["AirLoopHVAC:ReturnPlenum"]["Return-Plenum-1"],
        five_zone["AirTerminal:SingleDuct:VAV:Reheat"]["SPACE1-1 VAV Reheat"],
        five_zone["ZoneHVAC:AirDistributionUnit"]["SPACE1-1 ATU"],
    ):
        assert demand in topo.memberships(obj), obj.name


def test_listed_zone_equipment_belongs_to_its_equipment_connections(five_zone: IDFDocument) -> None:
    adu = five_zone["ZoneHVAC:AirDistributionUnit"]["SPACE1-1 ATU"]
    (zone_eq,) = [m for m in HVACTopology.from_document(five_zone).memberships(adu) if m.kind == "zone_equipment"]
    assert zone_eq.loop == ObjectKey("ZoneHVAC:EquipmentConnections", "SPACE1-1")
    assert (zone_eq.side, zone_eq.branch, zone_eq.position) == (None, None, None)


def test_a_component_on_no_loop_has_no_memberships() -> None:
    doc = new_document()
    doc.add("Fan:ConstantVolume", "Loose Fan", air_inlet_node_name="A", air_outlet_node_name="B", validate=False)
    assert HVACTopology.from_document(doc).memberships(doc["Fan:ConstantVolume"]["Loose Fan"]) == []


def test_memberships_are_stable_across_calls(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    coil = five_zone["Coil:Heating:Water"]["Main Heating Coil 1"]
    first = topo.memberships(coil)
    assert first
    assert topo.memberships(coil) == first


def test_loops_lists_every_air_plant_and_condenser_loop(five_zone: IDFDocument) -> None:
    loops = HVACTopology.from_document(five_zone).loops()
    assert {(o.obj_type, o.name) for o in loops} == {
        ("AirLoopHVAC", "VAV Sys 1"),
        ("PlantLoop", "Hot Water Loop"),
        ("PlantLoop", "Chilled Water Loop"),
    }
    assert loops[0].obj_type == "AirLoopHVAC"


def test_a_plant_chain_is_one_list_per_branch_in_branch_list_order(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    loop = five_zone["PlantLoop"]["Chilled Water Loop"]
    supply = [[o.name for o in branch] for branch in topo.chain(loop, "supply")]
    assert supply == [["CW Circ Pump"], ["Central Chiller"], ["Supply Side Bypass"], ["Supply Side Outlet Pipe"]]
    demand = [[o.name for o in branch] for branch in topo.chain(loop, "demand")]
    assert demand == [
        ["Cooling Demand Side Inlet Pipe"],
        ["Main Cooling Coil 1"],
        ["OA Cooling Coil 1"],
        ["Cooling Demand Side Bypass"],
        ["CW Demand Side Outlet Pipe"],
    ]


def test_an_air_loop_supply_chain_lists_its_branch_components_in_order(five_zone: IDFDocument) -> None:
    loop = five_zone["AirLoopHVAC"]["VAV Sys 1"]
    (branch,) = HVACTopology.from_document(five_zone).chain(loop, "supply")
    assert [o.name for o in branch] == ["OA Sys 1", "Main Cooling Coil 1", "Main Heating Coil 1", "Supply Fan 1"]


def test_an_air_loop_demand_chain_is_one_path_per_zone_then_the_return(five_zone: IDFDocument) -> None:
    loop = five_zone["AirLoopHVAC"]["VAV Sys 1"]
    *supply, back = HVACTopology.from_document(five_zone).chain(loop, "demand")
    assert len(supply) == 5
    assert all(path[0].obj_type == "AirLoopHVAC:ZoneSplitter" for path in supply)
    assert [[o.obj_type for o in path[1:]] for path in supply] == [
        ["AirTerminal:SingleDuct:VAV:Reheat", "Coil:Heating:Water"]
    ] * 5
    assert [o.name for o in back] == ["Return-Plenum-1"]


def test_chain_rejects_an_unknown_side_and_a_non_loop(five_zone: IDFDocument) -> None:
    topo = HVACTopology.from_document(five_zone)
    with pytest.raises(ValueError, match="side"):
        topo.chain(five_zone["PlantLoop"]["Hot Water Loop"], "middle")  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        topo.chain(five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"], "supply")


def test_zones_served_are_the_supplied_zones_not_the_return_plenum(five_zone: IDFDocument) -> None:
    served = HVACTopology.from_document(five_zone).zones_served(five_zone["AirLoopHVAC"]["VAV Sys 1"])
    assert {o.name for o in served} == {f"SPACE{i}-1" for i in range(1, 6)}
    assert all(o.obj_type == "Zone" for o in served)


def test_a_dual_duct_loop_serves_zones(dual_duct: IDFDocument) -> None:
    served = HVACTopology.from_document(dual_duct).zones_served(dual_duct["AirLoopHVAC"]["DUALDUCT_OTHER"])
    assert served
    assert all(o.obj_type == "Zone" for o in served)


# --------------------------------------------------------------------------------------------- #
# Dangling-node checks (T001, T002, T003, T004)
# --------------------------------------------------------------------------------------------- #

DANGLING = {"T001", "T002", "T003", "T004"}


def _zone_with_inlet(doc: IDFDocument, inlet: str) -> None:
    doc.add(
        "ZoneHVAC:EquipmentConnections",
        zone_name="Office",
        zone_air_inlet_node_or_nodelist_name=inlet,
        zone_air_node_name="Office Air",
        validate=False,
    )


def _heater(doc: IDFDocument, inlet: str) -> None:
    doc.add(
        "Coil:Heating:Electric", "Heater", air_inlet_node_name=inlet, air_outlet_node_name="Heater Out", validate=False
    )
    _zone_with_inlet(doc, "Heater Out")


def test_a_component_inlet_nothing_supplies_is_t001() -> None:
    doc = new_document()
    _heater(doc, "Nowhere")
    (t001,) = [f for f in check_topology(doc) if f.code == "T001"]
    assert t001.node == "Nowhere"
    assert t001.objects == (ObjectKey("Coil:Heating:Electric", "Heater"),)
    assert t001.severity == "warning"


def test_a_dangling_component_inlet_is_not_also_t030() -> None:
    doc = new_document()
    _heater(doc, "Nowhere")
    assert [f for f in check_topology(doc) if f.code == "T030"] == []


def test_a_zone_inlet_nothing_supplies_is_t002() -> None:
    doc = new_document()
    _zone_with_inlet(doc, "Office Inlet")
    findings = check_topology(doc)
    (t002,) = [f for f in findings if f.code == "T002"]
    assert t002.node == "Office Inlet"
    assert t002.severity == "warning"
    assert [f for f in findings if f.code in {"T001", "T030"}] == []


def test_a_zone_exhaust_nothing_draws_from_is_t003() -> None:
    doc = new_document()
    doc.add(
        "ZoneHVAC:EquipmentConnections",
        zone_name="Office",
        zone_air_exhaust_node_or_nodelist_name="Office Exhaust",
        zone_air_node_name="Office Air",
        validate=False,
    )
    (t003,) = [f for f in check_topology(doc) if f.code == "T003"]
    assert t003.node == "Office Exhaust"
    assert t003.severity == "warning"


def test_a_node_only_a_setpoint_manager_names_is_t004() -> None:
    doc = new_document()
    doc.add(
        "SetpointManager:Scheduled",
        "Lonely Manager",
        control_variable="Temperature",
        schedule_name="Always",
        setpoint_node_or_nodelist_name="Lonely Node",
        validate=False,
    )
    (t004,) = [f for f in check_topology(doc) if f.code == "T004"]
    assert t004.node == "Lonely Node"
    assert t004.objects == (ObjectKey("SetpointManager:Scheduled", "Lonely Manager"),)
    assert t004.severity == "warning"


def test_an_outdoor_air_node_inlet_is_not_t001() -> None:
    doc = new_document()
    doc.add("OutdoorAir:Node", "OA In", validate=False)
    _heater(doc, "OA In")
    assert [f for f in check_topology(doc) if f.code == "T001"] == []


def test_an_outdoor_air_nodelist_inlet_is_not_t001() -> None:
    doc = new_document()
    doc.add("OutdoorAir:NodeList", nodes=[{"node_or_nodelist_name": "OA In"}], validate=False)
    _heater(doc, "OA In")
    assert [f for f in check_topology(doc) if f.code == "T001"] == []


def test_a_loop_inlet_node_is_not_t001() -> None:
    doc = new_document()
    doc.add(
        "AirLoopHVAC",
        "Sys",
        supply_side_inlet_node_name="Sys In",
        supply_side_outlet_node_names="Heater Out",
        validate=False,
    )
    _heater(doc, "Sys In")
    assert [f for f in check_topology(doc) if f.code == "T001"] == []


def test_unmodified_models_have_no_dangling_nodes(five_zone: IDFDocument, dual_duct: IDFDocument) -> None:
    for doc in (five_zone, dual_duct):
        assert [f for f in HVACTopology.from_document(doc).check() if f.code in DANGLING] == []
