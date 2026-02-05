"""Tests for construction visualization."""

from __future__ import annotations

import pytest

from idfkit import new_document
from idfkit.objects import IDFObject
from idfkit.thermal import get_thermal_properties
from idfkit.visualization import SVGConfig, construction_to_svg, generate_construction_svg


class TestSVGGeneration:
    """Tests for SVG diagram generation."""

    @pytest.fixture
    def opaque_construction(self) -> IDFObject:
        """Create an opaque wall construction."""
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "Material",
            "Brick",
            {
                "roughness": "Rough",
                "thickness": 0.1,
                "conductivity": 0.6,
                "density": 1800,
                "specific_heat": 900,
            },
        )
        doc.add(
            "Material",
            "Insulation",
            {
                "roughness": "MediumSmooth",
                "thickness": 0.05,
                "conductivity": 0.04,
                "density": 30,
                "specific_heat": 1000,
            },
        )
        doc.add(
            "Material",
            "Gypsum Board",
            {
                "roughness": "Smooth",
                "thickness": 0.013,
                "conductivity": 0.16,
                "density": 800,
                "specific_heat": 1000,
            },
        )

        doc.add(
            "Construction",
            "ExteriorWall",
            {
                "outside_layer": "Brick",
                "layer_2": "Insulation",
                "layer_3": "Gypsum Board",
            },
        )

        return doc["Construction"]["ExteriorWall"]

    @pytest.fixture
    def glazing_construction(self) -> IDFObject:
        """Create a glazing construction."""
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "WindowMaterial:Glazing",
            "ClearGlass",
            {
                "optical_data_type": "SpectralAverage",
                "thickness": 0.006,
                "conductivity": 1.0,
                "solar_transmittance_at_normal_incidence": 0.775,
                "front_side_solar_reflectance_at_normal_incidence": 0.071,
                "front_side_infrared_hemispherical_emissivity": 0.84,
                "back_side_infrared_hemispherical_emissivity": 0.84,
            },
        )

        doc.add(
            "WindowMaterial:Gas",
            "ArgonGap",
            {
                "gas_type": "Argon",
                "thickness": 0.012,
            },
        )

        doc.add(
            "WindowMaterial:Glazing",
            "LowEGlass",
            {
                "optical_data_type": "SpectralAverage",
                "thickness": 0.006,
                "conductivity": 1.0,
                "solar_transmittance_at_normal_incidence": 0.6,
                "front_side_solar_reflectance_at_normal_incidence": 0.17,
                "front_side_infrared_hemispherical_emissivity": 0.84,
                "back_side_infrared_hemispherical_emissivity": 0.10,  # Low-E
            },
        )

        doc.add(
            "Construction",
            "DoubleGlazing",
            {
                "outside_layer": "ClearGlass",
                "layer_2": "ArgonGap",
                "layer_3": "LowEGlass",
            },
        )

        return doc["Construction"]["DoubleGlazing"]

    def test_construction_to_svg_returns_string(self, opaque_construction: IDFObject) -> None:
        svg = construction_to_svg(opaque_construction)
        assert isinstance(svg, str)
        assert svg.startswith("<svg")
        assert svg.endswith("</svg>")

    def test_svg_contains_construction_name(self, opaque_construction: IDFObject) -> None:
        svg = construction_to_svg(opaque_construction)
        assert "ExteriorWall" in svg

    def test_svg_contains_layer_names(self, opaque_construction: IDFObject) -> None:
        svg = construction_to_svg(opaque_construction)
        assert "Brick" in svg
        assert "Insulation" in svg
        # Gypsum Board is truncated to "Gypsu.." due to narrow layer width
        assert "Gypsu" in svg

    def test_svg_contains_thermal_properties(self, opaque_construction: IDFObject) -> None:
        svg = construction_to_svg(opaque_construction)
        assert "U =" in svg or "U=" in svg
        assert "R =" in svg or "R=" in svg

    def test_svg_contains_outside_inside_labels(self, opaque_construction: IDFObject) -> None:
        svg = construction_to_svg(opaque_construction)
        # Labels can be "OUT/IN" or "EXT/INT" depending on design
        assert "OUT" in svg or "EXT" in svg
        assert "IN" in svg or "INT" in svg

    def test_glazing_svg_contains_shgc(self, glazing_construction: IDFObject) -> None:
        svg = construction_to_svg(glazing_construction)
        assert "SHGC" in svg  # May be "SHGC=" or "SHGC ="

    def test_glazing_svg_contains_gas_type(self, glazing_construction: IDFObject) -> None:
        svg = construction_to_svg(glazing_construction)
        assert "Argon" in svg

    def test_generate_construction_svg_with_custom_config(self, opaque_construction: IDFObject) -> None:
        props = get_thermal_properties(opaque_construction)
        config = SVGConfig(width=800, height=300)
        svg = generate_construction_svg(props, config)

        assert 'width="800"' in svg
        assert 'height="300"' in svg

    def test_svg_valid_xml_structure(self, opaque_construction: IDFObject) -> None:
        svg = construction_to_svg(opaque_construction)

        # Check basic XML structure
        assert "<svg" in svg
        assert "</svg>" in svg
        assert "<defs>" in svg
        assert "</defs>" in svg
        assert "<style>" in svg
        assert "</style>" in svg

    def test_svg_escapes_special_characters(self) -> None:
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "Material",
            'Material <with> &special "chars"',
            {
                "roughness": "Rough",
                "thickness": 0.1,
                "conductivity": 0.6,
                "density": 1800,
                "specific_heat": 900,
            },
        )

        doc.add(
            "Construction",
            "Test",
            {"outside_layer": 'Material <with> &special "chars"'},
        )

        svg = construction_to_svg(doc["Construction"]["Test"])

        # Should escape < > & properly
        assert "&lt;" in svg or "&gt;" in svg or "&amp;" in svg

    def test_construction_to_svg_type_validation(self) -> None:
        with pytest.raises(TypeError, match="Expected IDFObject"):
            construction_to_svg("not an object")  # type: ignore[arg-type]

    def test_construction_to_svg_wrong_type(self) -> None:
        obj = IDFObject(obj_type="Zone", name="TestZone")
        with pytest.raises(TypeError, match="Expected Construction"):
            construction_to_svg(obj)


