"""Tests for IDFDocument class."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import IDFDocument, load_idf, new_document
from idfkit.cst import DocumentCST
from idfkit.exceptions import DuplicateObjectError, ValidationFailedError
from idfkit.objects import IDFCollection, IDFObject


class TestIDFDocumentInit:
    def test_default_version(self) -> None:
        from idfkit.versions import LATEST_VERSION

        doc = IDFDocument()
        assert doc.version == LATEST_VERSION

    def test_custom_version(self) -> None:
        doc = IDFDocument(version=(24, 1, 0))
        assert doc.version == (24, 1, 0)

    def test_filepath(self, tmp_path: Path) -> None:
        p = tmp_path / "test.idf"
        doc = IDFDocument(filepath=str(p))
        assert doc.filepath is not None
        assert str(doc.filepath) == str(p)

    def test_filepath_none(self) -> None:
        doc = IDFDocument()
        assert doc.filepath is None

    def test_schema_property(self, empty_doc: IDFDocument) -> None:
        assert empty_doc.schema is not None

    def test_collections_property(self) -> None:
        doc = IDFDocument()
        assert doc.collections == {}

    def test_references_property(self) -> None:
        doc = IDFDocument()
        assert doc.references is not None


class TestIDFDocumentCollectionAccess:
    def test_getitem_creates_empty_collection(self) -> None:
        doc = IDFDocument()
        coll = doc["Zone"]
        assert isinstance(coll, IDFCollection)
        assert len(coll) == 0

    def test_getitem_returns_same_collection(self) -> None:
        doc = IDFDocument()
        coll1 = doc["Zone"]
        coll2 = doc["Zone"]
        assert coll1 is coll2

    def test_getattr_python_alias(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "TestZone")
        zones = empty_doc.zones
        assert isinstance(zones, IDFCollection)
        assert len(zones) == 1

    def test_getattr_private_raises(self) -> None:
        doc = IDFDocument()
        with pytest.raises(AttributeError):
            _ = doc._something

    def test_getattr_dynamic_matching(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "TestZone")
        # Accessing via case-insensitive matching of existing collections
        coll = empty_doc.zone
        assert isinstance(coll, IDFCollection)

    def test_contains_existing_type(self, simple_doc: IDFDocument) -> None:
        assert "Zone" in simple_doc

    def test_contains_missing_type(self, simple_doc: IDFDocument) -> None:
        assert "NonexistentType" not in simple_doc

    def test_iter(self, simple_doc: IDFDocument) -> None:
        types = list(simple_doc)
        assert "Zone" in types
        assert "Material" in types

    def test_len(self, simple_doc: IDFDocument) -> None:
        assert len(simple_doc) > 0

    def test_len_empty(self) -> None:
        doc = IDFDocument()
        assert len(doc) == 0


class TestIDFDocumentObjectManipulation:
    def test_add_with_data_dict(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.add("Zone", "MyZone", {"x_origin": 10.0})
        assert obj.name == "MyZone"
        assert obj.x_origin == 10.0

    def test_add_with_kwargs(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.add("Zone", "MyZone", x_origin=10.0)
        assert obj.x_origin == 10.0

    def test_add_with_data_and_kwargs(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.add("Zone", "MyZone", {"x_origin": 10.0}, y_origin=20.0)
        assert obj.x_origin == 10.0
        assert obj.y_origin == 20.0

    def test_add_sets_schema(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.add("Zone", "MyZone")
        assert obj.schema_dict is not None

    def test_newidfobject(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.newidfobject("Zone", Name="TestZone", x_origin=5.0)
        assert obj.name == "TestZone"

    def test_addidfobject(self, empty_doc: IDFDocument) -> None:
        obj = IDFObject(obj_type="Zone", name="External")
        result = empty_doc.addidfobject(obj)
        assert result is obj
        assert len(empty_doc["Zone"]) == 1

    def test_addidfobjects(self, empty_doc: IDFDocument) -> None:
        objs = [
            IDFObject(obj_type="Zone", name="Z1"),
            IDFObject(obj_type="Zone", name="Z2"),
        ]
        results = empty_doc.addidfobjects(objs)
        assert len(results) == 2
        assert len(empty_doc["Zone"]) == 2

    def test_removeidfobject(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.add("Zone", "ToRemove")
        assert len(empty_doc["Zone"]) == 1
        empty_doc.removeidfobject(obj)
        assert len(empty_doc["Zone"]) == 0

    def test_removeidfobjects(self, empty_doc: IDFDocument) -> None:
        obj1 = empty_doc.add("Zone", "Z1")
        obj2 = empty_doc.add("Zone", "Z2")
        empty_doc.removeidfobjects([obj1, obj2])
        assert len(empty_doc["Zone"]) == 0

    def test_copyidfobject(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.add("Zone", "Original", {"x_origin": 5.0})
        copied = empty_doc.copyidfobject(obj, "CopiedZone")
        assert copied.name == "CopiedZone"
        assert copied.x_origin == 5.0
        assert len(empty_doc["Zone"]) == 2

    def test_copyidfobject_without_new_name(self, empty_doc: IDFDocument) -> None:
        obj = empty_doc.add("Zone", "Original")
        # Without a new name, it should raise DuplicateObjectError
        with pytest.raises(DuplicateObjectError):
            empty_doc.copyidfobject(obj)

    def test_getobject(self, simple_doc: IDFDocument) -> None:
        obj = simple_doc.getobject("Zone", "TestZone")
        assert obj is not None
        assert obj.name == "TestZone"

    def test_getobject_missing(self, simple_doc: IDFDocument) -> None:
        obj = simple_doc.getobject("Zone", "Nonexistent")
        assert obj is None

    def test_getobject_missing_type(self, simple_doc: IDFDocument) -> None:
        obj = simple_doc.getobject("Nonexistent", "X")
        assert obj is None


class TestIDFDocumentSingletons:
    def test_duplicate_seeded_building_raises(self) -> None:
        doc = new_document(version=(24, 1, 0))
        with pytest.raises(DuplicateObjectError):
            doc.add("Building", "OtherBuilding")

    def test_duplicate_seeded_global_geometry_rules_raises(self) -> None:
        doc = new_document(version=(24, 1, 0))
        with pytest.raises(DuplicateObjectError):
            doc.add(
                "GlobalGeometryRules",
                starting_vertex_position="UpperLeftCorner",
                vertex_entry_direction="Counterclockwise",
                coordinate_system="Relative",
            )

    def test_duplicate_non_seeded_singleton_raises(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Timestep", number_of_timesteps_per_hour=4)
        with pytest.raises(DuplicateObjectError):
            empty_doc.add("Timestep", number_of_timesteps_per_hour=6)

    def test_singleton_duplicate_check_is_case_insensitive(self) -> None:
        doc = new_document(version=(24, 1, 0))
        with pytest.raises(DuplicateObjectError):
            doc.add("building", "OtherBuilding")

    def test_non_singleton_still_allows_multiple(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "Z1")
        empty_doc.add("Zone", "Z2")
        assert len(empty_doc["Zone"]) == 2


class TestIDFDocumentRename:
    def test_rename_basic(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "OldName")
        empty_doc.rename("Zone", "OldName", "NewName")
        assert empty_doc.getobject("Zone", "NewName") is not None
        assert empty_doc.getobject("Zone", "OldName") is None

    def test_rename_updates_references(self, simple_doc: IDFDocument) -> None:
        simple_doc.rename("Zone", "TestZone", "RenamedZone")
        # The surfaces that referenced "TestZone" should now reference "RenamedZone"
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        assert wall.zone_name == "RenamedZone"

    def test_rename_nonexistent_raises(self, empty_doc: IDFDocument) -> None:
        with pytest.raises(KeyError):
            empty_doc.rename("Zone", "Nonexistent", "New")


class TestIDFDocumentSchedules:
    def test_get_schedule(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Schedule:Constant", "AlwaysOn", {"hourly_value": 1.0})
        sched = empty_doc.get_schedule("AlwaysOn")
        assert sched is not None
        assert sched.name == "AlwaysOn"

    def test_get_schedule_case_insensitive(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Schedule:Constant", "AlwaysOn", {"hourly_value": 1.0})
        assert empty_doc.get_schedule("alwayson") is not None
        assert empty_doc.get_schedule("ALWAYSON") is not None

    def test_get_schedule_missing(self, empty_doc: IDFDocument) -> None:
        assert empty_doc.get_schedule("Nonexistent") is None

    def test_schedules_cache_invalidation(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Schedule:Constant", "S1", {"hourly_value": 1.0})
        _ = empty_doc.schedules_dict  # populates cache
        empty_doc.add("Schedule:Constant", "S2", {"hourly_value": 0.5})
        # Cache should be invalidated
        assert "S2" in empty_doc.schedules_dict

    def test_get_used_schedules(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Schedule:Constant", "UsedSchedule", {"hourly_value": 1.0})
        empty_doc.add("Schedule:Constant", "UnusedSchedule", {"hourly_value": 0.5})
        empty_doc.add("Zone", "TestZone")
        # Using validate=False since we're only testing reference tracking, not full People validity
        empty_doc.add(
            "People",
            "TestPeople",
            {
                "zone_or_zonelist_or_space_or_spacelist_name": "TestZone",
                "number_of_people_schedule_name": "UsedSchedule",
            },
            validate=False,
        )
        used = empty_doc.get_used_schedules()
        assert "USEDSCHEDULE" in used


class TestIDFDocumentSurfaces:
    def test_getsurfaces_all(self, simple_doc: IDFDocument) -> None:
        surfaces = simple_doc.getsurfaces()
        assert len(surfaces) == 2

    def test_getsurfaces_by_type(self, simple_doc: IDFDocument) -> None:
        walls = simple_doc.getsurfaces("wall")
        assert len(walls) == 1
        assert walls[0].name == "TestWall"

    def test_getsurfaces_floor(self, simple_doc: IDFDocument) -> None:
        floors = simple_doc.getsurfaces("floor")
        assert len(floors) == 1
        assert floors[0].name == "TestFloor"

    def test_getsurfaces_no_match(self, simple_doc: IDFDocument) -> None:
        roofs = simple_doc.getsurfaces("roof")
        assert len(roofs) == 0


class TestIDFDocumentIteration:
    def test_all_objects(self, simple_doc: IDFDocument) -> None:
        all_objs = list(simple_doc.all_objects)
        assert len(all_objs) == len(simple_doc)
        assert all(isinstance(o, IDFObject) for o in all_objs)

    def test_objects_by_type(self, simple_doc: IDFDocument) -> None:
        pairs = list(simple_doc.objects_by_type())
        types = [t for t, _ in pairs]
        assert "Zone" in types
        assert "Material" in types


class TestIDFDocumentCopy:
    def test_copy(self, simple_doc: IDFDocument) -> None:
        copied = simple_doc.copy()
        assert copied is not simple_doc
        assert len(copied) == len(simple_doc)
        assert copied.version == simple_doc.version

    def test_copy_independence(self, simple_doc: IDFDocument) -> None:
        copied = simple_doc.copy()
        copied.add("Zone", "NewZone")
        assert len(copied["Zone"]) == 2
        assert len(simple_doc["Zone"]) == 1


class TestIDFDocumentStringRepresentation:
    def test_repr(self, empty_doc: IDFDocument) -> None:
        r = repr(empty_doc)
        assert "IDFDocument" in r
        assert "24.1.0" in r

    def test_str(self, simple_doc: IDFDocument) -> None:
        s = str(simple_doc)
        assert "IDFDocument" in s
        assert "Zone" in s


class TestIDFObjectsView:
    def test_idfobjects_access(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        zones = view["Zone"]
        assert len(zones) == 1

    def test_idfobjects_case_insensitive(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        zones = view["ZONE"]
        assert len(zones) == 1

    def test_idfobjects_contains(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        assert "Zone" in view
        assert "ZONE" in view
        assert "NonexistentType" not in view

    def test_idfobjects_iter(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        types = list(view)
        assert "Zone" in types

    def test_idfobjects_keys(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        keys = view.keys()
        assert isinstance(keys, list)
        assert "Zone" in keys

    def test_idfobjects_values(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        vals = view.values()
        assert all(isinstance(v, IDFCollection) for v in vals)

    def test_idfobjects_items(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        items = view.items()
        assert all(isinstance(k, str) and isinstance(v, IDFCollection) for k, v in items)

    def test_idfobjects_contains_non_string(self, simple_doc: IDFDocument) -> None:
        view = simple_doc.idfobjects
        assert 42 not in view


class TestNameChangeConsistency:
    """Verify that name changes via all code paths update collection index, referencing objects, and graph."""

    def test_name_setter_updates_collection_index(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone.name = "RenamedZone"
        assert simple_doc.getobject("Zone", "RenamedZone") is zone
        assert simple_doc.getobject("Zone", "TestZone") is None

    def test_name_setter_updates_referencing_objects(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone.name = "RenamedZone"
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        assert wall.zone_name == "RenamedZone"

    def test_name_setter_updates_graph(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone.name = "RenamedZone"
        refs = simple_doc.references.get_referencing("RenamedZone")
        assert len(refs) > 0
        assert not simple_doc.references.is_referenced("TestZone")

    def test_capital_name_setter_updates_all(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone.Name = "ViaCapitalName"
        assert simple_doc.getobject("Zone", "ViaCapitalName") is zone
        assert simple_doc.getobject("Zone", "TestZone") is None
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        assert wall.zone_name == "ViaCapitalName"

    def test_setattr_name_updates_all(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone.NAME = "ViaSetattr"
        assert simple_doc.getobject("Zone", "ViaSetattr") is zone
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        assert wall.zone_name == "ViaSetattr"

    def test_setitem_index_zero_updates_all(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone[0] = "ViaIndex"
        assert simple_doc.getobject("Zone", "ViaIndex") is zone
        assert simple_doc.getobject("Zone", "TestZone") is None
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        assert wall.zone_name == "ViaIndex"

    def test_rename_method_still_works(self, simple_doc: IDFDocument) -> None:
        simple_doc.rename("Zone", "TestZone", "ViaRename")
        assert simple_doc.getobject("Zone", "ViaRename") is not None
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        assert wall.zone_name == "ViaRename"

    def test_name_change_noop_when_same(self, simple_doc: IDFDocument) -> None:
        zone = simple_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone.name = "TestZone"
        assert simple_doc.getobject("Zone", "TestZone") is zone


class TestReferenceFieldChangeConsistency:
    """Verify that reference field changes update the graph."""

    def test_setattr_reference_field_updates_graph(self, simple_doc: IDFDocument) -> None:
        # Change the zone_name on a surface
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        # Add a second zone
        simple_doc.add("Zone", "Zone2")
        wall.zone_name = "Zone2"
        # Graph should now show the wall referencing Zone2
        refs = simple_doc.references.get_referencing("Zone2")
        assert wall in refs
        # Old reference should be removed
        refs_old = simple_doc.references.get_referencing("TestZone")
        assert wall not in refs_old

    def test_setitem_reference_field_updates_graph(self, simple_doc: IDFDocument) -> None:
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        assert wall.field_order is not None
        # Find the index of zone_name in field_order
        zone_idx = wall.field_order.index("zone_name") + 1  # +1 because index 0 is name
        simple_doc.add("Zone", "Zone2")
        wall[zone_idx] = "Zone2"
        refs = simple_doc.references.get_referencing("Zone2")
        assert wall in refs

    def test_non_reference_field_does_not_touch_graph(self, simple_doc: IDFDocument) -> None:
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        initial_refs = len(simple_doc.references)
        wall.number_of_vertices = 3
        assert len(simple_doc.references) == initial_refs

    def test_detached_object_no_crash(self) -> None:
        obj = IDFObject(obj_type="Zone", name="Detached")
        # No document, no crash
        obj.name = "Renamed"
        assert obj.name == "Renamed"
        obj.x_origin = 5.0
        assert obj.x_origin == 5.0


class TestGetIddGroupDict:
    def test_basic(self, simple_doc: IDFDocument) -> None:
        groups = simple_doc.getiddgroupdict()
        assert isinstance(groups, dict)
        # BuildingSurface:Detailed should be in "Thermal Zones and Surfaces" group
        assert "Thermal Zones and Surfaces" in groups
        assert "BuildingSurface:Detailed" in groups["Thermal Zones and Surfaces"]


class TestAddWithValidation:
    def test_add_valid_object_with_validation(self, empty_doc: IDFDocument) -> None:
        # Valid Zone object should succeed
        obj = empty_doc.add("Zone", "TestZone", x_origin=0.0, validate=True)
        assert obj.name == "TestZone"
        assert len(empty_doc["Zone"]) == 1

    def test_add_object_with_unknown_field_warns(self, empty_doc: IDFDocument) -> None:
        # Unknown field should raise ValidationFailedError
        with pytest.raises(ValidationFailedError) as exc_info:
            empty_doc.add("Zone", "TestZone", fake_field=123, validate=True)

        # Check the error message mentions the unknown field
        assert "fake_field" in str(exc_info.value)

    def test_add_without_validation_allows_unknown_field(self, empty_doc: IDFDocument) -> None:
        # With validate=False, unknown fields are silently accepted
        obj = empty_doc.add("Zone", "TestZone", fake_field=123, validate=False)
        assert obj.name == "TestZone"
        assert obj.data.get("fake_field") == 123

    def test_add_material_missing_required_field(self, empty_doc: IDFDocument) -> None:
        # Material requires roughness, thickness, conductivity, density, specific_heat
        with pytest.raises(ValidationFailedError) as exc_info:
            empty_doc.add("Material", "TestMaterial", roughness="MediumSmooth", validate=True)

        # Should report missing required fields
        assert "Required field" in str(exc_info.value) or "missing" in str(exc_info.value).lower()

    def test_add_material_with_all_required_fields(self, empty_doc: IDFDocument) -> None:
        # Material with all required fields should succeed
        obj = empty_doc.add(
            "Material",
            "TestMaterial",
            roughness="MediumSmooth",
            thickness=0.1,
            conductivity=1.0,
            density=2000.0,
            specific_heat=1000.0,
            validate=True,
        )
        assert obj.name == "TestMaterial"
        assert len(empty_doc["Material"]) == 1

    def test_add_with_invalid_enum_value(self, empty_doc: IDFDocument) -> None:
        # Invalid enum value should raise ValidationFailedError
        with pytest.raises(ValidationFailedError):
            empty_doc.add(
                "Material",
                "TestMaterial",
                roughness="InvalidRoughness",
                thickness=0.1,
                conductivity=1.0,
                density=2000.0,
                specific_heat=1000.0,
                validate=True,
            )

    def test_validation_default_is_true(self, empty_doc: IDFDocument) -> None:
        # By default, validation is enabled to catch errors early
        with pytest.raises(ValidationFailedError):
            empty_doc.add("Zone", "TestZone", unknown_param=42)


class TestDocumentProperties:
    """Tests for document property accessors."""

    def test_strict_property_default_true(self) -> None:
        doc = IDFDocument()
        assert doc.strict is True

    def test_strict_property_false(self) -> None:
        doc = IDFDocument(strict=False)
        assert doc.strict is False

    def test_cst_property_none_by_default(self, empty_doc: IDFDocument) -> None:
        assert empty_doc.cst is None

    def test_raw_text_property_none_by_default(self, empty_doc: IDFDocument) -> None:
        assert empty_doc.raw_text is None

    def test_cst_property_populated_by_preserve_formatting(self, idf_file: Path) -> None:
        doc = load_idf(str(idf_file), preserve_formatting=True)
        assert isinstance(doc.cst, DocumentCST)
        assert len(doc.cst.nodes) > 0

    def test_raw_text_property_populated_by_preserve_formatting(self, idf_file: Path) -> None:
        doc = load_idf(str(idf_file), preserve_formatting=True)
        assert isinstance(doc.raw_text, str)
        assert len(doc.raw_text) > 0

    def test_get_collection(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "Z1")
        coll = empty_doc.get_collection("Zone")
        assert isinstance(coll, IDFCollection)
        assert len(coll) == 1

    def test_keys_returns_nonempty_types(self, simple_doc: IDFDocument) -> None:
        keys = simple_doc.keys()
        assert "Zone" in keys
        assert "Material" in keys

    def test_values_returns_nonempty_collections(self, simple_doc: IDFDocument) -> None:
        vals = simple_doc.values()
        assert len(vals) > 0
        assert all(isinstance(v, IDFCollection) for v in vals)

    def test_items_returns_pairs(self, simple_doc: IDFDocument) -> None:
        items = simple_doc.items()
        types = [k for k, _ in items]
        assert "Zone" in types

    def test_getattr_raises_for_unknown(self, empty_doc: IDFDocument) -> None:
        with pytest.raises(AttributeError):
            _ = empty_doc.totally_unknown_attribute_xyz

    def test_getattr_raises_after_loop_with_no_match(self, empty_doc: IDFDocument) -> None:
        # Populate a collection so the __getattr__ loop iterates at least once
        empty_doc.add("Zone", "Z1", validate=False)
        with pytest.raises(AttributeError):
            _ = empty_doc.xyznonexistent123  # not in _PYTHON_TO_IDF, not matching 'Zone'

    def test_describe_raises_without_schema(self) -> None:
        doc = IDFDocument(version=(24, 1, 0))  # no schema
        with pytest.raises(ValueError, match="No schema"):
            doc.describe("Zone")

    def test_str_contains_sorted_types(self, simple_doc: IDFDocument) -> None:
        s = str(simple_doc)
        assert "Zone" in s
        # Sorted ensures alphabetical order
        zone_pos = s.index("Zone")
        material_pos = s.index("Material")
        assert material_pos < zone_pos  # "Material" < "Zone" alphabetically


class TestDocumentAddNoSchema:
    """Tests for add() when no schema is loaded."""

    def test_add_without_schema_does_not_validate(self) -> None:
        doc = IDFDocument(version=(24, 1, 0))  # no schema
        obj = doc.add("Zone", "TestZone", validate=False)
        assert obj.name == "TestZone"

    def test_resolve_schema_obj_type_no_schema(self) -> None:
        doc = IDFDocument(version=(24, 1, 0))
        result = doc._resolve_schema_obj_type("SomeType")  # pyright: ignore[reportPrivateUsage]
        assert result == "SomeType"

    def test_find_existing_collection_type_not_found(self, empty_doc: IDFDocument) -> None:
        result = empty_doc._find_existing_collection_type("NonExistent")  # pyright: ignore[reportPrivateUsage]
        assert result is None


class TestBuildFieldOrderForAdd:
    """Tests for _build_field_order_for_add static method."""

    def test_returns_none_when_base_is_none(self) -> None:
        result = IDFDocument._build_field_order_for_add(None, {}, None)  # pyright: ignore[reportPrivateUsage]
        assert result is None

    def test_extensible_with_user_extra_fields(self, empty_doc: IDFDocument) -> None:
        # Vertices are bucketed into the canonical wrapper; an arbitrary
        # non-schema field passes through into obj.data (writers ignore it).
        obj = empty_doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            {
                "surface_type": "Wall",
                "construction_name": "",
                "zone_name": "",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 2,
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                ],
                "extra_nonschema_field": 42.0,
            },
            validate=False,
        )
        assert obj.data["extra_nonschema_field"] == 42.0
        assert len(obj.data["vertices"]) == 2


class TestRemoveIdfObjectEdgeCases:
    """Extra remove tests to cover edge cases."""

    def test_remove_obj_not_in_collections(self, empty_doc: IDFDocument) -> None:
        obj = IDFObject(obj_type="GhostType", name="Ghost")
        # Should not raise even when type not in collections
        empty_doc.removeidfobject(obj)

    def test_remove_invalidates_schedule_cache(self, empty_doc: IDFDocument) -> None:
        sched = empty_doc.add("Schedule:Constant", "S1", {"hourly_value": 1.0})
        assert empty_doc.get_schedule("S1") is sched  # populate cache and verify present
        empty_doc.removeidfobject(sched)
        # After removal the schedule must no longer appear in the lookup result
        assert empty_doc.get_schedule("S1") is None

    def test_remove_with_cst(self, idf_file: Path) -> None:
        doc = load_idf(str(idf_file), preserve_formatting=True)
        assert doc.cst is not None
        zone = doc.getobject("Zone", "TestZone")
        assert zone is not None
        nodes_before = len(doc.cst.nodes)
        doc.removeidfobject(zone)
        # Node text should be cleared but node count stays the same
        assert len(doc.cst.nodes) == nodes_before


class TestNotifyNameChangeEdgeCases:
    """Tests for notify_name_change edge cases."""

    def test_schedule_rename_invalidates_cache(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Schedule:Constant", "OldSched", {"hourly_value": 1.0})
        assert empty_doc.get_schedule("OldSched") is not None  # populate cache and verify present
        empty_doc.rename("Schedule:Constant", "OldSched", "NewSched")
        # After rename the old name must be gone and the new name must be found
        assert empty_doc.get_schedule("OldSched") is None
        assert empty_doc.get_schedule("NewSched") is not None

    def test_rename_when_old_key_not_in_by_name(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "TestZone")
        zone = empty_doc.getobject("Zone", "TestZone")
        assert zone is not None
        # Manually remove from by_name to simulate stale state
        del empty_doc._collections["Zone"].by_name["TESTZONE"]  # pyright: ignore[reportPrivateUsage]
        # Rename should not crash even if old key is missing
        zone.name = "NewName"
        assert empty_doc.getobject("Zone", "NewName") is zone

    def test_rename_to_empty_string(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "TestZone")
        zone = empty_doc.getobject("Zone", "TestZone")
        assert zone is not None
        zone.name = ""
        assert zone.name == ""
        assert "TESTZONE" not in empty_doc._collections["Zone"].by_name  # pyright: ignore[reportPrivateUsage]

    def test_notify_name_change_obj_type_not_in_collections(self, empty_doc: IDFDocument) -> None:
        obj = IDFObject(obj_type="GhostType", name="Ghost")
        # Should not crash when the object type is not registered in any collection
        empty_doc.notify_name_change(obj, "OldName", "NewName")


class TestIndexObjectReferences:
    """Tests for _index_object_references fallback path."""

    def test_fallback_index_without_precomputed_ref_fields(self, empty_doc: IDFDocument) -> None:
        # Create an IDFObject without pre-computed ref_fields (no document set)
        obj = IDFObject(obj_type="Construction", name="C1", data={"outside_layer": "SomeMat"})
        # _ref_fields should be None for a raw IDFObject
        assert object.__getattribute__(obj, "_ref_fields") is None  # pyright: ignore[reportPrivateUsage]
        empty_doc._index_object_references(obj)  # pyright: ignore[reportPrivateUsage]
        refs = empty_doc.references.get_referencing("SomeMat")
        assert obj in refs

    def test_fallback_skips_non_reference_fields(self, empty_doc: IDFDocument) -> None:
        # ZoneAirContaminantBalance has both ref and non-ref fields.
        # The fallback loop should skip non-ref fields (734->733 branch).
        obj = IDFObject(
            obj_type="ZoneAirContaminantBalance",
            name="Test",
            data={
                "outdoor_carbon_dioxide_schedule_name": "MySched",
                "generic_contaminant_concentration": 0.5,
            },
        )
        assert object.__getattribute__(obj, "_ref_fields") is None  # pyright: ignore[reportPrivateUsage]
        empty_doc._index_object_references(obj)  # pyright: ignore[reportPrivateUsage]
        # Reference field should be registered
        refs = empty_doc.references.get_referencing("MySched")
        assert obj in refs


class TestGetReferencesAndSurfaces:
    """Tests for get_references and get_zone_surfaces."""

    def test_get_referencing(self, simple_doc: IDFDocument) -> None:
        # Call IDFDocument.get_referencing (not doc.references.get_referencing)
        refs = simple_doc.get_referencing("TestZone")
        assert len(refs) > 0

    def test_get_references(self, simple_doc: IDFDocument) -> None:
        wall = simple_doc.getobject("BuildingSurface:Detailed", "TestWall")
        assert wall is not None
        refs = simple_doc.get_references(wall)
        assert len(refs) > 0

    def test_get_zone_surfaces(self, simple_doc: IDFDocument) -> None:
        surfaces = simple_doc.get_zone_surfaces("TestZone")
        # simple_doc fixture defines exactly 2 surfaces for TestZone: TestWall and TestFloor
        assert len(surfaces) == 2
        names = [s.name for s in surfaces]
        assert "TestWall" in names
        assert "TestFloor" in names


class TestDocumentDescribeUnknownType:
    """Test describe() with unknown type (raises UnknownObjectTypeError)."""

    def test_describe_unknown_type_raises(self, empty_doc: IDFDocument) -> None:
        from idfkit.exceptions import UnknownObjectTypeError

        with pytest.raises(UnknownObjectTypeError):
            empty_doc.describe("TotallyFakeTypeXYZ")


class TestDocumentFindExistingCollectionTypeCaseInsensitive:
    """Test _find_existing_collection_type via case-insensitive loop."""

    def test_case_insensitive_match(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "Z1", validate=False)
        # 'zone' doesn't match directly but matches via the case-insensitive loop
        result = empty_doc._find_existing_collection_type("zone")  # pyright: ignore[reportPrivateUsage]
        assert result == "Zone"


class TestDocumentAddNoSchemaValidateTrue:
    """Test add() with no schema and validate=True (skips validation)."""

    def test_add_no_schema_validate_true(self) -> None:
        doc = IDFDocument(version=(24, 1, 0))  # no schema
        # With no schema, validation is skipped even when validate=True
        obj = doc.add("Zone", "TestZone", validate=True)
        assert obj.name == "TestZone"


class TestBuildFieldOrderExtensibleEarlyBreak:
    """Test extensible loop path where first group is not in field_data."""

    def test_extensible_no_data_fields_early_break(self) -> None:
        from idfkit.schema import ParsingCache

        result = IDFDocument._build_field_order_for_add(  # pyright: ignore[reportPrivateUsage]
            ["name", "x_origin"],
            {},  # empty - first group not in data, loop breaks immediately
            ParsingCache(
                obj_schema={},
                has_name=True,
                field_names=("x_origin",),
                all_field_names=("name", "x_origin"),
                field_types={},
                ref_fields=frozenset(),
                extensible=True,
                ext_size=1,
                ext_field_names=("vertex_x", "vertex_y"),
                ext_wrapper_key=None,
                ext_inner_props={},
            ),
        )
        assert result == ["name", "x_origin"]

    def test_field_order_returns_base_only(self) -> None:
        """After Phase 2, ``_build_field_order_for_add`` returns just the base.

        Extensible fields are tracked through the canonical wrapper
        (``obj.data[wrapper_key]``) and expanded by the writer at output
        time, so they no longer need to appear in ``field_order``.
        """
        from idfkit.schema import ParsingCache

        result = IDFDocument._build_field_order_for_add(  # pyright: ignore[reportPrivateUsage]
            ["name", "vertex_x"],
            {"vertex_x": 0.0, "vertex_y": 1.0},
            ParsingCache(
                obj_schema={},
                has_name=True,
                field_names=("vertex_x",),
                all_field_names=("name", "vertex_x"),
                field_types={},
                ref_fields=frozenset(),
                extensible=True,
                ext_size=2,
                ext_field_names=("vertex_x", "vertex_y"),
                ext_wrapper_key="data",
                ext_inner_props={},
            ),
        )
        assert result == ["name", "vertex_x"]


class TestRemoveCSTNoMatch:
    """Test CST removal when added object not in CST nodes."""

    def test_remove_programmatic_obj_with_cst(self, idf_file: Path) -> None:
        doc = load_idf(str(idf_file), preserve_formatting=True)
        assert doc.cst is not None
        # Add a new object programmatically — it won't be in CST nodes
        new_zone = doc.add("Zone", "ProgrammaticZone", validate=False)
        assert not any(n.obj is new_zone for n in doc.cst.nodes)
        # Removing it should traverse the CST loop without finding a match
        nodes_before = len(doc.cst.nodes)
        doc.removeidfobject(new_zone)
        assert len(doc.cst.nodes) == nodes_before  # no new node added/removed


class TestNotifyReferenceChangeNonString:
    """Test notify_reference_change when old/new values are not strings."""

    def test_non_string_old_value(self, empty_doc: IDFDocument) -> None:
        zone = empty_doc.add("Zone", "Z1", validate=False)
        # old_value is not a string -> old_str becomes None, call must not raise
        empty_doc.notify_reference_change(zone, "some_field", 42, "NewName")
        # Document state is unchanged: the zone is still present under its original name
        assert empty_doc.getobject("Zone", "Z1") is zone

    def test_non_string_new_value(self, empty_doc: IDFDocument) -> None:
        zone = empty_doc.add("Zone", "Z1", validate=False)
        # new_value is not a string -> new_str becomes None, call must not raise
        empty_doc.notify_reference_change(zone, "some_field", "OldName", 99)
        # Document state is unchanged: the zone is still present under its original name
        assert empty_doc.getobject("Zone", "Z1") is zone


class TestIndexObjectReferencesFallbackEmpty:
    """Test _index_object_references fallback with empty/None reference values."""

    def test_fallback_with_empty_reference_value(self, empty_doc: IDFDocument) -> None:
        obj = IDFObject(obj_type="Construction", name="C2", data={"outside_layer": ""})
        empty_doc._index_object_references(obj)  # pyright: ignore[reportPrivateUsage]
        refs = empty_doc.references.get_referencing("")
        assert obj not in refs

    def test_fallback_with_missing_reference_field(self, empty_doc: IDFDocument) -> None:
        obj = IDFObject(obj_type="Construction", name="C3", data={})
        empty_doc._index_object_references(obj)  # pyright: ignore[reportPrivateUsage]


class TestSchedulesDictEdgeCases:
    """Test _build_schedules_dict with empty-named schedules."""

    def test_schedule_with_empty_name_skipped(self, empty_doc: IDFDocument) -> None:
        # Add a schedule with empty name directly into the collection
        empty_sched = IDFObject(obj_type="Schedule:Constant", name="", data={"hourly_value": 1.0})
        empty_doc["Schedule:Constant"].add(empty_sched)
        sd = empty_doc.schedules_dict
        assert "" not in sd


class TestObjectsByTypeEdgeCases:
    """Test objects_by_type with empty collections."""

    def test_empty_collection_not_yielded(self, empty_doc: IDFDocument) -> None:
        _ = empty_doc["Zone"]  # creates empty collection
        pairs = list(empty_doc.objects_by_type())
        types = [t for t, _ in pairs]
        assert "Zone" not in types


class TestStrWithEmptyCollections:
    """Test __str__ skips empty collections."""

    def test_str_skips_empty_collections(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "Z1", validate=False)
        _ = empty_doc["Material"]  # creates empty Material collection
        s = str(empty_doc)
        assert "Zone" in s
        assert "Material" not in s

    def test_str_alphabetical_order(self, simple_doc: IDFDocument) -> None:
        s = str(simple_doc)
        # Types appear in sorted order
        assert s.index("Material") < s.index("Zone")


class TestAddUnknownObjectType:
    """Test add() raises when object type is unknown in schema."""

    def test_add_unknown_type_raises(self, empty_doc: IDFDocument) -> None:
        from idfkit.exceptions import UnknownObjectTypeError

        with pytest.raises(UnknownObjectTypeError):
            empty_doc.add("TotallyFakeType12345", "test")


class TestComputeRefFieldsFallback:
    """Test _compute_ref_fields when parsing cache is None (type not in schema)."""

    def test_fallback_when_no_parsing_cache(self) -> None:
        from idfkit.schema import EpJSONSchema

        # Schema with no properties -> get_parsing_cache returns None for any type
        schema = EpJSONSchema((24, 1, 0), {"properties": {}})
        result = IDFDocument._compute_ref_fields(schema, "Zone")  # pyright: ignore[reportPrivateUsage]
        assert result == frozenset()


class TestNotifyNameChangeStaledReferenceSkipped:
    """Test notify_name_change when referencing object's field value doesn't match."""

    def test_stale_reference_in_graph_skipped(self, empty_doc: IDFDocument) -> None:
        empty_doc.add("Zone", "Zone1")
        w1 = empty_doc.add(
            "BuildingSurface:Detailed",
            "W1",
            {
                "surface_type": "Wall",
                "construction_name": "",
                "zone_name": "Zone1",
                "outside_boundary_condition": "Outdoors",
            },
            validate=False,
        )
        # Register a stale reference so w1 shows as referencing Zone1 via a field
        # that doesn't actually have Zone1 as its value
        empty_doc.references.register(w1, "nonexistent_field", "Zone1")
        zone = empty_doc.getobject("Zone", "Zone1")
        assert zone is not None
        # Calling notify_name_change: w1.data.get('nonexistent_field') is None
        # so isinstance(None, str) is False -> line 690->688 branch
        empty_doc.notify_name_change(zone, "Zone1", "Zone2")
        # Should not crash
