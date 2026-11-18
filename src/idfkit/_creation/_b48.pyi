"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class SiteGroundReflectanceSnowModifier:
    def __call__(
        self,
        /,
        *,
        ground_reflected_solar_modifier: float | None = 1,
        daylighting_ground_reflected_solar_modifier: float | None = 1,
    ) -> None:
        """Create a new ``Site:GroundReflectance:SnowModifier`` and add it to the document.

        Specifies ground reflectance multipliers when snow resident on the ground. These multipliers are applied to the 'normal' ground reflectances specified in Site:GroundReflectance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundreflectancesnowmodifier
        """

class RoofIrrigation:
    def __call__(
        self,
        /,
        *,
        irrigation_model_type: Literal["Schedule", "SmartSchedule"] | None = ...,
        irrigation_rate_schedule_name: str | None = ...,
        irrigation_maximum_saturation_threshold: float | None = 40,
    ) -> None:
        """Create a new ``RoofIrrigation`` and add it to the document.

        Used to describe the amount of irrigation on the ecoroof surface over the course of the simulation runperiod.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#roofirrigation
        """

class AnyMaterialPropertyVariableThermalConductivity:
    def __call__(self, name: str, /, *, narrow_with_as_version_first: Never) -> None:
        """Create a new ``MaterialProperty:VariableThermalConductivity`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity using piecewise linear temperature-conductivity function. Name is followed by up to 100 sets of temperature-conductivity pairs. HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Has no effect with other HeatBalanceAlgorithm solution algorithms

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyvariablethermalconductivity
        """

class SurfacePropertiesVaporCoefficients:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        constant_external_vapor_transfer_coefficient: Literal["No", "Yes"] | None = "No",
        external_vapor_coefficient_value: float | None = 0,
        constant_internal_vapor_transfer_coefficient: Literal["No", "Yes"] | None = "No",
        internal_vapor_coefficient_value: float | None = 0,
    ) -> None:
        """Create a new ``SurfaceProperties:VaporCoefficients`` and add it to the document.

        The interior and external vapor transfer coefficients. Normally these value are calculated using the heat convection coefficient values. Use this object to used fixed constant values. Units are kg/Pa.s.m2 This will only work with the CombinedHeatAndMoistureFiniteElement algorithm for surfaces. Other algorithms will ignore these coefficients

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertiesvaporcoefficients
        """

class HotWaterEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        hot_water_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HotWaterEquipment:Instance`` and add it to the document.

        Sets internal gains for hot water equipment in the zone. The physical characteristics are given by the referenced HotWaterEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#hotwaterequipmentinstance
        """

class AnyZoneThermalChimney:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        zone_name: str,
        width_of_the_absorber_wall: float,
        cross_sectional_area_of_air_channel_outlet: float,
        distance_from_top_of_thermal_chimney_to_inlet_1: float,
        cross_sectional_areas_of_air_channel_inlet_1: float,
        availability_schedule_name: str | None = ...,
        discharge_coefficient: float | None = 0.8,
        distance_from_top_of_thermal_chimney_to_inlet_2: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_2: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_3: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_3: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_4: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_4: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_5: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_5: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_6: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_6: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_7: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_7: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_8: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_8: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_9: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_9: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_10: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_10: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_11: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_11: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_12: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_12: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_13: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_13: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_14: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_14: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_15: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_15: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_16: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_16: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_17: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_17: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_18: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_18: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_19: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_19: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_20: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_20: float | None = ...,
    ) -> None:
        """Create a new ``ZoneThermalChimney`` and add it to the document.

        A thermal chimney is a vertical shaft utilizing solar radiation to enhance natural ventilation. It consists of an absorber wall, air gap and glass cover with high solar transmissivity.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonethermalchimney
        """

class AirflowNetworkMultiZoneSurface:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        leakage_component_name: str,
        external_node_name: str | None = ...,
        window_door_opening_factor_or_crack_factor: float | None = 1,
        ventilation_control_mode: Literal[
            "ASHRAE55Adaptive",
            "AdjacentEnthalpy",
            "AdjacentTemperature",
            "CEN15251Adaptive",
            "Constant",
            "Enthalpy",
            "NoVent",
            "Temperature",
            "ZoneLevel",
        ]
        | None = "ZoneLevel",
        ventilation_control_zone_temperature_setpoint_schedule_name: str | None = ...,
        minimum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor: float | None = 100,
        indoor_and_outdoor_enthalpy_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor: float | None = 300000,
        venting_availability_schedule_name: str | None = ...,
        occupant_ventilation_control_name: str | None = ...,
        equivalent_rectangle_method: Literal["BaseSurfaceAspectRatio", "PolygonHeight", "UserDefinedAspectRatio"]
        | None = "PolygonHeight",
        equivalent_rectangle_aspect_ratio: float | None = 1,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Surface`` and add it to the document.

        This object specifies the properties of a surface linkage through which air flows. Airflow Report: Node 1 as an inside face zone; Node 2 as an outside face zone or external node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonesurface
        """

