from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import load_idf
from idfkit.simulation import simulate

# Forward-migrate the model transparently before running.
model = load_idf("old_building.idf")
result = simulate(model, "weather.epw", design_day=True, auto_migrate=True)

if result.migration_report is not None:
    print(result.migration_report.summary())

print(f"Simulation success: {result.success}")
# --8<-- [end:example]
