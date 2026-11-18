"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class SurfacePropertyConvectionCoefficients_v9_5_to_v9_6:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
            "ASTMC1340",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ],
        convection_coefficient_1: float | None = ...,
        convection_coefficient_1_schedule_name: str | None = ...,
        convection_coefficient_1_user_curve_name: str | None = ...,
        convection_coefficient_2_location: Literal["Inside", "Outside"] | None = ...,
        convection_coefficient_2_type: Literal[
            "ASHRAEVerticalWall",
            "ASTMC1340",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = ...,
        convection_coefficient_2: float | None = 0.1,
        convection_coefficient_2_schedule_name: str | None = ...,
        convection_coefficient_2_user_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:ConvectionCoefficients`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.6/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficients
        """

class ZoneHVACIdealLoadsAirSystem_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_exhaust_air_node_name: str | None = ...,
        system_inlet_air_node_name: str | None = ...,
        maximum_heating_supply_air_temperature: float | None = 50,
        minimum_cooling_supply_air_temperature: float | None = 13,
        maximum_heating_supply_air_humidity_ratio: float | None = 0.0156,
        minimum_cooling_supply_air_humidity_ratio: float | None = 0.0077,
        heating_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_heating_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_sensible_heating_capacity: float | Literal["Autosize"] | None = ...,
        cooling_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_cooling_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        heating_availability_schedule_name: str | None = ...,
        cooling_availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal[
            "", "ConstantSensibleHeatRatio", "ConstantSupplyHumidityRatio", "Humidistat", "None"
        ]
        | None = "ConstantSensibleHeatRatio",
        cooling_sensible_heat_ratio: float | None = 0.7,
        humidification_control_type: Literal["", "ConstantSupplyHumidityRatio", "Humidistat", "None"] | None = "None",
        design_specification_outdoor_air_object_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        demand_controlled_ventilation_type: Literal["", "CO2Setpoint", "None", "OccupancySchedule"] | None = "None",
        outdoor_air_economizer_type: Literal["", "DifferentialDryBulb", "DifferentialEnthalpy", "NoEconomizer"]
        | None = "NoEconomizer",
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:IdealLoadsAirSystem`` and add it to the document.

        Ideal system used to calculate loads without modeling a full HVAC system. All that is required for the ideal system are zone controls, zone equipment configurations, and the ideal loads system component. This component can be thought of as an ideal unit that mixes zone air with the specified amount of outdoor air and then adds or removes heat and moisture at 100% efficiency in order to meet the specified controls. Energy use is reported as DistrictHeatingWater and DistrictCooling.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-zone-forced-air-units/#zonehvacidealloadsairsystem
        """

class WallUnderground_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Underground`` and add it to the document.

        Allows for simplified entry of underground walls.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#wallunderground
        """

class People_v9_5:
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
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class AirflowNetworkDistributionComponentCoil_v9_3_to_v23_2:
    def __call__(
        self,
        /,
        *,
        coil_name: str,
        coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Water",
        ],
        air_path_length: float,
        air_path_hydraulic_diameter: float,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Coil`` and add it to the document.

        This object defines the name of a coil used in an air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentcoil
        """

class ConstructionComplexFenestrationState_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_thermal_model: str,
        basis_matrix_name: str,
        solar_optical_complex_front_transmittance_matrix_name: str,
        solar_optical_complex_back_reflectance_matrix_name: str,
        visible_optical_complex_front_transmittance_matrix_name: str,
        visible_optical_complex_back_transmittance_matrix_name: str,
        outside_layer_name: str,
        outside_layer_directional_front_absoptance_matrix_name: str,
        outside_layer_directional_back_absoptance_matrix_name: str,
        basis_type: Literal["", "LBNLWINDOW", "UserDefined"] | None = "LBNLWINDOW",
        basis_symmetry_type: Literal["", "Axisymmetric", "None"] | None = "None",
        gap_1_name: str | None = ...,
        cfs_gap_1_directional_front_absoptance_matrix_name: str | None = ...,
        cfs_gap_1_directional_back_absoptance_matrix_name: str | None = ...,
        layer_2_name: str | None = ...,
        layer_2_directional_front_absoptance_matrix_name: str | None = ...,
        layer_2_directional_back_absoptance_matrix_name: str | None = ...,
        gap_2_name: str | None = ...,
        gap_2_directional_front_absoptance_matrix_name: str | None = ...,
        gap_2_directional_back_absoptance_matrix_name: str | None = ...,
        layer_3_material: str | None = ...,
        layer_3_directional_front_absoptance_matrix_name: str | None = ...,
        layer_3_directional_back_absoptance_matrix_name: str | None = ...,
        gap_3_name: str | None = ...,
        gap_3_directional_front_absoptance_matrix_name: str | None = ...,
        gap_3_directional_back_absoptance_matrix_name: str | None = ...,
        layer_4_name: str | None = ...,
        layer_4_directional_front_absoptance_matrix_name: str | None = ...,
        layer_4_directional_back_absoptance_matrix_name: str | None = ...,
        gap_4_name: str | None = ...,
        gap_4_directional_front_absoptance_matrix_name: str | None = ...,
        gap_4_directional_back_absoptance_matrix_name: str | None = ...,
        layer_5_name: str | None = ...,
        layer_5_directional_front_absoptance_matrix_name: str | None = ...,
        layer_5_directional_back_absoptance_matrix_name: str | None = ...,
    ) -> None:
        """Create a new ``Construction:ComplexFenestrationState`` and add it to the document.

        Describes one state for a complex glazing system These input objects are typically generated by using WINDOW software and export to IDF syntax

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-surface-construction-elements/#constructioncomplexfenestrationstate
        """

class CoilHeatingDXVariableSpeed_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_heating_capacity: float,
        speed_1_reference_unit_gross_rated_heating_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_total_heating_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        rated_heating_capacity_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        speed_2_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:VariableSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), variable-speed, with defrost controls. Requires two to ten sets of performance data and will interpolate between speeds.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxvariablespeed
        """

class CoilHeatingDXMultiSpeed_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal[
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        number_of_speeds: float,
        speed_1_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_heating_cop: float,
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_heating_cop: float,
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_heating_capacity_function_of_temperature_curve_name: str,
        speed_2_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        region_number_for_calculating_hspf: float | None = 4,
        speed_1_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_heating_cop: float | None = ...,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_heating_cop: float | None = ...,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_rated_supply_air_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        speed_1_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_1_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_2_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_2_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_3_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_4_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:MultiSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric or engine-driven compressor and outdoor fan), multi-speed (or variable-speed), with defrost controls. Requires two to four sets of performance data and will interpolate between speeds.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxmultispeed
        """

class ZoneHVACBaseboardRadiantConvectiveWater_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_water_flow_rate: float | Literal["Autosize"],
        fraction_radiant: float,
        availability_schedule_name: str | None = ...,
        rated_average_water_temperature: float | None = 87.78,
        rated_water_mass_flow_rate: float | None = 0.063,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        convergence_tolerance: float | None = 0.001,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[_g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivewater
        """

class ChillerElectric_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
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
        """Create a new ``Chiller:Electric`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/energyplus-economics/cost-estimating/#chillerelectric
        """

class TableMultiVariableLookup_v9_0_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        interpolation_method: Literal[
            "", "EvaluateCurveToLimits", "LagrangeInterpolationLinearExtrapolation", "LinearInterpolationOfTable"
        ]
        | None = "LagrangeInterpolationLinearExtrapolation",
        number_of_interpolation_points: float | None = 3,
        curve_type: Literal["BiQuadratic", "Cubic", "Linear", "Quadratic", "QuadraticLinear", "Quartic"] | None = ...,
        table_data_format: Literal["", "SingleLineIndependentVariableWithMatrix"]
        | None = "SingleLineIndependentVariableWithMatrix",
        external_file_name: str | None = ...,
        x1_sort_order: Literal["", "Ascending", "Descending"] | None = "Ascending",
        x2_sort_order: Literal["", "Ascending", "Descending"] | None = "Ascending",
        normalization_reference: float | None = ...,
        minimum_value_of_x1: float | None = ...,
        maximum_value_of_x1: float | None = ...,
        minimum_value_of_x2: float | None = ...,
        maximum_value_of_x2: float | None = ...,
        minimum_value_of_x3: float | None = ...,
        maximum_value_of_x3: float | None = ...,
        minimum_value_of_x4: float | None = ...,
        maximum_value_of_x4: float | None = ...,
        minimum_value_of_x5: float | None = ...,
        maximum_value_of_x5: float | None = ...,
        minimum_value_of_x6: float | None = ...,
        maximum_value_of_x6: float | None = ...,
        minimum_table_output: float | None = ...,
        maximum_table_output: float | None = ...,
        input_unit_type_for_x1: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x2: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x3: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x4: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x5: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_x6: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        number_of_independent_variables: float | None = ...,
        number_of_values_for_independent_variable_x1: float | None = ...,
        field_1_determined_by_the_number_of_independent_variables: float | None = ...,
        field_2_determined_by_the_number_of_independent_variables: float | None = ...,
        values: list[_vd.TableMultiVariableLookupValuesItem_v9_0_to_v9_1] = ...,
    ) -> None:
        """Create a new ``Table:MultiVariableLookup`` and add it to the document.

        The multi-variable lookup table can represent from 1 to 6 independent variables and can interpolate these independent variables up to a 4th order polynomial. The polynomial order is assumed to be the number of interpolation points (n) minus 1. When any independent variable value is outside the table limits, linear extrapolation is used to predict the table result and is based on the two nearest data points in the table for that particular independent variable.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.
        """

class CoilCoolingDXMultiSpeed_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal[
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        number_of_speeds: float,
        speed_1_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_2_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        speed_1_gross_rated_cooling_cop: float | None = 3,
        speed_1_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_1_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_1_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_1_maximum_cycling_rate: float | None = 0,
        speed_1_latent_capacity_time_constant: float | None = 0,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_1_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_1_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_2_gross_rated_cooling_cop: float | None = 3,
        speed_2_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_2_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_2_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_2_maximum_cycling_rate: float | None = 0,
        speed_2_latent_capacity_time_constant: float | None = 0,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_2_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_cooling_cop: float | None = 3,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_3_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_3_maximum_cycling_rate: float | None = 0,
        speed_3_latent_capacity_time_constant: float | None = 0,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_3_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_cooling_cop: float | None = 3,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_4_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_4_maximum_cycling_rate: float | None = 0,
        speed_4_latent_capacity_time_constant: float | None = 0,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_4_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:MultiSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric or engine-driven compressor and condenser fan), multi-speed (or variable-speed). Optional moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data and will interpolate between speeds. Modeled as a single coil (multi-speed compressor or multiple compressors with row split or intertwined coil).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxmultispeed
        """

class RoofCeilingDetailed_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[_g.RoofCeilingDetailedVerticesItem] = ...,
    ) -> None:
        """Create a new ``RoofCeiling:Detailed`` and add it to the document.

        Allows for detailed entry of roof/ceiling heat transfer surfaces.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#roofceilingdetailed
        """

