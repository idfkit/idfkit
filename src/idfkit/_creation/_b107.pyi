"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ScheduleTypeLimits:
    def __call__(
        self,
        name: str,
        /,
        *,
        lower_limit_value: float | None = ...,
        upper_limit_value: float | None = ...,
        numeric_type: Literal["Continuous", "Discrete"] | None = ...,
        unit_type: Literal[
            "ActivityLevel",
            "Angle",
            "Availability",
            "Capacity",
            "Control",
            "ConvectionCoefficient",
            "DeltaTemperature",
            "Dimensionless",
            "Mode",
            "Percent",
            "Power",
            "PrecipitationRate",
            "Temperature",
            "Velocity",
        ]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``ScheduleTypeLimits`` and add it to the document.

        ScheduleTypeLimits specifies the data types and limits for the values contained in schedules

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduletypelimits
        """

class WindowMaterialGlazingEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        front_side_beam_beam_solar_transmittance: float,
        back_side_beam_beam_solar_transmittance: float,
        front_side_beam_beam_solar_reflectance: float,
        back_side_beam_beam_solar_reflectance: float,
        optical_data_type: Literal["Spectral", "SpectralAverage"] | None = "SpectralAverage",
        window_glass_spectral_data_set_name: str | None = ...,
        front_side_beam_beam_visible_solar_transmittance: float | None = ...,
        back_side_beam_beam_visible_solar_transmittance: float | None = ...,
        front_side_beam_beam_visible_solar_reflectance: float | None = ...,
        back_side_beam_beam_visible_solar_reflectance: float | None = ...,
        front_side_beam_diffuse_solar_transmittance: float | None = 0,
        back_side_beam_diffuse_solar_transmittance: float | None = 0,
        front_side_beam_diffuse_solar_reflectance: float | None = 0,
        back_side_beam_diffuse_solar_reflectance: float | None = 0,
        front_side_beam_diffuse_visible_solar_transmittance: float | None = 0,
        back_side_beam_diffuse_visible_solar_transmittance: float | None = 0,
        front_side_beam_diffuse_visible_solar_reflectance: float | None = 0,
        back_side_beam_diffuse_visible_solar_reflectance: float | None = 0,
        diffuse_diffuse_solar_transmittance: float | Literal["Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        back_side_diffuse_diffuse_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        diffuse_diffuse_visible_solar_transmittance: float | Literal["Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_visible_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        back_side_diffuse_diffuse_visible_solar_reflectance: float | Literal["Autocalculate"] | None = "Autocalculate",
        infrared_transmittance_applies_to_front_and_back_: float | None = 0,
        front_side_infrared_emissivity: float | None = 0.84,
        back_side_infrared_emissivity: float | None = 0.84,
        thermal_resistance: float | None = 0.158,
    ) -> None:
        """Create a new ``WindowMaterial:Glazing:EquivalentLayer`` and add it to the document.

        Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialglazingequivalentlayer
        """

class Window:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Window`` and add it to the document.

        Allows for simplified entry of Windows.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#window
        """

class SurfacePropertyGroundSurfaces:
    def __call__(
        self,
        name: str,
        /,
        *,
        ground_surfaces: Sequence[
            _g.SurfacePropertyGroundSurfacesGroundSurfacesItem | _g.SurfacePropertyGroundSurfacesGroundSurfacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:GroundSurfaces`` and add it to the document.

        This object defines a list of ground surfaces for use with an exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertygroundsurfaces
        """

class RoomAirTemperaturePatternNondimensionalHeight:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        pairs: Sequence[
            _g.RoomAirTemperaturePatternNondimensionalHeightPairsItem
            | _g.RoomAirTemperaturePatternNondimensionalHeightPairsGroup
        ] = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:NondimensionalHeight`` and add it to the document.

        Defines a distribution pattern for air temperatures relative to the current mean air temperature as a function of height. The height, referred to as Zeta, is nondimensional by normalizing with the zone ceiling height. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternnondimensionalheight
        """

class ZoneHVACBaseboardRadiantConvectiveSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_object: str,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_steam_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        degree_of_subcooling: float | None = 5,
        surface_fractions: Sequence[
            _g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsItem
            | _g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Steam`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivesteam
        """

class ZoneHVACExhaustControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        inlet_node_name: str,
        outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        design_exhaust_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        flow_control_type: Literal["FollowSupply", "Scheduled"] | None = "Scheduled",
        exhaust_flow_fraction_schedule_name: str | None = ...,
        supply_node_or_nodelist_name: str | None = ...,
        minimum_zone_temperature_limit_schedule_name: str | None = ...,
        minimum_exhaust_flow_fraction_schedule_name: str | None = ...,
        balanced_exhaust_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:ExhaustControl`` and add it to the document.

        Defines a controlled exhaust flow from a zone which finally feeds into one of AirLoopHVAC:ZoneMixer's inlets, which are part of an AirLoopHVAC:ExhaustSystem.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#zonehvacexhaustcontrol
        """

class AnyZoneHVACEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_distribution_scheme: Literal["SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"]
        | None = "SequentialLoad",
        equipment: Sequence[_g.AnyZoneHVACEquipmentListEquipmentItem | _g.AnyZoneHVACEquipmentListEquipmentGroup] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EquipmentList`` and add it to the document.

        List equipment in simulation order. Note that an ZoneHVAC:AirDistributionUnit object must be listed in this statement if there is a forced air system serving the zone from the air loop. Equipment is simulated in the order specified by Zone Equipment Cooling Sequence and Zone Equipment Heating or No-Load Sequence, depending on the thermostat request. For equipment of similar type, assign sequence 1 to the first system intended to serve that type of load. For situations where one or more equipment types has limited capacity or limited control, order the sequence so that the most controllable piece of equipment runs last. For example, with a dedicated outdoor air system (DOAS), the air terminal for the DOAS should be assigned Heating Sequence = 1 and Cooling Sequence = 1. Any other equipment should be assigned sequence 2 or higher so that it will see the net load after the DOAS air is added to the zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#zonehvacequipmentlist
        """

class AnyControllerOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        relief_air_outlet_node_name: str,
        return_air_node_name: str,
        mixed_air_node_name: str,
        actuator_node_name: str,
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        economizer_control_type: Literal[
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
        economizer_control_action_type: Literal["MinimumFlowWithBypass", "ModulateFlow"] | None = "ModulateFlow",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        electronic_enthalpy_limit_curve_name: str | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        lockout_type: Literal["LockoutWithCompressor", "LockoutWithHeating", "NoLockout"] | None = "NoLockout",
        minimum_limit_type: Literal["FixedMinimum", "ProportionalMinimum"] | None = "ProportionalMinimum",
        minimum_outdoor_air_schedule_name: str | None = ...,
        minimum_fraction_of_outdoor_air_schedule_name: str | None = ...,
        maximum_fraction_of_outdoor_air_schedule_name: str | None = ...,
        mechanical_ventilation_controller_name: str | None = ...,
        time_of_day_economizer_control_schedule_name: str | None = ...,
        high_humidity_control: Literal["No", "Yes"] | None = "No",
        humidistat_control_zone_name: str | None = ...,
        high_humidity_outdoor_air_flow_ratio: float | None = 1,
        control_high_indoor_humidity_based_on_outdoor_humidity_ratio: Literal["No", "Yes"] | None = "Yes",
        heat_recovery_bypass_control_type: Literal[
            "BypassWhenOAFlowGreaterThanMinimum", "BypassWhenWithinEconomizerLimits"
        ]
        | None = "BypassWhenWithinEconomizerLimits",
    ) -> None:
        """Create a new ``Controller:OutdoorAir`` and add it to the document.

        Controller to set the outdoor air flow rate for an air loop. Control options include fixed, proportional, scheduled, economizer, and demand-controlled ventilation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-controllers/#controlleroutdoorair
        """

class AnyChillerHeaterPerformanceElectricEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_cooling_mode_evaporator_capacity: float | Literal["Autosize"],
        reference_cooling_mode_cop: float,
        cooling_mode_cooling_capacity_function_of_temperature_curve_name: str,
        cooling_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        cooling_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        heating_mode_cooling_capacity_function_of_temperature_curve_name: str,
        heating_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        heating_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        reference_cooling_mode_leaving_chilled_water_temperature: float | None = 6.67,
        reference_cooling_mode_entering_condenser_fluid_temperature: float | None = 29.44,
        reference_cooling_mode_leaving_condenser_water_temperature: float | None = 35,
        reference_heating_mode_cooling_capacity_ratio: float | None = 0.75,
        reference_heating_mode_cooling_power_input_ratio: float | None = 1.38,
        reference_heating_mode_leaving_chilled_water_temperature: float | None = 6.67,
        reference_heating_mode_leaving_condenser_water_temperature: float | None = 49,
        reference_heating_mode_entering_condenser_fluid_temperature: float | None = 29.44,
        heating_mode_entering_chilled_water_temperature_low_limit: float | None = 12.22,
        chilled_water_flow_mode_type: Literal["ConstantFlow", "VariableFlow"] | None = "ConstantFlow",
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_hot_water_flow_rate: float | None = 0,
        compressor_motor_efficiency: float | None = 1,
        cooling_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "EnteringCondenser",
        cooling_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        heating_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "LeavingCondenser",
        heating_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``ChillerHeaterPerformance:Electric:EIR`` and add it to the document.

        This chiller model is a generic chiller-heater where the cooling mode performance is a function of condenser entering or leaving fluid temperature and the heating mode performance is typically a function of condenser leaving fluid temperature. Performance at off-reference conditions is modeled using three polynomial equations per mode. Six curve objects are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerheaterperformanceelectriceir
        """

class AnyGroundHeatExchangerPond:
    def __call__(
        self,
        name: str,
        /,
        *,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        pond_depth: float,
        pond_area: float,
        hydronic_tubing_inside_diameter: float,
        hydronic_tubing_outside_diameter: float,
        hydronic_tubing_thermal_conductivity: float,
        ground_thermal_conductivity: float,
        number_of_tubing_circuits: int,
        length_of_each_tubing_circuit: float,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Pond`` and add it to the document.

        A model of a shallow pond with immersed pipe loops. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerpond
        """

class ParametricLogic:
    def __call__(
        self, name: str, /, *, lines: Sequence[_g.ParametricLogicLinesItem | _g.ParametricLogicLinesGroup] = ...
    ) -> None:
        """Create a new ``Parametric:Logic`` and add it to the document.

        This object allows some types of objects to be included for some parametric cases and not for others. For example, you might want an overhang on a window in some parametric runs and not others. A single Parametric:Logic object is allowed per file. Consult the Input Output Reference for available commands and syntax.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/parametric-objects/#parametriclogic
        """
