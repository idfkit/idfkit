from __future__ import annotations

from idfkit.simulation import EnergyPlusConfig

config: EnergyPlusConfig = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import find_energyplus

config = find_energyplus()
print(f"Found EnergyPlus {config.version[0]}.{config.version[1]}")
# --8<-- [end:example]
