"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class SimulationControl:
    def __call__(
        self,
        /,
        *,
        do_zone_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_system_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_plant_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        run_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "Yes",
        run_simulation_for_weather_file_run_periods: Literal["", "No", "Yes"] | None = "Yes",
        do_hvac_sizing_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "No",
        maximum_number_of_hvac_sizing_simulation_passes: int | None = 1,
    ) -> None:
        """Create a new ``SimulationControl`` and add it to the document.

        Note that the following 3 fields are related to the Sizing:Zone, Sizing:System, and Sizing:Plant objects. Having these fields set to Yes but no corresponding Sizing object will not cause the sizing to be done. However, having any of these fields set to No, the corresponding Sizing object is ignored. Note also, if you want to do system sizing, you must also do zone sizing in the same run or an error will result.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#simulationcontrol
        """

class ZoneAirMassFlowConservation:
    def __call__(
        self,
        /,
        *,
        adjust_zone_mixing_and_return_for_air_mass_flow_balance: Literal[
            "", "AdjustMixingOnly", "AdjustMixingThenReturn", "AdjustReturnOnly", "AdjustReturnThenMixing", "None"
        ]
        | None = "None",
        infiltration_balancing_method: Literal["", "AddInfiltrationFlow", "AdjustInfiltrationFlow", "None"]
        | None = "AddInfiltrationFlow",
        infiltration_balancing_zones: Literal["", "AllZones", "MixingSourceZonesOnly"] | None = "MixingSourceZonesOnly",
    ) -> None:
        """Create a new ``ZoneAirMassFlowConservation`` and add it to the document.

        Enforces the zone air mass flow balance by either adjusting zone mixing object flow only, adjusting zone total return flow only, zone mixing and the zone total return flows, or adjusting the zone total return and zone mixing object flows. Zone infiltration flow air flow is increased or decreased depending user selection in the infiltration treatment method. If either of zone mixing or zone return flow adjusting methods or infiltration is active, then the zone air mass flow balance calculation will attempt to enforce conservation of mass for each zone. If flow balancing method is 'None' and infiltration is 'None', then the zone air mass flow calculation defaults to assume self-balanced simple flow mixing and infiltration objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneairmassflowconservation
        """

class SizingPeriodWeatherFileDays:
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

class ScheduleFileShading:
    def __call__(self, /, *, file_name: str) -> None:
        """Create a new ``Schedule:File:Shading`` and add it to the document.

        A Schedule:File:Shading points to a CSV file that has 8760-8784 hours of sunlit fraction data for all or some of the exterior surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#schedulefileshading
        """

