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
    "S3FileSystem",
    "SQLResult",
    "SimulationCache",
    "SimulationJob",
    "SimulationResult",
    "TabularRow",
    "TimeSeriesResult",
    "VariableInfo",
    "find_energyplus",
    "simulate",
    "simulate_batch",
]
