"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SurfaceConvectionAlgorithmInsideAdaptiveModelSelections:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        simple_buoyancy_vertical_wall_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq6NonHeatedWalls",
            "UserCurve",
        ]
        | None = "FohannoPolidoriVerticalWall",
        simple_buoyancy_vertical_wall_user_curve_name: str | None = ...,
        simple_buoyancy_stable_horizontal_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "AlamdariHammondStableHorizontal",
        simple_buoyancy_stable_horizontal_equation_user_curve_name: str | None = ...,
        simple_buoyancy_unstable_horizontal_equation_source: Literal[
            "", "AlamdariHammondUnstableHorizontal", "UserCurve", "WaltonUnstableHorizontalOrTilt"
        ]
        | None = "AlamdariHammondUnstableHorizontal",
        simple_buoyancy_unstable_horizontal_equation_user_curve_name: str | None = ...,
        simple_buoyancy_stable_tilted_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "WaltonStableHorizontalOrTilt",
        simple_buoyancy_stable_tilted_equation_user_curve_name: str | None = ...,
        simple_buoyancy_unstable_tilted_equation_source: Literal[
            "", "AlamdariHammondUnstableHorizontal", "UserCurve", "WaltonUnstableHorizontalOrTilt"
        ]
        | None = "WaltonUnstableHorizontalOrTilt",
        simple_buoyancy_unstable_tilted_equation_user_curve_name: str | None = ...,
        simple_buoyancy_windows_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "UserCurve",
        ]
        | None = "ISO15099Windows",
        simple_buoyancy_windows_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_vertical_wall_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KhalifaEq3WallAwayFromHeat",
            "UserCurve",
        ]
        | None = "KhalifaEq3WallAwayFromHeat",
        floor_heat_ceiling_cool_vertical_wall_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_stable_horizontal_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "AlamdariHammondStableHorizontal",
        floor_heat_ceiling_cool_stable_horizontal_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_unstable_horizontal_equation_source: Literal[
            "",
            "AlamdariHammondUnstableHorizontal",
            "KhalifaEq4CeilingAwayFromHeat",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "KhalifaEq4CeilingAwayFromHeat",
        floor_heat_ceiling_cool_unstable_horizontal_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_heated_floor_equation_source: Literal[
            "",
            "AlamdariHammondUnstableHorizontal",
            "AwbiHattonHeatedFloor",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "AwbiHattonHeatedFloor",
        floor_heat_ceiling_cool_heated_floor_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_chilled_ceiling_equation_source: Literal[
            "",
            "AlamdariHammondUnstableHorizontal",
            "KaradagChilledCeiling",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "KaradagChilledCeiling",
        floor_heat_ceiling_cool_chilled_ceiling_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_stable_tilted_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "ISO15099Windows", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "WaltonStableHorizontalOrTilt",
        floor_heat_ceiling_cool_stable_tilted_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_unstable_tilted_equation_source: Literal[
            "", "AlamdariHammondUnstableHorizontal", "ISO15099Windows", "UserCurve", "WaltonUnstableHorizontalOrTilt"
        ]
        | None = "WaltonUnstableHorizontalOrTilt",
        floor_heat_ceiling_cool_unstable_tilted_equation_user_curve_name: str | None = ...,
        floor_heat_ceiling_cool_window_equation_source: Literal[
            "", "ASHRAEVerticalWall", "AlamdariHammondVerticalWall", "ISO15099Windows", "UserCurve"
        ]
        | None = "ISO15099Windows",
        floor_heat_ceiling_cool_window_equation_user_curve_name: str | None = ...,
        wall_panel_heating_vertical_wall_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KhalifaEq6NonHeatedWalls",
            "UserCurve",
        ]
        | None = "KhalifaEq6NonHeatedWalls",
        wall_panel_heating_vertical_wall_equation_user_curve_name: str | None = ...,
        wall_panel_heating_heated_wall_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KhalifaEq5WallNearHeat",
            "UserCurve",
        ]
        | None = "AwbiHattonHeatedWall",
        wall_panel_heating_heated_wall_equation_user_curve_name: str | None = ...,
        wall_panel_heating_stable_horizontal_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "AlamdariHammondStableHorizontal",
        wall_panel_heating_stable_horizontal_equation_user_curve_name: str | None = ...,
        wall_panel_heating_unstable_horizontal_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondUnstableHorizontal",
            "KaradagChilledCeiling",
            "KhalifaEq7Ceiling",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "KhalifaEq7Ceiling",
        wall_panel_heating_unstable_horizontal_equation_user_curve_name: str | None = ...,
        wall_panel_heating_stable_tilted_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "ISO15099Windows", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "WaltonStableHorizontalOrTilt",
        wall_panel_heating_stable_tilted_equation_user_curve_name: str | None = ...,
        wall_panel_heating_unstable_tilted_equation_source: Literal[
            "", "AlamdariHammondUnstableHorizontal", "ISO15099Windows", "UserCurve", "WaltonUnstableHorizontalOrTilt"
        ]
        | None = "WaltonUnstableHorizontalOrTilt",
        wall_panel_heating_unstable_tilted_equation_user_curve_name: str | None = ...,
        wall_panel_heating_window_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "UserCurve",
        ]
        | None = "ISO15099Windows",
        wall_panel_heating_window_equation_user_curve_name: str | None = ...,
        convective_zone_heater_vertical_wall_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq6NonHeatedWalls",
            "UserCurve",
        ]
        | None = "FohannoPolidoriVerticalWall",
        convective_zone_heater_vertical_wall_equation_user_curve_name: str | None = ...,
        convective_zone_heater_vertical_walls_near_heater_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KhalifaEq5WallNearHeat",
            "UserCurve",
        ]
        | None = "KhalifaEq5WallNearHeat",
        convective_zone_heater_vertical_walls_near_heater_equation_user_curve_name: str | None = ...,
        convective_zone_heater_stable_horizontal_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "AlamdariHammondStableHorizontal",
        convective_zone_heater_stable_horizontal_equation_user_curve_name: str | None = ...,
        convective_zone_heater_unstable_horizontal_equation_source: Literal[
            "",
            "AlamdariHammondUnstableHorizontal",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq7Ceiling",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "KhalifaEq7Ceiling",
        convective_zone_heater_unstable_horizontal_equation_user_curve_name: str | None = ...,
        convective_zone_heater_stable_tilted_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "WaltonStableHorizontalOrTilt",
        convective_zone_heater_stable_tilted_equation_user_curve_name: str | None = ...,
        convective_zone_heater_unstable_tilted_equation_source: Literal[
            "", "AlamdariHammondUnstableHorizontal", "UserCurve", "WaltonUnstableHorizontalOrTilt"
        ]
        | None = "WaltonUnstableHorizontalOrTilt",
        convective_zone_heater_unstable_tilted_equation_user_curve_name: str | None = ...,
        convective_zone_heater_windows_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "KhalifaEq3WallAwayFromHeat",
            "UserCurve",
        ]
        | None = "ISO15099Windows",
        convective_zone_heater_windows_equation_user_curve_name: str | None = ...,
        central_air_diffuser_wall_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "ISO15099Windows",
            "UserCurve",
        ]
        | None = "GoldsteinNovoselacCeilingDiffuserWalls",
        central_air_diffuser_wall_equation_user_curve_name: str | None = ...,
        central_air_diffuser_ceiling_equation_source: Literal[
            "",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "FisherPedersenCeilingDiffuserCeiling",
            "UserCurve",
        ]
        | None = "FisherPedersenCeilingDiffuserCeiling",
        central_air_diffuser_ceiling_equation_user_curve_name: str | None = ...,
        central_air_diffuser_floor_equation_source: Literal[
            "",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableFloor",
            "FisherPedersenCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "UserCurve",
        ]
        | None = "GoldsteinNovoselacCeilingDiffuserFloor",
        central_air_diffuser_floor_equation_user_curve_name: str | None = ...,
        central_air_diffuser_window_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "UserCurve",
        ]
        | None = "GoldsteinNovoselacCeilingDiffuserWindow",
        central_air_diffuser_window_equation_user_curve_name: str | None = ...,
        mechanical_zone_fan_circulation_vertical_wall_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "ISO15099Windows",
            "KhalifaEq3WallAwayFromHeat",
            "UserCurve",
        ]
        | None = "KhalifaEq3WallAwayFromHeat",
        mechanical_zone_fan_circulation_vertical_wall_equation_user_curve_name: str | None = ...,
        mechanical_zone_fan_circulation_stable_horizontal_equation_source: Literal[
            "", "AlamdariHammondStableHorizontal", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "AlamdariHammondStableHorizontal",
        mechanical_zone_fan_circulation_stable_horizontal_equation_user_curve_name: str | None = ...,
        mechanical_zone_fan_circulation_unstable_horizontal_equation_source: Literal[
            "",
            "AlamdariHammondUnstableHorizontal",
            "KhalifaEq4CeilingAwayFromHeat",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "KhalifaEq4CeilingAwayFromHeat",
        mechanical_zone_fan_circulation_unstable_horizontal_equation_user_curve_name: str | None = ...,
        mechanical_zone_fan_circulation_stable_tilted_equation_source: Literal[
            "", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "WaltonStableHorizontalOrTilt",
        mechanical_zone_fan_circulation_stable_tilted_equation_user_curve_name: str | None = ...,
        mechanical_zone_fan_circulation_unstable_tilted_equation_source: Literal[
            "", "AlamdariHammondUnstableHorizontal", "UserCurve", "WaltonUnstableHorizontalOrTilt"
        ]
        | None = "WaltonUnstableHorizontalOrTilt",
        mechanical_zone_fan_circulation_unstable_tilted_equation_user_curve_name: str | None = ...,
        mechanical_zone_fan_circulation_window_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "UserCurve",
        ]
        | None = "ISO15099Windows",
        mechanical_zone_fan_circulation_window_equation_user_curve_name: str | None = ...,
        mixed_regime_buoyancy_assisting_flow_on_walls_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "UserCurve",
        ]
        | None = "BeausoleilMorrisonMixedAssistedWall",
        mixed_regime_buoyancy_assisting_flow_on_walls_equation_user_curve_name: str | None = ...,
        mixed_regime_buoyancy_opposing_flow_on_walls_equation_source: Literal[
            "",
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "UserCurve",
        ]
        | None = "BeausoleilMorrisonMixedOpposingWall",
        mixed_regime_buoyancy_opposing_flow_on_walls_equation_user_curve_name: str | None = ...,
        mixed_regime_stable_floor_equation_source: Literal[
            "",
            "AlamdariHammondStableHorizontal",
            "BeausoleilMorrisonMixedStableFloor",
            "UserCurve",
            "WaltonStableHorizontalOrTilt",
        ]
        | None = "BeausoleilMorrisonMixedStableFloor",
        mixed_regime_stable_floor_equation_user_curve_name: str | None = ...,
        mixed_regime_unstable_floor_equation_source: Literal[
            "",
            "AlamdariHammondUnstableHorizontal",
            "BeausoleilMorrisonMixedUnstableFloor",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "BeausoleilMorrisonMixedUnstableFloor",
        mixed_regime_unstable_floor_equation_user_curve_name: str | None = ...,
        mixed_regime_stable_ceiling_equation_source: Literal[
            "",
            "AlamdariHammondStableHorizontal",
            "BeausoleilMorrisonMixedStableCeiling",
            "UserCurve",
            "WaltonStableHorizontalOrTilt",
        ]
        | None = "BeausoleilMorrisonMixedStableCeiling",
        mixed_regime_stable_ceiling_equation_user_curve_name: str | None = ...,
        mixed_regime_unstable_ceiling_equation_source: Literal[
            "",
            "AlamdariHammondUnstableHorizontal",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "UserCurve",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = "BeausoleilMorrisonMixedUnstableCeiling",
        mixed_regime_unstable_ceiling_equation_user_curve_name: str | None = ...,
        mixed_regime_window_equation_source: Literal[
            "", "GoldsteinNovoselacCeilingDiffuserWindow", "ISO15099Windows", "UserCurve"
        ]
        | None = "GoldsteinNovoselacCeilingDiffuserWindow",
        mixed_regime_window_equation_user_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Inside:AdaptiveModelSelections`` and add it to the document.

        Options to change the individual convection model equations for dynamic selection when using AdaptiveConvectiongAlgorithm This object is only needed to make changes to the default model selections for any or all of the surface categories. This object is for the inside face, the side of the surface facing a thermal zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfaceconvectionalgorithminsideadaptivemodelselections
        """

class GroundHeatTransferSlabBoundConds:
    def __call__(
        self,
        /,
        *,
        evtr_is_surface_evapotranspiration_modeled: Literal["FALSE", "TRUE"],
        fixbc_is_the_lower_boundary_at_a_fixed_temperature: Literal["FALSE", "TRUE"],
        usrhflag_is_the_ground_surface_h_specified_by_the_user_: Literal["FALSE", "TRUE"],
        tdeepin: float | None = ...,
        userh_user_specified_ground_surface_heat_transfer_coefficient: float | None = ...,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:BoundConds`` and add it to the document.

        Supplies some of the boundary conditions used in the ground heat transfer calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabboundconds
        """

class RoomAirTemperaturePatternSurfaceMapping:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        surface_deltas: Sequence[
            _g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasItem
            | _g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasGroup
        ] = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:SurfaceMapping`` and add it to the document.

        Defines a distribution pattern for the air temperatures adjacent to individual surfaces. This allows controlling the adjacent air temperature on a surface-by-surface basis rather than by height. This allows modeling different adjacent air temperatures on the opposite sides of the zone. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternsurfacemapping
        """

class ThermostatSetpointThermalComfortFangerSingleCooling:
    def __call__(self, name: str, /, *, fanger_thermal_comfort_schedule_name: str) -> None:
        """Create a new ``ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling`` and add it to the document.

        Used for cooling only thermal comfort control. The PMV setpoint can be scheduled and varied throughout the simulation but only cooling is allowed with this control type.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointthermalcomfortfangersinglecooling
        """

class AirLoopHVACUnitaryFurnaceHeatOnly:
    def __call__(
        self,
        name: str,
        /,
        *,
        furnace_air_inlet_node_name: str,
        furnace_air_outlet_node_name: str,
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
    ) -> None:
        """Create a new ``AirLoopHVAC:Unitary:Furnace:HeatOnly`` and add it to the document.

        Unitary system, heating-only with constant volume supply fan (continuous or cycling) and heating coil (gas, electric, hot water, or steam). Identical to AirLoopHVAC:UnitaryHeatOnly.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryfurnaceheatonly
        """

class AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        bypass_duct_mixer_node_name: str,
        bypass_duct_splitter_node_name: str,
        air_outlet_node_name: str,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"],
        outdoor_air_mixer_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        outdoor_air_flow_rate_multiplier_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        priority_control_mode: Literal["", "CoolingPriority", "HeatingPriority", "LoadPriority", "ZonePriority"]
        | None = "ZonePriority",
        minimum_outlet_air_temperature_during_cooling_operation: float | None = 8,
        maximum_outlet_air_temperature_during_heating_operation: float | None = 50,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        plenum_or_mixer_inlet_node_name: str | None = ...,
        minimum_runtime_before_operating_mode_change: float | None = 0.25,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, steam, or DX air-to-air heat pump) and bypass damper for variable volume flow to terminal units. Used with AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat or AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatcoolvavchangeoverbypass
        """

class AnyAirConditionerVariableRefrigerantFlow:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_terminal_unit_list_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        gross_rated_cooling_cop: float | None = 3.3,
        cooling_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_capacity_ratio_boundary_curve_name: str | None = ...,
        cooling_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_boundary_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        cooling_combination_ratio_correction_factor_curve_name: str | None = ...,
        cooling_part_load_fraction_correlation_curve_name: str | None = ...,
        gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        heating_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_capacity_ratio_boundary_curve_name: str | None = ...,
        heating_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_boundary_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_performance_curve_outdoor_temperature_type: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        heating_combination_ratio_correction_factor_curve_name: str | None = ...,
        heating_part_load_fraction_correlation_curve_name: str | None = ...,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = ...,
        vertical_height_used_for_piping_correction_factor: float | None = ...,
        piping_correction_factor_for_length_in_cooling_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_cooling_mode_coefficient: float | None = 0,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = ...,
        piping_correction_factor_for_length_in_heating_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_heating_mode_coefficient: float | None = 0,
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
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        water_condenser_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        supply_water_storage_tank_name: str | None = ...,
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
        heat_recovery_cooling_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_capacity_fraction: float | None = 0.5,
        heat_recovery_cooling_capacity_time_constant: float | None = 0.15,
        heat_recovery_cooling_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        heat_recovery_heating_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0.15,
        heat_recovery_heating_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow`` and add it to the document.

        Variable refrigerant flow (VRF) air-to-air heat pump condensing unit (includes one or more electric compressors and outdoor fan). Serves one or more VRF zone terminal units. See ZoneHVAC:TerminalUnit:VariableRefrigerantFlow and ZoneTerminalUnitList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflow
        """

class LoadProfilePlant:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        load_schedule_name: str,
        peak_flow_rate: float,
        flow_rate_fraction_schedule_name: str,
        plant_loop_fluid_type: Literal["", "Steam", "Water"] | None = "Water",
        degree_of_subcooling: float | None = 5,
        degree_of_loop_subcooling: float | None = 20,
    ) -> None:
        """Create a new ``LoadProfile:Plant`` and add it to the document.

        Used to simulate a scheduled plant loop demand profile. Load and flow rate are specified using schedules. Positive values are heating loads, and negative values are cooling loads. The actual load met is dependent on the performance of the supply loop components. Optional inputs for steam loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-non-zone-equipment/#loadprofileplant
        """

class PlantEquipmentOperationOutdoorRelativeHumidity:
    def __call__(
        self,
        name: str,
        /,
        *,
        relative_humidity_range_1_lower_limit: float,
        relative_humidity_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        relative_humidity_range_2_lower_limit: float | None = ...,
        relative_humidity_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        relative_humidity_range_3_lower_limit: float | None = ...,
        relative_humidity_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        relative_humidity_range_4_lower_limit: float | None = ...,
        relative_humidity_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        relative_humidity_range_5_lower_limit: float | None = ...,
        relative_humidity_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        relative_humidity_range_6_lower_limit: float | None = ...,
        relative_humidity_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        relative_humidity_range_7_lower_limit: float | None = ...,
        relative_humidity_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        relative_humidity_range_8_lower_limit: float | None = ...,
        relative_humidity_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        relative_humidity_range_9_lower_limit: float | None = ...,
        relative_humidity_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        relative_humidity_range_10_lower_limit: float | None = ...,
        relative_humidity_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:OutdoorRelativeHumidity`` and add it to the document.

        Plant equipment operation scheme for outdoor relative humidity range operation. Specifies one or more groups of equipment which are available to operate for successive outdoor relative humidity ranges.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationoutdoorrelativehumidity
        """

class AvailabilityManagerLowTemperatureTurnOn:
    def __call__(self, name: str, /, *, sensor_node_name: str, temperature: float) -> None:
        """Create a new ``AvailabilityManager:LowTemperatureTurnOn`` and add it to the document.

        Overrides fan/pump schedules depending on temperature at sensor node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerlowtemperatureturnon
        """

class SetpointManagerSingleZoneReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        zone_node_name: str,
        zone_inlet_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        minimum_supply_air_temperature: float | None = -99,
        maximum_supply_air_temperature: float | None = 99,
    ) -> None:
        """Create a new ``SetpointManager:SingleZone:Reheat`` and add it to the document.

        This setpoint manager detects the control zone load, zone inlet node flow rate, and zone node temperature and calculates a setpoint temperature for the supply air that will satisfy the zone load (heating or cooling) for the control zone. This setpoint manager is not limited to reheat applications.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezonereheat
        """

class SetpointManagerMultiZoneMaximumHumidityAverage:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_humidity_ratio: float | None = 0.008,
        maximum_setpoint_humidity_ratio: float | None = 0.015,
    ) -> None:
        """Create a new ``SetpointManager:MultiZone:MaximumHumidity:Average`` and add it to the document.

        This setpoint manager sets the average supply air maximum humidity ratio based on moisture load requirements of all controlled zones in an air loop served by a central air-conditioner.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagermultizonemaximumhumidityaverage
        """

class RefrigerationSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        refrigeration_condenser_name: str,
        compressor_or_compressorlist_name: str,
        minimum_condensing_temperature: float,
        refrigeration_system_working_fluid_type: str,
        refrigerated_case_or_walkin_or_caseandwalkinlist_name: str | None = ...,
        refrigeration_transfer_load_or_transferload_list_name: str | None = ...,
        suction_temperature_control_type: Literal["", "ConstantSuctionTemperature", "FloatSuctionTemperature"]
        | None = "ConstantSuctionTemperature",
        mechanical_subcooler_name: str | None = ...,
        liquid_suction_heat_exchanger_subcooler_name: str | None = ...,
        sum_ua_suction_piping: float | None = 0,
        suction_piping_zone_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        number_of_compressor_stages: Literal[1, 2, ""] | None = 1,
        intercooler_type: Literal["", "Flash Intercooler", "None", "Shell-and-Coil Intercooler"] | None = "None",
        shell_and_coil_intercooler_effectiveness: float | None = 0.8,
        high_stage_compressor_or_compressorlist_name: str | None = ...,
    ) -> None:
        """Create a new ``Refrigeration:System`` and add it to the document.

        Simulates the performance of a supermarket refrigeration system when used along with other objects to define the refrigeration load(s), the compressor(s), and the condenser.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationsystem
        """

