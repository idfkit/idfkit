"""Tests for the HVAC diagram builder and renderers (idfkit.visualization.hvac)."""

from __future__ import annotations

import json

import pytest

from idfkit import new_document
from idfkit.document import IDFDocument
from idfkit.exceptions import HVACDiagramError
from idfkit.visualization import (
    HVACDiagramConfig,
    HVACGraph,
    build_hvac_graph,
    hvac_to_dot,
    hvac_to_mermaid,
)

V = (24, 1, 0)


def _vkey(obj_type: str, name: str) -> str:
    return f"{obj_type.upper()}::{name.upper()}"


def _branch(doc: IDFDocument, name: str, ct: str, cn: str, inn: str, outn: str) -> None:
    doc.add(
        "Branch",
        name,
        {
            "components": [
                {
                    "component_object_type": ct,
                    "component_name": cn,
                    "component_inlet_node_name": inn,
                    "component_outlet_node_name": outn,
                }
            ]
        },
        validate=False,
    )


def _air_and_plant_model() -> IDFDocument:
    """A single-zone DOAS air loop coupled to a chilled-water plant loop.

    Exercises: an outdoor-air mixer, a water cooling coil shared between the air
    supply branch and the plant demand branch (dual-loop), supply/return zone
    splitter/mixer, a zone terminal via an air distribution unit, and plant-side
    Connector:Splitter/Mixer parallel branches.
    """
    doc = new_document(V)
    doc.add("Zone", "Zone1", validate=False)

    # --- Air loop -------------------------------------------------------
    doc.add(
        "AirLoopHVAC",
        "DOAS",
        {
            "branch_list_name": "DOAS Supply Branches",
            "supply_side_inlet_node_name": "DOAS Supply Inlet Node",
            "supply_side_outlet_node_names": "DOAS Supply Outlet Node",
            "demand_side_inlet_node_names": "DOAS Demand Inlet Node",
            "demand_side_outlet_node_name": "DOAS Demand Outlet Node",
        },
        validate=False,
    )
    doc.add("BranchList", "DOAS Supply Branches", {"branches": [{"branch_name": "DOAS Supply Branch"}]}, validate=False)
    doc.add(
        "Branch",
        "DOAS Supply Branch",
        {
            "components": [
                {
                    "component_object_type": "AirLoopHVAC:OutdoorAirSystem",
                    "component_name": "DOAS OA System",
                    "component_inlet_node_name": "DOAS Supply Inlet Node",
                    "component_outlet_node_name": "DOAS Mixed Air Node",
                },
                {
                    "component_object_type": "Coil:Cooling:Water",
                    "component_name": "DOAS Cooling Coil",
                    "component_inlet_node_name": "DOAS Mixed Air Node",
                    "component_outlet_node_name": "DOAS Coil Outlet Node",
                },
                {
                    "component_object_type": "Fan:VariableVolume",
                    "component_name": "DOAS Supply Fan",
                    "component_inlet_node_name": "DOAS Coil Outlet Node",
                    "component_outlet_node_name": "DOAS Supply Outlet Node",
                },
            ]
        },
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:OutdoorAirSystem",
        "DOAS OA System",
        {"outdoor_air_equipment_list_name": "DOAS OA Equipment"},
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:OutdoorAirSystem:EquipmentList",
        "DOAS OA Equipment",
        {"component_1_object_type": "OutdoorAir:Mixer", "component_1_name": "DOAS OA Mixer"},
        validate=False,
    )
    doc.add(
        "OutdoorAir:Mixer",
        "DOAS OA Mixer",
        {
            "mixed_air_node_name": "DOAS Mixed Air Node",
            "outdoor_air_stream_node_name": "DOAS OA Inlet Node",
            "relief_air_stream_node_name": "DOAS Relief Node",
            "return_air_stream_node_name": "DOAS Supply Inlet Node",
        },
        validate=False,
    )
    doc.add(
        "Coil:Cooling:Water",
        "DOAS Cooling Coil",
        {
            "air_inlet_node_name": "DOAS Mixed Air Node",
            "air_outlet_node_name": "DOAS Coil Outlet Node",
            "water_inlet_node_name": "CHW Coil Inlet Node",
            "water_outlet_node_name": "CHW Coil Outlet Node",
        },
        validate=False,
    )
    doc.add(
        "Fan:VariableVolume",
        "DOAS Supply Fan",
        {"air_inlet_node_name": "DOAS Coil Outlet Node", "air_outlet_node_name": "DOAS Supply Outlet Node"},
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:SupplyPath",
        "DOAS Supply Path",
        {
            "supply_air_path_inlet_node_name": "DOAS Demand Inlet Node",
            "components": [
                {"component_object_type": "AirLoopHVAC:ZoneSplitter", "component_name": "DOAS Zone Splitter"}
            ],
        },
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:ZoneSplitter",
        "DOAS Zone Splitter",
        {"inlet_node_name": "DOAS Demand Inlet Node", "nodes": [{"outlet_node_name": "Zone1 Supply Node"}]},
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:ReturnPath",
        "DOAS Return Path",
        {
            "return_air_path_outlet_node_name": "DOAS Demand Outlet Node",
            "components": [{"component_object_type": "AirLoopHVAC:ZoneMixer", "component_name": "DOAS Zone Mixer"}],
        },
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:ZoneMixer",
        "DOAS Zone Mixer",
        {"outlet_node_name": "DOAS Demand Outlet Node", "nodes": [{"inlet_node_name": "Zone1 Return Node"}]},
        validate=False,
    )
    doc.add(
        "ZoneHVAC:EquipmentConnections",
        fields={
            "zone_name": "Zone1",
            "zone_conditioning_equipment_list_name": "Zone1 Equipment",
            "zone_air_node_name": "Zone1 Air Node",
            "zone_air_inlet_node_or_nodelist_name": "Zone1 Inlet Node",
            "zone_return_air_node_or_nodelist_name": "Zone1 Return Node",
        },
        validate=False,
    )
    doc.add(
        "ZoneHVAC:EquipmentList",
        "Zone1 Equipment",
        {
            "equipment": [
                {"zone_equipment_object_type": "ZoneHVAC:AirDistributionUnit", "zone_equipment_name": "Zone1 ADU"}
            ]
        },
        validate=False,
    )
    doc.add(
        "ZoneHVAC:AirDistributionUnit",
        "Zone1 ADU",
        {
            "air_distribution_unit_outlet_node_name": "Zone1 Inlet Node",
            "air_terminal_object_type": "AirTerminal:SingleDuct:ConstantVolume:NoReheat",
            "air_terminal_name": "Zone1 Terminal",
        },
        validate=False,
    )
    doc.add(
        "AirTerminal:SingleDuct:ConstantVolume:NoReheat",
        "Zone1 Terminal",
        {"air_inlet_node_name": "Zone1 Supply Node", "air_outlet_node_name": "Zone1 Inlet Node"},
        validate=False,
    )

    # --- Plant loop -----------------------------------------------------
    doc.add(
        "PlantLoop",
        "CHW Loop",
        {
            "plant_side_inlet_node_name": "CHW Supply Inlet Node",
            "plant_side_outlet_node_name": "CHW Supply Outlet Node",
            "plant_side_branch_list_name": "CHW Supply Branches",
            "plant_side_connector_list_name": "CHW Supply Connectors",
            "demand_side_inlet_node_name": "CHW Demand Inlet Node",
            "demand_side_outlet_node_name": "CHW Demand Outlet Node",
            "demand_side_branch_list_name": "CHW Demand Branches",
            "demand_side_connector_list_name": "CHW Demand Connectors",
        },
        validate=False,
    )
    _branch(
        doc,
        "CHW Supply Inlet Branch",
        "Pump:VariableSpeed",
        "CHW Pump",
        "CHW Supply Inlet Node",
        "CHW Pump Outlet Node",
    )
    _branch(
        doc,
        "CHW Chiller Branch",
        "Chiller:Electric:EIR",
        "CHW Chiller",
        "CHW Chiller Inlet Node",
        "CHW Chiller Outlet Node",
    )
    _branch(
        doc,
        "CHW Supply Bypass Branch",
        "Pipe:Adiabatic",
        "CHW Supply Bypass",
        "CHW Bypass Inlet Node",
        "CHW Bypass Outlet Node",
    )
    _branch(
        doc,
        "CHW Supply Outlet Branch",
        "Pipe:Adiabatic",
        "CHW Supply Outlet Pipe",
        "CHW Supply Outlet Pipe Inlet",
        "CHW Supply Outlet Node",
    )
    doc.add(
        "BranchList",
        "CHW Supply Branches",
        {
            "branches": [
                {"branch_name": "CHW Supply Inlet Branch"},
                {"branch_name": "CHW Chiller Branch"},
                {"branch_name": "CHW Supply Bypass Branch"},
                {"branch_name": "CHW Supply Outlet Branch"},
            ]
        },
        validate=False,
    )
    doc.add(
        "ConnectorList",
        "CHW Supply Connectors",
        {
            "connector_1_object_type": "Connector:Splitter",
            "connector_1_name": "CHW Supply Splitter",
            "connector_2_object_type": "Connector:Mixer",
            "connector_2_name": "CHW Supply Mixer",
        },
        validate=False,
    )
    doc.add(
        "Connector:Splitter",
        "CHW Supply Splitter",
        {
            "inlet_branch_name": "CHW Supply Inlet Branch",
            "branches": [
                {"outlet_branch_name": "CHW Chiller Branch"},
                {"outlet_branch_name": "CHW Supply Bypass Branch"},
            ],
        },
        validate=False,
    )
    doc.add(
        "Connector:Mixer",
        "CHW Supply Mixer",
        {
            "outlet_branch_name": "CHW Supply Outlet Branch",
            "branches": [
                {"inlet_branch_name": "CHW Chiller Branch"},
                {"inlet_branch_name": "CHW Supply Bypass Branch"},
            ],
        },
        validate=False,
    )
    doc.add(
        "Pump:VariableSpeed",
        "CHW Pump",
        {"inlet_node_name": "CHW Supply Inlet Node", "outlet_node_name": "CHW Pump Outlet Node"},
        validate=False,
    )
    doc.add(
        "Chiller:Electric:EIR",
        "CHW Chiller",
        {
            "chilled_water_inlet_node_name": "CHW Chiller Inlet Node",
            "chilled_water_outlet_node_name": "CHW Chiller Outlet Node",
            "condenser_type": "AirCooled",
        },
        validate=False,
    )
    doc.add(
        "Pipe:Adiabatic",
        "CHW Supply Bypass",
        {"inlet_node_name": "CHW Bypass Inlet Node", "outlet_node_name": "CHW Bypass Outlet Node"},
        validate=False,
    )
    doc.add(
        "Pipe:Adiabatic",
        "CHW Supply Outlet Pipe",
        {"inlet_node_name": "CHW Supply Outlet Pipe Inlet", "outlet_node_name": "CHW Supply Outlet Node"},
        validate=False,
    )

    _branch(
        doc,
        "CHW Demand Inlet Branch",
        "Pipe:Adiabatic",
        "CHW Demand Inlet Pipe",
        "CHW Demand Inlet Node",
        "CHW Demand Splitter Inlet",
    )
    _branch(
        doc, "CHW Coil Branch", "Coil:Cooling:Water", "DOAS Cooling Coil", "CHW Coil Inlet Node", "CHW Coil Outlet Node"
    )
    _branch(
        doc,
        "CHW Demand Bypass Branch",
        "Pipe:Adiabatic",
        "CHW Demand Bypass",
        "CHW Demand Bypass Inlet",
        "CHW Demand Bypass Outlet",
    )
    _branch(
        doc,
        "CHW Demand Outlet Branch",
        "Pipe:Adiabatic",
        "CHW Demand Outlet Pipe",
        "CHW Demand Mixer Outlet",
        "CHW Demand Outlet Node",
    )
    doc.add(
        "BranchList",
        "CHW Demand Branches",
        {
            "branches": [
                {"branch_name": "CHW Demand Inlet Branch"},
                {"branch_name": "CHW Coil Branch"},
                {"branch_name": "CHW Demand Bypass Branch"},
                {"branch_name": "CHW Demand Outlet Branch"},
            ]
        },
        validate=False,
    )
    doc.add(
        "ConnectorList",
        "CHW Demand Connectors",
        {
            "connector_1_object_type": "Connector:Splitter",
            "connector_1_name": "CHW Demand Splitter",
            "connector_2_object_type": "Connector:Mixer",
            "connector_2_name": "CHW Demand Mixer",
        },
        validate=False,
    )
    doc.add(
        "Connector:Splitter",
        "CHW Demand Splitter",
        {
            "inlet_branch_name": "CHW Demand Inlet Branch",
            "branches": [{"outlet_branch_name": "CHW Coil Branch"}, {"outlet_branch_name": "CHW Demand Bypass Branch"}],
        },
        validate=False,
    )
    doc.add(
        "Connector:Mixer",
        "CHW Demand Mixer",
        {
            "outlet_branch_name": "CHW Demand Outlet Branch",
            "branches": [{"inlet_branch_name": "CHW Coil Branch"}, {"inlet_branch_name": "CHW Demand Bypass Branch"}],
        },
        validate=False,
    )
    doc.add(
        "Pipe:Adiabatic",
        "CHW Demand Inlet Pipe",
        {"inlet_node_name": "CHW Demand Inlet Node", "outlet_node_name": "CHW Demand Splitter Inlet"},
        validate=False,
    )
    doc.add(
        "Pipe:Adiabatic",
        "CHW Demand Bypass",
        {"inlet_node_name": "CHW Demand Bypass Inlet", "outlet_node_name": "CHW Demand Bypass Outlet"},
        validate=False,
    )
    doc.add(
        "Pipe:Adiabatic",
        "CHW Demand Outlet Pipe",
        {"inlet_node_name": "CHW Demand Mixer Outlet", "outlet_node_name": "CHW Demand Outlet Node"},
        validate=False,
    )
    return doc


