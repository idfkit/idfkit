"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class ElectricEquipmentITEAirCooled_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        cpu_power_input_function_of_loading_and_air_temperature_curve_name: str,
        design_fan_air_flow_rate_per_power_input: float,
        air_flow_function_of_loading_and_air_temperature_curve_name: str,
        fan_power_input_function_of_flow_curve_name: str,
        air_flow_calculation_method: Literal["", "FlowControlWithApproachTemperatures", "FlowFromSystem"]
        | None = "FlowFromSystem",
        design_power_input_calculation_method: Literal["", "Watts/Area", "Watts/Unit"] | None = "Watts/Unit",
        watts_per_unit: float | None = ...,
        number_of_units: float | None = 1,
        watts_per_zone_floor_area: float | None = ...,
        design_power_input_schedule_name: str | None = ...,
        cpu_loading_schedule_name: str | None = ...,
        design_fan_power_input_fraction: float | None = 0,
        design_entering_air_temperature: float | None = 15,
        environmental_class: Literal["", "A1", "A2", "A3", "A4", "B", "C", "None"] | None = "None",
        air_inlet_connection_type: Literal["", "AdjustedSupply", "RoomAirModel", "ZoneAirNode"]
        | None = "AdjustedSupply",
        air_inlet_room_air_model_node_name: str | None = ...,
        air_outlet_room_air_model_node_name: str | None = ...,
        supply_air_node_name: str | None = ...,
        design_recirculation_fraction: float | None = 0,
        recirculation_function_of_loading_and_supply_temperature_curve_name: str | None = ...,
        design_electric_power_supply_efficiency: float | None = 1,
        electric_power_supply_efficiency_function_of_part_load_ratio_curve_name: str | None = ...,
        fraction_of_electric_power_supply_losses_to_zone: float | None = 1,
        cpu_end_use_subcategory: str | None = "ITE-CPU",
        fan_end_use_subcategory: str | None = "ITE-Fans",
        electric_power_supply_end_use_subcategory: str | None = "ITE-UPS",
        supply_temperature_difference: float | None = ...,
        supply_temperature_difference_schedule: str | None = ...,
        return_temperature_difference: float | None = ...,
        return_temperature_difference_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ElectricEquipment:ITE:AirCooled`` and add it to the document.

        This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#electricequipmentiteaircooled
        """

class DesignSpecificationOutdoorAir_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_method: Literal[
            "",
            "AirChanges/Hour",
            "Flow/Area",
            "Flow/Person",
            "Flow/Zone",
            "IndoorAirQualityProcedure",
            "Maximum",
            "ProportionalControlBasedOnDesignOccupancy",
            "ProportionalControlBasedonOccupancySchedule",
            "Sum",
        ]
        | None = "Flow/Person",
        outdoor_air_flow_per_person: float | None = 0.00944,
        outdoor_air_flow_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_per_zone: float | None = 0,
        outdoor_air_flow_air_changes_per_hour: float | None = 0,
        outdoor_air_schedule_name: str | None = ...,
        proportional_control_minimum_outdoor_air_flow_rate_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DesignSpecification:OutdoorAir`` and add it to the document.

        This object is used to describe general outdoor air requirements which are referenced by other objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-design-objects/#designspecificationoutdoorair
        """

