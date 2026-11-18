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
from idfkit import load_idf, new_document, save_idf

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
save_idf(doc, "out.idf")
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


# --8<-- [start:typed-collection-add]
# Through the collection: the parameters are the type's own, checked by the type checker, and the
# result is the type's class (Zone, Material, ...), not a plain IDFObject. Signature help shows the
# required fields with no default and the others with the schema's default.
office_zone = doc.zones.add("Office", x_origin=0.0, ceiling_height=3.0)
office_zone.multiplier = 2  # typed: an int, checked on assignment

insulation = doc["Material"].add(
    "XPS_25mm",
    roughness="Rough",
    thickness=0.025,
    conductivity=0.034,
    density=35.0,
    specific_heat=1400.0,
)
doc["Output:SQLite"].add(option_type="SimpleAndTabular")  # a type without a Name field: no name

# doc.zones.add("Lab", ceiling_hieght=3.0)                       # error: No parameter named "ceiling_hieght"
# doc.zones.add("Lab", zone_inside_convection_algorithm="Bogus")  # error: not one of the field's choices
# doc["Material"].add("XPS_50mm", thickness=0.05)                 # error: Arguments missing for parameters
#                                                                 #   "roughness", "conductivity", "density", ...
# doc["Output:SQLite"].add("Out", option_type="Simple")          # error: parameter "this_type_has_no_name_field"
# --8<-- [end:typed-collection-add]


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


# --8<-- [start:accessors]
# Any type in the schema is reachable as a typed attribute, not only common ones.
loops = doc.air_loop_hvacs  # IDFCollection[AirLoopHVAC]
coils = doc.coil_cooling_dx_single_speeds  # Coil:Cooling:DX:SingleSpeed
also_loops = doc["AirLoopHVAC"]  # equivalent
shades = doc.shading_building_detaileds  # Shading:Building:Detailed

# A typo names the closest matches and their object types:
#   >>> doc.shading_bulding
#   AttributeError: 'IDFDocument' object has no attribute 'shading_bulding'.
#   Did you mean:
#     shading_building   (Shading:Building:Detailed)
#     shading_buildings  (Shading:Building)
#     shading_fins       (Shading:Fin)
# --8<-- [end:accessors]


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


# --8<-- [start:versioned]
from idfkit import load_idf
from idfkit.document import AnyIDFDocument
from idfkit.versioned import IDFDocumentV9_4, as_version

legacy = as_version(load_idf("legacy.idf"), IDFDocumentV9_4)  # TypeError unless the file is 9.4
people = legacy["People"]["Office"]
people.update(zone_or_zonelist_name="Office")  # the 9.4 name; 9.6 renamed it, and the new name is an error here


def count_people(doc: AnyIDFDocument) -> int:
    """Accept a document of any supported release."""
    return len(doc["People"])


# --8<-- [end:versioned]


# --8<-- [start:versioned-read-write]
def use_natural_gas(doc: AnyIDFDocument) -> None:
    for heater in doc["WaterHeater:Mixed"]:
        fuel = heater.heater_fuel_type  # reads as str | None: any release's value can be in the file
        print(fuel)
        heater.heater_fuel_type = "NaturalGas"  # accepted: every release accepts it
        heater.update(heater_fuel_type="Electricity")  # update() is typed the same way
        # heater.heater_fuel_type = "DistrictHeatingWater"  # error: 9.3 to 23.1 reject it
        # heater.heater_fuel_type = "Steam"                 # error: 23.2 on rejects it


# --8<-- [end:versioned-read-write]


# --8<-- [start:versioned-range]
from typing import TypeVar

from idfkit.versioned import IDFDocumentSince26_1, IDFDocumentV26_1

# A function for 26.1 and later. IDFDocumentSince26_1 is IDFDocumentV26_1 | IDFDocumentV26_2, and
# grows when idfkit adds a release. The TypeVar hands the caller's own type back: a plain
# load_idf() result (IDFDocument, which is IDFDocumentV26_2) comes back as IDFDocument.
Since26_1 = TypeVar("Since26_1", bound=IDFDocumentSince26_1)


def use_district_steam(doc: Since26_1) -> Since26_1:
    for heater in doc["WaterHeater:Mixed"]:
        heater.heater_fuel_type = "DistrictHeatingSteam"  # both releases accept it
    return doc


latest = use_district_steam(load_idf("model.idf"))  # IDFDocument
older = use_district_steam(as_version(load_idf("older.idf"), IDFDocumentV26_1))  # IDFDocumentV26_1
# use_district_steam(legacy)  # error: a 9.4 document is not in the range
# --8<-- [end:versioned-range]


# --8<-- [start:versioned-exhaustive]
from typing_extensions import assert_never

from idfkit.versioned import IDFDocumentSince23_2


