"""A type another bundled release has is reported as missing from this release, not as unknown.

``doc.add("Lights:Definition", ...)`` on a 26.1 model, or ``doc.spaces`` on a 9.4 one, used to
raise ``Unknown object type`` or a bare ``AttributeError``, though ``idfkit check`` already knew the
type was added in a later release. Both now name the releases that have it and how to reach one.
"""

from __future__ import annotations

import pickle

import pytest

from idfkit import new_document
from idfkit._object_types import ALL_OBJECT_TYPES, PARTIAL_OBJECT_TYPES
from idfkit.exceptions import UnknownObjectTypeError
from idfkit.introspection import describe_object_type
from idfkit.schema import get_schema
from idfkit.versions import (
    ENERGYPLUS_VERSIONS,
    LATEST_VERSION,
    describe_presence,
    format_releases,
    not_in_release_message,
    object_type_releases,
)


def test_add_names_the_release_that_added_the_type() -> None:
    doc = new_document(version=(26, 1, 0))
    with pytest.raises(UnknownObjectTypeError) as excinfo:
        doc.add("Lights:Definition", "L1")
    message = str(excinfo.value)
    assert "Unknown object type" not in message
    assert "'Lights:Definition' is not an object type of EnergyPlus 26.1.0" in message
    assert "it was added in 26.2.0" in message
    assert "idfkit.migrate(doc, (26, 2, 0))" in message
    assert "new_document()" in message


def test_schema_lookup_names_no_document() -> None:
    """describe_object_type takes a schema, not a document: the message must not speak of one."""
    with pytest.raises(UnknownObjectTypeError) as excinfo:
        describe_object_type(get_schema((26, 1, 0)), "Lights:Definition")
    message = str(excinfo.value)
    assert "it was added in 26.2.0" in message
    assert "document" not in message.split("new_document")[0]
    assert "the model" not in message


def test_add_on_an_old_release_points_at_a_release_that_has_it() -> None:
    with pytest.raises(UnknownObjectTypeError, match=r"it was added in 9\.6\.0"):
        new_document(version=(9, 4, 0)).add("Space", "S")


def test_removed_type_says_when_it_was_removed() -> None:
    with pytest.raises(UnknownObjectTypeError) as excinfo:
        new_document().add("DistrictHeating", "D")
    message = str(excinfo.value)
    assert "it was removed in 23.2.0" in message
    assert "migrate" not in message


@pytest.mark.parametrize("attr", ["lights_definitions", "Lights_Definition"])
def test_accessor_names_the_release_that_added_the_type(attr: str) -> None:
    doc = new_document(version=(26, 1, 0))
    with pytest.raises(AttributeError) as excinfo:
        getattr(doc, attr)
    message = str(excinfo.value)
    assert message.startswith(f"'IDFDocument' object has no attribute '{attr}'.")
    assert "it was added in 26.2.0" in message
    assert not hasattr(doc, attr)


def test_accessor_error_survives_pickling() -> None:
    doc = new_document(version=(9, 4, 0))
    with pytest.raises(AttributeError) as excinfo:
        _ = doc.spaces
    restored = pickle.loads(pickle.dumps(excinfo.value))  # noqa: S301
    assert "added in 9.6.0" in str(restored)


def test_a_misspelling_is_still_unknown_with_a_suggestion() -> None:
    doc = new_document(version=(26, 1, 0))
    with pytest.raises(UnknownObjectTypeError, match=r"Unknown object type: 'Zoen'\. Did you mean 'Zone'\?"):
        doc.add("Zoen", "Z")
    with pytest.raises(AttributeError) as excinfo:
        getattr(doc, "zonez")  # noqa: B009
    assert "Did you mean" in str(excinfo.value)


def test_a_type_the_release_has_gives_no_release_message() -> None:
    assert not_in_release_message("Zone", (9, 4, 0)) is None
    assert not_in_release_message("Space", (9, 6, 0)) is None
    assert not_in_release_message("Zoen", (26, 1, 0)) is None


def test_message_for_a_type_last_in_an_older_release_creates_it_there() -> None:
    message = not_in_release_message("DistrictHeating", (9, 0, 1))
    assert message is None  # 9.0.1 has it
    message = not_in_release_message("Space", (8, 9, 0))
    assert message is not None
    assert "new_document()" in message  # the latest release has Space


def test_object_type_releases_matches_every_bundled_schema() -> None:
    # The generated table answers without loading a schema; it must agree with the schemas.
    for obj_type in ("Space", "Lights:Definition", "DistrictHeating", "Zone"):
        expected = tuple(
            v for v in ENERGYPLUS_VERSIONS if obj_type.casefold() in {t.casefold() for t in get_schema(v).object_types}
        )
        assert object_type_releases(obj_type) == expected
    assert object_type_releases("space") == object_type_releases("Space")
    assert object_type_releases("Zoen") == ()


def test_partial_table_only_lists_types_some_release_lacks() -> None:
    folded = {t.casefold() for t in ALL_OBJECT_TYPES}
    assert set(PARTIAL_OBJECT_TYPES) <= folded
    assert "zone" not in PARTIAL_OBJECT_TYPES
    assert object_type_releases("Zone") == ENERGYPLUS_VERSIONS
    assert LATEST_VERSION in object_type_releases("Space")


def test_describe_presence_and_format_releases() -> None:
    assert describe_presence([(26, 2, 0)], [(26, 1, 0)]) == "added in 26.2.0"
    assert describe_presence([(9, 4, 0)], [(9, 5, 0)]) == "removed in 9.5.0"
    assert describe_presence([(9, 4, 0), (24, 1, 0)], [(9, 5, 0)]) == "exists in 9.4.0, 24.1.0"
    assert format_releases([(9, 4, 0), (9, 5, 0), (9, 6, 0)]) == "9.4.0 to 9.6.0"
