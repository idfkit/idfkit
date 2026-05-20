from __future__ import annotations

from datetime import datetime
from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
schedule: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.schedules import evaluate

# Summer design day (typically peak cooling)
value = evaluate(
    schedule,
    datetime(2024, 7, 15, 14, 0),
    day_type="summer",
)

# Winter design day (typically peak heating)
value = evaluate(
    schedule,
    datetime(2024, 1, 15, 6, 0),
    day_type="winter",
)
# --8<-- [end:example]
