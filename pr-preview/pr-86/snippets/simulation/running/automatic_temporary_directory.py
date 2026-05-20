from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(model, weather)
print(result.run_dir)  # e.g., /tmp/idfkit_sim_abc123/
# --8<-- [end:example]
