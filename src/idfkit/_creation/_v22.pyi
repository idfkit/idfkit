"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class AirTerminalDualDuctVAV_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        hot_air_inlet_node_name: str,
        cold_air_inlet_node_name: str,
        maximum_damper_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_fraction: float | None = 0.2,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:DualDuct:VAV`` and add it to the document.

        Central air system terminal unit, dual duct, variable volume.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-air-distribution-equipment/#airterminaldualductvav
        """

class AirConditionerVariableRefrigerantFlow_v9_6_to_v22_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_terminal_unit_list_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_condenser_inlet_node_temperature_in_cooling_mode: float | None = -6,
        maximum_condenser_inlet_node_temperature_in_cooling_mode: float | None = 43,
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
        minimum_condenser_inlet_node_temperature_in_heating_mode: float | None = -20,
        maximum_condenser_inlet_node_temperature_in_heating_mode: float | None = 16,
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
        minimum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None = ...,
        maximum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflow
        """

class RunPeriod_v9_0_to_v9_5:
    def __call__(
        self,
        name: str,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-location-climate-weather-file-access/#runperiod
        """

class LifeCycleCostUseAdjustment_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ],
        multipliers: list[_g.LifeCycleCostUseAdjustmentMultipliersItem] = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:UseAdjustment`` and add it to the document.

        Used by advanced users to adjust the energy or water use costs for future years. This should not be used for compensating for inflation but should only be used to increase the costs of energy or water based on assumed changes to the actual usage, such as anticipated changes in the future function of the building. The adjustments begin at the start of the service period.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/energyplus-economics/lifecyclecost-useadjustment/#lifecyclecostuseadjustment
        """

class ShadowCalculation_v9_3_to_v22_1:
    def __call__(
        self,
        /,
        *,
        shading_calculation_method: Literal["", "Imported", "PixelCounting", "PolygonClipping", "Scheduled"]
        | None = "PolygonClipping",
        shading_calculation_update_frequency_method: Literal["", "Periodic", "Timestep"] | None = "Periodic",
        shading_calculation_update_frequency: float | None = 20,
        maximum_figures_in_shadow_overlap_calculations: float | None = 15000,
        polygon_clipping_algorithm: Literal[
            "", "ConvexWeilerAtherton", "SlaterBarskyandSutherlandHodgman", "SutherlandHodgman"
        ]
        | None = "SutherlandHodgman",
        pixel_counting_resolution: float | None = 512,
        sky_diffuse_modeling_algorithm: Literal["", "DetailedSkyDiffuseModeling", "SimpleSkyDiffuseModeling"]
        | None = "SimpleSkyDiffuseModeling",
        output_external_shading_calculation_results: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_within_shading_zone_groups: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_from_shading_zone_groups_to_other_zones: Literal["", "No", "Yes"] | None = "No",
        shading_zone_groups: list[_g.ShadowCalculationShadingZoneGroupsItem] = ...,
    ) -> None:
        """Create a new ``ShadowCalculation`` and add it to the document.

        This object is used to control details of the solar, shading, and daylighting models

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-simulation-parameters/#shadowcalculation
        """

class HVACTemplateZoneFanCoil_v9_0:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["", "ChilledWater", "ChilledWaterDetailedFlatModel"] | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 14,
        heating_coil_type: Literal["", "HotWater"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 50,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        capacity_control_method: Literal[
            "ASHRAE90VariableFan",
            "ConstantFanVariableFlow",
            "CyclingFan",
            "VariableFanConstantFlow",
            "VariableFanVariableFlow",
        ]
        | None = ...,
        low_speed_supply_air_flow_ratio: float | None = 0.33,
        medium_speed_supply_air_flow_ratio: float | None = 0.66,
        outdoor_air_schedule_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:FanCoil`` and add it to the document.

        4 pipe fan coil unit with optional outdoor air.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonefancoil
        """

class ThermalStorageIceSimple_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        ice_storage_type: Literal["IceOnCoilExternal", "IceOnCoilInternal"],
        capacity: float,
        inlet_node_name: str,
        outlet_node_name: str,
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Simple`` and add it to the document.

        This ice storage model is a simplified model It requires a setpoint placed on the Chilled Water Side Outlet Node It should be placed in the chilled water supply side outlet branch followed by a pipe. Use the PlantEquipmentOperation:ComponentSetpoint plant operation scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-water-heaters/#thermalstorageicesimple
        """

class SizingPeriodDesignDay_v9_0_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        month: float,
        day_of_month: float,
        day_type: Literal[
            "CustomDay1",
            "CustomDay2",
            "Friday",
            "Holiday",
            "Monday",
            "Saturday",
            "SummerDesignDay",
            "Sunday",
            "Thursday",
            "Tuesday",
            "Wednesday",
            "WinterDesignDay",
        ],
        wind_speed: float,
        wind_direction: float,
        maximum_dry_bulb_temperature: float | None = ...,
        daily_dry_bulb_temperature_range: float | None = 0,
        dry_bulb_temperature_range_modifier_type: Literal[
            "", "DefaultMultipliers", "DifferenceSchedule", "MultiplierSchedule", "TemperatureProfileSchedule"
        ]
        | None = "DefaultMultipliers",
        dry_bulb_temperature_range_modifier_day_schedule_name: str | None = ...,
        humidity_condition_type: Literal[
            "",
            "DewPoint",
            "Enthalpy",
            "HumidityRatio",
            "RelativeHumiditySchedule",
            "WetBulb",
            "WetBulbProfileDefaultMultipliers",
            "WetBulbProfileDifferenceSchedule",
            "WetBulbProfileMultiplierSchedule",
        ]
        | None = "WetBulb",
        wetbulb_or_dewpoint_at_maximum_dry_bulb: float | None = ...,
        humidity_condition_day_schedule_name: str | None = ...,
        humidity_ratio_at_maximum_dry_bulb: float | None = ...,
        enthalpy_at_maximum_dry_bulb: float | None = ...,
        daily_wet_bulb_temperature_range: float | None = ...,
        barometric_pressure: float | None = ...,
        rain_indicator: Literal["", "No", "Yes"] | None = "No",
        snow_indicator: Literal["", "No", "Yes"] | None = "No",
        daylight_saving_time_indicator: Literal["", "No", "Yes"] | None = "No",
        solar_model_indicator: Literal["", "ASHRAEClearSky", "ASHRAETau", "ASHRAETau2017", "Schedule", "ZhangHuang"]
        | None = "ASHRAEClearSky",
        beam_solar_day_schedule_name: str | None = ...,
        diffuse_solar_day_schedule_name: str | None = ...,
        ashrae_clear_sky_optical_depth_for_beam_irradiance_taub_: float | None = 0,
        ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud_: float | None = 0,
        sky_clearness: float | None = 0,
        ashrae_clear_sky_optical_depth_for_beam_irradiance_taub: float | None = ...,
        ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud: float | None = ...,
    ) -> None:
        """Create a new ``SizingPeriod:DesignDay`` and add it to the document.

        The design day object creates the parameters for the program to create the 24 hour weather profile that can be used for sizing as well as running to test the other simulation parameters. Parameters in this include a date (month and day), a day type (which uses the appropriate schedules for either sizing or simple tests), min/max temperatures, wind speeds, and solar radiation values.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-location-climate-weather-file-access/#sizingperioddesignday
        """

class ZoneHVACPackagedTerminalHeatPump_v22_2_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal["Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed"],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_convergence_tolerance: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalHeatPump`` and add it to the document.

        Packaged terminal heat pump (PTHP). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalheatpump
        """

class PlantEquipmentOperationSchemes_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_scheme_1_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ],
        control_scheme_1_name: str,
        control_scheme_1_schedule_name: str,
        control_scheme_2_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_2_name: str | None = ...,
        control_scheme_2_schedule_name: str | None = ...,
        control_scheme_3_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_3_name: str | None = ...,
        control_scheme_3_schedule_name: str | None = ...,
        control_scheme_4_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_4_name: str | None = ...,
        control_scheme_4_schedule_name: str | None = ...,
        control_scheme_5_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_5_name: str | None = ...,
        control_scheme_5_schedule_name: str | None = ...,
        control_scheme_6_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_6_name: str | None = ...,
        control_scheme_6_schedule_name: str | None = ...,
        control_scheme_7_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_7_name: str | None = ...,
        control_scheme_7_schedule_name: str | None = ...,
        control_scheme_8_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_8_name: str | None = ...,
        control_scheme_8_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperationSchemes`` and add it to the document.

        Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first that is 'Scheduled' on. That is, if control scheme 1 is not 'on' and control scheme 2 is -- then control scheme 2 is selected. Only plant equipment should be listed on a Control Scheme for this item.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationschemes
        """

class ZoneHVACWaterToAirHeatPump_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit", "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit", "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        design_specification_multispeed_object_type: Literal["UnitarySystemPerformance:Multispeed"] | None = ...,
        design_specification_multispeed_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:WaterToAirHeatPump`` and add it to the document.

        Water-to-air heat pump. Forced-convection heating-cooling unit with supply fan, water-to-air cooling and heating coils, supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-zone-forced-air-units/#zonehvacwatertoairheatpump
        """

class FloorDetailed_v9_6_to_v24_2:
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
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[_g.FloorDetailedVerticesItem] = ...,
    ) -> None:
        """Create a new ``Floor:Detailed`` and add it to the document.

        Allows for detailed entry of floor heat transfer surfaces.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.2/io-reference/overview/group-thermal-zone-description-geometry/#floordetailed
        """

class MaterialPropertyVariableThermalConductivity_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        temperature_1: float,
        thermal_conductivity_1: float,
        temperature_2: float,
        thermal_conductivity_2: float,
        temperature_3: float,
        thermal_conductivity_3: float,
        temperature_4: float | None = ...,
        thermal_conductivity_4: float | None = ...,
        temperature_5: float | None = ...,
        thermal_conductivity_5: float | None = ...,
        temperature_6: float | None = ...,
        thermal_conductivity_6: float | None = ...,
        temperature_7: float | None = ...,
        thermal_conductivity_7: float | None = ...,
        temperature_8: float | None = ...,
        thermal_conductivity_8: float | None = ...,
        temperature_9: float | None = ...,
        thermal_conductivity_9: float | None = ...,
        temperature_10: float | None = ...,
        thermal_conductivity_10: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:VariableThermalConductivity`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity using piecewise linear temperature-conductivity function. HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-surface-construction-elements/#materialpropertyvariablethermalconductivity
        """

class CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit_v23_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_to_refrigerant_hx_water_inlet_node_name: str,
        water_to_refrigerant_hx_water_outlet_node_name: str,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_total_cooling_capacity: float,
        speed_1_reference_unit_gross_rated_sensible_heat_ratio: float,
        speed_1_reference_unit_gross_rated_cooling_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["", "Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        fan_delay_time: float | None = 60,
        flag_for_using_hot_gas_reheat_0_or_1: float | None = 0,
        speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_2_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_3_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_4_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_5_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_5_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_6_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_6_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_7_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_7_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_8_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_8_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_9_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_9_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_10_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_10_waste_heat_function_of_temperature_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpvariablespeedequationfit
        """

class PythonPluginSearchPaths_v9_4_to_v9_6:
    def __call__(
        self,
        name: str,
        /,
        *,
        add_current_working_directory_to_search_path: Literal["", "No", "Yes"] | None = "Yes",
        add_input_file_directory_to_search_path: Literal["", "No", "Yes"] | None = "Yes",
        py_search_paths: list[_vd.PythonPluginSearchPathsPySearchPathsItem_v9_4_to_v9_6] = ...,
    ) -> None:
        """Create a new ``PythonPlugin:SearchPaths`` and add it to the document.

        Add directories to the search path for Python plugin modules The directory containing the EnergyPlus executable file is automatically added so that the Python interpreter can find the packaged up pyenergyplus Python package. By default, the current working directory and input file directory are also added to the search path. However, this object allows modifying this behavior. With this object, searching these directories can be disabled, and users can add supplemental search paths that point to libraries of plugin scripts.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.6/io-reference/overview/group-python-plugins/#pythonpluginsearchpaths
        """

class ZoneHVACBaseboardRadiantConvectiveSteam_v9_5_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_steam_flow_rate: float | Literal["Autosize"],
        design_object: str | None = ...,
        availability_schedule_name: str | None = ...,
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        degree_of_subcooling: float | None = 5,
        surface_fractions: list[_g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Steam`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivesteam
        """