class AirLoopHVACUnitaryFurnaceHeatCool_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        furnace_air_inlet_node_name: str,
        furnace_air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "CoilSystem:Cooling:DX:HeatExchangerAssisted"],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        reheat_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ]
        | None = ...,
        reheat_coil_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:Unitary:Furnace:HeatCool`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional reheat coil for dehumidification control. Identical to AirLoopHVAC:UnitaryHeatCool.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryfurnaceheatcool
        """

class BoilerHotWater_v9_1_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: str,
        nominal_thermal_efficiency: float,
        boiler_water_inlet_node_name: str,
        boiler_water_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        efficiency_curve_temperature_evaluation_variable: Literal["EnteringBoiler", "LeavingBoiler"] | None = ...,
        normalized_boiler_efficiency_curve_name: str | None = ...,
        design_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 99.9,
        boiler_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        parasitic_electric_load: float | None = 0,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Boiler:HotWater`` and add it to the document.

        This boiler model is an adaptation of the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Boiler performance curves are generated by fitting catalog data to polynomial equations. A constant efficiency boiler may be modeled by leaving the normalized boiler efficiency curve name input blank.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-plant-equipment/#boilerhotwater
        """

class ChillerCombustionTurbine_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        coefficient_1_of_fuel_input_curve: float | None = ...,
        coefficient_2_of_fuel_input_curve: float | None = ...,
        coefficient_3_of_fuel_input_curve: float | None = ...,
        coefficient_1_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_2_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_3_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_1_of_exhaust_flow_curve: float | None = ...,
        coefficient_2_of_exhaust_flow_curve: float | None = ...,
        coefficient_3_of_exhaust_flow_curve: float | None = ...,
        coefficient_1_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_2_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_3_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        gas_turbine_engine_capacity: float | Literal["Autosize"] | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_steam_saturation_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        fuel_type: Literal[
            "", "Diesel", "FuelOil#1", "FuelOil#2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "PropaneGas"
        ]
        | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        turbine_engine_efficiency: float | None = 0.35,
    ) -> None:
        """Create a new ``Chiller:CombustionTurbine`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-plant-equipment/#chillercombustionturbine
        """

class ScheduleYear_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_week_name_1: str,
        start_month_1: float,
        start_day_1: float,
        end_month_1: float,
        end_day_1: float,
        schedule_type_limits_name: str | None = ...,
        schedule_week_name_2: str | None = ...,
        start_month_2: float | None = ...,
        start_day_2: float | None = ...,
        end_month_2: float | None = ...,
        end_day_2: float | None = ...,
        schedule_week_name_3: str | None = ...,
        start_month_3: float | None = ...,
        start_day_3: float | None = ...,
        end_month_3: float | None = ...,
        end_day_3: float | None = ...,
        schedule_week_name_4: str | None = ...,
        start_month_4: float | None = ...,
        start_day_4: float | None = ...,
        end_month_4: float | None = ...,
        end_day_4: float | None = ...,
        schedule_week_name_5: str | None = ...,
        start_month_5: float | None = ...,
        start_day_5: float | None = ...,
        end_month_5: float | None = ...,
        end_day_5: float | None = ...,
        schedule_week_name_6: str | None = ...,
        start_month_6: float | None = ...,
        start_day_6: float | None = ...,
        end_month_6: float | None = ...,
        end_day_6: float | None = ...,
        schedule_week_name_7: str | None = ...,
        start_month_7: float | None = ...,
        start_day_7: float | None = ...,
        end_month_7: float | None = ...,
        end_day_7: float | None = ...,
        schedule_week_name_8: str | None = ...,
        start_month_8: float | None = ...,
        start_day_8: float | None = ...,
        end_month_8: float | None = ...,
        end_day_8: float | None = ...,
        schedule_week_name_9: str | None = ...,
        start_month_9: float | None = ...,
        start_day_9: float | None = ...,
        end_month_9: float | None = ...,
        end_day_9: float | None = ...,
        schedule_week_name_10: str | None = ...,
        start_month_10: float | None = ...,
        start_day_10: float | None = ...,
        end_month_10: float | None = ...,
        end_day_10: float | None = ...,
        schedule_week_name_11: str | None = ...,
        start_month_11: float | None = ...,
        start_day_11: float | None = ...,
        end_month_11: float | None = ...,
        end_day_11: float | None = ...,
        schedule_week_name_12: str | None = ...,
        start_month_12: float | None = ...,
        start_day_12: float | None = ...,
        end_month_12: float | None = ...,
        end_day_12: float | None = ...,
        schedule_week_name_13: str | None = ...,
        start_month_13: float | None = ...,
        start_day_13: float | None = ...,
        end_month_13: float | None = ...,
        end_day_13: float | None = ...,
        schedule_week_name_14: str | None = ...,
        start_month_14: float | None = ...,
        start_day_14: float | None = ...,
        end_month_14: float | None = ...,
        end_day_14: float | None = ...,
        schedule_week_name_15: str | None = ...,
        start_month_15: float | None = ...,
        start_day_15: float | None = ...,
        end_month_15: float | None = ...,
        end_day_15: float | None = ...,
        schedule_week_name_16: str | None = ...,
        start_month_16: float | None = ...,
        start_day_16: float | None = ...,
        end_month_16: float | None = ...,
        end_day_16: float | None = ...,
        schedule_week_name_17: str | None = ...,
        start_month_17: float | None = ...,
        start_day_17: float | None = ...,
        end_month_17: float | None = ...,
        end_day_17: float | None = ...,
        schedule_week_name_18: str | None = ...,
        start_month_18: float | None = ...,
        start_day_18: float | None = ...,
        end_month_18: float | None = ...,
        end_day_18: float | None = ...,
        schedule_week_name_19: str | None = ...,
        start_month_19: float | None = ...,
        start_day_19: float | None = ...,
        end_month_19: float | None = ...,
        end_day_19: float | None = ...,
        schedule_week_name_20: str | None = ...,
        start_month_20: float | None = ...,
        start_day_20: float | None = ...,
        end_month_20: float | None = ...,
        end_day_20: float | None = ...,
        schedule_week_name_21: str | None = ...,
        start_month_21: float | None = ...,
        start_day_21: float | None = ...,
        end_month_21: float | None = ...,
        end_day_21: float | None = ...,
        schedule_week_name_22: str | None = ...,
        start_month_22: float | None = ...,
        start_day_22: float | None = ...,
        end_month_22: float | None = ...,
        end_day_22: float | None = ...,
        schedule_week_name_23: str | None = ...,
        start_month_23: float | None = ...,
        start_day_23: float | None = ...,
        end_month_23: float | None = ...,
        end_day_23: float | None = ...,
        schedule_week_name_24: str | None = ...,
        start_month_24: float | None = ...,
        start_day_24: float | None = ...,
        end_month_24: float | None = ...,
        end_day_24: float | None = ...,
        schedule_week_name_25: str | None = ...,
        start_month_25: float | None = ...,
        start_day_25: float | None = ...,
        end_month_25: float | None = ...,
        end_day_25: float | None = ...,
        schedule_week_name_26: str | None = ...,
        start_month_26: float | None = ...,
        start_day_26: float | None = ...,
        end_month_26: float | None = ...,
        end_day_26: float | None = ...,
    ) -> None:
        """Create a new ``Schedule:Year`` and add it to the document.

        A Schedule:Year contains from 1 to 52 week schedules

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-schedules/#scheduleyear
        """

class EnvironmentalImpactFactors_v8_9_to_v23_1:
    def __call__(
        self,
        /,
        *,
        district_heating_efficiency: float | None = 0.3,
        district_cooling_cop: float | None = 3,
        steam_conversion_efficiency: float | None = 0.25,
        total_carbon_equivalent_emission_factor_from_n2o: float | None = 80.7272,
        total_carbon_equivalent_emission_factor_from_ch4: float | None = 6.2727,
        total_carbon_equivalent_emission_factor_from_co2: float | None = 0.2727,
    ) -> None:
        """Create a new ``EnvironmentalImpactFactors`` and add it to the document.

        Used to help convert district and ideal energy use to a fuel type and provide total carbon equivalent with coefficients Also used in Source=>Site conversions.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/input-for-output/#environmentalimpactfactors
        """

class SizingParameters_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        heating_sizing_factor: float | None = 1,
        cooling_sizing_factor: float | None = 1,
        timesteps_in_averaging_window: float | None = ...,
    ) -> None:
        """Create a new ``Sizing:Parameters`` and add it to the document.

        Specifies global heating and cooling sizing factors/ratios. These ratios are applied at the zone level to all of the zone heating and cooling loads and air flow rates. Then these new loads and air flow rates are used to calculate the system level flow rates and capacities and are used in all component sizing calculations. Specifies the width (in load timesteps) of a moving average window which is used to smooth the peak load across more than one timestep.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-design-objects/#sizingparameters
        """

class HVACTemplateZoneWaterToAirHeatPump_v8_9_to_v23_1:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
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
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["", "Coil:Cooling:WaterToAirHeatPump:EquationFit"] | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3.5,
        heat_pump_heating_coil_type: Literal["", "Coil:Heating:WaterToAirHeatPump:EquationFit"] | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 4.2,
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
        dedicated_outdoor_air_system_name: str | None = ...,
        supplemental_heating_coil_type: Literal["", "Electric", "HotWater"] | None = "Electric",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:WaterToAirHeatPump`` and add it to the document.

        Water to Air Heat Pump to be used with HVACTemplate:Plant:MixedWaterLoop

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonewatertoairheatpump
        """

