# Thermal Properties

The `idfkit.thermal` module provides functions to calculate thermal properties
for EnergyPlus construction assemblies, including R-value, U-value, and SHGC.

## Quick Start

```python
from idfkit import load_idf
from idfkit.thermal import calculate_r_value, calculate_u_value, get_thermal_properties

model = load_idf("building.idf")
wall = model["Construction"]["ExteriorWall"]

# Calculate individual properties
r_value = calculate_r_value(wall)
u_value = calculate_u_value(wall)

print(f"R-value: {r_value:.2f} m²·K/W")
print(f"U-value: {u_value:.2f} W/m²·K")

# Or get all properties at once
props = get_thermal_properties(wall)
print(f"R-value (with films): {props.r_value_with_films:.2f} m²·K/W")
print(f"U-value: {props.u_value:.2f} W/m²·K")
```

## Opaque Constructions

For opaque constructions (walls, roofs, floors), the module calculates:

- **R-value**: Thermal resistance in m²·K/W
- **U-value**: Overall heat transfer coefficient in W/m²·K

### Supported Material Types

| Material Type | How R-value is Calculated |
|---------------|---------------------------|
| `Material` | R = thickness / conductivity |
| `Material:NoMass` | R = thermal_resistance (provided directly) |
| `Material:AirGap` | R = thermal_resistance (provided directly) |

### Example: Multi-Layer Wall

```python
from idfkit import new_document
from idfkit.thermal import calculate_r_value, calculate_u_value

doc = new_document()

# Add materials
doc.add("Material", "Brick", {
    "roughness": "Rough",
    "thickness": 0.1,
    "conductivity": 0.6,
    "density": 1800,
    "specific_heat": 900,
})

doc.add("Material", "Insulation", {
    "roughness": "MediumSmooth",
    "thickness": 0.05,
    "conductivity": 0.04,
    "density": 30,
    "specific_heat": 1000,
})

doc.add("Material", "Gypsum", {
    "roughness": "Smooth",
    "thickness": 0.013,
    "conductivity": 0.16,
    "density": 800,
    "specific_heat": 1000,
})

# Create construction
doc.add("Construction", "InsulatedWall", {
    "outside_layer": "Brick",
    "layer_2": "Insulation",
    "layer_3": "Gypsum",
})

wall = doc["Construction"]["InsulatedWall"]

# Calculate R-value without surface films
r_no_films = calculate_r_value(wall, include_films=False)
print(f"R-value (assembly only): {r_no_films:.2f} m²·K/W")

# Calculate R-value with surface films (default)
r_with_films = calculate_r_value(wall, include_films=True)
print(f"R-value (with films): {r_with_films:.2f} m²·K/W")

# Calculate U-value (always includes films)
u_value = calculate_u_value(wall)
print(f"U-value: {u_value:.2f} W/m²·K")
```

### Surface Film Resistances

The module uses ASHRAE standard film resistances:

| Surface | Resistance (m²·K/W) |
|---------|---------------------|
| Exterior (15 mph wind) | 0.030 |
| Interior (still air) | 0.120 |
| Interior ceiling (heat up) | 0.107 |
| Interior floor (heat down) | 0.160 |

## Glazing Constructions

For glazing constructions (windows), the module calculates:

- **U-value**: Center-of-glass heat transfer coefficient
- **SHGC**: Solar Heat Gain Coefficient
- **VT**: Visible Transmittance

### Supported Glazing Material Types

| Material Type | Properties Used |
|---------------|-----------------|
| `WindowMaterial:SimpleGlazingSystem` | U-factor, SHGC, VT provided directly |
| `WindowMaterial:Glazing` | Thickness, conductivity, optical properties |
| `WindowMaterial:Gas` | Gas type, thickness |

### Example: Double Glazing

