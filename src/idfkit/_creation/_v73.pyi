"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AirConditionerVariableRefrigerantFlowFluidTemperatureControl_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        heat_pump_name: str,
        zone_terminal_unit_list_name: str,
        outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R410A",
        rated_evaporative_capacity: float | Literal["", "Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_mode: float | None = 16,
        reference_outdoor_unit_superheating: float | None = 3,
        reference_outdoor_unit_subcooling: float | None = 5,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["", "ConstantTemp", "VariableTemp"]
        | None = "VariableTemp",
        reference_evaporating_temperature_for_indoor_unit: float | None = 6,
        reference_condensing_temperature_for_indoor_unit: float | None = 44,
        variable_evaporating_temperature_minimum_for_indoor_unit: float | None = 4,
        variable_evaporating_temperature_maximum_for_indoor_unit: float | None = 13,
        variable_condensing_temperature_minimum_for_indoor_unit: float | None = 42,
        variable_condensing_temperature_maximum_for_indoor_unit: float | None = 46,
        outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None = 0.00425,
        outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None = ...,
        diameter_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 0.0762,
        length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 30,
        equivalent_length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 36,
        height_difference_between_outdoor_unit_and_indoor_units: float | None = 5,
        main_pipe_insulation_thickness: float | None = 0.02,
        main_pipe_insulation_thermal_conductivity: float | None = 0.032,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: float | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        compressor_maximum_delta_pressure: float | None = 4500000,
        number_of_compressor_loading_index_entries: float | None = 2,
        loading_indices: Sequence[
            _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlLoadingIndicesItem
            | _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlLoadingIndicesGroup
        ] = ...,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl`` and add it to the document.

        This is a key object in the new physics based VRF model applicable for Fluid Temperature Control It describes the Variable Refrigerant Flow system excluding the performance of indoor units Indoor units are modeled separately, see ZoneHVAC:TerminalUnit:VariableRefrigerantFlow

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflowfluidtemperaturecontrol
        """

class SizingSystem_v22_2_to_v25_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
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
    ) -> None:
        """Create a new ``Sizing:System`` and add it to the document.

        Specifies the input needed to perform sizing calculations for a central forced air system. System design air flow, heating capacity, and cooling capacity will be calculated using this input data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-design-objects/#sizingsystem
        """

class WindowPropertyFrameAndDivider_v8_9_to_v9_6:
    def __call__(
        self,
        name: str,
        /,
        *,
        frame_width: float | None = 0,
        frame_outside_projection: float | None = 0,
        frame_inside_projection: float | None = 0,
        frame_conductance: float | None = ...,
        ratio_of_frame_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        frame_solar_absorptance: float | None = 0.7,
        frame_visible_absorptance: float | None = 0.7,
        frame_thermal_hemispherical_emissivity: float | None = 0.9,
        divider_type: Literal["", "DividedLite", "Suspended"] | None = "DividedLite",
        divider_width: float | None = 0,
        number_of_horizontal_dividers: float | None = 0,
        number_of_vertical_dividers: float | None = 0,
        divider_outside_projection: float | None = 0,
        divider_inside_projection: float | None = 0,
        divider_conductance: float | None = 0,
        ratio_of_divider_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        divider_solar_absorptance: float | None = 0,
        divider_visible_absorptance: float | None = 0,
        divider_thermal_hemispherical_emissivity: float | None = 0.9,
        outside_reveal_solar_absorptance: float | None = 0,
        inside_sill_depth: float | None = 0,
        inside_sill_solar_absorptance: float | None = 0,
        inside_reveal_depth: float | None = 0,
        inside_reveal_solar_absorptance: float | None = 0,
    ) -> None:
        """Create a new ``WindowProperty:FrameAndDivider`` and add it to the document.

        Specifies the dimensions of a window frame, dividers, and inside reveal surfaces. Referenced by the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.6/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertyframeanddivider
        """

class SurfaceConvectionAlgorithmInside_v8_9_to_v9_4:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        algorithm: Literal["", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP"] | None = "TARP",
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Inside`` and add it to the document.

        Default indoor surface heat transfer convection algorithm to be used for all zones

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-simulation-parameters/#surfaceconvectionalgorithminside
        """

class MaterialPropertyVariableAbsorptance_v23_1_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_material_name: str,
        control_signal: Literal[
            "", "Scheduled", "SpaceHeatingCoolingMode", "SurfaceReceivedSolarRadiation", "SurfaceTemperature"
        ]
        | None = "SurfaceTemperature",
        thermal_absorptance_function_name: str | None = ...,
        thermal_absorptance_schedule_name: str | None = ...,
        solar_absorptance_function_name: str | None = ...,
        solar_absorptance_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:VariableAbsorptance`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-surface-construction-elements/#materialpropertyvariableabsorptance
        """
