from __future__ import annotations

from idfkit.simulation import ErrorReport, SimulationResult

errors: ErrorReport = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
if not result.success:
    print(errors.summary())
    for err in errors.fatal + errors.severe:
        print(err.message)
# --8<-- [end:example]
