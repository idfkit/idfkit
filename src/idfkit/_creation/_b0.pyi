"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyZoneAirHeatBalanceAlgorithm:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal["", "AnalyticalSolution", "EulerMethod", "ThirdOrderBackwardDifference"]
        | None = "ThirdOrderBackwardDifference",
    ) -> None:
        """Create a new ``ZoneAirHeatBalanceAlgorithm`` and add it to the document.

        Controls the zone/space air heat balance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#zoneairheatbalancealgorithm
        """

class FloorAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#flooradiabatic
        """

class SurfacePropertyHeatTransferAlgorithmSurfaceList:
    def __call__(
        self,
        name: str,
        /,
        *,
        algorithm: Literal[
            "",
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
        surface: Sequence[
            _g.SurfacePropertyHeatTransferAlgorithmSurfaceListSurfaceItem
            | _g.SurfacePropertyHeatTransferAlgorithmSurfaceListSurfaceGroup
        ] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:HeatTransferAlgorithm:SurfaceList`` and add it to the document.

        Determines which Heat Balance Algorithm will be used for a list of surfaces Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage: CondFD (Conduction Finite Difference) Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheattransferalgorithmsurfacelist
        """

class SurfacePropertyOtherSideCoefficients:
    def __call__(
        self,
        name: str,
        /,
        *,
        combined_convective_radiative_film_coefficient: float,
        constant_temperature: float | None = 0,
        constant_temperature_coefficient: float | None = 1,
        external_dry_bulb_temperature_coefficient: float | None = 0,
        ground_temperature_coefficient: float | None = 0,
        wind_speed_coefficient: float | None = 0,
        zone_air_temperature_coefficient: float | None = 0,
        constant_temperature_schedule_name: str | None = ...,
        sinusoidal_variation_of_constant_temperature_coefficient: Literal["", "No", "Yes"] | None = "No",
        period_of_sinusoidal_variation: float | None = 24,
        previous_other_side_temperature_coefficient: float | None = 0,
        minimum_other_side_temperature_limit: float | None = ...,
        maximum_other_side_temperature_limit: float | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:OtherSideCoefficients`` and add it to the document.

        This object sets the other side conditions for a surface in a variety of ways.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyothersidecoefficients
        """

class GroundHeatTransferBasementSimParameters:
    def __call__(
        self,
        /,
        *,
        f_multiplier_for_the_adi_solution: float | None = ...,
        iyrs_maximum_number_of_yearly_iterations_: float | None = 15,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:SimParameters`` and add it to the document.

        Specifies certain parameters that control the Basement preprocessor ground heat transfer simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementsimparameters
        """

class OtherEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
    ) -> None:
        """Create a new ``OtherEquipment:Definition`` and add it to the document.

        Defines the physical characteristics (design level and heat gain fractions) for 'other' equipment. Referenced by one or more OtherEquipment:Instance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#otherequipmentdefinition
        """

class AirTerminalSingleDuctVAVReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        damper_heating_action: Literal["", "Normal", "Reverse", "ReverseWithLimits"] | None = "ReverseWithLimits",
        maximum_flow_per_zone_floor_area_during_reheat: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_flow_fraction_during_reheat: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_reheat_air_temperature: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductvavreheat
        """

class PlantEquipmentOperationOutdoorDewpointDifference:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature_node_name: str,
        dewpoint_temperature_difference_range_1_lower_limit: float,
        dewpoint_temperature_difference_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        dewpoint_temperature_difference_range_2_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_3_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_4_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_5_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_6_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_7_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_8_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_9_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        dewpoint_temperature_difference_range_10_lower_limit: float | None = ...,
        dewpoint_temperature_difference_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:OutdoorDewpointDifference`` and add it to the document.

        Plant equipment operation scheme for outdoor dewpoint temperature difference operation. Specifies one or more groups of equipment which are available to operate for successive ranges based the difference between a reference node temperature and the outdoor dewpoint temperature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationoutdoordewpointdifference
        """

class EnergyManagementSystemTrendVariable:
    def __call__(self, name: str, /, *, ems_variable_name: str, number_of_timesteps_to_be_logged: int) -> None:
        """Create a new ``EnergyManagementSystem:TrendVariable`` and add it to the document.

        This object sets up an EMS trend variable from an Erl variable A trend variable logs values across timesteps

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemtrendvariable
        """

class AvailabilityManagerOptimumStart:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_type: Literal["", "ControlZone", "MaximumofZoneList", "StayOff"] | None = "ControlZone",
        control_zone_name: str | None = ...,
        zone_list_name: str | None = ...,
        maximum_value_for_optimum_start_time: float | None = 6,
        control_algorithm: Literal[
            "", "AdaptiveASHRAE", "AdaptiveTemperatureGradient", "ConstantStartTime", "ConstantTemperatureGradient"
        ]
        | None = "AdaptiveASHRAE",
        constant_temperature_gradient_during_cooling: float | None = ...,
        constant_temperature_gradient_during_heating: float | None = ...,
        initial_temperature_gradient_during_cooling: float | None = ...,
        initial_temperature_gradient_during_heating: float | None = ...,
        constant_start_time: float | None = ...,
        number_of_previous_days: int | None = 2,
    ) -> None:
        """Create a new ``AvailabilityManager:OptimumStart`` and add it to the document.

        Determines the optimal start of HVAC systems before occupancy.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanageroptimumstart
        """

class DemandManagerElectricEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        equipment: Sequence[
            _g.DemandManagerElectricEquipmentEquipmentItem | _g.DemandManagerElectricEquipmentEquipmentGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManager:ElectricEquipment`` and add it to the document.

        used for demand limiting ElectricEquipment objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerelectricequipment
        """

class GeneratorPhotovoltaic:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        photovoltaic_performance_object_type: Literal[
            "PhotovoltaicPerformance:EquivalentOne-Diode",
            "PhotovoltaicPerformance:Sandia",
            "PhotovoltaicPerformance:Simple",
        ]
        | None = ...,
        module_performance_name: str | None = ...,
        heat_transfer_integration_mode: Literal[
            "",
            "Decoupled",
            "DecoupledUllebergDynamic",
            "IntegratedExteriorVentedCavity",
            "IntegratedSurfaceOutsideFace",
            "IntegratedTranspiredCollector",
            "PhotovoltaicThermalSolarCollector",
        ]
        | None = "Decoupled",
        number_of_series_strings_in_parallel: float | None = 1,
        number_of_modules_in_series: float | None = 1,
    ) -> None:
        """Create a new ``Generator:Photovoltaic`` and add it to the document.

        Describes an array of photovoltaic (PV) modules. A series of different PV arrays can be connected to a single electric load center (and inverter) by listing them all in an ElectricLoadCenter:Generator object. PV performance is taken from the referenced PhotovoltaicPerformance:* object. Array tilt, azimuth, and gross area are taken from the referenced building surface or shading surface. The array surface participates normally in all shading calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#generatorphotovoltaic
        """

class CurveQuadratic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Quadratic`` and add it to the document.

        Quadratic curve with one independent variable. Input for a quadratic curve consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x + C3*x**2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvequadratic
        """

class TableLookup:
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
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: Sequence[_g.TableLookupValuesItem | _g.TableLookupValuesGroup] = ...,
    ) -> None:
        """Create a new ``Table:Lookup`` and add it to the document.

        Lookup tables are used in place of curves and can represent any number of independent variables (defined as Table:IndependentVariable objects in a Table:IndependentVariableList). Output values are interpolated within the bounds defined by each independent variable and extrapolated beyond the bounds according to the interpolation/extrapolation methods defined by each independent variable.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-tables/#tablelookup
        """
