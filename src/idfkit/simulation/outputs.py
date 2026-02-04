"""Output variable discovery and model injection.

Provides the :class:`OutputVariableIndex` for searching available output
variables and meters from a completed simulation, and adding them to a model
for subsequent runs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from .parsers.rdd import OutputMeter, OutputVariable, parse_mdd_file, parse_rdd_file

if TYPE_CHECKING:
    from ..document import IDFDocument
    from .result import SimulationResult


@dataclass(frozen=True, slots=True)
class OutputVariableIndex:
    """Index of available output variables and meters for a model.

    Constructed from .rdd and .mdd files produced by EnergyPlus during a
    simulation run. Provides search, filtering, and model injection methods.

    Attributes:
        variables: Available output variables from the .rdd file.
        meters: Available output meters from the .mdd file.
    """

    variables: tuple[OutputVariable, ...]
    meters: tuple[OutputMeter, ...]

    @classmethod
    def from_simulation(cls, result: SimulationResult) -> OutputVariableIndex:
        """Create an index from a completed simulation result.

        Args:
            result: A SimulationResult with .rdd (and optionally .mdd) files.

        Returns:
            An OutputVariableIndex populated from the simulation output.

        Raises:
            FileNotFoundError: If the .rdd file is not found.
        """
        rdd_path = result.rdd_path
        if rdd_path is None:
            msg = "No .rdd file found in simulation output"
            raise FileNotFoundError(msg)
        return cls.from_files(rdd_path, result.mdd_path)

    @classmethod
    def from_files(
        cls,
        rdd_path: str | Path,
        mdd_path: str | Path | None = None,
    ) -> OutputVariableIndex:
        """Create an index from .rdd and .mdd file paths.

        Args:
            rdd_path: Path to the .rdd file.
            mdd_path: Optional path to the .mdd file.

        Returns:
            An OutputVariableIndex populated from the files.
        """
        variables = parse_rdd_file(rdd_path)
        meters = parse_mdd_file(mdd_path) if mdd_path is not None else ()
        return cls(variables=variables, meters=meters)

    def search(self, pattern: str) -> list[OutputVariable | OutputMeter]:
        """Search variables and meters by name pattern.

        Uses case-insensitive regex matching against variable/meter names.

        Args:
            pattern: A regex pattern to match against names.

        Returns:
            List of matching OutputVariable and OutputMeter entries.
        """
        regex = re.compile(pattern, re.IGNORECASE)
        results: list[OutputVariable | OutputMeter] = []
        for v in self.variables:
            if regex.search(v.name):
                results.append(v)
        for m in self.meters:
            if regex.search(m.name):
                results.append(m)
        return results

    def filter_by_units(self, units: str) -> list[OutputVariable | OutputMeter]:
        """Filter variables and meters by unit type.

        Args:
            units: The unit string to filter by (case-insensitive).

        Returns:
            List of matching OutputVariable and OutputMeter entries.
        """
        units_lower = units.lower()
        results: list[OutputVariable | OutputMeter] = []
        for v in self.variables:
            if v.units.lower() == units_lower:
                results.append(v)
        for m in self.meters:
            if m.units.lower() == units_lower:
                results.append(m)
        return results

    def add_all_to_model(
        self,
        model: IDFDocument,
        *,
        frequency: str = "Timestep",
        filter_pattern: str | None = None,
    ) -> int:
        """Add output variables and meters to a model.

        Args:
            model: The IDFDocument to add outputs to.
            frequency: The reporting frequency for all added outputs.
            filter_pattern: Optional regex pattern to filter which variables
                and meters are added (case-insensitive match on name).

        Returns:
            The number of output objects added.
        """
        items: list[OutputVariable | OutputMeter] = (
            self.search(filter_pattern) if filter_pattern is not None else [*self.variables, *self.meters]
        )

        count = 0
        for item in items:
            if isinstance(item, OutputVariable):
                # Use empty name to avoid DuplicateObjectError when multiple
                # variables share the same key (e.g. "*"). EnergyPlus treats
                # empty Key_Value the same as "*".
                model.add(
                    "Output:Variable",
                    "",
                    variable_name=item.name,
                    reporting_frequency=frequency,
                )
                count += 1
            else:
                model.add(
                    "Output:Meter",
                    item.name,
                    reporting_frequency=frequency,
                )
                count += 1
        return count
