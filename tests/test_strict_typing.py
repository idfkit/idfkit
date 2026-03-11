"""Tests for strict typing features: Generic IDFDocument, IDFCollection, and stub generation."""

from __future__ import annotations

import pytest

from idfkit import IDFObject, new_document
from idfkit.objects import IDFCollection


class TestIDFDocumentStrict:
    """Test IDFDocument's strict (read-only) property and Generic[Strict] behavior."""

    def test_strict_default_false(self) -> None:
        doc = new_document()
        assert doc.strict is False

    def test_strict_true(self) -> None:
        doc = new_document(strict=True)
        assert doc.strict is True

    def test_strict_immutable(self) -> None:
        doc = new_document()
        with pytest.raises(AttributeError):
            doc.strict = True  # type: ignore[misc]

    def test_strict_preserved_on_copy(self) -> None:
        doc = new_document(strict=True)
        copy = doc.copy()
        assert copy.strict is True

    def test_non_strict_preserved_on_copy(self) -> None:
        doc = new_document(strict=False)
        copy = doc.copy()
        assert copy.strict is False

    def test_strict_true_raises_on_unknown_field(self) -> None:
        doc = new_document(strict=True)
        zone = doc.add("Zone", "TestZone")
        with pytest.raises(AttributeError):
            _ = zone.nonexistent_field_xyz

    def test_non_strict_returns_none_for_unknown_field(self) -> None:
        doc = new_document(strict=False)
        zone = doc.add("Zone", "TestZone")
        assert zone.nonexistent_field_xyz is None


class TestIDFCollectionGeneric:
    """Test that IDFCollection is generic and properly typed."""

    def test_collection_is_generic(self) -> None:
        """IDFCollection should accept a type parameter."""
        # This mainly tests that the Generic usage doesn't break runtime
        doc = new_document()
        zones = doc["Zone"]
        assert isinstance(zones, IDFCollection)

    def test_collection_iteration(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1")
        doc.add("Zone", "Z2")
        zones = doc["Zone"]
        zone_names = [z.name for z in zones]
        assert "Z1" in zone_names
        assert "Z2" in zone_names

    def test_collection_add_returns_object(self) -> None:
        doc = new_document()
        zone = doc.add("Zone", "TestZone")
        assert isinstance(zone, IDFObject)
        assert zone.name == "TestZone"

    def test_collection_first(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1")
        first = doc["Zone"].first()
        assert first is not None
        assert first.name == "Z1"

    def test_collection_filter(self) -> None:
        doc = new_document()
        doc.add("Zone", "Office1", x_origin=0.0)
        doc.add("Zone", "Office2", x_origin=10.0)
        result = doc["Zone"].filter(lambda z: z.x_origin == 0.0)
        assert len(result) == 1
        assert result[0].name == "Office1"

    def test_collection_to_list(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1")
        zone_list = doc["Zone"].to_list()
        assert isinstance(zone_list, list)
        assert len(zone_list) == 1


class TestStubGeneration:
    """Test the codegen module for generating type stubs."""

    def test_generate_stubs_produces_content(self) -> None:
        from idfkit.codegen.generate_stubs import generate_stubs

        content = generate_stubs((24, 1, 0))
        assert "class Zone(IDFObject):" in content
        assert "class Building(IDFObject):" in content
        assert "class Material(IDFObject):" in content

    def test_generate_stubs_has_typed_fields(self) -> None:
        from idfkit.codegen.generate_stubs import generate_stubs

        content = generate_stubs((24, 1, 0))
        assert "x_origin: float | None" in content
        assert "y_origin: float | None" in content

    def test_generate_stubs_skips_invalid_identifiers(self) -> None:
        from idfkit.codegen.generate_stubs import generate_stubs

        content = generate_stubs((24, 1, 0))
        # Field names starting with digits should be skipped
        assert "def 100_" not in content
        assert "def 2017_" not in content

    def test_generate_document_pyi_has_overloads(self) -> None:
        from idfkit.codegen.generate_stubs import generate_document_pyi

        content = generate_document_pyi((24, 1, 0))
        assert "class IDFDocument" in content
        assert "@overload" in content
        assert 'Literal["Zone"]' in content
        assert 'Literal["Building"]' in content

    def test_generate_document_pyi_has_generic_strict(self) -> None:
        from idfkit.codegen.generate_stubs import generate_document_pyi

        content = generate_document_pyi((24, 1, 0))
        assert "Generic[Strict]" in content
        assert "TypeVar" in content

    def test_to_class_name(self) -> None:
        from idfkit.codegen.generate_stubs import _to_class_name

        assert _to_class_name("BuildingSurface:Detailed") == "BuildingSurfaceDetailed"
        assert _to_class_name("Material:AirGap") == "MaterialAirGap"
        assert _to_class_name("Zone") == "Zone"
        assert _to_class_name("OS:Zone") == "OSZone"

    def test_schema_type_to_python(self) -> None:
        from idfkit.codegen.generate_stubs import _schema_type_to_python

        assert _schema_type_to_python(None, "number") == "float"
        assert _schema_type_to_python(None, "integer") == "int"
        assert _schema_type_to_python(None, "string") == "str"
        assert _schema_type_to_python(None, "array") == "list[Any]"
        assert _schema_type_to_python(None, None) == "str | float"

    def test_schema_type_to_python_any_of(self) -> None:
        from idfkit.codegen.generate_stubs import _schema_type_to_python

        field_schema = {"anyOf": [{"type": "number"}, {"type": "string"}]}
        result = _schema_type_to_python(field_schema, None, has_any_of=True)
        assert "float" in result
        assert "str" in result


class TestLoadIdfStrictFields:
    """Test that load_idf's strict_fields parameter works."""

    def test_load_idf_default_non_strict(self, tmp_path: pytest.TempPathFactory) -> None:
        from idfkit import load_idf, write_idf

        # Create a minimal IDF file
        doc = new_document()
        path = tmp_path / "test.idf"  # type: ignore[operator]
        write_idf(doc, str(path))

        loaded = load_idf(str(path))
        assert loaded.strict is False

    def test_load_idf_strict_fields(self, tmp_path: pytest.TempPathFactory) -> None:
        from idfkit import load_idf, write_idf

        doc = new_document()
        path = tmp_path / "test.idf"  # type: ignore[operator]
        write_idf(doc, str(path))

        loaded = load_idf(str(path), strict_fields=True)
        assert loaded.strict is True