@pytest.fixture
def hvac_doc() -> IDFDocument:
    return _air_and_plant_model()


@pytest.fixture
def graph(hvac_doc: IDFDocument) -> HVACGraph:
    return build_hvac_graph(hvac_doc)


def _edges_from(graph: HVACGraph, key: str) -> set[str]:
    return {e.dst for e in graph.edges if e.src == key}


def test_loops_discovered(graph: HVACGraph) -> None:
    by_type = {loop.loop_type: loop for loop in graph.loops}
    assert set(by_type) == {"AirLoopHVAC", "PlantLoop"}
    assert by_type["AirLoopHVAC"].name == "DOAS"
    assert by_type["PlantLoop"].name == "CHW Loop"


def test_supply_demand_partition(graph: HVACGraph) -> None:
    air = next(loop for loop in graph.loops if loop.loop_type == "AirLoopHVAC")
    plant = next(loop for loop in graph.loops if loop.loop_type == "PlantLoop")
    assert _vkey("Coil:Cooling:Water", "DOAS Cooling Coil") in air.supply_keys
    assert _vkey("Fan:VariableVolume", "DOAS Supply Fan") in air.supply_keys
    assert _vkey("AirTerminal:SingleDuct:ConstantVolume:NoReheat", "Zone1 Terminal") in air.demand_keys
    assert _vkey("Chiller:Electric:EIR", "CHW Chiller") in plant.supply_keys
    assert _vkey("Pump:VariableSpeed", "CHW Pump") in plant.supply_keys
    assert _vkey("Coil:Cooling:Water", "DOAS Cooling Coil") in plant.demand_keys


