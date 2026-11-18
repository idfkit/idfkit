"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class MaterialNoMass_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thermal_resistance: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
    ) -> None:
        """Create a new ``Material:NoMass`` and add it to the document.

        Regular materials properties described whose principal description is R (Thermal Resistance)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-surface-construction-elements/#materialnomass
        """

class CoilHeatingWaterToAirHeatPumpEquationFit_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        heating_capacity_coefficient_1: float,
        heating_capacity_coefficient_2: float,
        heating_capacity_coefficient_3: float,
        heating_capacity_coefficient_4: float,
        heating_capacity_coefficient_5: float,
        heating_power_consumption_coefficient_1: float,
        heating_power_consumption_coefficient_2: float,
        heating_power_consumption_coefficient_3: float,
        heating_power_consumption_coefficient_4: float,
        heating_power_consumption_coefficient_5: float,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpequationfit
        """

class ChillerHeaterAbsorptionDirectFired_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        nominal_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_to_cooling_capacity_ratio: float | None = 0.8,
        fuel_input_to_cooling_output_ratio: float | None = 0.97,
        fuel_input_to_heating_output_ratio: float | None = 1.25,
        electric_input_to_cooling_output_ratio: float | None = 0.01,
        electric_input_to_heating_output_ratio: float | None = 0,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        design_entering_condenser_water_temperature: float | None = 29,
        design_leaving_chilled_water_temperature: float | None = 7,
        design_chilled_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_hot_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        heating_capacity_function_of_cooling_capacity_curve_name: str | None = ...,
        fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None = ...,
        temperature_curve_input_variable: Literal["", "EnteringCondenser", "LeavingCondenser"]
        | None = "EnteringCondenser",
        condenser_type: Literal["", "AirCooled", "WaterCooled"] | None = "WaterCooled",
        chilled_water_temperature_lower_limit: float | None = 2,
        fuel_higher_heating_value: float | None = 0,
        fuel_type: Literal[
            "", "Diesel", "FuelOil#1", "FuelOil#2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "PropaneGas"
        ]
        | None = "NaturalGas",
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``ChillerHeater:Absorption:DirectFired`` and add it to the document.

        Direct fired gas absorption chiller-heater using performance curves similar to DOE-2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-plant-equipment/#chillerheaterabsorptiondirectfired
        """

class ZoneControlThermostatStagedDualSetpoint_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        number_of_heating_stages: float,
        stage_1_heating_temperature_offset: float,
        number_of_cooling_stages: float,
        stage_1_cooling_temperature_offset: float,
        heating_temperature_setpoint_schedule_name: str | None = ...,
        heating_throttling_temperature_range: float | None = 1.1,
        stage_2_heating_temperature_offset: float | None = ...,
        stage_3_heating_temperature_offset: float | None = ...,
        stage_4_heating_temperature_offset: float | None = ...,
        cooling_temperature_setpoint_base_schedule_name: str | None = ...,
        cooling_throttling_temperature_range: float | None = 1.1,
        stage_2_cooling_temperature_offset: float | None = ...,
        stage_3_cooling_temperature_offset: float | None = ...,
        stage_4_cooling_temperature_offset: float | None = ...,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat:StagedDualSetpoint`` and add it to the document.

        Define the Thermostat StagedDualSetpoint settings for a zone or list of zones. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostatstageddualsetpoint
        """

class EnergyManagementSystemTrendVariable_v8_9_to_v22_1:
    def __call__(self, name: str, /, *, ems_variable_name: str, number_of_timesteps_to_be_logged: float) -> None:
        """Create a new ``EnergyManagementSystem:TrendVariable`` and add it to the document.

        This object sets up an EMS trend variable from an Erl variable A trend variable logs values across timesteps

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemtrendvariable
        """

class ZoneHVACLowTemperatureRadiantElectric_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_setpoint_temperature_schedule_name: str,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
        ]
        | None = "MeanAirTemperature",
        heating_throttling_range: float | None = 0,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:Electric`` and add it to the document.

        Electric resistance low temperature radiant system

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantelectric
        """