class WindowMaterialGlazingRefractionExtinctionMethod:
    def __call__(
        self,
        name: str,
        /,
        *,
        thickness: float,
        solar_index_of_refraction: float,
        solar_extinction_coefficient: float,
        visible_index_of_refraction: float,
        visible_extinction_coefficient: float,
        infrared_transmittance_at_normal_incidence: float | None = 0,
        infrared_hemispherical_emissivity: float | None = 0.84,
        conductivity: float | None = 0.9,
        dirt_correction_factor_for_solar_and_visible_transmittance: float | None = 1,
        solar_diffusing: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``WindowMaterial:Glazing:RefractionExtinctionMethod`` and add it to the document.

        Glass material properties for Windows or Glass Doors Index of Refraction/Extinction Coefficient input method Not to be used for coated glass

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialglazingrefractionextinctionmethod
        """

class MaterialPropertyHeatAndMoistureTransferRedistribution:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_redistribution_points: int,
        moisture_content_1: float,
        liquid_transport_coefficient_1: float,
        moisture_content_2: float | None = ...,
        liquid_transport_coefficient_2: float | None = ...,
        moisture_content_3: float | None = ...,
        liquid_transport_coefficient_3: float | None = ...,
        moisture_content_4: float | None = ...,
        liquid_transport_coefficient_4: float | None = ...,
        moisture_content_5: float | None = ...,
        liquid_transport_coefficient_5: float | None = ...,
        moisture_content_6: float | None = ...,
        liquid_transport_coefficient_6: float | None = ...,
        moisture_content_7: float | None = ...,
        liquid_transport_coefficient_7: float | None = ...,
        moisture_content_8: float | None = ...,
        liquid_transport_coefficient_8: float | None = ...,
        moisture_content_9: float | None = ...,
        liquid_transport_coefficient_9: float | None = ...,
        moisture_content_10: float | None = ...,
        liquid_transport_coefficient_10: float | None = ...,
        moisture_content_11: float | None = ...,
        liquid_transport_coefficient_11: float | None = ...,
        moisture_content_12: float | None = ...,
        liquid_transport_coefficient_12: float | None = ...,
        moisture_content_13: float | None = ...,
        liquid_transport_coefficient_13: float | None = ...,
        moisture_content_14: float | None = ...,
        liquid_transport_coefficient_14: float | None = ...,
        moisture_content_15: float | None = ...,
        liquid_transport_coefficient_15: float | None = ...,
        moisture_content_16: float | None = ...,
        liquid_transport_coefficient_16: float | None = ...,
        moisture_content_17: float | None = ...,
        liquid_transport_coefficient_17: float | None = ...,
        moisture_content_18: float | None = ...,
        liquid_transport_coefficient_18: float | None = ...,
        moisture_content_19: float | None = ...,
        liquid_transport_coefficient_19: float | None = ...,
        moisture_content_20: float | None = ...,
        liquid_transport_coefficient_20: float | None = ...,
        moisture_content_21: float | None = ...,
        liquid_transport_coefficient_21: float | None = ...,
        moisture_content_22: float | None = ...,
        liquid_transport_coefficient_22: float | None = ...,
        moisture_content_23: float | None = ...,
        liquid_transport_coefficient_23: float | None = ...,
        moisture_content_24: float | None = ...,
        liquid_transport_coefficient_24: float | None = ...,
        moisture_content_25: float | None = ...,
        liquid_transport_coefficient_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Redistribution`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid transport coefficient and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferredistribution
        """

class AnyWallInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Interzone`` and add it to the document.

        Allows for simplified entry of interzone walls (walls between zones).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#wallinterzone
        """

class ShadingPropertyReflectance:
    def __call__(
        self,
        /,
        *,
        shading_surface_name: str,
        diffuse_solar_reflectance_of_unglazed_part_of_shading_surface: float | None = 0.2,
        diffuse_visible_reflectance_of_unglazed_part_of_shading_surface: float | None = 0.2,
        fraction_of_shading_surface_that_is_glazed: float | None = 0,
        glazing_construction_name: str | None = ...,
    ) -> None:
        """Create a new ``ShadingProperty:Reflectance`` and add it to the document.

        If this object is not defined for a shading surface the default values listed in following fields will be used in the solar reflection calculation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingpropertyreflectance
        """

class AnySurfacePropertyExposedFoundationPerimeter:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        exposed_perimeter_calculation_method: Literal["BySegment", "ExposedPerimeterFraction", "TotalExposedPerimeter"],
        total_exposed_perimeter: float | None = ...,
        exposed_perimeter_fraction: float | None = ...,
        surfaces: list[_g.AnySurfacePropertyExposedFoundationPerimeterSurfacesItem] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:ExposedFoundationPerimeter`` and add it to the document.

        Defines the perimeter of a foundation floor that is exposed to the exterior environment through the floor. User may either define the total exposed perimeter, fraction of perimeter exposed or individually define which segments of the floor surface perimeter are exposed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyexposedfoundationperimeter
        """

class GroundHeatTransferBasementYFACE:
    def __call__(self, /) -> None:
        """Create a new ``GroundHeatTransfer:Basement:YFACE`` and add it to the document.

        This is only needed when using manual gridding (not recommended) YFACE: Y Direction cell face coordinates: m

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementyface
        """

class RoomAirSettingsThreeNodeDisplacementVentilation:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        gain_distribution_schedule_name: str,
        number_of_plumes_per_occupant: float | None = 1,
        thermostat_height: float | None = 1.1,
        comfort_height: float | None = 1.1,
        temperature_difference_threshold_for_reporting: float | None = 0.4,
    ) -> None:
        """Create a new ``RoomAirSettings:ThreeNodeDisplacementVentilation`` and add it to the document.

        The UCSD model for Displacement Ventilation

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairsettingsthreenodedisplacementventilation
        """

class SwimmingPoolIndoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        average_depth: float,
        activity_factor_schedule_name: str,
        cover_schedule_name: str,
        pool_water_inlet_node: str,
        pool_water_outlet_node: str,
        setpoint_temperature_schedule: str,
        maximum_number_of_people: float,
        make_up_water_supply_schedule_name: str | None = ...,
        cover_evaporation_factor: float | None = 0,
        cover_convection_factor: float | None = 0,
        cover_short_wavelength_radiation_factor: float | None = 0,
        cover_long_wavelength_radiation_factor: float | None = 0,
        pool_heating_system_maximum_water_flow_rate: float | None = ...,
        pool_miscellaneous_equipment_power: float | None = ...,
        people_schedule: str | None = ...,
        people_heat_gain_schedule: str | None = ...,
    ) -> None:
        """Create a new ``SwimmingPool:Indoor`` and add it to the document.

        Specifies an indoor swimming pools linked to a floor surface. The pool is assumed to cover the entire floor to which it is linked.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#swimmingpoolindoor
        """

class ZoneInfiltrationEffectiveLeakageArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        effective_air_leakage_area: float,
        stack_coefficient: float,
        wind_coefficient: float,
        schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneInfiltration:EffectiveLeakageArea`` and add it to the document.

        Infiltration is specified as effective leakage area at 4 Pa, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * (AL /1000) SQRT(Cs*|(Tzone-Todb)| + Cw*WindSpd**2 ) If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneinfiltrationeffectiveleakagearea
        """

class AnyHVACTemplatePlantBoiler:
    def __call__(
        self,
        name: str,
        /,
        *,
        boiler_type: Literal["CondensingHotWaterBoiler", "DistrictHotWater", "HotWaterBoiler"],
        capacity: float | Literal["", "Autosize"] | None = "Autosize",
        efficiency: float | None = 0.8,
        fuel_type: Literal["Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"]
        | None = ...,
        priority: str | None = ...,
        sizing_factor: float | None = 1,
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1.1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 100,
        template_plant_loop_type: Literal["HotWater", "MixedWater"] | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Boiler`` and add it to the document.

        This object adds a boiler to an HVACTemplate:Plant:HotWaterLoop or MixedWaterLoop.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantboiler
        """

class SizingParameters:
    def __call__(
        self,
        /,
        *,
        heating_sizing_factor: float | None = 1,
        cooling_sizing_factor: float | None = 1,
        timesteps_in_averaging_window: int | None = ...,
    ) -> None:
        """Create a new ``Sizing:Parameters`` and add it to the document.

        Specifies global heating and cooling sizing factors/ratios. These ratios are applied at the zone level to all of the zone heating and cooling loads and air flow rates. Then these new loads and air flow rates are used to calculate the system level flow rates and capacities and are used in all component sizing calculations. Specifies the width (in load timesteps) of a moving average window which is used to smooth the peak load across more than one timestep.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingparameters
        """

class AnyZoneHVACOutdoorAirUnitEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_1_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_1_name: str | None = ...,
        component_2_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_3_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_4_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_5_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_6_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_7_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_8_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_8_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:OutdoorAirUnit:EquipmentList`` and add it to the document.

        Equipment list for components in a ZoneHVAC:OutdoorAirUnit. Components are simulated sequentially in the order given in the equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacoutdoorairunitequipmentlist
        """

class ZoneHVACLowTemperatureRadiantVariableFlowDesign:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        fluid_to_radiant_surface_heat_transfer_model: Literal["", "ConvectionOnly", "ISOStandard"]
        | None = "ConvectionOnly",
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_outside_diameter: float | None = 0.016,
        hydronic_tubing_conductivity: float | None = 0.35,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "SurfaceFaceTemperature",
            "SurfaceInteriorTemperature",
        ]
        | None = "MeanAirTemperature",
        setpoint_control_type: Literal["", "HalfFlowPower", "ZeroFlowPower"] | None = "HalfFlowPower",
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        heating_control_throttling_range: float | None = 0.5,
        heating_control_temperature_schedule_name: str | None = ...,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        changeover_delay_time_period_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design`` and add it to the document.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantvariableflowdesign
        """

class AirTerminalDualDuctConstantVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        hot_air_inlet_node_name: str,
        cold_air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:DualDuct:ConstantVolume`` and add it to the document.

        Central air system terminal unit, dual duct, constant volume.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminaldualductconstantvolume
        """

class AnyCoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpvariablespeedequationfit
        """

