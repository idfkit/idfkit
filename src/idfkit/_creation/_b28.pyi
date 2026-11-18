"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class SiteGroundTemperatureFCfactorMethod:
    def __call__(
        self,
        /,
        *,
        january_ground_temperature: float | None = 13,
        february_ground_temperature: float | None = 13,
        march_ground_temperature: float | None = 13,
        april_ground_temperature: float | None = 13,
        may_ground_temperature: float | None = 13,
        june_ground_temperature: float | None = 13,
        july_ground_temperature: float | None = 13,
        august_ground_temperature: float | None = 13,
        september_ground_temperature: float | None = 13,
        october_ground_temperature: float | None = 13,
        november_ground_temperature: float | None = 13,
        december_ground_temperature: float | None = 13,
    ) -> None: ...

class MaterialInfraredTransparent:
    def __call__(self, name: str, /) -> None: ...

class WindowMaterialScreenEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        screen_beam_diffuse_solar_transmittance: float,
        screen_beam_diffuse_solar_reflectance: float,
        screen_beam_beam_visible_transmittance: float,
        screen_beam_diffuse_visible_transmittance: float,
        screen_beam_diffuse_visible_reflectance: float,
        screen_beam_beam_solar_transmittance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        screen_infrared_transmittance: float | None = 0.02,
        screen_infrared_emissivity: float | None = 0.93,
        screen_wire_spacing: float | None = 0.025,
        screen_wire_diameter: float | None = 0.005,
    ) -> None: ...

class GlobalGeometryRules:
    def __call__(
        self,
        /,
        *,
        starting_vertex_position: Literal["LowerLeftCorner", "LowerRightCorner", "UpperLeftCorner", "UpperRightCorner"],
        vertex_entry_direction: Literal["Clockwise", "Counterclockwise"],
        coordinate_system: Literal["Relative", "World"],
        daylighting_reference_point_coordinate_system: Literal["", "Relative", "World"] | None = "Relative",
        rectangular_surface_coordinate_system: Literal["", "Relative", "World"] | None = "Relative",
    ) -> None: ...

class ZoneGroup:
    def __call__(self, name: str, /, *, zone_list_name: str, zone_list_multiplier: int | None = 1) -> None: ...

class AnyRoofCeilingDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[Any] = ...,
    ) -> None: ...

class FloorDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Space",
            "Surface",
            "Zone",
        ],
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[Any] = ...,
    ) -> None: ...

class AnyWindowPropertyStormWindow:
    def __call__(
        self,
        /,
        *,
        window_name: str,
        storm_glass_layer_name: str,
        month_that_storm_glass_layer_is_put_on: int,
        day_of_month_that_storm_glass_layer_is_put_on: int,
        month_that_storm_glass_layer_is_taken_off: int,
        day_of_month_that_storm_glass_layer_is_taken_off: int,
        distance_between_storm_glass_layer_and_adjacent_glass: float | None = 0.05,
    ) -> None: ...

class ShadingZoneDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        base_surface_name: str,
        transmittance_schedule_name: str | None = ...,
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[Any] = ...,
    ) -> None: ...

class SurfacePropertyConvectionCoefficientsMultipleSurface:
    def __call__(
        self,
        /,
        *,
        surface_type: Literal[
            "AllExteriorFloors",
            "AllExteriorRoofs",
            "AllExteriorSurfaces",
            "AllExteriorWalls",
            "AllExteriorWindows",
            "AllInteriorCeilings",
            "AllInteriorFloors",
            "AllInteriorSurfaces",
            "AllInteriorWalls",
            "AllInteriorWindows",
        ],
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
    ) -> None: ...

class GroundHeatTransferBasementManualGrid:
    def __call__(
        self,
        /,
        *,
        nx_number_of_cells_in_the_x_direction_20_: float,
        ny_number_of_cells_in_the_y_direction_20_: float,
        nzag_number_of_cells_in_the_z_direction_above_grade_4_always_: float,
        nzbg_number_of_cells_in_z_direction_below_grade_10_35_: float,
        ibase_x_direction_cell_indicator_of_slab_edge_5_20_: float,
        jbase_y_direction_cell_indicator_of_slab_edge_5_20_: float,
        kbase_z_direction_cell_indicator_of_the_top_of_the_floor_slab_5_20_: float,
    ) -> None: ...

