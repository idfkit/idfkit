"""Tests for the node-link JSON export of the model graph (``idfkit.graph.node_link``).

The format is ``contracts/node-link-json.md`` of spec 014 (research R-24). Most tests use a small
hand-built document; one whole-export test and the ``nodelink`` test use the vendored reference
model ``benchmarks/fixtures/HospitalLowEnergy.idf.gz``.
"""

from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path
from typing import Any, cast

import pytest

# `benchmarks/` is not on the import path under pytest; add the repository root, as
# tests/test_perf_budgets.py does, to reuse its reference-model loader.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import idfkit  # noqa: E402
from benchmarks._timing import load_reference_model  # noqa: E402
from idfkit import IDFDocument, new_document  # noqa: E402
from idfkit.graph import NODE_LINK_FORMAT_VERSION, ModelGraph, ObjectKey, save_node_link, write_node_link  # noqa: E402

TOP_LEVEL_KEYS = {"directed", "multigraph", "graph", "nodes", "edges"}
GRAPH_KEYS = {
    "format",
    "format_version",
    "idfkit_version",
    "energyplus_version",
    "layers",
    "unavailable",
    "coverage",
    "scope",
    "results_state",
}
SCOPE_KEYS = {"start", "hops", "node_kinds", "edge_kinds", "categories"}
NODE_REQUIRED = {"id", "kind", "layer", "label"}
NODE_BY_KIND = {"object": {"object_type", "name", "category"}, "node": {"name", "fluid"}}
EDGE_REQUIRED = {"source", "target", "key", "kind", "layer"}
EDGE_BY_KIND = {
    "reference": {"field"},
    "flow": {"field", "connection_type", "fluid", "provenance"},
    "control": {"field", "connection_type", "provenance"},
    "membership": {"side", "branch", "position", "loop_kind"},
}
NODE_LAYERS = {"object": "model", "node": "topology"}
EDGE_LAYERS = {"reference": "model", "flow": "topology", "control": "topology", "membership": "topology"}

FAN = ObjectKey("Fan:ConstantVolume", "Fan")


# --------------------------------------------------------------------------------------------- #
# Fixtures and helpers
# --------------------------------------------------------------------------------------------- #


@pytest.fixture
def small_doc() -> IDFDocument:
    """A zone with a wall (reference edges) and a fan feeding a coil (flow edges through node B)."""
    doc = new_document()
    doc.add("Zone", "Office", validate=False)
    doc.add(
        "Material",
        "M1",
        roughness="Rough",
        thickness=0.1,
        conductivity=1.0,
        density=1000,
        specific_heat=1000,
        validate=False,
    )
    doc.add("Construction", "C1", outside_layer="M1", validate=False)
    doc.add(
        "BuildingSurface:Detailed",
        "Wall",
        surface_type="Wall",
        construction_name="C1",
        zone_name="Office",
        validate=False,
    )
    doc.add("Fan:ConstantVolume", "Fan", air_inlet_node_name="A", air_outlet_node_name="B", validate=False)
    doc.add("Coil:Heating:Electric", "Coil", air_inlet_node_name="B", air_outlet_node_name="C", validate=False)
    return doc


@pytest.fixture(scope="module")
def reference_export() -> dict[str, Any]:
    """The whole node-link export of the reference model, built once for the module."""
    return ModelGraph(load_reference_model()).to_node_link()


def _export(graph: ModelGraph, **kwargs: Any) -> dict[str, Any]:
    """``graph.to_node_link(**kwargs)``, typed loosely so tests can index into it."""
    return graph.to_node_link(**kwargs)