def test_dual_loop_coil_is_single_vertex(graph: HVACGraph) -> None:
    coil = graph.vertex(_vkey("Coil:Cooling:Water", "DOAS Cooling Coil"))
    assert coil is not None
    # Exactly one vertex, but it belongs to both loops on different sides.
    matches = [v for v in graph.vertices if v.name == "DOAS Cooling Coil"]
    assert len(matches) == 1
    sides = {(m.loop_id.split("::")[-1], m.side) for m in coil.memberships}
    assert sides == {("DOAS", "supply"), ("CHW LOOP", "demand")}
    # It carries both its air and water node pairs.
    assert "DOAS Mixed Air Node" in coil.inlet_nodes
    assert "CHW Coil Inlet Node" in coil.inlet_nodes


def test_air_side_connectivity(graph: HVACGraph) -> None:
    oa = _vkey("OutdoorAir:Mixer", "DOAS OA Mixer")
    coil = _vkey("Coil:Cooling:Water", "DOAS Cooling Coil")
    fan = _vkey("Fan:VariableVolume", "DOAS Supply Fan")
    splitter = _vkey("AirLoopHVAC:ZoneSplitter", "DOAS Zone Splitter")
    assert coil in _edges_from(graph, oa)
    assert fan in _edges_from(graph, coil)
    assert splitter in _edges_from(graph, fan)  # supply outlet -> demand inlet alias


def test_splitter_fans_out(graph: HVACGraph) -> None:
    splitter = _vkey("Connector:Splitter", "CHW Supply Splitter")
    targets = _edges_from(graph, splitter)
    assert _vkey("Chiller:Electric:EIR", "CHW Chiller") in targets
    assert _vkey("Pipe:Adiabatic", "CHW Supply Bypass") in targets
    assert len(targets) == 2