# Through this range heater_fuel_type reads as 12 known choices (or None), so the checker can
# prove every one is handled. Through AnyIDFDocument it reads as str | None (8.9 to 9.2 accept any
# string), and no match over it can be exhaustive.
def is_district_heated(doc: IDFDocumentSince23_2, heater_name: str) -> bool:
    fuel = doc["WaterHeater:Mixed"][heater_name].heater_fuel_type
    match fuel:
        case "DistrictHeatingWater" | "DistrictHeatingSteam":
            return True
        case (
            "Coal"
            | "Diesel"
            | "Electricity"
            | "FuelOilNo1"
            | "FuelOilNo2"
            | "Gasoline"
            | "NaturalGas"
            | "OtherFuel1"
            | "OtherFuel2"
            | "Propane"
            | None
        ):
            return False
        case _:
            assert_never(fuel)  # reported if a choice is left unhandled


# --8<-- [end:versioned-exhaustive]


# --8<-- [start:versioned-new-document]
from typing import Literal

from idfkit import new_document

blank_94 = new_document(IDFDocumentV9_4)  # version (9, 4, 0), typed IDFDocumentV9_4
blank_94["People"]  # 9.4's People, with zone_or_zonelist_name
lax_94 = new_document(IDFDocumentV9_4[Literal[False]])  # non-strict, typed IDFDocumentV9_4[Literal[False]]
# --8<-- [end:versioned-new-document]


# --8<-- [start:versioned-renamed-field]
def set_people_zone(doc: AnyIDFDocument, people: str, zone: str) -> None:
    """Set a People object's zone, whatever the model's release.

    The field was renamed in 9.6, so AnyIDFDocument offers neither name. Each branch narrows the
    model to the releases that use one name, and update() is checked against all of them. The
    ranges are the releases idfkit supports, so since="9.6" takes every later release as it is added.
    """
    if doc.version < (9, 6, 0):
        as_version(doc, before="9.6")["People"][people].update(zone_or_zonelist_name=zone)
    else:
        as_version(doc, since="9.6")["People"][people].update(zone_or_zonelist_or_space_or_spacelist_name=zone)


# --8<-- [end:versioned-renamed-field]


# --8<-- [start:versioned-containment]
def ensure_sqlite_output(doc: AnyIDFDocument) -> None:
    """Add Output:SQLite unless the model already holds one.

    "Output:SQLite" in doc asks whether the model holds such an object, so it is False for an
    empty model of any release, and the body below is type-checked.
    """
    if "Output:SQLite" not in doc:
        doc.add("Output:SQLite", option_type="SimpleAndTabular")


def set_ceiling_heights(doc: AnyIDFDocument, height: float) -> None:
    """Branch on the release, not on "Space" in doc, then narrow with as_version.

    Space arrived in 9.6 and its ceiling_height field in 22.2. since="22.2" is every release from
    22.2 on, and grows when idfkit adopts a new one; a hand-written tuple of release types would not.
    """
    if doc.version < (22, 2, 0):
        return
    for space in as_version(doc, since="22.2")["Space"]:
        space.ceiling_height = height


# --8<-- [end:versioned-containment]


# --8<-- [start:typed-object-parameter]
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # the classes exist only in the stubs; importing them at run time fails
    # From idfkit.document, not idfkit: recent pyright reports "not exported" for the latter.
    from idfkit.document import AnyBuildingSurfaceDetailed, AnyZone, Zone


def latest_ceiling(zone: Zone) -> float | None:
    """A latest-release Zone only: a 9.4 zone (Zone_v8_9_to_v9_4) is rejected."""
    height = zone.ceiling_height
    return height if isinstance(height, float) else None


def any_ceiling(zone: AnyZone) -> float | None:
    """A Zone of any release: the latest one, a 9.4 one, or one reached through AnyIDFDocument."""
    height = zone.ceiling_height
    return height if isinstance(height, float) else None


def vertex_count(surface: AnyBuildingSurfaceDetailed) -> int:
    """Extensible groups are typed too: vertices exist in every release."""
    return sum(1 for vertex in surface.vertices if vertex.vertex_x_coordinate is not None)


any_ceiling(doc["Zone"]["Office"])
any_ceiling(as_version(load_idf("legacy.idf"), IDFDocumentV9_4)["Zone"]["Office"])
# --8<-- [end:typed-object-parameter]


# --8<-- [start:read-required]
from idfkit.exceptions import MissingRequiredFieldError

if TYPE_CHECKING:
    from idfkit.document import AnyMaterial


def r_value(mat: AnyMaterial) -> float:
    """thickness and conductivity are required in every release: they read as float, no guard."""
    return mat.thickness / mat.conductivity


absorptance = doc.materials["Concrete"].thermal_absorptance  # float | None: it has a default
effective = absorptance if absorptance is not None else 0.9  # the value EnergyPlus applies

legacy = load_idf("hand_written.idf")  # a file EnergyPlus would refuse may lack a required field
for mat in legacy.materials:
    if mat.get("thickness") is None:  # the untyped check: None when unset, never raises
        print(f"{mat.name} has no thickness")
        continue
    print(r_value(mat))
try:
    print(legacy.materials["Brick"].thickness)
except MissingRequiredFieldError as err:  # an AttributeError naming the object and the field
    print(err.obj_type, err.obj_name, err.field_name)
# --8<-- [end:read-required]
