"""
Thermal property calculations for EnergyPlus constructions.

Provides R-value, U-value, and SHGC calculations for opaque and glazing
constructions based on material layer properties.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .gas import typical_gap_r_value

if TYPE_CHECKING:
    from ..objects import IDFObject

# Construction layer field names in order (outside to inside)
_LAYER_FIELDS = (
    "outside_layer",
    "layer_2",
    "layer_3",
    "layer_4",
    "layer_5",
    "layer_6",
    "layer_7",
    "layer_8",
    "layer_9",
    "layer_10",
)

# Material types to search when resolving layer references
_MATERIAL_TYPES = (
    "Material",
    "Material:NoMass",
    "Material:AirGap",
    "WindowMaterial:Glazing",
    "WindowMaterial:Gas",
    "WindowMaterial:SimpleGlazingSystem",
)

# Standard surface film resistances (m²·K/W)
# From ASHRAE Fundamentals, Chapter 26
FILM_RESISTANCE = {
    # Exterior surface (15 mph wind)
    "exterior": 0.030,
    # Interior surface (still air)
    "interior": 0.120,
    # Interior surface - horizontal, heat flow up (ceiling)
    "interior_ceiling": 0.107,
    # Interior surface - horizontal, heat flow down (floor)
    "interior_floor": 0.160,
}

# NFRC standard film coefficients for windows (W/m²·K)
NFRC_FILM_COEFFICIENTS = {
    "exterior": 26.0,  # Winter conditions
    "interior": 7.7,  # Still air
}

# Standard glass conductivity (W/m·K)
GLASS_CONDUCTIVITY = 1.0


@dataclass
class LayerThermalProperties:
    """Thermal properties of a single layer.

    Attributes:
        name: Material name
        obj_type: EnergyPlus object type
        thickness: Layer thickness in meters (None for no-mass layers)
        conductivity: Thermal conductivity in W/m·K (None for no-mass layers)
        r_value: Thermal resistance in m²·K/W
        is_glazing: True if this is a glazing layer
        is_gas: True if this is a gas gap
        gas_type: Gas type if is_gas (Air, Argon, Krypton, Xenon)
        solar_transmittance: Solar transmittance at normal incidence (glazing only)
        solar_reflectance_front: Front-side solar reflectance (glazing only)
        visible_transmittance: Visible transmittance at normal incidence (glazing only)
        emissivity_front: Front-side infrared emissivity (glazing only)
        emissivity_back: Back-side infrared emissivity (glazing only)
        shgc: Solar heat gain coefficient (SimpleGlazingSystem only)
    """

    name: str
    obj_type: str
    thickness: float | None = None
    conductivity: float | None = None
    r_value: float = 0.0
    is_glazing: bool = False
    is_gas: bool = False
    gas_type: str | None = None
    solar_transmittance: float | None = None
    solar_reflectance_front: float | None = None
    visible_transmittance: float | None = None
    emissivity_front: float | None = None
    emissivity_back: float | None = None
    shgc: float | None = None


@dataclass
class ConstructionThermalProperties:
    """Thermal properties of a complete construction assembly.

    Attributes:
        name: Construction name
        layers: List of layer thermal properties (outside to inside)
        r_value: Total thermal resistance in m²·K/W (excluding films)
        r_value_with_films: Total R-value including surface films
        u_value: Overall heat transfer coefficient in W/m²·K (with films)
        is_glazing: True if this is a glazing construction
        shgc: Solar heat gain coefficient (glazing only)
        visible_transmittance: Visible transmittance (glazing only)
    """

    name: str
    layers: list[LayerThermalProperties] = field(default_factory=lambda: [])
    r_value: float = 0.0
    r_value_with_films: float = 0.0
    u_value: float = 0.0
    is_glazing: bool = False
    shgc: float | None = None
    visible_transmittance: float | None = None


def _get_material_by_name(construction: IDFObject, material_name: str) -> IDFObject | None:
    """Get material object by name from the document."""
    document = construction.theidf
    if document is None:
        return None

    for mat_type in _MATERIAL_TYPES:
        if mat_type in document.collections:
            mat = document.collections[mat_type].get(material_name)
            if mat is not None:
                return mat

    return None


def _get_material_layer(
    construction: IDFObject,
    material_name: str,
) -> LayerThermalProperties | None:
    """Get thermal properties for a material layer.

    Args:
        construction: Construction IDFObject (used to access parent document)
        material_name: Name of the material to look up

    Returns:
        LayerThermalProperties or None if material not found
    """
    mat = _get_material_by_name(construction, material_name)
    if mat is None:
        return None
    return _extract_layer_properties(mat)


def _extract_layer_properties(material: IDFObject) -> LayerThermalProperties:
    """Extract thermal properties from a material object.

    Args:
        material: Material IDFObject

    Returns:
        LayerThermalProperties with relevant thermal data
    """
    mat_type = material.obj_type

    if mat_type == "Material":
        thickness = material.thickness if material.thickness is not None else 0.0
        conductivity = material.conductivity if material.conductivity is not None else 1.0
        r_value = thickness / conductivity if conductivity > 0 else 0.0
        return LayerThermalProperties(
            name=material.name,
            obj_type=mat_type,
            thickness=thickness,
            conductivity=conductivity,
            r_value=r_value,
        )

    if mat_type == "Material:NoMass":
        r_value = material.thermal_resistance if material.thermal_resistance is not None else 0.0
        return LayerThermalProperties(
            name=material.name,
            obj_type=mat_type,
            r_value=r_value,
        )

    if mat_type == "Material:AirGap":
        r_value = material.thermal_resistance if material.thermal_resistance is not None else 0.0
        return LayerThermalProperties(
            name=material.name,
            obj_type=mat_type,
            r_value=r_value,
            is_gas=True,
            gas_type="Air",
        )

    if mat_type == "WindowMaterial:Glazing":
        thickness = material.thickness if material.thickness is not None else 0.006  # Default 6mm
        conductivity = material.conductivity if material.conductivity is not None else GLASS_CONDUCTIVITY
        r_value = thickness / conductivity if conductivity > 0 else 0.0

        # Get optical properties
        solar_trans = material.solar_transmittance_at_normal_incidence
        solar_refl_front = material.front_side_solar_reflectance_at_normal_incidence
        vis_trans = material.visible_transmittance_at_normal_incidence
        emiss_front = (
            material.front_side_infrared_hemispherical_emissivity
            if material.front_side_infrared_hemispherical_emissivity is not None
            else 0.84
        )
        emiss_back = (
            material.back_side_infrared_hemispherical_emissivity
            if material.back_side_infrared_hemispherical_emissivity is not None
            else 0.84
        )

        return LayerThermalProperties(
            name=material.name,
            obj_type=mat_type,
            thickness=thickness,
            conductivity=conductivity,
            r_value=r_value,
            is_glazing=True,
            solar_transmittance=solar_trans,
            solar_reflectance_front=solar_refl_front,
            visible_transmittance=vis_trans,
            emissivity_front=emiss_front,
            emissivity_back=emiss_back,
        )

    if mat_type == "WindowMaterial:Gas":
        thickness = material.thickness if material.thickness is not None else 0.012  # Default 12mm
        gas_type = material.gas_type if material.gas_type is not None else "Air"

        # Get R-value from typical values
        r_value = typical_gap_r_value(gas_type, thickness * 1000)

        return LayerThermalProperties(
            name=material.name,
            obj_type=mat_type,
            thickness=thickness,
            r_value=r_value,
            is_gas=True,
            gas_type=gas_type,
        )

    if mat_type == "WindowMaterial:SimpleGlazingSystem":
        # SimpleGlazingSystem provides U-factor directly (includes films)
        u_factor = material.u_factor if material.u_factor is not None else 2.0
        r_value = 1.0 / u_factor if u_factor > 0 else 0.0
        return LayerThermalProperties(
            name=material.name,
            obj_type=mat_type,
            r_value=r_value,
            is_glazing=True,
            shgc=material.solar_heat_gain_coefficient,
            visible_transmittance=material.visible_transmittance,
        )

    # Unknown material type
    return LayerThermalProperties(
        name=material.name,
        obj_type=mat_type,
        r_value=0.0,
    )


def get_construction_layers(construction: IDFObject) -> list[LayerThermalProperties]:
    """Get thermal properties for all layers in a construction.

    Args:
        construction: Construction IDFObject

    Returns:
        List of LayerThermalProperties from outside to inside
    """
    layers: list[LayerThermalProperties] = []

    for field_name in _LAYER_FIELDS:
        material_name = getattr(construction, field_name, None)
        if material_name:
            layer = _get_material_layer(construction, material_name)
            if layer:
                layers.append(layer)

    return layers


def _nfrc_film_resistance() -> float:
    """Total NFRC film resistance (exterior + interior) in m²·K/W."""
    return 1.0 / NFRC_FILM_COEFFICIENTS["exterior"] + 1.0 / NFRC_FILM_COEFFICIENTS["interior"]


def calculate_r_value(construction: IDFObject, include_films: bool = True) -> float:
    """Calculate R-value for a construction assembly.

    For opaque constructions, sums the thermal resistance of all layers.
    For glazing constructions with SimpleGlazingSystem, the stored R-value
    includes films; when ``include_films=False`` the NFRC film resistances
    are subtracted.

    Args:
        construction: Construction IDFObject
        include_films: Whether to include surface film resistances (default True)

    Returns:
        Thermal resistance in m²·K/W
    """
    layers = get_construction_layers(construction)

    if not layers:
        return 0.0

    # Check for SimpleGlazingSystem
    if len(layers) == 1 and layers[0].obj_type == "WindowMaterial:SimpleGlazingSystem":
        # r_value already includes films (1 / U-factor)
        if include_films:
            return layers[0].r_value
        return max(0.0, layers[0].r_value - _nfrc_film_resistance())

    # Sum layer resistances
    r_total = sum(layer.r_value for layer in layers)

    # Add film resistances
    if include_films:
        # Determine if this is a glazing construction
        is_glazing = any(layer.is_glazing for layer in layers)

        if is_glazing:
            # Use NFRC film coefficients for windows
            r_exterior = 1.0 / NFRC_FILM_COEFFICIENTS["exterior"]
            r_interior = 1.0 / NFRC_FILM_COEFFICIENTS["interior"]
        else:
            # Use ASHRAE film resistances for opaque
            r_exterior = FILM_RESISTANCE["exterior"]
            r_interior = FILM_RESISTANCE["interior"]

        r_total += r_exterior + r_interior

    return r_total


def calculate_u_value(construction: IDFObject) -> float:
    """Calculate U-value for a construction assembly.

    Args:
        construction: Construction IDFObject

    Returns:
        Overall heat transfer coefficient in W/m²·K
    """
    r_value = calculate_r_value(construction, include_films=True)
    if r_value > 0:
        return 1.0 / r_value
    return 0.0


def calculate_shgc(construction: IDFObject) -> float | None:
    """Calculate Solar Heat Gain Coefficient for a glazing construction.

    Uses simplified calculation based on solar transmittance and absorptance.
    For accurate values, use the full WINDOW/TARCOG algorithm.

    Args:
        construction: Construction IDFObject (must be glazing)

    Returns:
        SHGC value (0-1) or None if not a glazing construction
    """
    layers = get_construction_layers(construction)

    if not layers:
        return None

    # Check for SimpleGlazingSystem - SHGC is provided directly
    if len(layers) == 1 and layers[0].obj_type == "WindowMaterial:SimpleGlazingSystem":
        return layers[0].shgc

    # Check if this is a glazing construction
    glazing_layers = [layer for layer in layers if layer.is_glazing]
    if not glazing_layers:
        return None

    # Simplified SHGC calculation for multi-pane systems
    # Product of individual transmittances for direct component
    tau_direct = 1.0
    for layer in glazing_layers:
        if layer.solar_transmittance is not None:
            tau_direct *= layer.solar_transmittance

    # Absorbed component contribution (simplified)
    # For the outermost glazing layer, some absorbed radiation flows inward
    first_glazing = glazing_layers[0]
    if first_glazing.solar_transmittance is not None and first_glazing.solar_reflectance_front is not None:
        tau = first_glazing.solar_transmittance
        rho = first_glazing.solar_reflectance_front
        alpha = 1.0 - tau - rho

        # Inward-flowing fraction (simplified)
        # Uses NFRC film coefficients
        h_out = NFRC_FILM_COEFFICIENTS["exterior"]
        h_in = NFRC_FILM_COEFFICIENTS["interior"]
        n_i = alpha * (h_in / (h_out + h_in))

        shgc = tau_direct + n_i
        return min(shgc, 1.0)

    return tau_direct


def calculate_visible_transmittance(construction: IDFObject) -> float | None:
    """Calculate visible transmittance for a glazing construction.

    Args:
        construction: Construction IDFObject (must be glazing)

    Returns:
        Visible transmittance (0-1) or None if not a glazing construction
    """
    layers = get_construction_layers(construction)

    if not layers:
        return None

    # Check for SimpleGlazingSystem - VT is provided directly
    if len(layers) == 1 and layers[0].obj_type == "WindowMaterial:SimpleGlazingSystem":
        return layers[0].visible_transmittance

    # Product of individual visible transmittances
    vt = 1.0
    has_glazing = False

    for layer in layers:
        if layer.is_glazing and layer.visible_transmittance is not None:
            has_glazing = True
            vt *= layer.visible_transmittance

    return vt if has_glazing else None


def get_thermal_properties(construction: IDFObject) -> ConstructionThermalProperties:
    """Get complete thermal properties for a construction.

    Args:
        construction: Construction IDFObject

    Returns:
        ConstructionThermalProperties with all calculated values
    """
    layers = get_construction_layers(construction)

    # Determine if glazing
    is_glazing = any(layer.is_glazing for layer in layers)

    # Calculate R-values
    r_value = calculate_r_value(construction, include_films=False)
    r_value_with_films = calculate_r_value(construction, include_films=True)

    # Calculate U-value
    u_value = 1.0 / r_value_with_films if r_value_with_films > 0 else 0.0

    # Calculate SHGC and VT for glazing
    shgc = calculate_shgc(construction) if is_glazing else None
    vt = calculate_visible_transmittance(construction) if is_glazing else None

    return ConstructionThermalProperties(
        name=construction.name,
        layers=layers,
        r_value=r_value,
        r_value_with_films=r_value_with_films,
        u_value=u_value,
        is_glazing=is_glazing,
        shgc=shgc,
        visible_transmittance=vt,
    )
