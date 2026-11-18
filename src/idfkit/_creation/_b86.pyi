"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class WindowGapDeflectionState:
    def __call__(
        self,
        name: str,
        /,
        *,
        deflected_thickness: float | None = 0,
        initial_temperature: float | None = 25,
        initial_pressure: float | None = 101325,
    ) -> None:
        """Create a new ``WindowGap:DeflectionState`` and add it to the document.

        Used to enter data describing deflection state of the gap. It is referenced from WindowMaterial:Gap object only and it is used only when deflection model is set to MeasuredDeflection, otherwise it is ignored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowgapdeflectionstate
        """

class GroundHeatTransferSlabBldgProps:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        iyrs_number_of_years_to_iterate: float | None = 10,
        shape_slab_shape: float | None = ...,
        hbldg_building_height: float | None = ...,
        tin1_january_indoor_average_temperature_setpoint: float | None = 22,
        tin2_february_indoor_average_temperature_setpoint: float | None = 22,
        tin3_march_indoor_average_temperature_setpoint: float | None = 22,
        tin4_april_indoor_average_temperature_setpoint: float | None = 22,
        tin5_may_indoor_average_temperature_setpoint: float | None = 22,
        tin6_june_indoor_average_temperature_setpoint: float | None = 22,
        tin7_july_indoor_average_temperature_setpoint: float | None = 22,
        tin8_august_indoor_average_temperature_setpoint: float | None = 22,
        tin9_september_indoor_average_temperature_setpoint: float | None = 22,
        tin10_october_indoor_average_temperature_setpoint: float | None = 22,
        tin11_november_indoor_average_temperature_setpoint: float | None = 22,
        tin12_december_indoor_average_temperature_setpoint: float | None = 22,
        tinamp_daily_indoor_sine_wave_variation_amplitude: float | None = 0,
        convtol_convergence_tolerance: float | None = 0.1,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:BldgProps`` and add it to the document.

        Object provides information about the building and its operating conditions Monthly Average Temperature SetPoint fields specify the average indoor building set point temperatures for each month of the year. These fields are useful for simulating a building that is not temperature controlled for some of the year. In such a case, the average indoor set point temperatures can be obtained by first running the model in EnergyPlus with an insulated floor boundary condition, and then using the resulting monthly average zone temperatures in these fields.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabbldgprops
        """

class GroundHeatTransferBasementBldgData:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        dwall_wall_thickness: float | None = 0.2,
        dslab_floor_slab_thickness: float | None = 0.1,
        dgravxy_width_of_gravel_pit_beside_basement_wall: float | None = 0.3,
        dgravzn_gravel_depth_extending_above_the_floor_slab: float | None = 0.2,
        dgravzp_gravel_depth_below_the_floor_slab: float | None = 0.1,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:BldgData`` and add it to the document.

        Specifies the surface and gravel thicknesses used for the Basement preprocessor ground heat transfer simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementbldgdata
        """

class ElectricEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal["EquipmentLevel", "Watts/Area", "Watts/Person"]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        watts_per_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
    ) -> None:
        """Create a new ``ElectricEquipment:Definition`` and add it to the document.

        Defines the physical characteristics (design level and heat gain fractions) for electric equipment. Referenced by one or more ElectricEquipment:Instance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#electricequipmentdefinition
        """

