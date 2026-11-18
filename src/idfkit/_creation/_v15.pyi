"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class FanSystemModel_v9_4_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        design_maximum_air_flow_rate: float | Literal["Autosize"],
        design_pressure_rise: float,
        availability_schedule_name: str | None = ...,
        speed_control_method: Literal["", "Continuous", "Discrete"] | None = "Discrete",
        electric_power_minimum_flow_rate_fraction: float | None = 0.2,
        motor_efficiency: float | None = 0.9,
        motor_in_air_stream_fraction: float | None = 1,
        design_electric_power_consumption: float | Literal["", "Autosize"] | None = "Autosize",
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure", "TotalEfficiencyAndPressure"]
        | None = "PowerPerFlowPerPressure",
        electric_power_per_unit_flow_rate: float | None = ...,
        electric_power_per_unit_flow_rate_per_unit_pressure: float | None = 1.66667,
        fan_total_efficiency: float | None = 0.7,
        electric_power_function_of_flow_fraction_curve_name: str | None = ...,
        night_ventilation_mode_pressure_rise: float | None = ...,
        night_ventilation_mode_flow_fraction: float | None = ...,
        motor_loss_zone_name: str | None = ...,
        motor_loss_radiative_fraction: float | None = ...,
        end_use_subcategory: str | None = "General",
        number_of_speeds: float | None = 1,
        speed_fractions: list[_g.FanSystemModelSpeedFractionsItem] = ...,
    ) -> None:
        """Create a new ``Fan:SystemModel`` and add it to the document.

        Versatile simple fan that can be used in variable air volume, constant volume, on-off cycling, two-speed or multi-speed applications. Performance at different flow rates, or speed levels, is determined using separate performance curve or table or prescribed power fractions at discrete speed levels for two-speed or multi-speed fans.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-fans/#fansystemmodel
        """

class AirflowNetworkDistributionComponentFan_v8_9_to_v9_1:
    def __call__(
        self,
        /,
        *,
        fan_name: str,
        supply_fan_object_type: Literal["", "Fan:ConstantVolume", "Fan:OnOff", "Fan:VariableVolume"]
        | None = "Fan:ConstantVolume",
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Fan`` and add it to the document.

        This object defines the name of the supply Air Fan used in an Air loop.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentfan
        """

class AirConditionerVariableRefrigerantFlow_v9_3_to_v9_5:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_terminal_unit_list_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
        cooling_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_capacity_ratio_boundary_curve_name: str | None = ...,
        cooling_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_boundary_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        cooling_combination_ratio_correction_factor_curve_name: str | None = ...,
        cooling_part_load_fraction_correlation_curve_name: str | None = ...,
        gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        heating_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_capacity_ratio_boundary_curve_name: str | None = ...,
        heating_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_boundary_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_performance_curve_outdoor_temperature_type: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        heating_combination_ratio_correction_factor_curve_name: str | None = ...,
        heating_part_load_fraction_correlation_curve_name: str | None = ...,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = ...,
        vertical_height_used_for_piping_correction_factor: float | None = ...,
        piping_correction_factor_for_length_in_cooling_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_cooling_mode_coefficient: float | None = 0,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = ...,
        piping_correction_factor_for_length_in_heating_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_heating_mode_coefficient: float | None = 0,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: float | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        water_condenser_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        supply_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal[
            "",
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
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = ...,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = ...,
        heat_recovery_cooling_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_capacity_fraction: float | None = 0.5,
        heat_recovery_cooling_capacity_time_constant: float | None = 0.15,
        heat_recovery_cooling_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        heat_recovery_heating_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0.15,
        heat_recovery_heating_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow`` and add it to the document.

        Variable refrigerant flow (VRF) air-to-air heat pump condensing unit (includes one or more electric compressors and outdoor fan). Serves one or more VRF zone terminal units. See ZoneHVAC:TerminalUnit:VariableRefrigerantFlow and ZoneTerminalUnitList.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflow
        """

class OutputControlTableStyle_v8_9_to_v23_2:
    def __call__(
        self,
        /,
        *,
        column_separator: Literal[
            "", "All", "Comma", "CommaAndHTML", "CommaAndXML", "Fixed", "HTML", "Tab", "TabAndHTML", "XML", "XMLandHTML"
        ]
        | None = "Comma",
        unit_conversion: Literal["", "InchPound", "JtoGJ", "JtoKWH", "JtoMJ", "None"] | None = "None",
    ) -> None:
        """Create a new ``OutputControl:Table:Style`` and add it to the document.

        default style for the OutputControl:Table:Style is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a better choice. fixed puts spaces between the 'columns'. HTML produces tables in HTML. XML produces an XML file. note - if no OutputControl:Table:Style is included, the defaults are comma and None.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/standard-output-reports/outputcontrol-table-style/#outputcontroltablestyle
        """

class WallDetailed_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[_g.WallDetailedVerticesItem] = ...,
    ) -> None:
        """Create a new ``Wall:Detailed`` and add it to the document.

        Allows for detailed entry of wall heat transfer surfaces.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#walldetailed
        """

