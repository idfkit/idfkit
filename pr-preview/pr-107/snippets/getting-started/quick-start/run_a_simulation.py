from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate

result = simulate(
    model,
    weather="weather.epw",
    design_day=True,  # Fast design-day run
)

print(f"Success: {result.success}")
print(f"Runtime: {result.runtime_seconds:.1f}s")

# Check for errors
if result.errors.has_fatal:
    for err in result.errors.fatal:
        print(f"Error: {err.message}")
# --8<-- [end:example]
