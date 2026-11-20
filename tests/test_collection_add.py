"""Tests for ``IDFCollection.add``, the typed way to create an object through its collection."""

from __future__ import annotations

import copy
import pickle
from collections.abc import Callable
from typing import Any, SupportsIndex, cast

import pytest

from idfkit import IDFDocument, new_document
from idfkit.exceptions import (
    DuplicateObjectError,
    InvalidFieldError,
    UnknownObjectTypeError,
    UnknownObjectTypeWarning,
    ValidationFailedError,
)
from idfkit.objects import IDFCollection, IDFObject


@pytest.fixture
def doc() -> IDFDocument[Any]:
    return new_document()


class TestAdd:
    def test_adds_the_object_to_the_document(self, doc: IDFDocument[Any]) -> None:
        zone = doc["Zone"].add("Office", x_origin=1.0, ceiling_height=3.0)
        assert zone.name == "Office"
        assert zone.obj_type == "Zone"
        assert zone.ceiling_height == 3.0
        assert doc["Zone"]["Office"] is zone
        assert zone in doc["Zone"]

    def test_through_the_attribute_accessor(self, doc: IDFDocument[Any]) -> None:
        zone = doc.zones.add("Office")
        assert doc["Zone"]["Office"] is zone

    def test_validates_like_add(self, doc: IDFDocument[Any]) -> None:
        with pytest.raises(ValidationFailedError, match="Bogus"):
            doc["Zone"].add("Office", zone_inside_convection_algorithm="Bogus")  # pyright: ignore[reportArgumentType]
        with pytest.raises(InvalidFieldError, match="ceiling_hieght"):
            doc["Zone"].add("Office", ceiling_hieght=3.0)  # pyright: ignore[reportCallIssue]
        assert len(doc["Zone"]) == 0

    def test_a_failed_create_leaves_the_type_absent(self, doc: IDFDocument[Any]) -> None:
        zones = doc["Zone"]
        with pytest.raises(InvalidFieldError):
            zones.add("Office", ceiling_hieght=3.0)  # pyright: ignore[reportCallIssue]
        assert "Zone" not in doc.collections
        assert len(zones) == 0

    def test_duplicate_name_raises(self, doc: IDFDocument[Any]) -> None:
        doc["Zone"].add("Office")
        with pytest.raises(DuplicateObjectError):
            doc["Zone"].add("office")

    def test_nameless_type(self, doc: IDFDocument[Any]) -> None:
        sqlite = doc["Output:SQLite"].add(option_type="SimpleAndTabular")
        assert sqlite.option_type == "SimpleAndTabular"
        assert len(doc["Output:SQLite"]) == 1

    def test_indexes_references(self, doc: IDFDocument[Any]) -> None:
        zone = doc["Zone"].add("Office")
        doc.add("Construction", "Slab", validate=False)
        surface = doc["BuildingSurface:Detailed"].add(
            "Floor",
            surface_type="Floor",
            construction_name="Slab",
            zone_name="Office",
            outside_boundary_condition="Ground",
            sun_exposure="NoSun",
            wind_exposure="NoWind",
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 1.0, "vertex_z_coordinate": 0.0},
            ],
        )
        assert doc["BuildingSurface:Detailed"].referencing(zone) == [surface]
        assert len(surface.vertices) == 3

    def test_unknown_type_raises(self, doc: IDFDocument[Any]) -> None:
        with pytest.warns(UnknownObjectTypeWarning), pytest.raises(UnknownObjectTypeError):
            doc.get_collection("Zoen").add("Office")
        assert "Zoen" not in doc.collections

    def test_extra_positional_argument_raises(self, doc: IDFDocument[Any]) -> None:
        with pytest.raises(TypeError, match="positional"):
            doc["Zone"].add("Office", "Extra")  # pyright: ignore[reportCallIssue]

    def test_name_by_keyword_raises(self, doc: IDFDocument[Any]) -> None:
        """``doc.add("Zone", name="Office")`` works; a collection's name is positional only."""
        with pytest.raises(TypeError, match=r"add\('Office', \.\.\.\)"):
            doc.get_collection("Zone").add(name="Office")
        assert len(doc["Zone"]) == 0

    def test_collection_without_document_raises(self) -> None:
        collection: IDFCollection[IDFObject] = IDFCollection("Zone")
        with pytest.raises(TypeError, match="document"):
            collection.add("Office")


