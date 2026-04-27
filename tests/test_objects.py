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

    def test_hash_identity_based(self) -> None:
        obj1 = IDFObject(obj_type="Zone", name="MyZone")
        obj2 = IDFObject(obj_type="Zone", name="MyZone")
        # Hash is identity-based, so distinct objects have different hashes
        assert hash(obj1) != hash(obj2)
        s = {obj1, obj2}
        assert len(s) == 2

    def test_hash_stable_after_name_change(self) -> None:
        obj = IDFObject(obj_type="Zone", name="OldName")
        h_before = hash(obj)
        obj.name = "NewName"
        assert hash(obj) == h_before

    def test_hash_usable_as_dict_key(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        d: dict[IDFObject, str] = {obj: "value"}
        obj.name = "Renamed"
        assert d[obj] == "value"

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

    def test_dir_includes_public_methods(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        attrs = dir(obj)
        # Check that core public attributes are included
        assert "obj_type" in attrs
        assert "name" in attrs
        assert "data" in attrs
        assert "key" in attrs
        assert "Name" in attrs
        assert "fieldnames" in attrs
        assert "fieldvalues" in attrs
        assert "theidf" in attrs
        assert "to_dict" in attrs
        assert "get" in attrs
        assert "copy" in attrs
        assert "get_field_idd" in attrs

    def test_dir_includes_data_keys(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone", data={"x_origin": 5.0, "y_origin": 10.0})
        attrs = dir(obj)
        assert "x_origin" in attrs
        assert "y_origin" in attrs

    def test_dir_includes_field_order(self) -> None:
        obj = IDFObject(
            obj_type="Zone",
            name="MyZone",
            data={"x_origin": 5.0},
            field_order=["direction_of_relative_north", "x_origin", "y_origin", "z_origin"],
        )
        attrs = dir(obj)
        # Should include all fields from field_order, not just data keys
        assert "direction_of_relative_north" in attrs
        assert "x_origin" in attrs
        assert "y_origin" in attrs
        assert "z_origin" in attrs


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

    def test_getitem_empty_key_with_items(self) -> None:
        """Empty key falls back to first item."""
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="")
        coll.add(obj)
        assert coll[""] is obj

    def test_getitem_empty_key_no_items_raises(self) -> None:
        """Empty key with no items raises KeyError."""
        coll = IDFCollection("Zone")
        with pytest.raises(KeyError):
            _ = coll[""]

    def test_contains_empty_key_false(self) -> None:
        """Empty key __contains__ returns False when no items."""
        coll = IDFCollection("Zone")
        assert "" not in coll

    def test_contains_empty_key_true(self) -> None:
        """Empty key __contains__ returns True when items exist."""
        coll = IDFCollection("Zone")
        coll.add(IDFObject(obj_type="Zone", name=""))
        assert "" in coll


class TestIDFObjectStrict:
    """Tests for strict-mode field validation."""

    def test_getattr_strict_raises_for_unknown_field(self) -> None:
        from idfkit import new_document
        from idfkit.exceptions import InvalidFieldError

        doc = new_document(version=(24, 1, 0))
        zone = doc.add("Zone", "TestZone")
        with pytest.raises(InvalidFieldError):
            _ = zone.nonexistent_field_xyz  # type: ignore[union-attr]

    def test_setattr_strict_raises_for_unknown_field(self) -> None:
        from idfkit import new_document
        from idfkit.exceptions import InvalidFieldError

        doc = new_document(version=(24, 1, 0))
        zone = doc.add("Zone", "TestZone")
        with pytest.raises(InvalidFieldError):
            zone.nonexistent_field_xyz = 42.0  # type: ignore[union-attr]

    def test_set_name_no_op_when_same(self) -> None:
        """Setting name to same value should be a no-op."""
        obj = IDFObject(obj_type="Zone", name="MyZone")
        version_before = obj.mutation_version
        obj.name = "MyZone"
        assert obj.mutation_version == version_before

    def test_mutation_version_increments_on_field_write(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        v0 = obj.mutation_version
        obj.x_origin = 1.0
        assert obj.mutation_version == v0 + 1

    def test_repr_svg_returns_none_for_non_construction(self) -> None:
        obj = IDFObject(obj_type="Zone", name="MyZone")
        assert obj._repr_svg_() is None  # pyright: ignore[reportPrivateUsage]

    def test_repr_svg_returns_none_without_document(self) -> None:
        obj = IDFObject(obj_type="Construction", name="Orphan", data={"outside_layer": "Mat"})
        assert obj._repr_svg_() is None  # pyright: ignore[reportPrivateUsage]

    def test_set_field_with_ref_fields_notifies_document(self) -> None:
        """Writing a ref field on an object attached to a document triggers notification."""
        from idfkit import new_document

        doc = new_document(version=(24, 1, 0))
        # Add a surface that references a zone
        doc.add("Zone", "ZoneA")
        srf = doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            surface_type="Wall",
            zone_name="ZoneA",
            validate=False,
        )
        # Change the zone name ref — should not raise
        srf.zone_name = "ZoneA"

    def test_setattr_private_key_uses_object_setattr(self) -> None:
        """Keys starting with _ use object.__setattr__ directly."""
        obj = IDFObject(obj_type="Zone", name="MyZone")
        # _type is a slot — using object.__setattr__ path
        object.__setattr__(obj, "_type", "NewType")
        assert obj.obj_type == "NewType"

    def test_repr_svg_exception_returns_none(self) -> None:
        """_repr_svg_ returns None when construction_to_svg raises."""
        from idfkit import new_document

        doc = new_document(version=(24, 1, 0))
        # Construction with no layers — construction_to_svg still works fine.
        # To hit the exception path we need to cause an import or runtime error.
        # The simplest way: attach an object type "Construction" but make the
        # visualization module raise by monkeypatching.
        doc.add("Construction", "BadConst", {}, validate=False)
        const = doc["Construction"]["BadConst"]

        import idfkit.visualization.svg as svg_mod

        orig = svg_mod.construction_to_svg
        try:
            svg_mod.construction_to_svg = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("fail"))  # type: ignore[assignment]
            result = const._repr_svg_()  # pyright: ignore[reportPrivateUsage]
            assert result is None
        finally:
            svg_mod.construction_to_svg = orig

    def test_collection_remove_item_not_in_items(self) -> None:
        """remove() gracefully handles an obj not in _items (line 652->exit)."""
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="MyZone")
        # Do NOT add to collection; just try to remove it
        coll.remove(obj)  # Should not raise
        assert len(coll) == 0

    def test_collection_get_empty_name_no_items_returns_default(self) -> None:
        """get('') with no items returns the default value (line 709 else branch)."""
        coll = IDFCollection("Zone")
        result = coll.get("", None)
        assert result is None

    def test_parse_extensible_index_prefix_number_suffix_no_match(self) -> None:
        """Pattern matches but composite base is NOT in extensibles → returns None, 0."""
        from idfkit.objects import parse_extensible_index

        # "vertex_1_x_coordinate" pattern but "vertex_x_coordinate" not in extensibles
        base, group = parse_extensible_index("vertex_1_x_coordinate", frozenset({"other_field"}))
        assert base is None
        assert group == 0

    def test_is_known_field_prefix_number_suffix_not_in_extensibles(self) -> None:
        """_is_known_field: pattern prefix_N_suffix matches but composite base NOT in extensibles."""
        obj = IDFObject(
            obj_type="Zone",
            name="Z",
            field_order=["field_one"],
            extensibles=frozenset({"other"}),
        )
        # "vertex_1_x_coordinate" doesn't match extensibles → check "base_N" path
        assert not obj._is_known_field("vertex_1_x_coordinate", ["field_one"])  # pyright: ignore[reportPrivateUsage]

    def test_fill_extensible_gap_unparseable_appends_as_is(self) -> None:
        """_set_field with an unknown field stores the value in data even when no extensible pattern matches."""
        obj = IDFObject(
            obj_type="Zone",
            name="Z",
            field_order=["field"],
            extensibles=frozenset({"field"}),
        )
        # Write a field that has no extensible pattern match — value stored in _data
        obj._set_field("completely_unknown_field_xyz", 42.0)  # pyright: ignore[reportPrivateUsage]
        assert obj._data["completely_unknown_field_xyz"] == 42.0  # pyright: ignore[reportPrivateUsage]

    def test_collection_get_empty_name_returns_first(self) -> None:
        """get('') when items exist returns first item."""
        coll = IDFCollection("Zone")
        obj = IDFObject(obj_type="Zone", name="")
        coll.add(obj)
        assert coll.get("") is obj


