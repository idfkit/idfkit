"""
Gas properties for window glazing cavities.

Temperature-dependent correlations for common fill gases used in insulated
glazing units (IGUs). Properties are based on EnergyPlus engineering reference
and ISO 15099 standard.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# Standard gas types supported by EnergyPlus
GasType = Literal["Air", "Argon", "Krypton", "Xenon"]


@dataclass(frozen=True, slots=True)
class GasProperties:
    """Temperature-dependent gas properties.

    Properties are computed as polynomials of temperature:
        property(T) = a + b*T + c*T²

    where T is in Kelvin.

    Attributes:
        conductivity_a: Thermal conductivity coefficient a (W/m·K)
        conductivity_b: Thermal conductivity coefficient b (W/m·K²)
        conductivity_c: Thermal conductivity coefficient c (W/m·K³)
        viscosity_a: Dynamic viscosity coefficient a (kg/m·s)
        viscosity_b: Dynamic viscosity coefficient b (kg/m·s·K)
        viscosity_c: Dynamic viscosity coefficient c (kg/m·s·K²)
        specific_heat_a: Specific heat coefficient a (J/kg·K)
        specific_heat_b: Specific heat coefficient b (J/kg·K²)
        specific_heat_c: Specific heat coefficient c (J/kg·K³)
        molecular_weight: Molecular weight (g/mol)
    """

    conductivity_a: float
    conductivity_b: float
    conductivity_c: float
    viscosity_a: float
    viscosity_b: float
    viscosity_c: float
    specific_heat_a: float
    specific_heat_b: float
    specific_heat_c: float
    molecular_weight: float

    def conductivity(self, temperature_k: float) -> float:
        """Calculate thermal conductivity at given temperature.

        Args:
            temperature_k: Temperature in Kelvin

        Returns:
            Thermal conductivity in W/m·K
        """
        t = temperature_k
        return self.conductivity_a + self.conductivity_b * t + self.conductivity_c * t * t

    def viscosity(self, temperature_k: float) -> float:
        """Calculate dynamic viscosity at given temperature.

        Args:
            temperature_k: Temperature in Kelvin

        Returns:
            Dynamic viscosity in kg/m·s
        """
        t = temperature_k
        return self.viscosity_a + self.viscosity_b * t + self.viscosity_c * t * t

    def specific_heat(self, temperature_k: float) -> float:
        """Calculate specific heat at given temperature.

        Args:
            temperature_k: Temperature in Kelvin

        Returns:
            Specific heat in J/kg·K
        """
        t = temperature_k
        return self.specific_heat_a + self.specific_heat_b * t + self.specific_heat_c * t * t


# Gas property correlations from EnergyPlus Engineering Reference
# Based on ISO 15099 and WINDOW/THERM calculations
_GAS_PROPERTIES: dict[str, GasProperties] = {
    "AIR": GasProperties(
        conductivity_a=2.873e-3,
        conductivity_b=7.760e-5,
        conductivity_c=0.0,
        viscosity_a=3.723e-6,
        viscosity_b=4.940e-8,
        viscosity_c=0.0,
        specific_heat_a=1002.737,
        specific_heat_b=1.2324e-2,
        specific_heat_c=0.0,
        molecular_weight=28.97,
    ),
    "ARGON": GasProperties(
        conductivity_a=2.285e-3,
        conductivity_b=5.149e-5,
        conductivity_c=0.0,
        viscosity_a=3.379e-6,
        viscosity_b=6.451e-8,
        viscosity_c=0.0,
        specific_heat_a=521.9285,
        specific_heat_b=0.0,
        specific_heat_c=0.0,
        molecular_weight=39.948,
    ),
    "KRYPTON": GasProperties(
        conductivity_a=9.443e-4,
        conductivity_b=2.826e-5,
        conductivity_c=0.0,
        viscosity_a=2.213e-6,
        viscosity_b=7.777e-8,
        viscosity_c=0.0,
        specific_heat_a=248.0907,
        specific_heat_b=0.0,
        specific_heat_c=0.0,
        molecular_weight=83.80,
    ),
    "XENON": GasProperties(
        conductivity_a=4.538e-4,
        conductivity_b=1.723e-5,
        conductivity_c=0.0,
        viscosity_a=1.069e-6,
        viscosity_b=7.414e-8,
        viscosity_c=0.0,
        specific_heat_a=158.3397,
        specific_heat_b=0.0,
        specific_heat_c=0.0,
        molecular_weight=131.30,
    ),
}


def get_gas_properties(gas_type: str) -> GasProperties:
    """Get gas properties for a standard gas type.

    Args:
        gas_type: Gas type name (Air, Argon, Krypton, Xenon)

    Returns:
        GasProperties dataclass with temperature-dependent correlations

    Raises:
        ValueError: If gas type is not recognized
    """
    key = gas_type.upper()
    if key not in _GAS_PROPERTIES:
        valid = ", ".join(_GAS_PROPERTIES.keys())
        msg = f"Unknown gas type '{gas_type}'. Valid types: {valid}"
        raise ValueError(msg)
    return _GAS_PROPERTIES[key]


def gas_gap_resistance(
    gas_type: str,
    thickness: float,
    temperature_k: float = 293.15,
    delta_t: float = 15.0,
    emissivity_1: float = 0.84,
    emissivity_2: float = 0.84,
    tilt: float = 90.0,
) -> float:
    """Calculate thermal resistance of a gas-filled gap.

    Uses simplified ISO 15099 correlation for vertical gaps. For more accurate
    results, the full iterative TARCOG algorithm should be used.

    Args:
        gas_type: Gas type (Air, Argon, Krypton, Xenon)
        thickness: Gap thickness in meters
        temperature_k: Mean gap temperature in Kelvin (default: 20°C)
        delta_t: Temperature difference across gap in K (default: 15K)
        emissivity_1: Emissivity of surface 1 (default: 0.84 for clear glass)
        emissivity_2: Emissivity of surface 2 (default: 0.84 for clear glass)
        tilt: Tilt angle from horizontal in degrees (default: 90° vertical)

    Returns:
        Thermal resistance in m²·K/W
    """
    import math

    props = get_gas_properties(gas_type)

    # Gas properties at mean temperature
    k = props.conductivity(temperature_k)
    mu = props.viscosity(temperature_k)
    cp = props.specific_heat(temperature_k)

    # Density from ideal gas law (approximately)
    # rho = P * M / (R * T), at 101325 Pa
    r_gas = 8314.46  # J/(kmol·K)
    rho = 101325 * props.molecular_weight / (r_gas * temperature_k)

    # Prandtl number
    pr = mu * cp / k

    # Grashof number for natural convection
    g = 9.81  # m/s²
    beta = 1.0 / temperature_k  # Ideal gas approximation
    gr = (g * beta * delta_t * thickness**3 * rho**2) / (mu**2)

    # Rayleigh number
    ra = gr * pr

    # Nusselt number correlation for vertical enclosure (tilt = 90°)
    # Simplified Wright correlation
    if tilt >= 60:
        # Vertical or near-vertical
        nu = max(1.0, 0.0673838 * ra**0.333)
    else:
        # More horizontal - use different correlation
        nu = max(1.0, 0.0605 * ra**0.333 * (1 + (0.104 * ra**0.293) / (1 + (6310 / ra) ** 1.36)))

    # Convective resistance
    h_cv = nu * k / thickness
    r_cv = 1.0 / h_cv

    # Radiative resistance
    sigma = 5.67e-8  # Stefan-Boltzmann constant
    e_eff = 1.0 / (1.0 / emissivity_1 + 1.0 / emissivity_2 - 1.0)
    h_rad = 4.0 * sigma * e_eff * temperature_k**3
    r_rad = 1.0 / h_rad if h_rad > 0 else math.inf

    # Total gap resistance (parallel convection and radiation)
    r_total = 1.0 / (1.0 / r_cv + 1.0 / r_rad)

    return r_total


# Pre-computed typical R-values for standard gaps at NFRC conditions
# (20°C mean temperature, 15K temperature difference, clear glass ε=0.84)
TYPICAL_GAP_R_VALUES: dict[str, dict[float, float]] = {
    # gap thickness (mm) -> R-value (m²·K/W)
    "AIR": {
        6: 0.11,
        9: 0.13,
        12: 0.14,
        15: 0.14,
    },
    "ARGON": {
        6: 0.11,
        9: 0.14,
        12: 0.15,
        15: 0.16,
    },
    "KRYPTON": {
        6: 0.13,
        9: 0.16,
        12: 0.17,
        15: 0.17,
    },
    "XENON": {
        6: 0.14,
        9: 0.18,
        12: 0.19,
        15: 0.20,
    },
}


def typical_gap_r_value(gas_type: str, thickness_mm: float) -> float:
    """Get typical R-value for a gas gap at standard conditions.

    Uses interpolation from pre-computed values at NFRC standard conditions.
    For more accurate calculations, use gas_gap_resistance().

    Args:
        gas_type: Gas type (Air, Argon, Krypton, Xenon)
        thickness_mm: Gap thickness in millimeters

    Returns:
        Thermal resistance in m²·K/W
    """
    key = gas_type.upper()
    if key not in TYPICAL_GAP_R_VALUES:
        # Fall back to calculation
        return gas_gap_resistance(gas_type, thickness_mm / 1000)

    table = TYPICAL_GAP_R_VALUES[key]
    thicknesses = sorted(table.keys())

    # Clamp to range
    if thickness_mm <= thicknesses[0]:
        return table[thicknesses[0]]
    if thickness_mm >= thicknesses[-1]:
        return table[thicknesses[-1]]

    # Linear interpolation
    for i, t in enumerate(thicknesses[:-1]):
        t_next = thicknesses[i + 1]
        if t <= thickness_mm <= t_next:
            r1, r2 = table[t], table[t_next]
            frac = (thickness_mm - t) / (t_next - t)
            return r1 + frac * (r2 - r1)

    # Should not reach here
    return table[thicknesses[-1]]
