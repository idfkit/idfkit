"""Simulation progress tracking.

Provides a dataclass for progress events and a parser that extracts
structured progress information from EnergyPlus stdout output.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..document import AnyIDFDocument

__all__ = [
    "ProgressParser",
    "SimulationProgress",
]


@dataclass(frozen=True, slots=True)
class SimulationProgress:
    """Progress event emitted during a single EnergyPlus simulation.

    This dataclass represents a progress update parsed from EnergyPlus
    stdout output.  It is passed to user-supplied ``on_progress`` callbacks
    on [simulate][idfkit.simulation.runner.simulate] and
    [async_simulate][idfkit.simulation.async_runner.async_simulate].

    Attributes:
        phase: Current simulation phase.
        message: Raw EnergyPlus stdout line (stripped).
        percent: Estimated completion percentage (0.0-100.0), or ``None``
            when progress is indeterminate (e.g. during warmup).
        environment: Name of the current simulation environment, if known.
        warmup_day: Current warmup iteration (1-based), only set during
            the ``"warmup"`` phase.
        sim_day: Current simulation day-of-year (1-based), only set during
            the ``"simulating"`` phase.
        sim_total_days: Total number of simulation days, only set when the
            simulation period is known.
        job_index: Index of this job in a batch, or ``None`` for single
            simulations.
        job_label: Label of this job in a batch, or ``None`` for single
            simulations.
    """

    phase: Literal["preprocessing", "initializing", "warmup", "simulating", "postprocessing", "complete"]
    message: str
    percent: float | None = None
    environment: str | None = None
    warmup_day: int | None = None
    sim_day: int | None = None
    sim_total_days: int | None = None
    job_index: int | None = None
    job_label: str | None = None


class ProgressParser:
    """Parse EnergyPlus stdout lines into [SimulationProgress][idfkit.simulation.progress.SimulationProgress] events.

    Maintains internal state to track the current environment, warmup
    iteration count, and simulation day for percentage estimation.

    Recent EnergyPlus releases (26.1, for one) print ``Starting Simulation at
    01/01/2013 for RUN PERIOD 1`` without the period's end date, so the parser cannot learn
    the length of the period from stdout alone.  Pass *environment_days*
    (see [environment_days][idfkit.simulation.progress.environment_days]) so it
    can still report ``percent`` and ``sim_total_days``.  EnergyPlus prints
    ``EnergyPlus Completed Successfully`` to stderr: feed stderr lines to
    [parse_line][idfkit.simulation.progress.ProgressParser.parse_line] too to
    get the ``"complete"`` event, which is emitted at most once.

    A new instance should be created for each simulation run.  The parser
    is designed to be defensive — unrecognised lines return ``None`` and
    never raise.

    Examples:
        ```python
        parser = ProgressParser()
        for line in energyplus_stdout_lines:
            event = parser.parse_line(line)
            if event is not None:
                print(event.phase, event.percent)
        ```
    """

    _RE_WARMUP = re.compile(r"Warming up \{(\d+)\}")
    _RE_START_SIM = re.compile(
        r"Starting Simulation at (\d{2}/\d{2}(?:/\d{4})?) for (.+?)(?:\s+from (\d{2}/\d{2}(?:/\d{4})?) to (\d{2}/\d{2}(?:/\d{4})?))?$"
    )
    _RE_CONTINUE_SIM = re.compile(r"Continuing Simulation at (\d{2}/\d{2}(?:/\d{4})?) for (.+)")
    _RE_COMPLETED = re.compile(r"EnergyPlus Completed Successfully")
    _RE_INITIALIZING = re.compile(r"Initializing New Environment Parameters")
    _RE_WARMUP_COMPLETE = re.compile(r"Warmup Complete")
    _RE_WRITING_TABULAR = re.compile(r"Writing tabular output")
    _RE_WRITING_SQL = re.compile(r"Writing final SQL")

    def __init__(self, environment_days: Mapping[str, int] | None = None) -> None:
        """Create a parser.

        Args:
            environment_days: Length in days of each simulation environment,
                keyed by environment name (case and repeated spaces are
                ignored).  Used when EnergyPlus does not print the period's
                date range.
        """
        self._environment_days = {_env_key(k): v for k, v in (environment_days or {}).items()}
        self._completed = False
        self._environment: str | None = None
        self._warmup_day: int = 0
        self._sim_start_day: int | None = None
        self._sim_total_days: int | None = None
        self._job_index: int | None = None
        self._job_label: str | None = None

    def set_job_context(self, index: int, label: str) -> None:
        """Set batch job context that will be included in all emitted events.

        Args:
            index: Job index within the batch.
            label: Human-readable job label.
        """
        self._job_index = index
        self._job_label = label

    def parse_line(self, line: str) -> SimulationProgress | None:
        """Parse a single stdout line into a progress event.

        Args:
            line: A single line from EnergyPlus stdout.

        Returns:
            A [SimulationProgress][idfkit.simulation.progress.SimulationProgress] event, or ``None`` if the line
            does not contain progress information.
        """
        stripped = line.strip()
        if not stripped:
            return None

        m = self._RE_WARMUP.search(stripped)
        if m:
            self._warmup_day = int(m.group(1))
            return self._event("warmup", stripped, warmup_day=self._warmup_day)

        m = self._RE_INITIALIZING.search(stripped)
        if m:
            self._warmup_day = 0
            self._sim_start_day = None
            self._sim_total_days = None
            return self._event("initializing", stripped)

        m = self._RE_START_SIM.search(stripped)
        if m:
            date_str = m.group(1)
            environment = m.group(2).strip()
            self._environment = environment
            from_date = m.group(3) if m.lastindex and m.lastindex >= 3 else None
            to_date = m.group(4) if m.lastindex and m.lastindex >= 4 else None

            self._sim_start_day = _date_to_day_of_year(date_str)
            if from_date and to_date:
                start_d = _date_to_day_of_year(from_date)
                end_d = _date_to_day_of_year(to_date)
                self._sim_total_days = _day_span(start_d, end_d)
            else:
                self._sim_total_days = self._environment_days.get(_env_key(environment))

            current_day = self._sim_start_day
            percent = self._estimate_percent(current_day)
            return self._event(
                "simulating",
                stripped,
                percent=percent,
                environment=self._environment,
                sim_day=current_day,
                sim_total_days=self._sim_total_days,
            )

        m = self._RE_CONTINUE_SIM.search(stripped)
        if m:
            date_str = m.group(1)
            self._environment = m.group(2).strip()
            current_day = _date_to_day_of_year(date_str)
            percent = self._estimate_percent(current_day)
            return self._event(
                "simulating",
                stripped,
                percent=percent,
                environment=self._environment,
                sim_day=current_day,
                sim_total_days=self._sim_total_days,
            )

        m = self._RE_WARMUP_COMPLETE.search(stripped)
        if m:
            return self._event("warmup", stripped, warmup_day=self._warmup_day)

        if self._RE_WRITING_TABULAR.search(stripped) or self._RE_WRITING_SQL.search(stripped):
            return self._event("postprocessing", stripped)

        m = self._RE_COMPLETED.search(stripped)
        if m and not self._completed:
            self._completed = True
            return self._event("complete", stripped, percent=100.0)

        return None

    def _estimate_percent(self, current_day: int | None) -> float | None:
        """Estimate simulation percentage from the current day of year."""
        if current_day is None or self._sim_total_days is None or self._sim_start_day is None:
            return None
        if self._sim_total_days <= 0:
            return None

        elapsed = current_day - self._sim_start_day
        if elapsed < 0:
            # Wrap around year boundary
            elapsed += 365

        pct = (elapsed / self._sim_total_days) * 100.0
        return min(pct, 100.0)

    def _event(
        self,
        phase: Literal["preprocessing", "initializing", "warmup", "simulating", "postprocessing", "complete"],
        message: str,
        *,
        percent: float | None = None,
        environment: str | None = None,
        warmup_day: int | None = None,
        sim_day: int | None = None,
        sim_total_days: int | None = None,
    ) -> SimulationProgress:
        return SimulationProgress(
            phase=phase,
            message=message,
            percent=percent,
            environment=environment if environment is not None else self._environment,
            warmup_day=warmup_day,
            sim_day=sim_day,
            sim_total_days=sim_total_days,
            job_index=self._job_index,
            job_label=self._job_label,
        )


def _env_key(name: str) -> str:
    """Normalise an environment name the way EnergyPlus prints it: upper case, single spaces."""
    return " ".join(name.split()).upper()


def _int_field(obj: object, field: str) -> int | None:
    value = getattr(obj, field, None)
    if isinstance(value, bool) or value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def environment_days(model: AnyIDFDocument) -> dict[str, int]:
    """Return the length in days of each simulation environment *model* defines.

    Covers ``RunPeriod`` (from its begin and end month/day, ignoring years),
    ``SizingPeriod:DesignDay`` (one day each) and
    ``SizingPeriod:WeatherFileDays``.  The result is meant for
    [ProgressParser][idfkit.simulation.progress.ProgressParser], which
    [simulate][idfkit.simulation.runner.simulate] builds with it so progress
    events carry ``percent`` on EnergyPlus versions that do not print the
    period's date range.

    Args:
        model: The model about to be simulated.

    Returns:
        Days per environment name, in upper case with single spaces, as
        EnergyPlus prints it.
    """
    days: dict[str, int] = {}
    for obj_type in ("RunPeriod", "SizingPeriod:WeatherFileDays"):
        if obj_type not in model:
            continue
        for index, obj in enumerate(model[obj_type]):
            bm, bd = _int_field(obj, "begin_month"), _int_field(obj, "begin_day_of_month")
            em, ed = _int_field(obj, "end_month"), _int_field(obj, "end_day_of_month")
            if bm is None or bd is None or em is None or ed is None:
                continue
            span = _day_span(_date_to_day_of_year(f"{bm:02d}/{bd:02d}"), _date_to_day_of_year(f"{em:02d}/{ed:02d}"))
            name = getattr(obj, "name", None)
            if isinstance(name, str) and name.strip():
                days[_env_key(name)] = span
            elif obj_type == "RunPeriod":
                # EnergyPlus reports an unnamed run period as ``RUN PERIOD <n>``.
                days[f"RUN PERIOD {index + 1}"] = span
    if "SizingPeriod:DesignDay" in model:
        for obj in model["SizingPeriod:DesignDay"]:
            name = getattr(obj, "name", None)
            if isinstance(name, str) and name.strip():
                days[_env_key(name)] = 1
    return days


def _date_to_day_of_year(date_str: str) -> int:
    """Convert ``MM/DD`` or ``MM/DD/YYYY`` to a 1-based day of year.

    Uses a non-leap-year calendar (365 days). Returns 1 on parse failure.
    """
    parts = date_str.split("/")
    if len(parts) < 2:
        return 1
    try:
        month = int(parts[0])
        day = int(parts[1])
    except ValueError:
        return 1

    # Days in each month (non-leap year)
    days_before_month = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
    if 1 <= month <= 12 and 1 <= day <= 31:
        return days_before_month[month - 1] + day
    return 1


def _day_span(start: int, end: int) -> int:
    """Compute the number of days between two day-of-year values.

    Handles wrap-around (e.g. start=350, end=30 → 45 days).
    """
    if end >= start:
        return end - start + 1
    return (365 - start) + end + 1