class HVACTemplateZoneFanCoil:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["ChilledWater", "ChilledWaterDetailedFlatModel", "HeatExchangerAssistedChilledWater"]
        | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 14,
        heating_coil_type: Literal["Electric", "HotWater"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 50,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        capacity_control_method: Literal[
            "ASHRAE90VariableFan",
            "ConstantFanVariableFlow",
            "CyclingFan",
            "MultiSpeedFan",
            "VariableFanConstantFlow",
            "VariableFanVariableFlow",
        ]
        | None = ...,
        low_speed_supply_air_flow_ratio: float | None = 0.33,
        medium_speed_supply_air_flow_ratio: float | None = 0.66,
        outdoor_air_schedule_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:FanCoil`` and add it to the document.

        4 pipe fan coil unit with optional outdoor air.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonefancoil
        """

class ZoneHVACBaseboardRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_object: str,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_water_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        rated_average_water_temperature: float | None = 87.78,
        rated_water_mass_flow_rate: float | None = 0.063,
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        surface_fractions: Sequence[
            _g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsItem
            | _g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivewater
        """

class AnyCoilCoolingDXTwoStageWithHumidityControlMode:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        normal_mode_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"],
        normal_mode_stage_1_coil_performance_name: str,
        availability_schedule_name: str | None = ...,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        number_of_capacity_stages: int | None = 1,
        number_of_enhanced_dehumidification_modes: int | None = 0,
        normal_mode_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"] | None = ...,
        normal_mode_stage_1_2_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:TwoStageWithHumidityControlMode`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-stage with humidity control mode (e.g. sub-cool or hot gas reheat). Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data, see CoilPerformance:DX:Cooling. Stages are modeled as a face-split coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwostagewithhumiditycontrolmode
        """

class AnyGroundHeatExchangerSlinky:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        design_flow_rate: float | None = 0.002,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.4,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        pipe_outer_diameter: float | None = 0.02667,
        pipe_thickness: float | None = 0.002413,
        heat_exchanger_configuration: Literal["Horizontal", "Vertical"] | None = ...,
        coil_diameter: float | None = 1,
        coil_pitch: float | None = 0.2,
        trench_depth: float | None = 1.8,
        trench_length: float | None = 10,
        number_of_trenches: int | None = 1,
        horizontal_spacing_between_pipes: float | None = 2,
        maximum_length_of_simulation: float | None = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Slinky`` and add it to the document.

        This models a slinky horizontal heat exchanger placed in a series of trenches The model uses the model developed by: Xiong, Z., D.E. Fisher, and J.D. Spitler. 2015. Development and Validation of a Slinky Ground Heat Exchanger Model. Applied Energy 141: 57-69.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerslinky
        """

class DemandManagerAssignmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        meter_name: str,
        demand_limit_safety_fraction: float,
        demand_window_length: int,
        demand_manager_priority: Literal["All", "Sequential"],
        demand_limit_schedule_name: str | None = ...,
        billing_period_schedule_name: str | None = ...,
        peak_period_schedule_name: str | None = ...,
        manager_data: Sequence[
            _g.DemandManagerAssignmentListManagerDataItem | _g.DemandManagerAssignmentListManagerDataGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManagerAssignmentList`` and add it to the document.

        A high level control that makes demand limiting decisions based on a list of possible demand limiting strategies.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerassignmentlist
        """

class GeneratorWindTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_rotor_speed: float,
        rotor_diameter: float,
        overall_height: float,
        rated_power: float,
        rated_wind_speed: float,
        cut_in_wind_speed: float,
        cut_out_wind_speed: float,
        availability_schedule_name: str | None = ...,
        rotor_type: Literal["HorizontalAxisWindTurbine", "VerticalAxisWindTurbine"]
        | None = "HorizontalAxisWindTurbine",
        power_control: Literal[
            "FixedSpeedFixedPitch", "FixedSpeedVariablePitch", "VariableSpeedFixedPitch", "VariableSpeedVariablePitch"
        ]
        | None = "VariableSpeedVariablePitch",
        number_of_blades: float | None = 3,
        fraction_system_efficiency: float | None = 0.835,
        maximum_tip_speed_ratio: float | None = 5,
        maximum_power_coefficient: float | None = 0.25,
        annual_local_average_wind_speed: float | None = ...,
        height_for_local_average_wind_speed: float | None = 50,
        blade_chord_area: float | None = ...,
        blade_drag_coefficient: float | None = 0.9,
        blade_lift_coefficient: float | None = 0.05,
        power_coefficient_c1: float | None = 0.5176,
        power_coefficient_c2: float | None = 116,
        power_coefficient_c3: float | None = 0.4,
        power_coefficient_c4: float | None = 0,
        power_coefficient_c5: float | None = 5,
        power_coefficient_c6: float | None = 21,
    ) -> None:
        """Create a new ``Generator:WindTurbine`` and add it to the document.

        Wind turbine generator.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorwindturbine
        """