```python
from idfkit import new_document
from idfkit.thermal import calculate_u_value, calculate_shgc, get_thermal_properties

doc = new_document()

# Add glazing layers
doc.add("WindowMaterial:Glazing", "ClearGlass", {
    "thickness": 0.006,
    "solar_transmittance_at_normal_incidence": 0.775,
    "front_side_solar_reflectance_at_normal_incidence": 0.071,
    "visible_transmittance_at_normal_incidence": 0.881,
    "front_side_infrared_hemispherical_emissivity": 0.84,
    "back_side_infrared_hemispherical_emissivity": 0.84,
})

doc.add("WindowMaterial:Gas", "ArgonGap", {
    "gas_type": "Argon",
    "thickness": 0.012,
})

doc.add("WindowMaterial:Glazing", "LowEGlass", {
    "thickness": 0.006,
    "solar_transmittance_at_normal_incidence": 0.6,
    "front_side_solar_reflectance_at_normal_incidence": 0.17,
    "visible_transmittance_at_normal_incidence": 0.78,
    "front_side_infrared_hemispherical_emissivity": 0.84,
    "back_side_infrared_hemispherical_emissivity": 0.10,  # Low-E coating
})

# Create construction
doc.add("Construction", "DoubleGlazing", {
    "outside_layer": "ClearGlass",
    "layer_2": "ArgonGap",
    "layer_3": "LowEGlass",
})

window = doc["Construction"]["DoubleGlazing"]

# Get all thermal properties
props = get_thermal_properties(window)

print(f"U-value: {props.u_value:.2f} W/m²·K")
print(f"SHGC: {props.shgc:.2f}")
if props.visible_transmittance:
    print(f"VT: {props.visible_transmittance:.2f}")
```

### Gas Fill Properties

The module includes temperature-dependent property correlations for common
fill gases used in insulated glazing units:

| Gas | Molecular Weight | Thermal Performance |
|-----|------------------|---------------------|
| Air | 28.97 g/mol | Baseline |
| Argon | 39.95 g/mol | ~5% better than air |
| Krypton | 83.80 g/mol | ~10% better than air |
| Xenon | 131.30 g/mol | ~15% better than air |

```python
from idfkit.thermal import typical_gap_r_value

# R-value for a 12mm argon gap
r_argon = typical_gap_r_value("Argon", 12)  # 12mm
print(f"Argon gap R-value: {r_argon:.3f} m²·K/W")
```

## Layer-by-Layer Analysis

Use `get_construction_layers()` to analyze individual layers:

```python
from idfkit.thermal import get_construction_layers

layers = get_construction_layers(wall)

for layer in layers:
    print(f"{layer.name}:")
    print(f"  Type: {layer.obj_type}")
    if layer.thickness:
        print(f"  Thickness: {layer.thickness * 1000:.1f} mm")
    print(f"  R-value: {layer.r_value:.3f} m²·K/W")
```

## API Reference

### Functions

#### `calculate_r_value(construction, include_films=True)`

Calculate thermal resistance for a construction.

**Parameters:**
- `construction`: Construction IDFObject
- `include_films`: Include surface film resistances (default: True)

**Returns:** R-value in m²·K/W

---

#### `calculate_u_value(construction)`

Calculate overall heat transfer coefficient.

**Parameters:**
- `construction`: Construction IDFObject

**Returns:** U-value in W/m²·K

---

#### `calculate_shgc(construction)`

Calculate Solar Heat Gain Coefficient for glazing.

**Parameters:**
- `construction`: Construction IDFObject

**Returns:** SHGC (0-1) or None if not a glazing construction

---

#### `calculate_visible_transmittance(construction)`

Calculate visible light transmittance for glazing.

**Parameters:**
- `construction`: Construction IDFObject

**Returns:** VT (0-1) or None if not a glazing construction

---

#### `get_thermal_properties(construction)`

Get complete thermal properties for a construction.

**Parameters:**
- `construction`: Construction IDFObject

**Returns:** `ConstructionThermalProperties` dataclass with:
- `name`: Construction name
- `layers`: List of `LayerThermalProperties`
- `r_value`: R-value without films
- `r_value_with_films`: R-value with films
- `u_value`: U-value
- `is_glazing`: True if glazing construction
- `shgc`: SHGC (glazing only)
- `visible_transmittance`: VT (glazing only)

---

#### `get_construction_layers(construction)`

Get thermal properties for each layer.

**Parameters:**
- `construction`: Construction IDFObject

**Returns:** List of `LayerThermalProperties`

## Limitations

The thermal calculations in this module are simplified approximations:

1. **Center-of-glass only**: Frame and edge effects are not included
2. **Normal incidence**: Optical properties are for perpendicular solar radiation
3. **Simplified gas gaps**: Uses pre-computed R-values rather than full TARCOG iteration
4. **Standard conditions**: Film coefficients assume standard ASHRAE/NFRC conditions

For precise calculations, use the full EnergyPlus simulation or specialized
tools like WINDOW/THERM.

## See Also

- [Construction Visualization](visualization.md) — SVG diagrams for constructions
- [Objects](objects.md) — IDFObject reference
