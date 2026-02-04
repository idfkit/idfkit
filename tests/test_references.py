"""Tests for ReferenceGraph class."""

from __future__ import annotations

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
