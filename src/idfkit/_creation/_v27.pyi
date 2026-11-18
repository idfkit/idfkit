"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class ScheduleFile_v9_2_to_v9_6:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: float,
        rows_to_skip_at_top: float,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["", "Comma", "Semicolon", "Space", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["", "No", "Yes"] | None = "No",
        minutes_per_item: float | None = ...,
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.6/io-reference/overview/group-schedules/#schedulefile
        """

class ExteriorFuelEquipment_v9_3_to_v23_1:
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
        schedule_name: str,
        design_level: float,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Exterior:FuelEquipment`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-exterior-energy-use-equipment/#exteriorfuelequipment
        """

class ZoneThermalChimney_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        width_of_the_absorber_wall: float,
        cross_sectional_area_of_air_channel_outlet: float,
        zone_1_name: str,
        distance_from_top_of_thermal_chimney_to_inlet_1: float,
        cross_sectional_areas_of_air_channel_inlet_1: float,
        availability_schedule_name: str | None = ...,
        discharge_coefficient: float | None = 0.8,
        relative_ratios_of_air_flow_rates_passing_through_zone_1: float | None = 1,
        zone_2_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_2: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_2: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_2: float | None = ...,
        zone_3_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_3: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_3: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_3: float | None = ...,
        zone_4_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_4: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_4: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_4: float | None = ...,
        zone_5_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_5: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_5: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_5: float | None = ...,
        zone_6_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_6: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_6: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_6: float | None = ...,
        zone_7_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_7: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_7: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_7: float | None = ...,
        zone_8_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_8: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_8: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_8: float | None = ...,
        zone_9_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_9: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_9: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_9: float | None = ...,
        zone_10_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_10: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_10: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_10: float | None = ...,
        zone_11_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_11: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_11: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_11: float | None = ...,
        zone_12_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_12: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_12: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_12: float | None = ...,
        zone_13_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_13: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_13: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_13: float | None = ...,
        zone_14_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_14: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_14: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_14: float | None = ...,
        zone_15_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_15: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_15: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_15: float | None = ...,
        zone_16_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_16: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_16: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_16: float | None = ...,
        zone_17_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_17: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_17: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_17: float | None = ...,
        zone_18_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_18: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_18: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_18: float | None = ...,
        zone_19_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_19: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_19: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_19: float | None = ...,
        zone_20_name: str | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_20: float | None = ...,
        relative_ratios_of_air_flow_rates_passing_through_zone_20: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_20: float | None = ...,
    ) -> None:
        """Create a new ``ZoneThermalChimney`` and add it to the document.

        A thermal chimney is a vertical shaft utilizing solar radiation to enhance natural ventilation. It consists of an absorber wall, air gap and glass cover with high solar transmissivity.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-airflow/#zonethermalchimney
        """

class MaterialPropertyHeatAndMoistureTransferSorptionIsotherm_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_isotherm_coordinates: float,
        relative_humidity_fraction_1: float,
        moisture_content_1: float,
        relative_humidity_fraction_2: float | None = ...,
        moisture_content_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        moisture_content_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        moisture_content_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        moisture_content_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        moisture_content_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        moisture_content_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        moisture_content_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        moisture_content_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        moisture_content_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        moisture_content_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        moisture_content_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        moisture_content_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        moisture_content_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        moisture_content_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        moisture_content_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        moisture_content_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        moisture_content_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        moisture_content_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        moisture_content_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        moisture_content_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        moisture_content_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        moisture_content_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        moisture_content_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        moisture_content_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:SorptionIsotherm`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between moisture content and relative humidity fraction. Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersorptionisotherm
        """

class SurfacePropertyConvectionCoefficientsMultipleSurface_v8_9_to_v9_4:
    def __call__(
        self,
        /,
        *,
        surface_type: Literal[
            "AllExteriorFloors",
            "AllExteriorRoofs",
            "AllExteriorSurfaces",
            "AllExteriorWalls",
            "AllExteriorWindows",
            "AllInteriorCeilings",
            "AllInteriorFloors",
            "AllInteriorSurfaces",
            "AllInteriorWalls",
            "AllInteriorWindows",
        ],
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
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
            "BlockenWindard",
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
            "BlockenWindard",
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
        """Create a new ``SurfaceProperty:ConvectionCoefficients:MultipleSurface`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficientsmultiplesurface
        """

class PhotovoltaicPerformanceSandia_v8_9_to_v22_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        active_area: float | None = 1,
        number_of_cells_in_series: float | None = 1,
        number_of_cells_in_parallel: float | None = 1,
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
        sandia_database_parameter_delta_tc: float | None = ...,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Sandia`` and add it to the document.

        Describes performance input data needed for specific makes and models of production PV panels using the empirical coefficients assembled by Sandia National Laboratory.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesandia
        """