class AirflowNetworkMultiZoneComponentZoneExhaustFan:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_the_zone_exhaust_fan_is_off_at_reference_conditions: float,
        air_mass_flow_exponent_when_the_zone_exhaust_fan_is_off: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Component:ZoneExhaustFan`` and add it to the document.

        This object specifies the additional properties for a zone exhaust fan to perform multizone airflow calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonecomponentzoneexhaustfan
        """

class HVACTemplatePlantChilledWaterLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        pump_schedule_name: str | None = ...,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Intermittent",
        chiller_plant_operation_scheme_type: Literal["Default", "UserDefined"] | None = "Default",
        chiller_plant_equipment_operation_schemes_name: str | None = ...,
        chilled_water_setpoint_schedule_name: str | None = ...,
        chilled_water_design_setpoint: float | None = 7.22,
        chilled_water_pump_configuration: Literal[
            "ConstantPrimaryNoSecondary", "ConstantPrimaryVariableSecondary", "VariablePrimaryNoSecondary"
        ]
        | None = "ConstantPrimaryNoSecondary",
        primary_chilled_water_pump_rated_head: float | None = 179352,
        secondary_chilled_water_pump_rated_head: float | None = 179352,
        condenser_plant_operation_scheme_type: Literal["Default", "UserDefined"] | None = "Default",
        condenser_equipment_operation_schemes_name: str | None = ...,
        condenser_water_temperature_control_type: Literal["OutdoorWetBulbTemperature", "SpecifiedSetpoint"]
        | None = ...,
        condenser_water_setpoint_schedule_name: str | None = ...,
        condenser_water_design_setpoint: float | None = 29.4,
        condenser_water_pump_rated_head: float | None = 179352,
        chilled_water_setpoint_reset_type: Literal["None", "OutdoorAirTemperatureReset"] | None = "None",
        chilled_water_setpoint_at_outdoor_dry_bulb_low: float | None = 12.2,
        chilled_water_reset_outdoor_dry_bulb_low: float | None = 15.6,
        chilled_water_setpoint_at_outdoor_dry_bulb_high: float | None = 6.7,
        chilled_water_reset_outdoor_dry_bulb_high: float | None = 26.7,
        chilled_water_primary_pump_type: Literal[
            "FiveHeaderedPumps",
            "FourHeaderedPumps",
            "PumpPerChiller",
            "SinglePump",
            "ThreeHeaderedPumps",
            "TwoHeaderedPumps",
        ]
        | None = "SinglePump",
        chilled_water_secondary_pump_type: Literal[
            "FiveHeaderedPumps", "FourHeaderedPumps", "SinglePump", "ThreeHeaderedPumps", "TwoHeaderedPumps"
        ]
        | None = "SinglePump",
        condenser_water_pump_type: Literal[
            "FiveHeaderedPumps",
            "FourHeaderedPumps",
            "PumpPerTower",
            "SinglePump",
            "ThreeHeaderedPumps",
            "TwoHeaderedPumps",
        ]
        | None = "SinglePump",
        chilled_water_supply_side_bypass_pipe: Literal["No", "Yes"] | None = "Yes",
        chilled_water_demand_side_bypass_pipe: Literal["No", "Yes"] | None = "Yes",
        condenser_water_supply_side_bypass_pipe: Literal["No", "Yes"] | None = "Yes",
        condenser_water_demand_side_bypass_pipe: Literal["No", "Yes"] | None = "Yes",
        fluid_type: Literal[
            "EthyleneGlycol30",
            "EthyleneGlycol40",
            "EthyleneGlycol50",
            "EthyleneGlycol60",
            "PropyleneGlycol30",
            "PropyleneGlycol40",
            "PropyleneGlycol50",
            "PropyleneGlycol60",
            "Water",
        ]
        | None = "Water",
        loop_design_delta_temperature: float | None = 6.67,
        minimum_outdoor_dry_bulb_temperature: float | None = ...,
        chilled_water_load_distribution_scheme: Literal[
            "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
        condenser_water_load_distribution_scheme: Literal[
            "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
    ) -> None:
        """Create a new ``HVACTemplate:Plant:ChilledWaterLoop`` and add it to the document.

        Plant and condenser loops to serve all HVACTemplate chilled water coils, chillers, and towers.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantchilledwaterloop
        """

class CoilCoolingDXCurveFitPerformance:
    def __call__(
        self,
        name: str,
        /,
        *,
        base_operating_mode: str,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        unit_internal_static_air_pressure: float | None = ...,
        capacity_control_method: Literal["Continuous", "Discrete"] | None = "Discrete",
        evaporative_condenser_basin_heater_capacity: float | None = 0,
        evaporative_condenser_basin_heater_setpoint_temperature: float | None = 2,
        evaporative_condenser_basin_heater_operating_schedule_name: str | None = ...,
        compressor_fuel_type: Literal[
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
        alternative_operating_mode_1: str | None = ...,
        alternative_operating_mode_2: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Performance`` and add it to the document.

        DX cooling coil performance specification referencing one or more operating modes. Mode 1 is always the base design operating mode. Additional modes are optional states such as subcool reheat for humidity control.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitperformance
        """

