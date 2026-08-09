from __future__ import annotations

from datetime import datetime
from idfkit import IDFObject
from typing import Any

dt: Any = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
parse_time: Any = ...  # type: ignore[assignment]


# --8<-- [start:example]
def evaluate_day_interval(obj: IDFObject, dt: datetime) -> float:
    # Fields: Time 1, Value Until Time 1, Time 2, Value Until Time 2, ...
    current_time = dt.time()
    last_value = 0.0

    for i in range(1, 145):  # Max 144 intervals
        time_field = f"Time {i}"
        value_field = f"Value Until Time {i}"
        if not obj.get(time_field):
            break
        until_time = parse_time(obj[time_field])  # "HH:MM"
        if current_time < until_time:
            return float(obj[value_field])
        last_value = float(obj[value_field])

    return last_value


# --8<-- [end:example]
