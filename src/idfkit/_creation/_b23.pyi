"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyZoneAirMassFlowConservation:
    def __call__(
        self,
        /,
        *,
        infiltration_balancing_method: Literal["", "AddInfiltrationFlow", "AdjustInfiltrationFlow", "None"]
        | None = "AddInfiltrationFlow",
        infiltration_balancing_zones: Literal["", "AllZones", "MixingSourceZonesOnly"] | None = "MixingSourceZonesOnly",
    ) -> None:
        """Create a new ``ZoneAirMassFlowConservation`` and add it to the document.

        Enforces the zone air mass flow balance by either adjusting zone mixing object flow only, adjusting zone total return flow only, zone mixing and the zone total return flows, or adjusting the zone total return and zone mixing object flows. Zone infiltration flow air flow is increased or decreased depending user selection in the infiltration treatment method. If either of zone mixing or zone return flow adjusting methods or infiltration is active, then the zone air mass flow balance calculation will attempt to enforce conservation of mass for each zone. If flow balancing method is 'None' and infiltration is 'None', then the zone air mass flow calculation defaults to assume self-balanced simple flow mixing and infiltration objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneairmassflowconservation
        """

class AnySizingPeriodWeatherFileDays:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        day_of_week_for_start_day: Literal[
            "",
            "CustomDay1",
            "CustomDay2",
            "Friday",
            "Monday",
            "Saturday",
            "SummerDesignDay",
            "Sunday",
            "Thursday",
            "Tuesday",
            "Wednesday",
            "WinterDesignDay",
        ]
        | None = "Monday",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_rain_and_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``SizingPeriod:WeatherFileDays`` and add it to the document.

        Use a weather file period for design sizing calculations.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sizingperiodweatherfiledays
        """

class ConstructionAssignmentSet:
    def __call__(
        self,
        name: str,
        /,
        *,
        exterior_surface_construction_assignments_name: str | None = ...,
        interior_surface_construction_assignments_name: str | None = ...,
        ground_contact_surface_construction_assignments_name: str | None = ...,
        exterior_subsurface_construction_assignments_name: str | None = ...,
        interior_subsurface_construction_assignments_name: str | None = ...,
        interior_partition_construction_name: str | None = ...,
        adiabatic_surface_construction_name: str | None = ...,
    ) -> None:
        """Create a new ``ConstructionAssignmentSet`` and add it to the document.

        Defines a set of construction assignments for surfaces and sub-surfaces based on their type and outside boundary condition. Can be referenced by Building or Space objects. Space-level assignments take precedence over Building-level.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionassignmentset
        """

class FloorInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Floor:Interzone`` and add it to the document.

        Allows for simplified entry of floors using adjacent zone (interzone) heat transfer - adjacent surface should be a ceiling.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#floorinterzone
        """

class SurfacePropertySolarIncidentInside:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        construction_name: str,
        inside_surface_incident_sun_solar_radiation_schedule_name: str,
    ) -> None:
        """Create a new ``SurfaceProperty:SolarIncidentInside`` and add it to the document.

        Used to provide incident solar radiation on the inside of the surface. Reference surface-construction pair and if that pair is used in a simulation, then program will use value provided in schedule instead of calculating it.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertysolarincidentinside
        """

