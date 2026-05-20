from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, TimeSeriesResult

doc: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate

result = simulate(doc, "weather.epw", design_day=True)

# Query results
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",
)
print(f"Max temp: {max(ts.values):.1f}")
# --8<-- [end:example]