def test_plant_loop_closes(graph: HVACGraph) -> None:
    # The demand outlet pipe feeds back to the pump via the demand-outlet/supply-inlet alias.
    pump = _vkey("Pump:VariableSpeed", "CHW Pump")
    demand_outlet = _vkey("Pipe:Adiabatic", "CHW Demand Outlet Pipe")
    assert pump in _edges_from(graph, demand_outlet)


def test_zone_attachment(graph: HVACGraph) -> None:
    assert len(graph.zones) == 1
    zone = graph.zones[0]
    assert zone.name == "Zone1"
    # The ADU resolves to its contained terminal.
    assert _vkey("AirTerminal:SingleDuct:ConstantVolume:NoReheat", "Zone1 Terminal") in zone.equipment_keys
    terminal = graph.vertex(_vkey("AirTerminal:SingleDuct:ConstantVolume:NoReheat", "Zone1 Terminal"))
    assert terminal is not None
    assert terminal.zone == "Zone1"


def test_categories(graph: HVACGraph) -> None:
    def cat(t: str, n: str) -> str | None:
        v = graph.vertex(_vkey(t, n))
        return v.category if v else None

    assert cat("Coil:Cooling:Water", "DOAS Cooling Coil") == "coil"
    assert cat("Fan:VariableVolume", "DOAS Supply Fan") == "fan"
    assert cat("Pump:VariableSpeed", "CHW Pump") == "pump"
    assert cat("Chiller:Electric:EIR", "CHW Chiller") == "plant_equipment"
    assert cat("Connector:Splitter", "CHW Supply Splitter") == "junction"
    assert cat("OutdoorAir:Mixer", "DOAS OA Mixer") == "outdoor_air"
    assert cat("Pipe:Adiabatic", "CHW Supply Bypass") == "pipe"


def test_mermaid_output(graph: HVACGraph) -> None:
    out = graph.to_mermaid()
    assert out.startswith("flowchart LR")
    assert '["DOAS · AirLoopHVAC"]' in out
    assert '["CHW Loop · PlantLoop"]' in out
    assert 'subgraph zones["Zones"]' in out
    assert "classDef coil" in out
    assert "Coil:Cooling:Water" in out


def test_dot_output(graph: HVACGraph) -> None:
    out = graph.to_dot()
    assert out.startswith("digraph hvac {")
    assert "rankdir=LR;" in out
    assert "subgraph cluster_" in out
    assert out.rstrip().endswith("}")


def test_helper_functions_accept_document(hvac_doc: IDFDocument) -> None:
    assert hvac_to_mermaid(hvac_doc).startswith("flowchart")
    assert hvac_to_dot(hvac_doc).startswith("digraph")


def test_output_is_deterministic(hvac_doc: IDFDocument) -> None:
    g1 = build_hvac_graph(hvac_doc)
    g2 = build_hvac_graph(_air_and_plant_model())
    assert g1.to_mermaid() == g2.to_mermaid()
    assert g1.to_dot() == g2.to_dot()
    assert [v.key for v in g1.vertices] == [v.key for v in g2.vertices]


def test_to_dict_and_json(graph: HVACGraph) -> None:
    data = graph.to_dict()
    assert data["version"] == [24, 1, 0]
    assert {loop["loop_type"] for loop in data["loops"]} == {"AirLoopHVAC", "PlantLoop"}
    assert any(v["name"] == "DOAS Cooling Coil" for v in data["vertices"])
    # Round-trips through JSON.
    reparsed = json.loads(graph.to_json())
    assert reparsed["vertices"][0]["key"] == data["vertices"][0]["key"]


def test_config_group_by_side_off(graph: HVACGraph) -> None:
    out = graph.to_mermaid(HVACDiagramConfig(group_by_side=False))
    assert '["supply"]' not in out
    assert '["demand"]' not in out


def test_config_no_node_labels(graph: HVACGraph) -> None:
    out = graph.to_mermaid(HVACDiagramConfig(show_node_labels=False))
    assert "-->|" not in out
    assert "-->" in out


def test_config_direction(graph: HVACGraph) -> None:
    assert graph.to_mermaid(HVACDiagramConfig(direction="TB")).startswith("flowchart TB")


def test_empty_document() -> None:
    graph = build_hvac_graph(new_document(V))
    assert graph.is_empty
    assert graph.vertices == ()
    assert "No HVAC components found" in graph.to_mermaid()
    assert "No HVAC components found" in graph.to_dot()


def test_hvac_template_guard_raises() -> None:
    doc = new_document(V)
    doc.add("Zone", "Office", {"x_origin": 0.0, "y_origin": 0.0, "z_origin": 0.0}, validate=False)
    doc.add(
        "HVACTemplate:Zone:IdealLoadsAirSystem",
        "Office Ideal Loads",
        {"zone_name": "Office"},
        validate=False,
    )
    with pytest.raises(HVACDiagramError) as exc:
        build_hvac_graph(doc)
    assert "HVACTemplate:Zone:IdealLoadsAirSystem" in exc.value.template_types


def test_suspicious_node_warning() -> None:
    # A lone coil whose water nodes connect to nothing yields suspicious-node warnings.
    doc = new_document(V)
    doc.add(
        "Coil:Cooling:Water",
        "Lonely Coil",
        {
            "air_inlet_node_name": "Air In",
            "air_outlet_node_name": "Air Out",
            "water_inlet_node_name": "Water In",
            "water_outlet_node_name": "Water Out",
        },
        validate=False,
    )
    graph = build_hvac_graph(doc)
    kinds = {w.kind for w in graph.warnings}
    assert "suspicious_node" in kinds