class AirTerminalSingleDuctParallelPIUReheat_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        maximum_secondary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        fan_on_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        reheat_coil_air_inlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ParallelPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, parallel powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductparallelpiureheat
        """

class CoolingTowerSingleSpeed_v9_2_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_regime_air_flow_rate: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        free_convection_regime_u_factor_times_area_value: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | None = ...,
        free_convection_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        number_of_cells: float | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = "MinimalCell",
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:SingleSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a single-speed fan drawing air through the tower (induced-draft configuration). Added fluid bypass as an additional capacity control. 8/2008. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#coolingtowersinglespeed
        """

class OutputDebuggingData_v8_9_to_v9_3:
    def __call__(
        self, /, *, report_debugging_data: float | None = ..., report_during_warmup: float | None = ...
    ) -> None:
        """Create a new ``Output:DebuggingData`` and add it to the document.

        switch eplusout.dbg file on or off

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-simulation-parameters/#outputdebuggingdata
        """

class ZoneHVACEquipmentList_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_distribution_scheme: Literal["", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"]
        | None = "SequentialLoad",
        equipment: list[_vd.ZoneHVACEquipmentListEquipmentItem_v8_9_to_v9_0] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EquipmentList`` and add it to the document.

        List equipment in simulation order. Note that an ZoneHVAC:AirDistributionUnit or AirTerminal:SingleDuct:Uncontrolled object must be listed in this statement if there is a forced air system serving the zone from the air loop. Equipment is simulated in the order specified by Zone Equipment Cooling Sequence and Zone Equipment Heating or No-Load Sequence, depending on the thermostat request. For equipment of similar type, assign sequence 1 to the first system intended to serve that type of load. For situations where one or more equipment types has limited capacity or limited control, order the sequence so that the most controllable piece of equipment runs last. For example, with a dedicated outdoor air system (DOAS), the air terminal for the DOAS should be assigned Heating Sequence = 1 and Cooling Sequence = 1. Any other equipment should be assigned sequence 2 or higher so that it will see the net load after the DOAS air is added to the zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-zone-equipment/#zonehvacequipmentlist
        """

class ZoneHVACEquipmentList_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_distribution_scheme: Literal["", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"]
        | None = "SequentialLoad",
        equipment: list[_vd.ZoneHVACEquipmentListEquipmentItem_v9_3_to_v22_1] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EquipmentList`` and add it to the document.

        List equipment in simulation order. Note that an ZoneHVAC:AirDistributionUnit object must be listed in this statement if there is a forced air system serving the zone from the air loop. Equipment is simulated in the order specified by Zone Equipment Cooling Sequence and Zone Equipment Heating or No-Load Sequence, depending on the thermostat request. For equipment of similar type, assign sequence 1 to the first system intended to serve that type of load. For situations where one or more equipment types has limited capacity or limited control, order the sequence so that the most controllable piece of equipment runs last. For example, with a dedicated outdoor air system (DOAS), the air terminal for the DOAS should be assigned Heating Sequence = 1 and Cooling Sequence = 1. Any other equipment should be assigned sequence 2 or higher so that it will see the net load after the DOAS air is added to the zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-zone-equipment/#zonehvacequipmentlist
        """

class ComfortViewFactorAngles_v9_6_to_v23_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_name: str | None = ...,
        surface_1_name: str | None = ...,
        angle_factor_1: float | None = ...,
        surface_2_name: str | None = ...,
        angle_factor_2: float | None = ...,
        surface_3_name: str | None = ...,
        angle_factor_3: float | None = ...,
        surface_4_name: str | None = ...,
        angle_factor_4: float | None = ...,
        surface_5_name: str | None = ...,
        angle_factor_5: float | None = ...,
        surface_6_name: str | None = ...,
        angle_factor_6: float | None = ...,
        surface_7_name: str | None = ...,
        angle_factor_7: float | None = ...,
        surface_8_name: str | None = ...,
        angle_factor_8: float | None = ...,
        surface_9_name: str | None = ...,
        angle_factor_9: float | None = ...,
        surface_10_name: str | None = ...,
        angle_factor_10: float | None = ...,
        surface_11_name: str | None = ...,
        angle_factor_11: float | None = ...,
        surface_12_name: str | None = ...,
        angle_factor_12: float | None = ...,
        surface_13_name: str | None = ...,
        angle_factor_13: float | None = ...,
        surface_14_name: str | None = ...,
        angle_factor_14: float | None = ...,
        surface_15_name: str | None = ...,
        angle_factor_15: float | None = ...,
        surface_16_name: str | None = ...,
        angle_factor_16: float | None = ...,
        surface_17_name: str | None = ...,
        angle_factor_17: float | None = ...,
        surface_18_name: str | None = ...,
        angle_factor_18: float | None = ...,
        surface_19_name: str | None = ...,
        angle_factor_19: float | None = ...,
        surface_20_name: str | None = ...,
        angle_factor_20: float | None = ...,
        surface_21_name: str | None = ...,
        angle_factor_21: float | None = ...,
        surface_22_name: str | None = ...,
        angle_factor_22: float | None = ...,
        surface_23_name: str | None = ...,
        angle_factor_23: float | None = ...,
        surface_24_name: str | None = ...,
        angle_factor_24: float | None = ...,
        surface_25_name: str | None = ...,
        angle_factor_25: float | None = ...,
        surface_26_name: str | None = ...,
        angle_factor_26: float | None = ...,
        surface_27_name: str | None = ...,
        angle_factor_27: float | None = ...,
        surface_28_name: str | None = ...,
        angle_factor_28: float | None = ...,
        surface_29_name: str | None = ...,
        angle_factor_29: float | None = ...,
        surface_30_name: str | None = ...,
        angle_factor_30: float | None = ...,
        surface_31_name: str | None = ...,
        angle_factor_31: float | None = ...,
        surface_32_name: str | None = ...,
        angle_factor_32: float | None = ...,
        surface_33_name: str | None = ...,
        angle_factor_33: float | None = ...,
        surface_34_name: str | None = ...,
        angle_factor_34: float | None = ...,
        surface_35_name: str | None = ...,
        angle_factor_35: float | None = ...,
        surface_36_name: str | None = ...,
        angle_factor_36: float | None = ...,
        surface_37_name: str | None = ...,
        angle_factor_37: float | None = ...,
        surface_38_name: str | None = ...,
        angle_factor_38: float | None = ...,
        surface_39_name: str | None = ...,
        angle_factor_39: float | None = ...,
        surface_40_name: str | None = ...,
        angle_factor_40: float | None = ...,
        surface_41_name: str | None = ...,
        angle_factor_41: float | None = ...,
        surface_42_name: str | None = ...,
        angle_factor_42: float | None = ...,
        surface_43_name: str | None = ...,
        angle_factor_43: float | None = ...,
        surface_44_name: str | None = ...,
        angle_factor_44: float | None = ...,
        surface_45_name: str | None = ...,
        angle_factor_45: float | None = ...,
        surface_46_name: str | None = ...,
        angle_factor_46: float | None = ...,
        surface_47_name: str | None = ...,
        angle_factor_47: float | None = ...,
        surface_48_name: str | None = ...,
        angle_factor_48: float | None = ...,
        surface_49_name: str | None = ...,
        angle_factor_49: float | None = ...,
        surface_50_name: str | None = ...,
        angle_factor_50: float | None = ...,
        surface_51_name: str | None = ...,
        angle_factor_51: float | None = ...,
        surface_52_name: str | None = ...,
        angle_factor_52: float | None = ...,
        surface_53_name: str | None = ...,
        angle_factor_53: float | None = ...,
        surface_54_name: str | None = ...,
        angle_factor_54: float | None = ...,
        surface_55_name: str | None = ...,
        angle_factor_55: float | None = ...,
        surface_56_name: str | None = ...,
        angle_factor_56: float | None = ...,
        surface_57_name: str | None = ...,
        angle_factor_57: float | None = ...,
        surface_58_name: str | None = ...,
        angle_factor_58: float | None = ...,
        surface_59_name: str | None = ...,
        angle_factor_59: float | None = ...,
        surface_60_name: str | None = ...,
        angle_factor_60: float | None = ...,
        surface_61_name: str | None = ...,
        angle_factor_61: float | None = ...,
        surface_62_name: str | None = ...,
        angle_factor_62: float | None = ...,
        surface_63_name: str | None = ...,
        angle_factor_63: float | None = ...,
        surface_64_name: str | None = ...,
        angle_factor_64: float | None = ...,
        surface_65_name: str | None = ...,
        angle_factor_65: float | None = ...,
        surface_66_name: str | None = ...,
        angle_factor_66: float | None = ...,
        surface_67_name: str | None = ...,
        angle_factor_67: float | None = ...,
        surface_68_name: str | None = ...,
        angle_factor_68: float | None = ...,
        surface_69_name: str | None = ...,
        angle_factor_69: float | None = ...,
        surface_70_name: str | None = ...,
        angle_factor_70: float | None = ...,
        surface_71_name: str | None = ...,
        angle_factor_71: float | None = ...,
        surface_72_name: str | None = ...,
        angle_factor_72: float | None = ...,
        surface_73_name: str | None = ...,
        angle_factor_73: float | None = ...,
        surface_74_name: str | None = ...,
        angle_factor_74: float | None = ...,
        surface_75_name: str | None = ...,
        angle_factor_75: float | None = ...,
        surface_76_name: str | None = ...,
        angle_factor_76: float | None = ...,
        surface_77_name: str | None = ...,
        angle_factor_77: float | None = ...,
        surface_78_name: str | None = ...,
        angle_factor_78: float | None = ...,
        surface_79_name: str | None = ...,
        angle_factor_79: float | None = ...,
        surface_80_name: str | None = ...,
        angle_factor_80: float | None = ...,
        surface_81_name: str | None = ...,
        angle_factor_81: float | None = ...,
        surface_82_name: str | None = ...,
        angle_factor_82: float | None = ...,
        surface_83_name: str | None = ...,
        angle_factor_83: float | None = ...,
        surface_84_name: str | None = ...,
        angle_factor_84: float | None = ...,
        surface_85_name: str | None = ...,
        angle_factor_85: float | None = ...,
        surface_86_name: str | None = ...,
        angle_factor_86: float | None = ...,
        surface_87_name: str | None = ...,
        angle_factor_87: float | None = ...,
        surface_88_name: str | None = ...,
        angle_factor_88: float | None = ...,
        surface_89_name: str | None = ...,
        angle_factor_89: float | None = ...,
        surface_90_name: str | None = ...,
        angle_factor_90: float | None = ...,
        surface_91_name: str | None = ...,
        angle_factor_91: float | None = ...,
        surface_92_name: str | None = ...,
        angle_factor_92: float | None = ...,
        surface_93_name: str | None = ...,
        angle_factor_93: float | None = ...,
        surface_94_name: str | None = ...,
        angle_factor_94: float | None = ...,
        surface_95_name: str | None = ...,
        angle_factor_95: float | None = ...,
        surface_96_name: str | None = ...,
        angle_factor_96: float | None = ...,
        surface_97_name: str | None = ...,
        angle_factor_97: float | None = ...,
        surface_98_name: str | None = ...,
        angle_factor_98: float | None = ...,
        surface_99_name: str | None = ...,
        angle_factor_99: float | None = ...,
        surface_100_name: str | None = ...,
        angle_factor_100: float | None = ...,
    ) -> None:
        """Create a new ``ComfortViewFactorAngles`` and add it to the document.

        Used to specify radiant view factors for thermal comfort calculations. Note that the following angle factor fractions must sum up to 1.0 The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#comfortviewfactorangles
        """

class ConstructionPropertyInternalHeatSource_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        thermal_source_present_after_layer_number: float,
        temperature_calculation_requested_after_layer_number: float,
        dimensions_for_the_ctf_calculation: float,
        tube_spacing: float,
        construction_name: str | None = ...,
        two_dimensional_temperature_calculation_position: float | None = 0,
    ) -> None:
        """Create a new ``ConstructionProperty:InternalHeatSource`` and add it to the document.

        Internal heat source to be attached to a construction layer

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#constructionpropertyinternalheatsource
        """

class RunPeriod_v9_0_to_v9_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        begin_year: float | None = ...,
        end_year: float | None = ...,
        day_of_week_for_start_day: Literal["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
        | None = ...,
        use_weather_file_holidays_and_special_days: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["", "No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
        treat_weather_as_actual: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``RunPeriod`` and add it to the document.

        Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-location-climate-weather-file-access/#runperiod
        """
