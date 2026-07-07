from __future__ import annotations

from idfkit.simulation import SimulationCache

cache: SimulationCache = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Remove all cached entries
cache.clear()
# --8<-- [end:example]
