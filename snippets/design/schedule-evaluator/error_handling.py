from __future__ import annotations


# --8<-- [start:example]
class ScheduleEvaluationError(Exception):
    """Raised when schedule cannot be evaluated."""

    pass


class UnsupportedScheduleType(ScheduleEvaluationError):
    """Schedule type not yet implemented."""

    pass


class ScheduleReferenceError(ScheduleEvaluationError):
    """Referenced schedule not found in document."""

    pass


class MalformedScheduleError(ScheduleEvaluationError):
    """Schedule syntax is invalid."""

    pass


# --8<-- [end:example]
