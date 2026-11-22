"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyWindowPropertyFrameAndDivider:
    def __call__(
        self,
        name: str,
        /,
        *,
        frame_width: float | None = 0,
        frame_outside_projection: float | None = 0,
        frame_inside_projection: float | None = 0,
        frame_conductance: float | None = ...,
        ratio_of_frame_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        frame_solar_absorptance: float | None = 0.7,
        frame_visible_absorptance: float | None = 0.7,
        frame_thermal_hemispherical_emissivity: float | None = 0.9,
        divider_type: Literal["DividedLite", "Suspended"] | None = "DividedLite",
        divider_width: float | None = 0,
        number_of_horizontal_dividers: int | None = 0,
        number_of_vertical_dividers: int | None = 0,
        divider_outside_projection: float | None = 0,
        divider_inside_projection: float | None = 0,
        divider_conductance: float | None = 0,
        ratio_of_divider_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        divider_solar_absorptance: float | None = 0,
        divider_visible_absorptance: float | None = 0,
        divider_thermal_hemispherical_emissivity: float | None = 0.9,
        outside_reveal_solar_absorptance: float | None = 0,
        inside_sill_depth: float | None = 0,
        inside_sill_solar_absorptance: float | None = 0,
        inside_reveal_depth: float | None = 0,
        inside_reveal_solar_absorptance: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowProperty:FrameAndDivider`` and add it to the document.

        Specifies the dimensions of a window frame, dividers, and inside reveal surfaces. Referenced by the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertyframeanddivider
        """

class DuctLossConduction:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_name: str,
        airflownetwork_distribution_linkage_name: str,
        environment_type: Literal["Schedule", "Zone"] | None = "Zone",
        ambient_zone_name: str | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_humidity_ratio_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Duct:Loss:Conduction`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#ductlossconduction
        """

class ZoneControlThermostatStagedDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        number_of_heating_stages: int,
        stage_1_heating_temperature_offset: float,
        number_of_cooling_stages: int,
        stage_1_cooling_temperature_offset: float,
        heating_temperature_setpoint_schedule_name: str | None = ...,
        heating_throttling_temperature_range: float | None = 1.1,
        stage_2_heating_temperature_offset: float | None = ...,
        stage_3_heating_temperature_offset: float | None = ...,
        stage_4_heating_temperature_offset: float | None = ...,
        cooling_temperature_setpoint_base_schedule_name: str | None = ...,
        cooling_throttling_temperature_range: float | None = 1.1,
        stage_2_cooling_temperature_offset: float | None = ...,
        stage_3_cooling_temperature_offset: float | None = ...,
        stage_4_cooling_temperature_offset: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat:StagedDualSetpoint`` and add it to the document.

        Define the Thermostat StagedDualSetpoint settings for a zone or list of zones. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostatstageddualsetpoint
        """

class AnyChillerElectric:
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
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
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
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
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
        validate: bool = True,
    ) -> None:
        """Create a new ``Chiller:Electric`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#chillerelectric
        """

class EnergyManagementSystemInternalVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        internal_data_type: str,
        internal_data_index_key_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``EnergyManagementSystem:InternalVariable`` and add it to the document.

        Declares EMS variable as an internal data variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsysteminternalvariable
        """

class GeneratorFuelCellElectricalStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        choice_of_model: Literal["SimpleEfficiencyWithConstraints"] | None = ...,
        nominal_charging_energetic_efficiency: float | None = ...,
        nominal_discharging_energetic_efficiency: float | None = ...,
        simple_maximum_capacity: float | None = ...,
        simple_maximum_power_draw: float | None = ...,
        simple_maximum_power_store: float | None = ...,
        initial_charge_state: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Generator:FuelCell:ElectricalStorage`` and add it to the document.

        Used to describe the electrical storage subsystem for a fuel cell power generator. The electrical storage model is a very simple 'constrained bucket' model. Note that this electrical storage is embedded within the FC device.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellelectricalstorage
        """

class WaterUseWell:
    def __call__(
        self,
        name: str,
        /,
        *,
        storage_tank_name: str,
        pump_depth: float | None = ...,
        pump_rated_flow_rate: float | None = ...,
        pump_rated_head: float | None = ...,
        pump_rated_power_consumption: float | None = ...,
        pump_efficiency: float | None = ...,
        well_recovery_rate: float | None = ...,
        nominal_well_storage_volume: float | None = ...,
        water_table_depth_mode: Literal["Constant", "Scheduled"] | None = ...,
        water_table_depth: float | None = ...,
        water_table_depth_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WaterUse:Well`` and add it to the document.

        Simulates on-site water supply from a well. Well water is pumped out of the ground into a WaterUse:Storage. The operation of the ground water well is controlled by the associated WaterUse:Storage which is assumed to be operated as a vented cistern with no pressure tank.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-systems/#waterusewell
        """

class FaultModelFoulingChiller:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_object_type: Literal[
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
        ],
        chiller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        fouling_factor: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``FaultModel:Fouling:Chiller`` and add it to the document.

        This object describes the fouling fault of chillers with water-cooled condensers

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelfoulingchiller
        """

class MeterCustom:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ]
        | None = ...,
        variable_details: Sequence[_g.MeterCustomVariableDetailsItem | _g.MeterCustomVariableDetailsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Meter:Custom`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:Custom cannot reference another Meter:Custom or a Meter:CustomDecrement.

        ``variable_details`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Meter:Custom"].add(
            "Meter Custom 1",
            variable_details=[
                {"key_name": "Key 1", "output_variable_or_meter_name": "Output Variable or Meter 1"},
                {"key_name": "Key 2", "output_variable_or_meter_name": "Output Variable or Meter 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#metercustom
        """
