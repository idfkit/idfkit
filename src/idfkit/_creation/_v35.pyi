"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class FloorAdiabatic_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Floor:Adiabatic`` and add it to the document.

        Allows for simplified entry of exterior floors ignoring ground contact or interior floors. View Factor to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#flooradiabatic
        """

class ZoneInfiltrationDesignFlowRate_v22_2_to_v24_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str | None = ...,
        design_flow_rate_calculation_method: Literal[
            "AirChanges/Hour", "Flow/Area", "Flow/ExteriorArea", "Flow/ExteriorWallArea", "Flow/Zone"
        ]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_floor_area: float | None = ...,
        flow_rate_per_exterior_surface_area: float | None = ...,
        air_changes_per_hour: float | None = ...,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneInfiltration:DesignFlowRate`` and add it to the document.

        Infiltration is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Infiltration=Idesign * FSchedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.2/io-reference/overview/group-airflow/#zoneinfiltrationdesignflowrate
        """

class CoilCoolingDXVariableSpeed_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_total_cooling_capacity: float,
        speed_1_reference_unit_gross_rated_sensible_heat_ratio: float,
        speed_1_reference_unit_gross_rated_cooling_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        speed_1_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_1_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_2_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_3_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_4_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_5_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_6_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_7_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_condenser_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_8_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_9_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_10_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:VariableSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), variable-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxvariablespeed
        """

class ChillerHeaterPerformanceElectricEIR_v8_9_to_v26_1:
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
        condenser_type: Literal["AirCooled", "WaterCooled"] | None = "WaterCooled",
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
        validate: bool = True,
    ) -> None:
        """Create a new ``ChillerHeaterPerformance:Electric:EIR`` and add it to the document.

        This chiller model is a generic chiller-heater where the cooling mode performance is a function of condenser entering or leaving fluid temperature and the heating mode performance is typically a function of condenser leaving fluid temperature. Performance at off-reference conditions is modeled using three polynomial equations per mode. Six curve objects are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-plant-equipment/#chillerheaterperformanceelectriceir
        """

class LifeCycleCostUsePriceEscalation_v8_9_to_v9_2:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: str,
        escalation_start_year: float | None = ...,
        escalation_start_month: Literal[
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
        escalations: Sequence[
            _g.LifeCycleCostUsePriceEscalationEscalationsItem | _g.LifeCycleCostUsePriceEscalationEscalationsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``LifeCycleCost:UsePriceEscalation`` and add it to the document.

        Life cycle cost escalation factors. The values for this object may be found in the annual supplement to NIST Handbook 135 in Tables Ca-1 to Ca-5 and are included in an EnergyPlus dataset file.

        ``escalations`` takes the extensible groups in order, one dict per group:

        ```python
        doc["LifeCycleCost:UsePriceEscalation"].add(
            lcc_price_escalation_name="LCC Price Escalation Name",
            resource="Resource",
            escalations=[
                {"year_escalation": 0.0},
                {"year_escalation": 0.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/energyplus-economics/lifecyclecost-usepriceescalation/#lifecyclecostusepriceescalation
        """

class ElectricLoadCenterStorageLiIonNMCBattery_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_cells_in_series: float,
        number_of_strings_in_parallel: float,
        battery_mass: float,
        battery_surface_area: float,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        lifetime_model: Literal["KandlerSmith", "None"] | None = "KandlerSmith",
        initial_fractional_state_of_charge: float | None = 0.5,
        dc_to_dc_charging_efficiency: float | None = 0.95,
        battery_specific_heat_capacity: float | None = 1500,
        heat_transfer_coefficient_between_battery_and_ambient: float | None = 7.5,
        fully_charged_cell_voltage: float | None = 4.2,
        cell_voltage_at_end_of_exponential_zone: float | None = 3.53,
        cell_voltage_at_end_of_nominal_zone: float | None = 3.342,
        default_nominal_cell_voltage: float | None = 3.342,
        fully_charged_cell_capacity: float | None = 3.2,
        fraction_of_cell_capacity_removed_at_the_end_of_exponential_zone: float | None = 0.8075,
        fraction_of_cell_capacity_removed_at_the_end_of_nominal_zone: float | None = 0.976875,
        charge_rate_at_which_voltage_vs_capacity_curve_was_generated: float | None = 1,
        battery_cell_internal_electrical_resistance: float | None = 0.09,
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:LiIonNMCBattery`` and add it to the document.

        Uses Lithium Ion NMC model to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstorageliionnmcbattery
        """
