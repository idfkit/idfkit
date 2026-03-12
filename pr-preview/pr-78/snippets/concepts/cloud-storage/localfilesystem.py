from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import simulate

model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import LocalFileSystem

fs = LocalFileSystem()  # This is the default
result = simulate(model, weather)  # Implicitly uses LocalFileSystem
# --8<-- [end:example]
