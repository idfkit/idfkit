from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import simulate

model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(
    model,
    weather,
    extra_args=["--convert-only"],  # Just convert, don't simulate
)
# --8<-- [end:example]
