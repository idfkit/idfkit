"""Verified Python code for the "Simulate an office block" tutorial.

One coherent script: every region runs top-to-bottom against the ``doc`` built
in the first two regions, and the values it prints are the ones the page shows
underneath each step. The named regions are display markers consumed by
``docs/tutorials/office-block.md`` via ``--8<--`` includes.

Running this end to end needs a local EnergyPlus installation and, the first
time, a network connection for the weather download. Both are stated on the
page. pyright checks it on every ``make check`` whether or not either is
present, which is what stops a renamed builder or a changed keyword from
shipping as a broken lesson.
"""

from __future__ import annotations

# --8<-- [start:pin]
from idfkit import LATEST_VERSION, find_closest_version, new_document, version_string
from idfkit.simulation import find_energyplus

energyplus = find_energyplus()
doc = new_document(version=find_closest_version(energyplus.version) or LATEST_VERSION)

print(version_string(energyplus.version))
print(version_string(doc.version))
# --8<-- [end:pin]


# --8<-- [start:block]
from idfkit import ZoningScheme, create_block, footprint_rectangle

WIDTH, DEPTH, STORIES = 30.0, 18.0, 2

create_block(
    doc,
    name="Office",
    footprint=footprint_rectangle(width=WIDTH, depth=DEPTH),
    floor_to_floor=3.5,
    num_stories=STORIES,
    zoning=ZoningScheme.CORE_PERIMETER,
    perimeter_depth=4.5,
)

print(len(doc["Zone"]), "zones,", len(doc["BuildingSurface:Detailed"]), "surfaces")
for zone in doc["Zone"]:
    print(zone.name)
# --8<-- [end:block]


# --8<-- [start:envelope]
from idfkit import set_default_constructions, set_wwr

doc.add(
    "Material",
    "Concrete 200mm",
    roughness="MediumRough",
    thickness=0.2,
    conductivity=1.4,
    density=2400,
    specific_heat=900,
)
doc.add(
    "Material",
    "Insulation 100mm",
    roughness="MediumRough",
    thickness=0.1,
    conductivity=0.04,
    density=30,
    specific_heat=1400,
)
doc.add(
    "Construction",
    "Insulated Wall",
    outside_layer="Concrete 200mm",
    layer_2="Insulation 100mm",
)

doc.add(
    "WindowMaterial:SimpleGlazingSystem",
    "Double Glazing",
    u_factor=1.8,
    solar_heat_gain_coefficient=0.4,
)
doc.add("Construction", "Exterior Window", outside_layer="Double Glazing")

windows = set_wwr(doc, wwr=0.4, construction="Exterior Window")
opaque = set_default_constructions(doc, construction_name="Insulated Wall")

print(len(windows), "windows,", opaque, "opaque surfaces")
# --8<-- [end:envelope]


# --8<-- [start:weather]
from idfkit.weather import DesignDayManager, StationIndex, WeatherDownloader

nearest = StationIndex.load().nearest(41.88, -87.63, limit=1)[0]
print(f"{nearest.station.city} ({nearest.distance_km:.1f} km away)")

files = WeatherDownloader().download(nearest.station)
added = DesignDayManager(files.ddy).apply_to_model(doc, heating="99.6%")

for name in added:
    print(name)
# --8<-- [end:weather]


# --8<-- [start:condition]
doc.add(
    "HVACTemplate:Thermostat",
    "Office Setpoints",
    constant_heating_setpoint=20.0,
    constant_cooling_setpoint=24.0,
)

for zone in doc["Zone"]:
    doc.add(
        "HVACTemplate:Zone:IdealLoadsAirSystem",
        zone_name=zone.name,
        template_thermostat_name="Office Setpoints",
    )

print(len(doc["HVACTemplate:Zone:IdealLoadsAirSystem"]))
# --8<-- [end:condition]


# --8<-- [start:run]
from idfkit import validate_document
from idfkit.simulation import simulate

HEATING_RATE = "Zone Ideal Loads Supply Air Total Heating Rate"

doc.add("Output:Variable", key_value="*", variable_name=HEATING_RATE, reporting_frequency="Hourly")

print(len(validate_document(doc).errors))

result = simulate(doc, files.epw, design_day=True, energyplus=energyplus, output_dir="office-sizing")
print(result.success)
# --8<-- [end:run]


# --8<-- [start:read]
sql = result.sql

per_zone = [sql.get_timeseries(HEATING_RATE, v.key_value) for v in sql.list_variables() if v.name == HEATING_RATE]
block_kw = [sum(hour) / 1000 for hour in zip(*(series.values for series in per_zone))]

peak_kw = max(block_kw)
peak_at = per_zone[0].timestamps[block_kw.index(peak_kw)]
floor_area = WIDTH * DEPTH * STORIES

print(f"{len(per_zone)} zones, {len(block_kw)} hours")
print(f"peak {peak_kw:.1f} kW at {peak_at:%H:%M}, {peak_kw * 1000 / floor_area:.1f} W/m2")

for series in sorted(per_zone, key=lambda s: max(s.values), reverse=True):
    label = series.key_value.removesuffix(" IDEAL LOADS AIR SYSTEM").title()
    print(f"{label:36} {max(series.values) / 1000:5.1f} kW")
# --8<-- [end:read]
