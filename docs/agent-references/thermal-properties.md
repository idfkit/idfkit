# Thermal properties

`idfkit.thermal` computes envelope thermal performance from a `Construction` and its referenced materials: R-value, U-value, SHGC, visible transmittance, and gas-mixture properties. The math is closed-form (no simulation needed).

## When to use

- You're sanity-checking a construction against a code requirement (R-13, U-0.30, …).
- You're parametrically tuning insulation thickness or glazing assemblies.
- You need gas-gap resistance for IGU calculations.
- You're producing a construction summary report.

## Quick start

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:quickstart"
```

## Core API

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:core-api"
```

## Construction layers

`get_construction_layers(construction)` returns the layered material data in order (exterior → interior):

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:construction-layers"
```

Each `LayerThermalProperties` exposes `name`, `obj_type`, `thickness`, `conductivity`, the computed `r_value`, and glazing fields (`is_glazing`, `shgc`, `visible_transmittance`, …) for that layer.

## R-value and U-value

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:r-u-value"
```

The film coefficients are NFRC standard values (per surface orientation), exposed via `NFRC_FILM_COEFFICIENTS` and `FILM_RESISTANCE` if you need to inspect them.

## SHGC and visible transmittance

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:shgc-vt"
```

These work for `WindowMaterial:SimpleGlazingSystem` (read directly from fields) and detailed glazing assemblies (computed from layered `WindowMaterial:Glazing`).

For an unsupported glazing assembly, both return `None`.

## Whole-construction summary

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:summary"
```

Use this when you're emitting a construction report and don't want N round-trips.

## Gas-gap properties

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:gas-gap"
```

`gas_gap_resistance` accounts for conduction, convection, and radiation through the gas film — useful for IGU design when you're not relying on EnergyPlus's own glazing solver.

Custom gas mixtures: build a `GasProperties` instance manually with the constituent properties (conductivity, viscosity, density, specific heat) and use that instead of a `GasType` string.

## Worked example: comparing wall assemblies

```python
--8<-- "docs/snippets/agent_references/thermal-properties.py:worked-example"
```

(`R-value × 5.678` converts m²·K/W to IP-units ft²·°F·h/Btu.)

## Common mistakes

!!! failure "comparing R-values without films"

    ```python
    r_a = calculate_r_value(wall_a, include_films=False)
    r_b = calculate_r_value(wall_b)                         # includes films
    # Apples and oranges; r_a is intentionally lower
    ```

!!! success "fix one mode and stick to it"

    ```python
    --8<-- "docs/snippets/agent_references/thermal-properties.py:mistake-films-good"
    ```

!!! failure "using SHGC for an opaque construction"

    ```python
    shgc = calculate_shgc(opaque_wall)         # returns None
    ```

!!! success "branch on construction type or trust `None`"

    ```python
    --8<-- "docs/snippets/agent_references/thermal-properties.py:mistake-shgc-good"
    ```

!!! failure "running thermal calcs against an `IDFObject` that lacks `_document`"

    ```python
    loose_obj = IDFObject("Construction", "X", ...)   # no _document
    calculate_r_value(loose_obj)                       # can't resolve material references
    ```

!!! success "operate on objects belonging to a `doc`"

    ```python
    --8<-- "docs/snippets/agent_references/thermal-properties.py:mistake-doc-good"
    ```

## Related

- [document-and-objects.md](document-and-objects.md) — looking up constructions and materials.
- [geometry-and-surfaces.md](geometry-and-surfaces.md) — combining U-value with surface area for whole-wall heat loss.
- API docs: [py.idfkit.com/api/thermal/](https://py.idfkit.com/api/thermal/)
