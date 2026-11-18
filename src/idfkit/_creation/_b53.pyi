"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyWindowMaterialGasMixture:
    def __call__(
        self,
        name: str,
        /,
        *,
        thickness: float,
        number_of_gases_in_mixture: int,
        gas_1_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_1_fraction: float,
        gas_2_type: Literal["Air", "Argon", "Krypton", "Xenon"],
        gas_2_fraction: float,
        gas_3_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_3_fraction: float | None = ...,
        gas_4_type: Literal["Air", "Argon", "Krypton", "Xenon"] | None = ...,
        gas_4_fraction: float | None = ...,
    ) -> None:
        """Create a new ``WindowMaterial:GasMixture`` and add it to the document.

        Gas mixtures that are used in Windows or Glass Doors

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialgasmixture
        """

class AnyConstructionPropertyInternalHeatSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        thermal_source_present_after_layer_number: int,
        temperature_calculation_requested_after_layer_number: int,
        dimensions_for_the_ctf_calculation: int,
        tube_spacing: float,
        construction_name: str | None = ...,
        two_dimensional_temperature_calculation_position: float | None = 0,
    ) -> None:
        """Create a new ``ConstructionProperty:InternalHeatSource`` and add it to the document.

        Internal heat source to be attached to a construction layer

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionpropertyinternalheatsource
        """

class WallExterior:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Exterior`` and add it to the document.

        Allows for simplified entry of exterior walls. View Factor to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#wallexterior
        """

class GroundHeatTransferBasementEquivSlab:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        apratio_the_area_to_perimeter_ratio_for_this_slab: float,
        equivsizing_flag: Literal["FALSE", "TRUE"],
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:EquivSlab`` and add it to the document.

        Using an equivalent slab allows non-rectangular shapes to be modeled accurately. The simulation default should be EquivSizing=True

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementequivslab
        """

class RoomAirTemperaturePatternUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        pattern_control_schedule_name: str,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:UserDefined`` and add it to the document.

        Used to explicitly define temperature patterns that are to be applied to the mean air temperature within a thermal zone. Used with RoomAirModelType = UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternuserdefined
        """

class GasEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
    ) -> None:
        """Create a new ``GasEquipment:Definition`` and add it to the document.

        Defines the physical characteristics (design level and heat gain fractions) for gas equipment. Referenced by one or more GasEquipment:Instance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#gasequipmentdefinition
        """

class ElectricEquipmentITEAirCooledInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        electricequipment_ite_aircooled_definition_name: str,
        zone_or_space_name: str,
        multiplier: float | None = 1,
        design_power_input_schedule_name: str | None = ...,
        cpu_loading_schedule_name: str | None = ...,
        air_inlet_room_air_model_node_name: str | None = ...,
        air_outlet_room_air_model_node_name: str | None = ...,
        supply_air_node_name: str | None = ...,
        cpu_end_use_subcategory: str | None = "ITE-CPU",
        fan_end_use_subcategory: str | None = "ITE-Fans",
        electric_power_supply_end_use_subcategory: str | None = "ITE-UPS",
    ) -> None:
        """Create a new ``ElectricEquipment:ITE:AirCooled:Instance`` and add it to the document.

        This object describes air-cooled electric information technology equipment (ITE) which has variable power consumption as a function of loading and temperature. The performance characteristics are given by the referenced ElectricEquipment:ITE:AirCooled:Definition object. If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#electricequipmentiteaircooledinstance
        """

class AirflowNetworkMultiZoneZone:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        ventilation_control_mode: Literal[
            "", "ASHRAE55Adaptive", "CEN15251Adaptive", "Constant", "Enthalpy", "NoVent", "Temperature"
        ]
        | None = "NoVent",
        ventilation_control_zone_temperature_setpoint_schedule_name: str | None = ...,
        minimum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor: float | None = 100,
        indoor_and_outdoor_enthalpy_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor: float | None = 300000,
        venting_availability_schedule_name: str | None = ...,
        single_sided_wind_pressure_coefficient_algorithm: Literal["", "Advanced", "Standard"] | None = "Standard",
        facade_width: float | None = 10,
        occupant_ventilation_control_name: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Zone`` and add it to the document.

        This object is used to simultaneously control a thermal zone's window and door openings, both exterior and interior.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonezone
        """

class SpaceHVACZoneReturnMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_return_air_node_name: str,
        spaces: Sequence[_g.SpaceHVACZoneReturnMixerSpacesItem | _g.SpaceHVACZoneReturnMixerSpacesGroup] = ...,
    ) -> None:
        """Create a new ``SpaceHVAC:ZoneReturnMixer`` and add it to the document.

        Mixes the return airflow from one or more Spaces into a zone return node. All spaces in the zone must also have a SpaceHVAC:EquipmentConnections object. Used only when ZoneAirHeatBalanceAlgorithm 'Do Space Heat Balance for Simulation' is Yes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#spacehvaczonereturnmixer
        """

