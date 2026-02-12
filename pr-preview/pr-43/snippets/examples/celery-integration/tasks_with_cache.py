from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from pathlib import Path

from celery import Celery

from idfkit import load_idf
from idfkit.simulation import SimulationCache, simulate

app = Celery("tasks")
app.config_from_object("celeryconfig")

# Shared cache directory — must be accessible by all workers.
# Use a network file system (NFS, EFS) or a local directory if
# workers run on the same machine.
CACHE_DIR = Path("/shared/simulation-cache")
cache = SimulationCache(cache_dir=CACHE_DIR)


@app.task(bind=True, name="simulate_cached")
def simulate_cached(
    self,
    idf_path: str,
    weather_path: str,
    output_dir: str,
    design_day: bool = False,
) -> dict:
    """Simulate with content-addressed caching to skip duplicate work."""
    model = load_idf(idf_path)
    result = simulate(
        model,
        weather_path,
        output_dir=output_dir,
        design_day=design_day,
        cache=cache,
    )
    return {
        "success": result.success,
        "runtime": result.runtime_seconds,
        "output_dir": str(Path(result.run_dir).resolve()),
    }


# --8<-- [end:example]
