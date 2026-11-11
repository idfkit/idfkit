"""``IDFDocument.rename_node``: one pass over every field and ``NodeList`` entry that names a node.

A node is a name shared by fields, not an object, so ``rename`` cannot reach it. ``rename_node``
rewrites every node field the HVAC topology finds naming the node, and every ``NodeList`` entry
naming it, through the normal field-write path, atomically, and refuses to merge two nodes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from idfkit import IDFDocument, load_idf, new_document, write_idf
from idfkit.hvac import HVACTopology, NodeRenameResult, NodeUse, ObjectKey, check_topology
from idfkit.objects import IDFObject

LINKED = Path(__file__).parent / "fixtures" / "simulation" / "linked"

MIXED_AIR = "Mixed Air Node 1"
NEW_MIXED_AIR = "AHU-1 Mixed Air"
SETPOINT_LIST = "Main Branch SetPoint Node List"
OA_INLET = "Outside Air Inlet Node 1"
OA_INLET_LIST = "OutsideAirInletNodes"
SUPPLY_OUTLET = "VAV Sys 1 Outlet Node"


@pytest.fixture
def five_zone() -> IDFDocument:
    return load_idf(str(LINKED / "5ZoneAirCooled.idf"))


# --------------------------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------------------------- #


def _obj(doc: IDFDocument, key: ObjectKey) -> IDFObject:
    obj = doc.get_collection(key.object_type).get(key.name)
    assert obj is not None
    return obj


def _field_values(doc: IDFDocument, use: NodeUse) -> list[str]:
    """Every value the use's field holds on its object (one per extensible group for ``group.field``)."""
    obj = _obj(doc, use.object)
    if "." in use.field:
        wrapper, key = use.field.split(".", 1)
        return [str(item.get(key, "") or "") for item in obj.extensible_items(wrapper)]
    return [str(obj.data.get(use.field, "") or "")]


def _nodelist_entries(doc: IDFDocument, name: str) -> list[str]:
    return [str(item.get("node_name", "") or "") for item in doc["NodeList"][name].extensible_items("nodes")]


def _holds(values: list[str], node: str) -> bool:
    return any(v.upper() == node.upper() for v in values)


def _versions(doc: IDFDocument) -> dict[int, int]:
    return {id(o): o.mutation_version for o in doc.all_objects}


# --------------------------------------------------------------------------------------------- #
# The canonical rename
# --------------------------------------------------------------------------------------------- #


def test_canonical_rename_rewrites_every_use(five_zone: IDFDocument) -> None:
    before = HVACTopology.from_document(five_zone).uses(MIXED_AIR)
    # 5 direct fields (Branch x2, cooling coil, OA controller, OA mixer) + 1 via the setpoint NodeList.
    assert len(before) == 6

    result = five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    assert isinstance(result, NodeRenameResult)
    assert result.old == MIXED_AIR
    assert result.new == NEW_MIXED_AIR
    # 5 direct node fields + 1 NodeList entry == the number of uses reported before.
    assert result.fields_updated == len(before) == 6

    topo = HVACTopology.from_document(five_zone)
    after = topo.uses(NEW_MIXED_AIR)
    assert len(after) == len(before)
    assert {(u.object, u.field, u.via_nodelist) for u in after} == {(u.object, u.field, u.via_nodelist) for u in before}
    assert all(u.node == NEW_MIXED_AIR for u in after)
    assert NEW_MIXED_AIR in topo.nodes()
    assert all(n.upper() != MIXED_AIR.upper() for n in topo.nodes())
    with pytest.raises(KeyError):
        topo.uses(MIXED_AIR)

    for use in before:
        if use.via_nodelist is None:
            values = _field_values(five_zone, use)
            assert _holds(values, NEW_MIXED_AIR)
            assert not _holds(values, MIXED_AIR)