class RoomAirNode:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        node_type: Literal["Ceiling", "Control", "Floor", "Inlet", "MundtRoom", "Return"],
        zone_name: str,
        height_of_nodal_control_volume_center: float,
        surface_1_name: str | None = ...,
        surface_2_name: str | None = ...,
        surface_3_name: str | None = ...,
        surface_4_name: str | None = ...,
        surface_5_name: str | None = ...,
        surface_6_name: str | None = ...,
        surface_7_name: str | None = ...,
        surface_8_name: str | None = ...,
        surface_9_name: str | None = ...,
        surface_10_name: str | None = ...,
        surface_11_name: str | None = ...,
        surface_12_name: str | None = ...,
        surface_13_name: str | None = ...,
        surface_14_name: str | None = ...,
        surface_15_name: str | None = ...,
        surface_16_name: str | None = ...,
        surface_17_name: str | None = ...,
        surface_18_name: str | None = ...,
        surface_19_name: str | None = ...,
        surface_20_name: str | None = ...,
        surface_21_name: str | None = ...,
    ) -> None: ...

class RoomAirSettingsOneNodeDisplacementVentilation:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        fraction_of_convective_internal_loads_added_to_floor_air: float | None = ...,
        fraction_of_infiltration_internal_loads_added_to_floor_air: float | None = ...,
    ) -> None: ...

class ZoneAirBalanceOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        air_balance_method: Literal["", "None", "Quadrature"] | None = "Quadrature",
        induced_outdoor_air_due_to_unbalanced_duct_leakage: float | None = 0,
        induced_outdoor_air_schedule_name: str | None = ...,
    ) -> None: ...

class AnyAirflowNetworkMultiZoneComponentDetailedOpening:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_opening_is_closed: float,
        number_of_sets_of_opening_factor_data: int,
        opening_factor_2: float,
        air_mass_flow_exponent_when_opening_is_closed: float | None = 0.65,
        type_of_rectangular_large_vertical_opening_lvo_: Literal["", "HorizontallyPivoted", "NonPivoted"]
        | None = "NonPivoted",
        extra_crack_length_or_height_of_pivoting_axis: float | None = 0,
        opening_factor_1: float | None = 0,
        discharge_coefficient_for_opening_factor_1: float | None = 0.001,
        width_factor_for_opening_factor_1: float | None = 0,
        height_factor_for_opening_factor_1: float | None = 0,
        start_height_factor_for_opening_factor_1: float | None = 0,
        discharge_coefficient_for_opening_factor_2: float | None = 1,
        width_factor_for_opening_factor_2: float | None = 1,
        height_factor_for_opening_factor_2: float | None = 1,
        start_height_factor_for_opening_factor_2: float | None = 0,
        opening_factor_3: float | None = ...,
        discharge_coefficient_for_opening_factor_3: float | None = 0,
        width_factor_for_opening_factor_3: float | None = 0,
        height_factor_for_opening_factor_3: float | None = 0,
        start_height_factor_for_opening_factor_3: float | None = 0,
        opening_factor_4: float | None = ...,
        discharge_coefficient_for_opening_factor_4: float | None = 0,
        width_factor_for_opening_factor_4: float | None = 0,
        height_factor_for_opening_factor_4: float | None = 0,
        start_height_factor_for_opening_factor_4: float | None = 0,
        type_of_rectangular_large_vertical_opening_lvo: Literal["", "HorizontallyPivoted", "NonPivoted"] | None = ...,
    ) -> None: ...

class AirflowNetworkDistributionComponentDuct:
    def __call__(
        self,
        name: str,
        /,
        *,
        duct_length: float,
        hydraulic_diameter: float,
        cross_section_area: float,
        surface_roughness: float | None = 0.0009,
        coefficient_for_local_dynamic_loss_due_to_fitting: float | None = 0,
        heat_transmittance_coefficient_u_factor_for_duct_wall_construction: float | None = 0.943,
        overall_moisture_transmittance_coefficient_from_air_to_air: float | None = 0.001,
        outside_convection_coefficient: float | None = ...,
        inside_convection_coefficient: float | None = ...,
    ) -> None: ...

