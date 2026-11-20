# HVAC templates

`HVACTemplate:*` objects are EnergyPlus's high-level HVAC shortcuts: one object expands into the dozens of low-level `ZoneHVAC:*`, `AirLoopHVAC`, `PlantLoop`, `Coil:*`, `Fan:*`, `Branch`, and `BranchList` objects that EnergyPlus actually simulates. For agent workflows this is the single highest-leverage feature in idfkit — you can stand up a runnable model with realistic HVAC in a handful of `doc.add()` calls instead of dozens.

## When to use

- You're building a model from scratch or modifying one and need HVAC fast.
- You want a plausible energy estimate without modelling every coil, fan, and pump.
- You're comparing HVAC system types with otherwise-identical models.

When templates aren't enough (custom topology, unusual controls, retrofits) drop to hand-authored `AirLoopHVAC` / `PlantLoop` — see [hvac-loops.md](hvac-loops.md).

## Quick start: fastest energy estimate

```python
from idfkit import new_document
from idfkit.simulation import simulate

doc = new_document()
# ... create zones via create_block, etc.

# new_document() has no RunPeriod; without one (or design days with design_day=True)
# simulate() refuses the run, as EnergyPlus would have nothing to simulate.
doc.run_periods.add("Annual", begin_month=1, begin_day_of_month=1, end_month=12, end_day_of_month=31)

# Single Thermostat shared by every zone
doc.hvac_template_thermostats.add("OfficeT", constant_heating_setpoint=20.0, constant_cooling_setpoint=24.0)

# IdealLoadsAirSystem: no plant loops needed. Best for parametric studies.
for zone in doc["Zone"]:
    doc.hvac_template_zone_ideal_loads_air_systems.add(zone_name=zone.name, template_thermostat_name="OfficeT")

result = simulate(doc, "weather.epw", expand_objects=True)
```

## The four-tier layering

| Tier | What it does | Examples |
|---|---|---|
| **Thermostat** | Setpoints shared by zones. | `HVACTemplate:Thermostat` |
| **Zone** | One per conditioned zone — equipment that serves that zone. | `HVACTemplate:Zone:IdealLoadsAirSystem`, `:VAV`, `:FanCoil`, `:PTAC`, … |
| **System** | Air-side equipment that serves multiple zones (AHUs, DOAS). | `HVACTemplate:System:VAV`, `:UnitarySystem`, `:DedicatedOutdoorAir`, … |
| **Plant** | Water-side equipment (chillers, boilers, towers) and loops. | `HVACTemplate:Plant:ChilledWaterLoop`, `:HotWaterLoop`, `:Chiller`, `:Boiler`, `:Tower` |

Zone objects reference Systems by name; Systems reference Plants by name. Every Zone object references a Thermostat.

## Complete enumeration (EnergyPlus 26.2)

```
HVACTemplate:Thermostat

HVACTemplate:Zone:BaseboardHeat
HVACTemplate:Zone:ConstantVolume
HVACTemplate:Zone:DualDuct
HVACTemplate:Zone:FanCoil
HVACTemplate:Zone:IdealLoadsAirSystem
HVACTemplate:Zone:PTAC
HVACTemplate:Zone:PTHP
HVACTemplate:Zone:Unitary
HVACTemplate:Zone:VAV
HVACTemplate:Zone:VAV:FanPowered
HVACTemplate:Zone:VAV:HeatAndCool
HVACTemplate:Zone:VRF
HVACTemplate:Zone:WaterToAirHeatPump

HVACTemplate:System:ConstantVolume
HVACTemplate:System:DedicatedOutdoorAir
HVACTemplate:System:DualDuct
HVACTemplate:System:PackagedVAV
HVACTemplate:System:Unitary
HVACTemplate:System:UnitaryHeatPump:AirToAir
HVACTemplate:System:UnitarySystem
HVACTemplate:System:VAV
HVACTemplate:System:VRF

HVACTemplate:Plant:Boiler
HVACTemplate:Plant:Boiler:ObjectReference
HVACTemplate:Plant:ChilledWaterLoop
HVACTemplate:Plant:Chiller
HVACTemplate:Plant:Chiller:ObjectReference
HVACTemplate:Plant:HotWaterLoop
HVACTemplate:Plant:MixedWaterLoop
HVACTemplate:Plant:Tower
HVACTemplate:Plant:Tower:ObjectReference
```

