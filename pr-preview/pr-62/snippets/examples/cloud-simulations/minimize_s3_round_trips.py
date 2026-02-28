from __future__ import annotations

from idfkit.simulation import S3FileSystem, SQLResult, SimulationResult

fs: S3FileSystem = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
sql: SQLResult | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Query results once, process locally
result = SimulationResult.from_directory("run-001", fs=fs)

# This downloads the SQL file
sql = result.sql

# Multiple queries are local (file is cached)
ts1 = sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
ts2 = sql.get_timeseries("Zone Air Relative Humidity", "ZONE 1")
# --8<-- [end:example]
