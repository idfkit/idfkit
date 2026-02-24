from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import new_document

# Create a baseline model for EnergyPlus 24.1
model = new_document(version=(24, 1, 0))

# Update pre-seeded singleton objects
building = model["Building"].first()
if building is not None:
    building.name = "My Building"
    building.north_axis = 0
    building.terrain = "City"

geometry_rules = model["GlobalGeometryRules"].first()
if geometry_rules is not None:
    geometry_rules.starting_vertex_position = "UpperLeftCorner"
    geometry_rules.vertex_entry_direction = "Counterclockwise"
    geometry_rules.coordinate_system = "Relative"

# Add additional named objects
model.add("Zone", "Office", x_origin=0, y_origin=0, z_origin=0)

# Add an additional unnamed singleton object
model.add("Timestep", number_of_timesteps_per_hour=4)
# --8<-- [end:example]
