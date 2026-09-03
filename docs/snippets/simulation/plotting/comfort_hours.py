from __future__ import annotations

from idfkit.simulation import SQLResult

sql: SQLResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import plot_comfort_hours

# `sql` is result.sql from a completed simulation
fig = plot_comfort_hours(
    sql,
    ["THERMAL ZONE 1"],
    title="Thermal Comfort Analysis",
)
# --8<-- [end:example]
