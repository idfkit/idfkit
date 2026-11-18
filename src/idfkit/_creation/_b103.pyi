"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class CeilingInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Ceiling:Interzone`` and add it to the document.

        Allows for simplified entry of ceilings using adjacent zone (interzone) heat transfer - adjacent surface should be a floor

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#ceilinginterzone
        """

class ShadingBuilding:
    def __call__(
        self,
        name: str,
        /,
        *,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Shading:Building`` and add it to the document.

        used for shading elements such as trees, other buildings, parts of this building not being modeled these items are relative to the current building and would move with relative geometry

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zones-and-surfaces/#shadingbuilding
        """

class GroundHeatTransferSlabInsulation:
    def __call__(
        self,
        /,
        *,
        rins_r_value_of_under_slab_insulation: float | None = 0,
        dins_width_of_strip_of_under_slab_insulation: float | None = 0,
        rvins_r_value_of_vertical_insulation: float | None = 0,
        zvins_depth_of_vertical_insulation: float | None = 0,
        ivins_flag_is_there_vertical_insulation: Literal[0, 1] | None = 0,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:Insulation`` and add it to the document.

        This object supplies the information about insulation used around the slab. There are two possible configurations: under the slab or vertical insulation around the slab.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabinsulation
        """

class ElectricEquipmentITEAirCooledDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        cpu_power_input_function_of_loading_and_air_temperature_curve_name: str,
        design_fan_air_flow_rate_per_power_input: float,
        air_flow_function_of_loading_and_air_temperature_curve_name: str,
        fan_power_input_function_of_flow_curve_name: str,
        air_flow_calculation_method: Literal["FlowControlWithApproachTemperatures", "FlowFromSystem"]
        | None = "FlowFromSystem",
        design_power_input_calculation_method: Literal["EquipmentLevel", "Watts/Area"] | None = "EquipmentLevel",
        watts_per_unit: float | None = ...,
        watts_per_floor_area: float | None = ...,
        design_fan_power_input_fraction: float | None = 0,
        design_entering_air_temperature: float | None = 15,
        environmental_class: Literal["A1", "A2", "A3", "A4", "B", "C", "H1", "None"] | None = "None",
        air_inlet_connection_type: Literal["AdjustedSupply", "RoomAirModel", "ZoneAirNode"] | None = "AdjustedSupply",
        design_recirculation_fraction: float | None = 0,
        recirculation_function_of_loading_and_supply_temperature_curve_name: str | None = ...,
        design_electric_power_supply_efficiency: float | None = 1,
        electric_power_supply_efficiency_function_of_part_load_ratio_curve_name: str | None = ...,
        fraction_of_electric_power_supply_losses_to_zone: float | None = 1,
        supply_temperature_difference: float | None = ...,
        supply_temperature_difference_schedule: str | None = ...,
        return_temperature_difference: float | None = ...,
        return_temperature_difference_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ElectricEquipment:ITE:AirCooled:Definition`` and add it to the document.

        Performance characteristics for ElectricEquipment:ITE:AirCooled:Instance. Defines power, airflow, and efficiency as functions of loading and temperature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#electricequipmentiteaircooleddefinition
        """

class AirflowNetworkDistributionNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_name_or_node_name: str | None = ...,
        component_object_type_or_node_type: Literal[
            "AirLoopHVAC:OutdoorAirSystem",
            "AirLoopHVAC:ZoneMixer",
            "AirLoopHVAC:ZoneSplitter",
            "OAMixerOutdoorAirStreamNode",
            "Other",
            "OutdoorAir:Node",
            "OutdoorAir:NodeList",
            "Zone",
        ]
        | None = "Other",
        node_height: float | None = 0,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Node`` and add it to the document.

        This object represents an air distribution node in the AirflowNetwork model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributionnode
        """

class AnyZoneControlHumidistat:
    def __call__(self, name: str, /, *, narrow_with_as_version_first: Never, zone_name: str) -> None:
        """Create a new ``ZoneControl:Humidistat`` and add it to the document.

        Specifies zone relative humidity setpoint schedules for humidifying and dehumidifying.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolhumidistat
        """

class CoilHeatingDXSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_capacity_function_of_temperature_curve_name: str,
        heating_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = 0,
        region_number_for_calculating_hspf: int | None = 4,
        evaporator_air_inlet_node_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), single-speed, with defrost controls.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxsinglespeed
        """

class AnyAirLoopHVACOutdoorAirSystem:
    def __call__(self, name: str, /, *, controller_list_name: str, outdoor_air_equipment_list_name: str) -> None:
        """Create a new ``AirLoopHVAC:OutdoorAirSystem`` and add it to the document.

        Outdoor air subsystem for an AirLoopHVAC. Includes an outdoor air mixing box and optional outdoor air conditioning equipment such as heat recovery, preheat, and precool coils. From the perspective of the primary air loop the outdoor air system is treated as a single component.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#airloophvacoutdoorairsystem
        """

class BranchList:
    def __call__(
        self, name: str, /, *, branches: Sequence[_g.BranchListBranchesItem | _g.BranchListBranchesGroup] = ...
    ) -> None:
        """Create a new ``BranchList`` and add it to the document.

        Branches MUST be listed in Flow order: Inlet branch, then parallel branches, then Outlet branch. Branches are simulated in the order listed. Branch names cannot be duplicated within a single branch list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#branchlist
        """

class AnyChillerElectricEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_capacity: float | Literal["Autosize"],
        reference_cop: float,
        cooling_capacity_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        reference_leaving_chilled_water_temperature: float | None = 6.67,
        reference_entering_condenser_fluid_temperature: float | None = 29.4,
        reference_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        reference_condenser_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.2,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "WaterCooled",
        condenser_fan_power_ratio: float | None = 0,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Chiller:Electric:EIR`` and add it to the document.

        This chiller model is the empirical model from the DOE-2 building Energy simulation program. Chiller performance at off-reference conditions is modeled using three polynomial equations. Three curves objects are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerelectriceir
        """

class ChillerHeaterPerformanceElectricEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_cooling_mode_evaporator_capacity: float | Literal["Autosize"],
        reference_cooling_mode_cop: float,
        cooling_mode_cooling_capacity_function_of_temperature_curve_name: str,
        cooling_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        cooling_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        heating_mode_cooling_capacity_function_of_temperature_curve_name: str,
        heating_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        heating_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        reference_cooling_mode_leaving_chilled_water_temperature: float | None = 6.67,
        reference_cooling_mode_entering_condenser_fluid_temperature: float | None = 29.44,
        reference_cooling_mode_leaving_condenser_water_temperature: float | None = 35,
        reference_heating_mode_cooling_capacity_ratio: float | None = 0.75,
        reference_heating_mode_cooling_power_input_ratio: float | None = 1.38,
        reference_heating_mode_leaving_chilled_water_temperature: float | None = 6.67,
        reference_heating_mode_leaving_condenser_water_temperature: float | None = 49,
        reference_heating_mode_entering_condenser_fluid_temperature: float | None = 29.44,
        heating_mode_entering_chilled_water_temperature_low_limit: float | None = 12.22,
        chilled_water_flow_mode_type: Literal["ConstantFlow", "VariableFlow"] | None = "ConstantFlow",
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_hot_water_flow_rate: float | None = 0,
        compressor_motor_efficiency: float | None = 1,
        cooling_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "EnteringCondenser",
        cooling_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        heating_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "LeavingCondenser",
        heating_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``ChillerHeaterPerformance:Electric:EIR`` and add it to the document.

        This chiller model is a generic chiller-heater where the cooling mode performance is a function of condenser entering or leaving fluid temperature and the heating mode performance is typically a function of condenser leaving fluid temperature. Performance at off-reference conditions is modeled using three polynomial equations per mode. Six curve objects are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerheaterperformanceelectriceir
        """
