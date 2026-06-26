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
