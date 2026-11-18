"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class BuildingSurfaceDetailed_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Ceiling", "Floor", "Roof", "Wall"],
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
            "Surface",
            "Zone",
        ],
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.BuildingSurfaceDetailedVerticesItem | _g.BuildingSurfaceDetailedVerticesGroup] = ...,
    ) -> None:
        """Create a new ``BuildingSurface:Detailed`` and add it to the document.

        Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#buildingsurfacedetailed
        """

class SolarCollectorPerformanceIntegralCollectorStorage_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        ics_collector_type: Literal["", "RectangularTank"] | None = "RectangularTank",
        gross_area: float | None = ...,
        collector_water_volume: float | None = ...,
        bottom_heat_loss_conductance: float | None = 0.4,
        side_heat_loss_conductance: float | None = 0.6,
        aspect_ratio: float | None = 0.8,
        collector_side_height: float | None = 0.2,
        thermal_mass_of_absorber_plate: float | None = 0,
        number_of_covers: float | None = 2,
        cover_spacing: float | None = 0.05,
        refractive_index_of_outer_cover: float | None = 1.526,
        extinction_coefficient_times_thickness_of_outer_cover: float | None = 0.045,
        emissivity_of_outer_cover: float | None = 0.88,
        refractive_index_of_inner_cover: float | None = 1.37,
        extinction_coefficient_times_thickness_of_the_inner_cover: float | None = 0.008,
        emissivity_of_inner_cover: float | None = 0.88,
        absorptance_of_absorber_plate: float | None = 0.96,
        emissivity_of_absorber_plate: float | None = 0.3,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:IntegralCollectorStorage`` and add it to the document.

        Thermal and optical performance parameters for a single glazed solar collector with integral storage unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-solar-collectors/#solarcollectorperformanceintegralcollectorstorage
        """

class HeatPumpPlantLoopEIRCooling_v23_2_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        condenser_type: Literal["", "AirSource", "WaterSource"] | None = "WaterSource",
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 3,
        sizing_factor: float | None = 1,
        control_type: Literal["", "Load", "Setpoint"] | None = "Load",
        flow_mode: Literal["", "ConstantFlow", "VariableSpeedPumping"] | None = "ConstantFlow",
        minimum_part_load_ratio: float | None = 0,
        minimum_source_inlet_temperature: float | None = -100,
        maximum_source_inlet_temperature: float | None = 100,
        minimum_supply_water_temperature_curve_name: float | None = ...,
        maximum_supply_water_temperature_curve_name: float | None = ...,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Cooling`` and add it to the document.

        An EIR formulated water to water heat pump model, cooling operation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-plant-equipment/#heatpumpplantloopeircooling
        """
