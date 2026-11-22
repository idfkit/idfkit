"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
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
        validate: bool = True,
    ) -> None:
        """Create a new ``Exterior:FuelEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-exterior-energy-use-equipment/#exteriorfuelequipment
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
        multipliers: Sequence[
            _g.LifeCycleCostUseAdjustmentMultipliersItem | _g.LifeCycleCostUseAdjustmentMultipliersGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``LifeCycleCost:UseAdjustment`` and add it to the document.

        Used by advanced users to adjust the energy or water use costs for future years. This should not be used for compensating for inflation but should only be used to increase the costs of energy or water based on assumed changes to the actual usage, such as anticipated changes in the future function of the building. The adjustments begin at the start of the service period.

        ``multipliers`` takes the extensible groups in order, one dict per group:

        ```python
        doc["LifeCycleCost:UseAdjustment"].add(
            "LifeCycleCost UseAdjustment 1",
            resource="Coal",
            multipliers=[
                {"year_multiplier": 0.0},
                {"year_multiplier": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/energyplus-economics/lifecyclecost-useadjustment/#lifecyclecostuseadjustment
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
        pipe_segments: Sequence[
            _g.PipingSystemUndergroundPipeCircuitPipeSegmentsItem
            | _g.PipingSystemUndergroundPipeCircuitPipeSegmentsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PipingSystem:Underground:PipeCircuit`` and add it to the document.

        The pipe circuit object in an underground piping system. This object is simulated within an underground piping domain object and connected on a branch on a plant loop.

        ``pipe_segments`` takes the extensible groups in order, one dict per group:

        ```python
        doc["PipingSystem:Underground:PipeCircuit"].add(
            "PipingSystem Underground PipeCircuit 1",
            pipe_thermal_conductivity=1.0,
            pipe_density=1.0,
            pipe_specific_heat=1.0,
            pipe_inner_diameter=1.0,
            pipe_outer_diameter=1.0,
            design_flow_rate=1.0,
            circuit_inlet_node="Circuit Inlet Node 1",
            circuit_outlet_node="Circuit Outlet Node 1",
            radial_thickness_of_inner_radial_near_pipe_mesh_region=1.0,
            number_of_pipe_segments_entered_for_this_pipe_circuit=1.0,
            pipe_segments=[
                {"pipe_segment": "Pipe Segment 1"},
                {"pipe_segment": "Pipe Segment 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-node-branch-management/#pipingsystemundergroundpipecircuit
        """

class HVACTemplateSystemVRF_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = "Autosize",
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
        gross_rated_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = 30,
        vertical_height_used_for_piping_correction_factor: float | None = 10,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = 30,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: float | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_condenser_volume_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal[
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
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:System:VRF`` and add it to the document.

        Variable refrigerant flow (VRF) heat pump condensing unit. Serves one or more VRF zone terminal units (HVACTemplate:Zone:VRF).

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
        variable_details: Sequence[_g.MeterCustomVariableDetailsItem | _g.MeterCustomVariableDetailsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Meter:Custom`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:Custom cannot reference another Meter:Custom.

        ``variable_details`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Meter:Custom"].add(
            "Meter Custom 1",
            variable_details=[
                {"key_name": "Key 1", "output_variable_or_meter_name": "Output Variable or Meter 1"},
                {"key_name": "Key 2", "output_variable_or_meter_name": "Output Variable or Meter 2"},
            ],
        )
        ```

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
        gross_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
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
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Speed`` and add it to the document.

        DX cooling coil performance for a single speed within a single operating mode.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitspeed
        """
