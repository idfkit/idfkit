from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import simulate

model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.exceptions import SimulationError

try:
    result = simulate(model, weather)
except SimulationError as e:
    print(f"Simulation failed: {e}")
    print(f"Exit code: {e.exit_code}")
    print(f"Stderr: {e.stderr}")
# --8<-- [end:example]
