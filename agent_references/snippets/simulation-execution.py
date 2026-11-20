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
# No output_dir: EnergyPlus runs in a temp dir, which the with block deletes on exit.
with simulate(doc, "weather.epw", design_day=True) as result:
    result.raise_for_status()  # SimulationError quoting the fatal/severe messages if EnergyPlus failed
    print(result.errors.summary())  # counts, plus the fatal and first severe messages
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
# Safe whatever the model's version: a model already at config.version comes back as a copy.
doc = migrate(doc, target_version=config.version).migrated_model

# Option 2 — let simulate forward-migrate transparently
result = simulate(doc, "weather.epw", auto_migrate=True)
if result.migration_report is not None:  # None when the model already matched
    print(result.migration_report.summary())  # what was changed
# --8<-- [end:version-handling]


# --8<-- [start:design-day-vs-annual]
from idfkit.weather import DesignDayManager

# Quick smoke-test with the heating/cooling design days only — seconds.
# design_day=True needs SizingPeriod:DesignDay objects (new_document() adds none)
if "SizingPeriod:DesignDay" not in doc:
    DesignDayManager("weather.ddy").apply_to_model(doc)
result = simulate(doc, "weather.epw", design_day=True)

# Design days only, without a weather file (weather defaults to None)
result = simulate(doc, design_day=True)

# Full annual run — minutes. annual=True needs a RunPeriod (new_document() adds none)
if "RunPeriod" not in doc:
    doc.run_periods.add("Annual", begin_month=1, begin_day_of_month=1, end_month=12, end_day_of_month=31)
result = simulate(doc, "weather.epw", annual=True)

# Default (both flags False) — governed by SimulationControl in the IDF: the sizing periods,
# then the RunPeriods. A model with neither (a fresh new_document()) is refused before
# EnergyPlus starts, rather than "succeeding" with empty results.
result = simulate(doc, "weather.epw")
# --8<-- [end:design-day-vs-annual]


# --8<-- [start:async]
import asyncio
from idfkit.simulation import async_simulate


async def main():
    async with await async_simulate(doc, "weather.epw") as result:  # temp run_dir deleted on exit
        print(result.errors.summary())


asyncio.run(main())
# --8<-- [end:async]


# --8<-- [start:batch]
from idfkit.simulation import REFUSED_RUN_DIR, simulate_batch, SimulationJob

jobs = []
for wwr in (0.2, 0.3, 0.4, 0.5):
    variant = doc.copy()
    from idfkit import set_wwr

    set_wwr(variant, wwr=wwr)
    jobs.append(SimulationJob(model=variant, weather="weather.epw", label=f"wwr_{int(wwr * 100)}"))

with simulate_batch(jobs, max_workers=4) as batch:  # deletes the jobs' temp run dirs on exit
    for job, result in zip(jobs, batch):
        if result.run_dir == REFUSED_RUN_DIR:
            print(job.label, "refused:", result.stderr)  # EnergyPlus never ran
        else:
            print(job.label, result.errors.summary())
# --8<-- [end:batch]


# --8<-- [start:batch-fail-fast]
batch = simulate_batch(jobs, max_workers=4, fail_fast=True)  # stop at the first failed job
for result in batch.failed:  # the job that failed (and any that failed before the stop)
    print(result.errors.summary())
for result in batch.cancelled:  # never started, or EnergyPlus killed; nothing is raised
    print(result.refusal)  # "never started: job 'wwr_30' failed and fail_fast=True stopped the batch"
batch.cleanup()
# --8<-- [end:batch-fail-fast]


# --8<-- [start:caching]
from idfkit.simulation import SimulationCache

cache = SimulationCache(cache_dir=".sim_cache")
result = simulate(doc, "weather.epw", cache=cache)  # first call runs
result = simulate(doc, "weather.epw", cache=cache)  # second call cache-hits, milliseconds
print(result.cached)  # True: a hit; no output_dir, so run_dir is the read-only cache entry

# Bound it: evict least-recently-used entries after each store, or trim by size/age on demand.
cache = SimulationCache(cache_dir=".sim_cache", max_bytes=5 * 1024**3)
removed = cache.prune(max_bytes=1024**3, max_age=7 * 24 * 3600)  # entries removed
print(cache.size_bytes())
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
# and the accessors read them back from S3: each first read of a file is a download.
errors = result.errors  # downloads eplus.err
result.close()  # removes the local temp copy result.sql downloads; the S3 objects stay
# --8<-- [end:remote-s3]


# --8<-- [start:mistake-version-good]
result = simulate(doc, "weather.epw", auto_migrate=True)
# --8<-- [end:mistake-version-good]


# --8<-- [start:mistake-sql-good]
# simulate() auto-injects Output:SQLite if missing, so result.sql is there once the run succeeded.
# Without a .sql it raises OutputNotFoundError, naming the output to add or pointing to the .err file.
result = simulate(doc, "weather.epw").raise_for_status()
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


# --8<-- [start:mistake-cleanup-good]
with simulate_batch(jobs, max_workers=4) as batch:  # temp run dirs deleted on exit, no ResourceWarning
    for job, result in zip(jobs, batch):
        print(job.label, result.errors.summary())

kept = [
    SimulationJob(model=job.model, weather=job.weather, label=job.label, output_dir=f"runs/{job.label}") for job in jobs
]
for result in simulate_batch(kept, max_workers=4):  # your output_dir is never deleted
    print(result.run_dir)
# --8<-- [end:mistake-cleanup-good]
