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

from .config import EnergyPlusConfig, find_energyplus
from .outputs import OutputVariableIndex
from .parsers.csv import CSVColumn, CSVResult
from .parsers.err import ErrorMessage, ErrorReport
from .parsers.rdd import OutputMeter, OutputVariable
from .parsers.sql import EnvironmentInfo, SQLResult, TabularRow, TimeSeriesResult, VariableInfo
from .result import SimulationResult
from .runner import simulate

__all__ = [
    "CSVColumn",
    "CSVResult",
    "EnergyPlusConfig",
    "EnvironmentInfo",
    "ErrorMessage",
    "ErrorReport",
    "OutputMeter",
    "OutputVariable",
    "OutputVariableIndex",
    "SQLResult",
    "SimulationResult",
    "TabularRow",
    "TimeSeriesResult",
    "VariableInfo",
    "find_energyplus",
    "simulate",
]
