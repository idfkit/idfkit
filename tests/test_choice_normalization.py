"""Choice values are stored in the schema's spelling by default, and as written on opt-out.

The stubs type a choice field as ``Literal[...]`` in the schema's spelling. EnergyPlus matches
choices case-insensitively, so files routinely write ``WALL`` or ``autosize``. Unless a value is
stored in the schema's spelling, an exhaustive ``match`` that type-checks falls through at run time.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from idfkit import (
    load_epjson,
    load_idf,
    load_idf_with_diagnostics,
    new_document,
    save_idf,
    write_epjson,
    write_idf,
)
from idfkit.document import IDFDocument
from idfkit.objects import IDFObject

_V = (24, 1, 0)

_ODD_CASE_IDF = """\
Version, 24.1;

Zone, Z1;

Material,
  M1,                     !- Name
  mediumSMOOTH,           !- Roughness
  0.1, 1.0, 2000, 1000;

Construction, C1, M1;

BuildingSurface:Detailed,
  W1,                     !- Name
  WALL,                   !- Surface Type
  C1,                     !- Construction Name
  Z1,                     !- Zone Name
  ,                       !- Space Name
  outdoors,               !- Outside Boundary Condition
  ,                       !- Outside Boundary Condition Object
  SUNEXPOSED,             !- Sun Exposure
  windexposed,            !- Wind Exposure
  ,                       !- View Factor to Ground
  4,                      !- Number of Vertices
  0, 0, 3,  0, 0, 0,  10, 0, 0,  10, 0, 3;

Fan:ConstantVolume,
  F1,                     !- Name
  ,                       !- Availability Schedule Name
  0.7,                    !- Fan Total Efficiency
  600,                    !- Pressure Rise
  AUTOSIZE,               !- Maximum Flow Rate
  0.9,                    !- Motor Efficiency
  1,                      !- Motor In Airstream Fraction
  In,                     !- Air Inlet Node Name
  Out;                    !- Air Outlet Node Name

Output:Table:SummaryReports,
  allsummary,             !- Report 1 Name
  ZONECOMPONENTLOADSUMMARY; !- Report 2 Name

Material,
  M2,                     !- Name
  NotARoughness,          !- Roughness
  0.1, 1.0, 2000, 1000;
