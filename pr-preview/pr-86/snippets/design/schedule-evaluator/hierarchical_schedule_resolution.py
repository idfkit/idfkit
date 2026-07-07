from __future__ import annotations

from datetime import datetime
from idfkit import IDFDocument, IDFObject
from typing import Any

day_schedule_type: Any = ...  # type: ignore[assignment]
doc: IDFDocument = ...  # type: ignore[assignment]
dt: Any = ...  # type: ignore[assignment]
evaluate_day: Any = ...  # type: ignore[assignment]
evaluate_week: Any = ...  # type: ignore[assignment]
field_name_for_index: Any = ...  # type: ignore[assignment]
find_week_for_date: Any = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
week_type: Any = ...  # type: ignore[assignment]


# --8<-- [start:example]
def evaluate_year(obj: IDFObject, dt: datetime, doc: IDFDocument) -> float:
    # 1. Find which date range contains dt
    # 2. Get the referenced week schedule name
    # 3. Look up week schedule in document
    # 4. Evaluate week schedule for dt
    week_name = find_week_for_date(obj, dt)
    week_obj = doc.get_schedule(week_name) or doc[week_type][week_name]
    return evaluate_week(week_obj, dt, doc)


def evaluate_week_daily(obj: IDFObject, dt: datetime, doc: IDFDocument) -> float:
    # Schedule:Week:Daily has 12 fields: Sunday-Saturday + Holiday + Summer/Winter DD + Custom
    day_index = dt.weekday()  # 0=Mon, need to map to E+ order (Sun=0)
    field_map = {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}  # Python weekday → E+ field
    day_name = obj[field_name_for_index(field_map[day_index])]
    day_obj = doc[day_schedule_type][day_name]
    return evaluate_day(day_obj, dt, doc)


# --8<-- [end:example]
