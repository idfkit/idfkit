from __future__ import annotations

from idfkit import IDFObject

schedule: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.schedules import values

# Step function (default) - value changes at each Until time
step_values = values(schedule, timestep=4, interpolation="no")

# Linear interpolation between values
smooth_values = values(schedule, timestep=4, interpolation="average")
# --8<-- [end:example]
