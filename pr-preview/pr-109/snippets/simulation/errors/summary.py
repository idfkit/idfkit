from __future__ import annotations

from idfkit.simulation import ErrorReport

errors: ErrorReport = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get a formatted summary string
print(errors.summary())
# Output: "0 Fatal, 2 Severe, 15 Warnings"
# --8<-- [end:example]
