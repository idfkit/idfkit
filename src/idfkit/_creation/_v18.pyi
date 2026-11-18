"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class CoilCoolingDXSingleSpeed_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_cooling_cop: float | None = 3,
        rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        report_ashrae_standard_127_performance_ratings: Literal["No", "Yes"] | None = "No",
        zone_name_for_condenser_placement: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxsinglespeed
        """

class Window_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        shading_control_name: str | None = ...,
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Window`` and add it to the document.

        Allows for simplified entry of Windows.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-thermal-zone-description-geometry/#window
        """

class GroundHeatExchangerResponseFactors_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes: float,
        g_function_reference_ratio: float | None = 0.0005,
        g_functions: Sequence[
            _g.GroundHeatExchangerResponseFactorsGFunctionsItem | _g.GroundHeatExchangerResponseFactorsGFunctionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:ResponseFactors`` and add it to the document.

        Response factor definitions from third-party tool, commonly referred to a 'g-functions'

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#groundheatexchangerresponsefactors
        """

class WindowMaterialComplexShade_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        layer_type: Literal["BSDF", "OtherShadingType", "Perforated", "Venetian", "Woven"] | None = "OtherShadingType",
        thickness: float | None = 0.002,
        conductivity: float | None = 1,
        ir_transmittance: float | None = 0,
        front_emissivity: float | None = 0.84,
        back_emissivity: float | None = 0.84,
        top_opening_multiplier: float | None = 0,
        bottom_opening_multiplier: float | None = 0,
        left_side_opening_multiplier: float | None = 0,
        right_side_opening_multiplier: float | None = 0,
        front_opening_multiplier: float | None = 0.05,
        slat_width: float | None = 0.016,
        slat_spacing: float | None = 0.012,
        slat_thickness: float | None = 0.0006,
        slat_angle: float | None = 90,
        slat_conductivity: float | None = 160,
        slat_curve: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:ComplexShade`` and add it to the document.

        Complex window shading layer thermal properties

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-surface-construction-elements/#windowmaterialcomplexshade
        """

class PipingSystemUndergroundDomain_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        xmax: float,
        ymax: float,
        zmax: float,
        x_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        y_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        z_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        number_of_pipe_circuits_entered_for_this_domain: float,
        x_direction_mesh_density_parameter: float | None = 4,
        x_direction_geometric_coefficient: float | None = 1.3,
        y_direction_mesh_density_parameter: float | None = 4,
        y_direction_geometric_coefficient: float | None = 1.3,
        z_direction_mesh_density_parameter: float | None = 4,
        z_direction_geometric_coefficient: float | None = 1.3,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        this_domain_includes_basement_surface_interaction: Literal["No", "Yes"] | None = "No",
        width_of_basement_floor_in_ground_domain: float | None = ...,
        depth_of_basement_wall_in_ground_domain: float | None = ...,
        shift_pipe_x_coordinates_by_basement_width: Literal["No", "Yes"] | None = ...,
        name_of_basement_wall_boundary_condition_model: str | None = ...,
        name_of_basement_floor_boundary_condition_model: str | None = ...,
        convergence_criterion_for_the_outer_cartesian_domain_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_outer_cartesian_domain_iteration_loop: float | None = 500,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        pipe_circuits: Sequence[
            _g.PipingSystemUndergroundDomainPipeCircuitsItem | _g.PipingSystemUndergroundDomainPipeCircuitsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PipingSystem:Underground:Domain`` and add it to the document.

        The ground domain object for underground piping system simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-node-branch-management/#pipingsystemundergrounddomain
        """

class SizingPlant_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        plant_or_condenser_loop_name: str,
        loop_type: Literal["Condenser", "Cooling", "Heating", "Steam"],
        design_loop_exit_temperature: float,
        loop_design_temperature_difference: float,
        sizing_option: Literal["Coincident", "NonCoincident"] | None = "NonCoincident",
        zone_timesteps_in_averaging_window: float | None = 1,
        coincident_sizing_factor_mode: Literal[
            "GlobalCoolingSizingFactor", "GlobalHeatingSizingFactor", "LoopComponentSizingFactor", "None"
        ]
        | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Sizing:Plant`` and add it to the document.

        Specifies the input needed to autosize plant loop flow rates and equipment capacities. This information is initially used by components that use water for heating or cooling such as hot or chilled water coils to calculate their maximum water flow rates. These flow rates are then summed for use in calculating the Plant Loop flow rates.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-design-objects/#sizingplant
        """
