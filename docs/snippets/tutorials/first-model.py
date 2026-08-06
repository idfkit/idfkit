"""Verified code for the "Build your first model" tutorial.

This is a single, coherent script: every region runs top-to-bottom against the
one ``doc`` created in the first region. The named regions are display markers
consumed by ``docs/tutorials/first-model.md`` via ``--8<--`` includes.
"""

from __future__ import annotations

# --8<-- [start:new]
from idfkit import new_document

doc = new_document(version=(24, 1, 0))
print(doc.version)  # (24, 1, 0)
# --8<-- [end:new]


# --8<-- [start:block]
from idfkit import ZoningScheme, create_block, footprint_rectangle

create_block(
    doc,
    name="Office",
    footprint=footprint_rectangle(width=20.0, depth=12.0),
    floor_to_floor=3.0,
    num_stories=2,
    zoning=ZoningScheme.CORE_PERIMETER,
    perimeter_depth=4.0,
)

print(len(doc["Zone"]))  # 10
print(len(doc["BuildingSurface:Detailed"]))  # 60
# --8<-- [end:block]


# --8<-- [start:constructions]
# An opaque wall construction: one concrete layer.
doc.add(
    "Material",
    "Concrete",
    roughness="MediumRough",
    thickness=0.2,
    conductivity=1.4,
    density=2400,
    specific_heat=900,
)
doc.add("Construction", "Exterior Wall", outside_layer="Concrete")

# A window construction: one simple-glazing layer.
doc.add(
    "WindowMaterial:SimpleGlazingSystem",
    "Glazing",
    u_factor=1.8,
    solar_heat_gain_coefficient=0.4,
)
doc.add("Construction", "Exterior Window", outside_layer="Glazing")
# --8<-- [end:constructions]


# --8<-- [start:windows]
from idfkit import set_default_constructions, set_wwr

# Punch windows into the exterior walls at 40% window-to-wall ratio, using the
# glazing construction. Do this first so the windows claim their own construction.
windows = set_wwr(doc, wwr=0.4, construction="Exterior Window")

# Assign the opaque construction to every surface that still lacks one.
filled = set_default_constructions(doc, construction_name="Exterior Wall")

print(len(windows))  # 8
print(filled)  # 60
# --8<-- [end:windows]


# --8<-- [start:inspect]
zone = doc["Zone"].first()
print(zone.name)  # Office Story 1 Perimeter_South
# --8<-- [end:inspect]


# --8<-- [start:rename]
old_name = zone.name
referencing = doc.references.get_referencing(old_name)
print(len(referencing))  # 6 — the surfaces bounding this zone

doc.rename("Zone", old_name, "Office Lobby")

# The references followed the rename automatically: nothing dangles.
print(len(doc.references.get_referencing(old_name)))  # 0
print(len(doc.references.get_referencing("Office Lobby")))  # 6
# --8<-- [end:rename]


# --8<-- [start:validate]
from idfkit import validate_document

result = validate_document(doc)
print(result.is_valid)  # True
print(len(result.errors))  # 0
# --8<-- [end:validate]


# --8<-- [start:write]
from idfkit import write_idf

write_idf(doc, "office.idf")
# --8<-- [end:write]


# --8<-- [start:weather]
from idfkit.weather import DesignDayManager, StationIndex, WeatherDownloader

# idfkit locates, downloads, and caches weather + design-day data for you.
station = StationIndex.load().nearest(41.88, -87.63, limit=1)[0].station  # near Chicago
files = WeatherDownloader().download(station)

# Inject a design day (and update Site:Location) from the downloaded .ddy file.
added = DesignDayManager(files.ddy).apply_to_model(doc, update_location=True)
print(len(added))  # 1 — a winter heating design day
# --8<-- [end:weather]


# --8<-- [start:simulate]
# Ask EnergyPlus to report each zone's air temperature.
doc.add(
    "Output:Variable",
    key_value="*",
    variable_name="Zone Mean Air Temperature",
    reporting_frequency="Hourly",
)

from idfkit.simulation import simulate

# design_day=True runs only the sizing design day (seconds, not minutes). The
# model is version 24.1; auto_migrate forward-migrates it to your installed
# EnergyPlus first.
result = simulate(doc, files.epw, design_day=True, auto_migrate=True)
print(result.success)  # True
# --8<-- [end:simulate]


# --8<-- [start:read]
sql = result.sql

# One temperature series per zone — ten, matching the ten zones we built.
print(len(sql.list_variables()))  # 10

# EnergyPlus upper-cases key values, so the lobby is "OFFICE LOBBY".
lobby = sql.get_timeseries("Zone Mean Air Temperature", "OFFICE LOBBY")
print(len(lobby.values))  # 24 — one value per hour of the design day
print(round(max(lobby.values), 1))  # e.g. -0.9 (varies by EnergyPlus version + weather)
# --8<-- [end:read]
