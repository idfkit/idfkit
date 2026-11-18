"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnySurfacePropertyConvectionCoefficientsMultipleSurface:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficientsmultiplesurface
        """

class ExteriorLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_name: str,
        design_level: float,
        control_option: Literal["AstronomicalClock", "ScheduleNameOnly"] | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Exterior:Lights`` and add it to the document.

        only used for Meter type reporting, does not affect building loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-exterior-energy-use-equipment/#exteriorlights
        """

class ZoneHVACEnergyRecoveryVentilator:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_name: str,
        supply_air_flow_rate: float | Literal["Autosize"],
        exhaust_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_name: str,
        exhaust_air_fan_name: str,
        availability_schedule_name: str | None = ...,
        controller_name: str | None = ...,
        ventilation_rate_per_unit_floor_area: float | None = ...,
        ventilation_rate_per_occupant: float | None = ...,
        availability_manager_list_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EnergyRecoveryVentilator`` and add it to the document.

        This compound component models a stand-alone energy recovery ventilator (ERV) that conditions outdoor ventilation air and supplies that air directly to a zone. The ERV unit is modeled as a collection of components: air-to-air heat exchanger, supply air fan, exhaust air fan and an optional controller to avoid overheating of the supply air (economizer or free cooling operation).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacenergyrecoveryventilator
        """

class NodeList:
    def __call__(self, name: str, /, *, nodes: Sequence[_g.NodeListNodesItem | _g.NodeListNodesGroup] = ...) -> None:
        """Create a new ``NodeList`` and add it to the document.

        This object is used in places where lists of nodes may be needed, e.g. ZoneHVAC:EquipmentConnections field Zone Air Inlet Node or NodeList Name

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#nodelist
        """

class HeatPumpAirToWaterFuelFiredHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        normalized_capacity_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_plr_curve_name: str,
        air_source_node_name: str | None = ...,
        companion_cooling_heat_pump_name: str | None = ...,
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
        end_use_subcategory: str | None = "General",
        nominal_heating_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 60,
        design_temperature_lift: float | Literal["Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["EnteringCondenser", "LeavingCondenser"]
        | None = "EnteringCondenser",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        defrost_control_type: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_operation_time_fraction: float | None = 0,
        fuel_energy_input_ratio_defrost_adjustment_curve_name: str | None = ...,
        resistive_defrost_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
        minimum_unloading_ratio: float | None = 0.25,
    ) -> None:
        """Create a new ``HeatPump:AirToWater:FuelFired:Heating`` and add it to the document.

        The object defines a fuel-fired absorption heat pump based on equation-fit models.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-heating-and-cooling-equipment/#heatpumpairtowaterfuelfiredheating
        """

class FluidCoolerTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_entering_water_temperature: float,
        design_entering_air_temperature: float,
        design_entering_air_wet_bulb_temperature: float,
        design_water_flow_rate: float | Literal["Autosize"],
        high_fan_speed_air_flow_rate: float | Literal["Autosize"],
        high_fan_speed_fan_power: float | Literal["Autosize"],
        low_fan_speed_air_flow_rate: float | Literal["Autocalculate"],
        low_fan_speed_fan_power: float | Literal["Autocalculate"],
        performance_input_method: Literal["NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "NominalCapacity",
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        high_speed_nominal_capacity: float | None = ...,
        low_speed_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_nominal_capacity_sizing_factor: float | None = 0.5,
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        outdoor_air_inlet_node_name: str | None = ...,
    ) -> None:
        """Create a new ``FluidCooler:TwoSpeed`` and add it to the document.

        The fluid cooler is modeled as a cross flow heat exchanger (both streams unmixed) with two-speed fans (induced draft configuration).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#fluidcoolertwospeed
        """

class CurveBiquadratic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_y: float,
        coefficient5_y_2: float,
        coefficient6_x_y: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Biquadratic`` and add it to the document.

        Quadratic curve with two independent variables. Input consists of the curve name, the six coefficients, and min and max values for each of the independent variables. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x + C3*x**2 + C4*y + C5*y**2 + C6*x*y

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvebiquadratic
        """
