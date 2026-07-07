from __future__ import annotations

from idfkit.simulation import S3FileSystem, SimulationResult, TimeSeriesResult

fs: S3FileSystem = ...  # type: ignore[assignment]
num_cases: int = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
results: list[SimulationResult | None] = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import SimulationResult, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

# Reconstruct results
results = []
for i in range(num_cases):
    result = SimulationResult.from_directory(f"case-{i:04d}", fs=fs)
    results.append(result)

# Analyze
for i, result in enumerate(results):
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        "ZONE 1",
    )
    print(f"Case {i}: max temp = {max(ts.values):.1f}°C")
# --8<-- [end:example]
