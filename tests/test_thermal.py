"""Tests for thermal property calculations."""

from __future__ import annotations

import pytest

from idfkit import new_document
from idfkit.objects import IDFObject
from idfkit.thermal import (
    FILM_RESISTANCE,
    NFRC_FILM_COEFFICIENTS,
    calculate_r_value,
    calculate_shgc,
    calculate_u_value,
    calculate_visible_transmittance,
    get_construction_layers,
    get_thermal_properties,
)
from idfkit.thermal.gas import (
    TYPICAL_GAP_R_VALUES,
    gas_gap_resistance,
    get_gas_properties,
    typical_gap_r_value,
)


class TestGasProperties:
    """Tests for gas property correlations."""

    def test_get_gas_properties_air(self) -> None:
        props = get_gas_properties("Air")
        assert props.molecular_weight == pytest.approx(28.97, rel=0.01)

    def test_get_gas_properties_argon(self) -> None:
        props = get_gas_properties("Argon")
        assert props.molecular_weight == pytest.approx(39.948, rel=0.01)

    def test_get_gas_properties_krypton(self) -> None:
        props = get_gas_properties("Krypton")
        assert props.molecular_weight == pytest.approx(83.80, rel=0.01)

    def test_get_gas_properties_xenon(self) -> None:
        props = get_gas_properties("Xenon")
        assert props.molecular_weight == pytest.approx(131.30, rel=0.01)

    def test_get_gas_properties_case_insensitive(self) -> None:
        props1 = get_gas_properties("air")
        props2 = get_gas_properties("AIR")
        props3 = get_gas_properties("Air")
        assert props1 == props2 == props3

    def test_get_gas_properties_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown gas type"):
            get_gas_properties("Helium")

    def test_conductivity_increases_with_temperature(self) -> None:
        props = get_gas_properties("Air")
        k_low = props.conductivity(273.15)  # 0°C
        k_high = props.conductivity(323.15)  # 50°C
        assert k_high > k_low

    def test_typical_gap_r_value_air(self) -> None:
        r = typical_gap_r_value("Air", 12)
        assert r == pytest.approx(0.14, rel=0.1)

    def test_typical_gap_r_value_argon(self) -> None:
        r = typical_gap_r_value("Argon", 12)
        assert r == pytest.approx(0.15, rel=0.1)

    def test_typical_gap_r_value_krypton(self) -> None:
        r = typical_gap_r_value("Krypton", 12)
        assert r == pytest.approx(0.17, rel=0.1)

    def test_typical_gap_r_value_interpolates(self) -> None:
        r_6 = typical_gap_r_value("Argon", 6)
        r_9 = typical_gap_r_value("Argon", 9)
        r_7 = typical_gap_r_value("Argon", 7.5)
        # Should be between the two known values
        assert r_6 < r_7 < r_9

    def test_typical_gap_r_value_falls_back_to_calculation(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When gas type is not in TYPICAL_GAP_R_VALUES, fall back to gas_gap_resistance."""
        # Temporarily remove AIR from the lookup table
        monkeypatch.delitem(TYPICAL_GAP_R_VALUES, "AIR")
        r = typical_gap_r_value("Air", 12)
        assert r > 0

    def test_gas_gap_resistance_returns_positive(self) -> None:
        r = gas_gap_resistance("Air", 0.012)
        assert r > 0

    def test_gas_gap_resistance_horizontal_tilt(self) -> None:
        """Test gas_gap_resistance with tilt < 60 (more horizontal orientation)."""
        r_vertical = gas_gap_resistance("Air", 0.012, tilt=90.0)
        r_horizontal = gas_gap_resistance("Air", 0.012, tilt=30.0)
        # Both should be positive
        assert r_vertical > 0
        assert r_horizontal > 0

    def test_gas_gap_resistance_low_e(self) -> None:
        """Low-E coating should increase gap thermal resistance."""
        r_clear = gas_gap_resistance("Air", 0.012, emissivity_1=0.84, emissivity_2=0.84)
        r_low_e = gas_gap_resistance("Air", 0.012, emissivity_1=0.84, emissivity_2=0.10)
        assert r_low_e > r_clear


class TestOpaqueConstruction:
    """Tests for opaque construction thermal calculations."""

    @pytest.fixture
    def simple_wall(self) -> IDFObject:
        """Create a simple wall construction."""
        doc = new_document(version=(24, 1, 0))

        # Add materials
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
            "Gypsum",
            {
                "roughness": "Smooth",
                "thickness": 0.013,
                "conductivity": 0.16,
                "density": 800,
                "specific_heat": 1000,
            },
        )

        # Add construction
        doc.add(
            "Construction",
            "InsulatedWall",
            {
                "outside_layer": "Concrete",
                "layer_2": "Insulation",
                "layer_3": "Gypsum",
            },
        )

        return doc["Construction"]["InsulatedWall"]

    @pytest.fixture
    def wall_with_air_gap(self) -> IDFObject:
        """Create a wall with an air gap."""
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
            "Material:AirGap",
            "AirGap",
            {"thermal_resistance": 0.15},
        )
        doc.add(
            "Material",
            "Block",
            {
                "roughness": "MediumRough",
                "thickness": 0.1,
                "conductivity": 0.8,
                "density": 1600,
                "specific_heat": 900,
            },
        )

        doc.add(
            "Construction",
            "CavityWall",
            {
                "outside_layer": "Brick",
                "layer_2": "AirGap",
                "layer_3": "Block",
            },
        )

        return doc["Construction"]["CavityWall"]

    @pytest.fixture
    def wall_with_nomass(self) -> IDFObject:
        """Create a wall with a no-mass layer."""
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
            "Material:NoMass",
            "RigidInsulation",
            {"thermal_resistance": 1.5, "roughness": "Smooth"},
        )

        doc.add(
            "Construction",
            "InsulatedMass",
            {
                "outside_layer": "Concrete",
                "layer_2": "RigidInsulation",
            },
        )

        return doc["Construction"]["InsulatedMass"]

    def test_get_construction_layers(self, simple_wall: IDFObject) -> None:
        layers = get_construction_layers(simple_wall)
        assert len(layers) == 3
        assert layers[0].name == "Concrete"
        assert layers[1].name == "Insulation"
        assert layers[2].name == "Gypsum"

    def test_layer_r_values(self, simple_wall: IDFObject) -> None:
        layers = get_construction_layers(simple_wall)

        # Concrete: 0.2 / 1.7 = 0.118
        assert layers[0].r_value == pytest.approx(0.2 / 1.7, rel=0.01)

        # Insulation: 0.05 / 0.04 = 1.25
        assert layers[1].r_value == pytest.approx(0.05 / 0.04, rel=0.01)

        # Gypsum: 0.013 / 0.16 = 0.081
        assert layers[2].r_value == pytest.approx(0.013 / 0.16, rel=0.01)

    def test_calculate_r_value_without_films(self, simple_wall: IDFObject) -> None:
        r = calculate_r_value(simple_wall, include_films=False)
        expected = (0.2 / 1.7) + (0.05 / 0.04) + (0.013 / 0.16)
        assert r == pytest.approx(expected, rel=0.01)

    def test_calculate_r_value_with_films(self, simple_wall: IDFObject) -> None:
        r = calculate_r_value(simple_wall, include_films=True)
        expected = (
            FILM_RESISTANCE["exterior"] + (0.2 / 1.7) + (0.05 / 0.04) + (0.013 / 0.16) + FILM_RESISTANCE["interior"]
        )
        assert r == pytest.approx(expected, rel=0.01)

    def test_calculate_u_value(self, simple_wall: IDFObject) -> None:
        u = calculate_u_value(simple_wall)
        r = calculate_r_value(simple_wall, include_films=True)
        assert u == pytest.approx(1.0 / r, rel=0.01)

    def test_air_gap_resistance(self, wall_with_air_gap: IDFObject) -> None:
        layers = get_construction_layers(wall_with_air_gap)
        assert layers[1].r_value == pytest.approx(0.15, rel=0.01)
        assert layers[1].is_gas is True
        assert layers[1].gas_type == "Air"

    def test_nomass_resistance(self, wall_with_nomass: IDFObject) -> None:
        layers = get_construction_layers(wall_with_nomass)
        assert layers[1].r_value == pytest.approx(1.5, rel=0.01)
        assert layers[1].thickness is None

    def test_get_thermal_properties(self, simple_wall: IDFObject) -> None:
        props = get_thermal_properties(simple_wall)

        assert props.name == "InsulatedWall"
        assert len(props.layers) == 3
        assert props.is_glazing is False
        assert props.shgc is None
        assert props.u_value > 0
        assert props.r_value > 0
        assert props.r_value_with_films > props.r_value

    def test_shgc_returns_none_for_opaque(self, simple_wall: IDFObject) -> None:
        shgc = calculate_shgc(simple_wall)
        assert shgc is None

    def test_visible_transmittance_returns_none_for_opaque(self, simple_wall: IDFObject) -> None:
        vt = calculate_visible_transmittance(simple_wall)
        assert vt is None


class TestGlazingConstruction:
    """Tests for glazing construction thermal calculations."""

    @pytest.fixture
    def simple_glazing(self) -> IDFObject:
        """Create a simple glazing system."""
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "WindowMaterial:SimpleGlazingSystem",
            "SimpleWindow",
            {
                "u_factor": 2.0,
                "solar_heat_gain_coefficient": 0.4,
                "visible_transmittance": 0.6,
            },
        )

        doc.add(
            "Construction",
            "SimpleGlazing",
            {"outside_layer": "SimpleWindow"},
        )

        return doc["Construction"]["SimpleGlazing"]

    @pytest.fixture
    def double_glazing(self) -> IDFObject:
        """Create a double-pane glazing system."""
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
                "back_side_solar_reflectance_at_normal_incidence": 0.071,
                "visible_transmittance_at_normal_incidence": 0.881,
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
            "Construction",
            "DoubleGlazing",
            {
                "outside_layer": "ClearGlass",
                "layer_2": "ArgonGap",
                "layer_3": "ClearGlass",
            },
        )

        return doc["Construction"]["DoubleGlazing"]

    @pytest.fixture
    def low_e_glazing(self) -> IDFObject:
        """Create a low-e glazing system."""
        doc = new_document(version=(24, 1, 0))

        doc.add(
            "WindowMaterial:Glazing",
            "ClearGlass",
            {
                "optical_data_type": "SpectralAverage",
                "thickness": 0.006,
                "conductivity": 1.0,
                "solar_transmittance_at_normal_incidence": 0.6,
                "front_side_solar_reflectance_at_normal_incidence": 0.17,
                "back_side_solar_reflectance_at_normal_incidence": 0.22,
                "visible_transmittance_at_normal_incidence": 0.78,
                "front_side_infrared_hemispherical_emissivity": 0.84,
                "back_side_infrared_hemispherical_emissivity": 0.10,  # Low-E coating
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
            "ClearGlassInner",
            {
                "optical_data_type": "SpectralAverage",
                "thickness": 0.006,
                "conductivity": 1.0,
                "solar_transmittance_at_normal_incidence": 0.775,
                "front_side_solar_reflectance_at_normal_incidence": 0.071,
                "back_side_solar_reflectance_at_normal_incidence": 0.071,
                "visible_transmittance_at_normal_incidence": 0.881,
                "front_side_infrared_hemispherical_emissivity": 0.84,
                "back_side_infrared_hemispherical_emissivity": 0.84,
            },
        )

        doc.add(
            "Construction",
            "LowEGlazing",
            {
                "outside_layer": "ClearGlass",
                "layer_2": "ArgonGap",
                "layer_3": "ClearGlassInner",
            },
        )

        return doc["Construction"]["LowEGlazing"]

    def test_simple_glazing_u_value(self, simple_glazing: IDFObject) -> None:
        u = calculate_u_value(simple_glazing)
        # SimpleGlazingSystem provides U-factor directly
        assert u == pytest.approx(2.0, rel=0.01)

    def test_simple_glazing_shgc(self, simple_glazing: IDFObject) -> None:
        shgc = calculate_shgc(simple_glazing)
        assert shgc == pytest.approx(0.4, rel=0.01)

    def test_simple_glazing_visible_transmittance(self, simple_glazing: IDFObject) -> None:
        vt = calculate_visible_transmittance(simple_glazing)
        assert vt == pytest.approx(0.6, rel=0.01)

    def test_simple_glazing_r_value_without_films(self, simple_glazing: IDFObject) -> None:
        """SimpleGlazingSystem include_films=False should subtract NFRC film resistances."""
        r_with = calculate_r_value(simple_glazing, include_films=True)
        r_without = calculate_r_value(simple_glazing, include_films=False)
        film_r = 1.0 / NFRC_FILM_COEFFICIENTS["exterior"] + 1.0 / NFRC_FILM_COEFFICIENTS["interior"]
        assert r_with == pytest.approx(0.5, rel=0.01)  # 1/2.0
        assert r_without == pytest.approx(r_with - film_r, rel=0.01)
        assert r_without < r_with

    def test_simple_glazing_thermal_properties_r_values_differ(self, simple_glazing: IDFObject) -> None:
        """get_thermal_properties should report different r_value and r_value_with_films."""
        props = get_thermal_properties(simple_glazing)
        assert props.r_value_with_films > props.r_value

    def test_double_glazing_layers(self, double_glazing: IDFObject) -> None:
        layers = get_construction_layers(double_glazing)
        assert len(layers) == 3
        assert layers[0].is_glazing is True
        assert layers[1].is_gas is True
        assert layers[1].gas_type == "Argon"
        assert layers[2].is_glazing is True

    def test_double_glazing_u_value(self, double_glazing: IDFObject) -> None:
        u = calculate_u_value(double_glazing)
        # Typical double glazing U-value is around 1.5-3.5 W/m²K
        # (simplified calculation gives slightly higher values)
        assert 1.0 < u < 4.0

    def test_double_glazing_shgc(self, double_glazing: IDFObject) -> None:
        shgc = calculate_shgc(double_glazing)
        # SHGC should be less than single pane transmittance
        assert shgc is not None
        assert 0.3 < shgc < 0.8

    def test_double_glazing_visible_transmittance(self, double_glazing: IDFObject) -> None:
        vt = calculate_visible_transmittance(double_glazing)
        assert vt is not None
        # Product of two panes of clear glass (0.881 * 0.881 ≈ 0.776)
        assert 0.5 < vt < 0.9

    def test_low_e_layer_detected(self, low_e_glazing: IDFObject) -> None:
        layers = get_construction_layers(low_e_glazing)
        # First layer has low-e on back side
        assert layers[0].emissivity_back is not None
        assert layers[0].emissivity_back < 0.2

    def test_get_thermal_properties_glazing(self, double_glazing: IDFObject) -> None:
        props = get_thermal_properties(double_glazing)

        assert props.name == "DoubleGlazing"
        assert props.is_glazing is True
        assert props.shgc is not None
        assert props.u_value > 0


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_construction_with_missing_material_returns_empty_layers(self) -> None:
        """Test that constructions referencing non-existent materials return empty layers."""
        doc = new_document(version=(24, 1, 0))
        doc.add(
            "Construction",
            "MissingMaterial",
            {"outside_layer": "NonexistentMaterial"},
        )
        construction = doc["Construction"]["MissingMaterial"]

        layers = get_construction_layers(construction)
        assert layers == []

        r = calculate_r_value(construction)
        assert r == 0.0

    def test_construction_without_document(self) -> None:
        obj = IDFObject(
            obj_type="Construction",
            name="Orphan",
            data={"outside_layer": "SomeMaterial"},
        )

        layers = get_construction_layers(obj)
        # Can't resolve material without document
        assert layers == []