class AirflowNetworkDistributionComponentTerminalUnit:
    def __call__(
        self,
        /,
        *,
        terminal_unit_name: str,
        terminal_unit_object_type: Literal[
            "AirTerminal:SingleDuct:ConstantVolume:Reheat", "AirTerminal:SingleDuct:VAV:Reheat"
        ],
        air_path_length: float,
        air_path_hydraulic_diameter: float,
    ) -> None: ...

class HVACTemplateZoneVAVHeatAndCool:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_vav_system_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        constant_minimum_air_flow_fraction: float | None = 0.2,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        design_specification_outdoor_air_object_name_for_sizing: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        reheat_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "None",
        reheat_coil_availability_schedule_name: str | None = ...,
        maximum_reheat_air_temperature: float | None = ...,
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
    ) -> None: ...

class AnyHVACTemplateSystemUnitarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        control_type: Literal["", "Load", "SetPoint"] | None = "Load",
        control_zone_or_thermostat_location_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal[
            "",
            "ChilledWater",
            "ChilledWaterDetailedFlatModel",
            "HeatExchangerAssistedChilledWater",
            "HeatExchangerAssistedDX",
            "MultiSpeedDX",
            "None",
            "SingleSpeedDX",
            "SingleSpeedDXWaterCooled",
            "TwoSpeedDX",
            "TwoStageDX",
            "TwoStageHumidityControlDX",
        ]
        | None = "SingleSpeedDX",
        number_of_speeds_for_cooling: int | None = 1,
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_design_supply_air_temperature: float | None = 12.8,
        dx_cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal[
            "",
            "Electric",
            "Gas",
            "HotWater",
            "MultiSpeedDXHeatPumpAirSource",
            "MultiStageElectric",
            "MultiStageGas",
            "None",
            "SingleSpeedDXHeatPumpAirSource",
            "SingleSpeedDXHeatPumpWaterSource",
        ]
        | None = "Gas",
        number_of_speeds_or_stages_for_heating: int | None = 1,
        heating_coil_availability_schedule_name: str | None = ...,
        heating_design_supply_air_temperature: float | None = 50,
        heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_or_reheat_coil_type: Literal["", "DesuperHeater", "Electric", "Gas", "HotWater", "None"]
        | None = "None",
        supplemental_heating_or_reheat_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_or_reheat_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        supplemental_heating_or_reheat_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_or_reheat_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_or_reheat_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
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
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["", "Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "", "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        dehumidification_relative_humidity_setpoint: float | None = 60,
        dehumidification_relative_humidity_setpoint_schedule_name: str | None = ...,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_relative_humidity_setpoint: float | None = 30,
        humidifier_relative_humidity_setpoint_schedule_name: str | None = ...,
        sizing_option: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 300,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
    ) -> None: ...

class SizingSystem:
    def __call__(
        self,
        /,
        *,
        airloop_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        central_cooling_design_supply_air_temperature: float,
        central_heating_design_supply_air_temperature: float,
        type_of_load_to_size_on: Literal["", "Latent", "Sensible", "Total", "VentilationRequirement"]
        | None = "Sensible",
        design_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        central_heating_maximum_system_air_flow_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        type_of_zone_sum_to_use: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        central_cooling_design_supply_air_humidity_ratio: float | None = 0.008,
        central_heating_design_supply_air_humidity_ratio: float | None = 0.008,
        cooling_supply_air_flow_rate_method: Literal[
            "",
            "DesignDay",
            "Flow/System",
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
        ]
        | None = "DesignDay",
        cooling_supply_air_flow_rate: float | None = 0,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "",
            "DesignDay",
            "Flow/System",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedCoolingAirflow",
            "FractionOfAutosizedHeatingAirflow",
        ]
        | None = "DesignDay",
        heating_supply_air_flow_rate: float | None = 0,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        heating_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_heating_capacity: float | None = ...,
        system_outdoor_air_method: Literal[
            "", "Standard62.1SimplifiedProcedure", "Standard62.1VentilationRateProcedure", "ZoneSum"
        ]
        | None = "ZoneSum",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity", "None"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = ...,
        central_cooling_capacity_control_method: Literal["", "Bypass", "OnOff", "VAV", "VT"] | None = "OnOff",
        occupant_diversity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_coil_sizing_method: Literal[
            "", "CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity", "None"
        ]
        | None = "None",
        maximum_heating_capacity_to_cooling_capacity_sizing_ratio: float | None = 1,
    ) -> None: ...

