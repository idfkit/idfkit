"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class EnergyManagementSystemProgramCallingManager_v8_9_to_v9_0:
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
    ) -> None:
        """Create a new ``EnergyManagementSystem:ProgramCallingManager`` and add it to the document.

        Input EMS program. a program needs a name a description of when it should be called and then lines of program code for EMS Runtime language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogramcallingmanager
        """

class LifeCycleCostParameters_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        discounting_convention: Literal["", "BeginningOfYear", "EndOfYear", "MidYear"] | None = "EndOfYear",
        inflation_approach: Literal["", "ConstantDollar", "CurrentDollar"] | None = "ConstantDollar",
        real_discount_rate: float | None = ...,
        nominal_discount_rate: float | None = ...,
        inflation: float | None = ...,
        base_date_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        base_date_year: float | None = ...,
        service_date_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        service_date_year: float | None = ...,
        length_of_study_period_in_years: float | None = ...,
        tax_rate: float | None = ...,
        depreciation_method: Literal[
            "",
            "ModifiedAcceleratedCostRecoverySystem-10year",
            "ModifiedAcceleratedCostRecoverySystem-15year",
            "ModifiedAcceleratedCostRecoverySystem-20year",
            "ModifiedAcceleratedCostRecoverySystem-3year",
            "ModifiedAcceleratedCostRecoverySystem-5year",
            "ModifiedAcceleratedCostRecoverySystem-7year",
            "None",
            "StraightLine-27year",
            "StraightLine-31year",
            "StraightLine-39year",
            "StraightLine-40year",
        ]
        | None = "None",
    ) -> None:
        """Create a new ``LifeCycleCost:Parameters`` and add it to the document.

        Provides inputs related to the overall life-cycle analysis. It establishes many of the assumptions used in computing the present value. It is important that when comparing the results of multiple simulations that the fields in the LifeCycleCost:Parameters objects are the same for all the simulations. When this object is present the tabular report file will contain the Life-Cycle Cost Report.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/lifecyclecost-parameters/#lifecyclecostparameters
        """

class CoilHeatingElectricMultiStage_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: float,
        stage_1_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        stage_2_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Electric:MultiStage`` and add it to the document.

        Electric heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingelectricmultistage
        """