For full I/O Reference, see [docs.idfkit.com/io-reference/hvac-template-objects/group-hvac-templates/](https://docs.idfkit.com/io-reference/hvac-template-objects/group-hvac-templates/) or look up any individual type with `doc.describe("HVACTemplate:Zone:VAV")`.

## Worked example: full VAV + ChilledWater + HotWater system

```python
# Thermostat (shared)
doc.hvac_template_thermostats.add(
    "OfficeT",
    heating_setpoint_schedule_name="OfficeHtgSetpt",
    cooling_setpoint_schedule_name="OfficeClgSetpt",
)

# Zone equipment — one per zone
for zone in doc["Zone"]:
    doc.hvac_template_zone_vavs.add(
        zone_name=zone.name,
        template_vav_system_name="AHU-1",
        template_thermostat_name="OfficeT",
        zone_minimum_air_flow_input_method="Constant",
        constant_minimum_air_flow_fraction=0.3,
    )

# Air-side system
doc.hvac_template_system_vavs.add(
    "AHU-1",
    cooling_coil_type="ChilledWater",
    heating_coil_type="HotWater",
    cooling_coil_design_setpoint=12.8,
    heating_coil_design_setpoint=12.0,
    economizer_type="NoEconomizer",
)

# Water-side loops + sources
doc.hvac_template_plant_chilled_water_loop.add(
    "CHW Loop",
    chilled_water_design_setpoint=6.7,
    condenser_water_design_setpoint=29.4,
)
doc.hvac_template_plant_chillers.add(
    "Chiller 1",
    chiller_type="ElectricCentrifugalChiller",
    capacity="Autosize",
    nominal_cop=6.1,
    condenser_type="WaterCooled",
)
doc.hvac_template_plant_towers.add("CT-1", tower_type="SingleSpeed", high_speed_nominal_capacity="Autosize")

doc.hvac_template_plant_hot_water_loop.add("HW Loop", hot_water_design_setpoint=82.0)
doc.hvac_template_plant_boilers.add(
    "Boiler 1",
    boiler_type="HotWaterBoiler",
    capacity="Autosize",
    efficiency=0.90,
    fuel_type="NaturalGas",
)
```

Then run the simulation with expansion enabled — see below.

## Expanding templates

Templates must be expanded into low-level objects before EnergyPlus can simulate them. You have three options:

### Option 1 — let `simulate` handle it (recommended)

```python
from idfkit.simulation import simulate

result = simulate(doc, "weather.epw", expand_objects=True)
```

idfkit invokes `ExpandObjects` as a preprocessor and feeds EnergyPlus the expanded model. The original `doc` is untouched.

### Option 2 — expand explicitly via `doc.expand()` and inspect

```python
expanded = doc.expand()  # returns a new IDFDocument
# Templates are gone; the low-level equivalents are present
if "ZoneHVAC:IdealLoadsAirSystem" in expanded:
    for ideal in expanded["ZoneHVAC:IdealLoadsAirSystem"]:
        print(ideal.name, ideal.cooling_limit)
```

Use this when you want to study what `ExpandObjects` produced or hand-modify the result.

### Option 3 — function-style

```python
from idfkit.simulation import expand_objects

expanded = expand_objects(doc)
```

Equivalent to `doc.expand()`. Useful if you prefer free functions to methods.

All three return a new document whose `filepath` is `None`, even when there was nothing to expand, so a bare `expanded.save()` raises `ValueError` rather than overwriting the source: save it with `save_idf(expanded, path)` or `expanded.save(path)`.

`doc.expand()`, `expand_objects()`, `run_slab_preprocessor()` and `run_basement_preprocessor()` raise `ExpandObjectsError` when `ExpandObjects` reports a *Fatal* `Output:PreprocessorMessage`, such as a zone template naming a system that does not exist or a system with no zone; the error quotes the message. They no longer return a partly expanded model. `run_preprocessing()`, which `simulate()` uses, leaves the message for EnergyPlus, so `simulate()` returns `success=False` instead of raising.

The IDF writer pads every `HVACTemplate:*` and `GroundHeatTransfer:*` object to its schema `min_fields` with blank fields, as IDF Editor does, because `ExpandObjects` reads them from the IDF text and stops on a shorter one ("The number of fields in the IDD do not match"). Set only the fields you need; the blanks take their defaults.

All three require EnergyPlus to be installed (`ExpandObjects` is a C++ binary that ships with EnergyPlus). Discovery is automatic via `$ENERGYPLUS_DIR`, `$PATH`, or standard install locations.

## Enumerating templates already in a model

```python
for tmpl in doc.hvac_templates:
    print(tmpl.obj_type, tmpl.name)
# or
for tmpl_type in [t for t in doc.collections if t.startswith("HVACTemplate:")]:
    for tmpl in doc.get_collection(tmpl_type):
        print(tmpl_type, tmpl.name)
```

`doc.hvac_templates` is the convenience accessor for the most common template (`HVACTemplate:Zone:IdealLoadsAirSystem`); the loop covers every template type.

## Why expansion is destructive

After `doc.expand()`, the resulting document has zero `HVACTemplate:*` objects — they've been replaced by their low-level expansions. This means:

- You can't edit the templates after expansion (they're gone).
- The expanded document is committed to the topology `ExpandObjects` produced.
- If you want to tweak the system, edit the **template** first, then re-expand.

