from __future__ import annotations

from idfkit.simulation import SQLResult

sql: SQLResult | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
with SQLResult("/path/to/eplusout.sql") as sql:
    ts = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
    # Connection automatically closed on exit
# --8<-- [end:example]
