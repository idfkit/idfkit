from __future__ import annotations

from idfkit import IDFDocument

model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import new_document

# Create an empty model for EnergyPlus 24.1
model = new_document(version=(24, 1, 0))

# Add named objects
model.add("Building", "My Building", north_axis=0, terrain="City")
model.add("Zone", "Office", x_origin=0, y_origin=0, z_origin=0)

# Add unnamed objects (name parameter is optional)
model.add("Timestep", number_of_timesteps_per_hour=4)
model.add(
    "GlobalGeometryRules",
    starting_vertex_position="UpperLeftCorner",
    vertex_entry_direction="Counterclockwise",
    coordinate_system="Relative",
)
# --8<-- [end:example]