class ZoneHVACFourPipeFanCoil:
    def __call__(
        self,
        name: str,
        /,
        *,
        capacity_control_method: Literal[
            "ASHRAE90VariableFan",
            "ConstantFanVariableFlow",
            "CyclingFan",
            "MultiSpeedFan",
            "VariableFanConstantFlow",
            "VariableFanVariableFlow",
        ],
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"],
        supply_air_fan_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        maximum_cold_water_flow_rate: float | Literal["Autosize"],
        heating_coil_object_type: Literal["Coil:Heating:Electric", "Coil:Heating:Water"],
        heating_coil_name: str,
        maximum_hot_water_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        low_speed_supply_air_flow_ratio: float | None = 0.33,
        medium_speed_supply_air_flow_ratio: float | None = 0.66,
        outdoor_air_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        minimum_cold_water_flow_rate: float | None = 0,
        cooling_convergence_tolerance: float | None = 0.001,
        minimum_hot_water_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None: ...

class AnyZoneHVACPackagedTerminalAirConditioner:
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
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None: ...

class AnyAirTerminalDualDuctVAV:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        hot_air_inlet_node_name: str,
        cold_air_inlet_node_name: str,
        maximum_damper_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_fraction: float | None = 0.2,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None: ...

class CoilSystemCoolingWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["", "No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["", "No", "Yes"] | None = "No",
        minimum_air_to_water_temperature_offset: float | None = 0,
        economizer_lockout: Literal["", "No", "Yes"] | None = "Yes",
        minimum_water_loop_temperature_for_heat_recovery: float | None = 0,
        companion_coil_used_for_heat_recovery: str | None = ...,
    ) -> None: ...

class AnyCoilCoolingDXCurveFitOperatingMode:
    def __call__(
        self,
        name: str,
        /,
        *,
        speed_1_name: str,
        rated_gross_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_evaporator_air_flow_rate: float | Literal["Autosize"] | None = ...,
        rated_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        nominal_evaporative_condenser_pump_power: float | Literal["", "Autosize"] | None = 0,
        nominal_speed_number: int | None = ...,
        speed_2_name: str | None = ...,
        speed_3_name: str | None = ...,
        speed_4_name: str | None = ...,
        speed_5_name: str | None = ...,
        speed_6_name: str | None = ...,
        speed_7_name: str | None = ...,
        speed_8_name: str | None = ...,
        speed_9_name: str | None = ...,
        speed_10_name: str | None = ...,
    ) -> None: ...

class CoilCoolingDXCurveFitOperatingMode:
    def __call__(
        self,
        name: str,
        /,
        *,
        speed_1_name: str,
        rated_gross_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_evaporator_air_flow_rate: float | Literal["Autosize"] | None = ...,
        rated_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        nominal_evaporative_condenser_pump_power: float | Literal["", "Autosize"] | None = 0,
        nominal_speed_number: int | None = ...,
        speed_2_name: str | None = ...,
        speed_3_name: str | None = ...,
        speed_4_name: str | None = ...,
        speed_5_name: str | None = ...,
        speed_6_name: str | None = ...,
        speed_7_name: str | None = ...,
        speed_8_name: str | None = ...,
        speed_9_name: str | None = ...,
        speed_10_name: str | None = ...,
    ) -> None: ...

class AnyCoilCoolingDXMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal["Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"],
        number_of_speeds: int,
        speed_1_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_2_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        speed_1_gross_rated_cooling_cop: float | None = 3,
        speed_1_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_1_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_1_maximum_cycling_rate: float | None = 0,
        speed_1_latent_capacity_time_constant: float | None = 0,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_1_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_1_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_2_gross_rated_cooling_cop: float | None = 3,
        speed_2_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_2_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_2_maximum_cycling_rate: float | None = 0,
        speed_2_latent_capacity_time_constant: float | None = 0,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_2_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_cooling_cop: float | None = 3,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_3_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_3_maximum_cycling_rate: float | None = 0,
        speed_3_latent_capacity_time_constant: float | None = 0,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_3_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_cooling_cop: float | None = 3,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_4_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_4_maximum_cycling_rate: float | None = 0,
        speed_4_latent_capacity_time_constant: float | None = 0,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_4_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None: ...

class AnyCoilHeatingGasMultiStage:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_gas_burner_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        stage_2_gas_burner_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_gas_burner_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_gas_burner_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
    ) -> None: ...