class AirLoopHVACZoneSplitter:
    def __call__(
        self, name: str, /, *, inlet_node_name: str, nodes: list[_g.AirLoopHVACZoneSplitterNodesItem] = ...
    ) -> None:
        """Create a new ``AirLoopHVAC:ZoneSplitter`` and add it to the document.

        Split one air stream into N outlet streams (currently 500 per air loop, but extensible). Node names cannot be duplicated within a single zone splitter (AirLoopHVAC:ZoneSplitter) list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvaczonesplitter
        """

class AirLoopHVACSplitter:
    def __call__(
        self, name: str, /, *, inlet_node_name: str, nodes: list[_g.AirLoopHVACSplitterNodesItem] = ...
    ) -> None:
        """Create a new ``AirLoopHVAC:Splitter`` and add it to the document.

        Split one air stream from AirLoopHVAC:DedicatedOutdoorAirSystem outlet node into N outlet streams (currently 10 as default, but extensible). Node names should be Outdoor Air Stream Node Name in OutdoorAir:Mixer objects served by AirLoopHVAC objects listed in AirLoopHVAC:DedicatedOutdoorAirSystem.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacsplitter
        """

class ConnectorList:
    def __call__(
        self,
        name: str,
        /,
        *,
        connector_1_object_type: Literal["Connector:Mixer", "Connector:Splitter"],
        connector_1_name: str,
        connector_2_object_type: Literal["Connector:Mixer", "Connector:Splitter"] | None = ...,
        connector_2_name: str | None = ...,
    ) -> None:
        """Create a new ``ConnectorList`` and add it to the document.

        only two connectors allowed per loop if two entered, one must be Connector:Splitter and one must be Connector:Mixer

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#connectorlist
        """

class ChillerConstantCOP:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
    ) -> None:
        """Create a new ``Chiller:ConstantCOP`` and add it to the document.

        This constant COP chiller model provides a means of quickly specifying a Chiller where performance data is not available.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerconstantcop
        """

class DistrictHeatingSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        steam_inlet_node_name: str,
        steam_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        capacity_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DistrictHeating:Steam`` and add it to the document.

        Centralized source of Steam, such as a district heating system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#districtheatingsteam
        """

class CoolingTowerTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        high_fan_speed_air_flow_rate: float | Literal["Autosize"],
        high_fan_speed_fan_power: float | Literal["Autosize"],
        low_fan_speed_air_flow_rate: float | Literal["Autocalculate"],
        low_fan_speed_fan_power: float | Literal["Autocalculate"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        free_convection_regime_air_flow_rate: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        free_convection_regime_u_factor_times_area_value: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        high_speed_nominal_capacity: float | None = ...,
        low_speed_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_nominal_capacity_sizing_factor: float | None = 0.5,
        free_convection_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["", "Autosize"] | None = "Autosize",
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
        """Create a new ``CoolingTower:TwoSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a two-speed fan drawing air through the tower (induced-draft configuration). For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowertwospeed
        """

class AnyPlantEquipmentOperationThermalEnergyStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        on_peak_schedule: str,
        charging_availability_schedule: str,
        non_charging_chilled_water_temperature: float,
        charging_chilled_water_temperature: float,
        component_1_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ],
        component_1_name: str,
        component_1_demand_calculation_node_name: str,
        component_1_setpoint_node_name: str,
        component_1_flow_rate: float | Literal["Autosize"],
        component_1_operation_type: Literal["Cooling", "Dual", "Heating"],
        component_2_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_2_demand_calculation_node_name: str | None = ...,
        component_2_setpoint_node_name: str | None = ...,
        component_2_flow_rate: float | Literal["Autosize"] | None = ...,
        component_2_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_3_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_3_demand_calculation_node_name: str | None = ...,
        component_3_setpoint_node_name: str | None = ...,
        component_3_flow_rate: float | Literal["Autosize"] | None = ...,
        component_3_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_4_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_4_demand_calculation_node_name: str | None = ...,
        component_4_setpoint_node_name: str | None = ...,
        component_4_flow_rate: float | Literal["Autosize"] | None = ...,
        component_4_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_5_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_5_demand_calculation_node_name: str | None = ...,
        component_5_setpoint_node_name: str | None = ...,
        component_5_flow_rate: float | Literal["Autosize"] | None = ...,
        component_5_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_6_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_6_demand_calculation_node_name: str | None = ...,
        component_6_setpoint_node_name: str | None = ...,
        component_6_flow_rate: float | Literal["Autosize"] | None = ...,
        component_6_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_7_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_7_demand_calculation_node_name: str | None = ...,
        component_7_setpoint_node_name: str | None = ...,
        component_7_flow_rate: float | Literal["Autosize"] | None = ...,
        component_7_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_8_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_8_name: str | None = ...,
        component_8_demand_calculation_node_name: str | None = ...,
        component_8_setpoint_node_name: str | None = ...,
        component_8_flow_rate: float | Literal["Autosize"] | None = ...,
        component_8_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_9_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_9_name: str | None = ...,
        component_9_demand_calculation_node_name: str | None = ...,
        component_9_setpoint_node_name: str | None = ...,
        component_9_flow_rate: float | Literal["Autosize"] | None = ...,
        component_9_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_10_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_10_name: str | None = ...,
        component_10_demand_calculation_node_name: str | None = ...,
        component_10_setpoint_node_name: str | None = ...,
        component_10_flow_rate: float | Literal["Autosize"] | None = ...,
        component_10_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ThermalEnergyStorage`` and add it to the document.

        Plant equipment operation scheme for simpler input to control thermal (ice) energy storage systems. It replaces a host of setpoint managers with simple, single input values. For more complex controls, use the ComponentSetpoint scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationthermalenergystorage
        """

