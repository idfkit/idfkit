"""Tests for ``IDFCollection.create``, the typed way to add an object through its collection."""

from __future__ import annotations

import copy
import pickle
from collections.abc import Callable
from typing import Any, SupportsIndex, cast

import pytest

from idfkit import IDFDocument, new_document
from idfkit.exceptions import DuplicateObjectError, UnknownObjectTypeError, ValidationFailedError
from idfkit.objects import IDFCollection, IDFObject


@pytest.fixture
def doc() -> IDFDocument[Any]:
    return new_document()


class TestCreate:
    def test_adds_the_object_to_the_document(self, doc: IDFDocument[Any]) -> None:
        zone = doc["Zone"].create("Office", x_origin=1.0, ceiling_height=3.0)
        assert zone.name == "Office"
        assert zone.obj_type == "Zone"
        assert zone.ceiling_height == 3.0
        assert doc["Zone"]["Office"] is zone
        assert zone in doc["Zone"]

    def test_through_the_attribute_accessor(self, doc: IDFDocument[Any]) -> None:
        zone = doc.zones.create("Office")
        assert doc["Zone"]["Office"] is zone

    def test_validates_like_add(self, doc: IDFDocument[Any]) -> None:
        with pytest.raises(ValidationFailedError, match="Bogus"):
            doc["Zone"].create("Office", zone_inside_convection_algorithm="Bogus")  # pyright: ignore[reportArgumentType]
        with pytest.raises(ValidationFailedError, match="ceiling_hieght"):
            doc["Zone"].create("Office", ceiling_hieght=3.0)  # pyright: ignore[reportCallIssue]
        assert len(doc["Zone"]) == 0

    def test_a_failed_create_leaves_the_type_absent(self, doc: IDFDocument[Any]) -> None:
        zones = doc["Zone"]
        with pytest.raises(ValidationFailedError):
            zones.create("Office", ceiling_hieght=3.0)  # pyright: ignore[reportCallIssue]
        assert "Zone" not in doc.collections
        assert len(zones) == 0

    def test_duplicate_name_raises(self, doc: IDFDocument[Any]) -> None:
        doc["Zone"].create("Office")
        with pytest.raises(DuplicateObjectError):
            doc["Zone"].create("office")

    def test_nameless_type(self, doc: IDFDocument[Any]) -> None:
        sqlite = doc["Output:SQLite"].create(option_type="SimpleAndTabular")
        assert sqlite.option_type == "SimpleAndTabular"
        assert len(doc["Output:SQLite"]) == 1

    def test_indexes_references(self, doc: IDFDocument[Any]) -> None:
        zone = doc["Zone"].create("Office")
        doc.add("Construction", "Slab", validate=False)
        surface = doc["BuildingSurface:Detailed"].create(
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
        with pytest.raises(UnknownObjectTypeError):
            doc.get_collection("Zoen").create("Office")
        assert "Zoen" not in doc.collections

    def test_extra_positional_argument_raises(self, doc: IDFDocument[Any]) -> None:
        with pytest.raises(TypeError, match="positional"):
            doc["Zone"].create("Office", "Extra")  # pyright: ignore[reportCallIssue]

    def test_collection_without_document_raises(self) -> None:
        collection: IDFCollection[IDFObject] = IDFCollection("Zone")
        with pytest.raises(TypeError, match="document"):
            collection.create("Office")


class TestDetachedCollection:
    """A type with no objects yet is read as a detached empty collection; creating through it attaches it."""

    def test_the_collection_read_before_create_holds_the_object(self, doc: IDFDocument[Any]) -> None:
        zones = doc["Zone"]
        assert "Zone" not in doc.collections
        zone = zones.create("Office")
        assert zone in zones
        assert len(zones) == 1
        assert doc["Zone"] is zones

    def test_a_stale_detached_collection_still_adds_to_the_document(self, doc: IDFDocument[Any]) -> None:
        stale = doc["Zone"]
        doc.add("Zone", "First")
        second = stale.create("Second")
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
    def test_create_on_a_clone_adds_to_the_clone(
        self, doc: IDFDocument[Any], clone: Callable[[IDFDocument[Any]], IDFDocument[Any]]
    ) -> None:
        doc["Zone"].create("Office")
        twin = clone(doc)
        twin["Zone"].create("Lab")
        assert [z.name for z in twin["Zone"]] == ["Office", "Lab"]
        assert [z.name for z in doc["Zone"]] == ["Office"]


class TestOlderPickles:
    """A document pickled before collections knew their document still creates through them."""

    @staticmethod
    def _as_older_pickle(doc: IDFDocument[Any], monkeypatch: pytest.MonkeyPatch) -> bytes:
        """Pickle *doc* as an idfkit release before ``create()`` would: no collection has ``_document``."""

        def without_document(self: IDFCollection[Any], protocol: SupportsIndex) -> Any:
            reduced = cast("tuple[Any, ...]", object.__reduce_ex__(self, protocol))
            state = cast("tuple[None, dict[str, Any]]", reduced[2])
            slots = {k: v for k, v in state[1].items() if k != "_document"}
            return (*reduced[:2], (None, slots), *reduced[3:])

        with monkeypatch.context() as patch:
            patch.setattr(IDFCollection, "__reduce_ex__", without_document)
            return pickle.dumps(doc)

    def test_collections_are_relinked(self, doc: IDFDocument[Any], monkeypatch: pytest.MonkeyPatch) -> None:
        doc["Zone"].create("Office")
        older: IDFDocument[Any] = pickle.loads(self._as_older_pickle(doc, monkeypatch))  # noqa: S301
        lab = older["Zone"].create("Lab")
        assert older["Zone"]["Lab"] is lab
        assert [z.name for z in older["Zone"]] == ["Office", "Lab"]
        assert [z.name for z in doc["Zone"]] == ["Office"]

    def test_an_emptied_collection_says_to_use_add(
        self, doc: IDFDocument[Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        office = doc["Zone"].create("Office")
        doc.removeidfobject(office)
        older: IDFDocument[Any] = pickle.loads(self._as_older_pickle(doc, monkeypatch))  # noqa: S301
        with pytest.raises(TypeError, match=r"IDFDocument\.add"):
            older["Zone"].create("Lab")
        older.add("Zone", "Lab")
        assert [z.name for z in older["Zone"]] == ["Lab"]
