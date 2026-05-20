from __future__ import annotations

from idfkit.simulation import ErrorReport

errors: ErrorReport = ...  # type: ignore[assignment]
# --8<-- [start:example]
print(f"Fatal: {errors.fatal_count}")
print(f"Severe: {errors.severe_count}")
print(f"Warnings: {errors.warning_count}")
# --8<-- [end:example]
