from __future__ import annotations

from idfkit.simulation import SimulationResult

result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import plot_energy_balance

fig = plot_energy_balance(
    result,
    title="Annual Energy Balance",
)
# --8<-- [end:example]
