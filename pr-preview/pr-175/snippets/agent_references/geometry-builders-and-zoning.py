from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
surface: IDFObject = ...  # type: ignore[assignment]
rect: list[tuple[float, float]] = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import new_document, write_idf, ZoningScheme, create_block, footprint_rectangle

doc = new_document()
create_block(
    doc,
    name="Office",
    footprint=footprint_rectangle(width=50.0, depth=30.0),
    floor_to_floor=3.5,
    num_stories=3,
    zoning=ZoningScheme.CORE_PERIMETER,
)
write_idf(doc, "block.idf")
# --8<-- [end:quickstart]


# --8<-- [start:footprints]
from idfkit import (
    footprint_rectangle,
    footprint_l_shape,
    footprint_u_shape,
    footprint_courtyard,
)

rect = footprint_rectangle(width=50, depth=30)
ell = footprint_l_shape(width=40, depth=20, wing_width=20, wing_depth=15)
u = footprint_u_shape(width=40, depth=30, courtyard_width=15, courtyard_depth=10)
courtyard = footprint_courtyard(outer_width=40, outer_depth=30, inner_width=15, inner_depth=10)
# --8<-- [end:footprints]


# --8<-- [start:zoning-schemes]
from idfkit import ZoningScheme, ZoneFootprint

create_block(doc, "Office", rect, floor_to_floor=3.5, num_stories=3, zoning=ZoningScheme.BY_STOREY)

create_block(
    doc, "Office", rect, floor_to_floor=3.5, num_stories=3, zoning=ZoningScheme.CORE_PERIMETER, perimeter_depth=4.0
)

create_block(
    doc,
    "Office",
    rect,
    floor_to_floor=3.5,
    num_stories=3,
    zoning=ZoningScheme.CUSTOM,
    custom_zones=[
        ZoneFootprint(name_suffix="MeetingRoom", polygon=[(0, 0), (10, 0), (10, 10), (0, 10)]),
        ZoneFootprint(
            name_suffix="OpenPlan", polygon=[(10, 0), (50, 0), (50, 30), (10, 30), (10, 10), (0, 10), (0, 0)]
        ),
    ],
)
# --8<-- [end:zoning-schemes]


# --8<-- [start:multi-block]
from idfkit import create_block, link_blocks, footprint_rectangle, ZoningScheme

create_block(
    doc, "Base", footprint_rectangle(50, 30), floor_to_floor=3.5, num_stories=3, zoning=ZoningScheme.CORE_PERIMETER
)
create_block(
    doc,
    "Tower",
    footprint_rectangle(30, 20, origin=(10, 5)),
    floor_to_floor=3.5,
    num_stories=8,
    base_elevation=3.5 * 3,
    zoning=ZoningScheme.CORE_PERIMETER,
)

link_blocks(doc)  # auto-detect and link all stacked blocks
# or
link_blocks(doc, lower="Base", upper="Tower")  # link a specific pair
# --8<-- [end:multi-block]


# --8<-- [start:shading]
from idfkit import add_shading_block, footprint_rectangle

add_shading_block(
    doc,
    name="ParkingGarage",
    footprint=footprint_rectangle(40, 20, origin=(60, 0)),
    height=12.0,
)
# --8<-- [end:shading]


# --8<-- [start:building-edits]
from idfkit import bounding_box, scale_building, set_default_constructions

# Inspect — returns None if the model has no surfaces
bb = bounding_box(doc)
if bb is not None:
    (xmin, ymin), (xmax, ymax) = bb

# Scale all surfaces uniformly (e.g. for unit conversion or sensitivity studies)
scale_building(doc, factor=1.1)  # 10% larger

# Quickly assign a default construction to surfaces that lack one
set_default_constructions(doc, construction_name="Default Construction")
# --8<-- [end:building-edits]


# --8<-- [start:horizontal-adjacencies]
from idfkit import detect_horizontal_adjacencies, link_horizontal_surfaces

adjacencies = detect_horizontal_adjacencies(doc)
for adj in adjacencies:
    link_horizontal_surfaces(adj.roof_surface, adj.floor_surface)
# --8<-- [end:horizontal-adjacencies]


# --8<-- [start:split-surface]
from idfkit.geometry_builders import split_horizontal_surface

new_a, new_b = split_horizontal_surface(
    doc,
    surface,
    region=[(10, 0), (20, 0), (20, 10), (10, 10)],
)
# --8<-- [end:split-surface]


# --8<-- [start:mistake-ccw-good]
ccw_rect = footprint_rectangle(50, 30)  # CCW by construction
# --8<-- [end:mistake-ccw-good]


# --8<-- [start:mistake-hvac-good]
create_block(doc, "Office", footprint_rectangle(50, 30), floor_to_floor=3.5, num_stories=3)
for zone in doc["Zone"]:
    doc.add("HVACTemplate:Zone:IdealLoadsAirSystem", zone_name=zone.name, template_thermostat_name="OfficeThermostat")
# --8<-- [end:mistake-hvac-good]


# --8<-- [start:mistake-link-good]
link_blocks(doc)
# --8<-- [end:mistake-link-good]
