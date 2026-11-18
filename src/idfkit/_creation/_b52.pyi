"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class MaterialPropertyHeatAndMoistureTransferThermalConductivity:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        material_name: str,
        number_of_thermal_coordinates: int,
        moisture_content_1: float,
        thermal_conductivity_1: float,
        moisture_content_2: float | None = ...,
        thermal_conductivity_2: float | None = ...,
        moisture_content_3: float | None = ...,
        thermal_conductivity_3: float | None = ...,
        moisture_content_4: float | None = ...,
        thermal_conductivity_4: float | None = ...,
        moisture_content_5: float | None = ...,
        thermal_conductivity_5: float | None = ...,
        moisture_content_6: float | None = ...,
        thermal_conductivity_6: float | None = ...,
        moisture_content_7: float | None = ...,
        thermal_conductivity_7: float | None = ...,
        moisture_content_8: float | None = ...,
        thermal_conductivity_8: float | None = ...,
        moisture_content_9: float | None = ...,
        thermal_conductivity_9: float | None = ...,
        moisture_content_10: float | None = ...,
        thermal_conductivity_10: float | None = ...,
        moisture_content_11: float | None = ...,
        thermal_conductivity_11: float | None = ...,
        moisture_content_12: float | None = ...,
        thermal_conductivity_12: float | None = ...,
        moisture_content_13: float | None = ...,
        thermal_conductivity_13: float | None = ...,
        moisture_content_14: float | None = ...,
        thermal_conductivity_14: float | None = ...,
        moisture_content_15: float | None = ...,
        thermal_conductivity_15: float | None = ...,
        moisture_content_16: float | None = ...,
        thermal_conductivity_16: float | None = ...,
        moisture_content_17: float | None = ...,
        thermal_conductivity_17: float | None = ...,
        moisture_content_18: float | None = ...,
        thermal_conductivity_18: float | None = ...,
        moisture_content_19: float | None = ...,
        thermal_conductivity_19: float | None = ...,
        moisture_content_20: float | None = ...,
        thermal_conductivity_20: float | None = ...,
        moisture_content_21: float | None = ...,
        thermal_conductivity_21: float | None = ...,
        moisture_content_22: float | None = ...,
        thermal_conductivity_22: float | None = ...,
        moisture_content_23: float | None = ...,
        thermal_conductivity_23: float | None = ...,
        moisture_content_24: float | None = ...,
        thermal_conductivity_24: float | None = ...,
        moisture_content_25: float | None = ...,
        thermal_conductivity_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:ThermalConductivity`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between thermal conductivity and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferthermalconductivity
        """

class GlazedDoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``GlazedDoor`` and add it to the document.

        Allows for simplified entry of glass Doors.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#glazeddoor
        """

class WindowPropertyFrameAndDivider:
    def __call__(
        self,
        name: str,
        /,
        *,
        frame_width: float | None = 0,
        frame_outside_projection: float | None = 0,
        frame_inside_projection: float | None = 0,
        frame_conductance: float | None = 0,
        ratio_of_frame_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        frame_solar_absorptance: float | None = 0.7,
        frame_visible_absorptance: float | None = 0.7,
        frame_thermal_hemispherical_emissivity: float | None = 0.9,
        divider_type: Literal["", "DividedLite", "Suspended"] | None = "DividedLite",
        divider_width: float | None = 0,
        number_of_horizontal_dividers: int | None = 0,
        number_of_vertical_dividers: int | None = 0,
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
        nfrc_product_type_for_assembly_calculations: Literal[
            "",
            "CasementDouble",
            "CasementSingle",
            "CurtainWall",
            "DoorSidelite",
            "DoorTransom",
            "DualAction",
            "Fixed",
            "Garage",
            "Greenhouse",
            "HingedEscape",
            "HorizontalSlider",
            "Jal",
            "Pivoted",
            "ProjectingDual",
            "ProjectingSingle",
            "SideHingedDoor",
            "Skylight",
            "SlidingPatioDoor",
            "SpandrelPanel",
            "TropicalAwning",
            "TubularDaylightingDevice",
            "VerticalSlider",
        ]
        | None = "CurtainWall",
    ) -> None:
        """Create a new ``WindowProperty:FrameAndDivider`` and add it to the document.

        Specifies the dimensions of a window frame, dividers, and inside reveal surfaces. Referenced by the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertyframeanddivider
        """

class AnyCoilSystemCoolingDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        dx_cooling_coil_system_inlet_node_name: str,
        dx_cooling_coil_system_outlet_node_name: str,
        dx_cooling_coil_system_sensor_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["", "No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["", "No", "Yes"] | None = "No",
        use_outdoor_air_dx_cooling_coil: Literal["", "No", "Yes"] | None = "No",
        outdoor_air_dx_cooling_coil_leaving_minimum_air_temperature: float | None = 2,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX`` and add it to the document.

        Virtual container component that consists of a DX cooling coil and its associated controls. This control object supports several different types of DX cooling coils and may be placed directly in an air loop branch or outdoor air equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdx
        """

class EvaporativeCoolerDirectResearchSpecial:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        sensor_node_name: str,
        availability_schedule_name: str | None = ...,
        cooler_design_effectiveness: float | None = ...,
        effectiveness_flow_ratio_modifier_curve_name: str | None = ...,
        primary_air_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        recirculating_water_pump_design_power: float | Literal["", "Autosize"] | None = "Autosize",
        water_pump_power_sizing_factor: float | None = 90,
        water_pump_power_modifier_curve_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        drift_loss_fraction: float | None = ...,
        blowdown_concentration_ratio: float | None = ...,
        evaporative_operation_minimum_drybulb_temperature: float | None = ...,
        evaporative_operation_maximum_limit_wetbulb_temperature: float | None = ...,
        evaporative_operation_maximum_limit_drybulb_temperature: float | None = ...,
    ) -> None:
        """Create a new ``EvaporativeCooler:Direct:ResearchSpecial`` and add it to the document.

        Direct evaporative cooler with user-specified effectiveness (can represent rigid pad or similar media), and recirculating water pump, and secondary air fan. This model is controlled to meet the primary air outlet temperature setpoint.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-evaporative-coolers/#evaporativecoolerdirectresearchspecial
        """

class AnyAirConditionerVariableRefrigerantFlowFluidTemperatureControl:
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
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        compressor_maximum_delta_pressure: float | None = 4500000,
        number_of_compressor_loading_index_entries: int | None = 2,
        loading_indices: Sequence[
            _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlLoadingIndicesItem
            | _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlLoadingIndicesGroup
        ] = ...,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl`` and add it to the document.

        This is a key object in the new physics based VRF model applicable for Fluid Temperature Control It describes the Variable Refrigerant Flow system excluding the performance of indoor units Indoor units are modeled separately, see ZoneHVAC:TerminalUnit:VariableRefrigerantFlow

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflowfluidtemperaturecontrol
        """

class CurveFanPressureRise:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        minimum_value_of_qfan: float,
        maximum_value_of_qfan: float,
        minimum_value_of_psm: float,
        maximum_value_of_psm: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
    ) -> None:
        """Create a new ``Curve:FanPressureRise`` and add it to the document.

        Special curve type with two independent variables. Input for the fan total pressure rise curve consists of the curve name, the four coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1*Qfan**2+C2*Qfan+C3*Qfan*(Psm-Po)**0.5+C4*(Psm-Po) Po assumed to be zero See InputOut Reference for curve details

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvefanpressurerise
        """

class AnyOutputControlTableStyle:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        column_separator: Literal[
            "", "All", "Comma", "CommaAndHTML", "CommaAndXML", "Fixed", "HTML", "Tab", "TabAndHTML", "XML", "XMLandHTML"
        ]
        | None = "Comma",
        unit_conversion: Literal["", "InchPound", "JtoGJ", "JtoKWH", "JtoMJ", "None"] | None = "None",
    ) -> None:
        """Create a new ``OutputControl:Table:Style`` and add it to the document.

        default style for the OutputControl:Table:Style is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a better choice. fixed puts spaces between the 'columns'. HTML produces tables in HTML. XML produces an XML file. note - if no OutputControl:Table:Style is included, the defaults are comma and None.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/outputcontrol-table-style/#outputcontroltablestyle
        """
