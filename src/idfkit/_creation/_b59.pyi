"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnySiteGroundDomainSlab:
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
        horizontal_insulation: Literal["No", "Yes"] | None = "No",
        horizontal_insulation_material_name: str | None = ...,
        horizontal_insulation_extents: Literal["Full", "Perimeter"] | None = "Full",
        perimeter_insulation_width: float | None = ...,
        vertical_insulation: Literal["No", "Yes"] | None = "No",
        vertical_insulation_material_name: str | None = ...,
        vertical_insulation_depth: float | None = ...,
        simulation_timestep: Literal["Hourly", "Timestep"] | None = "Hourly",
        geometric_mesh_coefficient: float | None = 1.6,
        mesh_density_parameter: int | None = 6,
        validate: bool = True,
    ) -> None:
        """Create a new ``Site:GroundDomain:Slab`` and add it to the document.

        Ground-coupled slab model for on-grade and in-grade cases with or without insulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegrounddomainslab
        """

class DaylightingControls:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        daylighting_method: Literal["DElight", "SplitFlux"] | None = "SplitFlux",
        availability_schedule_name: str | None = ...,
        lighting_control_type: Literal["Continuous", "ContinuousOff", "Stepped"] | None = "Continuous",
        minimum_input_power_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.3,
        minimum_light_output_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.2,
        number_of_stepped_control_steps: int | None = 1,
        probability_lighting_will_be_reset_when_needed_in_manual_stepped_control: float | None = 1,
        glare_calculation_daylighting_reference_point_name: str | None = ...,
        glare_calculation_azimuth_angle_of_view_direction_clockwise_from_zone_y_axis: float | None = 0,
        maximum_allowable_discomfort_glare_index: float | None = 22,
        delight_gridding_resolution: float | None = ...,
        control_data: Sequence[_g.DaylightingControlsControlDataItem | _g.DaylightingControlsControlDataGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Daylighting:Controls`` and add it to the document.

        Dimming of overhead electric lighting is determined from each reference point. Glare from daylighting is also calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#daylightingcontrols
        """

class PipeUnderground:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        sun_exposure: Literal["NoSun", "SunExposed"],
        soil_material_name: str,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        pipe_inside_diameter: float | None = ...,
        pipe_length: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Pipe:Underground`` and add it to the document.

        Buried Pipe model: For pipes buried at a depth less than one meter, this is an alternative object to: HeatExchanger:Surface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipeunderground
        """

class AnyPumpConstantSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        pump_curve_name: str | None = ...,
        impeller_diameter: float | None = ...,
        rotational_speed: float | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        validate: bool = True,
    ) -> None:
        """Create a new ``Pump:ConstantSpeed`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#pumpconstantspeed
        """

class AnyHeatPumpPlantLoopEIRHeating:
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
        condenser_type: Literal["AirSource", "WaterSource"] | None = "WaterSource",
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = ...,
        sizing_factor: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Heating`` and add it to the document.

        An EIR formulated water to water heat pump model, heating operation

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpplantloopeirheating
        """

class AvailabilityManagerNightVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_zone_name: str,
        ventilation_temperature_schedule_name: str | None = ...,
        ventilation_temperature_difference: float | None = 2,
        ventilation_temperature_low_limit: float | None = 15,
        night_venting_flow_fraction: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``AvailabilityManager:NightVentilation`` and add it to the document.

        depending on zone and outdoor conditions overrides fan schedule to do precooling with outdoor air

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagernightventilation
        """

class OutputConstructions:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        details_type_1: Literal["Constructions", "Materials"] | None = ...,
        details_type_2: Literal["Constructions", "Materials"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Constructions`` and add it to the document.

        Adds a report to the eio output file which shows details for each construction, including overall properties, a list of material layers, and calculated results related to conduction transfer functions.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputconstructions
        """
