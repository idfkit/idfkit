"""
Thermal property calculations for EnergyPlus constructions.

This module provides functions to calculate R-value, U-value, and SHGC
for opaque and glazing constructions based on their material layers.

Example:
    >>> from idfkit import load_idf
    >>> from idfkit.thermal import calculate_r_value, calculate_u_value
    >>>
    >>> model = load_idf("building.idf")
    >>> wall = model["Construction"]["ExteriorWall"]
    >>>
    >>> r_value = calculate_r_value(wall)
    >>> u_value = calculate_u_value(wall)
    >>> print(f"R-value: {r_value:.2f} m²·K/W")
    >>> print(f"U-value: {u_value:.2f} W/m²·K")
"""

from __future__ import annotations

from .gas import (
    TYPICAL_GAP_R_VALUES,
    GasProperties,
    GasType,
    gas_gap_resistance,
    get_gas_properties,
    typical_gap_r_value,
)
from .properties import (
    FILM_RESISTANCE,
    NFRC_FILM_COEFFICIENTS,
    ConstructionThermalProperties,
    LayerThermalProperties,
    calculate_r_value,
    calculate_shgc,
    calculate_u_value,
    calculate_visible_transmittance,
    get_construction_layers,
    get_thermal_properties,
)

__all__ = [
    "FILM_RESISTANCE",
    "NFRC_FILM_COEFFICIENTS",
    "TYPICAL_GAP_R_VALUES",
    "ConstructionThermalProperties",
    "GasProperties",
    "GasType",
    "LayerThermalProperties",
    "calculate_r_value",
    "calculate_shgc",
    "calculate_u_value",
    "calculate_visible_transmittance",
    "gas_gap_resistance",
    "get_construction_layers",
    "get_gas_properties",
    "get_thermal_properties",
    "typical_gap_r_value",
]