class AnyPhotovoltaicPerformanceEquivalentOneDiode:
    def __call__(
        self,
        name: str,
        /,
        *,
        cell_type: Literal["AmorphousSilicon", "CrystallineSilicon"] | None = ...,
        number_of_cells_in_series: int | None = 36,
        active_area: float | None = 0.89,
        transmittance_absorptance_product: float | None = 0.95,
        semiconductor_bandgap: float | None = 1.12,
        shunt_resistance: float | None = 1000000,
        short_circuit_current: float | None = 6.5,
        open_circuit_voltage: float | None = 21.6,
        reference_temperature: float | None = 25,
        reference_insolation: float | None = 1000,
        module_current_at_maximum_power: float | None = 5.9,
        module_voltage_at_maximum_power: float | None = 17,
        temperature_coefficient_of_short_circuit_current: float | None = 0.02,
        temperature_coefficient_of_open_circuit_voltage: float | None = -0.079,
        nominal_operating_cell_temperature_test_ambient_temperature: float | None = 20,
        nominal_operating_cell_temperature_test_cell_temperature: float | None = 40,
        nominal_operating_cell_temperature_test_insolation: float | None = 800,
        module_heat_loss_coefficient: float | None = 30,
        total_heat_capacity: float | None = 50000,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:EquivalentOne-Diode`` and add it to the document.

        Describes the performance characteristics of Photovoltaic (PV) modules to be modeled using an equivalent one-diode circuit. This model is also known as the 4- or 5-parameter TRNSYS model for photovoltaics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformanceequivalentone-diode
        """

class HybridModelZone:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        calculate_zone_internal_thermal_mass: Literal["", "No", "Yes"] | None = "No",
        calculate_zone_air_infiltration_rate: Literal["", "No", "Yes"] | None = "No",
        calculate_zone_people_count: Literal["", "No", "Yes"] | None = "No",
        zone_measured_air_temperature_schedule_name: str | None = ...,
        zone_measured_air_humidity_ratio_schedule_name: str | None = ...,
        zone_measured_air_co2_concentration_schedule_name: str | None = ...,
        zone_input_people_activity_schedule_name: str | None = ...,
        zone_input_people_sensible_heat_fraction_schedule_name: str | None = ...,
        zone_input_people_radiant_heat_fraction_schedule_name: str | None = ...,
        zone_input_people_co2_generation_rate_schedule_name: str | None = ...,
        zone_input_supply_air_temperature_schedule_name: str | None = ...,
        zone_input_supply_air_mass_flow_rate_schedule_name: str | None = ...,
        zone_input_supply_air_humidity_ratio_schedule_name: str | None = ...,
        zone_input_supply_air_co2_concentration_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``HybridModel:Zone`` and add it to the document.

        Zones with measured air temperature data and a range of dates. If the range of temperature measurement dates includes a leap day, the weather data should include a leap day.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-hybrid-model/#hybridmodelzone
        """

class CurveQuartic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_x_3: float,
        coefficient5_x_4: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Quartic`` and add it to the document.

        Quartic (fourth order polynomial) curve with one independent variable. Input for a Quartic curve consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x + C3*x**2 + C4*x**3 + C5*x**4

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvequartic
        """
