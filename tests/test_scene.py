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

from idfkit import get_scene, load_idf, new_document, write_idf
from idfkit.scene import _READ, _UNREAD, Scene

_REPO = Path(__file__).resolve().parents[1]

#: Half the last place the engine's report prints, per coordinate. See the derivation in
#: ``runners/geometry_check.py``: it is a claim about one number, so the comparison is per
#: coordinate and not a distance between points.
TOLERANCE_M = 0.005

#: The four fixtures whose resolution this file asserts. The other three are the corpus's business:
#: ``lower-left-start`` is about the comparison rather than the rule, and ``simplified-only-unread``
#: and ``clockwise-entry`` have their own tests below and in later phases.
_FIXTURES = (
    "relative-zone-origin",
    "relative-zone-rotation",
    "north-axis-multizone",
    "world-nonzero-zone-origin",
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

    @pytest.mark.parametrize("fixture", (*_FIXTURES, "clockwise-entry", "lower-left-start", "simplified-only-unread"))
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

    def test_detailed_shading_resolves_and_is_marked_as_shading(self, tmp_path: Path) -> None:
        """FR-015. The 21 in ``world-nonzero-zone-origin`` are the only shading in the check set.

        Marked, not merely present: a consumer draws shading differently from a wall, and a shading
        surface that arrived looking like a heat transfer surface would be drawn as part of the
        building. It carries no zone, and its ``surface_type`` is its own object type, because the
        schema gives a shading surface no surface-type field to read one from.
        """
        source = tmp_path / "model.idf"
        source.write_text(_model_text("world-nonzero-zone-origin"), encoding="latin-1")
        scene = get_scene(load_idf(source))
        expected = _expected("world-nonzero-zone-origin")

        shading = [s for s in scene.surfaces if s.is_shading]
        assert len(shading) == 21
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
