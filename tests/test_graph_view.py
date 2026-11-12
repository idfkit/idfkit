"""The combined model graph (``idfkit.graph.ModelGraph``): identity, vocabulary, walks and bounds (T112)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from idfkit import IDFDocument, load_idf, new_document
from idfkit.graph import EdgeKind, GraphEdge, ModelGraph, NodeKind, ObjectKey, Subgraph
from idfkit.hvac import ComponentCategory, HVACTopology
from idfkit.simulation import ResultIndex, SimulationResult

LINKED = Path(__file__).parent / "fixtures" / "simulation" / "linked"

NODE_KIND_LAYER: dict[str, str] = {
    "object": "model",
    "node": "topology",
    "result_fact": "results",
    "message": "results",
}
EDGE_KIND_LAYER: dict[str, str] = {
    "reference": "model",
    "flow": "topology",
    "control": "topology",
    "membership": "topology",
    "result_link": "results",
}

COIL = ObjectKey("Coil:Heating:Water", "SPACE1-1 Zone Coil")
COIL_ID = "object:COIL:HEATING:WATER:SPACE1-1 ZONE COIL"
COOLING_COIL = ObjectKey("Coil:Cooling:Water", "Main Cooling Coil 1")
AIR_LOOP = ObjectKey("AirLoopHVAC", "VAV Sys 1")


@pytest.fixture(scope="module")
def five_zone() -> IDFDocument:
    return load_idf(str(LINKED / "5ZoneAirCooled.idf"))


@pytest.fixture
def shared_names() -> IDFDocument:
    """A zone, a schedule and a material all called "Office", and a wall naming two of them."""
    doc = new_document()
    doc.add("Zone", "Office")
    doc.add("Schedule:Constant", "Office", hourly_value=1.0, validate=False)
    doc.add(
        "Material",
        "Office",
        roughness="Rough",
        thickness=0.1,
        conductivity=1.0,
        density=1.0,
        specific_heat=1000.0,
        validate=False,
    )
    doc.add("Construction", "Wall", outside_layer="Office", validate=False)
    doc.add(
        "BuildingSurface:Detailed",
        "W1",
        surface_type="Wall",
        construction_name="Wall",
        zone_name="Office",
        outside_boundary_condition="Outdoors",
        validate=False,
    )
    return doc


@pytest.fixture
def ems_doc() -> IDFDocument:
    """A fan between two nodes, with an EMS sensor and actuator naming its outlet node."""
    doc = new_document()
    doc.add("Schedule:Constant", "Always On", hourly_value=1.0, validate=False)
    doc.add(
        "Fan:ConstantVolume",
        "Fan",
        availability_schedule_name="Always On",
        air_inlet_node_name="Mixed Air",
        air_outlet_node_name="Supply Air",
        validate=False,
    )
    doc.add(
        "EnergyManagementSystem:Sensor",
        "Supply Temp",
        output_variable_or_output_meter_index_key_name="Supply Air",
        output_variable_or_output_meter_name="System Node Temperature",
        validate=False,
    )
    doc.add(
        "EnergyManagementSystem:Actuator",
        "Supply Setpoint",
        actuated_component_unique_name="Supply Air",
        actuated_component_type="System Node Setpoint",
        actuated_component_control_type="Temperature Setpoint",
        validate=False,
    )
    return doc


def ids(sub: Subgraph) -> list[str]:
    return [n.id for n in sub.nodes]


def pairs(sub: Subgraph, kind: str | None = None) -> set[tuple[str, str]]:
    return {(e.source, e.target) for e in sub.edges if kind is None or e.kind == kind}


def edge(sub: Subgraph, source: str, target: str, kind: str) -> GraphEdge:
    found = [e for e in sub.edges if e.source == source and e.target == target and e.kind == kind]
    assert len(found) == 1, (source, target, kind, found)
    return found[0]


def walks(five_zone: IDFDocument) -> Iterator[Subgraph]:
    graph = ModelGraph(five_zone)
    yield graph.neighbourhood(COIL, hops=2)
    yield graph.neighbourhood(AIR_LOOP, hops=1)
    yield graph.neighbourhood("Mixed Air Node 1", hops=2)


# ---------------------------------------------------------------------------------------------- #
# Construction, layers and identity
# ---------------------------------------------------------------------------------------------- #


def test_construction_builds_no_layer(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[object] = []
    original = HVACTopology.from_document.__func__  # type: ignore[attr-defined]

    def counting(cls: type[HVACTopology], doc: Any) -> HVACTopology:
        calls.append(doc)
        return original(cls, doc)

    monkeypatch.setattr(HVACTopology, "from_document", classmethod(counting))
    doc = new_document()
    doc.add("Zone", "Office")
    graph = ModelGraph(doc)
    assert calls == []
    graph.neighbourhood(ObjectKey("Zone", "Office"))
    assert calls


def test_later_edits_are_visible_without_rebuilding_the_view() -> None:
    doc = new_document()
    doc.add("Schedule:Constant", "Always On", hourly_value=1.0, validate=False)
    graph = ModelGraph(doc)
    start = ObjectKey("Schedule:Constant", "Always On")
    before = graph.neighbourhood(start)
    assert ids(before) == ["object:SCHEDULE:CONSTANT:ALWAYS ON"]
    assert before.truncated is False

    doc.add(
        "Fan:ConstantVolume",
        "Fan",
        availability_schedule_name="Always On",
        air_inlet_node_name="In",
        air_outlet_node_name="Out",
        validate=False,
    )
    after = graph.neighbourhood(start)
    assert ids(after) == ["object:SCHEDULE:CONSTANT:ALWAYS ON", "object:FAN:CONSTANTVOLUME:FAN"]
    fan = graph.neighbourhood(ObjectKey("Fan:ConstantVolume", "Fan"))
    assert {"node:IN", "node:OUT"} <= set(ids(fan))


def test_layers_and_unavailable() -> None:
    graph = ModelGraph(new_document())
    assert graph.layers == ["model", "topology"]
    assert graph.unavailable == {"results": "no ResultIndex was passed in"}


def test_subgraph_carries_layers_unavailable_and_no_results_state(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL)
    assert sub.layers == ["model", "topology"]
    assert sub.unavailable == {"results": "no ResultIndex was passed in"}
    assert sub.results_state is None
    assert sub.coverage == ModelGraph(five_zone).coverage


def test_node_id_for_objects_and_nodes_is_case_insensitive(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    assert graph.node_id(COIL) == COIL_ID
    assert graph.node_id(ObjectKey("coil:heating:water", "space1-1 zone coil")) == COIL_ID
    assert graph.node_id("mixed air node 1") == "node:MIXED AIR NODE 1"
    assert graph.node_id(ObjectKey("Zone", "SPACE1-1")) == "object:ZONE:SPACE1-1"


def test_node_id_raises_key_error_for_a_missing_object(five_zone: IDFDocument) -> None:
    with pytest.raises(KeyError):
        ModelGraph(five_zone).node_id(ObjectKey("Zone", "No Such Zone"))


def test_unnamed_objects_get_their_zone_or_an_index(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    # ZoneHVAC:EquipmentConnections has no name field: it is known by the zone it serves.
    assert graph.node_id(ObjectKey("ZoneHVAC:EquipmentConnections", "SPACE1-1")) == (
        "object:ZONEHVAC:EQUIPMENTCONNECTIONS:SPACE1-1"
    )
    doc = new_document()
    doc.add("Output:Variable", key_value="*", variable_name="Zone Mean Air Temperature", validate=False)
    assert ModelGraph(doc).node_id(ObjectKey("Output:Variable", "Output:Variable")) == "object:OUTPUT:VARIABLE:#0"


def test_start_comes_first_and_ids_are_unique(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    sub = graph.neighbourhood(COIL, hops=2)
    assert sub.start == COIL_ID
    assert sub.nodes[0].id == COIL_ID
    assert len(ids(sub)) == len(set(ids(sub)))
    node_sub = graph.neighbourhood("mixed air node 1")
    assert node_sub.start == "node:MIXED AIR NODE 1"
    assert node_sub.nodes[0].node == "Mixed Air Node 1"


def test_node_payloads(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL)
    coil = sub.nodes[0]
    assert coil.kind == "object"
    assert coil.key == COIL
    assert coil.node is None
    assert coil.attrs["category"] == "heating_coil"
    water_in = next(n for n in sub.nodes if n.id == "node:SPACE1-1 ZONE COIL WATER IN NODE")
    assert water_in.kind == "node"
    assert water_in.key is None
    assert water_in.node == "SPACE1-1 Zone Coil Water In Node"
    assert water_in.attrs["fluid"] == "Water"


# ---------------------------------------------------------------------------------------------- #
# Vocabulary
# ---------------------------------------------------------------------------------------------- #


def test_vocabulary_is_closed_and_layer_is_fixed_by_kind(five_zone: IDFDocument) -> None:
    for sub in walks(five_zone):
        for node in sub.nodes:
            assert node.kind in NODE_KIND_LAYER
            assert node.layer == NODE_KIND_LAYER[node.kind]
        for e in sub.edges:
            assert e.kind in EDGE_KIND_LAYER
            assert e.layer == EDGE_KIND_LAYER[e.kind]
            assert e.key.startswith(f"{e.kind}:")


def test_node_ids_follow_the_kind(five_zone: IDFDocument) -> None:
    for sub in walks(five_zone):
        for node in sub.nodes:
            if node.kind == "object":
                assert node.key is not None
                if ":#" in node.id:  # an unnamed object serving no zone is known by its index
                    assert node.id.startswith(f"object:{node.key.object_type.upper()}:#")
                    continue
                assert node.id == f"object:{node.key.object_type.upper()}:{node.key.name.upper()}"
            else:
                assert node.node is not None
                assert node.id == f"node:{node.node.upper()}"


def test_edges_only_join_returned_nodes(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    subs = [*walks(five_zone), graph.neighbourhood(AIR_LOOP, hops=3, max_nodes=10)]
    for sub in subs:
        returned = set(ids(sub))
        for e in sub.edges:
            assert e.source in returned
            assert e.target in returned


def test_output_is_deterministic(five_zone: IDFDocument) -> None:
    first = ModelGraph(five_zone).neighbourhood(COIL, hops=2, max_nodes=30)
    second = ModelGraph(five_zone).neighbourhood(COIL, hops=2, max_nodes=30)
    assert first == second
    assert ids(first) == ids(second)
    assert [(e.source, e.target, e.key) for e in first.edges] == [(e.source, e.target, e.key) for e in second.edges]


# ---------------------------------------------------------------------------------------------- #
# Reference edges
# ---------------------------------------------------------------------------------------------- #


def test_reference_targets_resolve_to_the_typed_object_when_names_are_shared(shared_names: IDFDocument) -> None:
    graph = ModelGraph(shared_names)
    sub = graph.neighbourhood(ObjectKey("BuildingSurface:Detailed", "W1"))
    assert set(ids(sub)) == {"object:BUILDINGSURFACE:DETAILED:W1", "object:CONSTRUCTION:WALL", "object:ZONE:OFFICE"}
    zone_edge = edge(sub, "object:BUILDINGSURFACE:DETAILED:W1", "object:ZONE:OFFICE", "reference")
    assert zone_edge.key == "reference:zone_name"
    assert zone_edge.attrs["field"] == "zone_name"
    assert zone_edge.layer == "model"

    construction = graph.neighbourhood(ObjectKey("Construction", "Wall"))
    layer_edge = edge(construction, "object:CONSTRUCTION:WALL", "object:MATERIAL:OFFICE", "reference")
    assert layer_edge.attrs["field"] == "outside_layer"
    assert "object:ZONE:OFFICE" not in ids(construction)
    assert "object:SCHEDULE:CONSTANT:OFFICE" not in ids(construction)


def test_incoming_references_come_only_from_fields_that_name_that_type(shared_names: IDFDocument) -> None:
    graph = ModelGraph(shared_names)
    zone = graph.neighbourhood(ObjectKey("Zone", "Office"))
    assert ids(zone) == ["object:ZONE:OFFICE", "object:BUILDINGSURFACE:DETAILED:W1"]
    schedule = graph.neighbourhood(ObjectKey("Schedule:Constant", "Office"))
    assert ids(schedule) == ["object:SCHEDULE:CONSTANT:OFFICE"]
    assert schedule.edges == []
    assert schedule.truncated is False
    material = graph.neighbourhood(ObjectKey("Material", "Office"))
    assert ids(material) == ["object:MATERIAL:OFFICE", "object:CONSTRUCTION:WALL"]


def test_reference_edge_direction_is_referrer_to_referenced(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL)
    terminal = "object:AIRTERMINAL:SINGLEDUCT:VAV:REHEAT:SPACE1-1 VAV REHEAT"
    assert edge(sub, terminal, COIL_ID, "reference").attrs["field"] == "reheat_coil_name"
    assert edge(sub, COIL_ID, "object:SCHEDULE:COMPACT:REHEATCOILAVAILSCHED", "reference").key == (
        "reference:availability_schedule_name"
    )


# ---------------------------------------------------------------------------------------------- #
# Flow, control and membership edges
# ---------------------------------------------------------------------------------------------- #


def test_flow_edges_enter_inlets_and_leave_outlets(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL)
    inlet = edge(sub, "node:SPACE1-1 ZONE COIL WATER IN NODE", COIL_ID, "flow")
    assert inlet.key == "flow:water_inlet_node_name"
    assert inlet.attrs["connection_type"] == "Inlet"
    assert inlet.attrs["fluid"] == "Water"
    assert inlet.layer == "topology"
    outlet = edge(sub, COIL_ID, "node:SPACE1-1 IN NODE", "flow")
    assert outlet.attrs["field"] == "air_outlet_node_name"
    assert outlet.attrs["connection_type"] == "Outlet"
    assert outlet.attrs["fluid"] == "Air"
    assert ("node:SPACE1-1 ZONE COIL AIR IN NODE", COIL_ID) in pairs(sub, "flow")
    assert (COIL_ID, "node:SPACE1-1 ZONE COIL WATER OUT NODE") in pairs(sub, "flow")


def test_a_node_start_reaches_every_object_using_the_node(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood("Mixed Air Node 1")
    node = "node:MIXED AIR NODE 1"
    assert (node, "object:COIL:COOLING:WATER:MAIN COOLING COIL 1") in pairs(sub, "flow")
    assert ("object:OUTDOORAIR:MIXER:OA MIXING BOX 1", node) in pairs(sub, "flow")
    control = edge(sub, "object:CONTROLLER:OUTDOORAIR:OA CONTROLLER 1", node, "control")
    assert control.attrs["connection_type"] == "Sensor"
    assert "rule" not in control.attrs
    assert ("object:SETPOINTMANAGER:MIXEDAIR:MIXED AIR TEMP MANAGER 1", node) in pairs(sub, "control")


def test_ems_sensor_and_actuator_on_a_node_are_convention_control_edges(ems_doc: IDFDocument) -> None:
    sub = ModelGraph(ems_doc).neighbourhood("Supply Air")
    node = "node:SUPPLY AIR"
    sensor = edge(sub, "object:ENERGYMANAGEMENTSYSTEM:SENSOR:SUPPLY TEMP", node, "control")
    actuator = edge(sub, "object:ENERGYMANAGEMENTSYSTEM:ACTUATOR:SUPPLY SETPOINT", node, "control")
    for control in (sensor, actuator):
        assert control.attrs["rule"] == "ems_key"
        assert control.attrs["confidence"] == "convention"
        assert control.layer == "topology"
    assert sensor.attrs["connection_type"] == "Sensor"
    assert actuator.attrs["connection_type"] == "Actuator"
    assert ("object:FAN:CONSTANTVOLUME:FAN", node) in pairs(sub, "flow")


def test_membership_edges_point_from_component_to_loop(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COOLING_COIL, edge_kinds=["membership"])
    coil = "object:COIL:COOLING:WATER:MAIN COOLING COIL 1"
    assert ids(sub) == [coil, "object:AIRLOOPHVAC:VAV SYS 1", "object:PLANTLOOP:CHILLED WATER LOOP"]
    air = edge(sub, coil, "object:AIRLOOPHVAC:VAV SYS 1", "membership")
    assert air.key == "membership:air"
    assert dict(air.attrs) == {"side": "supply", "branch": "VAV Sys 1 Main Branch", "position": 1, "loop_kind": "air"}
    plant = edge(sub, coil, "object:PLANTLOOP:CHILLED WATER LOOP", "membership")
    assert dict(plant.attrs) == {
        "side": "demand",
        "branch": "Cooling Coil Branch",
        "position": 0,
        "loop_kind": "plant",
    }


def test_reheat_coil_is_a_member_of_its_air_loop_and_hot_water_loop(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL)
    air = edge(sub, COIL_ID, "object:AIRLOOPHVAC:VAV SYS 1", "membership")
    assert air.attrs["side"] == "demand"
    assert air.attrs["loop_kind"] == "air"
    plant = edge(sub, COIL_ID, "object:PLANTLOOP:HOT WATER LOOP", "membership")
    assert plant.attrs["branch"] == "SPACE1-1 Reheat Branch"
    assert plant.attrs["loop_kind"] == "plant"


def test_a_loop_start_walks_to_its_members(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(AIR_LOOP, edge_kinds=["membership"], max_nodes=1000)
    loop = "object:AIRLOOPHVAC:VAV SYS 1"
    members = {s for s, t in pairs(sub, "membership") if t == loop}
    assert "object:COIL:COOLING:WATER:MAIN COOLING COIL 1" in members
    assert COIL_ID in members
    assert all(e.target == loop for e in sub.edges)


def test_zone_equipment_is_a_member_of_its_equipment_connections() -> None:
    doc = load_idf(str(LINKED / "DOASDualDuctSchool.idf"))
    fan_coil = next(iter(doc["ZoneHVAC:FourPipeFanCoil"]))
    sub = ModelGraph(doc).neighbourhood(ObjectKey(fan_coil.obj_type, fan_coil.name), edge_kinds=["membership"])
    memberships = [e for e in sub.edges if e.kind == "membership"]
    assert memberships
    for e in memberships:
        assert e.target.startswith("object:ZONEHVAC:EQUIPMENTCONNECTIONS:")
        assert e.attrs["loop_kind"] == "zone_equipment"


# ---------------------------------------------------------------------------------------------- #
# Bounds
# ---------------------------------------------------------------------------------------------- #


def test_hops_zero_returns_the_start_alone_and_says_it_was_cut(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL, hops=0)
    assert ids(sub) == [COIL_ID]
    assert sub.edges == []
    assert sub.truncated is True
    assert sub.omitted_nodes >= 1
    assert sub.frontier == [COIL_ID]


def test_hops_zero_on_an_isolated_object_is_not_truncated() -> None:
    doc = new_document()
    doc.add("Zone", "Lonely")
    sub = ModelGraph(doc).neighbourhood(ObjectKey("Zone", "Lonely"), hops=0)
    assert ids(sub) == ["object:ZONE:LONELY"]
    assert sub.truncated is False
    assert sub.omitted_nodes == 0
    assert sub.frontier == []


def test_more_hops_reach_further(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    one = graph.neighbourhood(COIL, hops=1, max_nodes=10_000)
    two = graph.neighbourhood(COIL, hops=2, max_nodes=10_000)
    assert set(ids(one)) < set(ids(two))
    assert ids(two)[: len(ids(one))] == ids(one)  # breadth first: the first ring comes first


def test_frontier_and_omitted_nodes_after_a_hop_cut(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL, hops=1)
    assert sub.truncated is True
    assert sub.omitted_nodes > 0
    assert COIL_ID not in sub.frontier  # every neighbour of the start was returned
    assert set(sub.frontier) <= set(ids(sub))
    assert "object:AIRLOOPHVAC:VAV SYS 1" in sub.frontier


def test_max_nodes_bounds_the_walk(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    full = graph.neighbourhood(COIL, hops=2, max_nodes=10_000)
    cut = graph.neighbourhood(COIL, hops=2, max_nodes=5)
    assert len(cut.nodes) == 5
    assert ids(cut) == ids(full)[:5]
    assert cut.truncated is True
    assert cut.omitted_nodes >= 1
    assert cut.frontier
    assert set(cut.frontier) <= set(ids(cut))


def test_max_nodes_one_returns_the_start(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(COIL, hops=3, max_nodes=1)
    assert ids(sub) == [COIL_ID]
    assert sub.edges == []
    assert sub.truncated is True
    assert sub.frontier == [COIL_ID]


def test_an_uncut_walk_is_not_truncated(shared_names: IDFDocument) -> None:
    sub = ModelGraph(shared_names).neighbourhood(ObjectKey("Zone", "Office"), hops=10)
    assert set(ids(sub)) == {
        "object:ZONE:OFFICE",
        "object:BUILDINGSURFACE:DETAILED:W1",
        "object:CONSTRUCTION:WALL",
        "object:MATERIAL:OFFICE",
    }
    assert sub.truncated is False
    assert sub.omitted_nodes == 0
    assert sub.frontier == []


@pytest.mark.parametrize("hops", [-1, -5])
def test_negative_hops_raise_value_error(five_zone: IDFDocument, hops: int) -> None:
    with pytest.raises(ValueError, match="hops"):
        ModelGraph(five_zone).neighbourhood(COIL, hops=hops)


@pytest.mark.parametrize("max_nodes", [0, -1])
def test_max_nodes_below_one_raises_value_error(five_zone: IDFDocument, max_nodes: int) -> None:
    with pytest.raises(ValueError, match="max_nodes"):
        ModelGraph(five_zone).neighbourhood(COIL, max_nodes=max_nodes)


def test_missing_object_start_raises_key_error(five_zone: IDFDocument) -> None:
    with pytest.raises(KeyError):
        ModelGraph(five_zone).neighbourhood(ObjectKey("Coil:Heating:Water", "No Such Coil"))


def test_missing_node_start_raises_key_error(five_zone: IDFDocument) -> None:
    with pytest.raises(KeyError):
        ModelGraph(five_zone).neighbourhood("No Such Node")


# ---------------------------------------------------------------------------------------------- #
# Kind and category filters
# ---------------------------------------------------------------------------------------------- #


def test_edge_kinds_prune_the_walk(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    choices: list[list[EdgeKind]] = [["reference"], ["flow"], ["membership"], ["flow", "control"]]
    for kinds in choices:
        sub = graph.neighbourhood(COIL, hops=2, edge_kinds=kinds, max_nodes=10_000)
        assert {e.kind for e in sub.edges} <= set(kinds)
    references = graph.neighbourhood(COIL, hops=2, edge_kinds=["reference"], max_nodes=10_000)
    assert {n.kind for n in references.nodes} == {"object"}


def test_node_kinds_prune_the_walk(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    objects = graph.neighbourhood(COIL, hops=2, node_kinds=["object"], max_nodes=10_000)
    assert {n.kind for n in objects.nodes} == {"object"}
    assert {e.kind for e in objects.edges} <= {"reference", "membership"}
    # A node start with object nodes excluded has nowhere to go.
    alone = graph.neighbourhood("Mixed Air Node 1", hops=2, node_kinds=["node"])
    assert ids(alone) == ["node:MIXED AIR NODE 1"]
    assert alone.edges == []


def test_unknown_kinds_are_ignored(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    node_kinds: list[Any] = ["object", "hyperedge"]
    edge_kinds: list[Any] = ["reference", "membership", "teleport"]
    plain_nodes: list[NodeKind] = ["object"]
    plain_edges: list[EdgeKind] = ["reference", "membership"]
    assert graph.neighbourhood(COIL, hops=2, node_kinds=node_kinds) == graph.neighbourhood(
        COIL, hops=2, node_kinds=plain_nodes
    )
    assert graph.neighbourhood(COIL, hops=2, edge_kinds=edge_kinds) == graph.neighbourhood(
        COIL, hops=2, edge_kinds=plain_edges
    )


def test_result_kinds_name_nothing_while_the_results_layer_is_absent(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    sub = graph.neighbourhood(COIL, hops=2, edge_kinds=["result_link"])
    assert ids(sub) == [COIL_ID]
    assert sub.edges == []


def test_category_filter_keeps_the_start_and_matching_objects(five_zone: IDFDocument) -> None:
    sub = ModelGraph(five_zone).neighbourhood(AIR_LOOP, hops=3, categories=[ComponentCategory.HEATING_COIL])
    assert sub.nodes[0].id == "object:AIRLOOPHVAC:VAV SYS 1"
    others = sub.nodes[1:]
    assert others
    for node in others:
        if node.kind == "object":
            assert node.attrs["category"] == "heating_coil"
    assert {"object:COIL:HEATING:WATER:MAIN HEATING COIL 1", COIL_ID} <= set(ids(sub))
    returned = set(ids(sub))
    assert all(e.source in returned and e.target in returned for e in sub.edges)


def test_category_filter_accepts_plain_strings(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    as_enum = graph.neighbourhood(AIR_LOOP, hops=3, categories=[ComponentCategory.HEATING_COIL])
    as_text = graph.neighbourhood(AIR_LOOP, hops=3, categories=["heating_coil"])
    assert as_enum == as_text


def test_category_filter_keeps_fluid_nodes_on_the_path() -> None:
    doc = new_document()
    doc.add(
        "Fan:ConstantVolume", "Fan", air_inlet_node_name="Mixed Air", air_outlet_node_name="Fan Out", validate=False
    )
    doc.add(
        "Coil:Heating:Electric",
        "Heater",
        air_inlet_node_name="Fan Out",
        air_outlet_node_name="Supply Air",
        validate=False,
    )
    sub = ModelGraph(doc).neighbourhood(
        ObjectKey("Fan:ConstantVolume", "Fan"), hops=3, categories=[ComponentCategory.HEATING_COIL]
    )
    assert ids(sub) == ["object:FAN:CONSTANTVOLUME:FAN", "node:FAN OUT", "object:COIL:HEATING:ELECTRIC:HEATER"]
    assert pairs(sub) == {
        ("object:FAN:CONSTANTVOLUME:FAN", "node:FAN OUT"),
        ("node:FAN OUT", "object:COIL:HEATING:ELECTRIC:HEATER"),
    }
    # The other nodes were left out by the filter, not by a bound: they are no cut.
    assert "node:MIXED AIR" not in ids(sub)
    assert "node:SUPPLY AIR" not in ids(sub)
    assert sub.truncated is False


def test_category_filter_applies_before_max_nodes(five_zone: IDFDocument) -> None:
    graph = ModelGraph(five_zone)
    unfiltered = graph.neighbourhood(AIR_LOOP, hops=3, max_nodes=2)
    assert unfiltered.nodes[1].attrs.get("category") != "heating_coil"
    filtered = graph.neighbourhood(AIR_LOOP, hops=3, categories=["heating_coil"], max_nodes=2)
    assert len(filtered.nodes) == 2
    assert filtered.nodes[1].attrs["category"] == "heating_coil"
    assert filtered.truncated is True
    assert filtered.omitted_nodes >= 1


# ------------------------------------------------------------------------------- results layer


def _linked(tmp_path: Path, fixture: str = "MultiStory") -> tuple[IDFDocument, ResultIndex]:
    import shutil

    linked = Path(__file__).parent / "fixtures" / "simulation" / "linked"
    shutil.copy(linked / f"{fixture}.sql", tmp_path / "eplusout.sql")
    doc = load_idf(linked / f"{fixture}.idf")
    run = SimulationResult(run_dir=tmp_path, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0)
    return doc, ResultIndex.build(doc, run, run_revision=doc.revision, run_model_hash="h")


DX_COIL = ObjectKey("Coil:Cooling:DX:SingleSpeed", "Top East OA DX Coil")


def test_results_layer_is_present_with_a_result_index(tmp_path: Path) -> None:
    doc, index = _linked(tmp_path)
    graph = ModelGraph(doc, results=index)
    assert graph.layers == ["model", "topology", "results"]
    assert graph.unavailable == {}
    assert graph.results_state == "fresh"
    without = ModelGraph(doc)
    assert "results" not in without.layers
    assert "results" in without.unavailable
    assert without.results_state is None


def test_results_nodes_join_their_object_by_result_link(tmp_path: Path) -> None:
    doc, index = _linked(tmp_path)
    sub = ModelGraph(doc, results=index).neighbourhood(DX_COIL, hops=1, max_nodes=500)
    start = sub.start
    facts = [n for n in sub.nodes if n.kind == "result_fact"]
    messages = [n for n in sub.nodes if n.kind == "message"]
    assert facts
    assert messages
    assert all(n.layer == "results" and n.key == DX_COIL for n in facts)
    assert all(n.id.startswith("fact:COIL:COOLING:DX:SINGLESPEED:TOP EAST OA DX COIL:") for n in facts)
    assert {n.attrs["message_kind"] for n in messages} == {"dxcoil.low_outlet_temp"}
    links = [e for e in sub.edges if e.kind == "result_link"]
    assert links
    assert all(e.layer == "results" and e.target == start for e in links)
    assert {e.attrs["confidence"] for e in links} <= {"exact", "typed", "convention", "weak"}
    assert sub.results_state == "fresh"
    assert all(n.attrs["stale"] is False for n in facts + messages)


def test_result_nodes_walk_back_to_their_owner(tmp_path: Path) -> None:
    doc, index = _linked(tmp_path)
    graph = ModelGraph(doc, results=index)
    sub = graph.neighbourhood(DX_COIL, hops=2, max_nodes=2000, node_kinds=["object", "message"])
    message_ids = {n.id for n in sub.nodes if n.kind == "message"}
    assert message_ids
    assert {e.source for e in sub.edges if e.kind == "result_link"} == message_ids


def test_stale_results_are_walked_and_marked(tmp_path: Path) -> None:
    doc, index = _linked(tmp_path)
    next(iter(doc["Zone"])).multiplier = 3
    graph = ModelGraph(doc, results=index)
    assert graph.results_state == "stale"
    sub = graph.neighbourhood(DX_COIL, hops=1, max_nodes=500)
    results = [n for n in sub.nodes if n.layer == "results"]
    assert results
    assert all(n.attrs["stale"] is True for n in results)
    assert sub.results_state == "stale"


def test_results_kinds_can_be_filtered_out(tmp_path: Path) -> None:
    doc, index = _linked(tmp_path)
    graph = ModelGraph(doc, results=index)
    sub = graph.neighbourhood(DX_COIL, hops=1, edge_kinds=["reference", "flow", "control", "membership"])
    assert all(n.layer != "results" for n in sub.nodes)
    sub = graph.neighbourhood(DX_COIL, hops=1, node_kinds=["object", "node"])
    assert all(n.layer != "results" for n in sub.nodes)


def test_node_link_export_carries_the_results_layer(tmp_path: Path) -> None:
    doc, index = _linked(tmp_path)
    data = ModelGraph(doc, results=index).to_node_link()
    graph = data["graph"]
    assert isinstance(graph, dict)
    assert graph["layers"] == ["model", "topology", "results"]
    assert graph["unavailable"] == {}
    assert graph["results_state"] == "fresh"
    nodes = data["nodes"]
    edges = data["edges"]
    assert isinstance(nodes, list)
    assert isinstance(edges, list)
    kinds = {n["kind"] for n in nodes if isinstance(n, dict)}
    assert {"result_fact", "message"} <= kinds
    fact = next(n for n in nodes if isinstance(n, dict) and n["kind"] == "result_fact")
    assert {"object_type", "name", "metric", "value", "units", "source", "where", "multiplier", "stale"} <= set(fact)
    ids = {n["id"] for n in nodes if isinstance(n, dict)}
    links = [e for e in edges if isinstance(e, dict) and e["kind"] == "result_link"]
    assert links
    assert all(e["source"] in ids and e["target"] in ids for e in links)
    assert all({"confidence", "rule"} <= set(e) for e in links)
