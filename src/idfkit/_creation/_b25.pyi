"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class HeatBalanceSettingsConductionFiniteDifference:
    def __call__(
        self,
        /,
        *,
        difference_scheme: Literal["", "CrankNicholsonSecondOrder", "FullyImplicitFirstOrder"]
        | None = "FullyImplicitFirstOrder",
        space_discretization_constant: float | None = 3,
        relaxation_factor: float | None = 1,
        inside_face_surface_temperature_convergence_criteria: float | None = 0.002,
    ) -> None:
        """Create a new ``HeatBalanceSettings:ConductionFiniteDifference`` and add it to the document.

        Determines settings for the Conduction Finite Difference algorithm for surface heat transfer modeling.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#heatbalancesettingsconductionfinitedifference
        """

class AnyScheduleDayList:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        interpolate_to_timestep: Literal["", "Average", "Linear", "No"] | None = "No",
        minutes_per_item: int | None = ...,
        extensions: list[_g.ScheduleDayListExtensionsItem] = ...,
    ) -> None:
        """Create a new ``Schedule:Day:List`` and add it to the document.

        Schedule:Day:List will allow the user to list 24 hours worth of values, which can be sub-hourly in nature.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduledaylist
        """

class AnyScheduleYear:
    def __call__(
        self, name: str, /, *, narrow_with_as_version_first: Never, schedule_type_limits_name: str | None = ...
    ) -> None:
        """Create a new ``Schedule:Year`` and add it to the document.

        A Schedule:Year contains from 1 to 52 week schedules

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleyear
        """

class WindowMaterialDrapeEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        front_side_drape_beam_diffuse_solar_transmittance: float,
        back_side_drape_beam_diffuse_solar_transmittance: float,
        front_side_drape_beam_diffuse_solar_reflectance: float,
        back_side_drape_beam_diffuse_solar_reflectance: float,
        drape_beam_beam_solar_transmittance_at_normal_incidence: float | None = 0,
        drape_beam_beam_visible_transmittance: float | None = ...,
        drape_beam_diffuse_visible_transmittance: float | None = ...,
        drape_beam_diffuse_visible_reflectance: float | None = ...,
        drape_material_infrared_transmittance: float | None = 0.05,
        front_side_drape_material_infrared_emissivity: float | None = 0.87,
        back_side_drape_material_infrared_emissivity: float | None = 0.87,
        width_of_pleated_fabric: float | None = 0,
        length_of_pleated_fabric: float | None = 0,
    ) -> None:
        """Create a new ``WindowMaterial:Drape:EquivalentLayer`` and add it to the document.

        Specifies the properties of equivalent layer drape fabric materials. Shades are considered to be perfect diffusers (all transmitted and reflected radiation is hemispherically-diffuse) independent of angle of incidence. unpleated drape fabric is treated as thin and flat layer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialdrapeequivalentlayer
        """

class GeometryTransform:
    def __call__(
        self,
        /,
        *,
        current_aspect_ratio: float,
        new_aspect_ratio: float,
        plane_of_transform: Literal["", "XY"] | None = "XY",
    ) -> None:
        """Create a new ``GeometryTransform`` and add it to the document.

        Provides a simple method of altering the footprint geometry of a model. The intent is to provide a single parameter that can be used to reshape the building description contained in the rest of the input file.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#geometrytransform
        """

class Zone:
    def __call__(
        self,
        name: str,
        /,
        *,
        direction_of_relative_north: float | None = 0,
        x_origin: float | None = 0,
        y_origin: float | None = 0,
        z_origin: float | None = 0,
        type: int | None = 1,
        multiplier: int | None = 1,
        ceiling_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        zone_inside_convection_algorithm: Literal[
            "", "ASTMC1340", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP", "TrombeWall"
        ]
        | None = ...,
        zone_outside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "DOE-2", "MoWiTT", "SimpleCombined", "TARP"
        ]
        | None = ...,
        part_of_total_floor_area: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Zone`` and add it to the document.

        Defines a thermal zone of the building. Every zone contains one or more Spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#zone
        """

class SurfacePropertyLocalEnvironment:
    def __call__(
        self,
        name: str,
        /,
        *,
        exterior_surface_name: str | None = ...,
        sunlit_fraction_schedule_name: str | None = ...,
        surrounding_surfaces_object_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
        ground_surfaces_object_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:LocalEnvironment`` and add it to the document.

        This object defines the local environment properties of an exterior surface. One or more environment properties have to be defined and linked to the exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertylocalenvironment
        """

class HotWaterEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HotWaterEquipment`` and add it to the document.

        Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#hotwaterequipment
        """

class DaylightingDeviceTubular:
    def __call__(
        self,
        name: str,
        /,
        *,
        dome_name: str,
        diffuser_name: str,
        construction_name: str,
        diameter: float,
        total_length: float,
        effective_thermal_resistance: float | None = 0.28,
        transition_lengths: list[_g.DaylightingDeviceTubularTransitionLengthsItem] = ...,
    ) -> None:
        """Create a new ``DaylightingDevice:Tubular`` and add it to the document.

        Defines a tubular daylighting device (TDD) consisting of three components: a dome, a pipe, and a diffuser. The dome and diffuser are defined separately using the FenestrationSurface:Detailed object.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingdevicetubular
        """

class ZoneEarthtubeParameters:
    def __call__(
        self,
        /,
        *,
        earth_tube_model_parameters_name: str,
        nodes_above_earth_tube: int | None = 5,
        nodes_below_earth_tube: int | None = 3,
        earth_tube_dimensionless_boundary_above: float | None = 1,
        earth_tube_dimensionless_boundary_below: float | None = 0.25,
        earth_tube_solution_space_width: float | None = 4,
    ) -> None:
        """Create a new ``ZoneEarthtube:Parameters`` and add it to the document.

        Parameters that apply to the vertical model for an earth tube

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneearthtubeparameters
        """

class AirflowNetworkMultiZoneSurfaceCrack:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_at_reference_conditions: float,
        air_mass_flow_exponent: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Surface:Crack`` and add it to the document.

        This object specifies the properties of airflow through a crack.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonesurfacecrack
        """

class HVACTemplateZoneIdealLoadsAirSystem:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        system_availability_schedule_name: str | None = ...,
        maximum_heating_supply_air_temperature: float | None = 50,
        minimum_cooling_supply_air_temperature: float | None = 13,
        maximum_heating_supply_air_humidity_ratio: float | None = 0.0156,
        minimum_cooling_supply_air_humidity_ratio: float | None = 0.0077,
        heating_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_heating_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_sensible_heating_capacity: float | Literal["Autosize"] | None = ...,
        cooling_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_cooling_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        heating_availability_schedule_name: str | None = ...,
        cooling_availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal[
            "", "ConstantSensibleHeatRatio", "ConstantSupplyHumidityRatio", "Humidistat", "None"
        ]
        | None = "ConstantSensibleHeatRatio",
        cooling_sensible_heat_ratio: float | None = 0.7,
        dehumidification_setpoint: float | None = 60,
        humidification_control_type: Literal["", "ConstantSupplyHumidityRatio", "Humidistat", "None"] | None = "None",
        humidification_setpoint: float | None = 30,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "None", "Sum"
        ]
        | None = "None",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        design_specification_outdoor_air_object_name: str | None = ...,
        demand_controlled_ventilation_type: Literal["", "CO2Setpoint", "None", "OccupancySchedule"] | None = "None",
        outdoor_air_economizer_type: Literal["", "DifferentialDryBulb", "DifferentialEnthalpy", "NoEconomizer"]
        | None = "NoEconomizer",
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:IdealLoadsAirSystem`` and add it to the document.

        Zone with ideal air system that meets heating or cooling loads

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneidealloadsairsystem
        """

class HVACTemplateZonePTAC:
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
        cooling_coil_type: Literal["", "SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cooling_cop: float | None = 3,
        heating_coil_type: Literal["", "Electric", "Gas", "HotWater"] | None = "Electric",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
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
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:PTAC`` and add it to the document.

        Packaged Terminal Air Conditioner

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneptac
        """

