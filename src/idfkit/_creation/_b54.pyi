"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyMaterialPropertyHeatAndMoistureTransferSorptionIsotherm:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_isotherm_coordinates: int,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersorptionisotherm
        """

class MaterialPropertyHeatAndMoistureTransferSuction:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_suction_points: int,
        moisture_content_1: float,
        liquid_transport_coefficient_1: float,
        moisture_content_2: float | None = ...,
        liquid_transport_coefficient_2: float | None = ...,
        moisture_content_3: float | None = ...,
        liquid_transport_coefficient_3: float | None = ...,
        moisture_content_4: float | None = ...,
        liquid_transport_coefficient_4: float | None = ...,
        moisture_content_5: float | None = ...,
        liquid_transport_coefficient_5: float | None = ...,
        moisture_content_6: float | None = ...,
        liquid_transport_coefficient_6: float | None = ...,
        moisture_content_7: float | None = ...,
        liquid_transport_coefficient_7: float | None = ...,
        moisture_content_8: float | None = ...,
        liquid_transport_coefficient_8: float | None = ...,
        moisture_content_9: float | None = ...,
        liquid_transport_coefficient_9: float | None = ...,
        moisture_content_10: float | None = ...,
        liquid_transport_coefficient_10: float | None = ...,
        moisture_content_11: float | None = ...,
        liquid_transport_coefficient_11: float | None = ...,
        moisture_content_12: float | None = ...,
        liquid_transport_coefficient_12: float | None = ...,
        moisture_content_13: float | None = ...,
        liquid_transport_coefficient_13: float | None = ...,
        moisture_content_14: float | None = ...,
        liquid_transport_coefficient_14: float | None = ...,
        moisture_content_15: float | None = ...,
        liquid_transport_coefficient_15: float | None = ...,
        moisture_content_16: float | None = ...,
        liquid_transport_coefficient_16: float | None = ...,
        moisture_content_17: float | None = ...,
        liquid_transport_coefficient_17: float | None = ...,
        moisture_content_18: float | None = ...,
        liquid_transport_coefficient_18: float | None = ...,
        moisture_content_19: float | None = ...,
        liquid_transport_coefficient_19: float | None = ...,
        moisture_content_20: float | None = ...,
        liquid_transport_coefficient_20: float | None = ...,
        moisture_content_21: float | None = ...,
        liquid_transport_coefficient_21: float | None = ...,
        moisture_content_22: float | None = ...,
        liquid_transport_coefficient_22: float | None = ...,
        moisture_content_23: float | None = ...,
        liquid_transport_coefficient_23: float | None = ...,
        moisture_content_24: float | None = ...,
        liquid_transport_coefficient_24: float | None = ...,
        moisture_content_25: float | None = ...,
        liquid_transport_coefficient_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Suction`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid suction transport coefficient and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersuction
        """

