from __future__ import annotations

from idfkit import IDFDocument, IDFObject, Polygon3D, Vector3D

doc: IDFDocument = ...  # type: ignore[assignment]
surface: IDFObject = ...  # type: ignore[assignment]
other: Vector3D = ...  # type: ignore[assignment]
new_poly: Polygon3D = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import (
    load_idf,
    calculate_surface_area,
    calculate_surface_azimuth,
    calculate_zone_volume,
    set_wwr,
    intersect_match,
    Vector3D,
    Polygon3D,
)

doc = load_idf("building.idf")

# Per-surface
for surface in doc["BuildingSurface:Detailed"]:
    print(surface.name, calculate_surface_area(surface), calculate_surface_azimuth(surface))

# Per-zone
print(calculate_zone_volume(doc, "Office"))

# Bulk
set_wwr(doc, wwr=0.4, orientation="South")
intersect_match(doc)
# --8<-- [end:quickstart]


# --8<-- [start:vector3d]
v = Vector3D(1.0, 0.0, 0.0)
v.x, v.y, v.z
v + Vector3D(0, 1, 0)  # vector addition
v - Vector3D(0, 1, 0)
v.dot(other)
v.cross(other)
v.length()
v.normalize()
v.rotate_z(angle_deg=45)  # rotate about Z (vertical), degrees
# --8<-- [end:vector3d]


# --8<-- [start:polygon3d]
poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(10, 0, 0), Vector3D(10, 5, 0), Vector3D(0, 5, 0)])
poly.area  # 50.0
poly.centroid  # Vector3D
poly.normal  # outward normal as Vector3D
poly.azimuth  # 0-360, degrees clockwise from North
poly.tilt  # 0-180, degrees from horizontal
# --8<-- [end:polygon3d]


# --8<-- [start:surface-calculations]
from idfkit import (
    calculate_surface_area,
    calculate_surface_azimuth,
    calculate_surface_tilt,
)

surface = doc["BuildingSurface:Detailed"]["South Wall"]
calculate_surface_area(surface)  # m²
calculate_surface_azimuth(surface)  # 180 for a south wall (relative to North)
calculate_surface_tilt(surface)  # 90 for a vertical wall, 0 for a roof
# --8<-- [end:surface-calculations]


# --8<-- [start:surface-coords]
from idfkit.geometry import get_surface_coords, set_surface_coords

poly = get_surface_coords(surface)  # Polygon3D | None
set_surface_coords(surface, new_poly)  # writes vertices back, normal recomputed
# --8<-- [end:surface-coords]


# --8<-- [start:zone-calculations]
from idfkit import (
    calculate_zone_floor_area,
    calculate_zone_ceiling_area,
    calculate_zone_height,
    calculate_zone_volume,
)

zone_name = "Office"
calculate_zone_floor_area(doc, zone_name)
calculate_zone_ceiling_area(doc, zone_name)
calculate_zone_height(doc, zone_name)
calculate_zone_volume(doc, zone_name)
# --8<-- [end:zone-calculations]


# --8<-- [start:transforms]
from idfkit import translate_building, rotate_building, Vector3D

translate_building(doc, Vector3D(10.0, 5.0, 0.0))  # shift all vertices
rotate_building(doc, angle_deg=15.0)  # rotate about Z, anchor=origin
rotate_building(doc, angle_deg=15.0, anchor=Vector3D(50, 50, 0))
# --8<-- [end:transforms]


# --8<-- [start:wwr]
from idfkit import set_wwr

set_wwr(doc, wwr=0.4)  # all exterior walls
set_wwr(doc, wwr=0.4, orientation="South")  # only south walls
# Per-orientation ratios: call once per orientation.
for orientation, ratio in [("North", 0.3), ("South", 0.5), ("East", 0.4), ("West", 0.4)]:
    set_wwr(doc, wwr=ratio, orientation=orientation)
# --8<-- [end:wwr]


# --8<-- [start:intersect-match]
from idfkit import intersect_match

intersect_match(doc)  # mutates surfaces in place
# Every shared interior wall now has its boundary linked to the matching surface in the neighbour zone.
# --8<-- [end:intersect-match]


# --8<-- [start:polygon-2d]
from idfkit import (
    polygon_area_2d,
    polygon_contains_2d,
    polygon_intersection_2d,
    polygon_difference_2d,
)

a = [(0, 0), (10, 0), (10, 5), (0, 5)]
b = [(5, 0), (15, 0), (15, 5), (5, 5)]
inner = [(1, 1), (4, 1), (4, 4), (1, 4)]

polygon_area_2d(a)  # 50.0
polygon_contains_2d(a, inner)  # True (every vertex of inner is inside a)
polygon_intersection_2d(a, b)  # overlapping rectangle
polygon_difference_2d(a, b)  # a minus b
# --8<-- [end:polygon-2d]


# --8<-- [start:mistake-area-good]
calculate_surface_area(surface)
# --8<-- [end:mistake-area-good]


# --8<-- [start:mistake-rotate-good]
rotate_building(doc, angle_deg=90.0)  # rotates all vertices and zone origins
# --8<-- [end:mistake-rotate-good]


# --8<-- [start:mistake-wwr-good]
for orientation, ratio in [("North", 0.3), ("South", 0.5), ("East", 0.4), ("West", 0.4)]:
    set_wwr(doc, wwr=ratio, orientation=orientation)
# --8<-- [end:mistake-wwr-good]
