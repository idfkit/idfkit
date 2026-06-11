from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
schedule: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.schedules import values

# 15-minute intervals (4 per hour)
quarter_hourly = values(schedule, year=2024, timestep=4)
print(f"Values: {len(quarter_hourly)}")  # 35136 for leap year

# 1-minute intervals
minute_values = values(schedule, year=2024, timestep=60)
# --8<-- [end:example]
