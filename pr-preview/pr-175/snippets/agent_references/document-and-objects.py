from __future__ import annotations

from idfkit import IDFCollection, IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
zones: IDFCollection[IDFObject] = ...  # type: ignore[assignment]
office: IDFObject = ...  # type: ignore[assignment]
material: IDFObject = ...  # type: ignore[assignment]
surface: IDFObject = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import load_idf, new_document, write_idf

# Create or load
doc = new_document()  # blank model at LATEST_VERSION
doc = load_idf("building.idf")  # from disk

# Add an object — keyword args use Python snake_case field names
zone = doc.add("Zone", "Office", x_origin=0.0, y_origin=0.0, ceiling_height=3.0)

# Look up by type, then by name (both are O(1))
zone = doc["Zone"]["Office"]
print(zone.ceiling_height)  # 3.0

# Mutate fields by attribute
zone.ceiling_height = 3.5

# Persist
write_idf(doc, "out.idf")
# --8<-- [end:quickstart]


# --8<-- [start:add-object]
material = doc.add(
    "Material",
    "XPS_50mm",
    roughness="Rough",
    thickness=0.05,
    conductivity=0.034,
    density=35.0,
    specific_heat=1400.0,
)
# --8<-- [end:add-object]


# --8<-- [start:lookup]
# By type → collection
zones = doc["Zone"]
print(len(zones))  # how many zones

# Iterate the collection
for zone in zones:
    print(zone.name, zone.x_origin)

# By name → individual object (O(1))
office = doc["Zone"]["Office"]

# Attribute access for common types
for material in doc.materials:
    print(material.conductivity)
# --8<-- [end:lookup]


# --8<-- [start:modify]
zone = doc["Zone"]["Office"]
zone.ceiling_height = 3.5  # plain field
zone.direction_of_relative_north = 90.0
# --8<-- [end:modify]


# --8<-- [start:rename]
doc.rename("Zone", "Office", "OpenPlanArea")
# every BuildingSurface:Detailed.zone_name pointing at "Office" is now "OpenPlanArea"
# --8<-- [end:rename]


# --8<-- [start:extensible]
surface = doc.add(
    "BuildingSurface:Detailed",
    "South Wall",
    surface_type="Wall",
    construction_name="ExtWall",
    zone_name="Office",
    outside_boundary_condition="Outdoors",
)
surface.vertices.append(vertex_x_coordinate=0.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
surface.vertices.append(vertex_x_coordinate=10.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
# ...
print(len(surface.vertices))  # 4
# --8<-- [end:extensible]


# --8<-- [start:iterate]
# Every type, in schema-defined order
for obj_type, collection in doc.objects_by_type():
    print(obj_type, len(collection))

# Every individual object
for obj in doc.all_objects:
    if obj.obj_type.startswith("Zone"):
        print(obj.name)
# --8<-- [end:iterate]


# --8<-- [start:mistake-extensible-good]
surface.vertices.append(vertex_x_coordinate=1.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
# --8<-- [end:mistake-extensible-good]


# --8<-- [start:mistake-rename-good]
doc.rename("Zone", "Office", "OpenPlanArea")  # or zone.name = "OpenPlanArea"
# --8<-- [end:mistake-rename-good]
