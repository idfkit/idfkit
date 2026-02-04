"""EnergyPlus simulation execution and result handling.

Provides subprocess-based simulation execution, EnergyPlus installation
discovery, structured result containers, and .err file parsing.

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
from .parsers.err import ErrorMessage, ErrorReport
from .result import SimulationResult
from .runner import simulate

__all__ = [
    "EnergyPlusConfig",
    "ErrorMessage",
    "ErrorReport",
    "SimulationResult",
    "find_energyplus",
    "simulate",
]
