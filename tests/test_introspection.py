"""Tests for introspection module."""

from __future__ import annotations

import pytest

from idfkit import IDFDocument, new_document
from idfkit.introspection import (
    FieldDescription,
    ObjectDescription,
    _get_field_type,  # pyright: ignore[reportPrivateUsage]
    describe_object_type,
)
from idfkit.schema import EpJSONSchema, get_schema


@pytest.fixture
def schema() -> EpJSONSchema:
    """Load the v24.1.0 schema."""
    return get_schema((24, 1, 0))


class TestFieldDescription:
    def test_basic_str(self) -> None:
        fd = FieldDescription(name="x_origin", field_type="number", units="m")
        s = str(fd)
        assert "x_origin" in s
        assert "(number)" in s
        assert "[m]" in s

    def test_required_marker(self) -> None:
        fd = FieldDescription(name="roughness", required=True)
        s = str(fd)
        assert "[REQUIRED]" in s

    def test_enum_values_short(self) -> None:
        fd = FieldDescription(name="roughness", enum_values=["Smooth", "Rough"])
        s = str(fd)
        assert "choices=" in s
        assert "Smooth" in s

    def test_enum_values_truncated(self) -> None:
        fd = FieldDescription(
            name="roughness",
            enum_values=["VeryRough", "Rough", "MediumRough", "MediumSmooth", "Smooth", "VerySmooth"],
        )
        s = str(fd)
        assert "+3 more" in s

    def test_default_value(self) -> None:
        fd = FieldDescription(name="x_origin", default=0)
        s = str(fd)
        assert "default=0" in s

    def test_min_max(self) -> None:
        fd = FieldDescription(name="thickness", minimum=0, maximum=10)
        s = str(fd)
        assert "min=0" in s
        assert "max=10" in s

    def test_exclusive_min_max(self) -> None:
        fd = FieldDescription(name="thickness", exclusive_minimum=0.0, exclusive_maximum=100.0)
        s = str(fd)
        assert "min>0.0" in s
        assert "max<100.0" in s

    def test_reference_marker(self) -> None:
        fd = FieldDescription(name="zone_name", is_reference=True, object_list=["ZoneNames"])
        s = str(fd)
        assert "(reference)" in s


class TestObjectDescription:
    def test_basic_str(self) -> None:
        od = ObjectDescription(
            obj_type="Zone",
            memo="A zone is a thermal region.",
            fields=[
                FieldDescription(name="x_origin", field_type="number", units="m"),
                FieldDescription(name="y_origin", field_type="number", units="m"),
            ],
            required_fields=["x_origin"],
        )
        s = str(od)
        assert "=== Zone ===" in s
        assert "A zone is a thermal region." in s
        assert "Required fields: x_origin" in s
        assert "Fields (2):" in s
        assert "x_origin" in s
        assert "y_origin" in s

    def test_extensible_note(self) -> None:
        od = ObjectDescription(obj_type="Schedule:Compact", is_extensible=True, extensible_size=2)
        s = str(od)
        assert "Extensible object" in s
        assert "groups of 2" in s

    def test_repr_html_basic(self) -> None:
        od = ObjectDescription(
            obj_type="Zone",
            memo="Test memo",
            fields=[FieldDescription(name="x_origin", field_type="number", required=True)],
            required_fields=["x_origin"],
        )
        html = od._repr_html_()  # pyright: ignore[reportPrivateUsage]
        assert "<h3>Zone</h3>" in html
        assert "<em>Test memo</em>" in html
        assert "x_origin" in html
        assert "<strong>*</strong>" in html  # Required marker

    def test_repr_html_enum_short(self) -> None:
        od = ObjectDescription(
            obj_type="Material",
            fields=[FieldDescription(name="roughness", enum_values=["Smooth", "Rough"])],
        )
        html = od._repr_html_()  # pyright: ignore[reportPrivateUsage]
        assert "choices:" in html
        assert "Smooth" in html

    def test_repr_html_enum_truncated(self) -> None:
        od = ObjectDescription(
            obj_type="Material",
            fields=[
                FieldDescription(
                    name="roughness",
                    enum_values=["VeryRough", "Rough", "MediumRough", "MediumSmooth", "Smooth", "VerySmooth"],
                )
            ],
        )
        html = od._repr_html_()  # pyright: ignore[reportPrivateUsage]
        assert "total" in html

    def test_repr_html_minimum_and_maximum(self) -> None:
        od = ObjectDescription(
            obj_type="Material",
            fields=[FieldDescription(name="thickness", minimum=0.0, maximum=10.0)],
        )
        html = od._repr_html_()  # pyright: ignore[reportPrivateUsage]
        assert "min:" in html
        assert "max:" in html

    def test_repr_html_reference_field(self) -> None:
        od = ObjectDescription(
            obj_type="Zone",
            fields=[FieldDescription(name="zone_name", is_reference=True, object_list=["ZoneNames"])],
        )
        html = od._repr_html_()  # pyright: ignore[reportPrivateUsage]
        assert "reference" in html

    def test_repr_html_extensible_note(self) -> None:
        od = ObjectDescription(obj_type="Schedule:Compact", is_extensible=True, extensible_size=3)
        html = od._repr_html_()  # pyright: ignore[reportPrivateUsage]
        assert "Extensible object" in html
        assert "groups of 3" in html

    def test_repr_html_no_memo_no_required(self) -> None:
        od = ObjectDescription(obj_type="Timestep", fields=[])
        html = od._repr_html_()  # pyright: ignore[reportPrivateUsage]
        assert "<h3>Timestep</h3>" in html
        assert "<em>" not in html
        assert "Required:" not in html


