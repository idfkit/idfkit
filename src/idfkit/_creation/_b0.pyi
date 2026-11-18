"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class HeatBalanceAlgorithm:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal[
            "",
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
        surface_temperature_upper_limit: float | None = 200,
        minimum_surface_convection_heat_transfer_coefficient_value: float | None = 0.1,
        maximum_surface_convection_heat_transfer_coefficient_value: float | None = 1000,
    ) -> None: ...

class AnyZoneAirHeatBalanceAlgorithm:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal["", "AnalyticalSolution", "EulerMethod", "ThirdOrderBackwardDifference"]
        | None = "ThirdOrderBackwardDifference",
    ) -> None: ...

class AnyConstructionComplexFenestrationState:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        window_thermal_model: str,
        basis_matrix_name: str,
        solar_optical_complex_front_transmittance_matrix_name: str,
        solar_optical_complex_back_reflectance_matrix_name: str,
        visible_optical_complex_front_transmittance_matrix_name: str,
        visible_optical_complex_back_transmittance_matrix_name: str,
        outside_layer_name: str,
        basis_type: Literal["", "LBNLWINDOW", "UserDefined"] | None = "LBNLWINDOW",
        basis_symmetry_type: Literal["", "Axisymmetric", "None"] | None = "None",
        gap_1_name: str | None = ...,
        layer_2_name: str | None = ...,
        gap_2_name: str | None = ...,
        gap_3_name: str | None = ...,
        layer_4_name: str | None = ...,
        gap_4_name: str | None = ...,
        layer_5_name: str | None = ...,
    ) -> None: ...

class FloorAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class SurfacePropertyHeatTransferAlgorithmSurfaceList:
    def __call__(
        self,
        name: str,
        /,
        *,
        algorithm: Literal[
            "",
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
        surface: list[_g.SurfacePropertyHeatTransferAlgorithmSurfaceListSurfaceItem] = ...,
    ) -> None: ...

class SurfacePropertyOtherSideCoefficients:
    def __call__(
        self,
        name: str,
        /,
        *,
        combined_convective_radiative_film_coefficient: float,
        constant_temperature: float | None = 0,
        constant_temperature_coefficient: float | None = 1,
        external_dry_bulb_temperature_coefficient: float | None = 0,
        ground_temperature_coefficient: float | None = 0,
        wind_speed_coefficient: float | None = 0,
        zone_air_temperature_coefficient: float | None = 0,
        constant_temperature_schedule_name: str | None = ...,
        sinusoidal_variation_of_constant_temperature_coefficient: Literal["", "No", "Yes"] | None = "No",
        period_of_sinusoidal_variation: float | None = 24,
        previous_other_side_temperature_coefficient: float | None = 0,
        minimum_other_side_temperature_limit: float | None = ...,
        maximum_other_side_temperature_limit: float | None = ...,
    ) -> None: ...

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
    ) -> None: ...

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
    ) -> None: ...

class GroundHeatTransferBasementSimParameters:
    def __call__(
        self,
        /,
        *,
        f_multiplier_for_the_adi_solution: float | None = ...,
        iyrs_maximum_number_of_yearly_iterations_: float | None = 15,
        iyrs_maximum_number_of_yearly_iterations: float | None = ...,
    ) -> None: ...

class GroundHeatTransferBasementComBldg:
    def __call__(
        self,
        /,
        *,
        january_average_temperature: float | None = 22,
        february_average_temperature: float | None = 22,
        march_average_temperature: float | None = 22,
        april_average_temperature: float | None = 22,
        may_average_temperature: float | None = 22,
        june_average_temperature: float | None = 22,
        july_average_temperature: float | None = 22,
        august_average_temperature: float | None = 22,
        september_average_temperature: float | None = 22,
        october_average_temperature: float | None = 22,
        november_average_temperature: float | None = 22,
        december_average_temperature: float | None = 22,
        daily_variation_sine_wave_amplitude: float | None = 0,
    ) -> None: ...

class RoomAirTemperaturePatternConstantGradient:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_constant_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        temperature_gradient: float | None = ...,
    ) -> None: ...

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
        surface_deltas: list[_g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasItem] = ...,
    ) -> None: ...

class OtherEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
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
        carbon_dioxide_generation_rate: float | None = 0,
    ) -> None: ...

class AnyAirflowNetworkDistributionComponentReliefAirFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None: ...

class AirflowNetworkDistributionComponentReliefAirFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_mixer_name: str,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None: ...

class HVACTemplateZoneVAVFanPowered:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_vav_system_name: str,
        template_thermostat_name: str | None = ...,
        primary_supply_air_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        primary_supply_air_minimum_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        secondary_supply_air_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        flow_type: Literal["", "Parallel", "ParallelFromPlenum", "Series", "SeriesFromPlenum"] | None = "Parallel",
        parallel_fan_on_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        reheat_coil_type: Literal["", "Electric", "Gas", "HotWater"] | None = "Electric",
        reheat_coil_availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.7,
        fan_delta_pressure: float | None = 1000,
        fan_motor_efficiency: float | None = 0.9,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 12.8,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        zone_piu_fan_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
    ) -> None: ...

class ThermostatSetpointThermalComfortFangerSingleCooling:
    def __call__(self, name: str, /, *, fanger_thermal_comfort_schedule_name: str) -> None: ...

class AnyZoneHVACLowTemperatureRadiantVariableFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_hot_water_flow: float | Literal["Autosize"] | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        maximum_cold_water_flow: float | Literal["Autosize"] | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None: ...

class AirTerminalSingleDuctVAVReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        damper_heating_action: Literal["", "Normal", "Reverse", "ReverseWithLimits"] | None = "ReverseWithLimits",
        maximum_flow_per_zone_floor_area_during_reheat: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_flow_fraction_during_reheat: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_reheat_air_temperature: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None: ...

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
    ) -> None: ...

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
    ) -> None: ...

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
    ) -> None: ...

class AnyHeaderedPumpsConstantSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None: ...

class HeaderedPumpsConstantSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

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
    ) -> None: ...

class AnyChillerCombustionTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        coefficient_1_of_fuel_input_curve: float | None = ...,
        coefficient_2_of_fuel_input_curve: float | None = ...,
        coefficient_3_of_fuel_input_curve: float | None = ...,
        coefficient_1_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_2_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_3_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_1_of_exhaust_flow_curve: float | None = ...,
        coefficient_2_of_exhaust_flow_curve: float | None = ...,
        coefficient_3_of_exhaust_flow_curve: float | None = ...,
        coefficient_1_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_2_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_3_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        gas_turbine_engine_capacity: float | Literal["Autosize"] | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_steam_saturation_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        fuel_type: Literal["", "Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"] | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        turbine_engine_efficiency: float | None = 0.35,
    ) -> None: ...

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
    ) -> None: ...

class PlantEquipmentOperationOutdoorDewpointDifference:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature_node_name: str,
        dewpoint_temperature_difference_range_1_lower_limit: float,
        dewpoint_temperature_difference_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        dewpoint_temperature_difference_range_2_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_3_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_4_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_5_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_6_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_7_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_8_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_9_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_10_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None: ...

class EnergyManagementSystemTrendVariable:
    def __call__(self, name: str, /, *, ems_variable_name: str, number_of_timesteps_to_be_logged: int) -> None: ...

class AvailabilityManagerOptimumStart:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_type: Literal["", "ControlZone", "MaximumofZoneList", "StayOff"] | None = "ControlZone",
        control_zone_name: str | None = ...,
        zone_list_name: str | None = ...,
        maximum_value_for_optimum_start_time: float | None = 6,
        control_algorithm: Literal[
            "", "AdaptiveASHRAE", "AdaptiveTemperatureGradient", "ConstantStartTime", "ConstantTemperatureGradient"
        ]
        | None = "AdaptiveASHRAE",
        constant_temperature_gradient_during_cooling: float | None = ...,
        constant_temperature_gradient_during_heating: float | None = ...,
        initial_temperature_gradient_during_cooling: float | None = ...,
        initial_temperature_gradient_during_heating: float | None = ...,
        constant_start_time: float | None = ...,
        number_of_previous_days: int | None = 2,
    ) -> None: ...

class AvailabilityManagerLowTemperatureTurnOn:
    def __call__(self, name: str, /, *, sensor_node_name: str, temperature: float) -> None: ...

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
    ) -> None: ...

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
    ) -> None: ...

class SetpointManagerCondenserEnteringReset:
    def __call__(
        self,
        name: str,
        /,
        *,
        default_condenser_entering_water_temperature_schedule_name: str,
        minimum_design_wetbulb_temperature_curve_name: str,
        minimum_outside_air_wetbulb_temperature_curve_name: str,
        optimized_cond_entering_water_temperature_curve_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        minimum_lift: float | None = 11.1,
        maximum_condenser_entering_water_temperature: float | None = 32,
        cooling_tower_design_inlet_air_wet_bulb_temperature: float | None = 25.56,
    ) -> None: ...

class RefrigerationTransferLoadList:
    def __call__(
        self, name: str, /, *, transfer_loads: list[_g.RefrigerationTransferLoadListTransferLoadsItem] = ...
    ) -> None: ...

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
    ) -> None: ...

class DemandManagerElectricEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        equipment: list[_g.DemandManagerElectricEquipmentEquipmentItem] = ...,
    ) -> None: ...

class AnyDemandManagerVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["FixedRate", "Off", "ReductionRatio"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        fixed_rate: float | None = ...,
        reduction_ratio: float | None = ...,
        limit_step_change: float | None = ...,
        selection_control: Literal["", "All", "RotateMany", "RotateOne"] | None = "All",
        rotation_duration: int | None = ...,
        controllers: list[_g.DemandManagerVentilationControllersItem] = ...,
    ) -> None: ...

class GeneratorPhotovoltaic:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        photovoltaic_performance_object_type: Literal[
            "PhotovoltaicPerformance:EquivalentOne-Diode",
            "PhotovoltaicPerformance:Sandia",
            "PhotovoltaicPerformance:Simple",
        ]
        | None = ...,
        module_performance_name: str | None = ...,
        heat_transfer_integration_mode: Literal[
            "",
            "Decoupled",
            "DecoupledUllebergDynamic",
            "IntegratedExteriorVentedCavity",
            "IntegratedSurfaceOutsideFace",
            "IntegratedTranspiredCollector",
            "PhotovoltaicThermalSolarCollector",
        ]
        | None = "Decoupled",
        number_of_series_strings_in_parallel: float | None = 1,
        number_of_modules_in_series: float | None = 1,
    ) -> None: ...

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
    ) -> None: ...

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
    ) -> None: ...

class CurveQuadratic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
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
    ) -> None: ...

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
    ) -> None: ...

class TableLookup:
    def __call__(
        self,
        name: str,
        /,
        *,
        independent_variable_list_name: str,
        normalization_method: Literal["", "AutomaticWithDivisor", "DivisorOnly", "None"] | None = "None",
        normalization_divisor: float | None = 1,
        minimum_output: float | None = ...,
        maximum_output: float | None = ...,
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: list[_g.TableLookupValuesItem] = ...,
    ) -> None: ...