def test_result_lists_each_changed_object_once(five_zone: IDFDocument) -> None:
    result = five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    assert len(result.objects) == len(set(result.objects))
    assert set(result.objects) == {
        ObjectKey("Branch", "VAV Sys 1 Main Branch"),
        ObjectKey("Coil:Cooling:Water", "Main Cooling Coil 1"),
        ObjectKey("Controller:OutdoorAir", "OA Controller 1"),
        ObjectKey("OutdoorAir:Mixer", "OA Mixing Box 1"),
        ObjectKey("NodeList", SETPOINT_LIST),
    }
    assert ObjectKey("SetpointManager:MixedAir", "Mixed Air Temp Manager 1") not in result.objects


def test_rename_introduces_no_new_topology_finding(five_zone: IDFDocument) -> None:
    def signature(doc: IDFDocument) -> set[tuple[str, tuple[ObjectKey, ...], str | None]]:
        return {(f.code, f.objects, f.field) for f in check_topology(doc)}

    before = signature(five_zone)
    five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)
    assert signature(five_zone) - before == set()


def test_revision_moves(five_zone: IDFDocument) -> None:
    before = five_zone.revision
    five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)
    assert five_zone.revision > before


# --------------------------------------------------------------------------------------------- #
# NodeLists
# --------------------------------------------------------------------------------------------- #


def test_setpoint_nodelist_entry_is_rewritten_and_the_list_reference_is_not(five_zone: IDFDocument) -> None:
    spm = five_zone["SetpointManager:MixedAir"]["Mixed Air Temp Manager 1"]
    spm_version = spm.mutation_version

    five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    assert _nodelist_entries(five_zone, SETPOINT_LIST) == [
        NEW_MIXED_AIR,
        "Main Cooling Coil 1 Outlet Node",
        "Main Heating Coil 1 Outlet Node",
    ]
    assert spm.data["setpoint_node_or_nodelist_name"] == SETPOINT_LIST
    assert spm.mutation_version == spm_version

    via = [u for u in HVACTopology.from_document(five_zone).uses(NEW_MIXED_AIR) if u.via_nodelist is not None]
    assert [(u.object, u.field, u.via_nodelist) for u in via] == [
        (
            ObjectKey("SetpointManager:MixedAir", "Mixed Air Temp Manager 1"),
            "setpoint_node_or_nodelist_name",
            SETPOINT_LIST,
        )
    ]


def test_outdoor_air_nodelist_entry_is_rewritten(five_zone: IDFDocument) -> None:
    before = HVACTopology.from_document(five_zone).uses(OA_INLET)
    assert len(before) == 4
    oa_list = five_zone["OutdoorAir:NodeList"][0]
    oa_list_items = [dict(i) for i in oa_list.extensible_items()]
    oa_list_version = oa_list.mutation_version

    result = five_zone.rename_node(OA_INLET, "AHU-1 OA Inlet")

    assert _nodelist_entries(five_zone, OA_INLET_LIST) == ["AHU-1 OA Inlet"]
    # The OutdoorAir:NodeList names the list, not the node: it is untouched.
    assert [dict(i) for i in oa_list.extensible_items()] == oa_list_items
    assert oa_list.mutation_version == oa_list_version
    # 3 direct fields + 1 NodeList entry.
    assert result.fields_updated == 4
    assert set(result.objects) == {
        ObjectKey("AvailabilityManager:LowTemperatureTurnOff", "CW Low Temp Limit"),
        ObjectKey("Coil:Heating:Water", "OA Heating Coil 1"),
        ObjectKey("Controller:OutdoorAir", "OA Controller 1"),
        ObjectKey("NodeList", OA_INLET_LIST),
    }
    assert len(HVACTopology.from_document(five_zone).uses("AHU-1 OA Inlet")) == len(before)


# --------------------------------------------------------------------------------------------- #
# Branch, setpoint manager and unclassified fields
# --------------------------------------------------------------------------------------------- #


