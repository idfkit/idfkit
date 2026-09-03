from __future__ import annotations

from idfkit.simulation import SQLResult

sql: SQLResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import plot_temperature_profile

# `sql` is result.sql from a completed simulation
fig = plot_temperature_profile(
    sql,
    ["THERMAL ZONE 1", "THERMAL ZONE 2"],
    title="Zone Temperatures",
)
# --8<-- [end:example]