class TestDescribeObjectType:
    def test_zone(self, schema: EpJSONSchema) -> None:
        desc = describe_object_type(schema, "Zone")
        assert desc.obj_type == "Zone"
        assert desc.has_name is True
        assert len(desc.fields) > 0

        # Check that common Zone fields are present
        field_names = [f.name for f in desc.fields]
        assert "direction_of_relative_north" in field_names
        assert "x_origin" in field_names
        assert "y_origin" in field_names
        assert "z_origin" in field_names

    def test_material(self, schema: EpJSONSchema) -> None:
        desc = describe_object_type(schema, "Material")
        assert desc.obj_type == "Material"

        # Check required fields
        assert len(desc.required_fields) > 0
        assert "roughness" in desc.required_fields

        # Find roughness field and check it has enum values
        roughness = next((f for f in desc.fields if f.name == "roughness"), None)
        assert roughness is not None
        assert roughness.enum_values is not None
        assert "MediumSmooth" in roughness.enum_values

    def test_unknown_object_type_raises(self, schema: EpJSONSchema) -> None:
        with pytest.raises(KeyError, match="Unknown object type"):
            describe_object_type(schema, "NonexistentObjectType")

    def test_extensible_object(self, schema: EpJSONSchema) -> None:
        desc = describe_object_type(schema, "Schedule:Compact")
        assert desc.is_extensible is True
        assert desc.extensible_size is not None
        assert desc.extensible_size > 0
        field_names = [f.name for f in desc.fields]
        assert "field" in field_names

    def test_extensible_surface_includes_vertex_fields(self, schema: EpJSONSchema) -> None:
        desc = describe_object_type(schema, "BuildingSurface:Detailed")
        field_names = [f.name for f in desc.fields]
        assert "vertex_x_coordinate" in field_names
        assert "vertex_y_coordinate" in field_names
        assert "vertex_z_coordinate" in field_names

    def test_extensible_fields_have_field_type(self, schema: EpJSONSchema) -> None:
        """Extensible fields must have field_type populated (GH-92)."""
        desc = describe_object_type(schema, "Foundation:Kiva")
        ext_fields = {f.name: f for f in desc.fields if f.name.startswith("custom_block_")}
        assert len(ext_fields) == 4
        for name, f in ext_fields.items():
            assert f.field_type is not None, f"{name} has field_type=None"

        # Also verify BuildingSurface:Detailed vertex fields
        desc2 = describe_object_type(schema, "BuildingSurface:Detailed")
        vertex_fields = [f for f in desc2.fields if f.name.startswith("vertex_")]
        assert all(f.field_type == "number" for f in vertex_fields)

    def test_nameless_object(self, schema: EpJSONSchema) -> None:
        desc = describe_object_type(schema, "Timestep")
        assert desc.has_name is False

    def test_field_names_fallback_to_properties_keys(self, schema: EpJSONSchema) -> None:
        """When legacy_idd has no field_names entry, properties keys are used as fallback.

        ``Timestep`` has no entry in the legacy_idd order list, so ``get_field_names``
        returns ``[]`` and ``describe_object_type`` falls back to ``properties.keys()``.
        """
        desc = describe_object_type(schema, "Timestep")
        assert len(desc.fields) > 0


