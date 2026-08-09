from __future__ import annotations

from idfkit.simulation import S3FileSystem, SimulationResult

result: SimulationResult = ...  # type: ignore[assignment]
s3_fs: S3FileSystem = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = SimulationResult.from_directory("run-001", fs=s3_fs)

# Nothing downloaded yet
# ...

# Downloads only the SQLite file
ts = result.sql.get_timeseries(...)
# --8<-- [end:example]
