"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class ExteriorFuelEquipment_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_use_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
            "Water",
        ],
        schedule_name: str,
        design_level: float,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Exterior:FuelEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-exterior-energy-use-equipment/#exteriorfuelequipment
        """

class PumpVariableSpeedCondensate_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_steam_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None:
        """Create a new ``Pump:VariableSpeed:Condensate`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit. Variable Speed Condensate pump for Steam Systems

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-pumps/#pumpvariablespeedcondensate
        """

class ComponentCostLineItem_v8_9_to_v9_5:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        line_item_type: Literal[
            "Chiller:Electric",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:DX",
            "Coil:Heating:Fuel",
            "Construction",
            "Daylighting:Controls",
            "General",
            "Generator:Photovoltaic",
            "Lights",
            "Shading:Zone:Detailed",
        ],
        item_name: str,
        type: str | None = ...,
        object_end_use_key: str | None = ...,
        cost_per_each: float | None = ...,
        cost_per_area: float | None = ...,
        cost_per_unit_of_output_capacity: float | None = ...,
        cost_per_unit_of_output_capacity_per_cop: float | None = ...,
        cost_per_volume: float | None = ...,
        cost_per_volume_rate: float | None = ...,
        cost_per_energy_per_temperature_difference: float | None = ...,
        quantity: float | None = ...,
    ) -> None:
        """Create a new ``ComponentCost:LineItem`` and add it to the document.

        Each instance of this object creates a cost line item and will contribute to the total for a cost estimate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/energyplus-economics/cost-estimating/#componentcostlineitem
        """

class LifeCycleCostUseAdjustment_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ],
        multipliers: list[_g.LifeCycleCostUseAdjustmentMultipliersItem] = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:UseAdjustment`` and add it to the document.

        Used by advanced users to adjust the energy or water use costs for future years. This should not be used for compensating for inflation but should only be used to increase the costs of energy or water based on assumed changes to the actual usage, such as anticipated changes in the future function of the building. The adjustments begin at the start of the service period.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/energyplus-economics/lifecyclecost-useadjustment/#lifecyclecostuseadjustment
        """

class MeterCustomDecrement_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_meter_name: str,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ]
        | None = ...,
        variable_details: list[_g.MeterCustomDecrementVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Meter:CustomDecrement`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-simulation-parameters/#metercustomdecrement
        """

class PipingSystemUndergroundPipeCircuit_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        pipe_thermal_conductivity: float,
        pipe_density: float,
        pipe_specific_heat: float,
        pipe_inner_diameter: float,
        pipe_outer_diameter: float,
        design_flow_rate: float,
        circuit_inlet_node: str,
        circuit_outlet_node: str,
        radial_thickness_of_inner_radial_near_pipe_mesh_region: float,
        number_of_pipe_segments_entered_for_this_pipe_circuit: float,
        convergence_criterion_for_the_inner_radial_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_inner_radial_iteration_loop: float | None = 500,
        number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region: float | None = 3,
        pipe_segments: list[_g.PipingSystemUndergroundPipeCircuitPipeSegmentsItem] = ...,
    ) -> None:
        """Create a new ``PipingSystem:Underground:PipeCircuit`` and add it to the document.

        The pipe circuit object in an underground piping system. This object is simulated within an underground piping domain object and connected on a branch on a plant loop.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-node-branch-management/#pipingsystemundergroundpipecircuit
        """

class AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_terminal_unit_list_name: str,
        outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R410A",
        rated_evaporative_capacity: float | Literal["", "Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_only_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_only_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_only_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_only_mode: float | None = 16,
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -20,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 43,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["", "ConstantTemp", "VariableTemp"]
        | None = "VariableTemp",
        reference_evaporating_temperature_for_indoor_unit: float | None = 6,
        reference_condensing_temperature_for_indoor_unit: float | None = 44,
        variable_evaporating_temperature_minimum_for_indoor_unit: float | None = 4,
        variable_evaporating_temperature_maximum_for_indoor_unit: float | None = 13,
        variable_condensing_temperature_minimum_for_indoor_unit: float | None = 42,
        variable_condensing_temperature_maximum_for_indoor_unit: float | None = 46,
        outdoor_unit_evaporator_reference_superheating: float | None = 3,
        outdoor_unit_condenser_reference_subcooling: float | None = 5,
        outdoor_unit_evaporator_rated_bypass_factor: float | None = 0.4,
        outdoor_unit_condenser_rated_bypass_factor: float | None = 0.2,
        difference_between_outdoor_unit_evaporating_temperature_and_outdoor_air_temperature_in_heat_recovery_mode: float
        | None = 5,
        outdoor_unit_heat_exchanger_capacity_ratio: float | None = 0.3,
        outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None = 0.00425,
        outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None = ...,
        diameter_of_main_pipe_for_suction_gas: float | None = 0.0762,
        diameter_of_main_pipe_for_discharge_gas: float | None = 0.0762,
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
        initial_heat_recovery_cooling_capacity_fraction: float | None = 1,
        heat_recovery_cooling_capacity_time_constant: float | None = 0,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
        compressor_maximum_delta_pressure: float | None = 4500000,
        compressor_inverter_efficiency: float | None = 0.95,
        compressor_evaporative_capacity_correction_factor: float | None = 1,
        number_of_compressor_loading_index_entries: float | None = 2,
        loading_indices: list[
            _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHRLoadingIndicesItem
        ] = ...,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR`` and add it to the document.

        This is a key object in the new physics based VRF Heat Recovery (HR) model applicable for Fluid Temperature Control. It describes the VRF HR system excluding the performance of indoor units. Indoor units are modeled separately in the ZoneHVAC:TerminalUnit:VariableRefrigerantFlow object

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflowfluidtemperaturecontrolhr
        """

