"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class SurfacePropertyOtherSideConditionsModel:
    def __call__(
        self,
        name: str,
        /,
        *,
        type_of_modeling: Literal[
            "",
            "ConvectiveUnderwater",
            "GapConvectionRadiation",
            "GroundCoupledSurface",
            "UndergroundPipingSystemSurface",
        ]
        | None = "GapConvectionRadiation",
    ) -> None:
        """Create a new ``SurfaceProperty:OtherSideConditionsModel`` and add it to the document.

        This object sets up modifying the other side conditions for a surface from other model results.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyothersideconditionsmodel
        """

class AnyZoneInfiltrationEffectiveLeakageArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        effective_air_leakage_area: float,
        stack_coefficient: float,
        wind_coefficient: float,
    ) -> None:
        """Create a new ``ZoneInfiltration:EffectiveLeakageArea`` and add it to the document.

        Infiltration is specified as effective leakage area at 4 Pa, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * (AL /1000) SQRT(Cs*|(Tzone-Todb)| + Cw*WindSpd**2 ) If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneinfiltrationeffectiveleakagearea
        """

class ZoneCrossMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        source_zone_or_space_name: str,
        schedule_name: str | None = ...,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_receiving_temperature_schedule_name: str | None = ...,
        maximum_receiving_temperature_schedule_name: str | None = ...,
        minimum_source_temperature_schedule_name: str | None = ...,
        maximum_source_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneCrossMixing`` and add it to the document.

        ZoneCrossMixing exchanges an equal amount of air between two zones or spaces. Note that this statement affects the energy balance of both zones or spaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonecrossmixing
        """

class AnyAirflowNetworkDistributionNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_name_or_node_name: str | None = ...,
        component_object_type_or_node_type: Literal[
            "",
            "AirLoopHVAC:OutdoorAirSystem",
            "AirLoopHVAC:ZoneMixer",
            "AirLoopHVAC:ZoneSplitter",
            "OAMixerOutdoorAirStreamNode",
            "Other",
            "OutdoorAir:Node",
            "OutdoorAir:NodeList",
        ]
        | None = "Other",
        node_height: float | None = 0,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Node`` and add it to the document.

        This object represents an air distribution node in the AirflowNetwork model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributionnode
        """

class AirTerminalSingleDuctVAVReheatVariableSpeedFan:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_cooling_air_flow_rate: float | Literal["Autosize"],
        maximum_heating_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        fan_object_type: Literal["Fan:SystemModel", "Fan:VariableVolume"],
        fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with reheat coil (hot water, electric, gas, or steam) and variable-speed fan. These units are usually employed in underfloor air distribution (UFAD) systems where the air is supplied at low static pressure through an underfloor plenum. The fan is used to control the flow of conditioned air that enters the space.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductvavreheatvariablespeedfan
        """

class AirTerminalSingleDuctConstantVolumeCooledBeam:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooled_beam_type: Literal["Active", "Passive"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_total_chilled_water_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        number_of_beams: int | Literal["", "Autosize"] | None = "Autosize",
        beam_length: float | Literal["", "Autosize"] | None = "Autosize",
        design_inlet_water_temperature: float | None = 15,
        design_outlet_water_temperature: float | None = 17,
        coil_surface_area_per_coil_length: float | None = 5.422,
        model_parameter_a: float | None = 15.3,
        model_parameter_n1: float | None = 0,
        model_parameter_n2: float | None = 0.84,
        model_parameter_n3: float | None = 0.12,
        model_parameter_a0: float | None = 0.171,
        model_parameter_k1: float | None = 0.0057,
        model_parameter_n: float | None = 0.4,
        coefficient_of_induction_kin: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        leaving_pipe_inside_diameter: float | None = 0.0145,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:CooledBeam`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with cooled beam (active or passive).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumecooledbeam
        """

class AnyCoilCoolingDXCurveFitPerformance:
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitperformance
        """

class PipingSystemUndergroundDomain:
    def __call__(
        self,
        name: str,
        /,
        *,
        xmax: float,
        ymax: float,
        zmax: float,
        x_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        y_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        z_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        number_of_pipe_circuits_entered_for_this_domain: int,
        x_direction_mesh_density_parameter: int | None = 4,
        x_direction_geometric_coefficient: float | None = 1.3,
        y_direction_mesh_density_parameter: int | None = 4,
        y_direction_geometric_coefficient: float | None = 1.3,
        z_direction_mesh_density_parameter: int | None = 4,
        z_direction_geometric_coefficient: float | None = 1.3,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        this_domain_includes_basement_surface_interaction: Literal["", "No", "Yes"] | None = "No",
        width_of_basement_floor_in_ground_domain: float | None = ...,
        depth_of_basement_wall_in_ground_domain: float | None = ...,
        shift_pipe_x_coordinates_by_basement_width: Literal["No", "Yes"] | None = ...,
        name_of_basement_wall_boundary_condition_model: str | None = ...,
        name_of_basement_floor_boundary_condition_model: str | None = ...,
        convergence_criterion_for_the_outer_cartesian_domain_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_outer_cartesian_domain_iteration_loop: int | None = 500,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        pipe_circuits: Sequence[
            _g.PipingSystemUndergroundDomainPipeCircuitsItem | _g.PipingSystemUndergroundDomainPipeCircuitsGroup
        ] = ...,
    ) -> None:
        """Create a new ``PipingSystem:Underground:Domain`` and add it to the document.

        The ground domain object for underground piping system simulation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipingsystemundergrounddomain
        """

class ExternalInterfaceFunctionalMockupUnitExportFromVariable:
    def __call__(
        self, /, *, output_variable_index_key_name: str, output_variable_name: str, fmu_variable_name: str
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitExport:From:Variable`` and add it to the document.

        This object declares an FMU input variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitexportfromvariable
        """

class SetpointManagerScheduled:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal[
            "HumidityRatio",
            "MassFlowRate",
            "MaximumHumidityRatio",
            "MaximumMassFlowRate",
            "MaximumTemperature",
            "MinimumHumidityRatio",
            "MinimumMassFlowRate",
            "MinimumTemperature",
            "Temperature",
        ],
        schedule_name: str,
        setpoint_node_or_nodelist_name: str,
    ) -> None:
        """Create a new ``SetpointManager:Scheduled`` and add it to the document.

        The simplest Setpoint Manager simply uses a schedule to determine one or more setpoints. Values of the nodes are not used as input.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerscheduled
        """

class GeneratorInternalCombustionEngine:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_power_output: float | None = ...,
        electric_circuit_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        shaft_power_curve_name: str | None = ...,
        jacket_heat_recovery_curve_name: str | None = ...,
        lube_heat_recovery_curve_name: str | None = ...,
        total_exhaust_energy_curve_name: str | None = ...,
        exhaust_temperature_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        fuel_type: Literal[
            "", "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "Diesel",
        heat_recovery_maximum_temperature: float | None = 80,
    ) -> None:
        """Create a new ``Generator:InternalCombustionEngine`` and add it to the document.

        This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Engine performance curves are generated by fitting catalog data to second order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorinternalcombustionengine
        """

class CurveRectangularHyperbola2:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:RectangularHyperbola2`` and add it to the document.

        Rectangular hyperbola type 2 curve with one independent variable. Input consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = ((C1*x)/(C2+x))+(C3*x)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curverectangularhyperbola2
        """
