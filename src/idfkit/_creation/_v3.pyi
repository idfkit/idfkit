"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class EnergyManagementSystemProgramCallingManager_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        energyplus_model_calling_point: Literal[
            "AfterComponentInputReadIn",
            "AfterNewEnvironmentWarmUpIsComplete",
            "AfterPredictorAfterHVACManagers",
            "AfterPredictorBeforeHVACManagers",
            "BeginNewEnvironment",
            "BeginTimestepBeforePredictor",
            "EndOfSystemSizing",
            "EndOfSystemTimestepAfterHVACReporting",
            "EndOfSystemTimestepBeforeHVACReporting",
            "EndOfZoneSizing",
            "EndOfZoneTimestepAfterZoneReporting",
            "EndOfZoneTimestepBeforeZoneReporting",
            "InsideHVACSystemIterationLoop",
            "UnitarySystemSizing",
            "UserDefinedComponentModel",
        ]
        | None = ...,
        programs: list[_g.EnergyManagementSystemProgramCallingManagerProgramsItem] = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:ProgramCallingManager`` and add it to the document.

        Input EMS program. a program needs a name a description of when it should be called and then lines of program code for EMS Runtime language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogramcallingmanager
        """

class LifeCycleCostParameters_v8_9_to_v22_1:
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
        base_date_year: float | None = ...,
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
        service_date_year: float | None = ...,
        length_of_study_period_in_years: float | None = ...,
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

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/lifecyclecost-parameters/#lifecyclecostparameters
        """

class ZoneControlHumidistat_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        humidifying_relative_humidity_setpoint_schedule_name: str,
        dehumidifying_relative_humidity_setpoint_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneControl:Humidistat`` and add it to the document.

        Specifies zone relative humidity setpoint schedules for humidifying and dehumidifying.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-zone-controls-thermostats/#zonecontrolhumidistat
        """

class Material_v8_9_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thickness: float,
        conductivity: float,
        density: float,
        specific_heat: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
    ) -> None:
        """Create a new ``Material`` and add it to the document.

        Regular materials described with full set of thermal properties

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-surface-construction-elements/#material
        """

class CoilHeatingElectricMultiStage_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: float,
        stage_1_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        stage_2_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Electric:MultiStage`` and add it to the document.

        Electric heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingelectricmultistage
        """

