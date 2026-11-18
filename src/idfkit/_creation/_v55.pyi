"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class HeatExchangerAirToAirSensibleAndLatent_v8_9_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_supply_air_flow_rate: float | Literal["Autosize"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        exhaust_air_inlet_node_name: str,
        exhaust_air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        sensible_effectiveness_at_100_heating_air_flow: float | None = 0,
        latent_effectiveness_at_100_heating_air_flow: float | None = 0,
        sensible_effectiveness_at_75_heating_air_flow: float | None = 0,
        latent_effectiveness_at_75_heating_air_flow: float | None = 0,
        sensible_effectiveness_at_100_cooling_air_flow: float | None = 0,
        latent_effectiveness_at_100_cooling_air_flow: float | None = 0,
        sensible_effectiveness_at_75_cooling_air_flow: float | None = 0,
        latent_effectiveness_at_75_cooling_air_flow: float | None = 0,
        nominal_electric_power: float | None = 0,
        supply_air_outlet_temperature_control: Literal["", "No", "Yes"] | None = "No",
        heat_exchanger_type: Literal["", "Plate", "Rotary"] | None = "Plate",
        frost_control_type: Literal["", "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"]
        | None = "None",
        threshold_temperature: float | None = 1.7,
        initial_defrost_time_fraction: float | None = 0.083,
        rate_of_defrost_time_fraction_increase: float | None = 0.012,
        economizer_lockout: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``HeatExchanger:AirToAir:SensibleAndLatent`` and add it to the document.

        This object models an air-to-air heat exchanger using effectiveness relationships. The heat exchanger can transfer sensible energy, latent energy, or both between the supply (primary) and exhaust (secondary) air streams.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-heat-recovery/#heatexchangerairtoairsensibleandlatent
        """

class FuelFactors_v8_9_to_v9_2:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        existing_fuel_resource_name: str | None = ...,
        units_of_measure: str | None = ...,
        energy_per_unit_factor: float | None = ...,
        source_energy_factor: float | None = ...,
        source_energy_schedule_name: str | None = ...,
        co2_emission_factor: float | None = ...,
        co2_emission_factor_schedule_name: str | None = ...,
        co_emission_factor: float | None = ...,
        co_emission_factor_schedule_name: str | None = ...,
        ch4_emission_factor: float | None = ...,
        ch4_emission_factor_schedule_name: str | None = ...,
        nox_emission_factor: float | None = ...,
        nox_emission_factor_schedule_name: str | None = ...,
        n2o_emission_factor: float | None = ...,
        n2o_emission_factor_schedule_name: str | None = ...,
        so2_emission_factor: float | None = ...,
        so2_emission_factor_schedule_name: str | None = ...,
        pm_emission_factor: float | None = ...,
        pm_emission_factor_schedule_name: str | None = ...,
        pm10_emission_factor: float | None = ...,
        pm10_emission_factor_schedule_name: str | None = ...,
        pm2_5_emission_factor: float | None = ...,
        pm2_5_emission_factor_schedule_name: str | None = ...,
        nh3_emission_factor: float | None = ...,
        nh3_emission_factor_schedule_name: str | None = ...,
        nmvoc_emission_factor: float | None = ...,
        nmvoc_emission_factor_schedule_name: str | None = ...,
        hg_emission_factor: float | None = ...,
        hg_emission_factor_schedule_name: str | None = ...,
        pb_emission_factor: float | None = ...,
        pb_emission_factor_schedule_name: str | None = ...,
        water_emission_factor: float | None = ...,
        water_emission_factor_schedule_name: str | None = ...,
        nuclear_high_level_emission_factor: float | None = ...,
        nuclear_high_level_emission_factor_schedule_name: str | None = ...,
        nuclear_low_level_emission_factor: float | None = ...,
        nuclear_low_level_emission_factor_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``FuelFactors`` and add it to the document.

        Provides Fuel Factors for Emissions as well as Source=>Site conversions. OtherFuel1, OtherFuel2 provide options for users who want to create and use fuels that may not be mainstream (biomass, wood, pellets).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/input-for-output/#fuelfactors
        """

class SiteGroundDomainSlab_v8_9_to_v22_1:
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
        slab_boundary_condition_model_name: str,
        slab_location: Literal["InGrade", "OnGrade"],
        ground_domain_depth: float | None = 10,
        aspect_ratio: float | None = 1,
        perimeter_offset: float | None = 5,
        soil_thermal_conductivity: float | None = 1.5,
        soil_density: float | None = 2800,
        soil_specific_heat: float | None = 850,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        slab_material_name: str | None = ...,
        horizontal_insulation: Literal["", "No", "Yes"] | None = "No",
        horizontal_insulation_material_name: str | None = ...,
        horizontal_insulation_extents: Literal["", "Full", "Perimeter"] | None = "Full",
        perimeter_insulation_width: float | None = ...,
        vertical_insulation: Literal["", "No", "Yes"] | None = "No",
        vertical_insulation_material_name: str | None = ...,
        vertical_insulation_depth: float | None = ...,
        simulation_timestep: Literal["", "Hourly", "Timestep"] | None = "Hourly",
        geometric_mesh_coefficient: float | None = 1.6,
        mesh_density_parameter: float | None = 6,
    ) -> None:
        """Create a new ``Site:GroundDomain:Slab`` and add it to the document.

        Ground-coupled slab model for on-grade and in-grade cases with or without insulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-location-climate-weather-file-access/#sitegrounddomainslab
        """

class CoolingTowerSingleSpeed_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_air_flow_rate: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_air_flow_rate_sizing_factor: float | None = 0.1,
        free_convection_u_factor_times_area_value: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | None = ...,
        free_convection_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        number_of_cells: float | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = "MinimalCell",
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:SingleSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a single-speed fan drawing air through the tower (induced-draft configuration). Added fluid bypass as an additional capacity control. 8/2008. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-condenser-equipment/#coolingtowersinglespeed
        """
