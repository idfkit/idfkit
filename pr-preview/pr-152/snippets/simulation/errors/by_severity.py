from __future__ import annotations

from idfkit.simulation import ErrorReport, SimulationResult

errors: ErrorReport = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
errors = result.errors

# Fatal errors (simulation stopped)
for err in errors.fatal:
    print(f"FATAL: {err.message}")

# Severe errors (may cause incorrect results)
for err in errors.severe:
    print(f"SEVERE: {err.message}")

# Warnings
for warn in errors.warnings:
    print(f"Warning: {warn.message}")
# --8<-- [end:example]