"""


@pytest.fixture
def odd_case_idf(tmp_path: Path) -> Path:
    path = tmp_path / "odd.idf"
    path.write_text(_ODD_CASE_IDF, encoding="latin-1")
    return path


def _odd_case_epjson(tmp_path: Path) -> Path:
    data: dict[str, Any] = {
        "Version": {"Version 1": {"version_identifier": "24.1"}},
        "Material": {
            "M1": {
                "roughness": "mediumSMOOTH",
                "thickness": 0.1,
                "conductivity": 1.0,
                "density": 2000,
                "specific_heat": 1000,
            }
        },
        "Fan:ConstantVolume": {
            "F1": {
                "fan_total_efficiency": 0.7,
                "pressure_rise": 600,
                "maximum_flow_rate": "AUTOSIZE",
                "air_inlet_node_name": "In",
                "air_outlet_node_name": "Out",
            }
        },
        "Output:Table:SummaryReports": {
            "Output:Table:SummaryReports 1": {"reports": [{"report_name": "allsummary"}]},
        },
    }
    path = tmp_path / "odd.epJSON"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _report_names(doc: IDFDocument) -> list[Any]:
    reports = doc["Output:Table:SummaryReports"].first()
    assert reports is not None
    return [group["report_name"] for group in reports.data["reports"]]


# ---------------------------------------------------------------------------
# IDF
# ---------------------------------------------------------------------------


class TestIdf:
    def test_choices_read_in_schema_spelling(self, odd_case_idf: Path) -> None:
        doc = load_idf(odd_case_idf)
        wall = doc["BuildingSurface:Detailed"]["W1"]
        assert wall.surface_type == "Wall"
        assert wall.outside_boundary_condition == "Outdoors"
        assert wall.sun_exposure == "SunExposed"
        assert wall.wind_exposure == "WindExposed"
        assert doc["Material"]["M1"].roughness == "MediumSmooth"

    def test_sizing_keyword_in_numeric_field(self, odd_case_idf: Path) -> None:
        doc = load_idf(odd_case_idf)
        assert doc["Fan:ConstantVolume"]["F1"].maximum_flow_rate == "Autosize"

    def test_extensible_group_choices(self, odd_case_idf: Path) -> None:
        assert _report_names(load_idf(odd_case_idf)) == ["AllSummary", "ZoneComponentLoadSummary"]

    def test_unlisted_value_kept_as_written(self, odd_case_idf: Path) -> None:
        doc = load_idf(odd_case_idf)
        assert doc["Material"]["M2"].roughness == "NotARoughness"

    def test_reference_fields_untouched(self, odd_case_idf: Path) -> None:
        wall = load_idf(odd_case_idf)["BuildingSurface:Detailed"]["W1"]
        assert wall.construction_name == "C1"
        assert wall.zone_name == "Z1"

    def test_opt_out_keeps_file_text(self, odd_case_idf: Path) -> None:
        doc = load_idf(odd_case_idf, normalize_choices=False)
        assert doc.normalize_choices is False
        wall = doc["BuildingSurface:Detailed"]["W1"]
        assert wall.surface_type == "WALL"
        assert wall.sun_exposure == "SUNEXPOSED"
        assert doc["Fan:ConstantVolume"]["F1"].maximum_flow_rate == "AUTOSIZE"
        assert _report_names(doc) == ["allsummary", "ZONECOMPONENTLOADSUMMARY"]

    def test_opt_out_is_independent_of_strict(self, odd_case_idf: Path) -> None:
        normalized = load_idf(odd_case_idf, strict=False)
        assert normalized.normalize_choices is True
        assert normalized["BuildingSurface:Detailed"]["W1"].surface_type == "Wall"
        raw = load_idf(odd_case_idf, strict=False, normalize_choices=False)
        assert raw.strict is False
        assert raw["BuildingSurface:Detailed"]["W1"].surface_type == "WALL"

    def test_with_diagnostics(self, odd_case_idf: Path) -> None:
        assert load_idf_with_diagnostics(odd_case_idf).document["Material"]["M1"].roughness == "MediumSmooth"
        raw = load_idf_with_diagnostics(odd_case_idf, normalize_choices=False).document
        assert raw["Material"]["M1"].roughness == "mediumSMOOTH"

    def test_written_in_schema_spelling(self, odd_case_idf: Path) -> None:
        text = write_idf(load_idf(odd_case_idf))
        assert text is not None
        assert "Wall," in text
        assert "WALL," not in text

    def test_reparse_of_output_is_equal(self, odd_case_idf: Path, tmp_path: Path) -> None:
        doc = load_idf(odd_case_idf)
        out = tmp_path / "out.idf"
        save_idf(doc, out)
        again = load_idf(out, normalize_choices=False)
        assert again["BuildingSurface:Detailed"]["W1"].surface_type == "Wall"


class TestPreserveFormatting:
    def test_unmodified_file_round_trips_byte_for_byte(self, odd_case_idf: Path) -> None:
        doc = load_idf(odd_case_idf, preserve_formatting=True)
        assert doc["BuildingSurface:Detailed"]["W1"].surface_type == "Wall"
        assert write_idf(doc) == odd_case_idf.read_text(encoding="latin-1")

    def test_assigning_same_choice_in_other_case_is_not_a_change(self, odd_case_idf: Path) -> None:
        doc = load_idf(odd_case_idf, preserve_formatting=True)
        wall = doc["BuildingSurface:Detailed"]["W1"]
        wall.surface_type = "wall"
        assert wall.source_text is not None
        assert write_idf(doc) == odd_case_idf.read_text(encoding="latin-1")

    def test_modified_object_is_written_in_schema_spelling(self, odd_case_idf: Path) -> None:
        doc = load_idf(odd_case_idf, preserve_formatting=True)
        doc["BuildingSurface:Detailed"]["W1"].construction_name = "C1"  # unchanged: still verbatim
        doc["Material"]["M1"].thickness = 0.2
        text = write_idf(doc)
        assert text is not None
        assert "MediumSmooth" in text
        assert "WALL," in text  # the untouched surface keeps the author's text

    def test_epjson_unmodified_round_trips(self, tmp_path: Path) -> None:
        path = _odd_case_epjson(tmp_path)
        doc = load_epjson(path, preserve_formatting=True)
        assert doc["Material"]["M1"].roughness == "MediumSmooth"
        assert write_epjson(doc) == path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# epJSON
# ---------------------------------------------------------------------------


class TestEpjson:
    def test_choices_read_in_schema_spelling(self, tmp_path: Path) -> None:
        doc = load_epjson(_odd_case_epjson(tmp_path))
        assert doc["Material"]["M1"].roughness == "MediumSmooth"
        assert doc["Fan:ConstantVolume"]["F1"].maximum_flow_rate == "Autosize"
        assert _report_names(doc) == ["AllSummary"]

    def test_opt_out_keeps_file_text(self, tmp_path: Path) -> None:
        doc = load_epjson(_odd_case_epjson(tmp_path), normalize_choices=False)
        assert doc.normalize_choices is False
        assert doc["Material"]["M1"].roughness == "mediumSMOOTH"
        assert doc["Fan:ConstantVolume"]["F1"].maximum_flow_rate == "AUTOSIZE"
        assert _report_names(doc) == ["allsummary"]

    def test_opt_out_still_writes_canonical_epjson(self, tmp_path: Path) -> None:
        doc = load_epjson(_odd_case_epjson(tmp_path), normalize_choices=False)
        out = json.loads(write_epjson(doc) or "")
        assert out["Material"]["M1"]["roughness"] == "MediumSmooth"


# ---------------------------------------------------------------------------
# add() and assignment
# ---------------------------------------------------------------------------


def _material(doc: IDFDocument, roughness: str) -> IDFObject:
    return doc.add(
        "Material", "M", roughness=roughness, thickness=0.1, conductivity=1.0, density=2000.0, specific_heat=900.0
    )


class TestAdd:
    def test_add_normalizes(self) -> None:
        doc = new_document(_V)
        assert _material(doc, "mediumrough").roughness == "MediumRough"

    def test_add_normalizes_before_validation(self) -> None:
        doc = new_document(_V)
        fan = doc.add(
            "Fan:ConstantVolume",
            "F",
            fan_total_efficiency=0.7,
            pressure_rise=600.0,
            maximum_flow_rate="AUTOSIZE",
            air_inlet_node_name="In",
            air_outlet_node_name="Out",
        )
        assert fan.maximum_flow_rate == "Autosize"

    def test_add_extensible_groups_without_mutating_input(self) -> None:
        doc = new_document(_V)
        groups = [{"report_name": "allsummary"}, {"report_name": "AllSummaryAndMonthly"}]
        obj = doc.add("Output:Table:SummaryReports", reports=groups)
        assert [g["report_name"] for g in obj.data["reports"]] == ["AllSummary", "AllSummaryAndMonthly"]
        assert groups == [{"report_name": "allsummary"}, {"report_name": "AllSummaryAndMonthly"}]

    def test_add_opt_out(self) -> None:
        doc = new_document(_V, normalize_choices=False)
        assert doc.normalize_choices is False
        assert _material(doc, "mediumrough").roughness == "mediumrough"

    def test_collection_add_normalizes(self) -> None:
        doc = new_document(_V)
        mat = doc["Material"].add(
            "M", roughness="ROUGH", thickness=0.1, conductivity=1.0, density=2000.0, specific_heat=900.0
        )
        assert mat.roughness == "Rough"


class TestAssignment:
    def test_attribute_assignment(self) -> None:
        doc = new_document(_V)
        mat = _material(doc, "Rough")
        mat.roughness = "VERYSMOOTH"  # pyright: ignore[reportAttributeAccessIssue]
        assert mat.roughness == "VerySmooth"

    def test_item_assignment_and_update(self) -> None:
        doc = new_document(_V)
        mat = _material(doc, "Rough")
        mat["Roughness"] = "smooth"
        assert mat.roughness == "Smooth"
        mat.update(roughness="MEDIUMSMOOTH")
        assert mat.roughness == "MediumSmooth"

    def test_assigning_canonical_value_in_other_case_is_not_a_change(self) -> None:
        doc = new_document(_V)
        mat = _material(doc, "Rough")
        before = mat.mutation_version
        mat.roughness = "ROUGH"  # pyright: ignore[reportAttributeAccessIssue]
        assert mat.mutation_version == before

    def test_unlisted_value_kept(self) -> None:
        doc = new_document(_V)
        mat = _material(doc, "Rough")
        mat.roughness = "Bumpy"  # pyright: ignore[reportAttributeAccessIssue]
        assert mat.roughness == "Bumpy"

    def test_extensible_group_writes(self) -> None:
        doc = new_document(_V)
        obj = doc.add("Output:Table:SummaryReports", reports=[{"report_name": "AllSummary"}])
        view = obj["reports"]
        view[0].report_name = "allsummaryandmonthly"
        view.append(report_name="zonecomponentloadsummary")
        view.insert(0, {"report_name": "ALLSUMMARY"})
        view[1].update(report_name="ALLSUMMARYANDMONTHLY")
        assert [g["report_name"] for g in obj.data["reports"]] == [
            "AllSummary",
            "AllSummaryAndMonthly",
            "ZoneComponentLoadSummary",
        ]
        obj["reports"] = [{"report_name": "allsummary"}]
        assert obj.data["reports"] == [{"report_name": "AllSummary"}]

    def test_assignment_opt_out(self) -> None:
        doc = new_document(_V, normalize_choices=False)
        mat = _material(doc, "Rough")
        mat.roughness = "VERYSMOOTH"  # pyright: ignore[reportAttributeAccessIssue]
        assert mat.roughness == "VERYSMOOTH"
        obj = doc.add("Output:Table:SummaryReports", reports=[{"report_name": "allsummary"}])
        obj["reports"].append(report_name="zonecomponentloadsummary")
        assert [g["report_name"] for g in obj.data["reports"]] == ["allsummary", "zonecomponentloadsummary"]

    def test_detached_object_is_not_normalized(self) -> None:
        obj = IDFObject("Material", "M", data={"roughness": "rough"})
        obj.roughness = "ROUGH"
        assert obj.roughness == "ROUGH"


# ---------------------------------------------------------------------------
# The flag
# ---------------------------------------------------------------------------


class TestFlag:
    def test_default_is_on(self) -> None:
        assert new_document(_V).normalize_choices is True
        assert IDFDocument(version=_V).normalize_choices is True

    def test_copy_keeps_the_flag(self, odd_case_idf: Path) -> None:
        raw = load_idf(odd_case_idf, normalize_choices=False)
        twin = raw.copy()
        assert twin.normalize_choices is False
        assert twin["BuildingSurface:Detailed"]["W1"].surface_type == "WALL"
        assert new_document(_V).copy().normalize_choices is True

    def test_flag_survives_pickle(self) -> None:
        import pickle

        doc = new_document(_V, normalize_choices=False)
        assert pickle.loads(pickle.dumps(doc)).normalize_choices is False  # noqa: S301

    def test_is_read_only(self) -> None:
        doc = new_document(_V)
        with pytest.raises(AttributeError):
            doc.normalize_choices = False  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]


def test_exhaustive_match_on_energyplus_example_file() -> None:
    """The acceptance case: ``5ZoneAirCooled.idf`` writes WALL, FLOOR, CEILING and ROOF."""
    from idfkit.simulation.config import find_energyplus

    try:
        config = find_energyplus()
    except Exception:
        pytest.skip("EnergyPlus not installed")
    path = config.install_dir / "ExampleFiles" / "5ZoneAirCooled.idf"
    if not path.exists():
        pytest.skip("5ZoneAirCooled.idf not shipped with this EnergyPlus")
    doc = load_idf(path)
    seen: set[str] = set()
    for surface in doc.building_surfaces:
        match surface.surface_type:
            case "Wall" | "Floor" | "Ceiling" | "Roof":
                seen.add(surface.surface_type)
            case _:  # pragma: no cover - the failure this guards against
                pytest.fail(f"{surface.name}: {surface.surface_type!r} is not in the schema's spelling")
    assert seen == {"Wall", "Floor", "Ceiling", "Roof"}
