from __future__ import annotations

from idfkit.simulation import SimulationCache

cache: SimulationCache = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Clear everything
cache.clear()

# Or manually delete specific entries
import shutil

shutil.rmtree(cache.cache_dir / "abc123...")
# --8<-- [end:example]