class OutputIlluminanceMap_v22_2_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        z_height: float | None = 0,
        x_minimum_coordinate: float | None = 0,
        x_maximum_coordinate: float | None = 1,
        number_of_x_grid_points: int | None = 2,
        y_minimum_coordinate: float | None = 0,
        y_maximum_coordinate: float | None = 1,
        number_of_y_grid_points: int | None = 2,
    ) -> None:
        """Create a new ``Output:IlluminanceMap`` and add it to the document.

        reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-daylighting/#outputilluminancemap
        """

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
    ) -> None:
        """Create a new ``Floor:Adiabatic`` and add it to the document.

        Allows for simplified entry of exterior floors ignoring ground contact or interior floors. View Factor to Ground is automatically calculated.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

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
            "", "AirChanges/Hour", "Flow/Area", "Flow/ExteriorArea", "Flow/ExteriorWallArea", "Flow/Zone"
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
    ) -> None:
        """Create a new ``ZoneInfiltration:DesignFlowRate`` and add it to the document.

        Infiltration is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Infiltration=Idesign * FSchedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.2/io-reference/overview/group-airflow/#zoneinfiltrationdesignflowrate
        """

class EnergyManagementSystemMeteredOutputVariable_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "Steam",
            "WaterUse",
            "WellWaterDrawn",
        ],
        group_type: Literal["Building", "HVAC", "Plant", "System"],
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ],
        ems_program_or_subroutine_name: str | None = ...,
        end_use_subcategory: str | None = ...,
        units: str | None = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:MeteredOutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from an Erl variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemmeteredoutputvariable
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
        | Literal["", "Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
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
    ) -> None:
        """Create a new ``Coil:Cooling:DX:VariableSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), variable-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxvariablespeed
        """

class HeatExchangerFluidToFluid_v8_9_to_v25_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        loop_demand_side_inlet_node_name: str,
        loop_demand_side_outlet_node_name: str,
        loop_demand_side_design_flow_rate: float | Literal["Autosize"],
        loop_supply_side_inlet_node_name: str,
        loop_supply_side_outlet_node_name: str,
        loop_supply_side_design_flow_rate: float | Literal["Autosize"],
        heat_exchanger_u_factor_times_area_value: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heat_exchange_model_type: Literal[
            "",
            "CounterFlow",
            "CrossFlowBothMixed",
            "CrossFlowBothUnMixed",
            "CrossFlowSupplyMixedDemandUnMixed",
            "CrossFlowSupplyUnMixedDemandMixed",
            "Ideal",
            "ParallelFlow",
        ]
        | None = "Ideal",
        control_type: Literal[
            "",
            "CoolingDifferentialOnOff",
            "CoolingSetpointModulated",
            "CoolingSetpointOnOff",
            "CoolingSetpointOnOffWithComponentOverride",
            "DualDeadbandSetpointModulated",
            "DualDeadbandSetpointOnOff",
            "HeatingSetpointModulated",
            "HeatingSetpointOnOff",
            "OperationSchemeModulated",
            "OperationSchemeOnOff",
            "UncontrolledOn",
        ]
        | None = "UncontrolledOn",
        heat_exchanger_setpoint_node_name: str | None = ...,
        minimum_temperature_difference_to_activate_heat_exchanger: float | None = 0.01,
        heat_transfer_metering_end_use_type: Literal[
            "",
            "FreeCooling",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "LoopToLoop",
        ]
        | None = "LoopToLoop",
        component_override_loop_supply_side_inlet_node_name: str | None = ...,
        component_override_loop_demand_side_inlet_node_name: str | None = ...,
        component_override_cooling_control_temperature_mode: Literal[
            "", "DryBulbTemperature", "Loop", "WetBulbTemperature"
        ]
        | None = "Loop",
        sizing_factor: float | None = 1,
        operation_minimum_temperature_limit: float | None = ...,
        operation_maximum_temperature_limit: float | None = ...,
    ) -> None:
        """Create a new ``HeatExchanger:FluidToFluid`` and add it to the document.

        A fluid/fluid heat exchanger designed to couple the supply side of one loop to the demand side of another loop Loops can be either plant or condenser loops but no air side connections are allowed

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.2/io-reference/overview/group-condenser-equipment/#heatexchangerfluidtofluid
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
        chilled_water_flow_mode_type: Literal["", "ConstantFlow", "VariableFlow"] | None = "ConstantFlow",
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_hot_water_flow_rate: float | None = 0,
        compressor_motor_efficiency: float | None = 1,
        condenser_type: Literal["", "AirCooled", "WaterCooled"] | None = "WaterCooled",
        cooling_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "", "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "EnteringCondenser",
        cooling_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        heating_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "", "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "LeavingCondenser",
        heating_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``ChillerHeaterPerformance:Electric:EIR`` and add it to the document.

        This chiller model is a generic chiller-heater where the cooling mode performance is a function of condenser entering or leaving fluid temperature and the heating mode performance is typically a function of condenser leaving fluid temperature. Performance at off-reference conditions is modeled using three polynomial equations per mode. Six curve objects are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-plant-equipment/#chillerheaterperformanceelectriceir
        """

class LifeCycleCostUsePriceEscalation_v8_9_to_v9_2:
    def __call__(
        self,
        /,
        *,
        lcc_price_escalation_name: str,
        resource: str,
        escalation_start_year: float | None = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/energyplus-economics/lifecyclecost-usepriceescalation/#lifecyclecostusepriceescalation
        """

class AirLoopHVACDedicatedOutdoorAirSystem_v9_2_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_mixer_name: str,
        airloophvac_splitter_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        number_of_airloophvac: float,
        airloophvac_outdoorairsystem_name: str | None = ...,
        availability_schedule_name: str | None = ...,
        airloophvacs: list[_g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsItem] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:DedicatedOutdoorAirSystem`` and add it to the document.

        Defines a central forced air system to provide dedicated outdoor air to multiple AirLoopHVACs.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-air-path/#airloophvacdedicatedoutdoorairsystem
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
        lifetime_model: Literal["", "KandlerSmith", "None"] | None = "KandlerSmith",
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
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:LiIonNMCBattery`` and add it to the document.

        Uses Lithium Ion NMC model to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstorageliionnmcbattery
        """
