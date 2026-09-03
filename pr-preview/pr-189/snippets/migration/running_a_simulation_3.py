from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
# eppy-compatible shortcut (calls simulate() internally)
result = doc.run("weather.epw", design_day=True)
# --8<-- [end:example]