class SurfaceConstructionAssignments:
    def __call__(
        self,
        name: str,
        /,
        *,
        floor_construction_name: str | None = ...,
        wall_construction_name: str | None = ...,
        roof_ceiling_construction_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceConstructionAssignments`` and add it to the document.

        Defines construction assignments for the three opaque surface types (Floor, Wall, Roof/Ceiling) for a single boundary-condition category (exterior, interior, or ground-contact).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#surfaceconstructionassignments
        """

class LightsDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal["LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        return_air_fraction_calculated_from_plenum_temperature: Literal["No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
    ) -> None:
        """Create a new ``Lights:Definition`` and add it to the document.

        Defines the physical characteristics (design level and heat gain fractions) for lights. Referenced by one or more Lights:Instance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#lightsdefinition
        """

class CoilHeatingDXVariableRefrigerantFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_heating_capacity: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        coil_air_inlet_node: str,
        coil_air_outlet_node: str,
        heating_capacity_ratio_modifier_function_of_temperature_curve_name: str,
        heating_capacity_modifier_function_of_flow_fraction_curve_name: str,
        availability_schedule: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:VariableRefrigerantFlow`` and add it to the document.

        Variable refrigerant flow (VRF) direct expansion (DX) heating coil (air-to-air heat pump). Used with ZoneHVAC:TerminalUnit:VariableRefrigerantFlow. Condensing unit is modeled separately, see AirConditioner:VariableRefrigerantFlow.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxvariablerefrigerantflow
        """

class CoilWaterHeatingAirToWaterHeatPumpWrapped:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Wrapped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:WrappedCondenser system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpwrapped
        """

class AnyHeatPumpPlantLoopEIRCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        condenser_type: Literal["AirSource", "WaterSource"] | None = "WaterSource",
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = ...,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Cooling`` and add it to the document.

        An EIR formulated water to water heat pump model, cooling operation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpplantloopeircooling
        """

class PlantEquipmentOperationComponentSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        equipment_1_object_type: str,
        equipment_1_name: str,
        demand_calculation_1_node_name: str,
        setpoint_1_node_name: str,
        component_1_flow_rate: float | Literal["Autosize"],
        operation_1_type: Literal["Cooling", "Dual", "Heating"],
        equipment_2_object_type: str | None = ...,
        equipment_2_name: str | None = ...,
        demand_calculation_2_node_name: str | None = ...,
        setpoint_2_node_name: str | None = ...,
        component_2_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_2_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_3_object_type: str | None = ...,
        equipment_3_name: str | None = ...,
        demand_calculation_3_node_name: str | None = ...,
        setpoint_3_node_name: str | None = ...,
        component_3_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_3_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_4_object_type: str | None = ...,
        equipment_4_name: str | None = ...,
        demand_calculation_4_node_name: str | None = ...,
        setpoint_4_node_name: str | None = ...,
        component_4_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_4_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_5_object_type: str | None = ...,
        equipment_5_name: str | None = ...,
        demand_calculation_5_node_name: str | None = ...,
        setpoint_5_node_name: str | None = ...,
        component_5_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_5_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_6_object_type: str | None = ...,
        equipment_6_name: str | None = ...,
        demand_calculation_6_node_name: str | None = ...,
        setpoint_6_node_name: str | None = ...,
        component_6_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_6_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_7_object_type: str | None = ...,
        equipment_7_name: str | None = ...,
        demand_calculation_7_node_name: str | None = ...,
        setpoint_7_node_name: str | None = ...,
        component_7_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_7_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_8_object_type: str | None = ...,
        equipment_8_name: str | None = ...,
        demand_calculation_8_node_name: str | None = ...,
        setpoint_8_node_name: str | None = ...,
        component_8_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_8_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_9_object_type: str | None = ...,
        equipment_9_name: str | None = ...,
        demand_calculation_9_node_name: str | None = ...,
        setpoint_9_node_name: str | None = ...,
        component_9_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_9_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        equipment_10_object_type: str | None = ...,
        equipment_10_name: str | None = ...,
        demand_calculation_10_node_name: str | None = ...,
        setpoint_10_node_name: str | None = ...,
        component_10_flow_rate: float | Literal["Autosize"] | None = ...,
        operation_10_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ComponentSetpoint`` and add it to the document.

        Plant equipment operation scheme for component setpoint operation. Specifies one or pieces of equipment which are controlled to meet the temperature setpoint at the component outlet node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationcomponentsetpoint
        """

class FaultModelEnthalpySensorOffsetOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        enthalpy_sensor_offset: float | None = 0,
    ) -> None:
        """Create a new ``FaultModel:EnthalpySensorOffset:OutdoorAir`` and add it to the document.

        This object describes outdoor air enthalpy sensor offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelenthalpysensoroffsetoutdoorair
        """

class TableIndependentVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        interpolation_method: Literal["Cubic", "Linear"] | None = "Linear",
        extrapolation_method: Literal["Constant", "Linear"] | None = "Constant",
        minimum_value: float | None = ...,
        maximum_value: float | None = ...,
        normalization_reference_value: float | None = ...,
        unit_type: Literal["Angle", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: Sequence[_g.TableIndependentVariableValuesItem | _g.TableIndependentVariableValuesGroup] = ...,
    ) -> None:
        """Create a new ``Table:IndependentVariable`` and add it to the document.

        An independent variable representing a single dimension of a Table:Lookup object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-tables/#tableindependentvariable
        """