class DaylightingReferencePoint_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        x_coordinate_of_reference_point: float,
        y_coordinate_of_reference_point: float,
        z_coordinate_of_reference_point: float | None = 0.8,
    ) -> None:
        """Create a new ``Daylighting:ReferencePoint`` and add it to the document.

        Used by Daylighting:Controls to identify the reference point coordinates for each sensor. Reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-daylighting/#daylightingreferencepoint
        """

class WaterHeaterStratified_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float | Literal["Autosize"],
        tank_height: float | Literal["Autosize"],
        heater_1_setpoint_temperature_schedule_name: str,
        heater_2_setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        end_use_subcategory: str | None = "General",
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        heater_priority_control: Literal["", "MasterSlave", "Simultaneous"] | None = "MasterSlave",
        heater_1_deadband_temperature_difference: float | None = 0,
        heater_1_capacity: float | Literal["Autosize"] | None = ...,
        heater_1_height: float | None = ...,
        heater_2_deadband_temperature_difference: float | None = 0,
        heater_2_capacity: float | None = ...,
        heater_2_height: float | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        off_cycle_parasitic_height: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_height: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        skin_loss_fraction_to_zone: float | None = 1,
        off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_flue_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        use_side_inlet_height: float | None = 0,
        use_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        source_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_outlet_height: float | None = 0,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        number_of_nodes: int | None = 1,
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
        node_11_additional_loss_coefficient: float | None = 0,
        node_12_additional_loss_coefficient: float | None = 0,
        source_side_flow_control_mode: Literal[
            "", "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:Stratified`` and add it to the document.

        Water heater with stratified, multi-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:*.)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-water-heaters/#waterheaterstratified
        """

class CoilWaterHeatingAirToWaterHeatPumpVariableSpeed_v23_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_water_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        rated_water_heating_capacity_at_speed_1: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_reference_unit_water_pump_input_power_at_rated_conditions: float,
        speed_1_total_wh_capacity_function_of_temperature_curve_name: str,
        speed_1_total_wh_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_wh_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_cop_function_of_temperature_curve_name: str,
        speed_1_cop_function_of_air_flow_fraction_curve_name: str,
        speed_1_cop_function_of_water_flow_fraction_curve_name: str,
        number_of_speeds: int | None = 1,
        nominal_speed_level: int | None = 1,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["", "No", "Yes"] | None = "No",
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_water_heating_cop_at_speed_1: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_1: float | None = 0.85,
        rated_water_heating_capacity_at_speed_2: float | None = ...,
        rated_water_heating_cop_at_speed_2: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_2: float | None = 0.85,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_2_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_temperature_curve_name: str | None = ...,
        speed_2_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_3: float | None = ...,
        rated_water_heating_cop_at_speed_3: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_3: float | None = 0.85,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_3_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_temperature_curve_name: str | None = ...,
        speed_3_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_4: float | None = ...,
        rated_water_heating_cop_at_speed_4: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_4: float | None = 0.85,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_4_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_temperature_curve_name: str | None = ...,
        speed_4_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_5: float | None = ...,
        rated_water_heating_cop_at_speed_5: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_5: float | None = 0.85,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_5_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_temperature_curve_name: str | None = ...,
        speed_5_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_6: float | None = ...,
        rated_water_heating_cop_at_speed_6: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_6: float | None = 0.85,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_6_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_temperature_curve_name: str | None = ...,
        speed_6_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_7: float | None = ...,
        rated_water_heating_cop_at_speed_7: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_7: float | None = 0.85,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_7_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_temperature_curve_name: str | None = ...,
        speed_7_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_8: float | None = ...,
        rated_water_heating_cop_at_speed_8: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_8: float | None = 0.85,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_8_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_temperature_curve_name: str | None = ...,
        speed_8_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_9: float | None = ...,
        rated_water_heating_cop_at_speed_9: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_9: float | None = 0.85,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_9_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_temperature_curve_name: str | None = ...,
        speed_9_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_10: float | None = ...,
        rated_water_heating_cop_at_speed_10: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_10: float | None = 0.85,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_10_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_temperature_curve_name: str | None = ...,
        speed_10_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed`` and add it to the document.

        variable-speed Heat pump water heater (VSHPWH) heating coil, air-to-water direct-expansion (DX) system which includes a variable-speed water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpvariablespeed
        """

