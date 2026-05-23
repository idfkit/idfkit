# Thermal properties

`idfkit.thermal` computes envelope thermal performance from a `Construction` and its referenced materials: R-value, U-value, SHGC, visible transmittance, and gas-mixture properties. The math is closed-form (no simulation needed).

## When to use

- You're sanity-checking a construction against a code requirement (R-13, U-0.30, …).
- You're parametrically tuning insulation thickness or glazing assemblies.
- You need gas-gap resistance for IGU calculations.
- You're producing a construction summary report.

## Quick start

```python
from idfkit import load_idf
from idfkit.thermal import calculate_r_value, calculate_u_value, calculate_shgc

doc = load_idf("building.idf")
wall = doc["Construction"]["ExteriorWall"]

print(calculate_r_value(wall), "m²·K/W")    # opaque R-value with film resistances
print(calculate_u_value(wall), "W/m²·K")    # 1 / R

window = doc["Construction"]["DoublePane"]
print(calculate_shgc(window))                # Solar Heat Gain Coefficient
```

## Core API

```python
from idfkit.thermal import (
    calculate_r_value,                 # opaque + glazing, with/without films
    calculate_u_value,                 # 1 / r_value
    calculate_shgc,                    # glazing only
    calculate_visible_transmittance,   # glazing only
    get_construction_layers,           # ordered LayerThermalProperties
    get_thermal_properties,            # ConstructionThermalProperties bundle
    LayerThermalProperties,
    ConstructionThermalProperties,
    NFRC_FILM_COEFFICIENTS,
    FILM_RESISTANCE,
)

from idfkit.thermal.gas import (
    GasType,                           # AIR, ARGON, KRYPTON, XENON
    GasProperties,
    get_gas_properties,
    gas_gap_resistance,
    typical_gap_r_value,
    TYPICAL_GAP_R_VALUES,
)
```

## Construction layers

`get_construction_layers(construction)` returns the layered material data in order (exterior → interior):

```python
layers = get_construction_layers(wall)
for layer in layers:
    print(layer.material_name, layer.thickness, layer.conductivity, layer.r_value)
```

Each `LayerThermalProperties` exposes `material_name`, `material_type`, `thickness`, `conductivity`, `density`, `specific_heat`, and the computed `r_value` for that layer.

## R-value and U-value

```python
# Opaque wall: includes interior + exterior film resistances by default (NFRC)
r = calculate_r_value(wall)
r_no_films = calculate_r_value(wall, include_films=False)

u = calculate_u_value(wall)                # 1 / calculate_r_value(wall)
```

The film coefficients are NFRC standard values (per surface orientation), exposed via `NFRC_FILM_COEFFICIENTS` and `FILM_RESISTANCE` if you need to inspect them.

## SHGC and visible transmittance

```python
shgc = calculate_shgc(double_pane)         # 0..1
vt   = calculate_visible_transmittance(double_pane)
```

These work for `WindowMaterial:SimpleGlazingSystem` (read directly from fields) and detailed glazing assemblies (computed from layered `WindowMaterial:Glazing`).

For an unsupported glazing assembly, both return `None`.

## Whole-construction summary

```python
from idfkit.thermal import get_thermal_properties

p = get_thermal_properties(wall)
p.r_value                                  # m²·K/W
p.u_value                                  # W/m²·K
p.shgc                                     # None for opaque
p.visible_transmittance                    # None for opaque
p.thickness                                # total wall thickness (m)
p.layers                                   # list[LayerThermalProperties]
```

Use this when you're emitting a construction report and don't want N round-trips.

## Gas-gap properties

```python
from idfkit.thermal.gas import GasType, gas_gap_resistance, typical_gap_r_value

# Resistance of a 12 mm argon gap between two glass panes at 290 K mean temperature
r_gap = gas_gap_resistance(
    gas_type=GasType.ARGON,
    thickness_m=0.012,
    mean_temperature_k=290.0,
    delta_temperature_k=15.0,
)

# Quick lookup of "typical" R-value (used by simplified glazing)
r = typical_gap_r_value("argon", thickness_mm=12.0)
```

`gas_gap_resistance` accounts for conduction, convection, and radiation through the gas film — useful for IGU design when you're not relying on EnergyPlus's own glazing solver.

Custom gas mixtures: build a `GasProperties` instance manually with the constituent properties (conductivity, viscosity, density, specific heat) and pass it where `GasType` would go.

## Worked example: comparing wall assemblies

```python
from idfkit.thermal import calculate_r_value

for name in ("ExteriorWall_Baseline", "ExteriorWall_R30", "ExteriorWall_R40"):
    wall = doc["Construction"][name]
    r = calculate_r_value(wall)
    print(f"{name}: R-{r * 5.678:.0f} (R-{r:.2f} m²·K/W)")
```

(`R-value × 5.678` converts m²·K/W to IP-units ft²·°F·h/Btu.)

## Common mistakes

**BAD — comparing R-values without films**

```python
r_a = calculate_r_value(wall_a, include_films=False)
r_b = calculate_r_value(wall_b)                         # includes films
# Apples and oranges; r_a is intentionally lower
```

**GOOD — fix one mode and stick to it**

```python
r_a = calculate_r_value(wall_a)
r_b = calculate_r_value(wall_b)
```

**BAD — using SHGC for an opaque construction**

```python
shgc = calculate_shgc(opaque_wall)         # returns None
```

**GOOD — branch on construction type or trust `None`**

```python
shgc = calculate_shgc(construction)
if shgc is None:
    pass  # opaque, no SHGC to report
```

**BAD — running thermal calcs against an `IDFObject` that lacks `_document`**

```python
loose_obj = IDFObject("Construction", "X", ...)   # no _document
calculate_r_value(loose_obj)                       # can't resolve material references
```

**GOOD — operate on objects belonging to a `doc`**

```python
construction = doc["Construction"]["ExteriorWall"]
calculate_r_value(construction)
```

## Related

- [document-and-objects.md](document-and-objects.md) — looking up constructions and materials.
- [geometry-and-surfaces.md](geometry-and-surfaces.md) — combining U-value with surface area for whole-wall heat loss.
- API docs: [py.idfkit.com/api/thermal/](https://py.idfkit.com/api/thermal/)
