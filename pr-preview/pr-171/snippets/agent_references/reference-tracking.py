from __future__ import annotations

from idfkit import IDFCollection, IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
people: IDFObject = ...  # type: ignore[assignment]
surfaces: IDFCollection[IDFObject] = ...  # type: ignore[assignment]
referencing: list[IDFObject] = ...  # type: ignore[assignment]
target_name: str = ...  # type: ignore[assignment]
field: str = ...  # type: ignore[assignment]
target: str = ...  # type: ignore[assignment]
all_names: set[str] = ...  # type: ignore[assignment]
count: int = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
# Who points at this zone?
for obj in doc.get_referencing("Office"):
    print(obj.obj_type, obj.name)

# What does this People object reference?
people = doc["People"]["Office People"]
for target_name in doc.get_references(people):
    print(target_name)

# Rename — every reference updates automatically
doc["Zone"]["Office"].name = "Open_Office"
# or
doc.rename("Zone", "Office", "Open_Office")
# --8<-- [end:quickstart]


# --8<-- [start:find-referencing]
# Who points at "Office"?
referencing = doc.get_referencing("Office")
print(len(referencing))  # e.g. 8 (surfaces, people, lights, HVAC objects)

# With the originating field name
for obj, field in doc.references.get_referencing_with_fields("Office"):
    print(f"{obj.obj_type} '{obj.name}'.{field}")
# --8<-- [end:find-referencing]


# --8<-- [start:rename]
doc["Zone"]["Office"].name = "Open_Office"
# All fields across the document that pointed to "Office" now say "Open_Office":
#   BuildingSurface:Detailed.zone_name
#   People.zone_or_zonelist_or_space_or_spacelist_name
#   ZoneInfiltration:DesignFlowRate.zone_or_zonelist_or_space_or_spacelist_name
#   ...
# --8<-- [end:rename]


# --8<-- [start:find-references]
people = doc["People"]["Office People"]
for target_name in doc.get_references(people):
    print(target_name)
# 'Office'              (zone_or_zonelist_or_space_or_spacelist_name)
# 'Occupancy_Sched'     (number_of_people_schedule_name)
# 'Activity_Sched'      (activity_level_schedule_name)

# With field names
for field, target in doc.references.get_references_with_fields(people):
    print(field, "->", target)
# --8<-- [end:find-references]


# --8<-- [start:dangling]
all_names = {obj.name for obj in doc.all_objects if obj.name}
for obj, field, target in doc.references.get_dangling_references(all_names):
    print(f"{obj.obj_type} '{obj.name}'.{field} -> '{target}' (missing)")
# --8<-- [end:dangling]


# --8<-- [start:mistake-name-good]
zone.name = "Open_Office"
# --8<-- [end:mistake-name-good]


# --8<-- [start:mistake-field-good]
surfaces["South Wall"].zone_name = "Open_Office"  # graph updates
# --8<-- [end:mistake-field-good]


# --8<-- [start:mistake-count-good]
count = len(doc.get_referencing("Office"))  # O(1)
# --8<-- [end:mistake-count-good]