class TestIDFObjectReprSVG:
    """Tests for IDFObject._repr_svg_() method."""

    @pytest.fixture
    def wall_construction(self) -> IDFObject:
        """Create a wall construction."""
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "Material",
            "Concrete",
            {
                "roughness": "MediumRough",
                "thickness": 0.2,
                "conductivity": 1.7,
                "density": 2300,
                "specific_heat": 900,
            },
        )

        doc.add(
            "Construction",
            "MassWall",
            {"outside_layer": "Concrete"},
        )

        return doc["Construction"]["MassWall"]

    def test_repr_svg_returns_string_for_construction(self, wall_construction: IDFObject) -> None:
        svg = wall_construction._repr_svg_()
        assert svg is not None
        assert isinstance(svg, str)
        assert svg.startswith("<svg")

    def test_repr_svg_returns_none_for_non_construction(self) -> None:
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "TestZone", {"x_origin": 0.0})
        zone = doc["Zone"]["TestZone"]

        svg = zone._repr_svg_()
        assert svg is None

    def test_repr_svg_returns_none_without_document(self) -> None:
        obj = IDFObject(
            obj_type="Construction",
            name="Orphan",
            data={"outside_layer": "SomeMaterial"},
        )

        svg = obj._repr_svg_()
        assert svg is None


class TestSVGConfig:
    """Tests for SVG configuration."""

    def test_default_config(self) -> None:
        config = SVGConfig()
        assert config.width == 600
        assert config.height == 200
        assert config.padding == 20

    def test_custom_config(self) -> None:
        config = SVGConfig(
            width=1000,
            height=400,
            padding=30,
            min_layer_width=50,
        )
        assert config.width == 1000
        assert config.height == 400
        assert config.padding == 30
        assert config.min_layer_width == 50


class TestLayerColors:
    """Tests for layer color assignment."""

    def test_insulation_gets_insulation_color(self) -> None:
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "Material",
            "XPS Insulation Board",
            {
                "roughness": "Smooth",
                "thickness": 0.05,
                "conductivity": 0.034,
                "density": 35,
                "specific_heat": 1400,
            },
        )

        doc.add(
            "Construction",
            "InsulationOnly",
            {"outside_layer": "XPS Insulation Board"},
        )

        svg = construction_to_svg(doc["Construction"]["InsulationOnly"])
        # Insulation should get yellow color and use insulation pattern
        assert "hatch-insulation" in svg or "#f5e6a3" in svg.lower()

    def test_concrete_gets_gray_color(self) -> None:
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "Material",
            "Concrete Block",
            {
                "roughness": "MediumRough",
                "thickness": 0.2,
                "conductivity": 1.0,
                "density": 1900,
                "specific_heat": 900,
            },
        )

        doc.add(
            "Construction",
            "ConcreteWall",
            {"outside_layer": "Concrete Block"},
        )

        svg = construction_to_svg(doc["Construction"]["ConcreteWall"])
        # Concrete should get gray color and use concrete pattern
        assert "hatch-concrete" in svg or "#a8a8a8" in svg.lower()
