"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ZoneBaseboardOutdoorTemperatureControlled:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        capacity_at_low_temperature: float | Literal["Autosize"] | None = "Autosize",
        low_temperature: float | Literal["Autosize"] | None = "Autosize",
        capacity_at_high_temperature: float | Literal["Autosize"] | None = "Autosize",
        high_temperature: float | Literal["Autosize"] | None = "Autosize",
        fraction_radiant: float | None = 0,
        end_use_subcategory: str | None = "General",
        design_zone_heating_setpoint: float | None = 20,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneBaseboard:OutdoorTemperatureControlled`` and add it to the document.

        Specifies outside temperature-controlled electric baseboard heating. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonebaseboardoutdoortemperaturecontrolled
        """

class AnyEnergyManagementSystemProgramCallingManager:
    def __call__(
        self,
        name: str,
        /,
        *,
        energyplus_model_calling_point: Literal[
            "AfterComponentInputReadIn",
            "AfterNewEnvironmentWarmUpIsComplete",
            "AfterPredictorAfterHVACManagers",
            "AfterPredictorBeforeHVACManagers",
            "BeginNewEnvironment",
            "BeginTimestepBeforePredictor",
            "EndOfSystemSizing",
            "EndOfSystemTimestepAfterHVACReporting",
            "EndOfSystemTimestepBeforeHVACReporting",
            "EndOfZoneSizing",
            "EndOfZoneTimestepAfterZoneReporting",
            "EndOfZoneTimestepBeforeZoneReporting",
            "InsideHVACSystemIterationLoop",
            "UnitarySystemSizing",
            "UserDefinedComponentModel",
        ]
        | None = ...,
        programs: Sequence[
            _g.EnergyManagementSystemProgramCallingManagerProgramsItem
            | _g.EnergyManagementSystemProgramCallingManagerProgramsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``EnergyManagementSystem:ProgramCallingManager`` and add it to the document.

        Input EMS program. a program needs a name a description of when it should be called and then lines of program code for EMS Runtime language

        ``programs`` takes the extensible groups in order, one dict per group:

        ```python
        doc["EnergyManagementSystem:ProgramCallingManager"].add(
            "EnergyManagementSystem ProgramCallingManager 1",
            programs=[
                {"program_name": "Program 1"},
                {"program_name": "Program 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogramcallingmanager
        """