def _unitary_model() -> IDFDocument:
    """An air loop whose branch carries an AirLoopHVAC:UnitarySystem container.

    The fan and coils live inside the UnitarySystem (referenced by name), not on
    the branch — the case that previously dumped them into "Other equipment".
    """
    doc = new_document(V)
    doc.add("Zone", "Z", validate=False)
    doc.add(
        "AirLoopHVAC",
        "RTU",
        {
            "branch_list_name": "RTU Branches",
            "supply_side_inlet_node_name": "RTU Inlet",
            "supply_side_outlet_node_names": "RTU Unit Outlet",
            "demand_side_inlet_node_names": "RTU Demand Inlet",
            "demand_side_outlet_node_name": "RTU Demand Outlet",
        },
        validate=False,
    )
    doc.add("BranchList", "RTU Branches", {"branches": [{"branch_name": "RTU Branch"}]}, validate=False)
    doc.add(
        "Branch",
        "RTU Branch",
        {
            "components": [
                {
                    "component_object_type": "AirLoopHVAC:UnitarySystem",
                    "component_name": "RTU Unit",
                    "component_inlet_node_name": "RTU Inlet",
                    "component_outlet_node_name": "RTU Unit Outlet",
                }
            ]
        },
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:UnitarySystem",
        "RTU Unit",
        {
            "air_inlet_node_name": "RTU Inlet",
            "air_outlet_node_name": "RTU Unit Outlet",
            "supply_fan_object_type": "Fan:VariableVolume",
            "supply_fan_name": "RTU Fan",
            "cooling_coil_object_type": "Coil:Cooling:DX:SingleSpeed",
            "cooling_coil_name": "RTU Cooling",
            "heating_coil_object_type": "Coil:Heating:Fuel",
            "heating_coil_name": "RTU Heating",
        },
        validate=False,
    )
    doc.add(
        "Fan:VariableVolume",
        "RTU Fan",
        {"air_inlet_node_name": "RTU Inlet", "air_outlet_node_name": "RTU Fan Outlet"},
        validate=False,
    )
    doc.add(
        "Coil:Cooling:DX:SingleSpeed",
        "RTU Cooling",
        {"air_inlet_node_name": "RTU Fan Outlet", "air_outlet_node_name": "RTU Cooling Outlet"},
        validate=False,
    )
    doc.add(
        "Coil:Heating:Fuel",
        "RTU Heating",
        {"air_inlet_node_name": "RTU Cooling Outlet", "air_outlet_node_name": "RTU Unit Outlet"},
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:SupplyPath",
        "RTU Supply Path",
        {
            "supply_air_path_inlet_node_name": "RTU Demand Inlet",
            "components": [{"component_object_type": "AirLoopHVAC:ZoneSplitter", "component_name": "RTU Splitter"}],
        },
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:ZoneSplitter",
        "RTU Splitter",
        {"inlet_node_name": "RTU Demand Inlet", "nodes": [{"outlet_node_name": "Z Supply"}]},
        validate=False,
    )
    doc.add(
        "AirTerminal:SingleDuct:ConstantVolume:NoReheat",
        "Z Terminal",
        {"air_inlet_node_name": "Z Supply", "air_outlet_node_name": "Z Inlet"},
        validate=False,
    )
    return doc


def test_compound_unitary_system_expands() -> None:
    graph = build_hvac_graph(_unitary_model())
    # The container box is dropped — only its children are vertices.
    assert graph.vertex(_vkey("AirLoopHVAC:UnitarySystem", "RTU Unit")) is None
    # Every component lands in a loop; nothing is orphaned into "Other equipment".
    assert [v.key for v in graph.vertices if not v.memberships] == []
    rtu = next(loop for loop in graph.loops if loop.loop_type == "AirLoopHVAC")
    for child in ("RTU Fan", "RTU Cooling", "RTU Heating"):
        assert any(k.endswith(f"::{child.upper()}") for k in rtu.supply_keys)
    # The internal train is chained in sequence (no phantom parallel shortcut).
    fan = _vkey("Fan:VariableVolume", "RTU Fan")
    cooling = _vkey("Coil:Cooling:DX:SingleSpeed", "RTU Cooling")
    heating = _vkey("Coil:Heating:Fuel", "RTU Heating")
    assert cooling in _edges_from(graph, fan)
    assert heating in _edges_from(graph, cooling)


def test_subset_by_type(graph: HVACGraph) -> None:
    plant = graph.subset(loop_types=["PlantLoop"])
    assert {loop.loop_type for loop in plant.loops} == {"PlantLoop"}
    # The dual-loop coil is retained (it sits on the plant demand side).
    assert plant.vertex(_vkey("Coil:Cooling:Water", "DOAS Cooling Coil")) is not None
    # Air-only equipment is gone.
    assert plant.vertex(_vkey("Fan:VariableVolume", "DOAS Supply Fan")) is None


def test_subset_keeps_dual_loop_vertex_in_kept_loop(graph: HVACGraph) -> None:
    # After dropping the air loop, the water coil must group under the surviving
    # plant loop's demand side — not fall through to "Other equipment".
    from idfkit.visualization.hvac.layout import plan_layout

    plant = graph.subset(loop_types=["PlantLoop"])
    coil = plant.vertex(_vkey("Coil:Cooling:Water", "DOAS Cooling Coil"))
    assert coil is not None
    layout = plan_layout(plant)
    assert coil not in layout.ungrouped
    grouped = {v for vs in layout.by_group.values() for v in vs}
    assert coil in grouped
    assert "Other equipment" not in plant.to_mermaid()


def test_subset_by_name(graph: HVACGraph) -> None:
    air = graph.subset(loop_names=["DOAS"])
    assert [loop.name for loop in air.loops] == ["DOAS"]
    assert air.vertex(_vkey("Fan:VariableVolume", "DOAS Supply Fan")) is not None
    assert air.vertex(_vkey("Pump:VariableSpeed", "CHW Pump")) is None
    assert "PlantLoop" not in air.to_mermaid()


