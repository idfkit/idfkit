from __future__ import annotations

from idfkit.simulation import SimulationResult
from typing import Any

plt: Any = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Temperature
ts_temp = result.sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
axes[0].plot(ts_temp.timestamps, ts_temp.values)
axes[0].set_ylabel("Temperature (°C)")

# Humidity
ts_rh = result.sql.get_timeseries("Zone Air Relative Humidity", "ZONE 1")
axes[1].plot(ts_rh.timestamps, ts_rh.values)
axes[1].set_ylabel("Relative Humidity (%)")

plt.tight_layout()
plt.show()
# --8<-- [end:example]
