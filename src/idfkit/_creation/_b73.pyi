"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class RunPeriod:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
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
        first_hour_interpolation_starting_values: Literal["", "Hour1", "Hour24"] | None = "Hour24",
    ) -> None:
        """Create a new ``RunPeriod`` and add it to the document.

        Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#runperiod
        """

class WindowMaterialBlind:
    def __call__(
        self,
        name: str,
        /,
        *,
        slat_width: float,
        slat_separation: float,
        front_side_slat_beam_solar_reflectance: float,
        back_side_slat_beam_solar_reflectance: float,
        front_side_slat_diffuse_solar_reflectance: float,
        back_side_slat_diffuse_solar_reflectance: float,
        slat_beam_visible_transmittance: float,
        slat_orientation: Literal["", "Horizontal", "Vertical"] | None = "Horizontal",
        slat_thickness: float | None = 0.00025,
        slat_angle: float | None = 45,
        slat_conductivity: float | None = 221,
        slat_beam_solar_transmittance: float | None = 0,
        slat_diffuse_solar_transmittance: float | None = 0,
        front_side_slat_beam_visible_reflectance: float | None = ...,
        back_side_slat_beam_visible_reflectance: float | None = ...,
        slat_diffuse_visible_transmittance: float | None = 0,
        front_side_slat_diffuse_visible_reflectance: float | None = ...,
        back_side_slat_diffuse_visible_reflectance: float | None = ...,
        slat_infrared_hemispherical_transmittance: float | None = 0,
        front_side_slat_infrared_hemispherical_emissivity: float | None = 0.9,
        back_side_slat_infrared_hemispherical_emissivity: float | None = 0.9,
        blind_to_glass_distance: float | None = 0.05,
        blind_top_opening_multiplier: float | None = 0.5,
        blind_bottom_opening_multiplier: float | None = 0,
        blind_left_side_opening_multiplier: float | None = 0.5,
        blind_right_side_opening_multiplier: float | None = 0.5,
        minimum_slat_angle: float | None = 0,
        maximum_slat_angle: float | None = 180,
    ) -> None:
        """Create a new ``WindowMaterial:Blind`` and add it to the document.

        Window blind thermal properties

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialblind
        """

class SurfacePropertyHeatTransferAlgorithmMultipleSurface:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal[
            "AllExteriorFloors",
            "AllExteriorRoofs",
            "AllExteriorSurfaces",
            "AllExteriorWalls",
            "AllGroundContactSurfaces",
            "AllInteriorCeilings",
            "AllInteriorFloors",
            "AllInteriorSurfaces",
            "AllInteriorWalls",
        ],
        algorithm: Literal[
            "",
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
    ) -> None:
        """Create a new ``SurfaceProperty:HeatTransferAlgorithm:MultipleSurface`` and add it to the document.

        Determines which Heat Balance Algorithm will be used for a group of surface types Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage: CondFD (Conduction Finite Difference) Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheattransferalgorithmmultiplesurface
        """

class ZoneMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        source_zone_or_space_name: str,
        schedule_name: str | None = ...,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_receiving_temperature_schedule_name: str | None = ...,
        maximum_receiving_temperature_schedule_name: str | None = ...,
        minimum_source_temperature_schedule_name: str | None = ...,
        maximum_source_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneMixing`` and add it to the document.

        ZoneMixing is a simple air exchange from one zone or space to another. Note that this statement only affects the energy balance of the 'receiving' zone or space and will not produce any effect on the 'source' zone. Mixing statements can be complementary and include multiple zones, but the balancing of flows between zones is left to the user's discretion.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonemixing
        """

class ZoneRefrigerationDoorMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name_1: str,
        zone_or_space_name_2: str,
        schedule_name: str,
        door_height: float | None = 3,
        door_area: float | None = 9,
        door_protection_type: Literal["", "AirCurtain", "None", "StripCurtain"] | None = "None",
    ) -> None:
        """Create a new ``ZoneRefrigerationDoorMixing`` and add it to the document.

        Refrigeration Door Mixing is used for an opening between two zones (or spaces) that are at the same elevation but have different air temperatures. In this case, the mixing air flow between the two zones is determined by the density difference between the two zones. This would typically be used between two zones in a refrigerated warehouse that are controlled at different temperatures. It could also be used to model a door to a walk-in refrigerated space if that space were modeled as a zone instead of using the object Refrigeration:WalkIn.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonerefrigerationdoormixing
        """

class AnyZoneHVACEvaporativeCoolerUnit:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacevaporativecoolerunit
        """

class AnyCoilWaterHeatingAirToWaterHeatPumpWrapped:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "Yes",
        crankcase_heater_capacity: float | None = 0,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Wrapped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:WrappedCondenser system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpwrapped
        """

class AnySolarCollectorPerformanceIntegralCollectorStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        ics_collector_type: Literal["", "RectangularTank"] | None = "RectangularTank",
        gross_area: float | None = ...,
        collector_water_volume: float | None = ...,
        bottom_heat_loss_conductance: float | None = 0.4,
        side_heat_loss_conductance: float | None = 0.6,
        aspect_ratio: float | None = 0.8,
        collector_side_height: float | None = 0.2,
        thermal_mass_of_absorber_plate: float | None = 0,
        number_of_covers: int | None = 2,
        cover_spacing: float | None = 0.05,
        refractive_index_of_outer_cover: float | None = 1.526,
        extinction_coefficient_times_thickness_of_outer_cover: float | None = 0.045,
        emissivity_of_outer_cover: float | None = 0.88,
        refractive_index_of_inner_cover: float | None = 1.37,
        extinction_coefficient_times_thickness_of_the_inner_cover: float | None = 0.008,
        emissivity_of_inner_cover: float | None = 0.88,
        absorptance_of_absorber_plate: float | None = 0.96,
        emissivity_of_absorber_plate: float | None = 0.3,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:IntegralCollectorStorage`` and add it to the document.

        Thermal and optical performance parameters for a single glazed solar collector with integral storage unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformanceintegralcollectorstorage
        """