def test_branch_component_and_setpoint_manager_fields_are_rewritten(five_zone: IDFDocument) -> None:
    before = HVACTopology.from_document(five_zone).uses(SUPPLY_OUTLET)
    assert len(before) == 6

    result = five_zone.rename_node(SUPPLY_OUTLET, "AHU-1 Supply Outlet")

    assert result.fields_updated == 6
    branch = five_zone["Branch"]["VAV Sys 1 Main Branch"]
    assert branch.extensible_items()[-1]["component_outlet_node_name"] == "AHU-1 Supply Outlet"
    scheduled = five_zone["SetpointManager:Scheduled"]["Supply Air Temp Manager 1"]
    assert scheduled.data["setpoint_node_or_nodelist_name"] == "AHU-1 Supply Outlet"
    mixed = five_zone["SetpointManager:MixedAir"]["Mixed Air Temp Manager 1"]
    assert mixed.data["reference_setpoint_node_name"] == "AHU-1 Supply Outlet"
    assert mixed.data["fan_outlet_node_name"] == "AHU-1 Supply Outlet"
    assert ObjectKey("Branch", "VAV Sys 1 Main Branch") in result.objects
    assert ObjectKey("SetpointManager:Scheduled", "Supply Air Temp Manager 1") in result.objects


def test_branch_inlet_and_outlet_on_one_branch_count_twice_object_once(five_zone: IDFDocument) -> None:
    result = five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    items = five_zone["Branch"]["VAV Sys 1 Main Branch"].extensible_items()
    assert items[0]["component_outlet_node_name"] == NEW_MIXED_AIR
    assert items[1]["component_inlet_node_name"] == NEW_MIXED_AIR
    assert result.objects.count(ObjectKey("Branch", "VAV Sys 1 Main Branch")) == 1


def test_unclassified_node_field_is_rewritten() -> None:
    doc = new_document()
    doc.add(
        "Coil:Heating:Electric",
        "Heater",
        air_inlet_node_name="UV Mixed Air",
        air_outlet_node_name="UV Heated Air",
        validate=False,
    )
    doc.add("ZoneHVAC:UnitVentilator", "UV", mixed_air_node_name="UV Mixed Air", validate=False)
    uses = HVACTopology.from_document(doc).uses("UV Mixed Air")
    assert any(u.connection is None and u.object == ObjectKey("ZoneHVAC:UnitVentilator", "UV") for u in uses)

    result = doc.rename_node("UV Mixed Air", "UV Mixed")

    assert result.fields_updated == 2
    assert doc["ZoneHVAC:UnitVentilator"]["UV"].data["mixed_air_node_name"] == "UV Mixed"
    assert doc["Coil:Heating:Electric"]["Heater"].data["air_inlet_node_name"] == "UV Mixed"
    assert set(result.objects) == {
        ObjectKey("Coil:Heating:Electric", "Heater"),
        ObjectKey("ZoneHVAC:UnitVentilator", "UV"),
    }


# --------------------------------------------------------------------------------------------- #
# Case-insensitive matching
# --------------------------------------------------------------------------------------------- #


def test_old_name_matches_case_insensitively(five_zone: IDFDocument) -> None:
    result = five_zone.rename_node(MIXED_AIR.lower(), NEW_MIXED_AIR)

    assert result.fields_updated == 6
    topo = HVACTopology.from_document(five_zone)
    assert len(topo.uses(NEW_MIXED_AIR)) == 6
    with pytest.raises(KeyError):
        topo.uses(MIXED_AIR)


def test_fields_spelled_differently_in_the_model_are_all_rewritten(five_zone: IDFDocument) -> None:
    coil = five_zone["Coil:Cooling:Water"]["Main Cooling Coil 1"]
    coil.air_inlet_node_name = MIXED_AIR.upper()
    five_zone["NodeList"][SETPOINT_LIST].extensible_items()[0]["node_name"] = MIXED_AIR.lower()

    result = five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    assert result.fields_updated == 6
    assert coil.data["air_inlet_node_name"] == NEW_MIXED_AIR
    assert _nodelist_entries(five_zone, SETPOINT_LIST)[0] == NEW_MIXED_AIR
    assert len(HVACTopology.from_document(five_zone).uses(NEW_MIXED_AIR)) == 6


# --------------------------------------------------------------------------------------------- #
# Change notifications
# --------------------------------------------------------------------------------------------- #