def test_overview_mermaid(graph: HVACGraph) -> None:
    ov = graph.overview_mermaid()
    assert ov.startswith("flowchart")
    assert "DOAS<br/>AirLoopHVAC" in ov
    assert "CHW Loop<br/>PlantLoop" in ov
    assert '(["Zone1"])' in ov
    # The shared coil couples the plant loop to the air loop.
    assert '-->|"coil"|' in ov
    assert "classDef plantloop" in ov


def test_large_model_size_hint() -> None:
    # Small models carry no hint; the threshold is exercised on real models in CI-free smoke.
    assert "%%" not in build_hvac_graph(_air_and_plant_model()).to_mermaid()


def test_return_air_closes_the_loop(graph: HVACGraph) -> None:
    # The zone's return air flows back to the zone mixer, drawn as a dashed edge.
    mermaid = graph.to_mermaid()
    assert "-.->|return|" in mermaid
    # Off switch.
    assert "-.->|return|" not in graph.to_mermaid(HVACDiagramConfig(show_return_air=False))
    # DOT renders it dashed too.
    assert 'style=dashed, label="return"' in graph.to_dot()


# --- Zone equipment: fan coils, VRF, reheat coils ----------------------------


def _fan_coil_model() -> IDFDocument:
    """A zone served by a ZoneHVAC:FourPipeFanCoil with a water coil on a plant loop.

    The fan coil is a compound container: its OA mixer, fan, and coils are separate
    objects. The water cooling coil also sits on the chilled-water plant demand
    branch, so it is dual-membership (plant demand) while the air-only fan and OA
    mixer have no loop side and must cluster under their zone.
    """
    doc = new_document(V)
    doc.add("Zone", "Z", validate=False)
    # --- Chilled-water plant loop carrying the fan-coil cooling coil (demand) ---
    doc.add(
        "PlantLoop",
        "CHW",
        {
            "plant_side_branch_list_name": "CHW Supply Branches",
            "demand_side_branch_list_name": "CHW Demand Branches",
            "plant_side_inlet_node_name": "CHW Supply Inlet",
            "plant_side_outlet_node_name": "CHW Supply Outlet",
            "demand_side_inlet_node_name": "CHW Demand Inlet",
            "demand_side_outlet_node_name": "CHW Demand Outlet",
        },
        validate=False,
    )
    doc.add("BranchList", "CHW Supply Branches", {"branches": [{"branch_name": "CHW Pump Branch"}]}, validate=False)
    doc.add("BranchList", "CHW Demand Branches", {"branches": [{"branch_name": "FC Coil Branch"}]}, validate=False)
    _branch(doc, "CHW Pump Branch", "Pump:VariableSpeed", "CHW Pump", "CHW Supply Inlet", "CHW Supply Outlet")
    doc.add(
        "Pump:VariableSpeed",
        "CHW Pump",
        {"inlet_node_name": "CHW Supply Inlet", "outlet_node_name": "CHW Supply Outlet"},
        validate=False,
    )
    _branch(doc, "FC Coil Branch", "Coil:Cooling:Water", "FC Cooling Coil", "CHW Demand Inlet", "CHW Demand Outlet")
    # --- Zone equipment: the fan coil and its internal train --------------------
    doc.add(
        "ZoneHVAC:EquipmentConnections",
        "Z Equip",
        {
            "zone_name": "Z",
            "zone_conditioning_equipment_list_name": "Z Equip List",
            "zone_air_inlet_node_or_nodelist_name": "Z Inlet",
            "zone_air_node_name": "Z Air Node",
            "zone_return_air_node_or_nodelist_name": "Z Return",
        },
        validate=False,
    )
    doc.add(
        "ZoneHVAC:EquipmentList",
        "Z Equip List",
        {"equipment": [{"zone_equipment_object_type": "ZoneHVAC:FourPipeFanCoil", "zone_equipment_name": "Z FanCoil"}]},
        validate=False,
    )
    doc.add(
        "ZoneHVAC:FourPipeFanCoil",
        "Z FanCoil",
        {
            "air_inlet_node_name": "Z FC Return",
            "air_outlet_node_name": "Z Inlet",
            "outdoor_air_mixer_object_type": "OutdoorAir:Mixer",
            "outdoor_air_mixer_name": "Z FC OA Mixer",
            "supply_air_fan_object_type": "Fan:OnOff",
            "supply_air_fan_name": "Z FC Fan",
            "cooling_coil_object_type": "Coil:Cooling:Water",
            "cooling_coil_name": "FC Cooling Coil",
            "heating_coil_object_type": "Coil:Heating:Water",
            "heating_coil_name": "FC Heating Coil",
        },
        validate=False,
    )
    doc.add(
        "OutdoorAir:Mixer",
        "Z FC OA Mixer",
        {
            "mixed_air_node_name": "Z FC Mixed Air",
            "outdoor_air_stream_node_name": "Z FC OA Inlet",
            "relief_air_stream_node_name": "Z FC Relief",
            "return_air_stream_node_name": "Z FC Return",
        },
        validate=False,
    )
    doc.add(
        "Fan:OnOff",
        "Z FC Fan",
        {"air_inlet_node_name": "Z FC Mixed Air", "air_outlet_node_name": "Z FC Fan Outlet"},
        validate=False,
    )
    doc.add(
        "Coil:Cooling:Water",
        "FC Cooling Coil",
        {
            "air_inlet_node_name": "Z FC Fan Outlet",
            "air_outlet_node_name": "Z FC Cooling Outlet",
            "water_inlet_node_name": "CHW Demand Inlet",
            "water_outlet_node_name": "CHW Demand Outlet",
        },
        validate=False,
    )
    doc.add(
        "Coil:Heating:Water",
        "FC Heating Coil",
        {"air_inlet_node_name": "Z FC Cooling Outlet", "air_outlet_node_name": "Z Inlet"},
        validate=False,
    )
    return doc