class TestGetFieldType:
    def test_direct_type(self) -> None:
        result = _get_field_type({"type": "number"})
        assert result == "number"

    def test_anyof_prefers_number(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "string"}, {"type": "number"}]}
        result = _get_field_type(field_schema)
        assert result == "number"

    def test_anyof_prefers_integer(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "string"}, {"type": "integer"}]}
        result = _get_field_type(field_schema)
        assert result == "integer"

    def test_anyof_falls_back_to_string(self) -> None:
        field_schema: dict[str, object] = {"anyOf": [{"type": "string"}, {"enum": ["A", "B"]}]}
        result = _get_field_type(field_schema)
        assert result == "string"

    def test_anyof_enum_only_subschemas_returns_none(self) -> None:
        """anyOf with only enum sub-schemas (no 'type' key) returns None."""
        field_schema: dict[str, object] = {"anyOf": [{"enum": ["A", "B"]}]}
        result = _get_field_type(field_schema)
        assert result is None

    def test_enum_only_returns_string(self) -> None:
        result = _get_field_type({"enum": ["Yes", "No"]})
        assert result == "string"

    def test_empty_schema_returns_none(self) -> None:
        result = _get_field_type({})
        assert result is None


class TestDescribeObjectTypeExtensibleAlreadyInFieldNames:
    def test_extensible_field_already_in_field_names_not_duplicated(self, schema: EpJSONSchema) -> None:
        """Extensible fields already present in field_names should not be appended again.

        ``Site:SpectrumData`` has extensible fields (wavelength, spectrum) that also
        appear in the legacy_idd field_names, so ``ext_name not in field_names`` is
        False for those, exercising the loop-continue branch.
        """
        desc = describe_object_type(schema, "Site:SpectrumData")
        field_names = [f.name for f in desc.fields]
        # Confirm the extensible fields are present (not duplicated)
        assert field_names.count("wavelength") == 1
        assert field_names.count("spectrum") == 1


class TestDescribeObjectTypeEnumFromAnyOf:
    def test_enum_extracted_from_anyof(self, schema: EpJSONSchema) -> None:
        """Fields using anyOf-wrapped enums should still expose enum_values."""
        # Use a type known to have anyOf with enum (e.g. fields that allow empty string or enum)
        # Verify the describe path picks up enum values from anyOf sub-schemas
        desc = describe_object_type(schema, "Material")
        roughness = next((f for f in desc.fields if f.name == "roughness"), None)
        assert roughness is not None
        assert roughness.enum_values is not None


class TestIDFDocumentDescribe:
    def test_describe_zone(self) -> None:
        model = new_document(version=(24, 1, 0))
        desc = model.describe("Zone")
        assert isinstance(desc, ObjectDescription)
        assert desc.obj_type == "Zone"

        # Verify output can be printed
        output = str(desc)
        assert "Zone" in output
        assert "x_origin" in output

    def test_describe_material(self) -> None:
        model = new_document(version=(24, 1, 0))
        desc = model.describe("Material")

        # Check that required fields are identified
        assert "roughness" in desc.required_fields
        assert "thickness" in desc.required_fields

    def test_describe_unknown_type_raises(self) -> None:
        model = new_document(version=(24, 1, 0))
        with pytest.raises(KeyError):
            model.describe("NonexistentType")

    def test_describe_no_schema_raises(self) -> None:
        # Create document without schema
        model = IDFDocument(version=(24, 1, 0))
        with pytest.raises(ValueError, match="No schema loaded"):
            model.describe("Zone")
