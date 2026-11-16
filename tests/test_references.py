"""Tests for ReferenceGraph class."""

from __future__ import annotations

from idfkit import IDFDocument, new_document
from idfkit.objects import IDFCollection, IDFObject
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


class TestCollectionReferencing:
    """``IDFCollection.referencing``: the reference graph narrowed to one type."""

    @staticmethod
    def _model() -> IDFDocument:
        doc = new_document()
        doc.add("Zone", "Office")
        doc.add("Zone", "Core")
        for name, zone in (("Office_Wall", "Office"), ("Office_Floor", "Office"), ("Core_Wall", "Core")):
            doc.add(
                "BuildingSurface:Detailed",
                name,
                surface_type="Wall",
                construction_name="",
                zone_name=zone,
                outside_boundary_condition="Outdoors",
                validate=False,
            )
        doc.add("Lights", "Office_Lights", zone_or_zonelist_or_space_or_spacelist_name="Office", validate=False)
        doc.add(
            "FenestrationSurface:Detailed",
            "Office_Window",
            surface_type="Window",
            construction_name="",
            building_surface_name="Office_Wall",
            validate=False,
        )
        return doc

    def test_keeps_only_the_collections_type(self) -> None:
        doc = self._model()
        assert {o.obj_type for o in doc.get_referencing("Office")} == {"BuildingSurface:Detailed", "Lights"}
        surfaces = doc["BuildingSurface:Detailed"].referencing("Office")
        assert {s.name for s in surfaces} == {"Office_Wall", "Office_Floor"}
        assert {o.name for o in doc["Lights"].referencing("Office")} == {"Office_Lights"}

    def test_returns_the_documents_own_objects(self) -> None:
        doc = self._model()
        (window,) = doc["FenestrationSurface:Detailed"].referencing(doc["BuildingSurface:Detailed"]["Office_Wall"])
        assert window is doc["FenestrationSurface:Detailed"]["Office_Window"]

    def test_takes_a_name_or_an_object_and_matches_names_case_insensitively(self) -> None:
        doc = self._model()
        zone = doc["Zone"]["Office"]
        surfaces = doc["BuildingSurface:Detailed"]
        assert (
            set(surfaces.referencing(zone))
            == set(surfaces.referencing("Office"))
            == set(surfaces.referencing("oFFICE"))
        )

    def test_the_type_name_is_matched_case_insensitively(self) -> None:
        doc = self._model()
        lower = doc.get_collection("buildingsurface:detailed").referencing("Office")
        assert set(lower) == set(doc["BuildingSurface:Detailed"].referencing("Office"))
        assert len(doc.building_surface_detaileds.referencing("Office")) == 2

    def test_nothing_references_an_unknown_or_empty_name(self) -> None:
        doc = self._model()
        assert doc["BuildingSurface:Detailed"].referencing("Nowhere") == []
        assert doc["BuildingSurface:Detailed"].referencing("") == []

    def test_a_type_with_no_objects_answers_empty(self) -> None:
        doc = self._model()
        assert doc["People"].referencing("Office") == []

    def test_follows_renames_edits_and_removals(self) -> None:
        doc = self._model()
        surfaces = doc["BuildingSurface:Detailed"]
        doc.rename("Zone", "Office", "Open_Office")
        assert {s.name for s in surfaces.referencing("Open_Office")} == {"Office_Wall", "Office_Floor"}
        assert surfaces.referencing("Office") == []
        surfaces["Office_Floor"].zone_name = "Core"
        assert {s.name for s in surfaces.referencing("Core")} == {"Core_Wall", "Office_Floor"}
        doc.removeidfobject(surfaces["Core_Wall"])
        assert {s.name for s in surfaces.referencing("Core")} == {"Office_Floor"}

    def test_a_surface_renamed_after_it_was_filed_is_still_found(self) -> None:
        doc = self._model()
        wall = doc["BuildingSurface:Detailed"]["Office_Wall"]
        wall.name = "Office_South_Wall"
        assert wall in doc["BuildingSurface:Detailed"].referencing("Office")

    def test_each_object_comes_once_however_many_fields_name_the_target(self) -> None:
        doc = self._model()
        wall = doc["BuildingSurface:Detailed"]["Office_Wall"]
        wall.outside_boundary_condition = "Zone"
        wall.outside_boundary_condition_object = "Office"
        assert [s.name for s in doc["BuildingSurface:Detailed"].referencing("Office")].count("Office_Wall") == 1

    def test_an_object_added_under_another_spelling_of_its_type_is_found(self) -> None:
        doc = self._model()
        odd = IDFObject(
            obj_type="BUILDINGSURFACE:DETAILED",
            name="Odd_Wall",
            data={"surface_type": "Wall", "zone_name": "Office", "outside_boundary_condition": "Outdoors"},
        )
        doc.addidfobject(odd)
        assert odd in doc.get_collection("BuildingSurface:Detailed")
        assert odd in doc["BuildingSurface:Detailed"].referencing("Office")

    def test_unnamed_objects_are_matched_by_type(self) -> None:
        doc = new_document()
        doc.add("Schedule:Constant", "Always", hourly_value=1, validate=False)
        doc.add("Output:Variable", key_value="*", variable_name="Zone Mean Air Temperature", schedule_name="Always")
        doc.add("Output:Meter", key_name="Electricity:Facility", reporting_frequency="Hourly")
        found = doc["Output:Variable"].referencing("Always")
        assert [o.variable_name for o in found] == ["Zone Mean Air Temperature"]
        assert doc["Output:Meter"].referencing("Always") == []

    def test_a_copy_answers_from_its_own_graph(self) -> None:
        doc = self._model()
        copy = doc.copy()
        copy.rename("Zone", "Office", "Renamed")
        assert len(copy["BuildingSurface:Detailed"].referencing("Renamed")) == 2
        assert len(doc["BuildingSurface:Detailed"].referencing("Office")) == 2
        found = copy["BuildingSurface:Detailed"].referencing("Renamed")
        assert all(s in copy["BuildingSurface:Detailed"] for s in found)
        assert not any(s is doc["BuildingSurface:Detailed"][s.name] for s in found)

    def test_a_deep_copy_answers_from_its_own_graph(self) -> None:
        import copy
        import pickle

        doc = self._model()
        for clone in (copy.deepcopy(doc), pickle.loads(pickle.dumps(doc))):  # noqa: S301
            clone.rename("Zone", "Office", "Renamed")
            assert len(clone["BuildingSurface:Detailed"].referencing("Renamed")) == 2
        assert len(doc["BuildingSurface:Detailed"].referencing("Office")) == 2

    def test_objects_outside_a_document_reference_nothing(self) -> None:
        collection: IDFCollection[IDFObject] = IDFCollection("Zone")
        assert collection.referencing("Office") == []
        collection.add(
            IDFObject(obj_type="Lights", name="L", data={"zone_or_zonelist_or_space_or_spacelist_name": "Z"})
        )
        assert collection.referencing("Z") == []

    def test_a_collection_built_by_hand_answers_only_for_its_own_objects(self) -> None:
        doc = self._model()
        subset: IDFCollection[IDFObject] = IDFCollection("BuildingSurface:Detailed")
        subset.add(doc["BuildingSurface:Detailed"]["Office_Wall"])
        assert [s.name for s in subset.referencing("Office")] == ["Office_Wall"]

    def test_a_document_pickled_before_referencing_existed_answers(self) -> None:
        import pickle

        doc = self._model()
        # A pickled collection carries only its own slots, so its state is the same as in idfkit
        # releases before this method existed; check that stays so.
        state = doc["BuildingSurface:Detailed"].__reduce_ex__(2)[2]
        assert set(state[1]) == {"_by_name", "_items", "_type"}
        clone = pickle.loads(pickle.dumps(doc))  # noqa: S301
        assert len(clone["BuildingSurface:Detailed"].referencing("Office")) == 2
