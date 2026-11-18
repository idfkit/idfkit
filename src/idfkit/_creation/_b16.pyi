"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class WindowInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        outside_boundary_condition_object: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Window:Interzone`` and add it to the document.

        Allows for simplified entry of interzone windows (adjacent to other zones).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowinterzone
        """

class SurfacePropertyIncidentSolarMultiplier:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        surface_name: str,
        incident_solar_multiplier: float | None = 1,
        incident_solar_multiplier_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:IncidentSolarMultiplier`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyincidentsolarmultiplier
        """

class People:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["", "Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_floor_area: float | None = ...,
        floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["", "No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["", "AngleFactor", "EnclosureAveraged", "SurfaceWeighted"]
        | None = "EnclosureAveraged",
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "", "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        thermal_comfort_model_1_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_2_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_3_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_4_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_5_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_6_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_7_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        ankle_level_air_velocity_schedule_name: str | None = ...,
        cold_stress_temperature_threshold: float | None = 15.56,
        heat_stress_temperature_threshold: float | None = 30,
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        schedule_name: str,
        mass_transfer_coefficient: float | None = ...,
        henry_adsorption_constant_or_partition_coefficient: float | None = ...,
    ) -> None:
        """Create a new ``SurfaceContaminantSourceAndSink:Generic:BoundaryLayerDiffusion`` and add it to the document.

        Simulate generic contaminant source driven by the boundary layer diffusion controlled model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#surfacecontaminantsourceandsinkgenericboundarylayerdiffusion
        """

class ZoneEarthtube:
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
        earth_tube_model_type: Literal["", "Basic", "Vertical"] | None = "Basic",
        earth_tube_model_parameters: str | None = ...,
    ) -> None:
        """Create a new ``ZoneEarthtube`` and add it to the document.

        Earth Tube is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Earthtube=Edesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneearthtube
        """

