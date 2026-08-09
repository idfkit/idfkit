from __future__ import annotations

from idfkit.simulation import ErrorReport

errors: ErrorReport = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import ErrorReport

errors = ErrorReport.from_file("/path/to/eplusout.err")
print(errors.summary())
# --8<-- [end:example]
