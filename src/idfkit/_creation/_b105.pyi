"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class ZoneAirContaminantBalance:
    def __call__(
        self,
        /,
        *,
        carbon_dioxide_concentration: Literal["No", "Yes"] | None = "No",
        outdoor_carbon_dioxide_schedule_name: str | None = ...,
        generic_contaminant_concentration: Literal["No", "Yes"] | None = "No",
        outdoor_generic_contaminant_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneAirContaminantBalance`` and add it to the document.

        Determines which contaminant concentration will be simulates.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#zoneaircontaminantbalance
        """

class SurfacePropertyHeatTransferAlgorithmConstruction:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        construction_name: str,
        algorithm: Literal[
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
    ) -> None:
        """Create a new ``SurfaceProperty:HeatTransferAlgorithm:Construction`` and add it to the document.

        Determines which Heat Balance Algorithm will be used for surfaces that have a specific type of construction Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage: CondFD (Conduction Finite Difference) Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheattransferalgorithmconstruction
        """

class PeopleInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        people_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        multiplier: float | None = 1,
        ankle_level_air_velocity_schedule_name: str | None = ...,
        cold_stress_temperature_threshold: float | None = 15.56,
        heat_stress_temperature_threshold: float | None = 30,
    ) -> None:
        """Create a new ``People:Instance`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. The physical characteristics are given by the referenced People:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#peopleinstance
        """

class ZoneVentilationWindandStackOpenArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        opening_area: float | None = 0,
        opening_area_fraction_schedule_name: str | None = ...,
        opening_effectiveness: float | Literal["Autocalculate"] | None = "Autocalculate",
        effective_angle: float | None = 0,
        height_difference: float | None = 0,
        discharge_coefficient_for_opening: float | Literal["Autocalculate"] | None = "Autocalculate",
        minimum_indoor_temperature: float | None = -100,
        minimum_indoor_temperature_schedule_name: str | None = ...,
        maximum_indoor_temperature: float | None = 100,
        maximum_indoor_temperature_schedule_name: str | None = ...,
        delta_temperature: float | None = -100,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature: float | None = -100,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature: float | None = 100,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_wind_speed: float | None = 40,
    ) -> None:
        """Create a new ``ZoneVentilation:WindandStackOpenArea`` and add it to the document.

        This object is specified as natural ventilation driven by wind and stack effect only: Ventilation Wind = Cw * Opening Area * Schedule * WindSpd Ventilation Stack = Cd * Opening Area * Schedule * SQRT(2*g*DH*(|(Tzone-Todb)|/Tzone)) Total Ventilation = SQRT((Ventilation Wind)^2 + (Ventilation Stack)^2) If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneventilationwindandstackopenarea
        """

class HVACTemplatePlantTowerObjectReference:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_tower_name: str,
        cooling_tower_object_type: Literal[
            "CoolingTower:SingleSpeed", "CoolingTower:TwoSpeed", "CoolingTower:VariableSpeed"
        ]
        | None = "CoolingTower:SingleSpeed",
        priority: float | None = ...,
        template_plant_loop_type: Literal["ChilledWater", "MixedWater"] | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Tower:ObjectReference`` and add it to the document.

        This object references a detailed cooling tower object and adds it to an HVACTemplate:Plant:ChilledWaterLoop or MixedWaterLoop. The user must create a complete detailed cooling tower object with all required curve or performance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplanttowerobjectreference
        """

class CoilSystemCoolingDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        dx_cooling_coil_system_inlet_node_name: str,
        dx_cooling_coil_system_outlet_node_name: str,
        dx_cooling_coil_system_sensor_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["No", "Yes"] | None = "No",
        use_outdoor_air_dx_cooling_coil: Literal["No", "Yes"] | None = "No",
        outdoor_air_dx_cooling_coil_leaving_minimum_air_temperature: float | None = 2,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX`` and add it to the document.

        Virtual container component that consists of a DX cooling coil and its associated controls. This control object supports several different types of DX cooling coils and may be placed directly in an air loop branch or outdoor air equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdx
        """

class ChillerElectricASHRAE205:
    def __call__(
        self,
        name: str,
        /,
        *,
        representation_file_name: str,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        performance_interpolation_method: Literal["Cubic", "Linear"] | None = "Linear",
        rated_capacity: float | Literal["Autosize"] | None = "Autosize",
        sizing_factor: float | None = 1,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        chilled_water_maximum_requested_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_maximum_requested_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        oil_cooler_inlet_node_name: str | None = ...,
        oil_cooler_outlet_node_name: str | None = ...,
        oil_cooler_design_flow_rate: float | None = ...,
        auxiliary_inlet_node_name: str | None = ...,
        auxiliary_outlet_node_name: str | None = ...,
        auxiliary_cooling_design_flow_rate: float | None = ...,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Chiller:Electric:ASHRAE205`` and add it to the document.

        This chiller model utilizes ASHRAE Standard 205 compliant representations for chillers (Representation Specification RS0001).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerelectricashrae205
        """

class CoolingTowerPerformanceYorkCalc:
    def __call__(
        self,
        name: str,
        /,
        *,
        minimum_inlet_air_wet_bulb_temperature: float,
        maximum_inlet_air_wet_bulb_temperature: float,
        minimum_range_temperature: float,
        maximum_range_temperature: float,
        minimum_approach_temperature: float,
        maximum_approach_temperature: float,
        minimum_water_flow_rate_ratio: float,
        maximum_water_flow_rate_ratio: float,
        maximum_liquid_to_gas_ratio: float,
        coefficient_1: float,
        coefficient_2: float,
        coefficient_3: float,
        coefficient_4: float,
        coefficient_5: float,
        coefficient_6: float,
        coefficient_7: float,
        coefficient_8: float,
        coefficient_9: float,
        coefficient_10: float,
        coefficient_11: float,
        coefficient_12: float,
        coefficient_13: float,
        coefficient_14: float,
        coefficient_15: float,
        coefficient_16: float,
        coefficient_17: float,
        coefficient_18: float,
        coefficient_19: float,
        coefficient_20: float,
        coefficient_21: float,
        coefficient_22: float,
        coefficient_23: float,
        coefficient_24: float,
        coefficient_25: float,
        coefficient_26: float,
        coefficient_27: float,
    ) -> None:
        """Create a new ``CoolingTowerPerformance:YorkCalc`` and add it to the document.

        This object is used to define coefficients for the approach temperature correlation for a variable speed cooling tower when tower Model Type is specified as YorkCalcUserDefined in the object CoolingTower:VariableSpeed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowerperformanceyorkcalc
        """

class CondenserEquipmentOperationSchemes:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_scheme_1_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ],
        control_scheme_1_name: str,
        control_scheme_1_schedule_name: str,
        control_scheme_2_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_2_name: str | None = ...,
        control_scheme_2_schedule_name: str | None = ...,
        control_scheme_3_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_3_name: str | None = ...,
        control_scheme_3_schedule_name: str | None = ...,
        control_scheme_4_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_4_name: str | None = ...,
        control_scheme_4_schedule_name: str | None = ...,
        control_scheme_5_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_5_name: str | None = ...,
        control_scheme_5_schedule_name: str | None = ...,
        control_scheme_6_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_6_name: str | None = ...,
        control_scheme_6_schedule_name: str | None = ...,
        control_scheme_7_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_7_name: str | None = ...,
        control_scheme_7_schedule_name: str | None = ...,
        control_scheme_8_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_8_name: str | None = ...,
        control_scheme_8_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``CondenserEquipmentOperationSchemes`` and add it to the document.

        Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first that is 'Scheduled' on. That is, if control scheme 1 is not 'on' and control scheme 2 is -- then control scheme 2 is selected. Only condenser equipment should be listed on a Control Scheme for this item.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#condenserequipmentoperationschemes
        """

class GeneratorFuelCellPowerModule:
    def __call__(
        self,
        name: str,
        /,
        *,
        efficiency_curve_name: str,
        efficiency_curve_mode: Literal["Annex42", "Normalized"] | None = ...,
        nominal_efficiency: float | None = ...,
        nominal_electrical_power: float | None = ...,
        number_of_stops_at_start_of_simulation: float | None = ...,
        cycling_performance_degradation_coefficient: float | None = ...,
        number_of_run_hours_at_beginning_of_simulation: float | None = ...,
        accumulated_run_time_degradation_coefficient: float | None = ...,
        run_time_degradation_initiation_time_threshold: float | None = ...,
        power_up_transient_limit: float | None = ...,
        power_down_transient_limit: float | None = ...,
        start_up_time: float | None = ...,
        start_up_fuel: float | None = ...,
        start_up_electricity_consumption: float | None = ...,
        start_up_electricity_produced: float | None = ...,
        shut_down_time: float | None = ...,
        shut_down_fuel: float | None = ...,
        shut_down_electricity_consumption: float | None = ...,
        ancillary_electricity_constant_term: float | None = ...,
        ancillary_electricity_linear_term: float | None = ...,
        skin_loss_calculation_mode: Literal["ConstantRate", "QuadraticFunctionOfFuelRate", "UAForProcessGasTemperature"]
        | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        constant_skin_loss_rate: float | None = ...,
        skin_loss_u_factor_times_area_term: float | None = ...,
        skin_loss_quadratic_curve_name: str | None = ...,
        dilution_air_flow_rate: float | None = ...,
        stack_heat_loss_to_dilution_air: float | None = ...,
        dilution_inlet_air_node_name: str | None = ...,
        dilution_outlet_air_node_name: str | None = ...,
        minimum_operating_point: float | None = ...,
        maximum_operating_point: float | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:PowerModule`` and add it to the document.

        Describe the core power module subsystem of a fuel cell power generator. This includes the fuel cell stack, fuel reformer, and whatever ancillary devices are included inside. If the model has multiple FC generators that are of the exact same type, then only one of these objects is needed and all the Generator:FuelCell objects can reference it.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellpowermodule
        """
