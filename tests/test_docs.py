"""Tests for the documentation URL builder."""

from __future__ import annotations

import pytest

from idfkit.docs import (
    DocsUrl,
    docs_url_for_object,
    engineering_reference_url,
    io_reference_url,
    search_url,
)
from idfkit.schema import EpJSONSchema


@pytest.fixture(scope="session")
def schema() -> EpJSONSchema:
    from idfkit import get_schema

    return get_schema((24, 1, 0))


class TestIoReferenceUrl:
    def test_zone(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("Zone", (25, 2, 0), schema)
        assert result is not None
        assert result.url == (
            "https://docs.idfkit.com/v25.2/io-reference/overview/group-thermal-zone-description-geometry/#zone"
        )
        assert result.doc_set == "io-reference"
        assert result.version == "v25.2"
        assert result.label == "Zone — I/O Reference"

    def test_material(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("Material", (24, 1, 0), schema)
        assert result is not None
        assert "group-surface-construction-elements" in result.url
        assert "#material" in result.url
        assert result.version == "v24.1"

    def test_building_surface_detailed(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("BuildingSurface:Detailed", (25, 2, 0), schema)
        assert result is not None
        assert "#buildingsurfacedetailed" in result.url
        assert "group-thermal-zone-description-geometry" in result.url

    def test_hvactemplate_colon_object(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("HVACTemplate:Zone:IdealLoadsAirSystem", (25, 2, 0), schema)
        assert result is not None
        assert "#hvactemplatezoneidealloadsairsystem" in result.url
        # HVACTemplate objects don't have a group- page in the docs;
        # they appear in the HVAC Templates section via the mapping
        assert "hvac-templates" in result.url

    def test_coil_cooling_dx(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("Coil:Cooling:DX:SingleSpeed", (25, 2, 0), schema)
        assert result is not None
        assert "#coilcoolingdxsinglespeed" in result.url

    def test_unknown_object_type(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("NotARealObjectType", (25, 2, 0), schema)
        assert result is None

    def test_without_schema(self) -> None:
        # Should attempt to load default schema and resolve
        result = io_reference_url("Zone", (25, 2, 0))
        assert result is not None
        assert "#zone" in result.url

    def test_custom_base_url(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("Zone", (25, 2, 0), schema, base_url="https://custom.example.com")
        assert result is not None
        assert result.url.startswith("https://custom.example.com/")

    def test_version_formatting(self, schema: EpJSONSchema) -> None:
        result = io_reference_url("Zone", (9, 6, 0), schema)
        assert result is not None
        assert "/v9.6/" in result.url

    def test_nonexistent_version_returns_none(self, schema: EpJSONSchema) -> None:
        # 9.8.0 doesn't exist — no docs, no URL
        result = io_reference_url("Zone", (9, 8, 0), schema)
        assert result is None


class TestEngineeringReferenceUrl:
    def test_basic(self) -> None:
        result = engineering_reference_url((25, 2, 0))
        assert result is not None
        assert result.url == "https://docs.idfkit.com/v25.2/engineering-reference/"
        assert result.doc_set == "engineering-reference"
        assert result.version == "v25.2"
        assert result.label == "Engineering Reference"

    def test_custom_base_url(self) -> None:
        result = engineering_reference_url((25, 2, 0), base_url="https://example.com")
        assert result is not None
        assert result.url == "https://example.com/v25.2/engineering-reference/"

    def test_nonexistent_version_returns_none(self) -> None:
        assert engineering_reference_url((9, 8, 0)) is None


class TestSearchUrl:
    def test_basic(self) -> None:
        result = search_url("Zone", (25, 2, 0))
        assert result is not None
        assert result.url == "https://docs.idfkit.com/v25.2/io-reference/overview/"
        assert result.doc_set == "search"
        assert result.label == "Search: Zone"

    def test_custom_base_url(self) -> None:
        result = search_url("Zone", (25, 2, 0), base_url="https://example.com")
        assert result is not None
        assert result.url.startswith("https://example.com/")

    def test_nonexistent_version_returns_none(self) -> None:
        assert search_url("Zone", (9, 8, 0)) is None


class TestDocsUrlForObject:
    def test_known_object(self, schema: EpJSONSchema) -> None:
        result = docs_url_for_object("Zone", (25, 2, 0), schema)
        assert result is not None
        assert "io-reference" in result.url

    def test_unknown_object(self, schema: EpJSONSchema) -> None:
        result = docs_url_for_object("FakeObject", (25, 2, 0), schema)
        assert result is None


class TestDocsUrlDataclass:
    def test_frozen(self) -> None:
        url = DocsUrl(url="https://example.com", doc_set="test", version="v1.0", label="Test")
        with pytest.raises(AttributeError):
            url.url = "changed"  # type: ignore[misc]
