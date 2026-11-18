"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class CoilCoolingDXSingleSpeed_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_cooling_cop: float | None = 3,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        report_ashrae_standard_127_performance_ratings: Literal["", "No", "Yes"] | None = "No",
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxsinglespeed
        """

class ElectricEquipmentITEAirCooled_v9_6_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
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

        This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature. If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-internal-gains-people-lights-other/#electricequipmentiteaircooled
        """

class SizingZone_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["", "No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "", "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``Sizing:Zone`` and add it to the document.

        Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, heating, and ventilation air flows are then saved for system level and zone component design calculations.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-design-objects/#sizingzone
        """

class SizingZone_v24_2_to_v25_1:
    def __call__(
        self,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["", "No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "", "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
        zone_load_sizing_method: Literal[
            "", "Latent Load", "Sensible And Latent Load", "Sensible Load", "Sensible Load Only No Latent Load"
        ]
        | None = "Sensible Load Only No Latent Load",
        zone_latent_cooling_design_supply_air_humidity_ratio_input_method: Literal[
            "", "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_dehumidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_cooling_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_latent_heating_design_supply_air_humidity_ratio_input_method: Literal[
            "", "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_humidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_humidification_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_humidistat_dehumidification_set_point_schedule_name: str | None = ...,
        zone_humidistat_humidification_set_point_schedule_name: str | None = ...,
        type_of_space_sum_to_use: Literal["", "Coincident", "NonCoincident"] | None = "Coincident",
    ) -> None:
        """Create a new ``Sizing:Zone`` and add it to the document.

        Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, heating, and ventilation air flows are then saved for system level and zone component design calculations.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-design-objects/#sizingzone
        """

class OtherEquipment_v9_3_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = "None",
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_zone_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """

class BoilerHotWater_v9_0:
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
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 99.9,
        boiler_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        parasitic_electric_load: float | None = ...,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Boiler:HotWater`` and add it to the document.

        This boiler model is an adaptation of the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Boiler performance curves are generated by fitting catalog data to polynomial equations. A constant efficiency boiler may be modeled by leaving the normalized boiler efficiency curve name input blank.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-plant-equipment/#boilerhotwater
        """

class WaterHeaterMixed_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
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
        tank_volume: float | Literal["", "Autosize"] | None = 0,
        deadband_temperature_difference: float | None = 0,
        maximum_temperature_limit: float | None = ...,
        heater_control_type: Literal["", "Cycle", "Modulate"] | None = "Cycle",
        heater_maximum_capacity: float | Literal["Autosize"] | None = ...,
        heater_minimum_capacity: float | None = ...,
        heater_ignition_minimum_flow_rate: float | None = 0,
        heater_ignition_delay: float | None = 0,
        part_load_factor_curve_name: str | None = ...,
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
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        off_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_loss_fraction_to_zone: float | None = 1,
        on_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        on_cycle_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        source_side_flow_control_mode: Literal[
            "", "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``WaterHeater:Mixed`` and add it to the document.

        Water heater with well-mixed, single-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:PumpedCondenser.)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-water-heaters/#waterheatermixed
        """

class ZoneHVACHybridUnitaryHVAC_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_node_name: str,
        outdoor_air_node_name: str,
        supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        minimum_supply_air_temperature_schedule_name: str | None = ...,
        maximum_supply_air_temperature_schedule_name: str | None = ...,
        minimum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        maximum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        method_to_choose_controlled_inputs_and_part_runtime_fraction: Literal["", "Automatic", "User Defined"]
        | None = "Automatic",
        relief_node_name: str | None = ...,
        system_maximum_supply_air_flow_rate: float | None = ...,
        external_static_pressure_at_system_maximum_supply_air_flow_rate: float | None = ...,
        scaling_factor: float | None = 1,
        number_of_operating_modes: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = "Electricity",
        second_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = "None",
        third_fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = "None",
        objective_function_to_minimize: Literal["", "Electricity Use", "Second Fuel Use", "Third Fuel Use", "Water Use"]
        | None = "Electricity Use",
        design_specification_outdoor_air_object_name: str | None = ...,
        mode_0_name: str | None = ...,
        mode_0_supply_air_temperature_lookup_table_name: str | None = ...,
        mode_0_supply_air_humidity_ratio_lookup_table_name: str | None = ...,
        mode_0_system_electric_power_lookup_table_name: str | None = ...,
        mode_0_supply_fan_electric_power_lookup_table_name: str | None = ...,
        mode_0_external_static_pressure_lookup_table_name: str | None = ...,
        mode_0_system_second_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_third_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_water_use_lookup_table_name: str | None = ...,
        mode_0_outdoor_air_fraction: float | None = 0,
        mode_0_supply_air_mass_flow_rate_ratio: float | None = 0,
        modes: list[_g.ZoneHVACHybridUnitaryHVACModesItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:HybridUnitaryHVAC`` and add it to the document.

        Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operating mode, supply air flow rate, and outdoor air faction. Emperical lookup tables are required to map supply air temperature supply air humidity, electricity use, fuel uses, water use, fan electricity use, and external static pressure as a function of each indpednent varaible and each controlled input. In each timestep the model will choose one or more combinations of settings for mode, supply air flow rate, outdoor air faction, and part runtime fraction so as to satisfy zone requests for sensible cooling, heating, ventilation, and/or dehumidification with the least resource consumption. Equipment in this class may consume electricity, water, and up to two additional fuel types.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-zone-forced-air-units/#zonehvachybridunitaryhvac
        """

class CoilCoolingDXTwoSpeed_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        high_speed_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        high_speed_rated_sensible_heat_ratio: float | Literal["Autosize"],
        high_speed_rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        low_speed_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        low_speed_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        low_speed_rated_air_flow_rate: float | Literal["Autosize"],
        low_speed_total_cooling_capacity_function_of_temperature_curve_name: str,
        low_speed_energy_input_ratio_function_of_temperature_curve_name: str,
        availability_schedule_name: str | None = ...,
        high_speed_gross_rated_cooling_cop: float | None = 3,
        unit_internal_static_air_pressure: float | None = ...,
        low_speed_gross_rated_cooling_cop: float | None = 3,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        high_speed_evaporative_condenser_effectiveness: float | None = 0.9,
        high_speed_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        high_speed_evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = ...,
        low_speed_evaporative_condenser_effectiveness: float | None = 0.9,
        low_speed_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        low_speed_evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        low_speed_sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        low_speed_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:TwoSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-speed (or variable-speed). Requires two sets of performance data and will interpolate between speeds. Modeled as a single coil (multi-speed compressor or multiple compressors with row split or intertwined coil).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwospeed
        """

class SurfacePropertySurroundingSurfaces_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        sky_view_factor: float | None = 0.5,
        sky_temperature_schedule_name: str | None = ...,
        ground_view_factor: float | None = 0.5,
        ground_temperature_schedule_name: str | None = ...,
        surfaces: list[_g.SurfacePropertySurroundingSurfacesSurfacesItem] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:SurroundingSurfaces`` and add it to the document.

        This object defines a list of surrounding surfaces for an exterior surface.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-advanced-surface-concepts/#surfacepropertysurroundingsurfaces
        """

class GroundHeatExchangerSystem_v9_6_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        ground_thermal_conductivity: float,
        ground_thermal_heat_capacity: float,
        ghe_vertical_responsefactors_object_name: str | None = ...,
        g_function_calculation_method: Literal["", "UBHWTcalc", "UHFcalc"] | None = "UHFcalc",
        ghe_vertical_array_object_name: str | None = ...,
        vertical_well_locations: list[_g.GroundHeatExchangerSystemVerticalWellLocationsItem] = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:System`` and add it to the document.

        Models vertical ground heat exchangers systems using the response factor approach developed by Eskilson. Response factors are calculated using a finite line source model assuming uniform heat flux at the borehole wall if UHFcalc is specified, or uniform borehole wall temperature if UBHWTcalc is specified.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-condenser-equipment/#groundheatexchangersystem
        """

class SiteWaterMainsTemperature_v8_9:
    def __call__(
        self,
        /,
        *,
        calculation_method: Literal["Correlation", "Schedule"],
        temperature_schedule_name: str | None = ...,
        annual_average_outdoor_air_temperature: float | None = ...,
        maximum_difference_in_monthly_average_outdoor_air_temperatures: float | None = ...,
    ) -> None:
        """Create a new ``Site:WaterMainsTemperature`` and add it to the document.

        Used to calculate water mains temperatures delivered by underground water main pipes. Water mains temperatures are a function of outdoor climate conditions and vary with time of year.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-location-climate-weather-file-access/#sitewatermainstemperature
        """

class SiteWaterMainsTemperature_v9_0_to_v25_1:
    def __call__(
        self,
        /,
        *,
        calculation_method: Literal["", "Correlation", "CorrelationFromWeatherFile", "Schedule"]
        | None = "CorrelationFromWeatherFile",
        temperature_schedule_name: str | None = ...,
        annual_average_outdoor_air_temperature: float | None = ...,
        maximum_difference_in_monthly_average_outdoor_air_temperatures: float | None = ...,
    ) -> None:
        """Create a new ``Site:WaterMainsTemperature`` and add it to the document.

        Used to calculate water mains temperatures delivered by underground water main pipes. Water mains temperatures are a function of outdoor climate conditions and vary with time of year.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-location-climate-weather-file-access/#sitewatermainstemperature
        """

class GlobalGeometryRules_v8_9_to_v9_2:
    def __call__(
        self,
        /,
        *,
        starting_vertex_position: str,
        vertex_entry_direction: str,
        coordinate_system: str,
        daylighting_reference_point_coordinate_system: Literal["", "Absolute", "Relative", "World"] | None = "Relative",
        rectangular_surface_coordinate_system: Literal["", "Absolute", "Relative", "World"] | None = "Relative",
    ) -> None:
        """Create a new ``GlobalGeometryRules`` and add it to the document.

        Specifies the geometric rules used to describe the input of surface vertices and daylighting reference points.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-thermal-zone-description-geometry/#globalgeometryrules
        """

class ScheduleDayList_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        interpolate_to_timestep: Literal["", "Average", "Linear", "No"] | None = "No",
        minutes_per_item: float | None = ...,
        extensions: list[_g.ScheduleDayListExtensionsItem] = ...,
    ) -> None:
        """Create a new ``Schedule:Day:List`` and add it to the document.

        Schedule:Day:List will allow the user to list 24 hours worth of values, which can be sub-hourly in nature.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-schedules/#scheduledaylist
        """

class CoilWaterHeatingDesuperheater_v9_2_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        rated_inlet_water_temperature: float,
        rated_outdoor_air_temperature: float,
        maximum_inlet_water_temperature_for_heat_reclaim: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        tank_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        water_flow_rate: float,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        rated_heat_reclaim_recovery_efficiency: float | None = ...,
        heat_reclaim_efficiency_function_of_temperature_curve_name: str | None = ...,
        tank_object_type: Literal["", "WaterHeater:Mixed", "WaterHeater:Stratified"] | None = "WaterHeater:Mixed",
        water_pump_power: float | None = 0,
        fraction_of_pump_heat_to_water: float | None = 0.2,
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
    ) -> None:
        """Create a new ``Coil:WaterHeating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. This coil must be used with a water heater tank, see Water Heater:Mixed.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingdesuperheater
        """

class CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit_v8_9_to_v22_1:
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
        number_of_speeds: float | None = 2,
        nominal_speed_level: float | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["", "Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpvariablespeedequationfit
        """