class HVACTemplateSystemVRF:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
        gross_rated_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = 30,
        vertical_height_used_for_piping_correction_factor: float | None = 10,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = 30,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_condenser_volume_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
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
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -15,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 45,
    ) -> None:
        """Create a new ``HVACTemplate:System:VRF`` and add it to the document.

        Variable refrigerant flow (VRF) heat pump condensing unit. Serves one or more VRF zone terminal units (HVACTemplate:Zone:VRF).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemvrf
        """

class DesignSpecificationZoneAirDistribution:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_air_distribution_effectiveness_in_cooling_mode: float | None = 1,
        zone_air_distribution_effectiveness_in_heating_mode: float | None = 1,
        zone_air_distribution_effectiveness_schedule_name: str | None = ...,
        zone_secondary_recirculation_fraction: float | None = 0,
        minimum_zone_ventilation_efficiency: float | None = 0,
    ) -> None:
        """Create a new ``DesignSpecification:ZoneAirDistribution`` and add it to the document.

        This object is used to describe zone air distribution in terms of air distribution effectiveness and secondary recirculation fraction. It is referenced by Sizing:Zone and Controller:MechanicalVentilation objects

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#designspecificationzoneairdistribution
        """

class SizingPlant:
    def __call__(
        self,
        /,
        *,
        plant_or_condenser_loop_name: str,
        loop_type: Literal["Condenser", "Cooling", "Heating", "Steam"],
        design_loop_exit_temperature: float,
        loop_design_temperature_difference: float,
        sizing_option: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        zone_timesteps_in_averaging_window: int | None = 1,
        coincident_sizing_factor_mode: Literal[
            "GlobalCoolingSizingFactor", "GlobalHeatingSizingFactor", "LoopComponentSizingFactor", "None"
        ]
        | None = ...,
    ) -> None:
        """Create a new ``Sizing:Plant`` and add it to the document.

        Specifies the input needed to autosize plant loop flow rates and equipment capacities. This information is initially used by components that use water for heating or cooling such as hot or chilled water coils to calculate their maximum water flow rates. These flow rates are then summed for use in calculating the Plant Loop flow rates.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingplant
        """

class ZoneControlThermostatThermalComfort:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        thermal_comfort_control_type_schedule_name: str,
        thermal_comfort_control_1_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ],
        thermal_comfort_control_1_name: str,
        averaging_method: Literal["", "ObjectAverage", "PeopleAverage", "SpecificObject"] | None = "PeopleAverage",
        specific_people_name: str | None = ...,
        minimum_dry_bulb_temperature_setpoint: float | None = 0,
        maximum_dry_bulb_temperature_setpoint: float | None = 50,
        thermal_comfort_control_2_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ]
        | None = ...,
        thermal_comfort_control_2_name: str | None = ...,
        thermal_comfort_control_3_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ]
        | None = ...,
        thermal_comfort_control_3_name: str | None = ...,
        thermal_comfort_control_4_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ]
        | None = ...,
        thermal_comfort_control_4_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat:ThermalComfort`` and add it to the document.

        If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostatthermalcomfort
        """

class ThermostatSetpointSingleCooling:
    def __call__(self, name: str, /, *, setpoint_temperature_schedule_name: str | None = ...) -> None:
        """Create a new ``ThermostatSetpoint:SingleCooling`` and add it to the document.

        Used for a cooling only thermostat. The setpoint can be scheduled and varied throughout the simulation but only cooling is allowed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointsinglecooling
        """

class AnyAirTerminalSingleDuctVAVHeatAndCoolReheat:
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

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavheatandcoolreheat
        """

