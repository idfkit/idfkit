"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class People_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["", "Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_zone_floor_area: float | None = ...,
        zone_floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["", "No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["", "AngleFactor", "SurfaceWeighted", "ZoneAveraged"]
        | None = "ZoneAveraged",
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "", "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        thermal_comfort_model_1_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_2_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_3_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_4_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
        thermal_comfort_model_5_type: Literal["AdaptiveASH55", "AdaptiveCEN15251", "Fanger", "KSU", "Pierce"]
        | None = ...,
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class HeaderedPumpsConstantSpeed_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: float | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None:
        """Create a new ``HeaderedPumps:ConstantSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-pumps/#headeredpumpsconstantspeed
        """

class ChillerElectricEIR_v8_9_to_v24_1:
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
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "WaterCooled",
        condenser_fan_power_ratio: float | None = 0,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-plant-equipment/#chillerelectriceir
        """

class ZoneMixing_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        source_zone_name: str,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_zone_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_zone_temperature_schedule_name: str | None = ...,
        maximum_zone_temperature_schedule_name: str | None = ...,
        minimum_source_zone_temperature_schedule_name: str | None = ...,
        maximum_source_zone_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneMixing`` and add it to the document.

        ZoneMixing is a simple air exchange from one zone to another. Note that this statement only affects the energy balance of the 'receiving' zone and will not produce any effect on the 'source' zone. Mixing statements can be complementary and include multiple zones, but the balancing of flows between zones is left to the user's discretion.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zonemixing
        """

class ZoneEarthtube_v8_9_to_v23_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        design_flow_rate: float,
        minimum_zone_temperature_when_cooling: float,
        maximum_zone_temperature_when_heating: float,
        delta_temperature: float,
        average_soil_surface_temperature: float,
        amplitude_of_soil_surface_temperature: float,
        phase_constant_of_soil_surface_temperature: float,
        earthtube_type: Literal["", "Exhaust", "Intake", "Natural"] | None = "Natural",
        fan_pressure_rise: float | None = 0,
        fan_total_efficiency: float | None = 1,
        pipe_radius: float | None = 1,
        pipe_thickness: float | None = 0.2,
        pipe_length: float | None = 15,
        pipe_thermal_conductivity: float | None = 200,
        pipe_depth_under_ground_surface: float | None = 3,
        soil_condition: Literal["", "HeavyAndDamp", "HeavyAndDry", "HeavyAndSaturated", "LightAndDry"]
        | None = "HeavyAndDamp",
        constant_term_flow_coefficient: float | None = 1,
        temperature_term_flow_coefficient: float | None = 0,
        velocity_term_flow_coefficient: float | None = 0,
        velocity_squared_term_flow_coefficient: float | None = 0,
    ) -> None:
        """Create a new ``ZoneEarthtube`` and add it to the document.

        Earth Tube is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Earthtube=Edesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-airflow/#zoneearthtube
        """

class ComfortViewFactorAngles_v8_9_to_v9_5:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_name: str | None = ...,
        surface_1_name: str | None = ...,
        angle_factor_1: float | None = ...,
        surface_2_name: str | None = ...,
        angle_factor_2: float | None = ...,
        surface_3_name: str | None = ...,
        angle_factor_3: float | None = ...,
        surface_4_name: str | None = ...,
        angle_factor_4: float | None = ...,
        surface_5_name: str | None = ...,
        angle_factor_5: float | None = ...,
        surface_6_name: str | None = ...,
        angle_factor_6: float | None = ...,
        surface_7_name: str | None = ...,
        angle_factor_7: float | None = ...,
        surface_8_name: str | None = ...,
        angle_factor_8: float | None = ...,
        surface_9_name: str | None = ...,
        angle_factor_9: float | None = ...,
        surface_10_name: str | None = ...,
        angle_factor_10: float | None = ...,
        surface_11_name: str | None = ...,
        angle_factor_11: float | None = ...,
        surface_12_name: str | None = ...,
        angle_factor_12: float | None = ...,
        surface_13_name: str | None = ...,
        angle_factor_13: float | None = ...,
        surface_14_name: str | None = ...,
        angle_factor_14: float | None = ...,
        surface_15_name: str | None = ...,
        angle_factor_15: float | None = ...,
        surface_16_name: str | None = ...,
        angle_factor_16: float | None = ...,
        surface_17_name: str | None = ...,
        angle_factor_17: float | None = ...,
        surface_18_name: str | None = ...,
        angle_factor_18: float | None = ...,
        surface_19_name: str | None = ...,
        angle_factor_19: float | None = ...,
        surface_20_name: str | None = ...,
        angle_factor_20: float | None = ...,
    ) -> None:
        """Create a new ``ComfortViewFactorAngles`` and add it to the document.

        Used to specify radiant view factors for thermal comfort calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#comfortviewfactorangles
        """
