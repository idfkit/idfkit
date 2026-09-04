"""Tests for ReferenceGraph class."""

from __future__ import annotations

from idfkit import IDFDocument, new_document
from idfkit.objects import IDFObject
from idfkit.references import ReferenceGraph


class TestReferenceGraphRegister:
    def test_register_single(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1", data={"zone_name": "Z1"})
        graph.register(obj, "zone_name", "Z1")
        refs = graph.get_referencing("Z1")
        assert obj in refs

    def test_register_empty_name_ignored(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "")
        assert len(graph) == 0

    def test_register_multiple_references(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.register(obj, "schedule_name", "S1")
        refs = graph.get_references(obj)
        assert "Z1" in refs
        assert "S1" in refs

    def test_register_object_list(self) -> None:
        graph = ReferenceGraph()
        graph.register_object_list("ZoneNames", "Zone")
        stats = graph.stats()
        assert stats["object_lists"] == 1


class TestReferenceGraphLookup:
    def test_get_referencing(self, reference_graph: ReferenceGraph) -> None:
        refs = reference_graph.get_referencing("Zone1")
        assert len(refs) == 2

    def test_get_referencing_case_insensitive(self, reference_graph: ReferenceGraph) -> None:
        refs1 = reference_graph.get_referencing("Zone1")
        refs2 = reference_graph.get_referencing("zone1")
        refs3 = reference_graph.get_referencing("ZONE1")
        assert refs1 == refs2 == refs3

    def test_get_referencing_nonexistent(self, reference_graph: ReferenceGraph) -> None:
        refs = reference_graph.get_referencing("DoesNotExist")
        assert len(refs) == 0

    def test_get_referencing_with_fields(self, reference_graph: ReferenceGraph) -> None:
        refs = reference_graph.get_referencing_with_fields("Zone1")
        assert len(refs) == 2
        for _obj, field in refs:
            assert field == "zone_name"

    def test_get_references(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.register(obj, "schedule_name", "S1")
        refs = graph.get_references(obj)
        assert refs == {"Z1", "S1"}

    def test_get_references_with_fields(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        refs = graph.get_references_with_fields(obj)
        assert ("Z1", "zone_name") in refs

    def test_get_references_unknown_object(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        refs = graph.get_references(obj)
        assert len(refs) == 0

    def test_is_referenced(self, reference_graph: ReferenceGraph) -> None:
        assert reference_graph.is_referenced("Zone1") is True
        assert reference_graph.is_referenced("Zone2") is True
        assert reference_graph.is_referenced("Zone3") is False


class TestReferenceGraphUnregister:
    def test_unregister(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.unregister(obj)
        assert len(graph.get_referencing("Z1")) == 0
        assert len(graph.get_references(obj)) == 0

    def test_unregister_cleans_empty_refs(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.unregister(obj)
        assert not graph.is_referenced("Z1")

    def test_unregister_unknown_object(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        # Should not raise
        graph.unregister(obj)


class TestReferenceGraphDanglingReferences:
    def test_no_dangling(self, reference_graph: ReferenceGraph) -> None:
        valid_names = {"ZONE1", "ZONE2"}
        dangling = list(reference_graph.get_dangling_references(valid_names))
        assert len(dangling) == 0

    def test_with_dangling(self, reference_graph: ReferenceGraph) -> None:
        valid_names = {"ZONE1"}  # Zone2 not valid
        dangling = list(reference_graph.get_dangling_references(valid_names))
        assert len(dangling) == 1
        _obj, field, name = dangling[0]
        assert name == "ZONE2"
        assert field == "zone_name"

    def test_all_dangling(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "NonexistentZone")
        dangling = list(graph.get_dangling_references(set()))
        assert len(dangling) == 1


class TestReferenceGraphMisc:
    def test_clear(self, reference_graph: ReferenceGraph) -> None:
        reference_graph.clear()
        assert len(reference_graph) == 0
        assert reference_graph.stats()["total_references"] == 0

    def test_len(self, reference_graph: ReferenceGraph) -> None:
        assert len(reference_graph) == 3  # 3 registrations

    def test_stats(self, reference_graph: ReferenceGraph) -> None:
        stats = reference_graph.stats()
        assert stats["total_references"] == 3
        assert stats["objects_with_references"] == 3
        assert stats["names_referenced"] == 2


class TestReferenceGraphRenameTarget:
    def test_rename_target_updates_referenced_by(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "OldZone")
        graph.rename_target("OldZone", "NewZone")
        assert graph.is_referenced("NewZone")
        assert not graph.is_referenced("OldZone")

    def test_rename_target_updates_references(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "OldZone")
        graph.rename_target("OldZone", "NewZone")
        refs = graph.get_references(obj)
        assert "NEWZONE" in refs
        assert "OLDZONE" not in refs

    def test_rename_target_multiple_referrers(self) -> None:
        graph = ReferenceGraph()
        obj_a = IDFObject(obj_type="People", name="P1")
        obj_b = IDFObject(obj_type="Lights", name="L1")
        graph.register(obj_a, "zone_name", "Z1")
        graph.register(obj_b, "zone_name", "Z1")
        graph.rename_target("Z1", "Z1_Renamed")
        refs = graph.get_referencing("Z1_Renamed")
        assert obj_a in refs
        assert obj_b in refs
        assert not graph.is_referenced("Z1")

    def test_rename_target_noop_same_name(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.rename_target("Z1", "Z1")
        assert graph.is_referenced("Z1")

    def test_rename_target_nonexistent_is_noop(self) -> None:
        graph = ReferenceGraph()
        graph.rename_target("NoSuchName", "Whatever")
        assert len(graph) == 0

    def test_rename_target_merges_with_existing(self) -> None:
        graph = ReferenceGraph()
        obj_a = IDFObject(obj_type="People", name="P1")
        obj_b = IDFObject(obj_type="Lights", name="L1")
        graph.register(obj_a, "zone_name", "Z1")
        graph.register(obj_b, "zone_name", "Z2")
        # Rename Z1 -> Z2 should merge
        graph.rename_target("Z1", "Z2")
        refs = graph.get_referencing("Z2")
        assert obj_a in refs
        assert obj_b in refs


class TestReferenceGraphUpdateReference:
    def test_update_reference_basic(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.update_reference(obj, "zone_name", "Z1", "Z2")
        assert graph.is_referenced("Z2")
        assert not graph.is_referenced("Z1")
        refs = graph.get_references(obj)
        assert "Z2" in refs
        assert "Z1" not in refs

    def test_update_reference_old_none(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.update_reference(obj, "zone_name", None, "Z1")
        assert graph.is_referenced("Z1")

    def test_update_reference_new_none(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.update_reference(obj, "zone_name", "Z1", None)
        assert not graph.is_referenced("Z1")

    def test_update_reference_new_empty_string(self) -> None:
        graph = ReferenceGraph()
        obj = IDFObject(obj_type="People", name="P1")
        graph.register(obj, "zone_name", "Z1")
        graph.update_reference(obj, "zone_name", "Z1", "")
        assert not graph.is_referenced("Z1")


class TestExtensibleReferences:
    """Reference fields that live inside an extensible group are tracked like any other."""

    @staticmethod
    def _model() -> tuple[IDFDocument[bool], IDFObject]:
        doc = new_document(version=(26, 1, 0))
        doc.add("Zone", "Office")
        doc.add(
            "ElectricEquipment",
            name="Office Equipment",
            zone_or_zonelist_or_space_or_spacelist_name="Office",
            schedule_name="Always On",
            design_level_calculation_method="EquipmentLevel",
            design_level=100.0,
            validate=False,
        )
        manager = doc.add("DemandManager:ElectricEquipment", name="Mgr", limit_control="Fixed", selection_control="All")
        manager.equipment.append({"electric_equipment_name": "Office Equipment"})
        return doc, manager

    def test_a_group_reference_is_indexed(self) -> None:
        doc, manager = self._model()
        assert doc.references.get_referencing("Office Equipment") == {manager}

    def test_two_groups_naming_the_same_target_stay_two_edges(self) -> None:
        """Collapsing them would under-report the dangling check by one finding per repeat."""
        doc, manager = self._model()
        manager.equipment.append({"electric_equipment_name": "Office Equipment"})

        edges = doc.references.get_referencing_edges("Office Equipment")

        assert len(edges) == 2
        assert {index for _obj, _field, index in edges} == {0, 1}

    def test_editing_a_group_moves_the_edge(self) -> None:
        doc, manager = self._model()

        manager.equipment[0].electric_equipment_name = "Other Equipment"

        assert doc.references.get_referencing("Office Equipment") == set()
        assert doc.references.get_referencing("Other Equipment") == {manager}

    def test_renaming_a_target_rewrites_the_value_inside_the_group(self) -> None:
        doc, manager = self._model()

        doc.rename("ElectricEquipment", "Office Equipment", "Renamed Equipment")

        assert manager.equipment[0].electric_equipment_name == "Renamed Equipment"
        assert doc.references.get_referencing("Renamed Equipment") == {manager}
