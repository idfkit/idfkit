"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ConstructionAssignmentSet:
    def __call__(
        self,
        name: str,
        /,
        *,
        exterior_surface_construction_assignments_name: str | None = ...,
        interior_surface_construction_assignments_name: str | None = ...,
        ground_contact_surface_construction_assignments_name: str | None = ...,
        exterior_subsurface_construction_assignments_name: str | None = ...,
        interior_subsurface_construction_assignments_name: str | None = ...,
        interior_partition_construction_name: str | None = ...,
        adiabatic_surface_construction_name: str | None = ...,
    ) -> None:
        """Create a new ``ConstructionAssignmentSet`` and add it to the document.

        Defines a set of construction assignments for surfaces and sub-surfaces based on their type and outside boundary condition. Can be referenced by Building or Space objects. Space-level assignments take precedence over Building-level.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionassignmentset
        """

class GroundHeatTransferBasementEquivAutoGrid:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        clearance_distance_from_outside_of_wall_to_edge_of_3_d_ground_domain: float | None = 15,
        slabdepth_thickness_of_the_floor_slab: float | None = 0.1,
        basedepth_depth_of_the_basement_wall_below_grade: float | None = 2,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:EquivAutoGrid`` and add it to the document.

        EquivAutoGrid necessary when EquivSizing=TRUE, TRUE is is the normal case.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementequivautogrid
        """

class DaylightingDELightComplexFenestration:
    def __call__(
        self,
        name: str,
        /,
        *,
        complex_fenestration_type: str,
        building_surface_name: str,
        window_name: str,
        fenestration_rotation: float | None = 0,
    ) -> None:
        """Create a new ``Daylighting:DELight:ComplexFenestration`` and add it to the document.

        Used for DElight Complex Fenestration of all types

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingdelightcomplexfenestration
        """

class AirTerminalDualDuctVAVOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        outdoor_air_inlet_node_name: str,
        maximum_terminal_air_flow_rate: float | Literal["Autosize"],
        design_specification_outdoor_air_object_name: str,
        availability_schedule_name: str | None = ...,
        recirculated_air_inlet_node_name: str | None = ...,
        per_person_ventilation_rate_mode: Literal["CurrentOccupancy", "DesignOccupancy"] | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:DualDuct:VAV:OutdoorAir`` and add it to the document.

        Central air system terminal unit, dual duct, variable volume with special controls. One VAV duct is controlled to supply ventilation air and the other VAV duct is controlled to meet the zone cooling load.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminaldualductvavoutdoorair
        """

class AnyAirConditionerVariableRefrigerantFlowFluidTemperatureControlHR:
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
        rated_evaporative_capacity: float | Literal["Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_only_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_only_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_only_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_only_mode: float | None = 16,
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -20,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 43,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["ConstantTemp", "VariableTemp"]
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
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = 0,
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
        number_of_compressor_loading_index_entries: int | None = 2,
        loading_indices: Sequence[
            _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHRLoadingIndicesItem
            | _g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlHRLoadingIndicesGroup
        ] = ...,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR`` and add it to the document.

        This is a key object in the new physics based VRF Heat Recovery (HR) model applicable for Fluid Temperature Control. It describes the VRF HR system excluding the performance of indoor units. Indoor units are modeled separately in the ZoneHVAC:TerminalUnit:VariableRefrigerantFlow object

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflowfluidtemperaturecontrolhr
        """

class ChillerAbsorption:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_pumping_power: float | Literal["Autosize"],
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        condenser_outlet_node_name: str,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None = ...,
        coefficient_2_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None = ...,
        coefficient_3_of_the_hot_water_or_steam_use_part_load_ratio_curve: float | None = ...,
        coefficient_1_of_the_pump_electric_use_part_load_ratio_curve: float | None = ...,
        coefficient_2_of_the_pump_electric_use_part_load_ratio_curve: float | None = ...,
        coefficient_3_of_the_pump_electric_use_part_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        generator_inlet_node_name: str | None = ...,
        generator_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        generator_heat_source_type: Literal["HotWater", "Steam"] | None = "Steam",
        design_generator_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        degree_of_subcooling_in_steam_generator: float | None = 1,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``Chiller:Absorption`` and add it to the document.

        This indirect absorption chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Two sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerabsorption
        """

class AnyThermalStorageIceSimple:
    def __call__(
        self,
        name: str,
        /,
        *,
        ice_storage_type: Literal["IceOnCoilExternal", "IceOnCoilInternal"],
        capacity: float,
        inlet_node_name: str,
        outlet_node_name: str,
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Simple`` and add it to the document.

        This ice storage model is a simplified model It requires a setpoint placed on the Chilled Water Side Outlet Node It should be placed in the chilled water supply side outlet branch followed by a pipe. Use the PlantEquipmentOperation:ComponentSetpoint plant operation scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstorageicesimple
        """

class ExternalInterface:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        name_of_external_interface: Literal[
            "FunctionalMockupUnitExport", "FunctionalMockupUnitImport", "PtolemyServer"
        ],
    ) -> None:
        """Create a new ``ExternalInterface`` and add it to the document.

        This object activates the external interface of EnergyPlus. If the object ExternalInterface is present, then all ExtnernalInterface:* objects will receive their values from the BCVTB interface or from FMUs at each zone time step. If this object is not present, then the values of these objects will be fixed at the value declared in the 'initial value' field of the corresponding object, and a warning will be written to the EnergyPlus error file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterface
        """

class RefrigerationCondenserAirCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_effective_total_heat_rejection_rate_curve_name: str | None = ...,
        rated_subcooling_temperature_difference: float | None = 0,
        condenser_fan_speed_control_type: Literal["Fixed", "FixedLinear", "TwoSpeed", "VariableSpeed"] | None = "Fixed",
        rated_fan_power: float | None = 250,
        minimum_fan_air_flow_ratio: float | None = 0.2,
        air_inlet_node_name_or_zone_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        condenser_refrigerant_operating_charge_inventory: float | None = 0,
        condensate_receiver_refrigerant_inventory: float | None = 0,
        condensate_piping_refrigerant_inventory: float | None = 0,
    ) -> None:
        """Create a new ``Refrigeration:Condenser:AirCooled`` and add it to the document.

        Air cooled condenser for a refrigeration system (Refrigeration:System).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcondenseraircooled
        """

class FaultModelFoulingEvaporativeCooler:
    def __call__(
        self,
        name: str,
        /,
        *,
        evaporative_cooler_object_type: Literal["EvaporativeCooler:Indirect:WetCoil"],
        evaporative_cooler_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        fouling_factor: float | None = 1,
    ) -> None:
        """Create a new ``FaultModel:Fouling:EvaporativeCooler`` and add it to the document.

        This object describes the fouling fault of the wetted coil evaporative cooler

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelfoulingevaporativecooler
        """

class MeterCustomDecrement:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_meter_name: str,
        resource_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
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
        variable_details: Sequence[
            _g.MeterCustomDecrementVariableDetailsItem | _g.MeterCustomDecrementVariableDetailsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Meter:CustomDecrement`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:CustomDecrement cannot reference another Meter:CustomDecrement, either as the Source Meter Name or in the Key Name/Output Variable or Meter Name pairs, though it may reference a Meter:Custom.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#metercustomdecrement
        """
