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
- **RDD/MDD** (:class:`OutputVariableIndex`): Available output variables and meters.
- **ERR** (:class:`ErrorReport`): Errors, warnings, and simulation status.

The following parsers are **intentionally not implemented** as the SQLite output
covers the same data more reliably and completely:

- **ESO/MTR**: Binary-text time-series format (use SQLite instead).
- **HTML**: Tabular reports in HTML format (use SQLite's tabular data instead).
- **EIO**: Simulation metadata and invariant outputs (use SQLite instead).

If you have a specific need for these formats, please open an issue describing
your use case.
"""

from __future__ import annotations

from .batch import BatchResult, SimulationJob, simulate_batch
from .cache import CacheKey, SimulationCache
from .config import EnergyPlusConfig, find_energyplus
from .fs import FileSystem, LocalFileSystem, S3FileSystem
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
from .result import SimulationResult
from .runner import simulate

__all__ = [
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
    "S3FileSystem",
    "SQLResult",
    "SimulationCache",
    "SimulationJob",
    "SimulationResult",
    "TabularRow",
    "TimeSeriesResult",
    "VariableInfo",
    "find_energyplus",
    "get_default_backend",
    "plot_comfort_hours",
    "plot_energy_balance",
    "plot_temperature_profile",
    "simulate",
    "simulate_batch",
]
