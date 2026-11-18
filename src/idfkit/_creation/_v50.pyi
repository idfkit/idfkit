"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class SiteGroundDomainBasement_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        basement_floor_boundary_condition_model_name: str,
        basement_wall_boundary_condition_model_name: str,
        ground_domain_depth: float | None = 10,
        aspect_ratio: float | None = 1,
        perimeter_offset: float | None = 5,
        soil_thermal_conductivity: float | None = 1.5,
        soil_density: float | None = 2800,
        soil_specific_heat: float | None = 850,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        horizontal_insulation: Literal["", "No", "Yes"] | None = "No",
        horizontal_insulation_material_name: str | None = ...,
        horizontal_insulation_extents: Literal["", "Full", "Perimeter"] | None = "Full",
        perimeter_horizontal_insulation_width: float | None = ...,
        basement_wall_depth: float | None = ...,
        vertical_insulation: Literal["", "No", "Yes"] | None = "No",
        basement_wall_vertical_insulation_material_name: str | None = ...,
        vertical_insulation_depth: float | None = ...,
        simulation_timestep: Literal["", "Hourly", "Timestep"] | None = "Hourly",
        mesh_density_parameter: float | None = 4,
    ) -> None:
        """Create a new ``Site:GroundDomain:Basement`` and add it to the document.

        Ground-coupled basement model for simulating basements or other underground zones.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-location-climate-weather-file-access/#sitegrounddomainbasement
        """

class MaterialPropertyHeatAndMoistureTransferDiffusion_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        material_name: str,
        number_of_data_pairs: float,
        relative_humidity_fraction_1: float,
        water_vapor_diffusion_resistance_factor_1: float,
        relative_humidity_fraction_2: float | None = ...,
        water_vapor_diffusion_resistance_factor_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        water_vapor_diffusion_resistance_factor_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        water_vapor_diffusion_resistance_factor_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        water_vapor_diffusion_resistance_factor_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        water_vapor_diffusion_resistance_factor_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        water_vapor_diffusion_resistance_factor_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        water_vapor_diffusion_resistance_factor_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        water_vapor_diffusion_resistance_factor_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        water_vapor_diffusion_resistance_factor_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        water_vapor_diffusion_resistance_factor_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        water_vapor_diffusion_resistance_factor_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        water_vapor_diffusion_resistance_factor_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        water_vapor_diffusion_resistance_factor_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        water_vapor_diffusion_resistance_factor_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        water_vapor_diffusion_resistance_factor_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        water_vapor_diffusion_resistance_factor_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        water_vapor_diffusion_resistance_factor_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        water_vapor_diffusion_resistance_factor_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        water_vapor_diffusion_resistance_factor_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        water_vapor_diffusion_resistance_factor_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        water_vapor_diffusion_resistance_factor_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        water_vapor_diffusion_resistance_factor_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        water_vapor_diffusion_resistance_factor_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        water_vapor_diffusion_resistance_factor_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Diffusion`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between water vapor diffusion and relative humidity fraction Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferdiffusion
        """

class GeneratorMicroTurbine_v9_3_to_v9_4:
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
        fuel_type: Literal["", "NaturalGas", "Propane"] | None = "NaturalGas",
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
    ) -> None:
        """Create a new ``Generator:MicroTurbine`` and add it to the document.

        MicroTurbine generators are small combustion turbines (e.g., 25kW to 500kW). The model calculates electrical power output, fuel use, standby and ancillary power. Energy recovery from exhaust air can be used to heat water.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-electric-load-center-generator/#generatormicroturbine
        """

class FloorInterzone_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Floor:Interzone`` and add it to the document.

        Allows for simplified entry of floors using adjacent zone (interzone) heat transfer - adjacent surface should be a ceiling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#floorinterzone
        """