def _assert_json_values(value: object, path: str = "$") -> None:
    """Every value is a JSON scalar, a list of JSON values or a str-keyed dict of JSON values."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return
    if isinstance(value, list):
        for i, item in enumerate(cast("list[object]", value)):
            _assert_json_values(item, f"{path}[{i}]")
        return
    if isinstance(value, dict):
        for key, item in cast("dict[object, object]", value).items():
            assert isinstance(key, str), f"{path}: non-string key {key!r}"
            _assert_json_values(item, f"{path}.{key}")
        return
    pytest.fail(f"{path}: {type(value).__name__} is not a JSON value")


def _assert_structure(data: dict[str, Any]) -> None:
    """The structural guarantees of the contract: keys, unique ids, endpoints, keys by kind."""
    assert set(data) == TOP_LEVEL_KEYS
    assert "links" not in data
    assert data["directed"] is True
    assert data["multigraph"] is True
    assert set(data["graph"]) == GRAPH_KEYS
    assert set(data["graph"]["scope"]) == SCOPE_KEYS

    ids = [n["id"] for n in data["nodes"]]
    assert len(ids) == len(set(ids)), "node ids are not unique"
    known = set(ids)
    for node in data["nodes"]:
        assert set(node) >= NODE_REQUIRED, node
        assert NODE_BY_KIND.get(node["kind"], set()) <= set(node), node
        if node["kind"] in NODE_LAYERS:
            assert node["layer"] == NODE_LAYERS[node["kind"]]
    seen: set[tuple[str, str, str]] = set()
    for edge in data["edges"]:
        assert set(edge) >= EDGE_REQUIRED, edge
        assert EDGE_BY_KIND.get(edge["kind"], set()) <= set(edge), edge
        if edge["kind"] in EDGE_LAYERS:
            assert edge["layer"] == EDGE_LAYERS[edge["kind"]]
        assert edge["source"] in known, edge
        assert edge["target"] in known, edge
        triple = (edge["source"], edge["target"], edge["key"])
        assert triple not in seen, f"duplicate multigraph edge {triple}"
        seen.add(triple)


def _distances(data: dict[str, Any], start: str) -> dict[str, int]:
    """Hop distances from *start* over the export's edges, ignoring direction."""
    adjacency: dict[str, set[str]] = {}
    for edge in data["edges"]:
        adjacency.setdefault(edge["source"], set()).add(edge["target"])
        adjacency.setdefault(edge["target"], set()).add(edge["source"])
    depth = {start: 0}
    queue = deque([start])
    while queue:
        vid = queue.popleft()
        for other in adjacency.get(vid, ()):
            if other not in depth:
                depth[other] = depth[vid] + 1
                queue.append(other)
    return depth


# --------------------------------------------------------------------------------------------- #
# Serialisation
# --------------------------------------------------------------------------------------------- #


def test_write_node_link_round_trips_through_json(small_doc: IDFDocument) -> None:
    graph = ModelGraph(small_doc)
    text = write_node_link(graph)
    assert isinstance(text, str)
    assert json.loads(text) == _export(graph)


def test_write_node_link_passes_its_scope_arguments_through(small_doc: IDFDocument) -> None:
    graph = ModelGraph(small_doc)
    kwargs: dict[str, Any] = {"layers": ["model"], "node_kinds": ["object"], "edge_kinds": ["reference"]}
    assert json.loads(write_node_link(graph, **kwargs)) == _export(graph, **kwargs)
    assert json.loads(write_node_link(graph, start=FAN, hops=1)) == _export(graph, start=FAN, hops=1)


def test_every_value_is_a_json_value(small_doc: IDFDocument) -> None:
    _assert_json_values(_export(ModelGraph(small_doc)))


def test_save_node_link_writes_the_same_text_in_utf8(small_doc: IDFDocument, tmp_path: Path) -> None:
    small_doc.add("Zone", "Büro Ost", validate=False)
    graph = ModelGraph(small_doc)
    target = tmp_path / "graph.json"
    save_node_link(graph, target)
    assert target.read_bytes().decode("utf-8") == write_node_link(graph)
    assert "Büro Ost" in target.read_text(encoding="utf-8")


def test_save_node_link_accepts_a_string_path_and_scope(small_doc: IDFDocument, tmp_path: Path) -> None:
    graph = ModelGraph(small_doc)
    target = tmp_path / "scoped.json"
    save_node_link(graph, str(target), start=FAN, hops=2, layers=["model", "topology"])
    expected = write_node_link(graph, start=FAN, hops=2, layers=["model", "topology"])
    assert target.read_text(encoding="utf-8") == expected


# --------------------------------------------------------------------------------------------- #
# Structure and metadata
# --------------------------------------------------------------------------------------------- #


def test_small_export_meets_the_structural_contract(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc))
    _assert_structure(data)
    kinds = {e["kind"] for e in data["edges"]}
    assert {"reference", "flow"} <= kinds


def test_graph_metadata_values(small_doc: IDFDocument) -> None:
    meta = _export(ModelGraph(small_doc))["graph"]
    assert meta["format"] == "idfkit-model-graph"
    assert meta["format_version"] == NODE_LINK_FORMAT_VERSION == 1
    assert meta["idfkit_version"] == idfkit.__version__
    major, minor, patch = small_doc.version
    assert meta["energyplus_version"] == f"{major}.{minor}.{patch}"
    assert meta["layers"] == ["model", "topology"]
    assert meta["unavailable"] == {"results": "no ResultIndex was passed in"}
    assert meta["results_state"] is None
    assert set(meta["coverage"]) == {"partial", "uncovered"}
    assert isinstance(meta["coverage"]["partial"], bool)
    assert isinstance(meta["coverage"]["uncovered"], list)
    assert meta["scope"] == {"start": None, "hops": None, "node_kinds": None, "edge_kinds": None, "categories": None}