class TestDetachedCollection:
    """A type with no objects yet is read as a detached empty collection; adding through it attaches it."""

    def test_the_collection_read_before_create_holds_the_object(self, doc: IDFDocument[Any]) -> None:
        zones = doc["Zone"]
        assert "Zone" not in doc.collections
        zone = zones.add("Office")
        assert zone in zones
        assert len(zones) == 1
        assert doc["Zone"] is zones

    def test_a_stale_detached_collection_still_adds_to_the_document(self, doc: IDFDocument[Any]) -> None:
        stale = doc["Zone"]
        doc.add("Zone", "First")
        second = stale.add("Second")
        assert doc["Zone"]["Second"] is second
        assert [z.name for z in doc["Zone"]] == ["First", "Second"]

    def test_reading_still_does_not_store(self, doc: IDFDocument[Any]) -> None:
        _ = doc["Zone"]
        _ = doc.zones
        assert "Zone" not in doc.collections


def _copy(doc: IDFDocument[Any]) -> IDFDocument[Any]:
    return doc.copy()


def _deepcopy(doc: IDFDocument[Any]) -> IDFDocument[Any]:
    return copy.deepcopy(doc)


def _pickle(doc: IDFDocument[Any]) -> IDFDocument[Any]:
    return pickle.loads(pickle.dumps(doc))  # noqa: S301


class TestCopies:
    @pytest.mark.parametrize("clone", [_copy, _deepcopy, _pickle], ids=["copy", "deepcopy", "pickle"])
    def test_add_on_a_clone_adds_to_the_clone(
        self, doc: IDFDocument[Any], clone: Callable[[IDFDocument[Any]], IDFDocument[Any]]
    ) -> None:
        doc["Zone"].add("Office")
        twin = clone(doc)
        twin["Zone"].add("Lab")
        assert [z.name for z in twin["Zone"]] == ["Office", "Lab"]
        assert [z.name for z in doc["Zone"]] == ["Office"]


