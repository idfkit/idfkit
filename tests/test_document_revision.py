"""Tests for ``IDFDocument.revision`` and the derived-view cache (research R-06, R-21)."""

from __future__ import annotations

from idfkit import IDFDocument, new_document
from idfkit._derived import get_or_build


def _doc_with_zone() -> tuple[IDFDocument, int]:
    doc = new_document()
    doc.add("Zone", "Office")
    doc.add(
        "BuildingSurface:Detailed",
        "Wall 1",
        surface_type="Wall",
        construction_name="",
        zone_name="Office",
        outside_boundary_condition="Outdoors",
        sun_exposure="SunExposed",
        wind_exposure="WindExposed",
        validate=False,
    )
    return doc, doc.revision


class TestMutationsBumpOnce:
    def test_new_document_starts_low_and_add_bumps_once(self) -> None:
        doc = new_document()
        before = doc.revision
        doc.add("Zone", "Office")
        assert doc.revision == before + 1

    def test_remove_bumps_once(self) -> None:
        doc, before = _doc_with_zone()
        doc.removeidfobject(doc.getobject("Zone", "Office"))  # type: ignore[arg-type]
        assert doc.revision == before + 1

    def test_plain_field_assignment_bumps_once(self) -> None:
        doc, before = _doc_with_zone()
        zone = doc.getobject("Zone", "Office")
        assert zone is not None
        zone.x_origin = 3.0
        assert doc.revision == before + 1

    def test_reference_field_assignment_bumps_once(self) -> None:
        doc, before = _doc_with_zone()
        doc.add("Zone", "Lab")
        before = doc.revision
        wall = doc.getobject("BuildingSurface:Detailed", "Wall 1")
        assert wall is not None
        wall.zone_name = "Lab"
        assert doc.revision == before + 1

    def test_rename_bumps_once(self) -> None:
        doc, before = _doc_with_zone()
        doc.rename("Zone", "Office", "Office East")
        assert doc.revision == before + 1

    def test_name_assignment_bumps_once(self) -> None:
        doc, before = _doc_with_zone()
        zone = doc.getobject("Zone", "Office")
        assert zone is not None
        zone.name = "Office West"
        assert doc.revision == before + 1

    def test_extensible_edit_bumps(self) -> None:
        doc = new_document()
        doc.add("Zone", "A")
        doc.add("Zone", "B")
        zone_list = doc.add("ZoneList", "All", zones=[{"zone_name": "A"}], validate=False)
        before = doc.revision
        zone_list.zones.append(zone_name="B")
        assert doc.revision == before + 1

    def test_addidfobject_bumps_once(self) -> None:
        doc, _ = _doc_with_zone()
        other = new_document()
        copy = doc.getobject("Zone", "Office")
        assert copy is not None
        before = other.revision
        other.addidfobject(copy.copy())
        assert other.revision == before + 1

    def test_writing_the_same_value_is_not_a_change(self) -> None:
        doc, _ = _doc_with_zone()
        zone = doc.getobject("Zone", "Office")
        assert zone is not None
        zone.x_origin = 3.0
        before = doc.revision
        zone.x_origin = 3.0
        assert doc.revision == before

    def test_revision_is_monotonic(self) -> None:
        doc, _ = _doc_with_zone()
        seen = [doc.revision]
        zone = doc.getobject("Zone", "Office")
        assert zone is not None
        for value in (1.0, 2.0, 3.0):
            zone.x_origin = value
            seen.append(doc.revision)
        assert seen == sorted(seen)
        assert len(set(seen)) == len(seen)


class TestReadsDoNotBump:
    def test_reads_leave_revision_alone(self) -> None:
        doc, before = _doc_with_zone()
        zone = doc.getobject("Zone", "Office")
        assert zone is not None
        _ = zone.x_origin
        _ = zone.name
        _ = list(doc["Zone"])
        _ = doc.get_referencing("Office")
        _ = len(doc)
        _ = list(doc.all_objects)
        assert doc.revision == before


class TestGetOrBuild:
    def test_cached_until_revision_changes(self) -> None:
        doc, _ = _doc_with_zone()
        calls: list[int] = []

        def build() -> int:
            calls.append(doc.revision)
            return len(calls)

        first = get_or_build(doc, "view", build)
        second = get_or_build(doc, "view", build)
        assert first == second == 1
        assert len(calls) == 1

        zone = doc.getobject("Zone", "Office")
        assert zone is not None
        zone.x_origin = 9.0
        third = get_or_build(doc, "view", build)
        assert third == 2
        assert len(calls) == 2
        assert get_or_build(doc, "view", build) == 2
        assert len(calls) == 2

    def test_views_are_cached_separately(self) -> None:
        doc, _ = _doc_with_zone()
        assert get_or_build(doc, "a", lambda: "A") == "A"
        assert get_or_build(doc, "b", lambda: "B") == "B"
        assert get_or_build(doc, "a", lambda: "changed") == "A"

    def test_cache_belongs_to_one_document(self) -> None:
        doc1, _ = _doc_with_zone()
        doc2, _ = _doc_with_zone()
        assert get_or_build(doc1, "v", lambda: 1) == 1
        assert get_or_build(doc2, "v", lambda: 2) == 2

    def test_copy_starts_with_an_empty_cache(self) -> None:
        doc, _ = _doc_with_zone()
        get_or_build(doc, "v", lambda: "original")
        copied = doc.copy()
        assert get_or_build(copied, "v", lambda: "fresh") == "fresh"
