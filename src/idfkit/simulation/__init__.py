"""EnergyPlus simulation execution and result handling.

Provides subprocess-based simulation execution, EnergyPlus installation
discovery, structured result containers, output parsing, and variable
discovery.

Example:
    >>> from idfkit import load_idf
    >>> from idfkit.simulation import simulate, find_energyplus
    >>>
    >>> model = load_idf("building.idf")
    >>> result = simulate(model, "weather.epw")
    >>> print(result.errors.summary())

Parser Coverage
---------------

The module provides parsers for the most commonly used EnergyPlus output formats:

- **SQLite** (:class:`SQLResult`): Time-series data, tabular reports, and metadata.
  This is the recommended output format as it contains all simulation data in a
  single queryable file.
- **CSV** (:class:`CSVResult`): Time-series data in comma-separated format.
- **HTML** (:class:`HTMLResult`): Tabular reports in HTML format.
- **RDD/MDD** (:class:`OutputVariableIndex`): Available output variables and meters.
- **ERR** (:class:`ErrorReport`): Errors, warnings, and simulation status.

The following formats are **intentionally not implemented** as the SQLite output
covers the same data more reliably and completely:

- **ESO/MTR**: Binary-text time-series format (use SQLite instead).
- **EIO**: Simulation metadata and invariant outputs (use SQLite instead).

If you have a specific need for these formats, please open an issue describing
your use case.
"""

from __future__ import annotations

from ._common import prep_outputs
from .async_batch import SimulationEvent, async_simulate_batch, async_simulate_batch_stream
from .async_runner import async_simulate
from .batch import BatchResult, SimulationJob, simulate_batch
from .cache import CacheKey, SimulationCache
from .config import EnergyPlusConfig, find_energyplus
from .expand import (
    expand_objects,
    needs_ground_heat_preprocessing,
    run_basement_preprocessor,
    run_preprocessing,
    run_slab_preprocessor,
)
from .fs import AsyncFileSystem, AsyncLocalFileSystem, AsyncS3FileSystem, FileSystem, LocalFileSystem, S3FileSystem
from .outputs import OutputVariableIndex
from .parsers.csv import CSVColumn, CSVResult
from .parsers.err import ErrorMessage, ErrorReport
from .parsers.rdd import OutputMeter, OutputVariable
from .parsers.sql import EnvironmentInfo, SQLResult, TabularRow, TimeSeriesResult, VariableInfo
from .plotting import (
    PlotBackend,
    get_default_backend,
    plot_comfort_hours,
    plot_energy_balance,
    plot_temperature_profile,
)
from .progress import ProgressParser, SimulationProgress
from .progress_bars import tqdm_progress
from .result import SimulationResult
from .runner import simulate

__all__ = [
    "AsyncFileSystem",
    "AsyncLocalFileSystem",
    "AsyncS3FileSystem",
    "BatchResult",
    "CSVColumn",
    "CSVResult",
    "CacheKey",
    "EnergyPlusConfig",
    "EnvironmentInfo",
    "ErrorMessage",
    "ErrorReport",
    "FileSystem",
    "LocalFileSystem",
    "OutputMeter",
    "OutputVariable",
    "OutputVariableIndex",
    "PlotBackend",
    "ProgressParser",
    "S3FileSystem",
    "SQLResult",
    "SimulationCache",
    "SimulationEvent",
    "SimulationJob",
    "SimulationProgress",
    "SimulationResult",
    "TabularRow",
    "TimeSeriesResult",
    "VariableInfo",
    "async_simulate",
    "async_simulate_batch",
    "async_simulate_batch_stream",
    "expand_objects",
    "find_energyplus",
    "get_default_backend",
    "needs_ground_heat_preprocessing",
    "plot_comfort_hours",
    "plot_energy_balance",
    "plot_temperature_profile",
    "prep_outputs",
    "run_basement_preprocessor",
    "run_preprocessing",
    "run_slab_preprocessor",
    "simulate",
    "simulate_batch",
    "tqdm_progress",
]