class AnyAirTerminalSingleDuctConstantVolumeCooledBeam:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooled_beam_type: Literal["Active", "Passive"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_total_chilled_water_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        number_of_beams: int | Literal["", "Autosize"] | None = "Autosize",
        beam_length: float | Literal["", "Autosize"] | None = "Autosize",
        design_inlet_water_temperature: float | None = 15,
        design_outlet_water_temperature: float | None = 17,
        coil_surface_area_per_coil_length: float | None = 5.422,
        model_parameter_a: float | None = 15.3,
        model_parameter_n1: float | None = 0,
        model_parameter_n2: float | None = 0.84,
        model_parameter_n3: float | None = 0.12,
        model_parameter_a0: float | None = 0.171,
        model_parameter_k1: float | None = 0.0057,
        model_parameter_n: float | None = 0.4,
        coefficient_of_induction_kin: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        leaving_pipe_inside_diameter: float | None = 0.0145,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:CooledBeam`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with cooled beam (active or passive).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumecooledbeam
        """

class AnyCoilSystemIntegratedHeatPumpAirSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        supply_hot_water_flow_sensor_node_name: str,
        space_cooling_coil_name: str,
        space_heating_coil_name: str | None = ...,
        dedicated_water_heating_coil_name: str | None = ...,
        scwh_coil_name: str | None = ...,
        scdwh_cooling_coil_name: str | None = ...,
        scdwh_water_heating_coil_name: str | None = ...,
        shdwh_heating_coil_name: str | None = ...,
        shdwh_water_heating_coil_name: str | None = ...,
        indoor_temperature_limit_for_scwh_mode: float | None = 20,
        ambient_temperature_limit_for_scwh_mode: float | None = 27,
        indoor_temperature_above_which_wh_has_higher_priority: float | None = 20,
        ambient_temperature_above_which_wh_has_higher_priority: float | None = 20,
        flag_to_indicate_load_control_in_scwh_mode: int | None = 0,
        minimum_speed_level_for_scwh_mode: int | None = 1,
        maximum_water_flow_volume_before_switching_from_scdwh_to_scwh_mode: float | None = 0,
        minimum_speed_level_for_scdwh_mode: int | None = 1,
        maximum_running_time_before_allowing_electric_resistance_heat_use_during_shdwh_mode: float | None = 360,
        minimum_speed_level_for_shdwh_mode: int | None = 1,
    ) -> None:
        """Create a new ``CoilSystem:IntegratedHeatPump:AirSource`` and add it to the document.

        This object is used for air-source integrated heat pump, a collection of its working modes.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemintegratedheatpumpairsource
        """

class AnyAirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:MultiSpeed"],
        cooling_coil_name: str,
        number_of_speeds_for_heating: int,
        number_of_speeds_for_cooling: int,
        heating_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_2_supply_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        auxiliary_on_cycle_electric_power: float | None = 0,
        auxiliary_off_cycle_electric_power: float | None = 0,
        design_heat_recovery_water_flow_rate: float | None = 0,
        maximum_temperature_for_heat_recovery: float | None = 80,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_2_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed`` and add it to the document.

        Unitary system, heating and cooling, multi-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (DX air-to-air heat pump, gas, electric, hot water, or steam), and supplemental heating coil (gas, electric, hot water, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoairmultispeed
        """

class EvaporativeFluidCoolerTwoSpeed:
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
        design_spray_water_flow_rate: float,
        performance_input_method: Literal[
            "StandardDesignCapacity", "UFactorTimesAreaAndDesignWaterFlowRate", "UserSpecifiedDesignCapacity"
        ],
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        high_speed_standard_design_capacity: float | None = ...,
        low_speed_standard_design_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_standard_capacity_sizing_factor: float | None = 0.5,
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        high_speed_user_specified_design_capacity: float | None = ...,
        low_speed_user_specified_design_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_user_specified_design_capacity_sizing_factor: float | None = 0.5,
        design_entering_water_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_entering_air_temperature: float | None = 35,
        design_entering_air_wet_bulb_temperature: float | None = 25.6,
        high_speed_sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeFluidCooler:TwoSpeed`` and add it to the document.

        This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#evaporativefluidcoolertwospeed
        """

class WaterHeaterHeatPumpPumpedCondenser:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_setpoint_temperature_schedule_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        inlet_air_configuration: Literal["OutdoorAirOnly", "Schedule", "ZoneAirOnly", "ZoneAndOutdoorAir"],
        tank_name: str,
        dx_coil_name: str,
        compressor_location: Literal["Outdoors", "Schedule", "Zone"],
        fan_name: str,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
        exhaust_air_node_name: str | None = ...,
        inlet_air_temperature_schedule_name: str | None = ...,
        inlet_air_humidity_schedule_name: str | None = ...,
        inlet_air_zone_name: str | None = ...,
        tank_object_type: Literal["", "WaterHeater:Mixed", "WaterHeater:Stratified"] | None = "WaterHeater:Mixed",
        tank_use_side_inlet_node_name: str | None = ...,
        tank_use_side_outlet_node_name: str | None = ...,
        dx_coil_object_type: Literal[
            "",
            "Coil:WaterHeating:AirToWaterHeatPump:Pumped",
            "Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ]
        | None = ...,
        minimum_inlet_air_temperature_for_compressor_operation: float | None = 10,
        maximum_inlet_air_temperature_for_compressor_operation: float | None = 48.88888888889,
        compressor_ambient_temperature_schedule_name: str | None = ...,
        fan_object_type: Literal["", "Fan:OnOff", "Fan:SystemModel"] | None = "Fan:OnOff",
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
        parasitic_heat_rejection_location: Literal["", "Outdoors", "Zone"] | None = "Outdoors",
        inlet_air_mixer_node_name: str | None = ...,
        outlet_air_splitter_node_name: str | None = ...,
        inlet_air_mixer_schedule_name: str | None = ...,
        tank_element_control_logic: Literal["", "MutuallyExclusive", "Simultaneous"] | None = "Simultaneous",
        control_sensor_1_height_in_stratified_tank: float | None = ...,
        control_sensor_1_weight: float | None = 1,
        control_sensor_2_height_in_stratified_tank: float | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:HeatPump:PumpedCondenser`` and add it to the document.

        This object models an air-source heat pump for water heating where the water is pumped out of the tank, through a heating coil and returned to the tank. For wrapped condenser HPWHs, see WaterHeater:HeatPump:WrappedCondenser. WaterHeater:HeatPump:PumpedCondenser is a compound object that references other component objects - Coil:WaterHeating:AirToWaterHeatPump:*, Fan:OnOff, WaterHeater:Mixed or WaterHeater:Stratified

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheaterheatpumppumpedcondenser
        """

class ThermalStorageHotWaterStratified:
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
        top_setpoint_temperature_schedule_name: str | None = ...,
        bottom_setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = 0.0001,
        top_temperature_sensor_height: float | None = ...,
        bottom_temperature_sensor_height: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        nominal_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_flow_direction_schedule: str | None = ...,
        use_side_heat_transfer_effectiveness: float | None = 1,
        use_side_availability_schedule_name: str | None = ...,
        use_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        use_side_outlet_height: float | None = 0,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_flow_direction_schedule: str | None = ...,
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
        """Create a new ``ThermalStorage:HotWater:Stratified`` and add it to the document.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragehotwaterstratified
        """

class AirTerminalSingleDuctUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: int,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:UserDefined`` and add it to the document.

        Defines a generic single duct air terminal unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#airterminalsingleductuserdefined
        """

class SetpointManagerMultiZoneHumidityMinimum:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_humidity_ratio: float | None = 0.005,
        maximum_setpoint_humidity_ratio: float | None = 0.012,
    ) -> None:
        """Create a new ``SetpointManager:MultiZone:Humidity:Minimum`` and add it to the document.

        This setpoint manager sets the minimum supply air humidity ratio based on humidification requirements of a controlled zone with critical humidity ratio setpoint (i.e., a zone with the highest humidity ratio setpoint) in an air loop served by a central air-conditioner.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagermultizonehumidityminimum
        """

class WaterUseEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        peak_flow_rate: float,
        end_use_subcategory: str | None = "General",
        flow_rate_fraction_schedule_name: str | None = ...,
        target_temperature_schedule_name: str | None = ...,
        hot_water_supply_temperature_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        sensible_fraction_schedule_name: str | None = ...,
        latent_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``WaterUse:Equipment`` and add it to the document.

        A generalized object for simulating all water end uses. Hot and cold water uses are included, as well as controlled mixing of hot and cold water at the tap. The WaterUse:Equipment object can be used stand-alone, or coupled into a plant loop using the WaterUse:Connections object (see below). The WaterUse:Connections object allows water uses to be linked to WaterUse:Storage objects to store and draw reclaimed water. The object can also simulate drainwater heat recovery.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-systems/#wateruseequipment
        """

class FaultModelTemperatureSensorOffsetChillerSupplyWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
        ],
        chiller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_sensor_offset: float | None = 0,
    ) -> None:
        """Create a new ``FaultModel:TemperatureSensorOffset:ChillerSupplyWater`` and add it to the document.

        This object describes fault of chiller supply water temperature sensor offset

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodeltemperaturesensoroffsetchillersupplywater
        """

class CurveChillerPartLoadWithLift:
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
        coefficient6_c6: float,
        coefficient7_c7: float,
        coefficient8_c8: float,
        coefficient9_c9: float,
        coefficient10_c10: float,
        coefficient11_c11: float,
        coefficient12_c12: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_value_of_z: float,
        maximum_value_of_z: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        input_unit_type_for_y: Literal["", "Dimensionless"] | None = "Dimensionless",
        input_unit_type_for_z: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:ChillerPartLoadWithLift`` and add it to the document.

        This chiller part-load performance curve has three independent variables. Input consists of the curve name, the twelve coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x + C3*x**2 + C4*y + C5*y**2 + C6*x*y + C7*x**3 + C8*y**3 + C9*x**2*y + C10*x*y**2 + C11*x**2*y**2 + C12*z*y**3 x = dT* = normalized fractional Lift = dT / dTref y = PLR = part load ratio (cooling load/steady state capacity) z = Tdev* = normalized Tdev = Tdev / dTref Where: dT = Lift = Leaving Condenser Water Temperature - Leaving Chilled Water Temperature dTref = dT at the reference condition Tdev = Leaving Chilled Water Temperature - Reference Chilled Water Temperature

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvechillerpartloadwithlift
        """

class FluidPropertiesName:
    def __call__(self, /, *, fluid_name: str, fluid_type: Literal["Glycol", "Refrigerant"]) -> None:
        """Create a new ``FluidProperties:Name`` and add it to the document.

        potential fluid name/type in the input file repeat this object for each fluid

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fluid-properties/#fluidpropertiesname
        """

class OutputSchedules:
    def __call__(self, /, *, key_field: Literal["Hourly", "Timestep"]) -> None:
        """Create a new ``Output:Schedules`` and add it to the document.

        Produces a condensed reporting that illustrates the full range of schedule values in the eio output file. In the style of input: DaySchedule, WeekSchedule, and Annual Schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputschedules
        """

class AnyOutputTableMonthly:
    def __call__(
        self,
        name: str,
        /,
        *,
        digits_after_decimal: int | None = 2,
        variable_details: list[_g.OutputTableMonthlyVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Output:Table:Monthly`` and add it to the document.

        Provides a generic method of setting up tables of monthly results. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:Table:Monthly object often produces multiple tables in the output. A table is produced for every instance of a particular output variable. For example, a table defined with zone variables will be produced once for every zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-monthly/#outputtablemonthly
        """

class OutputDiagnostics:
    def __call__(self, /, *, diagnostics: list[_g.OutputDiagnosticsDiagnosticsItem] = ...) -> None:
        """Create a new ``Output:Diagnostics`` and add it to the document.

        Special keys to produce certain warning messages or effect certain simulation characteristics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#outputdiagnostics
        """
