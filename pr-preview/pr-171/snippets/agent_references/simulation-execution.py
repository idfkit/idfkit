from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import (
    BatchResult,
    EnergyPlusConfig,
    SimulationCache,
    SimulationJob,
    SimulationResult,
)

doc: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
config: EnergyPlusConfig = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
batch: BatchResult = ...  # type: ignore[assignment]
cache: SimulationCache = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import load_idf
from idfkit.simulation import simulate

doc = load_idf("building.idf")
result = simulate(doc, "weather.epw", design_day=True)
print(result.errors.summary())
# --8<-- [end:quickstart]


# --8<-- [start:core-api]
from idfkit.simulation import (
    simulate,  # sync, single model
    async_simulate,  # async, single model
    simulate_batch,  # sync, multiple jobs
    find_energyplus,  # discover the EnergyPlus install
    EnergyPlusConfig,  # pre-configured install handle
    SimulationCache,  # content-addressed cache
    SimulationJob,  # one job in a batch
    BatchResult,  # results from simulate_batch
    SimulationResult,  # result container — see result-parsing.md
    SimulationProgress,  # progress event payload
)
# --8<-- [end:core-api]


# --8<-- [start:discover]
from idfkit.simulation import find_energyplus

config = find_energyplus()  # latest installed
config = find_energyplus(version=(24, 1, 0))
print(config.executable, config.version)
# --8<-- [end:discover]


# --8<-- [start:version-handling]
# Option 1 — explicit migration before simulate (recommended for production)
from idfkit import migrate

doc = load_idf("v22_model.idf")
doc = migrate(doc, target_version=config.version).migrated_model

# Option 2 — let simulate forward-migrate transparently
result = simulate(doc, "weather.epw", auto_migrate=True)
print(result.migration_report.summary())  # what was changed
# --8<-- [end:version-handling]


# --8<-- [start:design-day-vs-annual]
# Quick smoke-test with the heating/cooling design days only — seconds
result = simulate(doc, "weather.epw", design_day=True)

# Full annual run — minutes
result = simulate(doc, "weather.epw", annual=True)

# Default (both flags False) — EnergyPlus's default, governed by SimulationControl in the IDF
result = simulate(doc, "weather.epw")
# --8<-- [end:design-day-vs-annual]


# --8<-- [start:async]
import asyncio
from idfkit.simulation import async_simulate


async def main():
    result = await async_simulate(doc, "weather.epw")
    print(result.errors.summary())


asyncio.run(main())
# --8<-- [end:async]


# --8<-- [start:batch]
from idfkit.simulation import simulate_batch, SimulationJob

jobs = []
for wwr in (0.2, 0.3, 0.4, 0.5):
    variant = doc.copy()
    from idfkit import set_wwr

    set_wwr(variant, wwr=wwr)
    jobs.append(SimulationJob(model=variant, weather="weather.epw", label=f"wwr_{int(wwr * 100)}"))

batch = simulate_batch(jobs, max_workers=4)
for job, result in zip(jobs, batch.results):
    print(job.label, result.errors.summary())
# --8<-- [end:batch]


# --8<-- [start:caching]
from idfkit.simulation import SimulationCache

cache = SimulationCache(cache_dir=".sim_cache")
result = simulate(doc, "weather.epw", cache=cache)  # first call runs
result = simulate(doc, "weather.epw", cache=cache)  # second call cache-hits, milliseconds
# --8<-- [end:caching]


# --8<-- [start:progress]
from idfkit.simulation import SimulationProgress


def on_progress(event: SimulationProgress) -> None:
    print(event.phase, event.percent, event.message)


result = simulate(doc, "weather.epw", on_progress=on_progress)

# Or for an interactive shell:
result = simulate(doc, "weather.epw", on_progress="tqdm")  # requires idfkit[progress]
# --8<-- [end:progress]


# --8<-- [start:remote-s3]
from idfkit.simulation import simulate, S3FileSystem

fs = S3FileSystem(bucket="my-sim-outputs")
result = simulate(
    doc,
    "weather.epw",
    output_dir="runs/2026-05-23/baseline",
    fs=fs,
)
# EnergyPlus runs in a local temp dir; outputs are uploaded to s3://my-sim-outputs/runs/2026-05-23/baseline/
# --8<-- [end:remote-s3]


# --8<-- [start:mistake-version-good]
result = simulate(doc, "weather.epw", auto_migrate=True)
# --8<-- [end:mistake-version-good]


# --8<-- [start:mistake-sql-good]
# simulate() auto-injects Output:SQLite if missing — just access result.sql safely:
if result.sql:
    ts = result.sql.get_timeseries("Zone Mean Air Temperature", "Office")
# --8<-- [end:mistake-sql-good]


# --8<-- [start:mistake-rerun-good]
cache = SimulationCache(cache_dir=".sim_cache")
for _ in range(10):
    result = simulate(doc, "weather.epw", cache=cache)  # cache-hits after the first
# --8<-- [end:mistake-rerun-good]


# --8<-- [start:mistake-errors-good]
result = simulate(doc, "weather.epw")
if result.errors.has_severe:
    print(result.errors.summary())
    for msg in result.errors.severe:
        print(msg.severity, msg.message)
    raise SystemExit("Simulation failed")
# --8<-- [end:mistake-errors-good]
