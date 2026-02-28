from __future__ import annotations

from idfkit.simulation import SimulationResult, TimeSeriesResult

result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
zone_names: list[str] = ...  # type: ignore[assignment]
# --8<-- [start:example]
import matplotlib.pyplot as plt

# Create custom figure
fig, ax = plt.subplots(figsize=(12, 6))

# Plot multiple series
for zone_name in zone_names:
    ts = result.sql.get_timeseries(
        "Zone Mean Air Temperature",
        zone_name,
    )
    ax.plot(ts.timestamps, ts.values, label=zone_name)

ax.legend()
ax.set_xlabel("Time")
ax.set_ylabel("Temperature (°C)")
plt.show()
# --8<-- [end:example]
