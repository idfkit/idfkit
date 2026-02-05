"""Tests for introspection module."""

from __future__ import annotations

import pytest

from idfkit import IDFDocument, new_document
from idfkit.introspection import FieldDescription, ObjectDescription, describe_object_type
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

    def test_repr_html(self) -> None:
        od = ObjectDescription(
            obj_type="Zone",
            memo="Test memo",
            fields=[FieldDescription(name="x_origin", field_type="number", required=True)],
            required_fields=["x_origin"],
        )
        html = od._repr_html_()
        assert "<h3>Zone</h3>" in html
        assert "<em>Test memo</em>" in html
        assert "x_origin" in html
        assert "<strong>*</strong>" in html  # Required marker


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

    def test_nameless_object(self, schema: EpJSONSchema) -> None:
        desc = describe_object_type(schema, "Timestep")
        assert desc.has_name is False


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
