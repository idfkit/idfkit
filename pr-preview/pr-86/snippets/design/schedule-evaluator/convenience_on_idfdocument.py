from __future__ import annotations

from datetime import datetime
from idfkit.schedules import DayType, Interpolation


# --8<-- [start:example]
class IDFDocument:
    def evaluate_schedule(
        self,
        name: str,
        dt: datetime,
        day_type: DayType = DayType.NORMAL,
    ) -> float:
        """Shorthand for evaluate(self.get_schedule(name), dt, self)"""

    def schedule_values(
        self,
        name: str,
        year: int = 2024,
        timestep: int = 1,
        day_type: DayType = DayType.NORMAL,
        interpolation: Interpolation = Interpolation.NO,
    ) -> list[float]:
        """Shorthand for values(self.get_schedule(name), ...)"""


# --8<-- [end:example]
