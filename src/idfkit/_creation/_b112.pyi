"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WindowShadingControl:
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
            "OnIfHighSolarOrHighLuminanceTillMidnight",
            "OnIfHighSolarOrHighLuminanceTillNextMorning",
            "OnIfHighSolarOrHighLuminanceTillSunset",
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
        shading_control_sequence_number: int | None = 1,
        construction_with_shading_name: str | None = ...,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["No", "Yes"] | None = "No",
        glare_control_is_active: Literal["No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        daylighting_control_object_name: str | None = ...,
        multiple_surface_control_type: Literal["Group", "Sequential"] | None = "Sequential",
        fenestration_surfaces: Sequence[
            _g.WindowShadingControlFenestrationSurfacesItem | _g.WindowShadingControlFenestrationSurfacesGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowShadingControl`` and add it to the document.

        Specifies the type, location, and controls for window shades, window blinds, and switchable glazing. Referencing the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        ``fenestration_surfaces`` takes the extensible groups in order, one dict per group:

        ```python
        doc["WindowShadingControl"].add(
            "WindowShadingControl 1",
            zone_name="Zone 1",
            shading_type="BetweenGlassBlind",
            shading_control_type="AlwaysOff",
            fenestration_surfaces=[
                {"fenestration_surface_name": "Fenestration Surface 1"},
                {"fenestration_surface_name": "Fenestration Surface 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowshadingcontrol
        """

class SurfacePropertyConvectionCoefficients:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        surface_name: str,
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
            "ASTMC1340",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "BlockenWindard",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ],
        convection_coefficient_1: float | None = ...,
        convection_coefficient_1_schedule_name: str | None = ...,
        convection_coefficient_1_user_curve_name: str | None = ...,
        convection_coefficient_2_location: Literal["Inside", "Outside"] | None = ...,
        convection_coefficient_2_type: Literal[
            "ASHRAEVerticalWall",
            "ASTMC1340",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "BlockenWindard",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = ...,
        convection_coefficient_2: float | None = 0.1,
        convection_coefficient_2_schedule_name: str | None = ...,
        convection_coefficient_2_user_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SurfaceProperty:ConvectionCoefficients`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficients
        """

class ZoneHVACPackagedTerminalHeatPump:
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
        no_load_supply_air_flow_rate_control_set_to_low_speed: Literal["No", "Yes"] | None = "Yes",
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_convergence_tolerance: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["Autosize"] | None = "Autosize",
        dx_heating_coil_sizing_ratio: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalHeatPump`` and add it to the document.

        Packaged terminal heat pump (PTHP). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalheatpump
        """

class ZoneHVACUnitVentilator:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        outdoor_air_control_type: Literal["FixedAmount", "FixedTemperature", "VariablePercent"],
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"],
        minimum_outdoor_air_schedule_name: str,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_fraction_or_temperature_schedule_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"],
        supply_air_fan_name: str,
        coil_option: Literal["Cooling", "Heating", "HeatingAndCooling", "None"],
        availability_schedule_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
        exhaust_air_node_name: str | None = ...,
        mixed_air_node_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        heating_coil_name: str | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ]
        | None = ...,
        cooling_coil_name: str | None = ...,
        cooling_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:UnitVentilator`` and add it to the document.

        Unit ventilator. Forced-convection ventilation unit with supply fan (constant-volume or variable-volume), optional chilled water cooling coil, optional heating coil (gas, electric, hot water, or steam) and controllable outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacunitventilator
        """

class AirTerminalSingleDuctConstantVolumeFourPipeBeam:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        primary_air_availability_schedule_name: str | None = ...,
        cooling_availability_schedule_name: str | None = ...,
        heating_availability_schedule_name: str | None = ...,
        chilled_water_inlet_node_name: str | None = ...,
        chilled_water_outlet_node_name: str | None = ...,
        hot_water_inlet_node_name: str | None = ...,
        hot_water_outlet_node_name: str | None = ...,
        design_primary_air_volume_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_chilled_water_volume_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_hot_water_volume_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        zone_total_beam_length: float | Literal["Autosize"] | None = "Autosize",
        rated_primary_air_flow_rate_per_beam_length: float | None = 0.035,
        beam_rated_cooling_capacity_per_beam_length: float | None = 600,
        beam_rated_cooling_room_air_chilled_water_temperature_difference: float | None = 10,
        beam_rated_chilled_water_volume_flow_rate_per_beam_length: float | None = ...,
        beam_cooling_capacity_temperature_difference_modification_factor_curve_name: str | None = ...,
        beam_cooling_capacity_air_flow_modification_factor_curve_name: str | None = ...,
        beam_cooling_capacity_chilled_water_flow_modification_factor_curve_name: str | None = ...,
        beam_rated_heating_capacity_per_beam_length: float | None = 1500,
        beam_rated_heating_room_air_hot_water_temperature_difference: float | None = 27.8,
        beam_rated_hot_water_volume_flow_rate_per_beam_length: float | None = ...,
        beam_heating_capacity_temperature_difference_modification_factor_curve_name: str | None = ...,
        beam_heating_capacity_air_flow_modification_factor_curve_name: str | None = ...,
        beam_heating_capacity_hot_water_flow_modification_factor_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with heating and/or cooling. Operates as two-pipe unit if heating or cooling water is omitted. Heating and/or cooling can be scheduled off for dedicated ventilation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumefourpipebeam
        """

class CoilCoolingWaterToAirHeatPumpParameterEstimation:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        nominal_cooling_coil_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        load_side_outside_surface_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R22",
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        fan_delay_time: float | None = 60,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:ParameterEstimation`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Parameter estimation model is a deterministic model that requires a consistent set of parameters to describe the operating conditions of the heat pump components.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpparameterestimation
        """

class DehumidifierDesiccantNoFans:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        process_air_inlet_node_name: str | None = ...,
        process_air_outlet_node_name: str | None = ...,
        regeneration_air_inlet_node_name: str | None = ...,
        regeneration_fan_inlet_node_name: str | None = ...,
        control_type: Literal["LeavingMaximumHumidityRatioSetpoint", "SystemNodeMaximumHumidityRatioSetpoint"]
        | None = ...,
        leaving_maximum_humidity_ratio_setpoint: float | None = ...,
        nominal_process_air_flow_rate: float | None = ...,
        nominal_process_air_velocity: float | None = ...,
        rotor_power: float | None = ...,
        regeneration_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        regeneration_coil_name: str | None = ...,
        regeneration_fan_object_type: Literal["Fan:ConstantVolume", "Fan:SystemModel", "Fan:VariableVolume"]
        | None = ...,
        regeneration_fan_name: str | None = ...,
        performance_model_type: Literal["Default", "UserCurves"] | None = ...,
        leaving_dry_bulb_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        leaving_dry_bulb_function_of_air_velocity_curve_name: str | None = ...,
        leaving_humidity_ratio_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        leaving_humidity_ratio_function_of_air_velocity_curve_name: str | None = ...,
        regeneration_energy_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        regeneration_energy_function_of_air_velocity_curve_name: str | None = ...,
        regeneration_velocity_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        regeneration_velocity_function_of_air_velocity_curve_name: str | None = ...,
        nominal_regeneration_temperature: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Dehumidifier:Desiccant:NoFans`` and add it to the document.

        This object models a solid desiccant dehumidifier. The process air stream is the air which is dehumidified. The regeneration air stream is the air which is heated to regenerate the desiccant. This object determines the process air outlet conditions, the load on the regeneration heating coil, the electric power consumption for the wheel rotor motor, and the regeneration air fan mass flow rate. All other heat exchangers are modeled as separate objects connected to the inlet and outlet nodes of the dehumidifier. The solid desiccant dehumidifier is typically used in an AirLoopHVAC:OutdoorAirSystem, but can also be specified in any AirLoopHVAC.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-humidifiers-and-dehumidifiers/#dehumidifierdesiccantnofans
        """
