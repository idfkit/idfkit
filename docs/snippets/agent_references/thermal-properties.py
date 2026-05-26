from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.thermal import (
    FILM_RESISTANCE,
    NFRC_FILM_COEFFICIENTS,
    ConstructionThermalProperties,
    LayerThermalProperties,
)
from idfkit.thermal.gas import (
    TYPICAL_GAP_R_VALUES,
    GasProperties,
    GasType,
    get_gas_properties,
)

doc: IDFDocument = ...  # type: ignore[assignment]
wall: IDFObject = ...  # type: ignore[assignment]
window: IDFObject = ...  # type: ignore[assignment]
double_pane: IDFObject = ...  # type: ignore[assignment]
wall_a: IDFObject = ...  # type: ignore[assignment]
wall_b: IDFObject = ...  # type: ignore[assignment]
opaque_wall: IDFObject = ...  # type: ignore[assignment]
construction: IDFObject = ...  # type: ignore[assignment]
layer: LayerThermalProperties = ...  # type: ignore[assignment]
props: ConstructionThermalProperties = ...  # type: ignore[assignment]
gas_type: GasType = ...  # type: ignore[assignment]
gas_props: GasProperties = ...  # type: ignore[assignment]
_films = NFRC_FILM_COEFFICIENTS
_resist = FILM_RESISTANCE
_gaps = TYPICAL_GAP_R_VALUES
_get_gas = get_gas_properties

# --8<-- [start:quickstart]
from idfkit import load_idf
from idfkit.thermal import calculate_r_value, calculate_u_value, calculate_shgc

doc = load_idf("building.idf")
wall = doc["Construction"]["ExteriorWall"]

print(calculate_r_value(wall), "m²·K/W")  # opaque R-value with film resistances
print(calculate_u_value(wall), "W/m²·K")  # 1 / R

window = doc["Construction"]["DoublePane"]
print(calculate_shgc(window))  # Solar Heat Gain Coefficient
# --8<-- [end:quickstart]


# --8<-- [start:core-api]
from idfkit.thermal import (
    calculate_r_value,  # opaque + glazing, with/without films
    calculate_u_value,  # 1 / r_value
    calculate_shgc,  # glazing only
    calculate_visible_transmittance,  # glazing only
    get_construction_layers,  # ordered LayerThermalProperties
    get_thermal_properties,  # ConstructionThermalProperties bundle
    LayerThermalProperties,
    ConstructionThermalProperties,
    NFRC_FILM_COEFFICIENTS,
    FILM_RESISTANCE,
)

from idfkit.thermal.gas import (
    GasType,  # Literal["Air", "Argon", "Krypton", "Xenon"]
    GasProperties,
    get_gas_properties,
    gas_gap_resistance,
    typical_gap_r_value,
    TYPICAL_GAP_R_VALUES,
)
# --8<-- [end:core-api]


# --8<-- [start:construction-layers]
layers = get_construction_layers(wall)
for layer in layers:
    print(layer.name, layer.thickness, layer.conductivity, layer.r_value)
# --8<-- [end:construction-layers]


# --8<-- [start:r-u-value]
# Opaque wall: includes interior + exterior film resistances by default (NFRC)
r = calculate_r_value(wall)
r_no_films = calculate_r_value(wall, include_films=False)

u = calculate_u_value(wall)  # 1 / calculate_r_value(wall)
# --8<-- [end:r-u-value]


# --8<-- [start:shgc-vt]
shgc = calculate_shgc(double_pane)  # 0..1
vt = calculate_visible_transmittance(double_pane)
# --8<-- [end:shgc-vt]


# --8<-- [start:summary]
from idfkit.thermal import get_thermal_properties

p = get_thermal_properties(wall)
p.r_value  # m²·K/W (material layers only)
p.r_value_with_films  # m²·K/W including NFRC surface films
p.u_value  # W/m²·K
p.shgc  # None for opaque
p.visible_transmittance  # None for opaque
p.is_glazing  # bool
p.layers  # list[LayerThermalProperties]
# --8<-- [end:summary]


# --8<-- [start:gas-gap]
from idfkit.thermal.gas import gas_gap_resistance, typical_gap_r_value

# Resistance of a 12 mm argon gap between two glass panes at 293 K mean temperature
r_gap = gas_gap_resistance(
    gas_type="Argon",  # "Air", "Argon", "Krypton", "Xenon"
    thickness=0.012,
    temperature_k=293.15,
    delta_t=15.0,
)

# Quick lookup of "typical" R-value (used by simplified glazing)
r = typical_gap_r_value("Argon", thickness_mm=12.0)
# --8<-- [end:gas-gap]


# --8<-- [start:worked-example]
from idfkit.thermal import calculate_r_value

for name in ("ExteriorWall_Baseline", "ExteriorWall_R30", "ExteriorWall_R40"):
    wall = doc["Construction"][name]
    r = calculate_r_value(wall)
    print(f"{name}: R-{r * 5.678:.0f} (R-{r:.2f} m²·K/W)")
# --8<-- [end:worked-example]


# --8<-- [start:mistake-films-good]
r_a = calculate_r_value(wall_a)
r_b = calculate_r_value(wall_b)
# --8<-- [end:mistake-films-good]


# --8<-- [start:mistake-shgc-good]
shgc = calculate_shgc(construction)
if shgc is None:
    pass  # opaque, no SHGC to report
# --8<-- [end:mistake-shgc-good]


# --8<-- [start:mistake-doc-good]
construction = doc["Construction"]["ExteriorWall"]
calculate_r_value(construction)
# --8<-- [end:mistake-doc-good]