class HeatPumpWaterToWaterEquationFitHeating:
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
        heating_capacity_curve_name: str,
        heating_compressor_power_curve_name: str,
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
        companion_cooling_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Heating`` and add it to the document.

        simple water-water hp curve-fit model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitheating
        """

class DistrictHeatingWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        capacity_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DistrictHeating:Water`` and add it to the document.

        Centralized source of hot water, such as a district heating system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#districtheatingwater
        """

class EvaporativeFluidCoolerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate_fan_power: float | Literal["Autosize"],
        design_spray_water_flow_rate: float,
        performance_input_method: Literal[
            "StandardDesignCapacity", "UFactorTimesAreaAndDesignWaterFlowRate", "UserSpecifiedDesignCapacity"
        ],
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        standard_design_capacity: float | None = ...,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        user_specified_design_capacity: float | None = ...,
        design_entering_water_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_entering_air_temperature: float | None = 35,
        design_entering_air_wet_bulb_temperature: float | None = 25.6,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeFluidCooler:SingleSpeed`` and add it to the document.

        This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#evaporativefluidcoolersinglespeed
        """

class AnyThermalStorageChilledWaterStratified:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float,
        tank_height: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = ...,
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
        use_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        use_side_outlet_height: float | None = 0,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_heat_transfer_effectiveness: float | None = 1,
        source_side_availability_schedule_name: str | None = ...,
        source_side_inlet_height: float | None = 0,
        source_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        tank_recovery_time: float | None = 4,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
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
    ) -> None:
        """Create a new ``ThermalStorage:ChilledWater:Stratified`` and add it to the document.

        Chilled water storage with a stratified, multi-node tank. The chilled water is 'used' by drawing from the 'Use Side' of the water tank. The tank is indirectly charged by circulating cold water through the 'Source Side' of the water tank.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragechilledwaterstratified
        """

class PlantComponentUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_plant_loop_connections: int,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        plant_connection_1_loading_mode: Literal[
            "DemandsLoad",
            "MeetsLoadWithNominalCapacity",
            "MeetsLoadWithNominalCapacityHiOutLimit",
            "MeetsLoadWithNominalCapacityLowOutLimit",
            "MeetsLoadWithPassiveCapacity",
        ],
        plant_connection_1_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ],
        main_model_program_calling_manager_name: str | None = ...,
        plant_connection_1_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_1_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_2_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_2_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_2_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_2_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        plant_connection_3_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_3_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_3_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_3_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_4_inlet_node_name: str | None = ...,
        plant_connection_4_outlet_node_name: str | None = ...,
        plant_connection_4_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_4_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_4_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_4_simulation_program_calling_manager_name: str | None = ...,
        air_connection_inlet_node_name: str | None = ...,
        air_connection_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantComponent:UserDefined`` and add it to the document.

        Defines a generic plant component for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#plantcomponentuserdefined
        """

class AnyElectricLoadCenterStorageBattery:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        number_of_battery_modules_in_parallel: int | None = 1,
        number_of_battery_modules_in_series: int | None = 1,
        maximum_module_capacity: float | None = ...,
        initial_fractional_state_of_charge: float | None = 1,
        fraction_of_available_charge_capacity: float | None = ...,
        change_rate_from_bound_charge_to_available_charge: float | None = ...,
        fully_charged_module_open_circuit_voltage: float | None = ...,
        fully_discharged_module_open_circuit_voltage: float | None = ...,
        voltage_change_curve_name_for_charging: str | None = ...,
        voltage_change_curve_name_for_discharging: str | None = ...,
        module_internal_electrical_resistance: float | None = ...,
        maximum_module_discharging_current: float | None = ...,
        module_cut_off_voltage: float | None = ...,
        module_charge_rate_limit: float | None = 1,
        battery_life_calculation: Literal["", "No", "Yes"] | None = "No",
        number_of_cycle_bins: int | None = 10,
        battery_life_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Battery`` and add it to the document.

        Uses the kinetic battery model (KiBaM) to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstoragebattery
        """

class CurveQuadraticLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_y: float,
        coefficient5_x_y: float,
        coefficient6_x_2_y: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:QuadraticLinear`` and add it to the document.

        Quadratic-linear curve with two independent variables. Input consists of the curve name, the six coefficients, and min and max values for each of the independent variables. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = (C1 + C2*x + C3*x**2) + (C4 + C5*x + C6*x**2)*y

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvequadraticlinear
        """

class ComponentCostLineItem:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        line_item_type: Literal[
            "Chiller:Electric",
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:DX",
            "Coil:Heating:Fuel",
            "Construction",
            "Daylighting:Controls",
            "General",
            "Generator:Photovoltaic",
            "Lights",
            "Shading:Zone:Detailed",
        ],
        item_name: str,
        type: str | None = ...,
        object_end_use_key: str | None = ...,
        cost_per_each: float | None = ...,
        cost_per_area: float | None = ...,
        cost_per_unit_of_output_capacity: float | None = ...,
        cost_per_unit_of_output_capacity_per_cop: float | None = ...,
        cost_per_volume: float | None = ...,
        cost_per_volume_rate: float | None = ...,
        cost_per_energy_per_temperature_difference: float | None = ...,
        quantity: float | None = ...,
    ) -> None:
        """Create a new ``ComponentCost:LineItem`` and add it to the document.

        Each instance of this object creates a cost line item and will contribute to the total for a cost estimate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#componentcostlineitem
        """