class AnyCoilSystemCoolingDXHeatExchangerAssisted:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
            "HeatExchanger:Desiccant:BalancedFlow",
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "Coil:Cooling:DX:VariableSpeed"],
        cooling_coil_name: str,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX:HeatExchangerAssisted`` and add it to the document.

        Virtual component consisting of a direct expansion (DX) cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energy to reheat the supply air leaving the cooling coil. This heat exchange process improves the latent removal performance of the cooling coil (lower sensible heat ratio).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdxheatexchangerassisted
        """

class AirConditionerVariableRefrigerantFlow:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_terminal_unit_list_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_condenser_inlet_node_temperature_in_cooling_mode: float | None = -6,
        maximum_condenser_inlet_node_temperature_in_cooling_mode: float | None = 43,
        cooling_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_capacity_ratio_boundary_curve_name: str | None = ...,
        cooling_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_boundary_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        cooling_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        cooling_combination_ratio_correction_factor_curve_name: str | None = ...,
        cooling_part_load_fraction_correlation_curve_name: str | None = ...,
        gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_condenser_inlet_node_temperature_in_heating_mode: float | None = -20,
        maximum_condenser_inlet_node_temperature_in_heating_mode: float | None = 16,
        heating_capacity_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_capacity_ratio_boundary_curve_name: str | None = ...,
        heating_capacity_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_low_temperature_curve_name: str | None = ...,
        heating_energy_input_ratio_boundary_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_temperature_curve_name: str | None = ...,
        heating_performance_curve_outdoor_temperature_type: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_energy_input_ratio_modifier_function_of_low_part_load_ratio_curve_name: str | None = ...,
        heating_energy_input_ratio_modifier_function_of_high_part_load_ratio_curve_name: str | None = ...,
        heating_combination_ratio_correction_factor_curve_name: str | None = ...,
        heating_part_load_fraction_correlation_curve_name: str | None = ...,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = ...,
        vertical_height_used_for_piping_correction_factor: float | None = ...,
        piping_correction_factor_for_length_in_cooling_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_cooling_mode_coefficient: float | None = 0,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = ...,
        piping_correction_factor_for_length_in_heating_mode_curve_name: str | None = ...,
        piping_correction_factor_for_height_in_heating_mode_coefficient: float | None = 0,
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
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        water_condenser_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        supply_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal[
            "",
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
        minimum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None = ...,
        maximum_condenser_inlet_node_temperature_in_heat_recovery_mode: float | None = ...,
        heat_recovery_cooling_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_capacity_fraction: float | None = 0.5,
        heat_recovery_cooling_capacity_time_constant: float | None = 0.15,
        heat_recovery_cooling_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        heat_recovery_heating_capacity_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0.15,
        heat_recovery_heating_energy_modifier_curve_name: str | None = ...,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
    ) -> None:
        """Create a new ``AirConditioner:VariableRefrigerantFlow`` and add it to the document.

        Variable refrigerant flow (VRF) air-to-air heat pump condensing unit (includes one or more electric compressors and outdoor fan). Serves one or more VRF zone terminal units. See ZoneHVAC:TerminalUnit:VariableRefrigerantFlow and ZoneTerminalUnitList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#airconditionervariablerefrigerantflow
        """

class AnyHeatPumpWaterToWaterEquationFitCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_cooling_capacity: float | Literal["Autosize"],
        reference_cooling_power_consumption: float | Literal["Autosize"],
        reference_coefficient_of_performance: float | None = 8,
        sizing_factor: float | None = 1,
        companion_heating_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Cooling`` and add it to the document.

        simple water-water heat pump curve-fit model

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitcooling
        """

class ZoneHVACRefrigerationChillerSet:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        chillers: Sequence[
            _g.ZoneHVACRefrigerationChillerSetChillersItem | _g.ZoneHVACRefrigerationChillerSetChillersGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:RefrigerationChillerSet`` and add it to the document.

        Works in conjunction with one or multiple air chillers, compressor racks, refrigeration systems, or refrigeration secondary system objects to simulate the performance of a group of air chillers cooling a single zone. The chiller set model passes information about the zone conditions to determine the performance of individual chiller coils within the set, thus providing the sensible and latent heat exchange with the zone environment.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacrefrigerationchillerset
        """

class GeneratorFuelCell:
    def __call__(
        self,
        name: str,
        /,
        *,
        power_module_name: str,
        air_supply_name: str,
        fuel_supply_name: str,
        water_supply_name: str,
        auxiliary_heater_name: str,
        heat_exchanger_name: str,
        electrical_storage_name: str,
        inverter_name: str,
        stack_cooler_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell`` and add it to the document.

        This generator model is the FC model from IEA Annex 42

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcell
        """

class OutputDebuggingData:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        report_debugging_data: Literal["", "No", "Yes"] | None = "No",
        report_during_warmup: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``Output:DebuggingData`` and add it to the document.

        switch eplusout.dbg file on or off

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#outputdebuggingdata
        """
