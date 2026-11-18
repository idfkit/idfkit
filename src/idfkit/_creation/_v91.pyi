"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class SurfacePropertyConvectionCoefficientsMultipleSurface_v8_9_to_v9_4:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
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
    ) -> None:
        """Create a new ``SurfaceProperty:ConvectionCoefficients:MultipleSurface`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficientsmultiplesurface
        """

class CoilCoolingWaterToAirHeatPumpEquationFit_v8_9_to_v9_4:
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
        total_cooling_capacity_coefficient_1: float,
        total_cooling_capacity_coefficient_2: float,
        total_cooling_capacity_coefficient_3: float,
        total_cooling_capacity_coefficient_4: float,
        total_cooling_capacity_coefficient_5: float,
        sensible_cooling_capacity_coefficient_1: float,
        sensible_cooling_capacity_coefficient_2: float,
        sensible_cooling_capacity_coefficient_3: float,
        sensible_cooling_capacity_coefficient_4: float,
        sensible_cooling_capacity_coefficient_5: float,
        sensible_cooling_capacity_coefficient_6: float,
        cooling_power_consumption_coefficient_1: float,
        cooling_power_consumption_coefficient_2: float,
        cooling_power_consumption_coefficient_3: float,
        cooling_power_consumption_coefficient_4: float,
        cooling_power_consumption_coefficient_5: float,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

class HeatPumpWaterToWaterEquationFitCooling_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_cooling_capacity: float | Literal["Autosize"],
        reference_cooling_power_consumption: float | Literal["Autosize"],
        cooling_capacity_coefficient_1: float,
        cooling_capacity_coefficient_2: float,
        cooling_capacity_coefficient_3: float,
        cooling_capacity_coefficient_4: float,
        cooling_capacity_coefficient_5: float,
        cooling_compressor_power_coefficient_1: float,
        cooling_compressor_power_coefficient_2: float,
        cooling_compressor_power_coefficient_3: float,
        cooling_compressor_power_coefficient_4: float,
        cooling_compressor_power_coefficient_5: float,
        reference_coefficient_of_performance: float | None = 8,
        sizing_factor: float | None = 1,
        companion_heating_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Cooling`` and add it to the document.

        simple water-water heat pump curve-fit model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitcooling
        """
