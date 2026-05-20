from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Quick validation
result = simulate(model, weather, design_day=True)
if result.success:
    # Then run full annual
    result = simulate(model, weather, annual=True)
# --8<-- [end:example]