class TestOlderPickles:
    """A document pickled before collections knew their document still adds through them."""

    @staticmethod
    def _as_older_pickle(doc: object, monkeypatch: pytest.MonkeyPatch) -> bytes:
        """Pickle *doc* (a document, or an object of one) as a release before collections held their document would: no collection has ``_document``."""

        def without_document(self: IDFCollection[Any], protocol: SupportsIndex) -> Any:
            reduced = cast("tuple[Any, ...]", object.__reduce_ex__(self, protocol))
            state = cast("tuple[None, dict[str, Any]]", reduced[2])
            slots = {k: v for k, v in state[1].items() if k != "_document"}
            return (*reduced[:2], (None, slots), *reduced[3:])

        with monkeypatch.context() as patch:
            patch.setattr(IDFCollection, "__reduce_ex__", without_document)
            return pickle.dumps(doc)

    def test_collections_are_relinked(self, doc: IDFDocument[Any], monkeypatch: pytest.MonkeyPatch) -> None:
        doc["Zone"].add("Office")
        older: IDFDocument[Any] = pickle.loads(self._as_older_pickle(doc, monkeypatch))  # noqa: S301
        lab = older["Zone"].add("Lab")
        assert older["Zone"]["Lab"] is lab
        assert [z.name for z in older["Zone"]] == ["Office", "Lab"]
        assert [z.name for z in doc["Zone"]] == ["Office"]

    def test_an_object_pickled_before_its_document(
        self, doc: IDFDocument[Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Pickle restores the object's collection while it is still reading the object itself."""
        office = doc["Zone"].add("Office")
        twin: IDFObject = pickle.loads(self._as_older_pickle(office, monkeypatch))  # noqa: S301
        older = cast("IDFDocument[Any]", twin._document)  # pyright: ignore[reportPrivateUsage]
        assert older["Zone"]["Office"] is twin
        lab = older["Zone"].add("Lab")
        assert [z.name for z in older["Zone"]] == ["Office", "Lab"]
        assert older["Zone"]["Lab"] is lab

    def test_an_emptied_collection_says_to_use_add(
        self, doc: IDFDocument[Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        office = doc["Zone"].add("Office")
        doc.removeidfobject(office)
        older: IDFDocument[Any] = pickle.loads(self._as_older_pickle(doc, monkeypatch))  # noqa: S301
        with pytest.raises(TypeError, match=r"IDFDocument\.add"):
            older["Zone"].add("Lab")
        older.add("Zone", "Lab")
        assert [z.name for z in older["Zone"]] == ["Lab"]


class TestDeprecatedObjectForm:
    """``add(obj)`` used to file an existing object; it still does, with a warning."""

    def test_warns_and_files_the_object_as_before(self, doc: IDFDocument[Any]) -> None:
        doc["Zone"].add("Office")
        legacy = IDFObject(obj_type="Zone", name="Legacy")
        with pytest.warns(DeprecationWarning, match=r"addidfobject"):
            filed = doc["Zone"].add(legacy)  # pyright: ignore[reportArgumentType]
        assert filed is legacy
        assert doc["Zone"]["Legacy"] is legacy

    def test_the_warning_points_at_the_caller(self, doc: IDFDocument[Any]) -> None:
        doc["Zone"].add("Office")
        with pytest.warns(DeprecationWarning) as record:
            doc["Zone"].add(IDFObject(obj_type="Zone", name="Legacy"))  # pyright: ignore[reportArgumentType]
        assert record[0].filename == __file__

    def test_a_standalone_collection_still_files(self) -> None:
        collection: IDFCollection[IDFObject] = IDFCollection("Zone")
        with pytest.warns(DeprecationWarning):
            collection.add(IDFObject(obj_type="Zone", name="A"))  # pyright: ignore[reportArgumentType]
        assert [z.name for z in collection] == ["A"]

    def test_a_duplicate_still_raises(self, doc: IDFDocument[Any]) -> None:
        doc["Zone"].add("Office")
        with pytest.warns(DeprecationWarning), pytest.raises(DuplicateObjectError):
            doc["Zone"].add(IDFObject(obj_type="Zone", name="office"))  # pyright: ignore[reportArgumentType]

    def test_the_keyword_spelling_still_files(self, doc: IDFDocument[Any]) -> None:
        """The deprecated form was ``add(self, obj)``, so ``add(obj=...)`` was valid too."""
        doc["Zone"].add("Office")
        legacy = IDFObject(obj_type="Zone", name="Legacy")
        collection = cast("IDFCollection[IDFObject]", doc["Zone"])
        with pytest.warns(DeprecationWarning) as record:
            filed = collection.add(obj=legacy)  # untyped collection: obj= type-checks as a field
        assert filed is legacy
        assert doc["Zone"]["Legacy"] is legacy
        assert record[0].filename == __file__


class _TaggedCollection(IDFCollection[IDFObject]):
    """A subclass with an attribute of its own (it has a ``__dict__``)."""


class TestCopyingCollections:
    @pytest.mark.parametrize("clone", [copy.copy, copy.deepcopy, lambda c: pickle.loads(pickle.dumps(c))])  # noqa: S301
    def test_a_subclass_keeps_its_attributes(self, clone: Callable[[Any], Any]) -> None:
        collection = _TaggedCollection("Zone")
        collection.tag = "kept"  # type: ignore[attr-defined]
        twin = clone(collection)
        assert twin.tag == "kept"
        assert twin.obj_type == "Zone"

    def test_a_detached_collection_pickles_without_the_model(self, doc: IDFDocument[Any]) -> None:
        for i in range(200):
            doc.add(
                "Material",
                f"M{i}",
                roughness="Rough",
                thickness=0.1,
                conductivity=1.0,
                density=1.0,
                specific_heat=900.0,
            )
        detached = doc["Zone"]
        assert len(pickle.dumps(detached)) < 1000
        restored: IDFCollection[IDFObject] = pickle.loads(pickle.dumps(detached))  # noqa: S301
        with pytest.raises(TypeError, match="document"):
            restored.add("Office")

    def test_a_stored_collection_keeps_its_document(self, doc: IDFDocument[Any]) -> None:
        doc["Zone"].add("Office")
        twin: IDFDocument[Any] = copy.deepcopy(doc)
        twin["Zone"].add("Lab")
        assert [z.name for z in twin["Zone"]] == ["Office", "Lab"]


class TestHandBuiltCollections:
    def test_a_hand_built_collection_holding_objects_has_no_document(self, doc: IDFDocument[Any]) -> None:
        zone = doc["Zone"].add("Office")
        subset: IDFCollection[IDFObject] = IDFCollection("Zone")
        subset._append(zone)  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(TypeError, match="document"):
            subset.add("Lab")
        assert [z.name for z in doc["Zone"]] == ["Office"]

    def test_the_constructor_takes_a_document(self, doc: IDFDocument[Any]) -> None:
        collection: IDFCollection[IDFObject] = IDFCollection("Zone", doc)
        collection.add("Office")
        assert doc["Zone"]["Office"].name == "Office"


class TestAddidfobjectRefusal:
    def test_a_refused_duplicate_is_not_linked_to_the_document(self, doc: IDFDocument[Any]) -> None:
        doc.add("Zone", "A")
        doc.add("BuildingSurface:Detailed", "Wall", zone_name="A", validate=False)
        duplicate = IDFObject(obj_type="Zone", name="A")
        with pytest.raises(DuplicateObjectError):
            doc.addidfobject(duplicate)
        duplicate.name = "B"
        assert doc["Zone"]["A"].name == "A"
        assert doc["BuildingSurface:Detailed"]["Wall"].zone_name == "A"