The `simulate(doc, ..., expand_objects=True)` path expands a copy for EnergyPlus to consume but leaves your in-memory `doc` untouched, so you can re-run after editing the templates.

## Common mistakes

!!! failure "mixing templates with hand-authored ZoneHVAC on the same zone"

    ```python
    doc.add("HVACTemplate:Zone:IdealLoadsAirSystem", zone_name="Office", template_thermostat_name="OfficeT")
    doc.add("ZoneHVAC:IdealLoadsAirSystem", "Office Ideal Loads", zone_supply_air_node_name="...")
    # ExpandObjects produces another ZoneHVAC:IdealLoadsAirSystem — now you have two,
    # the zone is double-conditioned, results are nonsense.
    ```

!!! success "pick one approach per zone"

    ```python
    doc.hvac_template_zone_ideal_loads_air_systems.add(zone_name="Office", template_thermostat_name="OfficeT")
    # ... or write the ZoneHVAC:IdealLoadsAirSystem by hand, but not both.
    ```

!!! failure "simulating without expansion"

    ```python
    result = simulate(doc, "weather.epw")      # expand_objects defaults to True, but if you opted out:
    result = simulate(doc, "weather.epw", expand_objects=False)
    # .err contains "HVACTemplate:Zone:VAV is an invalid object type"
    ```

!!! success "let `simulate` expand for you"

    ```python
    result = simulate(doc, "weather.epw", expand_objects=True)  # the default
    ```

!!! failure "expecting `doc.expand()` to mutate"

    ```python
    doc.expand()                               # discarded — expand() returns a new document
    simulate(doc, "weather.epw", expand_objects=False)   # original still has templates
    ```

!!! success "capture the return value"

    ```python
    expanded = doc.expand()
    simulate(expanded, "weather.epw", expand_objects=False)
    ```

## When to drop down

If you outgrow templates — needing custom controllers, unusual topology, plant interactions templates can't express — author `AirLoopHVAC` / `PlantLoop` directly. See [hvac-loops.md](hvac-loops.md).

## Related

- [hvac-loops.md](hvac-loops.md) — hand-authoring HVAC loops below the template layer.
- [simulation-execution.md](simulation-execution.md) — running models with `expand_objects=True`.
- [document-and-objects.md](document-and-objects.md) — `doc.add` and `doc.describe`.
- I/O Reference: [docs.idfkit.com/io-reference/hvac-template-objects/group-hvac-templates/](https://docs.idfkit.com/io-reference/hvac-template-objects/group-hvac-templates/)
