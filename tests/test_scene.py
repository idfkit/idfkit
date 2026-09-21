"""Geometry extraction resolves where the engine resolves, and leaves the model alone.

The counterpart of the JavaScript package's scene tests, assertion for assertion, and the
library-side half of the corpus check ``checks/geometry-vertices``.

THE TWO SOURCES OF EVIDENCE, AND WHY BOTH.

The corpus holds the seven fixture models and the expectations EnergyPlus itself produced for them.
They are not committed here: they belong to the corpus, where the cross-language claim is made, and
copying them would give the same bytes two homes. So the corpus assertions run when a corpus
checkout is reachable and are skipped when it is not, following ``tests/weather/test_epw_sentinels``.

The constructed assertions run always. They are what makes this a guard rather than a courtesy:
``make test`` on a bare checkout still fails an extractor that mutates the document, drops a
surface, or normalises a starting vertex.
"""

from __future__ import annotations

import csv
import gzip
import os
from pathlib import Path

import pytest

from idfkit import Polygon3D, Vector3D, get_scene, load_idf, new_document, write_idf
from idfkit.scene import _READ, _UNREAD, Scene

_REPO = Path(__file__).resolve().parents[1]

#: Half the last place the engine's report prints, per coordinate. See the derivation in
#: ``runners/geometry_check.py``: it is a claim about one number, so the comparison is per
#: coordinate and not a distance between points.
TOLERANCE_M = 0.005

#: The five fixtures whose resolution this file asserts. The other two are the corpus's business:
#: ``lower-left-start`` is about the comparison rather than the rule, and ``simplified-only-unread``
#: resolves nothing and is asserted on its own terms below.
#:
#: ``clockwise-entry`` is the only one of the seven that declares clockwise entry, which is one
#: fewer than SC-004 states the set holds. The counterfactual below measures the clause on the model
#: that is actually committed rather than on the two the criterion assumes.
_FIXTURES = (
    "relative-zone-origin",
    "relative-zone-rotation",
    "north-axis-multizone",
    "world-nonzero-zone-origin",
    "clockwise-entry",
)


def _corpus_dir() -> Path | None:
    """The corpus checkout, or ``None`` when there is not one at hand."""
    for candidate in (
        os.environ.get("IDFKIT_CONFORMANCE_DIR"),
        _REPO / "conformance",
        _REPO.parent / "idfkit-conformance",
    ):
        if candidate is None:
            continue
        path = Path(candidate) / "checks" / "geometry-vertices"
        if (path / "fixtures").is_dir() and (path / "expected").is_dir():
            return path
    return None


CORPUS = _corpus_dir()


def _model_text(name: str) -> str:
    assert CORPUS is not None
    with gzip.open(CORPUS / "fixtures" / f"{name}.idf.gz", "rt", encoding="latin-1") as handle:
        return handle.read()


def _expected(name: str) -> dict[str, tuple[str, tuple[tuple[float, float, float], ...]]]:
    """The engine's rows for one fixture, keyed by upper-cased surface name."""
    assert CORPUS is not None
    rows: dict[str, tuple[str, tuple[tuple[float, float, float], ...]]] = {}
    with (CORPUS / "expected" / f"{name}.csv").open(encoding="utf-8", newline="") as handle:
        for fields in csv.reader(line for line in handle if not line.startswith("#")):
            if not fields or fields[0] == "kind":
                continue
            count = int(fields[4])
            flat = [float(value) for value in fields[5 : 5 + count * 3]]
            rows[fields[1].upper()] = (
                fields[3],
                tuple((flat[at], flat[at + 1], flat[at + 2]) for at in range(0, len(flat), 3)),
            )
    return rows


def _ring_error(resolved, reported) -> float:
    """Smallest worst-coordinate error over the cyclic rotations, orientation preserved.

    The corpus runner's function, restated here rather than imported, because this file must work on
    a checkout with no corpus beside it.
    """
    if len(resolved) != len(reported):
        return float("inf")
    count = len(resolved)
    return min(
        max(
            max(abs(a - b) for a, b in zip(resolved[(at + shift) % count].as_tuple(), reported[at], strict=True))
            for at in range(count)
        )
        for shift in range(count)
    )


def _write(doc) -> str:
    """The document as the preserving writer renders it, which is the byte-level comparison."""
    return write_idf(doc, preserve_formatting=True)


# ---------------------------------------------------------------------------
# Constructed: these run on a bare checkout
# ---------------------------------------------------------------------------


