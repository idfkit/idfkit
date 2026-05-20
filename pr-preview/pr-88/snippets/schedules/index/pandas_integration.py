from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
schedule: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.schedules import to_series, plot_schedule

# Convert to pandas Series with datetime index
series = to_series(schedule, year=2024)
print(series.describe())

# Quick visualization
plot_schedule(schedule, year=2024)
# --8<-- [end:example]
