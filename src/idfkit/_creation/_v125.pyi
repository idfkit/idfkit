"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class ZoneHVACForcedAirUserDefined_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: float,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_1_inlet_node_name: str | None = ...,
        plant_connection_1_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:ForcedAir:UserDefined`` and add it to the document.

        Defines a generic zone air unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-user-defined-hvac-and-plant-component/#zonehvacforcedairuserdefined
        """

class GroundHeatExchangerSystem_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        ground_thermal_conductivity: float,
        ground_thermal_heat_capacity: float,
        ghe_vertical_responsefactors_object_name: str | None = ...,
        ghe_vertical_array_object_name: str | None = ...,
        vertical_well_locations: Sequence[
            _g.GroundHeatExchangerSystemVerticalWellLocationsItem
            | _g.GroundHeatExchangerSystemVerticalWellLocationsGroup
        ] = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:System`` and add it to the document.

        Models vertical ground heat exchangers systems using the response factor approach developed by Eskilson. Response factors are calculated using a finite line source model assuming uniform heat flux at the borehole wall.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-condenser-equipment/#groundheatexchangersystem
        """

class ZoneVentilationDesignFlowRate_v22_2_to_v24_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str | None = ...,
        design_flow_rate_calculation_method: Literal["AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        ventilation_type: Literal["Balanced", "Exhaust", "Intake", "Natural"] | None = "Natural",
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

        Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.2/io-reference/overview/group-airflow/#zoneventilationdesignflowrate
        """

class ZoneHVACPackagedTerminalHeatPump_v24_1_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal["Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed"],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_control_set_to_low_speed: Literal["No", "Yes"] | None = "Yes",
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_convergence_tolerance: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalHeatPump`` and add it to the document.

        Packaged terminal heat pump (PTHP). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalheatpump
        """

class TableOneIndependentVariable_v9_0_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        curve_type: Literal["Cubic", "Linear", "Quadratic", "Quartic"] | None = ...,
        interpolation_method: Literal[
            "EvaluateCurveToLimits", "LagrangeInterpolationLinearExtrapolation", "LinearInterpolationOfTable"
        ]
        | None = ...,
        minimum_value_of_x: float | None = ...,
        maximum_value_of_x: float | None = ...,
        minimum_table_output: float | None = ...,
        maximum_table_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        normalization_reference: float | None = ...,
        values: Sequence[
            _vd.TableOneIndependentVariableValuesItem_v9_0_to_v9_1
            | _vd.TableOneIndependentVariableValuesGroup_v9_0_to_v9_1
        ] = ...,
    ) -> None:
        """Create a new ``Table:OneIndependentVariable`` and add it to the document.

        Allows entry of tabular data pairs as alternate input for performance curve objects. Performance curve objects can be created using these inputs. Linear Table Equation: Output = a + bX Linear solution requires a minimum of 2 data pairs Quadratic Table Equation: Output = a + b*X + c*X**2 Quadratic solution requires a minimum of 3 data pairs Cubic Table Equation: Output = a + b*X + c* X**2 + d*X**3 Cubic solution requires a minimum of 4 data pairs Quartic Table Equation: Output = a + b*X + c* X**2 + d*X**3 + e*X**4 Quartic solution requires a minimum of 5 data pairs Exponent Table Equation: Output = a + b*X**c Exponent solution requires a minimum of 4 data pairs
        """

class AirflowNetworkDistributionComponentOutdoorAirFlow_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:OutdoorAirFlow`` and add it to the document.

        This object includes the outdoor air flow rate set by the Controller:OutdoorAir object in the airflow network.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentoutdoorairflow
        """

class CoilWaterHeatingAirToWaterHeatPumpPumped_v8_9_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_water_pump_power: float | None = 0,
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Pumped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:PumpedCondenser system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumppumped
        """

class AirLoopHVACOutdoorAirSystem_v9_2_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_equipment_list_name: str,
        controller_list_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:OutdoorAirSystem`` and add it to the document.

        Outdoor air subsystem for an AirLoopHVAC. Includes an outdoor air mixing box and optional outdoor air conditioning equipment such as heat recovery, preheat, and precool coils. From the perspective of the primary air loop the outdoor air system is treated as a single component.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-air-distribution/#airloophvacoutdoorairsystem
        """
