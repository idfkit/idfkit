from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import EnergyPlusConfig, simulate

config: EnergyPlusConfig = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Auto-discovery
result = simulate(model, weather)

# Explicit path
from idfkit.simulation import find_energyplus

config = find_energyplus("/custom/path/EnergyPlus-24-1-0")
result = simulate(model, weather, energyplus=config)

# Environment variable
# Set ENERGYPLUS_DIR=/path/to/EnergyPlus before running
result = simulate(model, weather)
# --8<-- [end:example]
