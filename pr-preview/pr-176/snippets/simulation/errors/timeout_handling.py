from __future__ import annotations

from idfkit import IDFDocument, SimulationError
from idfkit.simulation import simulate

model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
try:
    result = simulate(model, weather, timeout=60.0)
except SimulationError as e:
    if e.exit_code is None:
        print("Simulation timed out")
    else:
        print(f"Simulation failed with exit code {e.exit_code}")
# --8<-- [end:example]
