from __future__ import annotations

from datetime import datetime
from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
schedule: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.schedules import get_holidays, evaluate

# See what holidays are defined
holidays = get_holidays(doc, year=2024)
print(f"Holidays: {holidays}")

# Evaluation automatically uses holiday schedules on those dates
christmas = datetime(2024, 12, 25, 10, 0)
value = evaluate(schedule, christmas)
# --8<-- [end:example]
