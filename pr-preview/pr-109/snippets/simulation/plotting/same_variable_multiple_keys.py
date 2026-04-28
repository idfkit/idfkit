from __future__ import annotations

from idfkit.simulation import SimulationResult, TimeSeriesResult

result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for zone_name in ["ZONE 1", "ZONE 2", "ZONE 3"]:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone_name,
    )
    ax.plot(ts.timestamps, ts.values, label=zone_name)

ax.legend()
plt.show()
# --8<-- [end:example]
