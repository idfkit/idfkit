"""Tests for IDFObject and IDFCollection classes."""

from __future__ import annotations

import pytest

from idfkit.exceptions import DuplicateObjectError
from idfkit.objects import IDFCollection, IDFObject, to_idf_name, to_python_name

# ---------------------------------------------------------------------------
# Name conversion helpers
# ---------------------------------------------------------------------------


class TestNameConversion:
    def test_to_python_name_basic(self) -> None:
        assert to_python_name("X Origin") == "x_origin"

    def test_to_python_name_long(self) -> None:
        assert to_python_name("Direction of Relative North") == "direction_of_relative_north"

    def test_to_python_name_with_special_chars(self) -> None:
        assert to_python_name("Vertex 1 X-coordinate") == "vertex_1_x_coordinate"

    def test_to_idf_name_basic(self) -> None:
        assert to_idf_name("x_origin") == "X Origin"

    def test_to_idf_name_long(self) -> None:
        assert to_idf_name("direction_of_relative_north") == "Direction Of Relative North"


# ---------------------------------------------------------------------------
# IDFObject
# ---------------------------------------------------------------------------


class TestIDFObject:
    def test_create_basic(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert obj.obj_type == "Zone"
        assert obj.name == "MyZone"
        assert obj.data == {}

    def test_create_with_data(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 10.0})
        assert obj.x_origin == 10.0

    def test_name_property_setter(self) -> None:
        obj = IDFObject(obj_type="Zone", name="Old")
        obj.name = "New"
        assert obj.name == "New"

    def test_name_eppy_compatibility(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert obj.Name == "MyZone"
        obj.Name = "Updated"
        assert obj.Name == "Updated"
        assert obj.name == "Updated"

    def test_name_setter_case_insensitive(self) -> None:
        obj = IDFObject(obj_type="Zone", name="Original")
        obj.NAME = "ViaUpper"
        assert obj.name == "ViaUpper"
        obj.NaMe = "ViaMixed"
        assert obj.name == "ViaMixed"

    def test_key_property(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert obj.key == "Zone"

    def test_getattr_exact_match(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        assert obj.x_origin == 5.0

    def test_getattr_case_insensitive(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        assert obj.X_Origin == 5.0

    def test_getattr_returns_none_for_missing(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert obj.nonexistent_field is None

    def test_getattr_raises_for_private(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        with pytest.raises(AttributeError):
            _ = obj._something

    def test_setattr_normalizes_key(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        obj.X_Origin = 10.0
        assert obj.data["x_origin"] == 10.0

    def test_getitem_by_name(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        assert obj["x_origin"] == 5.0

    def test_getitem_index_zero_returns_name(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert obj[0] == "MyZone"

    def test_getitem_index_with_field_order(self) -> None:
        obj = IDFObject(
            obj_type="Zone",
            name="MyZone",
            data={"x_origin": 5.0, "y_origin": 10.0},
            field_order=["x_origin", "y_origin"],
        )
        assert obj[1] == 5.0
        assert obj[2] == 10.0

    def test_getitem_index_out_of_range(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", field_order=["x_origin"])
        with pytest.raises(IndexError):
            _ = obj[99]

    def test_setitem_by_name(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        obj["x_origin"] = 5.0
        assert obj.x_origin == 5.0

    def test_setitem_index_zero_sets_name(self) -> None:
        obj = IDFObject(obj_type="Zone", name="Old")
        obj[0] = "New"
        assert obj.name == "New"

    def test_setitem_index_with_field_order(self) -> None:
        obj = IDFObject(
            obj_type="Zone",
            name="MyZone",
            data={"x_origin": 0.0},
            field_order=["x_origin"],
        )
        obj[1] = 99.0
        assert obj.data["x_origin"] == 99.0

    def test_setitem_index_out_of_range(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", field_order=["x_origin"])
        with pytest.raises(IndexError):
            obj[99] = 1.0

    def test_repr(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert repr(obj) == "Zone('MyZone')"

    def test_str(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert str(obj) == "Zone: MyZone"

    def test_eq_same(self) -> None:
        obj1 = IDFObject(obj_type="Zone", name="A", data={"x": 1})
        obj2 = IDFObject(obj_type="Zone", name="A", data={"x": 1})
        assert obj1 == obj2

    def test_eq_different_name(self) -> None:
        obj1 = IDFObject(obj_type="Zone", name="A")
        obj2 = IDFObject(obj_type="Zone", name="B")
        assert obj1 != obj2

    def test_eq_different_type(self) -> None:
        obj1 = IDFObject(obj_type="Zone", name="A")
        assert obj1 != "not an object"

    def test_hash(self) -> None:
        obj1 = IDFObject(obj_type="Zone", name="MyZone")
        obj2 = IDFObject(obj_type="Zone", name="MyZone")
        assert hash(obj1) == hash(obj2)
        # Can be used in sets
        s = {obj1, obj2}
        assert len(s) == 1

    def test_to_dict(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        d = obj.to_dict()
        assert d == {"name": "MyZone", "x_origin": 5.0}

    def test_get_with_default(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        assert obj.get("x_origin") == 5.0
        assert obj.get("missing", "default") == "default"

    def test_copy(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        copied = obj.copy()
        assert copied == obj
        assert copied is not obj
        assert copied.data is not obj.data
        assert copied.data == obj.data

    def test_copy_no_document_reference(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", document=None)
        copied = obj.copy()
        assert copied.theidf is None

    def test_fieldnames_with_field_order(self) -> None:
        obj = IDFObject(
            obj_type="Zone",
            name="MyZone",
            data={"x_origin": 5.0},
            field_order=["x_origin", "y_origin"],
        )
        assert obj.fieldnames == ["Name", "x_origin", "y_origin"]

    def test_fieldnames_without_field_order(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        assert obj.fieldnames == ["Name", "x_origin"]

    def test_fieldvalues_with_field_order(self) -> None:
        obj = IDFObject(
            obj_type="Zone",
            name="MyZone",
            data={"x_origin": 5.0, "y_origin": 10.0},
            field_order=["x_origin", "y_origin"],
        )
        assert obj.fieldvalues == ["MyZone", 5.0, 10.0]

    def test_fieldvalues_without_field_order(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0})
        assert obj.fieldvalues == ["MyZone", 5.0]

    def test_schema_dict_property(self) -> None:
        schema = {"some": "schema"}
        obj = IDFObject(obj_type="Zone", name="MyZone", schema=schema)
        assert obj.schema_dict == schema

    def test_field_order_property(self) -> None:
        order = ["a", "b", "c"]
        obj = IDFObject(obj_type="Zone", name="MyZone", field_order=order)
        assert obj.field_order == order

    def test_theidf_property(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", document=None)
        assert obj.theidf is None


# ---------------------------------------------------------------------------
# IDFCollection
# ---------------------------------------------------------------------------


class TestIDFCollection:
    def test_create(self) -> None:
        coll = IDFCollection("Zone")
        assert coll.obj_type == "Zone"
        assert len(coll) == 0

    def test_add_and_getitem_by_name(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="MyZone")
        coll.add(obj)
        assert coll["MyZone"] is obj

    def test_add_case_insensitive_lookup(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="MyZone")
        coll.add(obj)
        assert coll["myzone"] is obj
        assert coll["MYZONE"] is obj

    def test_add_duplicate_raises(self) -> None:
        coll = IDFCollection("Zone")
        coll.add(IDFObject(obj_type="Zone", name="MyZone"))
        with pytest.raises(DuplicateObjectError):
            coll.add(IDFObject(obj_type="Zone", name="MyZone"))

    def test_add_empty_name_allowed(self) -> None:
        coll = IDFCollection("Zone")
        obj1 = IDFObject(obj_type="Zone", name="")
        obj2 = IDFObject(obj_type="Zone", name="")
        coll.add(obj1)
        coll.add(obj2)  # Multiple empty names are OK
        assert len(coll) == 2

    def test_getitem_by_index(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="MyZone")
        coll.add(obj)
        assert coll[0] is obj

    def test_getitem_missing_name_raises(self) -> None:
        coll = IDFCollection("Zone")
        with pytest.raises(KeyError):
            _ = coll["Nonexistent"]

    def test_remove(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="MyZone")
        coll.add(obj)
        coll.remove(obj)
        assert len(coll) == 0
        assert "MyZone" not in coll

    def test_contains_by_name(self) -> None:
        coll = IDFCollection("Zone")
        coll.add(IDFObject(obj_type="Zone", name="MyZone"))
        assert "MyZone" in coll
        assert "Other" not in coll

    def test_contains_by_object(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="MyZone")
        coll.add(obj)
        assert obj in coll

    def test_iter(self) -> None:
        coll = IDFCollection("Zone")
        obj1 = IDFObject(obj_type="Zone", name="A")
        obj2 = IDFObject(obj_type="Zone", name="B")
        coll.add(obj1)
        coll.add(obj2)
        items = list(coll)
        assert items == [obj1, obj2]

    def test_len(self) -> None:
        coll = IDFCollection("Zone")
        assert len(coll) == 0
        coll.add(IDFObject(obj_type="Zone", name="A"))
        assert len(coll) == 1

    def test_bool_empty(self) -> None:
        coll = IDFCollection("Zone")
        assert not coll

    def test_bool_nonempty(self) -> None:
        coll = IDFCollection("Zone")
        coll.add(IDFObject(obj_type="Zone", name="A"))
        assert coll

    def test_repr(self) -> None:
        coll = IDFCollection("Zone")
        coll.add(IDFObject(obj_type="Zone", name="A"))
        assert repr(coll) == "IDFCollection(Zone, count=1)"

    def test_get_existing(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="A")
        coll.add(obj)
        assert coll.get("A") is obj

    def test_get_missing(self) -> None:
        coll = IDFCollection("Zone")
        assert coll.get("Missing") is None
        assert coll.get("Missing", None) is None

    def test_first_nonempty(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="A")
        coll.add(obj)
        assert coll.first() is obj

    def test_first_empty(self) -> None:
        coll = IDFCollection("Zone")
        assert coll.first() is None

    def test_to_list(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="A")
        coll.add(obj)
        result = coll.to_list()
        assert result == [obj]
        # to_list() should return a copy, not the internal list
        result.append(IDFObject(obj_type="Zone", name="B"))
        assert len(coll) == 1

    def test_to_dict(self) -> None:
        coll = IDFCollection("Zone")
        coll.add(IDFObject(obj_type="Zone", name="A", data={"x": 1}))
        result = coll.to_dict()
        assert result == [{"name": "A", "x": 1}]

    def test_filter(self) -> None:
        coll = IDFCollection("Zone")
        coll.add(IDFObject(obj_type="Zone", name="A", data={"x_origin": 1.0}))
        coll.add(IDFObject(obj_type="Zone", name="B", data={"x_origin": 5.0}))
        coll.add(IDFObject(obj_type="Zone", name="C", data={"x_origin": 10.0}))
        result = coll.filter(lambda o: o.x_origin > 3.0)
        assert len(result) == 2
        assert result[0].name == "B"
        assert result[1].name == "C"

    def test_by_name_property(self) -> None:
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="MyZone")
        coll.add(obj)
        assert "MYZONE" in coll.by_name
        assert coll.by_name["MYZONE"] is obj