def test_asking_only_for_present_layers_leaves_nothing_unavailable(small_doc: IDFDocument) -> None:
    meta = _export(ModelGraph(small_doc), layers=["model", "topology"])["graph"]
    assert meta["layers"] == ["model", "topology"]
    assert meta["unavailable"] == {}
    assert meta["results_state"] is None


def test_object_and_node_entries_carry_their_identity(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc))
    by_id = {n["id"]: n for n in data["nodes"]}
    zone = by_id["object:ZONE:OFFICE"]
    assert (zone["kind"], zone["layer"], zone["object_type"], zone["name"]) == ("object", "model", "Zone", "Office")
    assert by_id["object:FAN:CONSTANTVOLUME:FAN"]["category"] == "fan"
    node_b = by_id["node:B"]
    assert (node_b["kind"], node_b["layer"], node_b["name"], node_b["fluid"]) == ("node", "topology", "B", "Air")


def test_ids_are_stable_across_exports(small_doc: IDFDocument) -> None:
    first = [n["id"] for n in _export(ModelGraph(small_doc))["nodes"]]
    second = [n["id"] for n in _export(ModelGraph(small_doc))["nodes"]]
    assert first == second


def test_scope_reflects_the_arguments(small_doc: IDFDocument) -> None:
    scope = _export(
        ModelGraph(small_doc), node_kinds=["object", "node"], edge_kinds=["reference", "flow"], start=FAN, hops=2
    )["graph"]["scope"]
    assert scope == {
        "start": "object:FAN:CONSTANTVOLUME:FAN",
        "hops": 2,
        "node_kinds": ["node", "object"],
        "edge_kinds": ["flow", "reference"],
        "categories": None,
    }


def test_scope_start_is_the_graph_node_id_of_a_node_name(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc), start="B", hops=0)
    assert data["graph"]["scope"]["start"] == "node:B"
    assert [n["id"] for n in data["nodes"]] == ["node:B"]
    assert data["edges"] == []


# --------------------------------------------------------------------------------------------- #
# start and hops
# --------------------------------------------------------------------------------------------- #


def test_start_without_hops_is_a_value_error(small_doc: IDFDocument) -> None:
    with pytest.raises(ValueError, match="together"):
        _export(ModelGraph(small_doc), start=FAN)


def test_hops_without_start_is_a_value_error(small_doc: IDFDocument) -> None:
    with pytest.raises(ValueError, match="together"):
        _export(ModelGraph(small_doc), hops=1)


def test_negative_hops_is_a_value_error(small_doc: IDFDocument) -> None:
    with pytest.raises(ValueError, match="hops"):
        _export(ModelGraph(small_doc), start=FAN, hops=-1)


def test_write_and_save_check_start_and_hops_too(small_doc: IDFDocument, tmp_path: Path) -> None:
    graph = ModelGraph(small_doc)
    with pytest.raises(ValueError):
        write_node_link(graph, start=FAN)
    with pytest.raises(ValueError):
        save_node_link(graph, tmp_path / "x.json", hops=1)
    assert not (tmp_path / "x.json").exists()


@pytest.mark.parametrize("hops", [0, 1, 2, 3])
def test_scoped_export_holds_exactly_the_nodes_within_reach(small_doc: IDFDocument, hops: int) -> None:
    graph = ModelGraph(small_doc)
    full = _export(graph)
    scoped = _export(graph, start=FAN, hops=hops)
    _assert_structure(scoped)
    start = "object:FAN:CONSTANTVOLUME:FAN"
    ids = {n["id"] for n in scoped["nodes"]}
    assert start in ids
    within = {vid for vid, d in _distances(full, start).items() if d <= hops}
    assert ids == within
    full_edges = {(e["source"], e["target"], e["key"]) for e in full["edges"]}
    scoped_edges = {(e["source"], e["target"], e["key"]) for e in scoped["edges"]}
    assert scoped_edges <= full_edges
    assert scoped_edges == {t for t in full_edges if t[0] in ids and t[1] in ids}


def test_scoped_export_from_a_reference_chain(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc), start=ObjectKey("Material", "M1"), hops=1)
    ids = {n["id"] for n in data["nodes"]}
    assert ids == {"object:MATERIAL:M1", "object:CONSTRUCTION:C1"}
    assert data["graph"]["scope"]["start"] == "object:MATERIAL:M1"
    assert data["graph"]["scope"]["hops"] == 1


def test_an_unknown_start_is_a_key_error(small_doc: IDFDocument) -> None:
    with pytest.raises(KeyError):
        _export(ModelGraph(small_doc), start=ObjectKey("Zone", "Nowhere"), hops=1)


