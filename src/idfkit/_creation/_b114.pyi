"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class SimulationControl:
    def __call__(
        self,
        /,
        *,
        do_zone_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_system_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_plant_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        run_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "Yes",
        run_simulation_for_weather_file_run_periods: Literal["", "No", "Yes"] | None = "Yes",
        do_hvac_sizing_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "No",
        maximum_number_of_hvac_sizing_simulation_passes: int | None = 1,
    ) -> None:
        """Create a new ``SimulationControl`` and add it to the document.

        Note that the following 3 fields are related to the Sizing:Zone, Sizing:System, and Sizing:Plant objects. Having these fields set to Yes but no corresponding Sizing object will not cause the sizing to be done. However, having any of these fields set to No, the corresponding Sizing object is ignored. Note also, if you want to do system sizing, you must also do zone sizing in the same run or an error will result.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#simulationcontrol
        """

class ZoneAirMassFlowConservation:
    def __call__(
        self,
        /,
        *,
        adjust_zone_mixing_and_return_for_air_mass_flow_balance: Literal[
            "", "AdjustMixingOnly", "AdjustMixingThenReturn", "AdjustReturnOnly", "AdjustReturnThenMixing", "None"
        ]
        | None = "None",
        infiltration_balancing_method: Literal["", "AddInfiltrationFlow", "AdjustInfiltrationFlow", "None"]
        | None = "AddInfiltrationFlow",
        infiltration_balancing_zones: Literal["", "AllZones", "MixingSourceZonesOnly"] | None = "MixingSourceZonesOnly",
    ) -> None:
        """Create a new ``ZoneAirMassFlowConservation`` and add it to the document.

        Enforces the zone air mass flow balance by either adjusting zone mixing object flow only, adjusting zone total return flow only, zone mixing and the zone total return flows, or adjusting the zone total return and zone mixing object flows. Zone infiltration flow air flow is increased or decreased depending user selection in the infiltration treatment method. If either of zone mixing or zone return flow adjusting methods or infiltration is active, then the zone air mass flow balance calculation will attempt to enforce conservation of mass for each zone. If flow balancing method is 'None' and infiltration is 'None', then the zone air mass flow calculation defaults to assume self-balanced simple flow mixing and infiltration objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneairmassflowconservation
        """

class ScheduleFileShading:
    def __call__(self, /, *, file_name: str) -> None:
        """Create a new ``Schedule:File:Shading`` and add it to the document.

        A Schedule:File:Shading points to a CSV file that has 8760-8784 hours of sunlit fraction data for all or some of the exterior surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#schedulefileshading
        """

class GroundHeatTransferBasementYFACE:
    def __call__(self, /) -> None:
        """Create a new ``GroundHeatTransfer:Basement:YFACE`` and add it to the document.

        This is only needed when using manual gridding (not recommended) YFACE: Y Direction cell face coordinates: m

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementyface
        """

class ConnectorList:
    def __call__(
        self,
        name: str,
        /,
        *,
        connector_1_object_type: Literal["Connector:Mixer", "Connector:Splitter"],
        connector_1_name: str,
        connector_2_object_type: Literal["Connector:Mixer", "Connector:Splitter"] | None = ...,
        connector_2_name: str | None = ...,
    ) -> None:
        """Create a new ``ConnectorList`` and add it to the document.

        only two connectors allowed per loop if two entered, one must be Connector:Splitter and one must be Connector:Mixer

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#connectorlist
        """

class ChillerConstantCOP:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
    ) -> None:
        """Create a new ``Chiller:ConstantCOP`` and add it to the document.

        This constant COP chiller model provides a means of quickly specifying a Chiller where performance data is not available.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerconstantcop
        """

class ExternalInterfaceFunctionalMockupUnitImportToActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        fmu_file_name: str,
        fmu_instance_name: str,
        fmu_variable_name: str,
        initial_value: float,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitImport:To:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitimporttoactuator
        """

class CurveSigmoid:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        coefficient5_c5: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Sigmoid`` and add it to the document.

        Sigmoid curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1+C2/[1+exp((C3-x)/C4)]**C5

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvesigmoid
        """

class OutputMeterMeterFileOnly:
    def __call__(
        self,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
    ) -> None:
        """Create a new ``Output:Meter:MeterFileOnly`` and add it to the document.

        Each Output:Meter:MeterFileOnly command picks meters to be put only onto meter file (.mtr). Not all meters are reported in every simulation. A list of meters that can be reported a list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-output-reporting/#outputmetermeterfileonly
        """