def _vrf_zone_model(master_type: str = "AirConditioner:VariableRefrigerantFlow") -> IDFDocument:
    """A zone served by a VRF terminal unit driven by an outdoor condensing unit.

    Exercises the ``_object_name`` field pairing (VRF terminal units), the bare
    ``_node`` suffix on VRF DX-coil air nodes, and the refrigerant network linking
    the master to each terminal unit through a ZoneTerminalUnitList. *master_type*
    selects the outdoor-unit variant (base vs. FluidTemperatureControl).
    """
    doc = new_document(V)
    doc.add("Zone", "Z", validate=False)
    doc.add(
        master_type,
        "VRF HP",
        {"zone_terminal_unit_list_name": "VRF List"},
        validate=False,
    )
    doc.add(
        "ZoneTerminalUnitList",
        "VRF List",
        {"zone_terminal_unit_list_name": "VRF List", "terminal_units": [{"zone_terminal_unit_name": "TU1"}]},
        validate=False,
    )
    doc.add(
        "ZoneHVAC:EquipmentConnections",
        "Z Equip",
        {
            "zone_name": "Z",
            "zone_conditioning_equipment_list_name": "Z Equip List",
            "zone_air_inlet_node_or_nodelist_name": "Z Inlet",
            "zone_air_node_name": "Z Air Node",
            "zone_return_air_node_or_nodelist_name": "Z Return",
        },
        validate=False,
    )
    doc.add(
        "ZoneHVAC:EquipmentList",
        "Z Equip List",
        {
            "equipment": [
                {
                    "zone_equipment_object_type": "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
                    "zone_equipment_name": "TU1",
                }
            ]
        },
        validate=False,
    )
    doc.add(
        "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
        "TU1",
        {
            "terminal_unit_air_inlet_node_name": "Z TU Return",
            "terminal_unit_air_outlet_node_name": "Z Inlet",
            "outside_air_mixer_object_type": "OutdoorAir:Mixer",
            "outside_air_mixer_object_name": "TU1 OA Mixer",
            "supply_air_fan_object_type": "Fan:OnOff",
            "supply_air_fan_object_name": "TU1 Fan",
            "cooling_coil_object_type": "Coil:Cooling:DX:VariableRefrigerantFlow",
            "cooling_coil_object_name": "TU1 Cooling",
            "heating_coil_object_type": "Coil:Heating:DX:VariableRefrigerantFlow",
            "heating_coil_object_name": "TU1 Heating",
        },
        validate=False,
    )
    doc.add(
        "OutdoorAir:Mixer",
        "TU1 OA Mixer",
        {
            "mixed_air_node_name": "TU1 Mixed Air",
            "outdoor_air_stream_node_name": "TU1 OA Inlet",
            "relief_air_stream_node_name": "TU1 Relief",
            "return_air_stream_node_name": "Z TU Return",
        },
        validate=False,
    )
    doc.add(
        "Fan:OnOff",
        "TU1 Fan",
        {"air_inlet_node_name": "TU1 Mixed Air", "air_outlet_node_name": "TU1 Fan Outlet"},
        validate=False,
    )
    # VRF DX coils use a bare ``_node`` suffix (no ``_name``) on their air nodes.
    doc.add(
        "Coil:Cooling:DX:VariableRefrigerantFlow",
        "TU1 Cooling",
        {"coil_air_inlet_node": "TU1 Fan Outlet", "coil_air_outlet_node": "TU1 Cooling Outlet"},
        validate=False,
    )
    doc.add(
        "Coil:Heating:DX:VariableRefrigerantFlow",
        "TU1 Heating",
        {"coil_air_inlet_node": "TU1 Cooling Outlet", "coil_air_outlet_node": "Z Inlet"},
        validate=False,
    )
    return doc


def _reheat_model() -> IDFDocument:
    """A single air loop with a VAV terminal whose reheat coil is electric (single-loop)."""
    doc = new_document(V)
    doc.add("Zone", "Z", validate=False)
    doc.add(
        "AirLoopHVAC",
        "VAV",
        {
            "branch_list_name": "VAV Branches",
            "supply_side_inlet_node_name": "VAV Inlet",
            "supply_side_outlet_node_names": "VAV Supply Outlet",
            "demand_side_inlet_node_names": "VAV Demand Inlet",
            "demand_side_outlet_node_name": "VAV Demand Outlet",
        },
        validate=False,
    )
    doc.add("BranchList", "VAV Branches", {"branches": [{"branch_name": "VAV Branch"}]}, validate=False)
    _branch(doc, "VAV Branch", "Fan:VariableVolume", "VAV Fan", "VAV Inlet", "VAV Supply Outlet")
    doc.add(
        "Fan:VariableVolume",
        "VAV Fan",
        {"air_inlet_node_name": "VAV Inlet", "air_outlet_node_name": "VAV Supply Outlet"},
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:SupplyPath",
        "VAV Supply Path",
        {
            "supply_air_path_inlet_node_name": "VAV Demand Inlet",
            "components": [{"component_object_type": "AirLoopHVAC:ZoneSplitter", "component_name": "VAV Splitter"}],
        },
        validate=False,
    )
    doc.add(
        "AirLoopHVAC:ZoneSplitter",
        "VAV Splitter",
        {"inlet_node_name": "VAV Demand Inlet", "nodes": [{"outlet_node_name": "Z Term Inlet"}]},
        validate=False,
    )
    doc.add(
        "AirTerminal:SingleDuct:VAV:Reheat",
        "Z Terminal",
        {
            "air_inlet_node_name": "Z Term Inlet",
            "air_outlet_node_name": "Z Inlet",
            "damper_air_outlet_node_name": "Z Damper Outlet",
            "reheat_coil_object_type": "Coil:Heating:Electric",
            "reheat_coil_name": "Z Reheat",
        },
        validate=False,
    )
    doc.add(
        "Coil:Heating:Electric",
        "Z Reheat",
        {"air_inlet_node_name": "Z Damper Outlet", "air_outlet_node_name": "Z Inlet"},
        validate=False,
    )
    return doc


