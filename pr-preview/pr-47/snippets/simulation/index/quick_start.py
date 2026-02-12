from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, TimeSeriesResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf
from idfkit.simulation import simulate

# Load a model and run a simulation
model = load_idf("building.idf")
result = simulate(model, "weather.epw", design_day=True)

# Check results
print(f"Success: {result.success}")
print(f"Runtime: {result.runtime_seconds:.1f}s")

# Query time-series data
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="THERMAL ZONE 1",
)
print(f"Max temp: {max(ts.values):.1f}°C")
# --8<-- [end:example]
