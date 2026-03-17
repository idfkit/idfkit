from __future__ import annotations

from idfkit.simulation import SimulationResult

result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import plot_comfort_hours

fig = plot_comfort_hours(
    result,
    zone_name="THERMAL ZONE 1",
    title="Thermal Comfort Analysis",
)
# --8<-- [end:example]