def test_every_changed_object_is_marked_mutated_and_no_other(five_zone: IDFDocument) -> None:
    versions = _versions(five_zone)

    result = five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    changed = {ObjectKey(o.obj_type, o.name) for o in five_zone.all_objects if o.mutation_version != versions[id(o)]}
    assert changed == set(result.objects)


def test_cached_topology_is_not_served_after_the_rename(five_zone: IDFDocument) -> None:
    stale = HVACTopology.from_document(five_zone)

    five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    fresh = HVACTopology.from_document(five_zone)
    assert fresh is not stale
    assert len(fresh.uses(NEW_MIXED_AIR)) == 6


def test_written_idf_carries_the_new_name(five_zone: IDFDocument) -> None:
    """The writer regenerates each rewritten object instead of echoing its preserved source text."""
    result = five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    text = write_idf(five_zone)
    assert text.count(NEW_MIXED_AIR) == result.fields_updated


# --------------------------------------------------------------------------------------------- #
# Errors leave the document unchanged
# --------------------------------------------------------------------------------------------- #


def _assert_untouched(doc: IDFDocument, revision: int, versions: dict[int, int]) -> None:
    assert doc.revision == revision
    assert _versions(doc) == versions
    assert len(HVACTopology.from_document(doc).uses(MIXED_AIR)) == 6


def test_unknown_node_raises_key_error(five_zone: IDFDocument) -> None:
    revision, versions = five_zone.revision, _versions(five_zone)

    with pytest.raises(KeyError):
        five_zone.rename_node("No Such Node", "Anything")

    _assert_untouched(five_zone, revision, versions)


def test_object_name_that_is_not_a_node_raises_key_error(five_zone: IDFDocument) -> None:
    revision, versions = five_zone.revision, _versions(five_zone)

    with pytest.raises(KeyError):
        five_zone.rename_node("Main Cooling Coil 1", "Anything")

    _assert_untouched(five_zone, revision, versions)


@pytest.mark.parametrize(
    "new",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="whitespace"),
        pytest.param(MIXED_AIR, id="same"),
        pytest.param(MIXED_AIR.upper(), id="same-other-case"),
        pytest.param("Main Cooling Coil 1 Outlet Node", id="existing-node"),
        pytest.param("main cooling coil 1 outlet node", id="existing-node-other-case"),
        pytest.param(OA_INLET, id="existing-node-via-nodelist"),
    ],
)
def test_invalid_new_name_raises_value_error(five_zone: IDFDocument, new: str) -> None:
    revision, versions = five_zone.revision, _versions(five_zone)

    with pytest.raises(ValueError, match=r"."):
        five_zone.rename_node(MIXED_AIR, new)

    _assert_untouched(five_zone, revision, versions)


# --------------------------------------------------------------------------------------------- #
# Atomicity
# --------------------------------------------------------------------------------------------- #


class _WriteFailedError(RuntimeError):
    pass


def test_failed_write_leaves_nothing_half_renamed(five_zone: IDFDocument, monkeypatch: pytest.MonkeyPatch) -> None:
    before = HVACTopology.from_document(five_zone).uses(MIXED_AIR)
    target = five_zone["Controller:OutdoorAir"]["OA Controller 1"]
    original = IDFObject._set_field  # pyright: ignore[reportPrivateUsage]

    def failing(self: IDFObject, python_key: str, value: Any) -> None:
        if self is target and value == NEW_MIXED_AIR:
            raise _WriteFailedError(python_key)
        original(self, python_key, value)

    monkeypatch.setattr(IDFObject, "_set_field", failing)

    with pytest.raises(_WriteFailedError):
        five_zone.rename_node(MIXED_AIR, NEW_MIXED_AIR)

    monkeypatch.undo()

    for use in before:
        if use.via_nodelist is None:
            values = _field_values(five_zone, use)
            assert _holds(values, MIXED_AIR), use
            assert not _holds(values, NEW_MIXED_AIR), use
    assert _nodelist_entries(five_zone, SETPOINT_LIST)[0] == MIXED_AIR

    topo = HVACTopology(five_zone)
    assert len(topo.uses(MIXED_AIR)) == len(before)
    with pytest.raises(KeyError):
        topo.uses(NEW_MIXED_AIR)
