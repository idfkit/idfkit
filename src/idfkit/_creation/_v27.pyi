"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ScheduleFile_v9_2_to_v9_6:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: float,
        rows_to_skip_at_top: float,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["Comma", "Semicolon", "Space", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["No", "Yes"] | None = "No",
        minutes_per_item: float | None = ...,
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.6/io-reference/overview/group-schedules/#schedulefile
        """

class AirflowNetworkDistributionComponentCoil_v8_9_to_v9_2:
    def __call__(
        self,
        /,
        *,
        coil_name: str,
        coil_object_type: Literal[
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Water",
        ],
        air_path_length: float,
        air_path_hydraulic_diameter: float,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Coil`` and add it to the document.

        This object defines the name of a coil used in an air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentcoil
        """

class Timestep_v8_9_to_v22_1:
    def __call__(self, /, *, number_of_timesteps_per_hour: float | None = 6) -> None:
        """Create a new ``Timestep`` and add it to the document.

        Specifies the 'basic' timestep for the simulation. The value entered here is also known as the Zone Timestep. This is used in the Zone Heat Balance Model calculation as the driving timestep for heat transfer and load calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-simulation-parameters/#timestep
        """

class CoilCoolingDXCurveFitPerformance_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        base_operating_mode: str,
        crankcase_heater_capacity: float | None = 0,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        unit_internal_static_air_pressure: float | None = ...,
        capacity_control_method: Literal["Continuous", "Discrete"] | None = "Discrete",
        evaporative_condenser_basin_heater_capacity: float | None = 0,
        evaporative_condenser_basin_heater_setpoint_temperature: float | None = 2,
        evaporative_condenser_basin_heater_operating_schedule_name: str | None = ...,
        compressor_fuel_type: Literal[
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "Electricity",
        alternative_operating_mode_1: str | None = ...,
        alternative_operating_mode_2: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Performance`` and add it to the document.

        DX cooling coil performance specification referencing one or more operating modes. Mode 1 is always the base design operating mode. Additional modes are optional states such as subcool reheat for humidity control.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitperformance
        """
