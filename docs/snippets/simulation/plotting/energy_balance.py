from __future__ import annotations

from idfkit.simulation import SQLResult

sql: SQLResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import plot_energy_balance

# `sql` is result.sql from a completed simulation
fig = plot_energy_balance(
    sql,
    title="Annual Energy Balance",
)
# --8<-- [end:example]