class HybridModelZone_v9_1_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        calculate_zone_internal_thermal_mass: Literal["", "No", "Yes"] | None = "No",
        calculate_zone_air_infiltration_rate: Literal["", "No", "Yes"] | None = "No",
        calculate_zone_people_count: Literal["", "No", "Yes"] | None = "No",
        zone_measured_air_temperature_schedule_name: str | None = ...,
        zone_measured_air_humidity_ratio_schedule_name: str | None = ...,
        zone_measured_air_co2_concentration_schedule_name: str | None = ...,
        zone_input_people_activity_schedule_name: str | None = ...,
        zone_input_people_sensible_heat_fraction_schedule_name: str | None = ...,
        zone_input_people_radiant_heat_fraction_schedule_name: str | None = ...,
        zone_input_people_co2_generation_rate_schedule_name: str | None = ...,
        zone_input_supply_air_temperature_schedule_name: str | None = ...,
        zone_input_supply_air_mass_flow_rate_schedule_name: str | None = ...,
        zone_input_supply_air_humidity_ratio_schedule_name: str | None = ...,
        zone_input_supply_air_co2_concentration_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``HybridModel:Zone`` and add it to the document.

        Zones with measured air temperature data and a range of dates. If the range of temperature measurement dates includes a leap day, the weather data should include a leap day.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-hybrid-model/#hybridmodelzone
        """

class LifeCycleCostUsePriceEscalation_v22_2_to_v23_1:
    def __call__(
        self,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ],
        escalation_start_year: int | None = ...,
        escalation_start_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        escalations: list[_g.LifeCycleCostUsePriceEscalationEscalationsItem] = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:UsePriceEscalation`` and add it to the document.

        Life cycle cost escalation factors. The values for this object may be found in the annual supplement to NIST Handbook 135 in Tables Ca-1 to Ca-5 and are included in an EnergyPlus dataset file.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/energyplus-economics/lifecyclecost-usepriceescalation/#lifecyclecostusepriceescalation
        """

class HVACTemplateSystemVRF_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
        gross_rated_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = 30,
        vertical_height_used_for_piping_correction_factor: float | None = 10,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = 30,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: float | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_condenser_volume_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal[
            "",
            "Diesel",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
        ]
        | None = "Electricity",
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -15,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 45,
    ) -> None:
        """Create a new ``HVACTemplate:System:VRF`` and add it to the document.

        Variable refrigerant flow (VRF) heat pump condensing unit. Serves one or more VRF zone terminal units (HVACTemplate:Zone:VRF).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemvrf
        """

class MeterCustom_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ]
        | None = ...,
        variable_details: list[_g.MeterCustomVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Meter:Custom`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:Custom cannot reference another Meter:Custom.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-simulation-parameters/#metercustom
        """

class CoilCoolingDXCurveFitSpeed_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_total_cooling_capacity_fraction: float,
        evaporator_air_flow_rate_fraction: float,
        condenser_air_flow_rate_fraction: float | None = ...,
        gross_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        gross_cooling_cop: float | None = 3,
        active_fraction_of_coil_face_area: float | None = 1,
        rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        evaporative_condenser_pump_power_fraction: float | None = 1,
        evaporative_condenser_effectiveness: float | None = 0.9,
        total_cooling_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        total_cooling_capacity_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        waste_heat_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Speed`` and add it to the document.

        DX cooling coil performance for a single speed within a single operating mode.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitspeed
        """

class HeatPumpAirToWaterFuelFiredCooling_v23_1_to_v25_1:
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
    ) -> None:
        """Create a new ``HeatPump:AirToWater:FuelFired:Cooling`` and add it to the document.

        The object defines a fuel-fired absorption heat pump based on equation-fit models.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-plant-heating-and-cooling-equipment/#heatpumpairtowaterfuelfiredcooling
        """

class ZoneControlContaminantController_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        carbon_dioxide_control_availability_schedule_name: str | None = ...,
        carbon_dioxide_setpoint_schedule_name: str | None = ...,
        minimum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        maximum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        generic_contaminant_control_availability_schedule_name: str | None = ...,
        generic_contaminant_setpoint_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneControl:ContaminantController`` and add it to the document.

        Used to control a zone to a specified indoor level of CO2 or generic contaminants, or to specify minimum CO2 concentration schedule name for a zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-zone-controls-thermostats/#zonecontrolcontaminantcontroller
        """