class AirflowNetworkDistributionComponentCoil_v8_9_to_v9_2:
    def __call__(
        self,
        /,
        *,
        coil_name: str,
        coil_object_type: Literal[
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentcoil
        """

class FaultModelPressureSensorOffsetOutdoorAir_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        pressure_sensor_offset: float | None = 0,
    ) -> None:
        """Create a new ``FaultModel:PressureSensorOffset:OutdoorAir`` and add it to the document.

        This object describes outdoor air pressure sensor offset

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.
        """

class ZoneVentilationDesignFlowRate_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_zone_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        ventilation_type: Literal["", "Balanced", "Exhaust", "Intake", "Natural"] | None = "Natural",
        fan_pressure_rise: float | None = 0,
        fan_total_efficiency: float | None = 1,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
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
        """Create a new ``ZoneVentilation:DesignFlowRate`` and add it to the document.

        Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow/#zoneventilationdesignflowrate
        """

class CoilCoolingWaterToAirHeatPumpEquationFit_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        total_cooling_capacity_coefficient_1: float,
        total_cooling_capacity_coefficient_2: float,
        total_cooling_capacity_coefficient_3: float,
        total_cooling_capacity_coefficient_4: float,
        total_cooling_capacity_coefficient_5: float,
        sensible_cooling_capacity_coefficient_1: float,
        sensible_cooling_capacity_coefficient_2: float,
        sensible_cooling_capacity_coefficient_3: float,
        sensible_cooling_capacity_coefficient_4: float,
        sensible_cooling_capacity_coefficient_5: float,
        sensible_cooling_capacity_coefficient_6: float,
        cooling_power_consumption_coefficient_1: float,
        cooling_power_consumption_coefficient_2: float,
        cooling_power_consumption_coefficient_3: float,
        cooling_power_consumption_coefficient_4: float,
        cooling_power_consumption_coefficient_5: float,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

class HotWaterEquipment_v9_6_to_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_zone_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HotWaterEquipment`` and add it to the document.

        Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#hotwaterequipment
        """

class HeatPumpWaterToWaterEquationFitCooling_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_cooling_capacity: float | Literal["Autosize"],
        reference_cooling_power_consumption: float | Literal["Autosize"],
        cooling_capacity_coefficient_1: float,
        cooling_capacity_coefficient_2: float,
        cooling_capacity_coefficient_3: float,
        cooling_capacity_coefficient_4: float,
        cooling_capacity_coefficient_5: float,
        cooling_compressor_power_coefficient_1: float,
        cooling_compressor_power_coefficient_2: float,
        cooling_compressor_power_coefficient_3: float,
        cooling_compressor_power_coefficient_4: float,
        cooling_compressor_power_coefficient_5: float,
        reference_coefficient_of_performance: float | None = 8,
        sizing_factor: float | None = 1,
        companion_heating_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Cooling`` and add it to the document.

        simple water-water heat pump curve-fit model

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitcooling
        """

class CentralHeatPumpSystem_v22_2_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_loop_inlet_node_name: str,
        cooling_loop_outlet_node_name: str,
        source_loop_inlet_node_name: str,
        source_loop_outlet_node_name: str,
        heating_loop_inlet_node_name: str,
        heating_loop_outlet_node_name: str,
        chiller_heater_modules_performance_component_object_type_1: Literal["ChillerHeaterPerformance:Electric:EIR"],
        chiller_heater_modules_performance_component_name_1: str,
        chiller_heater_modules_control_schedule_name_1: str,
        control_method: Literal["", "SmartMixing"] | None = "SmartMixing",
        ancillary_power: float | None = 0,
        ancillary_operation_schedule_name: str | None = ...,
        number_of_chiller_heater_modules_1: int | None = 1,
        chiller_heater_modules_performance_component_object_type_2: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_2: str | None = ...,
        chiller_heater_modules_control_schedule_name_2: str | None = ...,
        number_of_chiller_heater_modules_2: int | None = 1,
        chiller_heater_performance_component_object_type_3: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_performance_component_name_3: str | None = ...,
        chiller_heater_modules_control_schedule_name_3: str | None = ...,
        number_of_chiller_heater_modules_3: int | None = 1,
        chiller_heater_modules_performance_component_object_type_4: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_4: str | None = ...,
        chiller_heater_modules_control_schedule_name_4: str | None = ...,
        number_of_chiller_heater_modules_4: int | None = 1,
        chiller_heater_modules_performance_component_object_type_5: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_models_performance_component_name_5: str | None = ...,
        chiller_heater_modules_control_schedule_name_5: str | None = ...,
        number_of_chiller_heater_modules_5: int | None = 1,
        chiller_heater_modules_performance_component_object_type_6: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_6: str | None = ...,
        chiller_heater_modules_control_schedule_name_6: str | None = ...,
        number_of_chiller_heater_modules_6: int | None = 1,
        chiller_heater_modules_performance_component_object_type_7: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_7: str | None = ...,
        chiller_heater_modules_control_schedule_name_7: str | None = ...,
        number_of_chiller_heater_modules_7: int | None = 1,
        chiller_heater_modules_performance_component_object_type_8: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_8: str | None = ...,
        chiller_heater_modules_control_schedule_name_8: str | None = ...,
        number_of_chiller_heater_modules_8: int | None = 1,
        chiller_heater_modules_performance_component_object_type_9: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_9: str | None = ...,
        chiller_heater_modules_control_schedule_name_9: str | None = ...,
        number_of_chiller_heater_modules_9: int | None = 1,
        chiller_heater_modules_performance_component_object_type_10: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_10: str | None = ...,
        chiller_heater_modules_control_schedule_name_10: str | None = ...,
        number_of_chiller_heater_modules_10: int | None = 1,
        chiller_heater_modules_performance_component_object_type_11: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_11: str | None = ...,
        chiller_heater_module_control_schedule_name_11: str | None = ...,
        number_of_chiller_heater_modules_11: int | None = 1,
        chiller_heater_modules_performance_component_object_type_12: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_12: str | None = ...,
        chiller_heater_modules_control_schedule_name_12: str | None = ...,
        number_of_chiller_heater_modules_12: int | None = 1,
        chiller_heater_modules_performance_component_object_type_13: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_13: str | None = ...,
        chiller_heater_modules_control_schedule_name_13: str | None = ...,
        number_of_chiller_heater_modules_13: int | None = 1,
        chiller_heater_modules_performance_component_object_type_14: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_14: str | None = ...,
        chiller_heater_modules_control_schedule_name_14: str | None = ...,
        number_of_chiller_heater_modules_14: int | None = 1,
        chiller_heater_modules_performance_component_object_type_15: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_15: str | None = ...,
        chiller_heater_modules_control_schedule_name_15: str | None = ...,
        number_of_chiller_heater_modules_15: int | None = 1,
        chiller_heater_modules_performance_component_object_type_16: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_16: str | None = ...,
        chiller_heater_modules_control_schedule_name_16: str | None = ...,
        number_of_chiller_heater_modules_16: int | None = 1,
        chiller_heater_modules_performance_component_object_type_17: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_17: str | None = ...,
        chiller_heater_modules_control_schedule_name_17: str | None = ...,
        number_of_chiller_heater_modules_17: int | None = 1,
        chiller_heater_modules_performance_component_object_type_18: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_18: str | None = ...,
        chiller_heater_modules_control_control_schedule_name_18: str | None = ...,
        number_of_chiller_heater_modules_18: int | None = 1,
        chiller_heater_modules_performance_component_object_type_19: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_19: str | None = ...,
        chiller_heater_modules_control_schedule_name_19: str | None = ...,
        number_of_chiller_heater_modules_19: int | None = 1,
        chiller_heater_modules_performance_component_object_type_20: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_20: str | None = ...,
        chiller_heater_modules_control_schedule_name_20: str | None = ...,
        number_of_chiller_heater_modules_20: int | None = 1,
    ) -> None:
        """Create a new ``CentralHeatPumpSystem`` and add it to the document.

        This chiller bank can contain multiple chiller heaters and heat pump performance objects. Its function is to encapsulate the extra controls needed to turn individual modules on/off and whether they are to operate in cooling-only, heating-only or simultaneous cooling/heating mode and whether to connect the source water to the evaporator or condenser side.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-plant-equipment/#centralheatpumpsystem
        """

class Timestep_v8_9_to_v22_1:
    def __call__(self, /, *, number_of_timesteps_per_hour: float | None = 6) -> None:
        """Create a new ``Timestep`` and add it to the document.

        Specifies the 'basic' timestep for the simulation. The value entered here is also known as the Zone Timestep. This is used in the Zone Heat Balance Model calculation as the driving timestep for heat transfer and load calculations.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-simulation-parameters/#timestep
        """

class TableLookup_v9_2_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        independent_variable_list_name: str,
        normalization_method: Literal["", "AutomaticWithDivisor", "DivisorOnly", "None"] | None = "None",
        normalization_divisor: float | None = 1,
        minimum_output: float | None = ...,
        maximum_output: float | None = ...,
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: float | None = ...,
        external_file_starting_row_number: float | None = ...,
        values: list[_g.TableLookupValuesItem] = ...,
    ) -> None:
        """Create a new ``Table:Lookup`` and add it to the document.

        Lookup tables are used in place of curves and can represent any number of independent variables (defined as Table:IndependentVariable objects in a Table:IndependentVariableList). Output values are interpolated within the bounds defined by each independent variable and extrapolated beyond the bounds according to the interpolation/extrapolation methods defined by each independent variable.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-performance-tables/#tablelookup
        """

class CoilCoolingDXCurveFitPerformance_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        base_operating_mode: str,
        crankcase_heater_capacity: float | None = 0,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        unit_internal_static_air_pressure: float | None = ...,
        capacity_control_method: Literal["", "Continuous", "Discrete"] | None = "Discrete",
        evaporative_condenser_basin_heater_capacity: float | None = 0,
        evaporative_condenser_basin_heater_setpoint_temperature: float | None = 2,
        evaporative_condenser_basin_heater_operating_schedule_name: str | None = ...,
        compressor_fuel_type: Literal[
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
        alternative_operating_mode_1: str | None = ...,
        alternative_operating_mode_2: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Performance`` and add it to the document.

        DX cooling coil performance specification referencing one or more operating modes. Mode 1 is always the base design operating mode. Additional modes are optional states such as subcool reheat for humidity control.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitperformance
        """
