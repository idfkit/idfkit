"""Tests for IDFDocument class."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit import IDFDocument
from idfkit.exceptions import DuplicateObjectError
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
        empty_doc.add(
            "People",
            "TestPeople",
            {
                "zone_or_zonelist_or_space_or_spacelist_name": "TestZone",
                "number_of_people_schedule_name": "UsedSchedule",
            },
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


class TestGetIddGroupDict:
    def test_basic(self, simple_doc: IDFDocument) -> None:
        groups = simple_doc.getiddgroupdict()
        assert isinstance(groups, dict)
        # BuildingSurface:Detailed should be grouped under "BuildingSurface"
        assert "BuildingSurface" in groups