class OutputControlFiles_v9_4_to_v24_1:
    def __call__(
        self,
        /,
        *,
        output_csv: Literal["", "No", "Yes"] | None = "No",
        output_mtr: Literal["", "No", "Yes"] | None = "Yes",
        output_eso: Literal["", "No", "Yes"] | None = "Yes",
        output_eio: Literal["", "No", "Yes"] | None = "Yes",
        output_tabular: Literal["", "No", "Yes"] | None = "Yes",
        output_sqlite: Literal["", "No", "Yes"] | None = "Yes",
        output_json: Literal["", "No", "Yes"] | None = "Yes",
        output_audit: Literal["", "No", "Yes"] | None = "Yes",
        output_zone_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_system_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_dxf: Literal["", "No", "Yes"] | None = "Yes",
        output_bnd: Literal["", "No", "Yes"] | None = "Yes",
        output_rdd: Literal["", "No", "Yes"] | None = "Yes",
        output_mdd: Literal["", "No", "Yes"] | None = "Yes",
        output_mtd: Literal["", "No", "Yes"] | None = "Yes",
        output_end: Literal["", "No", "Yes"] | None = "Yes",
        output_shd: Literal["", "No", "Yes"] | None = "Yes",
        output_dfs: Literal["", "No", "Yes"] | None = "Yes",
        output_glhe: Literal["", "No", "Yes"] | None = "Yes",
        output_delightin: Literal["", "No", "Yes"] | None = "Yes",
        output_delighteldmp: Literal["", "No", "Yes"] | None = "Yes",
        output_delightdfdmp: Literal["", "No", "Yes"] | None = "Yes",
        output_edd: Literal["", "No", "Yes"] | None = "Yes",
        output_dbg: Literal["", "No", "Yes"] | None = "Yes",
        output_perflog: Literal["", "No", "Yes"] | None = "Yes",
        output_sln: Literal["", "No", "Yes"] | None = "Yes",
        output_sci: Literal["", "No", "Yes"] | None = "Yes",
        output_wrl: Literal["", "No", "Yes"] | None = "Yes",
        output_screen: Literal["", "No", "Yes"] | None = "Yes",
        output_extshd: Literal["", "No", "Yes"] | None = "Yes",
        output_tarcog: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``OutputControl:Files`` and add it to the document.

        Conditionally turn on/off output from EnergyPlus.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/input-for-output/#outputcontrolfiles
        """