class LifeCycleCostRecurringCosts_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        category: Literal[
            "",
            "Maintenance",
            "MajorOverhaul",
            "MinorOverhaul",
            "Operation",
            "OtherOperational",
            "Repair",
            "Replacement",
        ]
        | None = "Maintenance",
        cost: float | None = ...,
        start_of_costs: Literal["", "BasePeriod", "ServicePeriod"] | None = "ServicePeriod",
        years_from_start: float | None = ...,
        months_from_start: float | None = ...,
        repeat_period_years: float | None = 1,
        repeat_period_months: float | None = 0,
        annual_escalation_rate: float | None = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:RecurringCosts`` and add it to the document.

        Recurring costs are costs that repeat over time on a regular schedule during the study period. If costs associated with equipment do repeat but not on a regular schedule, use LifeCycleCost:NonrecurringCost objects instead.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/lifecyclecost-recurringcosts/#lifecyclecostrecurringcosts
        """

class HeaderedPumpsVariableSpeed_v9_1_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: float | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        minimum_flow_rate_fraction: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HeaderedPumps:VariableSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-pumps/#headeredpumpsvariablespeed
        """

class Roof_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Roof`` and add it to the document.

        Allows for simplified entry of roofs (exterior). View Factor to Ground is automatically calculated.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#roof
        """

class ConvergenceLimits_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        minimum_system_timestep: float | None = ...,
        maximum_hvac_iterations: float | None = 20,
        minimum_plant_iterations: float | None = 2,
        maximum_plant_iterations: float | None = 8,
    ) -> None:
        """Create a new ``ConvergenceLimits`` and add it to the document.

        Specifies limits on HVAC system simulation timesteps and iterations. This item is an advanced feature that should be used only with caution.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-simulation-parameters/#convergencelimits
        """

class AirTerminalSingleDuctSeriesPIUReheat_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_air_flow_rate: float | Literal["Autosize"],
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
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
        """Create a new ``AirTerminal:SingleDuct:SeriesPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, series powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductseriespiureheat
        """

class ZoneHVACEquipmentList_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_distribution_scheme: Literal["", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"]
        | None = "SequentialLoad",
        equipment: list[_vd.ZoneHVACEquipmentListEquipmentItem_v9_2] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EquipmentList`` and add it to the document.

        List equipment in simulation order. Note that an ZoneHVAC:AirDistributionUnit or AirTerminal:SingleDuct:Uncontrolled object must be listed in this statement if there is a forced air system serving the zone from the air loop. Equipment is simulated in the order specified by Zone Equipment Cooling Sequence and Zone Equipment Heating or No-Load Sequence, depending on the thermostat request. For equipment of similar type, assign sequence 1 to the first system intended to serve that type of load. For situations where one or more equipment types has limited capacity or limited control, order the sequence so that the most controllable piece of equipment runs last. For example, with a dedicated outdoor air system (DOAS), the air terminal for the DOAS should be assigned Heating Sequence = 1 and Cooling Sequence = 1. Any other equipment should be assigned sequence 2 or higher so that it will see the net load after the DOAS air is added to the zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-zone-equipment/#zonehvacequipmentlist
        """

