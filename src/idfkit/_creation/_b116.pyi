"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SiteGroundTemperatureBuildingSurface:
    def __call__(
        self,
        /,
        *,
        january_ground_temperature: float | None = 18,
        february_ground_temperature: float | None = 18,
        march_ground_temperature: float | None = 18,
        april_ground_temperature: float | None = 18,
        may_ground_temperature: float | None = 18,
        june_ground_temperature: float | None = 18,
        july_ground_temperature: float | None = 18,
        august_ground_temperature: float | None = 18,
        september_ground_temperature: float | None = 18,
        october_ground_temperature: float | None = 18,
        november_ground_temperature: float | None = 18,
        december_ground_temperature: float | None = 18,
    ) -> None:
        """Create a new ``Site:GroundTemperature:BuildingSurface`` and add it to the document.

        These temperatures are specifically for those surfaces that have the outside environment of 'Ground'. Documentation about what values these should be is located in the Auxiliary programs document (Ground Heat Transfer) as well as the InputOutput Reference. CAUTION - Do not use the 'undisturbed' ground temperatures from the weather data. These values are too extreme for the soil under a conditioned building. For best results, use the Slab or Basement program to calculate custom monthly average ground temperatures (see Auxiliary Programs). For typical commercial buildings in the USA, a reasonable default value is 2C less than the average indoor space temperature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperaturebuildingsurface
        """

class AnyWindowShadingControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        shading_type: Literal[
            "BetweenGlassBlind",
            "BetweenGlassShade",
            "ExteriorBlind",
            "ExteriorScreen",
            "ExteriorShade",
            "InteriorBlind",
            "InteriorShade",
            "SwitchableGlazing",
        ],
        shading_control_type: Literal[
            "AlwaysOff",
            "AlwaysOn",
            "MeetDaylightIlluminanceSetpoint",
            "OffNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnIfHighGlare",
            "OnIfHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighSolarOnWindow",
            "OnIfHighOutdoorAirTemperature",
            "OnIfHighSolarOnWindow",
            "OnIfHighZoneAirTempAndHighHorizontalSolar",
            "OnIfHighZoneAirTempAndHighSolarOnWindow",
            "OnIfHighZoneAirTemperature",
            "OnIfHighZoneCooling",
            "OnIfScheduleAllows",
            "OnNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnNightIfHeatingAndOffDay",
            "OnNightIfHeatingAndOnDayIfCooling",
            "OnNightIfLowInsideTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOnDayIfCooling",
        ],
        shading_control_sequence_number: int | None = 1,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["No", "Yes"] | None = "No",
        glare_control_is_active: Literal["No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        daylighting_control_object_name: str | None = ...,
        multiple_surface_control_type: Literal["Group", "Sequential"] | None = "Sequential",
        fenestration_surfaces: Sequence[
            _g.WindowShadingControlFenestrationSurfacesItem | _g.WindowShadingControlFenestrationSurfacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``WindowShadingControl`` and add it to the document.

        Specifies the type, location, and controls for window shades, window blinds, and switchable glazing. Referencing the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowshadingcontrol
        """

class AnyRoomAirTemperaturePatternSurfaceMapping:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        surface_deltas: Sequence[
            _g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasItem
            | _g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasGroup
        ] = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:SurfaceMapping`` and add it to the document.

        Defines a distribution pattern for the air temperatures adjacent to individual surfaces. This allows controlling the adjacent air temperature on a surface-by-surface basis rather than by height. This allows modeling different adjacent air temperatures on the opposite sides of the zone. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternsurfacemapping
        """

class AirflowNetworkMultiZoneWindPressureCoefficientArray:
    def __call__(
        self,
        name: str,
        /,
        *,
        wind_direction_1: float,
        wind_direction_2: float,
        wind_direction_3: float | None = ...,
        wind_direction_4: float | None = ...,
        wind_direction_5: float | None = ...,
        wind_direction_6: float | None = ...,
        wind_direction_7: float | None = ...,
        wind_direction_8: float | None = ...,
        wind_direction_9: float | None = ...,
        wind_direction_10: float | None = ...,
        wind_direction_11: float | None = ...,
        wind_direction_12: float | None = ...,
        wind_direction_13: float | None = ...,
        wind_direction_14: float | None = ...,
        wind_direction_15: float | None = ...,
        wind_direction_16: float | None = ...,
        wind_direction_17: float | None = ...,
        wind_direction_18: float | None = ...,
        wind_direction_19: float | None = ...,
        wind_direction_20: float | None = ...,
        wind_direction_21: float | None = ...,
        wind_direction_22: float | None = ...,
        wind_direction_23: float | None = ...,
        wind_direction_24: float | None = ...,
        wind_direction_25: float | None = ...,
        wind_direction_26: float | None = ...,
        wind_direction_27: float | None = ...,
        wind_direction_28: float | None = ...,
        wind_direction_29: float | None = ...,
        wind_direction_30: float | None = ...,
        wind_direction_31: float | None = ...,
        wind_direction_32: float | None = ...,
        wind_direction_33: float | None = ...,
        wind_direction_34: float | None = ...,
        wind_direction_35: float | None = ...,
        wind_direction_36: float | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:WindPressureCoefficientArray`` and add it to the document.

        Used only if Wind Pressure Coefficient (WPC) Type = Input in the AirflowNetwork:SimulationControl object. Number of WPC Values in the corresponding AirflowNetwork:MultiZone:WindPressureCoefficientValues object must be the same as the number of wind directions specified for this AirflowNetwork:MultiZone:WindPressureCoefficientArray object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonewindpressurecoefficientarray
        """

class AirflowNetworkDistributionComponentLeakageRatio:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_flow_rate: float,
        reference_pressure_difference: float,
        effective_leakage_ratio: float | None = ...,
        air_mass_flow_exponent: float | None = 0.65,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:LeakageRatio`` and add it to the document.

        This object is used to define supply and return air leaks with respect to the fan's maximum air flow rate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentleakageratio
        """

class ChillerAbsorptionIndirect:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_pumping_power: float | Literal["Autosize"],
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        condenser_outlet_node_name: str,
        generator_heat_input_function_of_part_load_ratio_curve_name: str,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = 30,
        condenser_inlet_temperature_lower_limit: float | None = 15,
        chilled_water_outlet_temperature_lower_limit: float | None = 5,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        pump_electric_input_function_of_part_load_ratio_curve_name: str | None = ...,
        generator_inlet_node_name: str | None = ...,
        generator_outlet_node_name: str | None = ...,
        capacity_correction_function_of_condenser_temperature_curve_name: str | None = ...,
        capacity_correction_function_of_chilled_water_temperature_curve_name: str | None = ...,
        capacity_correction_function_of_generator_temperature_curve_name: str | None = ...,
        generator_heat_input_correction_function_of_condenser_temperature_curve_name: str | None = ...,
        generator_heat_input_correction_function_of_chilled_water_temperature_curve_name: str | None = ...,
        generator_heat_source_type: Literal["HotWater", "Steam"] | None = "Steam",
        design_generator_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        temperature_lower_limit_generator_inlet: float | None = 0,
        degree_of_subcooling_in_steam_generator: float | None = 1,
        degree_of_subcooling_in_steam_condensate_loop: float | None = 0,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``Chiller:Absorption:Indirect`` and add it to the document.

        This indirect absorption chiller model is an enhanced model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. The chiller capacity is a function of condenser, chilled water, and generator temperatures. The heat input is a function of part-load ratio, condenser temperature, and chilled water temperature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerabsorptionindirect
        """

class CondenserLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        condenser_equipment_operation_scheme_name: str,
        condenser_loop_temperature_setpoint_node_name: str,
        maximum_loop_temperature: float,
        minimum_loop_temperature: float,
        maximum_loop_flow_rate: float | Literal["Autosize"],
        condenser_side_inlet_node_name: str,
        condenser_side_outlet_node_name: str,
        condenser_side_branch_list_name: str,
        condenser_side_connector_list_name: str,
        demand_side_inlet_node_name: str,
        demand_side_outlet_node_name: str,
        condenser_demand_side_branch_list_name: str,
        condenser_demand_side_connector_list_name: str,
        fluid_type: Literal["UserDefinedFluidType", "Water"] | None = "Water",
        user_defined_fluid_type: str | None = ...,
        minimum_loop_flow_rate: float | None = 0,
        condenser_loop_volume: float | Literal["Autocalculate"] | None = "Autocalculate",
        load_distribution_scheme: Literal[
            "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
        pressure_simulation_type: Literal["LoopFlowCorrection", "None", "PumpPowerCorrection"] | None = "None",
        loop_circulation_time: float | None = 2,
    ) -> None:
        """Create a new ``CondenserLoop`` and add it to the document.

        Defines a central plant condenser loop. CondenserLoop and PlantLoop are nearly identical except some components and operation schemes are applicable to only one loop type or the other.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-loops/#condenserloop
        """

class GeneratorMicroTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_electrical_power_output: float,
        reference_electrical_efficiency_using_lower_heating_value: float,
        electrical_power_function_of_temperature_and_elevation_curve_name: str,
        electrical_efficiency_function_of_temperature_curve_name: str,
        electrical_efficiency_function_of_part_load_ratio_curve_name: str,
        minimum_full_load_electrical_power_output: float | None = 0,
        maximum_full_load_electrical_power_output: float | None = ...,
        reference_combustion_air_inlet_temperature: float | None = 15,
        reference_combustion_air_inlet_humidity_ratio: float | None = 0.00638,
        reference_elevation: float | None = 0,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "NaturalGas",
        fuel_higher_heating_value: float | None = 50000,
        fuel_lower_heating_value: float | None = 45450,
        standby_power: float | None = 0,
        ancillary_power: float | None = 0,
        ancillary_power_function_of_fuel_input_curve_name: str | None = ...,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        reference_thermal_efficiency_using_lower_heat_value: float | None = 0,
        reference_inlet_water_temperature: float | None = ...,
        heat_recovery_water_flow_operating_mode: Literal["InternalControl", "PlantControl"] | None = "PlantControl",
        reference_heat_recovery_water_flow_rate: float | None = ...,
        heat_recovery_water_flow_rate_function_of_temperature_and_power_curve_name: str | None = ...,
        thermal_efficiency_function_of_temperature_and_elevation_curve_name: str | None = ...,
        heat_recovery_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        heat_recovery_rate_function_of_inlet_water_temperature_curve_name: str | None = ...,
        heat_recovery_rate_function_of_water_flow_rate_curve_name: str | None = ...,
        minimum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_temperature: float | None = ...,
        combustion_air_inlet_node_name: str | None = ...,
        combustion_air_outlet_node_name: str | None = ...,
        reference_exhaust_air_mass_flow_rate: float | None = ...,
        exhaust_air_flow_rate_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_flow_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        nominal_exhaust_air_outlet_temperature: float | None = ...,
        exhaust_air_temperature_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_temperature_function_of_part_load_ratio_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:MicroTurbine`` and add it to the document.

        MicroTurbine generators are small combustion turbines (e.g., 25kW to 500kW). The model calculates electrical power output, fuel use, standby and ancillary power. Energy recovery from exhaust air can be used to heat water.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatormicroturbine
        """