class PlantEquipmentOperationChillerHeaterChangeover:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_cooling_plant_setpoint_temperature: float,
        primary_heating_plant_setpoint_at_outdoor_high_temperature: float,
        outdoor_high_temperature: float,
        primary_heating_plant_setpoint_at_outdoor_low_temperature: float,
        outdoor_low_temperature: float,
        secondary_distribution_cooling_plant_setpoint_temperature: float | None = ...,
        secondary_distribution_heating_plant_setpoint_temperature: float | None = ...,
        zone_load_polling_zonelist_name: str | None = ...,
        cooling_only_load_plant_equipment_operation_cooling_load_name: str | None = ...,
        heating_only_load_plant_equipment_operation_heating_load_name: str | None = ...,
        simultaneous_cooling_and_heating_plant_equipment_operation_cooling_load_name: str | None = ...,
        simultaneous_cooling_and_heating_plant_equipment_operation_heating_load_name: str | None = ...,
        dedicated_chilled_water_return_recovery_heat_pump_name: str | None = ...,
        dedicated_hot_water_return_recovery_heat_pump_name: str | None = ...,
        boiler_setpoint_temperature_offset: float | None = 0.5,
        primary_heating_plant_setpoint_at_backup_outdoor_low_temperature: float | None = ...,
        backup_outdoor_low_temperature: float | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ChillerHeaterChangeover`` and add it to the document.

        Plant equipment operation object to control switchover between chiller and heater operation of chiller heater heat pump serving 2 plant loops. Poll zone loads and determine if plant should be in heating, cooling or simultaneous heating and cooling and dispatch equipment accordingly.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationchillerheaterchangeover
        """

class ExternalInterfaceFunctionalMockupUnitImportToActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        fmu_file_name: str,
        fmu_instance_name: str,
        fmu_variable_name: str,
        initial_value: float,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitImport:To:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitimporttoactuator
        """

class GeneratorMicroCHP:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        performance_parameters_name: str | None = ...,
        zone_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        generator_fuel_supply_name: str | None = ...,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:MicroCHP`` and add it to the document.

        Small-scale combined heat and power (micro CHP) electric generator using the model developed by IEA/ECBCS Annex 42 see www.cogen-sim.net. The model was developed for both internal combustion and Stirling cycle engines, but might be used for other types of residential CHP devices.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatormicrochp
        """

class CurveSigmoid:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        coefficient5_c5: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Sigmoid`` and add it to the document.

        Sigmoid curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1+C2/[1+exp((C3-x)/C4)]**C5

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvesigmoid
        """

class LifeCycleCostRecurringCosts:
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

class OutputMeterMeterFileOnly:
    def __call__(
        self,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
    ) -> None:
        """Create a new ``Output:Meter:MeterFileOnly`` and add it to the document.

        Each Output:Meter:MeterFileOnly command picks meters to be put only onto meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported a list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-output-reporting/#outputmetermeterfileonly
        """