class AnyCoilCoolingWaterToAirHeatPumpParameterEstimation:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        nominal_cooling_coil_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        load_side_outside_surface_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        refrigerant_type: str | None = "R22",
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:ParameterEstimation`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Parameter estimation model is a deterministic model that requires a consistent set of parameters to describe the operating conditions of the heat pump components.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpparameterestimation
        """

class AirLoopHVACUnitaryHeatOnly:
    def __call__(
        self,
        name: str,
        /,
        *,
        unitary_system_air_inlet_node_name: str,
        unitary_system_air_outlet_node_name: str,
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatOnly`` and add it to the document.

        Unitary system, heating-only with constant volume supply fan (continuous or cycling) and heating coil (gas, electric, hot water, or steam). Identical to AirLoopHVAC:Unitary:Furnace:HeatOnly.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatonly
        """

class AnyHeaderedPumpsVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        minimum_flow_rate_fraction: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None:
        """Create a new ``HeaderedPumps:VariableSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#headeredpumpsvariablespeed
        """

class HeaderedPumpsVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        minimum_flow_rate_fraction: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HeaderedPumps:VariableSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#headeredpumpsvariablespeed
        """

class AvailabilityManagerNightCycle:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_type: Literal[
            "",
            "CycleOnAny",
            "CycleOnAnyCoolingOrHeatingZone",
            "CycleOnAnyCoolingZone",
            "CycleOnAnyHeatingZone",
            "CycleOnAnyHeatingZoneFansOnly",
            "CycleOnAnyZoneFansOnly",
            "CycleOnControlZone",
            "StayOff",
        ]
        | None = "StayOff",
        thermostat_tolerance: float | None = 1,
        cycling_run_time_control_type: Literal["", "FixedRunTime", "Thermostat", "ThermostatWithMinimumRunTime"]
        | None = "FixedRunTime",
        cycling_run_time: float | None = 3600,
        control_zone_or_zone_list_name: str | None = ...,
        cooling_control_zone_or_zone_list_name: str | None = ...,
        heating_control_zone_or_zone_list_name: str | None = ...,
        heating_zone_fans_only_zone_or_zone_list_name: str | None = ...,
    ) -> None:
        """Create a new ``AvailabilityManager:NightCycle`` and add it to the document.

        Determines the availability of a loop or system: whether it is on or off. Depending on zone temperatures, overrides Schedules and forces system Fans on.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagernightcycle
        """

class AnyPhotovoltaicPerformanceSandia:
    def __call__(
        self,
        name: str,
        /,
        *,
        active_area: float | None = 1,
        number_of_cells_in_series: int | None = 1,
        number_of_cells_in_parallel: int | None = 1,
        short_circuit_current: float | None = ...,
        open_circuit_voltage: float | None = ...,
        current_at_maximum_power_point: float | None = ...,
        voltage_at_maximum_power_point: float | None = ...,
        sandia_database_parameter_aisc: float | None = ...,
        sandia_database_parameter_aimp: float | None = ...,
        sandia_database_parameter_c0: float | None = ...,
        sandia_database_parameter_c1: float | None = ...,
        sandia_database_parameter_bvoc0: float | None = ...,
        sandia_database_parameter_mbvoc: float | None = ...,
        sandia_database_parameter_bvmp0: float | None = ...,
        sandia_database_parameter_mbvmp: float | None = ...,
        diode_factor: float | None = ...,
        sandia_database_parameter_c2: float | None = ...,
        sandia_database_parameter_c3: float | None = ...,
        sandia_database_parameter_a0: float | None = ...,
        sandia_database_parameter_a1: float | None = ...,
        sandia_database_parameter_a2: float | None = ...,
        sandia_database_parameter_a3: float | None = ...,
        sandia_database_parameter_a4: float | None = ...,
        sandia_database_parameter_b0: float | None = ...,
        sandia_database_parameter_b1: float | None = ...,
        sandia_database_parameter_b2: float | None = ...,
        sandia_database_parameter_b3: float | None = ...,
        sandia_database_parameter_b4: float | None = ...,
        sandia_database_parameter_b5: float | None = ...,
        sandia_database_parameter_delta_tc_: float | None = ...,
        sandia_database_parameter_fd: float | None = ...,
        sandia_database_parameter_a: float | None = ...,
        sandia_database_parameter_b: float | None = ...,
        sandia_database_parameter_c4: float | None = ...,
        sandia_database_parameter_c5: float | None = ...,
        sandia_database_parameter_ix0: float | None = ...,
        sandia_database_parameter_ixx0: float | None = ...,
        sandia_database_parameter_c6: float | None = ...,
        sandia_database_parameter_c7: float | None = ...,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Sandia`` and add it to the document.

        Describes performance input data needed for specific makes and models of production PV panels using the empirical coefficients assembled by Sandia National Laboratory.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesandia
        """

class UtilityCostTariff:
    def __call__(
        self,
        name: str,
        /,
        *,
        output_meter_name: str,
        conversion_factor_choice: Literal[
            "CCF", "MCF", "MJ", "MMBtu", "Therm", "UserDefined", "gal", "kBtu", "kWh", "kgal", "m3"
        ]
        | None = ...,
        energy_conversion_factor: float | None = ...,
        demand_conversion_factor: float | None = ...,
        time_of_use_period_schedule_name: str | None = ...,
        season_schedule_name: str | None = ...,
        month_schedule_name: str | None = ...,
        demand_window_length: Literal["Day", "FullHour", "HalfHour", "QuarterHour", "Week"] | None = ...,
        monthly_charge_or_variable_name: float | str | None = ...,
        minimum_monthly_charge_or_variable_name: float | str | None = ...,
        real_time_pricing_charge_schedule_name: str | None = ...,
        customer_baseline_load_schedule_name: str | None = ...,
        group_name: str | None = ...,
        buy_or_sell: Literal["", "BuyFromUtility", "NetMetering", "SellToUtility"] | None = "BuyFromUtility",
    ) -> None:
        """Create a new ``UtilityCost:Tariff`` and add it to the document.

        Defines the name of a utility cost tariff, the type of tariff, and other details about the overall tariff. Each other object that is part of the tariff model references the tariff name. See UtilityCost:Charge:Simple, UtilityCost:Charge:Block, UtilityCost:Ratchet, UtilityCost:Qualify, UtilityCost:Variable and UtilityCost:Computation objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-tariff/#utilitycosttariff
        """

class AnyLifeCycleCostParameters:
    def __call__(
        self,
        name: str,
        /,
        *,
        discounting_convention: Literal["", "BeginningOfYear", "EndOfYear", "MidYear"] | None = "EndOfYear",
        inflation_approach: Literal["", "ConstantDollar", "CurrentDollar"] | None = "ConstantDollar",
        real_discount_rate: float | None = ...,
        nominal_discount_rate: float | None = ...,
        inflation: float | None = ...,
        base_date_month: Literal[
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
        base_date_year: int | None = ...,
        service_date_month: Literal[
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
        service_date_year: int | None = ...,
        length_of_study_period_in_years: int | None = ...,
        tax_rate: float | None = ...,
        depreciation_method: Literal[
            "",
            "ModifiedAcceleratedCostRecoverySystem-10year",
            "ModifiedAcceleratedCostRecoverySystem-15year",
            "ModifiedAcceleratedCostRecoverySystem-20year",
            "ModifiedAcceleratedCostRecoverySystem-3year",
            "ModifiedAcceleratedCostRecoverySystem-5year",
            "ModifiedAcceleratedCostRecoverySystem-7year",
            "None",
            "StraightLine-27year",
            "StraightLine-31year",
            "StraightLine-39year",
            "StraightLine-40year",
        ]
        | None = "None",
    ) -> None:
        """Create a new ``LifeCycleCost:Parameters`` and add it to the document.

        Provides inputs related to the overall life-cycle analysis. It establishes many of the assumptions used in computing the present value. It is important that when comparing the results of multiple simulations that the fields in the LifeCycleCost:Parameters objects are the same for all the simulations. When this object is present the tabular report file will contain the Life-Cycle Cost Report.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-parameters/#lifecyclecostparameters
        """

class OutputJSON:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        option_type: Literal["TimeSeries", "TimeSeriesAndTabular"],
        output_json: Literal["", "No", "Yes"] | None = "Yes",
        output_cbor: Literal["", "No", "Yes"] | None = "No",
        output_messagepack: Literal["", "No", "Yes"] | None = "No",
        unit_conversion_for_tabular_data: Literal[
            "",
            "InchPound",
            "InchPoundExceptElectricity",
            "JtoGJ",
            "JtoKWH",
            "JtoMJ",
            "None",
            "UseOutputControlTableStyle",
        ]
        | None = "UseOutputControlTableStyle",
        format_numeric_values_for_tabular_data: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Output:JSON`` and add it to the document.

        Output from EnergyPlus can be written to JSON format files.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputjson
        """