def test_fan_coil_groups_under_zone() -> None:
    from idfkit.visualization.hvac.layout import plan_layout

    graph = build_hvac_graph(_fan_coil_model())
    # The fan-coil container box is dropped — only its children are vertices.
    assert graph.vertex(_vkey("ZoneHVAC:FourPipeFanCoil", "Z FanCoil")) is None
    layout = plan_layout(graph)
    cluster = {v.key for v in layout.zone_clusters.get("Z", [])}
    # Air-only equipment clusters under its zone, not "Other equipment".
    assert _vkey("Fan:OnOff", "Z FC Fan") in cluster
    assert _vkey("OutdoorAir:Mixer", "Z FC OA Mixer") in cluster
    assert layout.ungrouped == []
    assert "Other equipment" not in graph.to_mermaid()
    # The water cooling coil keeps its plant membership but is still zone-tagged.
    coil = graph.vertex(_vkey("Coil:Cooling:Water", "FC Cooling Coil"))
    assert coil is not None
    assert any(m.loop_id.startswith("PLANTLOOP::") for m in coil.memberships)
    assert coil not in layout.zone_clusters.get("Z", [])
    assert coil.zone == "Z"


@pytest.mark.parametrize(
    "master_type",
    [
        "AirConditioner:VariableRefrigerantFlow",
        "AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl",
    ],
)
def test_vrf_refrigerant_network(master_type: str) -> None:
    from idfkit.visualization.hvac.layout import plan_layout

    graph = build_hvac_graph(_vrf_zone_model(master_type))
    # The terminal-unit container box is dropped; its DX coils became vertices
    # despite their bare ``_node``-suffixed air-node fields.
    assert graph.vertex(_vkey("ZoneHVAC:TerminalUnit:VariableRefrigerantFlow", "TU1")) is None
    assert graph.vertex(_vkey("Coil:Cooling:DX:VariableRefrigerantFlow", "TU1 Cooling")) is not None
    # The refrigerant network links the outdoor unit (any VRF variant) to each
    # terminal DX coil.
    master = _vkey(master_type, "VRF HP")
    terminals = {r.terminal_key for r in graph.refrigerant_edges if r.master_key == master}
    assert _vkey("Coil:Cooling:DX:VariableRefrigerantFlow", "TU1 Cooling") in terminals
    assert _vkey("Coil:Heating:DX:VariableRefrigerantFlow", "TU1 Heating") in terminals
    mermaid = graph.to_mermaid()
    assert "-.->|refrigerant|" in mermaid
    assert "VRF refrigerant system" in mermaid
    assert "Other equipment" not in mermaid
    # The DX coils group under their zone.
    cluster = {v.key for v in plan_layout(graph).zone_clusters.get("Z", [])}
    assert _vkey("Coil:Cooling:DX:VariableRefrigerantFlow", "TU1 Cooling") in cluster
    # Round-trips through to_dict and subset.
    assert graph.to_dict()["refrigerant"]
    assert graph.subset(loop_types=["AirLoopHVAC"]).refrigerant_edges == ()


def test_reheat_coil_attaches_to_terminal_loop() -> None:
    from idfkit.visualization.hvac.layout import plan_layout

    graph = build_hvac_graph(_reheat_model())
    coil = graph.vertex(_vkey("Coil:Heating:Electric", "Z Reheat"))
    assert coil is not None
    # The single-loop reheat coil inherits the terminal's air-loop demand side.
    assert [m.side for m in coil.memberships] == ["demand"]
    assert coil.memberships[0].loop_id == _vkey("AirLoopHVAC", "VAV")
    assert coil not in plan_layout(graph).ungrouped
    assert "Other equipment" not in graph.to_mermaid()


def _example_files_dir() -> object:
    """The EnergyPlus ExampleFiles directory, or None if no install is found."""

    try:
        from idfkit.simulation import find_energyplus

        ex = find_energyplus().install_dir / "ExampleFiles"
    except Exception:
        return None
    return ex if ex.is_dir() else None


@pytest.mark.parametrize(
    ("filename", "expand"),
    [
        ("VariableRefrigerantFlow_5Zone_wAirloop.idf", False),
        ("5ZoneFanCoilDOASCool.idf", False),
        ("HVACTemplate-5ZonePackagedVAV.idf", True),
    ],
)
def test_real_zone_equipment_models_have_no_orphans(filename: str, expand: bool) -> None:
    """On real zone-equipment models, nothing falls into 'Other equipment'."""
    from pathlib import Path

    from idfkit import load_idf
    from idfkit.visualization.hvac.layout import plan_layout

    ex_dir = _example_files_dir()
    if ex_dir is None:
        pytest.skip("EnergyPlus ExampleFiles not available")
    path = Path(str(ex_dir)) / filename
    if not path.exists():
        pytest.skip(f"{filename} not bundled with this EnergyPlus version")
    graph = build_hvac_graph(load_idf(path), expand=expand)
    # The only acceptable "ungrouped" vertices are VRF outdoor units, which render
    # in the dedicated refrigerant cluster rather than "Other equipment".
    masters = {r.master_key for r in graph.refrigerant_edges}
    assert [v.key for v in plan_layout(graph).ungrouped if v.key not in masters] == []
    assert "Other equipment" not in graph.to_mermaid()