class AirConditionerVariableRefrigerantFlowFluidTemperatureControl:
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
        rated_evaporative_capacity: float | Literal["Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_mode: float | None = 16,
        reference_outdoor_unit_superheating: float | None = 3,
        reference_outdoor_unit_subcooling: float | None = 5,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["ConstantTemp", "VariableTemp"]
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
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = 0,
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

class SetpointManagerMultiZoneHumidityMaximum:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_humidity_ratio: float | None = 0.008,
        maximum_setpoint_humidity_ratio: float | None = 0.015,
    ) -> None:
        """Create a new ``SetpointManager:MultiZone:Humidity:Maximum`` and add it to the document.

        This setpoint manager sets the maximum supply air humidity ratio based on dehumidification requirements of a controlled zone with critical humidity ratio setpoint (i.e., a zone with the lowest humidity ratio setpoint) in an air loop served by a central air-conditioner.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagermultizonehumiditymaximum
        """

class OutputControlFiles:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        output_csv: Literal["No", "Yes"] | None = "No",
        output_mtr: Literal["No", "Yes"] | None = "Yes",
        output_eso: Literal["No", "Yes"] | None = "Yes",
        output_eio: Literal["No", "Yes"] | None = "Yes",
        output_tabular: Literal["No", "Yes"] | None = "Yes",
        output_sqlite: Literal["No", "Yes"] | None = "Yes",
        output_json: Literal["No", "Yes"] | None = "Yes",
        output_audit: Literal["No", "Yes"] | None = "Yes",
        output_space_sizing: Literal["No", "Yes"] | None = "Yes",
        output_zone_sizing: Literal["No", "Yes"] | None = "Yes",
        output_system_sizing: Literal["No", "Yes"] | None = "Yes",
        output_dxf: Literal["No", "Yes"] | None = "Yes",
        output_bnd: Literal["No", "Yes"] | None = "Yes",
        output_rdd: Literal["No", "Yes"] | None = "Yes",
        output_mdd: Literal["No", "Yes"] | None = "Yes",
        output_mtd: Literal["No", "Yes"] | None = "Yes",
        output_end: Literal["No", "Yes"] | None = "Yes",
        output_shd: Literal["No", "Yes"] | None = "Yes",
        output_dfs: Literal["No", "Yes"] | None = "Yes",
        output_glhe: Literal["No", "Yes"] | None = "Yes",
        output_delightin: Literal["No", "Yes"] | None = "Yes",
        output_delighteldmp: Literal["No", "Yes"] | None = "Yes",
        output_delightdfdmp: Literal["No", "Yes"] | None = "Yes",
        output_edd: Literal["No", "Yes"] | None = "Yes",
        output_dbg: Literal["No", "Yes"] | None = "Yes",
        output_perflog: Literal["No", "Yes"] | None = "Yes",
        output_sln: Literal["No", "Yes"] | None = "Yes",
        output_sci: Literal["No", "Yes"] | None = "Yes",
        output_wrl: Literal["No", "Yes"] | None = "Yes",
        output_screen: Literal["No", "Yes"] | None = "Yes",
        output_extshd: Literal["No", "Yes"] | None = "Yes",
        output_tarcog: Literal["No", "Yes"] | None = "Yes",
        output_plant_component_sizing: Literal["No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``OutputControl:Files`` and add it to the document.

        Conditionally turn on/off output from EnergyPlus.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputcontrolfiles
        """

class OutputControlTimestamp:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        iso_8601_format: Literal["No", "Yes"] | None = "No",
        timestamp_at_beginning_of_interval: Literal["No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``OutputControl:Timestamp`` and add it to the document.

        Control timestamp format, currently applies only to JSON and native CSV (not CSV via ReadVars)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputcontroltimestamp
        """

class AnyOutputDiagnostics:
    def __call__(self, this_type_has_no_name_field: _g._PassFieldsAsKeywords = ..., /) -> None:
        """Create a new ``Output:Diagnostics`` and add it to the document.

        Special keys to produce certain warning messages or effect certain simulation characteristics.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#outputdiagnostics
        """