# --------------------------------------------------------------------------------------------- #
# Filters
# --------------------------------------------------------------------------------------------- #


def test_model_layer_only_has_no_topology(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc), layers=["model"])
    _assert_structure(data)
    assert data["graph"]["layers"] == ["model"]
    assert data["graph"]["unavailable"] == {}
    assert data["nodes"]
    assert all(n["kind"] == "object" and n["layer"] == "model" for n in data["nodes"])
    assert data["edges"]
    assert all(e["kind"] == "reference" for e in data["edges"])


def test_topology_layer_only_has_no_objects_and_so_no_edges(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc), layers=["topology"])
    _assert_structure(data)
    assert data["graph"]["layers"] == ["topology"]
    assert {n["kind"] for n in data["nodes"]} == {"node"}
    assert data["edges"] == []


def test_results_layer_asked_for_is_unavailable(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc), layers=["results"])
    assert data["graph"]["layers"] == []
    assert data["graph"]["unavailable"] == {"results": "no ResultIndex was passed in"}
    assert data["nodes"] == []
    assert data["edges"] == []


def test_node_kinds_filter(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc), node_kinds=["object"])
    _assert_structure(data)
    assert {n["kind"] for n in data["nodes"]} == {"object"}
    # Flow edges have a fluid node at one end, so none survive without node nodes.
    assert {e["kind"] for e in data["edges"]} == {"reference"}
    assert data["graph"]["scope"]["node_kinds"] == ["object"]

    nodes_only = _export(ModelGraph(small_doc), node_kinds=["node"])
    assert {n["id"] for n in nodes_only["nodes"]} == {"node:A", "node:B", "node:C"}
    assert nodes_only["edges"] == []


def test_edge_kinds_filter_keeps_nodes_and_drops_other_edges(small_doc: IDFDocument) -> None:
    graph = ModelGraph(small_doc)
    full = _export(graph)
    flow_only = _export(graph, edge_kinds=["flow"])
    _assert_structure(flow_only)
    assert {n["id"] for n in flow_only["nodes"]} == {n["id"] for n in full["nodes"]}
    assert {e["kind"] for e in flow_only["edges"]} == {"flow"}
    assert len(flow_only["edges"]) == sum(1 for e in full["edges"] if e["kind"] == "flow")
    assert flow_only["graph"]["scope"]["edge_kinds"] == ["flow"]

    reference_only = _export(graph, edge_kinds=["reference"])
    assert {e["kind"] for e in reference_only["edges"]} == {"reference"}


def test_unknown_kinds_are_ignored(small_doc: IDFDocument) -> None:
    graph = ModelGraph(small_doc)
    data = _export(graph, node_kinds=["object", "verdict"], edge_kinds=["reference", "standard"])
    _assert_structure(data)
    assert {n["kind"] for n in data["nodes"]} == {"object"}
    assert {e["kind"] for e in data["edges"]} == {"reference"}


def test_filters_apply_to_a_scoped_export(small_doc: IDFDocument) -> None:
    data = _export(ModelGraph(small_doc), start=FAN, hops=3, layers=["model"])
    assert [n["id"] for n in data["nodes"]] == ["object:FAN:CONSTANTVOLUME:FAN"]
    assert data["edges"] == []


# --------------------------------------------------------------------------------------------- #
# Reference model
# --------------------------------------------------------------------------------------------- #


def test_reference_model_export_meets_the_contract(reference_export: dict[str, Any]) -> None:
    data = reference_export
    _assert_structure(data)
    _assert_json_values(data)
    assert json.loads(json.dumps(data, ensure_ascii=False)) == data
    assert {e["kind"] for e in data["edges"]} == {"reference", "flow", "control", "membership"}
    assert {n["kind"] for n in data["nodes"]} == {"object", "node"}
    for edge in data["edges"]:
        if edge["kind"] == "control" and "rule" in edge:
            assert edge["rule"] == "ems_key"
            assert edge["confidence"] == "convention"
    coverage = data["graph"]["coverage"]
    for part in coverage["uncovered"]:
        assert set(part) == {"kind", "count", "examples", "reason"}
        assert all(set(example) == {"object_type", "name"} for example in part["examples"])
    if coverage["uncovered"]:
        assert coverage["partial"] is True


@pytest.mark.nodelink
def test_networkx_reads_the_export_with_no_keyword_arguments(reference_export: dict[str, Any]) -> None:
    networkx = pytest.importorskip("networkx")
    data = reference_export
    loaded = networkx.node_link_graph(data)
    assert isinstance(loaded, networkx.MultiDiGraph)
    assert loaded.number_of_nodes() == len(data["nodes"])
    assert loaded.number_of_edges() == len(data["edges"])