class AirLoopHVACDedicatedOutdoorAirSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_mixer_name: str,
        airloophvac_splitter_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        number_of_airloophvac: int,
        airloophvac_outdoorairsystem_name: str | None = ...,
        availability_schedule_name: str | None = ...,
        airloophvacs: list[Any] = ...,
    ) -> None: ...

class ConnectorMixer:
    def __call__(self, name: str, /, *, outlet_branch_name: str, branches: list[Any] = ...) -> None: ...

class SolarCollectorIntegralCollectorStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        integralcollectorstorageparameters_name: str,
        surface_name: str,
        inlet_node_name: str,
        outlet_node_name: str,
        bottom_surface_boundary_conditions_type: Literal["", "AmbientAir", "OtherSideConditionsModel"]
        | None = "AmbientAir",
        boundary_condition_model_name: str | None = ...,
        maximum_flow_rate: float | None = ...,
    ) -> None: ...

class AnyHeatPumpAirToWaterFuelFiredCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        normalized_capacity_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_plr_curve_name: str,
        air_source_node_name: str | None = ...,
        companion_heating_heat_pump_name: str | None = ...,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "NaturalGas",
        end_use_subcategory: str | None = "General",
        nominal_cooling_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 7,
        design_temperature_lift: float | Literal["", "Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["", "DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["", "EnteringEvaporator", "LeavingEvaporator"]
        | None = "EnteringEvaporator",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
    ) -> None: ...

class HeatPumpAirToWaterFuelFiredCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        normalized_capacity_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_plr_curve_name: str,
        air_source_node_name: str | None = ...,
        companion_heating_heat_pump_name: str | None = ...,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "NaturalGas",
        end_use_subcategory: str | None = "General",
        nominal_cooling_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 7,
        design_temperature_lift: float | Literal["", "Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["", "DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["", "EnteringEvaporator", "LeavingEvaporator"]
        | None = "EnteringEvaporator",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
        minimum_unloading_ratio: float | None = 0.25,
    ) -> None: ...

class HeatPumpWaterToWaterParameterEstimationCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        nominal_cop: float | None = ...,
        nominal_capacity: float | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        load_side_flow_rate: float | None = ...,
        source_side_flow_rate: float | None = ...,
        load_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        piston_displacement: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        compressor_suction_and_discharge_pressure_drop: float | None = ...,
        superheating: float | None = ...,
        constant_part_of_electromechanical_power_losses: float | None = ...,
        loss_factor: float | None = ...,
        high_pressure_cut_off: float | None = 500000000,
        low_pressure_cut_off: float | None = 0,
    ) -> None: ...

class AnyWaterHeaterSizing:
    def __call__(
        self,
        /,
        *,
        waterheater_name: str,
        design_mode: Literal[
            "PeakDraw", "PerFloorArea", "PerPerson", "PerSolarCollectorArea", "PerUnit", "ResidentialHUD-FHAMinimum"
        ]
        | None = ...,
        time_storage_can_meet_peak_draw: float | None = ...,
        time_for_tank_recovery: float | None = ...,
        nominal_tank_volume_for_autosizing_plant_connections: float | None = ...,
        number_of_bedrooms: int | None = ...,
        number_of_bathrooms: int | None = ...,
        storage_capacity_per_person: float | None = ...,
        recovery_capacity_per_person: float | None = ...,
        storage_capacity_per_floor_area: float | None = ...,
        recovery_capacity_per_floor_area: float | None = ...,
        number_of_units: float | None = ...,
        storage_capacity_per_unit: float | None = ...,
        recovery_capacity_perunit: float | None = ...,
        storage_capacity_per_collector_area: float | None = ...,
        height_aspect_ratio: float | None = ...,
    ) -> None: ...

class SetpointManagerSingleZoneHumidityMaximum:
    def __call__(
        self, name: str, /, *, setpoint_node_or_nodelist_name: str, control_zone_air_node_name: str
    ) -> None: ...

class AnyGeneratorMicroTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_electrical_power_output: float,
        reference_electrical_efficiency_using_lower_heating_value: float,
        electrical_power_function_of_temperature_and_elevation_curve_name: str,
        electrical_efficiency_function_of_temperature_curve_name: str,
        electrical_efficiency_function_of_part_load_ratio_curve_name: str,
        minimum_full_load_electrical_power_output: float | None = 0,
        maximum_full_load_electrical_power_output: float | None = ...,
        reference_combustion_air_inlet_temperature: float | None = 15,
        reference_combustion_air_inlet_humidity_ratio: float | None = 0.00638,
        reference_elevation: float | None = 0,
        fuel_type: Literal["", "NaturalGas"] | None = "NaturalGas",
        fuel_higher_heating_value: float | None = 50000,
        fuel_lower_heating_value: float | None = 45450,
        standby_power: float | None = 0,
        ancillary_power: float | None = 0,
        ancillary_power_function_of_fuel_input_curve_name: str | None = ...,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        reference_thermal_efficiency_using_lower_heat_value: float | None = 0,
        reference_inlet_water_temperature: float | None = ...,
        heat_recovery_water_flow_operating_mode: Literal["", "InternalControl", "PlantControl"] | None = "PlantControl",
        reference_heat_recovery_water_flow_rate: float | None = ...,
        heat_recovery_water_flow_rate_function_of_temperature_and_power_curve_name: str | None = ...,
        thermal_efficiency_function_of_temperature_and_elevation_curve_name: str | None = ...,
        heat_recovery_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        heat_recovery_rate_function_of_inlet_water_temperature_curve_name: str | None = ...,
        heat_recovery_rate_function_of_water_flow_rate_curve_name: str | None = ...,
        minimum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_temperature: float | None = ...,
        combustion_air_inlet_node_name: str | None = ...,
        combustion_air_outlet_node_name: str | None = ...,
        reference_exhaust_air_mass_flow_rate: float | None = ...,
        exhaust_air_flow_rate_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_flow_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        nominal_exhaust_air_outlet_temperature: float | None = ...,
        exhaust_air_temperature_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_temperature_function_of_part_load_ratio_curve_name: str | None = ...,
    ) -> None: ...

class ElectricLoadCenterInverterPVWatts:
    def __call__(
        self, name: str = "", /, *, dc_to_ac_size_ratio: float | None = 1.1, inverter_efficiency: float | None = 0.96
    ) -> None: ...

class AnyTableIndependentVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        interpolation_method: Literal["", "Cubic", "Linear"] | None = "Linear",
        extrapolation_method: Literal["", "Constant", "Linear"] | None = "Constant",
        minimum_value: float | None = ...,
        maximum_value: float | None = ...,
        normalization_reference_value: float | None = ...,
        unit_type: Literal[
            "", "Angle", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: list[Any] = ...,
    ) -> None: ...

class ParametricFileNameSuffix:
    def __call__(self, name: str = "", /, *, suffixes: list[Any] = ...) -> None: ...

class OutputSurfacesDrawing:
    def __call__(
        self,
        /,
        *,
        report_type: Literal["DXF", "DXF:WireFrame", "VRML"],
        report_specifications_1: Literal["", "RegularPolyline", "ThickPolyline", "Triangulate3DFace"]
        | None = "Triangulate3DFace",
        report_specifications_2: str | None = ...,
    ) -> None: ...

class OutputEnergyManagementSystem:
    def __call__(
        self,
        /,
        *,
        actuator_availability_dictionary_reporting: Literal["", "None", "NotByUniqueKeyNames", "Verbose"]
        | None = "None",
        internal_variable_availability_dictionary_reporting: Literal["", "None", "NotByUniqueKeyNames", "Verbose"]
        | None = "None",
        ems_runtime_language_debug_output_level: Literal["", "ErrorsOnly", "None", "Verbose"] | None = "None",
    ) -> None: ...

class OutputTableReportPeriod:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        begin_hour_of_day: int,
        end_month: int,
        end_day_of_month: int,
        end_hour_of_day: int,
        report_name: Literal[
            "AllResilienceSummaries", "CO2ResilienceSummary", "ThermalResilienceSummary", "VisualResilienceSummary"
        ]
        | None = ...,
        begin_year: int | None = ...,
        end_year: int | None = ...,
    ) -> None: ...

class OutputMeter:
    def __call__(
        self,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
    ) -> None: ...