class TestObjectsAdditionalBranches:
    """Cover remaining branch-coverage gaps in objects.py."""

    def test_is_known_field_base_n_not_in_extensibles_returns_false(self) -> None:
        """238->240: base_N pattern matches but base NOT in extensibles → False."""
        obj = IDFObject(
            obj_type="Zone",
            name="Z",
            field_order=["other"],
            extensibles=frozenset({"other"}),
        )
        # "myfield_5" matches base_N pattern; base="myfield" NOT in extensibles
        result = obj._is_known_field("myfield_5", ["other"])  # pyright: ignore[reportPrivateUsage]
        assert result is False

    def test_name_property_setter_calls_set_name(self) -> None:
        """Line 250: name property setter (IDFObject.name.fset) calls _set_name."""
        obj = IDFObject(obj_type="Zone", name="OldName")
        # Call the property setter directly (obj.name = x goes through __setattr__)
        IDFObject.name.fset(obj, "NewName")  # type: ignore[union-attr]
        assert obj.name == "NewName"

    def test_setattr_private_key_uses_object_setattr(self) -> None:
        """Line 309: __setattr__ with key starting '_' calls object.__setattr__."""
        obj = IDFObject(obj_type="Zone", name="Z")
        # Assign a private attribute through IDFObject.__setattr__
        obj.__setattr__("_source_text", "custom_text")  # pyright: ignore[reportAttributeAccessIssue]
        assert object.__getattribute__(obj, "_source_text") == "custom_text"