class GroundHeatTransferBasementEquivAutoGrid:
    def __call__(
        self,
        /,
        *,
        clearance_distance_from_outside_of_wall_to_edge_of_3_d_ground_domain: float | None = 15,
        slabdepth_thickness_of_the_floor_slab: float | None = 0.1,
        basedepth_depth_of_the_basement_wall_below_grade: float | None = 2,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:EquivAutoGrid`` and add it to the document.

        EquivAutoGrid necessary when EquivSizing=TRUE, TRUE is is the normal case.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementequivautogrid
        """

class AnyOtherEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
        ]
        | None = "None",
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """

class DaylightingDELightComplexFenestration:
    def __call__(
        self,
        name: str,
        /,
        *,
        complex_fenestration_type: str,
        building_surface_name: str,
        window_name: str,
        fenestration_rotation: float | None = 0,
    ) -> None:
        """Create a new ``Daylighting:DELight:ComplexFenestration`` and add it to the document.

        Used for DElight Complex Fenestration of all types

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingdelightcomplexfenestration
        """

class ExteriorWaterEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_name: str,
        design_level: float,
        fuel_use_type: Literal["", "Water"] | None = "Water",
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Exterior:WaterEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-exterior-energy-use-equipment/#exteriorwaterequipment
        """

class AnyZoneHVACPackagedTerminalHeatPump:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalheatpump
        """

class ZoneHVACLowTemperatureRadiantConstantFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_object: str,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        rated_flow_rate: float | Literal["Autosize"] | None = ...,
        pump_flow_rate_schedule_name: str | None = ...,
        rated_pump_head: float | None = 179352,
        rated_power_consumption: float | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_high_water_temperature_schedule_name: str | None = ...,
        heating_low_water_temperature_schedule_name: str | None = ...,
        heating_high_control_temperature_schedule_name: str | None = ...,
        heating_low_control_temperature_schedule_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_high_water_temperature_schedule_name: str | None = ...,
        cooling_low_water_temperature_schedule_name: str | None = ...,
        cooling_high_control_temperature_schedule_name: str | None = ...,
        cooling_low_control_temperature_schedule_name: str | None = ...,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water temperature circulating through the unit.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantconstantflow
        """

class ZoneHVACVentilatedSlab:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        outdoor_air_control_type: Literal["FixedAmount", "FixedTemperature", "VariablePercent"],
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"],
        minimum_outdoor_air_schedule_name: str,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_fraction_or_temperature_schedule_name: str,
        heating_high_air_temperature_schedule_name: str,
        heating_low_air_temperature_schedule_name: str,
        heating_high_control_temperature_schedule_name: str,
        heating_low_control_temperature_schedule_name: str,
        cooling_high_air_temperature_schedule_name: str,
        cooling_low_air_temperature_schedule_name: str,
        cooling_high_control_temperature_schedule_name: str,
        cooling_low_control_temperature_schedule_name: str,
        return_air_node_name: str,
        slab_in_node_name: str,
        outdoor_air_node_name: str,
        relief_air_node_name: str,
        outdoor_air_mixer_outlet_node_name: str,
        fan_outlet_node_name: str,
        fan_name: str,
        coil_option_type: Literal["Cooling", "Heating", "HeatingAndCooling", "None"],
        availability_schedule_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        system_configuration_type: Literal["", "SeriesSlabs", "SlabAndZone", "SlabOnly"] | None = "SlabOnly",
        hollow_core_inside_diameter: float | None = 0.05,
        hollow_core_length: float | None = ...,
        number_of_cores: float | None = ...,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "SurfaceTemperature",
            "ZoneAirDewPointTemperature",
        ]
        | None = "OutdoorDryBulbTemperature",
        zone_supply_air_node_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        heating_coil_name: str | None = ...,
        hot_water_or_steam_inlet_node_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ]
        | None = ...,
        cooling_coil_name: str | None = ...,
        cold_water_inlet_node_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:VentilatedSlab`` and add it to the document.

        Ventilated slab system where outdoor air flows through hollow cores in a building surface (wall, ceiling, or floor).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacventilatedslab
        """

class AnyAirTerminalSingleDuctVAVHeatAndCoolNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with no reheat coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavheatandcoolnoreheat
        """

class AnyAirTerminalSingleDuctParallelPIUReheat:
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
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ParallelPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, parallel powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductparallelpiureheat
        """

class AirTerminalDualDuctVAVOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        outdoor_air_inlet_node_name: str,
        maximum_terminal_air_flow_rate: float | Literal["Autosize"],
        design_specification_outdoor_air_object_name: str,
        availability_schedule_name: str | None = ...,
        recirculated_air_inlet_node_name: str | None = ...,
        per_person_ventilation_rate_mode: Literal["CurrentOccupancy", "DesignOccupancy"] | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:DualDuct:VAV:OutdoorAir`` and add it to the document.

        Central air system terminal unit, dual duct, variable volume with special controls. One VAV duct is controlled to supply ventilation air and the other VAV duct is controlled to meet the zone cooling load.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminaldualductvavoutdoorair
        """

class AnyCoilCoolingDXTwoSpeed:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwospeed
        """

class CoilCoolingWaterToAirHeatPumpEquationFit:
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
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        total_cooling_capacity_curve_name: str,
        sensible_cooling_capacity_curve_name: str,
        cooling_power_consumption_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        rated_entering_water_temperature: float | None = 30,
        rated_entering_air_dry_bulb_temperature: float | None = 27,
        rated_entering_air_wet_bulb_temperature: float | None = 19,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        fan_delay_time: float | None = 60,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

class CoilSystemHeatingDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_coil_object_type: Literal["Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed"],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``CoilSystem:Heating:DX`` and add it to the document.

        Virtual container component that consists of a DX heating coil (heat pump) and its associated controls. This control object supports two different types of DX heating coils and may be placed directly in an air loop branch or outdoor air equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemheatingdx
        """

class DehumidifierDesiccantSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        desiccant_heat_exchanger_object_type: Literal["HeatExchanger:Desiccant:BalancedFlow"],
        desiccant_heat_exchanger_name: str,
        sensor_node_name: str,
        regeneration_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        regeneration_air_fan_name: str,
        availability_schedule_name: str | None = ...,
        regeneration_air_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        regeneration_air_heater_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        regeneration_air_heater_name: str | None = ...,
        regeneration_inlet_air_setpoint_temperature: float | None = 46,
        companion_cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
        ]
        | None = ...,
        companion_cooling_coil_name: str | None = ...,
        companion_cooling_coil_upstream_of_dehumidifier_process_inlet: Literal["", "No", "Yes"] | None = "No",
        companion_coil_regeneration_air_heating: Literal["", "No", "Yes"] | None = "No",
        exhaust_fan_maximum_flow_rate: float | None = ...,
        exhaust_fan_maximum_power: float | None = ...,
        exhaust_fan_power_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Dehumidifier:Desiccant:System`` and add it to the document.

        This compound object models a desiccant heat exchanger, an optional heater, and associated fans. The process air stream is the air which is dehumidified. The regeneration air stream is the air which is heated to regenerate the desiccant. The desiccant heat exchanger transfers both sensible and latent energy between the process and regeneration air streams. The desiccant dehumidifier is typically used in an AirLoopHVAC:OutdoorAirSystem, but can also be specified in any AirLoopHVAC.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-humidifiers-and-dehumidifiers/#dehumidifierdesiccantsystem
        """

class AirLoopHVACUnitaryHeatCool:
    def __call__(
        self,
        name: str,
        /,
        *,
        unitary_system_air_inlet_node_name: str,
        unitary_system_air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
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
        """Create a new ``AirLoopHVAC:UnitaryHeatCool`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional reheat coil for dehumidification control. Identical to AirLoopHVAC:Unitary:Furnace:HeatCool.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatcool
        """

class AnyAirLoopHVACUnitaryHeatPumpAirToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed", "CoilSystem:IntegratedHeatPump:AirSource"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir`` and add it to the document.

        Unitary heat pump system, heating and cooling, single-speed with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), and supplemental heating coil (gas, electric, hot water, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoair
        """

class AirLoopHVACUnitaryHeatPumpAirToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed", "CoilSystem:IntegratedHeatPump:AirSource"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        dx_heating_coil_sizing_ratio: float | None = 1,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir`` and add it to the document.

        Unitary heat pump system, heating and cooling, single-speed with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), and supplemental heating coil (gas, electric, hot water, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoair
        """

class AnyAirConditionerVariableRefrigerantFlowFluidTemperatureControlHR:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_terminal_unit_list_name: str,
        outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R410A",
        rated_evaporative_capacity: float | Literal["", "Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_only_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_only_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_only_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_only_mode: float | None = 16,
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -20,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 43,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["", "ConstantTemp", "VariableTemp"]
        | None = "VariableTemp",
        reference_evaporating_temperature_for_indoor_unit: float | None = 6,
        reference_condensing_temperature_for_indoor_unit: float | None = 44,
        variable_evaporating_temperature_minimum_for_indoor_unit: float | None = 4,
        variable_evaporating_temperature_maximum_for_indoor_unit: float | None = 13,
        variable_condensing_temperature_minimum_for_indoor_unit: float | None = 42,
        variable_condensing_temperature_maximum_for_indoor_unit: float | None = 46,
        outdoor_unit_evaporator_reference_superheating: float | None = 3,
        outdoor_unit_condenser_reference_subcooling: float | None = 5,
        outdoor_unit_evaporator_rated_bypass_factor: float | None = 0.4,
        outdoor_unit_condenser_rated_bypass_factor: float | None = 0.2,
        difference_between_outdoor_unit_evaporating_temperature_and_outdoor_air_temperature_in_heat_recovery_mode: float
        | None = 5,
        outdoor_unit_heat_exchanger_capacity_ratio: float | None = 0.3,
        outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None = 0.00425,
        outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None = ...,
        diameter_of_main_pipe_for_suction_gas: float | None = 0.0762,
        diameter_of_main_pipe_for_discharge_gas: float | None = 0.0762,
        length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 30,
        equivalent_length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 36,
        height_difference_between_outdoor_unit_and_indoor_units: float | None = 5,
        main_pipe_insulation_thickness: float | None = 0.02,
        main_pipe_insulation_thermal_conductivity: float | None = 0.032,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        initial_heat_recovery_cooling_capacity_fraction: float | None = 1,
        heat_recovery_cooling_capacity_time_constant: float | None = 0,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
        compressor_maximum_delta_pressure: float | None = 4500000,
        compressor_inverter_efficiency: float | None = 0.95,
        compressor_evaporative_capacity_correction_factor: float | None = 1,
        number_of_compressor_loading_index_entries: int | None = 2,
        loading_indices: list[
            _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHRLoadingIndicesItem
        ] = ...,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR`` and add it to the document.

        This is a key object in the new physics based VRF Heat Recovery (HR) model applicable for Fluid Temperature Control. It describes the VRF HR system excluding the performance of indoor units. Indoor units are modeled separately in the ZoneHVAC:TerminalUnit:VariableRefrigerantFlow object

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflowfluidtemperaturecontrolhr
        """

class AirLoopHVACZoneMixer:
    def __call__(
        self, name: str, /, *, outlet_node_name: str, nodes: list[_g.AirLoopHVACZoneMixerNodesItem] = ...
    ) -> None:
        """Create a new ``AirLoopHVAC:ZoneMixer`` and add it to the document.

        Mix N inlet air streams into one (currently 500 per air loop, but extensible). Node names cannot be duplicated within a single zone mixer (AirLoopHVAC:ZoneMixer) list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvaczonemixer
        """

class SolarCollectorPerformancePhotovoltaicThermalBIPVT:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        boundary_conditions_model_name: str,
        effective_plenum_gap_thickness_behind_pv_modules: float,
        availability_schedule_name: str | None = ...,
        pv_cell_normal_transmittance_absorptance_product: float | None = 0.957,
        backing_material_normal_transmittance_absorptance_product: float | None = 0.87,
        cladding_normal_transmittance_absorptance_product: float | None = 0.85,
        fraction_of_collector_gross_area_covered_by_pv_module: float | None = 0.85,
        fraction_of_pv_cell_area_to_pv_module_area: float | None = 0.9,
        pv_module_top_thermal_resistance: float | None = 0.0044,
        pv_module_bottom_thermal_resistance: float | None = 0.0039,
        pv_module_front_longwave_emissivity: float | None = 0.85,
        pv_module_back_longwave_emissivity: float | None = 0.9,
        glass_thickness: float | None = 0.002,
        glass_refraction_index: float | None = 1.526,
        glass_extinction_coefficient: float | None = 4,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:PhotovoltaicThermal:BIPVT`` and add it to the document.

        Thermal performance parameters for Building-Integrated Photovoltaic-Thermal (BIPVT) solar collector.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformancephotovoltaicthermalbipvt
        """

class SolarCollectorPerformanceIntegralCollectorStorage:
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

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformanceintegralcollectorstorage
        """

class ChillerAbsorption:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_pumping_power: float | Literal["Autosize"],
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        condenser_outlet_node_name: str,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None = ...,
        coefficient_2_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None = ...,
        coefficient_3_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None = ...,
        coefficient_1_of_the_pump_electric_use_part_load_ratio_curve: float | None = ...,
        coefficient_2_of_the_pump_electric_use_part_load_ratio_curve: float | None = ...,
        coefficient_3_of_the_pump_electric_use_part_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        generator_inlet_node_name: str | None = ...,
        generator_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        generator_heat_source_type: Literal["", "HotWater", "Steam"] | None = "Steam",
        design_generator_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        degree_of_subcooling_in_steam_generator: float | None = 1,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``Chiller:Absorption`` and add it to the document.

        This indirect absorption chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Two sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerabsorption
        """

class CoolingTowerVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        model_type: Literal["", "CoolToolsCrossFlow", "CoolToolsUserDefined", "YorkCalc", "YorkCalcUserDefined"]
        | None = "YorkCalc",
        model_coefficient_name: str | None = ...,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | None = 3.9,
        design_range_temperature: float | None = 5.6,
        fan_power_ratio_function_of_air_flow_rate_ratio_curve_name: str | None = ...,
        minimum_air_flow_rate_ratio: float | None = 0.2,
        fraction_of_tower_capacity_in_free_convection_regime: float | None = 0.125,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = "MaximalCell",
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:VariableSpeed`` and add it to the document.

        This open wet tower model is based on purely empirical algorithms derived from manufacturer's performance data or field measurements. The user can select from two existing algorithms (CoolTools or YorkCalc), or they can enter their own correlation for approach temperature by using a variable speed tower model coefficient object. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowervariablespeed
        """

class AnyThermalStorageIceSimple:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstorageicesimple
        """

class AnyPlantEquipmentOperationSchemes:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationschemes
        """

class ExternalInterface:
    def __call__(
        self,
        /,
        *,
        name_of_external_interface: Literal[
            "FunctionalMockupUnitExport", "FunctionalMockupUnitImport", "PtolemyServer"
        ],
    ) -> None:
        """Create a new ``ExternalInterface`` and add it to the document.

        This object activates the external interface of EnergyPlus. If the object ExternalInterface is present, then all ExtnernalInterface:* objects will receive their values from the BCVTB interface or from FMUs at each zone time step. If this object is not present, then the values of these objects will be fixed at the value declared in the 'initial value' field of the corresponding object, and a warning will be written to the EnergyPlus error file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterface
        """

class RefrigerationCondenserAirCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_effective_total_heat_rejection_rate_curve_name: str | None = ...,
        rated_subcooling_temperature_difference: float | None = 0,
        condenser_fan_speed_control_type: Literal["", "Fixed", "FixedLinear", "TwoSpeed", "VariableSpeed"]
        | None = "Fixed",
        rated_fan_power: float | None = 250,
        minimum_fan_air_flow_ratio: float | None = 0.2,
        air_inlet_node_name_or_zone_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        condenser_refrigerant_operating_charge_inventory: float | None = 0,
        condensate_receiver_refrigerant_inventory: float | None = 0,
        condensate_piping_refrigerant_inventory: float | None = 0,
    ) -> None:
        """Create a new ``Refrigeration:Condenser:AirCooled`` and add it to the document.

        Air cooled condenser for a refrigeration system (Refrigeration:System).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcondenseraircooled
        """

class RefrigerationCondenserCascade:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_condensing_temperature: float,
        rated_effective_total_heat_rejection_rate: float,
        rated_approach_temperature_difference: float | None = 3,
        condensing_temperature_control_type: Literal["", "Fixed", "Float"] | None = "Fixed",
        condenser_refrigerant_operating_charge_inventory: float | None = ...,
        condensate_receiver_refrigerant_inventory: float | None = ...,
        condensate_piping_refrigerant_inventory: float | None = ...,
    ) -> None:
        """Create a new ``Refrigeration:Condenser:Cascade`` and add it to the document.

        Cascade condenser for a refrigeration system (Refrigeration:System). The cascade condenser is unlike the other condenser options because it rejects heat to another, higher-temperature, refrigeration system. That is, the cascade condenser acts as a heat rejection object for one system, but acts as a refrigeration load for another system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcondensercascade
        """

class RefrigerationGasCoolerAirCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_total_heat_rejection_rate_curve_name: str,
        gas_cooler_fan_speed_control_type: Literal["", "Fixed", "FixedLinear", "TwoSpeed", "VariableSpeed"]
        | None = "Fixed",
        rated_fan_power: float | None = 5000,
        minimum_fan_air_flow_ratio: float | None = 0.2,
        transition_temperature: float | None = 27,
        transcritical_approach_temperature: float | None = 3,
        subcritical_temperature_difference: float | None = 10,
        minimum_condensing_temperature: float | None = 10,
        air_inlet_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        gas_cooler_refrigerant_operating_charge_inventory: float | None = 0,
        gas_cooler_receiver_refrigerant_inventory: float | None = 0,
        gas_cooler_outlet_piping_refrigerant_inventory: float | None = 0,
    ) -> None:
        """Create a new ``Refrigeration:GasCooler:AirCooled`` and add it to the document.

        The transcritical refrigeration system requires a single gas cooler to reject the system heat.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationgascooleraircooled
        """

class ElectricLoadCenterGenerators:
    def __call__(
        self, name: str, /, *, generator_outputs: list[_g.ElectricLoadCenterGeneratorsGeneratorOutputsItem] = ...
    ) -> None:
        """Create a new ``ElectricLoadCenter:Generators`` and add it to the document.

        List of electric power generators to include in the simulation including the name and type of each generators along with availability schedule, rated power output, and thermal-to-electrical power ratio.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcentergenerators
        """

class FaultModelHumidistatOffset:
    def __call__(
        self,
        name: str,
        /,
        *,
        humidistat_name: str,
        humidistat_offset_type: Literal["", "ThermostatOffsetDependent", "ThermostatOffsetIndependent"]
        | None = "ThermostatOffsetIndependent",
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_humidistat_offset: float | None = 5,
        related_thermostat_offset_fault_name: str | None = ...,
    ) -> None:
        """Create a new ``FaultModel:HumidistatOffset`` and add it to the document.

        This object describes fault of humidistat offset

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelhumidistatoffset
        """

class FaultModelFoulingEvaporativeCooler:
    def __call__(
        self,
        name: str,
        /,
        *,
        evaporative_cooler_object_type: Literal["EvaporativeCooler:Indirect:WetCoil"],
        evaporative_cooler_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        fouling_factor: float | None = 1,
    ) -> None:
        """Create a new ``FaultModel:Fouling:EvaporativeCooler`` and add it to the document.

        This object describes the fouling fault of the wetted coil evaporative cooler

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelfoulingevaporativecooler
        """

class AnyLifeCycleCostRecurringCosts:
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
        years_from_start: int | None = ...,
        months_from_start: int | None = ...,
        repeat_period_years: int | None = 1,
        repeat_period_months: int | None = 0,
        annual_escalation_rate: float | None = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:RecurringCosts`` and add it to the document.

        Recurring costs are costs that repeat over time on a regular schedule during the study period. If costs associated with equipment do repeat but not on a regular schedule, use LifeCycleCost:NonrecurringCost objects instead.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-recurringcosts/#lifecyclecostrecurringcosts
        """

class MeterCustomDecrement:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_meter_name: str,
        resource_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ]
        | None = ...,
        variable_details: list[_g.MeterCustomDecrementVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Meter:CustomDecrement`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:CustomDecrement cannot reference another Meter:CustomDecrement, either as the Source Meter Name or in the Key Name/Output Variable or Meter Name pairs, though it may reference a Meter:Custom.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#metercustomdecrement
        """

class AnyPythonPluginOutputVariable:
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
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugin-system/#pythonpluginoutputvariable
        """

class PythonPluginOutputVariable:
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
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOilNo1",
            "FuelOilNo2",
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugin-system/#pythonpluginoutputvariable
        """
