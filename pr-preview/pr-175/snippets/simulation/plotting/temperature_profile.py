from __future__ import annotations

from idfkit.simulation import SimulationResult

result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import plot_temperature_profile

fig = plot_temperature_profile(
    result,
    zone_name="THERMAL ZONE 1",
    title="Zone Temperatures",
)
# --8<-- [end:example]
