from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(model, weather)

if not result.success:
    print(f"Exit code: {result.exit_code}")

    # Check errors
    if result.errors.has_fatal:
        for err in result.errors.fatal:
            print(f"Fatal: {err.message}")
# --8<-- [end:example]