class ConstructionInternalSource_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_present_after_layer_number: float,
        temperature_calculation_requested_after_layer_number: float,
        dimensions_for_the_ctf_calculation: float,
        tube_spacing: float,
        outside_layer: str,
        two_dimensional_temperature_calculation_position: float | None = 0,
        layer_2: str | None = ...,
        layer_3: str | None = ...,
        layer_4: str | None = ...,
        layer_5: str | None = ...,
        layer_6: str | None = ...,
        layer_7: str | None = ...,
        layer_8: str | None = ...,
        layer_9: str | None = ...,
        layer_10: str | None = ...,
    ) -> None:
        """Create a new ``Construction:InternalSource`` and add it to the document.

        Start with outside layer and work your way to the inside Layer Up to 10 layers total Enter the material name for each layer

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.
        """

class ZoneHVACEvaporativeCoolerUnit_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_inlet_node_name: str,
        cooler_outlet_node_name: str,
        supply_air_fan_object_type: Literal[
            "Fan:ComponentModel", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ],
        supply_air_fan_name: str,
        design_supply_air_flow_rate: float | Literal["Autosize"],
        fan_placement: Literal["BlowThrough", "DrawThrough"],
        cooler_unit_control_method: Literal[
            "ZoneCoolingLoadOnOffCycling", "ZoneCoolingLoadVariableSpeedFan", "ZoneTemperatureDeadbandOnOffCycling"
        ],
        first_evaporative_cooler_object_type: Literal[
            "EvaporativeCooler:Direct:CelDekPad",
            "EvaporativeCooler:Direct:ResearchSpecial",
            "EvaporativeCooler:Indirect:CelDekPad",
            "EvaporativeCooler:Indirect:ResearchSpecial",
            "EvaporativeCooler:Indirect:WetCoil",
        ],
        first_evaporative_cooler_object_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        zone_relief_air_node_name: str | None = ...,
        throttling_range_temperature_difference: float | None = 1,
        cooling_load_control_threshold_heat_transfer_rate: float | None = 100,
        second_evaporative_cooler_object_type: Literal[
            "EvaporativeCooler:Direct:CelDekPad",
            "EvaporativeCooler:Direct:ResearchSpecial",
            "EvaporativeCooler:Indirect:CelDekPad",
            "EvaporativeCooler:Indirect:ResearchSpecial",
            "EvaporativeCooler:Indirect:WetCoil",
        ]
        | None = ...,
        second_evaporative_cooler_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EvaporativeCoolerUnit`` and add it to the document.

        Zone evaporative cooler. Forced-convection cooling-only unit with supply fan, 100% outdoor air supply. Optional relief exhaust node

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-zone-forced-air-units/#zonehvacevaporativecoolerunit
        """

class WindowShadingControl_v9_2_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        shading_type: Literal[
            "BetweenGlassBlind",
            "BetweenGlassShade",
            "ExteriorBlind",
            "ExteriorScreen",
            "ExteriorShade",
            "InteriorBlind",
            "InteriorShade",
            "SwitchableGlazing",
        ],
        shading_control_type: Literal[
            "AlwaysOff",
            "AlwaysOn",
            "MeetDaylightIlluminanceSetpoint",
            "OffNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnIfHighGlare",
            "OnIfHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighSolarOnWindow",
            "OnIfHighOutdoorAirTemperature",
            "OnIfHighSolarOnWindow",
            "OnIfHighZoneAirTempAndHighHorizontalSolar",
            "OnIfHighZoneAirTempAndHighSolarOnWindow",
            "OnIfHighZoneAirTemperature",
            "OnIfHighZoneCooling",
            "OnIfScheduleAllows",
            "OnNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnNightIfHeatingAndOffDay",
            "OnNightIfHeatingAndOnDayIfCooling",
            "OnNightIfLowInsideTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOnDayIfCooling",
        ],
        shading_control_sequence_number: float | None = 1,
        construction_with_shading_name: str | None = ...,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["", "No", "Yes"] | None = "No",
        glare_control_is_active: Literal["", "No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["", "BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        daylighting_control_object_name: str | None = ...,
        multiple_surface_control_type: Literal["", "Group", "Sequential"] | None = "Sequential",
        fenestration_surfaces: list[_g.WindowShadingControlFenestrationSurfacesItem] = ...,
    ) -> None:
        """Create a new ``WindowShadingControl`` and add it to the document.

        Specifies the type, location, and controls for window shades, window blinds, and switchable glazing. Referencing the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-thermal-zone-description-geometry/#windowshadingcontrol
        """

class HeatPumpWaterToWaterEIRHeating_v9_1_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EIR:Heating`` and add it to the document.

        An EIR formulated water to water heat pump model, heating operation

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.
        """

class PythonPluginOutputVariable_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        python_plugin_variable_name: str,
        type_of_data_in_variable: Literal["Averaged", "Metered", "Summed"],
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        units: str | None = ...,
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "Steam",
            "WaterUse",
            "WellWaterDrawn",
        ]
        | None = ...,
        group_type: Literal["Building", "HVAC", "Plant", "System"] | None = ...,
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ]
        | None = ...,
        end_use_subcategory: str | None = ...,
    ) -> None:
        """Create a new ``PythonPlugin:OutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from a Python Plugin variable
        """
