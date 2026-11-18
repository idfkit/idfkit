"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SurfaceConvectionAlgorithmOutsideUserCurve:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        wind_speed_type_for_curve: Literal[
            "", "HeightAdjust", "ParallelComponent", "ParallelComponentHeightAdjust", "WeatherFile"
        ]
        | None = "HeightAdjust",
        hf_function_of_wind_speed_curve_name: str | None = ...,
        hn_function_of_temperature_difference_curve_name: str | None = ...,
        hn_function_of_temperature_difference_divided_by_height_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Outside:UserCurve`` and add it to the document.

        Used to describe a custom model equation for surface convection heat transfer coefficient If more than one curve is referenced they are all used and added together.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfaceconvectionalgorithmoutsideusercurve
        """

class AnySurfacePropertySurroundingSurfaces:
    def __call__(
        self,
        name: str,
        /,
        *,
        sky_view_factor: float | None = ...,
        sky_temperature_schedule_name: str | None = ...,
        ground_view_factor: float | None = ...,
        ground_temperature_schedule_name: str | None = ...,
        surfaces: Sequence[
            _g.SurfacePropertySurroundingSurfacesSurfacesItem | _g.SurfacePropertySurroundingSurfacesSurfacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:SurroundingSurfaces`` and add it to the document.

        This object defines a list of surrounding surfaces for an exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertysurroundingsurfaces
        """

class RoomAirTemperaturePatternTwoGradient:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_two_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_height: float | None = ...,
        return_air_height: float | None = ...,
        exhaust_air_height: float | None = ...,
        temperature_gradient_lower_bound: float | None = ...,
        temperature_gradient_upper_bound: float | None = ...,
        gradient_interpolation_mode: Literal[
            "OutdoorDryBulbTemperature",
            "SensibleCoolingLoad",
            "SensibleHeatingLoad",
            "ZoneAndOutdoorTemperatureDifference",
            "ZoneDryBulbTemperature",
        ]
        | None = ...,
        upper_temperature_bound: float | None = ...,
        lower_temperature_bound: float | None = ...,
        upper_heat_rate_bound: float | None = ...,
        lower_heat_rate_bound: float | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:TwoGradient`` and add it to the document.

        Used to model room air with two temperature gradients in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatterntwogradient
        """

class RoomAirSettingsUnderFloorAirDistributionInterior:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        number_of_diffusers: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        power_per_plume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        design_effective_area_of_diffuser: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        diffuser_slot_angle_from_vertical: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        thermostat_height: float | None = 1.2,
        comfort_height: float | None = 1.1,
        temperature_difference_threshold_for_reporting: float | None = 0.4,
        floor_diffuser_type: Literal["", "Custom", "HorizontalSwirl", "LinearBarGrille", "Swirl", "VariableArea"]
        | None = "Swirl",
        transition_height: float | Literal["", "Autocalculate"] | None = 1.7,
        coefficient_a: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_b: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_c: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_d: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_e: float | Literal["", "Autocalculate"] | None = "Autocalculate",
    ) -> None:
        """Create a new ``RoomAirSettings:UnderFloorAirDistributionInterior`` and add it to the document.

        This Room Air Model is applicable to interior spaces that are served by an underfloor air distribution system. The dominant sources of heat gain should be from people, equipment, and other localized sources located in the occupied part of the room. The model should be used with caution in zones which have large heat gains or losses through exterior walls or windows or which have considerable direct solar gain. Used with RoomAirModelType = UnderFloorAirDistributionInterior.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairsettingsunderfloorairdistributioninterior
        """

class SteamEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        steam_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``SteamEquipment:Instance`` and add it to the document.

        Sets internal gains for steam equipment in the zone. The physical characteristics are given by the referenced SteamEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#steamequipmentinstance
        """

class AirflowNetworkMultiZoneExternalNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        wind_pressure_coefficient_curve_name: str,
        external_node_height: float | None = 0,
        symmetric_wind_pressure_coefficient_curve: Literal["", "No", "Yes"] | None = "No",
        wind_angle_type: Literal["", "Absolute", "Relative"] | None = "Absolute",
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:ExternalNode`` and add it to the document.

        This object defines outdoor environmental conditions outside of the building.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizoneexternalnode
        """

class HVACTemplateSystemPackagedVAV:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        supply_fan_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_minimum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 1000,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["", "TwoSpeedDX", "TwoSpeedHumidControlDX"] | None = "TwoSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 12.8,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "None",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 10,
        heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_control_type: Literal["", "FixedMinimum", "ProportionalMinimum"]
        | None = "ProportionalMinimum",
        minimum_outdoor_air_schedule_name: str | None = ...,
        economizer_type: Literal[
            "",
            "DifferentialDryBulb",
            "DifferentialDryBulbAndEnthalpy",
            "DifferentialEnthalpy",
            "ElectronicEnthalpy",
            "FixedDewPointAndDryBulb",
            "FixedDryBulb",
            "FixedEnthalpy",
            "NoEconomizer",
        ]
        | None = "NoEconomizer",
        economizer_lockout: Literal["", "LockoutWithCompressor", "LockoutWithHeating", "NoLockout"]
        | None = "NoLockout",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        supply_fan_part_load_power_coefficients: Literal[
            "",
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
        night_cycle_control: Literal["", "CycleOnAny", "CycleOnAnyZoneFansOnly", "CycleOnControlZone", "StayOff"]
        | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        cooling_coil_setpoint_reset_type: Literal[
            "", "None", "OutdoorAirTemperatureReset", "Warmest", "WarmestTemperatureFirst"
        ]
        | None = "None",
        heating_coil_setpoint_reset_type: Literal["", "None", "OutdoorAirTemperatureReset"] | None = "None",
        dehumidification_control_type: Literal["", "CoolReheat", "None"] | None = "None",
        dehumidification_control_zone_name: str | None = ...,
        dehumidification_setpoint: float | None = 60,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_setpoint: float | None = 30,
        sizing_option: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 500,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
        return_fan_part_load_power_coefficients: Literal[
            "",
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
    ) -> None:
        """Create a new ``HVACTemplate:System:PackagedVAV`` and add it to the document.

        Packaged Variable Air Volume (PVAV) air loop with optional heating coil and optional preheat.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystempackagedvav
        """

class AnyZoneHVACCoolingPanelRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        maximum_chilled_water_flow_rate: float | Literal["Autosize"],
        fraction_radiant: float,
        rated_inlet_water_temperature: float | None = 5,
        rated_inlet_space_temperature: float | None = 24,
        rated_water_mass_flow_rate: float | None = 0.063,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "ZoneTotalLoad",
            "ZoneConvectiveLoad",
        ]
        | None = "MeanAirTemperature",
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: Sequence[
            _g.ZoneHVACCoolingPanelRadiantConvectiveWaterSurfaceFractionsItem
            | _g.ZoneHVACCoolingPanelRadiantConvectiveWaterSurfaceFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:CoolingPanel:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaccoolingpanelradiantconvectivewater
        """

class ZoneHVACAirDistributionUnit:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_distribution_unit_outlet_node_name: str,
        air_terminal_object_type: Literal[
            "AirTerminal:DualDuct:ConstantVolume",
            "AirTerminal:DualDuct:VAV",
            "AirTerminal:DualDuct:VAV:OutdoorAir",
            "AirTerminal:SingleDuct:ConstantVolume:CooledBeam",
            "AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam",
            "AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction",
            "AirTerminal:SingleDuct:ConstantVolume:NoReheat",
            "AirTerminal:SingleDuct:ConstantVolume:Reheat",
            "AirTerminal:SingleDuct:Mixer",
            "AirTerminal:SingleDuct:ParallelPIU:Reheat",
            "AirTerminal:SingleDuct:SeriesPIU:Reheat",
            "AirTerminal:SingleDuct:UserDefined",
            "AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat",
            "AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat",
            "AirTerminal:SingleDuct:VAV:NoReheat",
            "AirTerminal:SingleDuct:VAV:Reheat",
            "AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan",
        ],
        air_terminal_name: str,
        nominal_upstream_leakage_fraction: float | None = 0,
        constant_downstream_leakage_fraction: float | None = 0,
        design_specification_air_terminal_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:AirDistributionUnit`` and add it to the document.

        Central air system air distribution unit, serves as a wrapper for a specific type of air terminal unit. This object is referenced in a ZoneHVAC:EquipmentList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#zonehvacairdistributionunit
        """

class RefrigerationSubcooler:
    def __call__(
        self,
        name: str,
        /,
        *,
        subcooler_type: Literal["", "LiquidSuction", "Mechanical"] | None = "LiquidSuction",
        liquid_suction_design_subcooling_temperature_difference: float | None = ...,
        design_liquid_inlet_temperature: float | None = ...,
        design_vapor_inlet_temperature: float | None = ...,
        capacity_providing_system: str | None = ...,
        outlet_control_temperature: float | None = ...,
    ) -> None:
        """Create a new ``Refrigeration:Subcooler`` and add it to the document.

        Two types of subcoolers are modeled by the detailed refrigeration system. The liquid suction heat exchanger uses cool suction gas to subcool the hot condensate after it leaves the condenser and before it reaches the thermal expansion valve. A mechanical subcooler is used to transfer cooling capacity from one refrigeration system to another.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationsubcooler
        """

class OutputControlResilienceSummaries:
    def __call__(self, /, *, heat_index_algorithm: Literal["", "Extended", "Simplified"] | None = "Simplified") -> None:
        """Create a new ``OutputControl:ResilienceSummaries`` and add it to the document.

        Specifies methods for resilience reporting variables

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputcontrolresiliencesummaries
        """
