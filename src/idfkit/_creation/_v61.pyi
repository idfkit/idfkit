"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ScheduleFile_v22_1:
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
        minutes_per_item: float | None = 60,
        adjust_schedule_for_daylight_savings: Literal["No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-schedules/#schedulefile
        """

class HeatPumpWaterToWaterEquationFitHeating_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_heating_capacity: float | Literal["Autosize"],
        reference_heating_power_consumption: float | Literal["Autosize"],
        heating_capacity_coefficient_1: float,
        heating_capacity_coefficient_2: float,
        heating_capacity_coefficient_3: float,
        heating_capacity_coefficient_4: float,
        heating_capacity_coefficient_5: float,
        heating_compressor_power_coefficient_1: float,
        heating_compressor_power_coefficient_2: float,
        heating_compressor_power_coefficient_3: float,
        heating_compressor_power_coefficient_4: float,
        heating_compressor_power_coefficient_5: float,
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
        companion_cooling_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Heating`` and add it to the document.

        simple water-water hp curve-fit model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitheating
        """

class ZoneInfiltrationEffectiveLeakageArea_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        effective_air_leakage_area: float,
        stack_coefficient: float,
        wind_coefficient: float,
    ) -> None:
        """Create a new ``ZoneInfiltration:EffectiveLeakageArea`` and add it to the document.

        Infiltration is specified as effective leakage area at 4 Pa, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * (AL /1000) SQRT(Cs*|(Tzone-Todb)| + Cw*WindSpd**2 )

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zoneinfiltrationeffectiveleakagearea
        """

class AirTerminalSingleDuctVAVHeatAndCoolReheat_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        maximum_reheat_air_temperature: float | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with reheat coil (hot water, electric, gas, or steam).
        """

class ThermalStorageChilledWaterStratified_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float,
        tank_height: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_shape: Literal["HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = 0,
        temperature_sensor_height: float | None = ...,
        minimum_temperature_limit: float | None = ...,
        nominal_cooling_capacity: float | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_heat_transfer_effectiveness: float | None = 1,
        use_side_availability_schedule_name: str | None = ...,
        use_side_inlet_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        use_side_outlet_height: float | None = 0,
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_heat_transfer_effectiveness: float | None = 1,
        source_side_availability_schedule_name: str | None = ...,
        source_side_inlet_height: float | None = 0,
        source_side_outlet_height: float | Literal["Autocalculate"] | None = "Autocalculate",
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        tank_recovery_time: float | None = 4,
        inlet_mode: Literal["Fixed", "Seeking"] | None = "Fixed",
        number_of_nodes: float | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
    ) -> None:
        """Create a new ``ThermalStorage:ChilledWater:Stratified`` and add it to the document.

        Chilled water storage with a stratified, multi-node tank. The chilled water is 'used' by drawing from the 'Use Side' of the water tank. The tank is indirectly charged by circulating cold water through the 'Source Side' of the water tank.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-water-heaters/#thermalstoragechilledwaterstratified
        """
