"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyBuildingSurfaceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Ceiling", "Floor", "Roof", "Wall"],
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
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
        sun_exposure: Literal["NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.BuildingSurfaceDetailedVerticesItem | _g.BuildingSurfaceDetailedVerticesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``BuildingSurface:Detailed`` and add it to the document.

        Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors.

        ``vertices`` takes the extensible groups in order, one dict per group:

        ```python
        doc["BuildingSurface:Detailed"].add(
            "BuildingSurface Detailed 1",
            surface_type="Wall",
            construction_name="Construction 1",
            zone_name="Zone 1",
            outside_boundary_condition="Outdoors",
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 10.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#buildingsurfacedetailed
        """

class AnyGlazedDoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``GlazedDoor`` and add it to the document.

        Allows for simplified entry of glass Doors.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#glazeddoor
        """

class FoundationKiva:
    def __call__(
        self,
        name: str,
        /,
        *,
        initial_indoor_air_temperature: float | None = ...,
        interior_horizontal_insulation_material_name: str | None = ...,
        interior_horizontal_insulation_depth: float | None = 0,
        interior_horizontal_insulation_width: float | None = ...,
        interior_vertical_insulation_material_name: str | None = ...,
        interior_vertical_insulation_depth: float | None = ...,
        exterior_horizontal_insulation_material_name: str | None = ...,
        exterior_horizontal_insulation_depth: float | None = ...,
        exterior_horizontal_insulation_width: float | None = 0,
        exterior_vertical_insulation_material_name: str | None = ...,
        exterior_vertical_insulation_depth: float | None = ...,
        wall_height_above_grade: float | None = 0.2,
        wall_depth_below_slab: float | None = 0,
        footing_wall_construction_name: str | None = ...,
        footing_material_name: str | None = ...,
        footing_depth: float | None = 0.3,
        blocks: Sequence[_g.FoundationKivaBlocksItem | _g.FoundationKivaBlocksGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Foundation:Kiva`` and add it to the document.

        Refined definition of the foundation surface construction used to inform two-dimensional heat transfer calculated using the Kiva ground heat transfer methodology.

        ``blocks`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Foundation:Kiva"].add(
            "Foundation Kiva 1",
            blocks=[
                {
                    "custom_block_material_name": "Custom Block Material 1",
                    "custom_block_depth": 1.0,
                    "custom_block_x_position": 0.0,
                    "custom_block_z_position": 0.0,
                },
                {
                    "custom_block_material_name": "Custom Block Material 2",
                    "custom_block_depth": 1.0,
                    "custom_block_x_position": 0.0,
                    "custom_block_z_position": 0.0,
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#foundationkiva
        """

class HVACTemplateZoneBaseboardHeat:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater"] | None = "HotWater",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        dedicated_outdoor_air_system_name: str | None = ...,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:BaseboardHeat`` and add it to the document.

        Zone baseboard heating system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonebaseboardheat
        """

class AnyCoilWaterHeatingAirToWaterHeatPumpVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        rated_water_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_reference_unit_water_pump_input_power_at_rated_conditions: float,
        speed_1_total_wh_capacity_function_of_temperature_curve_name: str,
        speed_1_total_wh_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_wh_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_cop_function_of_temperature_curve_name: str,
        speed_1_cop_function_of_air_flow_fraction_curve_name: str,
        speed_1_cop_function_of_water_flow_fraction_curve_name: str,
        number_of_speeds: int | None = 1,
        nominal_speed_level: int | None = 1,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["No", "Yes"] | None = "No",
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        part_load_fraction_correlation_curve_name: str | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_2_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_temperature_curve_name: str | None = ...,
        speed_2_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_3_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_temperature_curve_name: str | None = ...,
        speed_3_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_4_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_temperature_curve_name: str | None = ...,
        speed_4_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_5_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_temperature_curve_name: str | None = ...,
        speed_5_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_6_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_temperature_curve_name: str | None = ...,
        speed_6_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_7_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_temperature_curve_name: str | None = ...,
        speed_7_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_8_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_temperature_curve_name: str | None = ...,
        speed_8_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_9_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_temperature_curve_name: str | None = ...,
        speed_9_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_10_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_temperature_curve_name: str | None = ...,
        speed_10_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed`` and add it to the document.

        variable-speed Heat pump water heater (VSHPWH) heating coil, air-to-water direct-expansion (DX) system which includes a variable-speed water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump system.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpvariablespeed
        """

class ZoneTerminalUnitList:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_terminal_unit_list_name: str,
        terminal_units: Sequence[
            _g.ZoneTerminalUnitListTerminalUnitsItem | _g.ZoneTerminalUnitListTerminalUnitsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneTerminalUnitList`` and add it to the document.

        List of variable refrigerant flow (VRF) terminal units served by a given VRF condensing unit. See ZoneHVAC:TerminalUnit:VariableRefrigerantFlow and AirConditioner:VariableRefrigerantFlow.

        ``terminal_units`` takes the extensible groups in order, one dict per group:

        ```python
        doc["ZoneTerminalUnitList"].add(
            zone_terminal_unit_list_name="Zone Terminal Unit List 1",
            terminal_units=[
                {"zone_terminal_unit_name": "Zone Terminal Unit 1"},
                {"zone_terminal_unit_name": "Zone Terminal Unit 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-variable-refrigerant-flow-equipment/#zoneterminalunitlist
        """

class AvailabilityManagerAssignmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        managers: Sequence[
            _g.AvailabilityManagerAssignmentListManagersItem | _g.AvailabilityManagerAssignmentListManagersGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AvailabilityManagerAssignmentList`` and add it to the document.

        Defines the applicable managers used for an AirLoopHVAC or PlantLoop. The priority of availability managers is based on a set of rules and are specific to the type of loop. The output from each availability manager is an availability status flag: NoAction, ForceOff, CycleOn, or CycleOnZoneFansOnly (used only for air loops).

        ``managers`` takes the extensible groups in order, one dict per group:

        ```python
        doc["AvailabilityManagerAssignmentList"].add(
            "AvailabilityManagerAssignmentList 1",
            managers=[
                {
                    "availability_manager_object_type": "AvailabilityManager:DifferentialThermostat",
                    "availability_manager_name": "Availability Manager 1",
                },
                {
                    "availability_manager_object_type": "AvailabilityManager:HighTemperatureTurnOff",
                    "availability_manager_name": "Availability Manager 2",
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#availabilitymanagerassignmentlist
        """

class ElectricLoadCenterStorageBattery:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        number_of_battery_modules_in_parallel: int | None = 1,
        number_of_battery_modules_in_series: int | None = 1,
        maximum_module_capacity: float | None = ...,
        initial_fractional_state_of_charge: float | None = 1,
        fraction_of_available_charge_capacity: float | None = ...,
        change_rate_from_bound_charge_to_available_charge: float | None = ...,
        fully_charged_module_open_circuit_voltage: float | None = ...,
        fully_discharged_module_open_circuit_voltage: float | None = ...,
        voltage_change_curve_name_for_charging: str | None = ...,
        voltage_change_curve_name_for_discharging: str | None = ...,
        module_internal_electrical_resistance: float | None = ...,
        maximum_module_discharging_current: float | None = ...,
        module_cut_off_voltage: float | None = ...,
        module_charge_rate_limit: float | None = 1,
        battery_life_calculation: Literal["No", "Yes"] | None = "No",
        number_of_cycle_bins: int | None = 10,
        battery_life_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Battery`` and add it to the document.

        Uses the kinetic battery model (KiBaM) to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstoragebattery
        """

class CurrencyType:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        monetary_unit: Literal[
            "AFN",
            "ALL",
            "ANG",
            "ARS",
            "AUD",
            "AWG",
            "AZN",
            "BAM",
            "BBD",
            "BGN",
            "BMD",
            "BND",
            "BOB",
            "BRL",
            "BSD",
            "BWP",
            "BYR",
            "BZD",
            "CAD",
            "CHF",
            "CLP",
            "CNY",
            "COP",
            "CRC",
            "CUP",
            "CZK",
            "DKK",
            "DOP",
            "EEK",
            "EGP",
            "EUR",
            "FJD",
            "GBP",
            "GHC",
            "GIP",
            "GTQ",
            "GYD",
            "HKD",
            "HNL",
            "HRK",
            "HUF",
            "IDR",
            "ILS",
            "IMP",
            "INR",
            "IRR",
            "ISK",
            "JEP",
            "JMD",
            "JPY",
            "KGS",
            "KHR",
            "KPW",
            "KRW",
            "KYD",
            "KZT",
            "LAK",
            "LBP",
            "LKR",
            "LRD",
            "LTL",
            "LVL",
            "MKD",
            "MNT",
            "MUR",
            "MXN",
            "MYR",
            "MZN",
            "NAD",
            "NGN",
            "NIO",
            "NOK",
            "NPR",
            "NZD",
            "OMR",
            "PAB",
            "PEN",
            "PHP",
            "PKR",
            "PLN",
            "PYG",
            "QAR",
            "RON",
            "RSD",
            "RUB",
            "SAR",
            "SBD",
            "SCR",
            "SEK",
            "SGD",
            "SHP",
            "SOS",
            "SRD",
            "SVC",
            "SYP",
            "THB",
            "TRL",
            "TRY",
            "TTD",
            "TVD",
            "TWD",
            "UAH",
            "USD",
            "UYU",
            "UZS",
            "VEF",
            "VND",
            "XCD",
            "YER",
            "ZAR",
            "ZWD",
        ],
        validate: bool = True,
    ) -> None:
        """Create a new ``CurrencyType`` and add it to the document.

        If CurrencyType is not specified, it will default to USD and produce $ in the reports.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/currencytype/#currencytype
        """
