"""NaN and infinity, which no EnergyPlus field takes, are refused where they enter and leave a document."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pytest

from idfkit import load_epjson, load_idf, load_idf_with_diagnostics, new_document, write_epjson, write_idf
from idfkit.document import IDFDocument
from idfkit.epjson_parser import get_epjson_version
from idfkit.epjson_parser import load_epjson as raw_load_epjson
from idfkit.exceptions import InvalidFieldError
from idfkit.objects import IDFObject
from idfkit.validation import validate_document

NON_FINITE = [float("nan"), float("inf"), float("-inf")]


def _material(doc: IDFDocument[Any]) -> IDFObject:
    return doc.add(
        "Material",
        "Brick",
        roughness="Rough",
        thickness=0.1,
        conductivity=1.0,
        density=1000.0,
        specific_heat=800.0,
    )


def _surface(doc: IDFDocument[Any]) -> IDFObject:
    doc.add("Zone", "Z")
    _material(doc)
    doc.add("Construction", "C", outside_layer="Brick")
    return doc.add(
        "BuildingSurface:Detailed",
        "Wall",
        surface_type="Wall",
        construction_name="C",
        zone_name="Z",
        outside_boundary_condition="Outdoors",
        vertices=[
            {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
            {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
        ],
    )


class TestEntry:
    @pytest.mark.parametrize("bad", NON_FINITE)
    def test_assignment_refused(self, bad: float) -> None:
        mat = _material(new_document())
        with pytest.raises(InvalidFieldError, match=r"Material 'Brick' field 'thickness' is (nan|inf|-inf)"):
            mat.thickness = bad
        assert mat.thickness == 0.1

    def test_item_assignment_refused(self) -> None:
        mat = _material(new_document())
        with pytest.raises(InvalidFieldError, match="thickness"):
            mat["thickness"] = float("nan")

    def test_add_refused_naming_the_field(self) -> None:
        doc = new_document()
        with pytest.raises(InvalidFieldError, match=r"thickness: non-finite") as info:
            doc.add(
                "Material",
                "Brick",
                roughness="Rough",
                thickness=float("nan"),
                conductivity=1.0,
                density=1000.0,
                specific_heat=800.0,
            )
        assert info.value.refused[0].reason == "non-finite"
        assert len(doc["Material"]) == 0

    def test_add_refused_without_validation(self) -> None:
        doc = new_document()
        with pytest.raises(InvalidFieldError, match="non-finite"):
            doc.add("Zone", "Z", x_origin=float("inf"), validate=False)

    def test_add_refuses_a_group_value(self) -> None:
        doc = new_document()
        _surface(doc)
        with pytest.raises(InvalidFieldError, match=r"vertices\[1\]\.vertex_y_coordinate: non-finite"):
            doc.add(
                "BuildingSurface:Detailed",
                "Wall 2",
                surface_type="Wall",
                construction_name="C",
                zone_name="Z",
                outside_boundary_condition="Outdoors",
                vertices=[
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": math.nan, "vertex_z_coordinate": 0.0},
                    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                ],
            )

    def test_update_refused_and_nothing_changed(self) -> None:
        mat = _material(new_document())
        with pytest.raises(InvalidFieldError, match="thickness: non-finite"):
            mat.update(conductivity=2.0, thickness=float("nan"))
        assert mat.conductivity == 1.0

    def test_group_slot_assignment_refused(self) -> None:
        surface = _surface(new_document())
        with pytest.raises(InvalidFieldError, match="vertex_x_coordinate"):
            surface.vertices[0].vertex_x_coordinate = float("inf")
        assert surface.vertices[0].vertex_x_coordinate == 0.0

    def test_group_append_and_replace_refused(self) -> None:
        surface = _surface(new_document())
        bad = {"vertex_x_coordinate": float("nan"), "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0}
        with pytest.raises(InvalidFieldError, match="vertex_x_coordinate"):
            surface.vertices.append(bad)
        with pytest.raises(InvalidFieldError, match="vertex_x_coordinate"):
            surface.vertices = [bad, bad, bad]
        assert len(surface.vertices) == 3

    def test_group_update_refused(self) -> None:
        surface = _surface(new_document())
        with pytest.raises(InvalidFieldError, match=r"'vertices\[1\]\.vertex_x_coordinate' is nan"):
            surface.vertices[1].update(vertex_x_coordinate=math.nan, vertex_y_coordinate=2.0)
        assert surface.data["vertices"][1] == {
            "vertex_x_coordinate": 0.0,
            "vertex_y_coordinate": 0.0,
            "vertex_z_coordinate": 0.0,
        }

    def test_group_append_names_the_new_index(self) -> None:
        surface = _surface(new_document())
        with pytest.raises(InvalidFieldError, match=r"'vertices\[3\]\.vertex_z_coordinate'"):
            surface.vertices.append(vertex_x_coordinate=1.0, vertex_y_coordinate=1.0, vertex_z_coordinate=math.inf)

    def test_update_wrapper_list_collected_with_other_refusals(self) -> None:
        surface = _surface(new_document())
        good = {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0}
        bad = {**good, "vertex_x_coordinate": math.nan}
        with pytest.raises(InvalidFieldError) as info:
            surface.update(vertices=[good, bad, good], bogus=1)
        assert [(e.name, e.reason) for e in info.value.refused] == [
            ("vertices[1].vertex_x_coordinate", "non-finite"),
            ("bogus", "unknown"),
        ]
        assert surface.vertices[0].vertex_z_coordinate == 3.0

    def test_unknown_key_holding_nan_is_refused_once_as_unknown(self) -> None:
        mat = _material(new_document())
        with pytest.raises(InvalidFieldError) as info:
            mat.update(foo=math.nan)
        assert [(e.name, e.reason) for e in info.value.refused] == [("foo", "unknown")]

    @pytest.mark.parametrize(
        ("key", "detail"), [("Thickness", "spell it 'thickness'"), ("foo", "not a field of Material")]
    )
    def test_add_reports_a_misspelled_nan_key_once_as_unknown(self, key: str, detail: str) -> None:
        doc = new_document()
        fields: dict[str, Any] = {
            "roughness": "Rough",
            "conductivity": 1.0,
            "density": 1000.0,
            "specific_heat": 800.0,
            key: math.nan,
        }
        with pytest.raises(InvalidFieldError) as info:
            doc.add("Material", "Brick", **fields)
        assert [(e.name, e.reason, e.detail) for e in info.value.refused] == [(key, "unknown", detail)]

    def test_finite_values_still_accepted(self) -> None:
        mat = _material(new_document())
        mat.thickness = 1e-300
        mat.conductivity = 1e300
        assert mat.thickness == 1e-300


class TestBackstops:
    """A value written straight into ``obj.data`` bypasses assignment; validation and writers catch it."""

    def test_validate_document_reports_e003(self) -> None:
        doc = new_document()
        _material(doc).data["thickness"] = float("nan")
        errors = validate_document(doc).errors
        assert [(e.code, e.field) for e in errors] == [("E003", "thickness")]
        assert "finite number" in errors[0].message

    def test_validate_document_reports_group_values(self) -> None:
        doc = new_document()
        _surface(doc).data["vertices"][2]["vertex_z_coordinate"] = float("inf")
        errors = [e for e in validate_document(doc).errors if e.code == "E003"]
        assert [e.field for e in errors] == ["vertices[2].vertex_z_coordinate"]

    def test_write_idf_refuses(self) -> None:
        doc = new_document()
        _material(doc).data["thickness"] = float("nan")
        with pytest.raises(ValueError, match=r"Material 'Brick' field 'thickness' is nan"):
            write_idf(doc)

    def test_write_idf_refuses_group_value(self) -> None:
        doc = new_document()
        _surface(doc).data["vertices"][1]["vertex_x_coordinate"] = float("-inf")
        with pytest.raises(ValueError, match=r"BuildingSurface:Detailed 'Wall' field 'vertex_x_coordinate' is -inf"):
            write_idf(doc)

    def test_write_epjson_refuses(self) -> None:
        doc = new_document()
        _material(doc).data["thickness"] = float("nan")
        with pytest.raises(ValueError, match=r"Material 'Brick' field 'thickness' is nan"):
            write_epjson(doc)

    def test_write_epjson_refuses_group_value(self) -> None:
        doc = new_document()
        _surface(doc).data["vertices"][0]["vertex_y_coordinate"] = float("nan")
        with pytest.raises(ValueError, match=r"vertices\[0\]\.vertex_y_coordinate"):
            write_epjson(doc)

    def test_write_epjson_output_is_strict_json(self) -> None:
        doc = new_document()
        _surface(doc)
        text = write_epjson(doc)

        def refuse(constant: str) -> Any:
            raise AssertionError(constant)

        json.loads(text, parse_constant=refuse)


class TestReading:
    @pytest.mark.parametrize("word", ["nan", "inf", "-Infinity", "NaN"])
    def test_idf_word_is_not_read_as_a_number(self, tmp_path: Path, word: str) -> None:
        path = tmp_path / "m.idf"
        path.write_text(f"Version,24.1;\nMaterial,Brick,Rough,{word},1,1000,800;\n", encoding="latin-1")
        assert load_idf(path)["Material"]["Brick"].thickness == word
        result = load_idf_with_diagnostics(path)
        assert [d.message for d in result.diagnostics] == [f"Field 'thickness' expects a number, got '{word}'"]
        doc = result.document
        assert doc["Material"]["Brick"].thickness == word
        assert [e.code for e in validate_document(doc).errors] == ["E003"]

    def test_epjson_nan_refused(self, tmp_path: Path) -> None:
        path = tmp_path / "m.epJSON"
        path.write_text(
            '{"Version": {"Version 1": {"version_identifier": "24.1"}},'
            ' "Material": {"Brick": {"roughness": "Rough", "thickness": NaN, "conductivity": 1,'
            ' "density": 1000, "specific_heat": 800}}}',
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="NaN is not valid JSON"):
            load_epjson(path)
        with pytest.raises(ValueError, match="NaN is not valid JSON"):
            raw_load_epjson(path)
        with pytest.raises(ValueError, match="NaN is not valid JSON"):
            get_epjson_version(path)