def _one_wall(**rules: str):
    """A single-zone model with one wall, built so each clause can be switched on alone."""
    model = new_document()
    # ``new_document`` already carries a GlobalGeometryRules, so each clause is switched by editing
    # the declaration rather than by adding a second one.
    declared = model["GlobalGeometryRules"].first()
    for name, value in rules.items():
        declared[name] = value
    model.add("Zone", "Z1", x_origin=10.0, y_origin=20.0, z_origin=0.0)
    model.add(
        "BuildingSurface:Detailed",
        "W1",
        surface_type="WALL",
        construction_name="",
        zone_name="Z1",
        outside_boundary_condition="Outdoors",
        number_of_vertices=4,
        vertices=[
            {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
            {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
            {"vertex_x_coordinate": 4, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
            {"vertex_x_coordinate": 4, "vertex_y_coordinate": 0, "vertex_z_coordinate": 3},
        ],
        validate=False,
    )
    return model


def _the_other_way(model):
    """The same wall, its ring traversed the other way from the same corner.

    The head is held and the tail reversed, which is what an author winding the other way writes.
    Reversing the whole list would move the starting vertex too, and the model would then differ in
    two respects rather than one.
    """
    wall = model["BuildingSurface:Detailed"].first()
    head, *tail = list(wall["vertices"])
    wall["vertices"] = [head, *reversed(tail)]
    return model


def _two_walls(**rules: str):
    """The one-wall model with a second wall six metres away in y.

    One wall lies in a plane, so its extent is flat in y and a defect in that coordinate cannot
    show. Two walls give the extent a non-zero size on all three axes. They share their x and z, so
    each of the six faces of the extent is touched by a vertex.

    W2 is wound the opposite way round from W1, so that the two outward normals point away from
    each other as the outward normals of the two long walls of a building do. The extent does not
    depend on this, but a model whose far wall faces inward while declaring ``Outdoors`` is a trap
    for anyone who reuses this helper for an assertion about normals.
    """
    model = _one_wall(**rules)
    model.add(
        "BuildingSurface:Detailed",
        "W2",
        surface_type="WALL",
        construction_name="",
        zone_name="Z1",
        outside_boundary_condition="Outdoors",
        number_of_vertices=4,
        vertices=[
            {"vertex_x_coordinate": 4, "vertex_y_coordinate": 6, "vertex_z_coordinate": 3},
            {"vertex_x_coordinate": 4, "vertex_y_coordinate": 6, "vertex_z_coordinate": 0},
            {"vertex_x_coordinate": 0, "vertex_y_coordinate": 6, "vertex_z_coordinate": 0},
            {"vertex_x_coordinate": 0, "vertex_y_coordinate": 6, "vertex_z_coordinate": 3},
        ],
        validate=False,
    )
    return model


class TestTheClausesAreConditional:
    def test_the_zone_origin_applies_under_relative(self) -> None:
        scene = get_scene(_one_wall(coordinate_system="Relative"))
        assert scene.surfaces[0].polygon.vertices[0].as_tuple() == (10.0, 20.0, 3.0)

    def test_the_zone_origin_does_not_apply_under_world(self) -> None:
        """The negative case, and the one the shipped private path gets wrong.

        Twelve of the example models declare World and carry a non-zero zone origin anyway.
        Applying it displaces every surface in them.
        """
        scene = get_scene(_one_wall(coordinate_system="World"))
        assert scene.surfaces[0].polygon.vertices[0].as_tuple() == (0.0, 0.0, 3.0)
        assert scene.applied.coordinate_system == "World"

    def test_clockwise_entry_reverses_the_ring_and_keeps_its_start(self) -> None:
        """Orientation is normalised; the starting vertex is not.

        Reversing a ring in place leaves the first vertex where the author put it, which is the
        distinction FR-008 draws and the corpus guards with ``lower-left-start``.
        """
        counter = get_scene(_one_wall(vertex_entry_direction="Counterclockwise")).surfaces[0].polygon
        clock = get_scene(_one_wall(vertex_entry_direction="Clockwise")).surfaces[0].polygon
        assert clock.vertices[0] == counter.vertices[0]
        assert [v.as_tuple() for v in clock.vertices[1:]] == [v.as_tuple() for v in reversed(counter.vertices[1:])]

    def test_the_classification_is_the_schema_s_spelling(self) -> None:
        """``WALL`` is authored, ``Wall`` is reported: the schema defines the value, not the file."""
        assert get_scene(_one_wall()).surfaces[0].surface_type == "Wall"

    def test_an_absent_rules_object_is_recorded_as_defaulted(self, tmp_path: Path) -> None:
        """A model stating neither object is read under the engine's assumptions, and says so.

        ``new_document`` supplies both, so this is parsed from text rather than built: the point is
        a document that genuinely lacks them.
        """
        source = tmp_path / "bare.idf"
        source.write_text("Version,26.1;\n\nZone,Z1;\n", encoding="latin-1")
        scene = get_scene(load_idf(source))
        assert "coordinate_system" in scene.applied.defaulted
        assert "north_axis" in scene.applied.defaulted
        assert scene.applied.coordinate_system == "Relative"


class TestASurfaceFacesTheWayTheModelSaysItFaces:
    """User story 4. The normal's sign comes from the declaration, not from the file's order.

    The corpus settles the clause against the engine on ``clockwise-entry``, which is the only
    committed model that declares it. What the corpus cannot settle is the invariance: that needs
    two models differing in exactly one declared field, and no example file ships with a twin. So
    the pair is constructed here, and it runs on a bare checkout.
    """

    def test_the_same_building_wound_either_way_carries_the_same_normal(self) -> None:
        """Acceptance scenario 3. Two models, one building, one answer.

        An author who winds the other way and says so has described no different wall. A consumer
        colouring by the sign of the normal, or culling back faces with it, must not be shown two
        buildings because two authors typed their vertices in different orders.
        """
        counter = _one_wall(vertex_entry_direction="Counterclockwise")
        clock = _the_other_way(_one_wall(vertex_entry_direction="Clockwise"))

        stated_counter = [dict(vertex) for vertex in counter["BuildingSurface:Detailed"].first()["vertices"]]
        stated_clock = [dict(vertex) for vertex in clock["BuildingSurface:Detailed"].first()["vertices"]]
        assert stated_counter != stated_clock, "the two models state the same vertices, so this proves nothing"

        one = get_scene(counter).surfaces[0]
        other = get_scene(clock).surfaces[0]
        assert one.normal == other.normal
        assert [v.as_tuple() for v in one.polygon.vertices] == [v.as_tuple() for v in other.polygon.vertices]
        assert one.normal == Vector3D(0.0, -1.0, 0.0)

    def test_the_declaration_alone_decides_the_sign(self) -> None:
        """The complement, and the reason the clause cannot be replaced by a winding heuristic.

        Same vertices, opposite declarations, opposite normals. A library that inferred the
        orientation from the geometry rather than reading the declaration would return one answer
        for both, and would be right about whichever model it happened to be shown.
        """
        one = get_scene(_one_wall(vertex_entry_direction="Counterclockwise")).surfaces[0]
        other = get_scene(_one_wall(vertex_entry_direction="Clockwise")).surfaces[0]
        assert one.normal == Vector3D(0.0, -1.0, 0.0)
        assert other.normal == Vector3D(0.0, 1.0, 0.0)

    def test_a_normal_is_a_unit_vector_in_every_reading(self) -> None:
        """FR-010 says outward normal, and a consumer lighting a face divides by nothing.

        ``Polygon3D.normal`` answers ``(0, 0, 1)`` for a degenerate ring, which is the one way a
        resolved surface could carry a direction that means nothing. A resolved surface cannot be
        degenerate, because a polygon of fewer than three vertices is unresolved with a reason.
        """
        for direction in ("Counterclockwise", "Clockwise"):
            normal = get_scene(_one_wall(vertex_entry_direction=direction)).surfaces[0].normal
            assert abs(normal.length() - 1.0) < 1e-12


class TestTheSceneCarriesItsExtent:
    """User story 5, FR-020. The extent encloses every resolved vertex and no more.

    These run on a bare checkout. The models have known dimensions, so the extent is asserted as an
    exact pair of corners rather than as a property of itself.
    """

    def test_the_extent_of_a_known_building_is_the_corners_of_that_building(self) -> None:
        bounds = get_scene(_two_walls(coordinate_system="World")).bounds
        assert bounds is not None
        assert bounds.min.as_tuple() == (0.0, 0.0, 0.0)
        assert bounds.max.as_tuple() == (4.0, 6.0, 3.0)

    def test_the_extent_is_of_the_resolved_geometry_and_not_of_the_stated_vertices(self) -> None:
        """The same two walls under Relative, where the zone origin moves them by (10, 20, 0).

        An extent taken from the vertices as written would be the World answer above for both
        models. This is the assertion that distinguishes the two.
        """
        bounds = get_scene(_two_walls(coordinate_system="Relative")).bounds
        assert bounds is not None
        assert bounds.min.as_tuple() == (10.0, 20.0, 0.0)
        assert bounds.max.as_tuple() == (14.0, 26.0, 3.0)

    def test_every_face_of_the_extent_is_touched_by_a_vertex(self) -> None:
        """``and no more`` is the half of FR-020 that a padded box would satisfy on enclosure alone."""
        scene = get_scene(_two_walls(coordinate_system="World"))
        assert scene.bounds is not None
        vertices = [vertex for surface in scene.surfaces for vertex in surface.polygon.vertices]
        for axis in ("x", "y", "z"):
            assert getattr(scene.bounds.min, axis) == min(getattr(vertex, axis) for vertex in vertices)
            assert getattr(scene.bounds.max, axis) == max(getattr(vertex, axis) for vertex in vertices)

    def test_an_object_that_did_not_resolve_does_not_enlarge_the_extent(self) -> None:
        """The extent is of the resolved geometry, so an unresolved object cannot stretch it.

        The orphan window here is a kilometre away. An extent taken over every geometry object the
        model states, rather than over the ones that were placed, would frame empty space.
        """
        model = _two_walls(coordinate_system="World")
        model.add(
            "FenestrationSurface:Detailed",
            "Orphan",
            surface_type="Window",
            construction_name="",
            building_surface_name="NoSuchWall",
            number_of_vertices=4,
            vertex_1_x_coordinate=1000,
            vertex_1_y_coordinate=0,
            vertex_1_z_coordinate=2,
            vertex_2_x_coordinate=1000,
            vertex_2_y_coordinate=0,
            vertex_2_z_coordinate=1,
            vertex_3_x_coordinate=1001,
            vertex_3_y_coordinate=0,
            vertex_3_z_coordinate=1,
            vertex_4_x_coordinate=1001,
            vertex_4_y_coordinate=0,
            vertex_4_z_coordinate=2,
            validate=False,
        )
        scene = get_scene(model)
        assert [entry.name for entry in scene.unresolved] == ["Orphan"]
        assert scene.bounds is not None
        assert scene.bounds.min.as_tuple() == (0.0, 0.0, 0.0)
        assert scene.bounds.max.as_tuple() == (4.0, 6.0, 3.0)

    def test_a_model_whose_geometry_all_failed_has_no_extent_rather_than_a_point(self) -> None:
        """FR-020's negative case on a model that states geometry and resolves none of it.

        The empty model and the model of unread types are asserted below. This is the third way a
        scene can hold no surfaces, and the one where an extent folded to a point at the origin
        would be most plausible, because vertices were read before the surface was refused.
        """
        model = _two_walls(coordinate_system="World")
        for wall in model["BuildingSurface:Detailed"]:
            wall["zone_name"] = "NoSuchZone"
        scene = get_scene(model)
        assert scene.surfaces == ()
        assert len(scene.unresolved) == 2
        assert scene.bounds is None


class TestNothingIsDroppedSilently:
    def test_an_empty_model_and_an_unread_model_are_different_answers(self) -> None:
        """FR-019, and the reason ``unattempted`` is a member rather than a count."""
        empty = get_scene(new_document())
        assert empty.surfaces == () and empty.unattempted == () and empty.bounds is None

        simplified = new_document()
        simplified.add("Zone", "Z1")
        simplified.add(
            "Wall:Exterior",
            "W1",
            construction_name="",
            zone_name="Z1",
            azimuth_angle=180.0,
            tilt_angle=90.0,
            starting_x_coordinate=0.0,
            starting_y_coordinate=0.0,
            starting_z_coordinate=0.0,
            length=4.0,
            height=3.0,
            validate=False,
        )
        scene = get_scene(simplified)
        assert scene.surfaces == ()
        assert len(scene.unattempted) == 1
        assert scene.unattempted[0].object_type == "Wall:Exterior"
        assert scene.unattempted[0].count == 1
        assert scene.bounds is None

    def test_a_fenestration_whose_parent_is_absent_is_unresolved_not_dropped(self) -> None:
        """FR-014. It never appears in ``surfaces``, because a window on no wall is not placed."""
        model = _one_wall()
        model.add(
            "FenestrationSurface:Detailed",
            "Orphan",
            surface_type="Window",
            construction_name="",
            building_surface_name="NoSuchWall",
            number_of_vertices=4,
            vertex_1_x_coordinate=1,
            vertex_1_y_coordinate=0,
            vertex_1_z_coordinate=2,
            vertex_2_x_coordinate=1,
            vertex_2_y_coordinate=0,
            vertex_2_z_coordinate=1,
            vertex_3_x_coordinate=2,
            vertex_3_y_coordinate=0,
            vertex_3_z_coordinate=1,
            vertex_4_x_coordinate=2,
            vertex_4_y_coordinate=0,
            vertex_4_z_coordinate=2,
            validate=False,
        )
        scene = get_scene(model)
        assert [s.name for s in scene.surfaces] == ["W1"]
        assert len(scene.unresolved) == 1
        assert scene.unresolved[0].name == "Orphan"
        assert scene.unresolved[0].reason == "parent-surface-not-found"
        # FR-014 asks for the missing parent by name. The reason says how to group the failure; the
        # name says which wall to go and find, without a second search through the document.
        assert scene.unresolved[0].missing_reference == "NoSuchWall"

    def test_a_surface_whose_zone_is_absent_names_the_zone_it_wanted(self) -> None:
        """The same defect class, and the same obligation: say what was pointed at."""
        model = _one_wall()
        model["BuildingSurface:Detailed"].first()["zone_name"] = "NoSuchZone"
        scene = get_scene(model)
        assert scene.surfaces == ()
        assert len(scene.unresolved) == 1
        assert scene.unresolved[0].reason == "zone-not-found"
        assert scene.unresolved[0].missing_reference == "NoSuchZone"

    def test_an_object_with_no_reference_to_miss_names_nothing(self) -> None:
        """``missing_reference`` is absent rather than empty when nothing was referenced."""
        model = _one_wall()
        wall = model["BuildingSurface:Detailed"].first()
        wall["vertices"] = [
            {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
            {"vertex_x_coordinate": 4, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
        ]
        scene = get_scene(model)
        assert len(scene.unresolved) == 1
        assert scene.unresolved[0].reason == "too-few-vertices"
        assert scene.unresolved[0].missing_reference is None


class TestEveryGeometryObjectIsAccountedFor:
    """SC-008 on a bare checkout: nothing in the model may vanish from the scene without a word."""

    #: The members of the schema's surfaces group that are not geometry objects, listed so that the
    #: sweep below can be exhaustive over the rest. A type is here because it states no surface: a
    #: zone or space is a container, a property object modifies a surface stated elsewhere,
    #: InternalMass states an area and a construction and no vertices, GlobalGeometryRules states
    #: the rules themselves, and GeometryTransform scales what is stated elsewhere.
    _NOT_GEOMETRY = frozenset({
        "GeometryTransform",
        "GlobalGeometryRules",
        "InternalMass",
        "ShadingProperty:Reflectance",
        "Space",
        "SpaceList",
        "WindowProperty:AirflowControl",
        "WindowProperty:FrameAndDivider",
        "WindowProperty:StormWindow",
        "WindowShadingControl",
        "Zone",
        "ZoneGroup",
        "ZoneList",
    })

    def test_every_surface_type_the_schema_knows_is_read_or_declared_unread(self) -> None:
        """The guard that catches a geometry type belonging to neither list.

        Counting the model against the two lists cannot catch a type absent from both: such a type
        is invisible to the count as it is to the scene, and the model reports as empty, which
        FR-019 exists to forbid. So the question is asked of the schema instead, which knows every
        surface type EnergyPlus has, rather than of the lists being checked.

        This is not hypothetical. It is how ``Wall:Detailed``, ``Floor:Detailed`` and
        ``RoofCeiling:Detailed`` were found: three detailed forms carrying explicit vertices, in
        neither list, and in no fixture, so nothing else would have said a word.
        """
        schema = new_document().schema
        assert schema is not None
        group = schema.get_group("BuildingSurface:Detailed")
        surfaces = {
            name for name in schema.object_types if schema.get_group(name) == group and name not in self._NOT_GEOMETRY
        }
        unaccounted = sorted(surfaces - set(_READ) - set(_UNREAD))
        assert not unaccounted, f"geometry types in neither list: {unaccounted}"

    def test_the_counts_add_up(self) -> None:
        """Resolved plus unresolved plus unattempted equals what the model holds."""
        model = _one_wall()
        model.add("Wall:Exterior", "Simple", construction_name="", zone_name="Z1", validate=False)
        model.add(
            "FenestrationSurface:Detailed",
            "Orphan",
            surface_type="Window",
            construction_name="",
            building_surface_name="NoSuchWall",
            number_of_vertices=3,
            vertex_1_x_coordinate=1,
            vertex_1_y_coordinate=0,
            vertex_1_z_coordinate=2,
            vertex_2_x_coordinate=1,
            vertex_2_y_coordinate=0,
            vertex_2_z_coordinate=1,
            vertex_3_x_coordinate=2,
            vertex_3_y_coordinate=0,
            vertex_3_z_coordinate=1,
            validate=False,
        )
        scene = get_scene(model)
        held = sum(len(model[object_type]) for object_type in (*_READ, *_UNREAD) if object_type in model)
        reported = len(scene.surfaces) + len(scene.unresolved) + sum(e.count for e in scene.unattempted)
        assert reported == held == 3


class TestBothListsComeBackInDocumentOrder:
    """FR-017a. The corpus compares both as sets, so only a direct assertion can catch a drift."""

    def test_unresolved_follows_the_file_and_not_the_type_order(self, tmp_path: Path) -> None:
        """The fenestration is stated first and must be reported first.

        Grouping by type would put the ``BuildingSurface:Detailed`` first, since it leads ``_READ``.
        The file says otherwise, and the file is what a reader is holding.
        """
        source = tmp_path / "model.idf"
        source.write_text(
            "Version, 26.1;\n"
            "GlobalGeometryRules, UpperLeftCorner, Counterclockwise, Relative;\n"
            "FenestrationSurface:Detailed, FirstStated, Window, , NoSuchWall, , , , , 3,\n"
            "  1,0,2, 1,0,1, 2,0,1;\n"
            "BuildingSurface:Detailed, SecondStated, Wall, , NoSuchZone, , Outdoors, , , , , 3,\n"
            "  0,0,3, 0,0,0, 4,0,0;\n",
            encoding="latin-1",
        )
        scene = get_scene(load_idf(source))
        assert [u.name for u in scene.unresolved] == ["FirstStated", "SecondStated"]

    def test_unattempted_follows_first_occurrence_and_not_the_list_order(self, tmp_path: Path) -> None:
        """``Window`` is stated before ``Wall:Exterior`` and must be named first.

        ``_UNREAD`` lists the walls before the windows, so a producer iterating that constant would
        report them the other way round and no corpus comparison would notice.
        """
        source = tmp_path / "model.idf"
        source.write_text(
            "Version, 26.1;\n"
            "Window, StatedFirst, , SomeWall, , 1, 0, 1, 1.5, 1.2;\n"
            "Wall:Exterior, StatedSecond, , Z1, , 180, 90, 0, 0, 0, 4, 3;\n",
            encoding="latin-1",
        )
        scene = get_scene(load_idf(source))
        assert [e.object_type for e in scene.unattempted] == ["Window", "Wall:Exterior"]
        assert [e.count for e in scene.unattempted] == [1, 1]


class TestTheDocumentIsUnchanged:
    def test_extraction_does_not_touch_a_constructed_model(self) -> None:
        model = _one_wall()
        before = _write(model)
        get_scene(model)
        assert _write(model) == before


# ---------------------------------------------------------------------------
# Corpus: the engine's own answer, when a checkout is reachable
# ---------------------------------------------------------------------------


@pytest.mark.skipif(CORPUS is None, reason="no idfkit-conformance checkout to read the fixtures from")
class TestAgainstTheEngine:
    @pytest.mark.parametrize("fixture", _FIXTURES)
    def test_the_document_is_unchanged(self, fixture: str, tmp_path: Path) -> None:
        """FR-003, and the guarantee the whole read-only view rests on.

        Not "unchanged in the fields extraction reads": unchanged. A preserving write before and
        after yields identical bytes.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        doc = load_idf(source)
        before = _write(doc)
        get_scene(doc)
        assert _write(doc) == before

    @pytest.mark.parametrize("fixture", _FIXTURES)
    def test_every_surface_agrees_with_the_engine(self, fixture: str, tmp_path: Path) -> None:
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        scene = get_scene(load_idf(source))
        expected = _expected(fixture)

        assert scene.surfaces, f"{fixture} resolved nothing"
        for surface in scene.surfaces:
            row = expected.get(surface.name.upper())
            assert row is not None, f"{fixture}: {surface.name} is not in the engine's report"
            error = _ring_error(surface.polygon.vertices, row[1])
            assert error <= TOLERANCE_M, f"{fixture}: {surface.name} is {error:.4f} m out"

    @pytest.mark.parametrize("fixture", _FIXTURES)
    def test_every_normal_points_where_the_engine_s_ring_points(self, fixture: str, tmp_path: Path) -> None:
        """FR-010 against the oracle rather than against this library's own arithmetic.

        The engine reports vertices and not normals, so the direction compared against is the one
        its own reported ring computes. That is not circular: the ring comparison is insensitive to
        where a ring starts, and a surface could agree with the engine as a set of corners while
        being traversed the other way. This is the assertion that says it is not.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        scene = get_scene(load_idf(source))
        expected = _expected(fixture)

        for surface in scene.surfaces:
            reported = Polygon3D([Vector3D(*vertex) for vertex in expected[surface.name.upper()][1]])
            agreement = surface.normal.dot(reported.normal)
            assert agreement > 0.999, f"{fixture}: {surface.name} faces {agreement:.4f} of the way the engine faces"

    def test_the_clockwise_model_needs_the_clause_it_declares(self, tmp_path: Path) -> None:
        """SC-004's measurement, taken rather than assumed.

        That ``clockwise-entry`` passes says the clause does no harm. What says the clause is
        load-bearing is what happens without it, and the way to ask without keeping a second
        implementation around is to undo it on the output: reverse each ring back, holding its head,
        which is exactly what a library that never wrote the clause would have returned.

        Every one of the eight surfaces then disagrees with the engine, and the worst is 4.0 m out.
        Three of the 726 geometry-bearing example models declare clockwise entry, so a library
        without the clause passes on 723 of them and is wrong about every surface of the other
        three: an error that reads as a modelling mistake rather than a library one, which is why
        SC-004 asks for the measurement.

        The criterion says two such models are in the set and one is, which is recorded beside
        ``_FIXTURES`` above rather than worked around here.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text("clockwise-entry"), encoding="latin-1")
        scene = get_scene(load_idf(source))
        expected = _expected("clockwise-entry")

        assert scene.applied.is_clockwise, "the fixture no longer declares clockwise entry"
        assert len(scene.surfaces) == 8

        worst = 0.0
        for surface in scene.surfaces:
            reported = expected[surface.name.upper()][1]
            vertices = list(surface.polygon.vertices)
            without_the_clause = [vertices[0], *reversed(vertices[1:])]
            error = _ring_error(without_the_clause, reported)
            assert error > TOLERANCE_M, f"{surface.name} agrees with the engine either way round"
            worst = max(worst, error)
        assert worst >= 4.0, f"the clause is worth {worst:.4f} m, and SC-004 claims at least 4.0 m"

    @pytest.mark.parametrize("fixture", _FIXTURES)
    def test_every_fenestration_names_the_parent_the_engine_names(self, fixture: str, tmp_path: Path) -> None:
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        scene = get_scene(load_idf(source))
        expected = _expected(fixture)

        windows = [s for s in scene.surfaces if s.parent_surface is not None]
        for surface in windows:
            base = expected[surface.name.upper()][0]
            assert surface.parent_surface.upper() == base.upper()
        if fixture == "world-nonzero-zone-origin":
            assert len(windows) == 24

    @pytest.mark.parametrize("fixture", _FIXTURES)
    def test_a_parent_is_carried_exactly_on_fenestration(self, fixture: str, tmp_path: Path) -> None:
        """FR-013 says exactly, and the engine's report is the reason that word has to be tested.

        The engine names a base surface for zone-attached shading too: 21 of the 99 rows in
        ``world-nonzero-zone-origin`` carry one. The scene deliberately does not, because
        ``parent_surface`` means the surface a fenestration sits on and nothing else. Without this
        assertion a reader comparing the two reports would have no way to tell the choice from an
        oversight, and a consumer grouping windows by that field would silently collect shading.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        scene = get_scene(load_idf(source))

        for surface in scene.surfaces:
            carried = surface.parent_surface is not None
            assert carried == (surface.object_type == "FenestrationSurface:Detailed"), (
                f"{fixture}: {surface.object_type} {surface.name} carries parent_surface={surface.parent_surface!r}"
            )

        if fixture == "world-nonzero-zone-origin":
            shading = [s for s in scene.surfaces if s.is_shading]
            assert len(shading) == 21
            assert all(s.parent_surface is None for s in shading)

    @pytest.mark.parametrize("fixture", (*_FIXTURES, "lower-left-start", "simplified-only-unread"))
    def test_nothing_in_the_model_is_missing_from_the_scene(self, fixture: str, tmp_path: Path) -> None:
        """SC-008 over all seven fixtures: every geometry object is resolved, refused, or counted.

        The constructed version of this runs on a bare checkout. This one runs it over real models,
        where the counts are large enough that a surface dropped in one branch of the resolution
        would not stand out in a total anyone eyeballed.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        doc = load_idf(source)
        scene = get_scene(doc)

        held = sum(len(doc[object_type]) for object_type in (*_READ, *_UNREAD) if object_type in doc)
        reported = len(scene.surfaces) + len(scene.unresolved) + sum(e.count for e in scene.unattempted)
        assert reported == held, (
            f"{fixture}: model holds {held} geometry objects, scene accounts for {reported} "
            f"({len(scene.surfaces)} resolved, {len(scene.unresolved)} unresolved, "
            f"{sum(e.count for e in scene.unattempted)} unattempted)"
        )

    @pytest.mark.parametrize(("fixture", "count"), (("world-nonzero-zone-origin", 21), ("relative-zone-origin", 3)))
    def test_detailed_shading_resolves_and_is_marked_as_shading(self, fixture: str, count: int, tmp_path: Path) -> None:
        """FR-015 over both fixtures that carry shading: 21 surfaces in one and 3 in the other.

        All 24 are ``Shading:Zone:Detailed``, the zone-attached form, which is the one FR-015 names
        because it resolves against its zone's frame rather than against the building's. The other
        two detailed forms are read by the same branch and are not in the check set, so the type
        assertion below is the only thing standing behind them here.

        Marked, not merely present: a consumer draws shading differently from a wall, and a shading
        surface that arrived looking like a heat transfer surface would be drawn as part of the
        building. It carries no zone, and its ``surface_type`` is its own object type, because the
        schema gives a shading surface no surface-type field to read one from.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        scene = get_scene(load_idf(source))
        expected = _expected(fixture)

        shading = [s for s in scene.surfaces if s.is_shading]
        assert len(shading) == count
        for surface in shading:
            assert surface.object_type in {
                "Shading:Site:Detailed",
                "Shading:Building:Detailed",
                "Shading:Zone:Detailed",
            }
            assert surface.surface_type == surface.object_type
            assert surface.zone == ""
            assert expected[surface.name.upper()][1], f"{surface.name} is not in the engine's report"

        assert all(not s.is_shading for s in scene.surfaces if s.object_type == "BuildingSurface:Detailed")

    # ``lower-left-start`` joins the five here. It is excluded from ``_FIXTURES`` because it is
    # about the starting-vertex comparison rather than about a rule, and an extent is a per-axis
    # minimum and maximum over a ring, which is insensitive to where that ring starts. So its 41
    # surfaces are an oracle this claim can have for nothing.
    @pytest.mark.parametrize("fixture", (*_FIXTURES, "lower-left-start"))
    def test_the_extent_is_the_extent_of_the_vertices_the_engine_reports(self, fixture: str, tmp_path: Path) -> None:
        """FR-020 against the oracle rather than against this library's own vertices.

        The constructed assertions above take the extent over what this library resolved, so an
        extent and a resolution that are wrong in the same way agree with each other. Here the six
        extremes are computed from the engine's report.

        The oracle is restricted to the surfaces the scene resolved, so a surface dropped from the
        scene altogether is dropped from both sides of this comparison and passes. That case is
        ``test_nothing_in_the_model_is_missing_from_the_scene``; what this catches is an extent
        computed over anything other than the geometry that was resolved.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text(fixture), encoding="latin-1")
        scene = get_scene(load_idf(source))
        expected = _expected(fixture)
        assert scene.bounds is not None

        absent = [surface.name for surface in scene.surfaces if surface.name.upper() not in expected]
        assert not absent, f"{fixture}: {absent} are not in the engine's report"

        reported = [vertex for surface in scene.surfaces for vertex in expected[surface.name.upper()][1]]
        for axis, at in (("x", 0), ("y", 1), ("z", 2)):
            low, high = min(v[at] for v in reported), max(v[at] for v in reported)
            assert abs(getattr(scene.bounds.min, axis) - low) <= TOLERANCE_M, f"{fixture}: min {axis}"
            assert abs(getattr(scene.bounds.max, axis) - high) <= TOLERANCE_M, f"{fixture}: max {axis}"

    def test_the_unread_model_resolves_nothing_and_says_what_it_saw(self, tmp_path: Path) -> None:
        source = tmp_path / "model.idf"
        source.write_text(_model_text("simplified-only-unread"), encoding="latin-1")
        scene = get_scene(load_idf(source))
        assert scene.surfaces == ()
        assert scene.bounds is None
        assert sum(entry.count for entry in scene.unattempted) > 0
        assert "Wall:Exterior" in {entry.object_type for entry in scene.unattempted}

    def test_the_scene_is_stable_across_runs(self, tmp_path: Path) -> None:
        """Guarantee 5. Two runs of the same input agree, so a diff of two scenes is readable."""
        source = tmp_path / "model.idf"
        source.write_text(_model_text("relative-zone-origin"), encoding="latin-1")
        first: Scene = get_scene(load_idf(source))
        second: Scene = get_scene(load_idf(source))
        assert [s.name for s in first.surfaces] == [s.name for s in second.surfaces]
        assert first.bounds == second.bounds
