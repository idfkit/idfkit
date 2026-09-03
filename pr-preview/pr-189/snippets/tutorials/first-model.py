"""Verified Python code for the "Build your first model" tutorial.

This is a single, coherent script: every region runs top-to-bottom against the
one ``doc`` created in the first region, and the values it prints are the ones
the page shows underneath each step. The named regions are display markers
consumed by ``docs/tutorials/first-model.md`` via ``--8<--`` includes.

The page's TypeScript tabs are the same lesson in the other language and stay
literal on the page: the site builds without the second language's toolchain
(FR-058), so there is nothing here to check them against.
"""

from __future__ import annotations

# --8<-- [start:create]
from idfkit import new_document, version_string

doc = new_document(version=(26, 1, 0))

print(version_string(doc.version))
# --8<-- [end:create]


# --8<-- [start:zone]
zone = doc.add("Zone", "Open Office", ceiling_height=2.7, multiplier=1)

print(zone.name, zone.ceiling_height)
# --8<-- [end:zone]


# --8<-- [start:surface]
doc.add(
    "Material",
    "Brick 100mm",
    roughness="MediumRough",
    thickness=0.1,
    conductivity=0.89,
    density=1920,
    specific_heat=790,
)

doc.add("Construction", "Exterior Wall", outside_layer="Brick 100mm")

wall = doc.add(
    "BuildingSurface:Detailed",
    "North Wall",
    surface_type="Wall",
    construction_name="Exterior Wall",
    zone_name="Open Office",
    outside_boundary_condition="Outdoors",
    sun_exposure="SunExposed",
    wind_exposure="WindExposed",
)
# --8<-- [end:surface]


# --8<-- [start:vertices]
wall.vertices.extend([
    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 2.7},
    {"vertex_x_coordinate": 0, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
    {"vertex_x_coordinate": 5, "vertex_y_coordinate": 0, "vertex_z_coordinate": 0},
    {"vertex_x_coordinate": 5, "vertex_y_coordinate": 0, "vertex_z_coordinate": 2.7},
])

print(len(wall.vertices))
# --8<-- [end:vertices]


# --8<-- [start:validate]
from idfkit import validate_document

result = validate_document(doc)

print(len(result.errors))
# --8<-- [end:validate]


# --8<-- [start:rename]
print(wall.zone_name)

doc.rename("Zone", "Open Office", "Open Plan")

print(wall.zone_name)
print(", ".join(o.name for o in doc.get_referencing("Open Plan")))
# --8<-- [end:rename]


# --8<-- [start:save]
from idfkit import save_idf

save_idf(doc, "office.idf")
# --8<-- [end:save]


# --8<-- [start:reread]
from idfkit import load_idf

reread = load_idf("office.idf")

print(version_string(reread.version))

for z in reread["Zone"]:
    print(f"{z.name}: ceiling {z.ceiling_height} m")

wall_again = reread["BuildingSurface:Detailed"]["North Wall"]
print(len(wall_again.vertices))
print(wall_again.vertices[0].vertex_z_coordinate)
# --8<-- [end:reread]
