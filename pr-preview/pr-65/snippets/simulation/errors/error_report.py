from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import ErrorReport, SimulationResult

errors: ErrorReport = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate

result = simulate(model, weather)

# Access the error report
errors = result.errors

# Check for problems
if errors.has_fatal:
    print("Simulation had fatal errors")
if errors.has_severe:
    print("Simulation had severe errors")
if errors.warning_count > 0:
    print(f"Simulation had {errors.warning_count} warnings")
# --8<-- [end:example]
