"""Tests for strict typing features: Generic IDFDocument, IDFCollection, and stub generation."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from idfkit import IDFObject, new_document
from idfkit.objects import IDFCollection


class TestIDFDocumentStrict:
    """Test IDFDocument's strict (read-only) property and Generic[Strict] behavior."""

    def test_strict_default_true(self) -> None:
        doc = new_document()
        assert doc.strict is True

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

    def test_get_collection_returns_same_as_getitem(self) -> None:
        doc = new_document()
        doc.add("Zone", "Z1")
        assert doc.get_collection("Zone") is doc["Zone"]

    def test_get_collection_missing_type_returns_empty(self) -> None:
        doc = new_document()
        coll = doc.get_collection("Zone")
        assert len(coll) == 0

    def test_copy_strict_enforces_strict_on_objects(self) -> None:
        doc = new_document(strict=True)
        doc.add("Zone", "Office")
        copy = doc.copy()
        zone = copy["Zone"]["Office"]
        with pytest.raises(AttributeError):
            _ = zone.nonexistent_field_xyz


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

    def test_generate_document_pyi_uses_typeddict(self) -> None:
        from idfkit.codegen.generate_stubs import generate_document_pyi

        content = generate_document_pyi((24, 1, 0))
        assert "class IDFDocument" in content
        assert "_ObjectTypeMap" in content
        assert "get_collection" in content

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


class TestLoadIdfStrict:
    """Test that load_idf's strict parameter works."""

    def test_load_idf_default_strict(self, tmp_path: Path) -> None:
        from idfkit import load_idf, write_idf

        # Create a minimal IDF file
        doc = new_document()
        path = tmp_path / "test.idf"
        write_idf(doc, str(path))

        loaded = load_idf(str(path))
        assert loaded.strict is True

    def test_load_idf_strict_false(self, tmp_path: Path) -> None:
        from idfkit import load_idf, write_idf

        doc = new_document()
        path = tmp_path / "test.idf"
        write_idf(doc, str(path))

        loaded = load_idf(str(path), strict=False)
        assert loaded.strict is False


class TestLoadEpjsonStrict:
    """Test that load_epjson's strict parameter works."""

    def test_load_epjson_default_strict(self, tmp_path: Path) -> None:
        from idfkit import load_epjson, write_epjson

        doc = new_document()
        path = tmp_path / "test.epJSON"
        write_epjson(doc, str(path))

        loaded = load_epjson(str(path))
        assert loaded.strict is True

    def test_load_epjson_strict_false(self, tmp_path: Path) -> None:
        from idfkit import load_epjson, write_epjson

        doc = new_document()
        path = tmp_path / "test.epJSON"
        write_epjson(doc, str(path))

        loaded = load_epjson(str(path), strict=False)
        assert loaded.strict is False


class TestStubRuntimeConsistency:
    """Verify that document.pyi declares every public method/property of the runtime class."""

    def test_document_pyi_covers_all_public_methods(self) -> None:
        from idfkit.codegen.generate_stubs import generate_document_pyi
        from idfkit.document import IDFDocument

        pyi_content = generate_document_pyi((24, 1, 0))

        # Collect public methods/properties defined directly on IDFDocument
        # (not inherited from EppyDocumentMixin or object)
        own_public: set[str] = set()
        for name in IDFDocument.__dict__:
            if name.startswith("_") and name not in (
                "__init__",
                "__contains__",
                "__iter__",
                "__len__",
                "__getattr__",
            ):
                continue
            member = IDFDocument.__dict__[name]
            if isinstance(member, (property, staticmethod, classmethod)) or callable(member):
                own_public.add(name)

        # Also include class-level annotations (version, filepath)
        for name in getattr(IDFDocument, "__annotations__", {}):
            if not name.startswith("_"):
                own_public.add(name)

        missing = {name for name in own_public if f" {name}" not in pyi_content and f".{name}" not in pyi_content}
        assert not missing, f"Methods/properties missing from document.pyi: {sorted(missing)}"

    def test_document_pyi_method_signatures_match(self) -> None:
        """Check that stub parameter names match runtime parameter names."""
        from idfkit.codegen.generate_stubs import generate_document_pyi
        from idfkit.document import IDFDocument

        pyi_content = generate_document_pyi((24, 1, 0))

        # Spot-check key method signatures
        for method_name in ("add", "rename", "get_referencing", "get_references"):
            sig = inspect.signature(getattr(IDFDocument, method_name))
            for param_name in sig.parameters:
                if param_name == "self":
                    continue
                assert param_name in pyi_content, (
                    f"Parameter '{param_name}' of {method_name}() not found in document.pyi"
                )
