from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.simulation import SimulationResult

doc: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
expanded: IDFDocument = ...  # type: ignore[assignment]
tmpl: IDFObject = ...  # type: ignore[assignment]
tmpl_type: str = ...  # type: ignore[assignment]
ideal: IDFObject = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import new_document
from idfkit.simulation import simulate

doc = new_document()
# ... create zones via create_block, etc.

# Single Thermostat shared by every zone
doc.add("HVACTemplate:Thermostat", "OfficeT", constant_heating_setpoint=20.0, constant_cooling_setpoint=24.0)

# IdealLoadsAirSystem: no plant loops needed. Best for parametric studies.
for zone in doc["Zone"]:
    doc.add("HVACTemplate:Zone:IdealLoadsAirSystem", zone_name=zone.name, template_thermostat_name="OfficeT")

result = simulate(doc, "weather.epw", expand_objects=True)
# --8<-- [end:quickstart]


# --8<-- [start:worked-example]
# Thermostat (shared)
doc.add(
    "HVACTemplate:Thermostat",
    "OfficeT",
    heating_setpoint_schedule_name="OfficeHtgSetpt",
    cooling_setpoint_schedule_name="OfficeClgSetpt",
)

# Zone equipment — one per zone
for zone in doc["Zone"]:
    doc.add(
        "HVACTemplate:Zone:VAV",
        zone_name=zone.name,
        template_vav_system_name="AHU-1",
        template_thermostat_name="OfficeT",
        zone_minimum_air_flow_input_method="Constant",
        constant_minimum_air_flow_fraction=0.3,
    )

# Air-side system
doc.add(
    "HVACTemplate:System:VAV",
    "AHU-1",
    cooling_coil_type="ChilledWater",
    heating_coil_type="HotWater",
    cooling_coil_design_setpoint=12.8,
    heating_coil_design_setpoint=12.0,
    economizer_type="NoEconomizer",
)

# Water-side loops + sources
doc.add(
    "HVACTemplate:Plant:ChilledWaterLoop",
    "CHW Loop",
    chilled_water_design_setpoint=6.7,
    condenser_water_design_setpoint=29.4,
)
doc.add(
    "HVACTemplate:Plant:Chiller",
    "Chiller 1",
    chiller_type="ElectricCentrifugalChiller",
    capacity="Autosize",
    condenser_type="WaterCooled",
)
doc.add("HVACTemplate:Plant:Tower", "CT-1", tower_type="SingleSpeed", high_speed_nominal_capacity="Autosize")

doc.add("HVACTemplate:Plant:HotWaterLoop", "HW Loop", hot_water_design_setpoint=82.0)
doc.add(
    "HVACTemplate:Plant:Boiler",
    "Boiler 1",
    boiler_type="HotWaterBoiler",
    capacity="Autosize",
    efficiency=0.90,
    fuel_type="NaturalGas",
)
# --8<-- [end:worked-example]


# --8<-- [start:expand-option1]
from idfkit.simulation import simulate

result = simulate(doc, "weather.epw", expand_objects=True)
# --8<-- [end:expand-option1]


# --8<-- [start:expand-option2]
expanded = doc.expand()  # returns a new IDFDocument
# Templates are gone; the low-level equivalents are present
if "ZoneHVAC:IdealLoadsAirSystem" in expanded:
    for ideal in expanded["ZoneHVAC:IdealLoadsAirSystem"]:
        print(ideal.name, ideal.cooling_limit)
# --8<-- [end:expand-option2]


# --8<-- [start:expand-option3]
from idfkit.simulation import expand_objects

expanded = expand_objects(doc)
# --8<-- [end:expand-option3]


# --8<-- [start:enumerate]
for tmpl in doc.hvac_templates:
    print(tmpl.obj_type, tmpl.name)
# or
for tmpl_type in [t for t in doc.collections if t.startswith("HVACTemplate:")]:
    for tmpl in doc[tmpl_type]:
        print(tmpl_type, tmpl.name)
# --8<-- [end:enumerate]


# --8<-- [start:mistake-mix-good]
doc.add("HVACTemplate:Zone:IdealLoadsAirSystem", zone_name="Office", template_thermostat_name="OfficeT")
# ... or write the ZoneHVAC:IdealLoadsAirSystem by hand, but not both.
# --8<-- [end:mistake-mix-good]


# --8<-- [start:mistake-simulate-good]
result = simulate(doc, "weather.epw", expand_objects=True)  # the default
# --8<-- [end:mistake-simulate-good]


# --8<-- [start:mistake-expand-good]
expanded = doc.expand()
simulate(expanded, "weather.epw", expand_objects=False)
# --8<-- [end:mistake-expand-good]
