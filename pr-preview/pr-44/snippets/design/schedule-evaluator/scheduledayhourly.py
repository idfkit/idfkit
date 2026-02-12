from __future__ import annotations

from datetime import datetime
from idfkit import IDFObject
from typing import Any

dt: Any = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]


# --8<-- [start:example]
def evaluate_day_hourly(obj: IDFObject, dt: datetime) -> float:
    hour = dt.hour  # 0-23
    field_name = f"Hour {hour + 1}"  # "Hour 1" through "Hour 24"
    return float(obj[field_name])


# --8<-- [end:example]
